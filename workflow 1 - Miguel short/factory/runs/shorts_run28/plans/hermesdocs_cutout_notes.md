# hermesdocs cutout: notes (author_cutout, 2026-09-23)

The plan is built as written. Three small points to record:

1. **Core top 192, not the handoff's centring formula.** Section 2 of the handoff gives
   `top = round(stage_centre - 302 * k)`, which is 197.2 for this body's stage zone
   (192 .. 806.4). I used 192, the split's placement, like the hermeshub cutout. The content
   band 252..736 is 70.4 px clear of the zone bottom and 238 px above his highest crown
   (974), and the plan's bespoke bboxes then map 1:1 onto the cutout page.
2. **`--phone-at` for "open safe documents" uses the module's core box**
   (`SC.BESPOKE`: 0.3519,0.1771,0.7074,0.351), not the plan's 0.3519,0.1781,0.7056,0.351.
   The handoff says `SC.BESPOKE` boxes are authoritative for crops. The module's box
   includes the open door slab out to core x 764. The other two boxes are identical in both.
3. **Depth field cast order.** `DF.field` picks `cast[(7j + 5i) % len]`. With the plan's
   seven marks, every lane would show a single mark over and over. `FIELD_ORDER` repeats the
   plan's roster over eight slots (claude twice, never adjacent). Every lane carries all
   seven marks, the chassis allows repeats, and the roster is the plan's list with no
   substitution.
