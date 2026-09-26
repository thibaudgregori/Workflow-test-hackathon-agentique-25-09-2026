# cursorworkspace — CUTOUT (TikTok) lane notes

Written by the CUTOUT author. The plan (`plans/cursorworkspace_plan.json`) is the
contract and this lane built it. Nothing below is a change to the plan; these are
the places the plan left a choice, plus the one thing the handoff offered and this
lane declined, with the reason.

## 1. NO POP-BEHIND, AND IT IS THE PLAN'S RULING RATHER THAN AN OMISSION

Cutout format law 16 puts a live app card across a depth lane "on the beat where
he NAMES the tool". Every tool this take names — Cursor, Google Workspace, Gmail,
Google Calendar, Google Drive, Google Sheets — is a STAGE subject mark.
ROUND-2/3 law 6 keeps the story's own subject mark out of the depth field (the
run-9 defect), and the plan says in as many words (`cast_note`,
`cutout_logo_lanes_note`) that all six are deliberately ABSENT from the lanes.
Not one of the six DEPTH marks (claude-code, codex, copilot, notion, slack,
airtable) is ever spoken, so a card carrying one would pop a live app window for
a tool the viewer has not heard of, on a beat about somebody else.

`per_lane_notes.cutout_tiktok` states it directly: *"THE POP-BEHIND: the plan
spends no beat on one."* The handoff (section 4 clause 8) offers the alternative
— spend the format's best detail on the chapter-1 tile arrivals at 7.70 / 8.86 /
10.76 and suppress the scene's own `popin` there. That was declined: those three
elements ARE the Gmail, Calendar and Drive subject tiles, so handing them to a
card crossing a depth lane is the same violation approached from the other end.

Same ruling, same reasoning and the same run: `kimifable_cutout` shipped without
one on 2026-09-08 for the identical reason. Recorded in the build as
`depth_field.pop_behind_why_none`.

## 2. THE SEAT IS THE SCENE'S OWN ORIGIN, NOT THE HANDOFF'S ~0.95

The handoff's section-2 gate-scaling table predicts the cutout will scale the
shared core by about 0.95 and warns that a 16 core-px gutter would then arrive at
15.2. That was the chassis's habit, not a measurement of THIS body.

`gen/cursorworkspace_cutout_envelope.py` sweeps every frame of the shipped alpha
and returns a stage zone of **192.0 … 811.4** — 619.4 px. The scene's CONTENT
BAND is 468.5 core px (98 … 566.5), so the largest legal k is 1.2879 and `place()`
caps it at **1.0**: a core is never blown up past the size it was authored at. At
k = 1 the band already lands legally where the plan put it, so `top` is the
scene's own `CANVAS_OFFSET` (192.0) and `left` is 0.0 — the cutout's canvas rects
ARE the scene's canvas rects.

That is not tidiness. `phone_test_page --plan` crops frame-normalised boxes, and a
re-centred core would hand the cold namer crops offset from the objects they are
supposed to contain — a rigged test, with the builder as the one who rigged it.
`place()` still returns the handoff's centring formula when the band does not fit.

Consequence: every gutter arrives at its authored size. The tightest non-block
pair in the piece is `key-cursor` ⟷ `read-arrow` at **27.92 core px = 27.92 canvas
px**, above the 24 px AIM rather than merely above the 16 px refusal, so the
handoff's 26.52 prediction is a number this session did not need.

## 3. THE PHONE TEST: FIVE ROUNDS, TWO MODELS, AND ONE HEDGE THAT IS THE MODEL

`review/phone_scores_cursorworkspace_cutout.json` carries every read, hedges
included. Summary: **ten reads across five independent rounds and two reader
models; zero readers named a different object.**

* object 0, *an arch bridge* — `bridge` **sure** 4/4.
* object 1, *a settings panel* — `toggle switch` 5/5, **sure 2/5**. All three
  hedges are the CONFIGURED reader model; both haiku rounds are sure.

This lane did NOT redraw the sealed module over that hedge, and the reason is
evidence rather than convenience:

* No reader has ever named a DIFFERENT object. Across the artwork seal's twelve
  reads of four drawings and this lane's five, the answer is `toggle switch`
  seventeen times out of seventeen. The plan's own named failures for this object
  (`open_questions` 6) are *a receipt*, *a calculator*, *a keyboard* and *a card*
  — nobody has said one.
* The hedge is diagnosed and the diagnosis is on the record. The artwork seal ran
  the same model over a CONTROL crop of the connector row alone
  (`review/proofs_cursorworkspace/diag/diag_row.json`) and it hedged there too, so
  the hedge is about UI mocks AS A CLASS, not about this drawing. The plan makes
  the reader model part of the evidence (`open_questions` 9) and this file names
  it per round.
* SCORE THE IDEA, NOT THE NOUN (Miguel, 2026-09-06). The switch is the drawn
  CONTENT of this settings panel and the single motion that IS the video's claim,
  so `toggle switch` is the same thing named by its subject.
* The split lane adjudicated the IDENTICAL pixels PASS on the identical reasoning
  (`review/phone_scores_cursorworkspace_split.json`) and has already staged
  `staging/youtube/cursorworkspace_split.mp4` against a hash-bound phone-pass.
  Redrawing the sealed module now would invalidate that pass and that render for a
  confidence score, not for an identification.

If the clerk disagrees, the remedy the handoff names is a repair round under
`production.py scene-lock` — a cross-lane action, not a quiet edit here.

## 4. NO DISAGREEMENT WITH THE PLAN

There is none to log. `open_doubts` is empty, the plan's two bespoke boxes and
their `t` values match the sealed module to **0.00 px and 0.00 s** (the 2026-09-08
reconstruction folded the built geometry in, so scene notes 1–6 are history), the
depth roster is `cutout_logo_lanes` verbatim and asserted equal at import time,
and the six stage marks are the plan's `marks` map verbatim.

## 5. WHAT THIS LANE INHERITED FROM THE SPLIT, ON PURPOSE

The LAW 37 / 39 / 40 / 41 / 42 / 4 / 6 / 46 / 47 asserts, the cue re-read and the
caption partitioner (including the orphan repartition that "to" needs on this
take) are the split lane's code, imported by copy into this generator. Both
masters seat the SAME module against the SAME plan on the SAME transcript, so
re-deriving them differently would only let two platforms disagree about one
video. What is authored here is everything the CUTOUT owns: the measured
envelope, the plate box and its origin, the depth field, the matte layer set, the
seat and the outro handle.
