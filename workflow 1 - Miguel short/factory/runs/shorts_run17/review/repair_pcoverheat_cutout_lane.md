# pcoverheat, cutout lane — repair round, 2026-09-08

**The lane held on a rule, not on a drawing.** `production.py::consensus` refused
objects 1 and 3 with *"only 2 of 6 independent readers were sure"*, so the author
correctly wrote `verdict: FAIL` into `phone_scores_pcoverheat_cutout.json`,
`phone-pass` refused the project, and the lane returned `staged: ""`.

Object 1 is `phone_pcoverheat_cutout/01.png`, an arrow onto a bar. **Six of six**
independent readers named it a download arrow. Zero different. The same drawing
sealed at the artwork seat hours earlier on `sure` 3 of 6
(`artwork_scores_pcoverheat.json`) — nothing about the ink changed between the two
seats, only which way a noisy flag landed four times.

## What changed at the source

* `pipeline/production.py::consensus` — the half-must-be-`sure` line is replaced by
  *half the reads must have REACHED the object* (`intended`/`synonym`), plus a floor
  of **one** reader `sure` of a name that reached it in five words or fewer. The
  misread rule is untouched and still fails a second different name first.
* `pipeline/production.py::read_rows` — a reader answer over five words is stamped
  `over_five_words` and priced in `consensus` instead of refusing the whole round.
* `STANDARD.md` → THE PHONE TEST, and the lane brief in `daily-shorts.js`.
* Regression: `pipeline/prep/test_regressions_2026_09_04.py`, four checks asserted
  on this recording's six rounds (20 → 24 checks, all clear).

## For the re-run author

The six rounds on disk are good evidence and do not need re-dispatching. **Re-rule
the scoring rows under the rule above** — the `verdict` column still carries the
HOLD written under the old line — and score each read's `match` as
intended | synonym | different. Under the new rule this recording's four objects
measure `agreed` 5, 6, 6, 5 of 6 with `sure_agreed` 5, 2, 6, 1.
