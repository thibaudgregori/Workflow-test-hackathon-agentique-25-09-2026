# geminigems — CUTOUT author's notes

**No disagreement with the plan.** The lane, the beats, the four bespoke
objects, the five labels and their below/centred placement, the lifetimes, the
three connectors, the blocks, the one emphasis and the `cutout_logo_lanes`
roster were built exactly as written, through the sealed shared scene module
(`gen/geminigems_scene.py`, imported unmodified). The plan's `open_doubts` was
empty and nothing new was found. Four things are recorded here because they
touched a tolerance or a tool contract, not because the build departed from the
plan.

1. **`qc_pass --phone-at` takes NORMALISED boxes, not canvas pixels.** The
   first spec wrote the plan's canvas boxes and `phone_crops.py` refused the
   whole render with *"object #0 has an empty box at phone scale"*: its
   `--space` default is `norm`, so `410,422,670,637` was read as a fraction of
   the frame. The boxes are now the same objects' normalised `bbox`. One render
   was spent on it ($0.0137, 20:40 to 20:42); the second render passed every qc
   check. The `--at` boxes the Phone Test takes are the same normalised values.

2. **The background-haze gate is the instrument's own, not a stricter one.**
   The sibling cutout lane's build gated on `longest_run_s > 0.0`, which is the
   number *that* recording happened to have. This session has 2 frames over the
   1500 px floor inside ONE 0.2 s run at 2.0 s — the instant the stage-17 viewer
   already ran down to the source's own motion blur on the raised hand — so
   `hold` is FALSE against a `hold_seconds_limit` of 1.0 s. The gate now reads
   the metric's own contract (`hold` or a run past `hold_seconds_limit`), which
   is what `matte_review.py` itself judges on.

3. **The plan's `bespoke_objects[1].bbox` sits 10.0 px above the drawing.**
   Handoff section 9.4 says so explicitly: the plan's normalised boxes were
   sketched before the drawings existed, and the parcel that was finally made
   shares the gem's own 260x215 authoring box and baseline. The other three land
   inside 0.1 px. `SC.BESPOKE` is authoritative for geometry (handoff 9.4), the
   comparison is made in normalised space with the split's own 12 px tolerance,
   and the Phone Test was cut with `--plan` as instructed. Both lanes cut the
   same boxes, because this lane seats the core at the identity seat.

4. **The Gemini watcher never ran on the staged file.** `clerk_video_gemini.py`
   died on a 429 RESOURCE_EXHAUSTED (the org's monthly spending cap) while
   uploading its first window, so `review/cands_geminigems_cutout.json` does not
   exist for this render and `render_and_check` staged on qc alone under its own
   watcher-unavailable rule. `review/cands_geminigems_cutout.prior1.json` is a
   watcher pass from 18:42 against an EARLIER build of this lane (a session that
   was killed before it returned): 0 candidates, 0 blocking, $0.0242. It is
   corroboration, not this render's evidence — the clerk owes this file its own
   look.

**The reusable media is the central library's.** The bed and the three effects
resolve through `~/Documents/Workspace/assets/audio/{music,sfx}/shorts-factory/`
per PRODUCTION.md's "Reusable media source"; nothing changed in the mix.
