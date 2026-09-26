# What shorts_run24 cost

**$1.48 for the whole run.** 12 files were staged, so a delivered short cost **$0.123**.

Every number below was measured by the code that made the call and written to `costs.jsonl` at that moment. Nothing here is re-priced, and nothing is added by hand.

## By service

| service | USD |
|---|---|
| Modal | 0.8380 |
| Gemini | 0.5126 |
| ElevenLabs | 0.1293 |
| **run total** | **1.4799** |

## By stage

| stage | USD |
|---|---|
| scribe | 0.1293 |
| sweep | 0.1287 |
| track | 0.0871 |
| ship | 0.3145 |
| render | 0.3076 |
| watch | 0.4272 |
| gate3 | 0.0854 |

## By video

| video | Modal | Gemini | ElevenLabs | other | total |
|---|---|---|---|---|---|
| claudesessions | 0.2097 | 0.1447 | 0.0097 | 0.0000 | **0.3641** |
| cursorspacex | 0.1743 | 0.1962 | 0.0154 | 0.0000 | **0.3859** |
| geminigems | 0.1935 | 0.1717 | 0.0173 | 0.0000 | **0.3825** |
| primeagent | 0.2604 | 0.0000 | 0.0282 | 0.0000 | **0.2886** |
| transcripts | 0.0000 | 0.0000 | 0.0587 | 0.0000 | **0.0587** |
| **run** | **0.8380** | **0.5126** | **0.1293** | **0.0000** | **1.4799** |

## By format

| format | USD |
|---|---|
| cutout | 0.2421 |
| split | 0.2904 |
| whiteboard | 0.2877 |

A format's line holds only the money that is spent per format — the render, its watcher and its Gate 3. The cut, the sweep, the track and the matte are paid once per recording and serve all three formats, so they are in the video's line and not here.

## Stages this run never recorded

These stages exist in the pipeline and wrote no ledger row. A stage with a known reason is not a hole; a stage without one either did not run, or ran and was never booked — and that is the only way the run total above can be too low.

- `draft` — no draft render was paid for before the real one
- `verify` — no flag verification round ran
- `clerk_watch` — the clerk did not re-watch — procedure v3.1, as intended

## Notes

- ElevenLabs Scribe: estimate at $0.40/audio-hour (ElevenLabs Scribe list rate, tools/elevenlabs.md; the API returns no cost, so this is not measured).
- Ledger: `/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/runs/shorts_run24/costs.jsonl` (85 row(s) after replace-by-key).
