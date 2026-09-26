# What shorts_run17 cost

**$0.76 for the whole run.** 10 files were staged, so a delivered short cost **$0.076**.

Every number below was measured by the code that made the call and written to `costs.jsonl` at that moment. Nothing here is re-priced, and nothing is added by hand.

## By service

| service | USD |
|---|---|
| Modal | 0.6900 |
| ElevenLabs | 0.0713 |
| **run total** | **0.7613** |

## By stage

| stage | USD |
|---|---|
| scribe | 0.0713 |
| sweep | 0.1445 |
| track | 0.0811 |
| ship | 0.2909 |
| render | 0.1735 |

## By video

| video | Modal | Gemini | ElevenLabs | other | total |
|---|---|---|---|---|---|
| cursorworkspace | 0.1418 | 0.0000 | 0.0143 | 0.0000 | **0.1561** |
| eudisclosure | 0.1296 | 0.0000 | 0.0166 | 0.0000 | **0.1462** |
| kimifable | 0.2031 | 0.0000 | 0.0190 | 0.0000 | **0.2221** |
| pcoverheat | 0.2156 | 0.0000 | 0.0214 | 0.0000 | **0.2370** |
| **run** | **0.6900** | **0.0000** | **0.0713** | **0.0000** | **0.7613** |

## By format

| format | USD |
|---|---|
| cutout | 0.0589 |
| split | 0.0344 |
| whiteboard | 0.0802 |

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
- Ledger: `/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/runs/shorts_run17/costs.jsonl` (36 row(s) after replace-by-key).
