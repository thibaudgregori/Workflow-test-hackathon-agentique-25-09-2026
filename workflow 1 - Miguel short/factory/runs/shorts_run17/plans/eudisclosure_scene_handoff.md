# eudisclosure — SHARED LANE SCENE HANDOFF

**STATUS: HOLD. THE SCENE IS BUILT AND NOT SEALED.**
`review/artwork_pass_eudisclosure.json` does **not** exist, and that is
deliberate: two of the four bespoke objects failed the cold read on confidence.
`production.py artwork-check` will refuse, and **no lane may build on this
module until it is sealed.** Section 7 carries the measurement, the two
remaining moves and what a repair round would have to change. The previous
approval, written at 01:16 against the **superseded** plan (a rubber stamp, a
brightness slider), has been parked as
`review/artwork_pass_eudisclosure.superseded_20260908_0116.json` so nothing can
consume it by accident.

The plan this scene is built from is the **08:16 revision** of
`plans/eudisclosure_plan.json`. It is a different plan from the one the 01:xx
artwork answered: the lane is the same (diagram build) but the objects are not
— no rubber stamp, no slider, no dial, no meter.

---

## 0. THE ARGUMENT, IN ONE LINE

In Europe anything made with AI must now carry a declaration → it covers the
chatbot you talk to and the media it makes → for an image the declaration forks
into AI GENERATED or AI MODIFIED → and an ordinary photograph whose sun you
recoloured lands in the second bucket.

Transcript is truth: **no date, no "EU AI ACT", no article number and no legal
citation appears anywhere**, because none of them is spoken in this take.

---

## 1. THE MODULE

    shorts_run17/gen/eudisclosure_scene.py

One intrinsic **1080 x 600 core**, authored once and placed twice:

| lane | placement |
|---|---|
| classic split (YouTube) | the top zone, `k = 1.00`, core top = `SC.CANVAS_OFFSET` = 192.0 |
| cutout (TikTok) | the stage zone, `k` derived from THAT session's matte envelope |

The Reels whiteboard does **not** import this module. It redraws the same
argument as marker ink from the same plan, in its own drawing style.

### Entry point

```python
import eudisclosure_scene as SC
html, tweens = SC.build(media=None, lockup=lockup_html)
```

* returns `(html, tweens)` in **core coordinates**; `canvas_y = core_y + 192`.
* `build()` runs every assertion in section 8 before it emits a byte. A
  geometry mistake is a `SystemExit`, never a silent render.
* `SC.report()` returns the whole paperwork block (rects diffed against the
  plan, connectors, gutters, symmetry, band, label axes, outro clearance,
  phone sizes). `python gen/eudisclosure_scene.py` prints it.

### `media` — THERE IS NO RASTER IN THIS SCENE

`media` is unused and may be `{}` or `None`. The plan puts **no registry mark
on the stage**: the script names no product, model or company in 100 words, so
LAW 2 has nothing to bind and `SC.CAST_FILES` is empty by construction. The
chart's 112 px tile grammar is exercised where it belongs in this video, in the
cutout's depth lanes.

### `lockup` — the outro's handle block

The chassis lockup (`captions.outro_chip_html` + `outro_daily_html`), dropped
into `#o-slot` at core `(0, 260)`, width 1080, height 142. **The handle is the
only string that differs between the two masters**: `@migueltorrezai` on the
YouTube split, `@migueltorrez.ai` on the cutout and the whiteboard.

---

## 2. THE UNITS

* Core is **1080 x 600**. All geometry below is core px.
* `SC.CANVAS_OFFSET = 192.0`, so `canvas_y = core_y + 192`.
* **Declared content band**: core `y 94 .. 568` = canvas `y 286 .. 760`.
  * below LAW 30's top-10 % line (canvas 192) and below the whiteboard's legal
    surface top (canvas 281.25);
  * 36.9 px above the whiteboard's legal surface bottom (canvas 796.875);
  * 142.7 px above the split's RENDERING pill top (canvas 902.705).
* **Ink x extents**: 230.5 .. 868.0. LAW 30's rails are 162 .. 918, so 68.5 px
  of left clearance and 50.0 px of right clearance.
* Fonts: JetBrains Mono 800 uppercase for **every** piece of type. Key term 48
  px / letter-spacing 2.0; all seven other keys 26 px / letter-spacing 1.2.

### GATE-SCALING

The cutout scales the shared core by ~0.95. The **tightest non-block gutter in
the whole video is 28.0 core px** (`key-disclosure ↔ key-photo`, chapter 2),
which arrives as **26.6 px** on the cutout — over the 24 px aim and well over
the 16 px refusal. Every other chapter's tightest pair is >= 128 px.

---

## 3. THE GEOMETRY, IN CORE px

Names are the DOM ids. `(x, y, w, h)` seats; `[x0, y0, x1, y1]` boxes.

### The anchor (on screen 2.98 → the outro)

| id | box | note |
|---|---|---|
| `key-disclosure` | `[334, 94, 746, 152]` | `AI DISCLOSURE`, 48 px, centre 540.0, the board's ONE anchor |

### Chapter 0 — 0.42 → 10.26

| id | box | note |
|---|---|---|
| `tag` | `[462, 188, 618, 304]` | body seat `(478, 200, 140, 104)`; box includes the cord |
| `tag-string` | full-core overlay | the cord, `data-overlap-ok` |
| `conn-left` | `(486.96, 304) → (320, 384)` | terracotta |
| `bubble` | `[244, 384, 396, 512]` | body 152 x 112 + a 16 px tail |
| `key-chatbot` | `[256, 528, 384, 568]` | `CHATBOT`, centre 320.0 |
| `conn-right` | `(593.04, 304) → (760, 384)` | terracotta, the mirror |
| `stack` | `[684, 384, 836, 496]` | two overlapping cards, `.stkc` |
| `key-aicontent` | `[670, 528, 850, 568]` | `AI CONTENT`, centre 760.0 |

### Chapter 1 — 10.52 → 14.60

| id | box | note |
|---|---|---|
| `gen-card` | `[244, 304, 476, 468]` | born centred at `[424, 304, 656, 468]`, slides left 180 px at 11.90 |
| `key-generated` | `[254, 494, 466, 534]` | `AI GENERATED`, centre 360.0 |
| `conn-or` | `(476, 386) → (604, 386)` | the word `or`, drawn |
| `mod-card` | `[604, 304, 836, 468]` | the dog-ear is a 40 px leg at the top-right |
| `key-modified` | `[622, 494, 818, 534]` | `AI MODIFIED`, centre 720.0 |

### Chapter 2 — 14.86 → 23.36

| id | box | note |
|---|---|---|
| `key-photo` | `[434, 180, 646, 220]` | `A REAL IMAGE`, ABOVE, centre 540.0 |
| `photo` | `[340, 228, 740, 454]` | 400 x 226, an 18 px white mat, a second inner rule |
| `key-color` | `[392, 480, 688, 520]` | `COLOR OR LIGHTING`, BELOW, centre 540.0 |
| `tag2-string` | full-core overlay | from the photograph's right edge at `(740, 408)` |
| `tag-2` | `[740, 404, 846, 498]` | body seat `(744, 404, 102, 94)` |
| `key-disclose` | `[722, 518, 868, 558]` | `DISCLOSE`, BELOW, centre 795.0 |

### The outro

| id | seat | note |
|---|---|---|
| `o-sheet` | bleeds `(-60, -240, 1200, 1100)` | the OPAQUE rising sheet, `data-bleed` |
| `o-glyph` | `(494, 104, 108, 80)` | the hang label, small; its cord puts the INK centre on 540.0 |
| `o-rule` | `(448, 224, 184, 7)` | terracotta |
| `o-slot` | `(0, 260, 1080, 142)` | the chassis lockup |

### Symmetry

Chapters 0 and 1 are mirror-symmetric about x = 540 to **0.0 px** on their own
ink extents. Chapter 2's **subject** composition (`key-disclosure`, `key-photo`,
`photo`, `key-color`) is centred on 540.0 to **0.0 px**; the payoff lockup
(`tag-2`, `key-disclose`) is authored **off the axis on purpose** — the label
hangs off the photograph's right edge on a cord, which is the picture the last
sentence makes — and pushes the chapter's full extents to an optical axis of
601.0 (+61.0 px) for the last 1.26 s of the argument. `SC.assert_symmetry()`
holds chapters 0/1 and the chapter-2 subject to 0.001 px and REPORTS the payoff
offset rather than hiding it.

---

## 4. THE CONNECTORS (LAW 40)

All three ends come out of `SC.anchor_points(box, n, side, inset=0.16)`, the
law's own helper, and `SC.assert_connector_anchors()` re-derives them before a
byte is written.

| id | from | to | target | draws | node lands |
|---|---|---|---|---|---|
| `conn-left` | `(486.96, 304.0)` | `(320.0, 384.0)` | `bubble` | 3.96 | 4.10 |
| `conn-right` | `(593.04, 304.0)` | `(760.0, 384.0)` | `stack` | 5.06 | 5.20 |
| `conn-or` | `(476.0, 386.0)` | `(604.0, 386.0)` | `mod-card` | 12.60 | 12.92 |

* Chapter 0 is ONE source fanning into TWO targets, so LAW 40's letter (two
  arrows into one target) does not bind — the ends are built with the law's own
  helper anyway. Both ends are **level to 0.0 px** and **mirror-symmetric about
  540.0 to 0.0 px**; both origins are mirror-symmetric too.
* Every connector stamps `data-connect-to` and `data-overlap-ok` (a connector
  MUST touch what it joins) and terminates AT the target's virtual rectangle,
  mid-edge, clear of the corner radius. **No arrowheads** — the plan's word is
  *line*, three times.
* No connector crosses printed type: the only type below y = 304 starts at
  y = 494 (`key-generated`, `key-modified`) and y = 528 (`key-chatbot`,
  `key-aicontent`), and every stroke stops at y = 386 or above.
* BUILD ORDER: each line draws **with** the node it reaches, overlapping by
  ~0.14 s, so a line is never a stem to nothing.

---

## 5. EVERY ASSET KEY IT RESOLVES

`SC.CAST_FILES` is **empty**. Nothing on the stage is a raster.
`assert_cast_resolves()` has nothing to check for the split.

`SC.CUTOUT_LANE_FILES` — the cutout's depth lanes only, the plan's topical
roster, six real colour marks, `mistral` among them because the story's own
jurisdiction is Europe:

```
chatgpt   ai-models/chatgpt-color.png
gemini    ai-models/gemini-color.png
claude    ai-models/claude-color.png
grok      ai-models/grok.png
mistral   ai-models/mistral.png
meta      ai-models/meta.png
```

All six resolve on disk today under `~/Documents/Workspace/assets/logos/`.
Tiles are 112 px, 3 px ink-alpha border, radius 18, the mark's ink sized by
`mark_img`; repeat marks across the three lanes rather than leaving a grey
blank (LAW 29). There is no subject mark to keep out of the lanes, because the
script names no product.

---

## 6. WHAT YOU MUST CHANGE TO SEAT IT IN THE STAGE ZONE

The core is one absolutely-positioned wrapper with a **static**
`transform: scale(k)` and `transform-origin: 0 0`. The scale is a PLACEMENT,
never a move (LAW 1 / LAW 21).

1. Wrap `SC.build()`'s html in your own `#core` div and set `scale(k)` and the
   core's top from your session's own matte envelope.
2. Assert the band lands legally in YOUR frame: the scene paints core
   `y 94 .. 568`, so the canvas band is `192 + k * 94` to `192 + k * 568` in the
   split and whatever your envelope makes of it in the cutout. Nothing may
   enter the frame's top 10 % or the side rails.
3. `SC.BESPOKE` boxes are **core** boxes. Map them through your own placement
   before you cut phone crops — a frame-normalised box from one lane is wrong
   in the other.
4. Cutout seating: his cap top sits at ~44 % of frame height (canvas y ~845)
   and the plate solve measured `head_px_on_canvas` 451.8. The lowest ink is
   canvas 760, so nothing comes near the silhouette and **nothing is ever
   declared `behind`**.
5. Do not re-author the drawing. If a reader refuses one of its objects, take
   `production.py scene-lock --run <run> --vid eudisclosure --holder <lane>`,
   redraw it here, re-read it cold over 3 rounds and re-run `artwork-pass`.

---

## 7. THE PHONE TEST — READ, AND **NOT** SEALED

Five independent rounds, `pipeline/cold_read.py`, blind copies under random
tokens, one `claude -p` per crop from `/tmp` on absolute paths, no plan, no
topic, no key. **Twenty reads, zero dispatch failures, zero readers naming a
different thing.** Evidence:

```
review/phone_reader_eudisclosure_artwork_r1.json .. _r5.json
review/scores_eudisclosure_artwork.json
review/proofs_eudisclosure_r5/{00,01,02,03}.png      the crops that were read
```

| # | object | phone px | reader answers | sure | verdict |
|---|---|---|---|---|---|
| 0 | a hanging label | 58 x 44 | `price tag` x 5 | **5/5** | PASS |
| 1 | a sparkle picture | 87 x 62 | `framed picture`, `framed picture`, `framed picture (photo frame)`, `picture frame with mountain`, `framed mountain picture` | **1/5** | **FAIL** |
| 2 | a dog-eared photo | 87 x 62 | `framed landscape photo picture`, `photograph` x 3, `photograph of mountains` | **1/5** | **FAIL** |
| 3 | a framed photograph | 150 x 84 | `framed picture of mountains`, `framed landscape picture` x 4 | **3/5** | PASS |

**What failed is the CONFIDENCE, not the noun.** Twenty of twenty reads named
the intended object or an obvious synonym; the plan's own PASS lists for objects
1 and 2 contain `photo` and `picture with a sparkle` verbatim. But STANDARD.md's
cold-read clause makes **a hedge a FAIL**, and `production.consensus` requires
at least half the reads to be `sure`. Both were applied as written. Neither was
relaxed.

### What was tried, in order (every crop and every answer is on disk)

| round | object 1 drawing | object 2 drawing | result |
|---|---|---|---|
| r1 | spark over a shallow horizon curve | fold 32, terracotta stroke across the ridge | 1 unsure / 1 unsure |
| r2/r3 | spark over a terrain line, spark r 38 | fold 40, stroke moved clear of the ridge | 0/3, 1/3 sure |
| r4 | + a mount-tone picture field | + a mount-tone picture field | 0/3, 1/3 sure |
| probe | the same drawing at 150 x 106 | — | `sparkle over jagged line`, **cannot tell** — bigger is WORSE |
| probe | the same drawing + an inner mat | — | `framed picture (photo frame)`, unsure — the mat alone does not move it |
| r5 | **metaphor 2**: the spark stands where the sun would be, over one broad mountain | fold 40, thinner stroke, sun moved clear of the fold | 1/5, 1/5 sure |
| probe2 | + an inner mat on the current drawing | + an inner mat | 1 sure / 1 unsure — one sample, not a measurement |

### What the data actually says

* **Size is not the lever.** Object 0 is the SMALLEST crop in the set (58 x 44)
  and the ONLY one at 5/5 sure. Object 1 enlarged to 150 x 106 read *worse*.
* **The lever is iconic unambiguity.** `price tag` is one named everyday thing.
  A picture is a container plus its content, and the reader hedges over which
  one it is being asked to name — every hedge in this set is on a picture, and
  the one picture that clears the bar (object 3) does so at 3/5, marginally.
* **The instrument is noisy and the pipeline says so.** Object 3's crop is
  byte-identical across the r4 and r5 dispatches and came back 3/3 sure in one
  set and 1/3 in the next. Pooled over nine reads of the same pixels it is 6/9.
  That is exactly the variance `production.evidence_rounds` documents.

### The two moves left, for whoever takes the scene lock

1. **Give objects 1 and 2 the photograph's mat.** It is the only structural
   difference left between them and the object that passes, and probe2 returned
   one `sure` on it. It costs the plan's clause "the photograph is deliberately
   the ONLY object with a visible frame margin" — that clause exists to keep
   chapter 2's silhouette distinct, and the photograph would still be 1.7x
   larger, matted white, and alone on its board.
2. **Replace chapter 1's comparison with two objects that are not pictures.**
   The fork is about images, so this is a PLAN question, not an artwork one: it
   needs the planner, not a redraw. Both of this stage's metaphor attempts for
   object 1 are spent (spark over a bare horizon; spark standing in for the sun
   in a landscape), which is why this returns HOLD instead of a third.

---

## 8. WHAT THE MODULE ASSERTS BEFORE IT EMITS A BYTE

`build()` calls all six; `report()` returns their output.

| assertion | what it measures |
|---|---|
| `assert_connector_anchors()` | LAW 40 — all six points from the law's own helper, level and mirror-symmetric to 0.0 px |
| `assert_gutters()` | LAW 41 — every concurrent non-block pair, per chapter, against a 16 px floor and a 24 px aim, with the cutout's k=0.95 number beside it |
| `assert_symmetry()` | LAW 15 / LAW 19 — chapters 0/1 and chapter 2's subject to 0.001 px; the payoff's offset reported |
| `assert_band()` | the declared band and LAW 30's rails, including the generated card's OPEN seat |
| `assert_label_axes()` | LAW 39 — every key above or below its host and inside that host's ±15 % band |
| `assert_outro_clear()` | ROUND-2/3 LAW 3 — the last board ink is DISCLOSE at 23.02, 0.34 s before the outro anchor |

---

## 9. THE CUE SHEET

Every value is a word START from `cuts/eudisclosure/transcript_tight.json`
unless marked *authored*, and every authored cue sits inside its own word's
1.0 s LABEL_WINDOW.

| cue | t | word / why |
|---|---|---|
| `tag` | 0.420 | *authored*, inside `live` — the label draws itself, alone, on the axis |
| `keyterm` | 2.980 | *authored*, 0.08 s after `AI,` ends — the key term, FIRST among all type |
| `connL` | 3.960 | *authored*, the gap before `chatbot` |
| `bubble` | 4.100 | *authored*, inside `chatbot` |
| `keychat` | 4.620 | *authored*, 0.02 s after `chatbot` |
| `connR` | 5.060 | `AI` |
| `stack` | 5.200 | *authored*, the gap before `generated` |
| `keycont` | 5.800 | *authored*, inside `content.` |
| `emph` | 7.420 | `generated`, of the phrase `AI generated images` — the stack's border flip |
| `erase0` | 10.260 | *authored*, the connective `you have to say` — CHAPTER SEAM 0 |
| `gencard` | 10.520 | *authored*, INSIDE the erase (SEAM_LAP); completes on `image` |
| `genhorizon` | 11.000 | `image` |
| `genspark` | 11.540 | `AI` |
| `genslide` | 11.900 | *authored*, inside `generated` — the ONE displacement |
| `keygen` | 12.520 | *authored*, 0.02 s after `generated` |
| `connor` | 12.600 | *authored*, inside `or` |
| `modcard` | 12.920 | *authored*, inside `AI` |
| `modstroke` | 13.300 | `modified.` |
| `keymod` | 13.400 | *authored*, INSIDE its own word — 1.20 s of settled screen time |
| `erase1` | 14.600 | *authored*, the connective `So if you took a` — CHAPTER SEAM 1 |
| `photo` | 14.860 | *authored*, INSIDE the erase (SEAM_LAP) |
| `keyphoto` | 15.900 | *authored*, 0.06 s after `image` |
| `photospark` | 18.860 | *authored*, the gap before `slight` |
| `recolour` | 20.420 | *authored*, inside `color` — the sun goes terracotta |
| `rays` | 20.960 | `lighting,` — two rays finish their own path |
| `keycolor` | 21.320 | *authored*, 0.04 s after `lighting,` |
| `tag2` | 22.100 | *authored*, inside `also` — the label drops, swings once, settles |
| `keydisclose` | 22.720 | *authored*, inside `disclose` |
| `outro` | 23.360 | *authored*, 0.02 s after `that.` — the OPAQUE RISING SHEET |

Seams: `SC.SEAMS = (10.26, 14.60)`. Run `seam_check.py` on the Reels render with
`--seams 10.26 14.60`.

---

## 10. WHAT I LEARNED BUILDING IT (so you do not learn it twice)

1. **The plan changed under the artwork.** The 01:16 approval answered a plan
   with a rubber stamp and a brightness slider; the 08:16 plan has neither and
   explicitly refuses a slider, dial or meter. `stage_cache.py` caught it
   (`found: false`) because the plan json is in the stage fingerprint. Always
   re-read the plan before trusting a cached artwork PASS.
2. **The cold reader's confidence flag is high-variance and its noun is not.**
   Twenty reads, zero wrong nouns, eight hedges. If you are chasing `sure`, you
   are chasing the instrument as much as the drawing — measure over rounds
   before you redraw, and never over one.
3. **Bigger is not clearer.** The same card at 87 x 62 read `framed picture`
   unsure and at 150 x 106 read `sparkle over jagged line, cannot tell`. What
   moved object 0 to 5/5 was a closed, named silhouette, not pixels.
4. **Siblings on one row must share a seat width.** Unequal key seats put
   chapter 0's optical axis at 553 instead of 540 and `assert_symmetry()`
   refused the build. `_seat(text, centre, top, twin=...)` is the fix and it is
   LAW 7's "same-theme cards = same size" as well as LAW 15.
5. **The plan's own label boxes imply a ~23 px key.** The GRAPHIC CHART's
   reference sets it at 28. This module uses 26, keeps every key CENTRE the
   plan's own value, and re-derives each seat as ink + 12 px.
