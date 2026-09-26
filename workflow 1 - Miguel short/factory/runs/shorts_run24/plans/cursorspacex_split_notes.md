# cursorspacex — SPLIT lane notes (YouTube)

Author: the split author. The plan was built as written; nothing in it was
improvised around. Two REPORTED disagreements, neither of which changes what the
viewer sees, and one law-forced departure that the artwork author had already
taken and written up.

## 1. The plan's bespoke bbox is 4.0 px wider on x than the drawing

`plans/cursorspacex_plan.json -> bespoke_objects[0].bbox` is
`[0.3676, 0.1583, 0.6324, 0.3104]`, i.e. canvas x 397.0 .. 683.0. The sealed
drawing's own box is `SC.BESPOKE[0]["core"] = (401, 112, 679, 404)`, i.e. canvas
x 401.0 .. 679.0. y agrees to 0.03 px; x is 4.0 px wider on each side.

Handoff section 9.5 states that "the plan's normalised box was updated to match".
That is true of y and not of x.

What I did: built the plan, cut the Phone Test with `--plan` as instructed, and
REPORTED the delta instead of refusing it. 4.0 canvas px is 1.5 px at 405x720 —
it is padding around the same sealed ink, not a different object, and the
confirmation reader named the object correctly through it. `compare_phone_boxes`
carries the measurement and refuses anything over 6 px.

What I would have done: had the plan and the drawing disagreed by enough to
change the crop's content, I would have held the lane rather than choosing a
box. They do not.

## 2. `MATTES_FINAL.md` does not exist in this run

The task text names `runs/shorts_run24/MATTES_FINAL.md` as the marker that makes
the mattes consumed-and-never-redone. There is no such file. It makes no
difference to this lane — the split needs the CUT and nothing else and made no
Modal call of any kind — but the CUTOUT author should know that the marker is
absent while `prep/stages/cursorspacex.ship.json` is `ok` with
`review_status: "needs_final_visual_review"`. That is stage 17's
(`matte_review`) subject, not mine, and I did not touch the matte, the
selection, the plate or the alpha.

## 3. Law-forced departures already taken by the artwork author

Handoff section 9 lists five. All five are reproduced here unchanged because
the split consumes the module and mutates nothing. The two that a law forced
rather than arithmetic:

* **9.1** — the retired flag is a SOLID stroke at falling opacity
  (1.00 -> 0.74 -> 0.55 -> 0.40) and not the plan's "broken outline", because a
  live `stroke-dasharray` removes an element from Gate 1's checks and the dash
  law then owns the reveal (LAW 44, and the run-22 dash defect). This build
  asserts the absence rather than assuming it: `assert_no_hidden_ink` refuses
  the page if `strokeDasharray`, `strokeDashoffset` or `strokeOpacity` appears
  anywhere in the emitted scene, and proves that every id authored at
  `opacity:0` is raised by a tween. 0 repairs were needed, 0 module bytes
  changed — unlike runs 21 and 22, this scene fades its ink in and never draws
  it with a dash.
* **9.4** — the outro sheet rises at 18.30 and not on the sign-off's first word
  (17.88), because the Grok tile only lands at 17.44 and raising the sheet on
  "Now" would cover the finished claim 0.44 s after it completed. The authored
  cue sits inside the 1.0 s LABEL_WINDOW of the spoken "Now," (17.88 .. 18.96)
  and is verified there, not assumed.

## 4. Things this lane owns and decided, for the cutout author's record

* k = 1.00, left = 0.0, top = 192.0 — the handoff's own numbers, nothing raised.
* Connector check instants: `conn-spacex` 17.20, `conn-grok` 18.10. Both are
  HELD (stroke complete 15.02 and 17.88, targets alive, both before the sheet).
  The cutout will need its own instants only if it re-times; the geometry is
  identical at k = 1.00.
* NO `data-emphasis` is stamped on this page. Both emphases are LAW 38 rule 2
  panel border flips on the cards' own strokes: they add no element, so there
  is nothing in the DOM to declare, and declaring a target as its own
  `data-emphasis-target` would make `visual_laws.CHECK_JS` compare an element's
  ink with itself. `geometry_audit --strict` returns 0 errors / 0 warnings on
  that reading.
