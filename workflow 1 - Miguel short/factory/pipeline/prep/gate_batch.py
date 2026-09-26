#!/usr/bin/env python
"""gate_batch.py — ONE watcher for a whole batch's stage markers.

Added 2026-09-14 (run 19 supervisor note 4 and the efficiency review).  The
workflow used to spawn one GATE agent per recording per stage, and each of
them sat idle for up to 570 s waiting on its own marker; with six recordings
that is twelve waiting agents before a single pixel exists.  prep_batch does
the whole batch in one process, so the markers land within minutes of each
other and one watcher can report all of them.

This file judges nothing.  It polls `gate_marker.gate()` for every id and
returns when every id has PASSED or is FINAL, or when the wait is up.  A
recording whose marker is still non-ok is handed back exactly as
`gate_marker` reports it, so the workflow's per-recording repair round runs
unchanged for that one id.

usage: gate_batch.py --run <run> --stage cut|ship --ids a,b,c [--wait-s 570] [--poll-s 5]
prints one json object:
  {"stage", "ids": {id: <gate_marker result>}, "settled": [...], "pending": [...],
   "all_settled": bool, "waited_s": float}
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gate_marker import MAX_WAIT_S, PASS_STATUS, FINAL_STATUS, gate  # noqa: E402


def settled(state: dict) -> bool:
    return state.get("status") in PASS_STATUS or state.get("status") in FINAL_STATUS


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", required=True)
    ap.add_argument("--stage", required=True)
    ap.add_argument("--ids", required=True, help="comma-separated recording ids")
    ap.add_argument("--wait-s", type=float, default=MAX_WAIT_S)
    ap.add_argument("--poll-s", type=float, default=5.0)
    ap.add_argument("--log-tail", type=int, default=8)
    a = ap.parse_args()
    ids = [x.strip() for x in a.ids.split(",") if x.strip()]
    t0 = time.time()
    deadline = t0 + min(a.wait_s, MAX_WAIT_S)
    out = {}
    while True:
        for vid in ids:
            if vid in out and settled(out[vid]):
                continue
            try:
                out[vid] = gate(a.run, vid, a.stage, 0.0, a.poll_s, a.log_tail)
            except Exception as exc:                          # noqa: BLE001
                out[vid] = {"id": vid, "stage": a.stage, "status": "unreadable", "final": False,
                            "override_used": False, "error": f"{type(exc).__name__}: {exc}"}
        pending = [v for v in ids if not settled(out[v])]
        # RETURN AS SOON AS EVERY MARKER HAS LANDED, settled or not (2026-09-14,
        # run 20, first live use): waiting for a non-ok id to turn ok held the two
        # good recordings hostage behind one refused cut.  An id whose marker
        # says error/REFUSED is handed back as it stands; the workflow's
        # per-recording gate + repair round own it from there.  Only a MISSING or
        # still-RUNNING marker is worth waiting for here.
        # ...and an id whose CUT already failed will never land a later marker
        # until its repair round runs: it is not worth waiting for either
        # (run 20: grok1080's cutout waited on grokwatch's ship behind a refused cut).
        def upstream_blocked(v):
            if a.stage == "cut":
                return False
            try:
                c = gate(a.run, v, "cut", 0.0, a.poll_s, 0)
            except Exception:                                 # noqa: BLE001
                return False
            return c.get("status") not in PASS_STATUS and c.get("status") not in ("missing", "running")
        unlanded = [v for v in pending if out[v].get("status") in ("missing", "running", "unreadable") and not upstream_blocked(v)]
        if not pending or not unlanded or time.time() >= deadline:
            break
        time.sleep(a.poll_s)
    rec = {"stage": a.stage, "ids": out, "unlanded": [v for v in ids if out[v].get("status") in ("missing", "running", "unreadable") and not upstream_blocked(v)],
           "settled": [v for v in ids if settled(out[v])], "pending": [v for v in ids if not settled(out[v])],
           "all_settled": all(settled(out[v]) for v in ids), "waited_s": round(time.time() - t0, 1)}
    print(json.dumps(rec, indent=1, default=str))


if __name__ == "__main__":
    main()
