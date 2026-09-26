# stripekai whiteboard: where the build departs from the plan's letter

1. **Outro glyph (o-glyph) not drawn.** The plan puts a small toolbox on the rising sheet. The shared harness `whiteboard_build.outro_block()` owns the sheet (rule, handle, daily AI) and `assert_outro_clear()` refuses any ink authored at or after the outro anchor (31.82). I did not fork the harness, so the sheet carries the rule and the lockup only. To add the glyph, extend `outro_block()` once for every whiteboard.
2. **The toolbox slides right and shrinks in chapter 1.** The plan's `whiteboard_version` says the board does not need to redraw it smaller. Its `picture` has the slide, and LAW 51 says a shared object moves the same way in every lane. So the drawn toolbox moves with one transform (x0.8, 10.10-10.60), the same move the split makes. Nothing is redrawn.
3. **The crowd draws from 14.10, not 13.80.** At 13.80 the shrinking person is still mid-move and would overlap figure 1 while it draws. The eleven figures start at 14.10 and are 0.05 s apart, so they finish by 14.66. Nothing is spoken about them before 15.34.
4. **The connector sits level at the person's shoulder line, not at the box centres.** `anchor_points(...,1,...)` puts the person's end in the gap between head and shoulders. The single connector ends on toolbox-seat1's virtual rectangle (left side, fraction 0.77). LAW 40 passes.
5. **The counters `1,000 / SKILLS` and `500 / INTERNAL TOOLS` are written** on their words (7.10 / 7.60 / 8.72 / 9.58), as the plan's picture says. They are not in LABEL_PLAN because they are not names of drawn objects.
6. **Caption regroup (LAW 4).** The chunker emitted a lone pill `organizations.` at the same moment the board writes ORGANIZATIONS. I recut the same words as `how to use AI inside` | `of their organizations.`.
7. **The --phone-at boxes come from the board's own geometry.** The whiteboard places every object at the plan's normalised bbox (scene core px -> board u), so these boxes agree with the plan's to within about 0.01.

## Style redo (Miguel's note, 2026-09-23)

8. **Every object is redrawn by hand.** Argument, chapters, keys, timings, rigids, blocks, connector and seams are unchanged. The drawing layer changed: every outline is now a hand-plotted `b.stroke()` point list (bowed sides, rounded-by-hand corners, closed outlines that overshoot their start, lopsided circles) drawn at the chassis marker wobble. All ~200 solid `fill()` shapes (card, mount and terracotta) are gone.
9. **The plan's "fill terracotta" is marker scribble.** The ten 83% people, the seven week cells and the screwdriver grip are coloured in with terracotta zig-zag hatching. Their outline stays ink, and a solid fill is not allowed any more.
10. **Occlusion without card fills.** Tools behind the toolbox body, the heap behind the standing tools and each heap tool behind the ones dropped after it are clipped and never inked. Before, an opaque card fill covered them.
11. **Only two non-stroke elements remain:** the typed JetBrains Mono keys and the Stripe registry wordmark on the hand-drawn nameplate (a registry mark, per LAW 2).
