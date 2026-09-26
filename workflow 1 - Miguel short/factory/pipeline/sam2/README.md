# SAM2 — the factory's tracked matte

*Promoted out of the format lab (archived on Drive under Testing & Experiments) on 2026-09-01, when the lab closed and Miguel
approved all seven definitive videos.  The lab write-up
(`references/laws/SAM2.md`, four passes and ~1,650 lines) is still the
evidence; this directory is the operating manual and the code that runs.*

The **cutout** format needs Miguel cut out of his chair with a cream die-cut rim
around him. This is how that matte is made. Nothing else in the factory needs
it — the other five approved formats (classic split, facesplit, takeover,
artifact spine, whiteboard) never touch this lane.

---

## The one-paragraph version

Hand a plate and a frame-0 mask to a deployed Modal function, get back a lossless
alpha, run it through a frozen post stack, and you have a matte whose trim does
not shimmer. **~7 minutes and ~$0.17 per 54-second video.** The model is SAM 2,
which is a *video* segmenter: it carries a memory bank and *propagates* a
decision made once, instead of re-deciding the silhouette from scratch 1,354
times. That single change is what fixed the flicker Morgane and Miguel could both
see, and it is why the old spatial chair-exclusion mask — which was quietly
amputating his hand every time he raised it — could be deleted instead of tuned.

---

## Files

| file | what |
|---|---|
| `modal_app.py` | **the deployed app** `shorts-factory-sam2`. `track` / `track_h100` (GPU, self-checking and self-healing), **`ship_remote`** (CPU-only: the post stack, the three VP9 layers and both gates — see §"The ship lane"), `check` (CPU, re-sweep a finished alpha for a tenth of a cent) and `probe_tools` (what the ship path will actually run). |
| `track.py` | local driver: packs a plate + prompts, calls the deployed function, writes the alpha and the measured cost |
| `plate.py` | per-session plate derivation — `measure` then `build` |
| `prompt0.py` | the frame-0 mask prompt: BiRefNet silhouette minus the headrest |
| `ship.py` | the post stack + the cream rim → the shipped matte set (v5: cut / rim / alpha; see §4) |
| `post.py` | the frozen spatial + polish + rim primitives, vendored so nothing imports the lab |
| `protrusion.py` | **the second leak detector**: a lifted, persistent, plate-dark run above the shoulder line. Runs inside `ship.py` on every session; see §"The protrusion gate". |
| `outline.py` | **the third furniture detector** (LAW 48): a silhouette edge that runs straight for 40+ rows, and plate-dark pixels the mask kept beside his jaw. Runs inside `ship.py` on every session, on the ALPHA, before the encode; see §"The outline gate". |
| `bolsterfix.py` | the manual heal, for furniture the automatic one under-cut: same `heal_frame`, window from `protrusion.scan()` |
| `wingfix.py` | the manual heal for a headrest WING beside the head, which has no shoulder line under it and which `bolsterfix` therefore cannot touch. `prompt0`'s own wing cut, applied to every corrective keyframe; see §"ROUND 3". |
| `contain.py` | IoU containment: did this change stay in its lane? |
| `stability.py` | the four flicker instruments |
| `frame0_sheet.py` | the 2× before/after picture that goes with `stability --frame0` |
| `sessions/` | one directory per session: plate, the display plate, prompts, alpha, the matte set, run records |
| `work/` | scratch, including this promotion's own verification run |

The deployed source is mirrored at
`projects/personal/infra/modal/apps/shorts-factory-sam2/modal_app.py` per that
repo's convention, and the app is in its registry.

---

## The standing decisions

Two of them, both Miguel's, both 2026-08-31, both load-bearing.

### STANDING DECISION — the compute path

> **Two deployed lanes since 2026-09-03: `track` (A10, every number below) and `track_h100` (same body, H100; `track.py --gpu h100`, or `gpu: "h100"` on the intake row). Run 11 is the A/B.**
>
> **Modal A10G · fp32 · `sam2.1_hiera_base_plus` · chunk 350 / overlap 8 ·
> v3 post stack + cream rim.** ~7 min and ~$0.17 per 54 s video.

- **MPS is dead.** Not slow — *wrong*. `torch.backends.mps.is_available()`
  returns True, the model runs without error, and it returns noise: the frame-0
  probe on MPS produced a salt-and-pepper mask over the entire frame, area
  278,160 px scattered edge to edge. Nothing warns you. Later, on a re-test, it
  was also only 1.28× CPU and made the machine unusable — killed at 44 %.
- **CPU works and is not the answer.** 1,354 frames in 27-33 minutes at
  ~1,200-1,470 ms/frame, ~310 % CPU, 6.4 GB resident. Fine for a lab, not fine
  for a nightly factory run, and it occupies the machine.
- **`sam2.1_hiera_large` was tested and rejected**, on identical prompts: $0.24,
  1.44× slower, statistically a wash, marginally *worse* on the deciding flicker
  instrument. Miguel watched the A/B: *"I don't really see a + to using the large
  one."* It is not in the deployed image at all.
- **bf16 is 3× faster ($0.058/video) and has a measurably different contour.**
  Reachable via `--dtype bf16`, reserved for a possible bulk back-catalogue job,
  and only after the full gate chain and Miguel's eyes.

### STANDING RULE — FRAME 0

> **A frame-0 prompt may never be a frame that ships.**

SAM2 **re-segments** a prompted frame from the prompt it is handed. So frame 0
arrives as a from-scratch segmentation while every other frame in the run is a
memory-conditioned propagation — and it lands *rougher than its own neighbours*,
on the one frame that decides whether anyone watches. Measured on the last matte
this bit: frame 0's cap-crown roughness was **1st of 8** in its own opening,
1.23× the mean; on the raw track its curvature was 1.385 against 0.545-0.589 for
frames 2-5, **2.4× rougher than its neighbours**.

It bites whether the prompt is points *or* a mask, and the anomaly does not have
to be on the same edge twice: one plate's was the right edge, the next one's was
the cap crown and the left. **Point the instrument at the whole silhouette, not
at whichever edge failed last time.**

Three parts, and which one does the work:

1. **THE WARM-UP LAP — this is the fix.** Chunk 0's frame list is
   `[f0] + [f15, f14 … f1] + [f0, f1, f2 …]`; the prompt lands on local index 0,
   which is a **copy of frame 0 that is thrown away**, and emission starts at
   local index 16. The real frame 0 then arrives as a propagation with a
   16-frame memory bank behind it, exactly like frame 300. Cost: 16 frames,
   1.2 % of a 1,354-frame run. `--warm 15` is the shipped value and the default.
2. **MIRRORED PAD on the temporal median** (`ship.py`, not here). Replicate
   padding made output 0's 3-frame window `[f0, f0, f1]`, and a binary median
   with a duplicated vote *is* that vote — frame 0 was the only frame in the
   video the smoother never touched. Mirroring makes it `[f1, f0, f1]`.
   Frame-0 right-edge curvature: replicate **0.794**, mirror **0.483**.
3. **MASK PROMPTS — right in principle, MEASURE BEFORE ADOPTING.** A
   BiRefNet-general silhouette is the sibling ports' frame-0 prompt and remains
   the default, but it seeds the memory bank for the *entire* run. On one plate
   it could not be adopted: it was a strict superset of the tracked mask by
   +30,993 px, ~10,000 px of which was a uniform 2-3 px fringe around the whole
   silhouette that no measurement could remove. Tracked end to end that fringe
   survived as a permanent **+2.3 % silhouette**, and the cap top rose 1 px
   against a caption-pill clearance whose margin was 0.5 px. A new matte, not a
   fix. `prompt0.py --against` runs that diff for you.

**So: prompt frame 0 with a mask, OR give the prompted frame a warm-up lap so it
never ships.** With the lap in place the prompt frame is discarded anyway, which
is what makes the lap the safer of the two.

---

## The recipe, end to end

```bash
V=~/Documents/Workspace/.venv/bin/python
cd projects/personal/content/shorts-factory/pipeline/sam2
```

### 1. Derive the plate — measured on THIS session's master, always

```bash
$V plate.py measure --src /path/to/cuts/<session>/master.mp4 --out sessions/<session>
# read measure.json, sanity-check the kept duplicates, then:
$V plate.py build   --src /path/to/cuts/<session>/master.mp4 --out sessions/<session>
```

**Nothing about the plate may be inherited.** A previous session's crop window
belongs to a different day, a different chair and a different distance to the
lens. The invariant that ports is **head height**, not the rectangle:
`FRAMING.md` fixes the cutout plate at **496 px of head on the 1080×1920
delivery canvas** (head_frac 0.259), and every gutter, lane width and clearance
the approved chassis is guarded with is a function of that number. `plate.py`
solves `crop_w = 1080 / (496 / head_h_measured)`, rounds to an even 1.2:1 window,
centres it on the measured face and **bottom-plants** it — which is what makes
his chest run off the plate the way the format needs, and why `border_bleed`
exists downstream.

`measure` also does the **de-conform** (Global Law 6): OBS conformed a 25 fps
capture into a 30 fps container by duplicating one frame in six. A 160×90 gray
frame-diff separates duplicates from real frames by orders of magnitude — every
duplicate under 0.08 mean |dY| against a 20th percentile of ~0.41 for the rest,
a 5× gap — so the duplicate *set* is a measurement, not a guess. Dropping all of
them runs slightly short of true duration, so a handful are **kept on take
splices**, where a held frame is invisible, holding |drift| under half a frame.
`plate.py` proposes them; **look at them before building.**

**THE DE-CONFORM IS NOT ALWAYS THERE — run 9 (2026-09-01) captures are 25 fps
NATIVE.** Measured on `2026-09-01 13-55-22`: `r_frame_rate` 25/1, and a 500-frame
cadence scan found `dup_count` **0**, `dup_frac` **0.0** — against run 8's 167-295
dropped frames per session. OBS was not conforming on this batch, so there is no
one-in-six duplicate and nothing to drop. That is a *cleaner* input, not a
problem, but it used to **crash the build**: `drop_expr([])` is the empty string,
so the `vf` came out as `select='not()'` and ffmpeg died with `Undefined constant
or missing '(' in ')'`. Fixed 2026-09-01 — the `select` clause is now emitted
only when the de-conform actually removes frames, and `setpts`/`crop`/`scale` are
unchanged, so exactly one `scale=W:H` still survives for
`ship.py::build_display_plate` to re-target. **A `plate.json` whose `ffmpeg_vf`
has no `select=` is correct for a native-25 capture**, and the display plate cuts
from it normally.

### 2. Build the frame-0 prompt

```bash
# stage 1 needs rembg + the BiRefNet weights, which live in the bake-off venv
.../pipeline/prep/.venv-birefnet/bin/python \
    prompt0.py birefnet --session sessions/<session>

# stage 2: cut the headrest out, using the PLATE's own luma
$V prompt0.py cut --session sessions/<session> \
    --wing-right 718 --wing-right-rows 400,620 \
    --wing-left  352 --wing-left-rows  400,520 \
    --against sessions/<previous>/alpha_v1.mkv
```

The wing columns and rows are **measured on this frame**, at zoom with a
coordinate grid, not guessed. The cut is dark-only (a bright jaw can never be
removed), column-bounded (the black t-shirt below the wings is never touched)
and row-bounded to the band the wings occupy. **Do not widen a band
symmetrically for its own sake** — on one plate, widening the left band to match
the right's rows would have reached y 580-600, where the mask's left edge is his
*shoulder* coming into frame, and amputated it.

Corrective keyframes for later frames (the black-cap-against-dark-chair bands)
go in the same `prompts/` directory as `kf_%05d.png`. They are the lab's
`sam2_capprompt.py` / `sam2_leftprompt.py` technique: take the *previous* track's
mask at that frame and re-cut one band to an edge measured off the plate. That
tooling stayed in the lab, because it is per-plate regime detection that needs
re-deriving for a different chair, a lighter cap or a different key light — see
`_shared/SAM2.md` §v2.3 and §v3.4 before rebuilding it.

### 3. Track

```bash
# the cents-priced probe first — the warm-up lap plus 40 frames
$V track.py --session sessions/<session> --plate sessions/<session>/plate_wide_25.mp4 \
    --prompts sessions/<session>/prompts --tag probe --limit 40

# then the whole take
$V track.py --session sessions/<session> --plate sessions/<session>/plate_wide_25.mp4 \
    --prompts sessions/<session>/prompts --tag v1
```

`track.py` hydrates the **deployed** function by name. It does not import
`modal_app.py`, does not `modal run`, and cannot accidentally deploy a local
edit. Redeploy deliberately: `modal deploy modal_app.py`.

**Chunking is not a compromise.** The video predictor pre-allocates
`N × 3 × 1024 × 1024` float32 — 17 GB for a full take — so the clip is walked in
chunks of 350 with an 8-frame overlap, and chunk *k+1* is conditioned with
`add_new_mask` on the mask chunk *k* produced for that exact frame. Those 8
frames are decided **twice**, and their disagreement is the seam's error bar. It
is reported in every run record; the lab's ran 0.9967-0.9995, improving across a
take as the memory bank warms.

**The track checks itself and, if it has to, fixes itself.** Every `track` call
ends with a frozen-column sweep over its own alpha and returns a verdict; if the
verdict is `furniture` it derives corrective keyframes, re-propagates inside the
same container and sweeps again. You do not run anything for this and there is
no flag to remember — see **The leak check** below for what the verdict means
and what to do when it says `needs_human`.

**THE H100 IS THE DEFAULT LANE** (Miguel, 2026-09-03).  `--gpu` defaults to
`h100`; `--gpu a10` is still there and is what every published lab number was
measured on.  Measured on run 11: **2.73x faster per frame for 1.23x the cost
per frame** (astramath 91.4 ms/frame vs costpertask 249.2 on the A10).  The
alpha is bit-identical H100-to-H100; A10-vs-H100 differs by at most 6/255 on the
soft alpha and **0.999997** agreement after the >127 threshold the post stack
actually uses — a floating-point reduction-order difference, not a shape change.

**THE SEAM FLOOR.**  `iou_min` is whole-frame pixel agreement between the two
chunks that both decided an overlap frame — not an IoU, despite the name.  Since
2026-09-03 a seam below **`SEAM_FLOOR = 0.995`** lands in the record's
`seam_warning` list and `track.py` prints `** BELOW THE FLOOR **` next to it.
It **reports**; it never fails the run, because a seam is a joint in a matte a
human is about to look at, not a reason to throw away a paid GPU run.  The lab
range is 0.9967-0.9995, so the floor sits below every measured seam and above
nothing.

### 3b. Track AND ship, in one dispatch — `--ship`

```bash
$V track.py --session sessions/<session> --plate sessions/<session>/plate_wide_25.mp4 \
    --prompts sessions/<session>/prompts --tag v1 \
    --ship --display 1386x990 \
    --display-plate sessions/<session>/plate_display_1386x990.mp4 \
    --edge-box '1386x990+-153+930' --plate-json sessions/<session>/plate.json
```

The GPU container writes the alpha, the tracked plate and the display plate to
`/vol/<session>/`, commits, **spawns** the CPU-only `ship_remote` and exits — so
the H100 stops billing the moment tracking ends — and `track.py` collects the
second container by call id.  It comes back with the three webm layers, the ship
record and both gate verdicts, and writes them into the session exactly where
`ship.py` would have.  A gate refusal returns `ship.status = "refused"` with the
gate's own sentence, **no layers**, and exit code **3** — the alpha still comes
back, because bolsterfix/wingfix plus a re-track is the remedy and they need it.

The **display plate** is the one piece that cannot move: it is cut from the 4K
master, which never leaves the laptop.  `prep_batch.py` starts it in the
background the moment the plate stage lands (9.6 s on astramath, 14.5 s on
costpertask), so it is off the critical path by the time the track dispatches.

### 4. Ship

```bash
$V ship.py --alpha   sessions/<session>/alpha_v1.mkv \
           --plate   sessions/<session>/plate_wide_25.mp4 \
           --master  <run>/cuts/<id>/master.mp4 \
           --display 1188x990 \
           --out     sessions/<session>/matte_<session>_v5
```

**THREE outputs from one pass (v5, 2026-09-01):**

| file | what it carries | encode |
|---|---|---|
| `matte_<s>_v5_cut.webm` | **his pixels**: the plate re-cut at display size, alpha = the trim | VP9 + alpha, `--crf` (default **10**) |
| `matte_<s>_v5_rim.webm` | **the die-cut shape**: flat cream `#FFFDF9`, alpha = the 7 px *dilated* trim | VP9 + alpha, **lossless** |
| `matte_<s>_v5_alpha.webm` | **the mask alone**: flat mid-gray, alpha = the trim | VP9 + alpha, **lossless** |

The cutout chassis stages `_cut` as `assets/v/matte.webm` and `_rim` as
`assets/v/matte_rim.webm`, stacked at z and z-1. `_alpha` is the measurement
surface (stability, containment, envelope) and is not staged.

#### V5 — why the face left the matte

**The defect (Miguel, 2026-09-01).** Up to v4 this script wrote ONE picture per
variant whose RGB was the plate and whose alpha was the trim, at **VP9 crf 24**.
That put his face through a *second* lossy generation — the plate is already
x264 crf 16 — and the chassis then displayed the 1080x900 result at 1188x990, a
1.10 upscale on top of the compression noise. Measured on `deepresearch` with
the face-HF instrument (a 1.6x face-height crop, std of the σ-2.0 high-pass, at
native resolution):

| stage | encode | face HF |
|---|---|---|
| `plate_wide_25.mp4` | x264 crf 16, 1080x900 | **5.43** |
| `matte_deepresearch_rim.webm` | VP9 crf 24, same pixels | **7.55**  (+39 %) |

**The VP9 pass alone was the +40 % the audit measured.** Nothing about SAM2, the
temporal median, the polish or the rim was implicated — the trim was never the
problem, the *container it rode in* was.

The fix has three parts.

1. **The RGB is re-cut from the master at final display size.** `--master` plus
   the session's `plate.json` re-runs the recorded de-conform + crop with the
   scale target swapped for the chassis's display box and x264 crf 12, writing
   `plate_display_<W>x<H>.mp4`. Only the *scale target* changes, so the frame
   SET is identical to the one the alpha was tracked against — same `select`
   expression, same order, same count — and the two streams stay in lockstep
   frame for frame. One generation from the 4K master, at the size the browser
   actually paints, so nothing upscales at composite time.
2. **The RGB is encoded near-lossless**, `--crf 10`, and everything outside a
   4 px dilation of the trim is flooded flat cream so the encoder spends its
   bits on him and not on a room it is about to discard.
3. **The cream rim leaves the face file.** v4 blended cream into the RGB of the
   same picture that carried his face. v5 emits it as its own layer: flat cream,
   alpha = the *dilated* silhouette. Stacked underneath, it composites to
   exactly the v4 result — cream shows only where the cutout is transparent —
   and a `drop-shadow` on it still reads as one solid body, because its alpha is
   the whole dilated shape and not a ring.

**THE POST STACK STILL RUNS IN PLATE SPACE**, and the finished alphas are
resampled up to the display size afterwards. That ordering is deliberate:
BLEED 8, MORPH_K 2, SIGMA_HI 4.0, FEATHER 0.55 and RIM_PX 7 are frozen values in
1080x900 pixels and `envelope.json` was measured against them. Running the stack
at 1188x990 would silently re-tune all five. Resampling the finished *soft* alpha
up by 1.10 is exactly what the browser did to the v4 matte anyway, so the trim
and the rim keep the weight Miguel approved — and the envelope stays valid, which
is what makes v5 a contained **swap** rather than a rebuild.

**Why the chassis does not mask in the browser.** The alpha-only track exists,
and the obvious design is a high-quality plate `<video>` masked by it at
composite time. Chromium cannot: `mask-image` takes an *image*, not a media
element, and `mask: url(#svg)` over a `<foreignObject>` video is not reliably
rasterised. The only working route is a per-frame `<canvas>` or WebGL pass, which
breaks HyperFrames' deterministic seek-and-capture contract and re-imposes
exactly the per-frame compositing cost cutout Law 3 forbids — the format's own
headline finding is that eight zero-blur drop-shadows on a 1080x1920 `<video>`
took a 4.5 min render to a projected 3 hours. So the multiply happens **here**,
offline, once, near-lossless, and the browser only ever stacks two ordinary
alpha videos. The quality goal is met by deleting the two lossy steps, not by
moving where the multiply happens.

**`--emit legacy`** reproduces the v4 pair (`<stem>.webm` + `<stem>_rim.webm`
with the rim in the RGB) at plate resolution and crf 24, unchanged, so the two
can be diffed.

An envelope re-derivation must NOT be run against a v5 `_cut` or `_rim` file:
those are at display scale, and `cutout5_envelope.py` reports plate-space
pixels. Re-derive from the `_alpha` track with the display scale divided out, or
from an `--emit legacy` pass.

The stack itself is unchanged:

```
0.5 cut → keep-largest + fill-holes → BORDER BLEED (8 px, three edges)
→ 3-frame temporal median, MIRROR-PADDED → 2× polish → cream die-cut rim
```

- **No S-curve.** It existed to kill BiRefNet's translucent-chair haze. SAM2
  emits calibrated logits; the equivalent is a straight sigmoid > 0.5.
- **No spatial exclusion mask.** Deleting it *fixed a bug*: it was subtracting
  1,328-2,372 px of raised hand — 92-100 % skin by the plate's own colour — to
  buy at most 191 px of genuine chair.
- **The temporal median stays.** The plan predicted SAM2 would make it
  unnecessary. It did not: it buys 23 % of the mean and 44 % of the worst case on
  the deciding instrument, and frame-to-frame IoU min 0.820 → 0.963. Its *job*
  changed — it is no longer suppressing gross re-decisions, it is smoothing
  boundary quantisation — but it is not free to drop.
- **The polish is sub-pixel and the parameters are frozen.** UP 2 / SIGMA_HI 4.0
  / MORPH_K 2 / FEATHER 0.55. Upsampling *before* the blur is what makes it
  sub-pixel; INTER_AREA back to 1× turns a half-pixel lattice into a genuine 1 px
  anti-aliased edge instead of a blurred hard one. σ was chosen by eye at 10× on
  the brim notch, the ear and the shoulder: at 2.0 the stairs are legible, at 3.0
  faint, at **4.0 gone with the brim notch still a square corner**, at 5.0 the
  notch bevels, at 6.0 it is a blob. Miguel is bald, so there is no fine organic
  texture on this trim to protect and the smoothing is harder than a haired
  subject would allow.
- **The rim is dilated in 2× space from the smoothed silhouette**, so it inherits
  the curves instead of repeating every jaggy at 7 px offset.

### 5. Prove it

```bash
$V contain.py  --a sessions/<s>/alpha_prev.mkv --b sessions/<s>/alpha_v1.mkv --lo 20
$V stability.py --frame0 --matte sessions/<s>/matte_<s>_rim.webm
$V stability.py --still --plate sessions/<s>/plate_wide_25.mp4 \
      --matte before_rim.webm --matte after_rim.webm
$V frame0_sheet.py --before before_rim.webm --after after_rim.webm --out sheet.png
```

**Containment is the gate for a matte SWAP.** If the body of the video provably
did not move, the envelope does not need re-deriving and the composition
document regenerates byte-identical — that is what makes it a swap rather than a
rebuild. The floor is measured: a CPU-vs-A10G port of an identical prompt gave
mean IoU 0.999997, min 0.999982, **0 frames below 0.999**.

**Hold the previous track's chunk size when proving containment.** Moving the
seams contaminates the measurement with a re-chunking.

---

## The leak check — the pass that heals itself

Every `track` call ends by proving its own alpha has no furniture in it, and
repairs itself once if it does. Nothing to run, nothing to remember; the verdict
is in the run record as `leak_check`.

### What it catches, and why nothing else could

A frame-0 prompt is cut from the plate's own **luma**, and luma cannot tell a
black gaming chair from a black t-shirt. On `grokprice` the wing cut was row-
bounded at 605/608 because that is where his shoulder arrives — and below that
row the seat-back's **side bolsters** flare out, went into the prompt, and
propagated as two black tabs standing on his shoulders for all 1,294 frames.

What resolves it is not luma, it is **time**. The chair is bolted down and he is
not. Per-column top-most ON row, over every frame of the track:

| column | mean top-y | **sd** |
|---|---|---|
| x 780 | 634.0 | 6.94 |
| **x 800** | **605.3** | **0.45** |
| **x 820** | **608.9** | **0.37** |
| x 860 | 684.5 | 4.65 |

**A shoulder that talks for 52 seconds does not hold a column to half a pixel
while the columns either side of it move by 5-7.**

### The verdict is one test, and only one

`clean` or `furniture`, decided **solely** by the frozen-column rule: a column
with `sd <= 1.0` whose flanks 25-70 px away run `sd >= 3.0`, in a run at least
8 columns wide, on the shoulder band (measurable in ≥ 99 % of frames and at
least 250 px below the crown). Everything else in the report is evidence, not
verdict.

It is one test because one test is what has never misfired:

| track | columns at sd ≤ 1.0 | min shoulder sd | verdict |
|---|---|---|---|
| `grokprice` v1, leaking | **39** (x 794-832) | **0.23** | `furniture` |
| `grokprice` v2, manually fixed | 0 | 2.61 | `clean` |
| `grokpublish`, clean | 0 | 4.73 | `clean` |

`grokpublish` is the trap that matters. Its worst head-band frames are his
**raised index finger** entering at the image-left edge (f151-157), which walks
the mask edge 100 px in six frames — sd 74-176 through that band. Real motion is
loud, and the sweep only fires on silence, so the finger cannot trip it.

### The heal

Once — and only once — the sweep has *proven* there is furniture on this plate,
a softer companion pass looks for the rest of it: a robust quadratic is fitted to
each shoulder segment's median profile, and runs that sit **above** that line
while being both quieter than their own segment and plate-dark are the same
piece of furniture seen from the other side. On `grokprice` this recovers the
left bolster (lift 13.1 px, sd ratio 0.69, dark 0.999) and rejects the innocent
candidate at x 105-152 (sd ratio 1.12). It **never runs on a clean track.**

The correction itself is `bolsterfix.py` with the gap and the anchors derived
instead of hand-read: his shoulder line is measurable everywhere the tabs do not
cover it, so the covered span is filled by a robust quadratic through the columns
that **did** measure, and everything above that line, inside the gap, that the
plate says is dark is removed. Corrective keyframes are laid down front-loaded —
every 40 frames to f440, then every 60, and never fewer than 4 in any chunk —
and the whole take is **re-propagated inside the same container**, then swept
again.

**The guard rails, all of them:**

1. **Subtractive only.** The output mask is always a subset of the input. The
   correction can remove chair; it can never invent body.
2. **The luma guard.** Nothing brighter than luma 70 is ever removed. His hands
   cross this band at f80, f416, f512 and f800 and are never dark.
3. **The bracket.** The reconstructed line must sit between the two anchor edges
   that bracket the gap. On the raised-hand frame the raw quadratic predicted
   y = 936 on a 900-row plate; without this it would have started eating black
   t-shirt, luma guard or no luma guard. Out-of-bracket fits are thrown away for
   a straight line between the edges.
4. **The depth cap.** No column may be cut deeper than 2.5× the leak the sweep
   actually measured. This is a removal of a tab of known height, not a licence
   to restructure a silhouette.
5. **Exactly ONE heal iteration.** Never a loop.
6. **A heal that would remove nothing does not run.** If the derived cut is under
   200 px a second propagation is not paid for; the run comes back `needs_human`.

### Reading the verdict

```jsonc
"leak_check": {
  "verdict": "clean",        // clean | furniture
  "healed": true,            // was a corrective re-propagation run
  "needs_human": false,      // the healed track STILL shows frozen columns
  "pre_heal":  { ... },      // the sweep as it found the track
  "post_heal": { ... },      // the sweep after the heal
  "windows":   [ ... ],      // gaps, anchor bands, row windows, measured lift
  "companion": [ ... ],      // every lift candidate, accepted or not, with why
  "heal_report": { ... },    // per keyframe: cut px, luma of the cut, depths
  "shoulder_sd": { "before": 0.23, "after": 2.95 }
}
```

- **`verdict: clean`, `healed: false`** — nothing was wrong, nothing was touched.
- **`verdict: clean`, `healed: true`** — furniture was found and removed. The
  shipped `alpha` is the healed track; the original is kept beside it on the
  volume as `alpha_<tag>_preheal.mkv`, and the derived corrective masks are in
  `/vol/<session>/heal_<tag>/`.
- **`needs_human: true`** — stop and look. **Both** tracks come back in the same
  response (`alpha` healed, `alpha_preheal` original), the reason is in
  `leak_check["reason"]`, and every derived mask is on the volume. Nothing is
  re-run automatically: a second heal on a track the first one could not fix is
  how a pipeline eats a silhouette.

### Auditing a track that already exists

`check` is the same sweep on a CPU container, for a track that was produced
earlier. No GPU, no re-track:

```python
import modal
modal.Function.from_name("shorts-factory-sam2", "check").remote(
    session="grokpublish", tag="v1")          # reads /vol/<session>/alpha_<tag>.mkv
```

Roughly **$0.0003** and about nine seconds for a 1,021-frame take, against ~$0.13
to track it again. Pass `alpha=<bytes>` instead to audit a file that was never on
the volume.

### What it was proved against, 2026-09-01

Both runs on the **deployed** app, against the two tracks whose ground truth
already existed.

**`grokprice`, re-run from its ORIGINAL v1 prompts** — the pass had to find the
bolsters for itself and repair them with no human in the loop:

| | |
|---|---|
| verdict, as found | **`furniture`** — 39 columns at sd ≤ 1.0, x 794-832, sd_mean **0.478** against flank **4.68** |
| companion | left tab x 270-306 **accepted** (lift 13.1, sd ratio 0.69, dark 0.999); x 105-152 **rejected** (sd ratio 1.12) |
| heal windows derived | x **264-312** and x **783-856** — hand-read in the manual fix as 262-321 and 775-857 |
| corrective keyframes | **26**, at 0 40 … 440 500 … 1280 — the manual fix's list, column for column, and ≥ 4 in every chunk (9/7/6/4) |
| the cut | 3,988-6,654 px per keyframe, median 5,201, **max luma of any removed pixel 57** against a guard of 70 |
| fits rejected / columns depth-capped | **0 / 0** |
| verdict after re-propagation | **`clean`** — 0 frozen columns, min shoulder sd 0.23 → **2.28** |
| seams | 0.99896 / 0.99901 / 0.99926 (manual v2: 0.99895 / 0.99902 / 0.99927) |

The shoulder columns the whole argument was about, before and after, measured on
the raw alpha:

| column | before mean / sd | **after mean / sd** |
|---|---|---|
| x 290 | 616.1 / 6.35 | **657.6 / 10.42** |
| **x 800** | 605.3 / **0.45** | **655.8 / 2.92** |
| **x 820** | 608.9 / **0.37** | **667.9 / 3.33** |
| x 230 (control) | 681.2 / 8.50 | 681.3 / 8.49 |
| x 940 (control) | 713.2 / 8.76 | 713.2 / 8.84 |

**Against the manual fix**, whole-track and frame for frame: IoU **0.999465**
mean, **0.997246** min, and only **87** disagreeing pixels per frame outside the
two heal windows — about 0.03 px of contour along a ~2,600 px perimeter. The
derived keyframe masks themselves match the hand-built ones at IoU 0.99902 mean.

**`grokpublish`, the trap** — run through the deployed `check`: **`clean`**, 0
columns at sd ≤ 1.0, min shoulder sd **4.73**. The raised index finger walks that
band by sd 74-176 and the sweep correctly ignores it.

Total Modal spend for both proofs: **$0.2831** ($0.2828 for the self-healing
grokprice run, which pays for two propagations; $0.0003 for the CPU check).

### Turning it off

`leak_check=False` skips the sweep entirely; `leak_heal=False` keeps the verdict
and skips the repair. Both default to on and neither should be a production
setting — they exist so a change to the sweep can be isolated as a single
variable.

---

## The protrusion gate — the second detector, and the one that fires on residue

*Added 2026-09-02, on `kimiram`. Code: `protrusion.py`; the fix it points at:
`bolsterfix.py`. It runs automatically inside `ship.py`.*

### The defect, and why the run record said `clean`

`kimiram`'s shipped cutout carried a hard-edged black tab standing straight out
of his image-right shoulder, roughly 16x14 px at phone scale, from ~10 s to the
end of the video. The rim stroke wrapped neatly around it, so the matte treated
it as part of him. The independent Viewer Test called it a Phone Test fail:
*"cannot be named in three words. It is the first thing the eye finds on a flat
background, and it is crude."*

`run_v1.json` said:

```jsonc
"leak_check": { "verdict": "clean", "healed": true, "needs_human": false,
                "shoulder_sd": { "before": 0.84, "after": 2.18 } }
```

Every word of that is true. **The sweep did not miss the furniture — the HEAL
WINDOW missed most of it.**

| | |
|---|---|
| frozen run, as found | x **818-833** (16 px) |
| heal window, padded | x **812-839** (28 px) |
| the tab, measured on the shipped alpha | x **~789-862** (~74 px) |
| what the heal cut, per keyframe | 576-739 px, max depth 25 |

A heal window is `frozen ∪ accepted companion`. The companion pass exists
precisely to widen a frozen core into the whole bolster, and here it **saw the
tab and threw it away on a rounding margin**:

```
companion candidate  x 795-854   lift_mean 17.8  lift_max 22.9
                     dark_frac 1.000        <- perfectly plate-dark
                     sd_ratio  0.80         <- REJECTED, cfg sd_ratio_max 0.75
```

Then the second sweep ran on the healed track, found nothing frozen — because
the *residue* is not frozen — and stamped `clean`.

### Why quietness was the wrong question

`sd_ratio` asks "is this run quieter than its own shoulder segment?" That is the
frozen test in a softer dress, and it is the right question for `grokprice`,
whose leak was a **seat-back side bolster he was not touching**: bolted down,
silent, sd 0.23.

`kimiram`'s leak is the **chair headrest he is leaning against**. It is
furniture, it is black, it is on screen for 90 % of the take — and it moves a
little, because he moves and the mask boundary where tab meets shoulder moves
with him. Quietness cannot see it. 0.80 against 0.75.

### What `protrusion.py` asks instead

Not *is it quiet* but **is it always there, and is it dark?**

1. Robust quadratic shoulder line per segment (the same `_seg_fit`; furniture is
   rejected as a one-sided outlier, so the surviving line is the shoulder the
   tab interrupts).
2. **LIFT** — a run of columns whose median top-y sits `lift_min` (8 px) above
   that line, mean lift over `lift_mean_min` (10 px), at least 20 px wide.
3. **PERSISTENCE** — in what fraction of frames does the run still stand at
   least `lift_min/2` above the line? Furniture is bolted to the room; a raised
   hand is not. Floor **0.75**.
4. **DARKNESS** — the plate, between the tab's top and the fitted line, is black
   at the same `luma <= 70` the heal is allowed to cut at. Floor **0.85**.
5. **`sd_abs_max` (12 px)** — and it is *not* the companion's test in disguise.
   The companion's is RELATIVE (`sd_in / sd_segment <= 0.75`) and that is what
   lost the tab. This is an ABSOLUTE ceiling, deliberately loose: a chair may
   jiggle 12 px with a man leaning on it and still be a chair. A silhouette edge
   that wanders 30 px is an arm.

### Calibration — measured, not asserted (2026-09-02)

| session | verdict | evidence |
|---|---|---|
| `kimiram` v1 (the defect, already "healed") | **`protrusion`** | x 795-854, w 60, lift 16.9, sd 7.82, persist **0.99**, dark **1.000** |
| `grokprice` v1 (known leaking, ground truth) | **`protrusion`** | x 789-850 (lift 27.6) **and** x 270-305 (lift 13.2) — the manual fix hand-read these as 775-857 and 262-321 |
| `grokpublish` (the approved clean foundation) | **`clean`** | its only candidate, x 300-314, is refused twice: sd **30.6** against a 12 ceiling, width 15 against a 20 floor |
| `perplexityprojects`, `impossibletask`, `deepresearch`, `elevenagents`, `erdos`, `meatwrapper` | `clean` | — |
| `hermesvoicemagic` | `protrusion` | x 77-132, lift 11.9, sd 2.38, persist 1.00, dark 0.94 — an unexamined back-catalogue candidate. **RETRACTED in round 2**: it is his rounded shoulder curving out of frame at 1.18 px/px, not a tab. See below. |
| **`kimiram` v2 (after `bolsterfix`)** | **`clean`** | and the frozen sweep now reports `verdict: clean, healed: FALSE` — there was no furniture left to find |

`grokpublish` is the trap that matters here exactly as it is for the frozen
sweep. Its loudest head-band event is his raised index finger. A finger is
lifted, so `lift` alone would flag it — and it fails the other tests at once:
it wanders, and it is skin, not black. **Real motion is transient, loud and
bright; furniture is permanent, quiet and black.**

### Running it

```bash
$V protrusion.py --alpha sessions/<s>/alpha_v1.mkv \
                 --plate sessions/<s>/plate_wide_25.mp4   # exit 0 clean / 3 found
```

**It also runs inside `ship.py`, on every session, before a frame is encoded**,
and `ship.py` REFUSES to write a matte from an alpha that fails it. That is
deliberate: the whole lesson of the kimiram defect is that `leak_check: clean`
in a run record is not the same thing as a clean file, and a guard is only a
guard if it is called. Override with `--allow-protrusion`, and say why in the
paperwork.

### Fixing what it finds — `bolsterfix.py`

`track`'s heal is automatic and remains the normal path. When it under-cuts,
`bolsterfix.py` re-runs the **same** correction — identical `heal_frame`,
identical guard rails (subtractive only, luma guard 70, the anchor-edge bracket,
the 2.5x depth cap, one iteration) — with the window supplied by
`protrusion.scan()` instead of by `frozen ∪ companion`. Only the window changes,
and the window is the thing that was wrong.

```bash
$V bolsterfix.py --session sessions/kimiram \
                 --alpha sessions/kimiram/alpha_v1.mkv \
                 --plate sessions/kimiram/plate_wide_25.mp4 \
                 --out   sessions/kimiram/prompts_v2
$V track.py --session sessions/kimiram --plate sessions/kimiram/plate_wide_25.mp4 \
            --prompts sessions/kimiram/prompts_v2 --tag v2
```

On `kimiram` that derived **gap x 789-860, 180 anchor columns balanced 90/90,
lift_max 22.9, 27 corrective keyframes**, cutting a median **2,084 px** per
keyframe (against the automatic heal's 576-739) at a **max removed luma of 67**
against the guard of 70. The re-propagation cost **$0.1456** and came back with
seam agreement 0.9984 / 0.9989 / 0.9990 and both detectors clean. Before/after
crops at 12 s / 20 s / 30 s:
`(run 9) review/kimiram_headrest_before_after.png`.

### ROUND 2 — the gate measured the second tab and threw it away

*2026-09-02, hours after the section above was written.*

`bolsterfix` + one re-propagation closed the image-right tab. Both detectors
said `clean`. The independent round-2 Viewer Test came back with **the same
defect on the other shoulder** — image-LEFT, x ~275-304, standing from the first
frame to **28.0 s** of a 47.9 s video and gone after it. 58 % of the take and the
whole hook.

The gate had measured it. It is in both run reports, as a rejected candidate:

```
x 275-304   width 30   lift_mean 13.1   lift_max 16.9
            dark_frac   0.980      <- plate-dark
            persistence 0.604      <- REJECTED, floor 0.75
            sd_in      12.04       <- REJECTED, ceiling 12.0
```

Both rejections are the same arithmetic mistake, and it is not the thresholds:
**every statistic was computed over the whole video.**

| | |
|---|---|
| the tab stands for | 28.0 s of 47.9 s = **0.585 of the take** |
| whole-video persistence | **0.604** — a hair under a floor written for furniture that never leaves |
| whole-video `sd` of those columns | **12.04** — and it does not wander. The top-y sits at ~516 for 28 s and ~533 afterwards; a statistic that spans that step reads a 12 px wander **that no single second of the video contains** |
| the same columns inside a 5 s window | persistence **1.000**, sd **0.86**, lift 13.6 |

Whole-video statistics punish a defect for ENDING. A tab that owns the hook and
stops before the outro is exactly the shape they cannot see, and it is not a
rare shape — he shifts in his chair, and the chair stops touching his shoulder.

### What changed — three things, all measured

**1. THE WINDOW.** Persistence, wander and darkness are now measured inside a
sliding **5 s window, hop 1 s**, and the candidate runs are re-detected per
window off that window's own median. **One qualifying window is a verdict.** The
whole-take window is still evaluated, last, so the gate can only ever be MORE
sensitive than the one that shipped.

**2. `seg_edge_margin` (10 px) — the neck.** A shoulder segment is cut where the
column sd says "transition", i.e. at the neck, and a quadratic cannot follow the
silhouette climbing into it. So the last ~15 columns of every segment read as
`lift` on a perfectly clean matte: measured on kimiram alpha_v2's **clean** half
(28-48 s) the run x 276-319 reports lift 18.7, persistence 1.000, dark 0.896 —
every test passed, and it is his neck. A real tab is bounded by the DATA (the
lift falls back under `lift_min`); a neck run is bounded by the SEGMENT. A run
that comes within 10 columns of either end of its segment is discarded whole,
never trimmed. Clearances: kimiram left tab 15 columns, kimiram right tab 21,
grokprice's two 15 and 262; the neck artefact, 2.

**3. `local_lift_min` (10 px) and `max_slope` (1.0) — the arm.** Every surviving
candidate is re-measured against its own neighbours with `heal_frame`'s own
anchor geometry — a quadratic through the 90 columns either side, offset 3 — and
must still stand 10 px above THAT, on a shoulder shallow enough to be one.

| | segment lift | local lift | local slope | verdict |
|---|---|---|---|---|
| kimiram left tab x 273-304 | 13.6 | **17.2** | **-0.46** | protrusion |
| kimiram right tab x 794-857 | 18.5 | **40.5** | **+0.52** | protrusion |
| grokprice bolster x 784-856 | 40.0 | **50.0** | **+0.46** | protrusion |
| `meatwrapper` x 33-68 | 11.5 | 16.1 | **-1.85** | **silent** |
| `hermesvoicemagic` x 76-129 | 12.4 | 10.5 | **-1.18** | **silent** |

The local re-fit alone is not enough: a quadratic through the neighbours of a
steeply falling edge under-predicts it as badly as the segment fit did, so
`meatwrapper`'s image-left run survives it at 16.1 px. What it cannot survive is
being asked WHERE IT SITS. That silhouette is his upper arm dropping out of the
bottom-left of the plate at **1.85 px per column**, and the leak check's entire
domain is the SHOULDER — the shallow part of the outline furniture can stand on.
The two populations sit either side of 1.0 by a factor of two.

This test RETRACTS a row from the table above: `hermesvoicemagic` x 77-132 was
listed as an unexamined `protrusion`, and the pixels say it is his rounded
shoulder curving out of frame. No tab, nothing for a heal to cut. It was a false
positive and it is now silent.

### Recalibration — the full corpus, 2026-09-02

| session | verdict | evidence |
|---|---|---|
| `kimiram` alpha_v1 | **protrusion x2** | x 273-304 (persist 1.000, sd 0.78, dark 0.984, best window 15-20 s) **and** x 794-857 (persist 1.000, sd 5.99, dark 1.000) — it now finds BOTH tabs in one pass |
| `kimiram` alpha_v2 (the round-2 defect) | **protrusion** | x 273-304, persist **1.000**, sd **0.86**, dark 0.983, local lift 17.2, slope -0.46 |
| `kimiram` alpha_v3 (after the second `bolsterfix`) | **clean** | — |
| `grokprice` alpha_v1 (known leaking, ground truth) | **protrusion** | x 784-856, persist 1.000, dark 1.000, local lift 50.0 |
| `grokprice` alpha_v2 (its manual fix) | `clean` | — |
| `grokpublish` (the approved clean foundation) | `clean` | loudest candidate x 111-140, local lift **2.1**, dark 0.000 — his finger, and it is skin |
| `perplexityprojects` | `clean` | loudest local lift 1.1 |
| `impossibletask`, `deepresearch`, `erdos` | `clean` | no candidate reaches the floor |
| `elevenagents` | `clean` | x 927-990 has local lift 25.7 and slope 0.26 — and persistence **0.52** and dark **0.000**: it is his hand, transient and bright |
| `meatwrapper` | `clean` | x 33-68 refused on slope 1.87 — his arm leaving frame |
| `hermesvoicemagic` | `clean` | x 76-129 refused on slope 1.18 — his rounded shoulder (**retraction**, see above) |

### The two things NOT changed

`LEAK["sd_ratio_max"]` in `modal_app.py` is still 0.75, for the reason given
above. And the thresholds this gate already had — `lift_min` 8, `lift_mean_min`
10, `persist_min` 0.75, `dark_min` 0.85, `sd_abs_max` 12, `min_width` 20 — are
all unchanged. Round 2 changed **what interval they are measured over** and added
two geometry guards that windowing made necessary. Not one number was loosened.

### The second heal — kimiram alpha_v3

```bash
$V bolsterfix.py --session sessions/kimiram --alpha sessions/kimiram/alpha_v2.mkv \
                 --plate sessions/kimiram/plate_wide_25.mp4 --out sessions/kimiram/prompts_v3
$V track.py --session sessions/kimiram --plate sessions/kimiram/plate_wide_25.mp4 \
            --prompts sessions/kimiram/prompts_v3 --tag v3
```

---

### ROUND 3 — the gate had no idea the head band existed

*2026-09-02, on `codexnondev`. Code: `protrusion.WING` + `_ledges()`; the fix it
points at: `wingfix.py`.*

Miguel, reviewing the shipped cutout: *"the RIGHT side of the headrest was not
cut out of the matte — you can see it behind his shoulder."* Both detectors had
passed it. `run_v2.json` says `leak_check: clean, frozen: []`, and re-running
`protrusion.py` on the shipped `alpha_v2.mkv` returns **`clean`, 104 candidates,
0 accepted** — its loudest candidate is x 1107-1212, `dark_frac` 0.40, which is
his hand.

Neither detector was wrong. **Neither was looking at the defect.**

```
the shipped alpha, top-y per column at t = 20 s
    x  860   870   880   890   900   910   920   930   940   950
    y   71    80    91   115   202   216   248   313   504   508
        \___ his cap ___/     \______ the wing ______/  \_ him _/

the sweep's shoulder segments          x 175-522   and   x 943-1317
```

The chair's image-right headrest wing stands **beside his head**, from y ~195
just under the cap down to y ~478 where his own shoulder starts: 60 columns
wide, 280 rows tall, plate luma 2-25, welded to his jaw by a black-on-black
strip. And the segment boundary at **943** lands on the tab's outer edge, which
is not a coincidence: a segment is cut where the column sd says "transition",
and the head-plus-wing is the loudest thing in the frame. The wing is therefore
in the head gap, and the head gap is the one place `scan()`'s main loop never
goes — it iterates `for x0, x1 in segs`.

Widening the segments would not have helped either, because the wing does not
have the shape the whole lane is written for. `lift` is measured against a
fitted SHOULDER LINE; the wing's left neighbours are his HEAD, which is *higher*
than it, so `_local_lift` returns a NEGATIVE lift. There is nothing for it to
stand above.

#### What the wing test asks

Not *does it stand above a shoulder* but **does something hang off the side of
his head that is too wide, too flat, too dark and too still to be his neck?**

Walking outward from a shoulder segment's inner end, a LEDGE is the run of
columns whose window-median top-y sits `clear` (60 px) above that segment's edge
row and `below_crown` (120 px) under the crown — neither head nor shoulder.
**His neck makes one of these on thirteen of the fourteen sessions.** Four tests
separate the two, and each was measured before it was written:

| | the defect | loudest CLEAN value | threshold |
|---|---|---|---|
| **WIDTH** — a neck is a ramp, a wing is a slab | **80** | 33 (`meatwrapper`) | `min_width` **40** |
| **WANDER** — sd of the run's top-y in-window | **3.53** | 28.0 (`perplexityprojects`) | `sd_max` **30** |
| **PITCH** — a neck climbs, a wing hangs (px/col) | **3.06** | 3.59 (`hermesvoicemagic`) | `slope_max` **3.5** |
| **DARKNESS** — the plate between ledge and shoulder | **0.929** | 0.806 (`impossibletask`) | `dark_min` **0.85** |

All four must hold, plus `persist_min` 0.90 inside a 5 s window. **No clean
session fails fewer than three of the four**, and the defect passes all four.
WANDER is the physics: the chair does not move, and his neck does — the same
argument PERSISTENCE makes for the frozen tab, pointed at the other axis.

#### Recalibration — the full corpus, windowed, 2026-09-02

| session | verdict | loudest ledge |
|---|---|---|
| **`codexnondev` alpha_v2 (the defect)** | **`wing`** | x 863-942, **w 80, sd 3.53, slope 3.06, dark 0.929, persist 1.000**, in all 42 windows |
| **`codexnondev` alpha_v3 (after `wingfix`)** | **`clean`** | x 866-885, w 20, sd 45.4 — his neck, and it moves like one now the chair is gone |
| `codexvoice` | `clean` | x 654-677, w 24, sd 33.0, slope 4.79, dark 0.792 |
| `deepresearch` | `clean` | x 336-357, w 22, sd 42.4, slope 6.32, dark 0.712 |
| `deepseekflash` | `clean` | x 358-378, w 21, sd 36.0, slope 4.77, dark 0.773 |
| `elevenagents` | `clean` | x 711-732, w 22, sd 40.0, slope 4.95, dark 0.769 |
| `erdos` | `clean` | x 347-372, w 26, sd 48.9, slope 6.11, dark 0.723 |
| `grokprice` | `clean` | x 329-349, w 21, sd 39.5, slope 7.80, dark 0.762 |
| `grokpublish` | `clean` | x 331-351, w 21, sd 43.9, slope 7.37, dark 0.770 |
| `hermesvoicemagic` | `clean` | x 711-730, w 20, sd 53.3, slope 3.59, dark 0.782 |
| `impossibletask` | `clean` | x 551-570, w 20, sd 45.5, slope 5.75, dark 0.806 |
| `kimiram` | `clean` | x 654-673, w 20, sd 32.5, slope 4.61, dark 0.732 |
| `meatwrapper` | `clean` | x 702-734, w 33, sd 43.1, slope 3.61, dark 0.741 |
| `perplexityprojects` | `clean` | x 537-558, w 22, sd 28.0, slope 4.73, dark 0.726 |
| `sparkchrome` | `clean` | x 348-368, w 21, sd 30.7, slope 5.05, dark 0.764 |

Not one threshold in the shoulder lane was touched. `scan()` now returns
`wing`, `protrusion`, `protrusion+wing` or `clean`; `ship.py` refuses on any of
the three and names which fix to reach for. The CLI exits 3 on anything but
`clean`.

#### Fixing what it finds — `wingfix.py`

`bolsterfix` cannot heal this: every guard rail it inherits from `heal_frame` is
stated against a shoulder line that does not exist here. `wingfix.py` re-uses
`prompt0.cmd_cut`'s rule instead — the one the factory already trusts to take
the wings out of a frame-0 prompt — and applies it to every corrective keyframe:

> inside the wing ROWS, at or beyond the wing's measured inner COLUMN, any mask
> pixel darker than DARK is furniture

dark-only (his ear reads 100-105 where the wing beside it reads 16-18),
column-bounded so the t-shirt is untouched, row-bounded above by the cap and
below by the row his own shoulder arrives at, subtractive, keep-largest, CLOSE,
re-subtract. `--measure` reads the band off the plate; `--dry` renders the
proposed cut so a human looks at it before any GPU is booked, which matters here
because the pixels it must not take are the same colour as the ones it must.

**AND IT NEVER SHOULD HAVE BEEN NEEDED.** `prompt0.py` has had this exact cut
since it was written, and `codexnondev`'s frame-0 prompt was built with it
**disabled**: `kf_report_00000.json` says `wing_right: null`,
`removed_right_px: 0`. The wing rode into the mask prompt, SAM2 seeded its
memory bank with it, and propagated it through all 1,115 frames. `--wing-right`
is not an optional flourish; on a plate with a black chair behind him it is the
prompt.

On `codexnondev` this derived **27 corrective keyframes**, cutting a median
**11,538 px** each (min 10,260, max 13,376) at a max removed luma of **60**
against a guard of 60, for **2.08-2.54 %** of the silhouette. The
re-propagation cost **$0.144** and came back with seam agreement 0.9996 /
0.9996 / 0.9995 and both detectors clean. Before/after crops at 12 s / 20 s /
30 s and a full-take both-shoulder scan:
`(run 9) review/codexnondev_headrest_right.png`.

---

## The outline gate — the third detector, and the one that fires on what the heal LEFT

*Added 2026-09-04, on `reasoninglevel`. Code: `outline.py`; the fix it points at:
`wingfix.py`, driven by `prep_batch`'s auto-repair loop. LAW 48 in
`STANDARD.md`; the repair that became the law:
`references/evidence/hermeskanban_outline_repair/review/repair_hermeskanban_outline.md`.*

### The defect, and why BOTH earlier detectors said clean

`hermeskanban` (run 12) and `reasoninglevel` (run 13) shipped cutouts with
`protrusion: clean` and `EDGE CLIP: CLEAN`, and Miguel rejected both:

> "hermes kanban tiktok has a bad outline compared to the rest, there is a bit
> of chair on my left side and some flicker compared to the rest, minimal but
> there."
>
> "reasoning level cutout has a problem, the chair next to my head (left side
> of the screen) is present as my outline."

**Neither detector was wrong. Neither was looking at the defect.** Everything
in `protrusion.py` is a TOP-Y question — a tab standing above a fitted shoulder
line, or a ledge hanging off the head — and the surviving half of a headrest
WEDGE stands above nothing. `wingfix`'s window is a rectangle; the wedge's inner
edge slants about one column per 3.3 rows; so everything of it to the body side
of the cut column survives, welded to the shoulder where `keep-largest` cannot
drop it, hanging no higher than his own jaw.

What it leaves is measurable in exactly two ways, and they are the repair
record's own two measurements:

1. **THE STRAIGHT EDGE.** While the wedge survives, the silhouette's extreme
   column IS the cut column, for as long as the cut ran. On the rejected
   `hermeskanban` alpha that was ~132 of 164 rows at exactly x 462. A human
   edge is never a straight column.
2. **THE RETAINED DARK PLATE.** The mask is holding pixels whose plate is
   chair-black. A heal that stopped one column short of the object it was
   cutting shows up here and nowhere else.

### What the gate asks, and the band that makes it specific

Per frame, per side, inside the **head band** — the 180 rows ending at the
SHOULDER ARRIVAL (where the silhouette's width reaches 1.35× the head's):

| instrument | measured | approved corpus | rejected | ceiling |
|---|---|---|---|---|
| longest identical-column run, p95 over frames | rows | 33 - 50 | 59 - 132 | **60** |
| share of frames carrying a >= 40-row run | — | 0.018 - 0.264 | 0.466 - 0.993 | **0.40** |
| retained plate-dark (luma <= 60) in a 50-column inward band, p95 | share of band | 0.14 - 0.62 | 0.99 - 1.00 | **0.78** |

**The band is the whole trick.** Above it is his CAP, which is black and whose
side is a genuinely straight vertical edge for 40-107 rows on mattes Miguel
approved. Below it is his T-SHIRT, which is black. Measured over the whole
crown-to-bottom span, instrument 1 reads a p95 of 42-75 rows on the approved
corpus against 46-132 on the rejected ones — **no separation** — and instrument
2 reads 29,000-40,000 px on every matte in the corpus, clean or not, because it
is counting his own clothes. Windowed to the band, both separate cleanly. And
the band is stable to derive, because the plate solve freezes the geometry:
across nine tracked alphas the crown sits at row 13-28, the head is 323-334 px
wide and the shoulder arrival lands at row 466-499.

**Both instruments are needed.** `hermeskanban` v2 — the file Miguel rejected —
is caught by the straight-edge test alone (132 rows) and passes the dark test,
because its surviving wedge is a thin sliver. `hermesdesktop` v1 and `dgxspark`
v1 are caught far more loudly by the dark test. `reasoninglevel` v1 fails both.

### Calibration — measured, not asserted (2026-09-04)

The whole run-12/13 cutout corpus, stride 5, whole take, both sides. Nine
alphas, eighteen sides, **nine of nine verdicts correct**: every matte Miguel
approved and delivered passes, every matte he rejected or that needed a repair
before delivery refuses. The table is in `outline.py`'s docstring.

### Fixing what it finds

`prep_batch`'s auto-repair loop, gate `outline` → `wingfix.py` on the refusing
side, with the window the gate measured: the band's rows (top lifted 20,
**bottom left exactly at the shoulder arrival**, because `wingfix` cuts dark and
his shirt is black), a cut column from the deepest inward retained-dark column
plus 10 px, and `--chunk 40`. Full description and the first live run:
`pipeline/prep/README.md`, §"The outline gate".

The gate reproduces the hand-driven repair independently: on `hermeskanban`'s
refused alpha it measures a cut column of **509**, against the **510** a human
read off `wingfix --measure` and shipped.

### Running it

```bash
$V outline.py --alpha sessions/<s>/alpha_v1.mkv \
              --plate sessions/<s>/plate_wide_25.mp4   # exit 0 clean / 3 found
```

It also runs inside `ship.py` on every session, between the protrusion gate and
the encode, and `ship.py` REFUSES to write a matte from an alpha that fails it.
`--allow-outline` takes a written reason and records it. `--no-outline-gate`
exists for a port with no head band; the two instruments are stated against this
factory's frozen head scale and mean nothing without it.

### The known limit, and it is Miguel's own ruling

LAW 48 says **p95**, so p95 is what refuses, and a sub-second burst is therefore
invisible to it. `hermesdesktop` v2's right side maxes at **8,873 px (0.98 of
the band) on ONE frame at 1.4 s** — the chair splash at the very start of that
take that Miguel saw and explicitly told us not to redo. Every other approved
matte's max is <= 5,671, so a max-based test at ~7,000 would catch it and pass
everything else. It is not built, because it would refuse a file its owner
accepted. `dark_frac_max` is recorded in the `law48` block and never gated.

---

## The end frames are their OWN frame, never a neighbour's (2026-09-04)

A BINARY MEDIAN WITH A DUPLICATED VOTE IS THAT VOTE. `render()`'s temporal
median pads the sequence at both ends, and both padding modes duplicate a
frame — but they duplicate DIFFERENT ones. `replicate`'s window at output 0 is
`[f0, f0, f1]` and resolves to **f0**; `mirror`'s is `[f1, f0, f1]` and resolves
to **f1**. So from 2026-08-31, when mirror became the default, the opening frame
of every matte carried **frame ONE's silhouette over frame ZERO's picture**, and
the tail frame carried the second-to-last's.

Measured on the alphas themselves (`spatial()`, the same primitive `render`
feeds the median), pixels the neighbour's mask adds that the frame's own does
not have:

| matte | frame 0 | last frame |
|---|---|---|
| `dgxspark` alpha_v2 | **7,195 px** | 1,466 px |
| `viberesearch` alpha_v1 | 2,140 px | 1,573 px |
| `reasoninglevel` alpha_v2 | 1,340 px | 2,044 px |
| `hermeskanban` alpha_v4 | 705 px | 97 px |

On `dgxspark` those 7,195 pixels are background revealed inside his hand, which
moves ~100 px in that frame — **on a track SAM2 had got right.** And the
0.483-against-0.794 edge-curvature measurement that bought mirror its default
was never measuring a smoothed frame 0 at all. It was measuring frame 1.

**The fix is independent of `pad`.** `compose(..., is_end=True)` takes the
window's own centre frame and skips the median, which is exactly what a
replicate window resolves to for any window size. `windows()` carries one frame
of lookahead so the LAST output frame can be named in a streaming pass. Only the
two end frames of a take are affected; the interior is byte for byte what it
was, and both `workers` paths get the flag, so the workers-1-equals-workers-12
md5 parity is unchanged.

The ship json records the check under **`end_frame_check`**: `revealed_px` (0 by
construction, recorded anyway, because a check nobody can read is not a check)
and `median_would_add_px` / `median_would_lose_px` — the defect that used to
ship, per end frame.

---

## The instruments, and the wrong metric each one replaced

**`--still` — matte motion without picture motion.** Compute mean |Δluma|
between consecutive plate frames, take the quietest 20 %, and on exactly those
frames measure the XOR area between consecutive masks: how many pixels changed
their mind while the man was still. On a frame where the whole picture moved by
≤ 1.38 luma levels, *his hands did not move either*, so XOR cannot be charged to
legitimate tracking.

> The obvious metric — per-frame area and left/right extent, then diff them —
> ranked the tracked matte **worse**. Every one of its "worst" frames decoded to
> his hands entering or leaving frame. A silhouette that correctly grows by
> 67,697 px when two hands come up is not flickering, it is tracking. And the
> old build's extent trace was *artificially* calm because its exclusion
> rectangle physically clamped the very edge being measured.

**`--bands` — the per-row edge trace.** `--still`'s head band is 410 rows tall
and one number over 410 rows cannot see a 45-row sliver switching on and off. So
trace the leftmost and rightmost ON pixel for every frame and every row, and
measure the |Δ| of a *band's mean row extent* between consecutive still frames.
Band mean rather than per-row max, because the defect is a whole band moving
together and averaging is what separates that from the ±1 px quantisation every
band has.

> **`--scan` before you name bands.** The image-LEFT defect went unfixed for a
> whole pass because the left-hand bands had been chosen to *control* a
> right-hand investigation and were looking 35 rows too low.

**`--frame0` — is frame 0 an outlier against its own opening?** A rank, not an
absolute number, because the claim is about a prompted frame differing from
propagated ones.

**`--trace` — the raw per-frame table.** Reported for completeness and *not* the
verdict. It is contaminated in both directions and it is printed rather than
omitted, because the fair-looking number is not always the flattering one.

**Roughness** (`post.roughness`, and the per-edge variant in `stability`) is
measured **on the alpha, never on a thresholded copy**. The gain is sub-pixel, so
re-quantising before measuring throws away exactly what is being tested — doing
it the wrong way once reported −12.8 % for a change that is unmissable at 10×.
Perimeter was tried first and rejected: an 8-connected staircase and a 45° line
have nearly the same arc length.

---

## What this promotion measured

The lane was verified on 2026-09-01 against the **standing hermesinfinite
matte** — the round-6 DEFINITIVE cutout's own raw track,
`_shared/sam2/alpha/sam2_canon_v4.mkv`.

Same plate, same 24 `capfix_v3` keyframe masks, same chunk 350 / overlap 8, same
`warm=15` lap, fp32 on an A10 — but through the *promoted* code and the
*deployed* app, with the plate handed over as mp4 bytes and exploded to JPEG
inside the container.

| | |
|---|---|
| frames compared | 350 (all of chunk 0, opening included) |
| body IoU mean | **0.999673** |
| body IoU min | **0.999130** |
| **frames below 0.999** | **0** → `CONTAINED` |
| disagreeing px, mean | 126.4 of ~387,000 |
| mean silhouette area delta | **−10.6 px of 387,145** |
| frame 0 | IoU 0.99970, 113 px |
| speed / cost | 340.4 ms/frame, $0.0502 for 350 frames |

The residual (0.99967 against the CPU-vs-GPU port's 0.999997 floor) is the JPEG
re-encode: the lab tarred JPEGs made by macOS ffmpeg, this run made them with the
container's. Pass `--frames-tar` for a bit-exact rerun when that matters.

The **post stack** was then verified the same way. `ship.py` on that alpha,
against the approved `matte_sam2_rim_v4.webm`:

| | |
|---|---|
| rim matte IoU, frames 0-7 | **0.999557** mean, **0.999433** min |
| frame 0, cap crown | 0.596 px vs 0.589 neighbour mean — **1.01×, rank 4 of 8** |
| frame 0, left edge | 0.766 px vs 0.811 — **0.94×, rank 4 of 8** |
| frame 0, right edge | 0.939 px vs 0.904 — 1.04×, rank 3 of 8 |

Frame 0 is **not an outlier on any edge**, which is the whole claim of the
standing rule and reproduces the lab's own v4 result (rank 4th and 7th of 8
there). The warm-up lap and the mirrored pad both survived the promotion.

Total spend for the whole promotion, measured: **$0.063**.

### One finding that contradicts an easy assumption

**A truncated probe is NOT a prefix of the full run.** The first smoke ran 24
frames with the same prompt directory and came back at IoU 0.9929 against the
lab track — 24 of 24 frames below 0.999. That is not drift and not
nondeterminism: with `--limit 24` the chunk only contains keyframe 0, whereas the
real chunk 0 contains keyframes 0, 40, 80, 120, 140, 160, 200, 240, 280 and 320.
**SAM2 attends to every conditioning frame in the chunk regardless of temporal
order**, so a mask at f320 changes the decision at f10. Re-running with
`--limit 350` — one true chunk — landed at 0.99967 and zero frames below the
floor.

So: a `--limit 40` probe is a fine way to buy a **frame-0** answer for cents (it
is what the lab used, and the opening is where the lap does its work), but it may
not be compared frame-for-frame against a full track. **For containment, run a
whole chunk.**

---

## Known limits, carried forward honestly

1. **The corrective keyframes compound.** Each pass seeds its keyframe masks from
   the previous pass's masks with one band rewritten, so an error *outside* the
   rewritten band at a keyframe propagates forward rather than being fixed.
   Three passes now sit on top of one another. The band tables say there was
   nothing to propagate; the dependency is real.
2. **The regime detectors assume this set.** They refuse rows where
   wall→chair→cap is not clean (21-46 usable rows of 47-65 per keyframe) and fit
   the rest. A different chair, a lighter cap or a different key light needs them
   **re-derived, not re-used** — and that tooling deliberately stayed in the lab.
3. **`sam2.1_hiera_large` and bf16 are untested at production quality.** Large
   was A/B'd and rejected; bf16 was measured faster with a different contour and
   has never been through the gate chain.
4. **Not tried, and still the principled version of two fixes:** tracking the
   chair as a **second SAM2 object**, which would make both cap/chair boundaries
   a *competition* between two tracked objects instead of two prompted
   corrections.
5. **The leak check only sees furniture that is FROZEN, and only on a shoulder.**
   A chair that moves with him — a headrest that rocks, anything he leans on —
   has a live column and the sweep will call the track clean. So will a leak that
   sits above the crown or outside the body band. The sweep is a proof of a
   specific failure, not a general-purpose matte grader, and the gate chain
   (`contain`, `--still`, `--frame0`, Gemini QC) is still what says a matte
   ships.
6. **A heal is a deliberate removal, so whole-frame containment will fail it.**
   `contain.py` is built for "the body must not have moved"; when the change IS a
   removal it reports NOT CONTAINED and it is right to. Run it with the heal
   windows masked out and report the share of disagreement inside them —
   `grokprice`'s was 92.8 % inside the windows, and masked IoU 0.9988 mean.

---

## The ship lane — `ship_remote`, and where the matte is made now

*Added 2026-09-03.  Full measurement: `(run 11) review/phase1_remote_ship.md`.*

`ship.py`'s CLI now wraps an importable core, `ship.ship_all(...)`, which runs
the protrusion gate, `render()` and the edge-clip gate in that order and raises
`ShipRefused` (carrying the partial record) on either.  The deployed
`ship_remote` calls exactly that function, so the laptop lane and the Modal lane
are the same code, the same order and the same printed verdicts.

**The GPU never ships.**  The first cut of this ran `ship_all` inside the track
container and it was both slower and dearer: 133 s at 8 cores, **148 s at 32**
(more cores made it worse), with the H100 idling at $0.001097/s throughout —
costpertask's container cost **$0.51** against $0.13 for its track alone.  A GPU
held open for a libvpx encode is the most expensive CPU on Modal.  So the track
spawns `ship_remote` (no GPU, **32 cores**, 24 GiB) and exits.

**Two things make the CPU lane fast enough to be worth it.**

1. `render(workers=N)` composes whole output FRAMES on a thread pool and writes
   them in strict order.  It is a scheduling change, not a maths change, and
   that is proven: workers 1 and workers 12 decode to the same md5 on all three
   layers.  Modal runs 12.
2. `cv2.setNumThreads(1)` around that pool.  OpenCV sizes its own pool from the
   machine's *visible* CPUs (~48-60 on a Modal host), not the cgroup quota, so
   12 frames in flight multiplied the crowd instead of the throughput —
   **154.8 s → 104.8 s** on astramath.  Restored on the way out, because it is a
   library-global and `ship.py` is importable.

**The two LOSSLESS layers are encoded fast, the CUT layer is not touched.**
`-lossless 1` means the decoded pixels are the input pixels whatever the speed,
the tiling or the thread count, so rim and mask get
`-cpu-used 8 -threads 8 -tile-columns 2`.  Proven by decoding: identical md5,
and the files came out **27 % smaller**.  The cut layer is crf 10, i.e. lossy,
and every one of those knobs moves its pixels — its line stays frozen at
`-cpu-used 3`, no `-threads`, no `-tile-columns`.

**THE ENCODER IS PART OF THE MATTE.**  Debian bookworm ships ffmpeg 5.1, and 5.1
converts RGB to YUV on the BT.601 matrix while tagging the file BT.709.  These
three layers are exactly that conversion (`bgra` rawvideo → `yuva420p`), so the
image carries a **static n9.0 build** under `/opt/ffmpeg`, matched to the
laptop's release line, and `ship.py` reaches it through `SHIP_FFMPEG`.
`/opt/ffmpeg` is deliberately **not on PATH**: the JPEG explode and the ffv1
alpha writer on the track path still run Debian's 5.1, exactly as every
published A10 number was measured.  `probe_tools()` reports both builds and
whether the four mounted python files import — run it after any image change.

**What is NOT bit-identical, measured on astramath (bit-identical alpha, so the
ship is the only variable):**

| | |
|---|---|
| rim / mask layer RGB (flat cream, flat gray) | **identical** |
| rim / mask layer ALPHA | 0.999993 agreement, **max 2/255**, ~100 dB |
| cut layer ALPHA | 63.7 dB |
| cut layer RGB (crf 10) | **42.6 dB** |

Two causes, cleanly separated.  The 2/255 on the *lossless* layers can only be
the **OpenCV build** — Linux/x86-64 and macOS/arm64 round the last bit of
`GaussianBlur`/`resize`/`dilate` differently — and it is a sub-pixel feather
rounding, not a shape change: both gates read **identical** numbers off it, every
`edges` sub-metric and every frame-edge window, on both recordings.  The cut
layer's RGB is a different **libvpx build** of the same ffmpeg release line.
Neither can be removed without running macOS libraries on Modal.  The face-detail
gate is unaffected — `cutout_media.py` measures face HF on the **display plate**,
which is still cut here.  `--ship-local` reproduces the old pixels exactly.

**The floor, and it is the encoders.**  `ship_remote` reports its own split:
74 % of the render wall is this thread blocked writing into a full encoder pipe
(astramath 59.4 s of 80.0; costpertask 106.2 of 147.6).  The compose side runs at
~35 fps; the pipeline delivers 8.8.  Modal's vCPU runs libvpx roughly 3x slower
per core than an M5 Pro performance core, and the cut layer's intra-tile row-mt
cannot be widened without changing the matte.

**Which lane to use.**  The `workers` split and the lossless tuning live in the
shared `ship.py`, so the laptop got faster too — astramath 56.6 → **25.2 s**,
costpertask ~120 → **55.9 s**.  For one or two recordings the laptop is now the
faster lane (`prep_batch.py --ship-local`).  Modal wins when the batch is wide,
because N ships get N separate 32-core containers instead of sharing this
machine, and whenever the laptop has to stay free.

| | astramath | costpertask |
|---|---|---|
| ship, laptop (2026-09-03 morning) | 67.3 s | 152.2 s |
| ship, laptop (tuned) | ~29 s | ~60 s |
| ship, `ship_remote` 32 cores | 104.8 s | 197.2 s |
| ship cost, `ship_remote` | $0.0521 | $0.0967 |


## Cost

A10 on-demand, Modal's published rates, billed boot → scaledown:

| | |
|---|---|
| GPU (A10) | $0.000306/s |
| CPU, 4 cores | $0.0000131/s each |
| memory, 16 GiB | $0.00000222/s each |
| **54 s video, 1,354 frames** | **~$0.17**, ~7 min |
| 40-frame probe | ~$0.009 |
| 350-frame chunk | ~$0.05 |
| the leak check on a clean track | **free** — the sweep is one boolean argmax per frame, accumulated as each frame is written, against a 240 ms/frame GPU step |
| a track that heals itself | **~2×**, because the take is propagated twice |
| `check` on an existing alpha, CPU only | **~$0.0003** |
| **H100 lane** (`--gpu h100`, the default since 2026-09-03) | $0.001097/s — **2.73x faster per frame for 1.23x the cost per frame** |
| **`ship_remote`** (CPU only, 32 cores, 24 GiB) | $0.0521 astramath (706 f) / $0.0967 costpertask (1300 f) |
| ship inside the GPU container — **rejected** | $0.25-$0.55 per video, and slower than the laptop.  Never do this. |

Every run record carries its own `measured_cost_usd`, computed the same way the
GPU bench computed its, so the numbers stay comparable with
`gpu_bench/BENCHMARK_REPORT.md`.

---

## Provenance

| this file | came from |
|---|---|
| `modal_app.py` | `_shared/gpu_bench/benchmodal/app/bench_sam2.py` (image, sizing, cost) + `_shared/sam2/frame0fix/track_modal.py` (lap, handoff, seams) |
| `ship.py` | `_shared/sam2/frame0fix/ship.py` = `sam2_ship.py::render_v2` + mirrored pad |
| `post.py` | `_shared/matte_bakeoff/mb_post.py` + `_shared/sam2/sam2_smooth.py` |
| `plate.py` | `cutout_ports/airtable/gen/measure_source.py` + `build_plate.py` + `_shared/measure_head.py` |
| `prompt0.py` | `cutout_ports/airtable/gen/birefnet0.py` + `prompt0.py` |
| `contain.py` | `_shared/sam2/frame0fix/contain.py` |
| `stability.py` | `_shared/sam2/sam2_capband.py` + `sam2_flicker.py` + `sam2_thirds.py` + `sam2_smooth.py` |
| `frame0_sheet.py` | `_shared/sam2/frame0fix/frame0_sheet.py` |

The lab directories stay on disk untouched. They hold the evidence — the
proof sheets, the A/B clips, the per-keyframe measurements — and every number
quoted here is measured there.

---

## The exclusion objects — `exclude=`, and the end of the rectangle era

*Added 2026-09-04.  Test record: `(run 13) review/chair2obj_reasoninglevel_sheet.png`,
`chair2obj_hermesdesktop_sheet.png`, the previews in
`~/Movies/Shorts Factory/Format Lab/cutout/_run13_matte_previews/`, and the
LEARNINGS.md entry of the same date.  This is "Known limits" item 4, done.*

Miguel on the shipped `reasoninglevel` cutout: *"my left shoulder is chopped on a
straight vertical line, and at the end a piece of the headrest arm sits by my
left ear."*  One defect, two symptoms, and neither is SAM2 tracking badly.  SAM2
was given ONE positive prompt and nothing ever said **that black thing beside the
black cap is not him**, so every repair had to be a RECTANGLE cut out of a wedge
that slants a column per 3.3 rows: `wingfix`'s window bottom amputates the
shoulder, its top leaves the arm by the ear.

**SAM2 is a multi-object segmenter.  Now the factory uses that.**

    track.py ... --exclude-box 450,188,566,458 \
                 --exclude-points '490,260,1;492,305,1;502,355,1;508,405,1;600,120,0;560,250,0;480,560,0' \
                 --exclude-dilate 2 --exclude-name 'left headrest wing'

`_track(exclude=...)` takes one dict or a LIST of dicts — `{"box": [x0,y0,x1,y1],
"points": [[x,y,label],...], "dilate": 2, "name": "..."}` — and gives each its own
object id from `EXCL_ID0` (2) upward.  Both objects are prompted on the DISCARDED
warm-lap copy of frame 0, so the STANDING RULE holds for all of them; both are
propagated in the SAME loop, on the same predictor, over the same exploded
frames; and the emitted alpha is

    obj1  AND NOT  (union of the exclusion masks, each dilated `dilate` px)

per frame.  Across a chunk boundary **obj 1 is handed off the SUBTRACTED mask**,
so its memory bank progressively stops carrying the furniture instead of
re-acquiring it every 350 frames; each exclusion object is handed off its own.
The exclusion objects are also written out as one diagnostic ffv1 alpha,
`alpha_<tag>_exclude.mkv` (volume + `--session` dir), because the thing that did
the subtracting has to be watchable, not inferred from what is missing.
`exclude=None` — the default — is byte-identical to every track before it:
`logits[0]`, one object, no dilation, no second memory bank.

**One box and seven clicks beat 80 corrective keyframe masks on every
instrument.**  `reasoninglevel`, chair residue in `x 440..570 / y 190..450`
(mask ∧ plate luma ≤ 60), stride 2 over the whole take:

| | median | p95 | max | frames > 1,000 px |
|---|---|---|---|---|
| v1, rejected by Miguel | 12,339 | 15,764 | 16,895 | 383/383 |
| v2, the shipped `wingfix` repair | 723 | 1,964 | 3,383 | 81/383 |
| **chair as obj 2** | **487** | **925** | **1,051** | **5/383** |

The ear band alone (`y 190..290`, above where the wingfix window began) goes from
a 3,357 px max to 888, and the last 2.6 s of the take — Miguel's "at the end" —
from mean 965 / max 3,357 to mean 224 / max 330.  Edge jitter on the amputated
rows collapses: row 480 from 15.58 px mean / **p95 75** / 28.1 % of frames moving
≥ 5 px to 0.78 / **p95 1** / 0.9 %, row 460 from 4.98 / 27.0 / 14.5 % to
0.98 / 2.0 / 0.7 % — both then BETTER than `costpertask`, the matte Miguel
accepted.  Cap rows and the entire right side are unchanged to the pixel.

**It is cheaper than the repair it replaces.**  Two objects tracked at
117.0 ms/frame against 157.6 for the one-object wingfix re-track (80 keyframe
masks cost more than a second object does): **$0.1156 against $0.1523**, and all
three gates passed on ROUND 0 — no refusal, no `wingfix`, no second GPU run.

**`hermesdesktop`, the second case.**  Obj 2 = the right headrest wing
(`--exclude-box 880,175,972,472`, five positive and three negative clicks).  Its
obj-1 prompt was the session's CURRENT `prompts/kf_00000.png`, which run 13's own
repair had already overwritten with both wings cut — so this measures what the
second object ADDS ON TOP of a shipped repair.  It adds the thing LAW 48's
docstring says it deliberately does not gate: the right-side retained-dark MAX
falls from **0.98 to 0.65**, i.e. the chair splash at the start that Miguel saw
and accepted is gone.  In the shipped `cut` layer the new matte drops a
**12,976 px** blob at 0.24 s, 12,513 at 0.28 s and 12,283 at 7.24 s, and takes
away from HIM a median of 14 px (max 452).  Right-side edge jitter halves at rows
320-440 (2.54 → 0.55 px mean at row 440); the left side and the cap are identical
to the pixel.

### Choosing the prompt — the procedure that worked

1. Extract frame 0 of the plate the track will run on.
2. Print the per-row runs of `luma <= 60` across the suspect columns.  The wedge
   is the run whose extremes move monotonically with the row; his jaw is the
   bright side of it, his shirt is the run that appears below the shoulder
   arrival.
3. Box the wedge only, and stop the box's bottom ABOVE the shoulder arrival.
4. Put the positive clicks at the CENTRE of the dark run, one per ~60 rows.
5. Put negative clicks on his cap, on his cheek at the interface, and — the one
   that matters most — on his SHOULDER below the box, which is what stops the
   exclusion object growing down into his shirt.
6. Render a proof overlay (box + green/red dots over a shadow-boosted frame 0)
   and LOOK at it before spending.  Both prompts here were right first time.

### What is still open

* The dilation is a global `dilate` px.  Where the chair touches his cap the
  boundary is a genuine occlusion and 0 px would be correct; where it touches
  bright skin 2 px is free.  A luma-aware dilation is the obvious next
  refinement, and it is NOT needed for either of these two videos.
* Nothing wires `exclude` into `prompt0.py` or `prep_batch.py` yet, so the
  prompt is chosen by hand per session.  The mechanical part — find the wedge's
  dark runs on frame 0, box them, click the centres — is exactly what
  `prompt0.py`'s wing instrument already measures and abstains on, so that is
  where it belongs.
* Both tests excluded ONE wing.  `exclude` takes a list, so obj 2 = left wing and
  obj 3 = right wing in one call is supported and untested.

### The margin: 2 px against 4 px, measured (2026-09-04)

Miguel asked to see `--exclude-dilate 4` after approving the 2 px outline, because a faint dark
line still reads along his left temple at ~8 s and ~16 s.  Session
`sessions/reasoninglevel_chair2obj_d4`, everything else identical.  **The default stays 2.**

| | left straight p95 / at-line | left dark p95 | jaw sliver rows 300-420 | chair residue y190-450 | frames > 1,000 px | silhouette |
|---|---|---|---|---|---|---|
| margin 2 px | 39 / 5.2 % | 1,973 (22 %) | 0.7 px/frame (max 4) | median 488 / max 1,051 | 11 / 765 | — |
| margin 4 px | 39 / 5.2 % | 1,858 (21 %) | **0.0 px/frame (max 1)** | median 387 / max 979 | **0 / 765** | **−736 px/frame** |

The gates cannot separate them.  4 px does close the last measurable sliver, and it costs a flat
2 px of contour at every chair-contact row (0.0 px at the four no-chair control rows, so the
mechanism is clean) and 736 px/frame of him.

**The dark line he is seeing is not chair.**  Paint every mask pixel within 8 px of the left edge
whose plate luma < 45 and look at f200 and f400: all of them sit in one blob at rows ~185-215,
where his BLACK CAP BRIM meets the wall above the ear.  Rows 220-330 — the ear and temple
contour — carry none, in either run.  Only cutting into his cap would remove it.

**Do not build a contact-aware margin.**  Of the 720 px/frame the wider margin removes, 401 are
bright (luma >= 110, his skin) and 230 are dark.  54.2 % of the chair mask's boundary is a
body-contact seam and 42.8 % faces bright wall, and the extra margin is FREE on the wall-facing
share and expensive on the contact share — the opposite of "wide where it touches".  The
refinement worth building is a **luma-gated dilation**: grow the exclusion mask by 4 px but only
into pixels darker than ~60, the same guard `wingfix` uses.  That keeps the extra dark removal
and gives back all the skin.  One more track would confirm it.

### The luma-gated dilation — `luma_dilate`, an OPTION (2026-09-04)

    track.py ... --exclude-dilate 2 \
                 --exclude-luma-dilate 8 --exclude-luma-max 60 \
                 --exclude-luma-rows 194,432

Per exclusion object: `luma_dilate` (px, **0 = off, the default**), `luma_max` (dark means plate
luma below this — `EXCL_LUMA_MAX` 60, the same guard `wingfix` uses) and `luma_rows` ([r0, r1]).
The mask is grown a further `luma_dilate` px by **geodesic dilation inside the dark set**, seeded
from the UNDILATED chair mask: one 3x3 dilate per step, intersected back with `{luma < luma_max}`
each time.  So the growth follows the dark object and **a bright pixel stops it dead** — it
cannot reach skin at any reach.  The per-frame count of what the gate took beyond the flat margin
lands in the run record as `exclude_luma_gate_px`.

`luma_rows` exists because the gate's one real hazard is the black things that are HIS and touch
the chair: his cap above the ear and his t-shirt at the shoulder.  Unfenced on `reasoninglevel` at
reach 6, **333 of the 375 px/frame it removes are his shirt.**  Fenced to 194..432, 59 of 65 land
on the target.

Measured on `reasoninglevel` against the 2 px and 4 px flat margins (the target is the dark strip
at plate `x 502..512, rows 194..232` — the headrest arm passing behind the top of his left ear,
60.8 px/frame at 2 px of margin):

| | junction px (mean / p95 / max) | takes from him | bright skin | shift on the 3 jaw-skin control rows |
|---|---|---|---|---|
| 2 px flat | 60.8 / 101 / 119 | — | — | — |
| 4 px flat | 33.1 / 55 / 75 | 720 px/f | 401 | +2 / +2 / +2 |
| **2 px + 8 dark-only** | **15.9 / 43 / 53** | **65 px/f** | **0.6** | **+0 / +0 / +0** |

Cost: edge jitter at the two junction rows only — row 200 p95 3 -> 6 px (1.6 % -> 7.9 % of frames
moving >= 5 px), row 215 p95 4 -> 6.  Everything else is unchanged to two decimals, and the gates
cannot separate the two files.

**Do not raise the reach past 8 on this plate.**  15.9 px/frame survive because a bright wall
sliver separates the chair from his cap on many frames and the flood stops there — that remainder
IS his cap.  At reach 16 the flood leaks around the sliver and takes 383 px out of his cap at
1 s (215 at 24 s).  8 is the last value that takes the strip and leaves the cap.

---

## THE STANDARD CLEANING PASS (2026-09-04, deployed v18)

Miguel: *"sure make it the main pass!"*  The chair-as-second-object matte with the dark-only
margin is now what `prep_batch` runs by default, with no human in the loop.  STANDARD.md's
"THE CHAIR IS A SECOND OBJECT" is the law; this is the wiring.

### The defaults, and where they live

They live in ONE place — `modal_app.py` — so no driver can silently pin an old value.  When an
exclusion object is given and says nothing about its margin, it gets:

| | value | constant |
|---|---|---|
| flat margin | 2 px | `EXCL_DILATE` |
| dark-only reach | 8 px | `EXCL_LUMA_DILATE` |
| "dark" | plate luma < 60 | `EXCL_LUMA_MAX` |
| fence | `crown + 180 .. arrival - 48` | `EXCL_FENCE_BELOW_CROWN` / `EXCL_FENCE_ABOVE_ARRIVAL` |
| temporal support | 20% of a chunk | `EXCL_TEMPORAL_FRACTION` |
| ... codec headroom | +10 luma | `EXCL_TEMPORAL_LUMA_SLACK` |
| ... **reach** | **20 px** | **`EXCL_TEMPORAL_REACH`** |

**THE REACH IS NOT OPTIONAL (2026-09-05).**  A temporal support gated on darkness alone owns his
BEARD: on `game33c` it removed the chair on all 691 frames and then punched enclosed cream holes
up to 940 px into his own face (the prior render's number was 46).  A carried support is a
**bridge over a gap in the current frame's own evidence** — it applies only within
`EXCL_TEMPORAL_REACH` px of THIS frame's flat+luma chair mask, and on a frame where that mask is
empty it claims nothing.  20 px is measured: the legitimate bridge (obj3's dropped lower wing)
sits p95 7.7 / max 19.6 px from the current chair, the damaging support 20-107 px.  On top of it,
`enclosed_holes()` hands back anything the subtraction leaves fully enclosed by the presenter and
corrects the diagnostic union with it, `ship.py` re-checks both and REFUSES
(`gate="presenter_loss"`), and `support_refit.py` re-applies the whole rule to an older session's
saved masks with no GPU call.  See STANDARD.md "NO REPAIR MAY REMOVE SKIN (2026-09-05)".

The fence is DERIVED, not typed: `derive_band()` (a by-value copy of `outline.py::_band`, copied
rather than imported so the GPU path never depends on a mount) reads the crown and the shoulder
arrival off the frame-0 silhouette.  The top offset is crown-relative because the ear-top
junction's rows are set by his head; the bottom is arrival-relative because what it protects is
his black t-shirt.  On `reasoninglevel` (crown 14, arrival 481) the container derived
**[194, 433]** — the hand-measured value of the day before, to a row.  The run record carries
`exclude_band`, and each exclusion object carries `luma_fence`: `auto`, `explicit`,
`none (explicit)` or `disabled: ...`.

**If the band cannot be measured the gate turns ITSELF off** (`luma_dilate` 0) and the flat
margin still runs.  An unfenced dark flood eats his t-shirt — measured: at reach 6, 333 of the
375 px/frame it removes are shirt — so guessing is worse than abstaining.

### `chairprompt.py` — the automatic prompt

    chairprompt.py --plate sessions/<v>/plate_wide_25.mp4 \
                   --body  sessions/<v>/prompts/birefnet_00000.png \
                   --overlay <proof.png> --json <out.json>

Exit 0 when a wing was found on either side, 3 when neither.  Hand `--body` the **BiRefNet**
mask, not the wing-cut prompt: it is the body before any cut, so the wing is inside it and its
band extremes are where the search window belongs.

The detector, and every guard, with the measurement that put it there:

| guard | value | why |
|---|---|---|
| the sandwich | dark run with non-dark on BOTH sides | his cap is dark with his head on one side only; his shirt has nothing bright below it |
| search window | `edge_out` 40 px outside the silhouette edge, `edge_in` 200 inside | a dark thing in the plushie shelf is not his headrest |
| `cap_floor` | search never starts above `crown + 165` | above it is his CAP; one cap run joining the component made every wing 260 rows tall and 200 px wide, and `hermesdesktop` failed on exactly that |
| connected regions | not a row-by-row chain | a chain follows whichever run is outermost and DRIFTS — `hermesdesktop`'s right chain drifted 194 px of columns |
| `min_rows` / `max_box_w` | 80 rows / 150 px | a wedge is tall and narrow; the wall and his face are not |
| two-pass band | wings subtracted, band re-derived | the silhouette INCLUDES the wings, so the width reaches 1.35x too early |
| `pos_inset` | clicks 12 % in from the wing's end rows | the first row is where it vanishes under his cap brim; a boundary click is how you tell SAM2 his cap is the chair |
| negatives | cap, cheek at the interface, shoulder INBOARD of the wing, chest | the naive "below the box at the wing's centre" negative lands ON THE CHAIR whenever the box stops short of the wing's bottom |

### Regression — every run-12 and run-13 recording, detection only

    crown / arrival        left                             right
    astramath      16/495  box [407,191,514,458]  260 rows  none
    chatgptwork    11/496  box [382,192,497,459]  260 rows  none
    costpertask    11/476  box [551,172,699,439]  260 rows  none
    hermeskanban    4/439  box [393,165,505,402]  230 rows  none
    reasoninglevel 14/480  box [460,176,566,443]  260 rows  none
    dgxspark       14/488  box [332,184,491,451]  260 rows  none
    hermesdesktop  16/405  box [514,177,619,368]  184 rows  box [869,177,969,368]
    viberesearch   26/494  none                             none

Seven of eight left wings, one right, and **all three required cases** (reasoninglevel-left,
hermesdesktop-right, hermeskanban-left).  Every found box was checked by eye on a proof overlay:
none of them is on his face.  `reasoninglevel`'s auto box is within 10-15 px of the hand-picked
one on every edge and its four positives are within 5-17 px of the hand-picked clicks.

**The right side misses systematically, and that is where the defect is NOT.**  On the right his
hair and sideburn are dark and touch the wing, so the sandwich fails and the components merge past
the 150 px ceiling.  LAW 48's own calibration says the same thing from the other end: every
approved matte's right side runs dark p95 0.50-0.62 and has always been accepted, and both
rejected files were LEFT.  `viberesearch` finds nothing on either side because no wing is beside
his head on that plate; it gets the old pass, byte-identical, which is what it shipped with.

### Regression — one full standard pass on `dgxspark`, an approved matte with a repaired wing

Its frame-0 prompt in the session is the REPAIRED one (run 13's own repair overwrote it), so this
measures the chair object added on top of a shipped repair.

| | LAW 48 left p95 / max / at-line / dark p95 | right p95 / at-line / dark p95 | left-wing residue median / p95 / max | area |
|---|---|---|---|---|
| shipped v3 | 45 / 65 / 13.1 % / 2,205 (24 %) | 47 / 26.7 % / 5,251 (58 %) | 389 / 803 / 1,687 (18/477 over 1,000) | — |
| standard pass | 46 / 67 / 12.0 % / **2,123** (23 %) | **36 / 2.6 % / 5,155** (57 %) | **311 / 659 / 1,563** (14/477) | −923 px/f |

Three gates clean, round 0.  Right side much better (at-line 26.7 % -> 2.6 %), left better on
residue and at-line and +1 row of straight p95 (46 against a 60 ceiling).  Jitter identical
within noise on 14 rows, both edges (biggest delta 0.35 px mean, +3.1 pp on one row's >= 5 px
share).  **Not a regression.**

### Flags

| flag | where | effect |
|---|---|---|
| `--exclude-json FILE` | `track.py` | a `chairprompt` record or a bare list; left -> obj 2, right -> obj 3 |
| `--no-chair-object` | `track.py`, `prep_batch.py` | one object, the pre-2026-09-04 path exactly |
| `no_chair_object: true` | intake row | the same, per recording |
| `--exclude-luma-dilate N` | `track.py` | override the reach; **0 turns the gate off** and leaves the flat margin |
| `--exclude-luma-max L` | `track.py` | override "dark" |
| `--exclude-luma-rows r0,r1` | `track.py` | override the fence |
| `--exclude-no-fence` | `track.py` | deliberately unfenced.  It eats his t-shirt; not a production path |
| `--exclude-box` / `--exclude-points` / `--exclude-dilate` / `--exclude-name` | `track.py` | the hand path, unchanged |

### THE FLARE TEST — why the shoulder arrival misread, and the fix (2026-09-04)

`hermesdesktop`'s frame-0 arrival read **405 against a true ~476**, which made its chair box and
its fence about 100 rows too short and left the wing's lower half inside obj 1 for a whole take.

**THE CAUSE, measured on its frame-0 BiRefNet width profile.**  The 1.35x rule reads the
silhouette's EXTREME COLUMNS, and while the headrest wings are inside the silhouette **those
extremes ARE THE WINGS**:

    row   left  right  width          row   left  right  width
    316    528    943    416          466    519    965    447
    366    530    960    431          476    521    995    475   <- his shoulder
    406    523    965    443  <-1.35x  486    521   1010    490
    436    519    966    448          496    514   1017    504

`left` sits at 519-530 and `right` at 943-966 for a hundred and fifty rows — both WING edges,
~90 px wider than his head — so the width creeps 416 -> 448 and clears 1.35x (442.1) at row 406.
His shoulder arrives at 476, where `right` jumps 965 -> 995 -> 1017 and `left` starts falling
521 -> 489 -> 470.  `reasoninglevel` escaped the identical trap by **eleven pixels** of width
(its peak is 437 against a 448.2 threshold).  That is luck, not design.

**THE FIX.  A head-plus-furniture column is near-vertical; a SHOULDER FLARES.**  From the 1.35x
candidate, walk forward to the first row whose width has grown `flare_px` (20) over the preceding
`flare_win` (20) rows, clamped by `shoulder_max` exactly as before.  It can only ever move the
arrival LATER.  Identical code in three places — `outline.py::_band`, `modal_app.py::derive_band`
and `chairprompt.py::derive_band` — verified by hashing the `_flare` body in all three.

| video | arrival before | after | chair box bottom before -> after |
|---|---|---|---|
| astramath | 496 | 496 | 458 -> 459 |
| chatgptwork | 496 | 496 | 459 -> 459 |
| costpertask | 477 | 477 | 439 -> 440 |
| hermeskanban | 440 | 440 | 402 -> 403 |
| reasoninglevel | 481 | **484** | 443 -> 447 |
| dgxspark | 489 | 489 | 451 -> 452 |
| **hermesdesktop** | **405** | **474** | **368 -> 437** |
| viberesearch | 494 | 494 | none |

**The gate's verdicts do not move.**  `_band` also runs per frame inside LAW 48, so the whole
calibration corpus was re-measured: `reasoninglevel` v1 still REFUSES (87 / 99.4 % / 9,048,
unchanged), `hermeskanban` v2 still REFUSES (132 / 20.0 % / 4,212, matching the calibration table
to the pixel), and `costpertask` v1, `dgxspark` v3, `hermesdesktop` v2 and the two current shipped
mattes are byte-for-byte the same numbers.  The ONE alpha that moved is `hermesdesktop` v1, the
only one that still contains its wings: it refuses HARDER (left 69 -> 74 p95, at-line 46.6 % ->
82.2 %) because the band finally sits on his shoulder instead of on the wings.  That is the fix
working, on the gate as well as on the prompt.

**Two things the fix broke and how they were settled.**

1. **The two-pass band started fighting it.**  Subtracting the detected wing over the rows the
   detector labelled, and not below them, leaves an artificial width STEP at the wing's last
   labelled row — and a step is what the flare test looks for.  `hermesdesktop` pass 1 read 474,
   pass 2 read 434, its own artifact.  So the second pass may only ever move the arrival LATER;
   when it reads earlier, pass 1 stands and the rejection is recorded.
2. **A window ladder was tried and REJECTED.**  With the arrival corrected, `hermesdesktop`'s
   right-hand component now merges and the tallest search window loses that wing.  Shortening the
   window rescues it — and invents a right-hand "wing" on SEVEN of the eight recordings, every one
   a box over his cheek and nose with positive clicks on his skin.  **A false chair object carves
   his face**, so `row_hi_ladder` is one entry long.  Two discriminators were worked through and
   both fail: "the component's outboard edge must touch the silhouette edge" passes the false
   positives, and "outside the head's bright core" fails the TRUE wings, whose wedges slant
   inboard as they descend.  Reinstating the ladder needs a discriminator that survives both.

### `chairprompt.from_refusal` — a chair prompt from a gate's own refusal (2026-09-04)

Both gates report the window they refuse on, so a refusal is a seed for an exclusion object, not a
mystery.  `outline` gives rows + `wing_column`; `protrusion` gives the wing's own `x0`/`x1`.

    from_refusal(plate, body_png, side="right", rows=(180, 470),
                 wing_cols=(781, 857), gate="protrusion")

The window is used **verbatim** and the region is NOT grown.  A first cut grew the seed into its
connected component so the wedge's inboard slant would come along — and at those rows every dark
thing is connected, so the region ran through his beard, neck and shirt (grokbuild 291 px, trycrm
349).  A chair object does not need a precise box; SAM2 refines from the clicks.

**And it must look like a wedge.**  A window wider than `max_box_w` (150) returns
`{"found": False, "verdict": "not a wing"}` with the measurement in `why`.  That test is the guard
that stops the self-heal carving a face: `grokbuild`/run 14's outline refusal names cut column 494
with the silhouette edge at 768 — a 275 px window — and the dark inside the mask there is his own
beard, lips, jaw and neck with the chair correctly excluded outside the edge.  Two wingfix rounds
had already punched ~8,000 px/frame of holes in his neck before it was caught.

Proven on run 14: `trycrm` right (protrusion, x781-857 → box [773,176,865,447], width 77, median
run 69, luma mean 12.4) and `game33c` right both derived automatically and passed in one round.
