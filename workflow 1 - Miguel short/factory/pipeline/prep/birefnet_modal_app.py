"""shorts-factory-birefnet — the master-sweep GPU lane.

WHAT THIS IS.  `birefnet_master_sweep.py` measures, in MASTER pixels, how far
the silhouette ever reaches left and right, so `platelib.py` can build the plate
over-wide from the start instead of discovering the amputation after a whole
SAM2 track.  It is a CHOOSING instrument and it is embarrassingly parallel — one
independent BiRefNet forward pass per sampled frame — but on the laptop it runs
on `CPUExecutionProvider` and took **1787 s for 106 frames** on the 2026-09-02
prep test: 96 % of the whole prep plate stage, for a measurement that decides
two integers per side.

So the same ONNX graph runs here on a GPU instead.

PARITY IS THE WHOLE POINT, so nothing about the arithmetic is re-imagined:

  * the SAME weights.  `BiRefNet-general-epoch_244.onnx`, the exact file
    `rembg`'s `birefnet-general` session downloads (md5 7a35a014...), curled into
    an image layer rather than mounted from a volume, so a cold container never
    waits on a mount to have weights.
  * the SAME preprocessing.  `rembg.sessions.base.BaseSession.normalize`
    reproduced line for line: PIL LANCZOS to 1024x1024, divide by the image's own
    max, ImageNet mean/std, CHW, float32.
  * the SAME postprocessing.  `BiRefNetSessionGeneral.predict`: sigmoid, min-max
    renormalise over the whole map, uint8, PIL LANCZOS back to the sweep's
    1280x720, which is exactly the alpha channel `rembg.remove(...,
    post_process_mask=False)` hands back.
  * the SAME clean-up.  `keep_largest` on `alpha > 127`, then per-row leftmost
    and rightmost columns scaled by 3840/1280.

`rembg` itself is NOT installed: importing it drags in pymatting, numba,
scikit-image and scipy for code paths this sweep never touches.  The twenty
lines it actually uses are reproduced above and were proved byte-identical to
`rembg`'s own output on the laptop before this app was written (max abs alpha
difference 0 over the sampled frames).

THE PROXY.  The sweep only ever needs EXTENTS, and it resamples the master to
1280x720 before looking at anything, so the caller sends a 1280x720 proxy rather
than a 100-190 MB master.  The in-container decode still runs
`scale=1280:720:flags=area` unconditionally, so a full master handed to the same
function takes the identical path.  `--full` on the driver sends the master
instead, and the parity note in `pipeline/prep/README.md` carries the measured
proxy-vs-master delta.

TWO GPUs, DELIBERATELY.  `sweep` runs on A10G and `sweep_t4` on T4, same body,
so the cheaper-per-sweep of the two is a measurement and not an opinion.  See
the README: A10G wins on BOTH axes at this batch size, so `sweep` is the one
`birefnet_master_sweep.py` calls.

Calling it, from anywhere:

    import modal
    fn = modal.Function.from_name("shorts-factory-birefnet", "sweep")
    rec = fn.remote(video=proxy_bytes, stride=6)

`birefnet_master_sweep.py` is that call with the proxy build, the cost
arithmetic and the file handling already written.
"""
from __future__ import annotations

import json
import subprocess
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import modal

# The exact asset rembg's birefnet-general session fetches (md5
# 7a35a0141cbbc80de11d9c9a28f52697).  Baked as an image layer, not a volume
# file: weights are immutable build inputs, and the volume stays disposable.
ONNX_URL = ("https://github.com/danielgatis/rembg/releases/download/v0.0.0/"
            "BiRefNet-general-epoch_244.onnx")
ONNX = "/root/models/birefnet-general.onnx"

# onnxruntime-gpu needs a CUDA + cuDNN userland, and pinning a `nvidia/cuda`
# base image to match the wheel is a guessing game — 12.6.2-cudnn loaded the
# wheel's CPU provider only and `get_providers()` came back
# `['CPUExecutionProvider']`.  The `[cuda,cudnn]` extras pull the exact nvidia
# wheels this ORT build was compiled against and ORT's own `preload_dlls()`
# finds them, so the CUDA version is the wheel's problem instead of ours.
image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("ffmpeg", "curl", "libgl1", "libglib2.0-0")
    .pip_install("onnxruntime-gpu[cuda,cudnn]==1.29.0", "numpy==2.5.2",
                 "pillow==12.3.0", "opencv-python-headless==5.0.0.93")
    .run_commands(
        "mkdir -p /root/models && "
        f"curl -sSL -o {ONNX} {ONNX_URL}",
        "python -c \"import hashlib,sys;h=hashlib.md5(open('%s','rb').read())"
        ".hexdigest();sys.exit(0 if h=='7a35a0141cbbc80de11d9c9a28f52697' "
        "else 'BiRefNet weights md5 mismatch: '+h)\"" % ONNX,
    )
)

app = modal.App("shorts-factory-birefnet")

# Run artifacts only.  Every sweep leaves its own record behind, so a dropped
# return never means paying for the GPU twice.
vol = modal.Volume.from_name("shorts-factory-birefnet", create_if_missing=True)

T_IMPORT = time.time()
CONTAINER_ID = str(uuid.uuid4())

W, H = 1280, 720                 # the sweep's own resolution, unchanged
MASTER_W = 3840
MEAN = (0.485, 0.456, 0.406)     # rembg's ImageNet constants, unchanged
STD = (0.229, 0.224, 0.225)

CPU_CORES, MEM_GIB = 8.0, 16.0
# Modal's published on-demand rates, the same constants `pipeline/sam2` prices
# with, so the two apps' reported costs are directly comparable.
GPU_USD_S = {"A10G": 0.000306, "T4": 0.000164}
CPU_USD_S_CORE, MEM_USD_S_GIB = 0.0000131, 0.00000222


# =============================================================================
# the arithmetic, reproduced from rembg 2.0.81
# =============================================================================
def _preprocess(rgb):
    """`BaseSession.normalize(img, ImageNet mean/std, (1024, 1024))`."""
    import numpy as np
    from PIL import Image
    im = Image.fromarray(rgb).convert("RGB").resize(
        (1024, 1024), Image.Resampling.LANCZOS)
    ary = np.array(im)
    ary = ary / max(np.max(ary), 1e-6)
    tmp = np.zeros((1024, 1024, 3))
    for c in range(3):
        tmp[:, :, c] = (ary[:, :, c] - MEAN[c]) / STD[c]
    return np.expand_dims(tmp.transpose((2, 0, 1)), 0).astype(np.float32)


def _postprocess(out):
    """`BiRefNetSessionGeneral.predict`'s tail: sigmoid, min-max, back to WxH."""
    import numpy as np
    from PIL import Image
    pred = 1.0 / (1.0 + np.exp(-out[:, 0, :, :]))
    mi, ma = np.min(pred), np.max(pred)
    pred = np.squeeze((pred - mi) / (ma - mi))
    mask = Image.fromarray((pred * 255).astype("uint8"), mode="L")
    return np.array(mask.resize((W, H), Image.Resampling.LANCZOS))


def _keep_largest(m):
    import cv2
    import numpy as np
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    if n <= 1:
        return m
    return lab == (1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])))


def _probe_frames(src: Path) -> int:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
         "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(src)],
        capture_output=True, text=True, check=True).stdout.strip()
    return int(out)


def _decode(src: Path):
    """Identical filter to the local sweep, so a proxy and a master agree."""
    import numpy as np
    p = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(src), "-vf",
         f"scale={W}:{H}:flags=area", "-pix_fmt", "rgb24", "-f", "rawvideo",
         "-"], stdout=subprocess.PIPE, bufsize=W * H * 3 * 4)
    n = W * H * 3
    try:
        while True:
            b = p.stdout.read(n)
            if len(b) < n:
                return
            yield np.frombuffer(b, np.uint8).reshape(H, W, 3)
    finally:
        p.stdout.close()
        p.wait()


# =============================================================================
# the sweep
# =============================================================================
def _sweep(video: bytes, stride: int, dense: str, fps: float, src: str,
           session: str, gpu: str) -> dict:
    import numpy as np
    import onnxruntime as ort

    t_fn = time.time()
    work = Path("/root/run")
    work.mkdir(parents=True, exist_ok=True)
    clip = work / "in.mp4"
    clip.write_bytes(video)

    t_load = time.time()
    # onnxruntime-gpu ships the CUDA EP as a shared library that dlopens the
    # nvidia wheels' .so files.  Nothing puts those on the loader path, so
    # WITHOUT this call the session builds happily and silently reports
    # `['CPUExecutionProvider']` — no exception, no warning, a 30x slower run
    # that still returns correct numbers.  It is the whole GPU lane in one line.
    ort.preload_dlls()
    so = ort.SessionOptions()
    sess = ort.InferenceSession(
        ONNX, sess_options=so,
        providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
    in_name = sess.get_inputs()[0].name
    providers = sess.get_providers()
    if "CUDAExecutionProvider" not in providers:
        raise RuntimeError(
            f"CUDA EP unavailable; session has {providers}, build offers "
            f"{ort.get_available_providers()}.  Run `diag` for the loader's "
            "own account of why.")
    t_ready = time.time()

    frames = _probe_frames(clip)
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

    # The ONNX graph's batch dim is FIXED at 1 (input_image [1, 3, 1024, 1024]),
    # so the batch here is the whole frame list in one GPU-resident call rather
    # than a batched tensor: the CPU preprocessing of the next frames overlaps
    # the current forward pass, which is what actually keeps the A10 fed.
    t_gpu0 = time.time()
    pool = ThreadPoolExecutor(max_workers=4)
    pending: dict[int, object] = {}
    order: list[int] = []
    PREFETCH = 6

    def drain(i):
        out = sess.run(None, {in_name: pending.pop(i).result()})[0]
        al = _postprocess(out)
        m = _keep_largest(al > 127)
        lm = np.where(m, cols, W).min(axis=1)
        rm = np.where(m, cols, -1).max(axis=1)
        left[i] = [int(v) for v in lm]
        right[i] = [int(v) for v in rm]

    for i, rgb in enumerate(_decode(clip)):
        if i not in want:
            continue
        pending[i] = pool.submit(_preprocess, rgb.copy())
        order.append(i)
        while len(order) > PREFETCH:
            drain(order.pop(0))
    while order:
        drain(order.pop(0))
    pool.shutdown()
    t_gpu1 = time.time()

    rec = dict(
        src=src or str(clip), sweep_scale=[W, H], master_px_per_sweep_px=scale,
        stride=stride, dense_windows=dense_windows, frames_measured=len(left),
        model="birefnet-general", fps=fps, frames_total=frames,
        wall_seconds=round(time.time() - t_fn, 1),
        leftmost_master_by_frame={
            str(k): [(v * scale if v < W else -1) for v in lm]
            for k, lm in sorted(left.items())},
        rightmost_master_by_frame={
            str(k): [(v * scale if v >= 0 else -1) for v in rm]
            for k, rm in sorted(right.items())},
        lane=dict(
            where="modal", app="shorts-factory-birefnet", gpu=gpu,
            container=CONTAINER_ID, onnx=Path(ONNX).name,
            providers=providers,
            input_bytes=len(video),
            model_load_seconds=round(t_ready - t_load, 1),
            inference_seconds=round(t_gpu1 - t_gpu0, 1),
            seconds_per_frame=round((t_gpu1 - t_gpu0) / max(1, len(left)), 3),
            t_import_epoch=T_IMPORT, t_fn_enter_epoch=t_fn,
        ),
    )
    rec["lane"]["t_fn_exit_epoch"] = time.time()

    out = Path("/vol") / (session or "run")
    out.mkdir(parents=True, exist_ok=True)
    (out / f"sweep_{int(t_fn)}.json").write_text(json.dumps(rec))
    vol.commit()
    print(f"swept {len(left)}/{len(want)} frames in "
          f"{rec['lane']['inference_seconds']}s gpu "
          f"({rec['lane']['seconds_per_frame']}s/frame)", flush=True)
    return rec


@app.function(image=image, gpu="A10G", volumes={"/vol": vol}, timeout=1800,
              memory=(16384, 24576), cpu=CPU_CORES, scaledown_window=2)
def sweep(video: bytes, stride: int = 6, dense: str = "", fps: float = 25.0,
          src: str = "", session: str = "run") -> dict:
    """The master-space silhouette sweep, on an A10G.  Same JSON as the local
    script, plus a `lane` block recording where and how fast it ran."""
    return _sweep(video, stride, dense, fps, src, session, "A10G")


@app.function(image=image, gpu="T4", volumes={"/vol": vol}, timeout=1800,
              memory=(16384, 24576), cpu=CPU_CORES, scaledown_window=2)
def sweep_t4(video: bytes, stride: int = 6, dense: str = "", fps: float = 25.0,
             src: str = "", session: str = "run") -> dict:
    """The same sweep on a T4, kept so the GPU choice stays a measurement."""
    return _sweep(video, stride, dense, fps, src, session, "T4")


@app.function(image=image, gpu="A10G", timeout=600)
def diag() -> dict:
    """What the CUDA EP loader actually sees.  Cents, and it answers the only
    question that ever goes wrong here."""
    import onnxruntime as ort
    out = {"ort": ort.__version__, "available": ort.get_available_providers(),
           "device": ort.get_device()}
    import glob
    import inspect
    ort.set_default_logger_severity(0)
    out["preload_signature"] = str(inspect.signature(ort.preload_dlls))
    try:
        ort.preload_dlls()
        out["preload"] = "ok"
    except Exception as exc:
        out["preload"] = f"{type(exc).__name__}: {exc}"[:1000]
    cuda_so = glob.glob("/usr/local/lib/python3.12/site-packages/onnxruntime/"
                        "capi/libonnxruntime_providers_cuda.so") or glob.glob(
        "/usr/lib/python3*/site-packages/onnxruntime/capi/"
        "libonnxruntime_providers_cuda.so") or glob.glob(
        "/**/libonnxruntime_providers_cuda.so", recursive=True)
    out["cuda_provider_so"] = cuda_so[:2]
    if cuda_so:
        ldd = subprocess.run(["ldd", cuda_so[0]], capture_output=True, text=True)
        out["ldd_missing"] = [l.strip() for l in ldd.stdout.splitlines()
                              if "not found" in l]
    out["nvidia_wheels"] = sorted(
        Path(x).name for x in glob.glob(
            "/usr/local/lib/python3.12/site-packages/nvidia/*"))[:40]
    try:
        s = ort.InferenceSession(ONNX, providers=["CUDAExecutionProvider"])
        out["session_providers"] = s.get_providers()
    except Exception as exc:
        out["session_error"] = f"{type(exc).__name__}: {exc}"[:2000]
    out["nvidia_smi"] = subprocess.run(
        ["nvidia-smi", "--query-gpu=name,driver_version",
         "--format=csv,noheader"], capture_output=True, text=True).stdout.strip()
    print(json.dumps(out, indent=1), flush=True)
    return out


def cost(rec: dict, dispatched_at: float) -> dict:
    """Billed container seconds -> USD, boot to scaledown.

    Same arithmetic as `pipeline/sam2/modal_app.py::cost`: a container bills from
    its own module import to the last function exit, plus `scaledown_window`.
    """
    lane = rec["lane"]
    billed = (lane["t_fn_exit_epoch"] - lane["t_import_epoch"]) + 2.0
    gpu = billed * GPU_USD_S[lane["gpu"]]
    cpu = billed * CPU_CORES * CPU_USD_S_CORE
    mem = billed * MEM_GIB * MEM_USD_S_GIB
    lane["cold_start_seconds"] = round(lane["t_import_epoch"] - dispatched_at, 2)
    lane["billed_container_seconds"] = round(billed, 1)
    lane["measured_cost_usd"] = round(gpu + cpu + mem, 4)
    lane["cost_breakdown_usd"] = dict(gpu=round(gpu, 4), cpu=round(cpu, 4),
                                      mem=round(mem, 4))
    return rec
