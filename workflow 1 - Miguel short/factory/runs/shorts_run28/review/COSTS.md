# What shorts_run28 cost

**$0.66 for the whole run.** 12 files were staged, so a delivered short cost **$0.055**.

Every number below was measured by the code that made the call and written to `costs.jsonl` at that moment. Nothing here is re-priced, and nothing is added by hand.

## By service

| service | USD |
|---|---|
| Modal | 0.5897 |
| ElevenLabs | 0.0684 |
| **run total** | **0.6581** |

## By stage

| stage | USD |
|---|---|
| scribe | 0.0684 |
| sweep | 0.1377 |
| track | 0.0762 |
| ship | 0.2231 |
| render | 0.1527 |

## By video

| video | Modal | Gemini | ElevenLabs | other | total |
|---|---|---|---|---|---|
| eudisclosure | 0.1449 | 0.0000 | 0.0031 | 0.0000 | **0.1480** |
| grokfeatures | 0.1739 | 0.0000 | 0.0039 | 0.0000 | **0.1777** |
| hermesdocs | 0.1454 | 0.0000 | 0.0031 | 0.0000 | **0.1485** |
| hermeshub | 0.1255 | 0.0000 | 0.0027 | 0.0000 | **0.1282** |
| transcripts | 0.0000 | 0.0000 | 0.0557 | 0.0000 | **0.0557** |
| **run** | **0.5897** | **0.0000** | **0.0684** | **0.0000** | **0.6581** |

## By format

| format | USD |
|---|---|
| cutout | 0.0698 |
| split | 0.0391 |
| whiteboard | 0.0438 |

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
- Ledger: `/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/runs/shorts_run28/costs.jsonl` (36 row(s) after replace-by-key).
