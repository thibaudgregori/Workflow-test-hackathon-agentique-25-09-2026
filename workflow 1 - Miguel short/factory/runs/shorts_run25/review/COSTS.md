# What shorts_run25 cost

**$0.75 for the whole run.** 12 files were staged, so a delivered short cost **$0.062**.

Every number below was measured by the code that made the call and written to `costs.jsonl` at that moment. Nothing here is re-priced, and nothing is added by hand.

## By service

| service | USD |
|---|---|
| Modal | 0.6680 |
| ElevenLabs | 0.0798 |
| **run total** | **0.7478** |

## By stage

| stage | USD |
|---|---|
| scribe | 0.0798 |
| sweep | 0.1629 |
| track | 0.0690 |
| ship | 0.2433 |
| render | 0.1928 |

## By video

| video | Modal | Gemini | ElevenLabs | other | total |
|---|---|---|---|---|---|
| claudeconcise | 0.2270 | 0.0000 | 0.0100 | 0.0000 | **0.2370** |
| grokimagine2 | 0.0938 | 0.0000 | 0.0036 | 0.0000 | **0.0974** |
| nextslide | 0.1842 | 0.0000 | 0.0037 | 0.0000 | **0.1878** |
| transcripts | 0.0000 | 0.0000 | 0.0596 | 0.0000 | **0.0596** |
| warpgrok | 0.1630 | 0.0000 | 0.0029 | 0.0000 | **0.1659** |
| **run** | **0.6680** | **0.0000** | **0.0798** | **0.0000** | **0.7478** |

## By format

| format | USD |
|---|---|
| cutout | 0.0929 |
| split | 0.0476 |
| whiteboard | 0.0523 |

A format's line holds only the money that is spent per format — the render, its watcher and its Gate 3. The cut, the sweep, the track and the matte are paid once per recording and serve all three formats, so they are in the video's line and not here.

## Stages this run never recorded

These stages exist in the pipeline and wrote no ledger row. A stage with a known reason is not a hole; a stage without one either did not run, or ran and was never booked — and that is the only way the run total above can be too low.

- `draft` — no draft render was paid for before the real one
- `watch` — no reason on record. CHECK IT.
- `gate3` — no reason on record. CHECK IT.
- `verify` — no flag verification round ran
- `clerk_watch` — the clerk did not re-watch — procedure v3.1, as intended

## Notes

- ElevenLabs Scribe: estimate at $0.40/audio-hour (ElevenLabs Scribe list rate, tools/elevenlabs.md; the API returns no cost, so this is not measured).
- Ledger: `/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/runs/shorts_run25/costs.jsonl` (34 row(s) after replace-by-key).
