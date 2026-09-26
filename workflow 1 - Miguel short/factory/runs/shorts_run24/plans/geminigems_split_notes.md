# geminigems — SPLIT LANE NOTES (YouTube)

**No disagreement with the plan.** The lane, the beats, the pictures, the
bespoke objects, the labels and their placement, the lifetimes, the connectors,
the blocks and the cast were built exactly as `plans/geminigems_plan.json`
writes them. Three things are recorded here because the CUTOUT author reads the
same scene module and will meet two of them.

## 1. The plan's bespoke `bbox` for the parcel is 10.0 px below the drawing

The plan carries NORMALISED canvas boxes sketched before the drawings existed
(the handoff says so in its section 9.4 and names `SC.BESPOKE` authoritative for
geometry). Measured at this lane's seat (k = 1.00, top = 192):

| object | plan norm y0..y1 | built canvas y0..y1 | max delta |
|---|---|---|---|
| a cracked gem | .2198 .. .3318 | 422.0 .. 637.0 | 0.1 px |
| a tied parcel | .2250 .. .3370 | 422.0 .. 637.0 | **10.04 px** |
| two people together | .2656 .. .3646 | 510.0 .. 700.0 | 0.05 px |
| a crowd of people | .2656 .. .3646 | 510.0 .. 700.0 | 0.05 px |

The parcel that was finally drawn shares the gem's own 260x215 authoring box and
its baseline, so it sits 10 px HIGHER than the sketch. I built the module's
geometry and set this lane's plan-comparison tolerance to 12 px with every delta
printed (`gen/_build_geminigems_split.json -> plan_geometry`), rather than moving
a sealed drawing to match a pre-drawing number. **The cutout should do the same
and cut its phone crops from `SC.BESPOKE` through its own k and origin.**

## 2. LAW 42 is read in its own letter, not in run 22's stricter copy

The gem is on screen 0.30 .. 10.46, which is 48.6 % of a 20.92 s take. LAW 42
says a chaptered build "must give every mark a finite `t_to` OR a name in
`board_anchors`", and that "anything visible for more than 40 % of the runtime
**without that declaration** is an error". The gem HAS a finite `t_to` at the
chapter-2 seam, and the plan's own lifetime table declares it that way
(`anchor: null`, `t_to: 10.46`). Run 22's split generator carried a flat 40 %
refusal that ignored the declaration clause; this lane implements the law as
written and prints every share plus each over-40 % mark's declaration.

## 3. `qc_pass --phone-at` takes NORMALISED boxes, not canvas px

`pipeline/phone_crops.py` defaults to `--space norm`, and `qc_pass` forwards
`--phone-at` without a space flag. A first render of this lane passed the plan's
CANVAS boxes and died on `object #0 has an empty box at phone scale:
[166050, 303840, 405, 720]` — one wasted render ($0.0081 Modal + $0.0318
watcher). The spec now carries the normalised `bbox` from
`gen/_geom_geminigems_split.json`. **The cutout and whiteboard lanes want the
same.**

## Nothing was repaired on the emitted tween list

Run 22's split had to raise element opacity on drawn strokes and close a broken
dasharray. Measured on this page: both drawn classes (`.crk`, `.cline`) carry
`stroke-opacity="0"` and no element `opacity`, and every one declares
`pathLength="100"`, so `draw()`'s fixed `strokeDasharray:100` IS each path's own
length. `module_bytes_changed: 0`, `strokes_revealed: 0`, `dashes_closed: 0`.
