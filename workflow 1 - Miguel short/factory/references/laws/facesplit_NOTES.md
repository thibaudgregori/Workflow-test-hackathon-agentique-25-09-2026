# FACESPLIT — full-face into 50/50 (format lab, 2026-08-29)

Source: `format_lab/hermesinfinite/` (the shipped cut of "Hermes Agent can now
have literally infinite tools", 54.1s, 185 words). Three renders, 1080x1920,
same audio, same back half, same palette — only the FORMAT changes.

| | what it does | render | duration / size |
|---|---|---|---|
| v1 | EARLY + HARD. Full-face for 11.9s with four modest punch-ins, then a HARD CUT into the split landing exactly on the word "procedural", key term already in the zone | `out/facesplit_v1.mp4` | 54.11s / 55.3 MB |
| v2 | LATE + ANIMATED. Full-face for the whole setup (19.7s, seven punch-ins incl. the key term at 1.18 on his face), then the frame physically COMPRESSES into its band as a designed beat | `out/facesplit_v2.mp4` | 54.11s / 61.8 MB |
| v3 | ROUND TRIP. v1's opening exactly, then at 50.18s the zone lets go and the face grows back out of its band to own the frame for the sign-off, handle chip over the footage | `out/facesplit_v3.mp4` | 54.11s / 58.1 MB |

Staged to `~/Movies/Shorts Factory/Format Lab/facesplit_v{1,2,3}.mp4`.

## The build

**Two crops, one camera.** `facesplit_tight.mp4` (crop 1216x2160 @x=1267 →
1080x1920) and `facesplit_band.mp4` (crop 2206x2160 @x=772 → 1080x1058), both
cut from the same 4K master and both spanning its FULL height. That last part is
the whole trick: because neither crop loses vertical range, the tight video
scaled by k = 1057.5/1920 = 0.5508 is pixel-for-pixel the band video's framing,
so the compress in v2 lands on the band exactly and the source swap underneath is
invisible. `dy` is solved from the seam (`dy = SEAM_PX - (1-k)*ORIGIN_Y`), never
typed. The provided `face_full.mp4` was not used — a crop with unknown parameters
would have made that geometry an eyeball job.

**Punch grammar.** Scale only, on a fixed origin at the head (50% / 37.7%), so
nothing can drift (Law 1). Two verbs: `push` (0.16s in on power4.out, then it
HOLDS at the new level) and `punch` (0.14s in, 0.50s settle back to the hold).
Every time is a word start from `transcript_words.json`, and the scheduler tracks
the running hold so the transition always begins from a known scale. Range used:
1.05–1.18.

**Back half.** One object for the whole split: AVAILABLE TOOLS (a shelf of real
brand marks that later extends until it bleeds off both frame edges = infinite)
over a CONTEXT WINDOW card with a CONTEXT USED meter. Procedural disclosure is
staged physically — one tool at a time flies in and sits at the card's centre,
then leaves; "tools consume context" fills all six slots and completes the meter;
"context is finite" caps it; "very picky" leaves one survivor which slides to the
centre and drains the meter; "all the tools we will ever need" explodes the shelf
past both edges while the meter holds at its marker; "MCP servers" names the
shelf. Makers beat (Nous Research + HERMES chip) plays over a faded stage so the
object's state survives it.

**SFX** (ElevenLabs, generated once, reused across all three): `facesplit_cut`
(the hard switch + the meter hitting its ceiling), `facesplit_slide` (the v2
compress + the shelf explosion), `facesplit_tick` (a tile seating), and
`facesplit_lift` (v3's return). Mixed at 0.18, voice 1, bed 0.065. Measured
margin (p85 − p15, mono 16k s16le, 33ms): v1 20.73 dB, v2 20.73, v3 20.43 — all
inside the approved corpus band.

## What works

- **The format itself is strong.** A talking-head open buys ~10–20 seconds of
  attention that the split format currently spends on a diagram nobody is looking
  at yet, and the switch to the split then reads as "now here comes the thing"
  instead of "this is the layout".
- **The punch-ins carry the front half.** Four of them across 12 seconds is
  enough; the settle-back `punch` on a rhetorical question ("...all at once?")
  and the step-and-stay `push` on a claim ("crack the code") do different jobs and
  the difference is legible.
- **v2's compress is the best single moment in the batch.** Because it is real
  geometry rather than a dissolve, the face does not change size, position or
  crop at the swap — the frame just closes around him. It reads as a camera move,
  not an edit.
- **Landing the hard cut ON the key word** (v1: the composition is already split
  when he says "procedural") is much better than cutting in the pause before it.
- **The shelf bleeding off both edges** is the cheapest possible "infinite" and it
  works; the meter holding at its marker while the shelf triples is the argument.

## What fought me

- **GSAP `fromTo` asymmetry.** A property present in `fromVars` but absent from
  `toVars` animates back to the element's current value — which, after the
  `tl.set(...,{opacity:0},0)` every entrance uses, is zero. The outro rule drew
  itself and then faded itself out, and it survived the first stills pass because
  it is only 11px tall. Every property a `fromTo` touches now appears on both
  sides (`grow()`).
- **Two layout modes means captions have two homes.** A pill must never be alive
  while the layout it is anchored to is moving, so the caption builder takes the
  transition times as forced phrase breaks AND clamps any pill that still spans
  one. Without the clamp, v2's "...needs them." pill sat in the lower third while
  the frame compressed around it.
- **Build order across a late entrance.** v2 skips the whole first act of the
  stage, so the shelf has to exist before the first tile can fly off it; the
  entrance and the fill are derived from the entrance time rather than hard-coded
  to the word ("Tools consume") that drives them in v1/v3.
- **The v3 sign-off lockup wanted the house rule** (mark / rule / handle), but on
  footage a 150du rule between the caption pill and the handle reads as an
  underline of the pill. Over the face the lockup is the two type lines only.
- **Playwright's `wait_for_function` never resolves against these pages** while a
  plain `evaluate` poll does — worth knowing before someone debugs a "hanging"
  stills pass for twenty minutes.

## Ranking (mine)

1. **v2 (late + animated).** Best hook — 20 seconds of face is exactly how the
   references open, the key term landing at 1.18 on his own face is stronger than
   the same term as a card, and the compress is a beat the other two do not have.
   Cost: the explainer is compressed into 30 seconds and the fill beat feels
   slightly rushed. Still the one I would ship.
2. **v3 (round trip).** The ending genuinely lands better — the CTA is a person
   asking, at full size, which is what a follow actually is. It loses to v2 only
   because its front half is v1's. **The return is the finding here**: it is worth
   taking into whichever opening wins, including the current production format.
3. **v1 (early + hard).** The safest and the least interesting. The cut on
   "procedural" is a good edit, but at 11.9s it gives up the format's main
   advantage almost immediately and from there it is the existing split short.

## Laws this format would need if adopted

1. **ONE SWITCH PER SHORT (plus at most one return).** The value is in commitment;
   a format that flips modes repeatedly is the mode-switch reference (ref2), a
   different format with different rules.
2. **THE SWITCH LANDS ON A WORD, never in a pause.** Cut on the first syllable of
   the claim the zone is about to show, or start the animated compress on the
   breath immediately before it.
3. **PUNCH-INS ARE SCALE ONLY, ON A FIXED HEAD ORIGIN, AND THEY HOLD.** 1.05–1.18,
   0.14–0.16s in, and then still. No pans, no drift, no origin changes — a moving
   origin is a dolly and it fights the cut. Never more than one punch per ~3s.
4. **CAPTIONS HAVE TWO HOMES AND NEVER STRADDLE.** Lower third (y=1560) in
   full-face, the seam in split; a pill spanning a switch gets clamped.
5. **THE FULL-FACE HALF CARRIES NO GRAPHICS.** No lower-thirds, no floating
   labels, no chips over the face except the sign-off lockup. If a beat needs a
   graphic, that beat belongs after the switch — that is what the switch is for.
6. **BOTH FACE CROPS COME FROM THE SAME MASTER AND SPAN ITS FULL HEIGHT.** This is
   what makes an animated transition exact instead of approximate; a tight crop of
   unknown provenance forces a dissolve.
7. **THE SIGN-OFF LOCKUP OVER FOOTAGE DROPS THE RULE** and keeps ≥100px of air
   below the caption pill (the seam law's equivalent when there is no seam).
8. **Law 20 applies to the SPLIT's opening, not the video's.** In this format the
   hook is Miguel; the first thing the visual zone ever shows must still be a
   subject with a state (here the key term, then the object), never an empty
   vessel — the card enters alone, centred, and is filled within ~2s.

## Files

- generators: `facesplit_lib.py`, `facesplit_v{1,2,3}_gen.py`
- sfx: `facesplit_sfx.py` → `sfx/facesplit_{cut,slide,tick,lift}.mp3`
- projects: `v1/`, `v2/`, `v3/` (assets symlinked to `stage/`)
- inspection: `facesplit_stills.py`, contact sheets in `probe/`
- derivatives: `v/facesplit_{tight,band}.mp4`, `v/facesplit_audio.m4a`

---

# FIX ROUND 1 — 2026-08-30 (verdict: REDESIGN, brief misunderstood)

Miguel's review (`format_lab/REVIEW_2026-08-30.md`):

> **facesplit — REDESIGN (misunderstood brief)**
> - Wanted: DYNAMIC switching between full-face and 50/50, back and forth,
>   whenever what's relevant changes — NOT one committed transition.
> - Zooms far, far too aggressive. Derive the cap empirically (Global Law 1).
> - Visuals otherwise "remarkable".

Deliverable: **`out/facesplit_fix.mp4`** — 1080x1920, **25fps**, 1353 frames,
54.12s, 63.6 MB, sha256 `cbf1b728…`. Staged to
`~/Movies/Shorts Factory/Format Lab/Fixed/facesplit_fix.mp4`.
Files: `facesplit_fix_lib.py`, `facesplit_fix_gen.py`, `facesplit_fix_cam.py`,
`facesplit_fix_check.py`, project `fix/`, assets `stage_fix/`,
plate `v/facesplit_fix_cam_25.mp4`, evidence `probe/decoded/`,
measurements `facesplit_fix_check.json` + `facesplit_fix_cam_report.json`.

The v1/v2/v3 generators and renders above are **untouched**; this is a parallel
build, so the two rounds stay comparable.

## What changed against the review

**1. The format is now a MODE ENGINE, not an opening plus a split.**
Thirteen segments, twelve switches, face when the moment is him talking to you
and split only while a visual is earning the zone:

| # | t | mode | span | why |
|---|---|---|---|---|
| 1 | 0.00 | FACE | 3.08 | the hook: the man making the claim |
| 2 | 3.08 cut | SPLIT | 2.68 | THE CRAM — every tool slams into the context window, meter pegs at 100%. That picture IS "loads every tool all at once?" |
| 3 | 5.76 cut | FACE | 5.68 | "Well, spoiler, they don't." The wrong picture is deleted on the cut |
| 4 | 11.44 **COMPRESS** → 11.88 | SPLIT | 10.84 | lands ON "procedural"; key term, then disclosure staged physically, then the meter completes on "finite" |
| 5 | 22.72 cut | FACE | 2.76 | "the best way to handle your context is by-" — advice from a person |
| 6 | 25.48 cut | SPLIT | 4.12 | "-being VERY PICKY": ring, cull, one survivor |
| 7 | 29.60 cut | FACE | 1.12 | a 1.1s seize |
| 8 | 30.72 cut | SPLIT | 3.64 | lands on "Nous": mark, lab, chip |
| 9 | 34.36 cut | FACE | 1.24 | a 1.2s seize |
| 10 | 35.60 cut | SPLIT | 4.92 | lands on "ALL of the tools": the shelf runs off both edges, meter does not move |
| 11 | 40.52 cut | FACE | 3.12 | "If you have a Hermes agent…" — second person |
| 12 | 43.64 cut | SPLIT | 6.56 | MCP lockup, the 2% tick on "bloating", the light wave |
| 13 | 50.20 **EXPAND** → 50.64 | FACE | 3.52 | he takes the frame back for the sign-off |

**20.9s face / 33.2s split.** Segments run 1.12s to 10.84s, so the switching has
a rhythm rather than a metronome. Format law 1 from round 1 ("ONE SWITCH PER
SHORT plus at most one return") is **repealed** — it was the misreading.

**2. ZERO zooms. Not one.** Global Law 1 said the punch-ins were far too
aggressive; the fix is not smaller punch-ins, it is none. Both rest states
render at their derived plate scale forever:

| | face_frac | head_frac | vs FRAMING contract |
|---|---|---|---|
| SPLIT band | 0.192 – 0.201 | 0.254 – 0.258 | want 0.2007 / 0.2585 |
| FACE full-bleed | 0.417 – 0.442 | 0.544 – 0.566 | want 0.4282 / 0.5514 |

Round 1 shipped up to **0.509 face_frac / 0.723 head_frac**. The split band is
now inside the reference reel's own card-mode band (0.196–0.238) with shoulders
and upper torso in frame, and the full-face beats sit at the physical ceiling of
a 9:16 crop, never past it.

**All the punch energy is the switch.** wide→max is a **2.133x head-height
change delivered as a single-frame cut** — FRAMING rule 4, and the takeover
grammar Miguel said he prefers over animated creep.

**3. The compress/expand survives as the SIGNATURE move, used twice.** Eleven
switches are hard cuts; the two that are the statement are animated: the frame
closing into its band to land on the key term, and letting go for the sign-off
(v3's finding, kept — the CTA is a person asking, at full size).

**4. 25fps** (Global Law 6). Authored `data-fps="25"`, rendered at 25, every
switch and every SFX on the 0.04s grid. Measured duplicate rate in the delivered
mp4: **0.15% (2 frames)**, down from the source's 16.8%.

**5. SFX LAW v2.** The tamed palette at its class constants (structure 0.120,
detail 0.077), twelve one-shots in 54s, `data-start` = the event frame with **no
lead/lag offsets** (the palette is onset-trimmed, so the old `-0.06` compensation
would now double-count). Four of the face flashes are deliberately **silent** —
an effect on every switch is untamed however quiet it is. Speech margin
**20.87 dB** (p85−p15, mono 16k s16le, 33ms), inside the approved run-7 band.

**6. Global Law 3** — both CONTEXT USED meters reach by `width` with a live
`border-radius`; verified round-capped at the 0.18 reading on a decoded frame.
**Global Law 4** — the seven extra shelf tiles do not exist on screen until
"ALL of the tools"; cap, hold marker and MCP lockup all wait for their word.
**Global Law 5** — nothing moves that a word did not ask for.

## The finding worth keeping: A PLATE IS AUTHORED AT THE RESOLUTION OF ITS LARGEST ON-SCREEN SIZE

The first build of this round used two plates (`face_wide_25` for the band,
`face_max_25` for full-bleed) and ran the compress by scaling the wide plate up
2.133x. It renders, and at 8x on a decoded still the first frame of the move is
**visibly softer than the frame before it** — brow hair and lash detail smear,
because 1080 source px are being stretched across 2304.

The fix is not a crossfade and not a mid-move source swap. Both modes are the
same full-height slice of the master, both bottom-aligned on the canvas, so they
are related by ONE scale about the canvas's **bottom centre** (1920/900 =
2.13333, and 2592/2.13333 = 1215 master px = the ceiling crop). Render that one
window at **2304x1920** — its largest on-screen size — and the whole format is a
single `<video>` with `transform-origin: 50% 100%` at scale 1.00 (face) or
0.46875 (split). Nothing is ever upscaled, at either rest state or anywhere in
between; there is **not one source swap in the composition**, and the re-shot
comparison at 11.40 vs 11.44 is indistinguishable.

`facesplit_fix_cam.py` builds it, reusing `_shared/build_face_crops.py`'s
de-conform model verbatim.

## Other things that cost time

- **The head measurement.** A hand-rolled luminance scan read every frame
  0.03–0.21 too high: the black chair above the cap and the black t-shirt below
  the chin sit in the same luminance band as the subject — the identical failure
  `MATTE.md` documents for segmentation. Use `_shared/measure_head.py`.
  And judge on `face_frac`: `measure_head`'s `head_frac` falls back to
  `face_h * 1.42` when the cap scan misses, but this subject's measured ratio is
  **1.287**, so the fallback reports ~+0.026 of pure arithmetic.
- **`gsap_exit_missing_hard_kill`.** The render runs four workers seeking
  non-linearly, so every exit now carries a `tl.set(opacity:0)` at its landing.
  Both `out()` and `unfly()` emit it; the lint went 2 errors → 0.
- **Captions need a blackout, not just a break.** A pill has one home per mode
  (seam 1020 / lower third 1560) and twelve forced breaks keep it from straddling
  a cut — but during the 0.44s of an animated move it has no home at all, so
  `build_captions` takes blackout windows and slides a pill's start past them.
- **The zone grew** from 460du to 544du (the band is 900px, not 1057px), so each
  block declares its ink extent and is centred in the new zone rather than
  re-typing coordinates.

## Format laws, rewritten for the fix round

1. **SWITCH WHENEVER RELEVANCE CHANGES.** Face for claims, questions, asides,
   second person and the sign-off; split only while a visual is earning the zone.
   Segments may be as short as ~1s. (Repeals round 1's law 1.)
2. **EVERY SWITCH LANDS ON A WORD**, and every switch time is a frame time.
3. **HARD CUT IS THE DEFAULT SWITCH.** The animated compress/expand is reserved
   for the two beats where the switch is itself the statement.
4. **NO ZOOM.** Both modes render at their derived plate scale. The switch is
   the punch (2.133x head height); a punch-in inside a mode is redundant and
   re-breaks Global Law 1.
5. **ONE CAMERA.** A single plate authored at its largest on-screen size, with
   `transform-origin: 50% 100%`. No source swaps, ever.
6. **THE FULL-FACE MODE CARRIES NO GRAPHICS** except the sign-off lockup, which
   keeps 100px of air below the caption pill (measured: pill box bottom 1612,
   handle top 1716).
7. **ONE PERSISTENT ZONE OBJECT.** The stage spans every split segment so its
   state survives each face excursion, and nothing inside it animates while it is
   hidden.
8. **Law 20 applies to the SPLIT's opening.** Here that is 3.08s: the card lands
   ON the cut frame and is full 1.4s later — never an empty vessel.

---

# FIX ROUND 2 — 2026-08-30 (verdict: "really fantastic work!", one thing wrong)

Miguel's round-2 review (`format_lab/REVIEW_2026-08-30.md`, ROUND 2):

> **facesplit**: "really fantastic work!" but full-face still TOO ZOOMED.

Deliverable: **`out/facesplit_fix2.mp4`** — 1080x1920, **25fps**, 1353 frames,
54.12s, 56.2 MB, sha256 `b4d6cca7…`. Staged to
`~/Movies/Shorts Factory/Format Lab/Fixed2/facesplit_fix2.mp4`.
Files: `facesplit_fix2_lib.py`, `facesplit_fix2_gen.py`, `facesplit_fix2_cam.py`,
`facesplit_fix2_check.py`, project `fix2/`, assets `stage_fix2/`,
plate `v/facesplit_fix2_cam_25.mp4`, stills `probe/fix2/`,
delivered frames `probe/decoded2/`, measurements `facesplit_fix2_check.json` +
`facesplit_fix2_cam_report.json`. Round 1's build is untouched and still renders.

## What did NOT change

Everything he liked. **The thirteen-segment mode engine and all twelve switch
times are byte-identical to round 1** — same map, same 20.91s face / 33.20s
split, same two animated signature moves (COMPRESS 11.44 lands on "procedural",
EXPAND 50.20 for the sign-off), same SFX set at the same frames, same zone
object and its whole choreography, same captions machinery, same 25fps,
same audio mix (margin 20.87 dB, identical to round 1's measurement).
The SPLIT band is also unchanged: measured 0.192–0.201 face_frac against 0.2007.

## The one change, and why it is not a crop

**Round 1's FACE mode was already ON the 0% standard.** Its window was 1215
master px wide, face_frac 0.4282, head_frac 0.5514; `_shared/ZOOM_STANDARD.md`'s
0% window is 1216 px at face_frac 0.4304, centred 4 px away. So "reframe the
full-face segments on the 0% standard" is a **no-op as a crop instruction** —
and it cannot be otherwise, because 0% is a physical floor: a 2160-tall master
cannot give a full-bleed 9:16 window wider than `2160 x 9/16 = 1215` px
(`FRAMING.md` §4). There is no wider full-bleed crop anywhere in the source.

The lab had already written down the only remaining lever, twice, and round 1
had broken it:

> FRAMING.md §4 — "the zoom cap cannot be a crop parameter. **It is a
> composition law:** a face-led rest state is a plate that does not fill the
> canvas."
> FRAMING.md §5 hard rule 2 — "**A full-bleed face is never the rest state.**"

Round 1 used the full-bleed CEILING as a rest state for six segments and 20.9s.
Round 2 obeys the rule. FACE keeps the full canvas **width** (it still bleeds
396 px off each side) and gives the bottom **360 px** back to the cream ground —
the mirror of what SPLIT already does with the top 1020 px:

| | plate on canvas | master window | face_frac | head_frac | eye depth |
|---|---|---|---|---|---|
| round 1 FACE | 1080x1920 at y 0 | 1215 px | 0.4282 | 0.5514 | 40.1 % |
| **round 2 FACE** | **1872x1560 at y 0** | **1495 px** | **0.3479** | **0.4480** | **32.5 %** |
| SPLIT (both rounds) | 1080x900 at y 1020 | 2592 px | 0.2007 | 0.2585 | — |

**A 19 % smaller head**, 280 more master px of him across the frame, and the eye
line lifts off dead centre into the upper third. Measured on the delivered mp4
(MediaPipe, `_shared/measure_head.py`): face 0.335–0.358 where round 1 read
0.417–0.442. 0.348 sits just under the widest full-face frame in Miguel's own
reference reel (`FRAMING.md` §3: its full-face mode runs 0.359–0.419), i.e. the
zoomed-out end of the band his own reference validates — not a new invention.

Centring also adopts ZOOM_STANDARD's **union** centre (x=1878 over 64 frames)
instead of round 1's 14-frame median (x=1874), so the format now shares the
standard's horizontal reference. 4 px.

## Re-derived: the compress-into-band math

The two modes are still the SAME full-height 2592 px slice of the master, so
they are still related by ONE uniform scale — but they are no longer both
bottom-aligned, so `transform-origin: 50% 100%` no longer maps one onto the
other. The fixed point is solved instead of assumed:

```
s        = 900 / 1560 = 15/26 = 0.5769231
origin_y (1 - s) = 1020   ->   origin_y = 1020 x 26/11 = 2410.909 px
check    : 2410.909 + s (1560 - 2410.909) = 1920.000     (the band's bottom)
           2410.909 + s (   0 - 2410.909) = 1020.000     (the band's top)
origin_x = 936 px (element centre; 1872 x s = 1080 exactly)
```

So the camera is still ONE `<video>` with ONE animated property. The plate is
authored at **1872x1560 = its largest on-screen size** (round 1's finding, kept
verbatim): at FACE the visible 1080 canvas px map **1:1** onto 1080 plate px, at
SPLIT the whole plate lands in 1080x900 as a pure downscale. Nothing is upscaled
anywhere, and the compress/expand are still real geometry, not a dissolve. The
switch is now a **1.733x** head-height change (was 2.133x) — still far above
FRAMING rule 4's 1.15x mode-switch threshold, so it is still a hard cut, and
this format still contains **zero** punch-ins and zero creep. ZOOM_STANDARD's
5 % / 10 % ladder is deliberately unused here: facesplit punches by switching
modes, not by cropping tighter.

## Two things the change gave away for free

1. **The caption pill now rides the seam in BOTH modes.** Round 1 already parked
   the face pill at y=1560 (a lower third, over his chest); in round 2 that y IS
   the boundary between footage and ground. Two caption homes stopped being two
   rules and became one: *the pill sits on the seam, and the seam moves with the
   mode* (1020 split / 1560 face). Nothing in `build_captions` changed.
2. **The sign-off lockup lost its scrim.** In round 1 the lockup had to sit on
   the footage and needed a 460 px black gradient under it to be legible. It now
   stands on the cream ground: scrim deleted, handle in INK, "daily AI" in TERRA,
   pill bottom 1612 → handle top 1716 (the format's 100 px of air, unchanged),
   last baseline clearing the frame bottom by ~103 px. **Nothing is painted over
   his face at any point in the video any more** — format law 6, now literal.

## Format laws, amended for round 2

Round 1's laws 1, 2, 3, 5, 7, 8 stand as written. Two are rewritten:

4. **NO ZOOM — and the FACE mode is not full-bleed either.** Both modes render
   at their derived scale forever. FACE is a plate that stands ON the ground
   (1872x1560 at y 0, cream below), never a plate that covers the canvas.
   A full-bleed face is the 0 % ceiling and the ceiling is not a rest state.
6. **THE FULL-FACE MODE CARRIES NO GRAPHICS AT ALL.** Not "except the sign-off
   lockup" — the lockup lives on the ground now, below the seam, and so does the
   caption pill's lower half. There is no scrim and no type over the face.

## The finding worth keeping

**When a subject is "too zoomed" and the crop is already at the source's floor,
the remaining zoom lives in the LAYOUT, not the camera.** A 9:16 full-bleed crop
of a 16:9 master magnifies the head by 3.16x by construction and no re-crop
touches that. The only way further out is to stop being full-bleed — give some
of the canvas back to the design ground and let the plate be smaller than the
frame. FRAMING.md said this in round 1 and the build ignored it because
"full-face" was read as "fills the frame". It does not have to. Measure the
floor first (`ZOOM_STANDARD.md`), and when you are already standing on it, the
next lever is the page.

---

# Fix round 3 — `facesplit_fix3.mp4` (2026-08-30)

Morgane's review + Miguel's rulings + Global Law 12. Staged at
`~/Movies/Shorts Factory/Format Lab/Fixed3/facesplit_fix3.mp4`.
Files: `facesplit_fix3_lib.py`, `facesplit_fix3_gen.py`, `facesplit_fix3_cam.py`,
`facesplit_fix3_check.py`, project `fix3/`, assets `stage_fix3/`,
plate `v/facesplit_fix3_cam_25.mp4`, stills `probe/fix3/`, measurements
`facesplit_fix3_check.json` + `facesplit_fix3_cam_report.json`. Rounds 1 and 2
are untouched and still render.

## What did NOT change (fourth round running)

**The thirteen-segment mode engine and all twelve switch times are byte-identical
to rounds 1 and 2** — same map, same 20.91 s face / 33.20 s split, same two
animated signature moves (COMPRESS 11.44 landing on "procedural", EXPAND 50.20
for the sign-off), same SFX set at the same frames, same zone choreography, same
25 fps, same audio mix (margin **20.87 dB**, identical to rounds 1 and 2 to the
centibel). Zero zooms, zero punch-ins, zero creep — third round running.

## 1. FULL-FACE = THE RAW 0 % CROP, FULL BLEED

Round 2's face-plate-on-a-cream-ground is dead by ruling. FACE fills the frame
again on ZOOM_STANDARD's 0 % window. This is **proved on pixels, not on a
landmark model**: decode the same timestamp from the delivered render and from
`_shared/face_zoom00_25.mp4` (the 0 % standard plate itself) and correlate.

| t | MAE above the pill (y<1250) | best vertical shift |
|---|---|---|
| 1.20 | 3.22 / 255 | **0 px** |
| 8.40 | 3.16 | **0 px** |
| 23.60 | 3.05 | **0 px** |
| 41.60 | 3.29 | **0 px** |
| 52.20 | 3.19 | **0 px** |

Zero offset at every probe: the face mode is not *close to* the 0 % window, it
**is** the 0 % window. The residual ~3/255 is h264 plus the 0.08 % width-rounding
difference between the two builds. face_frac 0.4282 / head_frac 0.5514.

Why the MediaPipe rows now need a wider face-mode tolerance, honestly stated: the
caption pill lands ON his jaw (see §2 — Law 12 leaves nowhere else), landmark 152
is partly occluded, and face_frac reads 2-4 % low on wide-pill frames. Measured
side by side against the reference plate at the same timestamps, ours reads
0.4015 where the un-captioned reference reads 0.4168 on the *same frame*. That is
the instrument, not the framing, which is why the pixel test above is the
authority and `TOL_FACE` says so in the code.

## 2. ONE CAPTION POSITION — GLOBAL LAW 12, DERIVED

Morgane: *"not a fan of the captions drastically changing position between
modes."* Round 2 had two homes (1020 split / 1560 face) and the face one measured
**84 %** — a Law 12 fail. Round 3 has ONE home for all 54 s and both modes:

```
CAP_BOTTOM = 1380 px = 71.88 % of frame height
```

Measured on the delivered mp4 by finding the terracotta pill by exact colour:

| mode | t | pill top | pill bottom | bottom % | x0 | x1 |
|---|---|---|---|---|---|---|
| face | 1.60 | 1292 | **1380** | 71.88 | 254 | 824 |
| face | 7.20 | 1270 | **1380** | 71.88 | 364 | 716 |
| face | 23.60 | 1270 | **1380** | 71.88 | 252 | 828 |
| face | 41.20 | 1270 | **1380** | 71.88 | 312 | 768 |
| split | 4.40 | 1272 | **1380** | 71.88 | 218 | 862 |
| split | 17.60 | 1270 | **1380** | 71.88 | 298 | 782 |
| split | 31.60 | 1270 | **1380** | 71.88 | 302 | 778 |
| split | 45.20 | 1270 | **1380** | 71.88 | 274 | 806 |

**Distinct bottom edges across the whole video: exactly one, 1380.0 px. Spread
0.00 px.** Bottom 1380 <= the 1382 limit; every pill's right edge <= 862 < 918
(the platform rail column) and left edge >= 218 > 162.

### Why 1380 and not the "preferred 40-65 % band"

Because with a full-bleed 0 % face the preferred band is his face. Measured over
64 frames (`_shared/zoomstd_samples.json`) on the full-bleed canvas:

```
head top   min 192   median 295   max 327
chin       min 1282  median 1382  max 1448
```

**His chin sits ON the 72 % line.** So no legal caption position in a full-bleed
face frame clears his face at all; the only question is which part of him it
lands on, and the LOWEST legal pill is the one that clears his mouth (~1200) by
180 px and sits on the jaw/neck. Everything else in this round follows from
pinning that one number.

### What had to move so BOTH modes could host it: the split band

With the pill pinned, the split band gets one job — its head must start below the
pill and his chin must never be cut. For a full-height window the FACE
magnification is fixed by arithmetic for ANY crop width
(`1080 / (1920/2160) = 1215` master px visible), so the free parameter is the
crop width, and the crop width sets the band height. Solve:

```
head_top_split(worst) = SEAM + 192 s > 1380      chin(worst) = SEAM + 1448 s < 1920
SEAM = 1318 (the pill's own centre line)
CROP_W 2970 -> plate 2640x1920 -> s = 1080/2640 = 9/22 = 0.4090909
band 1080x785.45 at y 1318..2103.45
```

| | plate on canvas | master window | face_frac | head_frac | head % of 1920 |
|---|---|---|---|---|---|
| round 2 FACE | 1872x1560 at y 0 | 1495 px | 0.3479 | 0.4480 | 44.8 % |
| **round 3 FACE** | **1080x1920 full bleed** | **1215 px** | **0.4282** | **0.5514** | **55.1 %** |
| round 2 SPLIT | 1080x900 at y 1020 | 2592 px | 0.2007 | 0.2585 | 25.8 % |
| **round 3 SPLIT** | **1080x785 at y 1318** | **2970 px** | **0.1752** | **0.2256** | **22.6 %** |

Measured on the delivered mp4: split face_frac 0.1650-0.1752 against 0.1752;
face 0.4005-0.4328 (pill-occluded, see §1).

Worst-case clearances, over all 64 sampled poses: pill bottom 1380 to the highest
split head top 1396.5 = **16.5 px of air**; lowest split chin 1910.4 to the frame
bottom = **9.6 px**. Both hold on the extreme frame, not just the median.

**The band bleeding 183 px off the bottom is the point, not a side effect.** Law
12 bans meaningful content in the bottom 28 % (1382-1920); what lands there is
his black t-shirt — in BOTH modes. His head, the pill, and every graphic sit
above 72 %.

### The fixed point, re-solved

The two rects are not bottom-aligned any more (the band bleeds), so:

```
origin_y (1 - s) = 1318   ->   origin_y = 1318 x 22/13 = 2230.462 px
check top    : 2230.462 + s (   0 - 2230.462) = 1318.000
check bottom : 2230.462 + s (1920 - 2230.462) = 2103.455
origin_x = 1320 px (both rects centred on the canvas axis)
```

Still ONE `<video>` and ONE animated property. The plate is authored at its
largest on-screen size (2640x1920 = the face mode), so FACE maps 1080 canvas px
onto 1080 plate px 1:1 and SPLIT is a pure downscale. Nothing is upscaled.

### The pixel-exactness detour worth writing down

The first round-3 render measured the pill bottom at **1378 on one pill and 1380
on the others**. Cause: an inline-block's static position depends on the parent
line box's baseline, and the pill's height was fractional (`1.28 x font-size` in
design units), so `translateY(-100%)` translated by a fractional amount and
Chrome rounded differently per font size. Three changes made it exact — the
container kills its own line box (`font-size:0; line-height:0`), the pill takes
`vertical-align:bottom` so no baseline creeps in, and every vertical measurement
is an INTEGER number of CSS px (padding 19, line-height `round(1.28 x fs)`).
Re-measured: one distinct bottom edge, spread 0.00 px.

**A "stable caption position" is a pixel claim, so measure it as one.** Averages
hide a 2 px bob.

### The right-rail budget

Law 12 also bans meaningful content in the right 15 % column (x>918) for
y 30-95 %, and the pill lives at y 1270-1380 — inside that band on all three
platforms. So the pill is budgeted to **756 px wide** (right edge exactly 918),
down from the old 975 px, and the font floor drops 19 -> 17 du so the longest
phrase still fits on one line. `cap_font` **floors** to 0.1 du instead of
rounding: rounding up pushed one pill to 757 px, and 918 is a law line, not a
target. Widest delivered pill: 756 px. 52 pills, all single-line.

## 3. THE "ROUNDED SHAPE THINGY" — found and removed (Global Law 11)

Decoded at 28 s: it is the CONTEXT USED meter. The rounded track carried a
**detached square end-marker** (`-cap`, 5x24 du, terracotta, sticking out above
and below the track) and a **detached hold tick** (`-hold`, 3 du) — at the 0.72+
fill reading it renders as a hammer head glued to a pill. Law 11 is explicit:
*one pill-shaped fill, min-width = track height, no detached ticks or end
markers, remaining progress = empty track only.* Both are deleted. Their beats
moved onto the object itself: "finite" is now the fill ARRIVING at 100 % plus a
1.02 tick on the card, "no longer / without bloating" is the fill dropping to
20.5 % and moving 2 %. The delivered meter is one terracotta lozenge with two
true semicircular ends and nothing else.

## 4. The Google Drive ring at ~28 s — centred

Off its tile by exactly one plate border width. A `position:absolute` child is
laid out against its parent's **padding** box, so the ring's -8 du inset was
measured from inside the tile's 2 du border and the ring landed 3.75 px right and
down. Arithmetic, before and after:

```
round 2  ring left = tile_left + 3.75 - 15    -> ring centre = tile centre + 3.75
round 3  ring left = tile_left + 3.75 - 18.75 -> ring centre = tile centre + 0.00
```

`left/top = px(-(RING_GAP + PLATE_BORDER))`. Scanline check on the delivered
frames at 27.90 s, inner gap between the ring stroke and the tile: round 2
**L/R 10/16, T/B 11/17** (6 px asymmetric both ways); round 3 **L/R 14/12**
(2 px, antialiasing on a mid-move element).

## 5. The sign-off keeps its scrim back

The face is full bleed again, so the lockup sits on footage and his t-shirt is
black — round 1's 460 px bottom gradient returns, handle in white, "daily AI" in
TERRA_2. Law 12 exempts the outro @handle chip and this is the ONLY thing in the
build that uses the exemption: the caption pill still ends at 1380 through the
sign-off, and the lockup starts at 1716, so it keeps 336 px of air below the pill.

## Delivered numbers

`1080x1920 · 25/1 CFR · 1353 frames · 54.12 s · 55.6 MB · rendered in 40 s`
duplicate frames 2 (0.15 %) · speech margin 20.87 dB (p85 -16.07 / p15 -36.94)
FRAMING **PASS** · LAW 12 CAPTION BAND **PASS** · LAW 7 0 % ALIGNMENT **PASS**

## The findings worth keeping

1. **When a law and a framing ruling collide, solve for the law and move the
   layout.** "Caption bottom <= 72 %" and "full-bleed 0 % face" are incompatible
   as stated — his chin IS the 72 % line — so the caption goes to the lowest
   legal line and the SPLIT BAND is what moves to meet it. The band height was
   never the sacred number; the switch map was.
2. **A composition constant that must not move needs integer geometry.** Inline
   layout plus fractional heights will silently give you two positions where you
   asked for one, and only a pixel measurement will tell you.
3. **When your measuring instrument is inside the frame, it stops being an
   instrument.** The caption pill occludes the chin landmark, so MediaPipe cannot
   arbitrate face framing in this build. Correlating against the standard's own
   plate can, and gives a stronger answer (0 px offset) than a tolerance ever did.

---

# Fix round 4 — `facesplit_fix4.mp4` (2026-08-30).  EXACTLY 50/50.

Round 3 verdict, Miguel: **"no longer 50/50... not good for us."**  Round 3 had
re-proportioned the two zones (1318 visual / 785 band) to buy the single caption
seat.  Wrong trade — 50/50 IS the format.  Round 4 restores it as an exact
number, keeps the seat, and pays for both by moving the SPLIT MAGNIFICATION.
Staged at `~/Movies/Shorts Factory/Format Lab/Fixed4/facesplit_fix4.mp4`.
Files: `facesplit_fix4_lib.py`, `facesplit_fix4_gen.py`, `facesplit_fix4_cam.py`,
`facesplit_fix4_check.py`, project `fix4/`, assets `stage_fix4/`, plate
`v/facesplit_fix4_cam_25.mp4`, stills `probe/fix4/`, measurements
`facesplit_fix4_check.json` + `facesplit_fix4_cam_report.json`.  Rounds 1-3 are
untouched and still render.

## What did NOT change (fifth round running)

The thirteen-segment mode engine and all twelve switch times are byte-identical
to rounds 1-3 — same map, same 20.91 s face / 33.20 s split, same two animated
signature moves (COMPRESS 11.44 landing on "procedural", EXPAND 50.20 for the
sign-off), same SFX set at the same frames, same Law-11 meter, same 25 fps, same
audio mix (margin **20.87 dB**, identical to rounds 1-3 to the centibel).  Zero
zooms, zero punch-ins, zero creep — fourth round running.  The FACE mode is the
raw 0 % full-bleed crop and is pixel-unchanged (see §3).

## 1. THE SEAM IS 960.  EXACTLY.  AND IT IS ASSERTED, NOT INTENDED.

```
visual zone   y    0 .. 960     512.0 design units
face band     y  960 .. 1920    the other half
```

Measured on the DELIVERED mp4 by scanning the frame's outer margins (x<60,
x>=1020 — nothing in the zone reaches those columns below y 500) for the last row
of exact cream `#F6F1EA` before the footage starts:

| mode | t | boundary | % of frame | cream dev @959 | cream dev @961 |
|---|---|---|---|---|---|
| split | 4.40 | **960** | 50.000 | 3.00 | 38.91 |
| split | 17.60 | **960** | 50.000 | 3.00 | 39.37 |
| split | 27.60 | **960** | 50.000 | 3.00 | 38.92 |
| split | 31.60 | **960** | 50.000 | 3.00 | 38.63 |
| split | 45.20 | **960** | 50.000 | 3.00 | 38.50 |
| face | 1.60 | none (full bleed) | — | 127.86 | 127.99 |
| face | 41.20 | none (full bleed) | — | 128.23 | 128.34 |

**Distinct seam rows across the whole video: exactly one, 960. Spread 0 px.
zone 960 / band 960.**  The lib refuses to import if that stops being true:

```python
if SEAM_PX != 960.0 or (1920.0 - SEAM_PX) != SEAM_PX:
    raise SystemExit("THE SPLIT IS NOT 50/50: ...")
```

plus asserts on `ZONE_H * S == SEAM_PX`, on `s == 0.625`, on
`origin_y == 2560`, on both origin checks, and on the plate's scale origin
sitting on the composition axis.  `write()` then re-checks the EMITTED HTML: one
`.tz` height, one `.scap` seat, and no caption carrying its own `top:`.

## 2. THE CAPTION SEAT DID NOT MOVE — AND THAT IS WHAT "66-70 %" MEANT

Miguel asked for the single seat at "~66-70 % of frame height, on the torso in
both modes."  Round 3's seat already IS that seat, measured by its centre line:

```
CAP_BOTTOM = 1380 px   bottom 71.88 % (the Law-12 limit)   CENTRE 69.0-69.6 %
```

| mode | t | pill top | pill bottom | bottom % | **centre %** | x0 | x1 | centre x |
|---|---|---|---|---|---|---|---|---|
| face | 1.60 | 1292 | **1380** | 71.88 | 69.58 | 254 | 826 | 540 |
| face | 7.20 | 1270 | **1380** | 71.88 | 69.01 | 364 | 716 | 540 |
| face | 23.60 | 1270 | **1380** | 71.88 | 69.01 | 252 | 828 | 540 |
| face | 41.20 | 1270 | **1380** | 71.88 | 69.01 | 312 | 768 | 540 |
| split | 4.40 | 1272 | **1380** | 71.88 | 69.06 | 218 | 862 | 540 |
| split | 17.60 | 1270 | **1380** | 71.88 | 69.01 | 298 | 782 | 540 |
| split | 31.60 | 1270 | **1380** | 71.88 | 69.01 | 302 | 778 | 540 |
| split | 45.20 | 1270 | **1380** | 71.88 | 69.01 | 274 | 806 | 540 |

**One distinct bottom edge, 1380.0 px, spread 0.00 px, across both modes and the
whole 54 s.**  Every pill's centre x is 540.0 — the composition axis — and every
right edge (max 862) clears the platform rail column at 918, every left edge (min
218) clears 162.

Raising the BOTTOM to a literal 70 % (1344) was tried on paper and rejected: it
drags the pill's top to 1234, which is above his chin at its highest pose (1282),
so the pill would climb back onto his jaw in face mode — the exact thing round 3
solved and Miguel approved ("it lands on his chest").  The centre-line reading is
the one that satisfies both the number he gave and the landing he described.

## 3. WHAT A 50/50 BAND COSTS, AND WHY THE PILL LANDS ON HIS CAP

This is the honest part.  With the seam pinned at 960 the split mapping is
`canvas_y = 960 + s * plate_y`, and two things stop being negotiable (poses from
`_shared/zoomstd_samples.json`, 64 frames, on the full-bleed 0 % canvas: head top
192/295/327, chin 1282/1382/1448):

* `head_top_split = 960 + 192 s <= 1152` for ANY s < 1.  Round 3's answer —
  "his head starts BELOW the pill" — is arithmetically **unavailable** in a 50/50
  band, because Law 12 forbids the pill below 1382.  The pill has to land on him.
* a full-height window that exactly FILLS a 960 band forces `s = 0.5`, which puts
  his eye line at 1371 and the pill straight across his eyes.

So s is pushed past 0.5 — the plate is taller than the band and bleeds off the
frame bottom, the same device round 3 used — which walks his features DOWN the
band until the pill clears his face.  Bounded on both sides, then snapped exact:

```
chin never cut : 960 + 1448 s <= 1920            ->  s <= 0.6630
integer plate  : CAM_W = 1080/s and CROP_W = CAM_W*9/8 both even

s = 5/8 = 0.625 -> CAM_W 1728, CROP_W 1944, band content 1200px tall,
                   240px bleeding below the frame (his black t-shirt, in the
                   bottom 28% where Law 12 wants nothing meaningful anyway)
```

| | plate on canvas | master window | face_frac | head_frac | head % of 1920 |
|---|---|---|---|---|---|
| round 3 FACE | 1080x1920 full bleed | 1215 px | 0.4282 | 0.5514 | 55.1 % |
| **round 4 FACE** | **1080x1920 full bleed** | **1215 px** | **0.4282** | **0.5514** | **55.1 %** |
| round 3 SPLIT | 1080x785 at y 1318 | 2970 px | 0.1752 | 0.2256 | 22.6 % |
| **round 4 SPLIT** | **1080x1200 at y 960** | **1944 px** | **0.2677** | **0.3446** | **34.5 %** |

Where he lands in the band, over all 64 sampled poses:

```
split head top   1080.0 / 1144.4 / 1164.4    (min / median / max pose)
split chin       1761.2 / 1823.8 / 1865.0    -> 55.0 px of worst-case headroom
pill top 1270    starts 105.6 px BELOW the lowest head top -> it is on the CAP
face mesh top    1309.9 (median landmark-10 depth) -> 70 px above the pill's
                 bottom; brows, eyes, nose and mouth are all below the pill
```

The proof that his FACE is not covered is the instrument, not the eye: in FACE
mode the pill occludes the chin and MediaPipe reads `face_frac` up to **-0.0288**
low; in SPLIT mode, with the pill on the cap, the same instrument reads within
**±0.0131** of the wanted 0.2677 on every probe (0.2546 / 0.2612 / 0.2669 /
0.2717).  The mesh is undisturbed because nothing of the face is under the pill.

## 4. THE VISUAL ZONE IS RE-FITTED, NOT RE-DRAWN

The zone lost 358 px (1318 -> 960 = 512.0 du).  Blocks still declare their ink
extent and get centred — but centred in the zone's **legal band**, not in the
zone: naive centring of the 360 du stage in a 512 du zone puts its first ink at
y 142 px, inside Law 12's forbidden top 10 % (192 px).  `dy_for` now centres in
`[ZONE_INK_TOP 102.4du = 192px, ZONE_INK_BOT 488du = 915px]` and raises if a
block does not fit.  Delivered ink: stage **216..891 px**, term **408..699**,
makers **300..807**; the bleeding shelf ends at 362 px (limit 576).  All above
the seam, all clear of the pill lane (1270), none in the top 10 %.

## Delivered numbers

`1080x1920 · 25/1 CFR · 1353 frames · 54.12 s · 67.0 MB · rendered in 38.9 s`
duplicate frames 2 (0.15 %) · speech margin 20.87 dB (p85 -16.07 / p15 -36.94)
**50/50 SPLIT PASS** (seam 960, spread 0) · FRAMING **PASS** ·
LAW 12 CAPTION BAND **PASS** (one bottom edge, spread 0.00) ·
LAW 7 0 % ALIGNMENT **PASS** (best_dy 0 px at all five probes, MAE 2.71-2.76 —
better than round 3's 3.05-3.29, because the narrower plate resamples closer)

## The findings worth keeping

1. **A format's identity is a constant, not a variable — so make it a build
   failure.** Round 3 lost 50/50 because the seam was a value the solver was
   allowed to touch.  In round 4 the seam is asserted at import on exact
   arithmetic and re-checked on the emitted HTML, and the solver is pointed at
   the magnification instead.  Same three constraints, one fewer degree of
   freedom, and the answer came out exact: s = 5/8, origin 2560, zone 512.0 du.
2. **When two rulings are geometrically incompatible, say which one is
   impossible and prove it.** "Pill on his chest in split mode" cannot exist in a
   50/50 band: his chin sits at 72 % of the master's height, so in ANY window
   containing his whole head the chin lands at 960 + 0.72 * band, i.e. 1650+,
   and Law 12 caps the pill at 1382.  The reachable optimum is the pill on the
   CAP with the whole face below it, and that is what shipped.
3. **A percentage without an edge named is ambiguous, and the ambiguity is where
   the round is won.** "Seat at 66-70 %" and "bottom <= 72 %" look contradictory
   until you notice one is a centre and the other an edge.  The pill that Miguel
   already approved measures 71.88 % at the bottom and 69.0-69.6 % at the centre:
   it was never two requirements, it was one.
4. **Re-fitting a zone is not scaling a zone.** Losing 358 px of visual zone did
   not shrink one glyph: the blocks are centred in a legal band that Law 12
   defines, so the layout moved and the type did not.


---

# FIX ROUND 5 — the band reframed, one font size, and one ruling proved impossible

`out/facesplit_fix5.mp4` · staged `~/Movies/Shorts Factory/Format Lab/Fixed5/facesplit_fix5.mp4`
1080x1920 · 25/1 CFR · 1353 frames · 54.12 s · 70.6 MB · 2 duplicate frames (0.15 %)
speech margin 20.87 dB — identical to rounds 1-4 to the centibel.
Thirteen segments, every switch time unchanged for the FIFTH round, every content
beat preserved. Zero zooms, zero punch-ins. **No sliding pill anywhere.**

## 0. THE POSE ENVELOPE, MEASURED ON ALL 1625 MASTER FRAMES

Round 4 solved its framing against 64 samples and a MEDIAN pose, which is why a
WORST-POSE defect ("the pill lands on my forehead") survived it.  Round 5 opens
by measuring five landmarks on **every** master frame
(`facesplit_fix5_measure.py` -> `facesplit_fix5_pose.json`, MediaPipe
FaceLandmarker + the zoomstd luminance cap scan), in master px:

| landmark | min | p05 | median | p95 | max |
|---|---|---|---|---|---|
| cap top | 241.0 | 297.9 | 342.0 | 364.0 | 399.0 |
| hairline (lm10) | 564.8 | 586.8 | 621.8 | 659.4 | 685.8 |
| brow top | 679.5 | 721.3 | **764.4** | 803.2 | 830.1 |
| eye line | 787.7 | 831.7 | 873.3 | 911.0 | 935.5 |
| lower lip (lm17) | 1216.0 | 1277.1 | 1361.3 | 1425.3 | 1507.9 |
| chin (lm152) | 1435.5 | 1491.4 | 1553.0 | 1609.9 | **1659.6** |

## 1. THE CHEST SEAT IS NOT REACHABLE.  HERE IS THE ARITHMETIC.

Miguel's ruling was *"reframe the face so the pill zone lands on his CHEST in the
band."*  Two lines close it, and no crop, magnification or anchor can reopen them:

```
pill BELOW the chin  ->  960 + k*1659.6 <= 1380   ->  k <= 0.2531
cover a 960px band   ->  k*2160        >= 960     ->  k >= 0.4444
```

There is no k.  Without algebra: **at the most zoomed-out framing a 960 px band
can legally hold, his chest occupies canvas y 1651..1920 — 86 % to 100 % of frame
height — and Global Law 12 forbids the caption below y 1382 (72 %).  The chest and
the legal caption lane do not overlap.**  Lifting the chest into the lane needs a
band showing ~4400 master rows above it; the camera only ever saw 2160.  His head
occupies the middle 65 % of every master frame and there are only 241 rows of wall
above his cap — 138 canvas px at the working scale — so the pill's lane, which
starts 310 px below the seam, is always inside his head.

Three ways out exist and all three break something Miguel has already ruled on:
a wider lens (a reshoot), a lower seat (Law 12 / Morgane's platform-UI finding),
or an unequal split (round 4's ruling).  **Round 5 changed none of them** and took
the reachable optimum instead.

## 2. WHAT ROUND 5 DID MOVE: k = 5/9 -> 4/7, ITS MEASURED MAXIMUM

The band's magnification is the one free number, and y0 = 0 (the master row on the
seam) is optimal — any y0 > 0 shows a LOWER slice and walks his face UP the band,
deeper into the pill.  So k is capped only by "the chin never leaves the frame":

```
960 + k*1659.6 <= 1914      ->  k <= 0.57484
CROP_W multiple of 18       ->  CROP_W 1890, CAM_W 1680
                                k = 1080/1890 = 4/7 EXACTLY
                                s = 1080/1680 = 9/14 EXACTLY,  k = s * 8/9
```

| | round 4 (k=5/9) | round 5 (k=4/7) |
|---|---|---|
| brow at the MEDIAN pose | 1384.7 | **1396.8** |
| pill bottom | 1380.0 | 1380.0 |
| **clearance** | **-4.7 px (on the brow)** | **+16.8 px (on the cap)** |
| chin at the LOWEST pose | 1882.0 | 1908.3 (frame 1920) |
| split head_frac | 0.3446 | 0.3545 |

Measured on the DELIVERED mp4, MediaPipe every 0.24 s over 129 split frames:
pill-bottom-to-brow **median +14.0 px** (round 4: -4.7 at the median pose), above
the brow on **84.5 %** of frames, and pill-bottom-to-eyeline **min +38.2 px** — his
eyes, nose and mouth are never under the pill on any frame of the video.
`probe/fix5_split_r4_vs_r5.png` is the side-by-side.

**The geometry is also expressed exactly now.**  Round 4 solved a transform-origin
fixed point (origin_y 2560) that only works for one s.  Round 5 puts the origin on
the plate's TOP edge and carries the seating in an explicit translate:

```
transform-origin: 840px 0px
FACE   scale 1,      y 0     ->  canvas_y = plate_y          (raw full bleed)
SPLIT  scale 9/14,   y 960   ->  canvas_y = 960 + (9/14)*plate_y
```

exact for any s, with FACE provably untouched.  **THE SEAM IS STILL 960, ASSERTED**
— on `Fraction` arithmetic at import, on both rect edges, and re-checked on the
emitted HTML — and measured on the delivered pixels at **960 exactly, spread 0,
zone 960 / band 960**, six probes.

## 3. FACE MODE: THE PILL CAME OFF HIS CHIN

Miguel: *"his chin sits ~y1330 at raw 0 %, so the pill grazes the chin line.  Seat
it so it reads as sitting on his neck/chest, not his mouth."*  FACE mode is frozen
by Law 7 (the 0 % window, proved again at **best_dy 0 px on all five probes**), so
the only lever is the pill's HEIGHT — which is the font size.  The bound is his
LOWER LIP over the 689 master frames inside a FACE segment, on the face canvas:

```
lip bottom   p95 1260.1   p99 1284.2   p99.5 1292.1   max 1301.6
pad 19 -> 17, pill 87px, TOP 1293, BOTTOM 1380 (67.34 % .. 71.88 %)
```

Delivered: the pill's top edge is **below his lower lip on 76/76 sampled face
frames (min +6.9 px, median +92.5)**.  Round 4's seat (top 1270) was clean on
677/689 with a worst dip of 31.6 px.  `probe/fix5_face_r4_vs_r5.png`.

Landmark 152 — the face-mesh "chin" — is **not** the visible chin for this
subject: measured against the beard line it sits ~62 canvas px lower, in the neck.
Deriving the pill from it produced a 30 px caption for no visible gain; measured,
then rejected, and the note is in the lib so round 6 does not repeat it.

## 4. ROUND 4 REALLY DID HAVE FONT-SIZE DRIFT.  EIGHT SIZES.

Miguel asked to find whether it was true.  It was, and the cause is one line:
round 4's `cap_font(text)` returned `min(30, budget / (EM * len(text)))` — **the
size was a function of the phrase length.**  Same instrument on both delivered
mp4s (find each pill by its fill in the caption lane, measure its box with a
sub-pixel edge crossing, measure the rendered x-height as the longest contiguous
run of rows carrying >= 40 % of peak ink):

| | round 4 | round 5 |
|---|---|---|
| font sizes declared in the HTML | **8** (37.31 / 39.75 / 44.25 / 45.94 / 49.69 / 51.94 / 54.38 / 56.25 px) | **1** (a single CSS rule, no inline styles) |
| rendered x-heights | **10 distinct** (18,19,21,22,24,25,26,27,28,38) — modal 27 on 57.7 % | **20 px on 52 of 53 pills (98.1 %)** |
| pill box height | median 108.6, spread **24.5 px** | median 86.5, spread **3.3 px** (sub-pixel noise on one nominal 87) |

Round 5's single size is 22.2du = **41.62 px**, derived (not chosen) from §3's
mouth bound.  One line per pill is kept by giving the CHUNKER the line budget:
a phrase breaks BEFORE the word that would overflow 28 characters.  Same words,
same timings, earlier break points — 53 pills instead of 52, nothing re-worded,
nothing dropped.  The build refuses to emit a page with more than one
`.scappill` font-size or with any inline style on a pill.

## 5. GATES

```
50/50 SPLIT              PASS   seam 960, spread 0, zone 960 / band 960
LAW 12 CAPTION BAND      PASS   top 1293 (+-0.5), bottom 1380 (+-0.7), worst 71.89 %
                                one seat, both modes, x in [233,918]
ONE FONT SIZE (new)      PASS   1 declaration, x-height 20px on 52/53 pills
PILL vs FACE (new)       PASS   face: below the lip on 76/76 (min +6.9)
                                split: eyes clear on 129/129 (min +38.2)
LAW 7 0 % ALIGNMENT      PASS   best_dy 0 px at all five probes, MAE 3.07-3.29
FRAMING (Law 1)          PASS   face 0.4282/0.5514 unchanged, split 0.2753/0.3545
LAW 6 FRAMERATE          PASS   25/1 CFR, 2 duplicates (0.15 %)
AUDIO MIX                PASS   margin 20.87 dB (p85 -16.07 / p15 -36.94)
```

## The findings worth keeping

1. **A worst-pose complaint cannot be answered with a median-pose measurement.**
   Round 4's geometry was solved on 64 frames and a median and it was right about
   the median — the pill cleared the brow by 4.7 px there.  Miguel was looking at
   the other half of the distribution.  Round 5 measures all 1625 frames and
   solves on percentiles, and the same instrument then grades the delivered file.
2. **When a ruling is unreachable, publish the two inequalities that close it.**
   "Pill on the chest" is not a taste disagreement, it is `k <= 0.2531` versus
   `k >= 0.4444`.  Naming the three exits (wider lens / lower seat / unequal
   split) turns a refusal into a decision Miguel can actually make.
3. **The direction of a reframe is not obvious and is worth deriving.**  The
   instinct is to zoom OUT to get more chest into the band.  Zooming out moves the
   pill DOWN his face — toward the eyes — because the master's headroom shrinks
   faster than his head does.  The optimum is the tightest framing that still
   keeps his chin in frame, which is the opposite of the instinct.
4. **Pin a format constant to a CSS rule, not to a call site.**  Round 4's font
   size was computed per pill and written inline 52 times, so drift was invisible
   in review and impossible to assert.  One declaration in the stylesheet makes
   "one font size" a grep, and the build now refuses any pill carrying an inline
   style.
5. **Measure type on the x-height, not on an ink bounding box.**  A bounding box
   clusters by which glyphs a phrase happens to contain (a cap is shorter than an
   ascender; 'y' descends and 'o' does not), so it cannot separate "one size" from
   "several".  The longest contiguous run of rows above 40 % of peak ink is the
   lowercase body and it is identical for every phrase at a given size — 52 of 53
   pills landed on exactly 20 px.  Two weaker versions failed first and both are
   in the code comments: min/max of thresholded rows reads CAP height on an
   ascender-heavy phrase, and the run around the peak row collapses when the peak
   is a single crossbar-aligned spike.
6. **A sub-pixel edge needs a local background, not a fixed threshold.**  The
   pill's top edge is antialiased against cream in one mode and shadowed skin in
   the other, and shadowed skin is only 37 away from #C4573A — closer than the
   fixed tolerance a first pass used, which leaked and reported an 87 px pill as
   106.  The 50 % crossing between the fill and the LOCAL background is the only
   version that reads the same number in both modes.

---

# ROUND 6 — THE CLOSING CAPTIONS ROUND (2026-08-31)

`facesplit_fix6_gen.py` / `facesplit_fix6_lib.py` → `out/facesplit_fix6.mp4`,
staged to `~/Movies/Shorts Factory/Format Lab/Fixed6/facesplit_fix6.mp4`.
Two changes, and nothing else in the video moves.

## 1. THE CANONICAL PILL — the format stops designing its own caption

Every round so far let the format solve its caption locally; round 5 went
furthest and DERIVED a size (22.2du = 41.62px) from this format's own mouth
bound. Round 6 takes it out of the format's hands. The pill is now the
PUBLISHED factory pill, lifted verbatim from
`shorts_run8/projects/mcpupgrade_icon/index.html` — the rule behind 97.1% of the
7,614 published caption pills:

```css
.scap     { left:0; width:1080px; text-align:center; }
.scappill { display:inline-block; transform:translateY(-50%);
            background:#C4573A; color:#fff; font-family:Nunito,sans-serif;
            font-weight:800; padding:18.8px 33.8px; border-radius:22.5px;
            white-space:nowrap; }
```

In this factory's design space those are round numbers: 56.2 = px(30du),
33.8 = px(18du), 18.8 = px(10du), 22.5 = px(12du). There is no `line-height` in
the published rule, so the pill is **114.59px tall** — measured in the render
browser, not assumed, and constant for every phrase.

**The shrink formula is dead.** The published `cap_font()` returned
`min(30, budget/(EM*len))`; round 4 shipped eight sizes because of it. A phrase
that will not fit the 756px width budget is now SPLIT at a word boundary into
two caption beats. **5 of the 55 pills here are width-forced splits.** No word
is re-worded, dropped or re-timed; only break points move.

**The width model is gone too.** Round 5 chunked on `0.575em per character`,
which over-estimates this corpus by ~12% — every pill it accepted was real, but
it broke phrases that would have fitted. Round 6 asks the render browser: one
Chromium, the exact pill CSS, all 2,745 candidate word-runs measured in one
pass, cached against a hash of CSS+corpus (`facesplit_fix6_type.json`).

## 2. TWO SEATS, ONE PER MODE, SWAPPED AS A HARD CUT (Miguel, confirmed)

| mode | seat | pill | note |
|---|---|---|---|
| SPLIT | `.scap.seam`, centre **960** | 902.7 .. 1017.3 | ON the seam, exactly as the 32 published shorts sit theirs |
| FACE | `.scap.chest`, centre **1322.70** | 1265.4 .. **1380.0 (71.88%)** | round 5's below-lip seat, still pinned by its BOTTOM at Law 12's line |

The machinery that makes the swap a cut was already there: the chunker forces a
phrase break at every one of the twelve switches and blacks captions out across
the two animated moves, so no pill is ever alive while its seat changes.

**Delivered, measured on decoded frames:** seam pills 903.1–903.3 top /
1017.2–1017.5 bottom (centre 50.02% — the seam), chest pills 1265.6–1265.9 /
1379.3–1380.1 (71.88%). Both seats stable to **0.3px** across the video.

## 3. THE ONE-FRAME BUG THIS ROUND FOUND

A frame-exact scan of all twelve switches (`probe/fix6/switchscan.py`) caught
ONE wrong-seat frame in the whole video: at 22.72 — the first frame of face mode
— the pill *"and context is finite."* was still on screen **in the seam seat**,
which in face mode lands across his chin. Root cause is not the layout, it is
floating point: the renderer decides visibility on `data-start + data-duration`,
and `21.26 + 1.46` is `22.720000000000002`, so a clip that ends exactly ON the
switch survives one frame into the next mode. `5.14 + 0.62` sums to exactly
5.76 and was clean, which is why it presented as a one-off rather than a class.
**Fix:** every clip is trimmed by half a frame (0.02s), so the last visible
frame is the last frame strictly before the nominal end whatever the float does.
Re-rendered: 12/12 switches clean, zero wrong-seat frames.

This is a FACTORY-WIDE lesson, not a facesplit one: any format whose captions
change anything on a switch frame has the same exposure.

## 4. THE SEAT FIT, RECHECKED (the canonical pill is 27.6px taller)

* **SPLIT / seam.** The pill's top edge is 902.7 and the visual zone's lowest
  ink is the CONTEXT WINDOW card at **891.0** — 11.7px of clearance, asserted at
  import (`ZONE_INK_BOTTOM < CAP_SPLIT_TOP`) because nothing in the zone is
  allowed to move to make room. Below the seam it clears the highest split-mode
  head top (1083) by 66px, and MediaPipe reads the pill's bottom **334–416px
  above his brow on 129/129 probes**: in split mode the pill is entirely off his
  face.
* **FACE / chest.** Holding round 5's TOP edge (1293) would push the bottom to
  1407.6 = **73.3%**, past Law 12, so the bottom stays pinned at 1380 and the top
  rises to 1265.4. Cost, measured on all 512 face-mode frames of the delivered
  file: MediaPipe's landmark 17 sits behind the pill's top edge on 8 frames
  (worst -24.3px) instead of round 5's 4. **That landmark is wrong for this
  subject** — round 5 already found landmark 152 lands ~62px into his neck, and
  `probe/fix6/lipscan.png` draws lm17 straight across his BEARD on all eight
  frames it flags. Settled on the delivered pixels at 3x with a row ruler
  (`probe/fix6/lip_zoom.png`): at the video's two worst open-mouth poses (0.44s
  and 23.84s) the pill's top edge sits **4–10px below the visible bottom of his
  lower lip**. Tight, and never on it.

  **If Miguel wants that air back**, the trade is one line: move the chest seat's
  bottom to 1407.6 (73.3%) and the top returns to round 5's 1293, restoring 28px
  of mouth clearance at the cost of 25px of Law-12 margin. TikTok's earliest UI
  is at 75% (1440), so 73.3% is still clear — but it is past the law as written,
  so it is Miguel's call, not the builder's.

## 5. CONTAINMENT

Decoded-pixel diff, every one of the 1,353 frames, round 6 vs the DEFINITIVE
(round 5) file, threshold 12 grey levels: **all material difference is in the two
caption bands.** Outside them the whole video differs by 4,808 pixels TOTAL —
about 3.7 per frame out of 2,073,600 — h264 requantisation noise, and no single
frame carries more than 400. `probe/fix6/containment.json`.

## 6. GATES

```
50/50 SPLIT              PASS   seam 960, spread 0, zone 960 / band 960
LAW 12 CAPTION BAND      PASS   seam centre 50.02%, chest bottom 71.88%,
                                both seats stable to 0.3px, x in [171,909]
TWO-SEAT SWAP (new)      PASS   12/12 switches, 0 wrong-seat frames
ONE FONT SIZE            PASS   one CSS declaration, no inline styles;
                                x-height median 26.85px, MAD 0.06px,
                                54/55 pills within 1.5px
PILL vs FACE             PASS   split: pill 334-416px above his brow, 129/129
                                face: 4-10px below the lip at the worst poses
                                (pixel ruler; the landmark is unreliable here)
LAW 7 0% ALIGNMENT       PASS   unchanged
FRAMING (Law 1)          PASS   unchanged
LAW 6 FRAMERATE          PASS   25/1 CFR
AUDIO MIX                PASS   margin 20.87 dB
```

## 7. FINDINGS WORTH KEEPING

1. **A clip that ends ON a cut frame is a floating-point coin flip.** Trim every
   clip by half a frame; never let `start + duration` be the arbiter of a frame
   the composition cares about.
2. **Measure type in the render browser, don't model it.** The 0.575em advance
   model cost this video phrase breaks it did not need. One Chromium, 2,745
   runs, one cache — and the same call verifies the pill's HEIGHT, so a font that
   fails to load becomes a build failure instead of a shifted seat.
3. **Measure the pill at an integer page position.** Stacked in flow, or laid out
   past ~250,000px down a page, Chromium reports the SAME box as 114.56 /
   114.59 / 114.61 — three pill heights where there is one. Batches of 250 at
   `top: i*200` fixed it.
4. **The face mesh is not a face on this subject.** Round 5 learned it for
   landmark 152; round 6 learned it for landmark 17 on open-mouth poses. When a
   landmark gate fails, look at the pixels before you move the design.
5. **Two seats need a frame-exact instrument, not a probe grid.** The 0.24s grid
   said the swap was perfect. The frame-by-frame scan found the one bad frame.
   And `ffmpeg -ss t` returns the first frame PAST t, so a frame is addressed by
   its exact frame time — `t + 0.004` silently reads frame n+1 and would have
   let the bug through a second time.
