# kimifable — SPLIT (YouTube) author notes

**The plan was built as written.** Nothing in this file is an improvisation on
the argument: the lane, the nine beats, the four chapters and their seams, the
key term, all six written keys with their BELOW placement, both emphases, the
lifetimes, the blocks, the zero pointing cues, the cast that is not mine and the
1-of-3 that runs through every chapter are the plan's. What follows is the four
places where the built page and the plan's LETTER differ, each one recorded with
the measurement or the law that forced it, plus two observations the next author
should not have to re-derive.

Project: `shorts_run17/projects/kimifable_split`
Generator: `shorts_run17/gen/kimifable_gen.py`
Shared scene (SEALED, consumed, not touched): `shorts_run17/gen/kimifable_scene.py`

---

## 1. THE SEALED SCENE'S GEOMETRY WINS OVER THE PLAN'S `canvas_rects` — 30 rects

`assert_canvas_rects()` compares three sources on every build: the plan's
`canvas_rects`, the sealed module's own `SC.canvas_rects()`, and the inline
`left/top/width/height` of the emitted DOM. **The DOM matches the module to
0.0 px on every rect** (the 2026-09-05 rule, satisfied). The MODULE differs from
the PLAN on 30 rects, from 4.0 px (`bar-base`) to 91.0 px (`fable-coin-3`).

That is not a deviation this lane chose. The plan's own amendment records it:

> `plan.amendments[0].scale_note` — *"The sealed module draws at a LARGER scale
> than this plan's canvas_rects, because the draft's own numbers put the hook
> object on a phone at 66x39 px — under every crop that has ever passed a cold
> read here, which the draft itself flagged as the run's likeliest [risk]."*

and three of the deltas are the plan's own three amended drawings: the tag lies
flat with no cord (`kimi-tag`, `fable-tag`, the coins now in one row inside the
tag instead of stacked beside it), the scorecard gained its clipboard
(`scorecard` 316 → 632 instead of 320 → 600, the clip standing above the board's
top edge), and the stack of three windows became one folder (`sheet-stack`).

**The rule I applied:** the module is bound by
`review/artwork_pass_kimifable.json` to three independent cold-read rounds on
these exact drawings. Building the plan's rects would mean drawing a board that
was never read. Every delta is in `gen/_build_kimifable.json` →
`formats.split.canvas_rects.deviations_from_plan`, with the plan rect, the built
rect and the pixel delta, so a clerk sees the arithmetic rather than a claim.

The WHITEBOARD builds from the plan file, which the plan's amendment already
updated to the sealed drawings, so the three platforms still argue one picture.

## 2. THE PLAN'S CAPTION CLEARANCE WAS DERIVED AGAINST A 960 SEAT; THE SPLIT'S SEAM IS 862.5

`plan.shared_layout_note` and `plan.per_lane_notes.split_youtube` both compute
the clearance under the caption pill as `960 − 114.59/2 = 902.705`. **The
published classic split does not seat the pill at 960.** The face plate is
`face_bottom_hd.mp4`, 1080x1058, so the seam — and the pill centre — is
`1920 − 1057.5 = 862.5`, which is the number every shipped split in this factory
uses and the one that puts the pill centre at 44.9 % of frame height (LAW 30's
"the published classic split already complies (pill centre ~44%)").

So the real numbers, measured by `guard_core_band()` on the page that renders:

| | plan's assumption | what renders |
|---|---|---|
| pill centre | 960 | **862.5** |
| pill top (114.59 height, never the frozen 108.2 seat) | 902.705 | **805.21** |
| lowest ink | canvas 772 (plan's rects) | **canvas 746** (`key-build` bottom) |
| clearance | 130.7 px | **59.21 px** |

59.21 px is comfortably over the 24 px THE SEAM IS SACRED floor, so this is a
recorded difference and not a defect — but the plan's 130.7 px is not a number
any lane should quote, and the cutout author should derive its own clearance from
its own envelope rather than from either figure.

## 3. LAW 40 REPORTS SKIP, AND `visual_laws` HAS AN EMPTY NODE LIST ON THIS PAGE

The brief asks every connector to declare `data-connect-to` /
`data-anchor-side` / `data-anchor-fraction` / `data-check-at`, and every emphasis
to declare `data-emphasis` / `data-emphasis-target` / `data-check-at`. **This
page emits none of those attributes, and that is correct rather than missing.**

* **No connector exists.** The plan's two cords went with the hung tag
  (`plan.connectors_note`, amended 2026-09-08: independent readers named a peaked
  box with a punched hole on a string a *birdhouse*, twice). `SC.CONNECTORS` is
  empty, `SC.assert_no_connectors()` runs inside `build()`, and
  `assert_no_connector_law()` re-asserts it on the emitted string and also proves
  the two vestigial `cordL`/`cordR` cue entries reference nothing. No target
  receives an arrow, so LAW 40's letter does not bind.
* **Both emphases are PANEL BORDER FLIPS** on `kimi-tile` (0.939 s, "beat") and
  `kimi-tile3` (25.600 s, "viable") — LAW 38 rule 2, DOM lane, the target's OWN
  border tweened `rgba(17,17,17,0.16)` → `rgb(221,114,89)` over 0.38 s. The
  emphasis IS the target, so a `data-emphasis` declaration would be measured for
  4 px of clearance from itself and for a colour differing from its own ink —
  two manufactured violations of a rule the flip does not break. The handoff
  says so in as many words (§5, last bullet: *"Do not add
  `data-emphasis="box"` to a tile"*). `assert_emphasis_law()` asserts both flips
  instead, against their targets' lifetimes.

`pipeline/visual_laws.py`'s `CHECK_JS` selects
`[data-connect-to],[data-emphasis],.connector,.arrow`; on this page that
selector matches zero elements, which is why `geometry_audit --strict` returns
**0 errors / 0 warnings** rather than a list of undeclared anchors.

## 4. THE PHONE TEST CROPS COME FROM `--geom`, NEVER `--plan`

`phone_test_page.py`'s precedence is `--at` > `--plan` > `--geom`. Passing
`--plan` here would crop the plan's stale boxes at the plan's
entrance-completion instants and hand a cold namer pictures of a board this
build never drew. Two reasons, both recorded in
`formats.split.phone_test_vs_plan`:

1. the bboxes predate the approved scale rebuild (note 1 above) — e.g. the price
   tag is 112x51 phone px as built against 66x39 as planned;
2. `SC.BESPOKE`'s `t` values are HELD instants (3.00 / 10.00 / 15.60 / 24.60),
   never the last frame of an entrance, so the reader judges the object and not
   the animation;

and the plan's list is also in a **different order** from the scene's (the plan
has website-layout second, the scene has the scorecard second), so the compare is
matched by NAME, never by index.

---

## Two things the next author should not re-derive

**A. The score bars are the only declared rects authored inside a parent.**
`score-bar-1..3` sit at `left:0;top:0` inside their own `score-row-i`, whose
origin is `(ROW_X, by − BAR_H)`. Any tool that reads inline `left/top` off the
DOM and compares it to `SC.canvas_rects()` must add that offset or it will
report a 376 px error on a box that is exactly right. Everything else in this
scene is a direct child of `#core`.

**B. The take's two witnesses disagree, and the cut is still correct.**
`prep/kimifable.json → stages.cut.corroboration` reads
`marker: "bound"`, **`gap: "DISAGREES"`**, `witnessed: true`,
`allow_uncorroborated: false`; the keeper opens at raw word 118 / 93.2 s, 138 of
256 raw words, 8 openings seen. The cut gate passed it
(`review/agent_done_gate_cut_kimifable.json`: `status ok`,
`override_used false`), and `clean_tokens()` re-verifies on the tight
transcript that the opening key "Kimi K3 just beat" occurs exactly once, that no
word is partial, and that LAW 47's tail is inside `last word + 0.20 s + one
frame`. It is recorded here because a disagreeing witness is worth a line in the
paperwork even when the take is clean.

---

## Prep numbers this lane consumed (all markers status `ok`)

| stage | wall | the numbers |
|---|---|---|
| cut | 76.5 s | master 38.12 s, tight audio 38.098 s, `analysis_wav_written: false` (48 kHz only, by design) |
| take | — | raw word 118 / 93.2 s, 138 of 256 raw words, 8 openings; marker **bound**, gap **DISAGREES**, witnessed true |
| plate | 160.4 s | crop `2440x1830+610+236`, `scale_k` 0.491803, head 452.1 canvas px, **over-wide TRUE**, `plate_box` 1320x990 at (−120, 930), `centred: false` |
| prompt0 | 47.0 s | `wing_review` true, `wing_cut_applied` false (the instrument abstained) |
| selection | 88.3 s | `matting/kimifable/selection.json` |
| track | 89.4 s | matanyone2, **$0.02283** |
| ship | 102.0 s | 953 frames 1320x990 @25, soft alpha, rim 7, fractional alpha 18,428,379 px, min person fraction 0.4287, **$0.03984** |
| cues | 0.0 s | **cue_count 0** — LAW 37 re-run agrees, no source card anywhere |

The plate, prompt0, selection, track and ship stages serve the CUTOUT. This lane
consumed the cut and nothing else, and made no Modal call except the render.

---

## RENDER, AND THE ONE THING THE CLERK MUST BE TOLD

`render_and_check.py --stage`, one job, one round, no fix rounds.

| | |
|---|---|
| render | 1080x1920, 953 frames @25, h264, 38.141 s, **86.2 s wall, $0.0127** (container `3e1f5770`) |
| `qc_pass` | **PASS in 20.6 s** — 12 checks, 0 failed |
| staged | `staging/youtube/kimifable_split.mp4` |

qc verdicts: `decoded_blank_frames` PASS · `zero_ink_law` PASS ·
`clip_coverage_page` PASS · `double_exposure` REPORTED (ok, the only zero-ink
instants are the three chapter wipes and the outro sheet, which are the erases
themselves) · `face_centring` PASS (band warning 4.72 % at 37.0 s, warning level
on the split's fixed approved crop) · `pill_canon_rendered` PASS ·
`gate1_geometry_audit` PASS · `gate2_frame_review` PASS ·
`gate3_gemini_describe` REPORTED · `audio_guards` PASS (treble delta −0.19 dB
against the voice master, tolerance 6; speech margin 19.33 dB p85−p15 @33 ms
s16le; A/V lag 0 ms, r 0.9956) · `contact_sheet` PASS · `phone_crops` PASS.

**THERE IS NO `review/cands_kimifable_split.json`, AND IT IS NOT TO BE
BACKFILLED.** The Gemini watcher and Gate 3 both returned
`429 RESOURCE_EXHAUSTED — your project has exceeded its monthly spending cap`.
`render_and_check` recorded `watch_unavailable` and staged on qc alone
(`watcher UNAVAILABLE (Gemini spending cap) — staged on qc alone; the clerk
decodes it`). Per RUN-13 REVIEW CHANGES §1: *"A missing cands file is reported,
never backfilled. That render was watched by nothing; say so and rule on your
own decode."* So this file was watched by nothing and the clerk rules on its own
decode. Gate 3 is advisory anyway (2026-09-05).
