# What shorts_run27 cost

**$1.37 for the whole run.** 21 files were staged, so a delivered short cost **$0.065**.

Every number below was measured by the code that made the call and written to `costs.jsonl` at that moment. Nothing here is re-priced, and nothing is added by hand.

## By service

| service | USD |
|---|---|
| Modal | 1.2614 |
| ElevenLabs | 0.1105 |
| **run total** | **1.3719** |

## By stage

| stage | USD |
|---|---|
| scribe | 0.1105 |
| sweep | 0.3704 |
| track | 0.1004 |
| ship | 0.4209 |
| render | 0.3697 |

## By video

| video | Modal | Gemini | ElevenLabs | other | total |
|---|---|---|---|---|---|
| ccremote | 0.2089 | 0.0000 | 0.0039 | 0.0000 | **0.2128** |
| claudemanaged | 0.2345 | 0.0000 | 0.0043 | 0.0000 | **0.2388** |
| codexappshots | 0.1924 | 0.0000 | 0.0038 | 0.0000 | **0.1962** |
| codexsiri | 0.1568 | 0.0000 | 0.0040 | 0.0000 | **0.1608** |
| falagent | 0.1918 | 0.0000 | 0.0037 | 0.0000 | **0.1955** |
| lunafree | 0.0494 | 0.0000 | 0.0023 | 0.0000 | **0.0517** |
| streamdeck | 0.2276 | 0.0000 | 0.0034 | 0.0000 | **0.2310** |
| transcripts | 0.0000 | 0.0000 | 0.0851 | 0.0000 | **0.0851** |
| **run** | **1.2614** | **0.0000** | **0.1105** | **0.0000** | **1.3719** |

## By format

| format | USD |
|---|---|
| cutout | 0.1738 |
| split | 0.1163 |
| whiteboard | 0.0796 |

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
- Ledger: `/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/runs/shorts_run27/costs.jsonl` (58 row(s) after replace-by-key).
