"""Where the CURRENT run lives. One helper, used everywhere a tool needs a run folder.

NOTHING PERMANENT LIVES IN A RUN (Miguel, 2026-09-20). Run folders are disposable working
state, retired the moment their shorts are published and archived on Drive. So no tool may
pin a run by number: `newest_run()` is the only default, and a run that is not on disk is a
clear error, never a silent read of somebody else's folder.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

FACTORY = Path(__file__).resolve().parents[1]
RUNS_ROOT = FACTORY / "runs"          # every shorts_run<N> lives here (2026-09-21, out of the factory root)


def run_number(path: Path) -> int:
    m = re.search(r"shorts_run(\d+)$", path.name)
    return int(m.group(1)) if m else -1


def all_runs(root: Path = RUNS_ROOT) -> list[Path]:
    return sorted((d for d in root.glob("shorts_run*") if d.is_dir() and run_number(d) >= 0), key=run_number)


def newest_run(root: Path = RUNS_ROOT) -> Path:
    """`SHORTS_RUN` in the environment wins; otherwise the highest-numbered run on disk."""
    env = os.environ.get("SHORTS_RUN")
    if env:
        return Path(env).expanduser().resolve()
    runs = all_runs(root)
    if not runs:
        raise FileNotFoundError(f"no shorts_run<N> folder under {root}; pass --run or set SHORTS_RUN")
    return runs[-1]
