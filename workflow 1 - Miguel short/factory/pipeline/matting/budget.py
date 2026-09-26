"""Experiment budget ledger for paid matting calls (opt-in, `experiment_budget=True` in client.execute).

Ported from the outline lab's run_test.py on 2026-09-20 so production code stops importing a dated
experiment folder. The ledger lives in the run under review (`<run>/review/experiment_budget.json`),
never beside the tools; SHORTS_RUN or the newest run on disk decides which run.
"""
import fcntl, json, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runs import newest_run  # noqa: E402


def _run():
    return Path(os.environ["SHORTS_RUN"]).expanduser().resolve() if os.environ.get("SHORTS_RUN") else newest_run()


def _ledger():
    d = _run() / "review"; d.mkdir(parents=True, exist_ok=True)
    return d / "experiment_budget.json"


def reserve(request_id, spec, reserve_usd=.40):
    ledger = _ledger()
    with (ledger.parent / ".experiment_budget.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        data = json.loads(ledger.read_text()) if ledger.exists() else {"limit_usd": 10, "build_and_overhead_reserve_usd": 2, "calls": []}
        if any(r["id"] == request_id for r in data["calls"]):
            raise RuntimeError("This request was already dispatched; use saved output or inspect its call ID. No blind retry.")
        spent = round(data.get("build_and_overhead_reserve_usd", 2) * 100) + sum(round(x.get("accounted_usd", x["reserved_usd"]) * 100) for x in data["calls"])
        if spent + round(reserve_usd * 100) > round(data["limit_usd"] * 100):
            raise RuntimeError("Budget exhausted")
        data["calls"].append({"id": request_id, "reserved_usd": reserve_usd, "spec": spec, "state": "reserved", "at": time.time()})
        ledger.write_text(json.dumps(data, indent=2))


def update(request_id, **fields):
    ledger = _ledger()
    with (ledger.parent / ".experiment_budget.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        data = json.loads(ledger.read_text())
        next(x for x in data["calls"] if x["id"] == request_id).update(fields)
        ledger.write_text(json.dumps(data, indent=2))
