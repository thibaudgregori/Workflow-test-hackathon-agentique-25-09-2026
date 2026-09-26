# Patch for `.claude/workflows/daily-shorts.js` spawn() — apply AFTER run 19 finishes, then `node pipeline/workflow_dryrun.mjs`

## Change 1: a cap seen in the error text never spawns anything
In `spawn()`, right after `const text = ...` and `let capped = ...`:

```js
    // 2026-09-13 (run 19): a cap in the ERROR TEXT is the parent's cap. Nothing we
    // spawn can run, the sleeper included, so probing/sleeping/retrying here turned
    // one cap into 56 API errors in 29 s. Mark the lane and get out; the run ends on
    // its done-files and is resumed after the reset named in the text.
    if (err && capped) {
      const why = `USAGE CAP at ${label} (${text.slice(0, 200)})`
      if (!capNotes.length) capNotes.push(why)
      noteFail(label, 'usage cap: not retried, not repaired; resume after the reset')
      cappedLanes.add(label)
      return null
    }
```
and declare `const cappedLanes = new Set()` beside `capNotes`.

## Change 2: the sleeper path stays only for a cap seen from OUTSIDE (null return AND the probe cannot run), and a sleeper that did not actually sleep is not a tick
Replace `await sleeper(label + '#' + ticks, ph, TEN_MIN, why)` + `continue` with:
```js
      const slept = await sleeper(label + '#' + ticks, ph, TEN_MIN, why)
      if (slept !== 'slept') {            // the sleeper itself was refused: nothing can run
        noteFail(label, 'usage cap: even the sleeper could not run; resume after the reset')
        cappedLanes.add(label)
        return null
      }
      continue
```

## Change 3: no repair round for a capped lane
Where a lane's non-ok result feeds `REPAIR(...)` (the `repair:` spawn at ~line 777): skip when `cappedLanes.has(<lane label>)` and record `needs_repair` as `capped` instead.

## Change 4: harness scenario (c) must change with it
`pipeline/workflow_dryrun.mjs` scenario c currently asserts the author is retried 3x with 2 sleepers on a 429 text. Under the new rule the assertion is: ONE call, zero sleepers, zero probes, `usage_cap` reported, lane in `needs_repair` as capped. Add scenario (f): null return + probe null → sleeper returns "slept" → retry (the outside-cap path unchanged), and (g): sleeper returns null → lane capped, no retry.
