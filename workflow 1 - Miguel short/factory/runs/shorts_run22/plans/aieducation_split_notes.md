# aieducation — SPLIT AUTHOR NOTES

I built the plan. Nothing below changed what the plan argues; the two entries
are a MEASURED DEFECT in the shared module's animation (not in its drawing) and
one observation the cutout lane and the clerk should have.

## 1. THE SHARED MODULE NEVER MAKES ITS DRAWN STROKES VISIBLE (a defect, repaired format-side)

`aieducation_scene.py`'s glyphs author every stroke at element `opacity="0"` and
reveal it with `fadeink()` (`tl.to(..., opacity:1)`). Its `draw()` helper
animates `strokeDashoffset` and raises `strokeOpacity` — it never touches
element opacity. So every stroke that is DRAWN instead of faded stays invisible
for the whole video:

* `#arc .ar` — the rotation arc's curve. At 12.60 the heart carried its
  arrowhead (`.arh`, faded) and no arc.
* `#head .bb` and `#head .wb` — the two crown ticks and the dashed heart inside
  the cranium. At 17.40 the crop was a bare profile: exactly the ink three
  independent readers named at the artwork seal ("head profile with heart") was
  missing from the animated page.

The artwork proof harness (`_aieducation_proof.py`) paints stills through
`_ink_on()`, which rewrites `opacity="0"` to `1`. That is why the seal round saw
ink the animated page does not, and why no automatic gate caught it: a still
crop cannot see a reveal that never fires.

Second, `draw()` uses a FIXED `strokeDasharray:100` for every path, so a path
longer than 100 units rests at offset 0 as a dash/gap pattern — a broken draw-on
(the run-19 dash law: the reveal dash must equal the path's own length). Once
the arc became visible it was a broken sweep, and the three connectors were
dashed lines.

**What I did.** I repaired both on the EMITTED tween list only
(`reveal_drawn_ink()` in `gen/aieducation_split_gen.py`): one
`tl.set(opacity:1)` at the same instant `draw()` raises strokeOpacity, and one
`tl.set(strokeDasharray:"none")` at the instant each draw completes. Geometry,
timing and the sealed drawing are unchanged, and **no byte of the shared module
was touched** — the cutout author is reading the same file while this runs.

**What I would have done** if the run had room for it: fix `draw()` itself, two
lines, under `production.py scene-lock` — it is one helper and it fixes both
DOM lanes at once.

**THE CUTOUT LANE HAS THIS DEFECT TOO.** Whoever seats this scene for TikTok
must carry the same repair, or ship an arc-less heart and a head with nothing in
it.

## 2. TWO KEYS LAND LATER THAN THE PLAN'S LETTER (the module's choice, inside the law)

The plan puts `3D ANATOMY` at 9.26, `GUESSWORK` at 16.52 and `INSIDE` at 20.18.
The module lands them at 9.62, 17.02 and 20.54. Every one is inside its own
word's 1.0 s LABEL_WINDOW (`anatomy` 9.26-10.96, `imagine` 16.52-17.98, `how`
20.54-21.66) and the word-sync screenshots confirm the first visible state, so
this is legal and I built it as the module has it rather than moving a sealed
scene's timeline. Recorded because the whiteboard lane is working from the
plan's numbers and will land the same keys ~0.4 s earlier.

## 3. THE PLAN'S `open_questions` I DID NOT ACT ON

The plan's first open question invites the split author to crop the inner zoom
to the heart alone if heart-plus-panel does not read at 405x720. I looked at the
page at 6.40 s: the screenshot's 3D heart is ~90 design px with the word "Heart"
legible beside it, so the authored `ZOOM_K = 1.92` stands and I changed nothing.
The other two questions belong to the cutout and to the outro glyph.
