#!/usr/bin/env python3
"""THE COST LEDGER — one append-only line per paid call, written where the price
is measured.

WHY (Miguel, 2026-09-04): "by the end of the video I want to know modal cost per
video plus per total run as well as gemini costs ... every paid service I want to
quantify."  Run 13's cost table was assembled BY HAND out of six different
artefact families (`prep/_batch.json`, `gen/_rc_*.json`, `review/cands_*.json`,
`review/clerk_cands_*.json`, the Gate 3 number that was printed and never
stored, and the sam2 session run records), and it came out low: the report says
~$2.7, the artefacts say ~$2.9 before the chair job.  Money that is re-added by
hand every run is money that is reported wrong.

WHAT THIS IS.  A file, `<run>/costs.jsonl`, one JSON object per line:

    {"key":   "gemini|watch|dgxspark|split|review/cands_dgxspark_split.json@1788492367",
     "ts":    "2026-09-04T13:05:11Z",
     "run":   "shorts_run<N>",
     "service": "modal" | "gemini" | "elevenlabs" | "other",
     "stage": "sweep|track|ship|repair|render|watch|gate3|verify|clerk_watch|scribe",
     "video": "dgxspark" | null,
     "fmt":   "split" | null,
     "usd":   0.050347,
     "units": "97.6 gpu-s H100"  |  "83,038 in / 11,460 out tokens"  |  "84 s audio",
     "note":  "post-render watcher, gemini-3.5-flash-lite",
     "ref":   "review/cands_dgxspark_split.json@1788492367"}

NOTHING IS RE-PRICED HERE.  Every `usd` this ledger holds was computed by the
code that made the call — `sam2/track.py:cost`, `render/modal_render.py:price`,
the Gemini watchers' own token arithmetic, `qc_v3`'s own arithmetic.  The one
price this module owns is ElevenLabs Scribe, because the API returns no cost and
nothing else in the factory computes one (see SCRIBE_USD_PER_AUDIO_HOUR).

THE KEY, AND WHY A RE-RUN DOES NOT DOUBLE COUNT.  `key` is
`service|stage|video|fmt|ref`, and a `record()` whose key already exists
REPLACES that line instead of adding one.  So re-reading a report, re-running
the backfill, or a retry that lands the same artefact twice cannot inflate a
total.  For that to work the `ref` must name ONE PAID CALL, not one file: every
call site therefore writes `<path relative to the run>@<the call's own measured
identity>` — the Modal container's `t_import_epoch` or `container` id, the
render's own epoch for the watcher that watched it, the audio duration for a
Scribe pass.  A second round writes a second container, hence a second key.

RUN RESOLUTION, in order: the explicit `run` argument, then `$SHORTS_RUN`, then
walking up from the `ref` path until a `shorts_run*` directory appears.  A call
site that cannot resolve a run does not raise — see `safe_record`, which is what
the pipeline itself calls, so a broken ledger can never fail a render.

CLI
---
    costs.py add --run <run> --service elevenlabs --stage scribe \
        --video <id> --units "84 s audio" --usd 0.0093 [--note ...] [--ref ...]
    costs.py list  --run <run> [--service modal] [--video id]
    costs.py total --run <run>
    costs.py compact --run <run>       # rewrite the file with replaced keys dropped

The report that turns this into per-video / per-format / per-run tables is
`pipeline/cost_report.py`.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import sys
import time
from pathlib import Path

WORKSPACE = Path.home() / "Documents" / "Workspace"
F = WORKSPACE / "projects/personal/content/shorts-factory"

LEDGER_NAME = "costs.jsonl"
LOCK_NAME = ".costs.lock"

SERVICES = ("modal", "gemini", "elevenlabs", "other")

# ---------------------------------------------------------------------------
# THE ONE PRICE THIS FILE OWNS
# ---------------------------------------------------------------------------
# ElevenLabs Scribe v2 returns `audio_duration_secs` and NO cost and NO
# character count, and no other file in this factory prices it — so a Scribe
# pass was invisible in every run total before 2026-09-04.  The rate is the
# published Speech-to-Text list rate per hour of audio; `tools/elevenlabs.md`
# carries it under "Speech To Text" with this constant named as its consumer.
# It is an ESTIMATE against the live plan (the plan may bill less), every row it
# produces says so in its note, and the override exists so a verified rate
# replaces it without a code change.
SCRIBE_USD_PER_AUDIO_HOUR = float(
    os.environ.get("SCRIBE_USD_PER_AUDIO_HOUR", "0.40"))
SCRIBE_RATE_SOURCE = (f"estimate at ${SCRIBE_USD_PER_AUDIO_HOUR:.2f}/audio-hour "
                      f"(ElevenLabs Scribe list rate, tools/elevenlabs.md; "
                      f"the API returns no cost, so this is not measured)")


def scribe_usd(seconds: float | int | None) -> float:
    """The Scribe estimate for `seconds` of audio.  0.0 for a missing duration,
    because a guessed duration is worse than an absent row."""
    try:
        s = float(seconds)
    except (TypeError, ValueError):
        return 0.0
    if s <= 0:
        return 0.0
    return round(s / 3600.0 * SCRIBE_USD_PER_AUDIO_HOUR, 6)


# ---------------------------------------------------------------------------
# where the ledger lives
# ---------------------------------------------------------------------------
def _looks_like_run(p: Path) -> bool:
    if p.name.startswith("shorts_run"):
        return True
    return (p / "prep").is_dir() and (p / "review").is_dir()


def resolve_run(run: str | Path | None = None,
                ref: str | Path | None = None) -> Path:
    """The run directory, from the explicit argument, then `$SHORTS_RUN`, then
    by walking up from `ref`.  Raises when none of the three answers."""
    for cand in (run, os.environ.get("SHORTS_RUN") or None):
        if not cand:
            continue
        p = Path(str(cand)).expanduser()
        if not p.is_absolute():
            p = (F / p) if (F / p).exists() else p.resolve()
        p = p.resolve()
        if p.is_dir():
            here = p
            for _ in range(8):
                if _looks_like_run(here):
                    return here
                if here.parent == here:
                    break
                here = here.parent
            return p                       # a directory was named; trust it
    if ref:
        here = Path(str(ref)).expanduser().resolve()
        if here.is_file():
            here = here.parent
        for _ in range(10):
            if _looks_like_run(here):
                return here
            if here.parent == here:
                break
            here = here.parent
    raise ValueError("costs: no run — pass run=, set $SHORTS_RUN, or give a "
                     "ref inside a shorts_run* directory")


def ledger_path(run: str | Path | None = None,
                ref: str | Path | None = None) -> Path:
    return resolve_run(run, ref) / LEDGER_NAME


def rel(run: str | Path, path: str | Path | None) -> str | None:
    """`path` relative to the run when it is inside it, else its absolute
    string.  Refs are stored short so a ledger reads like a run."""
    if path is None:
        return None
    root = resolve_run(run)
    p = Path(str(path)).expanduser()
    try:
        p = p.resolve()
    except OSError:
        pass
    try:
        return str(p.relative_to(root))
    except ValueError:
        return str(p)


def call_ref(run: str | Path, path: str | Path | None,
             ident: str | int | float | None) -> str:
    """THE REF SHAPE: `<path relative to the run>@<this call's own identity>`.

    `ident` is whatever the paid call already measured about itself and never
    repeats: a Modal `container` id, `t_import_epoch`, an audio duration.  It is
    what makes a second round a second ledger row instead of a replacement."""
    base = rel(run, path) or "-"
    if ident in (None, ""):
        return base
    if isinstance(ident, float):
        ident = f"{ident:.0f}" if ident > 1e6 else f"{ident}"
    return f"{base}@{ident}"


def make_key(service: str, stage: str, video: str | None, fmt: str | None,
             ref: str | None) -> str:
    return "|".join([str(service), str(stage), str(video or "-"),
                     str(fmt or "-"), str(ref or "-")])


# ---------------------------------------------------------------------------
# read / write
# ---------------------------------------------------------------------------
def _read_lines(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for ln in path.read_text().splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            rows.append(json.loads(ln))
        except json.JSONDecodeError:
            continue                       # a torn line is never a total
    return rows


class _Lock:
    """One writer at a time, across THREADS and PROCESSES.  prep_batch writes
    from five threads, render_and_check from one thread per render, and
    track.py writes from its own process — all into the same file."""

    def __init__(self, run: Path):
        self.p = run / LOCK_NAME
        self.h = None

    def __enter__(self):
        self.p.parent.mkdir(parents=True, exist_ok=True)
        self.h = self.p.open("a+")
        fcntl.flock(self.h.fileno(), fcntl.LOCK_EX)
        return self

    def __exit__(self, *exc):
        try:
            fcntl.flock(self.h.fileno(), fcntl.LOCK_UN)
        finally:
            self.h.close()
        return False


def record(run: str | Path | None, service: str, stage: str, usd: float, *,
           video: str | None = None, fmt: str | None = None,
           units: str | None = None, note: str | None = None,
           ref: str | None = None, ts: str | None = None) -> dict:
    """Append one paid call to `<run>/costs.jsonl`, replacing its own key.

    Returns the row that was written.  `service` outside the known four is
    accepted as `other` with the given name kept in the note, because an
    unpriced new service must still show up in a total."""
    root = resolve_run(run, ref)
    svc = str(service).lower()
    if svc not in SERVICES:
        note = f"service={service}; " + (note or "")
        svc = "other"
    row = {
        "key": make_key(svc, stage, video, fmt, ref),
        "ts": ts or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "run": root.name,
        "service": svc,
        "stage": str(stage),
        "video": video,
        "fmt": fmt,
        "usd": round(float(usd or 0.0), 6),
        "units": units,
        "note": (note or None) and str(note).strip() or None,
        "ref": ref,
    }
    path = root / LEDGER_NAME
    with _Lock(root):
        existing = _read_lines(path)
        if any(r.get("key") == row["key"] for r in existing):
            kept = [r for r in existing if r.get("key") != row["key"]] + [row]
            tmp = path.with_suffix(".jsonl.tmp")
            tmp.write_text("".join(json.dumps(r) + "\n" for r in kept))
            os.replace(tmp, path)
        else:
            with path.open("a") as h:
                h.write(json.dumps(row) + "\n")
    return row


def safe_record(*a, **kw) -> dict | None:
    """`record` that can never fail a pipeline stage.  THIS is what every call
    site uses: a ledger is bookkeeping, and bookkeeping does not get to kill a
    render that Modal has already been paid for."""
    try:
        return record(*a, **kw)
    except Exception as exc:                                     # noqa: BLE001
        print(f"[costs] not recorded ({type(exc).__name__}: {exc})",
              file=sys.stderr, flush=True)
        return None


def record_many(run: str | Path | None, rows: list[dict]) -> int:
    """`rows` are `record` kwargs without `run`.  One lock for the batch."""
    n = 0
    for r in rows:
        if safe_record(run, r.pop("service"), r.pop("stage"),
                       r.pop("usd"), **r) is not None:
            n += 1
    return n


def load(run: str | Path | None = None, ref: str | Path | None = None,
         *, dedupe: bool = True) -> list[dict]:
    """Every row, LAST WRITE PER KEY WINNING.  Replacement happens on write as
    well, but a reader that dedupes cannot be fooled by a file that was
    appended to while a rewrite was in flight."""
    rows = _read_lines(resolve_run(run, ref) / LEDGER_NAME)
    if not dedupe:
        return rows
    by_key: dict[str, dict] = {}
    for r in rows:
        by_key[r.get("key") or json.dumps(r, sort_keys=True)] = r
    return list(by_key.values())


def total(run: str | Path | None = None) -> float:
    return round(sum(float(r.get("usd") or 0.0) for r in load(run)), 6)


def compact(run: str | Path | None = None) -> int:
    """Rewrite the file with only the surviving row per key.  Returns the
    number of lines dropped."""
    root = resolve_run(run)
    path = root / LEDGER_NAME
    with _Lock(root):
        raw = _read_lines(path)
        by_key: dict[str, dict] = {}
        for r in raw:
            by_key[r.get("key") or json.dumps(r, sort_keys=True)] = r
        kept = list(by_key.values())
        tmp = path.with_suffix(".jsonl.tmp")
        tmp.write_text("".join(json.dumps(r) + "\n" for r in kept))
        os.replace(tmp, path)
    return len(raw) - len(kept)


# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="record one paid call")
    a.add_argument("--run", default=None)
    a.add_argument("--service", required=True)
    a.add_argument("--stage", required=True)
    a.add_argument("--usd", type=float, required=True)
    a.add_argument("--video", default=None)
    a.add_argument("--fmt", default=None)
    a.add_argument("--units", default=None)
    a.add_argument("--note", default=None)
    a.add_argument("--ref", default=None)

    for name in ("list", "total", "compact"):
        s = sub.add_parser(name)
        s.add_argument("--run", default=None)
        if name == "list":
            s.add_argument("--service", default=None)
            s.add_argument("--stage", default=None)
            s.add_argument("--video", default=None)

    p = ap.parse_args()
    if p.cmd == "add":
        row = record(p.run, p.service, p.stage, p.usd, video=p.video,
                     fmt=p.fmt, units=p.units, note=p.note, ref=p.ref)
        print(json.dumps(row))
        return 0
    if p.cmd == "list":
        rows = [r for r in load(p.run)
                if (not p.service or r.get("service") == p.service)
                and (not p.stage or r.get("stage") == p.stage)
                and (not p.video or r.get("video") == p.video)]
        rows.sort(key=lambda r: (r.get("service") or "", r.get("stage") or "",
                                 r.get("video") or ""))
        for r in rows:
            print(f"{r.get('service'):<11} {r.get('stage'):<12} "
                  f"{str(r.get('video') or '-'):<16} "
                  f"{str(r.get('fmt') or '-'):<12} "
                  f"${float(r.get('usd') or 0):>9.6f}  {r.get('units') or ''}")
        print(f"{len(rows)} row(s)  "
              f"${round(sum(float(r.get('usd') or 0) for r in rows), 6)}")
        return 0
    if p.cmd == "total":
        print(json.dumps({"run": resolve_run(p.run).name,
                          "rows": len(load(p.run)),
                          "total_usd": total(p.run)}, indent=1))
        return 0
    print(json.dumps({"dropped": compact(p.run)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
