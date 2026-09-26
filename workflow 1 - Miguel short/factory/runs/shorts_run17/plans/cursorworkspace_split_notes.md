# cursorworkspace — SPLIT (YouTube) author's notes

The plan is `plans/cursorworkspace_plan.json`. Its `open_doubts` list is empty and
this lane built what it says. Six things below are places where the built master
DIFFERS from the plan's letter or where the plan's own arithmetic does not survive
contact with the split chassis. Nothing here changes the ARGUMENT, the lane, the
beats, the objects, the labels or the cast; two of them are LAW-forced, three are
consequences of consuming the SEALED scene module rather than re-deriving it, and
one is a measurement the plan got wrong that I am recording rather than hiding.

The shared scene module `gen/cursorworkspace_scene.py` was consumed unmodified.
Its sha256 still matches `review/artwork_pass_cursorworkspace.json`. Every
declaration this lane needed that the module does not emit was stamped onto the
EMITTED HTML string in `declare_contracts()`, never onto the module, because the
CUTOUT author is reading the same file for TikTok while this runs.

---

## 1. THE PLAN DERIVED THE CAPTION CLEARANCE AGAINST A SEAT OF 960. THE SPLIT'S SEAT IS 862.5.

`plan.shared_layout_note` and `plan.per_lane_notes.split_youtube` both derive the
bottom clearance from *"the split's RENDERING pill top, 960 - 114.59/2 =
902.705"*, and the scene handoff repeats it (§4 clause 3, "144.2 px"). The
classic split does not seat its pill at the frame centre. It seats it on the
SEAM, and the seam is fixed by the delivery-sized face plate: `face_bottom_hd.mp4`
is 1080x1058, so the seam is 1920 - 1057.5 = **862.5**, which is what
`shorts_run15/gen/{geminitools,harnessrace,shieldstral}_gen.py` and this run's
own `eudisclosure_gen.py` all use.

Rendering pill top is therefore **805.205**, not 902.705, and the real clearance
under the lowest ink (canvas 758.5, the trough of the lowest water wave) is
**46.71 px**, not 144.2.

I built the plan anyway: 46.71 px clears the 24 px floor `guard_core_band` refuses
on, LAW 30's top-10 % line is cleared by 98 px, and nothing in the scene may move
because the module is sealed. What I would have done differently is write the
plan's clearance sum against 862.5 in the first place — the number it quotes is
the one a whiteboard or a cutout would use, not the split's.

**This matters to the CUTOUT author**: your seat is your own session's envelope
and neither 960 nor 862.5 applies to you, but the handoff's "144.2 px" is not a
number to reuse.

## 2. THE PHONE TEST WAS CUT FROM `--geom`, NOT FROM `--plan`.

`phone_test_page.py`'s precedence is `--at` > `--plan` > `--geom`, so passing the
plan would have silently cropped the plan's boxes at the plan's instants. On this
video those are not what the scene draws:

| | plan | built |
|---|---|---|
| an arch bridge | t 1.60, bbox 0.213 / 0.301 / 0.787 / 0.3734 | t **2.30**, bbox 0.19259 / 0.30208 / 0.80741 / 0.39505 |
| a settings panel | t 13.90, bbox 0.2407 / 0.2125 / 0.7593 / 0.3385 | t **14.20**, bbox 0.24074 / 0.2125 / 0.75926 / 0.35208 |

The bridge's box moved because the artwork author replaced two straight ripple
dashes with three WAVES (`plans/cursorworkspace_scene_notes.md` note 2), which
dropped the lowest ink from core 562.5 to 566.5 — the plan's own box stops at
canvas 717, so cropping it would cut the water off, and the water is the single
change that turned an *unsure* "arched bridge" into six *sure* reads of "bridge
over water" during the seal. Every plan `t` is an entrance-COMPLETION time;
`SC.BESPOKE` gives a HELD instant, and a crop taken on the last frame of an
entrance judges the animation, not the object.

The deltas are recorded in `gen/_build_cursorworkspace.json ->
formats.split.phone_test_vs_plan` rather than hidden, and the same built boxes
are what `--phone-at` hands `qc_pass` at render time.

## 3. `row-text` IS DECLARED `data-label-for="conn-row"` ON THE EMITTED PAGE.

Gate 1 (`geometry_audit`, LAW 3 "a name goes above or below, never beside")
raised one warning on the first build:

> `row-text ('WORKSPACE') sits BESIDE row-ws-tile: centre off by +142px on a
> +/-55px band.`

The scene deliberately gives `row-text` no `data-label-for`: the word WORKSPACE
is the connector row's own CONTENT, mock-UI anatomy, not a side label. With no
declaration the gate GUESSES a host, and its auto-inference explicitly skips any
candidate that CONTAINS the label (`_lcontains`) — so it skips `conn-row`, the
thing the word actually names, and welds the name to the 84 px icon beside it.
The plan's own lifetimes say a `mark:` rigid *"is a DECORATION under LAW 39,
never hosts a label"*, and that tile is exactly that.

So the host is DECLARED on the emitted string, which is telling the gate the
truth rather than silencing it. With the host stated, the name sits 44 px off the
row's own axis on a ±322 px band and the check passes on the merits. The stamp
asserts containment and the axis offset before it will write. No geometry moves.
Gate 1 is now 0 errors / 0 warnings, and `--strict` is 0/0 as well.

## 4. SS3b NEEDED A RE-CUT, NOT A MERGE, ON ONE BEAT.

`captions.merge_function_only_beats` can only FOLD an orphan into a neighbour.
The word `to` in *"...customized page directly **to** your Google Workspace."*
cannot be folded either way inside the 756 px seat: `to` + its right neighbour
measures **792.1 px** and `to` + its left neighbour measures **802.0 px**. The
canonical merge legally cannot repair it, and `assert_no_function_only_beat`
would have failed the build on a sentence that is perfectly splittable.

`repair_orphan_beats()` generalises the third fallback `merge_board_key_beats`
already uses for LAW 4: an exact O(n²) dynamic program over the union's word
boundaries, minimising (number of parts, then squared slack), rejecting any part
that overflows the seat, repeats a printed board key, or that
`captions.is_orphan_beat` refuses. Nothing is widened, nothing is shrunk and no
law is relaxed — the same words are cut at a different place.

The result is `"your cursor from the" / "customized" / "page directly to" /
"your Google Workspace."`. **`"customized page"` was rejected by LAW 4**, not by
the splitter: the board prints CUSTOMIZED PAGE, so that exact string is in
`forbidden`. That is the law working, and it is why a lone `customized` (aspect
3.20, well over the 1.45 badge line) is the best legal cut.

## 5. LAW 47 IS REPORTED, NOT PLANNED AROUND — AND I AM NOT STOPPING ON IT.

The cut master is 21.532 s; the last word ends at 21.280. Tail = **0.252 s**
against a cap of 0.20 + one frame = 0.240 s, i.e. **0.012 s over — a third of a
frame** of container rounding. It is the CUT's, not the scene's: the scene's last
authored board ink completes at 16.66 and the outro anchor is 17.319, so nothing
this lane owns is late. The handoff records it as "reported, not planned around"
and the prep `cut` marker is status ok, so `clean_tokens` measures it, records
`law47_overshoot_s`, and stops the build only past 0.30 s. Refusing a FINAL cut
over a third of a frame would be the wrong call.

## 6. THE TAKE'S CORROBORATION GAP READS `DISAGREES`.

`prep/stages/cursorworkspace.cut.json -> corroboration` is
`{marker: "equality", gap: "DISAGREES", witnessed: true,
allow_uncorroborated: false}` — the equality marker and the witness carry the
cut, the gap heuristic dissents. I did not re-cut (the stage is status ok and I
can name no measured defect in what it produced), and the transcript's own
evidence agrees with the marker: the take opens cleanly on `If you're using
Cursor,` at 0.119 s and that phrase never returns. It is recorded in the build
report rather than swallowed.

---

## WHAT I DID NOT DO

* I did not touch `gen/cursorworkspace_scene.py`, `plans/cursorworkspace_scene_handoff.md`
  or any matting artefact. No Modal call of any kind was made by this lane.
* I did not build a cutout or a whiteboard, and I did not take the scene lock —
  no reader refused either bespoke object.
* I did not run the Viewer Test on my own work (Miguel, 2026-09-02).

---

# RE-DISPATCH SESSION, 2026-09-08 08:37-08:55 — NOTHING WAS REBUILT, AND HERE IS WHY

`stage_cache.py check --label split_cursorworkspace` returned `found=false`, so
the workflow spawned this lane a second time. The miss is MECHANICAL, not a
defect: `plans/<vid>_plan.json` is inside this lane's fingerprint and the plan
file was overwritten at 08:32 by a re-dispatched plan agent, which says so
itself in `plan.reconstruction_note`. The plan's bytes changed; nothing the
plan DESCRIBES changed.

## 7. THE RECONSTRUCTED PLAN AND THE BUILT PAGE NOW AGREE, INCLUDING NOTE 2 ABOVE

The reconstruction folded the BUILT geometry back into the plan, so the table in
note 2 is history: `plan.bespoke_objects` is now `an arch bridge` @ **2.30**
bbox 0.19259/0.30208/0.80741/0.39505 and `a settings panel` @ **14.20** bbox
0.24074/0.2125/0.75926/0.35208 — the built values, to five decimals. This
session therefore ran `phone_test_page.py` with **`--plan`** (not `--geom`), and
the crops it cut are BYTE-IDENTICAL to the ones the first session cut from
`--geom`: `00.png` sha256 `e04e6b4d0da6460af9abd2a9fbddcdb4006d70b0797113f1cd2e5ba559b21c40`,
`01.png` `ec6cd44e56e8f6e6d745686744ff838f5888c9dd00a43b6c4b731607d24c3651`.
`gen/_build_cursorworkspace.json -> formats.split.phone_test_vs_plan` still
records the ORIGINAL plan's numbers and is now historical, not live.

Note 1 above stands unchanged and is still a live disagreement: the
reconstructed `plan.per_lane_notes.split_youtube` STILL derives the bottom
clearance from a 960 seat ("144.2 px under the rendering pill's top
(902.705)... 201.5 px above the seam (960)"). The split's seam is **862.5**,
the rendering pill top is **805.205** and the true clearance under the lowest
ink (canvas 758.5) is **46.71 px**. Legal — 24 px floor cleared, LAW 30's
top-10 % line cleared by 98 px — but the plan's number is wrong and no lane
should reuse it.

## 8. WHAT WAS RE-VERIFIED, LIVE, RATHER THAN ASSUMED

* `production.py artwork-check` exit 0, verdict PASS, 2 objects, 6 seal rounds;
  the sealed module still hashes `f8c1e9bf...` and the handoff `0b6586fc...`.
  The module was NOT opened for writing by this lane.
* `production.py phone-check` exit 0: the binding approval
  `review/phone_pass_cursorworkspace_split.json` is still bound to the live
  `project_sha256 8a2e9ce4...` and all five of its evidence hashes still match.
* `prerender_check` PASS in 2.76 s — refs_resolve, assets_not_placeholder
  (6 rasters), page_audit, caption_canon_page (25 pills, modal h 114.61 px,
  spread 0.0), gate1 0 errors / 0 warnings.
* `geometry_audit --strict` **0 errors, 0 warnings** (21.5 s @ 0.5 s step),
  written to `gen/_geomstrict_cursorworkspace_split.json` with `--out` so the
  project's own `geometry_audit/report.json` — which is phone-approval evidence
  — was left byte-identical.
* SS3b by hand: 25 beats, `assert_no_function_only_beat` PASS on the MEASURED
  pill widths, min aspect 1.77 against a 1.45 badge line, **2 function-word
  merges** plus the one `repair_orphan_beats` re-cut of note 4. (`is_orphan_beat`
  called WITHOUT a width flags `"Now,"` on the sub-4-character fallback; with the
  measured 202.8 px it is not a badge and not an orphan. The width is the law.)
* The staged file is untouched: `staging/youtube/cursorworkspace_split.mp4`
  sha256 `329e15a934d761de9a871d28a466995d3efeaa37e51196a51c48c61c4decd538`,
  the same hash the first session's cache recorded, from the same $0.0087 Modal
  render whose `qc_pass` returned PASS.
* No Modal call, no matting call, no re-render, no re-cut was made by this
  session.

## 9. THE FINDING THIS SESSION OWES THE CLERK: OBJECT 1'S CONFIDENCE RATE FELL

Five FRESH cold-read rounds were dispatched on the byte-identical crops
(rounds 4, 5, 6 on the inherited configured reader; round7haiku and round7opus
on named models). Object 0 came back `bridge` / **sure** five times out of five
— eight of eight over the whole lane record.

Object 1 came back `toggle switch` five times out of five as well — **eight of
eight names, and fourteen of fourteen counting the artwork seal's six rounds,
with not one reader ever naming a different object and not one "cannot tell"**
— but only ONE of the five was `sure`. Over all eight lane rounds that is
**sure 3 of 8**, split by model: haiku 3/3 sure, opus 0/2, inherited configured
reader 0/3.

I submitted ALL EIGHT rounds to `production.py phone-pass` with the full
scoring file `review/phone_scores_cursorworkspace_split_all8.json`, so the
instrument and not the author would rule on the enlarged sample. It refused,
verbatim:

> `ValueError: Object 1: only 3 of 8 independent readers were sure; a drawing
> under half the readers can name confidently needs revision`

It wrote nothing: `review/phone_pass_cursorworkspace_split.json` is byte-identical
to before the call, and the binding approval on rounds 1-3 (2 of 3 sure, which
the same instrument accepted) still stands and still passes `phone-check`.

**I did not overwrite the approval, I did not cherry-pick a passing subset, and
I did not take the scene lock.** The reasons, stated so the clerk can overrule
them:

1. The drawing is not unreadable — it is over-specified. The crop is a cream
   settings card with a title bar carrying the Cursor mark, one connector row
   with the Google Workspace mark and the word WORKSPACE, and one large
   terracotta toggle. A reader asked to name "the single everyday object" sees
   a container AND its control and has to pick one; every reader picks the
   control, and some flag the choice as uncertain. That is the container-versus-
   content case Miguel's 2026-09-06 amendment (STANDARD.md -> THE PHONE TEST)
   settles as a PASS — "a reader who names the drawn content or its container
   ... PASSES".
2. The hedge is not a model-wide mood this hour: the same reader pool returned
   4/4 `sure` on `kimifable`'s crops at 08:24-08:25.
3. The failure this rule was written for is run 16's kimiwork app window, which
   two independent readers called "Refrigerator". Fourteen reads, one noun, zero
   misses is the opposite measurement.
4. The remedy the rule points at — revision — is not this lane's to make. The
   module is SEALED, the artwork owner re-affirmed the seal at 08:36 today
   (`review/agent_done_artwork_cursorworkspace.json`), the handoff forbids any
   lane redrawing it, and the WHITEBOARD author started on the same module at
   08:37. Taking `gen/.cursorworkspace_scene.lock` mid-flight would break both.

The clerk has every number above plus both scoring files and all eight reader
JSONs, and it is the independent judge here, not me.
