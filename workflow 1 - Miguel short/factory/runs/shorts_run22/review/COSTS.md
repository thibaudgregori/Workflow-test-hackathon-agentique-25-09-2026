# What shorts_run22 cost

**$0.55 for the whole run.** 3 files were staged, so a delivered short cost **$0.183**.

Every number below was measured by the code that made the call and written to `costs.jsonl` at that moment. Nothing here is re-priced, and nothing is added by hand.

## By service

| service | USD |
|---|---|
| Modal | 0.2929 |
| Gemini | 0.2534 |
| ElevenLabs | 0.0036 |
| **run total** | **0.5498** |

## By stage

| stage | USD |
|---|---|
| scribe | 0.0036 |
| sweep | 0.0373 |
| track | 0.0423 |
| ship | 0.1372 |
| render | 0.0761 |
| watch | 0.2132 |
| gate3 | 0.0402 |

## By video

| video | Modal | Gemini | ElevenLabs | other | total |
|---|---|---|---|---|---|
| aieducation | 0.2929 | 0.2534 | 0.0036 | 0.0000 | **0.5498** |
| **run** | **0.2929** | **0.2534** | **0.0036** | **0.0000** | **0.5498** |

## By format

| format | USD |
|---|---|
| cutout | 0.0548 |
| split | 0.1620 |
| whiteboard | 0.1127 |

A format's line holds only the money that is spent per format — the render, its watcher and its Gate 3. The cut, the sweep, the track and the matte are paid once per recording and serve all three formats, so they are in the video's line and not here.

## Stages this run never recorded

These stages exist in the pipeline and wrote no ledger row. A stage with a known reason is not a hole; a stage without one either did not run, or ran and was never booked — and that is the only way the run total above can be too low.

- `draft` — no draft render was paid for before the real one
- `verify` — no flag verification round ran
- `clerk_watch` — the clerk did not re-watch — procedure v3.1, as intended

## Notes

- ElevenLabs Scribe: estimate at $0.40/audio-hour (ElevenLabs Scribe list rate, tools/elevenlabs.md; the API returns no cost, so this is not measured).
- Ledger: `/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/runs/shorts_run22/costs.jsonl` (26 row(s) after replace-by-key).
