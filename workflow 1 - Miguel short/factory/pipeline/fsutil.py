"""File digests and atomic json, once. 2026-09-20: ten private copies of the same streaming sha256."""
from __future__ import annotations
import hashlib, json, os
from pathlib import Path


def digest(path: Path | str, algorithm: str = "sha256") -> str:
    h = hashlib.new(algorithm)
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def atomic_json(path: Path | str, data) -> None:
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n")
    os.replace(tmp, p)
