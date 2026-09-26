# kimifable — SHARED LANE SCENE HANDOFF

**Written by the ARTWORK AUTHOR for the SPLIT and CUTOUT authors.** The plan is
the contract (`plans/kimifable_plan.json`); this file is the convenience. If
anything below disagrees with the plan, the plan wins **except** on the three
points listed in §6, which are departures the plan's own Phone-Test risk note
anticipated and which independent cold readers forced. Those are written up with
their evidence in `plans/kimifable_scene_notes.md`.

**The scene is SEALED**: `review/artwork_pass_kimifable.json` binds this module,
this handoff, three independent cold-read rounds and the scoring. **No format
lane may redraw a bespoke object in it.** If a reader refuses one downstream,
that is a repair round and it has an owner — take
`production.py scene-lock --run shorts_run17 --vid kimifable --holder <lane>`,
redraw, re-read cold over three rounds and re-run `artwork-pass`. "Not mine to
change" is not a terminal reason there.

---

## 1. THE MODULE

| | |
|---|---|
| path | `shorts_run17/gen/kimifable_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import kimifable_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| self-check | `SC.self_check()` — LAW 41 gutters, LAW 15 axis, LAW 30 band, per chapter |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |
| proof renderer | `shorts_run17/gen/kimifable_proof.py` (stills only, no GSAP, no render) |

`build()` returns the WHOLE 38.12 s scene: html to drop inside one
`transform: scale(k)` wrapper, and a list of `tl.*` javascript strings to
concatenate into your own timeline tail. It authors nothing outside the core, it
reads no files, and it takes no format argument — every difference between the
two formats is in the PLACEMENT and in the `lockup` string. It calls
`assert_no_connectors()` on its own output before returning.

### `media` — the two marks the scene paints
```python
{"_kimi_img":  CC.mark_img(LOGO_URL["kimi"],   "kimi",   SC.MARK_SIDE_TILE),   # 56.0
 "_fable_img": CC.mark_img(LOGO_URL["claude"], "claude", SC.MARK_SIDE_TILE)}
```
`CC.MARK_INK[key]` must be populated by `CC.measure_mark(key, src)` first and the
`LOGO_URL` values must be page-relative (`assets/logos/<basename>`). Each string
is emitted THREE times — once per chapter that names that model. `mark_img`
writes no id, so three copies are three drawings and never a duplicate id.
`MARK_SIDE_TILE` is an **ink side in CORE px**: do not rescale it for the cutout,
the core's own `scale(k)` carries it.

### `lockup` — the outro's handle block
```python
CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W) \
  + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W)
```
Seated inside the scene's own `#o-slot`. `handle_key` is the ONLY string that
differs between the masters: `"yt"` on the split, `"tiktok_ig"` on the cutout.

---

## 2. THE UNITS

**CORE px = the plan's CANVAS px with y shifted by −192.**

```
canvas_y = core_y + SC.CANVAS_OFFSET      # 192.0
canvas_x = core_x                          # every core x survives verbatim
```

* `SC.CORE_W, SC.CORE_H = 1080.0, 600.0`
* `SC.CONTENT_Y0, SC.CONTENT_Y1 = 94.0, 554.0` — the band the core DECLARES it
  paints in (**canvas 286 … 746** on the split). Y0 is the key term's box top,
  which is the whiteboard's own legal-surface top and clear of LAW 30's top-10 %
  line at 192; Y1 is BUILD COST's box bottom, the lowest ink in the video. Both
  are REAL painted ink, not a reserved envelope. Clearances that fall out of it:
  **53.2 px** to the whiteboard's reserved band (canvas 799.2) and **156.7 px**
  to the split's RENDERING pill top (960 − 114.59/2 = 902.705, derived from the
  pill height that RENDERS and never from the frozen 108.2 seat constant).
* `SC.INK_X0, SC.INK_X1 = 200.0, 880.0` — readable ink stops at 880, clear of
  LAW 30's right rail (x > 918).
* **Every chapter's ink extents are mirror-symmetric about x = 540 to 0.00 px**
  (`self_check()` refuses a build over 0.5 px). So `left = (1080 − 1080·k) / 2`.
  The two deliberately off-axis moments are LAW 19's own choreography: the price
  tag opens centred on 540 and displaces left as the Kimi tile arrives, and the
  folder does the same in chapter 3.
* Seat the core so its CONTENT BAND — not its box — is centred on your stage
  zone's centre:
  ```python
  top = round(centre - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 * k, 2)
  ```
  Centring the 600-tall BOX is the wrong sum and a LAW 15 defect.

**GATE-SCALING (run 12).** Gate 1 measures canvas px and the cutout scales the
shared core by ~0.95, so a 16 core-px gutter arrives as 15.2 canvas px and is
refused on the cutout while passing on the split. Every non-block gutter here is
authored at **≥ 28 CORE px**; `SC.self_check()` measures all of them per chapter
and refuses the build under that floor.

| chapter | tightest non-block gutter | at k = 0.95 | ink x | ink y | axis error |
|---|---|---|---|---|---|
| 0 headline | 78.0 (`fable-tile` ⟷ `key-price`) | 74.1 | 226 … 854 | 94 … 478 | 0.00 |
| 1 caveat | (one declared block) | — | 340 … 740 | 124 … 510 | 0.00 |
| 2 what each is for | 28.0 (`bar-fable` ⟷ `fable-tile2`) | 26.6 | 206.6 … 873.4 | 100 … 496 | 0.00 |
| 3 payoff | 28.0 (`build-track` ⟷ `key-designs`) | 26.6 | 200 … 880 | 120 … 554 | 0.00 |

**Declared blocks (`data-block`), exempt from each other's gutter only:**
`kimi0` = kimi-tile + kimi-tag + kimi-coin; `fable0` = fable-tile + fable-tag +
the three coins; `bench` = scorecard + score-head + the three rows and bars +
key-bench; `kimi2`; `front` = design-window + key-frontend; `fable2`; `price2` =
bar-base + the three bars + key-expensive; `stack` = sheet-stack + key-designs;
`kimi3`; `fable3`; `eq` = equals + key-similar; `cost` = build-track +
build-fill + num-66 + key-build. `SC.DECLARED_BLOCKS` is the machine-readable
twin.

---

## 3. THE FOUR CHAPTERS (LAW 43's default, the plan's own call)

`SC.BOARD_MODE = "chapters"`, `SC.BOARD_CHAPTERS` carries the seams and holds.
Nothing accumulates across a seam: **no element carries `data-anchor`**, every
rigid declares a finite `t_to` in `SC.LIFETIMES`, and one `#wipe` element serves
all three erases — an opaque cream sheet that rises to cover in 0.16 s, holds
while the outgoing chapter is switched off behind it, and carries on off the top
in 0.12 s. It is itself ink, so `assert_zone_never_blank()` holds across every
handover (ROUND-2/3 LAW 1).

| # | window | erase | the picture |
|---|---|---|---|
| 0 | 0.079 – 4.55 | 4.55 | PRICE PER TOKEN over two marks, each with its price tag under it: one coin against three |
| 1 | 4.75 – 11.50 | 11.50 | the benchmark scorecard on its clipboard, one terracotta row of three |
| 2 | 11.70 – 21.60 | 21.60 | Kimi + its website layout, against Fable + its price column |
| 3 | 21.80 – 32.34 | **32.64 = the outro wipe** | the folder of designs, KIMI = FABLE, and the cost track cut to a third |

Chapter 3's erase IS the outro wipe, so it never hands over to another board:
`assert_outro_clear()` must find no ink authored at or after 32.64. The last
board ink is `-66%`, finishing at 31.95.

---

## 4. THE CANVAS RECTS IT DRAWS

`SC.canvas_rects()` returns every declared rect as CANVAS px `[x0, y0, x1, y1]`
— assert them against what you emit to 2 px (the 2026-09-05 rule) and log any
deviation with its reason. The headline numbers:

| id | canvas rect |
|---|---|
| `key-price` (KEY TERM, 48 px, ls 2) | 305, 286 → 775, 344 |
| `kimi-tile` / `fable-tile` | 300, 422 → 412, 534 / 668, 422 → 780, 534 |
| `kimi-tag` / `fable-tag` | 226, 574 → 486, 670 / 594, 574 → 854, 670 |
| `kimi-coin` | 371, 605 → 405, 639 |
| `fable-coin-1..3` | 697/739/781, 605 → +34, 639 |
| `scorecard` (board + clip) | 340, 316 → 740, 632 |
| `score-bar-1..3` | 376, 442 → 622, 474 · 376, 506 → 512, 538 · 376, 570 → 594, 602 |
| `key-bench` | 417.6, 658 → 662.4, 702 |
| `kimi-tile2` / `fable-tile2` | 300, 292 → 412, 404 / 668, 292 → 780, 404 |
| `design-window` | 212, 432 → 500, 609.2 |
| `bar-a` / `bar-fable` / `bar-c` / `bar-base` | 596, 545.2 → 648, 609.2 · 698, 432 → 750, 609.2 · 800, 507.2 → 852, 609.2 · 588, 609.2 → 860, 615.2 |
| `key-frontend` / `key-expensive` (ONE baseline, EQUAL seats) | 206.6, 644 → 505.4, 688 / 574.6, 644 → 873.4, 688 |
| `sheet-stack` (the folder) | 206, 312 → 494, 512 |
| `key-designs` | 236.6, 544 → 463.4, 588 |
| `kimi-tile3` / `equals` / `fable-tile3` | 548, 318 → 660, 430 · 688, 358 → 736, 390 · 764, 318 → 876, 430 |
| `key-similar` | 571.6, 462 → 852.4, 506 |
| `build-track` / `num-66` / `key-build` | 200, 616 → 880, 676 · 554, 622 → 754, 670 · 444.6, 702 → 635.4, 746 |

`build-fill` is authored at the CUT width (227 px of a 668 px fill = 34 %) and
the entrance sets it to 668 and tweens it down on the word *cut* — so the
authored HTML is the held frame, which is what makes still proofs possible
without GSAP.

---

## 5. EVERY ASSET KEY IT RESOLVES

| registry key | file | where it lands | ink side (core px) |
|---|---|---|---|
| `kimi` | `assets/logos/ai-models/kimi.png` | `#kimi-tile`, `#kimi-tile2`, `#kimi-tile3` | 56 = 0.50 of the 112 px tile (chart clause 5) |
| `claude` | `assets/logos/ai-models/claude-color.png` | `#fable-tile`, `#fable-tile2`, `#fable-tile3` | 56 |

**MARK IDENTITY, and these are FILE choices, not design choices:**
* **`kimi` is the raster `kimi.png`, not `kimi-mark.svg`** — the svg is a Simple
  Icons single-path MONOCHROME glyph and LAW 12 retired monochrome reductions as
  defaults. The raster is 112×112, i.e. 1:1 against the tile at HD delivery, and
  downscales cleanly to the 56 px ink with no upscale anywhere.
* **FABLE 5's MARK IS `claude` (`claude-color.png`)**, and the plan calls that a
  decision rather than a fallback: Anthropic ships no separate "Fable" asset, so
  under LAW 35 the Claude sunburst IS this model family's product mark. Never
  legal in its place: `claude-code` (the CLI mascot — a different product),
  `claude-code-sticker` (retired by MARK IDENTITY), `claude-black` (monochrome,
  LAW 12), `claude-cowork` (a different product). If a dedicated `fable` key is
  ever registered, swap it and re-seal.
* All six tiles share ONE rounded-square treatment (112 px, radius 18, 3 px
  `rgba(17,17,17,.16)` border, `#FFFDF9` fill) — LAW 32, no odd one out. Each
  tile carries a BACKGROUND, so Gate 1's `_loutline` can never read the emphasis
  border-flip as an outline and the raster inside can never be read as boxed
  image text (LAW 38 rule 2b). **Do not add `data-emphasis="box"` to a tile.**

**THE DEPTH CAST IS YOURS, NOT THE SCENE'S.** The plan's `cast` /
`cutout_logo_lanes` are `openai, gemini, deepseek, qwen, mistral, grok` — the
other frontier models you pay for by the token and could put a design job
through. `openai` and **not** `chatgpt`: this short is about price per token and
the consumer-app mark argues the wrong category. `kimi` and `claude` are
deliberately ABSENT — they are this story's own subject marks and they live on
the STAGE (a subject mark in the depth field is the run-9 defect). You still own
`cutout_depthfield.assert_cast_resolves()` before a frame renders.

**THERE IS NO SOURCE CARD AND NO POST ANYWHERE IN THIS VIDEO.**
`pointing_cues.scan` returns **zero** cues on the tight transcript
(`gen/_cues_kimifable.json`), no sentence names a platform, and GLOBAL LAW 3 puts
a post on screen only when the post IS the news. Do not invent one.

---

## 6. WHERE THIS SCENE DEPARTS FROM THE PLAN — three, all forced by cold reads

Full evidence in `plans/kimifable_scene_notes.md` and
`review/artwork_scoring_kimifable.json`.

1. **THE TWO CORDS ARE GONE and the tags lie FLAT.** The plan hangs each price
   tag off its tile by a cord that terminates on `anchor_points(TAG_BOX, 1,
   "top")`. Independent readers named a hanging tag *"hanging pendant lamp"*,
   *"birdhouse"* ×2, *"handbag hanging by strap"* and *"hanging birdhouse"* — a
   peaked box with a punched hole on a string IS a birdhouse, at every stroke
   weight and every crop size tried. The tag now lies flat under its tile, point
   to the left, hole in the point, welded to the tile in one declared block, and
   has been named *"price tag"* on every read since. **There is no connector
   anywhere in this scene**: `SC.CONNECTORS` is empty and
   `SC.assert_no_connectors(html)` refuses a `data-connect-to` that reappears.
   If your lane wants one back, it is a repair round and it re-seals.
2. **THE SCORECARD IS ON A CLIPBOARD.** Same card, same three ruled rows, same
   single terracotta bar — plus the board and the clip. As a plain bordered card
   it was named *"bar chart"* by seven readers and **not one could commit**; one
   wrote the reason into its own answer, *"bar chart (not an object)"*.
3. **THE PAYOFF'S STACK OF WINDOWS IS A FOLDER.** The plan draws "a lot of
   designs" as three copies of the window glyph. Every reader named that
   correctly and only three of nine could commit, and one called it *"stack of
   credit cards"* — a stack of three is not the SINGLE everyday object the
   reader is asked for. The folder makes the same claim as one object, with
   pages standing out of it carrying this video's own window chrome.

Everything else is the plan as written: the lane, the nine beats, the four
chapters and their seams, every cue, the key term, all six keys and their BELOW
placement, both emphases, the lifetimes, the blocks, the 1-of-3 that runs through
all four chapters, and the outro on this video's own themed object.

---

## 7. WHAT YOU MUST CHANGE TO SEAT IT IN THE STAGE ZONE (cutout)

1. **`k`** = `(ZY1 − ZY0) / (SC.CONTENT_Y1 − SC.CONTENT_Y0)` off YOUR session's
   envelope (the content band is **460 core px** tall, not the 600 px box);
   `top` from the `seat_core` formula in §2; `left = (1080 − 1080·k)/2`.
2. **`plate_origin()` MUST READ `left` FROM `plate.json → plate_box`** and never
   compute `(1080 − box_w)/2`. The plate is OVER-WIDE by default and its box is
   deliberately not centred. `prep/stages/kimifable.plate.json` had not landed
   when this module was written — read it, do not quote this file for it.
3. **Derive the caption clearance with the pill that RENDERS (114.59)**, never
   the frozen 108.2 seat constant.
4. **THE MATTE IS CONSUMED, NEVER REDONE.** When
   `shorts_run17/MATTES_FINAL.md` exists, `matting/kimifable/matte_kimifable_v5_{cut,rim,alpha}.webm`
   and its `plate.json` / `selection.json` are approved as they are: no
   re-track, no re-selection, no repair pass, no Modal matting call of any kind.
   Stamp the staged matte BY CONTENT (path + size + mtime), never by name.
5. **Declarations to keep.** The scene emits `data-block`, `data-label-for`,
   `data-overlap-ok`, `data-inside` and `data-bleed`. Do not strip any. The four
   coins carry `data-overlap-ok` + `data-inside` because a coin is CONTAINED by
   the tag it sits in; `#wipe` and `#o-sheet` carry `data-bleed`.
6. **GLOBAL LAW 8 / the edge-fade guard.** Nothing in this core touches a frame
   edge (margins ≥ 200 left, ≥ 200 right in every chapter), so
   `cutout_core.guard_edge_fade` has no target inside the scene; your lane
   wrappers still need theirs. `#wipe` and `#o-sheet` are the two deliberate
   bleeds and both are declared.
7. **NEVER OCCLUDE HIM.** The lowest ink is core 554 → **canvas 746** on the
   split, against a cap top at ~44 % of frame height (~y 845), so nothing here
   comes near the silhouette and nothing needs a `behind` declaration — but
   re-derive it from YOUR envelope, because your `top` is not mine.
8. **Gate 1 only sees the direct children of a clip.** This format wraps the
   whole scene in one `#core` div, so `check_layout` measures one box. Carry
   `SC.self_check()` into your build; a green Gate 1 on this shape is not
   evidence about geometry.

---

## 8. THE PROOF EVIDENCE

| what | where |
|---|---|
| seal record | `review/artwork_pass_kimifable.json` |
| scoring, with every read judged | `review/artwork_scoring_kimifable.json` |
| cold-read rounds (3, independent) | `review/phone_reader_kimifable_artwork_round{1,2,3}.json` |
| candidate round (two tag drawings) | `review/phone_reader_kimifable_artwork_cand.json` |
| the earlier probes that forced §6 | `review/phone_reader_kimifable_artwork_probe{,_haiku,2,3,4}.json`, `review/_probe{5,6,7,8}.json` |
| phone crops the readers saw (1:1, 405×720) | `review/proofs/kimifable_seal/{00,01,02,03}.png` |
| the four chapter frames they were cut from | `review/proofs/kimifable_seal/chapter{0,1,2,3}_full.png` (+ `_phone.png`) |
| blind copies handed to the readers | `review/cold/kimifable-*/` |
| chart comparison against run 15 | `review/proofs/kimifable_vs_run15.png` |

The four sealed crops and what three independent readers called them:

| # | intended | phone px | round 1 | round 2 | round 3 |
|---|---|---|---|---|---|
| 0 | a price tag | 113 × 51 | price tag (unsure) | price tag (sure) | price tag (sure) |
| 1 | a benchmark scorecard | 165 × 133 | clipboard (sure) | clipboard (sure) | clipboard (sure) |
| 2 | a website layout | 123 × 82 | web browser window (sure) | browser window (sure) | web browser window (sure) |
| 3 | a folder of designs | 123 × 90 | file folder (sure) | file folder (sure) | file folder (sure) |

Readers were `claude -p --model opus`, one independent process per crop, launched
from `/tmp` on the absolute path of a blind copy under a random token, with no
plan, no topic and no answer key. The pipeline's configured default reader was
refusing every dispatch with a usage cap, which is a dispatch failure and not a
read; a `haiku` control named three of the four crops wrong with full confidence
and was not used.

---

## 9. WHAT I LEARNED DRAWING IT (so you do not learn it twice)

1. **BIGGER IS NOT CLEARER.** Scaling the hanging tag up 27 % — a strictly
   larger crop, 57 × 59 instead of 45 × 57 — turned *"price tag"* into
   *"hanging birdhouse"* on the very next read. Silhouette beats pixels every
   time; the object's identity is its outline, not its size.
2. **THE READER IS ASKED FOR AN EVERYDAY OBJECT, AND IT MEANS IT.** Two of this
   scene's four objects failed on that word alone and neither failure was about
   legibility: a bar chart is not a thing a person has held (fix: a clipboard),
   and a stack of three windows is not *a* thing at all (fix: a folder). Both
   went from "named right, cannot commit" to three-of-three `sure` with no
   change to the claim the picture makes.
3. **A LONGER STRING MADE IT WORSE.** Lengthening the tag's cord from 34 to
   50 px, on the theory that a visible string proves a tag, produced
   *"birdhouse"*, *"birdhouse"*, *"handbag hanging by strap"*. When a cue is
   ambiguous, adding more of it adds more ambiguity.
4. **PICK THE READER, THEN KEEP IT.** `haiku` answers `sure` to everything and
   was wrong on 3 of 4 crops; `opus` names correctly and hedges. A confident
   wrong reader is worse than an unsure right one, and mixing them makes the
   evidence incoherent. Every round in the seal is the same model.
5. **THE AUTHORED HTML IS THE HELD FRAME.** Every entrance in this module is a
   `fromTo` whose `to` is the authored style, so a still proof needs no GSAP and
   no lane project — `kimifable_proof.py` forces opacity to 1, hides the other
   chapters, screenshots 1080 × 1920 and downscales to 405 × 720. That is why
   nine design rounds cost zero renders.
6. **OPACITY BELONGS IN THE `to`, NEVER ONLY IN THE `from`.** Inherited from the
   run-14 handoff and honoured here: a later `to(..., {opacity:0})` records 0 as
   its start value under the timeline PRIME every seek-based tool performs, and
   Gate 1 drops any atom under 0.15 opacity — so an invisible element reads as
   an absent one.
7. **THE TWO KEYS OF CHAPTER 2 SHARE ONE BASELINE AND ONE SEAT WIDTH.** Three
   keys on one row at two baselines is the defect Miguel CONFIRMED in the run-13
   clerk pass, and unequal sibling seats push the composition's optical axis off
   540 — which `self_check()` refuses. `FRONT-END DESIGN` is the longer string,
   so both seats are 298.8 px.
8. **THE COINS ARE DIVS, NOT SVG CIRCLES.** Gate 1's `_lring` returns true on the
   `<circle>` TAG whatever its fill, and then `enclose` errors if the circle
   contains another live atom within 26 px. Every disc in this scene that is a
   thing in the argument is a bordered div with `border-radius: 50%` (the run-14
   coin's own solution); the only `<circle>` elements left are id-less strokes
   inside a drawing.
