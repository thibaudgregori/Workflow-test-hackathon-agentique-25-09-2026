# ccremote whiteboard: where the board departs from the plan

The plan was built as written: same objects, labels, chapters, erase times, connectors and emphasis targets. These are the places where the whiteboard differs, and why.

1. **Lever motion.** The plan's whiteboard_version says "erase the down stroke, draw it up". Instead, the lever is drawn DOWN and then swings UP about its pivot at 13.38. This is the same 0.40 s back.out rotation the scene module uses (LAW 51: a shared object moves the same way in every lane).
2. **Tape.** The scene slaps the tape in with a scale and rotate. On the board the marker draws the tape across the pivot, tilted -8 degrees, with torn zig-zag ends. The two lengthwise lines were dropped because they crossed the lever and read as a '#'. The tape has no card fill: the brief bans solid fills on drawn objects.
3. **Outro glyph.** The plan wants a small switch with the lever up on the outro sheet. The harness authors the sheet: `outro_block`, rule, handle, daily AI. `assert_outro_clear` refuses any ink authored at or after the outro anchor. So there is no glyph on the sheet. It comes from a law, not a preference.
4. **Coordinates.** The plan's bboxes are the split's canvas. The board is 576 x 460 u. The marker also needs a 41.3 u reach above its tip, and the right rail sits at x 489.6 below y 307. So the objects keep the plan's order, sides and symmetry but sit at their own seats. The switch is (248,236,328,364) u, the phone is its mirror at x 118, and the tile column is centred at x 455. The `--phone-at` boxes are this board's seats.
5. **Checklist type.** The rows use 32 px mono with 52.5 px gaps. The plan said 28 px with 64 px gaps. Larger type was more legible on the phone, and the gaps were narrowed so row 2's box stays off the right rail.
6. **Fills.** The plan says "card fill" for the plate and note. Here every object is outline only, following the brief's ban on solid fills.
7. **Key-term size.** REMOTE CONTROL is 25 u (46.9 px), against the plan's 48 px. At 48 px it would come within about 8 u of the top session tile.
