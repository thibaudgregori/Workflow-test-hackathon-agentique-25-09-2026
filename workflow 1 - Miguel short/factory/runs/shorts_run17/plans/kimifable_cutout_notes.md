# kimifable — CUTOUT lane notes (TikTok, @migueltorrez.ai)

Written by the cutout author. **The plan was built as written.** Nothing here is
a creative change to `plans/kimifable_plan.json` or to the sealed shared scene
`gen/kimifable_scene.py`; the four entries below are the only places where this
lane had to make a call the plan does not spell out, and each one is recorded so
the clerk and the artwork author can see the reasoning instead of guessing at it.

---

## 1. NO POP-BEHIND — the plan's ruling, and a live tension with a chassis law

`formats/cutout/CHASSIS.md` format law 16 says the pop-behind IS part of the
format: *"a live app card crosses a depth lane at his shoulder on the beat where
he names the tool"*, and *"a cutout without it is missing the detail Miguel
named"*.

This video has no legal beat for it. The only two tools the take names are
**Kimi K3** and **Fable 5**, and both are STAGE subject marks — ROUND-2/3 law 6
keeps the story's own subject mark out of the depth field (the run-9 defect), and
the plan says in as many words that `kimi` and `claude` are *"deliberately ABSENT
from the lanes"*. Not one of the six depth marks (`openai`, `gemini`, `deepseek`,
`qwen`, `mistral`, `grok`) is ever spoken, so a card carrying one would pop a live
app window for a tool the viewer has not heard of, on a beat that is about
somebody else.

The plan declares no pop-behind window and the plan is the contract, so this
build ships without one. **What I would have done if the plan had asked:** seat
the crossing on *"AI models have very specific domains"* (8.24–9.68), the one
sentence that is about the category rather than about either subject — a
`gemini` or `deepseek` card crossing the mid lane there argues the sentence
instead of contradicting it. Recorded for Miguel, not acted on.

## 2. `stamp_meter_id` — a lane stamp on this lane's own page, not a scene edit

`cutout_core.guard_edge_fade` (GLOBAL LAW 8) exempts a rounded meter's inner clip
by construction — *"fading it would fade the pill's own cap"* — and it detects a
meter **structurally**, by the `<track id>-fill` child the format's own meters
emit, *"so a new meter never has to be added to a list"*.

The sealed scene names this video's cost meter `build-track` and its fill
`build-fill`, one character short of that convention, so the detector missed a
meter that is unmistakably one: a 680×60 rounded track at canvas x 200…880 with
`overflow:hidden`, holding a single pill-shaped fill with `min-width` = the track
height (LAW 23 / cutout law 14). It touches no frame edge — it is **200 px clear
of both** — so there is nothing for GLOBAL LAW 8 to protect, and a mask there
would fade the pill's own cap.

`prerender_check` calls `guard_edge_fade(html)` with no exemption channel, so an
`exempt={"build-track"}` argument in my generator would have passed my build and
failed the gate. **The scene is not this lane's file** — it is SEALED and it is
the split's page too, and the guard is cutout-only — so the id is renamed on
**this lane's own emitted page** (markup and the scene's own tween selector, both
substitutions asserted), exactly the shape run 16 used for `stamp_visual_contract`.
Recorded so the artwork author can fold `build-track-fill` into the module for the
next run; nothing about the drawing, the geometry or the animation changes.

## 3. The Phone Test is administered on `--geom`, not on `--plan`

`phone_test_page.py --plan` would crop the plan's `bespoke_objects` boxes. The
**sealed module deliberately draws at a larger scale than those boxes**, and the
plan itself records why (`amendments[0].scale_note`: the draft's numbers put the
hook object on a phone at 66×39 px, under every crop that has ever passed a cold
read here) and says in as many words that *"a clerk should not read the scale
difference as a deviation"*. Cropping the draft boxes would hand the cold namer
four windows offset from the objects they are supposed to contain — a rigged
test, and the builder would be the one who rigged it. So the crops come from
`gen/_geom_kimifable_cutout.json`, whose boxes are `SC.BESPOKE` mapped through
this build's own seat (k = 1.0, left = 0, top = 192 — so they ARE the scene's
canvas rects). Asserted in `assert_phone_boxes`.

## 4. Object 0's cold reads, in full, including the read the tool could not take

Four full independent rounds are the scored evidence. A fifth dispatch (`round3`)
went to **object 0 only**, as a confirmation read after round 1 hedged, and
`production.read_rows` refuses an evidence round that does not answer every
object — so it is not in the hashed evidence set. It is **not** dropped:

| object | intended | round1 | round2 | round3 | round4 | round5 |
|---|---|---|---|---|---|---|
| 0 | a price tag | luggage tag *(unsure)* | price tag *(sure)* | luggage tag *(unsure)* | price tag *(sure)* | price tag *(sure)* |
| 1 | a benchmark scorecard | clipboard *(sure)* | clipboard *(sure)* | — | clipboard *(sure)* | clipboard *(sure)* |
| 2 | a website layout | web browser window *(sure)* | web browser window *(sure)* | — | web browser window *(sure)* | browser window *(sure)* |
| 3 | a folder of designs | file folder *(sure)* | file folder *(sure)* | — | file folder *(sure)* | file folder *(sure)* |

Object 0 over **all five** reads: **0 different, 3 of 5 sure** — which passes
`production.consensus`' own arithmetic (`3*2 >= 5`) on the larger denominator as
well as on the scored four. Excluding round 3 was not allowed to change the
verdict and it does not. *"luggage tag"* is a sibling noun of the same thing and
the plan's own re-read guidance lists it as a passing answer; the hedge is the
instrument, not the drawing — `production.consensus` records this exact
sure/unsure/unsure/sure pattern on byte-identical crops as the reason one draw is
not a measurement. The crop is 112×51 against the artwork seal's own 113×51 and
is otherwise the same pixels.
