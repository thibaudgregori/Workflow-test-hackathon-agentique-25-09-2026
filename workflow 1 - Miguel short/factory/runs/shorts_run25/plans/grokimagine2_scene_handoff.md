# grokimagine2 — SHARED LANE SCENE HANDOFF

**Written by the design agent for the SPLIT author and Astra's CUTOUT.** The plan
(`plans/grokimagine2_plan.json`) is the contract; this file is the convenience. If
anything here disagrees with the plan, the plan wins and you write your own note.
Section 9 lists where this module departs from the plan's letter.

Neither lane redraws anything in this module. The scene is sealed with
`production.py seal` (v4: module + handoff hashes, `review/artwork_pass_grokimagine2.json`);
a lane that builds on a changed module is refused.

---

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/grokimagine2_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import grokimagine2_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_grokimagine2_proof.py` (`--set seal`, `--set compose`) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the WHOLE 32.32 s scene: html to drop inside one
`transform: scale(k)` wrapper, and a list of `tl.*` JavaScript strings for your own
timeline. It reads no files and takes no format argument; every difference between
the two formats is PLACEMENT plus the `lockup` string. It calls
`SC.assert_anchor_law()` before it writes a byte. It emits 83 tweens; the eases it
names are the chassis' own: `SOFT`, `POP`, `SWING`. Labels use class `mono` (the
chassis' JetBrains Mono uppercase rule). The podium digits are SVG `<text>` in
`JetBrains Mono` 800, so the page must load that face (the chassis does).

### `media` — the one raster the scene paints

```python
{"_grok_img": CC.mark_img(LOGO_URL["grok"], "grok", SC.MARK_SIDE["grok"])}   # 74.0
```

`CC.MARK_INK["grok"]` must be populated by `CC.measure_mark("grok", src)` first, and
the URL must be page-relative (`assets/logos/<basename>`). The same `<img>` string
is used by BOTH tiles (`#grok-tile` in chapter 0, `#grok-tile-2` from chapter 2 on).
The side is an INK side in CORE px; the core's own `scale(k)` carries it.

**THE FILE IS NAMED, NOT GUESSED** (`SC.LOGO_FILES`): `grok` =
`ai-models/grok.png` (registry key `grok`, aliases xai / spacexai). No Grok Imagine
product mark exists in the library; never the SpaceX wordmark.

There is no source post, no screenshot and no other raster in this video
(`pointing_cues.py` returned zero cues).

### `lockup` — the outro's handle block

```python
CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W) \
  + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W)
```

Seated inside the scene's own `#o-slot`. `handle_key` is the only string that
differs between masters: `"yt"` on the split, `"tiktok_ig"` on the cutout.

---

## 2. THE UNITS

**CORE px = the plan's CANVAS px with y shifted by -192.** `canvas_y = core_y + 192`,
x untouched. `SC.CORE_W, SC.CORE_H = 1080.0, 600.0`.

* `SC.CONTENT_Y0, SC.CONTENT_Y1 = 80.0, 532.0`: the band the core really paints in
  (canvas 272 … 724, 14.2 % … 37.7 % of frame height). Y0 is the chapter-1 palette
  top and the chapter-3 tile top; Y1 is the `BEST VIDEO MODEL` key's bottom. The
  outro also lives inside it (glyph top 146, slot bottom 500). At k = 1 the lowest
  ink clears the caption pill's top (~787.7) by ~64 px.
* Every chapter is symmetric about x = 540 (chapter 3's ink extents are 210 … 870).
  So `left = (1080 − 1080·k) / 2`.
* Seat the core so its CONTENT BAND is centred on your stage zone:
  `top = round(centre - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 * k, 2)`.

**GATE-SCALING.** Non-block gutters are authored at ≥ 20 core px: output-key seats
26 (chapter 1), picture-to-wand 70 (chapter 3), bus-to-output tops 38. Smaller gaps
are inside DECLARED blocks (`SC.DECLARED_BLOCKS`): tile-on-step-2 4, tile-over-picture
20, keys-under-objects 18-20.

---

## 3. THE TIMELINE

`SC.CUE` carries every instant (word STARTS from `cuts/grokimagine2/transcript_tight.json`
unless marked `authored`, each inside its word's 1.0 s window). `SC.BEAT_EDGES` is the
plan's beat table; `SC.DUR = 32.32`.

| ch | t | on screen |
|---|---|---|
| 0 | 0.10–5.80 | the palette alone on the axis (0.14); `GROK IMAGINE 2.0` (1.30); the Grok tile above it (3.06) |
| 1 | 5.80–13.00 | key + tile fade, the palette travels up and shrinks to 0.7 (5.80, origin 0 0); per word a terracotta line drops from its bottom edge and the object pops: phone/`MOCKUPS` (7.82/8.00/8.66), poster/`INFOGRAPHICS` (9.56/9.62/9.76), instant photo/`IMAGES` (10.56/10.62/10.76), clapperboard/`VIDEOS` (11.10/11.16/11.30); holds through "anything that you might need" |
| 2 | 13.00–17.86 | chapter 1 fades while the podium pops INSIDE the erase (13.00); the Grok tile drops onto step 2 on "two" (14.36); step 2's outline flips terracotta 14.56–17.40; `BEST VIDEO MODEL` (16.40) |
| 3 | 17.86–28.24 | podium + key fade, the Grok tile travels to the top centre (17.86); the framed picture pops centred under it (19.14); on "Magic" picture + tile slide left 165 (21.00) and the wand pops right (21.10), `MAGIC WAND` (21.40); dashed selection snaps round the sun (22.50); `ANY IMAGE` (24.80); on "replace" the sparkle flashes (26.34), the sun fades (26.40) and the crescent moon pops in its place (26.52) |
| 4 | 28.24–32.32 | opaque rising sheet (28.24); the small wand (28.72), rule (29.02), lockup (29.12) |

Every erase is a handover, never a blank (LAW 43 / LAW 45): the palette itself crosses
seam 1, the podium draws inside the seam-2 erase, the Grok tile crosses seam 3. The
last board event (the moon) settles by 26.82, 1.42 s before the outro anchor.

---

## 4. THE FOUR BESPOKE OBJECTS — DO NOT REDRAW

`SC.BESPOKE` carries CORE boxes and the held instant of each. Self-checked at phone
size (405x720) by the design agent, v4 (no cold readers).

| i | object | t | core box | proof |
|---|---|---|---|---|
| 0 | a painter's palette | 2.60 | 400, 228, 680, 438 | `review/proof_grokimagine2/00.png` |
| 1 | a winners' podium | 16.90 | 250, 250, 830, 470 | `01.png` |
| 2 | a framed picture | 20.80 | 375, 212, 705, 462 | `02.png` (after 'replace': `08.png`) |
| 3 | a magic wand | 22.20 | 610, 222, 870, 452 | `03.png` |

`SC.ICONS` lists the four LABELLED output icons of chapter 1 (phone, poster, polaroid,
clapper; proofs `04`-`07`). They are not bespoke objects: each carries its written name.
Map `core` boxes through your own k and origin when you cut phone crops.

---

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 40**: four connectors, one source, four targets. `SC.CONN_FROM = anchor_points(PALETTE1_BOX, 1, "bottom")` = (540, 227);
  ends `SC.A_OUT[k] = anchor_points(OUT_BOX[k], 1, "top")` = (195|425|655|885, 300), level to 0 px
  and mirrored about 540. Route: trunk to the bus at y 262, then drop. `data-connect-to` + `data-overlap-ok`.
* **LAW 39 / 50**: eight keys, each `data-label-for`, entirely BELOW its host, centred to 0 px.
  The four output keys are siblings: 26 px, 204 px seat, baseline core 470. `MAGIC WAND` / `ANY IMAGE`
  are siblings: 28 px, 192 px seat, baseline core 480. DOM ids of the output keys are
  `key-phone`, `key-poster`, `key-polaroid`, `key-clapper` (the plan names them by their word).
* **LAW 41**: `SC.DECLARED_BLOCKS`, stamped as `data-block`.
* **LAW 42**: `SC.LIFETIMES`. Chaptered board: every board mark has a finite window; only the four
  outro marks are anchors (`SC.SCENE_ANCHORS`).
* **LAW 38**: exactly ONE emphasis, the step-2 outline flip (`#podium .pstep2` stroke → `rgb(221,114,89)`
  and back). The dashed selection is an OBJECT (Magic Wand's selection), authored inside the picture's
  block, not emphasis. No `<circle>` tag anywhere; round shapes are two-arc paths.
* **LAW 51**: the picture's sun and moon are `<g>`s inside `#picture`, so they travel with the picture;
  the sparkle `<g class="spk">` scales about its own centre (`svgOrigin "74 50"`) inside `#wand`.
  Any lane that draws these must move/replace them the same way.
* **THE GHOST RULE**: every connector declares `pathLength="100"`, rests at `stroke-opacity:0` and
  reveals 0.04 s after its draw starts.

---

## 6. THE POINTING CUE

None. `pointing_cues.py --vid grokimagine2`: "no pointing cue in this take"; `gen/_cues_grokimagine2.json`
has `cues: []`; the prep `cues` marker agrees (cue_count 0).

---

## 7. WHAT THE CUTOUT OWNS

* The matte and stage-zone seating. At plan time `cut`, `plate` (over-wide, crop 2912x1820+626+270,
  scale_k 0.4945, face_dx 1.5 %), `prompt0` (wing_review true, the instrument abstained, no cut) and
  `cues` had landed; `track` said `skipped` (matanyone2) and no `ship` marker existed. The Astra
  matte step owns the selection and the matte. `plate_origin()` must read `left` from `plate_box`.
* `SC.CUTOUT_LOGO_LANES = ("midjourney", "flux", "minimax", "higgsfield", "gemini", "chatgpt")`, files in
  `SC.CUTOUT_LOGO_FILES` (relative to `assets/logos/`). Image and video generators in Grok Imagine's own
  category, mixed, none repeated, never `grok` (it is on the stage). All seven files (stage + lanes)
  pass `cutout_depthfield.assert_cast_resolves` (checked 2026-09-22).
* Your own k and origin. The logo lanes fade in after the hook lands, never later.

## 8. WHAT THE WHITEBOARD DOES NOT DO

It does not import this module. It redraws the same argument in marker ink per beat
`whiteboard_version` in the plan: same objects, same labels, same key term, same
sun-to-moon swap inside the selection on "replace".

---

## 9. WHERE THIS MODULE DEPARTS FROM THE PLAN'S LETTER

1. The output keys' DOM ids are `key-phone` … `key-clapper`; the plan's lifetimes/blocks call them
   `key-mockups` … `key-videos`. Same four elements, same windows.
2. The plan's `bbox` values are normalised canvas boxes; `SC.BESPOKE` carries the real CORE boxes and is
   authoritative for geometry.
3. The Grok tile over the picture is carried from the podium (`#grok-tile-2`), so its lifetime runs
   14.36–28.24 as the plan says; it is one element, moved twice (17.86 and 21.00).

---

## 10. PROOF EVIDENCE

| what | where |
|---|---|
| phone-size crops, one object alone per 405x720 frame | `review/proof_grokimagine2/00.png` … `08.png` |
| tight crops | `review/proof_grokimagine2/NN_tight.png` |
| crop manifest | `review/proof_grokimagine2/proofs_seal.json` |
| composed chapter frames (GRAPHIC CHART clause 9) | `review/proof_grokimagine2/compose_{ch0,ch1,ch2,ch3a,ch3,ch3b,outro}.png` and `*_phone.png` |
| the seal record | `review/artwork_pass_grokimagine2.json` |
