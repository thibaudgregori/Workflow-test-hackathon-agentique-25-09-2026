"""The factory's roots, resolved from this file, never from a home-relative literal.

2026-09-20: 38 files each spelled `Path.home() / "Documents/Workspace/..."`; the second audit asked for one
resolver. New code imports these; old code resolves from `Path(__file__)` (same values).
"""
from pathlib import Path

FACTORY = Path(__file__).resolve().parents[1]
WORKSPACE = FACTORY.parents[3]
VENV_PY = WORKSPACE / ".venv/bin/python"
MOVIES = Path.home() / "Movies"
SHORTS_LIBRARY = MOVIES / "Shorts Factory"            # Ready to Publish / Partially Published / Published Shorts
