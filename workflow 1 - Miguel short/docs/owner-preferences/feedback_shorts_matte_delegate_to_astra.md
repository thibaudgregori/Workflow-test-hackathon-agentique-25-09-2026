---
name: feedback_shorts_matte_delegate_to_astra
description: "When a shorts cutout matte is rejected on sight, hand the whole matte to Codex Astra with frame evidence and rerun the standard selection-and-track lane; never hand-patch the alpha"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8d388668-a29a-48be-998b-e8df70b57f3f
  modified: 2026-09-14T09:23:29.172Z
---

When Miguel rejects a cutout matte ("poorly done", "cutting part of my face"), do not patch the alpha with luma or window rules and do not iterate by hand. Delegate the matte to Codex Astra (`codex:codex-rescue`, `--model gpt-6-astra --effort medium`, never CCX) with the frame-level evidence, and let it redraw the frame-0 contour and rerun the factory's own selection-and-track lane (SAM2 with no chair object and a temporal-1 finish was what worked on geo, run 19, 2026-09-14). Astra's sandbox has no network, so the parent session runs the Modal track, cold readers, phone-pass and render on its instructions.

**Why:** On geo I patched the alpha four times (chair cuts, chair reference, SAM2 chair guard); each fix passed every automated gate and each was rejected on sight, and the chair guard carved his face on 1331 of 1335 frames. Astra measured the defect first, fixed it through the standard lane, verified every frame, and Miguel called the result perfect on the first showing. His words: "start from the raw file again", "follow step 1 of the process and use all of the existing infrastructure", "he does the cutout perfectly".

**How to apply:** rejected matte = Astra owns it end to end; I only run network steps and open the result. Also open a stale export never: verify the package hash equals the staged render before opening. See [[project_fable5_video_factory]] and [[feedback_astra_via_codex_plugin]].
