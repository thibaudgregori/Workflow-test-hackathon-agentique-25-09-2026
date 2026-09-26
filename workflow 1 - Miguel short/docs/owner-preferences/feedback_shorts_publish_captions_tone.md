---
name: feedback_shorts_publish_captions_tone
description: "Shorts publishing (Instagram + TikTok via Zernio, YouTube via uploader) must auto-generate description/caption, tags/hashtags and cover per platform, in Miguel's own tone of voice, with length adapting to the content"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1ad6e9a8-54c1-4a5a-a394-38253392daad
  modified: 2026-09-07T13:26:51.594Z
---

Miguel, 2026-09-07: "In the upload process can you also take into consideration that we wanted to have a description, tags, and everything automated to be included? Make sure to stay truthful to my tone of voice if possible please. Yep both for Instagram and TikTok. The length of the description can change according to what is being done."

**Why:** publishing a short is caption + tags + cover + timing, not just the file; a generic caption reads like a bot.
**How to apply:** the publish queue writes, per short, a TikTok caption (≤2,200 chars, hashtags inline), an Instagram caption (≤2,200, ≤30 hashtags, hashtag block optionally in the first comment) and the YouTube description/tags through the uploader, all sourced from the short's tight transcript and plan; tone comes from Miguel's own past captions and spoken lines (short, direct, plain words, LatAm Spanish rules when Spanish); length scales with what the short actually says (a one-claim short gets one line plus tags, a how-to gets steps). Covers per [[feedback_shorts_cover_highlight_biggest]]. Scheduling is Zernio's scheduler (scheduledFor / queue slots); YouTube native publishAt. Track everything in the Notion inbox row (per-platform status + URLs). See [[project_fable5_video_factory]].

**Voice profile written 2026-09-07** from all 74 available transcripts + 45 shipped YouTube descriptions: `projects/personal/content/shorts-factory/pipeline/publish/VOICE.md` (hook claim first, plain-words proof with a named example, numbers as the argument, second-person takeaway, fixed follow CTA, 2-sentence description template, per-platform hashtag counts). Captions must be generated from that file, not from memory.

## Index notes (moved from MEMORY.md 2026-09-23)

- length adapts to content, tone from his own captions; Zernio scheduler for IG/TT
