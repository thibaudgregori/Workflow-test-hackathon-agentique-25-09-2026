---
name: feedback-thumbnail-logo-at-finger
description: "In personal YouTube thumbnails, the most important logo/element must sit where Miguel's finger is pointing"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 06d9f7d4-8700-4925-8734-696855da933b
  modified: 2026-08-05T20:12:43.621Z
---

In personal "face + logos" YouTube thumbnails, whatever the video is actually about (the hero logo) must be placed on the spot or side that Miguel's finger/hand is pointing at in the base photo. Secondary logos go on the opposite side.

**Why:** Miguel deliberately points in the base screenshot. A hero logo placed away from the point breaks the gesture and wastes the strongest visual cue in the frame.

**How to apply:** Check where the hand points in the base photo before choosing logo order. In `execution/generate_personal_thumbnail.py` placement follows registry `preferred_side` plus arg order (first logo = largest, gets the first matching slot). With an upward point on the right, set the hero logo's `preferred_side` to `right` and pass it FIRST so it lands in the `upper_right` slot (x 0.76, y 0.24), which sits directly above the finger. Pass the secondary logo by file path to bypass its own side preference and let it fall into `upper_left`. Related: [[feedback-add-missing-logos-to-assets]], [[feedback-hermes-use-nous-girl]], [[feedback-no-logo-outlines]].
