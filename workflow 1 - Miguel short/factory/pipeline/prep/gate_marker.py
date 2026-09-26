#!/usr/bin/env python
"""Read a prep stage marker and decide the gate, deterministically.

WHY THIS EXISTS (run 17, eudisclosure, 2026-09-08).  The MATTE GATE is an
agent whose entire job is to read ONE json file and say what it says.  It was
also told to poll for up to forty minutes, so it had to keep itself alive
across dozens of turns with a monitor or a background loop.  On run 17 that
agent returned NOTHING three times in a row and never even wrote its started
sentinel, while `prep/stages/eudisclosure.ship.json` had said `"status": "ok"`
on disk since 00:45:23.  `gateErr(null)` turned that into the string "the gate
agent never returned", `gateWithRepair` could not tell it apart from a refused
encode, and it spent the recording's ONE repair round on an answer that was
lying on disk the whole time.

So the judgement leaves the model and comes here:

  * ONE bounded command answers the gate.  `--wait-s` blocks in python until
    the marker turns ok, so the gate agent runs a single Bash call and
    returns.  A forty-minute agentic poll becomes N short calls driven by the
    workflow's own poll loop, and an agent that cannot survive a long wait can
    no longer lose a lane.
  * THE OVERRIDE WINS, always, without anyone remembering to look for it.
  * A HALF-WRITTEN MARKER IS NOT A VERDICT.  `mark_stage` writes with
    `write_text`, which is not atomic, so a reader can catch a truncated file.
    That is `unreadable`, it is never final, and while waiting it is simply
    retried.
  * IT NEVER RAISES.  A gate that crashes is a gate that returns nothing, and
    returning nothing is the failure this module was written to end.
  * AN "ok" IS ONLY AS GOOD AS THE FILES UNDER IT (run 17, cursorworkspace,
    2026-09-08).  The first version of this module proved a shipped matte by
    `is_file()` alone, so an `ok` marker over a truncated, empty, half-copied or
    stale webm still read `ok` and `outputs` silently came back with two layers
    instead of three.  Both run-17 repair agents then verified the three
    sha256 by hand against `ship_v5.json` - the manifest the ship stage already
    writes for exactly this purpose.  That hand-check now lives in the rule:
    `verify_outputs` re-hashes the three layers and an `ok` whose files do not
    match its own manifest becomes `outputs_incomplete`, which is NOT a pass and
    NOT final, so the workflow polls (a layer still flushing settles) and then
    repairs instead of building a lane on a broken matte.  With no manifest to
    check against, nothing is downgraded.

Statuses out: the marker's own word (`ok`, `reused`, `error`, `REFUSED`,
`SKIPPED_NEEDS_KEY`, ...), plus `missing` when no marker exists yet and
`unreadable` when one exists but does not parse, and
`outputs_incomplete` when a passing ship marker's own matte layers do not match
`ship_v5.json`.  `final` is true ONLY for
`SKIPPED_NEEDS_KEY` and `not_a_short`; everything else stays pollable, exactly
as GATE_NOT_FINAL in the workflow requires.

    gate_marker.py --run <run> --id eudisclosure --stage ship [--wait-s 570]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

LAYERS = ("cut", "rim", "alpha")
PASS_STATUS = ("ok", "reused")
FINAL_STATUS = ("SKIPPED_NEEDS_KEY", "not_a_short")
MAX_WAIT_S = 570          # the Bash tool caps one call at 600 s
SCALAR = (str, int, float, bool, type(None))


def marker_paths(run, vid: str, stage: str) -> tuple[Path, Path]:
    """(override, marker).  The override is written by a repair agent."""
    d = Path(run) / "prep" / "stages"
    return d / f"{vid}.{stage}.override.json", d / f"{vid}.{stage}.json"


def _load(p: Path):
    """(dict, state) where state is 'ok', 'missing' or 'unreadable'."""
    try:
        if not p.is_file():
            return None, "missing"
        d = json.loads(p.read_text())
        return (d, "ok") if isinstance(d, dict) else (None, "unreadable")
    except (OSError, ValueError):
        return None, "unreadable"


def read_marker(run, vid: str, stage: str) -> dict:
    """The gate's answer for one stage, right now, with the override applied."""
    over, main = marker_paths(run, vid, stage)
    d, state = _load(over)
    used_override = d is not None
    if d is None:
        d, state = _load(main)
    out = {"id": vid, "stage": stage, "override_used": used_override,
           "marker": str(over if used_override else main)}
    if d is None:
        out.update({"status": state, "final": False, "keys": {}})
        return out
    keys = d.get("keys") or {}
    status = d.get("status") or "missing"
    out.update({"status": status,
                "final": status in FINAL_STATUS,
                "at": d.get("at"),
                "wall_s": d.get("wall_s"),
                "keys": {k: v for k, v in keys.items() if isinstance(v, SCALAR)},
                "error": keys.get("error") or d.get("error") or ""})
    return out


def passed(state: dict) -> bool:
    return state.get("status") in PASS_STATUS


def outputs(run, vid: str, stage: str) -> dict:
    """The artifacts a downstream lane needs, and whether they are on disk."""
    if stage != "ship":
        return {}
    s = Path(run) / "matting" / vid
    return {layer: str(p) for layer in LAYERS
            for p in [s / f"matte_{vid}_v5_{layer}.webm"] if p.is_file()}


def _sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_outputs(run, vid: str, stage: str) -> dict:
    """Are the three layers on disk the ones ship_v5.json says were encoded?

    `no_manifest` (nothing to check against - never a downgrade), `ok` (all
    three present, non-empty and sha256-equal), or `mismatch` with the reasons.
    It never raises: an unreadable manifest is simply nothing to check against.
    """
    out = {"verified": "no_manifest", "layers": outputs(run, vid, stage),
           "bad": []}
    if stage != "ship":
        return out
    s = Path(run) / "matting" / vid
    man, state = _load(s / "ship_v5.json")
    hashes = (man or {}).get("hashes")
    if state != "ok" or not isinstance(hashes, dict) or not all(
            isinstance(hashes.get(k), str) and hashes[k] for k in LAYERS):
        return out
    bad = []
    for layer in LAYERS:
        p = s / f"matte_{vid}_v5_{layer}.webm"
        try:
            if not p.is_file():
                bad.append(f"{layer}: missing")
            elif p.stat().st_size == 0:
                bad.append(f"{layer}: empty file")
            elif _sha256(p) != hashes[layer]:
                bad.append(f"{layer}: sha256 differs from ship_v5.json")
        except OSError as exc:                                # noqa: PERF203
            bad.append(f"{layer}: {type(exc).__name__}")
    out["bad"] = bad
    out["verified"] = "mismatch" if bad else "ok"
    return out


def settle(run, vid: str, stage: str, st: dict) -> dict:
    """A passing word is only settled once the artifacts under it agree."""
    if stage != "ship" or not passed(st):
        return st
    ver = verify_outputs(run, vid, stage)
    st["outputs"] = ver["layers"]
    st["outputs_verified"] = ver["verified"]
    if ver["verified"] == "mismatch":
        st["marker_status"] = st["status"]
        st["status"] = "outputs_incomplete"
        st["final"] = False
        st["outputs_bad"] = ver["bad"]
        st["error"] = ("the marker says {} but its matte layers do not match "
                       "ship_v5.json: {}".format(st["marker_status"],
                                                 "; ".join(ver["bad"])))
    return st


def log_tail(run, n: int = 20) -> str:
    try:
        return "\n".join((Path(run) / "prep" / "_batch.log").read_text()
                         .splitlines()[-n:])
    except OSError:
        return ""


def gate(run, vid: str, stage: str, wait_s: float = 0.0,
         poll_s: float = 5.0, tail: int = 20, _clock=time.monotonic,
         _sleep=time.sleep) -> dict:
    """Block up to wait_s for the marker to pass, then report what it says."""
    deadline = _clock() + min(max(wait_s, 0.0), MAX_WAIT_S)
    t0 = _clock()
    while True:
        st = settle(run, vid, stage, read_marker(run, vid, stage))
        if passed(st) or st["final"] or _clock() >= deadline:
            break
        _sleep(max(poll_s, 0.5))
    st["waited_s"] = round(_clock() - t0, 1)
    ok = passed(st)
    if not ok:
        st["outputs"] = {}
        st["log_tail"] = log_tail(run, tail)
    if stage == "ship":
        st["track_cost_usd"] = read_marker(run, vid, "track")["keys"].get("cost_usd")
    return st


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run", required=True)
    p.add_argument("--id", required=True)
    p.add_argument("--stage", required=True)
    p.add_argument("--wait-s", type=float, default=0.0,
                   help=f"block until the marker passes, at most {MAX_WAIT_S}s")
    p.add_argument("--poll-s", type=float, default=5.0)
    p.add_argument("--log-tail", type=int, default=20)
    a = p.parse_args()
    try:
        out = gate(a.run, a.id, a.stage, a.wait_s, a.poll_s, a.log_tail)
    except Exception as exc:                              # noqa: BLE001
        # A GATE NEVER RETURNS NOTHING.  Even a bug here reports a pollable,
        # non-final state instead of leaving the workflow with a null.
        out = {"id": a.id, "stage": a.stage, "status": "unreadable",
               "final": False, "override_used": False,
               "error": f"{type(exc).__name__}: {exc}"}
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
