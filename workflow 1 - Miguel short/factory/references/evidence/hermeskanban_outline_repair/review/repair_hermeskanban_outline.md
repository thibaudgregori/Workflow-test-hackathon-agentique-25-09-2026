# hermeskanban cutout — outline repair (2026-09-03)

Miguel, on the run-12 TikTok cutout: *"hermes kanban tiktok has a bad outline
compared to the rest, there is a bit of chair on my left side and some flicker
compared to the rest, minimal but there."*

Only this one file was touched. The split and the whiteboard were not re-rendered.

---

## 1. What the measurement found (BEFORE — shipped matte, alpha_v2)

Everything below is measured on the 1440x900 plate (`plate_wide_25.mp4`) against
the tracked alpha, 699 frames, every frame, no sampling.

**The chair is a WEDGE, not a column.** `wingfix` cut a rectangle
`x 0..461, rows 135..464`. The headrest wing's inner edge is not a column: it
slants roughly one column per 3.3 rows, sitting at x≈448 at row 150 and reaching
x≈481-500 by the shoulder line (row 464). Everything of the wedge to the RIGHT of
column 461 therefore survived the cut, welded to his shoulder below row 464 so
`keep-largest` could not drop it either.

| BEFORE (alpha_v2) | value |
|---|---|
| chair strip retained inside the silhouette — mask ∧ plate luma ≤ 60, `x 462..515, y 300..463` | mean **727 px**, median 637, p95 946, **max 7,218 px**; **31 / 699** frames over 1,000 px |
| left silhouette edge, row 420 | median column **495** (his true body edge is ~500-511) |
| straight-vertical-edge signature: rows in 300..463 whose leftmost column is exactly 462 | **~132 of 164 rows** on a typical frame (a human silhouette never has a 130-row straight column — this is the "bad outline") |
| overhang box `x 350..470, y 150..500` | median 7,999 px, p95 13,195, max 19,717 @ f467 |

**Edge jitter** — mean absolute frame-to-frame change of the leftmost silhouette
column, five rows through the head band, against `costpertask` alpha_v1, the
matte Miguel accepted:

| row | v2 BEFORE jit / p95 / ≥5px | costpertask (accepted) jit / p95 / ≥5px |
|---|---|---|
| 180 | 2.22 / 9.0 / 13.3 % | 1.75 / 5.0 / 7.0 % |
| 240 | 1.07 / 3.0 / 1.6 % | 1.84 / 4.0 / 1.8 % |
| 300 | 1.00 / 3.0 / 1.1 % | 1.56 / 3.0 / 1.7 % |
| 360 | 2.83 / 7.2 / **8.7 %** | 2.24 / 4.0 / 3.7 % |
| 420 | 3.53 / **15.2** / **10.7 %** | 2.71 / 3.0 / 3.3 % |

Rows 360 and 420 — exactly where the retained wedge lives — are 2-5x the accepted
video's p95. That is the flicker: the edge oscillates between the cut column (462)
and his real body edge (~500) as the tracker regrows and the keyframes reset it.

Contact sheet: `repair_hermeskanban_outline_before.png` (8 frames, cutout over
cream, 2x zoom on the suspect band). Seven of the eight tiles carry a visible slab
left of his face; only f440, an old corrective keyframe, is clean.

---

## 2. What was changed, and why

**Round 1 (alpha_v3) — denser corrective keyframes. Did not fix it; kept as a base.**
`wingfix --alpha alpha_v1 --wing-left 461 --rows-left 135,464 --chunk 40`
(72 corrective keyframes instead of 16, max gap 10 frames instead of 60). Track
`--tag v3` on H100: 120.0 s, $0.1526, seam IoU min 0.999, leak check clean.
Re-measured: the chair strip got **worse** (mean 1,079, p95 3,753) and jitter rose,
because the defect is not propagation drift — the keyframe masks themselves
retained the wedge to the right of column 461. Round 1 was not the fix, but its
narrow, full-height cut at 72 keyframes is correct and is carried inside round 2.

**Round 2 (alpha_v4) — the wide, low window chained onto v3. This is the fix.**
`wingfix --alpha alpha_v3 --wing-left 510 --rows-left 300,464 --chunk 40`
→ `prompts_v4` → track `--tag v4`.

Why chained rather than one call: `wingfix`'s window is a single rectangle, and no
single rectangle works here. A window wide enough at the bottom (x ≤ 510) carves
his CAP at the top whenever he leans left — verified on the `--dry` proof at f467,
where x ≤ 510 over rows 135..464 ate his cap, eyebrow and part of his beard. A
window that clears the cap (rows ≥ 300) leaves the wedge's upper half. Running the
narrow/full-height cut first and the wide/low cut on its result gives both bands
without ever putting the cap inside a wide window.

Guards on the round-2 cut: 72 masks, cut min 810 / median 3,750 / max 7,472 px,
**max luma of any removed pixel 60** (the guard itself), silhouette lost
0.15-1.38 %. Visual `--dry` proofs were reviewed at f420, f434, f455, f467, f560,
f665, f672, f679, f690 before spending: no red on his face at any of them.

Track v4: H100, 128.0 s billed, **$0.1517**, seam @350 IoU min 0.99934 / mean
0.99945, leak check **clean**.

Ship (laptop, exactly as `prep_batch.ship_matte` runs it, no `--allow-*` flags):

```
ship.py --alpha alpha_v4.mkv --plate plate_wide_25.mp4 \
        --out matte_hermeskanban_v5 --emit v5 --pad mirror \
        --master shorts_run12/cuts/hermeskanban/master.mp4 \
        --display 1584x990 --edge-box 1584x990+-153+930
```

The previous v5 layers + ship json were copied to
`pipeline/sam2/sessions/hermeskanban/_v5_before_outline_fix/` before the overwrite.

---

## 3. AFTER (alpha_v4, shipped as matte_hermeskanban_v5_*)

| metric | BEFORE (v2) | AFTER (v4) |
|---|---|---|
| chair strip, mean | 727 px | **185 px** |
| chair strip, median | 637 px | **176 px** |
| chair strip, p95 | 946 px | **327 px** |
| chair strip, max | 7,218 px | **522 px** |
| frames with > 1,000 px of chair | 31 / 699 | **0 / 699** |
| left edge median, row 420 | 495 (cut column) | **500** (his body) |
| left edge median, row 360 | 478 | **480** |

Edge jitter, same five rows (jit mean / p95 / share of ≥5 px jumps):

| row | BEFORE (v2) | AFTER (v4) | costpertask (accepted) |
|---|---|---|---|
| 180 | 2.22 / 9.0 / 13.3 % | 3.63 / 14.0 / 17.9 % | 1.75 / 5.0 / 7.0 % |
| 240 | 1.07 / 3.0 / 1.6 % | 1.20 / 3.0 / 2.1 % | 1.84 / 4.0 / 1.8 % |
| 300 | 1.00 / 3.0 / 1.1 % | 1.03 / 3.0 / 1.0 % | 1.56 / 3.0 / 1.7 % |
| 360 | 2.83 / 7.2 / 8.7 % | **2.04 / 4.0 / 4.2 %** | 2.24 / 4.0 / 3.7 % |
| 420 | 3.53 / 15.2 / 10.7 % | **1.69 / 3.0 / 2.4 %** | 2.71 / 3.0 / 3.3 % |

Rows 360 and 420 — the rows the defect lived in — are now at or better than the
accepted video's numbers. Row 180 is the one that got worse (17.9 % vs 13.3 % of
frames moving ≥ 5 px); it is above the repaired band, in the cap/ear rows, and it
is the cost of 72 corrective keyframes instead of 16. It is not where the chair was.

Contact sheet: `repair_hermeskanban_outline_after.png`, same eight frames. Six of
the eight are now clean cream-to-skin edges. Two (f455 = 18.20 s, f467 = 18.68 s)
still show a pale slab — see the honest limit below.

**What is NOT fixed.** For roughly one second around 18.2-18.8 s he leans right and
a strip of BRIGHT WALL (plate luma 150-180, the same brightness as his cheek) is
left inside the silhouette between the chair and his face. `wingfix` and
`bolsterfix` both remove *dark* pixels only, and `keep-largest` cannot drop that
strip because it touches his cheek directly. No existing tool in
`pipeline/sam2/` can remove it; the README's own known-limit #4 (track the chair
as a SECOND SAM2 object, so both boundaries become a competition) is the
principled fix and has never been built.

---

## 4. Verdicts

| gate | verdict |
|---|---|
| track v4 leak check | clean (healed false, needs_human false) |
| track v4 seam @350 | IoU min 0.99934, mean 0.99945 |
| ship — PROTRUSION gate | **clean** |
| ship — edge clip gate | **CLEAN** (0 plate-border defects; the 7 frame-right frames at 16.84-17.08 s are the pre-existing hand-at-frame-edge window, unchanged) |
| prerender_check (rebuilt cutout project) | **PASS**, 7/7 checks, 0 errors / 0 warnings |
| render | 1080x1920, 699 f, landed in 118.0 s |
| qc_pass | **PASS** — 16/16 verdicts pass (`double_exposure` REPORTED as always), `whiteboard_seam_law` skipped |
| Gemini watcher (gemini-3.5-flash-lite) | **PASS**, **0 candidates**, 0 blocking, 0 motion |

Staged to `~/Movies/Shorts Factory/Daily/2026-09-03/tiktok/hermeskanban_cutout.mp4`.
The rejected render was moved to `.../tiktok/_rejected_v1/hermeskanban_cutout.mp4`
before staging. `_build_hermeskanban.json` was regenerated for both formats and the
split project directory verified byte-identical to its pre-repair snapshot.

## 5. Cost

| item | USD |
|---|---|
| track v3 (H100, 128.8 s billed) | 0.1526 |
| track v4 (H100, 128.0 s billed) | 0.1517 |
| ship (laptop) | 0.0000 |
| render (Modal) | 0.0151 |
| Gemini watcher | 0.0297 |
| **total** | **0.3491** |

---

## 6. For the skill — what prep should check so a gate catches this next time

`protrusion.py` passed a matte Miguel rejected because it only asks a
**top-y profile** question: it finds columns whose silhouette TOP is a furniture
top rising above a shoulder. It is structurally blind to furniture that sits
*beside and below* the head band — the half of a wedge that survives to the right
of a `wingfix` cut column, welded to the shoulder so `keep-largest` keeps it.

Add a **post-heal gate** to the ship lane, running on the shipped alpha:

1. **Straight-edge test.** For each frame, walk the silhouette's leftmost and
   rightmost column per row through the body band and refuse any run of ≥ 40
   consecutive rows whose extreme column is identical (±1). A human edge is never
   a straight column; this matte had ~132 such rows and passed everything.
2. **Retained-dark test, keyed to the heal window.** After any `wingfix` /
   `bolsterfix`, measure `mask ∧ plate-luma ≤ dark` in a 50-column band just
   OUTSIDE the cut column, over the cut's rows, and refuse when the median exceeds
   a few hundred px. Here it was median 637 / max 7,218 px, i.e. the heal
   demonstrably stopped one column short of the object it was cutting.
3. **Record the wedge slope.** `wingfix --measure` already prints the always-dark
   rows per column; prep should read the slope off it and refuse a rectangle whose
   single inner column cannot cover a wedge that slants more than ~1 column per
   5 rows — that is the signal to chain two windows (narrow/full-height, then
   wide/low) instead of trying one.

**Tooling gap, reported not patched:** `wingfix`'s window is a rectangle and its
keyframe cadence is fixed in `modal_app.LEAK` (only reachable indirectly through
`--chunk`). A wedge-shaped wing needs either a slanted window (`--wing-left-at
row:col,row:col`) or the two-pass chain used here, which costs a second track.
And no tool in the directory can remove a BRIGHT background strip welded to his
cheek — that one needs the second-SAM2-object idea from README known-limit #4.
