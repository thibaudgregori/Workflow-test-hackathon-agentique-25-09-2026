# hermesbrowser — SHARED LANE SCENE HANDOFF

**From the design agent, for the SPLIT author and for Astra's CUTOUT.** The plan
(`plans/hermesbrowser_plan.json`) is the contract; this file is the convenience. If
they disagree, the plan wins. Neither lane redraws anything in this module: it is
sealed (`review/artwork_pass_hermesbrowser.json`, production v4), and a lane that
builds on a changed module is refused.

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/hermesbrowser_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import hermesbrowser_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_hermesbrowser_proof.py` (renders the real timeline, crops, frames, sheet) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the whole 26.48 s scene (`SC.DUR`): html to drop inside ONE
`transform: scale(k)` wrapper (`transform-origin: 0 0`, 1080 x 600 core) and a
list of `tl.*` strings to append to your own paused timeline `tl`. It reads no
files and takes no format argument. Eases are emitted as string literals
(`"power3.out"`, `"back.out(2.05)"`, `"power2.inOut"`), so the page needs no
`SWING` constant. Labels carry their own inline JetBrains Mono / uppercase style
and the class `mono`; every element uses class `abs` (the page must define
`.abs{position:absolute}`; `box-sizing:border-box` is assumed for the bordered
browser and tiles, as the chassis pages already do).

### `media`: ONE raster, two ids

```python
key, rel = next(iter(SC.LOGO_FILES.items()))   # "nous-girl-line", "ai-models/nous-girl-line.png"
CC.MARK_INK[key] = CC.measure_mark(key, LOGOS / rel)
img = CC.mark_img("assets/nous-girl-line.png", key, SC.MARK_SIDE)   # MARK_SIDE = 74 (ink, by area)
media = {"_hermes_img": img, "_hermes_img_c": img}
```

MARK IDENTITY: Hermes is the Nous girl (Miguel's standing rule, never the Hermes H
glyph), file `nous-girl-line.png` (transparent line art; the white-boxed
`nous-girl.png` is plate-on-plate on a card tile). No other mark is on the stage.

## 2. UNITS AND PLACEMENT

* Core px, `canvas_y = core_y + 192` in the split. Content band
  `SC.CONTENT_Y0 .. SC.CONTENT_Y1` = 70 .. 574 (canvas 262 .. 766), horizontal
  ink 130 .. 945; the composition is centred on x = 540 at every chapter start.
* **Cutout:** seat the same core in the stage zone above the silhouette's crown:
  pick `k` so that core 70..574 lands between the frame's top-10 % line and
  the pill-clearance line derived from THIS session's matte envelope (pill that
  renders = 114.59 px), and `left = (1080 - 1080 k) / 2` so x = 540 stays the
  axis. Nothing else changes. Author gutters are >= 24 core px so a k near 0.95
  still clears the 16 px refusal line.
* Tightest non-block gutters (core px): verb object to verb object 120; object
  top to browser bottom 52 (the links cross it); MAIN BROWSER seat to
  HERMES AGENT seat 218 after the slide; bubble tail tip to tile top 10 (declared
  block `chat`).

## 3. THE TIMELINE (`SC.CUE`, word starts from `cuts/hermesbrowser/transcript_tight.json`)

| t | event |
|---|---|
| 0.10 | "Hermes": Hermes tile pops ALONE on x = 540 (LAW 19/20) |
| 0.46 | "Agent": **HERMES AGENT** written above, 48 px, first type (LAW 9) |
| 1.08 | "browser": tile slides left; browser window pops at (416, 230); BROWSER 1.30 |
| 2.34 | "desktop application": app frame draws round tile + browser |
| 3.58 | "Now,": chapter A leaves (0.30); browser glides to top centre (330, 100) |
| 7.30 / 7.40 / 7.50 | "see": binoculars, SEE, link into browser bottom |
| 8.70 / 8.80 / 8.90 | "operate": steering wheel, OPERATE, link |
| 9.34 / 9.44 / 9.54 | "analyze": microscope, ANALYZE, link |
| 9.92 - 11.40 | "anything": browser outline flips terracotta and back |
| 11.74 | "So": chapter B objects, words, links leave; browser holds |
| 13.50 | "main": MAIN BROWSER under the browser |
| 15.40 | "any question": browser + MAIN BROWSER slide -200; "?" bubble pops 15.56 |
| 18.24 / 18.40 | "Hermes": tile under the bubble; HERMES AGENT on the MAIN BROWSER line |
| 20.04 | "do the task": arrow Hermes -> browser right edge; page clears 20.24; tick 20.38 |
| 21.38 | "help you": Hermes tile border flips terracotta, HELD |
| 22.30 | opaque rising sheet (0.46 s); board cleared 22.78; binoculars glyph 22.80, rule 23.10, lockup 23.20 |

Beat edges `SC.BEAT_EDGES`.

## 4. THE THREE BESPOKE OBJECTS (`SC.BESPOKE`, core boxes, held instants)

| i | name | t | core box | own-eyes check at 405x720 |
|---|---|---|---|---|
| 0 | pair of binoculars | 8.40 | 135, 362, 325, 514 | `review/proof_hermesbrowser/00.png`: two barrels, eyepieces, focus post; reads "binoculars" |
| 1 | car steering wheel | 9.30 | 445, 362, 635, 514 | `01.png`: rim, hub, three spokes; reads "steering wheel" |
| 2 | science lab microscope | 10.40 | 755, 362, 945, 514 | `02.png` (redrawn once: the first tube floated free of the arm and the stage read as two lines); now tube held by the arm over a stage bar; reads "microscope" |

Map `core` through your own k/origin for any crop. None is on the refused
UI-glyph list (cylinder, gear, bell, magnifier: the magnifier was refused at plan
time for ANALYZE). The browser, app frame and bubble are UI chrome, never bespoke.

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 39 / 50**: `data-label-for` on all seven labels. Verb row: same 28 px,
  same 190 px seat, one baseline `SC.VERB_ROW_Y = 530`. Chapter C: MAIN BROWSER and
  HERMES AGENT, same 232 px seat, one baseline `SC.C_ROW_Y = 334`.
* **LAW 40**: three verb links into `hb-browser`, ends from
  `anchor_points(SC.BROWSER_B, 3, "bottom")` = 397.2 / 540 / 682.8 at y 310 (the
  proof asserts equality with `whiteboard_build.anchor_points`); the Hermes arrow
  ends at `anchor_points(SC.BROWSER_C, 1, "right")` = (550, 205). All carry
  `data-connect-to="hb-browser"` and `data-overlap-ok`. Links draw AFTER their node.
* **LAW 41**: `SC.DECLARED_BLOCKS`, stamped as `data-block`; `data-container` on
  `#app-frame`.
* **LAW 42 / 43 / 45**: `SC.BOARD_MODE = "chapters"`, seams 3.58 and 11.74, outro
  22.30 (`SC.BOARD_CHAPTERS`). The browser is the only anchor
  (`SC.SCENE_ANCHORS`) and is complete on screen through both seams.
  `SC.LIFETIMES` has every window.
* **LAW 38**: two border flips on DRAWN objects (browser outline, Hermes tile
  border). No ring, ellipse, `<circle>` tag or highlight anywhere.
* **LAW 28 / 51**: each object is ONE wrapper div (`#obj-<name>`); the browser and
  MAIN BROWSER receive the identical slide tween.
* **Ghost rule**: drawn strokes declare `pathLength="100"`, rest at
  stroke-opacity 0 and reveal one frame after the draw starts.

## 6. THE POINTING CUE

None (`gen/_cues_hermesbrowser.json`, `cues: []`; cues marker cue_count 0).

## 7. WHAT THE CUTOUT OWNS

* The matte. Markers at design time: plate ok (over-wide, crop
  2992x1870+213+236, scale_k 0.481283, head 450.9 px, face_dx 0.039 %);
  prompt0 ok with `wing_review: true` (instrument abstained, removed_px 0);
  **selection ERROR and track REFUSED** by the chair audit (right side, 2528 px
  leak at mean luma 50.4 over a ceiling of 40, which the audit itself says reads
  as beard/jaw, not chair). Astra re-reviews `matting/hermesbrowser/prompts/kf_overlay_00000.png`
  and the contour. `plate_origin()` reads `left` from `plate_box`.
* `SC.CUTOUT_LOGO_LANES = ("chatgpt", "perplexity", "claude", "gemini",
  "openclaw", "copilot")`: assistants that live in or drive a browser; all six
  resolve (`review/proof_hermesbrowser/proofs.json`). `nous-girl-line` is excluded
  (it is on the stage). Lanes fade in once the hook has landed.

## 8. THE WHITEBOARD

Does not import this module. Redraws the same argument per the plan's
`whiteboard_version` fields: HERMES AGENT first, the tile, the browser with
BROWSER, the app frame; chapter B's browser at the top with binoculars / steering
wheel / microscope and SEE / OPERATE / ANALYZE, terracotta lines into the
browser's bottom; chapter C's MAIN BROWSER, the "?" bubble, the Hermes tile with
HERMES AGENT on the same line, the arrow and the tick.

## 9. DEPARTURES FROM THE PLAN'S LETTER

None. The plan's bespoke bboxes were updated to the final drawn boxes (objects
enlarged from 170x136 to 190x152 after the first proof read small at phone size).

## 10. PROOF EVIDENCE

`review/proof_hermesbrowser/`: `00.png` `01.png` `02.png` (bespoke crops at
405x720 scale), `zoom_NN.png` (the same at full size), `frame_*.png` /
`frame_*_phone.png` (thirteen composed frames 0.60 to 24.50 s), `sheet.png`
(contact sheet of the top zone), `proofs.json` (boxes, mark resolution, LAW 40
anchor equality).
