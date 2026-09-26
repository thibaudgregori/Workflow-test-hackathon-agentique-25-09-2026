# FRAMING — the derived zoom cap and the source crops every rebuild uses

**Authority:** `format_lab/REVIEW_2026-08-30.md` Global Law 1 (ZOOM CAP) and
Global Law 6 (25→30fps judder). Underneath: `STANDARD.md`'s 20 laws.
**Scope:** the `hermesinfinite` fix round. Every face-bearing rebuild in this
round pulls its face from `format_lab/_shared/`, not from
`hermesinfinite/face_full.mp4`.

Miguel: *"Overall I think you do zoom in way too much on my face. Ideally we
shouldn't have to zoom so aggressively — not just my face, my entire torso and
such can also be in the video."* Everything below is measured, not guessed.

---

## 1. Method

Head geometry is measured with MediaPipe FaceLandmarker
(`~/.cache/thumbnail-factory/face_landmarker.task`) plus a luminance scan, on
frames decoded straight out of the videos. Two metrics, both expressed as a
fraction of the **1080×1920 delivery canvas** — never of a plate's own height,
because the plates are not all 1920 tall:

| metric | definition | why |
|---|---|---|
| `face_frac` | (chin lm152 − brow lm10) / 1920 | landmark-only. Hat- and hairstyle-independent, so it compares across subjects and across reference videos. **This is the metric the law is written in.** |
| `head_frac` | (chin lm152 − top of cap) / 1920 | what a viewer actually calls "how big is his head". Cap top found by scanning the head column for the black-cap/warm-wall luminance edge. |

For this subject the two are locked together: `head_frac = 1.287 × face_frac`
(measured over 14 master frames).

Scripts: `_shared/build_face_crops.py`, `_shared/verify_face_crops.py`.
Raw measurements: `_shared/face_crops_report.json`,
`_shared/face_crops_verify.json`.

---

## 2. What the lab actually shipped (the thing Miguel rejected)

Measured on the rendered lab MP4s, before/after every declared punch-in.

**takeover_v1** — 20 declared punches at scale 1.00 → 1.18, measured either side
of each cut (10 punch pairs survive; the rest fall inside takeover scenes):

| | face_frac | head_frac |
|---|---|---|
| rest floor | 0.409 – 0.430 | 0.542 – 0.557 |
| after a 1.12–1.18 punch | 0.459 – 0.509 | 0.594 – **0.723** |

The worst single frame (t=46.9, declared scale 1.16) puts his head at **72.3% of
the frame height**.

**pureface_v3** — dense sweep, 133 sampled frames across the full 54s:

| | min | median | p90 | max |
|---|---|---|---|---|
| face_frac | 0.395 | 0.444 | 0.484 | 0.528 |
| head_frac | 0.526 | 0.604 | 0.660 | 0.732 |

---

## 3. The benchmark — Miguel's own reference reel

`references/ref2_instagram_split.mp4` is the reel Miguel chose as the
mode-switch reference. Swept every 0.4s; 57 of 113 frames carry a face. The
distribution is cleanly **bimodal**, matching its two documented layout modes:

| mode | n | face_frac min | median | max |
|---|---|---|---|---|
| M1 — face in a card / split | 23 | 0.196 | **0.220** | 0.238 |
| M2 — full-face | 34 | 0.359 | **0.393** | **0.419** |

**The verdict, quantified:**
- pureface_v3's *widest* frame (0.395) equals the reference's *median*
  full-face frame (0.393). Its median (0.444) is **6% above the reference's
  single most zoomed frame ever** (0.419). All 133 sampled frames sit at or
  above the reference's full-face median.
- The reference spends 40% of its face time at face_frac ≈ 0.22 — a framing our
  lab never once used.
- Intra-mode spread in the reference: card 0.196→0.238 = **1.21×**, full-face
  0.359→0.419 = **1.17×**. That is the entire zoom range it uses *within* a
  mode. Everything bigger is done by **cutting to a different mode**.

---

## 4. The physical ceiling (read this before proposing a wider full-bleed)

The master is 3840×2160. A full-bleed 9:16 crop must satisfy `w/h = 0.5625` with
`h ≤ 2160`, so the **widest possible full-bleed window is 1215×2160**. Any
9:16 crop of a 16:9 master therefore magnifies the head by `16/9 ÷ 9/16 = 3.16×`
relative to the width it had in the master, and no amount of re-cropping changes
that.

Measured consequence: master `head_frac` 0.551 → `face_full.mp4` `head_frac`
0.553. They are the same number, because `face_full.mp4` is a full-height,
horizontal-only crop. **The existing face crop was already at the physical
floor. The lab's punch-ins went below the floor, into territory the source
cannot support.**

So the zoom cap cannot be a crop parameter. **It is a composition law:** a
face-led rest state is a *plate that does not fill the canvas width*. This is
exactly the reference's M1 grammar, and exactly the switching Miguel praised in
takeover and asked for in facesplit.

---

## 5. THE LAW

Three plates. All three are the same full-height slice of the master at three
widths, so head size on canvas is set **entirely by crop width**:

```
head_px_on_canvas = 1191 × (1080 / crop_width)
```

| plate | role | crop_w | face_frac | head_frac | head px | plate size |
|---|---|---|---|---|---|---|
| `face_wide_25` | **REST** — the default for every face-led format | 2592 | **0.201** | **0.259** | 496 | 1080×900 |
| `face_std_25` | **MID** — split band, half-frame face, secondary beats | 1728 | **0.301** | **0.388** | 744 | 1080×1350 |
| `face_max_25` | **CEILING** — full-bleed, punch destination only | 1216 | **0.428** | **0.551** | 1058 | 1080×1920 |

**Where the three numbers come from**

- **REST 0.201.** 2592 is the narrowest window in which Miguel's whole shoulder
  line fits inside the frame: measured shoulder span 2511 px, plus 3.2% margin.
  It lands at the wide end of the reference's card-mode band (0.196–0.238) — i.e.
  it is *derived from his own body*, and independently confirmed by the reel he
  picked. Shoulders and upper torso in, 144 px of headroom above the cap.
- **MID 0.301.** 1728 = 2592 / 1.5, the midpoint between the reference's two
  clusters. Shoulders run off the sides; chest still reads.
- **CEILING 0.428.** The physical floor of a full-bleed 9:16 crop (§4), and
  within 2% of the reference's most zoomed frame ever recorded (0.419). It is
  the ceiling *by construction* — you cannot legally go past it, and you cannot
  physically go wider while full-bleed.

### Hard rules

1. **`face_max_25` renders at scale 1.00. Always. Punch-ins on it are banned.**
   It is already at the ceiling; scaling it is what produced the 0.72 head_frac
   frames Miguel rejected.
2. **A full-bleed face is never the rest state.** Rest is `face_wide_25` on a
   canvas the format owns. `hermesinfinite/face_full.mp4` is retired from
   rest-state use for this round.
3. **Within-mode punch multiplier ≤ 1.15**, derived from the reference's own
   intra-cluster spread (1.17× / 1.21×), and it may never carry a plate past
   face_frac 0.43:
   - `face_wide_25` → max 1.15 (face_frac 0.231, still inside the card band)
   - `face_std_25` → max 1.15 (face_frac 0.346, under the ceiling)
   - `face_max_25` → **1.00**
4. **Size changes bigger than 1.15 are MODE SWITCHES, executed as HARD CUTS**
   between plates — Miguel's stated preference ("the takeover's zoom *style*
   (hard cut punch-ins) is the preferred grammar over animated creep"):
   wide→std ×1.50 · std→max ×1.42 · wide→max ×2.13 (head height ratios).
5. **A punch is a single-frame cut, not a tween.** Use `tl.set(...)`, not
   `tl.to(..., duration: 0.05)` — at 25fps a 0.05s tween spans 1.25 frames and
   renders one intermediate scale, which reads as a smear. Minimum hold after a
   punch stays 0.4s (existing `guard_punch_holds`).
6. **No animated zoom creep** anywhere. A scale that moves across more than one
   frame without a cut is idle motion (STANDARD Law 1).

### Placement on the 1080×1920 canvas

All three plates are full master height, so the eye line sits at the same
relative depth in each: **40.1% down the plate**. Headroom above the cap:
144 px (wide) · 216 px (std) · 306 px (max).

`face_wide_25` leaves 1020 px of canvas. That surplus is the format's design
ground — captions, plates, diagrams, the split's top half. It is not padding to
be scaled away; scaling the plate up to fill the canvas re-breaks Law 1.

---

## 6. The crop windows (reproducible)

Cut from `hermesinfinite/source_cut_master.mp4` (3840×2160). Measured master
geometry, medians over 14 frames:

```
face centre x  1874 px      head top (cap)   345 px      head height  1191 px
eye line y      865 px      chin y          1545 px      face height   925 px
shoulder span  2511 px
```

Every window is `crop_w × 2160` at `y=0`, x-centred on the face:

| file | ffmpeg crop | scale | out |
|---|---|---|---|
| `face_wide_25.mp4` | `crop=2592:2160:578:0` | `1080:900` | 1080×900 |
| `face_std_25.mp4` | `crop=1728:2160:1010:0` | `1080:1350` | 1080×1350 |
| `face_max_25.mp4` | `crop=1216:2160:1266:0` | `1080:1920` | 1080×1920 |

`face_max_25` uses 1216 rather than 1215 to keep the crop width even for
yuv420p; the resulting 0.08% horizontal squeeze is below perception.

**Generalising to future recordings** (any 4K 16:9 master):
`REST crop_w = shoulder_span × 1.032` · `MID crop_w = REST / 1.5` ·
`MAX crop_w = master_h × 9/16`.

---

## 7. The 25fps de-conform (Global Law 6)

The master is 1625 frames / 54.16667s at 30fps, of which **exactly 273 (16.8%)
are conform duplicates**. Verified two independent ways that agree on 1352
uniques: a 160×90 gray frame-diff scan (dupes cluster at diff < 0.08, real
frames above 1.0 — a 12× margin, so the set is unambiguous) and `mpdecimate` at
three different threshold sets.

The 273 duplicates are **7 arithmetic runs of step 6** whose phase resets at the
four take splices (13.10s, 25.9s, 47.3s, 53.4s).

1352 uniques over 54.16667s is 24.96 fps, not 25 — the splices ate ~2 frames of
content while keeping wall-clock duration. Three ways to land that on a 25fps
timeline, and **only one is right**:

| approach | result |
|---|---|
| `mpdecimate,fps=25` | re-duplicates **173 frames (12.8%)**. Puts the judder straight back in. Measured, not theorised. |
| `mpdecimate,setpts=N/(25*TB)` | true CFR 25 but **87ms short**; the face drifts ahead of its own audio. |
| **keep 2 dupes at the splices (frames 782, 1605)** | **1354 frames, true CFR 25/1, 54.16s, residual drift −6.7ms.** ← what we ship |

The two surviving duplicates sit on take splices, where a single held frame is
invisible. They were chosen by walking cumulative drift, not by eye.

```
select='not(<7 runs>)',setpts=N/(25*TB),crop=…,scale=…    -fps_mode cfr -r 25
```

Do **not** substitute the `fps` filter for `setpts` here, and do not encode with
`-fps_mode passthrough` at 24.96 — that produces a file whose container still
advertises `r_frame_rate=30/1`, and every downstream decoder re-inserts the 273
duplicates.

---

## 8. Verification

`verify_face_crops.py` decodes 4 frames of each derivative and checks size, fps,
frame count, duration, duplicate rate, and both head and face fractions against
the declared spec (tolerance ±0.020 canvas-height points; natural head sway is
±0.015). Result:

| file | size | fps | frames | dur | dupes | head_frac want→got | face_frac want→got |
|---|---|---|---|---|---|---|---|
| `face_wide_25.mp4` | 1080×900 | 25.0 | 1354 | 54.16 | 2 (0.15%) | 0.2585 → **0.2587** | 0.2007 → **0.1996** |
| `face_std_25.mp4` | 1080×1350 | 25.0 | 1354 | 54.16 | 2 (0.15%) | 0.3877 → **0.3901** | 0.3011 → **0.3033** |
| `face_max_25.mp4` | 1080×1920 | 25.0 | 1354 | 54.16 | 2 (0.15%) | 0.5509 → **0.5551** | 0.4279 → **0.4320** |

**ALL PASS.** Duplicate rate drops from 16.8% (source) to 0.15%.

---

## 9. Consequences for the fix round

- **pureface** — "too zoomed in" is not fixable as a full-bleed format from this
  source (§4). It rebuilds on `face_wide_25` with the canvas surplus as design
  ground, using `face_max_25` only as a punctuation cut.
- **facesplit** — the requested dynamic switching maps directly onto the plate
  set: `face_max_25` for full-face beats, `face_std_25` for the 50/50 band,
  `face_wide_25` for rest. Hard cuts, no tweens.
- **takeover** — keep the grammar, replace the source with `face_max_25` at
  scale 1.00 and drop the 1.08–1.18 punch table; the drama comes from the
  wide→max cut instead.
- **cutout** — "wants SHOULDERS visible" is `face_wide_25` by construction: it is
  the narrowest window his shoulder line fits inside.
