# deepseekprices — whiteboard author's notes

The plan was built as written, with two departures from the letter of a
`whiteboard_version` field. Both are required by a law. There are also three timing notes.

## 1. The tag and the DeepSeek column SLIDE. They are not erased and redrawn (LAW 51)

The plan's beat 1 whiteboard_version says "the tag is erased and redrawn one step
left". Beat 2 says "the column is erased and redrawn at the right end". The shared
scene (split + cutout) SLIDES both objects instead: the tag moves dx -210 core px
on 'increasing', and the DeepSeek column moves +264 core px on 'one'. LAW 51 says a
shared object moves the same way in every lane. So the whiteboard slides them
too, with the same moves at the same words: the tag moves -112 u over 3.20-3.60,
and the column (tile, whale, 4X bar and 4X counter as one group) moves +140.8 u
over 16.92-17.42. It also keeps the tag's one swing on 'victim' (0.74-1.56), as
the split does.
What I would have done without LAW 51: exactly this. An erase-and-redraw
leaves the tag missing for ~0.3 s, right while the gauge starts.

## 2. Timing notes (all inside the label law's 1.0 s window)

* `2X` is written at 14.82, after the bar grows to 2X on 'two' (14.70-14.82).
  `4X` is written at 15.50, after the bar grows to 4X on 'four' (15.36-15.50).
  The bar moves first, then the number on top of it. The typed value always
  matches the spoken one: 2X over "two to", 4X over "four X".
* `AI EMPLOYEE` is written at 29.00 (plan 28.68). The pen first draws the
  lanyard, clip and badge card with the whale (28.68-29.00). The last stroke
  completes at 29.34, before the outro sheet rises at 29.54.
* The chart's DeepSeek column (tile + whale + 1X bar) is drawn at 12.22-12.48,
  inside the 0.30 s erase. The shared baseline follows at 12.52-12.74, so the
  seam lands on a nameable object, not on a bare line (LAW 45).

## 3. The outro glyph

Plan beat 4 puts a small plain tag glyph (no mark) on the rising sheet above the
rule. The harness's `outro_block` has no glyph slot. I wrapped it inside the
generator; the harness is not forked. The glyph sits on the same opaque sheet at
226 px, above the rule at 322.5 px. The harness's coverage proof and all its
numbers are unchanged.

## Marker redraw (2026-09-23, rerun for style)

Miguel's note: run 26's board looked like the split's clean vector icons. Same argument, chapters, labels, timings, seams and rigids; only the ink changed:
- Every solid fill removed (tag body, gauge hub, bar fills, tower body, power button, badge card, outro glyph).
- Bars shaded with 45-degree marker hatching; the DeepSeek bar hatching fades with each 1X/2X step.
- Perfect circles replaced by hand loops that breathe and overshoot their start; outlines overshoot their first corner.
- Marker wobble raised to the run-24 reference range (0.2-0.3 u on silhouettes).
- 'locally': the power ring and glyph change to terracotta ink plus three terracotta ticks (was a solid terracotta fill).
- 'AI employee': the vents under the badge card are wiped at 28.68 because the card is line, not an opaque patch.
