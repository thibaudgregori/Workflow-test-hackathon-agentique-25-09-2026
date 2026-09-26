#!/usr/bin/env python3
"""DRAFT + WATCH — buy the sense verdict before the real render.

WHY (Miguel, 2026-09-03)
------------------------
`prerender_check.py` proves the page obeys the geometry laws and
`phone_test_page.py` proves each bespoke object is cut at phone scale.  Neither
can answer the question that actually rejects a short: *do the pictures argue
the sentences?*  Only the moving-clip watcher answers that, and until now it ran
on a finished portrait-4k render — which is exactly the artefact you did not
want to pay for.

So: a CHEAP render on Modal, the SAME watcher, before the real one.

WHAT "CHEAP" MEANS HERE, AND THE CONSTRAINT THAT SHAPES IT
----------------------------------------------------------
`hyperframes render --resolution` only takes PRESETS, and its own rule is that
"the scale must be an integer multiple" of the composition — so **there is no
540x960 preset to ask for**, on any composition this factory builds.

Nor is there a resolution to drop.  Since 2026-09-03 (HD delivery) every daily
page — split included — is authored 1080x1920 with no zoom, and there is nothing
below that.  (Runs 1-10 authored the split `data-width="2160"` with `zoom:2`; the
80.1 s figure below was measured on such a page.)

**The entire saving is `-q draft`, and it is large.**  The same
`sparkchrome_split`, 633 frames at 2160x3840: **80.1 s of render for $0.0061**
at draft, against the high-quality 1080x1920 cutout's 100.2 s for $0.0146 — 2.4x
cheaper on a frame four times the size.

The 540x960 artefact Miguel asked for is produced from that draft with one ffmpeg
scale (`--proxy`, on by default) and written beside it, so the draft can be
eyeballed at real phone size.  **The watcher is fed the NATIVE draft, not the
proxy**: `clerk_video_gemini` re-encodes whatever it is given to 720x1280, and
handing it a 540-wide file would make it upscale — a different input to the same
model is a different verdict, and the point of this stage is that its verdict
predicts the post-render one.

WHAT IT DOES NOT DO
-------------------
It does not adjudicate, and it does not gate on candidate count.  Gemini
produces CANDIDATES; a clerk rules on them.  What this stage buys is the chance
to see a candidate list while the page is still cheap to change.

    exit 0   the draft rendered and the watcher returned no BLOCKING candidate
    exit 2   blocking candidates — address them or waive each one IN WRITING
             before the real render (this is a stop, not a verdict)
    exit 1   the draft render or the watcher failed

CLI
---
    draft_watch.py <project> [--vid <id>] [--fmt split|cutout|whiteboard]
        --out-dir <scratch> [--json <report>] [--no-watch] [--keep]
        [--thinking medium] [--proxy/--no-proxy]
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

F = Path(__file__).resolve().parents[2]
PY = str(Path.home() / "Documents/Workspace/.venv/bin/python")

PROXY_W, PROXY_H = 540, 960


def infer(project: Path) -> tuple[str, str]:
    """(vid, fmt) from the factory's own `<id>_<fmt>` project naming."""
    name = project.name
    for f in ("whiteboard", "cutout", "facesplit", "artifactspine", "takeover",
              "split"):
        if name.endswith("_" + f):
            return name[: -len(f) - 1], f
    return name, ""


def draft_render(project: Path, out: Path, quality: str, function: str) -> dict:
    """One Modal render at the composition's NATIVE size, draft quality.

    `modal_render.py` is invoked as a subprocess with `--json` rather than
    imported, so the numbers in the report are the ones its own table prints —
    the wall clock, the billed container seconds and the measured cost.
    """
    rj = out.with_suffix(".render.json")
    cmd = [PY, str(F / "pipeline/render/modal_render.py"), str(project),
           "-o", str(out), "-q", quality, "--function", function,
           "--json", str(rj)]
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    wall = round(time.time() - t0, 1)
    rec = {"cmd": " ".join(cmd), "returncode": r.returncode,
           "wall_s": wall, "stdout": r.stdout[-3000:], "stderr": r.stderr[-2000:]}
    if rj.exists():
        try:
            got = json.loads(rj.read_text())
            if got:
                g = got[0]
                rec |= {"render_seconds": g.get("render_seconds"),
                        "modal_wall_seconds": g.get("wall_seconds"),
                        "cold_start_seconds": g.get("cold_start_seconds"),
                        "billed_container_seconds": g.get("billed_container_seconds"),
                        "cost_usd": g.get("measured_cost_usd"),
                        "upload_mb": round((g.get("upload_bytes") or 0) / 1e6, 2),
                        "probe": g.get("probe")}
        except Exception as exc:                                     # noqa: BLE001
            rec["json_error"] = str(exc)
    rec["pass"] = r.returncode == 0 and out.exists() and out.stat().st_size > 0
    return rec


def proxy(src: Path, dest: Path) -> dict:
    """The 540x960 artefact: one scale, no re-timing, audio copied."""
    t0 = time.time()
    r = subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(src),
         "-vf", f"scale={PROXY_W}:{PROXY_H}", "-c:v", "libx264", "-preset",
         "veryfast", "-crf", "26", "-c:a", "copy", str(dest)],
        capture_output=True, text=True)
    return {"path": str(dest), "size": f"{PROXY_W}x{PROXY_H}",
            "returncode": r.returncode, "wall_s": round(time.time() - t0, 1),
            "bytes": dest.stat().st_size if dest.exists() else 0,
            "stderr": r.stderr[-800:],
            "note": "eyeball artefact only — the watcher is fed the NATIVE draft"}


def watch(render: Path, vid: str, fmt: str, out_json: Path,
          thinking: str) -> dict:
    cmd = [PY, str(F / "pipeline/clerk_video_gemini.py"), str(render), vid,
           "--out", str(out_json), "--thinking", thinking]
    if fmt:
        cmd += ["--fmt", fmt]
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    rec = {"cmd": " ".join(cmd), "returncode": r.returncode,
           "wall_s": round(time.time() - t0, 1), "out": str(out_json),
           "stderr": r.stderr[-2000:]}
    if out_json.exists():
        got = json.loads(out_json.read_text())
        cands = got.get("candidates") or []
        rec |= {"model": got.get("model"), "cost_usd": got.get("cost_usd"),
                "watcher_wall_s": got.get("wall_clock_s"),
                "counts": got.get("counts"),
                "video_summary": (got.get("video_summary") or "")[:600],
                "candidates": [{k: c.get(k) for k in
                                ("t_start", "t_end", "klass", "severity",
                                 "motion_or_held", "claim")} for c in cands]}
    rec["pass"] = r.returncode == 0
    return rec


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("--vid", default=None)
    ap.add_argument("--fmt", default=None)
    ap.add_argument("--out-dir", type=Path, required=True,
                    help="scratch directory for the draft, the proxy and the "
                         "candidate list")
    ap.add_argument("-q", "--quality", default="draft",
                    choices=["draft", "standard", "high"])
    ap.add_argument("--function", default="render_c4",
                    help="deployed Modal function. The draft lane defaults to "
                         "the 4-core box: a draft is not worth 8 cores.")
    ap.add_argument("--thinking", default="medium",
                    help="clerk_video_gemini --thinking. NEVER 'low' — at low "
                         "the same call returns zero candidates.")
    ap.add_argument("--no-watch", dest="watch", action="store_false",
                    help="render the draft only (measurement mode)")
    ap.add_argument("--no-proxy", dest="proxy", action="store_false")
    ap.add_argument("--keep", action="store_true",
                    help="keep the draft MP4 (default: keep; --no-keep deletes)")
    ap.add_argument("--no-keep", dest="keep", action="store_false")
    ap.set_defaults(keep=True)
    ap.add_argument("--json", type=Path, default=None)
    a = ap.parse_args()

    project = a.project.resolve()
    if not (project / "index.html").exists():
        print(f"no index.html in {project}", file=sys.stderr)
        return 2
    vid, fmt = infer(project)
    vid, fmt = a.vid or vid, (a.fmt or fmt)
    out_dir = a.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    draft = out_dir / f"{project.name}_draft.mp4"

    t0 = time.time()
    rec: dict = {"project": str(project), "vid": vid, "fmt": fmt,
                 "lane": f"Modal {a.function}, -q {a.quality}, the "
                         f"composition's NATIVE size (no --resolution: there is "
                         f"no 540x960 preset, and the split is already authored "
                         f"2160x3840 so portrait-4k on it is a 1x no-op). The "
                         f"whole saving is -q draft."}

    rec["draft_render"] = draft_render(project, draft, a.quality, a.function)
    if not rec["draft_render"]["pass"]:
        print(json.dumps(rec, indent=1))
        print("\nDRAFT RENDER FAILED — see stderr above", file=sys.stderr)
        return 1

    if a.proxy:
        rec["proxy_540x960"] = proxy(draft, out_dir / f"{project.name}_540x960.mp4")

    if a.watch:
        rec["watch"] = watch(draft, vid, fmt,
                             out_dir / f"cands_draft_{vid}_{fmt}.json", a.thinking)
    else:
        rec["watch"] = {"skipped": "--no-watch"}

    rec["total_wall_s"] = round(time.time() - t0, 1)
    r, w = rec["draft_render"], rec.get("watch") or {}
    rec["total_cost_usd"] = round((r.get("cost_usd") or 0)
                                  + (w.get("cost_usd") or 0), 6)
    blocking = (w.get("counts") or {}).get("blocking", 0)
    rec["blocking_candidates"] = blocking
    rec["verdict"] = ("RENDER-READY" if not blocking else
                      "HOLD — address or waive each blocking candidate IN WRITING")

    print(f"\nDRAFT + WATCH  {project.name}")
    print("-" * 74)
    p = r.get("probe") or {}
    print(f"  draft render   {p.get('width')}x{p.get('height')} "
          f"{p.get('frames')}f  render {r.get('render_seconds')}s  "
          f"wall {r['wall_s']}s  ${r.get('cost_usd')}")
    if a.proxy:
        print(f"  540x960 proxy  {rec['proxy_540x960']['bytes'] / 1e6:.1f} MB  "
              f"{rec['proxy_540x960']['wall_s']}s")
    if a.watch:
        print(f"  watcher        {w.get('model')}  {w.get('counts')}  "
              f"wall {w['wall_s']}s  ${w.get('cost_usd')}")
        for c in (w.get("candidates") or []):
            print(f"      {c['severity']:<9} {c['t_start']}-{c['t_end']:<6} "
                  f"{c['klass']:<26} {str(c['claim'])[:70]}")
    print("-" * 74)
    print(f"  {rec['verdict']}   total {rec['total_wall_s']}s   "
          f"${rec['total_cost_usd']}")

    if not a.keep and draft.exists():
        draft.unlink()
    if a.json:
        a.json.parent.mkdir(parents=True, exist_ok=True)
        a.json.write_text(json.dumps(rec, indent=1, default=str))
        print(f"  report -> {a.json}")
    return 2 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
