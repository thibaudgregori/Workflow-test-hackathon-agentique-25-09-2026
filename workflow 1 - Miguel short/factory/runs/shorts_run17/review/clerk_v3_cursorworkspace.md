# CLERK v3.1 — cursorworkspace (run 17) — INDEPENDENT VIEWER TEST

Judged 3 staged renders. Duration 21.56 s each, 1080x1920, 25 fps.

## STEP 1 — THE WATCHER'S CANDIDATES: THERE ARE NONE

`review/cands_cursorworkspace_split.json`, `..._cutout.json`, `..._whiteboard.json`
**do not exist**. No `cands_*.json` exists for ANY video in shorts_run17.
Per v3.1 the hole is reported, never backfilled: **all three renders were watched
by nothing**, and every row below is CLERK-ORIGINATED from my own decode.

Cause on record (`review/watcher_unavailable_cursorworkspace_cutout.md`): the Gemini
API project hit an account-level `429 RESOURCE_EXHAUSTED — monthly spending cap`;
the cutout watch exited 1 after 17.1 s. The same cap turned `gate3_gemini_describe`
into REPORTED on all three qc_pass files, with `describe_errors = null` on each —
so Gate 3 handed me no candidates either.

**WATCHER COST I DID NOT SPEND: $0.00 on all three renders** (no billed watch
completed; the only attempt failed at upload after 17.1 s wall clock). The usual
$0.08–0.10 per 25 s render was not incurred and not available to me.

---

# RENDER 1 — SPLIT (youtube/cursorworkspace_split.mp4)

## NO-SENSE TABLE (CONFIRMED)
| # | window | klass | measurement |
|---|---|---|---|
| — | — | — | **none. 0 CONFIRMED.** |

## DISMISSED
| # | window | klass | verdict | measurement / reason |
|---|---|---|---|---|
| S1 (clerk) | 0.00–0.48 | empty_zone | REFUTED | visual zone ink < 0.0008 for **0.52 s**; 0.52 s < 1.5 s. Also KNOWN-ACCEPTED #1 (opening draw-on). |
| S2 (clerk) | 11.60–11.76 | empty_zone | REFUTED | **0.20 s** of emptiness between the icon row and the browser card; 0.20 s < 1.5 s. |
| S3 (clerk) | 17.60–17.80 | empty_zone | REFUTED | **0.24 s** between the card chapter and the outro card; 0.24 s < 1.5 s. |
| S4 (clerk) | 10.40–13.02 | named_tool_no_mark ("Google Sheets") | REFUTED | word ends **11.02**; Sheets tile ink rises **10.80**, settled **11.12**. Mark present AT the word, absence 0 s vs the 2 s test. (Noted: it holds settled only 11.12–11.52, ~0.40 s, then dissolves. No law covers a short hold; recorded so Miguel can arbitrate.) |
| S5 (clerk) | 6.40–6.80 | cramp_overlap_clipping | ACCEPTED-BEHAVIOUR #11 | bridge scene and next scene both at partial opacity, one leaving — a cross-dissolve, not a collision. |

**SPLIT: 0 CONFIRMED / 5 dismissed. PASS.**

---

# RENDER 2 — CUTOUT (tiktok/cursorworkspace_cutout.mp4)

## NO-SENSE TABLE (CONFIRMED)
| # | window | klass | measurement |
|---|---|---|---|
| — | — | — | **none. 0 CONFIRMED.** |

## DISMISSED
| # | window | klass | verdict | measurement / reason |
|---|---|---|---|---|
| C1 (clerk) | 0.00–0.48 | empty_zone | REFUTED | **0.52 s** < 1.5 s; KNOWN-ACCEPTED #1. |
| C2 (clerk) | 11.60–11.76 | empty_zone | REFUTED | **0.20 s** < 1.5 s. |
| C3 (clerk) | 17.60–17.80 | empty_zone | REFUTED | **0.24 s** < 1.5 s. |
| C4 (clerk) | 10.40–13.02 | named_tool_no_mark ("Google Sheets") | REFUTED | identical to S4: ink rises 10.80, word ends 11.02, 0 s absence vs 2 s test. |
| C5 (clerk) | 1.60–21.56 | cramp_overlap_clipping (lane tiles vs silhouette) | ACCEPTED-BEHAVIOUR #3 | full-res lane band decoded at 9.0 / 14.0 / 20.0 s: tiles pass BEHIND the body and are occluded by it — the format's depth cue. |
| C6 (clerk) | 1.60–21.56 | cramp_overlap_clipping (tiles at frame edge) | ACCEPTED-BEHAVIOUR #4 | left/right edge tiles are soft-faded, no hard mid-frame slice found in any of the 3 full-width lane crops. |
| C7 (clerk) | 8.54–9.30 | empty/late label under DRIVE | REFUTED | DRIVE label absent at 9.00, legible by **9.30**; word ends 9.08 → 0.22 s, and KNOWN-ACCEPTED #1 (arrival animation). |
| C8 (clerk) | 6.40–6.80 | cramp_overlap_clipping | ACCEPTED-BEHAVIOUR #11 | cross-dissolve. |

**CUTOUT: 0 CONFIRMED / 8 dismissed. PASS.**

---

# RENDER 3 — WHITEBOARD (reels/cursorworkspace_whiteboard.mp4)

## NO-SENSE TABLE (CONFIRMED)
| # | window | klass | measurement |
|---|---|---|---|
| — | — | — | **none. 0 CONFIRMED.** |

## DISMISSED
| # | window | klass | verdict | measurement / reason |
|---|---|---|---|---|
| W1 (clerk) | 0.00–0.32 | empty_zone | REFUTED | **0.36 s** < 1.5 s; KNOWN-ACCEPTED #1. Independently confirmed by the zero-ink scan: `leading_empty_frames = 9` (0.36 s), `blank_frames = []`, min judged ink 0.00204 at 0.36 s. |
| W2 (clerk) | 5.40–5.80 | cramp_overlap_clipping (pencil over the Google G tile) | ACCEPTED-BEHAVIOUR #5 | decoded at 5.4 / 5.6 / 5.8: the tip is ON the arrowhead it is drawing, which terminates at that tile. Pencil on the ink it is drawing = the format's mechanic. |
| W3 (clerk) | 16.00–16.40 | cramp_overlap_clipping (pencil inside the browser card) | ACCEPTED-BEHAVIOUR #5 | pencil is on the card chrome it is drawing; it does not cross the finished CUSTOMIZED PAGE label above it. |
| W4 (clerk) | 11.20–11.60 | named_tool_no_mark ("Google Sheets") | REFUTED | ink in the SHEETS slot rises **10.88**, settled 10.96–11.44; word ends 11.02 → 0 s absence vs the 2 s test. |
| W5 (clerk) | 6.50 / 11.40 / 18.20 | lingering_mark (board clears between chapters) | REFUTED | ink is cleared at each chapter change and the new chapter starts clean; no old-chapter ink stands on top of a new one (KNOWN-ACCEPTED #6 read the other way round — nothing lingers). |

**WHITEBOARD: 0 CONFIRMED / 5 dismissed. PASS.**

---

# PHONE TEST (delivered files, 405x720 crops, cold)

Manifest mode: `phone-test` on all three (2 bespoke objects each). No
`phone_flag_cursorworkspace_*.md` exists — nothing was pre-flagged.

| sheet | # | t | my cold answer | key | verdict |
|---|---|---|---|---|---|
| split | 00 | 2.3 s | "bridge over water" | an arch bridge | **PASS** |
| split | 01 | 14.2 s | "Google Workspace toggle" | a settings panel | **PASS** |
| cutout | 00 | 2.3 s | "bridge over water" | an arch bridge | **PASS** |
| cutout | 01 | 14.2 s | "Google Workspace toggle" | a settings panel | **PASS** |
| whiteboard | 00 | 1.6 s | "bridge over water" | an arch bridge | **PASS** |
| whiteboard | 01 | 13.9 s | "Google Workspace toggle" | a settings panel | **PASS** |

6/6 PASS, no hedges, every answer 3 words. Object 01 was named by its control
("toggle") rather than its container ("panel") — same object, no ambiguity,
scored PASS.

Sheets reviewed:
`review/phone_cursorworkspace_split.png`, `review/phone_cursorworkspace_cutout.png`,
`review/phone_cursorworkspace_whiteboard.png`.

# INSTRUMENTS (spot-check)

* Files exist, all three **21.56 s / 1080x1920 / 25 fps**.
* Caption canon: caption band sampled at 4 Hz end to end on the split. 25 chunks,
  full transcript coverage, no hole, no repeat, one pill on the seam.
* Handles: split (youtube) **@migueltorrezai**; cutout (tiktok) and whiteboard
  (reels) **@migueltorrez.ai**. Correct per format.
* `face_center_check.py` on the reels render: `full_face n=0`; band n=43,
  **worst dx 4.35 % at t=16.5 s**, tol 4.0 %; script verdict **PASS**.
* `whiteboard_build.py --vid cursorworkspace` zero-ink scan on the reels render:
  539 frames, `blank_frames = []`, min judged ink **0.0020419** at 0.36 s,
  verdict **PASS**.

# VERDICT: **PASS** — 3 renders judged, 0 CONFIRMED, 18 dismissed, Phone Test 6/6.
