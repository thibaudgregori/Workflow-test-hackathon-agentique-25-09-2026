# PURE FACE — format lab notes

**Format id:** `pureface` · **Source:** `format_lab/hermesinfinite` (hermesinfinite, 54.17s)
**Renders:** `format_lab/pureface/out/pureface_v{1,2,3}.mp4` — 1080x1920, 30fps, 54.17s
**Staged:** `~/Movies/Shorts Factory/Format Lab/pureface_v{1,2,3}.mp4`

Miguel is full-frame for the entire 54 seconds. There is not one icon, plate,
diagram, arrow, logo or drawn object in any of the three variants. The only
things on screen besides him are the factory caption pill and the outro chip.
The production restraint IS the format, and the question these three answer is
**how good can captions plus camera moves alone look, and where does "more"
stop helping**.

Everything that is not the format is held identical to the factory so the
format is the only variable Miguel is judging: the caption pill system
(`build_captions`/`clean_words`/`cap_font` lifted from
`shorts_run8/gen/geministt_kinetic_gen.py` — law-6 stutter filter, the >0.32s
gap chunker, the backward merge, the 35.6-56.2px font band), the palette, Nunito
800 caption type, JetBrains Mono chip type, the `@migueltorrezai` outro chip, and
the AUDIO MIX LAW (voice 1, `bed_split_v2` at 0.065, SFX 0.18).

---

## The three variants

| | v1 MINIMAL | v2 KINETIC CAPTIONS | v3 AGGRESSIVE |
|---|---|---|---|
| camera moves | **11** | **18** | **34** |
| zoom levels | 1.00 / 1.055 / 1.07 / 1.09 | 1.00 / 1.06 / 1.09 / 1.12 | 1.00 / 1.06 / 1.12 / 1.17 |
| move length | 0.50-0.66s, `power2.inOut` | 0.40-0.56s, `power3.out` | 0.22-0.36s, `power4.out` |
| reframes | none | none | 3 (x-45, y+55, x+45) |
| caption treatment | plain factory pill, hard cut | 13 lit words + 5 word-stacks | 17 lit words + every pill pops in |
| SFX | none | none | 19 (6 punch, 4 rise, 8 tick, 1 spare) |
| longest still stretch | 13.2s (22.8 → 36.5) | 5.3s | 2.4s |

**v1 MINIMAL** — the quietest possible edit. Eleven pushes across 54 seconds,
each landing on a key word (`literally infinite`, `procedural disclosure`,
`Tools consume context`, `will ever need`, `just unbelievable`) and then holding
completely still until the next idea. Nothing else happens. Everything is a
purposeful event with a long hold, so law 1 is satisfied by construction rather
than by tuning.

**v2 KINETIC CAPTIONS** — the caption stops being a subtitle and becomes the
graphic. Two devices:
- **lit words**: 13 words change colour to `#F2C14E` and scale up on their own
  spoken instant, then hold. The pop is a `transform`, never a font-size change,
  so the pill's width never twitches mid-life.
- **word stacks**: five phrases leave the one-line pill and build as a centred
  vertical stack, one pill per spoken word — `have / literally / infinite /
  tools.`, `crack / the / code.`, the key term `called / procedural /
  disclosure.`, `Tools / consume / context,`, `will / ever / need,`. The stack
  re-centres on its axis at every partial state (law 15) and the first word opens
  centred before the second displaces it (law 19), which is exactly the factory's
  arrival grammar applied to type instead of plates. A stack **replaces** its
  phrase's pill, so law 4 is never in play.

**v3 AGGRESSIVE** — the "how much is too much" probe. Every sentence gets a
move and the long sentences get two, snapped in a quarter of a second and held.
Four zoom levels plus three lateral reframes that push the frame off its axis for
a beat and put it back. Every caption pill enters with a 0.14s scale pop instead
of a hard cut, 17 words light, and an ElevenLabs SFX layer (bespoke `pf_punch` /
`pf_rise` / `pf_tick`, generated once in `sfx/` and shared) marks the six hardest
zoom-ins, the four biggest releases, and eight of the lit words.

---

## What I believe works

1. **Word stacks are the single best idea in the three.** They give a
   face-only short a genuine *visual* beat — something is being built on screen,
   not just read — while remaining 100% Miguel's own words at his own timing. The
   key term `procedural disclosure` finally gets the centre-stage debut law 9
   asks for, without a plate, an icon or a diagram existing anywhere in the
   video. If pure face ships, this is the device that carries it.
2. **Micro-timing is the whole game.** Every move is anchored to a transcript
   cue string (`Cue.at()` resolves it against `transcript_words.json` and
   asserts the occurrence), never to a hand-typed second. A punch that lands
   40ms after its word reads as a mistake in a way it never does under a
   diagram, because there is nothing else for the eye to blame.
3. **The 1.00 release matters more than the zoom.** Going back to full frame on
   a new idea ("You think an AI agent...", "That means that the best way...")
   reads as a paragraph break. In v1 the eleven moves are basically the
   video's punctuation, and that alone gives the piece a shape.
4. **Restraint is genuinely viable.** v1 has zero graphics and eleven slow
   pushes and it does not feel broken — it feels like a well-cut talking head.
   As a speed format this is minutes of work per short instead of hours.

## What fought me

1. **A scaled word eats its neighbours' spaces.** Emphasis by
   `transform: scale()` grows the word by `w*(s-1)/2` into each gutter. At the
   first pass the key term rendered as **`calledproceduraldisclosure.`** — three
   words welded together. Two fixes, both now structural: adjacent lit words are
   banned outright (`guard_no_adjacent_emphasis`), and the scale is **derived per
   word** from the available gutter (`emph_scale`) instead of being a constant,
   so `unbelievable.` at 43.9px lights at 1.096 while `MCP` at 56.2px lights at
   1.12. Constant emphasis scale is simply wrong when the caption font is
   length-driven.
2. **Stack pitch has to clear the pill, not the font.** First stack pass used
   66px type on a 118px pitch against a 127px-tall pill — the pills overlapped on
   screen. Pitch is now asserted against the measured pill box
   (`fs*1.36 + 2*pad + 16px gap`).
3. **The transform origin can only move at scale 1.** Changing
   `transform-origin` mid-timeline teleports the frame unless the scale happens
   to be exactly 1. All three variants therefore pin the origin at `50% 36%`
   (his eye line, which keeps the cap crown in frame up to s≈1.20) and do
   reframes with `x`/`y` translate instead, bounded by `reframe_limits()` so no
   frame edge can ever show.
4. **`face_full.mp4` is already the widest legal window.** The 4K master is
   3840x2160; a full-height 9:16 slice is 1215px wide, which is what `face_full`
   already is. There is no punching OUT past 1.00 without letterboxing, so the
   format's whole camera range lives between 1.00 and ~1.20.
5. **The outro chip needed changing.** The factory chip is a translucent wash
   (`rgba(246,241,234,0.13)`) designed for a flat cream or dark plate. Over live
   footage it is invisible. Pure face ships it **opaque cream on ink text** with
   a drop shadow, at y=1270 — 120px clear of the caption pill.

## Laws this format would need if adopted

- **PF-1 — THE CUE IS THE CLOCK.** Every camera move and every caption event is
  anchored to a resolved transcript cue, asserted by occurrence. No hand-typed
  timestamps in a face-led generator, ever. With nothing else on screen a 2-frame
  miss is the only defect there is.
- **PF-2 — A MOVE IS AN EVENT.** Zoom in, arrive, HOLD. No move under 0.20s and
  no move over 0.90s (that is a creep, i.e. law-1 idle motion), and a minimum
  hold between consecutive moves (0.9s in the quiet cut, 0.30s in the loud one).
  Enforced by `guard_punch_holds`.
- **PF-3 — THE FRAME NEVER SHOWS AN EDGE.** Scale >= 1.00 always, and any x/y
  reframe is validated against the scale's translate budget before it is
  authored. A black sliver on one frame is an unshippable defect.
- **PF-4 — LIT WORDS ARE NEVER ADJACENT, AND THEIR SCALE IS DERIVED.** See
  above. A constant emphasis scale on a length-driven caption font is a
  collision waiting for the longest word.
- **PF-5 — A STACK IS A CENTRED BUILD.** Word stacks re-centre on their own axis
  at every partial state and open centred (laws 15 and 19 carried into type), and
  the pitch is asserted against the measured pill box, not the font size.
- **PF-6 — OPAQUE CHROME OVER FOOTAGE.** Any chip, pill or plate that sits over
  live footage is opaque with a drop shadow. Translucent factory chrome is a
  flat-plate device and does not transfer.
- **PF-7 — THE CAPTION LINE IS FIXED AT y=1440.** It is the format's only
  constant, so it is the format's seam: nothing else may sit within 100px of it
  (the outro chip lives at 1270), and no stack may extend past y=1640 into the
  platform UI zone.
- **PF-8 — LAW 20 IS SATISFIED BY MIGUEL PLUS THE DEVICE.** In a face-led format
  the hook subject is Miguel and the format's own device (v2 opens on the
  four-word `have / literally / infinite / tools.` stack building on his words).
  No bolted-on hook object — that would break the format's one rule.

## Audio

Measured with the pinned instrument (mono 16 kHz s16le, 33 ms frame,
p85−p15) via `pureface_mixcheck.py`:

| file | margin | pause floor |
|---|---|---|
| **pureface_v1** | **20.89 dB** | −36.96 dBFS |
| **pureface_v2** | **20.89 dB** | −36.96 dBFS |
| **pureface_v3** (with SFX) | **20.81 dB** | −36.87 dBFS |
| geministt_kinetic (approved) | 17.72 dB | −40.30 dBFS |
| mcpupgrade_icon (approved) | 17.31 dB | −40.11 dBFS |
| airtable_icon (approved) | 17.08 dB | −39.47 dBFS |
| hermesvoicemagic_icon (approved) | 15.77 dB | −38.54 dBFS |

Above the approved corpus, not below it. The bed matters more here than in a
split-format short — with no graphics track, 54 seconds of dry voice would feel
like a raw upload, and 0.065 is doing real work.

## Files

```
format_lab/pureface/
  pureface_common.py      chassis: captions, pill CSS, audio block, punch guards
  pureface_v1_gen.py      MINIMAL
  pureface_v2_gen.py      KINETIC CAPTIONS
  pureface_v3_gen.py      AGGRESSIVE
  pureface_sfx.py         ElevenLabs sound-generation (cached in sfx/)
  pureface_mixcheck.py    the AUDIO MIX LAW instrument
  _geom_pureface_v*.json  every move, stack box and lit word dumped to disk
  pureface_v{1,2,3}/      HyperFrames projects (assets -> stage/)
  stage/                  v/face.mp4 (-> face_full.mp4), v/audio.m4a, music, sfx
  out/                    the three renders
```

---

# FIX ROUND 1 — `pureface_fix` (2026-08-30)

**Render:** `format_lab/pureface/out/pureface_fix.mp4` — 1080x1920, **25fps**,
1354 frames, 54.16s
**Staged:** `~/Movies/Shorts Factory/Format Lab/Fixed/pureface_fix.mp4`
**Generator:** `pureface_fix_gen.py` · project `pureface_fix/` · stage `stage_fix/`
**Geometry:** `_geom_pureface_fix.json` · **Gate 1:** 0 errors, 0 warnings

Miguel's verdict on the format was **WEAK**, with two named defects. Both are
fixed here, in one flagship calibrated between v1 (11 moves) and v2 (18): this
build has **15 camera events, 11 lit words, 5 stacks, 4 SFX**. v3 is dead.

---

## FIX 1 — framing (Global Law 1)

> *"Overall I think you do zoom in way too much on my face. Ideally we shouldn't
> have to zoom so aggressively — not just my face, my entire torso and such can
> also be in the video."*

`hermesinfinite/face_full.mp4` is retired from this format. The build sits on the
derived plate set from `_shared/FRAMING.md`:

| | plate | on canvas | face_frac | role |
|---|---|---|---|---|
| **REST** | `face_wide_25` | 1080x900 band, flush to the canvas top | **0.201** | 83% of runtime |
| **CEILING** | `face_max_25` | 1080x1920 full bleed, scale **1.00** always | 0.428 | 17%, punctuation only |

The format's whole shape changed as a consequence, and this is the important
part: **a face-led rest state cannot fill the canvas** (FRAMING §4 — a 9:16 crop
of a 16:9 master magnifies the head 3.16x, so `face_full` was already at the
physical floor and the old punch-ins went *below* it). So the rest state is a
band, and the **1020px surplus below it is the design ground where the type
lives**. Ink ground, warm radial lifting off the band seam, inner shadow so the
plate reads as a card sitting on a ground rather than a letterbox bar.

**Measured on decoded frames of the delivered MP4** (`pureface_fix_check.py`,
same MediaPipe instrument FRAMING used, n=12):

| | min | max |
|---|---|---|
| **fix, wide (rest + punch)** | **0.186** | **0.236** |
| fix, full bleed (s=1.00) | 0.419 | 0.440 |
| **rejected `pureface_v3`** | **0.395** | **0.528** (median 0.444, *every* frame) |

The rejected build never once went below 0.395. This one spends 83% of its
runtime between 0.19 and 0.24 — inside the card-mode band of Miguel's own
reference reel (0.196-0.238). The full-bleed frames read 0.419-0.440 against a
declared 0.428; that is `face_max_25` at scale 1.00 plus natural head sway
(FRAMING's own verification tolerance is +-0.020), not a scaling violation.

**Camera grammar.** Three states, and **every change is a single-frame HARD
CUT** — `tl.set`, never `tl.to` (FRAMING hard rule 5: at 25fps a 0.05s tween
spans 1.25 frames and renders one intermediate scale, which reads as a smear).
This is the takeover grammar Miguel named as preferred over animated creep.

* `wide 1.00` -> `wide 1.15` — within-mode punch, the derived ceiling
* `wide` <-> `max` — MODE SWITCH, x2.13 head height
* `max` never scales

15 events, minimum hold 0.40s, longest hold 11.9s (31.92 -> 43.80, which is
where the `will / ever / need,` stack does the work instead).

## FIX 2 — emphasis: SCALE + WEIGHT, zero colour

The gold `#F2C14E` + orange treatment is gone; the generator asserts that
`P.SUN` appears nowhere in the emitted HTML. An emphasised word gets **bigger
and bolder and nothing else**: scale 1.116-1.13 (still derived per word from the
available gutter) plus Nunito **800 -> 900**.

Weight cannot be tweened on a static font without reflowing the pill, so the
word is authored as **two stacked copies**: a w900 copy in normal flow that
*sets the box*, and a w800 copy absolutely positioned over it at `width:100%`.
Crossfading them over 0.10s thickens the glyphs while the layout box never
moves — the pill's width cannot twitch mid-life, which was the failure mode that
forced the colour treatment in the first place. 11 lit words; adjacency still
banned; none may fall inside a stack (asserted).

**The word stacks survive** — they were the discovery and they are still the
device that carries the format — recoloured to the neutral treatment: the key
word of each stack gets its own pill scaled to 1.10 with the same weight
crossfade, and no colour anywhere.

---

## Two things this round taught, both worth keeping

**1. A caption axis is per-MODE, and that is not a violation of the seam law.**
PF-7 fixed the caption line at one y. In a two-mode format one y is impossible:
the wide-mode axis (1290, optically centred in the design ground) lands
**squarely on his mouth** in full bleed. Measured with MediaPipe lm152 across all
four full-bleed windows at a 0.12s step (n=80), his **chin reaches y=1440.1**.
The full-bleed axis is therefore *derived* — `chin_max + 18px clear + half the
tallest pill that mode carries` = **1533.8** — not typed.

This is only safe because **every mode cut was aligned to a caption boundary**
at author time, so no caption ever straddles a mode change and the axis only
ever moves on the same frame the entire picture changes. The straddle guard has
to compare **frames, not seconds**: a clip at `data-start 17.74` and a cut at
`17.76` are both frame 444 at 25fps, and a seconds-based check reports a
straddle the render never shows.

**2. A pre-render browser sheet cannot see a defect in a mode it wasn't designed
for.** The mouth collision passed the headless sheet, Gate 1 (0 errors), and my
own eye — because in wide mode, where the layout was designed, it looked
correct. It only appeared on decoded frames of the real MP4. Two consequences
now baked in: the shot tool must emulate clip windows (a raw `file://` load has
no HyperFrames runtime, so all 52 captions paint at once and the sheet is a
lie), and **every mode a format has gets its own sampled frames.**

Minor, same class: the factory's single-line caption rule made the video's
**payoff** caption ("context, which is just unbelievable.", 36 chars) the
*smallest* pill in the piece. A phrase that would drop below 58px now wraps to
two lines and keeps a big face instead. 2 of 47 pills wrap.

---

## What changed structurally vs v1/v2

| | v1 / v2 / v3 | **fix** |
|---|---|---|
| fps | 30 (17% conform dupes) | **25 native, dupes dropped** |
| source plate | `face_full.mp4` full bleed | `face_wide_25` + `face_max_25` |
| rest framing | face_frac 0.40-0.53 | **0.19-0.24** |
| zoom motion | tweened, 0.22-0.66s | **single-frame hard cuts** |
| emphasis | `#F2C14E` + scale | **scale + weight 800->900, no colour** |
| caption | 35.6-56.2px, one line, y=1440 | 45-76px, wraps at 58, y=1290 wide / 1534 bleed |
| ground | none (full bleed) | ink + warm radial, 1020px design ground |
| SFX | none / 19 bespoke at 0.18 | **4 `soft_whoosh` at the pinned 0.120** |

## Audio

| file | margin @33ms | pause floor |
|---|---|---|
| **pureface_fix** | **20.88 dB** | -36.95 dBFS |
| pureface_v1 (no SFX) | 20.89 dB | -36.96 dBFS |
| pureface_v3 (19 SFX @0.18) | 20.81 dB | -36.87 dBFS |

Voice 1, bed 0.065, SFX at `_shared/SFX.md`'s **structure** constant `0.120` —
never hand-set. Four `soft_whoosh` one-shots, one per cut INTO full bleed and
nothing else; the releases are silent because a release is a relaxation. Every
one is scheduled at `ceil(cue x 25)/25`, the exact frame the cut paints on, so
the sync error against SFX.md's +-1 frame budget is **zero** rather than merely
inside budget. The palette is onset-trimmed, so no lead/lag offset is applied —
adding one would double-count.

**Flag for Miguel:** neither v1 nor v2 had SFX, and the review did not ask for
any here. Four tamed structure-class hits were added because a hard cut to full
bleed is exactly the event the new palette exists for. Trivial to strip — delete
the `sfx` list in `pureface_fix_gen.main()`.

## Laws PF-1..PF-8 after this round

PF-1 (cue is the clock), PF-2 (a move is an event), PF-3 (the frame never shows
an edge), PF-4 (lit words never adjacent, scale derived), PF-5 (a stack is a
centred build), PF-6 (opaque chrome over footage), PF-8 (Miguel + the device
satisfy Law 20) all stand unchanged. Three amendments:

* **PF-2 amended** — a move is not merely an event, it is a **CUT**. No tween of
  any duration on the face. The hold minimum (0.4s) survives; the move duration
  is now always 0.
* **PF-3 amended** — the frame never shows an edge, and now also never shows the
  *ground* through the band: the punch overflows the 900px band downward by 81px
  at 1.15, which the ground panel covers by z-order (the split-screen reference
  pattern), so no clipping wrapper is needed around the video.
* **PF-7 replaced** — **the caption axis is fixed PER MODE and derived from his
  face, and it may only change on the frame a mode change happens.** Aligning
  every mode cut to a caption boundary is what makes that legal.
* **PF-9 (new)** — **EMPHASIS IS SCALE AND WEIGHT. Never colour.** Weight is
  animated with the two-copy box-setting trick so the layout cannot reflow.

## Files added this round

```
pureface_fix_gen.py      the flagship generator
pureface_fix_shot.py     pre-render browser sheet (emulates clip windows)
pureface_fix_check.py    post-render self check on decoded MP4 frames
pureface_fix/            HyperFrames project (assets -> stage_fix/)
stage_fix/               v/face_wide.mp4 + v/face_max.mp4 (25fps, -g 25),
                         v/audio.m4a, music/bed_split.mp3, sfx/ (tamed palette)
_geom_pureface_fix.json  every move, axis, stack box, lit word and SFX
out/pureface_fix.mp4     the render
```

`stage_fix/v/*` are **re-encoded** from `_shared/face_{wide,max}_25.mp4` with
`-g 25 -keyint_min 25 -sc_threshold 0`: the shared plates carry keyframes every
10s, and the HyperFrames compiler warns that sparse keyframes cause seek
failures and frozen frames. Deterministic rendering needs dense keyframes.
