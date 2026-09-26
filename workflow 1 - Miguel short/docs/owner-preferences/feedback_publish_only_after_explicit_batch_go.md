---
name: feedback_publish_only_after_explicit_batch_go
description: "Never create or schedule a social post until Miguel has seen the exact list (titles, platforms, times) and answered yes to that list; 'you can start pushing' inside a planning message is not that yes (2026-09-07 incident: 6 posts scheduled, 1 YouTube Short went public for a minute, all retracted)"
metadata:
  type: feedback
---

2026-09-07: Miguel wrote "let's start uploading… find the ones that have different themes so I can put them one-to-one… you can start pushing them… let me know which one you think is the better first video." I selected five and ran the publish script immediately. He replied: "did you literally just start uploading them without my fucking permission?" Six Zernio posts existed; the YouTube Short DMhGl5xXDuo was public for about a minute before I retracted it; the five scheduled posts were deleted before going live.

**Why:** a message that asks for a selection and a recommendation is a request to see the plan, even when it also says "you can start". Posting is outward-facing and not fully reversible (YouTube keeps the upload in history; TikTok posts cannot be deleted via API).
**How to apply:** publishing is a two-step: (1) present the exact batch, titles, platforms, times, first video; (2) create posts only after a yes to that list, in a message of its own. Same for scheduling. Applies to every Zernio, YouTube or LinkedIn write, and to subagents running the publish script. See [[feedback_shorts_publish_captions_tone]].

**Follow-up incident, same day:** killing a publish run mid-upload does not cancel YouTube's resumable upload; two interrupted uploads (Harness, DeepSeek) completed server-side and went public at their publishAt with the old titles, unseen by the sync. Deleted on Miguel's word. Rule: after any stopped run, execute `pipeline/publish/reconcile_youtube.py`; never assume a kill undid a platform write.
