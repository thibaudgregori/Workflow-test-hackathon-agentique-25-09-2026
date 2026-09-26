# `pipeline/prep` — the front of the factory

The prep stage turns a Filmed recording into everything the matte lane needs:
the cut master (`cutlib.py`), the measured plate (`platelib.py`), the frame-0
prompt (`promptlib.py`), the reviewed selection and the MatAnyone 2 finish; the SAM2
track is the stage-18 fallback. `prep_batch.py` runs the whole front for a batch of videos.
Sessions live in `<run>/matting/<id>/` (the factory-wide `pipeline/sam2/sessions` root was
the pre-run-22 default and is being retired).

This manual covers **the one stage that leaves the machine**: the BiRefNet master
sweep — and, below, the one encoder decision the cut stage makes locally.

---

## The intermediate encoder — videotoolbox since 2026-09-03

`cuts/<id>/master.mp4` and the two face plates are **intermediates**: later
stages decode them, nothing ever delivers them. On macOS `cutlib.py` cuts all
three with Apple's hardware encoder at constant quality:

```
-c:v h264_videotoolbox -q:v 85 -pix_fmt yuv420p          # cut master
-c:v h264_videotoolbox -q:v 85 -pix_fmt yuv420p -g 25    # both face plates
```

`q:v 85` is the first rung of the quality sweep whose bitrate clears the libx264
files it replaces — 41.9 Mbit/s against crf 17's 25.9 on the 4K master, 17.1
against 8.0 on `face_full_hd.mp4`, 9.1 against 4.0 on `face_bottom_hd.mp4` — and
it measures **SSIM 0.988 / PSNR 46.7 dB against the x264 master** on sampled
frames. `-g 25` keeps the plates' own sparse-plate assertion satisfied
(videotoolbox honours `-g` exactly). Audio, filters, fps and `+faststart` are
unchanged.

`videotoolbox_available()` probes once per process — Darwin **and** the encoder
listed by `ffmpeg -encoders`. When it is false, `intermediate_video_args()`
emits the old `libx264` flags token for token, so a Linux or Modal run produces
the file it produced before. The post-master chores (both plates, and the
audio -> Scribe chain) then run in one `ThreadPoolExecutor`; `measure_face` still
finishes first because `face_cx` decides both crop windows.

**Measured on 2026-09-03** (M5 Pro, whole `build_cut()` call, mean of two runs):
`costpertask` 59.4 s -> **39.2 s**, `astramath` 39.9 s -> **30.2 s**, with
`source_take_start` / `source_take_end` / `cut_master_duration` identical to the
millisecond, `face_cx` within 0.1 px, identical crop windows and frame counts,
and a byte-identical `audio.m4a`. Full table:
`(run 11) review/cut_speedtest.md`.

---

## HISTORICAL (SAM2 lane, until 2026-09-05): the track+ship lane — H100 by default, ship on Modal's CPU (2026-09-03)

*Full measurement: `(run 11) review/phase1_remote_ship.md`.*

Three things changed in `prep_batch.py`.

**`--gpu` defaults to `h100`.**  Measured on run 11: 2.73x faster per frame for
1.23x the cost per frame.  An intake row's own `gpu` field still overrides it,
and `--gpu a10` is the lane every published lab number was measured on.

**The display plate moved out of ship and into the background.**  It is the one
piece of ship that cannot leave this machine — it is re-cut from the 4K master —
so `start_display_plate()` fires it as its own subprocess the moment the plate
stage lands, and `await_display_plate()` joins it at dispatch.  It is its own
stage now (`stages.display_plate.wall_s`).  Measured fresh: **9.6 s** astramath,
**14.5 s** costpertask, all of it off the critical path.  `ship.build_display_plate`
is the function in both lanes, so the x264 line and its up-to-date cache check
are not duplicated.

**The layers and the gates come back with the track.**  `dispatch_tracks` adds
`--ship --display WxH --display-plate ... --edge-box ... --plate-json ...` and
`collect_remote_ship()` then only has to check paperwork: the display plate this
machine cut, the three webms' own dimensions against the ship record's, and the
two gate verdicts.  The GPU is released before the encode starts — the ship runs
in the CPU-only `ship_remote` container that the track spawns.

`--ship-local` keeps the pre-2026-09-03 lane (`ship_matte`, `ship.py` on this
machine) for parity runs.  **Refusal semantics are unchanged in both lanes:** a
refused ship is `status: REFUSED` carrying the gate's own sentence, the stage is
an error, and the remedy is bolsterfix/wingfix plus a re-track — never an
`--allow-*`.  `track.py` exits **3** on a gate refusal so the track itself is
still recorded `ok` and its paid alpha is kept.

`--emit` is free-form (only `legacy` is special), which is how a parity run
writes `v5b`/`v5c` layers without touching a shipped `v5`.

### `_batch.json` counts every Modal dollar now

`modal_cost_usd` counted the **track lane only**, so the BiRefNet sweep's
$0.03-$0.06 per video had to be re-added by hand out of the plate stage — which
is exactly the arithmetic a report gets wrong, and did, in
`bench_timing_prep.md`.  It now sums **sweep + track + ship** and carries

```
"modal_cost_breakdown_usd": {"sweep": ..., "track": ..., "ship": ...}
```

`sweep_cost_usd()` reads `stages.plate.sweep.lane.measured_cost_usd`; verified
against this morning's untouched packages it recovers astramath **$0.0339** and
costpertask **$0.0585**.  `_batch.json` also gains `ship_seconds` per video, and
each package gains `stages.ship.where` (`modal-cpu` | `laptop`),
`stages.ship.ship_seconds`, `stages.ship.cost_usd` and
`stages.display_plate.wall_s`.

### Which ship lane to use

The frame-parallel compose and the fast lossless encoder settings live in the
**shared** `ship.py`, so the laptop lane got faster too.

| | astramath (706 f) | costpertask (1300 f) |
|---|---|---|
| ship, laptop, before | 67.3 s | 152.2 s |
| ship, laptop, tuned (`--ship-local`) | ~29 s | ~60 s |
| ship, `ship_remote` (32 cores) | 104.8 s · $0.0521 | 197.2 s · $0.0967 |

For one or two recordings the laptop is now the faster lane.  Modal wins when the
batch is wide — N ships get N separate 32-core containers instead of sharing this
machine's cores — and whenever the laptop has to stay free.  Both lanes run the
same code and the same gates.

---

## The auto-repair loop — two verification rounds inside prep (2026-09-03)

*Miguel, after run 12 refused three of four recordings and every refusal needed
a human to run a known mechanical repair: "we should auto-detect it and fix it.
I wanted to have at least two verification loops inside of the main loop so we
don't lose so much time."*

The ship verdict is no longer the end of the batch. When a ship is REFUSED,
`prep_batch.py` runs the repair a human would run, re-tracks on the same GPU
lane and re-ships through the same lane — **up to two rounds per recording** —
and only then reports a failure. **Nothing here weakens a gate.** There is no
`--allow-*` anywhere in `prep_batch.py`, both gates run unchanged on every
round, and a matte still ships only when both pass on their own terms.

### What triggers a round

Only a `REFUSED` ship stage, and only when it names a repairable gate.
`refusal_gate()` reads the container's own `gate` field on the Modal lane
(`collect_remote_ship`) and `ship.py`'s printed sentence on the laptop lane
(`ship_matte`), so both lanes classify identically.

| verdict | fix | what it does |
|---|---|---|
| **PROTRUSION**, scan has `wings` | `wingfix.py` | the headrest wing hanging beside the head. The columns and the row band come from the gate's OWN verdict — the wing's `x0`/`x1`, its ledge top row and the `shoulder_ref` row it hangs above — so the window is measured, never guessed. `--wing-right <x0>` for a right wing, `--wing-left <x1>` for a left one. It writes corrective prompt masks (frame 0 included) into `prompts_<tag>`. |
| **PROTRUSION**, no wings | `bolsterfix.py` | furniture above the shoulder line. It derives its own window from `protrusion.scan()`; only `--session/--alpha/--plate/--out` are handed in. |
| **EDGE CLIP** | a **wider plate** | under LAW 44's 2026-09-03 ruling this can only fire when the plate border is ON SCREEN, so the remedy the law itself prescribes is the whole fix. Per gated side: the gate's worst negative limb margin, plus the 24 px aim (`platelib.WANT_MARGIN_CANVAS`), converted to master px through `k * PLATE_SCALE`, **added to the extension that side already carries**, handed to `solve_overwide` as `need_floor_master_px`. Then `build_plate` again (the cached sweep is not re-paid), `promptlib.build_prompt0` on the new plate, a fresh display plate, re-track, re-ship. **A side whose border is already off screen by more than the rim is never widened** — it does not gate, and widening it would move the plate for a touch nobody can see. |
| anything else (`edge_box`, a stage error) | none | reported verbatim, no retry. An `edge_box` refusal means two files disagree; re-tracking would only pay for the same disagreement again. |

The gate's own verdict is re-derived by calling **`ship.protrusion_gate()`** —
the same function the ship lane calls — in its own process, because the printed
line carries the wing's columns but not its row band, and `wingfix` needs the
band.

### The two-round cap

Round `r` writes tag `v{r+1}`: `v1` refused → `v2` → `v3`. Every earlier tag
**stays on disk** (a refused alpha is the input the next fix reads, and it is
the evidence for the refusal). After round 2 is still refused the ship stage
becomes **`REFUSED_AFTER_2_ROUNDS`**, carrying every round's verdict verbatim in
`stages.ship.rounds_verdicts`. `--repair-rounds N` changes the cap;
`--no-repair` restores the pre-2026-09-03 behaviour for measuring the loop.

### Where the records land

Per package, `<run>/prep/<id>.json`:

```jsonc
"stages": {
  "repair": {
    "rounds": [{"round": 1, "gate": "protrusion", "fix": "wingfix",
                "tag": "v2", "track_seconds": ..., "ship_status": "ok",
                "cost_usd": ...}],
    "final_tag": "v2",
    "total_extra_cost_usd": ..., "total_extra_wall_s": ...,
    "round0": {"tag": "v1", "track": {...}, "ship": {...}}
  }
}
```

Each round also records the fix's own numbers — the wing windows the gate found
and the cut wingfix made, or the per-side `need_floor_master_px` arithmetic and
the plate box before and after.

**`stages.track` and `stages.ship` point at the FINAL tag's records**, so every
downstream station reads the alpha and the layers that actually passed;
`reconcile()` is pointed at that tag too, or it would recover `run_v1.json` over
a `v2` that passed. `stages.repair.round0` keeps the first attempt's records so
the money it spent is still in the batch's arithmetic.

In `_batch.json`:

- `repairs: {id: n_rounds}` — absent means the recording passed in round 0
- `repair_detail` — each round's `{round, gate, fix, tag, track_seconds, ship_status, cost_usd}`
- `modal_cost_breakdown_usd` gains a **`repair`** line, and `modal_cost_usd`
  is `sweep + track + ship + repair`. `track` and `ship` stay the ROUND-0 sums
  (read out of `stages.repair.round0` where a repair happened), so the repair
  loop's spend is separated instead of folded in
- `summary_lines` — the same one line per recording the console prints last

### The summary line

The last thing the run says, one line per recording:

```
hermeskanban         PASS after 1 repair (wingfix)
astramath            PASS in round 0
costpertask          REFUSED after 2 rounds (protrusion, protrusion)
```

---

## The BiRefNet master sweep

### What it measures, and why the plate cannot be built without it

A tracked SAM2 alpha lives in **plate** space. When the plate's own border cuts
him, the alpha is flush against that border *there*, so it cannot say how much
more of him is outside the crop — the measurement a wider window has to be
chosen against does not exist in plate space at all.

The sweep produces it in **master** pixels: for every sampled frame, the leftmost
and rightmost silhouette column of every master row, from the same
BiRefNet-general mask `prompt0.py birefnet` already trusts for the frame-0
prompt. `platelib.measure_silhouette` then reduces that to the only four numbers
the plate solve consumes:

| per side | what it is |
|---|---|
| `shoulder_baseline_master_row` | the highest master row that contacts the head-parity border on ≥ 90 % of measured frames — below it, his shoulders run off both edges on every approved cutout, and that is not the defect |
| `extreme_master_x_above_baseline` | the furthest the silhouette ever reaches above that row — the hand, the elbow, the raised arm, the things that get amputated |

Everything else in the JSON is working material for those two.

### Where it runs — Modal by default since 2026-09-03

The sweep is one independent BiRefNet forward pass per sampled frame, and on the
laptop it ran on `CPUExecutionProvider`. On the 2026-09-02 prep test that was
**1,787 s for 106 frames — 96 % of the whole plate stage**, for a measurement
that decides two integers per side.

The same ONNX graph now runs on a Modal **A10G** through
`shorts-factory-birefnet`.

```bash
# the normal path: build a 720p proxy, sweep it on the A10G
~/Documents/Workspace/.venv/bin/python pipeline/prep/birefnet_master_sweep.py \
    --src <cuts/<id>/master.mp4> --out <gen/_birefnet_master_<id>.json> --stride 6

# send the master itself instead of the proxy (bit-identical input to the local
# lane, at the cost of an 84-190 MB upload)
    ... --full

# the CPU fallback, and the ONLY path that needs the bake-off venv
pipeline/prep/.venv-birefnet/bin/python \
    pipeline/prep/birefnet_master_sweep.py --local --src ... --out ...
```

`platelib.build_plate(..., sweep_local=False)` and
`prep_batch.py` (with `--sweep-local` to fall back) pick the interpreter to
match: the Modal lane needs `modal` from the workspace venv, the local lane needs
`rembg` from the bake-off venv. **The cache is unchanged and lane-blind** — a
sweep JSON already on disk is never paid for twice, whoever produced it.

### What is on the far side

`pipeline/prep/birefnet_modal_app.py`, deployed as **`shorts-factory-birefnet`**:

- `sweep(video, stride=6, dense="", fps=25.0, src="", session="run") -> dict` — A10G
- `sweep_t4(...)` — identical body on a T4, kept so the GPU choice stays a
  measurement and not an opinion
- `diag() -> dict` — what the CUDA EP loader sees; cents, and it answers the only
  question that has ever gone wrong here

The image is `debian_slim` + `onnxruntime-gpu[cuda,cudnn]==1.29.0` with the
**exact** `BiRefNet-general-epoch_244.onnx` `rembg` downloads, curled into an
image layer and **md5-checked in the build** (`7a35a014…`). Volume
`shorts-factory-birefnet` keeps every run's JSON so a dropped return never means
paying for the GPU twice. No schedule, no web endpoint, no secrets.

`rembg` is **not** installed there. Importing it drags in pymatting, numba,
scikit-image and scipy for code paths the sweep never touches, so the twenty
lines it actually uses — `BaseSession.normalize`, then
`BiRefNetSessionGeneral.predict`'s sigmoid / min-max / LANCZOS tail — are
reproduced in the app. That reproduction was proved **byte-identical** to
`rembg`'s own output on the laptop first: `alpha_max_abs_diff = 0` on frames 0,
300 and 630 of the prep-test master.

---

## Measured: 2026-09-03

### Wall clock and cost, per sweep

Prep-test master, 631 frames, stride 6 → **106 frames measured**.

| lane | inference | client wall | billed container | cost |
|---|---|---|---|---|
| laptop CPU (`--local`, 2026-09-02) | — | **1,787.6 s** | — | free, and the machine is unusable |
| **Modal A10G**, 720p proxy | **57.9 s** (0.546 s/frame) | 207.1 s cold / **~70 s warm** | 69.8 s | **$0.0312** |
| Modal T4, the identical proxy | 159.1 s (1.501 s/frame) | 412.3 s cold | 174.3 s | $0.0530 |

Cold start was **137.1 s** of the A10G's 207.1 s — a first pull of a ~4 GB image
on a fresh GPU host. Warm, the client wall is the container's own span: ~70 s.

**31x faster than the laptop, for three cents.** The 60 s target is met on the
GPU stage (57.9 s) and on a warm call end to end; a cold first call in a batch
pays the image pull once and every later video in the same batch runs warm.

**A10G, and it is not close.** The T4's GPU-second is 0.54x the A10G's, but it
runs **2.75x slower** on this graph, so it costs **70 % more per sweep** and takes
almost three times as long — and CPU + memory, which bill for the whole container
either way, turn a slow GPU into a double loss ($0.0245 of the T4's $0.0530
against $0.0098 of the A10G's $0.0312). `sweep_t4` stays deployed only so the
choice is re-measurable. Their outputs agree: over the identical proxy, 543 of
63,785 left rows and 1,581 right rows differ at all (max 60 / 75 master px, mean
0.03 / 0.14), and the take-wide extremes are identical.

Cost breakdown at A10G / 8 cores / 16 GiB: GPU $0.0214, CPU $0.0073, memory
$0.0025. The arithmetic is `pipeline/sam2/modal_app.py::cost`'s, with the same
published rates, so the two GPU lanes' numbers are directly comparable.

A second, longer subject: run 9's **perplexityprojects** (1,354 frames, stride 6
plus the `390-430` dense window → **159 frames measured**) ran **86.9 s** on the
GPU at the same 0.547 s/frame, 277.8 s of client wall with a 176.6 s cold start,
for **$0.0454**.

### Parity — the numbers `platelib` actually uses

Modal A10G on the 720p proxy **vs** the laptop CPU sweep on the master
(`references/evidence/prep_parity/_birefnet_master_preptest.json`, 2026-09-02), read through
`platelib.measure_silhouette` at the shipped head-parity crop `2208x1840+714+320`:

| | laptop CPU | Modal A10G | delta |
|---|---|---|---|
| left `shoulder_baseline_master_row` | 2013 | 2013 | **0** |
| left `extreme_master_x_above_baseline` | 645 | 645 | **0** |
| right `shoulder_baseline_master_row` | 1908 | 1908 | **0** |
| right `extreme_master_x_above_baseline` | 3012 | 3012 | **0** |
| take-wide leftmost / rightmost master x | 525 / 3192 | 525 / 3192 | **0 / 0** |

Fed through `solve_overwide`, both produce the **same** over-wide window
`2576x1840+530+320`, the **same** plate `1260x900`, and the **same** 184 master
px of extension per side — which is exactly the plate the prep test shipped.

And the same test against a **run-9** sweep — `perplexityprojects`, replayed at
its own stride 6 with its own `390-430` dense window, read at that session's
head-parity crop `2208x1840+710+200`:

| | laptop CPU (run 9) | Modal A10G | delta |
|---|---|---|---|
| left `shoulder_baseline_master_row` | 1929 | 1929 | **0** |
| left `extreme_master_x_above_baseline` | 666 | 666 | **0** |
| right `shoulder_baseline_master_row` | 1899 | 1899 | **0** |
| right `extreme_master_x_above_baseline` | 3126 | 3126 | **0** |
| take-wide leftmost / rightmost master x | 504 / 3159 | 504 / 3159 | **0 / 0** |

Same solved crop `2576x1840+618+200`, same plate `1260x900`, same extension.

### Parity — the raw rows, and the honest caveat

Row for row the two JSONs are **not** identical, and the cause is the proxy, not
the GPU:

| comparison | left max row delta | right max row delta | rows differing |
|---|---|---|---|
| preptest: A10G on the 720p proxy vs laptop CPU on the master | 267 master px | 234 master px | 12,892 / 63,785 and 21,701 / 63,785 |
| ↳ median row delta | 0 | 0 | — |
| ↳ 90th percentile | 3 master px | 99 master px | — |
| perplexityprojects, same comparison | 549 master px | 237 master px | 31,519 and 31,510 / 97,297 |
| **A10G vs T4**, the identical proxy | 60 master px | 75 master px | **543 and 1,581** / 63,785 |

**Two causes, both measured, and the bigger one is the proxy.**

1. **The proxy.** Running the *laptop CPU* BiRefNet on the same crf-12 proxy
   reproduces the disagreement against the master (max 1,804 / 1,807 master px on
   frame 6, 64 / 114 rows of 720). Nothing about CUDA is involved.
2. **CUDA vs CPU kernels.** CPU and A10G on the **identical** proxy still differ
   by up to 108 master px on 30-100 rows of 720 (frames 0, 6, 300, 504, 630).
   GPU against GPU is an order of magnitude tighter — the A10G/T4 row above.

BiRefNet's mask is genuinely near-binary-unstable at a handful of rows, and where
the silhouette's connectivity flips the per-row extreme can jump by hundreds of
master px. That is a property of the model, not of this port.

Raising proxy quality narrows it but does not close it — crf 10 in **yuv444p**
brings frame 6 from 1,804 to 114 master px — and a truly lossless proxy is
**larger than the master** (yuv444 qp 0: 189 MB, rgb24 FFV1: 260 MB, against an
84 MB master), so lossless is not a proxy at all.

**Why the proxy is still the default.** The instrument's output is those four
integers, and they are identical. The rows that disagree are rows the solve never
reads: they sit at master rows 348-1,404, above the shoulder baseline but inboard
of the take-wide extreme, and the solve takes an extremum over the whole take —
which is stable because the extreme frames agree. When a plate is being argued
over and the raw rows have to match, `--full` sends the master and the input is
bit-identical.

The prep-test master was rebuilt from `cuts/preptest/edl.json` for this
comparison (the original was cleaned up). The rebuild is exact: 631 frames, and
the laptop CPU sweep on the rebuild reproduces the 2026-09-02 JSON with **0
delta on all 720 rows** of frames 0, 300 and 630.

---

## Failure modes worth knowing

**`RuntimeError: CUDA EP unavailable`.** `onnxruntime-gpu` ships the CUDA
provider as a shared library that dlopens the nvidia wheels' `.so` files, and
nothing puts those on the loader path. Without `ort.preload_dlls()` the session
builds **happily and silently** on `['CPUExecutionProvider']` — no exception, no
warning, a 30x slower run that still returns correct numbers. The app calls
`preload_dlls()` before every session and refuses to run without CUDA. `diag()`
prints `ldd`'s missing list and the nvidia wheels present when it needs proving.

**Pinning a `nvidia/cuda` base image is a guessing game.** `12.6.2-cudnn` gave
`['CPUExecutionProvider']` because ORT 1.29 wants **CUDA 13**
(`libcudart.so.13`, `libcublas.so.13`). The `[cuda,cudnn]` extras pull the exact
wheels the ORT build was compiled against, so the CUDA version is the wheel's
problem instead of ours.

**The upload is the slow half on a big master.** The 720p proxy costs ~1.4 s to
build and takes the payload from 84 MB to 17 MB. `--full` is correct but slow on
this connection.

### A crashed stage gets up to two retries (2026-09-03, run 12)

`prompt0` re-runs up to twice, 5 s apart, if `build_prompt0` raises (the BiRefNet
subprocess died with `recursive_mutex lock failed` when four ran at once; the
resume passed in 7.5 s). Every attempt is recorded under `stages.prompt0.retries`. A
third crash is the real error and is reported as before. Gate refusals are the
auto-repair loop's business, not this retry's.

### The outline gate — LAW 48, BUILT 2026-09-04

*Was a TODO here until 2026-09-04. Code: `pipeline/sam2/outline.py`, wired as
`ship.outline_gate` between the protrusion gate and the encode. Calibration
table: the module docstring.*

The protrusion gate asks only a top-y-profile question and passed two mattes
Miguel rejected on sight — `hermeskanban` in run 12 and `reasoninglevel` in run
13 — both carrying the half of a headrest WEDGE that survives to the body side
of a rectangular `wingfix` cut. `outline.py` is that defect's own two
measurements, run on the ALPHA before a frame is encoded so a refusal costs
seconds and lands here:

| instrument | what it asks | ceiling |
|---|---|---|
| **straight edge** | per frame, the longest run of consecutive rows whose extreme silhouette column is identical (±1), inside the head band | a >= **40**-row run on more than **40 %** of frames, or a **p95 of 60 rows** |
| **retained dark** | per frame, the plate-dark pixels (luma <= 60) the mask KEPT in a 50-column band running inward from its own edge, as a share of that band | **p95 above 0.78** |

**Both are windowed to the HEAD BAND** — the 180 rows ending at the shoulder
arrival, i.e. jaw, neck and the top of the shoulder. Above it is his black cap,
whose side is a genuinely straight edge for 40-107 rows on approved mattes;
below it is his black t-shirt. Measured over the whole body, neither instrument
separates a rejected matte from an approved one at all. Windowed, both do, with
a clear gap on either side of every threshold (approved p95 33-50 rows and
0.14-0.62 of the band; rejected 59-132 rows and 0.99-1.00).

**The repair.** An outline refusal is `REPAIRABLE_GATES`' third member and runs
`wingfix.py` on the refusing side with the window the gate MEASURED:

- **rows** — the head band's own rows, top lifted by 20, **bottom left exactly
  at the shoulder arrival**. There is no bottom margin on purpose: `wingfix`
  cuts every mask pixel darker than its guard, and his t-shirt is black.
- **cut column** — the deepest inward column that still holds retained
  plate-dark pixels (a `reach` walk with no 50-column ceiling, so a saturated
  count cannot under-size the window), plus 10 px.
- **`--chunk 40`**, i.e. a corrective keyframe every <= 10 frames. The default
  cadence leaves gaps SAM2 regrows the wedge inside, which is the flicker half
  of Miguel's complaint.

The gate independently reproduces the hand-driven repair: on `hermeskanban`'s
refused alpha it measures a cut column of **509** over rows 279-499, against the
**510** over rows 300-464 a human read off `wingfix --measure` and shipped.

A wedge is not a rectangle, so if one window leaves an upper band, **round 2
re-measures round 1's alpha and cuts again** — the two-window chain the
hermeskanban repair had to be driven by hand, now done by the loop.

**First live run (`reasoninglevel`, 2026-09-04):** refused in **1.7 s** before
any encode, one round, `wingfix --wing-left 577 --rows-left 288,488 --chunk 40`
(80 corrective keyframes, median 14,159 px cut, max removed luma 60 against a
guard of 60), re-track on H100 128.5 s / **$0.1523**, re-ship 64 s, PASS. The
left side went from straight-run p95 87 rows / 99.4 % of frames / dark p95
9,048 px (100 % of the band) to **42 rows / 9.2 % / 1,388 px (15 %)**.

**The known limit, and it is Miguel's own ruling.** The law says p95, so p95 is
what refuses, and a sub-second burst is therefore invisible to it:
`hermesdesktop` v2's right side maxes at 8,873 px (0.98 of the band) on ONE
frame at 1.4 s — the chair splash at the very start that Miguel saw and told us
not to redo. Every other approved matte's max is <= 5,671. `dark_frac_max` is
recorded in the `law48` block for exactly this reason and is **never gated**: a
max-based test would refuse a file its owner accepted.

---

## THE CHAIR PROMPT — a sub-stage of `prompt0` (2026-09-04)

Miguel approved the chair-as-second-object matte and asked for it as the main pass, so `prompt0`
now produces TWO prompts: the frame-0 body mask it always produced, and the headrest wing's box
and clicks.  STANDARD.md's "THE CHAIR IS A SECOND OBJECT" is the law, `pipeline/sam2/README.md`
"THE STANDARD CLEANING PASS" has the detector's guards and the regression numbers, and this is
what changed in prep.

**The stage.**  `chair_prompt_stage(session)` calls `pipeline/sam2/chairprompt.chair_prompt` on
`plate_wide_25.mp4` frame 0 with `prompts/birefnet_00000.png` as the silhouette, and writes:

    <session>/chair_prompt.json                     the box + clicks, per side
    <session>/prompts/chair_overlay_00000.png       the proof overlay
    package.stages.prompt0.chair_prompt             side, box, points, band, luma stats

**It never raises.**  A detector that throws must not cost a paid GPU run, so the stage catches
everything, deletes the json and records `{"status": "error", ...}`.  No json means no exclusion
object, which is the old single-object pass, byte-identical.  A MISS is the same thing and is not
an error: `viberesearch` has no wing beside his head and gets exactly what it shipped with.

**`build_track_cmd` picks it up.**  The `--exclude-json` flag is added when the file exists and
the package does not carry `no_chair_object`.  It is in `build_track_cmd`, so a REPAIR ROUND
re-tracks with the chair object too — the fallback stacks on the standard pass rather than
replacing it.

**`wingfix` is still the fallback and nothing about it changed.**  If LAW 48 refuses after the
two-object track, `auto_repair` runs as before.  On the run-12/13 corpus the two-object pass made
that unnecessary on `reasoninglevel` (PASS in round 0 where the old pass needed a repair round),
but the branch is live and is what catches a wing the detector missed.

**A REPLATE INVALIDATES IT.**  `repair_round`'s widen branch re-derives the chair prompt right
after `build_prompt0`, for the same reason it re-cuts the display plate: every coordinate the
chair prompt carries is in plate pixels, and the plate just changed size.  Without that the
exclusion box lands on his cheek.

### Flags

| flag | effect |
|---|---|
| `--no-chair-object` | batch-wide: no second object anywhere.  The pre-2026-09-04 pass exactly |
| `no_chair_object: true` on an intake row | the same, for one recording |

### What a standard pass looks like now

`reasoninglevel`, 2026-09-04, `--skip cut,plate,display_plate,cues --ship-local --tag c1`:

    prompt0   13.0 s   chair_prompt found LEFT, box [460,176,566,443], 4 positive / 4 negative
    track    120.0 s   H100, $0.1228, obj 2 margin 2 px + 8 px dark-only, fence [194,433] auto
    ship      64.4 s   protrusion clean / LAW 48 clean (left p95 37.8, at-line 4.6 %,
                       dark 1,991 px = 22 %) / edge clip CLEAN
    PASS in round 0 — no repair round, one GPU run

### THE PROMPT GUARD — a repair is never silently re-derived (2026-09-04)

`prompt0` REFUSES to rewrite a frame-0 prompt that has been repaired, because re-deriving it
throws the repair away.  Measured, on `hermesdesktop`: the standard pass re-ran `prompt0`, the
UNCUT BiRefNet prompt came back, obj 1 went back to tracking him plus both wings, and the matte
came out holding **11,434 px/frame more** than the file it was replacing.

**The comparison, and the one backup name.**  `promptlib.preserve_original(session)` snapshots
`prompts/kf_00000.png` to **`prompts/_original/kf_00000.png`** the first time anything is about to
change it, and never again; `prompt0` also writes it the first time it runs.  Before this every
repair invented its own name — `prompts_v1`, `prompts_v1_backup`, `prompts_v2`, `prompts_v4` — and
on `hermesdesktop` and `dgxspark` the repair OVERWROTE `prompts/` and archived the original under
a name that reads like a version, so "the original frame-0 prompt" was not recoverable from the
session's shape alone.  One name, written once.

`promptlib.prompt_is_repaired(session)` compares the live prompt against `_original/` and reports
`repaired`, both areas, and the removed / added pixel counts.  When it says repaired:

    prompt0 status "kept"   — BiRefNet is not run at all (0.2 s instead of 14 s)
    wings_source            — "N/A — the repaired frame-0 prompt was KEPT"
    package.stages.prompt0.prompt_guard  — the full comparison
    the log line names the removed px and says how to override

**Overriding it**: `--reset-prompt` on `prep_batch`, or `reset_prompt: true` on the intake row.
The REPLATE branch passes it unconditionally and must: the plate changed size, so the old prompt's
pixels are in the wrong coordinate system and keeping them would be worse than losing the repair.

Seeded on the four sessions whose original was identifiable: `hermesdesktop` (repaired, 12,936 px
removed), `dgxspark` (repaired, 11,105 px removed), `hermeskanban` and `reasoninglevel` (live
prompt IS the original).  Every other session gets its snapshot the next time `prompt0` runs.

#### The chair prompt can be supplied by hand, and the record says so

`row["chair_prompt"] = {"<side>": {"box": [...], "points": [...], "source": "..."}}` on the intake
row overrides the detector for that side — the same rule `derive_wings` already follows for
`wings`: **an explicit intake row outranks the instrument.**  Used on `hermesdesktop`'s RIGHT
wing, which the sandwich test cannot see safely (his hair touches it, and the only search window
that finds it also finds a "wing" on seven faces).

The record never pretends a hand prompt was measured.  The overridden side carries `source`,
`replaced_detector_verdict` and the detector's own `why`; the top level carries
`overridden_sides`; and the proof overlay is redrawn with the hand box and clicks in it.

---

## THE SELF-HEALS (run 14, 2026-09-04)

Miguel: *"every time you encounter bugs like this fix them; the idea is to have a self-healing
loop."*  Three run-14 prep failures, three pipeline fixes, one regression suite:
`~/…/.venv/bin/python pipeline/prep/test_regressions_2026_09_04.py` (27 checks now, each asserted
against the run's own case; the three run-14 ones are still the first three).

### A missing run record is recovered, not fatal

`track.py` writes the run record LAST — after the alpha is downloaded and the remote ship is
collected — so a crash on that line loses a paid track with every artifact intact.  The ship stage
now calls `recover_run_record(session, tag)` before erroring: the CONTAINER wrote its own copy to
`/vol/<session>/run_<tag>.json` before returning, so it is pulled down, stamped
`recovered_from_volume`, and the stage carries on.  No re-track.

### A gate refusal becomes a chair prompt before it becomes a cut

`chair_from_gate(pkg, gate=…, law=…, scan=…)` is tried FIRST in both repair branches.  Both gates
report the window they are refusing on — `outline` gives rows + a `wing_column`, `protrusion`
gives the wing's own columns — and `chairprompt.from_refusal()` turns that window into a box, four
positives down its dark spine and the standard four negatives.  Derived prompts are merged into
`<session>/chair_prompt.json` (with `source` naming the gate and `derived_sides` listing them) and
the re-track picks them up through `--exclude-json`.  A chair-object fix REUSES the previous
round's prompts: it changes `exclude=`, not the frame-0 mask, so pointing the re-track at an empty
`prompts_<tag>/` would re-segment from nothing.

**It refuses to guess, and that is the point.**  A window wider than `max_box_w` (150 px) is called
`"not a wing"` and no prompt is produced — grokbuild's outline refusal names a 275 px window
because the gate fired on his own jaw-to-shoulder line, and deriving a chair object there would
have carved his neck automatically.  The rejection is recorded in the repair round as a finding:
the remedy for a false positive is a reasoned `--allow-outline`, never another cut.

Proven on run 14: `trycrm` and `game33c` both refused protrusion on the right, both had a real
wing, both derived a prompt from the gate's own numbers and passed after ONE round with no cut and
no human.

### Inner stumbles no longer refuse a cut

See STANDARD.md "INNER STUMBLES STAY".  `cutlib.detect_take` reads the marker rule off the last
marker BEFORE the keeper (`markers_before`), so an inner stumble cannot make it disagree with the
content rule, and closure records inner markers instead of raising.  `edl.json` carries
`inner_markers` (index, text, start, end, nine-word context) and `markers_before_keeper`.

### A gate that returns nothing is answered by the marker (run 17, 2026-09-08)

`gate_marker.py` is the gate's judgement in deterministic python, and it ALWAYS answers:

    python pipeline/prep/gate_marker.py --run <run> --id <id> --stage ship [--wait-s 570]

It applies the override rule (`<id>.<stage>.override.json` wins), blocks in python until the marker
passes so a gate agent runs ONE bounded Bash call instead of keeping itself alive through a
forty-minute poll, calls a half-written marker `unreadable` rather than a verdict (`mark_stage`
uses `write_text`, which is not atomic), reports `missing` instead of raising, and prints
`status`/`final`/`override_used`/`waited_s`/`error`/`outputs`/`log_tail` in the shape the workflow
gate schema expects.  `final` is true only for `SKIPPED_NEEDS_KEY` and `not_a_short`.

**Why.**  On run 17 the matte gate for `eudisclosure` returned NOTHING on all three spawn attempts
and never wrote its started sentinel, while `prep/stages/eudisclosure.ship.json` had said `"ok"`
since 00:45:23 with all three matte layers on disk and hash-matching `ship_v5.json`.  The workflow
called that "the gate agent never returned", could not tell it apart from a refused encode, and
spent the recording's ONE repair round on an answer that was lying on disk.  So `gateWatch` in
`.claude/workflows/daily-shorts.js` never believes a null gate any more: it spawns the one-command
`marker:<stage> <id>` reader and uses what the marker itself says.  Checks:
`test_regressions_2026_09_04.py` (3 checks bound to this recording's numbers) and
`pipeline/test_workflow.mjs` (a null `gate:ship` must reach the marker reader, cost no repair round
and still run the cutout lane).

### One reader is not a fallback, and an `ok` is only as good as its layers (run 17, cursorworkspace)

The SECOND recording of run 17 lost its `gate:ship` the same way, three minutes after the fix above
landed, and it exposed two holes in it.

**The fallback was itself an agent.**  `markerRead` is spawned to cover "an agent returned nothing",
so when it also comes back empty the workflow is straight back in the trap.  `gateWatch` now spawns
it `MARKER_READS` (2) times, each a fresh spawn with its own label and sentinel, and if every one is
empty the poll is logged as *the marker on disk is UNREAD*, which is not the same as non-ok.
`gateErr(null)` no longer reads like a stage failure either: it names the agent-dispatch failure and
hands the repair agent the exact `gate_marker.py` command as its first move.

**An `ok` marker did not prove its own files.**  `gate_marker.outputs()` checked `is_file()` and
nothing else, so an `ok` over a truncated, empty, half-copied or stale webm still read `ok`, and
`outputs` quietly came back with two layers instead of three - which is why both run-17 repair
agents re-hashed the three webms by hand against `ship_v5.json`.  That hand-check is now the rule:
`gate_marker.verify_outputs()` re-hashes the three layers against the manifest the ship stage
already writes, and a passing marker whose files disagree with it becomes `outputs_incomplete` -
NOT a pass, NOT final, so the gate polls (a layer still flushing settles) and then repairs instead
of building a lane on a broken matte.  With no readable manifest nothing is downgraded
(`outputs_verified: "no_manifest"`), because a missing file to check against is not a defect.
Checks: `test_regressions_2026_09_04.py` (2 more, bound to cursorworkspace's 538 frames, 1386x990
and its three recorded sha256) and `pipeline/test_workflow.mjs` scenario 5 (a null gate plus a null
reader is retried, costs no repair round and still runs the cutout).

### The keeper opening can sit mid-breath (run 19, geo, 2026-09-13)

The content rule picks the LAST scripted opening, and that word is not always where the delivered
SENTENCE begins.  geo's take is *"this is why | AI SEO, also known as GEO, is brutally hard"*: the
keeper `AI` (w26, 37.38 s) lands 0.141 s after `why` inside ONE breath, so no `>= SILENCE_RUN_MIN`
silence exists anywhere before it and `measured_head` refused — which failed `cut`, then `plate`
("no cut master"), `prompt0` (blocked), `cues` ("no tight transcript") and `track` ("No valid
prepared plate"), i.e. one head rule cost the whole recording.

`cutlib.utterance_lead_in()` now answers it: the take starts at the head of the utterance carrying
the keeper — the maximal run of words joined by transcript gaps below `SILENCE_RUN_MIN`, bounded to
8 words / 3.0 s, and never crossing an earlier scripted opening or a discard marker (those words
are the abandoned attempt).  `build_cut` calls it ONLY on the "no silence run" refusal, re-measures
the head at that boundary and records `take_detection.lead_in_walk_back`; if that boundary has no
measured silence either, the refusal stands.  On geo it returns w23 `this is why` @36.779 with a
real 0.48 s silence run (36.169–36.649) in front of it, head 36.549, cross-check 2b 0.13 s, master
53.456 s opening on the complete sentence with both abandoned attempts (13.0 s, 25.3 s) excluded.
`take_word_index` is untouched, so a hand-pinned `expected.take_index` still asserts.

Two blockers the same repair uncovered, both fixed in the same spirit:

* **The VPN preflight refused a batch that uploads nothing.**  `vpn_preflight` guards Modal uploads
  — `plate` (the BiRefNet sweep; local under `--sweep-local`), `track`, `ship` — but it ran before
  the plan, so a cut-only repair with all three skipped was still refused at launch and a held lane
  lost a round to it.  It now takes `skip`/`sweep_local` and only refuses when a Modal stage is
  actually planned; the refusal is unchanged the moment one is.
* **A skipped stage un-passed the marker the gates poll.**  The package json has merged since run 14
  ("A RE-RUN MERGES, IT DOES NOT ERASE") but `mark_stage` rewrote unconditionally, so a targeted
  `--skip track,ship` repair stamped `"skipped"` over an `ok` ship marker and the matte gate would
  have polled a paid, shipped matte as if it had never run.  A `skipped`/`reused` record now leaves
  a PASSING marker alone; every verdict the run really measured still lands.

Checks: `test_regressions_2026_09_04.py` (3 more, bound to geo's own word indexes, gaps and
measured silence run).


## THE MATTE VIEWER TEST AND THE SAM2 FALLBACK (2026-09-14)

A passing ship marker is not a matte anyone has looked at. Stage 17 (`matte_review:<id>`) runs `pipeline/matting/matte_review.py` and a fresh agent opens its sheets; a HOLD runs stage 18, `pipeline/matting/fallback_sam2.py` (reviewed contour as the only SAM2 prompt, `--no-chair-object`, temporal-1 finish, install with `*.pre_fallback` backups, ship marker re-stamped with `keys.fallback`). Details and the geo history: `PRODUCTION.md` and `STAGES.md` rows 17-18.
