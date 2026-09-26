#!/usr/bin/env python3
"""RENDER AND CHECK — every check starts the moment ITS render lands.

WHY (Miguel, 2026-09-03)
------------------------
`modal_render.py` already fans three renders out at once, and they come back at
three different times: the 1080x1920 whiteboard in about a minute, the
split (2160x3840 before 2026-09-03, 1080x1920 since) in several.  Until now the checks waited for the whole batch,
so the fastest render sat idle behind the slowest one and every qc_pass and
every watcher call ran in a queue afterwards.  Nothing about that is necessary:
a check needs ONE file, and that file exists the instant its own render returns.

So this driver submits the renders, and **as each MP4 lands it starts that
file's own qc_pass and its own Gemini watcher, in a thread**.  The last render's
checks are the only ones still running when the last render finishes.  The
result is ONE json — per render: the Modal record, the qc_pass report and the
watcher's candidate list — which is what the clerk adjudicates against when the
last one is in.

**Nothing is re-implemented.**  `modal_render`'s own `pack`, `one`, `price` and
`table` are imported and called; `qc_pass.py` and `clerk_video_gemini.py` are
invoked as their own CLIs, with their own flags, and their own JSON is read
back.  This file schedules; it does not measure.

THE SPEC
--------
A JSON file (or `-` for stdin):

    {"out_dir": "<run>/output",
     "run": "<run>",
     "jobs": [
       {"project": "<run>/projects/spark_split",
        "vid": "sparkchrome", "fmt": "split",
        "quality": "high",
        "stage": "~/Movies/Shorts Factory/Daily/2026-09-03/youtube/spark_split.mp4",
        "qc_args": ["--voice-master", "...", "--phone-at", "12.4:...:moon"],
        "watch": true}
     ]}

Per job, `"watch_waiver": "<reason with a measurement>"` lets a render with a
BLOCKING watcher candidate stage anyway, and is recorded on the record; without it
a blocking candidate fails the watch check (2026-09-03).  Prior rounds' qc / watch /
report JSONs are archived as `<stem>.priorN.json`, never overwritten.

Per job, everything but `project` is optional: `vid`/`fmt` are inferred from the
`<id>_<fmt>` project name, `quality` defaults to high, `resolution` to the
composition's own size, and `qc_args` is appended verbatim to the qc_pass call
so a format's extra inputs (`--alpha`, `--edge-box`, `--plate`, `--seams`,
`--phone-at`) stay the caller's business.  A `stage` path is copied to AFTER
qc_pass and the watcher have both passed on that file — a render is not staged
until its checks are in, and this is where that order is actually enforced.

    exit 0   every render landed and every qc_pass verdict passed
    exit 1   something failed; the report names it

CLI
---
    render_and_check.py --spec jobs.json [--json report.json]
        [--no-watch] [--no-qc] [--function render] [--stage]
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import shutil
import subprocess
import sys
import threading
import time
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
F = HERE.parents[1]
sys.path.insert(0, str(HERE))

import modal_render as MR                                            # noqa: E402

sys.path.insert(0, str(F / "pipeline"))
import costs as COSTS                                                # noqa: E402

PY = str(Path.home() / "Documents/Workspace/.venv/bin/python")
APP = MR.APP

_lock = threading.Lock()


def log(tag: str, msg: str) -> None:
    with _lock:
        print(f"[{time.strftime('%H:%M:%S')}] {tag:<26} {msg}", flush=True)


def infer(project: Path) -> tuple[str, str]:
    name = project.name
    for f in ("whiteboard", "cutout", "facesplit", "artifactspine", "takeover",
              "split"):
        if name.endswith("_" + f):
            return name[: -len(f) - 1], f
    return name, ""


def render_args(job: dict, function: str) -> types.SimpleNamespace:
    """The namespace `modal_render.one` reads. Built here rather than parsed,
    because this driver is a caller of that function, not of its CLI."""
    return types.SimpleNamespace(
        quality=job.get("quality", "high"),
        resolution=job.get("resolution") or "",
        fps=job.get("fps"), workers=job.get("workers"),
        session=job.get("session", time.strftime("%Y%m%d-%H%M%S")),
        function=function)


# GEMINI IS PAUSED (Miguel, 2026-09-22: "remove the gemini watcher from the main flow right now").
# Both Gemini calls are off by default: the post-render watcher and qc_pass's Gate 3 describe pass.
# Miguel reviews every staged video himself. Pass --watch to turn both back on for one call.
GEMINI_PAUSED = True


def run_qc(job: dict, render: Path, run: Path | None, out_json: Path, gemini: bool = False) -> dict:
    _archive_prior(out_json)
    cmd = [PY, str(F / "pipeline/qc/qc_pass.py"), str(render),
           "--project", str(job["project"]), "--vid", job["vid"],
           "--fmt", job["fmt"], "--out", str(out_json)]
    if run:
        cmd += ["--run", str(run)]
    if job.get("geom"):
        cmd += ["--geom", str(job["geom"])]
    cmd += [str(x) for x in (job.get("qc_args") or [])]
    if not gemini:
        if "--skip" in cmd:
            i = cmd.index("--skip") + 1
            cmd[i] = ",".join(x for x in (cmd[i].split(",") + ["gate3"]) if x)
        else:
            cmd += ["--skip", "gate3"]
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    rec = {"cmd": " ".join(cmd), "returncode": r.returncode,
           "wall_s": round(time.time() - t0, 1), "report": str(out_json),
           "stdout": r.stdout[-6000:], "stderr": r.stderr[-2000:]}
    if out_json.exists():
        # qc_pass owns the verdict, not this driver. It writes a top-level
        # `verdicts` map (PASS / FAIL / SKIP / ERROR / REPORTED) and a top-level
        # `pass` computed from it; a per-check "pass" key exists on SOME checks
        # and not others, and reading that instead is how this driver first
        # reported every green check on an approved render as a FAIL.
        got = json.loads(out_json.read_text())
        verdicts = got.get("verdicts") or {}
        rec |= {"verdicts": verdicts,
                "failed": [k for k, v in verdicts.items()
                           if v not in ("PASS", "REPORTED")],
                "skipped": got.get("skipped"),
                "wall_s_by_check": got.get("wall_s"),
                "total_wall_s": got.get("total_wall_s")}
        rec["pass"] = bool(got.get("pass")) and r.returncode == 0
    else:
        rec["pass"] = False
        rec["failed"] = ["qc_pass wrote no report"]
    return rec


def run_watch(job: dict, render: Path, out_json: Path, thinking: str) -> dict:
    _archive_prior(out_json)
    # THE TRANSCRIPT IS THIS RUN'S, EXPLICITLY (2026-09-06): the watcher used to
    # glob every shorts_run* and take the lexically last one, so a run-16 file
    # was watched against run 9's words.  Pass the current run's tight
    # transcript and let the watcher refuse a missing one.
    run_dir = Path(job.get("run") or "")
    if not run_dir.name:
        run_dir = next((p for p in render.resolve().parents if p.name.startswith("shorts_run")), Path(""))
    transcript = run_dir / "cuts" / job["vid"] / "transcript_tight.json"
    cmd = [PY, str(F / "pipeline/clerk_video_gemini.py"), str(render),
           job["vid"], "--fmt", job["fmt"], "--out", str(out_json),
           "--thinking", thinking, "--transcript", str(transcript)]
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    rec = {"cmd": " ".join(cmd), "returncode": r.returncode,
           "wall_s": round(time.time() - t0, 1), "out": str(out_json),
           "stderr": r.stderr[-2000:]}
    if out_json.exists():
        got = json.loads(out_json.read_text())
        rec |= {"model": got.get("model"), "cost_usd": got.get("cost_usd"),
                "counts": got.get("counts"),
                "video_summary": (got.get("video_summary") or "")[:400],
                "candidates": [{k: c.get(k) for k in
                                ("t_start", "t_end", "klass", "severity",
                                 "motion_or_held", "claim")}
                               for c in (got.get("candidates") or [])]}
    # A BLOCKING CANDIDATE BLOCKS (2026-09-03, run 12's flags report): until
    # now `pass` was "the watcher process exited 0", so two blocking
    # `named_tool_no_mark` candidates on hermeskanban staged untouched.  Now a
    # blocking candidate fails the check UNLESS the job carries a written
    # waiver (`"watch_waiver": "<why, with a measurement>"`), which is recorded
    # on the record so the clerk and the flags report can see it.  The watcher
    # is still a stop, not a verdict: the clerk rules on the staged file.
    blocking = [c for c in rec.get("candidates", []) if c.get("severity") == "blocking"]
    waiver = (job.get("watch_waiver") or "").strip()
    rec["blocking_candidates"] = len(blocking)
    if blocking and waiver:
        rec["waived_in_writing"] = waiver
    rec["pass"] = (r.returncode == 0) and (not blocking or bool(waiver))
    if blocking and not waiver:
        rec["failed_because"] = (f"{len(blocking)} blocking watcher candidate(s) and no "
                                 f"watch_waiver on the job")
    # UNAVAILABLE IS NOT A VERDICT (2026-09-06): when the Gemini project is at
    # its monthly spending cap every upload returns 429 RESOURCE_EXHAUSTED and
    # the watcher cannot look at the file at all.  That is neither a pass nor a
    # defect; it is recorded as `unavailable`, it does not block staging on its
    # own (the clerk's own decode is mandatory anyway and the procedure covers a
    # missing cands file), and it is never re-tried for money.
    if r.returncode != 0 and not out_json.exists() and (
            "RESOURCE_EXHAUSTED" in r.stderr or "spending cap" in r.stderr):
        rec["unavailable"] = True
        rec["unavailable_because"] = "Gemini API 429 RESOURCE_EXHAUSTED (monthly spending cap); $0"
        rec["pass"] = None
    return rec


def _archive_prior(path: Path) -> None:
    """Keep the previous round's report instead of overwriting it (2026-09-03:
    both Gate 3 failures of run 12 were lost to the next round writing the same
    path).  `<stem>.prior<N><suffix>` beside the file, N counting up."""
    if not path.exists():
        return
    n = 1
    while True:
        cand = path.with_name(f"{path.stem}.prior{n}{path.suffix}")
        if not cand.exists():
            path.replace(cand)
            return
        n += 1


def one_job(fn, job: dict, tar: bytes, args, out_dir: Path, run: Path | None,
            gen: Path, review: Path, do_qc: bool, do_watch: bool,
            thinking: str, stage: bool) -> dict:
    """Render this project, then IMMEDIATELY check the file it produced.

    Everything after `MR.one` returns is this thread's own work, so a fast
    render's checks overlap a slow render still in flight — which is the entire
    point of this driver.
    """
    name = Path(job["project"]).name
    tag = f"{job['vid']}_{job['fmt']}"
    out = out_dir / f"{name}.mp4"
    t0 = time.time()
    log(tag, "render dispatched")
    rec: dict = {"job": {k: job[k] for k in ("project", "vid", "fmt") if k in job}}
    try:
        r = MR.one(fn, tar, name, args, out)
    except Exception as exc:                                         # noqa: BLE001
        rec |= {"render": {"pass": False, "error": f"{type(exc).__name__}: {exc}"},
                "pass": False, "wall_s": round(time.time() - t0, 1)}
        log(tag, f"RENDER FAILED  {exc}")
        return rec
    rec["render"] = {**r, "pass": True}
    log(tag, f"render landed  {r['probe']['width']}x{r['probe']['height']} "
             f"{r['probe']['frames']}f  wall {r['wall_seconds']}s  "
             f"${r['measured_cost_usd']}  -> checks start NOW")

    # ── THE COST LEDGER (2026-09-04) ────────────────────────────────────────
    # Booked the instant the file lands, out of `modal_render.price`'s own
    # arithmetic.  The ref carries the container's start epoch, so a fix
    # round's re-render is a SECOND row instead of overwriting the first —
    # which is exactly the money run 13's hand table lost ($0.22 reported
    # against $0.29 of renders actually paid for).
    epoch = r.get("t_import_epoch")
    if run:
        COSTS.safe_record(
            run, "modal", "render", float(r.get("measured_cost_usd") or 0.0),
            video=job.get("vid"), fmt=job.get("fmt") or None,
            units=(f"{r.get('billed_container_seconds')} container-s x "
                   f"{r.get('cores')} cores, {r['probe']['frames']}f "
                   f"{r['probe']['width']}x{r['probe']['height']}"),
            note=f"{job.get('quality', 'high')}-quality render of {name}",
            ref=COSTS.call_ref(run, out, epoch))

    # qc_pass and the watcher are independent of each other; both only need the
    # file that just landed.
    with cf.ThreadPoolExecutor(max_workers=2) as ex:
        futs = {}
        if do_qc:
            futs["qc_pass"] = ex.submit(
                run_qc, job, out, run, gen / f"_qcpass_{job['vid']}_{job['fmt']}.json", do_watch)
        if do_watch:
            futs["watch"] = ex.submit(
                run_watch, job, out,
                review / f"cands_{job['vid']}_{job['fmt']}.json", thinking)
        for k, f in futs.items():
            rec[k] = f.result()
            log(tag, f"{k} done  {rec[k]['wall_s']}s  "
                     f"{'PASS' if rec[k].get('pass') else 'FAIL'}")

    # THE WATCHER AND GATE 3 BOOK THEMSELVES.  `clerk_video_gemini` and
    # `qc_v3` (inside `qc_pass`) each know their own token bill and each write
    # their own `costs.jsonl` row, so the same Gemini call is booked once
    # whether this driver made it or a hand-run did.  This driver books only
    # the render, which is the only price it is the caller of.

    watch_ok = (not do_watch) or rec["watch"]["pass"] or bool(rec["watch"].get("unavailable"))
    ok = (rec["render"]["pass"]
          and (not do_qc or rec["qc_pass"]["pass"])
          and watch_ok)
    rec["pass"] = ok
    if do_watch and rec["watch"].get("unavailable"):
        rec["watch_unavailable"] = rec["watch"]["unavailable_because"]
        log(tag, "watcher UNAVAILABLE (Gemini spending cap) - staged on qc alone; the clerk decodes it")

    if stage and job.get("stage") and ok:
        dest = Path(job["stage"]).expanduser()
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(out, dest)
        rec["video_start_fix_s"] = zero_video_start(dest)
        rec["staged"] = str(dest)
        log(tag, f"staged -> {dest}")
    elif job.get("stage") and not ok:
        rec["staged"] = None
        rec["not_staged_because"] = "a check on this render did not pass"
    rec["wall_s"] = round(time.time() - t0, 1)
    return rec


def zero_video_start(path: Path) -> float:
    """A staged file's picture must start at t=0 (run 24, Prime Agent, 2026-09-22).

    Two renders came back with the video stream starting 21 ms after the audio;
    QuickTime shows a black first frame for that gap.  The frames are fine, only
    the container timestamp is late, so the fix is a stream-copy remux that shifts
    the video to zero (no re-encode; the audio then leads by < 1 frame).
    Returns the offset that was removed (0.0 when there was none)."""
    import subprocess, tempfile
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                            "stream=start_time", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        off = float(probe.stdout.strip() or 0)
    except ValueError:
        return 0.0
    if off <= 0.001:
        return 0.0
    tmp = Path(tempfile.mkstemp(suffix=".mp4", dir=path.parent)[1])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-itsoffset", f"-{off}", "-i", str(path), "-i", str(path),
                    "-map", "0:v", "-map", "1:a", "-c", "copy", "-movflags", "+faststart", str(tmp)], check=True)
    tmp.replace(path)
    return round(off, 6)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", required=True, help="jobs JSON, or - for stdin")
    ap.add_argument("--json", type=Path, default=None, help="write the report here")
    ap.add_argument("--function", default="render",
                    help="deployed Modal function: render (8 cores, default) | render_c32 | render_c16 | render_c8 | render_c4")
    ap.add_argument("--thinking", default="medium",
                    help="clerk_video_gemini --thinking; NEVER 'low'")
    ap.add_argument("--no-qc", dest="qc", action="store_false")
    ap.add_argument("--no-watch", dest="watch", action="store_false")
    ap.add_argument("--watch", dest="watch", action="store_true",
                    help="turn the Gemini watcher and Gate 3 back on (paused by default since 2026-09-22)")
    ap.set_defaults(watch=not GEMINI_PAUSED)
    ap.add_argument("--stage", action="store_true",
                    help="copy each render to its job's `stage` path once its "
                         "own checks have passed")
    a = ap.parse_args()

    spec = json.loads(sys.stdin.read() if a.spec == "-"
                      else Path(a.spec).read_text())
    jobs = spec["jobs"]
    run = Path(spec["run"]).resolve() if spec.get("run") else None
    out_dir = Path(spec.get("out_dir")
                   or (run / "output" if run else ".")).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    gen = Path(spec.get("gen") or (run / "gen" if run else out_dir)).resolve()
    review = Path(spec.get("review") or (run / "review" if run else out_dir)).resolve()
    gen.mkdir(parents=True, exist_ok=True)
    review.mkdir(parents=True, exist_ok=True)

    for j in jobs:
        p = Path(j["project"]).resolve()
        j["project"] = str(p)
        vid, fmt = infer(p)
        j.setdefault("vid", vid)
        j.setdefault("fmt", fmt)
        if run:
            j.setdefault("run", str(run))       # the watcher's transcript is THIS run's
        if run and not j.get("geom"):
            g = run / "gen" / f"_geom_{j['vid']}.json"
            if g.exists():
                j["geom"] = str(g)

    if run and (run / "production-policy.json").exists():
        sys.path.insert(0, str(F / "pipeline"))
        from production import check_phone
        for job in jobs:
            check_phone(run, job["vid"], job["fmt"], job["project"])
            if job.get("stage") and not Path(job["stage"]).resolve().is_relative_to((run / "staging").resolve()):
                raise ValueError("Production renders must stage inside the run; final delivery needs independent approval")

    # PACK FIRST, ALL OF THEM.  A broken asset reference is a packing error and
    # it must stop the batch before a single container starts, not after.
    packed = []
    for j in jobs:
        tar, members = MR.pack(Path(j["project"]))
        packed.append(tar)
        print(f"[pack] {Path(j['project']).name:<30} {len(tar) / 1e6:>6.2f} MB  "
              f"{len(members)} referenced file(s)")

    fn = MR.modal.Function.from_name(APP, a.function)

    t0 = time.time()
    results = []
    with cf.ThreadPoolExecutor(max_workers=len(jobs)) as ex:
        futs = [ex.submit(one_job, fn, j, tar, render_args(j, a.function),
                          out_dir, run, gen, review, a.qc, a.watch,
                          a.thinking, a.stage)
                for j, tar in zip(jobs, packed)]
        for f in cf.as_completed(futs):
            results.append(f.result())
    batch_wall = round(time.time() - t0, 1)

    recs = [r["render"] for r in results if r["render"].get("pass")]
    modal_cost = round(sum(r.get("measured_cost_usd", 0) for r in recs), 4)
    gem_cost = round(sum((r.get("watch") or {}).get("cost_usd") or 0
                         for r in results), 6)
    report = {
        "batch_wall_s": batch_wall,
        "renders": len(results),
        "passed": sum(1 for r in results if r["pass"]),
        "modal_cost_usd": modal_cost,
        "gemini_watcher_cost_usd": gem_cost,
        "total_cost_usd": round(modal_cost + gem_cost, 6),
        "serial_equivalent_s": round(sum(r["wall_s"] for r in results), 1),
        "results": results,
    }

    print("\n" + "=" * 78)
    print(f"{'render':<28} {'wall':>7} {'render':>8} {'qc':>7} {'watch':>7} "
          f"{'cands':>6}  verdict")
    print("-" * 78)
    for r in sorted(results, key=lambda x: x["job"].get("vid", "")):
        j = r["job"]
        q, w = r.get("qc_pass") or {}, r.get("watch") or {}
        print(f"{j.get('vid', '?') + '_' + j.get('fmt', '?'):<28} "
              f"{r['wall_s']:>6.1f}s "
              f"{(r['render'].get('render_seconds') or 0):>7.1f}s "
              f"{(q.get('wall_s') or 0):>6.1f}s "
              f"{(w.get('wall_s') or 0):>6.1f}s "
              f"{str((w.get('counts') or {}).get('candidates', '-')):>6}  "
              f"{'PASS' if r['pass'] else 'FAIL'}")
        for k in (q.get("failed") or []):
            print(f"    qc FAIL  {k}")
    print("-" * 78)
    print(f"batch wall {batch_wall}s against {report['serial_equivalent_s']}s of "
          f"the same work one render at a time")
    print(f"modal ${modal_cost}   gemini watcher ${gem_cost}   "
          f"total ${report['total_cost_usd']}")

    if a.json:
        a.json.parent.mkdir(parents=True, exist_ok=True)
        _archive_prior(a.json)
        a.json.write_text(json.dumps(report, indent=1, default=str))
        print(f"report -> {a.json}")

    # ── THE RUN'S COST, BY THE END OF THE VIDEO (Miguel, 2026-09-04) ────────
    # The ledger rows were written as each price was measured; this refreshes
    # `<run>/review/COSTS.md` and `costs.json` so the number exists the moment
    # the last file of this batch is staged, without anyone asking for it.  It
    # is a read of a text file and it can never change this driver's exit code.
    if run and a.stage:
        try:
            import cost_report as CR                             # noqa: E402
            rep = CR.build(Path(run))
            (Path(run) / "review").mkdir(parents=True, exist_ok=True)
            (Path(run) / "review" / "COSTS.md").write_text(CR.markdown(rep))
            (Path(run) / "review" / "costs.json").write_text(
                json.dumps(rep, indent=1))
            per = rep["usd_per_delivered_short"]
            print(f"[costs] {rep['run']} to date: ${rep['total_usd']:.4f} "
                  f"(modal ${rep['by_service'].get('modal', 0):.4f}, gemini "
                  f"${rep['by_service'].get('gemini', 0):.4f}, elevenlabs "
                  f"${rep['by_service'].get('elevenlabs', 0):.4f}) over "
                  f"{rep['staged_shorts']} staged file(s)"
                  + (f" = ${per:.3f} per short" if per else "")
                  + f"  -> {Path(run) / 'review' / 'COSTS.md'}", flush=True)
        except Exception as exc:                                 # noqa: BLE001
            print(f"[costs] report not written ({type(exc).__name__}: {exc})",
                  file=sys.stderr, flush=True)
    return 0 if report["passed"] == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
