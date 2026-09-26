# Codex (gpt-6-astra, xhigh) audit of the cut-out pipeline, 2026-09-05

# CUT-OUT pipeline audit — 2026-09-05

Scope: requested source files and historical sections, saved game33c tracking/shipping records, and small in-memory reproductions. No GPU jobs or repairs were run. Modal’s metadata endpoint was unreachable, so findings describe the inspected source and saved artifacts, not a verified current deployment.

## A. Concrete bugs and fragile logic

### A1. “Not a wing” does not stop destructive repair — critical

[`chairprompt.py:642`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/sam2/chairprompt.py:642) returns `found=False`, `verdict="not a wing"` for an overwide window. Its explanation explicitly recommends avoiding another cut.

But [`prep_batch.py:1474`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/prep/prep_batch.py:1474) reduces that result to whether a prompt was derived. If none was derived, it builds `outline_args`; [`prep_batch.py:1503`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/prep/prep_batch.py:1503) explicitly logs “NOT a wedge … falling back to wingfix.”

**Failure scenario:** grokbuild’s 275-pixel window identifies beard, jaw and neck. The guard prevents creating a chair object but still permits `wingfix` to carve the same region. The historical 7,719–8,174 pixels/frame of neck loss remain a reachable failure class.

The protrusion branch has the same conflation at line 1415. Detector uncertainty, detector error, an existing exclusion object, and evidence of anatomy all become reasons to try a rectangle.

**Required invariant:** “not a wing” must veto that destructive operation. It must not automatically waive the outline gate either.

### A2. Existing chair objects cannot receive targeted corrections

[`prep_batch.py:1336`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/prep/prep_batch.py:1336) skips any side already listed as excluded.

**Failure scenario:** game33c has objects 2 and 3, but one tracks the wrong extent beside the head. A later refusal cannot improve its prompt through this path; the repair loop treats the mere existence of an object as sufficient treatment.

Furthermore, [`prep_batch.py:1311`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/prep/prep_batch.py:1311) always supplies the original frame-zero body mask, and the `from_refusal` call supplies no event frame. Outline refusal windows combine median row bounds and percentile reach measurements across time.

**Failure scenario:** the chair is visible at the failed frame but hidden at frame zero, or the presenter has leaned into that window. A geometrically plausible refusal becomes a prompt on the wrong image.

### A3. Repair rounds can lose prompt lineage; replating can reuse stale coordinates

[`prep_batch.py:1391`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/prep/prep_batch.py:1391) initializes every round from `session/prompts`. Chair-only repairs write no replacement prompt directory, so the fallback at lines 1446 and 1517 can return to those original prompts.

**Failure scenario:** round one creates corrected dense prompts; round two adds a chair object and silently drops those corrections. Conversely, an existing `prompts_<tag>` directory can be reused merely because it contains keyframes.

After replating, [`prep_batch.py:1568`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/prep/prep_batch.py:1568) re-applies the intake’s chair override. [`prep_batch.py:610`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/prep/prep_batch.py:610) copies its coordinates directly.

**Failure scenario:** widening changes plate coordinates, but an old override box lands on the cheek. The comments correctly identify this risk; the override path does not transform or invalidate those coordinates.

### A4. The straight-run counter undercounts valid runs — reproduced

[`outline.py:233`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/sam2/outline.py:233), `_longest_flat`, advances to `j - 1` after a run. That skips alternative starting positions needed to find the longest range within tolerance.

In-memory reproduction:

| Input edge columns, tolerance 1 | Correct longest run | Returned |
|---|---:|---:|
| `[100] + [101] × 35 + [102] × 35` | 70 rows | 36 rows |

**Failure scenario:** a 70-row near-vertical furniture edge escapes both the 60-row p95 ceiling and the 40-row persistence count.

Fixing this alone will also expose more legitimate jaw contours. Repair safety and anatomy calibration must accompany it.

### A5. Missing measurements can become “clean” — reproduced

[`outline.py:367`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/sam2/outline.py:367) silently uses the shorter of the alpha and plate stacks. Unmeasurable bands are skipped; no measured runs produces `measured: 0`; line 496 returns clean when there are no refusals.

Direct reproductions:

- Four entirely empty alpha frames → **clean**, both sides measured zero.
- Four alpha frames paired with zero plate frames → **clean**, zero frames checked.

This demonstrates a component-level acceptance hole, not proof that every surrounding stage would accept those inputs.

**Failure scenario:** disappearance, severe cropping, or a truncated decode removes the evidence the gate needs, making its result look better.

### A6. LAW 48 does not measure “never a bad outline”

[`ship.py:762`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/sam2/ship.py:762) defaults to stride 5. [`outline.py:439`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/sam2/outline.py:439) aggregates p95 and prevalence; reported maxima do not gate.

The saved game33c v5 report checks **139 of 691 frames** and returns clean. Its left/right straight p95 values are 39.1/38.1; dark fractions are 24.1%/58.0%.

Two independent weaknesses follow:

- Four out of five frames are unmeasured.
- Short failures can disappear into a percentile. With 139 samples, six values of 100 and 133 values of 20 still produce p95 **20**.

There is no temporal-order test: shuffling otherwise identical frame measurements leaves the decision unchanged.

Finally, [`ship.py:778`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/sam2/ship.py:778) runs furniture/outline checks **before** temporal median, polish, resizing and encoding. The subsequent gate checks borders, not the finished head/chair boundary.

**Failure scenario:** game33c’s brief chair residue passes; a later post-processing change can introduce another outline defect without rerunning an outline check.

### A7. Chair prompts lack the semantic safeguards their descriptions imply

The “sandwich” condition at [`chairprompt.py:273`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/sam2/chairprompt.py:273) checks the pixels immediately outside a maximal dark run. By definition, those adjacent pixels are already non-dark. It does not establish a bright wall on one side and presenter anatomy on the other.

**Failure scenario:** a dark region bounded by merely slightly lighter pixels passes that part of the test. Hair touching the chair merges regions and can defeat the width limits, explaining the structural weakness behind the right-side misses.

The refusal fallback introduces a separate issue: [`chairprompt.py:659`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/sam2/chairprompt.py:659) takes the minimum and maximum of **all** dark pixels in each row; line 686 places a positive click at their midpoint.

**Failure scenario:** two disconnected dark patches surround bright cheek pixels. Their midpoint becomes a positive “chair” click on the cheek. The midpoint is not checked for membership in the selected dark component.

### A8. Chair masks are handed across chunks, but chair knowledge is not

Objects 2 and 3 are correctly copied at [`modal_app.py:1402`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/sam2/modal_app.py:1402). **A missing handoff for object 3 is not the bug.**

However, each chunk creates a fresh predictor state at line 1250 and initializes each object from one thresholded handoff mask at lines 1300–1306. Original clicks, appearance history and prior conditioning frames are not carried across.

Later keyframe prompts at line 1314 apply only to the presenter. Exclusion prompts are frame-zero box/points only.

**Failure scenarios:**

- A locally wrong chair mask becomes the next chunk’s authoritative seed.
- A truly lost chair can be handed over as empty.
- An oversized chair exclusion cuts the body, and the already-subtracted presenter mask seeds that damage into the next chunk.

Subtraction at line 1354 happens outside the predictor; it does not itself teach the presenter object that those pixels are chair during that chunk.

### A9. Seam “IoU” is background-dominated agreement and cannot stop shipping

[`modal_app.py:1373`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/sam2/modal_app.py:1373) computes whole-image equality, not intersection-over-union. At game33c’s 1620×900 size, the 0.995 floor permits roughly **7,290 disagreeing pixels**.

Only the final presenter mask is compared, not each exclusion object. The overlap is not reconciled.

At [`modal_app.py:1595`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/sam2/modal_app.py:1595), shipping is spawned before seam warnings are evaluated; those warnings do not refuse the result.

**Failure scenario:** thousands of wrong pixels around the jaw are overwhelmed by unchanged background and either pass the statistic or produce only a warning.

### A10. Dark dilation is a source of flicker and anatomy loss

[`modal_app.py:1217`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/sam2/modal_app.py:1217) grows exclusions through pixels below a hard luma threshold. Connectivity can change abruptly from a one-pixel brightness change.

This is already measured in [`LEARNINGS.md:15793`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/LEARNINGS.md:15793): row-200 jitter p95 increased from **3 to 6 pixels**, and movements ≥5 pixels rose from **1.6% to 7.9%**.

The fence is derived once from frame zero at [`modal_app.py:1441`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/sam2/modal_app.py:1441). It does not follow a leaning head or rising shoulder. `_flare` returns the original shoulder estimate even when it finds no qualifying flare.

**Failure scenario:** a fence safe for the opening pose later overlaps a dark neck or shirt. Dark skin, beard, cap and clothing remain removable; “dark-only” is not an anatomy guarantee. The unconditional two-pixel margin has even fewer protections.

### A11. Endpoint borrowing is fixed; interior borrowing remains

[`ship.py:393`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/sam2/ship.py:393) correctly uses the current mask at the first and last frames.

Interior frames still use an unwarped median:

- `[foreground, background, foreground]` becomes foreground.
- `[background, foreground, background]` becomes background.

**Failure scenario:** a fast hand or newly revealed background occupies a pixel for one frame. The median puts a neighboring silhouette over the current RGB image.

The endpoint report’s `revealed_px=0` is assigned by construction at line 251; it is not a measurement of the final polished/encoded edge.

A separate short-input bug is reproducible: with one input frame and the default mirrored three-frame window, [`ship.py:335`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/sam2/ship.py:335) supplies insufficient padding and emits **zero output windows**.

### A12. Infrastructure errors can weaken quality checks

[`prep_batch.py:641`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/prep/prep_batch.py:641) catches detector/overlay errors, removes the chair JSON, and returns an error record. Subsequent tracking uses the single-object path when that file is absent. Even an explicit override depends on automatic detection succeeding first.

[`ship.py:297`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/sam2/ship.py:297) stops when either input decode stops without asserting equal frame counts or timestamps. Encoder return codes at line 536 are ignored.

**Failure scenarios:** a detector exception removes chair handling; unequal inputs silently truncate the result; an encoder failure leaves partial artifacts whose prefix can still be inspected.

### A13. The final border gate has a narrower contract than complete outline safety

[`edge_clip_check.py:369`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/edge_clip_check.py:369) measures four vertical columns. It does not provide a full-frame top/crown/rim check; LAW 44a’s separate sampled check cannot substitute for that.

Its shoulder baseline at line 270 is the median of the observed border contact.

**Failure scenario:** an arm connected to the torso touches a visible plate edge for most of the take and becomes the baseline rather than a detected rise.

The exemption for sufficiently offscreen plate borders is intentional and should remain. A phone-frame crop is not automatically a plate-clipping defect.

### A14. Reproduction is not pinned tightly enough

[`modal_app.py:117`](/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory/pipeline/sam2/modal_app.py:117) clones SAM2’s current default branch. The run record stores model/config names, not the SAM2 commit, checkpoint hash or resolved predictor options.

**Failure scenario:** rebuilding the same local source changes tracking behavior while retaining an apparently identical configuration label.

A particularly important assumption to verify: the current official B+ configuration sets `use_mask_input_as_output_without_sam: true`. A supplied mask can therefore be returned directly on its conditioning frame; “SAM2 will refine every rough mask prompt” is unsafe. This is verified upstream behavior, not confirmation of the unreachable deployment. [Official B+ configuration](https://raw.githubusercontent.com/facebookresearch/sam2/main/sam2/configs/sam2.1/sam2.1_hiera_b%2B.yaml).

## B. Top five changes, ranked

Cost reference: game33c contains 691 frames at 25 fps. Its saved record reports **116.35 seconds first propagation plus 128.88 seconds healing propagation**. The advertised 354.9 ms/frame includes both. One comparable additional healing pass scales to approximately **140 GPU seconds for 30 seconds of video**, or **280 for 60 seconds**, excluding startup and additional work.

### 1. Gate every finished frame, including temporal stability

Retain cheap early checks, then validate the actual decoded, composited delivery after median, polish, scaling, rim and encoding.

Each frame needs separate scores for:

- Retained chair/background.
- Missing presenter pixels, especially face, neck, hands and cap.
- Boundary displacement and holes.
- Motion-compensated temporal inconsistency.
- Plate-edge and crown clearance.
- Measurement confidence and completeness.

Use hard limits for critical defects. A combined risk score can take the **maximum normalized violation**, so good performance elsewhere cannot compensate for a neck hole. Stability must use motion compensation and occlusion handling: a correctly moving head should not be penalized merely for moving.

**GPU cost:** zero for decode, geometry, coverage and deterministic comparisons. A learned motion/quality component needs benchmarking. At 25 fps, an additional `m` milliseconds/frame costs `0.75m` GPU seconds per 30-second clip.

**Before adoption:** measure false accepts, false refusals and unresolved frames on entire held-out takes. Require detection of game33c’s transition, one-frame injected wedges and post-processing defects while accepting the intact grokbuild lean.

This ranks first because it prevents a defect from being silently delivered regardless of which producer introduced it.

### 2. Replace the destructive fallback with explicit outcomes and preservation checks

Give each side one of four outcomes: **verified chair, verified anatomy, unresolved, infrastructure error**. Preserve the active prompt lineage and coordinate transform explicitly.

A practical fallback ladder:

1. Inspect the actual failing frame and neighboring visibility states.
2. Correct the existing chair object, or add a missing object, using independently validated prompts.
3. Retrack the affected interval with reliable anchors on both sides; rerun final quality checks.
4. Try an independently evaluated portrait/matting candidate if semantic separation remains unresolved.
5. If separation remains ambiguous, use an approved alternate format/source treatment or hold delivery.

A rectangle should require positive evidence that every removed region is furniture and that protected body regions survive. Detector failure is not that evidence.

For future recordings, **removing the visible headrest or changing its contrast/separation from hair and clothing has zero inference cost** and directly reduces the ambiguity that generated these failures.

**GPU cost:** zero for dispatch, lineage and preservation logic. Retracking adds approximately the interval’s measured propagation cost; a full comparable extra pass is about 140 seconds/30-second clip. Independent-model fallbacks add their measured inference cost.

**Before adoption:** replay grokbuild’s two harmful repairs; mixed left/right outcomes; existing-object drift; detector exceptions; second-round repairs; and replating with overrides. Require zero newly removed protected-body pixels. Report fallback frequency and cutout completion rate.

### 3. Make chair tracking observable and correctable throughout the take

Keep presenter and chair identities explicit. Compare:

- Accurate full masks.
- Tight box plus validated positive/negative clicks.
- Multiple conditioning frames.
- A single chair object versus independently tracked visible wings.

Negative clicks on the presenter constrain a **chair** object; chair/background negative clicks constrain a **presenter** object. They are object-specific instructions, not global exclusions. Validate every generated click against its intended region.

Prompt at visibility changes and difficult poses, not only frame zero. Test fixed budgets of one, three and five conditioning frames against an adaptive strategy. Accurate masks can stabilize a track; repeated rough masks can repeatedly reintroduce the same defect.

Save, per object and per frame:

- Raw mask/logits and object-presence output.
- Effective mask after flat and dark dilation.
- Presenter mask before subtraction.
- Final subtracted mask.
- Prompt identity, timestamp and chunk mapping.

For chunks, compare each object’s boundary and foreground-region overlap. Preserve reliable conditioning evidence, or reinitialize from several validated anchors. Do not carry an empty or suspicious mask forward without distinguishing occlusion from tracking failure.

Current upstream SAM2 defaults to seven spatial mask-memory slots, with separate conditioning-frame and object-pointer behavior. A 16-frame warm lap is not a 16-slot memory bank. Increasing memory length is not a free fix: memory-position parameters depend on its size, and more stale evidence can preserve a wrong object. First test temporal stride and conditioning-frame policy at the checkpoint’s supported configuration. [Official SAM2 implementation](https://raw.githubusercontent.com/facebookresearch/sam2/main/sam2/modeling/sam2_base.py).

A separate background object merits an ablation, especially for visible wall leakage. It must provide independent evidence; `background = 1 − presenter` adds none. Broad background masks also make whole-image agreement less useful. SAM2 exposes separate per-object inference and optional non-overlap handling, so adding an object does not automatically establish correct semantic ownership. [Official video predictor](https://raw.githubusercontent.com/facebookresearch/sam2/main/sam2/sam2_video_predictor.py).

**GPU cost:** extra prompts, memory and object decoding are unmeasured here; benchmark them separately. Full backward propagation adds approximately another pass. Restrict it to uncertain intervals if validated. Do not infer a fourth object’s cost from a simple object-count ratio.

**Before adoption:** compare chair recall, presenter loss, disappearance/reappearance events, seam errors, peak VRAM and GPU seconds on identical inputs. Include actual occlusion, where an empty visible-chair mask can be correct.

**Game33c diagnosis:** both recorded exclusion objects remained nonempty: minima were 11,320 and 5,632 pixels. Its only recorded chunk seam is frame 350, at 14 seconds. Thus whole-object disappearance and that seam do not explain the reported 4–5.2-second event. Local mask drift, changing overlap with the presenter, hard luma connectivity, and post-processing remain hypotheses. The missing per-object/effective-mask traces prevent attribution.

### 4. Replace the upright straight-line ceiling with anatomy-aware evidence

A 61-row jaw is not worse than a 59-row jaw merely because it crosses an upright calibration threshold.

Use head scale and pose to define head, jaw, neck, shoulder and chair-adjacent regions. Compare the outline in a pose-relative coordinate system; retain straightness as supporting evidence. A straight segment overlapping independently identified jaw anatomy should not trigger a furniture cut by itself.

Move the dilation fence with the relevant anatomy each frame. If shoulder/pose confidence fails, return unresolved. A failed flare search must not masquerade as a successful anatomical measurement.

**GPU cost:** zero for geometric normalization once landmarks exist. A new landmark/pose model requires measured milliseconds/frame and follows the same `0.75m` conversion above.

**Before adoption:** label upright and leaning examples independently of the current alpha. Hold out complete recordings. Measure false refusal versus lean angle/head scale and false acceptance of real wedges. Grokbuild should pass intact; hermeskanban, reasoninglevel and hermesdesktop furniture should still fail. Simply changing 60 to 80 does not meet that requirement.

### 5. Refine the edge after semantic separation; benchmark guided filtering and matting

The current `polish(am > 0.5)` discards soft alpha before rebuilding a feather. It smooths a contour without proving what that contour belongs to.

Test an RGB-guided filter first within a narrow uncertain boundary band, preserving confident foreground and background. Guided filtering can align smoothing with image structure, but it cannot decide that a dark edge belongs to chair rather than hair. [Original guided-filter work](https://people.csail.mit.edu/kaiming/eccv10/index.html).

Then compare ViTMatte using a validated trimap: certain presenter, certain background, uncertain edge. A trimap that marks chair as certain foreground cannot be expected to repair that classification. [Official ViTMatte implementation](https://github.com/hustvl/ViTMatte).

**BiRefNet should be evaluated as a refinement candidate, but the existing sweep is not a refiner.** It samples frames and exports silhouette extrema for framing. Those summaries cannot reconstruct detailed alpha. Keep that framing function; separately evaluate a matting checkpoint at delivery coordinates and temporal cadence. Official BiRefNet distinguishes general segmentation and matting models. [Official BiRefNet model documentation](https://github.com/ZhengPeng7/BiRefNet).

**GPU cost:**

- CPU guided filter: zero GPU time; measure CPU latency.
- ViTMatte/BiRefNet matting: unknown on this pipeline until benchmarked.
- The existing game33c BiRefNet-general sweep measured 0.532 seconds/sample on A10G. Running that graph at every frame would take approximately **399 GPU seconds/30-second clip**, or **798/60 seconds**. That is a baseline extrapolation, not a matting-model forecast.

**Before adoption:** compare boundary alpha error, hair detail, foreground loss, chair residue and temporal flicker after final encoding. Include “no refinement” as the control. A sharper single frame with worse temporal stability loses.

## C. What “100% perfect” acceptance must measure

The operational contract should be:

> Every delivered cutout has every frame checked against explicit limits, contains no unresolved critical region, and carries evidence tied to the exact delivered bytes.

That is enforceable. Universal correctness on arbitrary footage where chair and hair are visually indistinguishable is not. Achieving reliable unattended delivery requires controlled capture, measurable limits and an abstention/fallback path.

### Per-frame measurements

| Measurement | What must be recorded and gated |
|---|---|
| Frame integrity | Expected frame index, timestamp, dimensions and RGB/alpha pairing. Reject missing, duplicate, reordered or truncated frames. Decode the actual alpha plane. |
| Presenter preservation | Missing area and largest missing component separately for face, beard/neck, cap/hair, torso and hands. A low “bright skin removed” count cannot excuse dark-neck loss. |
| Furniture/background residue | Retained alpha mass, area, extent and largest component in independently identified non-presenter regions, including both chair sides. |
| Boundary accuracy | Inward and outward distance errors separately, at final display scale. Whole-body IoU cannot hide a jaw defect. |
| Matting quality | Alpha error, gradient/connectivity error, holes and halos. Evaluate compositing against the actual cream/rim treatment and diagnostic contrasting backgrounds. |
| Temporal consistency | Motion-compensated boundary displacement, alpha residuals and appearance/disappearance events, with occlusion confidence. |
| Subtraction safety | Per-object effective exclusion overlap with protected presenter regions; confidence in chair visibility. |
| Crop/rim safety | Crown/top clearance and visible plate-border contacts after scaling and rim construction, preserving the authorized offscreen-border exemption. |
| Measurement validity | Whether every required region was measured reliably. “Unmeasured” must never mean clean. |

**Offline and runtime evidence must remain distinct.** Ground-truth comparisons require independently labelled evaluation footage. Production estimators approximate those quantities; their confidence needs calibration against that footage.

An initial acceptance specification could require:

- Zero leakage into labelled chair/background **interiors** beyond alpha quantization tolerance.
- Zero holes in labelled opaque presenter interiors.
- At most one final-display-pixel boundary error on well-defined opaque boundaries.
- A separately calibrated soft-alpha tolerance for hair and motion blur.
- Zero critical temporal events, including single-frame events.
- Zero unresolved critical frames.

These are proposed targets to validate, not thresholds established by this audit. Ambiguous boundary pixels need explicit uncertainty labels rather than fabricated precision.

### Per-video measurements

Acceptance must require all of the following:

1. **Coverage:** checked frames equal decoded delivery frames equal expected frames.
2. **Critical defects:** zero failed frames; retain maximum severity, frame/time and location. Percentiles remain diagnostics.
3. **Temporal events:** zero unapproved flicker events; record event count, duration and peak displacement.
4. **Anatomy preservation:** no repair-induced regression in any protected region.
5. **Boundary cases:** explicit first/last-frame and chunk-boundary results.
6. **Provenance:** hashes for source, crop/transform, prompts, checkpoint, code/configuration and delivered layers/video.
7. **Decision lineage:** every repair, fallback and override recorded; a reason string alone cannot establish quality.
8. **Operational yield:** report accepted cutouts, alternate-format fallbacks, holds, retries and GPU seconds per accepted video.

Yield matters: a gate that rejects everything achieves zero bad deliveries while failing the factory’s purpose.

### Mandatory regression corpus

Preserve both defective and correct versions of:

- Hermeskanban, reasoninglevel and hermesdesktop: attached chair wedges.
- Game33c: the reported 4–5.2-second transition, expanded to **every native frame**, plus the complete video.
- Grokbuild: intact lean as a positive control; both neck-carved versions as negatives.
- Endpoint-borrow examples, including moving hands.
- All eight chair-detection plates, including the seven right-side misses.

Add controlled fault injections:

- One-frame chair leakage and one-frame body loss.
- Chair occlusion versus tracker disappearance.
- An empty exclusion at a chunk handoff.
- Connected hair/headrest and shadowed neck.
- Stale coordinates after replating.
- Detector/encoder failure and mismatched frame counts.
- Empty alpha; one-, two- and three-frame clips.
- The 70-row counterexample.
- A defect introduced only by median, polish or final composition.

Freeze thresholds before testing held-out recordings. Historical approval with a known flaw must not silently turn that flaw into a correct training label.

Finally, report **false acceptance per video**, not just millions of correlated passing frames. Zero failures in 3,000 independent representative videos supports an approximate 95% upper bound of 0.1% failure—not proof of perfection. Routine manual inspection can fall substantially once this contract is validated; difficult unseen inputs still require reliable fallback rather than an unconditional “clean.”
