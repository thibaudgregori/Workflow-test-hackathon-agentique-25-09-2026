---
name: project_shorts_factory_stage_register
description: The shorts factory has a permanent numbered stage register (STAGES.md) guarded by a test; workflow edits must update it, and STANDARD/workflow edits mid-run invalidate sealed stage caches
metadata:
  type: project
---

Created 2026-09-06 at Miguel's request ("a standardized way of laying out the workflow stages… I liked when it was very organized"): `projects/personal/content/shorts-factory/STAGES.md` = 16 numbered stages (Intake, Cut, Plate, Selection, Matte, Cues, Plan, Artwork, Lanes, Build-green, Cold reader, Render+check, Repair, Clerk, Deliver, Publish), numbers permanent, retired stages keep their number. `pipeline/test_stage_register.py` fails when a workflow phase or agent label prefix has no row.

**Why:** the stage list drifted across the workflow script, the skill prose and STANDARD; one owner keeps it organized.
**How to apply:** any change to `.claude/workflows/daily-shorts.js` updates STAGES.md in the same commit and the test is run. Never edit STANDARD.md or the workflow script while a run is live: `pipeline/stage_cache.py` fingerprints both and a resume then re-plans from zero (re-seal with `stage_cache.py save` if it happens). See [[feedback_shorts_top_zone_graphic_chart]] and [[project_fable5_video_factory]].

## Index notes (moved from MEMORY.md 2026-09-23)

- STANDARD/workflow edits during a run invalidate every sealed stage cache
