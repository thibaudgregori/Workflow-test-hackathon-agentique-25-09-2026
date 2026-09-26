# What shorts_run26 cost

**$0.69 for the whole run.** 15 files were staged, so a delivered short cost **$0.046**.

Every number below was measured by the code that made the call and written to `costs.jsonl` at that moment. Nothing here is re-priced, and nothing is added by hand.

## By service

| service | USD |
|---|---|
| Modal | 0.6132 |
| ElevenLabs | 0.0725 |
| **run total** | **0.6858** |

## By stage

| stage | USD |
|---|---|
| scribe | 0.0725 |
| sweep | 0.1803 |
| track | 0.0401 |
| ship | 0.1328 |
| render | 0.2600 |

## By video

| video | Modal | Gemini | ElevenLabs | other | total |
|---|---|---|---|---|---|
| deepseekprices | 0.0983 | 0.0000 | 0.0037 | 0.0000 | **0.1020** |
| grokdesktop | 0.0957 | 0.0000 | 0.0039 | 0.0000 | **0.0996** |
| hermesbrowser | 0.0809 | 0.0000 | 0.0029 | 0.0000 | **0.0838** |
| openairesets | 0.1304 | 0.0000 | 0.0023 | 0.0000 | **0.1327** |
| stripekai | 0.2079 | 0.0000 | 0.0040 | 0.0000 | **0.2119** |
| transcripts | 0.0000 | 0.0000 | 0.0557 | 0.0000 | **0.0557** |
| **run** | **0.6132** | **0.0000** | **0.0725** | **0.0000** | **0.6858** |

## By format

| format | USD |
|---|---|
| cutout | 0.0920 |
| split | 0.0559 |
| whiteboard | 0.1121 |

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
- Ledger: `/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/runs/shorts_run26/costs.jsonl` (41 row(s) after replace-by-key).
