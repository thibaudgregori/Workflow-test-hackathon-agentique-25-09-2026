#!/usr/bin/env python3
"""THE COST REPORT — what a run cost, per video, per service, per short.

Reads `<run>/costs.jsonl` (see `pipeline/costs.py`) and writes two files:

    <run>/review/COSTS.md      the tables a person reads
    <run>/review/costs.json    the same numbers for a workflow to quote

It ADDS UP; it does not price anything.  Every dollar here was measured by the
code that made the call and written to the ledger at that moment, so this file
cannot disagree with the run unless the ledger is missing a row — and a missing
row is visible, because the report also says which stages it never saw.

    cost_report.py --run <run> [--md] [--json] [--quiet]

`--md` / `--json` print the rendered markdown / the json to stdout as well; the
two files are written either way.  `render_and_check.py --stage` calls this
after the last render of its batch, so the number exists by the end of the
video without anyone asking for it.
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import costs as C                                                # noqa: E402

SERVICE_ORDER = ("modal", "gemini", "elevenlabs", "other")
# Every stage the instrumented call sites can write, in pipeline order, so a
# stage that is MISSING from a run is visible as a gap rather than an absence.
# A repair round's re-track books under `track` (it is the same container on a
# new tag), which is why there is no `repair` stage here.
STAGE_ORDER = ("scribe", "sweep", "track", "ship", "draft",
               "render", "watch", "gate3", "verify", "clerk_watch")
# stages whose absence is normal and says something rather than nothing
EXPECTED_ZERO = {
    "ship": "the matte shipped on the laptop (`--ship-local`), which is free",
    "draft": "no draft render was paid for before the real one",
    "verify": "no flag verification round ran",
    "clerk_watch": "the clerk did not re-watch — procedure v3.1, as intended",
}
HUMAN = {"modal": "Modal", "gemini": "Gemini", "elevenlabs": "ElevenLabs",
         "other": "other"}


def _f(x) -> float:
    try:
        return float(x or 0.0)
    except (TypeError, ValueError):
        return 0.0


def staged_shorts(run: Path) -> tuple[int, list[str]]:
    """The delivered files, out of the render driver's own reports.

    `render_and_check` records the destination it copied to on the record that
    passed its checks, so the staged set is the truth about what the run
    delivered — not the number of renders it paid for (run 13 paid for 24
    renders and delivered 12 files)."""
    dests: list[str] = []
    for p in sorted(glob.glob(str(run / "gen" / "_rc_*.json"))):
        try:
            d = json.loads(Path(p).read_text())
        except Exception:                                        # noqa: BLE001
            continue
        for r in (d.get("results") or []):
            if isinstance(r, dict) and r.get("staged"):
                dests.append(str(r["staged"]))
    uniq = sorted(set(dests))
    return len(uniq), uniq


def build(run: Path) -> dict:
    rows = C.load(run)
    services = {s: 0.0 for s in SERVICE_ORDER}
    stages: dict[str, float] = {}
    videos: dict[str, dict] = {}
    fmts: dict[str, float] = {}
    for r in rows:
        svc = r.get("service") or "other"
        usd = _f(r.get("usd"))
        services[svc] = services.get(svc, 0.0) + usd
        stages[r.get("stage") or "-"] = stages.get(r.get("stage") or "-", 0.0) + usd
        vid = r.get("video") or "(run-wide)"
        v = videos.setdefault(vid, {s: 0.0 for s in SERVICE_ORDER}
                              | {"total": 0.0, "rows": 0, "stages": {}})
        v[svc] = v.get(svc, 0.0) + usd
        v["total"] += usd
        v["rows"] += 1
        v["stages"][r.get("stage") or "-"] = round(
            v["stages"].get(r.get("stage") or "-", 0.0) + usd, 6)
        if r.get("fmt"):
            fmts[r["fmt"]] = fmts.get(r["fmt"], 0.0) + usd

    for v in videos.values():
        for k in list(v):
            if isinstance(v[k], float):
                v[k] = round(v[k], 6)

    n_staged, dests = staged_shorts(run)
    run_total = round(sum(services.values()), 6)
    seen = {s for s in stages}
    return {
        "run": run.name,
        "run_dir": str(run),
        "ledger": str(run / C.LEDGER_NAME),
        "rows": len(rows),
        "total_usd": run_total,
        "by_service": {k: round(v, 6) for k, v in services.items()},
        "by_stage": {k: round(stages[k], 6)
                     for k in list(STAGE_ORDER) + sorted(set(stages) - set(STAGE_ORDER))
                     if k in stages},
        "by_video": dict(sorted(videos.items())),
        "by_format": {k: round(v, 6) for k, v in sorted(fmts.items())},
        "staged_shorts": n_staged,
        "staged_files": dests,
        "usd_per_delivered_short": (round(run_total / n_staged, 6)
                                    if n_staged else None),
        "stages_never_recorded": [s for s in STAGE_ORDER if s not in seen],
        "scribe_rate_note": C.SCRIBE_RATE_SOURCE,
    }


def markdown(rep: dict) -> str:
    w: list[str] = []
    a = w.append
    a(f"# What {rep['run']} cost")
    a("")
    tot = rep["total_usd"]
    n = rep["staged_shorts"]
    per = rep["usd_per_delivered_short"]
    a(f"**${tot:.2f} for the whole run.** "
      + (f"{n} file{'s' if n != 1 else ''} were staged, so a delivered short "
         f"cost **${per:.3f}**." if per is not None
         else "Nothing was staged yet, so there is no per-short number."))
    a("")
    a("Every number below was measured by the code that made the call and "
      "written to `costs.jsonl` at that moment. Nothing here is re-priced, and "
      "nothing is added by hand.")
    a("")

    a("## By service")
    a("")
    a("| service | USD |")
    a("|---|---|")
    for s in SERVICE_ORDER:
        v = rep["by_service"].get(s, 0.0)
        if v:
            a(f"| {HUMAN[s]} | {v:.4f} |")
    a(f"| **run total** | **{tot:.4f}** |")
    a("")

    a("## By stage")
    a("")
    a("| stage | USD |")
    a("|---|---|")
    for k, v in rep["by_stage"].items():
        a(f"| {k} | {v:.4f} |")
    a("")

    a("## By video")
    a("")
    a("| video | Modal | Gemini | ElevenLabs | other | total |")
    a("|---|---|---|---|---|---|")
    for vid, v in rep["by_video"].items():
        a(f"| {vid} | {v.get('modal', 0):.4f} | {v.get('gemini', 0):.4f} | "
          f"{v.get('elevenlabs', 0):.4f} | {v.get('other', 0):.4f} | "
          f"**{v.get('total', 0):.4f}** |")
    a(f"| **run** | **{rep['by_service'].get('modal', 0):.4f}** | "
      f"**{rep['by_service'].get('gemini', 0):.4f}** | "
      f"**{rep['by_service'].get('elevenlabs', 0):.4f}** | "
      f"**{rep['by_service'].get('other', 0):.4f}** | **{tot:.4f}** |")
    a("")

    if rep["by_format"]:
        a("## By format")
        a("")
        a("| format | USD |")
        a("|---|---|")
        for k, v in rep["by_format"].items():
            a(f"| {k} | {v:.4f} |")
        a("")
        a("A format's line holds only the money that is spent per format — the "
          "render, its watcher and its Gate 3. The cut, the sweep, the track "
          "and the matte are paid once per recording and serve all three "
          "formats, so they are in the video's line and not here.")
        a("")

    if rep["stages_never_recorded"]:
        a("## Stages this run never recorded")
        a("")
        a("These stages exist in the pipeline and wrote no ledger row. A stage "
          "with a known reason is not a hole; a stage without one either did "
          "not run, or ran and was never booked — and that is the only way the "
          "run total above can be too low.")
        a("")
        for s in rep["stages_never_recorded"]:
            a(f"- `{s}` — {EXPECTED_ZERO.get(s, 'no reason on record. CHECK IT.')}")
        a("")

    a("## Notes")
    a("")
    a(f"- ElevenLabs Scribe: {rep['scribe_rate_note']}.")
    a(f"- Ledger: `{rep['ledger']}` ({rep['rows']} row(s) after "
      "replace-by-key).")
    a("")
    return "\n".join(w)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--run", default=None)
    ap.add_argument("--md", action="store_true", help="also print the markdown")
    ap.add_argument("--json", action="store_true", help="also print the json")
    ap.add_argument("--quiet", action="store_true",
                    help="write the files, print only the one-line total")
    a = ap.parse_args()

    run = C.resolve_run(a.run)
    rep = build(run)
    review = run / "review"
    review.mkdir(parents=True, exist_ok=True)
    md = markdown(rep)
    (review / "COSTS.md").write_text(md)
    (review / "costs.json").write_text(json.dumps(rep, indent=1))

    if a.md:
        print(md)
    if a.json:
        print(json.dumps(rep, indent=1))
    if not a.quiet:
        per = rep["usd_per_delivered_short"]
        print(f"[costs] {rep['run']}: ${rep['total_usd']:.4f} total "
              f"(modal ${rep['by_service'].get('modal', 0):.4f}, "
              f"gemini ${rep['by_service'].get('gemini', 0):.4f}, "
              f"elevenlabs ${rep['by_service'].get('elevenlabs', 0):.4f}) "
              f"over {rep['staged_shorts']} staged file(s)"
              + (f" = ${per:.3f} per short" if per is not None else "")
              + f"  -> {review / 'COSTS.md'}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
