# falagent — SHARED LANE SCENE HANDOFF

**From the design agent, for the SPLIT author and for the CUTOUT author.** The plan
(`plans/falagent_plan.json`) is the contract; this file is the convenience. If they
disagree, the plan wins and you write your own note. Neither lane redraws anything in
this module: it is sealed with `production.py seal` (v4: module + handoff hashes,
`review/artwork_pass_falagent.json`), and a lane that builds on a changed module is
refused. Section 9 lists where this module departs from the plan's letter.

---

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/falagent_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import falagent_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_falagent_proof.py` (`--set seal` static crops, `--set compose` settled chapter frames, `--set timeline` the REAL GSAP timeline: bespoke crops, 18 frames, both ends of every connector at 3x) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the WHOLE 33.24 s scene: html to drop inside ONE
`transform: scale(k)` wrapper (`transform-origin: 0 0`), and a list of 93 `tl.*`
JavaScript strings for your own timeline. It reads no files and takes no format
argument; every difference between the two formats is PLACEMENT plus the `lockup`
string. It calls `SC.assert_anchor_law()` before it writes a byte.

**EASES.** The tweens name three chassis eases as bare identifiers: `SOFT`, `POP`,
`SWING`. Define them BEFORE the tweens, as the sibling generators do:
`const POP="back.out(2.05)";const SOFT="power3.out";const SWING="power2.inOut";`.
One tween (the dart) carries a quoted literal ease, `"power2.in"`.

Keys use class `mono` (the chassis' JetBrains Mono uppercase rule, weight 800 set
inline). The address-bar text `fal.ai` sets `text-transform:none` inline (it is a URL,
UI text, not a label).

### `media` — five rasters

```python
for key, rel in SC.LOGO_FILES.items():
    CC.MARK_INK[key] = CC.measure_mark(key, LOGOS / rel)
media = {f"_{key}_img": CC.mark_img(LOGO_URL[key], key, SC.MEDIA_SIDES[key])
         for key in SC.LOGO_FILES}
#   _falai_img   72.0 (the 132 px fal plate; used by #fal-tile AND #fal-tile-2)
#   _flux_img, _gemini_img, _minimax_img, _qwen_img   56.0 (112 px tiles)
```

The URL must be page-relative (`assets/logos/<basename>`).

**THE FILES ARE NAMED, NOT GUESSED** (`SC.LOGO_FILES`, relative to
`~/Documents/Workspace/assets/logos/`):

| key | file | note |
|---|---|---|
| `falai` | `ai-models/falai-mark.png` | the library's fal favicon (`tool-web-icons-20260914/falai.png`) with its opaque pale-pink ground keyed to alpha, geometry untouched; derived 2026-09-23, `falai-mark.provenance.json` beside it, catalogue rebuilt. Never use the favicon itself: it paints a pink square inside the tile |
| `flux` | `ai-models/flux.png` | |
| `gemini` | `ai-models/gemini-color.png` | the colour spark |
| `minimax` | `ai-models/minimax-color.png` | |
| `qwen` | `ai-models/qwen.png` | |

All five pass `cutout_depthfield.assert_cast_resolves` (checked 2026-09-23).

There is no source post, no screenshot and no other raster in this video
(`pointing_cues.py` returned zero cues).

### `lockup` — the outro's handle block

```python
CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W) \
  + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W)
```

Seated inside the scene's own `#o-slot` (core top 324). `handle_key` is the only
string that differs between masters: `"yt"` on the split, `"tiktok_ig"` on the cutout.

---

## 2. THE UNITS

**CORE px = the plan's CANVAS px with y shifted by -192.** `canvas_y = core_y + 192`,
x untouched. `SC.CORE_W, SC.CORE_H = 1080.0, 600.0`.

* `SC.CONTENT_Y0, SC.CONTENT_Y1 = 86.0, 494.0`: the band the core really paints in
  (canvas 278 … 686, 14.5 % … 35.7 % of frame height). Y0 is the browser window's top
  edge (ch6); Y1 is the `ANY GENERATION` key's box bottom. At k = 1 the lowest ink
  clears the caption pill's top (~787.7) by ~100 px.
* Every chapter is symmetric about x = 540 (ink extents: ch0 264 … 816, ch1 160 …
  904, ch2 256 … 824, ch3 410 … 670, ch4 240 … 840, ch5 230 … 906, ch6 220 … 860).
  So `left = (1080 − 1080·k) / 2`.
* Seat the core so its CONTENT BAND is centred on your stage zone:
  `top = round(centre - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 * k, 2)`.
* Rail check (x > 918 at y ≥ 30 % of the frame): at k = 1 nothing readable passes
  x 918 (the widest right-hand key, `IMAGES`, has ink to ~884; `FAL AGENT` ink to
  ~888). On the cutout, check the right-hand keys against your own mapping.

**GATE-SCALING.** Non-block gutters are authored at ≥ 24 core px: every key sits 24 px
under its host; clapper ↔ palette 80+, palette ↔ easel 90+, model tiles 40 apart (a
series), ch5 plate ↔ FINE-TUNED 24, dartboard-2 / strip-2 ≥ 30 from FINE-TUNED's box.
The connectors run 70+ px clear of every key (conn-prompt passes FINE-TUNED's box
at x 378 when the box starts at 410).

---

## 3. THE TIMELINE

`SC.CUE` carries every instant (word STARTS from `cuts/falagent/transcript_tight.json`
unless marked `authored`, each inside its word's 1.0 s window). `SC.BEAT_EDGES` is the
plan's beat table; `SC.DUR = 33.24`.

| ch | t | on screen |
|---|---|---|
| 0 | 0.10–6.34 | the PALETTE pops alone on the axis (0.10, 'Creative'); a terracotta spark pops by the brush tip ('AI', 1.22); the palette slides left ('best', 2.24, the ONE LAW-19 displacement); the fal plate pops right ('fal.ai', 2.88); the terracotta line palette → plate draws ('just', 3.78); `FAL AGENT` under the plate ('agent', 4.88, the first type in the video) |
| 1 | 6.34–11.68 | plate, line and key fade while the palette glides back to centre at 0.85 ('creative', 6.34); the CLAPPERBOARD pops left ('videos', 8.56) and its stick claps shut and re-opens (8.80); `VIDEOS` (8.62); the EASEL pops right ('images', 9.40); `IMAGES` (9.46); holds through 'the hard thing is not' |
| 2 | 11.68–13.02 | everything fades while four model tiles pop IN the erase ('choosing', 11.68, 0.05 apart): FLUX, Gemini, MiniMax, Qwen; the Gemini tile's border flips terracotta ('the', 12.02) and back ('It's', 12.62); `THE MODEL` (12.12) |
| 3 | 13.02–15.16 | the DARTBOARD pops IN the erase ('getting', 13.02); `THE PROMPT` ('prompt', 13.46); the dart flies in along its axis and lands in the bullseye (13.70-13.88, inside 'right') |
| 4 | 15.16–17.86 | the FILM STRIP pops IN the erase ('all', 15.16); the same cat pops into each frame ('generations', 15.52, 0.16 apart); `CONSISTENT` (16.40); the three frame outlines flip terracotta ('across', 17.04) and back (17.66) |
| 5 | 17.86–24.10 | the fal plate pops back at top centre IN the erase ('fal', 17.86); `FINE-TUNED` (19.18); the small dartboard and small strip pop below ('do', 20.04 / 20.12); two terracotta lines draw from the plate's sides to their tops ('exactly', 20.40) |
| 6 | 24.10–29.06 | key, dartboard-2, strip-2 and lines fade; the BROWSER WINDOW pops round the centre and the plate walks into its left side ('inside', 24.10, 0.46 s); `fal.ai` appears in the address bar ('website', 25.14); the picture card (the cat) and the video card (a small clapperboard) pop on the right ('help', 26.80 / 26.90); two lines draw plate → cards ('you', 27.06); `ANY GENERATION` under the window ('generation', 27.74) |
| 7 | 29.06–33.24 | opaque rising sheet (29.06); the small palette glyph without spark (29.54), rule (29.84), lockup (29.94) |

Every erase is a handover, never a blank (LAW 43 / LAW 45): the palette crosses seam 1,
the model tiles / dartboard / strip / plate pop inside seams 2-5, the plate crosses
seam 6 into the window. The last board event (the output lines) settles by 27.36; the
last key lands by 28.02, 1.04 s before the outro anchor.

---

## 4. THE FIVE BESPOKE OBJECTS — DO NOT REDRAW

`SC.BESPOKE` carries CORE boxes and the held instant of each. Self-checked at phone
size (405x720) by the design agent (v4, no cold readers), on BOTH the static paint and
the real timeline.

| i | object | t | core box | proof |
|---|---|---|---|---|
| 0 | an artist's palette | 2.00 | 407.2, 145.4, 672.8, 332.6 | `review/proof_falagent/00.png`, `tl_00.png` |
| 1 | a movie clapperboard | 9.30 | 160, 144, 340, 340 | `01.png`, `tl_01.png` |
| 2 | a painter's easel | 10.40 | 756, 114, 904, 346 | `02.png`, `tl_02.png` |
| 3 | a dartboard with dart | 14.60 | 410, 96, 670, 356 | `03.png`, `tl_03.png` |
| 4 | a film strip | 16.90 | 240, 110, 840, 310 | `04.png`, `tl_04.png` |

`05.png` is the browser window (UI chrome, declared `data-ui="1"`, not a bespoke
object). Map `core` boxes through your own k and origin when you cut crops.

---

## 5. THE DECLARATIONS YOU INHERIT

* **CONNECTORS TOUCH WHAT THEY CONNECT (Miguel, 2026-09-22) + LAW 40.** Five
  connectors, `SC.CONNECTORS` (id → from, to, ends). Every end sits on the OUTER edge
  of the outline it joins, computed from the object's authored outline;
  `SC.assert_anchor_law()` re-derives each and refuses a gap or an overshoot above
  0.5 px (all five report 0.0 px). The round cap laps 3 px into the outline, so no
  cream shows. Verified on the real timeline: `review/proof_falagent/tl_conn_*.png`.
  * `conn-friend` palette → `fal-tile`: (529.5, 239) the palette's rightmost outline
    point → (684, 239) the plate's left edge; level.
  * `conn-prompt` `fal-tile-2` → `dartboard-2`: (474, 166) → (300, 330) the ring's
    outer edge at 12 o'clock. `conn-consist` → `strip-2`: (606, 166) → (780, 330).
    Mirror-symmetric about x 540.
  * `conn-out-a` / `conn-out-b` plate → `out-image` / `out-video`:
    `anchor_points(FAL3_BOX, 2, "right", inset=0.25)` = (434, 249) / (434, 315),
    clear of the plate's 18 px corner radius, → (618, 212) / (618, 352); mirrored
    about the plate's middle (282).
  * Each carries `data-connect-to` + `data-overlap-ok`, declares `pathLength="100"`
    and obeys THE GHOST RULE (stroke-opacity 0 until 0.04 s after its draw starts).
  * All tiles/cards are `box-sizing: border-box`, so the box edge IS the visible
    border in any page. Do not override it.
* **LAW 39 / 50**: eight keys, each `data-label-for`, ALL below their hosts and centred
  on their host's axis: `FAL AGENT` → `fal-tile`, `VIDEOS` → `clapper`, `IMAGES` →
  `easel` (the two siblings share one baseline), `THE MODEL` → `model-row` (a
  transparent `data-container` holding the four tiles), `THE PROMPT` → `dartboard`,
  `CONSISTENT` → `strip`, `FINE-TUNED` → `fal-tile-2`, `ANY GENERATION` → `window`.
  `FAL AGENT` and `FINE-TUNED` both name the fal plate and both sit under it.
* **LAW 9**: the key term `FAL AGENT` (48 px, 25.6 design units) is the first type in
  the video, written alone on 'agent' (4.88).
* **LAW 41**: `SC.DECLARED_BLOCKS`, stamped as `data-block`. `#window` is a
  `data-container` (`data-ui="1"`) for the plate and the two output cards.
* **LAW 42**: `SC.LIFETIMES`. Chaptered board: every board mark has a finite window;
  only the four outro marks are anchors (`SC.SCENE_ANCHORS`). The longest board marks
  are `#fal-tile-2` (17.86-29.54, 35.1 %) and `#palette` (0.10-11.68, 34.8 %).
* **LAW 38**: exactly TWO emphases, both boxing on drawn objects, no highlight (no
  raster text exists): `#model-1` border → `rgb(221,114,89)` at 12.02, back at 12.62;
  `#strip .stfr` strokes → terracotta at 17.04, back at 17.66. No `<circle>` or
  `<ellipse>` tag anywhere; every round shape is a two-arc path.
* **LAW 51**: the dart, the cats, the spark and the clapper stick are INSIDE their
  objects' elements, so they move with them. The dart flies within `#dartboard`; the
  clapper's stick rotates about its own hinge (`svgOrigin "16 70"`).
* **HIDDEN-AT-0 SETS**: `#palette .spk`, `#dartboard .dart` and `#strip .cat` are set to
  opacity 0 at t = 0 by `tl.set` (their HTML is visible so the proof harness can paint
  the settled state). Prime the timeline (progress 1 → 0) as Gate 1 does before you
  sample it.

---

## 6. THE POINTING CUE

None. `pointing_cues.py --vid falagent`: "no pointing cue in this take";
`gen/_cues_falagent.json` has `cues: []`; the prep `cues` marker agrees (cue_count 0).

---

## 7. WHAT THE CUTOUT OWNS

* The matte and stage-zone seating. Markers at the end of the artwork: `cut` ok
  (33.24 s, "model-authored keep ranges"), `plate` ok (over-wide, crop
  3640x1820+52+238, scale_k 0.4945, face_dx −0.02 %, head 449.7 canvas px), `prompt0`
  ok (wing_review true, the instrument abstained, no cut), `selection` ok ("selection
  inputs ready for the outline review"), `track` ok (matanyone2, $0.0169 est.), `ship`
  ok (831 frames, soft alpha, rim 7, min person fraction 0.286, $0.0417 est.), both
  `needs_final_visual_review`; `cues` ok. The Astra matte step owns the selection
  review and the matte. `plate_origin()` must read `left` from `plate_box`.
* `SC.CUTOUT_LOGO_LANES = ("flux", "midjourney", "higgsfield", "minimax", "gemini",
  "openai")`, files in `SC.CUTOUT_LOGO_FILES` (relative to `assets/logos/`): the image
  and video models and the creative AI platforms a fal user works among. Mixed, none
  repeated, never `falai` (it is on the stage). All six pass
  `cutout_depthfield.assert_cast_resolves` (checked 2026-09-23).
* Your own k and origin. The logo lanes fade in after the hook lands (after 0.50, when
  the palette has popped), never later.

## 8. WHAT THE WHITEBOARD DOES NOT DO

It does not import this module. It redraws the same argument in marker ink per beat
`whiteboard_version` in the plan: the same palette (thumb hole, dabs, brush, spark),
the fal mark pasted in a drawn plate with the line to it, the clapperboard and easel
either side of the palette, the four model marks in drawn tiles, the dartboard with the
dart, the film strip with the same cat three times, the plate with lines to the small
dartboard and strip, the browser window with fal.ai, the cat card and the clapperboard
card; same keys at the same words.

---

## 9. WHERE THIS MODULE DEPARTS FROM THE PLAN'S LETTER

1. The plan's `bbox` values are normalised canvas boxes at the split placement;
   `SC.BESPOKE` carries the real CORE boxes and is authoritative for geometry.
2. The plan's `spark`, `dart` and `cats` are classes inside their objects (`.spk`,
   `.dart`, `.cat-0..2`), not separate ids; `url` is `#window .urltxt`. Same windows.
3. The plan's `model-row` is a transparent container `#model-row` holding `#model-0`
   … `#model-3` (FLUX, Gemini, MiniMax, Qwen; the pick is `#model-1`).
4. `conn-out-a` / `conn-out-b` start at `anchor_points(..., inset=0.25)` rather than the
   default 0.16, to land on the plate's straight edge clear of its corner radius (the
   2026-08-16 junction note).

---

## 10. PROOF EVIDENCE

| what | where |
|---|---|
| phone-size crops, one object alone per 405x720 frame (static paint) | `review/proof_falagent/00.png` … `05.png`, `NN_tight.png` (3x) |
| the same objects seeked on the REAL timeline | `review/proof_falagent/tl_00.png` … `tl_04.png` |
| 18 real-timeline frames across every chapter and seam | `review/proof_falagent/tl_frame_*.png` |
| both ends of every connector at 3x, real timeline | `review/proof_falagent/tl_conn_<id>_<0|1>.png` |
| composed settled chapter frames (GRAPHIC CHART clause 9) | `review/proof_falagent/compose_*.png` and `*_phone.png` |
| manifests | `proofs_seal.json`, `proofs_compose.json`, `proofs_timeline.json` (0 page errors) |
| the seal record | `review/artwork_pass_falagent.json` |
