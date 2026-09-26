#!/usr/bin/env python
"""bolsterfix.py — THE MANUAL HEAL, for furniture the deployed heal under-cut.

The README has named this file since the leak check shipped; this is it, written
out on the day it was first needed (kimiram, run 9, 2026-09-02).

WHAT IT IS FOR.  `track`'s own heal is automatic and it is the normal path.  It
derives its window from `frozen ∪ accepted companion`, and on `kimiram` that
window came out 28 px wide against a 74 px chair-headrest tab, because the
companion's `sd_ratio <= 0.75` test rejected the tab at 0.80.  See
`protrusion.py` for the full autopsy.  This script re-runs the SAME correction
— identical `heal_frame`, identical guard rails — with the window supplied by
`protrusion.scan()` (or by hand), writes the corrective keyframes as prompt
masks, and hands them back to the deployed `track` for one re-propagation.

Nothing about the arithmetic is new and nothing here is a workaround: the fix is
the same quadratic shoulder line, the same luma <= 70 guard, the same bracket,
the same depth cap, the same front-loaded keyframe cadence.  Only the WINDOW is
different, and the window is the thing that was wrong.

    # 1. derive the corrective keyframes
    $V bolsterfix.py --session sessions/kimiram \
                     --alpha   sessions/kimiram/alpha_v1.mkv \
                     --plate   sessions/kimiram/plate_wide_25.mp4 \
                     --out     sessions/kimiram/prompts_v2

    # 2. re-propagate them on the deployed app (~$0.17, ~7 min)
    $V track.py --session sessions/kimiram \
                --plate   sessions/kimiram/plate_wide_25.mp4 \
                --prompts sessions/kimiram/prompts_v2 --tag v2

    # 3. ship, then re-scan
    $V ship.py --alpha sessions/kimiram/alpha_v2.mkv ...
    $V protrusion.py --alpha sessions/kimiram/alpha_v2.mkv \
                     --plate sessions/kimiram/plate_wide_25.mp4     # must be clean

GUARD RAILS — every one of `track`'s, unchanged, because they are `heal_frame`'s
and this calls `heal_frame`: subtractive only, luma guard 70, the anchor-edge
bracket, the 2.5x depth cap, exactly one iteration.  The only judgement this
script adds is which columns to point it at, and that judgement is measured.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def read_indices(path: Path, w: int, h: int, wants: set[int]) -> dict:
    """Decode only the frames we need, as (h, w) uint8."""
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path),
                        "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                       capture_output=True)
    n = len(r.stdout) // (w * h)
    a = np.frombuffer(r.stdout, np.uint8)[:n * w * h].reshape(n, h, w)
    return {g: a[g] for g in sorted(wants) if g < n}, n


def main() -> None:
    import cv2

    ap = argparse.ArgumentParser()
    ap.add_argument("--session", required=True)
    ap.add_argument("--alpha", required=True, help="the alpha that still leaks")
    ap.add_argument("--plate", required=True, help="plate_wide_25.mp4 (luma)")
    ap.add_argument("--out", required=True, help="prompt dir to write")
    ap.add_argument("--frame0", default=None,
                    help="frame-0 prompt to heal; default <session>/prompts/"
                         "kf_00000.png is IGNORED and frame 0 is healed from "
                         "the alpha, exactly as track's own heal does")
    ap.add_argument("--window", default=None,
                    help="force a window, 'x0:x1[,x0:x1]'; default = "
                         "protrusion.scan()'s accepted windows")
    ap.add_argument("--chunk", type=int, default=350)
    ap.add_argument("--stride", type=int, default=5, help="scan sampling")
    a = ap.parse_args()

    ma = _load("modal_app")
    prot = _load("protrusion")

    alpha_p, plate_p = Path(a.alpha), Path(a.plate)
    W, H = prot.probe_wh(alpha_p)
    if prot.probe_wh(plate_p) != (W, H):
        raise SystemExit("plate and alpha differ in size")

    # ── 1. the window ────────────────────────────────────────────────────────
    A = prot.read_gray(alpha_p, W, H, a.stride)
    P = prot.read_gray(plate_p, W, H, a.stride * 8)
    scan = prot.scan(A, P)
    if a.window:
        wins = [tuple(int(v) for v in t.split(":")) for t in a.window.split(",")]
        src = "forced"
    else:
        wins = [(w["x0"], w["x1"]) for w in scan["windows"]]
        src = "protrusion.scan"
    if not wins:
        raise SystemExit("no protrusion window: nothing to heal")
    print(f"WINDOWS ({src}): {wins}")

    # ── 2. the plan, through the deployed app's own planner ──────────────────
    # `sweep` gives the arrays and segments; the frozen list is REPLACED by the
    # protrusion windows and the companion is disabled, so `heal_windows`
    # returns exactly the columns measured above and nothing else.
    tops = np.stack([ma.top_columns(f) for f in A])
    sw = ma.sweep(tops)
    sw["frozen"] = [dict(x0=int(x0), x1=int(x1)) for x0, x1 in wins]
    cfg = dict(ma.LEAK, sd_ratio_max=-1.0)          # companion accepts nothing

    n_all = int(round(float(subprocess.run(
        ["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
         "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0",
         str(alpha_p)], capture_output=True, text=True).stdout.strip())))
    kf = ma.heal_keyframes(n_all, a.chunk, cfg)
    print(f"{n_all} frames, {len(kf)} corrective keyframes")

    probe = sorted({int(round(i * (n_all - 1) / max(cfg["dark_probe"] - 1, 1)))
                    for i in range(cfg["dark_probe"])})
    A_need, _ = read_indices(alpha_p, W, H, set(kf) | set(probe))
    L_need, _ = read_indices(plate_p, W, H, set(kf) | set(probe))

    plan, comp = ma.plan_windows(sw, [L_need[g] for g in probe if g in L_need],
                                 [A_need[g] for g in probe if g in A_need],
                                 H, cfg)
    if not plan:
        raise SystemExit("no anchor columns: needs_human")
    for p in plan:
        print(f"  gap {p['gap']}  anchors {len(p['anchors'])} "
              f"{p['anchor_sides']}  lift_max {p['lift_max']}  rows {p['rows']}")

    # ── 3. the corrective keyframes ──────────────────────────────────────────
    out = Path(a.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    reps, cuts = {}, []
    for g in kf:
        m0 = A_need.get(g)
        if m0 is None:
            continue
        m, rep = ma.heal_frame(m0 > 127, L_need[g], plan, cfg)
        cv2.imwrite(str(out / f"kf_{g:05d}.png"), (m * 255).astype(np.uint8))
        reps[str(g)] = rep
        cuts.append(rep["cut_px"])
    lmax = max((v["luma_of_cut"]["max"] for v in reps.values()), default=-1)
    print(f"CUT n={len(cuts)} min={min(cuts)} max={max(cuts)} "
          f"median={int(np.median(cuts))}  |  max luma of any removed pixel "
          f"{lmax} (guard {cfg['luma_guard']})")
    if np.median(cuts) < cfg["min_cut_px"]:
        raise SystemExit("the heal had nothing removable to cut")
    if lmax > cfg["luma_guard"]:
        raise SystemExit("LUMA GUARD BREACHED — refusing to write this heal")

    report = dict(session=str(a.session), alpha=str(alpha_p),
                  window_source=src, windows=[list(w) for w in wins],
                  protrusion=({k: v for k, v in scan.items()
                               if k not in ("segments",)}),
                  plan=[dict(gap=p["gap"], anchor_cols=len(p["anchors"]),
                             anchor_sides=p["anchor_sides"],
                             lift_max=p["lift_max"], rows=p["rows"])
                        for p in plan],
                  keyframes=kf, cut_px=dict(
                      n=len(cuts), min=int(min(cuts)), max=int(max(cuts)),
                      median=int(np.median(cuts))),
                  luma_of_cut_max=int(lmax), heal_report=reps)
    (out / "bolsterfix.json").write_text(json.dumps(report, indent=1))
    print(f"\n{len(cuts)} prompt masks -> {out}")
    print("next: track.py --prompts", out, "--tag v2")


if __name__ == "__main__":
    main()
