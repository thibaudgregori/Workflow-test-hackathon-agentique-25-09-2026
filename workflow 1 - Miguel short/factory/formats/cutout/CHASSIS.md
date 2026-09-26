# CUTOUT — chassis

**Status:** approved, **and named THE STANDARD** (Miguel, round 4:
*"Looks amazing, bravo! I think we cracked trimming… this is the standard!"*).
Round 6 closed the caption and the frame-0 matte fix. Promoted from
the format lab (archived on Drive under Testing & Experiments) on 2026-09-01.
**Lab record:** `references/laws/cutout_NOTES.md` + `references/laws/SAM2.md` (the
matte pipeline, 6 rounds + v2/v3/v4) — derivations live there; this file is the
operating manual.

---

## What the chassis does

Miguel's background-removed silhouette stands **IN FRONT of** a full-bleed
1080x1920 explainer world — no seam, no split, no face slot. The world is behind
him and it is the whole frame. A cream die-cut **RIM** separates him from it
(confirmed round 2), and the world has **depth**: tiles live in three lanes (far
/ mid / near) that parallax behind and beside him — round 1: *"things happening
behind me was super cool"*.

The object is **THE SHELF**: a rack of real tool tiles that keeps going past the
frame edge. Every beat is the same rack seen differently — lit all at once (the
wrong mental model), one slot at a time (procedural disclosure), then tiling out
of frame while the context vessel stays low.

**The silhouette is the layout.** Safe areas, the caption seat and the stage zone
are all DERIVED from a measured matte envelope (`lib/envelope.json`), never typed.

---

## Running it

```bash
~/Documents/Workspace/.venv/bin/python chassis_gen.py                     # standing v4 matte, YouTube handle
~/Documents/Workspace/.venv/bin/python chassis_gen.py --handle tiktok_ig  # TikTok/IG
~/Documents/Workspace/.venv/bin/python chassis_gen.py --matte /path/to/matte.webm
```

| knob | default | what it does |
|---|---|---|
| `--handle` | `yt` | outro chip: `yt` = `@migueltorrezai`, `tiktok_ig` = `@migueltorrez.ai`. **Only the outro differs.** |
| `--matte` | the standing v4 (resolved, see below) | the matte is a **chassis INPUT**. In v5 it is the `_cut.webm` member of a SET |
| `--matte-mode` | `auto` | `layered` = v5 cut + rim layers; `baked` = the v4 single element; `auto` picks layered when a `_rim.webm` twin exists |
| `--proxy` | off | allow the RVM development stand-in matte. Never for a ship. |
| `--out` | `./build` | project root. The lab is never written to. |

| file | what it is |
|---|---|
| `chassis_gen.py` | the beat map, the lanes, the scenes, the caption build, staging, the geometry report |
| `lib/cutout_core.py` | the format primitives: plates, tiles, meters, marks, the envelope reader |
| `lib/cutout6_pillw.py` | the Chromium pill measurer (canon from `pipeline/captions.py`) |
| `lib/envelope.json` | the measured matte envelope — the layout is derived FROM this |
| `lib/cutout6_check.py`, `cutout6_containment.py`, `cutout6_matteswap_check.py` | the post-render gates (checks 21 FACE HF and 22 TREBLE live in `cutout6_check.py`) |
| `lib/cutout_media.py` | the VOICE source resolver + the 8-16 kHz band gate |
| `lib/cutout_facehf.py` | the face-noise instrument, and why its crop size is the whole instrument |
| `lib/cutout5_envelope.py` | re-derives `envelope.json` when the shipped matte's silhouette actually changes |
| `lib/cutout_depthfield.py` | **THE DEPTH FIELD** — the background, the lane geometry, the step schedule and the pop-behind card, frozen off the approved grokpublish render. No build writes its own any more |

---

## THE DEPTH FIELD (pinned, 2026-09-01)

The world behind him is **not a per-video decision**. It lives in
`lib/cutout_depthfield.py`, frozen off
the format lab (archived on Drive under Testing & Experiments) — the render Miguel approved and called
the format's best moment.

**Frozen, and a build may not change any of it:**

| | |
|---|---|
| tile sides | far **78**, mid **116**, near **148** |
| tile gaps | **30 / 36 / 44** (pitch 108 / 152 / 192) |
| cream between lanes | **26 px**, both gutters |
| band height | **394 px** |
| opacities | 0.34 / 0.66 / 1.00 |
| step distances | 46 / 112 / 208 px |
| tile ink | **0.50 x tile**, sized by INK AREA (`mark_img`) |
| edge fade | 46 px, on each lane's own canvas-wide wrapper |
| strip extents | 2 pitches lead-in, 2 pitches tail past the full travel |
| schedule | intro settle + **one step per spoken beat** (12 over a 40 s take) |

**Chosen per video, and only this:**

1. the **cast** — a roster of real registry marks, repeats allowed, no
   placeholders, and never the story's own subject mark (that belongs on the
   stage);
2. which mark the **pop-behind card** carries and on which beats it crosses —
   the beats where he NAMES the tool.

**The seat is the one thing still solved per body**, because a different day,
chair and lens put his silhouette somewhere else. `DF.seat()` slides the whole
RIGID stack down the legal band and scores each candidate on the **5th percentile
of the PER-FRAME gutter**; among the safe seats the one nearest the foundation's
own offset from the caption pill (**+63.6 px**) wins, so the band keeps its
approved relationship to the type. All three run-9 rebuilds landed within
**0.4 px** of that offset.

```python
import cutout_depthfield as DF
bf         = json.loads(Path(f"_df/bandframes_{VID}.json").read_text())
y0, seat   = DF.seat(bf, cap_bottom=..., plate_top=..., plate_scale=..., plate_left=...)
lanes      = DF.lanes_at(y0)
beats      = DF.step_beats(words, dur, n=12, fps=25)
html, g, n = DF.field(lanes, media, CAST, len(beats))
tweens     = DF.schedule(lanes, beats)
pop, ptw, r= DF.pop_behind("pop", lanes, media, "codex", [(t0, t1)])
```

The per-frame band extents come from
`python lib/cutout_depthfield.py <matte_*_alpha.webm> <out.json>` — always the
**alpha** layer, never `_rim` (its alpha is the 7 px dilated die-cut, so every
gutter reads 7 px short on both sides).

**THE CROWN IS A HEAD, NOT A CUT (2026-09-03, `supergrokplus`).** The seat is
derived from the envelope's `union.y0`, so the seat is only as good as the alpha
it is measured on. `pipeline/sam2/plate.py::window()` bottom-plants the crop and
sizes it off head height alone, and on a take where he sits high in the 4K master
that put the crop's top edge BELOW his cap: all 938 frames touched alpha row 0,
the envelope read the plate's own top row as the crown, and the pill was seated
the canon clearance above a FLAT ~490 px slice across his head. Miguel's read was
"the cutout video is clipping my head". LAW 44 could never have caught it — LAW 44
gates the plate's LEFT and RIGHT borders only.

**Production-v2 follow-up (2026-09-05):** the crop now aims for 64px above the highest measured crown, and `pipeline/matting/headroom.py` rejects ANY full matte frame below the 24px floor before export. Production rendering requires that exact guard PASS. This stronger check supersedes the historical median-based crop/quarter-of-samples tolerance described below.

Historical checks:

| where | what |
|---|---|
| `plate.py::window(head_top=…)` | the crop slides UP until the cap has `HEADROOM_ON_CANVAS` (24 px) of clear plate above it. `k` and `x0` are untouched, so head height and face centring are untouched; it spends the bottom of his chest, which the format runs off the canvas anyway |
| `platelib.build_plate` crown gate | refuses a plate whose `cap_top_on_plate * paint_scale` is under `HEADROOM_HARD_FLOOR` (8 px, the rim dilation) and records a `headroom` block |
| `cutout6_check.check_crown_clearance` (check 27) | measured on the DELIVERED mp4: the pill's bottom edge and the first row of him under it, every 0.5 s. Fails on a clearance under 24 px OR on the crown sitting on the plate's top row for more than a quarter of samples |

**And the clearance is derived with the pill that RENDERS.** The seat arithmetic
used `CAP_H` 108.2, the frozen fix5 seat constant, while the pill measures 114.59
— so every seat ever derived this way delivered **23.3 px**, not the 26.5 px it
claimed. It never mattered while the crown was a rounded arc. Per-video envelopes
now use `CAP_H_TRUE` for the clearance and keep `CAP_H` only for Law 31's audit of
the pill's own box.

**The outcome check is `cutout6_check.check_depth_field()`**, measured on the
emitted HTML, downstream of whoever wrote it. It re-derives tile size, pitch,
inter-lane gutter, band height and step count off the page and fails the build on
any drift. It exists because a guard inside this module cannot fire for a builder
who never calls it — the exact failure of run 9.

---

## THE MATTE (v4 convention — pinned)

The matte is **not produced by this chassis**. It is an input, and its production
path is a standing decision.

**STANDING DECISION (Miguel, 2026-08-31)** — production matte path:
**Modal A10G · fp32 · `sam2.1_hiera_base_plus` · chunk 350 / overlap 8 · v3 post
stack + cream rim.** ~7 min and ~$0.17 per 54s video.
MPS is dead (1.28x vs CPU, machine unusable). `hiera_large` is a statistical wash
at 1.44x the cost — not adopted. bf16 is 3x faster but a measurably different
contour, reserved for a possible bulk back-catalogue job and only after the full
gate chain plus Miguel's eyes.

**STANDING RULE — FRAME 0 (Miguel, 2026-08-31)** — a frame-0 point prompt may
never be a frame that ships. A prompted frame is a from-scratch segmentation off
dots while every other frame is a memory-conditioned propagation, so frame 0
arrives with a visibly rougher contour. The fix is a **warm-up lap** (prompt a
throwaway copy of f0, emit from local index 16, so the real frame 0 arrives as a
propagation with a 16-frame memory bank) plus **mirrored padding** on the
temporal median. **v4 IS v3 re-tracked under that rule** — it is the standing
matte.

### Prerequisite and resolution

Producing a matte needs the **Modal SAM2 tracking app deployed** (the tracker
does not run locally). The pipeline lives at `pipeline/sam2/`:

    pipeline/sam2/modal_app.py   the Modal A10G tracking app
    pipeline/sam2/plate.py       plate prep
    pipeline/sam2/track.py       the tracked run (warm-up lap lives here)
    pipeline/sam2/post.py        the post stack (mirrored-pad temporal median)
    pipeline/sam2/ship.py        render the shipped .webm
    pipeline/sam2/contain.py     the containment instrument for a matte swap

`chassis_gen.py` resolves `matte_sam2_rim_v4.webm` in this order, first hit wins:

    pipeline/sam2/mattes/matte_sam2_rim_v4.webm
    pipeline/sam2/matte_sam2_rim_v4.webm
    formats/_shared/matte_sam2_rim_v4.webm      (the lab archive, the fallback)

**The envelope was measured on v3 and deliberately NOT re-derived for v4**: the
fix is contained to the opening frames, and the raw tracks agree at the GPU
port's noise floor from frame 20 on (proved by `pipeline/sam2/contain.py`). That
is why v4 arrives through the EXPLICIT matte path — `pick_matte` asserts the
*default* against the envelope's source, and an explicit matte bypasses that
assertion by design. **Re-point the default and the envelope together, or
neither.**

**A matte swap cannot touch the document.** The composition names the constant
`assets/v/matte.webm`, so `index.html` diffs EMPTY across a swap — that is the
first half of the swap proof. The second half is the decoded-pixel check against
a null control (`cutout6_matteswap_check.py`).

---

## THE MATTE IS A LAYER SET (v5 — pinned, 2026-09-01)

Two defects Miguel confirmed in the 13 cutout remakes were fixed together. Both
were invisible to every geometry gate the format had, because neither is
geometry.

### Defect 1 — his face was re-encoded into the matte

v4 staged ONE `<video>`: a webm whose RGB was his face at **VP9 crf 24** with the
cream rim blended into it, displayed at 1188x990 from a 1080x900 source. So his
face went through a second lossy generation and then a 1.10 browser upscale.

Measured on `deepresearch` with `lib/cutout_facehf.py` (skin-only crop):

| stage | face HF |
|---|---|
| `plate_wide_25.mp4`, x264 crf 16, 1080x900 | 6.98 |
| `matte_deepresearch_rim.webm`, VP9 crf 24 | 6.88 |
| the finished remake, after the 1.10 upscale + delivery encode | **5.65** |
| the published original (4K, downscaled to the 1080 canvas) | 6.50 |

The remake's face was **13 % SOFTER than the published original** — the chain
was not adding grain, it was smearing detail away, and the 1.10 upscale did most
of the damage.

**The fix, in three parts** (all in `pipeline/sam2/ship.py` §V5):

1. the RGB is re-cut **from the 4K master at the display box** (1188x990) at
   x264 crf 12, so nothing upscales in the browser;
2. it is encoded **near-lossless** (VP9 crf 10), with everything outside a 4 px
   dilation of the trim flooded flat so the bits go to him;
3. the **cream rim becomes its own layer** instead of being painted into the
   picture that carries his face.

The chassis now stacks two ordinary alpha videos:

```
z 59   assets/v/matte_rim.webm    flat cream #FFFDF9, alpha = the 7px DILATED trim
z 60   assets/v/matte.webm        his pixels, alpha = the trim
```

The composite is arithmetically the v4 picture — cream shows only where the
cutout is transparent. **The drop-shadow moves to the rim layer, and that is why
the rim's alpha is the whole dilated body and not a ring**: a ring-shaped alpha
casts a ring-shaped shadow. It is still ONE filter, so Law 3 holds.

Result on the rebuilt `deepresearch`: plate 6.62 -> cut webm 6.60 -> **finished
short 6.63**, i.e. **1.9 % from the published original's 6.50** and 1.0008x its
own plate.

**Why the chassis does not mask a plate video with an alpha video.** `ship.py`
also emits `_alpha.webm`, and the obvious design is a high-quality plate
`<video>` masked by it at composite time. Chromium cannot: `mask-image` takes an
*image*, not a media element, and `mask: url(#svg)` over a `<foreignObject>`
video is not reliably rasterised. The only working route is a per-frame
`<canvas>` or WebGL pass, which breaks HyperFrames' deterministic
seek-and-capture contract and re-imposes exactly the per-frame compositing cost
**Law 3** forbids (eight zero-blur drop-shadows once took a 4.5 min render to a
projected 3 hours). So the multiply happens offline, once, near-lossless, and the
browser only stacks. `_alpha.webm` remains the measurement surface.

### Defect 2 — the voice was the 16 kHz analysis track

`publish_batch.py` copied the cut's `audio.wav` into every package as
`source_audio.wav`. That wav is the **analysis** track: 16 kHz mono, so its
Nyquist limit is 8 kHz. Ten of the thirteen remakes mixed from it.

8-16 kHz band power relative to full band:

| | 8-16 kHz |
|---|---|
| the cut master `audio.m4a`, 48 kHz stereo | -30.6 dB |
| the published original short | -31.2 dB (0.6 dB off master) |
| the remake, mixed from the wav | **-49.0 dB** (18.4 dB off master) |
| the rebuilt remake | **-30.8 dB** (0.2 dB off master) |

The fix is `lib/cutout_media.py`: `resolve_voice` picks the full-quality 48 kHz
track and **refuses** a low-rate one by name; the analysis wav ships as
`analysis_16k_mono_DO_NOT_MIX.wav`; and check 22 gates the finished mix's
8-16 kHz band to within **6 dB** of the voice master's.

**The stale staged asset caught this fix out once, and the guard is the lesson.**
The first fixed run resolved the right 48 kHz master, recorded it in
`_geom_cutout.json`, and then kept the 16 kHz `stage/v/voice.m4a` already sitting
there — because the matte's mtime rule ("re-copy only when the staged file is
OLDER") said the wrong file was newer. `stage_voice` now stamps the source path,
re-probes the STAGED file's rate, and measures the STAGED file's own band.

### Defect 1, residual — THE LAYER BOX MUST BE INTEGRAL (v5.1, 2026-09-01)

v5 fixed *where his face pixels come from* and left *where they land* wrong. The
box was DERIVED from `PLATE_SCALE`, and a scale that is not a clean multiple of
a 1080x900 plate produces a fractional one. `grokprice` (`PLATE_SCALE 1.0592`)
painted its **1144x954** encoded layers into

    left:-32.0px; top:966.7px; width:1143.9px; height:953.3px

so Chromium bilinear-resampled every frame of his face. It is the only one of
the thirteen remakes that did not reach parity with its own plate:

| | face HF | vs plate |
|---|---|---|
| `plate_display_1144x954.mp4` | 7.470 | — |
| `matte_grokprice_v5_cut.webm` | 7.401 | 0.991 — the encode is fine |
| the render, fractional box | 6.492 | **0.869** |
| the plate under that exact transform | 6.467 | 0.866 — reproduced to 0.4 % |
| **the render, integral box (v5.1)** | **7.477** | **1.001** |

Nothing upstream was implicated. The whole 13 % was the box.

**THE BOX IS NOW THE PLATE'S ENCODED SIZE, NOT THE SCALE.** `chassis_gen.BOX_W`
/ `BOX_H` are probed off the staged layer (`cutout_media.probe_wh`), the offsets
are whole pixels derived from them, and `PLATE_SCALE` is snapped to the encoded
height over `PLATE_H` so `box_h == PLATE_H * PLATE_SCALE` exactly. For
`grokprice` that is 1144x954 at (-32, 966) with `PLATE_SCALE 1.06` — 1.06 is not
a nudge of 1.0592, it is the truth of the file, which was rendered 954 px tall
from a 2160 px crop. The chassis' own 1.10 already lands 1188x990 at (-54, 930),
so this is a **no-op for it and the promotion diff stays empty**.

**THE GUARD — `chassis_gen.guard_plate_box(stage, stage_dir)`**, called before
every other guard in `main()`, is the single assertion that would have caught
this before the render rather than after it. Four checks, because each one alone
forces a resample:

1. box width and height are WHOLE PIXELS
2. `left` and `top` are WHOLE PIXELS (`966.7` was enough on its own)
3. the box equals the ENCODED dimensions of `assets/v/matte.webm`
4. ... and of `assets/v/matte_rim.webm`

It raises `SystemExit` and names the fix. The result is recorded as
`plate.box` in `_geom_*.json`, and `lib/cutout6_check.py::check_plate_box`
(check **23**) re-asserts it from that record so any port's build can be audited
without re-running its generator. Face HF (check 21) only catches the outcome,
after a 90-second render, and only just: 0.869 is 0.131 off parity against a
0.12 tolerance.

### What v5 does NOT change

- **The post stack still runs in plate space.** BLEED 8 / MORPH_K 2 /
  SIGMA_HI 4.0 / FEATHER 0.55 / RIM_PX 7 are frozen in 1080x900 pixels and
  `lib/envelope.json` was measured against them; the finished soft alphas are
  resampled up to 1188x990 afterwards, which is what the browser did to the v4
  matte anyway. **So the envelope stays valid and v5 is a contained swap.**
- **The document still names constants.** `assets/v/matte.webm` and
  `assets/v/matte_rim.webm` are literals, so a matte swap still leaves
  `index.html` byte-identical.
- **`--matte-mode baked` reproduces v4 exactly**, and with the default v4 matte
  (which has no `_rim` twin) `auto` resolves to `baked` — which is why
  `chassis_gen.py` with no arguments still reproduces
  `references/builds/chassis/cutout/fix6/index.html` **byte for byte**.

**An envelope re-derivation must never run against a v5 `_cut` or `_rim` file** —
those are at display scale and `cutout5_envelope.py` reports plate-space pixels.
Re-derive from `_alpha.webm` with the display scale divided out, or from an
`--emit legacy` pass.

---

## Format laws

1. **THE SILHOUETTE IS THE LAYOUT.** Safe areas derive from the measured envelope,
   never typed. Every scene atom is either provably clear of the silhouette union
   on every frame, or explicitly declared `behind`.
2. **NEVER OCCLUDE HIM.** No foreground element crosses his silhouette; captions
   may sit over the TORSO only and must clear the head band.
3. **NO FILTER STACKS ON THE CUTOUT.** Rims, glows and outlines are baked into the
   matte offline. One `drop-shadow` is the ceiling.
4. **CREAM ONLY WHILE THE SUBJECT IS DARK.** A ground within ~20% of the subject's
   clothing value is banned.
5. **THE DOCK IS AN ANCHOR.** An element arriving beside the presenter is centred
   on the FREE COLUMN's axis, not the frame axis. Flanking pairs are normalised to
   the same size, taken from the narrower side.
6. **THE MATTE IS AN ASSET WITH A VERDICT.** Every cutout ships with a decoded edge
   review at 4+ timestamps and a written verdict. Dark-on-dark subjects are a known
   failure mode and must be caught before the build, not after.
6b. **HIS FACE IS NEVER RE-ENCODED TWICE, AND NEVER UPSCALED** (v5, 2026-09-01):
   the RGB is cut from the master AT the display box and encoded near-lossless,
   and the cream rim is a separate layer. Gated by check 21 FACE HF: the finished
   short must sit within 12 % of its own plate on the skin-only crop.
6c. **THE VOICE IS THE 48 kHz MASTER, NEVER THE ANALYSIS WAV** (v5, 2026-09-01):
   a 16 kHz mono track has an 8 kHz Nyquist ceiling. Gated by check 22 TREBLE:
   the mix's 8-16 kHz band must sit within 6 dB of the voice master's.
7. **RECORD FOR THE FORMAT.** A cutout wants a half-body frame with headroom,
   **shoulders visible**, and NOTHING dark directly behind the shoulders. A set
   rule, not a build rule.
8. **NO PLACEHOLDER TILES** (Law 10, hardened by Law 14): tile fields always carry
   REAL provider logos — repeat rather than leave a gray blank, and never a generic
   glyph.
9. **LABEL + OBJECT = ONE BLOCK** (Law 9): a name moves with its object, always.
10. **TILE CORNER CONSISTENCY** (Law 13): every mark on a tile gets the same rounded
    corner treatment. No pointed-corner odd-one-out.
11. **PRODUCT MARK OVER COMPANY MARK** (Law 16): when a specific product is
    discussed, use ITS logo, never the parent company fallback.
12. **MARK CONTAINMENT IS A QC CHECK** (Law 17): a logo must stay inside its box.
    `cutout6_containment.py` is the instrument.
13. **EDGE FADE** (Law 8): elements CUT by the frame edge get a thin alpha fade,
    not a hard clip. Cards and UI never touch the edges at all.
    **DEPTH LANES MUST USE THE CHASSIS LANE PATTERN.** Tiles go inside a per-lane,
    canvas-wide wrapper carrying the 90deg fade — `cutout_core.lane_wrap()`,
    `EDGE_FADE = 46` — and the build calls `cutout_core.guard_edge_fade(html)`.
    A generator that parents tiles straight to a full-frame layer ships them
    hard-chopped AND makes the guard blind, because with no wrapper there is no
    clipping container for it to inspect (run 9, both cutouts, all gates green).
    The outcome check that does not care who built the page is Gate 1's
    `edgefade` DOM sweep in `pipeline/geometry_audit.py`.
14. **ROUNDED-BAR FILLS: CONTINUOUS PILL ONLY** (Law 11): one pill-shaped fill,
    min-width = track height, no detached ticks or end markers.
15. **THE DEPTH FIELD IS THE CHASSIS'S, NOT THE BUILD'S** (2026-09-01). Tile
    sizes, gaps, inter-lane gutters, band height, opacities, step distances and
    the step schedule come from `lib/cutout_depthfield.py` and nothing else. A
    build chooses the CAST and the pop-behind mark/beats; everything else is a
    constant. Gated by `cutout6_check.check_depth_field()` on the emitted HTML.
16. **THE POP-BEHIND IS PART OF THE FORMAT** (2026-09-01). A live app card
    crosses a depth lane at his shoulder on the beat where he names the tool,
    is occluded by him, and re-emerges on the far side. **The host lane clears
    for the length of the crossing** — two objects at the same distance read as
    clutter, not as depth. A cutout without it is missing the detail Miguel
    named ("the nice little animation you used to pop behind me").

---

## Known traps

- **The headrest.** A black chair behind a black t-shirt defeats segmentation.
  Round 2 still had the headrest visible on the right at times — the fix is a
  spatial exclusion region, not just a better model.
- **`stage_assets` only re-copies the matte when the staged file is OLDER than the
  source**, so a newer *stale* staged matte is silently kept. Delete
  `stage/v/matte.webm` before a swap (the lab's `cutout6_matteswap.sh` does this
  first, for exactly this reason). v5 adds a `stage/v/_matte_source.txt` stamp so
  a change of source or of layering mode drops both staged files regardless of
  mtimes — **and the same trap bit the voice fix on its first run**, which is why
  `stage_voice` stamps, re-probes and re-measures the STAGED file.
- **A layer box derived from `PLATE_SCALE` is a resample waiting to happen.** Any
  port whose scale is not a clean multiple of 1080x900 gets a fractional box and
  a sub-pixel offset, and the browser then resamples his face for the whole take
  — `grokprice` lost 13 % of its plate's detail this way and every geometry gate
  passed. The box must be the **encoded** size of the staged layer, at integer
  offsets; `guard_plate_box` fails the build otherwise. Never hand-type a box.
- **The face-noise instrument is only honest on a crop that is provably inside his
  face.** `cutout_facehf.py` at k=1.6 (the crop the original defect audit used) is
  wider than his head and lands on the cream die-cut edge, which the split-format
  originals do not have at all; identical face pixels read 1.00x at k<=0.7 and
  1.39x at k=0.8. Quote k=0.55 (`K_SKIN`) for face noise; k=1.6 means "face plus
  edge" and nothing else.
- **The caption seat is FROZEN at the fix5 numbers** and the build asserts it
  (`CAP_Y, ZY1, CAP_H == 949.5, 868.9, 108.2`). It also asserts the pill is the
  canonical one. Both are build failures, not review notes.
- **Captions behind the platform UI** was Morgane's exact complaint at
  `cutout_fix2` (caption bottom ~96%). The current seat sits at 52.4% of frame
  height — well inside Law 12's 72% line. Do not move it down.
- **A limb sliced flat by the frame edge (ROUND-4 LAW 44).** The bust base
  spilling past both side edges is the format working; a HAND doing it is the
  defect. Because the cream keyline is dilated from the same alpha, a hand cut by
  the canvas ends in a bare vertical slice with no outline, and it reads as an
  amputation. Three staged cutouts shipped it with every gate green
  (`impossibletask` 1.08 s + 0.16 s, `kimiram` 0.80 s + 0.20 s) — three of the
  four windows are UNDER the 2.5 s stride a clerk spot-checks at, so **sampling
  cannot clear this class**. `pipeline/edge_clip_check.py` sweeps every frame of
  the take in ~40 s, structurally: at each visible edge column the bust run is
  the one touching the bottom row, and a defect is a run DETACHED from it or that
  run climbing >30 canvas px above the take's own shoulder baseline. (A
  bottom-15 % exclusion was tried and flags 100 % of frames — the shoulder is
  16.8 % of the silhouette at the edge column.) It is a post-ship gate in
  `pipeline/sam2/ship.py` (`--allow-edge-clip "<reason>"` to override in writing)
  and check 26 in `cutout6_check.py`. And note the interaction with the trap
  below it: `plate.py` sizes the head for a plate shown 1:1, but this chassis
  paints it at 1.10, so a window derived straight from `plate.py` is ~10 % too
  tight and buys the clip as well as the head-parity error.
- **THE OVER-WIDE PLATE — the standard remedy for LAW 44.** A limb *leaving
  frame* is not the defect; the shoulders do it on every frame and the keyline
  traces them into the edge. The defect is that the trim is cut by the **plate's
  own border**, so the 7 px rim is cut with it and the shape enters the frame
  with no outline on that side. A re-crop cannot fix it in general: on `kimiram`
  no 1.2:1 window satisfied the law at any column (defect frames 117 / 120 / 76 /
  20 / 26 / 24 for a visible-left master edge from 650 to 1000 — an optimum of
  20, never a zero), because the resting shoulder line falls from master row 1616
  at x 900 to 2062 at x 700 and an edge further out sits where his body is a
  sliver. **The remedy: keep `k`, the head scale and the face centre exactly, and
  extend the master crop sideways so the plate is WIDER than the visible frame
  and sits at a more negative left offset.** Nothing on canvas moves — same
  visible master window, same head parity, same face centre, and every frozen
  post parameter (BLEED 8, MORPH_K 2, SIGMA_HI 4.0, FEATHER 0.55, RIM_PX 7) stays
  valid because a plate px is still the same physical size. kimiram: box
  1188x990 at (-54, 930) → **1485x990 at (-351, 930)**, plate 1350x900 from
  master crop `2820x1880+128+280`, 78 canvas px of margin between the plate
  border and the leftmost silhouette of the whole take. Two consequences the
  chassis had to absorb, both recorded in `plate.json`'s `overwide` block:
  **(1)** the plate is no longer 1.2:1 — that ratio exists to make `plate.py`'s
  head-parity solve one-variable, and here the scale is already solved and
  inherited, so the aspect is free; **(2)** the box is no longer CENTRED, so
  `cutout_geometry()` reads `box_left` from `plate.json` instead of computing
  `(W - box_w) / 2`. The integral-box law is unchanged and still asserted: box ==
  the encoded size of every staged layer, at whole-pixel offsets.
- **TWO MORE THINGS AN OVER-WIDE PLATE MOVES,** found shipping the second one
  (`impossibletask`, 2026-09-02: box 1188x990 at (-54, 930) → **1386x990 at
  (-252, 930)**, plate 1260x900 from master crop `2660x1900+270+260`, the crop
  extended on the LEFT ONLY so the right border does not move, 53.1 canvas px of
  margin between the plate border and the leftmost limb-band silhouette of the
  whole take, `k` and the visible master window 753.63-2826.37 identical to
  0.01 px). **(3) PLATE SPACE IS NO LONGER 1080x900.** Anything that rescaled a
  matte alpha "back to plate space" with a hard-coded 1080 now squashes the
  silhouette horizontally and hands its consumer a body 20-28 % narrower than the
  one on screen. `cutout_depthfield.measure_band_frames` probes the alpha's own
  encoded size instead, and `_gutters` derives its multiplier from the record
  (`k_eff = 900 * plate_scale / bf.plate.h`) rather than trusting the caller's
  `plate_scale`, so both conventions and every band record already on disk map
  identically. A per-video envelope script must do the same: hold PH at 900 and
  DERIVE the width from the matte's aspect. **(4) THE STAGED MATTE MUST BE
  STAMPED BY CONTENT, NOT BY NAME.** `ship.py --out` always writes the same
  filenames, so a generator that skips the copy when `stamp == str(src)` never
  refreshes a re-tracked matte. That shipped: the round-4 widening landed at
  10:25 and `stage/impossibletask_cutout/v/matte.webm` stayed at the 20:42
  lift-plate matte, so two renders composited the matte the widening had
  replaced while check 26 swept the session file and reported the new one — a
  green gate on a video that did not contain what the gate measured. The stamp
  now carries size and mtime on a second line (line 1 stays the bare path,
  because `check_edge_clip` reads it to find the alpha sibling to sweep).
- **Temporal matte flicker** is the historical failure. The SAM2 tracked pass with
  the warm memory bank + 3-frame temporal median + 0.6px feather is the fix; any
  new matte must pass the same flicker instrument.
- **Charts use standard flat-top bars** (Law 15): no rounded/pill bars, and never a
  line traced across bar tops.
- A future variant worth building (Morgane's suggestion, logged): this format with
  a **real screen recording** behind him.

---

## Proof of promotion

`chassis_gen.py` (default `--handle yt`, default v4 matte) reproduces the approved
round-6 page **byte-for-byte**:

| chassis output | lab round-6 output | result |
|---|---|---|
| `build/cutout/index.html` | `references/builds/chassis/cutout/fix6/index.html` | identical |

The staged matte is `matte_sam2_rim_v4.webm` (recorded in
`build/_geom_cutout.json` as `"matte": "matte_sam2_rim_v4.webm [alpha 57.7%
transparent @24s]"`). `--handle tiktok_ig` differs on **exactly one line**: the
`#o-handle` div.

**v5 does not break this.** The v4 matte has no `_rim.webm` twin, so `--matte-mode
auto` resolves to `baked` and `Stage.video(rim=None)` emits the v4 markup
character for character; the diff was re-run on 2026-09-01 and is still
identical. What DID change in that run is the audio: the chassis now stages
`formats/_shared/hermesinfinite/source_cut_master.mp4` (48 kHz stereo, 8-16 kHz band
-30.06 dB) instead of that directory's 16 kHz `source_audio.wav`.

---

## ROUND-4 LAWS (Miguel, 2026-09-02) — global, enforced in Gate 1

Four laws added by round 4 bind this chassis. They are not format opinions; the
full text is `STANDARD.md → ROUND-4 LAWS`, and the instrument is
`pipeline/geometry_audit.py → check_layout()`, which walks the WHOLE subtree of
every active clip and judges every element that carries an `id` (in this factory
an id is the author saying "this is a thing"; id-less SVG internals are strokes
of a drawing, not objects in an argument).

| law | Gate 1 finding | the rule |
|---|---|---|
| 38 — emphasis matches its target | `enclose` | NEVER a ring, an ellipse or a circle, on any target. TEXT ON AN IMAGE (post card, screenshot, document, UI capture) takes the marker HIGHLIGHT: `rgba(198,103,72,0.32)`, radius 6 px, wiped open left-to-right over 0.34 s, ONE FILL PER LINE, `data-overlap-ok`. A DRAWN OBJECT or scene TYPE takes BOXING — the run-3-8 panel border flip (`.node.hero { border-color: TERRA_L }` tweened via `borderColor` over 0.38 s), which is explicitly fine and still owes `cramp` its 16 px gutter to NEIGHBOURS. ERROR: a ring around a thing; a box whose target is image text. WARNING: a highlight on a drawn object. Opt out with `data-container`; declare a raster the namer misses with `data-asset` |
| 39 — names | `sidelabel` | A name goes ABOVE or BELOW the thing it names, centre inside the object's horizontal extent ±15 %. Declare the pair with `data-label-for="<object id>"` (ERROR); an undeclared geometric weld is a WARNING |
| 40 — arrows | `anchorline` | Connectors into ONE target terminate on that target's VIRTUAL BOUNDING RECTANGLE, at the same height (±4 px) or mirror-symmetric about its axis. Declare with `data-connect-to="<target id>"` |
| 41 — spacing | `cramp`, `crossing` | Gutter aim 24 px, refusal floor **16 px**; a connector never crosses printed type (judged on the type's core band). Nothing overlaps unless authored as one block — `data-block="<name>"`. A welded label, a container's contents, a paragraph and a ≥3 identical-shape series are blocks automatically |

ROUND-4 LAW 37 (a pointing cue raises the source post, with the highlight) is a
SCRIPT law and is checked at plan time by `pipeline/pointing_cues.py`.

ROUND-4 **LAW 44** (the silhouette never touches a side edge above the bust) is a
MATTE law, not a DOM one, so it is enforced where the matte is made and where it
is audited: `pipeline/sam2/ship.py` refuses to ship a clipping matte, and
`cutout6_check.py` check 26 re-asserts it on the staged layer. Full take, every
frame — see *Known traps*.

ROUND-4 **LAW 42** (a mark leaves when its beat is done) reaches the DOM lane
through a declaration, not through a reviewer's judgement. The whiteboard lane
names its long-lived marks in `board_anchors=`; a DOM build declares one by
stamping **`data-anchor="1"`** on the element — the same shape as LAW 40's
`data-connect-to` and LAW 39's `data-label-for`. Anything alive for more than
**40 %** of the runtime without that attribute is the defect the law is named
for ("the perplexity logo stays and just bothers the entire flow"); anything
carrying it is a CLAIM, answerable at the gate, that this mark is the spine of
the argument and exits the moment the argument leaves it. First declared on
`kimiram` (round 5, 2026-09-02): the Kimi `K` dwells 4.9–34.4 s ≈ **59–62 %**
because every figure in that video is the price of running *that* model — the
round-4 viewer test read it as an anchor by hand, and it is now declared as one
in `kimiram_scene.SCENE_ANCHORS`.

Escape hatches, used only with a written reason: `data-overlap-ok`,
`data-block`, `data-container`, `data-spacing-ok`.
