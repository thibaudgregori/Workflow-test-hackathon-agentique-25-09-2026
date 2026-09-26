# grokfeatures: SHARED LANE SCENE HANDOFF

**Written by the design agent for the SPLIT author and the CUTOUT author.** The plan
(`plans/grokfeatures_plan.json`) is the contract and this file is the convenience. If
anything here disagrees with the plan, the plan wins and you write your own note.
Section 9 lists where this module departs from the plan's letter.

Neither lane redraws anything in this module. The scene is sealed with
`production.py seal` (v4: module + handoff hashes, `review/artwork_pass_grokfeatures.json`).
A lane that builds on a changed module is refused.

---

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/grokfeatures_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import grokfeatures_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_grokfeatures_proof.py` (see its `media()` for the exact media calls) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the WHOLE 34.77 s scene: the html to drop inside one
`transform: scale(k)` wrapper (`transform-origin: 0 0`) and a list of `tl.*` JavaScript
strings for your own `tl` timeline. It reads no files and takes no format argument.
Every difference between the two formats is PLACEMENT plus the `lockup` string. It
calls `SC.assert_anchor_law()` before it writes a byte.

**Eases are string literals** (`"power3.out"`, `"back.out(2.05)"`, `"power2.inOut"`,
`"power2.in"`, `"power1.inOut"`). Labels use class `mono` (JetBrains Mono, uppercase;
weight 800 is set inline). Your page must load JetBrains Mono 800. Elements use class
`abs`: give it `position:absolute; box-sizing:border-box` as the chassis already does.
Prime the timeline (`tl.progress(1).progress(0)`) before sampling: every element is
authored hidden and revealed by its tween.

### `media`: the rasters the scene paints

```python
for key, rel in SC.LOGO_FILES.items():            # names, never guesses (MARK IDENTITY)
    CC.MARK_INK[key] = CC.measure_mark(key, LOGOS / rel)   # copy the file into assets/logos/
media = {mkey: CC.mark_img(f"assets/logos/{Path(SC.LOGO_FILES[k]).name}", k, side)
         for mkey, (k, side) in SC.MEDIA_SIDES.items()}
```

| media key | logo (registry key = file) | ink side (CORE px) | where |
|---|---|---|---|
| `_chatgpt_img` | `chatgpt` = `ai-models/chatgpt-color.png` | 74 | tile on podium step 1 |
| `_gemini_img` | `gemini` = `ai-models/gemini-color.png` | 74 | tile on podium step 2 |
| `_grok_img` | `grok` = `ai-models/grok.png` | 74 | the Grok tile (ch 1) AND the Grok Build tile (ch 2) |
| `_spacex_img` | `spacex` = `ai-models/spacex-wordmark.svg` (alias spacex-ai) | 92 (by area; ~262 x 32 ink) | the SpaceX AI plate (ch 4) |

Sizes are ink sides in CORE px. Do not rescale them for the cutout: the core's own
`scale(k)` carries them.

### `lockup`: the outro's handle block

```python
CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W) \
  + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W)
```

It is seated inside the scene's own `#o-slot` (core top 250). `handle_key` is the only
string that differs between masters: `"yt"` on the split, `"tiktok_ig"` on the cutout.

---

## 2. THE UNITS

**CORE px = the plan's CANVAS px with y shifted by -192.** `canvas_y = core_y + 192`,
and x is untouched. `SC.CORE_W, SC.CORE_H = 1080.0, 600.0`.

* `SC.CONTENT_Y0, SC.CONTENT_Y1 = 88.0, 534.0` is the band the core really paints
  (canvas 280 to 726, 14.6 % to 37.8 % of frame height). Y0 is the calendar's binder
  arches and the feature icons' tops. Y1 is the single-line label row's box bottom
  (MODELS + APPS, 24 FEATURES, GROK BUILD, all at core 490..534). The open box's
  bottom ink is ~534 too. At k = 1 the lowest ink clears the caption pill's top
  (~787.7) by ~61 px.
* Every chapter is symmetric about x = 540 (ink extents: podium 315 to 765 with the
  floor hairline 140 to 940; calendar 356 to 724, then after the slide calendar 228
  to Grok Build label 858; feature row 120 to 960 with the box 363 to 717; pile 320
  to 760 under the plate 370 to 710). The ONE transient asymmetry is the Grok tile
  standing on the floor at x 805..917 from 1.52 to 1.90 before it hops onto step 3.
  So `left = (1080 - 1080*k) / 2`.
* For the cutout, seat the core so its CONTENT BAND is centred on your stage zone:
  `top = round(centre - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 * k, 2)`.
* Rightmost ink: the DEEP RESEARCH icon to core x 960 and its label to ~932, and the
  Grok tile's floor position to 917 (1.52 to 2.3 s). None is caption text; the
  composition may sit under the platform rail (LAW 30 amendment). Recheck under your k.

---

## 3. THE TIMELINE

`SC.CUE` carries every instant (word STARTS from `cuts/grokfeatures/transcript_tight.json`
unless marked `authored`). `SC.BEAT_EDGES` is the plan's beat table. `SC.DUR = 34.77`.

| ch | t | on screen |
|---|---|---|
| 0 | 0.10-8.60 | the winners podium draws ALONE on the axis with its floor hairline (0.10); ChatGPT's tile drops onto step 1 (0.40), Gemini's onto step 2 (0.62); on "Grok" (1.52) the Grok tile lands on the floor right of the podium; on "slowly" (1.90) ONE slow 0.70 s hop onto the empty step 3; `TOP 3` above (3.26, the first type); the Grok tile's border flips terracotta (3.30) and back (4.60); numerals 1 2 3 on the step faces (3.50); `MODELS` under the podium (6.16), it slides left and `+ APPS` lands beside it (7.38); all leave 8.30 |
| 1 | 8.44-15.00 | the calendar page draws centred (8.44, complete by ~8.85); on "shipped" 24 terracotta ticks fill the day squares in date order, one per 0.039 s (9.96-10.98); `24 FEATURES` under it (10.92, on "24"); on "Grok" the page and its label slide left 128 (13.06); the Grok Build tile pops on the right, bottom-aligned (13.30); the terracotta arrow draws page -> tile (13.56) and `GROK BUILD` lands under the tile on the same baseline (13.60); all leave 14.70 |
| 2 | 14.84-24.70 | the open cardboard box draws centred (14.84, complete by ~15.15); each feature icon rises out of the box's opening to its seat on its word, its two-line name 0.30 s later: dashboard (17.06), photo + wave (18.32), node triangle (19.50), page stack + down arrow (21.18); on "name" the box outline flips terracotta (23.28) and back (23.98); icons and names leave 24.40 |
| 3 | 24.56-29.80 | the box STAYS (it carries the seam): flaps vanish, the opening becomes a taped lid (24.56); the SpaceX plate pops at the top (25.52); the closed box shrinks into the pile's bottom-row slot 1 (26.40); eleven parcels drop out of the plate onto the pile, one per 0.26 s (26.64-29.58), top two rotated -3 / +4 deg |
| 4 | 29.80-34.77 | opaque rising sheet (29.80); the small podium glyph (30.30), rule (30.60), lockup (30.70) |

Every erase hands over to an idea (LAW 45): the calendar and the box are complete
within 0.30 s of their seams, and seam 3 is carried by the box itself.

---

## 4. THE FOUR BESPOKE OBJECTS: DO NOT REDRAW

`SC.BESPOKE` carries CORE boxes and the held instant of each. The design agent checked
every one at phone size (405x720) in v4 (no cold readers).

| i | object | t | core box | proof |
|---|---|---|---|---|
| 0 | three-step winners podium | 4.20 | 296, 90, 784, 470 | `review/proof_grokfeatures/00.png` |
| 1 | calendar full of checkmarks | 12.60 | 340, 84, 740, 468 | `01.png` |
| 2 | open cardboard box | 16.40 | 350, 310, 730, 538 | `02.png` |
| 3 | pile of cardboard boxes (under the SpaceX plate) | 29.60 | 300, 104, 780, 518 | `03.png` |

`SC.UI_OBJECTS`: the four feature icons (`04.png`), UI-level, named by their keys.
Map `core` boxes through your own k and origin when you cut phone crops.

---

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 40 / CONNECTORS TOUCH WHAT THEY CONNECT.** One connector, `#arrow-cal`
  (`data-connect-to="t-gbuild"`, `data-connect-from="cal"`, `data-overlap-ok`): tail
  (596, 402) = the calendar page's OUTER right edge after the -128 slide (butt cap), tip
  (702, 402) = the Grok Build tile's OUTER left edge = `anchor_points(tile, 1, "left")`.
  Measured in the browser: tail gap 0.0 px, tip gap 0 px (`proofs.json`,
  `end_tail.png`, `end_tip.png`). The tiles STAND on the podium steps (bottom edge on
  the step's top ink), a declared block.
* **LAW 39 / 50.** `TOP 3` ABOVE `podium` (the key term, 48 px). Every other name is
  BELOW its object: `MODELS` and `+ APPS` -> `podium`, `24 FEATURES` -> `cal`,
  `GROK BUILD` -> `t-gbuild` (these three single-line classes share ONE baseline, core
  490), the four two-line feature names (24 px, core 236) -> `ic-dash`, `ic-modal`,
  `ic-agent`, `ic-deep`. All carry `data-label-for`.
* **LAW 41**: `SC.DECLARED_BLOCKS`, stamped as `data-block`.
* **LAW 42**: `SC.LIFETIMES`. Chaptered board: every board mark has a finite window;
  only the four outro marks are anchors (`SC.SCENE_ANCHORS`). `#box` lives 14.84-30.28
  (open box, then parcel).
* **LAW 38**: two box emphases, both border/outline flips of drawn objects: `#t-grok`
  border to `rgb(221,114,89)` 3.30-4.84, `#box .bxo` stroke 23.28-24.22. No ring, no
  `<circle>` tag anywhere (round things are paths), no highlight (no raster text).
* **LAW 28 / 51**: numerals are children of `#podium`; ticks are part of `#cal`'s SVG;
  `#key-24` slides with `#cal` by the same tween. The pile parcels are separate
  elements that never move once landed.
* **HIDDEN-AT-0**: every element is authored at `opacity:0` (or stroke-opacity 0) and
  revealed by its tween.

---

## 6. THE POINTING CUE

None: `pipeline/pointing_cues.py --vid grokfeatures` returned no cue
(`gen/_cues_grokfeatures.json`, `cues: []`). No source card, nothing waived.

## 7. WHAT THE CUTOUT OWNS

* The matte and stage-zone seating. At plan time: `cut` ok (34.77 s, 71.4 s wall,
  "model-authored keep ranges"), `plate` ok (over-wide, crop 2864x1790+647+242, scale_k
  0.5028, face_dx 0.036 %), `prompt0` ok (wing_review true; the instrument abstained, no
  cut), `selection` present, `track` RUNNING (matanyone2, no cost booked yet), no `ship`
  marker, `cues` ok (0). The Astra matte step owns the selection and the matte.
  `plate_origin()` must read `left` from `plate_box`.
* `SC.CUTOUT_LOGO_LANES = ("claude", "deepseek", "meta", "perplexity", "mistral", "kimi")`,
  files in `SC.CUTOUT_LOGO_FILES`: the other AI contenders Grok is racing. Mixed, none
  repeated, never grok, chatgpt, gemini or spacex (all on the stage). All six pass
  `cutout_depthfield.assert_cast_resolves`, and so do the four stage marks.
* Your own k and origin. The logo lanes fade in after the hook lands (after 3.26, when
  TOP 3 is written), never later.

## 8. WHAT THE WHITEBOARD DOES NOT DO

It does not import this module. It redraws the same argument in marker ink per beat
`whiteboard_version` in the plan: the same podium with ChatGPT / Gemini / Grok and the hop,
TOP 3, MODELS + APPS, the calendar with 24 ticks, the arrow into the Grok Build mark, the
open box with the four icons, the closing box and the parcel pile under SpaceX. The keys
are the same and land on the same words.

## 9. WHERE THIS MODULE DEPARTS FROM THE PLAN'S LETTER

1. The plan's `bbox` values are normalised canvas boxes at the split's placement.
   `SC.BESPOKE` carries the real CORE boxes and is authoritative for geometry (the open
   box sits 20 px lower than the plan's bbox, to keep a 32 px gutter under the feature
   names once the icons grew to 120 px).
2. Plan ids map to DOM ids: `podium` = `#podium` (+ `#floor`), `chatgpt-tile` =
   `#t-chatgpt`, `gemini-tile` = `#t-gemini`, `grok-tile` = `#t-grok`, `key-term-top-3` =
   `#key-top3`, `label-models` / `label-apps` = `#key-models` / `#key-apps`, `calendar` =
   `#cal`, `label-24-features` = `#key-24`, `grok-build-tile` = `#t-gbuild`,
   `arrow-calendar-to-grok-build` = `#arrow-cal`, `open-box` / `parcel` = `#box`,
   `icon-*` = `#ic-dash|modal|agent|deep`, labels `#key-dash|modal|agent|deep`,
   `spacex-plate` = `#spacex`, `box-pile` = `#parcel-0, #parcel-2 .. #parcel-11`.
3. The plan says the parcel shrinks into the pile as the icons leave. It holds centred
   and closed under the SpaceX plate until 26.40, and then shrinks, so nothing sits alone
   off the axis for 1.4 s (LAW 19).

---

## 10. PROOF EVIDENCE

| what | where |
|---|---|
| phone-size crops, one object alone per 405x720 frame | `review/proof_grokfeatures/00.png` to `04.png` (+ `_x3` zooms) |
| composed frames at every beat (GRAPHIC CHART clause 9) | `review/proof_grokfeatures/frame_*.png`, `*_phone.png`, `sheet.png` |
| connector-end zooms | `review/proof_grokfeatures/end_tail.png`, `end_tip.png` |
| manifest (crops, mark resolution, connector gaps, page errors: none) | `review/proof_grokfeatures/proofs.json` |
| the seal record | `review/artwork_pass_grokfeatures.json` |
