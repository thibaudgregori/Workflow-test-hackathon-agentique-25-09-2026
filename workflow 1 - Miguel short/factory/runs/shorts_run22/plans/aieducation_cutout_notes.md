# aieducation — CUTOUT lane notes (run 22)

Project `shorts_run22/projects/aieducation_cutout`, staged to
`shorts_run22/staging/tiktok/aieducation_cutout.mp4`.

## The seat

Measured, not typed. `gen/aieducation_cutout_envelope.py` swept every frame of
the shipped alpha (803 frames, 1584x990) and returned `CAP_Y 870.2 / ZY0 192.0 /
ZY1 786.4`, a 594.4 px stage zone against a 552.0 px content band. The cap at
k = 1.0 binds, so the scene is seated unscaled at `top = 192.0, left = 0.0` —
**the split's own origin**. The two DOM lanes therefore paint the same canvas
rects, which makes LAW 51's cross-lane parity exact rather than approximate, and
makes the cold Phone Test crop the objects the plan means.

Crown gate: 0 of 803 frames put his topmost alpha row on the plate's top row.
Production headroom guard: 0 unsafe frames, min top clearance 25.3 px against a
24 px floor. Rendered crown clearance measured on the delivered file: min 63.0
px, median 70.0 px over 66 samples.

## The depth field

Roster is the plan's `cutout_logo_lanes`, unchanged and topical: `chatgpt`,
`claude`, `gemini`, `cursor`, `grok`, `lovable`. Six marks against the field's
stride of 7, gcd 1, so every lane cycles all six with no repeat knob. Band
seated at 991.5..1385.5 with a 164.0 px margin; 53 tiles; 9 steps at the
foundation's pulse (29.32 s of usable span / 3.167 s).

The three cast marks appear on the STAGE and in the LANES. That is the plan's
own written instruction (`cutout_logo_lanes_note`), and the run-9 "subject mark
in the depth field" defect has no target here: this video's subject is the
anatomy HEART, a drawing, and no drawing can be a registry key.

**No pop-behind, and it is a measurement rather than an omission.** Cutout law 16
keys the crossing to the beat where he NAMES the tool. A lexical sweep of all six
lane marks over the whole tight transcript returns ZERO hits — the only proper
nouns in the take are "X" (the platform, card chrome, deliberately not a lane
mark) and "AI". There is no legal beat to key a crossing to, and the build
refuses rather than improvising one.

## Two format-side repairs, both on the emitted output only

The sealed module on disk was not touched. The split author is reading the same
file and has already shipped from it.

**1. `reveal_drawn_ink`** — reproduced from the split unchanged. The module's
`draw()` raises `strokeOpacity` but never element opacity and uses a fixed
`strokeDasharray:100`, so three sealed strokes never appear and every drawn
stroke rests as a broken dash. LAW 51 makes copying this repair mandatory: a
stroke that draws in one lane and is invisible in the other is exactly the
cross-lane divergence the law names.

**2. `reframe_go_closer`** — the ONE camera move, re-aimed. The clerk CONFIRMED a
`cramp_overlap_clipping` row against the SPLIT for it (`review/final_aieducation.json`,
S1, 6.15–6.90 s, settled 6.40–6.85): the source card zooms 1.92x and its own post
text is sliced at both frame edges while held, losing the leading "A " of line 1
and the "@" of "@threejs". A confirmed defect is not reproduced in a new render.

Same instant (5.92), same scale (1.92), same origin (486, 372), same duration
(0.56 s), same easing. Only the AIM changes, from the module's `x:54, y:-72` to
`x:-49.7, y:-111.7`, which centres the SCREENSHOT the plan says to go closer into
and keeps every edge of it inside the frame and inside the measured stage zone.
Measured at the held instant: the screenshot lands at canvas
`98.4, 206.5 .. 981.6, 759.5` (883.2 x 553.0 px, 1.92x its size at rest) with the
stage zone at 192.0..786.4 and a 24 px frame margin.

The card's CHROME leaves by FADING over 0.30 s — the X mark, the handle, the
hairline, the post body and the spent marker fill — and the cream panel dissolves
(background to transparent, border to 0). That is the plan's own sentence ("the
card's chrome may leave the frame to pay for it") paid honestly instead of
sliced, and it is also what clears GLOBAL LAW 8: the panel was the one painted
box straddling a frame edge with no alpha ramp.

**This is a deliberate divergence from the split, and the clerk should read it as
one.** LAW 51 binds the parts of a shared object to move together, and they do:
everything inside `#card-wrap` still moves as one. What differs is where the
camera points and how the chrome exits, and it differs because the split's aim is
a confirmed defect.

**3. `unclip_shot`** (same discipline, one line). `#pc-shot` is the screenshot's
frame; the module gives it `overflow:hidden` purely to round the raster's
corners, and the `<img>` inside is authored at exactly the content size with
`object-fit:cover`, so the clip crops no pixel. GLOBAL LAW 8 cannot tell a
cosmetic clip from a hard-chopped lane, and fading a framed picture's edges would
be the wrong answer, so the clip is removed on the emitted string and the radius
moves onto the raster (8 px = the 10 px frame radius less the 2 px border). The
page then has no unmasked clipping container at all; the three lane wrappers all
carry their mask.

## The matte

Consumed as it shipped. No Modal matting call of any kind was made by this lane;
the only Modal call it makes is the render.

Stage 17's HOLD was a path-resolution bug (the batch shipped into the shared
sessions root; `matte_review.py` only looked run-local), fixed at source by the
repair round. Stage 18's SAM2 fallback refused and was never installed. The haze
gate then held the FIRST shipped matte and the contour was redrawn and re-shipped.
The current metrics (`review/matte_aieducation/metrics.json`) are clean and are
GATED by the build rather than quoted: background haze longest run **0.0 s**,
hold false, frames over floor 0; frozen_edge runs **[]**, hold false; chair band
p50 **143**; extra components 0; holes 1 sampled frame; IoU p05 0.9612.
