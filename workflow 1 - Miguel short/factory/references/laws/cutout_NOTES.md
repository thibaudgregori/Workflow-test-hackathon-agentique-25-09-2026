# CUTOUT COMMENTARY — format-lab prototype (2026-08-29)

Source: `format_lab/hermesinfinite` — the shipped cut of *"Hermes Agent can now
have literally infinite tools"* (54.187s, 185 spoken words, 52 caption pills).
Three variants, same cut, same story, same factory language. Only the staging
of the presenter against the world changes.

    v1 ANCHOR       k=0.52   out/cutout_v1.mp4
    v2 IMMERSED     k=0.78   out/cutout_v2.mp4
    v3 INTERACTIVE  k=0.62   out/cutout_v3.mp4

---

## The format in one line

Miguel's background-removed silhouette stands IN FRONT of a full-bleed
1080x1920 explainer world — no seam, no split, no face slot. The world is
behind him and it is the whole frame.

## The object (Law 13 / Law 20)

**THE SHELF.** A rack of real tool tiles that keeps going past the frame edge.
Every beat is the same rack seen differently: lit all at once (the wrong mental
model), one slot at a time (procedural disclosure), then tiling out of frame
while the context vessel stays low. The hook is Miguel plus the rack building
row by row on his words — the format's own device, not a bolted-on prop.

Beat map (identical across variants, so the comparison is clean):

| # | anchor | beat |
|---|---|---|
| b0 | 0.00 | HOOK — the shelf builds, then reveals it continues past the frame |
| b1 | 3.14 | the wrong model: every tile lit at once, context meter rams full |
| b2 | 6.28 | "they don't" — wall cools, meter drains, the Nous mark arrives |
| b3 | 9.88 | LAW 9 key term: PROCEDURAL / DISCLOSURE, centre stage |
| b4 | 13.34 | the signature move: one tool per beat, previous drops to outline |
| b5 | 20.00 | context is FINITE — a vessel with a hard end wall; being picky drains it |
| b6 | 29.70 | Nous Research → the agent it ships |
| b7 | 34.68 | the rack tiles out of frame in word-synced steps |
| b8 | 41.98 | hand it every MCP server; the meter barely moves |
| b9 | 50.74 | outro: calm row, rule, `@migueltorrezai`, daily AI |

---

## THE MATTE — honest verdict

Pipeline (all in `matte/`, all reproducible):

1. `hyperframes remove-background` (u2net_human_seg, CoreML) →
   `cutout_matte.webm`, 1625 frames, ~68 ms/frame, ~2 min.
2. `cutout_matte_clean.webm` — alpha `eq=contrast=3.2:brightness=-0.04` then
   two `erosion` passes. Kills the semi-transparent halo (soft-alpha fraction
   drops from 1.0% of the frame to a hard edge) and pulls the cut 2px inside
   the subject.
3. `cutout_matte_final.webm` — the **chair cut**, see below.
4. `cutout_matte_stroked.webm` — the die-cut rim baked in (alpha dilated 5x,
   filled cream `#FFFDF9`, original overlaid). This is what ships.

Steps 1-2 were deleted after use (workspace cleanup rule); `_final` and
`_stroked` are kept. Exact commands to rebuild from `face_full.mp4`:

```bash
node $HYPERFRAMES_ROOT/packages/cli/dist/cli.js remove-background face_full.mp4 \
  -o matte/cutout_matte.webm --quality best --device coreml

ffmpeg -c:v libvpx-vp9 -i matte/cutout_matte.webm -filter_complex \
 "[0:v]format=yuva420p,split[a][b];[b]alphaextract,eq=contrast=3.2:brightness=-0.04,erosion,erosion[al];[a][al]alphamerge,format=yuva420p" \
 -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 26 -row-mt 1 -cpu-used 5 -g 30 -an matte/cutout_matte_clean.webm

python cutout_chair_mask.py
ffmpeg -c:v libvpx-vp9 -i matte/cutout_matte_clean.webm -loop 1 -i matte/chair_mask.png -filter_complex \
 "[0:v]format=yuva420p,split[a][b];[b]alphaextract,format=gray[al];[1:v]format=gray,scale=1080:1920[mk];[al][mk]blend=all_mode=multiply:shortest=1,format=gray[al2];[a][al2]alphamerge,format=yuva420p" \
 -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 26 -row-mt 1 -cpu-used 5 -g 30 -an -shortest matte/cutout_matte_final.webm

ffmpeg -c:v libvpx-vp9 -i matte/cutout_matte_final.webm -f lavfi -i color=c=0xFFFDF9:s=1080x1920 -filter_complex \
 "[0:v]format=yuva420p,split=2[src][a];[a]alphaextract,dilation,dilation,dilation,dilation,dilation[da];[1:v]format=yuva420p,scale=1080:1920[wb];[wb][da]alphamerge[rim];[rim][src]overlay=format=auto:shortest=1,format=yuva420p[o]" \
 -map "[o]" -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 26 -row-mt 1 -cpu-used 5 -g 30 -an matte/cutout_matte_stroked.webm
```

**Edge quality on hair/cap: very good.** Miguel wears a cap, which is the best
possible case — the cut follows the brim cleanly and the ear/jaw edges hold at
full res. Checked on decoded frames at t=2/15/30/40/45/52.

**The real defect: the black gaming chair behind him.** u2net keeps it. It is
the same value as his cap and shirt AND it is contiguous with him — measured,
the alpha is ONE connected component on every sampled frame, so neither a
threshold nor a largest-component pass separates them. What *does* separate
them is geometry: over 54 sampled frames his own right-hand limit sits at
849-893px in the cap band and under 810px in the face band, while the merged
run reaches 930-1006px. So `cutout_chair_mask.py` builds a static alpha window
whose right limit follows his measured profile (872-902px between y=770 and
y=1300) and releases to the full frame where his shoulder legitimately sweeps
out below y=1410.

After that a small chair sliver survives at his right shoulder. It now reads as
a collar/hood rather than as a black slab, and the baked cream rim finishes the
job. **Verdict: usable, not perfect.** A real production version of this format
should either (a) re-shoot against a wall with no chair in frame, or (b) run a
better matting model (RVM/BiRefNet-class) — u2net_human_seg cannot do
dark-on-dark separation.

---

## What each variant does differently

### v1 ANCHOR — the news desk
Miguel is a bottom-third bust (k=0.52, head-top at y=1026). The story owns an
840px-tall stage above him that he never enters. Six-column shelf, 132px tiles,
three rows plus two half-rows clipped by the container to say "it keeps going".
Full-width horizontal context meter. Nothing ever travels behind him — the
composition is strictly stacked.

### v2 IMMERSED — depth
Miguel at k=0.78 (about 50% bigger linearly than v1). The world is no longer
above him; it is around him. Three **depth lanes** of tool tiles run across the
frame at 78 / 116 / 168px, opacity 0.34 / 0.66 / 1.0, and **step** by 46 / 112 /
208px on the same spoken beat — one event, three parallax depths. Every lane is
declared `behind` and gets eaten by his silhouette: a tile disappears at his
left edge and re-emerges on the other side. A fourth, closest lane (236px)
arrives on "all of the tools". The type story is squeezed into the TOP BAND
(96..537) — all the clear full-width real estate a subject this size leaves.

### v3 INTERACTIVE — staged acknowledgement
Miguel at k=0.62 and **slid 80px right of the frame axis**. Every named thing
**docks** at a position measured off his own silhouette: `Stage.band_gutters()`
returns the narrowest free x-range beside him across a y band, and
`Docks.fit()` solves the largest plate that clears it on every frame. Two docks
stack down the over-the-shoulder channel (head-top+34 and head-top+254, both
189px, one shared x); the context meter is a vertical 74px column standing at
his right shoulder. In b4 the four needed tools fly out of their slots and seat
ping-pong down the channel — the arrivals land where he could plausibly be
looking, with no hand tracking anywhere.

**This variant was rebuilt once, for a measured reason.** Centred at k=0.62 he
leaves ~150px of free width on *each* side at head height, which caps a docked
plate at 125px. The first render proved that reads as decoration, not as a
statement. Sliding him 80px right merges two useless channels into ONE ~230px
channel — literally a news over-the-shoulder graphic — and the docks grow 50%
to 189px. The thin context column is then the only thing that still fits on his
right, and it is the one element narrow enough to want to be there.

---

## What works

- **The staging reads immediately.** A cutout over a full-bleed world is a
  format viewers already know from news and reaction video; it costs zero
  explanation. The 840px stage in v1 is a bigger canvas than the factory's
  460du seam zone and it shows — diagrams can be twice the size.
- **No seam means no seam law.** The whole "nothing touches the caption chip or
  the divider" class of defects disappears, because there is no divider.
- **The occlusion guard is the format's spine.** Every scene atom is recorded
  and swept against the silhouette union (48 bands, sampled at 2fps over the
  whole take). Front atoms that would be eaten by him are a BUILD ERROR; v2's
  parallax lanes have to *declare* `behind=True`. It caught eleven real
  collisions in v3 before a single frame was rendered.
- **Docks-from-the-matte works.** v3's dock positions were never typed; every
  one of them is solved from his measured profile, so they hold on frames where
  he leans.
- **The baked die-cut rim** separates a black shirt/cap from a light ground for
  free and hides the matte's remaining rough edge.

## What fought me

- **THE FILTER STACK ALMOST KILLED THE RUN.** The die-cut rim was first authored
  as eight zero-blur `drop-shadow()`s on the `<video>`. Chromium re-runs that
  chain on every composited frame of a 1080x1920 video: the render went from
  ~4.5 min to a projected **3+ hours** for the same 54s (measured: 60% in 15
  minutes and slowing). Baking the rim into the matte with one 60-second ffmpeg
  pass gives the identical look at zero per-frame cost. **Never put a filter
  stack on a full-frame video element in this framework.**
- **A dark subject cannot use a dark ground.** Miguel's shirt and cap are black,
  so the factory's `INK_2` dark sections are unusable in this format — he would
  vanish into them. Every section here is cream. That removes one of the
  factory's rhythm tools (the dark-ground beat) and the format has to find
  another.
- **The close-up crop is expensive.** `face_full.mp4` is a tight bust whose
  shoulders already touch both frame edges, so scaling him down is the only way
  to make room and it costs face size fast. At v1's k=0.52 his head is ~200px
  tall — fine, but the format wants a wider recording (half-body, some air) to
  really breathe.
- **v2's gutters are tight.** At k=0.78 the clear channels beside his torso are
  ~97-160px. The lanes read as depth, but individual tiles are only ever fully
  legible beside his HEAD, where his silhouette narrows. The depth illusion
  works; the tiles as information do not, in the lower lanes.
- **Label placement fights the silhouette.** Labels under a docked plate fall
  into a narrower gutter than the plate itself. In v3 they had to move ABOVE the
  plates, into the wide band just under his chin line.

---

## Laws this format would need if adopted

1. **THE SILHOUETTE IS THE LAYOUT.** Safe areas are derived from a measured
   matte envelope, never typed. Any scene atom is either provably clear of the
   silhouette union on every frame, or explicitly declared `behind`. (Gate 1
   would need a per-project envelope, not just the geometry sweep.)
2. **NEVER OCCLUDE HIM.** No foreground element may cross his silhouette;
   captions may sit over the TORSO only, and must clear the head band by 90px.
   Restates Law 17's spirit for real footage.
3. **NO FILTER STACKS ON THE CUTOUT.** Rims, glows and outlines are baked into
   the matte offline. One `drop-shadow` is the ceiling.
4. **CREAM ONLY WHILE THE SUBJECT IS DARK.** A ground whose value is within
   ~20% of the subject's clothing is banned. If a dark ground is wanted, the
   subject needs a light garment or a rim strong enough to survive it.
5. **THE DOCK IS AN ANCHOR (extends Law 15/19).** In face-led formats an element
   that arrives beside the presenter is centred on the FREE COLUMN's axis, not
   on the frame axis. Flanking pairs are normalised to the same size, taken from
   the narrower side.
6. **THE MATTE IS AN ASSET WITH A VERDICT.** Every cutout ships with a decoded
   edge review at 4+ timestamps and a written verdict, exactly like an asset
   health check. Dark-on-dark subjects (black chair, black hoodie, dark set)
   are a known u2net failure mode and must be caught before build, not after.
7. **RECORD FOR THE FORMAT.** The recording rule changes: a cutout format wants
   a half-body frame with headroom and NOTHING dark directly behind the
   shoulders. This is a set rule, not a build rule.

---

## Ranking

**1. v1 ANCHOR.** The most confident short of the three and the one I would put
in front of an audience. The 840px stage is the biggest, calmest canvas any
factory format has had; the shelf, the five on-demand slots and the context
vessel all get to be full-size and centred, and Miguel is present the whole time
without ever competing with the diagram. It is the least ambitious use of the
cutout — nothing passes behind him, he is functionally a lower-third presence —
but it is the version where the FORMAT costs the explainer nothing and adds a
face.

**2. v3 INTERACTIVE.** The most interesting idea and the one worth developing.
Off-centre staging plus a solved dock column is a genuinely different reading
from anything in the factory, the vertical context meter standing at his
shoulder is the single nicest beat produced in this run, and the b4 ping-pong
(a tool flying out of its slot and seating beside his head) is exactly the
"staged interaction" the brief asked for. It loses to v1 on density: the clear
zone above his head is 710px instead of 840, which forces the shelf and slots
smaller, and half the frame is a channel that only ever holds one 189px plate,
so the composition breathes more than it should. Recording him with more
headroom would flip this ranking.

**3. v2 IMMERSED.** The depth illusion genuinely works — tiles vanish at his cap
and re-emerge, the three step distances read as three distances, and at t=22 it
is the best-looking still of the whole run. But it makes the world into
wallpaper. At k=0.78 the clear channels are 97-160px, so the lower lanes only
ever show half-tiles, and the type story is squeezed into a 470px band. As
information design it is the weakest of the three; as a hook device (the first
3 seconds of v2 are the most arresting of the run) it is the strongest. The
honest conclusion is that IMMERSED is a *move*, not a format — worth stealing
for the opening 3-5 seconds of v1 or v3.

## Files

    cutout_core.py            shared chassis: Stage, occlusion guard, atoms, captions, audio
    cutout_v1_gen.py          v1 ANCHOR generator
    cutout_v2_gen.py          v2 IMMERSED generator
    cutout_v3_gen.py          v3 INTERACTIVE generator
    cutout_measure_matte.py   silhouette envelope (48 bands, 2fps over the take)
    cutout_chair_mask.py      the measured chair cut
    cutout_sfx.py             ElevenLabs sound-generation, 5 cues, cached in sfx/
    cutout_check.py           12-frame contact sheet from a render
    matte/                    the four matte generations + envelope.json + chair_mask.png
    sfx/                      step_in, wall_slam, plate_dock, layer_pass, meter_fill
    v1/ v2/ v3/               HyperFrames projects (index.html + assets symlink)
    out/                      renders
    frames/                   contact sheets + the matte edge-review stills

---

# FIX ROUND 1 — `cutout_fix.mp4`
*task id `cutout_fix`, 2026-08-30. Authority: `format_lab/REVIEW_2026-08-30.md`.*

> **"Really really really like the idea"**, especially the depth effect —
> *"things happening behind me was super cool"*. **v1 avatar size is the right
> size.** v3's idea liked but execution off: wants to be **CENTERED**, head still
> too big / too much real estate. Wants **SHOULDERS** visible. Matte problem:
> black chair + black t-shirt defeat the segmentation.

This round does not add a v4. It collapses the three prototypes into **one
cutout**, built only from the parts Miguel approved:

| taken from | what |
|---|---|
| **v1** | the whole stage story — shelf, key term, on-demand slots, context vessel, MCP payoff, outro. The variant he ranked first. |
| **v2** | the depth lanes. The move he singled out. |
| **v3** | nothing. Off-centre staging was rejected; he is on the composition axis. |

Everything below is measured. Numbers with no source are not in this file.

## 1. The staging, and why every number is what it is

| | value | derivation |
|---|---|---|
| plate | `_shared/face_wide_25.mp4`, 1080x900 | FRAMING.md REST plate — the narrowest window his measured 2511px shoulder line fits inside |
| scale | **1.00** | see below |
| position | left 0, top 1020 (bottom-anchored) | plate is exactly canvas width; his torso runs off the bottom edge instead of ending in a cut |
| cap top / chin | 1163.8 / 1663.8 | master 345/1545 of 2160, x 900/2160, + 1020 |
| head on canvas | **496px, head_frac 0.259** | 1191 master px x 900/2160 |
| STAGE zone | 100 .. 1050 (950px) | everything above him, always clear |
| DEPTH band | 1120 .. 1514 | the three lanes |
| caption pill | centre 1784 | chest-height lower third |

**Why scale 1.00 and not "exactly v1's size".** v1 is the size he approved, so it
was measured rather than assumed: MediaPipe + cap scan on `out/cutout_v1.mp4` at
t=6/15/22/30/40/50 gives **head_frac median 0.276 (528px)**. This plate at scale
1.00 gives **0.259 (496px)** — 6% smaller. Matching 0.276 exactly needs scale
1.065, and his shoulders occupy **1046 of the plate's 1080px**, so anything above
**1.032** crops the shoulders straight back off. *Exact-v1-head and full-shoulders
are mutually exclusive at this canvas width.* Shoulders win: he asked for them by
name, and the 6% head delta is inside the ±0.015 natural-sway band FRAMING.md
measures on the source. Verified on the shipped render: **head_frac 0.257, face
centre 538px against the 540 axis (-2px).**

**The stage got bigger, so the scenes moved.** v1's head sat at y=1026 and its
scenes were authored for a zone of 100..940. Here his cap is at 1164 and the zone
is 100..1050 — 114px taller. Left alone the story hugs the top of a stage it
wasn't designed for. `rebalance()` therefore derives **one offset per scene
group** by centring that group's recorded atom union in the new zone:
`shelf +65 · term +12 · ondemand +132 · context +166 · lab +157 · payoff +133 ·
outro +66`. b0/b1/b2/b7 share a group because they are four views of the same
shelf; giving them independent offsets made the shelf jump 62px between the hook
and the next beat. The occlusion and zone guards then run on the *shifted*
coordinates, so rebalancing cannot smuggle an atom onto him.

## 2. The depth effect, kept and aimed

v2's lane parameters are **unchanged** — tile 78/116/148, opacity 0.34/0.66/1.00,
step 46/112/208px per beat. They already read at this scale and there was no
reason to redesign what he liked. What moved is the **Y band**: v2 ran them at
636/880/1188 across a k=0.78 subject's torso, where the measured clear channels
were only 97-160px and NOTES.md's own verdict was *"the tiles as information do
not [work], in the lower lanes"*. Here they run at **1120 / 1224 / 1366**, across
his head and shoulder line, where the measured worst-case gutter is:

| lane | tile | y | worst gutter L | worst gutter R | strip (derived) | travel |
|---|---|---|---|---|---|---|
| far | 78 | 1120 | 357 | 321 | -216 .. 1848 | 552 |
| mid | 116 | 1224 | 297 | 301 | -304 .. 2728 | 1344 |
| near | 148 | 1366 | 213 | 296 | -384 .. 3960 | 2496 |

`guard_lanes()` enforces both halves of that: a lane must **cross** the
silhouette (or there is no depth cue at all) **and** leave a gutter wider than
one whole tile on both sides (or what re-emerges from behind him is a sliver
rather than a tool). Both are build errors, not review notes.

The lanes are one persistent layer for the whole 54s rather than v2's per-section
copies, so the parallax is continuous across cuts. They **step, never drift** —
12 discrete steps, each on a named spoken beat.

**Why v3's docked plates are not also here.** They would want the same real
estate. v3's whole argument was that the free channel beside him is where a
docked plate belongs, and at this staging that channel is 296-366px wide — the
widest it has ever been, so a dock would finally be full size. But it is the
identical band the lanes cross, and a static plate parked in a lane's path either
occludes the lane or gets occluded by it; either way one of the two stops
meaning anything. Miguel praised the depth more than the docking, so the channel
goes to the depth. If the dock is ever wanted back, the honest version moves the
lanes off the head band, and then they stop being the thing he liked.

## 3. Global laws, one by one

**Law 1 — zoom.** No punch-ins exist in this format. The plate renders at 1.00
throughout, head_frac 0.259, which sits inside the reference reel's card-mode
band (0.196-0.238) rather than above its most-zoomed frame ever.

**Law 2 — SFX.** The old five cues are gone. They peaked **13.4 dB over bed
presence** and carried up to **533ms of leading silence** before their own
transient (`wall_slam`). The new set is the tamed palette at its pinned class
constants, **rationed from v1's 11 cues to 7**, and every one is frame-locked to
n/25 with no compensating offset:

| t | cue | class | volume |
|---|---|---|---|
| 0.040 | `soft_whoosh` | structure | 0.120 |
| 5.120 | `low_thump` | structure | 0.120 |
| 7.000 | `reverse_air` | structure | 0.120 |
| 10.480 | `page_turn` | detail | 0.077 |
| 19.200 | `pop` | detail | 0.077 |
| 21.520 | `low_thump` | structure | 0.120 |
| 36.560 | `soft_whoosh` | structure | 0.120 |

Every `data-start` is an exact multiple of 0.04 — verified in the emitted HTML.

And the result is measured on the finished mix, on SFX.md's own pinned
instrument (mono 16 kHz **s16le**, 33ms frame RMS): the render's **p85 is
-16.1 dBFS against the -16.00 SFX.md measured for the bare voice**, and its true
peak is **-0.91 dBFS**. The mix is still the voice; the effects colour moments
inside it rather than sitting on top of it. That is the whole content of Global
Law 2, and it is now a check rather than a claim.

**Law 3 — rounded fills.** The audit cleared cutout's meters only because the bar
is tall enough to survive a squashed cap, and told the next regeneration to adopt
R1 anyway. Done: `meter()` authors a `width:0` fill carrying the track's own
radius, `fill_to()` reaches by **width**, floored at one cap diameter, and the
build fails if any `-fill` is still driven by `scaleX`. **Measured on the decoded
render**, not asserted: the fill's reach at its vertical centre versus two pixels
from its top and bottom edges — a semicircular cap bulges by about its radius, a
chord bulges by ~0.

| probe | track radius | measured bulge |
|---|---|---|
| `b5-ves` @ 27.54s (34% reading) | 55 | **36px** |
| `b8-ves` @ 45.16s (20% reading) | 55 | **40px** |

**Law 4 — no peek-ahead.** Sections are clipped clips; nothing from a later beat
is on screen before its words. The lanes are ambient texture, not un-spoken
content, exactly as in the v2 pass he praised.

**Law 5 — no unmotivated moves.** Two translations survive, both spoken: the Nous
plate rides left on *"the lab behind Hermes"*, the MCP plate rides left on
*"just give up"*. Every lane step lands on a named word.

**Law 6 — 25fps.** Authored at 25 and rendered at 25, from the de-conformed
plate. **Duplicate-frame rate on the decoded render: 0.00%**, against 16.8% in
the source master. Duration is `1354/25 = 54.16` exactly, so the last frame is a
real frame rather than a re-timed one.

## 4. The matte

Ships on the bake-off winner: `birefnet-general` plus the full post stack —
haze-kill S-curve, keep-largest + fill-holes, 3-frame temporal median, feather
0.6, no erosion, cream die-cut rim. **Chair leak 2.006% -> 0.056% of frame
(36x)** against the u2net matte the prototypes used. MATTE.md is the authority;
nothing about it was re-derived here.

The file that shipped is `matte_fix_best_rim.webm`, produced by running the
mattebakeoff agent's **own `mb_render.py`** over its **own**
`alpha/birefgen_canon_full.mkv` — same code, same alpha, same parameters, written
to a cutout-local path so the two agents could never race for one filename. That
path fired because `_shared/matte_best_rim.webm` had not appeared five minutes
after the alpha pass exited at 03:16 (6146s, 4540 ms/frame). Alpha verified at
**56.9% fully transparent**.

**Layout could not wait 2.4 hours for that alpha**, so it was built against a
deliberately conservative envelope first: `--src rvm`, over the RVM alpha already
on disk. RVM is the bake-off's *loser* at 15x the chair leak, so its silhouette
is fatter where the chair is. The ship pass then re-derived the true envelope and
re-ran every guard against it.

**And the superset assumption did not hold everywhere — 723 of 900 rows escape
it.** That is not a bug in the reasoning, it is the reason the guards are re-run
rather than trusted: RVM does not merely *add* the chair, it also *loses* real
subject (MATTE.md measures it rendering the black t-shirt semi-transparent), and
the winner's baked rim adds 7px where the conservative envelope only padded 4.
So the true silhouette is wider than the loser's in the torso rows even while
being far narrower at the chair. Concretely, the near lane's worst left gutter
went **296 -> 213px** on the true envelope. Still wider than its 148px tile, so
the lane guard passed — but it passed on a **measurement**, not on an assumption.
*A conservative proxy is worth building against and worth nothing to trust.*

**`face_full.mp4` is retired here.** The old envelope was measured on that tight
bust and is geometrically meaningless against a 1080x900 plate.

## 5. Three things that cost real time

**An ffmpeg pad consumed twice silently produces a matte with no alpha.** The
proxy's alpha plane feeds both `alphamerge` (the cut) and the `dilation` chain
(the rim). Wiring one label into two consumers does not error: **ffmpeg exits 0,
prints nothing at `-v warning`, and writes a webm whose background is fully
opaque** — his real room, chair and all, painted over the scene. It renders, it
looks *plausible* at thumbnail size, and it is completely wrong. Worse,
`ffprobe` cannot catch it: a VP9+alpha webm reports `pix_fmt=yuv420p` either way,
because the alpha rides in a WebM BlockAdditional side channel. Measured, the
broken graph gives **0.1% transparent pixels where the correct one gives 55.4%**.
Fix: an explicit `split=2`. Guard: `assert_alpha()` now decodes the alpha and
refuses any matte under 25% transparent, in the matte builder **and** in the
generator's asset stager.

**The occlusion check was wrong twice, in two different ways.** First it was a
colour heuristic — "terra-coloured pixels inside the head box" — and reported
**308,791** of them. They were his face; skin is exactly `r>150, r-b>60, r-g>40`.
Replaced with a generated **control composite** (the matte over the bare ground,
nothing else) diffed against the render, which measured 1.45%. Then widening the
lanes pushed that to **2.30% and a hard fail** — because a *bounding box* around
his head also contains ground, and the depth lanes cross that ground on purpose.
The check was measuring the format's best feature as a defect. It now builds the
mask from the control's own non-ground pixels, eroded 5px so the die-cut rim is
not compared against itself, and compares **only pixels that are him**. Result:
**0.00%** on every sampled frame. Both errors share one shape: *a proxy for "is
something on him" that is not actually derived from where he is.*

**Making the lanes persistent nearly threw the depth away in the second half.**
v2 re-authored its lanes inside every section, so its step offset reset ten
times and a fixed 2600px strip was always plenty. Made continuous across the
whole 54s, the near lane takes all 12 steps: `12 x 208 = 2496px` of travel
against a strip that starts at x=-760 and ends at 1840, so it finishes at
-3256..-656 — **entirely off canvas**. Measured on that render, pixel variance in
the near lane's gutters: **46.9 -> 0.7 by t=24 on the right, 0.3 by t=44 on the
left**, and the mid lane gone from the right by t=44. The depth wall quietly
drained away exactly during the payoff, and it is invisible in any single early
frame — the contact sheet at t=1.6/8.4/18 looks perfect. Fix: each strip's width
is now **derived from its own travel** (`lane_strip()`), the build refuses a
strip that cannot cover 0..1080 after its last step, and check 8 re-measures the
gutter variance on the finished render. The general rule: *the moment a stepping
element becomes persistent instead of per-section, its extent stops being a
constant and becomes a function of the schedule.*

## 6. Self-check

Result on the shipped file, every line re-derived from decoded frames:

```
1  CONTAINER     1080x1920  25/1  1354 frames
2  JUDDER        duplicate frames 0.00%              (source was 16.8%)
3  AVATAR        head_frac median 0.2569             (v1 approved 0.276, -6.9%)
4  CENTRED       face centre x 538px                 (axis 540, offset -2px)
5  SHOULDERS     0 dark pixels at either frame edge in the shoulder band
6  NO OCCLUSION  0.00% of his own head-band pixels differ from the control
7  ROUND FILL    cap bulge 36px and 40px             (straight would be ~0, radius 55)
8  DEPTH         weakest lane gutter variance 6.7    (a drained lane reads 0.2-0.9)
9  AUDIO         54.17s  peak -0.91 dBFS  p50 -22.6 / p85 -16.1 / p95 -13.7
ALL CHECKS PASS
```


`cutout_fix_check.py` re-derives every claim from the decoded render and exits 1
on any failure — container, judder, avatar size, centring, shoulders, occlusion,
round fills, depth survival, audio. Contact sheet: `frames/cutout_fix_sheet.png`.

**"Shoulders visible" is checked as a fact, not a look:** the ground is cream and
he is in black, so a dark pixel in the first or last three columns of the shoulder
band means the crop clipped him. Measured: **0**. The retired tight crop fails
this by construction — its shoulders touch both frame edges.

## 7. Files

    cutout_fix_gen.py         the one cutout — generator
    cutout_fix_envelope.py    silhouette envelope on the wide plate (conservative + true)
    cutout_fix_matte.py       matte staging + the RVM development proxy
    cutout_fix_check.py       7 self-checks on the decoded render
    cutout_fix_ship.sh        winner-matte ship pass (envelope -> build -> render -> check -> stage)
    matte_fix_best_rim.webm   the matte that shipped (winner alpha through mb_render.py)
    matte_fix_proxy_rim.webm  the RVM development stand-in (NOT shippable)
    fix/                      HyperFrames project
    stage_fix/                staged assets (matte, voice, bed, tamed sfx, logos)
    fix_envelope_conservative.json   RVM superset envelope (layout was built on this)
    fix_envelope.json                winner-matte envelope (the build ships against this)
    _geom_cutout_fix.json     every derived number this build used
    out/cutout_fix.mp4        the render
    frames/cutout_fix/        the decoded self-check frames

---

# FIX ROUND 2 — `cutout_fix2.mp4`
*task id `cutout2`, 2026-08-30. Authority: `format_lab/REVIEW_2026-08-30.md` § ROUND 2.*

> **"a LOT better."** Keep the cream die-cut **RIM** (confirmed). Remaining:
> (a) the headrest still visible on the right at times — *"fix with more effort
> (spatial exclusion region, not just the model)"*; (b) gray placeholder tiles
> must always carry REAL logos, repeats allowed; (c) at ~33s "Nous Research"
> did not move with its Hermes card. Plus global laws 8 (edge fade) and 11
> (continuous pill fills, no detached ticks).

Round 1's staging, sizing, centring, shoulders and depth parallax are
**unchanged** — they are what he liked. Four defects were fixed and nothing else
was touched. Every number below is measured on decoded pixels; the checker
(`cutout2_check.py`) re-derives all of them and each one is a BEFORE/AFTER
against `cutout_fix.mp4`, the file he was looking at.

## 1. The headrest — solved by geometry, not by another model

**Where it actually was.** `cutout2_diag_leak.py` streamed the winner alpha
(`birefgen_canon_full.mkv`) through the same `spatial()` post step the renderer
uses and recorded, per frame, the rightmost ON pixel of all 900 rows. In the
neck band his own silhouette sits at **x≈690 (p50)**; the bulge reaches
**770–835** on **272 of 1354 frames**, in **23 windows spread across the whole
54s** — not one bad moment. And it stops at the SAME place every time: the
recurring ceiling at **x=796–833** is the signature of a static object, not of a
man leaning.

**The discriminator, and why the obvious ones fail.**

| candidate rule | why it fails |
|---|---|
| better model | round 1 already shipped the bake-off winner; MATTE.md measures the residue as a *genuine merge*, thicker than any structuring element that would not also eat his shoulder |
| brighter/darker threshold | chair and shirt share a luminance band by construction |
| a typed rectangle | brittle, and it cuts him the moment he leans |
| **temporal stillness** | **most of the way there** — the headrest never moves, he does |

Stillness alone is not enough, and the counter-example is exact: at (620, 820)
the chair has **std 8.0**; at (640, 760) **his own shoulder** has **std 9.0**. A
black shirt held still looks like a black chair held still. The third axis
separates them — **how often the matte itself calls the pixel subject**:

```
his shoulder (640,760):   on-fraction 0.99      persistent  -> KEEP
the chair    (620,820):   on-fraction 0.11      intermittent -> CUT
```

A leak is intermittent by definition; a body part is not. So the exclusion is

```
chair  =  dark (mean < 105)  AND  still (std < 12)  AND  matte-on < 0.40
```

morphologically opened, closed 25px (to bridge the gaps his shoulder
occasionally punches through the chair column), **intersected back with the
still&dark evidence** so closing can never invent exclusion over a moving pixel,
kept as components reaching above y=700, grown 2px, feathered 1px.

Result: **58,499 px = 6.0% of the plate**, in five components — the right-hand
headrest wing (692,321 156x345), the left wing and the dark shelf shadow behind
it, and two small chair edges at the frame's right. Derivation sheet:
`cutout2/frames/headrest_derivation.png` (mean · temporal-std · mask overlay).

**Applied in the only place it can go** (`cutout2_matte.py`), BEFORE
keep-largest: cutting the chair severs the bridge, and keep-largest then drops
whatever fragment is left floating. Doing it afterwards leaves the fragment
welded on. It is re-applied after fill-holes so the notch cannot be filled back
in.

**Measured on the shipped mattes, on the frames that leaked** (mask eroded 8px
so neither build is charged for its own antialiased cut edge, clean alpha not
the rim file — the rim is a deliberate 7px dilation and would score as leak):

| | chair pixels inside the exclusion region, mean over 20 leak frames |
|---|---|
| round 1 | **4,448 / frame** |
| round 2 | **0 / frame** |
| worst single frame, round 2 | **0 px (0.00% of the region)** |

Side effect worth recording: the true silhouette is now **up to 85px narrower on
338 of 811 live rows**, so the near lane's worst left gutter went **213 → 289px**.
Every guard was re-run on the new envelope (`cutout2_envelope.json`) rather than
assumed — a narrower silhouette is not automatically safe, it changes which lane
offsets are legal.

## 2. Global Law 10 — no placeholder tiles

Round 1 drew `blank_plate` (a grey lozenge) on **1 lane cell in 4** and on
**3 whole shelf rows**. The roster grew **14 → 26 marks** (`ROSTER`, 24 of them
tile marks, plus `nous` and `mcp`), lane cells now index it with **stride 7**
(coprime with 24, so no repeat inside one screen width and the three lanes never
march in step), and the 6x5 shelf takes rows A/B/C/D plus one deliberate repeat
row — Law 10 says repeat rather than blank.

`blank_plate` is **shadowed by a function that raises**, so the ban is structural
and not a matter of remembering. Measured on the render: **156 tiles drawn, 178
logo images in the DOM, 26 distinct marks**, and a blank-glyph detector (the
glyph composites to an achromatic 217 over white, so: achromatic blobs in luma
205–232, area ≥500, square-ish, ≥75% filled) finds **34 glyphs in round 1 and 0
in round 2** over the same ten frames.

## 3. Global Law 9 — label + object = one block

Root cause, not a nudge. Round 1 gave `#b6-nous` (base x = `PL_SOLO` = 390) and
`#b6-nl` (base x = `PL_L` = 190) the **same** ride tween, `x = PL_L - PL_SOLO =
-200`. For the plate that lands on 190. For the label, whose base was *already*
190, it lands on **-10** — off the frame edge, 200px from the card it names.
*Two elements, two coordinate origins, one delta: the arithmetic can only be
right for one of them.*

The fix removes the second origin. `block()` emits ONE positioned group holding
the object and its name in **local** coordinates; motion targets the group; the
label animates opacity only. Four blocks now exist — `b2-lock + b2-name`,
`b6-nous + b6-nl`, `b6-herm + b6-hl`, `b8-mcp + b8-ml`. `guard_label_blocks`
fails the build if any positional tween ever names a labelled object again, so
the bug is no longer expressible.

Measured at the exact beat Miguel named, label ink centroid vs its own card:

| phase | t | round 1 | round 2 |
|---|---|---|---|
| before the ride | 31.54 | +1.3 px | +0.7 px |
| **during** | 32.10 | **-190.6 px** | **+0.6 px** |
| **after** | 33.04 | **-198.6 px** | **-0.1 px** |

(The card centre is read from the WHITE card rectangles, not from ink: the card
band also holds the "HERMES" wordmark, whose black type drags a dark-ink
centroid to the midpoint of the two cards — measured 531 when the Nous card is
at 340. A check that measures the wrong thing passes for the wrong reason.)

## 4. Global Law 8 — edge fade

Scope per the law: only things **cut by an edge**. Two exist here, and both now
end in a 46px alpha ramp (one third of a shelf tile — the widest fade that still
leaves half a tile at full opacity):

* the three **depth lanes**, whose strips are 2–4x canvas width by design and are
  therefore cut by the FRAME edge. Each strip now lives inside a canvas-width
  wrapper carrying a horizontal mask; the step tweens still target the strip, so
  the parallax is untouched.
* the **shelf half-rows** at local y=-74 and y=558, cut by their own container.
  That clip is the "it keeps going" device and it stays — it just stops being a
  hard chop.

Exempt, each for a stated reason: `#root` and the section clips (nothing is cut
by them that the frame edge does not already cut), `#lanes` (it holds the three
already-faded wrappers), and the meter inner clips (they exist to hold the fill
inside the track radius — fading one would fade the pill's own cap, which is the
opposite of Law 11). `guard_edge_fade` fails the build on any other
`overflow:hidden` container without a mask.

Measured on the render, mean deviation from the cream ground in the depth band,
4px slabs walking in from x=0 at t=8.4:

```
round 1   23.0  36.0  47.2  47.1  48.9  25.7 ...
round 2    3.6   6.5  11.6  13.9  13.8  15.6 ...
```

## 5. Global Law 11 — one continuous pill, no end marker

The artefact Miguel screenshotted was `b5-wall`: a 14px bar standing INSIDE the
vessel track, 20px from its end, to say "context is finite". It is a detached
end marker and it is gone. Finiteness is now said by the **track's own border**,
which goes terra on the word and cools again on "picky".

`borderColor` only, never `borderWidth`: the track is `box-sizing:border-box`
and its inner clip is sized `w-8 / h-8`, so growing the border shrinks the
padding box under a fixed-size child and the fill would bleed past the radius.

`guard_round_fills` is geometric, not by name: **no recorded atom may sit inside
a meter's track rectangle**, compared within a scene (atoms from different scenes
overlap in space but never in time — the first version of this check reported 35
false intruders across the whole timeline). Measured on the render, at the 34%
reading, the darkest column mean of the EMPTY tail, over the middle half of the
track's rows:

| | darkest empty-track column |
|---|---|
| round 1 | **209.0** (the wall) |
| round 2 | **251.8** (clean track) |

Round 1's four meters already reached by `width` with the track's own radius
(Law 3, round 1); that is unchanged, and the min-width floor is one cap diameter
— 46px on the shelf meters, 110px on the vessels.

## 6. Self-check

Round 1's nine checks re-run unmodified on the new file (via a shim directory of
symlinks, so no file belonging to another task was edited), plus five new ones:

```
1  CONTAINER     1080x1920  25/1  1354 frames
2  JUDDER        duplicate frames 0.00%
3  AVATAR        head_frac median 0.2572            (v1 approved 0.276, -6.8%)
4  CENTRED       face centre x 539px                (axis 540, offset -1px)
5  SHOULDERS     0 dark pixels at either frame edge in the shoulder band
6  NO OCCLUSION  0.00% of his own head-band pixels differ from the control
7  ROUND FILL    cap bulge 36px and 40px            (straight would be ~0)
8  DEPTH         weakest lane gutter variance 10.2  (round 1: 6.7)
9  AUDIO         54.17s  peak -0.91 dBFS  p50 -22.6 / p85 -16.1 / p95 -13.7
10 HEADREST      4448 px/frame -> 0 px/frame in the exclusion region
11 NO BLANKS     34 blank glyphs -> 0
12 LABEL BLOCK   -198.6px -> -0.1px at t=33.04
13 EDGE FADE     23.0 -> 3.6 deviation at the frame edge
14 LAW 11        209.0 -> 251.8 darkest empty-track column
ALL CHECKS PASS
```

**Every round-2 check is checked for DISCRIMINATION as well as for passing** —
each one fails on `cutout_fix.mp4` and the checker exits 1 if it does not. A
check that passes on both files has measured nothing; two of these (the blank
detector and the end-marker probe) did exactly that on their first version and
were rebuilt.

## 7. What is still true and was not touched

Staging, plate, scale 1.00, centring, the 950px stage zone, the rebalance
offsets, the depth-lane parameters, the caption band, the SFX palette and the
25fps container are round 1's, unchanged. The cream die-cut rim ships, confirmed.

## 8. Files

    cutout2_diag_leak.py       per-row right-extent sweep + on-fraction map (evidence)
    cutout2_headrest_mask.py   the exclusion: still & dark & rarely-subject
    cutout2_matte.py           post stack + exclusion -> matte_cutout2[_rim].webm
    cutout2_envelope.py        silhouette envelope on the excluded matte
    cutout2_gen.py             the generator (laws 8/9/10/11 + their guards)
    cutout2_check.py           the five round-2 checks + round 1's nine
    cutout2_diag_frames.py     contour-over-source proof frames
    matte_cutout2_rim.webm     the matte that ships
    cutout2_envelope.json      the envelope every guard ran against
    _geom_cutout_fix2.json     every derived number this build used
    fix2/                      HyperFrames project
    stage_fix2/                staged assets
    out/cutout_fix2.mp4        the render
    cutout2/frames/            headrest_derivation · exclusion_proof · leakproof
                               · sheet_ba (before/after) · sheet_v2 · sheet_q

---

# FIX ROUND 3 — `cutout_fix3.mp4`
*task id `cutout3`, 2026-08-30. Authority: `format_lab/REVIEW_2026-08-30.md` § ROUND 3.*

> **Morgane, on cutout:** *"captions likely unreadable behind platform UI"* and
> *"the head cutout is not stable"*. Miguel: *"I do agree with her overall"*,
> **captions are the priority**, and **zoom is dropped until the new lens** — no
> virtual set, no matte-on-ground, no blur-pad, no punch-ins.

Two things change. Everything Miguel has already approved — v1 avatar size,
centred, shoulders, the cream die-cut rim, the depth parallax, real logos in
every tile, the edge fades, the welded label+object blocks, the continuous-pill
meters, the SFX palette, the 25 fps container — is round 2's, and the checker
re-runs round 1's nine checks and round 2's four surviving checks on the new
file to prove it rather than assert it.

## 1. The matte — SAM2 ships

`_shared/SAM2.md` verdict: **"Ship it."** `matte_cutout2_rim.webm` is replaced by
`_shared/matte_sam2_rim.webm`, and it is a drop-in by construction: 1080x900,
1354 frames, 25 fps, cream die-cut rim already baked, alpha 57.6 % transparent
at t=24.

The difference is not cosmetic. Rounds 1 and 2 ran **BiRefNet per frame** — the
model answered "which pixels are the person" from scratch 1,354 times, and every
stabiliser downstream (haze kill, keep-largest, 3-frame median, and in round 2 a
static rectangle over the chair) existed to paper over that after the fact. SAM 2
**tracks one prompted object** through the clip. On the numbers `SAM2.md`
measured, over the 271 frames where the picture is standing still:

| still-frame edge motion (px) | round 2 shipped | SAM2 shipped |
|---|---|---|
| whole plate, worst frame | 7,024 | **2,925** |
| **head band, worst frame** | **5,599** | **1,606** |
| head band, mean | 575.1 | **530.2** |

It also removed a defect nobody had named: round 2's exclusion rectangle was
**amputating his raised hand**, up to 2,372 px of it, every time it entered the
chair region.

**Nothing about that was inherited on trust.** `SAM2.md`'s own adoption note says
the silhouette is a different shape and every guard derived from the old envelope
must be re-measured. `cutout3_envelope.py` re-measures it on 452 sampled frames:

```
union y90..899  x0..1079        head y90..680  x134..992
right edge vs round 2:  mean  -3.9px   max +72px   364/810 rows narrowed
left  edge vs round 2:  mean -33.7px   max +13px   402/810 rows narrowed
```

Read that carefully — the mean on the LEFT is negative, i.e. the new silhouette
is **33.7px WIDER** on that side. That is the hand round 2 was cutting off.
A wider subject makes every lane gutter and every occlusion clearance *tighter*,
which is exactly why "the matte got better" is not a licence to skip the guards.
Measured effect on the depth lanes:

| lane | round 2 gutters L / R | round 3 gutters L / R | tile |
|---|---|---|---|
| far  | 357 / 321 | 358 / 322 | 78 |
| mid  | 297 / 301 | 299 / 303 | 116 |
| near | 289 / 337 | **218** / 327 | 148 |

The near lane lost 71px of left gutter to his hand and still clears its own tile
by 70px, so the depth cue is intact and the guard is the reason we know.

## 2. Global Law 12 — the caption

Round 2's pill sat at y=1784: **bottom edge 1838, i.e. 95.7 % of frame height**,
underneath TikTok's creator block (75 %), Shorts' title row (81 %) and Reels'
username (86 %). That is Morgane's complaint, and the review's own table already
called this format's caption the worst offender in the lab.

**Why it could not just move up.** The law wants bottom <= 1382 (72 %) and a
centre in 40-65 %. But 1110..1920 is HIM (the measured silhouette's union top is
canvas y=1110) and 1120..1514 is the depth band. The only cream left is the
shelf between the story stage and his hat, so the frame is **re-divided**:

```
   0 ..  192   dead band     Law 12: nothing meaningful in the top 10%
 192 ..  940   STAGE ZONE    was 100..1050
 940 ..  970   gutter
 970 .. 1078   CAPTION       centre 1024 = 53.3%, bottom 1078 = 56.2%
1078 .. 1110   gutter to his cap
1120 .. 1514   DEPTH BAND    unchanged
1110 .. 1920   HIM           unchanged
```

Every one of those numbers is a constraint, not a preference, and `guard_caption`
asserts all five separately: bottom under the 72 % line, centre inside the
preferred band, 30px clear of the stage zone, 32px clear of him, 42px clear of
the first lane.

**The stage zone shrank by 210px and nothing had to be redrawn.** `rebalance()`
already centres each scene's own block in the zone by a derived offset, so the
scenes simply re-centre: the shelf group's offset goes +65 -> +56, and because
the zone's CENTRE barely moved (575 -> 566) the scenes barely move either. The
one real constraint is that the tallest group (the shelf's, 740px from the shelf
top to the meter bottom) still has to fit; the new zone is 748px, and
`guard_stage` fails the build if it does not.

**Stability is structural, not observed.** There is one `CAP_Y` for the whole
video, so Morgane's *"not a fan of the captions drastically changing position
between modes"* cannot happen here by construction — and the checker still
measures it on the render rather than trusting the constant.

## 3. Global Law 12 — the other two zones, and where I drew the line

The law also bans meaningful content from the **bottom 28 %**, the **top 10 %**
and the **right 15 % column** (x>918, y 30-95 %). `guard_law12` sweeps every
recorded atom against all three. The first two are free and are now hard build
failures. The third is not free, so here is exactly what was done and what was
not.

**Fixed, because the occluded part carries meaning:**

| what | round 2 | round 3 | why |
|---|---|---|---|
| the four meters | x 84..996 / 120..960 | **162..918** | a meter's RIGHT END is where Law 11 says finiteness — "the track's own border is the end wall". Under a Like button it says nothing. |
| the 5 on-demand slots | 5x150+4x30 = 870, slot 4 at x=975 | 5x132+4x24 = **756** | 57px of the fifth tool's plate and 19px of its own mark were under the rail. 132/24 is the shelf's own tile pitch, so the slots are now literally one shelf tile each — an alignment gained, not a compromise. |
| the 6 context candidates + vessel | 6x120+5x24 = 840 | 6x106+5x24 = **756** | same six tools, same vessel-equals-candidates alignment. |
| the MCP server rail | 500+420 = 920 | 494+420 = **914** | 2px over the line. |
| the caption pill | up to **958px wide**, right edge **x=1019** | <=751px, right edge **x=916** | see below. |

One derived constant does all of it: a centred object is symmetric about the
axis, so its half-width cannot exceed 918-540, i.e. `SAFE_W = 756`.

**The caption's own width was the subtle one.** Round 2 sized captions to the
960px content column and met the box by *shrinking type* — a long line came out
at 43px, a short one at 54px. At y=1784 nobody cared. At y=1024 that pill runs
101px into the rail. Round 3 inverts the rule: **one caption size, the largest
this composition uses (54px), and any phrase too long to fit 756px at that size
is SPLIT at a real word boundary**, both halves taking their own word timings.
52 pills become 61, all of them 54px, none wider than 751px. Median pill duration
0.94s -> 0.84s and the shortest 0.36s -> 0.32s, so the rhythm is unchanged.

That splitter found a Law 4 trap on its first run. `"called procedural
disclosure."` splits most evenly into `"called procedural"` + `"disclosure."`,
and `"disclosure."` repeats the **DISCLOSURE** headline on screen verbatim — the
exact double-caption `caption_identity_guard` exists to catch. Split points are
therefore ranked by balance and the first one that paints no on-screen string is
taken, which gives `"called"` + `"procedural disclosure."`.

**NOT fixed, and stated rather than hidden:** the shelf tile fields still end at
x=996 (78px into the rail, 59 % of one 132px tile column) and the three depth
lanes are full-bleed by design. Both are **repeating logo texture**: Law 10
already licenses those fields to repeat marks, which is the same statement as
"no single cell carries information", so occluding one is lossless. Narrowing
the shelf would mean 5 columns instead of 6 — a change to the single most
recognisable image of a format Miguel called *"a LOT better"*, to protect a
repeated logo. `guard_law12` therefore HARD-FAILS on readable atoms in the rail
and MEASURES the texture, reporting 7 atoms and their exact intrusion in the
geometry file. If Miguel wants the whole composition on the 756 grid, COLS 6->5
is a one-line change and 5 rows x 5 columns is 25 cells against a 26-mark roster,
i.e. every cell distinct.

## 4. Two measurements that were wrong before they were right

Both new checks failed on their first version, and both were the check's fault.

**The matte check measured tracking as if it were flicker.** Comparing per-frame
XOR on *every* frame said round 3 was 6.3 % WORSE in the head band. It is the
trap `sam2_flicker.py` documents: round 2 amputates the raised hand, so its matte
holds a static hole and scores a small delta, while round 3 correctly tracks a
moving hand and scores a large one. The metric was inverted to the one Morgane's
complaint actually implies — **flicker is matte motion WITHOUT picture motion** —
by selecting the quietest 20 % of consecutive plate frames and asking about the
matte only there.

**The caption sweep found his face.** A naive terracotta test (`r-b > 60`) passes
on skin, which reads about (200,160,130); the detector reported the pill "at
100 % of frame height" because it had located his cheek. The separating channel
is `r-g` — terra #C4542E has 112, skin has ~40. And the zone check masked "him"
by blanking every row from the plate top down, which also blanked round 2's
caption and made the check score round 2 as clean; it said so itself, via its own
discrimination assertion, which is the only reason it was caught.

## 5. Self-check

`cutout3_check.py` re-runs round 1's nine checks and round 2's four surviving
checks on the new file, unmodified, through the same symlink shim round 2 used
— so no file belonging to another task was edited — and adds four of its own.
The BEFORE side of every round-3 check is `cutout_fix2.mp4`, the file Morgane
reviewed.

```
INHERITED (round 1, on cutout_fix3)
1  CONTAINER   1080x1920  25/1  1354 frames
2  JUDDER      duplicate frames 0.00%
3  AVATAR      head_frac median 0.2592          (v1 approved 0.276, -6.1%)
4  CENTRED     face centre x 537px              (axis 540, offset -3px)
5  SHOULDERS   0 dark pixels at either frame edge in the shoulder band
6  NO OCCLUSION 0.00% of his own pixels differ from the matte-only control
7  ROUND FILL  cap bulge 40px and 38px          (straight would be ~0)
8  DEPTH       weakest lane gutter variance 10.2
9  AUDIO       54.17s  peak -0.91 dBFS  p50 -22.6 / p85 -16.1 / p95 -13.7

INHERITED (round 2, on cutout_fix3, vs round 1)
11 NO BLANKS   34 blank glyphs -> 0
12 LABEL BLOCK -198.8px -> +0.1px at t=33.04
13 EDGE FADE   23.0 -> 3.7 deviation at the frame edge
14 LAW 11      209.0 -> 251.3 darkest empty-track column

NEW (round 3, vs cutout_fix2)
10 MATTE       flicker on the quietest 20% of frames (271 pairs)
11 LAW 12 BAND caption pill bottom 1840px (95.8%) -> 1080px (56.2%)
12 LAW 12 ZONES caption px in the bottom 28%: 757,790 -> 0
13 PILL WIDTH  widest measured right edge x960 -> x874   (rail line x918)
ALL CHECKS PASS
```

**Check 10 in full** — the metric is `sam2_flicker.py`'s, re-run on the two
alphas that were actually composited into the two renders (`stage_fix2/v/` and
`stage_fix3/v/`), not on lab intermediates:

| still-frame edge motion, px | round 2 | round 3 | |
|---|---|---|---|
| whole plate, mean | 1,190.5 | 950.4 | −20.2 % |
| whole plate, p95 | 2,821 | 1,863 | −34.0 % |
| whole plate, worst | 7,373 | **2,755** | **−62.6 %** |
| head band, mean | 573.2 | 516.1 | −10.0 % |
| head band, p95 | 1,088 | 1,091 | +0.3 % |
| head band, worst | 5,653 | **1,645** | **−70.9 %** |

Those independently reproduce `SAM2.md`'s own table to within 5 %, which is the
point of measuring the shipped files rather than quoting the sibling.

**Check 12 in full:**

| zone | round 2 | round 3 |
|---|---|---|
| top 10 %, any ink | 0 | 0 |
| bottom 28 %, caption pixels | 757,790 | **0** |
| right rail column, caption pixels | 2,332 | **0** |
| right rail column, stage texture | 30,797 | 27,308 (the shelf field, §3) |

One number that is NOT an improvement and is reported anyway: the pill's centre
spread over the 90-frame sweep is **0px in both builds**. Round 2's caption was
already perfectly stable — it was stable in the wrong place. Morgane's
"drastically changing position between modes" note was about facesplit, not this
format, and the sweep says so rather than letting the round claim a fix it did
not make.

**Every round-3 check is checked for DISCRIMINATION as well as for passing** —
each one must fail on `cutout_fix2.mp4` and the checker exits 1 if it does not.
Three of the four failed that test on their first version and were rebuilt (§4);
the fourth, the head-band p95, is reported at +0.3 % rather than quietly dropped,
because SAM2's own paperwork predicted it and a table that only shows the
flattering rows is not a measurement.

## 6. What is still true and was not touched

The plate (`_shared/face_wide_25.mp4`, 1080x900, scale 1.00, centred, shoulders
in), the cream die-cut rim, the three depth lanes and their 12-step schedule,
the 26-mark real-logo roster, the 46px edge fades, the welded label+object
blocks, the R1 pill meters, the 7-cue SFX palette at its pinned class constants,
the caption typeface and colour, and the 25 fps container are round 2's,
unchanged. No zoom, no punch-in, no virtual set, no matte-on-ground, no
blur-pad: Miguel dropped the whole zoom programme until the new lens, and
nothing in this build reintroduces it.

**Morgane's third cutout note — "would shine with a REAL screen recording behind
him" — is still unbuilt.** It is a staging idea for a future variant and it does
not belong in a round whose brief was the matte and the captions.

## 7. Files

    cutout3_envelope.py        re-measure the silhouette on the SAM2 matte
    cutout3_envelope.json      the envelope every guard ran against
    cutout3_gen.py             the generator (Law 12 + its two guards)
    cutout3_check.py           the four round-3 checks + rounds 1 and 2's
    _geom_cutout_fix3.json     every derived number this build used
    fix3/                      HyperFrames project
    stage_fix3/                staged assets (incl. the SAM2 matte it composited)
    out/cutout_fix3.mp4        the render
    cutout3/round3_checks.json the measurements above, as JSON
    logs/cutout3_check.log     the full check run

Staged: `/Users/migle/Movies/Shorts Factory/Format Lab/Fixed3/cutout_fix3.mp4`

---

# FIX ROUND 5 — `cutout_fix5.mp4`

*Task `cutout5`, 2026-08-31. Authority: `REVIEW_2026-08-30.md` § ROUND 4 —
**cutout_fix3c is APPROVED and is THE STANDARD** — plus Miguel's round-5 ruling
on top of it: **make him ~10 % bigger**, and do it by SCALING, not shifting.*

**Ships:** `/Users/migle/Movies/Shorts Factory/Format Lab/Fixed5/cutout_fix5.mp4`
— 1080x1920, 25 fps, 1354 frames, 34.5 MB.

## 0. The one-line verdict

`PLATE_SCALE` 1.00 -> 1.10 about the plate's **bottom centre**. His cap rose
**76 px** (median of 60 decoded frames), his base did not move, and the scale can
be read back out of the pixels: **k = 1.0997**. Everything the round-4 verdict
approved is intact; the 80 px of vertical budget the bigger silhouette consumed
came out of the tool-shelf scene, not out of the caption seat.

## 1. Why a scale and not a shift, in geometry

A shift of the plate up by *d* moves his cap up by *d* and his shoulders up by
*d* — and the plate's bottom edge with them, so a strip of bare cream *d* px
tall opens between his chest and the frame bottom. Full-bleed is the format
(Law 1's raw 0 % plate); the strip would be a hole.

A scale about the bottom centre is the map

    y  ->  k*y + (1-k)*1920          x  ->  540 + k*(x-540)

whose fixed point is **y = 1920, the frame's bottom edge**. The base is welded
there by construction, and only the cap moves. The plate grows past both side
edges by 54 px, which costs nothing: rows 840..900 of the matte are already
edge-to-edge (`row_x0 = 0, row_x1 = 1080`), and `#root` clips.

| | round 3/4 (the standard) | round 5 |
|---|---|---|
| PLATE_SCALE | 1.00 | **1.10** |
| plate box | 1080x900 at (0, 1020) | **1188x990 at (-54, 930)** |
| head height (FRAMING geometry) | 500 px, 26.0 % of frame | **550 px, 28.7 %** |
| silhouette union top | 1111 | **1030** |
| nominal cap top | 1163.8 | **1088.1** |
| chin | 1663.8 | **1638.1** |

## 2. The envelope debt, paid

`cutout3c_matteswap.sh` swapped `matte_sam2_rim_v2` -> `_v3` and deliberately did
**not** re-measure the envelope ("the brief is a matte swap and not a new
layout"); `_shared/SAM2.md` records the re-derivation as owed. It could not be
deferred again, because at k=1.10 every gutter and every clearance is a function
of the silhouette's real shape. `cutout5_envelope.py` measures the SHIPPED file:

    matte_sam2_rim_v3.webm   452 frames   union y91..899 x0..1079
                             head  y91..680 x135..990
    vs the v1-matte envelope every earlier guard used:
      row_x0  mean +1.4 px   max +80 px      row_x1  mean +0.6 px  max +62 px

The envelope is measured in PLATE space and is therefore scale-free — `FixStage`
maps it with `k` — so the same file describes the bigger silhouette correctly.

**What the debt actually cost: nothing, and that is worth stating.** Re-measured
at k=1.00, the lane gutters are 218 / 299 / 218-vs-327 px — identical to the
numbers fix3c was guarded with. The v3 changes land in rows the lanes do not
cross. Every gutter that moved in round 5 moved because of the SCALE:

| lane | tile | fix3c as guarded (v1 env, k=1.00) | v3 env, k=1.00 | **v3 env, k=1.10** |
|---|---|---|---|---|
| far | 78 | 322.0 | 323.0 | **279.3** |
| mid | 116 | 299.0 | 299.0 | **273.8** |
| near | 148 | 218.0 | 218.0 | **148.4** |

## 3. What 10 % costs, and who pays it

The budget above him is fixed at both ends: Law 12 owns 0..192, and his union
top is now 1030 instead of 1111. That is **838 px**, where round 3 had 919.
Into it must fit the stage zone, the 108.2 px caption pill and 26 px of cream on
each side of the pill. **The caption seat is not negotiable** — one stable seat,
in the cream, clear of his cap, clear of the depth band, Law-12 compliant — so
the 80 px comes out of the story furniture:

    0    .. 192    dead band       (unchanged)
    192  .. 869    STAGE ZONE      (was 192..940)
    869  .. 895    gutter          (26, unchanged)
    895  .. 1004   CAPTION         (centre 949.5 = 49.5 %, bottom 52.3 %)
    1004 .. 1030   gutter to his cap (26, unchanged)
    1120 .. 1514   DEPTH BAND      (unchanged — the lanes did not move)
    1030 .. 1920   HIM

Round 3 hard-coded `CAP_Y = 1024` and `ZY1 = 940` and wrote the derivation in a
comment. At a new `PLATE_SCALE` both numbers are wrong by 80 px and a comment
cannot notice, so round 5 **executes** the derivation instead, off the measured
union top. That is the structural fix, not the new constants.

`rebalance()` used to only CENTRE each scene's block in the zone. It now also
**fits** it: `s = zone_height / group_height` when the group is over size, about
the zone centre, with every recorded atom and every meter rectangle rewritten to
the resulting coordinates so the guards and the pixel checker keep measuring
what is on screen. It is a UNIFORM scale (nothing inside a scene is
re-proportioned — the round-4 facesplit failure was the opposite of this) and it
is PER GROUP:

| group | authored | fitted | s |
|---|---|---|---|
| **shelf** (hook/wrong/spoiler/infinite) | 740 | **677** | **0.9147** |
| term, ondemand, context, lab, payoff, outro | 465, 465, 358, 235, 384, 417 | same | **1.0000** |

Eight of the nine scenes are geometrically identical to fix3c. One — the tool
shelf, a texture field of logo tiles and the least legibility-critical thing in
the video — is 8.5 % smaller.

## 4. 1.10 is the ceiling, by 0.1 %

Binary-searching the near lane's gutter against its own tile width on the v3
envelope: **the largest legal PLATE_SCALE is 1.1011.** At 1.10 the near lane's
worst gutter is 148.4 px against a 148 px tile — 0.4 px of margin. Miguel's
"~10 %" landed one thousandth under the number where a whole tile stops fitting
beside him and the depth cue Miguel called the format's best moment starts to
read as a sliver. **Anything past 1.1011 requires re-authoring the near lane,
not just moving a constant**, and this is the number to look at first if a
future round asks for bigger again.

## 5. Self-check — `cutout5_check.py`

Four measurements, all off decoded pixels, all against `cutout_fix3c.mp4`.

**14 CAP TOP — the ruling, read back out of the render.** His cap is located per
frame by darkness inside a window nothing else can occupy (below both builds'
pill bottoms, above the mid lane, x 280..800; a lane tile at opacity 0.34/0.66
over cream cannot go below 165/85, his cap sits at 20-50, the threshold is 70).

| | fix3c (standard) | fix5 (round 5) |
|---|---|---|
| cap top, min | 1122 | **1043** |
| cap top, median | 1158 | **1082** |
| cap top, max | 1166 | **1091** |
| cream px under him, rows 1900-1919 | 0 | **0** |

His cap rose **76 px** (median; 75..79 across the sweep). The scale is then read
off the lever to the anchor rather than off a regression — his cap only travels
44 px across the take, so a line fitted to (y3, y5) has a slope dominated by
±1 px quantisation, while the ~800 px lever to y=1920 turns the same 1 px into
0.0013 of k. **k = 1.0997, spread 0.0022 over 60 frames.** The identity
`y5 = 1.10*y3 - 192` holds with a mean residual of **+0.15 px** and a worst case
of **0.90 px**, which is the anchor and the size proven in one line. And the
anchor is also simply looked at: zero cream under him in either build, so
nothing opened at his base.

**15 COLLISIONS — the clearance table at the new size.**

| element | rule | measured | limit |
|---|---|---|---|
| caption pill | bottom clear of his cap (union of 452 frames) | 26.5 | >= 26.0 |
| caption pill | top clear of the stage zone | 26.5 | >= 26.0 |
| caption pill | bottom clear of the first depth lane | 116.4 | >= 26.0 |
| caption pill | bottom above Law 12's 72 % line | 378.8 | > 0 |
| stage atoms | atoms overlapping the silhouette | 0 | == 0 |
| stage atoms | lowest front atom (`b1-met`) to the pill top | 26.5 | >= 26.0 |
| stage atoms | highest front atom above the top-10 % line | 0.0 | >= 0 |
| lane far | worst gutter beside him (78 px tile) | 279.3 | >= 78 |
| lane mid | worst gutter beside him (116 px tile) | 273.8 | >= 116 |
| lane near | worst gutter beside him (148 px tile) | 148.4 | >= 148 |
| plate | his base to the frame bottom | 0.0 | == 0 |

The geometric rows come from the build's own guards, which run against the UNION
envelope — the worst of 452 frames, not an average — so each is a guarantee over
the whole take. The tightest of them is then re-measured off the render frame by
frame: **pill bottom to the top of his cap, 60 frames, min 37 px, median 76 px,
max 85 px.** (The decoded minimum is larger than the geometric 26.5 because the
geometric number is against the union — the single highest frame of the take —
while the decoded sweep is 60 samples of a moving head.)

**16 ONE FONT — round 5's new law, measured on glyphs.** 138 pills swept.

| | measured |
|---|---|
| pill height, distinct values over the whole video | **[112]** — one value, spread 0 px |
| implied font from that height | 56.9 px (declared 54 px; the browser's line box is 1.37em, the generator's worst case assumed 1.30em) |
| glyph ink height | 34..49 px, p50 48, p95 49 — one cluster |

Pill height is a pure function of font size (`line-height*fs + 2*pad`), so a
single value over 138 pills is an exact proof of a single size; the glyph ink is
measured as well because the law asks for glyphs, and 49 px is one 54 px
ascender-to-descender extent.

> **A measurement bug caught by its own implausibility, worth writing down.**
> The first glyph pass reported ink heights of **3..30 px** for a 54 px font.
> `pill_component` returns the TERRA connected component, which is the pill with
> the letters punched OUT of it — the white glyphs are exactly the pixels it does
> not contain, so ANDing "white" with that mask measures the antialiased fringe
> and nothing else. The fix is to flood-fill the outside first and take the white
> inside the SOLID pill. A number that is impossible for the thing it claims to
> measure is a bug in the measurement, not a finding.

**17 LAW 12 — re-earned at the new seat**, because the caption moved 74.5 px up
and none of round 3's numbers carry over.

| | fix3c | fix5 | limit |
|---|---|---|---|
| pill bottom | 1080 (56.2 %) | **1006 (52.4 %)** | <= 1382 (72 %) |
| pill centre | 53.3 % | **49.5 %** | 40-65 % |
| centre spread over 90 frames (ONE seat) | 0.0 px | **0.0 px** | <= 8 |
| widest pill right edge | — | **x874** | rail line x918 |
| ink in the top 10 % | — | **0 px** | <= 200 |
| caption px in the bottom 28 % | — | **0 px** | 0 |
| caption px in the right rail column | — | **0 px** | 0 |
| stage TEXTURE px in the right rail | 30,797 (round 2) | 2,107 | reported, licensed (§3 of round 3) |

## 6. What is still true and was not touched

The raw 0 % full-bleed plate and its matte (`matte_sam2_rim_v3`, the round-4
standing matte), the cream die-cut rim, the centred/symmetric composition, the
three depth lanes with their y band, tile sizes, opacities and 12-step schedule,
the 26-mark real-logo roster, the 46 px edge fades, the welded label+object
blocks, the R1 pill meters, the 7-cue tamed SFX palette, the caption typeface,
colour, ONE 54 px size and 756 px width bound, and the 25 fps container are
fix3c's, unchanged. No zoom, no punch-in, no new staging idea.

## 7. Files

    cutout5_envelope.py        re-measure the silhouette on the SHIPPED v3 matte
    cutout5_envelope.json      the envelope every round-5 guard ran against
    cutout5_toprow.py          what the union top IS (his cap, not a raised hand)
    cutout5_gen.py             the generator (derived seat + fit-then-centre)
    cutout5_check.py           checks 14-17
    _geom_cutout_fix5.json     every derived number this build used
    fix5/                      HyperFrames project
    stage_fix5/                staged assets
    out/cutout_fix5.mp4        the render
    logs/check_fix5.json       checks 14-17 as JSON
    logs/check_fix5.log        the full check run
    logs/fix5_frames/          the fix3c-vs-fix5 comparison sheet

Staged: `/Users/migle/Movies/Shorts Factory/Format Lab/Fixed5/cutout_fix5.mp4`

---

# ROUND 6 — THE CLOSING CAPTIONS ROUND (`cutout_fix6`)

**Brief.** Every definitive format video must carry the IDENTICAL caption
specification. cutout_fix5 is Miguel's favourite and is APPROVED, so this round
is the minimum possible touch: put the caption pill on the canonical spec, at its
existing fix5 seat, and change nothing else.

## 1. What the canonical pill IS — read, then measured

It is not a lab invention. It is the PUBLISHED factory's own pill, taken from
`shorts_run8/projects/mcpupgrade_icon/index.html` and then MEASURED in the render
browser rather than assumed:

| | canonical (published) | fix5 | fix6 |
|---|---|---|---|
| font | Nunito 800, **56.2px** | Nunito 800, 54.0px | **56.2px** |
| padding | **18.8px 33.8px** | 19.0px 34.0px | **18.8px 33.8px** |
| radius | **22.5px** | 22px | **22.5px** |
| background / colour | **#C4573A / #fff** | same | same |
| letter-spacing / transform | **normal / none** | same | same |
| box-shadow | **none** | `0 6px 22px rgba(20,20,22,.22)` | **none** |
| RENDERED pill height | **114.59px** (38 pills, ONE value, spread 0) | 112px | **114.59px** |
| line box | **1.3699em** | 1.3699em (the generator modelled 1.30) | **1.3699em** |

56.2 is 30 design units x 1.875 — the published project authors at 576 wide and
scales into the 1080 space, which is why the spec reads "30px" upstream and
56.2px here. **The pill height to compare across formats is 114.59px.**

**The shadow is the one change that is not type or padding.** The canon has none;
leaving fix5's would make cutout the single format that does not match the
standard. It is one constant (`box-shadow` in `base_css`) if Miguel wants it back.

## 2. The seat did NOT move, and that is enforced

The canonical pill is 2.6px taller than fix5's. Re-solving the seat from the new
height would move `CAP_Y`, `ZY1`, the stage zone and every rebalanced atom in an
APPROVED video, so `CAP_H` is now a **frozen literal (108.2)** and both
`cutout6_gen.py:main` and `guard_caption` hard-fail if `CAP_Y`/`ZY1` come out as
anything other than **949.5 / 868.9**. The taller pill grows 1.3px each way about
its fixed centre instead. Measured on the render: **fix5 centre 950.0 -> fix6
949.0, spread 0.0px over 90 frames; bottom 1006 in both.**

One honest correction while here: fix5's clearances were reported as 26.5px from
a 1.30em model, but the pill it painted was 112px, so the REAL clearance was
24.6px — and that build was approved. fix6's real clearance is **23.3px**, and
the guard now asserts against the true rendered height instead of a model.

## 3. The width estimator is retired

Rounds 2-5 sized the pill with `0.575 * len(text) * fs + 2*pad`. At 56.2px that
estimate calls `"procedural disclosure."` a **778.6px** pill; Chromium lays out
**670.4px**. The estimate therefore demanded a split whose only two halves —
`"procedural"` and `"disclosure."` — both repeat an on-screen headline verbatim,
and the build **deadlocked on Law 4**. That is an estimator failure, not a design
problem, so `cutout6_pillw.py` now lays the real `.scappill` box out in Chromium
(the renderer itself), over every contiguous word run of every phrase, and caches
the answers. It also refuses to measure unless `document.fonts.check` confirms
Nunito 800 answered — a canvas `measureText` shortcut was tried first and
silently under-reported by ~70px against a fallback face.

Round 3's law is unchanged: **one size, never shrink, split at a real word
boundary with real word timings.** Only the ruler changed.

| | fix5 | fix6 |
|---|---|---|
| pills | 61 | **58** |
| phrases split | 9 | **6** |
| widest pill | 751.1px (estimated) | **725.3px (measured)** -> right edge **x902**, rail x918 |
| word stream | — | **byte-identical to fix5** (58 pills concatenate to the same words, same first/last timing, same 53.66s of pill time) |

## 4. Containment — and the control that makes it a verdict

**The mp4 diff cannot answer this question.** H.264 allocates bits across the
whole frame, so changing the caption perturbs the silhouette's macroblocks by up
to 63/255 with no content change at all. That number is reported and deliberately
NOT asserted on.

The comparison is made BEFORE the encoder: both projects rendered as RGBA
png-sequences, all 1354 frame pairs diffed exactly. And because the RENDERER is
not bit-exact run to run, fix5 was rendered a **second** time as a NULL CONTROL.

| rows | fix5 -> fix6 | what it is |
|---|---|---|
| 874..1037 | **102,985 px** | the pill + the retired shadow's halo — **the caption band** |
| everything else | **323 px** (worst cluster 212) | scattered antialiasing |
| — | **313 px** (worst cluster 196) | **the same measurement between two renders of fix5 ITSELF** |

Law 12's top band: **0 px**. Source-level: the two `index.html` files differ on
exactly 126 lines — the `<title>`, the five `.scappill` CSS lines, and the caption
clips. Nothing else in the composition differs by a byte.

**Verdict: outside the caption band, fix6 differs from fix5 by no more, and no
differently, than fix5 differs from a second render of itself.**

## 5. One font, on rendered glyphs (round 5's law, re-earned)

138 pills swept off `cutout_fix6.mp4`:

| | measured |
|---|---|
| pill height, distinct values | **[114]** — one value, spread 0px (canon 114.59) |
| implied font from that height | **55.8px** (declared 56.2, 1.3699em line box) |
| glyph ink | 40..51px, p50 50, p95 51 — one cluster |

## 6. Untouched

The v3 matte, the cream die-cut rim, PLATE_SCALE 1.10 and the planted base, the
depth field and its 12-step schedule, the 26-mark logo roster, the edge fades,
the welded label blocks, the R1 pill meters, the 7-cue SFX palette, the rebalance
and the 25fps container are fix5's, byte-identical.

## 7. Files

    cutout6_gen.py                 the generator (canonical pill, frozen seat)
    cutout6_pillw.py               the retired estimator's replacement (Chromium)
    cutout6_pillw.json             the measured width cache (352 strings)
    cutout6_check.py               checks 18-20
    cutout6_containment.py         the lossless png diff + its null control
    _geom_cutout_fix6.json         every derived number this build used
    fix6/                          HyperFrames project
    stage_fix6/                    staged assets
    out/cutout_fix6.mp4            the render
    logs/check_fix6.json/.log      checks 18-20
    logs/containment_fix6.json     the containment geography and the control
    logs/fix6_masks/*.npz          the two union diff masks (the raw evidence)

Staged: `/Users/migle/Movies/Shorts Factory/Format Lab/Fixed6/cutout_fix6.mp4`
