# MATTE — the black-on-black bake-off

Fix round `mattebakeoff`, 2026-08-30. Miguel's brief: *"Try as hard as you can
with different models and see what works best by comparing, I will also change
for upcoming videos but I want to prepare worst case scenarios."*

This footage IS the worst case: a **black gaming chair** directly behind a
**black cap** and a **black t-shirt**, lit by a soft key from the front so the
chair and the subject share the same luminance band. Everything below is
measured on it, and the ceiling is stated honestly.

---

## TL;DR

| | |
|---|---|
| **Winner** | `birefnet-general` (BiRefNet general checkpoint, via rembg 2.0.81 ONNX) |
| **Runner-up** | `bria-rmbg` — wins on the raw matte, **loses after post-processing** |
| **Loser** | `u2net_human_seg` — the model the shipped cutout used |
| **Improvement** | composite defect **2.18 → 0.16** (13× better); chair leak **2.006% → 0.056% of frame (36× less)** |
| **Biggest surprise** | **RVM lost.** The temporal video-matting specialist is 4th. |
| **Second surprise** | **Erosion is a net negative here** — measured 46:1 against. |
| **Ceiling** | Software gets the chair from *"a black hood welded to his head"* to *"a few hundred fused pixels at one shoulder"*. It does not reach zero. |
| **Filming fix** | Lifting the chair out of black to mid-grey removes **88%** of what is left. |

Deliverables: `_shared/matte_best.webm` (clean cutout, straight alpha) and
`_shared/matte_best_rim.webm` (cream die-cut baked in). Both 1080x900, 25fps,
1354 frames, 54.16s.

---

## 1. What the failure actually is

The shipped cutout blamed "the chair survives segmentation". That is true but
it undersells it. Measured on the lab's canonical wide plate:

**`u2net_human_seg` does not retain a chair fragment — it classifies the entire
chair as part of the person.** The alpha is a single connected component
covering **45.2% of the frame**, and the silhouette reads as a man wearing an
enormous hood. This is why no threshold, no largest-component filter and no
static geometric mask ever fully fixed it: there is nothing to filter, the
model's answer is simply the wrong shape.

Two distinct defects have to be separated, because they behave completely
differently under post-processing:

| defect | what it looks like | fixable in post? |
|---|---|---|
| **chair leak** | solid black slab attached to his head/shoulder | **No.** It is the model's shape. |
| **haze** | chair kept at alpha 0.2–0.6 — a translucent grey smear over a bright scene | **Yes, cheaply.** One S-curve. |
| **subject loss** | bits of him missing | Only by not causing it. |

The scoring below weights haze 1.5× because a *translucent* wrong answer looks
worse on screen than a hard one — it reads as a dirty lens rather than an edit.

---

## 2. Method

**Source.** All work is at **native 25fps** (Global Law 6). The 30fps master is
25fps conformed by duplicating one frame in six; the duplicate is deterministic
at `n mod 6 == 3`, verified by `mpdecimate` over the first 120 frames. Decimation:

```
select=not(eq(mod(n\,6)\,3)),setpts=N/25/TB   ->  1625 -> 1354 frames, 54.16s
```

**Plate.** The bake-off ran twice: first on a bake-off-local 1080x1920 crop,
then re-verified on the lab's canonical delivery plate
`_shared/face_wide_25.mp4` (1080x900, shoulders + upper torso, per Global Law 1).
All numbers quoted here are from the canonical plate.
Snapshot: `matte_bakeoff/src/canon_wide_25.mp4`,
sha256 `09cf4fcc4916eca5f35ef640ff5f42053fdff839d8b6e624ba4be9d276077f5e`.

**The 5 failure-zone frames.** Chosen objectively, not by eye. A chair-leak scan
saturated (the baseline leaks on *every* frame), so frames were picked at the
peaks of **head-motion energy** in the cap+face band — the turnarounds where the
chair/shirt/hair boundary is moving — plus one calm control:

| frame | t | why |
|---|---|---|
| 79 | 3.16s | turnaround, motion 10.1 |
| 202 | 8.08s | turnaround, motion 10.8 |
| 486 | 19.44s | **calm control**, motion 2.3 |
| 793 | 31.72s | turnaround, motion 11.6 |
| 1225 | 49.00s | turnaround, motion 12.1 (highest) |

**Scoring without ground truth.** There is no labelled matte for this footage,
so a **panel consensus** is used: a pixel is "certainly him" when all-but-one of
the five strong candidates agree, "certainly not him" when at most one does.
Pixels the panel disagrees on are excluded — every model is graded only on what
the panel is confident about. Chair leak is additionally **weighted by source
darkness**, so retaining a black chair is penalised and retaining a bit of pale
wall is not.

```
defect_score = chair_leak% + subject_loss% + 1.5 x haze%     (lower is better)
```

**Reproducibility caveat, found the hard way.** ONNX Runtime's CPU provider is
bit-reproducible at a *fixed* thread count, but under CPU contention the
reduction order shifts and — because this footage sits exactly on the model's
decision boundary in the chair region — whole chair regions flip. A first pass
run under load gave chair-leak numbers ~2× lower than the truth. **Every number
in this document was regenerated with `intra_op_num_threads=8` on an otherwise
idle machine, and verified bit-identical across three fresh sessions.** That the
result is knife-edge sensitive is itself a finding: it is the same instability
that makes the raw matte flicker frame to frame.

---

## 3. Model ranking

Eight candidates were actually run: the shipped baseline, four BiRefNet/ISNet-class
single-image models via `rembg` 2.0.81, both Robust Video Matting variants,
plus MODNet and ormbg pulled directly as ONNX.

### 3a. Raw matte, no post-processing

| # | model | chair leak % | subject loss % | haze % | **defect** | ms/frame |
|---|---|---|---|---|---|---|
| 1 | `bria-rmbg` | 0.109 | 0.196 | 0.529 | **1.099** | 5340 |
| 2 | `birefnet-general` | 0.067 | 0.236 | 0.624 | **1.240** | 6479 |
| 3 | `birefnet-portrait` | 0.027 | 0.545 | 0.794 | **1.763** | 5485 |
| 4 | `rvm_mobilenetv3` | 0.836 | 0.202 | 1.294 | **2.978** | **21** |
| 5 | `u2net_human_seg` *(shipped)* | 2.000 | 0.117 | 1.013 | **3.636** | 484 |
| 6 | `modnet` | 1.096 | 0.273 | 1.635 | **3.820** | 95 |
| 7 | `isnet-general-use` | 0.202 | 0.390 | 2.384 | **4.168** | 857 |
| 8 | `ormbg` | 0.745 | **25.708** | 18.198 | **53.749** | 1196 |

`rvm_resnet50` tracked `rvm_mobilenetv3` closely and slightly worse on every
axis (49 ms/frame); `birefnet-massive` was visibly the worst of the BiRefNets
(heavy milky alpha across the torso) and was dropped after the first pass.

### 3b. After the post stack — **this is the ranking that matters**

| # | model | chair leak % | subject loss % | haze % | **defect** | Δ rank |
|---|---|---|---|---|---|---|
| **1** | **`birefnet-general`** | **0.056** | **0.017** | **0.060** | **0.163** | +1 |
| 2 | `bria-rmbg` | 0.100 | 0.034 | 0.051 | 0.210 | −1 |
| 3 | `birefnet-portrait` | 0.004 | 0.366 | 0.070 | 0.475 | — |
| 4 | `isnet-general-use` | **0.010** | 0.085 | 0.363 | 0.639 | **+3** |
| 5 | `rvm_mobilenetv3` | 0.808 | 0.104 | 0.109 | 1.076 | −1 |
| 6 | `modnet` | 1.074 | 0.011 | 0.135 | 1.287 | — |
| 7 | `u2net_human_seg` *(shipped)* | 2.006 | 0.004 | 0.114 | 2.181 | −2 |
| 8 | `ormbg` | 0.467 | 24.329 | 1.545 | 27.114 | — |

**The ranking rearranges, and the winner flips.** `bria-rmbg` leads on the raw
matte purely because it emits the least haze — and haze is exactly what one
S-curve removes for free. `isnet-general-use` goes from **last to 4th**, because
its entire problem was haze too. Once everything is post-processed,
`birefnet-general` wins on chair leak *and* subject loss simultaneously.

> **Rank models on the post-processed result, never on the raw alpha.**
> Otherwise you pick whichever model is already best at the problem you were
> about to solve for free, and overlook the one that is best at the problem you
> cannot solve at all.

Note row 7: the baseline's chair leak is **2.000% → 2.006%** across the entire
post stack. Post-processing cannot rescue a wrong shape.

### 3c. ormbg — the clearest proof of the black-on-black thesis

`ormbg` is an *open, human-specialised* background remover, so on paper it should
be ideal. It is the worst result in the field by a factor of 25, and its failure
is diagnostic rather than random: **it drops the entire black t-shirt** (subject
loss 25.7% of the frame) while *keeping* the sunflowers and the plushies on the
shelf behind him. Given a black garment under soft frontal light it does not
merely mis-cut the boundary — it declines to believe the torso is a person at
all. Preprocessing follows the author's official recipe exactly
(`(x/255 − 0.5) / 1.0`, bilinear to 1024², min-max normalised output), so this
is the model's real behaviour, not a harness bug. See
`cmp/sheet_scene_ormbg.png`.

### 3d. Why RVM lost — the counterintuitive result

Robust Video Matting is the model *designed* for this job: recurrent, temporally
aware, built for video person matting. It came 4th.

- **Its temporal advantage is real but tiny.** On the same 100-frame turnaround
  window (frames 760–859, measured on the bake-off's 1080x1920 crop where both
  models had full-sequence alpha): RVM churn **0.516%** vs single-image BiRefNet
  **0.571%** — only 10% steadier (p95 1.32% vs 1.77%, 25% steadier in the tail).
  A 3-frame temporal median on the single-image output closes that gap for free.
- **Its failure mode is the ugly one.** RVM does not confidently keep the chair,
  it goes *uncertain* — 1.294% haze, the second-worst in the field. Over a
  bright scene that is a grey veil across his ear and jaw. It also renders the
  black t-shirt semi-transparent, so the background bleeds through his torso.
- **Its chair leak is 15× the winner's** (0.836% vs 0.056%).

RVM runs at **21 ms/frame vs 6479** — 300× faster, whole clip in 28 seconds.
If throughput ever matters more than the chair, it is the fallback. For this
footage it is not good enough.

---

## 4. Recommended pipeline for BLACK-ON-BLACK footage

```
1  DECIMATE     drop n mod 6 == 3        -> native 25fps            (Global Law 6)
2  MODEL        rembg birefnet-general, CPUExecutionProvider,
                intra_op_num_threads=8   -> raw alpha, ffv1 gray (lossless)
3  HAZE KILL    smoothstep S-curve, lo=0.35 hi=0.68                 1.240 -> 0.252
4  KEEP LARGEST largest connected component + interior hole fill    0.252 -> 0.163
5  TEMPORAL     median over a 3-frame window (median, not mean)
6  FEATHER      Gaussian sigma 0.6.  NO inward erosion.
7  COMPOSITE    cream #FFFDF9 die-cut rim, dilate 7px, subject on top
```

**Why each step, with the number it bought** (winner model, canonical plate):

| step | chair leak % | subject loss % | haze % | defect |
|---|---|---|---|---|
| A raw | 0.067 | 0.236 | 0.624 | 1.240 |
| B + haze kill | 0.057 | 0.015 | 0.119 | **0.252** |
| C + largest + holes | 0.056 | 0.017 | 0.060 | **0.163** |
| D + erode 2px | 0.087 | 0.429 | 0.667 | 1.516 ❌ |

### The erosion finding — 46:1 against

The lab's previous practice was a 2px inward erosion "to pull the cut inside the
subject". Measured on the winner across a 4×3 sweep of erosion radius × feather
sigma:

| erode | feather | chair leak % | subject loss % | defect |
|---|---|---|---|---|
| **0** | **0** | 0.0560 | 0.0172 | **0.1631** |
| 1 | 0 | 0.0518 | 0.1896 | 0.3313 |
| 2 | 0 | 0.0471 | 0.4298 | 0.5673 |
| 3 | 0 | 0.0437 | 0.6189 | 0.7529 |
| 0 | 0.6 | 0.0594 | 0.0500 | 0.7042 |
| 2 | 1.2 | 0.0476 | 0.4353 | 1.5012 |

Going from erode 0 to erode 2 saves **0.0089 pp** of chair and costs
**0.4126 pp** of him — a **46:1 losing trade**. Visual check at 4× zoom on the cap/ear edge
against both a bright and a dark backdrop confirms it: **there is no background
fringe to erode away**, because the haze-kill step already forced every edge
pixel to commit. Erosion at 2px visibly eats the ear.

**Use erode 0, feather 0.6.** The feather is a sub-pixel AA ramp only; the
metric over-penalises it because it cannot distinguish deliberate anti-aliasing
from chair haze.

### Bridge severing — tested, does not work

Where the chair is *connected* to his shoulder, the largest-component filter is
powerless. A morphological opening (radius 9 and 13) to sever the bridge,
followed by bounded regrowth into the original mask, was implemented and
measured: **chair leak identical to 4 decimal places at both radii.** The
residual chair is fused to his shoulder across a bridge thicker than 26px. This
is not a thin bridge that morphology can cut — it is a genuine merge.

### The cream die-cut rim — it does the opposite of what was assumed

The lab's note says the rim "hides edge sins by design". Tested over a dark
backdrop, that is only half true:

- It **hides fringe sins** — halo, semi-transparency, aliasing — completely, and
  it solves the real problem that a man in a black shirt on a dark scene simply
  disappears. On dark backgrounds the rim is not decoration, it is what makes
  the format legible.
- It **amplifies shape sins.** The rim traces the silhouette, so the residual
  chair wedge at his left shoulder in f79 becomes a visible kink in a clean
  cream outline — more noticeable than it was without the rim.

So the rim is not a substitute for a good matte. It buys legibility, not
forgiveness.

---

## 5. What filming changes would buy — measured, not asserted

The set change cannot be re-shot, so it was simulated: the pixels the panel
agrees are background **and** are dark (i.e. exactly the chair) were modified,
everything else left untouched, and the winning model re-run.

| setup | chair leak % | vs as-shot |
|---|---|---|
| **A** as-shot (black chair) | 0.0673 | — |
| **B** chair lifted to mid-grey | **0.0083** | **8× less chair** |
| **C** chair gone, plain wall behind | 0.0236 | 2.9× less |

**Ranked recommendations for future recordings:**

1. **Get the chair headrest out of black.** A light throw, a towel, a grey
   cushion cover over the headrest — anything that lifts it 2+ stops off the
   shirt — removes ~88% of the residual leak. This is the highest
   value-per-effort change by a wide margin, and it costs nothing.
2. **Or get the chair out of frame** — sit forward, or drop the seat so the
   headrest falls below the shoulder line. Slightly less effective than (B) in
   the simulation only because the replacement wall patch is synthetic; in
   reality this is at least as good.
3. **Don't wear black on the days you want cutouts.** Any mid-tone top gives the
   model a luminance edge to find at the shoulder, which is where the fused
   bridge forms.
4. **Record at 30 or 60fps in OBS** (already Global Law 6). Unrelated to matting
   but it removes the decimation step and the judder entirely.
5. Separation light on the shoulders would be the studio answer, but (1) alone
   gets most of the win for zero setup.

Not required: a green screen. The winner already handles hair, the cap brim and
the ear at full resolution; the *only* thing that beats it is separating the
chair from the shirt in luminance.

---

## 6. Honest ceiling

**What is fixed.** The chair is no longer part of him. The silhouette is a man
with a cap and shoulders, not a man in a hood. Hair, cap brim, ear and jaw edges
are clean at full resolution on all five failure frames, on both bright and dark
backdrops. Chair leak is down 36× from the shipped baseline.

**What is not, and will not be, fixed in software.** On the highest-motion
turnarounds a **small chair wedge remains fused to the shoulder** — visible in
f79 (left) and f1225 (right) in `HERO_before_after.png`. It survives every
filter tried because it is a genuine merge, not a fragment: same luminance, same
texture, contiguous, and thicker than any structuring element that would not
also destroy his shoulder. The old `cutout_chair_mask.py` static geometric
window can still shave it, at the cost of being re-measured for every new
framing — brittle, and not recommended as a default.

**Residual flicker.** The winner is a single-image model, so the silhouette
still breathes slightly frame to frame (churn ~0.57% before temporal median).
The 3-frame median removes the visible part; a viewer will not see it at the
avatar sizes this format uses, but at full-bleed it would show.

**Cost.** 6.5 s/frame, ~2.4 hours for a 54-second clip on this machine, CPU
only. CoreML compilation of the 973 MB ONNX graph stalled past 8 minutes and was
abandoned; thread tuning gave nothing. If a clip must turn around fast,
`rvm_mobilenetv3` does it in 28 seconds at 15× the chair leak.

**Bottom line for Miguel:** this footage is now usable for the cutout format,
and v1/v2 (which he liked) will look materially cleaner. But black-chair-behind-
black-shirt will always cost a residual wedge at hard turnarounds. Thirty
seconds with a light-coloured throw over the headrest is worth more than any
model in this bake-off.

---

## 7. Files

```
_shared/matte_best.webm            FINAL clean cutout, VP9+alpha, 1080x900 25fps 54.16s
_shared/matte_best_rim.webm        same + cream #FFFDF9 die-cut rim baked in
_shared/MATTE.md                   this document

_shared/matte_bakeoff/
  mb_lib.py           shared helpers, scene mocks, metrics
  mb_pick_frames.py   failure-zone frame selection by head-motion energy
  mb_bake2.py         bake-off on any plate, geometry-relative bands
  mb_leak.py          consensus-based chair-leak / subject-loss scoring
  mb_seq.py           single-image model -> lossless gray alpha video
  mb_rvm.py           Robust Video Matting runner (MPS)
  mb_temporal.py      churn / edge-jitter flicker metrics
  mb_post.py          the rescue stack
  mb_comboscore.py    per-step scoring + bridge severing
  mb_filming.py       simulated set changes
  mb_render.py        final VP9+alpha render
  cmp/HERO_before_after.png    the headline proof sheet
  cmp/sheet_*_canon*.png       per-model contact sheets (alpha / checker / bright scene)
  cmp/combo_*.png              rescue-stack progression, bright and dark
  cmp/edge_sweep.png           erosion/feather at 4x zoom
  select/*.json                every number in this document
```

### Reproduce

```bash
cd format_lab/_shared/matte_bakeoff
V=./venv/bin/python

# 1. bake-off on the canonical plate (idle machine, pinned threads)
$V mb_bake2.py --srcpath src/canon_wide_25.mp4 --tag canon2 --threads 8 \
    --rvm rvm_mobilenetv3=alpha/rvm_mbv3_canon.mkv
$V mb_leak.py --adir alpha/frames_canon2 --srcpath src/canon_wide_25.mp4 \
    --models u2net_human_seg,isnet-general-use,birefnet-general,birefnet-portrait,bria-rmbg,rvm_mobilenetv3 \
    --out select/leak_canon2.json

# 2. winning model over the full clip  (~2.4 h)
$V mb_seq.py --model birefnet-general --src src/canon_wide_25.mp4 \
    --out alpha/birefgen_canon_full.mkv --providers cpu --threads 8

# 3. post stack + final render
$V mb_render.py --alpha alpha/birefgen_canon_full.mkv --src src/canon_wide_25.mp4 \
    --out ../matte_best.webm --rim-out ../matte_best_rim.webm \
    --temporal 3 --feather 0.6 --rim-px 7
```

Environment: `matte_bakeoff/venv` (rembg 2.0.81, onnxruntime 1.29.0, torch 2.13.0,
opencv 5.0.0). Model weights cache to `~/.u2net/` and `~/.rembg/models/`.
