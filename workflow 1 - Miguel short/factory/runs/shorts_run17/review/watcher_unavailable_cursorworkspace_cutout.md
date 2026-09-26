# Gemini watcher UNAVAILABLE — cursorworkspace / cutout (2026-09-08 08:53)

`review/cands_cursorworkspace_cutout.json` **does not exist**, and it is not a
lane failure. `render_and_check.py` started the watcher the instant the render
landed; it exited 1 after 17.1 s with the same account-level block every other
video in this run hit:

```
429 RESOURCE_EXHAUSTED
"Your project has exceeded its monthly spending cap."
https://ai.studio/spend
```

The stderr is recorded verbatim in
`gen/_rc_cursorworkspace_cutout.json -> results[0].watch.stderr`
(`upload_retry` gave up at `clerkvid_cursorworkspace_cutout_p1_w1.mp4`). The same
cap also turned qc_pass's own `gate3_gemini_describe` into **REPORTED** rather
than PASS — see `gen/_qcpass_cursorworkspace_cutout.json -> verdicts`.

That is an ACCOUNT-LEVEL block on the Gemini API project, not a property of this
video: no `cands_*.json` exists for ANY video in shorts_run17. Raising a spend
cap is a billing decision and belongs to Miguel, so nothing here was changed and
no other provider was substituted.

`render_and_check` recorded the render as `watch_unavailable` and staged it on
qc_pass alone, which is its own rule — an unavailable watcher is not a BLOCKING
candidate. **No `watch_waiver` was written, because there was no candidate to
waive.**

WHAT THE CLERK GETS INSTEAD, for this file:

* `gen/_qcpass_cursorworkspace_cutout.json` — 16 checks, 0 failed:
  `zero_ink_law` PASS, `clip_coverage_page` PASS (25 caption clips, 0 holes, 0
  ghosts), `face_centring` PASS, `pill_canon_rendered` PASS,
  `gate1_geometry_audit` PASS (0 errors / 0 warnings at a 0.25 s step),
  `gate2_frame_review` PASS, `cutout_checks_24_25` PASS, `edge_clip` PASS,
  `face_hf_vs_plate` PASS, `head_scale_vs_framing` PASS, `audio_guards` PASS,
  `contact_sheet` and `phone_crops` PASS. `double_exposure` and
  `gate3_gemini_describe` are REPORTED.
* `gen/_prerender_cursorworkspace_cutout.json` — Gate 1 PASS before render, with
  the cutout edge-fade guard and checks 24+25.
* `projects/cursorworkspace_cutout/geometry_audit/report.json` — strict, 0
  errors, 0 warnings.
* `review/phone_pass_cursorworkspace_cutout.json` — the hash-bound phone
  approval over FOUR independent two-crop cold-reader rounds on two models, with
  the scoring in `review/phone_scores_cursorworkspace_cutout.json` (the fifth,
  single-crop round is disclosed there as a diagnostic, and it is a hedge).
* the AUTHOR'S own look at the delivered file (never a Viewer Test — that is the
  clerk's): frames at 2 / 5 / 8 / 13 / 16 / 19 s, plus cream and dark composites
  of the matte at 0 / 3 / 7 / 11 / 15 / 21.4 s.

If the cap is lifted, the watcher can be re-run on the staged file with the exact
command recorded in `gen/_rc_cursorworkspace_cutout.json -> results[0].watch.cmd`;
`render_and_check` will archive nothing, because no prior candidate list exists to
archive.
