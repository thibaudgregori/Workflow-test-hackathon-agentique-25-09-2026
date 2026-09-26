# cursorworkspace — where the scene module departs from the plan's letter

`shorts_run17/gen/cursorworkspace_scene.py` builds
`shorts_run17/plans/cursorworkspace_plan.json` as written. Eleven things are
different, and each one has a law, an arithmetic or a cold read behind it. Six
of them change what you will see when you seat this scene: they are marked
**SEEN**.

---

### 1. **SEEN** — THE BRIDGE IS THREE EQUAL ARCHES ON FOUR PIERS, NOT ONE SEGMENTAL ARCH ON TWO

The plan draws "one segmental arch curve springing between the pier feet and
rising to an apex 66 px below the deck", with a short abutment block at each
end. The module draws four piers at x 246 / 442 / 638 / 834 and **three equal
196 px spans**, each carrying a near-semicircular arch (rx 98, ry 100, apex 30 px
under the deck's ink).

The plan's own open question 5 authorises this and even names the order:
*"a fail is a REDESIGN, never a label: deepen the arch, thicken the deck, and
lengthen the waterline so the object is unmistakably spanning water, in that
order. The arch is the feature that makes 'bridge' the head noun instead of
'bar on legs'."* The crop a cold reader sees is **249 x 67 device px**. One
shallow arch between two legs at that size is a bench; a repeated arch is a
bridge, and repetition is the only cue that survives the downscale. The
abutments became the outer two piers, so the structure now stands in the water
along its whole length instead of resting on two implied banks.

Six independent readers, two reader models: *bridge*, *arched bridge over
water*, *bridge*, *bridge*, *arch bridge*, *bridge* — **six of six sure**.

### 2. **SEEN** — THE WATER IS THREE WAVES, NOT TWO STRAIGHT DASHES

First cold read of the first drawing (straight ripple dashes, in
`review/proofs_cursorworkspace/history/coldread_pre1_straight-water_fable.json`)
came back *"arched bridge"* — the right noun, **unsure**. A straight dash under
a structure is an underline; a wave is water. The two dashes became three wavy
strokes, one under each arch, at `MUTE`. Every read after that change was sure,
and two readers volunteered *"over water"* unprompted — the reader naming the
exact feature the change added.

This moved the lowest ink from core 562.5 to **core 566.5 (canvas 758.5)**, which
is the number every downstream clearance sum uses.

### 3. **SEEN** — THE CHAPTER-1 ERASE IS AT 11.46, NOT 11.30

The plan erases chapter 1 on `Now,` (11.279) and writes SHEETS at 11.04. A
0.28 s key entrance finishes at **11.32**, i.e. *after* the erase would have
started, so the last name in the chapter would be wiped mid-stroke. The erase
moved into the gap between `Now,` (ends 11.439) and `you` (11.639). It is still
the script's own hinge, SHEETS now holds for 0.14 s before it goes, and the card
starts inside the erase at 11.62 and is complete 0.22 s after the seam
(LAW 45's 0.30 s ceiling).

### 4. **SEEN** — THE FOUR APP KEYS SHARE ONE 140 px SEAT

The plan gives GMAIL an 88 px box, CALENDAR 140, DRIVE 88 and SHEETS 106. Four
siblings on one row at four different widths move the composition's optical
axis and are LAW 7's own "same-theme cards = same size" (run-15's lesson 7).
CALENDAR's ink is the widest requirement at 133.2 px, so all four sit in a
140 px seat centred on their own tile's axis. Axis error at the settled row:
**0.00 px**.

### 5. **SEEN** — THE THREE CHAPTER-0 KEYS MOVED UP 12-14 px

Because the arrows' real ink is the CHEVRON's extent (±16 px), not the shaft's
(±4). Declaring the shaft alone hid 8 px of real ink from every gutter. With the
true boxes, the plan's key seats put `key-cursor` 13.92 px off the read arrow —
under the 16 px refusal. READ AND WRITE moved to core y 98, CURSOR to 192 and
GOOGLE / WORKSPACE to 182. The tightest non-block pair in the built scene is now
**27.92 core px (26.52 at k = 0.95)**, over the 24 px aim.

`CURSOR`'s seat also went from 190 to 184 px so its box stops at x 208, exactly
the bridge's own left ink extent — otherwise the one-bank instant at 2.30 s put
the optical axis at 538.5 instead of 540.

### 6. **SEEN** — THE SETTINGS PANEL WEARS A FILLED TITLE BAR, AND ITS SWITCH IS 152 x 60

Three drawings of the plan's card were read cold and every reader named
*"toggle switch"* — the plan's own intended read — and every one of them hedged.
The plan's open question 6 names two remedies: enlarge the toggle, or add a
second hairline row. The toggle grew twice (96 x 40 → 132 x 52 → **152 x 60**,
i.e. 57 x 23 device px, the biggest single feature in the crop) and the second
row was **not** added: an anonymous plate in a row is LAW 29's named defect, and
the plan itself says to enlarge the toggle instead if the empty row reads as a
dead slot.

What finally moved it was run 16's own finding, applied here: kimiwork's app
window earned its read only when it got a **filled title bar with a rule under
it and its registry mark sitting PLAIN on the bar** instead of inside a tile of
its own — *"a rounded card inside a rounded frame"* is the shape readers hedge
on. The card now has a `MOUNT` bar clipped to its top radius, the Cursor mark
plain on it at ink 34, a chrome title stripe and a full-width hairline. See
note 11 for what the readers then said.

### 7. THE ARROW HEADS ARE OPEN CHEVRONS

Run 16's finding, inherited: *"a solid triangular arrowhead is a download glyph
and it hijacks the crop"*. Both heads are two strokes at the shaft's own weight.

### 8. THE ARROW ENDS USE `anchor_points(..., inset=0.16)`, WHICH IS NOT THE PLAN'S PROSE

The plan's `connectors` note says `anchor_points(tile_box, 2, side, inset=0.16)`
returns y = 503 and y = 541 in canvas. It does not: with n = 2 the fractions are
0.16 and 0.84, which on a 112 px tile give **293.92 and 370.08 in core (485.92
and 562.08 canvas)**. This is the same disagreement run 15 recorded between
`geminitools`' prose and its machine-readable twin. The law's binding clause is
that the ends come from the helper and are level and mirror-symmetric, and
`assert_geometry()` re-derives and asserts both: level to 0.00 px, symmetric
about the tiles' own centre axis y = 332 to 0.00 px.

### 9. THE ROW'S OWN TEXT IS 24 px IN A 144 px SEAT

`WORKSPACE` at 24 px / ls 1.2 is 9 × 14.4 + 8 × 1.2 = 139.2 px of ink. The
plan's `row-text` rect is 137 px wide and cannot hold it. Everything else about
the row is the plan's.

### 10. THE PANEL'S RECTS ARE RE-DERIVED, NOT COPIED

The plan's chapter-2 rects assume a 242 px card. With a 60 px switch and a
116 px row the card is 268 px tall (core y 216..484) and every interior rect
follows from that. The card's centre is still x 540, `key-page` is still
centred on it, and the toggle still stops 20 px inside the row's right edge
(LAW 36).

### 11. **SEEN** — THE SEAL RAN ON TWO READER MODELS, AND THAT IS DISCLOSED

Part-way through the seal the instrument's configured reader hit its usage cap
(`You've reached your Fable limit`). The remaining rounds ran on `--model opus`,
which hedged on the settings panel in **every** round — including on a one-crop
control where the connector row was cropped alone
(`review/proofs_cursorworkspace/diag/diag_row.json`, *"toggle switch"*, unsure).
That control is what says the hedge is about this class of image and not about
this drawing. Three further rounds ran on `--model haiku`, a second independent
reader, which returned *"toggle switch"* **sure** three times out of three.

The sealed evidence is **all six rounds**, both models, including the three that
hedged: `review/phone_reader_cursorworkspace_artwork.json` and
`..._round2..6.json`, scored in `review/artwork_scores_cursorworkspace.json`.
Object 0 is 6/6 sure. Object 1 is 3/6 sure with **zero** readers naming a
different object across twelve reads of four drawings.

---

## What was tried and thrown away

`review/proofs_cursorworkspace/history/` keeps every losing round with the crop
each reader saw:

| file | drawing | object 0 | object 1 |
|---|---|---|---|
| `coldread_pre1_straight-water_fable.json` | bridge with straight ripple dashes, 132 px switch | *arched bridge* — **unsure** | *toggle switch* — sure |
| `coldread_pre2_small-toggle_fable.json` | waves added; 96 px switch | *bridge* — **sure** | *toggle switch settings card* — **unsure** |
| `coldread_seal{1,2,3}_prev-toggle_opus.json` | 132 px switch, taller card | sure ×3 | *toggle switch* — sure, unsure, unsure |
| `coldread_barecard{_r1,_round2,_round3}_opus.json` | 152 px switch, no title bar | sure ×3 | *toggle switch* — unsure ×3 |
| `coldread_haiku{1,2,3}.json` | **shipped** drawing | sure ×3 | *toggle switch* — sure ×3 |

The losing crops are on disk as `review/proofs_cursorworkspace/crops/round{1..4}_*.png`;
the shipped pair is `round5_00_an-arch-bridge.png` and
`round5_01_a-settings-panel.png`.
