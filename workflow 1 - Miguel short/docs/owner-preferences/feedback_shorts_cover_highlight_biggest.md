---
name: feedback_shorts_cover_highlight_biggest
description: Shorts covers (Instagram/TikTok, shorts-thumbnail-factory) must make the terracotta highlight line the biggest type and carry the video's keyword
metadata:
  type: feedback
---

Miguel, 2026-09-07, reviewing the Plants cover where the fitter had shrunk PASSION PROJECT to the smallest line: "I always want you to make the highlight the biggest word… I always want the big orange thing to have the bigger words and the keyword for the video."

**Why:** the orange block is what the eye lands on in the feed; the keyword belongs there at the largest size, set-up lines are secondary.
**How to apply:** the renderer (`execution/render_shorts_thumbnail.py`) caps other lines at 86% of the highlight and refuses a headline whose highlight is not the largest; write short keyword lines and shorter set-up lines. Same 1080x1920 master goes to both platforms; the 3:4 grid image is a preview only. See [[feedback_shorts_top_zone_graphic_chart]].

**Addendum 2026-09-07 (same day):** the highlight must also be SHORT. A long keyword line (IMPOSSIBLE, OPEN WEIGHTS, CODEX VOICE) fits only at 115-150 px, so the whole block shrinks and floats to the top with a hole above the face. Miguel flagged 04, 08, 12, 17, 19, 20 in the 29-cover collage and asked for "a word that has a similar number of characters at the bottom". Rule: highlight <= 8 characters, renderer refuses under 160 px (`HIGHLIGHT_MIN` in `execution/render_shorts_thumbnail.py`); move the long word into a set-up line and pick a short whole-word keyword (IMPOSSIBLE / TASKS BEFORE / BED).

**Addendum 2 (2026-09-07):** the pose must fill the gap. Arms-crossed and neutral-smile cutouts render bigger (head ~170 px higher than the finger poses), so Miguel wants them under the shorter headline blocks. Renderer now predicts the headline-to-head gap per pose, accepts only 70-155 px (`GAP_MIN/GAP_MAX`), and `--pose auto` picks a fitting pose; batch renders still spread poses by hand.

**Bank v7 (2026-09-07):** Miguel wants visual variety in the grid ("I don't look the same in every one"); different shirts are fine (dark, no readable slogans; the cap is the anchor). Three plush poses added from the Off-White tee shoot: plush-cheek, plush-shoulder, plush-profile. Wide poses get `cover_max_width` in the bank manifest (1180 for cheek/profile) so the plush bleeds ~49 px per side instead of shrinking the face; `render_shorts_cover_options.py` honours `subject_max_w` (default 984 unchanged).

**v7.1 (2026-09-07):** Miguel judged my cutouts "not very good" and was right (chair welded to the jaw, wrist halo, flattened plush feet). Precision cutout work goes to Astra via the Codex plugin, not to me inline; plush-profile deactivated (he dislikes the pose).

**Coherence incident (2026-09-07 evening):** cover 07 read "STOP COUNTING / TOKENS / PER TASK" for a video saying the opposite (compare cost per task, not per token); it was posted on TikTok/Instagram before Miguel caught it. Rule: read the three lines as ONE sentence and check it states the video's claim; renderer now requires `headline_sentence`, `video_claim`, `headline_matches_claim`; batches get an independent Astra re-read of every cover vs transcript. Covers cannot be changed after posting on TikTok (stitched frame) or Instagram (no cover update in the Graph API).

**Miguel, 2026-09-07 late:** no extra Astra audit call for covers/captions. The author (me) reads the complete transcript and writes cover text and captions that state the video's point; that read is the gate and must be respected every time. Keep the renderer's headline_sentence/video_claim fields.
