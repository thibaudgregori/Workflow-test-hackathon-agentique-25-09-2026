#!/usr/bin/env python3
"""clerk_video_batch.py — RUN THE VIEWER TEST'S WATCHER ON A WHOLE VIDEO AT ONCE.

`pipeline/semantic_review.md` says "one video = three Gemini calls (split, cutout,
whiteboard) and one clerk report".  Until 2026-09-02 the procedure ran those three
one after another, and each of them ran its own four windows one after another —
twelve independent network calls in a single file, laid end to end.

    MEASURED, 2026-09-02, on the clerk-v3 repair pass (5 renders):
      serial, --jobs 1 : codexvoice_split 236.5 s, codexvoice_cutout 611.0 s
                         -> the five-render pass was still unfinished at 50 min
      parallel         : see `wall_clock_s` in each `cands_*.json` of the re-run

Nothing about the procedure asked for that order.  Every window is its own encode,
its own upload, its own prompt and its own response; the union happens afterwards
in `merge_passes`, and the clerk adjudicates the union.  The only thing making it
serial was two nested `for` loops.

THIS RUNNER FANS OUT THE RENDERS; `clerk_video_gemini.py --jobs` FANS OUT THE
WINDOWS INSIDE EACH ONE.  Three renders x four windows = twelve calls in flight,
which is one call's latency for a whole video instead of twelve.

COST IS UNCHANGED.  Concurrency changes WHEN the tokens are spent, not how many:
the same renders, the same windows, the same media resolution, the same model.
The per-call retry in `clerk_video_gemini.generate_retry` absorbs the 429/503s
that only concurrency produces.

    # a whole video, all three staged renders, all windows, in parallel
    $PY pipeline/clerk_video_batch.py codexvoice --day 2026-09-02

    # or name the files explicitly (any number, any format)
    $PY pipeline/clerk_video_batch.py --render split=/path/a.mp4 \
        --render cutout=/path/b.mp4 --vid codexvoice
"""
from __future__ import annotations

import argparse
import concurrent.futures as cfutures
import json
import subprocess
import sys
import time
from pathlib import Path

F = Path(__file__).resolve().parents[1]
PY = str(Path.home() / "Documents/Workspace/.venv/bin/python")
CLERK = F / "pipeline/clerk_video_gemini.py"
PLATFORM = {"split": "youtube", "cutout": "tiktok", "whiteboard": "reels"}
from runs import newest_run  # noqa: E402
STAGE_ROOT = None  # resolved per call: <newest run>/staging (Daily/ was pre-migration state, 2026-09-20)


def one(vid: str, fmt: str, mp4: Path, out: Path, jobs: int, extra: list[str]) -> dict:
    t0 = time.time()
    log = out.with_suffix(".log")
    cmd = [PY, str(CLERK), str(mp4), vid, "--fmt", fmt, "--out", str(out),
           "--jobs", str(jobs), *extra]
    with log.open("w") as fh:
        rc = subprocess.call(cmd, stdout=fh, stderr=subprocess.STDOUT)
    rec = {"fmt": fmt, "render": str(mp4), "out": str(out), "log": str(log),
           "exit": rc, "wall_clock_s": round(time.time() - t0, 1)}
    if rc == 0 and out.exists():
        d = json.loads(out.read_text())
        rec |= {"counts": d["counts"], "cost_usd": d["cost_usd"],
                "watcher_wall_clock_s": d["wall_clock_s"], "jobs": d.get("jobs")}
    print(f"[{fmt}] exit={rc} {rec['wall_clock_s']}s "
          f"{rec.get('counts', '')} ${rec.get('cost_usd', 0)}", file=sys.stderr)
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("video_id", nargs="?", default=None)
    ap.add_argument("--day", default=None,
                    help="Daily/<day> folder to read the staged renders from")
    ap.add_argument("--render", action="append", default=[],
                    help="fmt=/path/to.mp4 — repeatable; overrides --day discovery")
    ap.add_argument("--vid", default=None, help="video id when using --render")
    ap.add_argument("--out-dir", default=None, help="defaults to <newest run>/review")
    ap.add_argument("--jobs", type=int, default=4,
                    help="concurrent WINDOW calls inside each render (default 4)")
    ap.add_argument("--render-jobs", type=int, default=3,
                    help="concurrent RENDERS (default 3 = one video's three formats)")
    ap.add_argument("--tag", default="", help="suffix for the output filenames")
    a, extra = ap.parse_known_args()
    if a.out_dir is None:
        from runs import newest_run
        a.out_dir = str(newest_run() / "review")

    vid = a.vid or a.video_id
    if not vid:
        ap.error("a video id is required (positional, or --vid with --render)")

    jobs_in: list[tuple[str, Path]] = []
    if a.render:
        for spec in a.render:
            fmt, _, path = spec.partition("=")
            jobs_in.append((fmt, Path(path)))
    else:
        if not a.day:
            ap.error("--day is required unless --render is given")
        for fmt, plat in PLATFORM.items():
            p = newest_run() / "staging" / plat / f"{vid}_{fmt}.mp4"
            if p.exists():
                jobs_in.append((fmt, p))
    if not jobs_in:
        ap.error("no renders found to watch")

    out_dir = Path(a.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    with cfutures.ThreadPoolExecutor(max_workers=max(1, a.render_jobs)) as pool:
        recs = list(pool.map(
            lambda fp: one(vid, fp[0], fp[1],
                           out_dir / f"cands{a.tag}_{vid}_{fp[0]}.json",
                           a.jobs, extra),
            jobs_in))

    rep = {"video_id": vid, "renders": len(recs), "render_jobs": a.render_jobs,
           "window_jobs": a.jobs,
           "wall_clock_s": round(time.time() - t0, 1),
           "sum_of_render_wall_clock_s": round(sum(r["wall_clock_s"] for r in recs), 1),
           "cost_usd": round(sum(r.get("cost_usd", 0.0) for r in recs), 6),
           "failed": [r["fmt"] for r in recs if r["exit"] != 0],
           "results": recs}
    print(json.dumps(rep, indent=1))
    return 1 if rep["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
