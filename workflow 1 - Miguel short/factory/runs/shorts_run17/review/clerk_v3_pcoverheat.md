# CLERK v3.1 — pcoverheat — VERDICT: PASS

Renders judged: **3 of 3** (split / whiteboard / cutout). All 1080x1920, 25 fps, 37.181 s.

## STEP 1 — THE WATCHER'S CANDIDATES: ALL THREE FILES ARE MISSING

`cands_pcoverheat_split.json`, `cands_pcoverheat_whiteboard.json` and
`cands_pcoverheat_cutout.json` **do not exist**. Neither does any
`watcher_unavailable_pcoverheat_*.md` (the run wrote those for
`eudisclosure_whiteboard` and `cursorworkspace_cutout`, so the mechanism exists
and simply did not fire here).

**All three pcoverheat renders were watched by nothing.** Per v3.1 I report the
hole and do not backfill it: no watcher was re-run, so the watcher cost I did not
spend is **$0.0000 on all three files, 0 s of wall clock** — there was no watcher
call to inherit.

Cause, read out of the run's own gate-3 record (`gen/_qcpass_pcoverheat_*.json`
→ `checks.gate3_gemini_describe`): the Gemini project is over its cap.

```
429 RESOURCE_EXHAUSTED — "Your project has exceeded its monthly spending cap."
upload retry 1/2/3 all 429 → RuntimeError: upload failed
rc=1, wall 20.39 s (split) / 20.85 s (whiteboard) / 20.82 s (cutout)
```

Consequence for **GATE 3 (advisory)**: `verdicts.gate3_gemini_describe = REPORTED`
on all three, but the describe pass **crashed on upload and produced zero
`describe_errors`**. There is nothing from gate 3 to adjudicate — the REPORTED is
an infrastructure failure, not a picture claim.

So every row below is **clerk-originated**, from my own decode.

## MY OWN DECODE (the part that works)

* 41 whole frames per render at 0.5–37.0 s (`scale=430:-1`, no cropping), plus
  high-resolution whole frames at 4.3 / 11.3 / 30.5 s.
* A continuous **10 fps ink curve** of the visual zone (y 0.03–0.40, x 0.05–0.95)
  over the full 37.2 s of each render — 372 samples per lane — so every
  `empty_zone` window is measured, not eyeballed.
* Sentence-by-sentence cross-check against `cuts/pcoverheat/transcript_tight.json`.

**The picture argues the sentence, beat for beat:** overheating laptop with heat
lines (0.1–2.9) → X post card, header `𝕏 @XFREEZE · X`, body "my MacBook was
heating up my lap… so I asked Grok Build to investigate. It found the culprit"
(3.3–6.9, under "like this guy did on X") → THREE APPS with three marks
(6.9–13.9) → INSTALL download arrow (12.5–13.9) → TELL THEM speech bubble
(14.1–…) → PROCESSES table filling HOT / RAM / CPU in the order they are spoken
(18–25) → culprit row ringed red + THE CULPRIT (30.5–32.3) → close ⊗ (32.0) →
handle card (33.7–end).

**Platform law:** the sentence says "on X" and the card wears the X frame and the
X glyph. No mismatch.

**named_tool_no_mark, measured:** "Codex" ends 8.78, its mark begins landing at
8.4 (ink 0.95 → 1.21 → 1.31); "Claude Cowork" mark settled by 9.8; "Grok Build"
ends 10.60, mark settled by 10.5. Every mark is present **before** its word ends.

**missing_source_post:** `pointing_cues.py --vid pcoverheat` returns exactly one
cue — `{"t": 3.24, "kind": "person", "phrase": "like this guy", "card_hold_s":
[2.0, 4.0]}`. The X card holds 3.3–6.9 s ≈ **3.6 s**, inside the required window.
Satisfied on all three renders.

---

# SPLIT — /shorts_run17/staging/youtube/pcoverheat_split.mp4

### NO-SENSE (CONFIRMED) — 0 rows
| window | klass | measurement |
|---|---|---|
| *(none)* | | |

### DISMISSED — 3 rows
| # | window | klass | verdict | reason (measured) |
|---|---|---|---|---|
| S1 *(clerk-originated)* | 32.85–33.25 s | empty_zone | **REFUTED** | Zone ink hits 0.00 % at 32.9 and 33.1, back to 1.05 % at 33.3. Settled emptiness = **0.4 s < 1.5 s**. Beat handover, culprit table → handle card. |
| S2 *(clerk-originated)* | 13.85–14.05 s | empty_zone | **REFUTED** | Ink 5.93 % at 13.7 → 0.00 % at 13.9 → 0.73 % at 14.1. Settled emptiness = **0.2 s < 1.5 s**. |
| S3 *(clerk-originated)* | 6.7–8.4 s | empty_zone | **REFUTED** | Zone is not empty: it carries the settled "THREE APPS" heading, ink **0.93–1.25 %**, never 0. The law requires the zone carry *nothing*. Icons then land 8.4 / 9.8 / 10.5 — KNOWN-ACCEPTED #1 (entry animations) covers the stagger. |

**Handle:** `@migueltorrezai` (YouTube) — correct for this lane.

---

# WHITEBOARD — /shorts_run17/staging/reels/pcoverheat_whiteboard.mp4

### NO-SENSE (CONFIRMED) — 0 rows
| window | klass | measurement |
|---|---|---|
| *(none)* | | |

### DISMISSED — 2 rows
| # | window | klass | verdict | reason (measured) |
|---|---|---|---|---|
| W1 *(clerk-originated)* | 13.7–14.1 s | empty_zone | **REFUTED** | The whiteboard **never reaches zero ink** anywhere in 37.2 s. Minimum across the whole render is 1.00 % at 13.9 s. 0.0 s of emptiness < 1.5 s. |
| W2 *(clerk-originated)* | 0.5–2.5 s, 22.0 s, 30.5 s | ring_or_box_on_image_text / cramp | **ACCEPTED-BEHAVIOUR (#5)** | The marker tip sits on the glyphs and on the table row it is drawing at that instant (laptop + "OVERHEATING", the HOT column, "THE CULPRIT"). Pencil-on-its-own-ink is the format's mechanic. It never crosses a different, finished block. Item #6 also covers the held board ink. |

**Handle:** `@migueltorrez.ai` (Reels) — correct for this lane.

---

# CUTOUT — /shorts_run17/staging/tiktok/pcoverheat_cutout.mp4

### NO-SENSE (CONFIRMED) — 0 rows
| window | klass | measurement |
|---|---|---|
| *(none)* | | |

### DISMISSED — 3 rows
| # | window | klass | verdict | reason (measured) |
|---|---|---|---|---|
| C1 *(clerk-originated)* | 32.85–33.25 s | empty_zone | **REFUTED** | Ink 7.83 % at 32.7 → 0.00 % at 32.9 and 33.1 → 1.21 % at 33.3. Settled emptiness = **0.4 s < 1.5 s**. |
| C2 *(clerk-originated)* | 13.85–14.05 s | empty_zone | **REFUTED** | Ink 7.59 % at 13.7 → 0.00 % at 13.9 → 0.87 % at 14.1. Settled emptiness = **0.2 s < 1.5 s**. |
| C3 *(clerk-originated)* | 3.4–37.0 s | cramp_overlap_clipping | **ACCEPTED-BEHAVIOUR (#3 + #4)** | Parallax logo tiles pass behind the silhouette and are hidden by it (depth cue, #3); tiles at the left and right canvas edges are edge-faded / partly outside frame (#4). Checked the 760 px whole frame at 11.3 s: no hard mid-frame slice, every truncation is at a canvas edge. |

**Handle:** `@migueltorrez.ai` (TikTok) — correct for this lane.

---

# STEP 3 — THE PHONE TEST — PASS (12 / 12)

Four bespoke objects per sheet, three sheets, cropped alone at 405x720. Answers
were written into the manifests **before** any key was opened; no
`phone_flag_pcoverheat_*.md` exists in the run, so **no object was carrying a
known cold-read failure into this render**.

| sheet | # | t | my cold answer (<=3 words) | key | result |
|---|---|---|---|---|---|
| split | 00 | 1.9 s | overheating laptop | an_open_laptop | **PASS** |
| split | 01 | 13.3 s | download arrow | a_download_arrow | **PASS** |
| split | 02 | 16.6 s | speech bubble | a_speech_bubble | **PASS** |
| split | 03 | 25.9 s | process monitor table | a_process_list | **PASS** |
| whiteboard | 00 | 2.1 s | overheating laptop | an open laptop | **PASS** |
| whiteboard | 01 | 13.45 s | download arrow | a download arrow | **PASS** |
| whiteboard | 02 | 16.3 s | speech bubble | a speech bubble | **PASS** |
| whiteboard | 03 | 25.6 s | process monitor table | a process list | **PASS** |
| cutout | 00 | 1.9 s | overheating laptop | an open laptop | **PASS** |
| cutout | 01 | 13.3 s | download arrow | a download arrow | **PASS** |
| cutout | 02 | 16.6 s | speech bubble | a speech bubble | **PASS** |
| cutout | 03 | 25.9 s | process monitor table | a process list | **PASS** |

No sheet declared mode `spaced-fallback`; all three are real Phone Tests with
four bespoke objects each.

**One handling note, not a defect and not a fail.** The **cutout** sheet's crop
boxes are misregistered against their objects: #00 clips the top of the heat
lines, #02 shows only the lower band of the speech bubble with "TELL THEM" sliced
through its cap-height, and #03 cuts the "PROCESSES" title off the table. I named
all three correctly anyway, so the objects pass. The bounding boxes in
`phone_pcoverheat_cutout.json` are what want fixing, in the review artefact, not
in the render — the same objects are framed correctly on the split and whiteboard
sheets and are correct in the delivered cutout frames themselves (verified at
16.0 s and 26.0 s).

Contact sheets reviewed:
* /Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/runs/shorts_run17/review/phone_pcoverheat_split.png
* /Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/runs/shorts_run17/review/phone_pcoverheat_whiteboard.png
* /Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/runs/shorts_run17/review/phone_pcoverheat_cutout.png
* /Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/runs/shorts_run17/review/sheet_pcoverheat_split.png
* /Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/runs/shorts_run17/review/sheet_pcoverheat_whiteboard.png
* /Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/runs/shorts_run17/review/sheet_pcoverheat_cutout.png

---

# STEP 4 — INSTRUMENTS — PASS

| instrument | result |
|---|---|
| files exist / duration | 3/3 present. **37.181333 s** each, identical; 1080x1920, 25 fps. 35.5 / 33.1 / 31.6 MB. |
| handle canon | split `@migueltorrezai`; whiteboard `@migueltorrez.ai`; cutout `@migueltorrez.ai`. Correct per lane. |
| caption canon | Spot-checked at ~40 timestamps per render against `transcript_tight.json`; one pill on the seam, wording matches the spoken words in all three. Chunking differs between lanes (e.g. split "like this guy did on X." as one pill vs whiteboard "like this guy did" / "on X.") — same words, different break, not a discrepancy. |
| `face_center_check.py` (reels) | **PASS**. `worst_dx_pct` (band) = **5.19 %** at t = 3.0 s, n = 74; `full_face` n = 0; tol 4.0 %; script verdict `PASS`. |
| `whiteboard_build.py --vid pcoverheat` (reels, zero-ink scan) | **PASS**. 929 frames, 25 fps, zone 1080x799, `min_ink_frac_judged` = **0.00203843** at 0.2 s, `blank_frames` = **[]**. |

**Discrepancy to record:** the only instrument-level anomaly in this video is
infrastructure, not picture — the Gemini spend cap took out both the post-render
watcher (no `cands` files) and gate-3 describe-mode (rc=1 on all three). The
run's semantic coverage for pcoverheat therefore rests entirely on this clerk's
own decode. That is a real reduction in redundancy and Miguel should know it,
even though it changes no verdict here.

---

## VERDICT: **PASS** — 3 renders judged, **0 CONFIRMED**, 8 DISMISSED (all 8 clerk-originated; 5 REFUTED on measurement, 3 ACCEPTED-BEHAVIOUR), Phone Test 12/12.
