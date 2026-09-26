# openairesets whiteboard: where the board departs from the plan's letter

Author: author_whiteboard_openairesets, 2026-09-23. The plan was built as written. These are the small departures and why.

1. **Sand colour.** The sand uses the chart's light terracotta, `rgb(221,114,89)` (the scene's `TERRA_L`), not `TERRA`. The strict visual contract refuses a `box_emphasis` that shares an ink colour with its target, and the box has to stay `TERRA`. The drawing reads the same way.
2. **Outro lockup.** The plan asks for the lockup to sit on a small ink hourglass. The harness outro (`outro_block`) is the fixed chassis lockup, and `assert_outro_clear` refuses any ink authored at or after the outro anchor (16.08). So the board uses the standard rising sheet, terracotta rule, mono handle and daily line, with no hourglass glyph. The law wins here.
3. **The flip.** Built as the plan says: a terracotta curved flip arrow is drawn beside the glass on 'resets' (1.66), then the top bulb is inked full (1.96 to 2.14). The glass is not rotated. The arrow sits at the lower right, because the OpenAI arrow already uses the left side and the tag uses the upper right.
4. **Handover to the row.** The big hourglass carries across the 9.10 seam and shrinks into the row's left seat on 'to' (10.26). This is a group transform, the same motion the split uses (LAW 51), not an erase and redraw. The row's left glass stays empty.
5. **KEEP BUILDING** is written at 14.56, not 14.60, because 'building' ends at 14.54. This stops the pen from overlapping the top course, which starts at 14.80 (0.04 s after 'things' at 14.76).
6. **Phone-at boxes** are this board's own object boxes, measured at the plan's times (2.9, 12.7, 15.4). They are not the split's normalized bboxes, because the whiteboard layout differs.

## Style redo, 2026-09-23 (Miguel's note: the run-26 boards looked like the split pasted on cream)

The argument, chapters, labels, timings, seam (9.10) and phone-at boxes are unchanged. Only the drawing changed:

- The hourglass is now drawn with its own hand-plotted walls instead of the split's glass curves. The caps, posts and walls are all `b.stroke()` marker paths with a heavier hand wobble (0.30 u).
- The sand is no longer a pair of filled, clipped rectangles. It is terracotta marker hatching, drawn band by band (8 bands on the big glass, 5 on each small one). A drain wipes the top bands from the top down while it scribbles bottom bands in from the base. The falling stream is a thin marker line.
- The bricks lost their translucent fill. Each one is a wobbling marker outline with terracotta zig-zag hatching.
- The tag, its string and hole, the flip arrow and the OpenAI connector all have more wobble. The OpenAI registry mark stays a pasted colour logo in its tile, as LAW 2 requires.
- The only `b.shape()` calls left are the group wrappers, the invisible anchor rect the connector lands on, and the logo image.
