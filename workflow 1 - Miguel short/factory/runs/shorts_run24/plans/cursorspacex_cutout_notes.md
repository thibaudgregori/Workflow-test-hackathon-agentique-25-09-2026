# cursorspacex — CUTOUT author's notes

**No disagreement with the plan.** The lane, the beats, the one bespoke object,
the label, the lifetimes, the two connectors, the blocks, the two emphases and
the `cutout_logo_lanes` roster were built exactly as written, through the sealed
shared scene module. Two things are recorded here because they touched a
tolerance, not because the build departed from the plan.

1. **The plan's `bespoke_objects[0].bbox` is 4 px wider per side than the
   drawing.** Normalised it is `0.3676, 0.1583, 0.6324, 0.3104` = canvas
   `397.0, 303.9, 683.0, 596.0`; the module's own `SC.BESPOKE[0]["core"]` is
   `401, 112, 679, 404` = canvas `401, 304, 679, 596`. The two agree exactly in
   y and are both centred on x = 540 to 0.0 px; the difference is 4 px of
   horizontal pad around the assembly. Handoff section 9.5 makes the module's
   core box authoritative for geometry, so `compare_phone_boxes()` carries a
   stated 4.1 px tolerance plus a hard equality check on the centre, and the
   Phone Test was cut with `--plan` as instructed. A crop 8 px wider than the
   ink is a crop of the same object, and the cold reader named it on one round.

2. **The reusable media moved to the central library.** `assets/music/` and
   `assets/sfx/` no longer exist under the factory root; the bed and the three
   effects now resolve through `~/Documents/Workspace/assets/audio/{music,sfx}/
   shorts-factory/`, which is what PRODUCTION.md's "Reusable media source"
   section asks for. The run-22 generator's factory-local paths are stale and
   this build reads the library instead. Nothing about the mix changed: the same
   `bed_split_v2.mp3`, `whoosh.mp3`, `pop.mp3`, `click.mp3`.

**The plan's `open_doubts` was empty and nothing new was found.**
