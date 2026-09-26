# kimifable — WHITEBOARD author's notes

Every line here is a DEPARTURE from `plans/kimifable_plan.json` or a build-time
derivation the plan could not take. The plan was built anyway; nothing below
changes what the video ARGUES, only how the board realises it.

I found **no open doubt**. `open_doubts` is empty and stayed empty: every
question this build raised was one an author can settle with a measurement.

---

## 1. The hook's emphasis fires at 1.30, not on the word "beat" (0.94)

*The plan*: "the tile's own border flips terracotta on the same word — Kimi is
the winner" (beat 0, `emphasis[0]`).

*Built*: `box_emphasis(kimi-tile)` at **1.30**.

*Why*: the Kimi tile is drawn 0.96 → 1.22. An emphasis fired at 0.94 would pop a
terracotta box around a tile that does not exist yet — it would be an emphasis on
nothing, and on a whiteboard the ink arrives progressively rather than all at
once, which is the difference between this lane and the DOM lanes the plan timed
for. 1.30 is 0.08 s after the tile completes and still inside the word's own
breath. LAW 1 (one purposeful event, then it HOLDS) is unaffected.

## 2. The clipboard is PORTRAIT, and the plan's `scorecard` rect is not reproduced

*The plan*: `canvas_rects.scorecard = [340, 320, 740, 600]` — 400 × 280 canvas
px, landscape 1.43:1.

*Built*: 164 × 172 board units (307 × 322 canvas px), portrait, with the paper
drawn as its own inset sheet and the clip STRADDLING the top edge with its jaw
line showing.

*Why*: the plan's own instrument said so. Cold round 1 read the landscape board
**"briefcase" (unsure)** — a wide rounded box with a small tab on top is a case
with a handle, and in marker ink the tab reads as one. The plan's amendment
(`bespoke_objects[2].amended`) put the scorecard on a clipboard precisely so a
reader would have an everyday object to name; a landscape clipboard is not one.
Round 2 read it **"clipboard" (sure)**, which is the same verdict the sealed
artwork earned three times. Evidence:
`review/phone_reader_kimifable_whiteboard.json` (round 1) and
`review/phone_reader_kimifable_whiteboard_round2.json`.

## 3. Both price tags are the SAME SIZE, and the Fable tag's coins sit in a ROW

*The plan* is internally split here: `bespoke_objects[0].how_drawn` says "BOTH
tags are the SAME tag at the SAME SIZE (LAW 7, same-theme-same-size)", while
`canvas_rects` gives `kimi-tag` 176 × 104 canvas px and `fable-tag` 176 × 160 —
a 54 % taller tag, because the first draft stacked the three coins vertically.

*Built*: both tags 138 × 51 board units, and the three Fable coins sit in a ROW
inside the tag.

*Why*: LAW 7 is a law and the rect list is a layout. The sealed lane scene
resolved the same conflict the same way (`kimi-tag` and `fable-tag` both
260 × 96 canvas px, coins in a row — scene handoff §4), so all three platforms
show the viewer the same claim: one identical object, a different COUNT inside.
Two tags of different heights would have argued that Fable's tag is bigger,
which is not what the script says.

## 4. `KIMI = FABLE` is registered as ONE rigid (`eq-lockup`)

*The plan*: `labels[4]` welds SIMILAR RESULTS to `equals`, "the equals is the
object the key names (the claim is the equality, not either tile)".

*Built*: the two tiles and the equals sign register as one rigid `eq-lockup`
from 28.30 (the tiles' own solo rigids retire there; their ink does not move).

*Why*: `assert_label_side` computes the host itself — it welds a key to the
NEAREST concurrent non-decorative rigid, never to the one the plan names. With
the two tiles registered separately they are 17.1 u from the key and the equals
sign is 38.4 u, so the law welded SIMILAR RESULTS to `fable-tile3` and refused
the build: *"centre off by −57.6 u against a ±38.8 u band"*. Registering the
lockup as one object is what makes the key name the EQUALITY — exactly the
plan's stated intent — and it passes at dx 0.0 u on a ±113.7 u band.

## 5. Board type is 13.0 u (keys) and 24.0 u (the key term), not the plan's px

*The plan*'s key boxes are 44 canvas px tall (≈ 15.2 u) and the key term is
48 canvas px. This board writes every key at **13.0 u JetBrains Mono 700
UPPERCASE** and the key term at **24.0 u** (over `KEY_TERM_MIN_FS` 22).

*Why*: the plan's type sizes are the DOM lanes'. The board's own type sits
inside a 576 × 460 surface with a marker's stroke weight beside it; the run-17
whiteboards' key face is the same JetBrains Mono at the same scale, which is
what the GRAPHIC CHART asks for. The key term is still the largest type on the
board by 85 %, written first, alone, and welded to nothing (its box bottom is
42.8 u above the tiles — deliberately more than `LABEL_WELD_U` 40).

## 6. The cost fill is ONE element, not the plan's two rects

*The plan* lists `build-fill_full` and `build-fill_cut` as two canvas rects.

*Built*: ONE terracotta pill (`build-fill`), authored at the CUT width, entering
at the FULL width at 29.66 and tweened down to the cut at 30.14 over 0.48 s.

*Why*: LAW 23 — "a progress fill is ONE pill-shaped element with min-width =
track height". Two rects would be two elements and the second would terminate
somewhere. The residual is 34 % of the track, which is the same 1-of-3 the
coins, the clipboard row and the price column make.

---

## What is NOT a departure

* **No connectors anywhere.** `connectors_note` says so, the sealed scene
  asserts it, and this board declares `connectors=()`. LAW 40 reports SKIP.
* **No source card.** Zero pointing cues in `gen/_cues_kimifable.json` and in
  prep's `stages.cues`; no sentence names a platform. Nothing raised, nothing
  waived.
* **The three sealed amendments are honoured in full**: flat tags with the point
  to the left and the hole in the point, the scorecard on a clipboard, and one
  folder instead of a stack of three windows.
* **Four chapters, three erases, the outro wipe** — the plan's own board mode,
  its own seams (4.55 / 11.50 / 21.60) and its own hold windows.

## 7. The outro carries NO themed price tag — a LAW forbids it

*The plan*: beat 8, "the chassis outro lockup ... seated on this video's own
themed object — a single price tag, drawn small beside the rule".

*Built*: the chassis lockup alone (terracotta rule, JetBrains Mono
`@migueltorrez.ai`, `daily AI`), with no drawn object beside it.

*The law*: ROUND-2/3 LAW 3 and the whiteboard label law's clause 4, enforced by
`whiteboard_build.assert_outro_clear()`:

> `late = sorted({r["name"] for r in b.rigids if float(r["t0"]) >= t0})`
> `raise SystemExit("OUTRO — ink is authored at or after the outro starts ... Nothing may be drawn into the region the handle card occupies")`

The whiteboard's outro is an OPAQUE RISING SHEET that wipes the board; the card
is printed ON that sheet by `outro_block()`, which takes a handle and a daily
time and nothing else. Any ink authored at or after 32.64 refuses the build in
place. On the DOM lanes the themed object is a static element in the outro slot
and the plan's instruction is buildable there; on the board it is not.
LAW 10's per-video theme is still carried, by the object the video OPENS on: the
price tag is the hook, drawn alone and centred at 0.30 s.
