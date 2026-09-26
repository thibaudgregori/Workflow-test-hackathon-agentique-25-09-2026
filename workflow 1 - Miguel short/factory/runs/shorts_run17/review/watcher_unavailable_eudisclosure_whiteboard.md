# Gemini watcher UNAVAILABLE — eudisclosure / whiteboard (2026-09-08 01:50)

`review/cands_eudisclosure_whiteboard.json` **does not exist**, and it is not a
lane failure. `render_and_check.py` started the watcher the instant the render
landed and it exited 1; re-running `pipeline/clerk_video_gemini.py` by hand
reproduced it three times with the same underlying error on every upload:

```
429 RESOURCE_EXHAUSTED
"Your project has exceeded its monthly spending cap."
https://ai.studio/spend
```

That is an ACCOUNT-LEVEL block on the Gemini API project, not a property of this
video: no `cands_*.json` exists for ANY video in shorts_run17. Raising a spend
cap is a billing decision and belongs to Miguel, so nothing here was changed and
no other provider was substituted.

`render_and_check` recorded the render as `watch_unavailable` and staged it on
qc_pass alone, which is its own rule — an unavailable watcher is not a BLOCKING
candidate. **No `watch_waiver` was written, because there was no candidate to
waive.**

WHAT THE CLERK GETS INSTEAD, for this file:

* `gen/_qcpass_eudisclosure_whiteboard.json` — 13 checks, 0 failed, including
  `whiteboard_seam_law` PASS on seams 6.15 / 13.90, `zero_ink_law` PASS,
  `pill_canon_rendered` PASS, `gate1_geometry_audit` PASS, `gate2_frame_review`
  PASS, `phone_crops` PASS, `audio_guards` PASS.
* `gen/_prerender_eudisclosure_whiteboard.json` — Gate 1 PASS before render.
* `projects/eudisclosure_whiteboard/geometry_audit/report.json` — strict, 0
  errors, 0 warnings.
* `review/phone_pass_eudisclosure_whiteboard.json` — the hash-bound phone
  approval over four independent cold-reader rounds.

If the cap is lifted, the watcher can be re-run on the staged file with the
exact command recorded in `gen/_rc_eudisclosure_whiteboard.json ->
results[0].watch.cmd`; `render_and_check` will archive nothing, because no prior
candidate list exists to archive.
