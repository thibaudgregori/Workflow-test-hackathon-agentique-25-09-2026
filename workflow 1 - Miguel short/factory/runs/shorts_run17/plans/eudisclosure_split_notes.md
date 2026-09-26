# eudisclosure — SPLIT lane notes (YouTube, classic 50/50)

Written by the SPLIT author. `plans/eudisclosure_plan.json` is the contract and
`plans/eudisclosure_scene_handoff.md` is the artwork author's seating brief;
this file is the exception report and the repair-round record.

**OUTCOME: HOLD. Nothing is staged.** The build is green on every page check —
`prerender_check` PASS, `geometry_audit --strict` 0 errors / 0 warnings — and
the phone gate refuses bespoke object 03. `production.py phone-pass` was run
and returned `A failed object cannot be rendered`, so no approval record exists
and `render_and_check` would refuse. That is the correct behaviour and it was
not worked around.

---

## 1. WHERE THIS BUILD DEPARTS FROM THE PLAN'S LETTER

### 1.1 The phone test crops from `--geom`, not from `--plan`

The brief says to pass `--plan plans/eudisclosure_plan.json` to
`phone_test_page.py`. This build passes `--geom gen/_geom_eudisclosure.json`
instead, and the reason is in the artwork author's own exception report
(`plans/eudisclosure_scene_notes.md` s1): the plan's `bespoke_objects` bboxes
put the three objects on a phone at **40 x 40, 46 x 36 and 103 x 16 px**, and
the scene that was actually built — and sealed — rebuilt the whole composition
at legible scale, so the built boxes are **58 x 49, 66 x 57 and 99 x 28**.
`phone_test_page`'s documented precedence is `--plan` over `--geom`, so passing
`--plan` would have cropped stale rectangles at entrance-completion instants
and handed a cold namer pictures of a board this build never drew. The deltas
are recorded in `gen/_build_eudisclosure.json -> phone_test_vs_plan` rather
than hidden. This is the same call run 16's split author made for the same
reason.

### 1.2 The connector declarations are stamped on the emitted string

`visual_laws.CHECK_JS` requires `data-anchor-side` / `data-anchor-fraction` /
`data-check-at` on every element carrying `data-connect-to`. The shared scene
emits `data-connect-to` and `data-overlap-ok` only, and the handoff forbids
mutating the module while the cutout author reads it, so the three attributes
are stamped onto the emitted HTML in `declare_contracts()`. No geometry moves;
the side is the side the scene's own `anchor_points()` call used, the fraction
is derived off the target's declared box (both 0.5000, both proved to sit on
the edge to 1e-6), and the check instants (12.40 and 13.25) are asserted to be
completed, still-visible states inside both the connector's and the target's
lifetimes.

### 1.3 No `data-emphasis` element exists, deliberately

Both emphasis targets (`image-card`, `tag-modified`) are DRAWN PANELS, so
LAW 38 rule 2's boxing is the PANEL BORDER FLIP — the target's own border
tweened to terracotta. The emphasis IS the target, so declaring it would be
measured for 4 px clearance from itself and for a colour differing from its own
ink: two violations of a rule the flip does not break. The handoff (§6 clause 5)
names this explicitly. Both flips are asserted in `assert_emphasis_law` instead.

### 1.4 The caption pill centre is the seam, not canvas 960

The plan's `shared_layout_note` derives its bottom clearance against a pill top
of 902.705 (a pill centred at canvas 960). The split's caption seat IS THE SEAM,
862.5, so the pill top that renders is **805.21** and the clearance under the
lowest ink (canvas 768) is **37.21 px**, not 196.7. Still clear, still derived
with the pill height that RENDERS (114.59) rather than the frozen 108.2 seat
constant, and asserted in `guard_core_band`. Recorded because the plan's number
would mislead the next reader.

### 1.5 The cold reader ran on a substitute model

`cold_read.py` defaults to the configured reader model. Plain `claude -p`
returned `You've reached your Fable limit` on every attempt across this session,
so the reader that sealed this scene four hours ago could not be used. See §3.

Everything else is built as the plan wrote it: the lane, the seven beats, the
pictures, the three bespoke objects, the seven keys and their BELOW placement,
the lifetimes and the three declared anchors, the two connectors, the nine
blocks, the two emphases, the three chapters and both seams.

---

## 2. THE LANE, QUOTED

    "lane": "diagram build"

and the plan's own justification, verbatim:

> The script names no product at all, so there is nothing for icon
> choreography to choreograph and no number for a counter, but it does describe
> a MECHANISM that widens twice - a disclosure mark you must apply, the two
> labels an image has to choose between, and the hair-thin edit that still trips
> it - so the honest lane is the one that assembles that mechanism on screen and
> extends it.

The intake row suggested "steps & checklist"; the plan overrode it and owned the
override. This lane builds the plan.

---

## 3. THE READER INSTRUMENT, AND WHY IT WAS CALIBRATED BEFORE IT WAS TRUSTED

The first dispatch failed outright: three `claude -p exited 1: You've reached
your Fable limit`. A capped reader is not a read, and `cold_read.py` refuses
those rows rather than scoring them.

`claude-opus-4-5` answered, and named the three objects **binder clip / coat
hanger / key**. Before treating that as a verdict on the drawings, it was run on
the ARTWORK stage's own sealed crops — the ones its four sealed rounds named
`rubber stamp`, `picture frame` and `brightness slider`, every one *sure*:

| reader | sealed 01 | sealed 02 | sealed 03 |
|---|---|---|---|
| `claude-opus-4-5` | rubber stamp *sure* | **coffee mug** *sure* | **key** *sure* |
| `claude-opus-4-1` (→ Opus 5) | rubber stamp *sure* | framed landscape picture *sure* | brightness dimmer slider control **unsure** |
| `claude-opus-5[1m]` | rubber stamp *sure* | framed landscape picture *sure* | brightness slider **unsure** |
| `claude-opus-5` | rubber stamp *sure* | framed picture of mountain *sure* | brightness slider control **unsure** |

`claude-opus-4-5` fails two of three proven objects and was discarded; its
answers are kept at `review/phone_reader_eudisclosure_split.uncalibrated_opus45.json`
so the discard is on the record rather than in my head. The three remaining
aliases are calibrated on the stamp and the photo — and **every one of them
hedges on the sealed slider**. That is the single most important measurement in
this file: the confidence token for this object class is a property of today's
instrument, established on a known-good control, and it is why §5 does not read
"the slider is a bad drawing" full stop.

Evidence: `review/reader_instrument_control_eudisclosure_split.json`,
`review/reader_instrument_control_eudisclosure_split_calibrated.json`.

---

## 4. THE PHONE TEST, AS SCORED

Four independent rounds, byte-identical crops, `claude-opus-4-1`:

| # | intended | r1 | r2 | r3 | r4 | verdict |
|---|---|---|---|---|---|---|
| 00 | a rubber stamp | rubber stamp *sure* | rubber stamp *sure* | rubber stamp *sure* | rubber stamp *sure* | **PASS** 4/4 |
| 01 | a framed photo | framed picture of mountain **unsure** | framed picture *sure* | framed picture *sure* | framed picture of mountain *sure* | **PASS** 4/4 intended, 3/4 sure |
| 02 | a brightness slider | brightness slider control *sure* | **unidentifiable line drawing** *cannot tell* | **dumbbell** *cannot tell* | brightness slider *sure* | **FAIL** |

Two further single-object dispatches: `dimmer switch (brightness slider)`
*unsure* and `barbell` *cannot tell*.

Object 01 is scored PASS under SCORE THE IDEA, NOT THE NOUN (Miguel,
2026-09-06): "framed picture" and "framed picture of mountain" are the container
and the content of a framed photo, and the artwork seal's own profile for this
object was the same shape (4/4 `picture frame`, 3/4 sure).

Object 02 is scored FAIL. **Three independent readers converged on the barbell
family** (`dumbbell`, `barbell`, plus one outright refusal), and a converging
misread is the drawing rather than the instrument. `production.py consensus`
refuses it on `MISREAD_MAX` and the build was not rendered.

---

## 5. THE REPAIR ROUND — NINE DRAWINGS, CUT AND READ COLD

The scene lock was taken (`production.py scene-lock --holder split`), because
"not mine to change" is not a terminal reason on a repair round. Every candidate
was rendered at real phone size through the artwork author's own proof harness
and read by fresh independent readers. `gen/eudisclosure_slider_candidates.py`
holds all of them; the reads are in
`review/phone_reader_eudisclosure_split_cand*_r*.json`.

**Why the barbell happens:** a starburst at each end of a bar with a grip across
the middle IS a barbell, and the small-sun-to-big-sun SCALE that was meant to
say BRIGHTNESS is exactly what supplies the two weight plates.

| # | drawing | seat | reads |
|---|---|---|---|
| — | the sealed original | 264 x 76 (99 x 28 phone) | slider *sure*, unidentifiable, dumbbell, slider *sure*, dimmer **unsure**, barbell |
| A | sun at one end only | 264 x 76 | `light bulb` **unsure**, `sparkler` **unsure** |
| B | an open stroke wedge | 264 x 76 | `flashlight shining a beam` **unsure**, `tweezers` **unsure** |
| C | the original at the body row's full height | 264 x 152 (99 x 56 phone) | `dimmer switch brightness slider` **unsure**, `dimmer switch / brightness icon` *cannot tell* |
| D | C with a plain disc for the dim end | 264 x 152 | `light switch` **unsure**, `light bulb with switch` *cannot tell* |
| E | a sun over a rounded RAIL, knob riding it | 264 x 152 | `brightness slider (dimmer switch)` **unsure** x2 |
| F | E with the dim disc kept beside the sun | 264 x 152 | `brightness slider (dimmer switch)` **unsure**, `brightness dimmer slider` **unsure** |
| G | a paint brush over a dab of colour | 264 x 152 | `marker pen` *sure*, `marker pen` **unsure** |
| H | a round dimmer dial with a tick arc | 264 x 152 | `alarm clock` **unsure** x2 |
| I | G with a proper splayed brush head | 264 x 152 | `nail polish bottle`, `lipstick tube` x3, all **unsure** |

Two findings worth keeping:

1. **The taller seat is a real improvement and costs nothing.** Growing the
   slider to fill the body row (core y 356..508, the rows its two neighbours
   already occupy) doubles the reader's vertical from 28 to 56 phone px, makes
   the three objects on that row ONE height — LAW 32's sibling consistency — and
   every gutter survives: photo-real 28, window-shot 28, key-disclose 24 (the
   floor exactly), key-realimage and key-screenshot 36.9. Candidates C, D, E and
   F on that seat produced **zero** barbells across ten reads, against three in
   six on the sealed seat. The repaired module is preserved at
   `gen/eudisclosure_scene.slider_repair_candidateF.py.bak`.

2. **No drawing can close the gate today.** `production.py consensus` requires
   at least half the readers to be *sure*. E and F are named correctly by every
   reader and NOT ONE will say *sure* — and a 3x upscale of C hedges too, so it
   is not resolution and not silhouette size. The readers' own answers say why:
   they cannot tell whether the glyph is a brightness slider, a dimmer switch or
   a light/dark toggle. They are unsure WHICH light control it is, not whether
   it is one. That is the same hedge the calibration control produced on the
   sealed crop.

**The module was reverted to its sealed bytes and the lock released.** The
repaired scene cannot be re-sealed (`artwork-pass` runs the same `consensus`
and refuses 0/4 sure), and leaving a broken seal on disk would have failed
`artwork-check` for the CUTOUT author too and deadlocked a second lane for a
problem it did not cause. `eudisclosure_scene.py` is back to
`d3e960ae2e4845a1b8d5da980ce2a4237da182608941aed23e26d97e67ae80f5`,
`artwork-check` passes, the lock is released, and the project on disk was
rebuilt from the sealed module and re-verified green.

---

## 6. WHAT THE CLERK / THE NEXT SESSION SHOULD DECIDE

Two readings of the same evidence, and this lane deliberately did not pick for
you:

* **The drawing.** Three readers made a barbell out of the sealed slider. That
  is a converging misread and the seat is genuinely too short at 99 x 28.
  Candidate F on the taller seat fixes the misread completely and is ready on
  disk.
* **The instrument.** Every reader available today hedges on the slider,
  including on the crop the run's own reader called *sure* four times this
  morning. The gate's 50 %-sure bar may simply be unreachable for this object
  class on this substitute, in which case F would seal the moment the Fable
  lane is back.

The cheap next step is to re-run four rounds on the sealed crops when the reader
lane recovers. If the sealed drawing reproduces its 4/4 *sure*, the split is
green as it stands and only needs a render. If it does not, adopt candidate F
from `gen/eudisclosure_scene.slider_repair_candidateF.py.bak`, re-seal with
`artwork-pass`, and tell the cutout author to rebuild.

Also flagged, smaller: object 01 drew two *unsure* rounds out of four. It passes
the bar (3/4 sure) and matches the artwork seal's own profile, but it is the
second-most marginal object in the composition and it is on the record here.
