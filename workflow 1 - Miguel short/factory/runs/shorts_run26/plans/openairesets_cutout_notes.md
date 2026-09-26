# openairesets: cutout author notes

The cutout builds the plan and consumes the sealed scene unchanged on disk
(`gen/openairesets_scene.py`, sha256 422919c7...). It imports the split
generator's helpers, so it carries the same two law-forced departures on the
EMITTED page that `plans/openairesets_split_notes.md` records:

1. ` / MONTH` lands on the start of "month" (5.52) instead of "per" (5.36): LAW 24, no peek-ahead.
2. The emphasis box is inked TERRA_L instead of TERRA, because the sand is TERRA and
   `geometry_audit.py --strict` refuses an emphasis in its target's own ink.

One cutout-only layout decision, not a plan departure: the logo lanes sit above the
scene section in the DOM. The module parks its opaque outro sheet below the core
(canvas y > 792) until 16.08, and on the first build the mid and near lanes vanished
under it. With the lanes above the scene they show from HOOK_CLEAR (2.50 s) on.
