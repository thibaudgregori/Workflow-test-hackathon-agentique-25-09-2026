#!/usr/bin/env python3
"""MASTER-SPACE SILHOUETTE SWEEP — the generic form of run 9's
`sweep_master_birefnet_<id>.py`, both edges, any session.

WHY IT EXISTS.  A tracked SAM2 alpha lives in PLATE space.  When the plate's own
border cuts him, the alpha is flush against its border THERE, so it cannot say
how much more of him is outside the crop — the measurement that a wider window
has to be chosen against does not exist in plate space at all.  This produces it
in MASTER pixels, with the same BiRefNet-general silhouette `prompt0.py birefnet`
already trusts for the frame-0 prompt.  Same model, same `keep_largest` clean-up,
pointed at the master instead of the plate.

It is a CHOOSING instrument, not a shipping one.  The window it justifies is
proved afterwards on the newly tracked SAM2 alpha, every frame, by
`pipeline/edge_clip_check.py` inside `ship.py`.

RESOLUTION.  BiRefNet resamples whatever it is handed to 1024x1024 internally, so
the master is fed at 1280x720 and the answer is scaled back by 3 (3840/1280).
Three master px is ~1.5 plate px at a typical k — an order of magnitude finer
than the 24-canvas-px margin that is being designed against.

WHERE IT RUNS — MODAL BY DEFAULT SINCE 2026-09-03
-------------------------------------------------
The sweep is one independent BiRefNet forward pass per sampled frame, and on the
laptop's `CPUExecutionProvider` it cost **1787 s for 106 frames** on the
2026-09-02 prep test — 96 % of the whole prep plate stage.  The same ONNX graph
now runs on a Modal A10G through `shorts-factory-birefnet`, and because the
sweep only ever needs EXTENTS and resamples to 1280x720 before looking at
anything, the caller ships a 1280x720 PROXY instead of a 100-190 MB master.

    default    build the proxy, call `shorts-factory-birefnet::sweep`
    --full     send the master itself, same function, same in-container filter
    --local    the old CPU path, in the bake-off venv (the fallback)

The JSON is byte-comparable either way: the Modal record carries an extra `lane`
block and nothing else moves.  Measured parity and cost live in
`pipeline/prep/README.md`.

THE LOCAL PATH RUNS IN THE BAKE-OFF VENV, not the workspace venv:

    F/pipeline/prep/.venv-birefnet/bin/python \
        pipeline/prep/birefnet_master_sweep.py --local --src <master.mp4> \
        --out <sweep.json> --stride 6

The MODAL path runs in the workspace venv (it needs `modal`, not `rembg`).
`platelib.py` picks the interpreter to match; nothing imports this file.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

W, H = 1280, 720
MASTER_W = 3840
APP, FN = "shorts-factory-birefnet", "sweep"


# =============================================================================
# the proxy
# =============================================================================
def build_proxy(src: Path, dst: Path, crf: int = 12) -> Path:
    """The 1280x720 proxy the GPU lane is fed.

    `scale=1280:720:flags=area` is the SAME filter the sweep itself applies to
    whatever it is handed, so the only thing between a proxy and the master is
    one x264 generation at crf 12 — measured at 0 delta on the prep-test master
    (see `pipeline/prep/README.md`).  It costs ~1.4 s and takes the upload from
    84 MB to 17 MB.
    """
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(src), "-vf",
         f"scale={W}:{H}:flags=area", "-an", "-c:v", "libx264",
         "-preset", "veryfast", "-crf", str(crf), "-pix_fmt", "yuv420p",
         str(dst), "-y"], check=True)
    return dst


# =============================================================================
# the modal lane
# =============================================================================
def sweep_modal(src: Path, *, stride: int = 6, dense: str = "",
                fps: float = 25.0, full: bool = False,
                session: str = "run") -> dict:
    """Hand the proxy (or the master) to `shorts-factory-birefnet::sweep`."""
    import modal                                              # noqa: PLC0415
    fn = modal.Function.from_name(APP, FN)

    t0 = time.time()
    with tempfile.TemporaryDirectory() as tmp:
        payload = (src if full
                   else build_proxy(src, Path(tmp) / "proxy.mp4"))
        t_proxy = time.time()
        blob = payload.read_bytes()
        rec = fn.remote(video=blob, stride=stride, dense=dense, fps=fps,
                        src=str(src), session=session)

    lane = rec.setdefault("lane", {})
    lane["proxy"] = not full
    lane["proxy_seconds"] = round(t_proxy - t0, 1)
    lane["client_wall_seconds"] = round(time.time() - t0, 1)
    lane["uploaded_bytes"] = len(blob)

    # the cost arithmetic lives with the app, so both shorts-factory GPU lanes
    # price with one set of constants
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from birefnet_modal_app import cost                        # noqa: PLC0415
    cost(rec, t0)
    rec["wall_seconds"] = lane["client_wall_seconds"]
    return rec


# =============================================================================
# the local lane (the fallback)
# =============================================================================
def keep_largest(m: np.ndarray) -> np.ndarray:
    import cv2                                                # noqa: PLC0415
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    if n <= 1:
        return m
    return lab == (1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])))


def decode(src: Path, w: int, h: int):
    p = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(src), "-vf",
         f"scale={w}:{h}:flags=area", "-pix_fmt", "rgb24", "-f", "rawvideo",
         "-"], stdout=subprocess.PIPE, bufsize=w * h * 3 * 4)
    n = w * h * 3
    try:
        while True:
            b = p.stdout.read(n)
            if len(b) < n:
                return
            yield np.frombuffer(b, np.uint8).reshape(h, w, 3)
    finally:
        p.stdout.close()
        p.wait()


def probe_frames(src: Path) -> int:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
         "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(src)],
        capture_output=True, text=True, check=True).stdout.strip()
    return int(out)


def sweep_local(src: Path, *, stride: int = 6, dense: str = "",
                fps: float = 25.0) -> dict:
    """BiRefNet on this machine's CPU.  Minutes per video; the fallback only."""
    from PIL import Image                                      # noqa: PLC0415
    from rembg import new_session, remove                      # noqa: PLC0415
    sess = new_session("birefnet-general", providers=["CPUExecutionProvider"])

    frames = probe_frames(src)
    scale = MASTER_W // W
    want = set(range(0, frames, stride))
    dense_windows = []
    for chunk in [c for c in dense.split(",") if c.strip()]:
        lo, hi = (int(x) for x in chunk.split("-"))
        dense_windows.append([lo, hi])
        want |= set(range(lo, hi))
    want.add(frames - 1)

    cols = np.arange(W)[None, :]
    left: dict[int, list[int]] = {}
    right: dict[int, list[int]] = {}
    t0 = time.time()
    done = 0
    for i, rgb in enumerate(decode(src, W, H)):
        if i not in want:
            continue
        al = np.asarray(remove(Image.fromarray(rgb), session=sess,
                               post_process_mask=False))[..., 3]
        m = keep_largest(al > 127)
        lm = np.where(m, cols, W).min(axis=1)
        rm = np.where(m, cols, -1).max(axis=1)
        left[i] = [int(v) for v in lm]
        right[i] = [int(v) for v in rm]
        done += 1
        if done % 25 == 0:
            el = time.time() - t0
            print(f"  {done}/{len(want)}  {el:.0f}s  "
                  f"eta {el / done * (len(want) - done):.0f}s", flush=True)

    return dict(
        src=str(src), sweep_scale=[W, H], master_px_per_sweep_px=scale,
        stride=stride, dense_windows=dense_windows, frames_measured=len(left),
        model="birefnet-general", fps=fps, frames_total=frames,
        wall_seconds=round(time.time() - t0, 1),
        # extreme MASTER x per MASTER row, per measured frame.  -1 = empty row.
        leftmost_master_by_frame={
            str(k): [(v * scale if v < W else -1) for v in lm]
            for k, lm in sorted(left.items())},
        rightmost_master_by_frame={
            str(k): [(v * scale if v >= 0 else -1) for v in rm]
            for k, rm in sorted(right.items())},
        lane=dict(where="local", providers=["CPUExecutionProvider"]),
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--src", required=True, type=Path, help="the cut master")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--stride", type=int, default=6)
    ap.add_argument("--dense", default="",
                    help="extra frame ranges swept at EVERY frame: 'a-b,c-d'")
    ap.add_argument("--fps", type=float, default=25.0)
    ap.add_argument("--local", action="store_true",
                    help="the CPU fallback, in the bake-off venv")
    ap.add_argument("--full", action="store_true",
                    help="modal lane: send the master, not the 720p proxy")
    ap.add_argument("--session", default="run", help="modal volume folder")
    a = ap.parse_args()

    # THE CACHE, unchanged: a sweep already on disk is never paid for twice,
    # whichever lane produced it.  `platelib.py` checks this too; keeping it
    # here means a hand-run of this script is idempotent as well.
    if a.out.exists():
        rec = json.loads(a.out.read_text())
        print(f"cached {a.out}: {rec['frames_measured']} frames "
              f"({rec.get('lane', {}).get('where', 'local')})", flush=True)
        return 0

    if a.local:
        rec = sweep_local(a.src, stride=a.stride, dense=a.dense, fps=a.fps)
    else:
        rec = sweep_modal(a.src, stride=a.stride, dense=a.dense, fps=a.fps,
                          full=a.full, session=a.session)

    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(rec))
    lane = rec.get("lane", {})
    where = lane.get("where", "local")
    if lane.get("gpu"):
        where += " " + lane["gpu"]
    print(f"wrote {a.out}: {rec['frames_measured']} frames in "
          f"{rec['wall_seconds']}s on {where}", flush=True)
    if lane.get("measured_cost_usd") is not None:
        print(f"  cost ${lane['measured_cost_usd']}  "
              f"(billed {lane['billed_container_seconds']}s, cold start "
              f"{lane['cold_start_seconds']}s)", flush=True)
        # THE COST LEDGER (2026-09-04).  The sweep's money lives inside the
        # plate stage, which is exactly why every run-11 total had to be
        # re-added by hand.  A HAND-RUN sweep books itself here; inside
        # prep_batch the package books it, with the same ref and the same vid,
        # so the two can only replace each other and never double.
        _run = os.environ.get("SHORTS_RUN")
        if _run:
            import sys as _sys
            _sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
            import costs as COSTS                                # noqa: E402
            _vid = (os.environ.get("SHORTS_VID")
                    or a.out.stem.replace("_birefnet_master_", "")
                    .replace("birefnet_master_", "") or None)
            COSTS.safe_record(
                _run, "modal", "sweep",
                float(lane["measured_cost_usd"]), video=_vid,
                units=(f"{lane.get('billed_container_seconds')} container-s "
                       f"{lane.get('gpu') or ''}").strip(),
                note="BiRefNet master sweep (the plate solve)",
                ref=COSTS.call_ref(_run, a.out, lane.get("container")
                                   or lane.get("t_import_epoch")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
