# openairesets — SHARED LANE SCENE HANDOFF

**Written by the design agent (plan + artwork) for the SPLIT and CUTOUT authors.**
The plan is the contract (`plans/openairesets_plan.json`); this file is the
convenience. If anything below disagrees with the plan, the plan wins and you
write your own note. Section 9 lists where the module departs from the plan's
letter.

Neither lane redraws anything in this module. It is sealed by
`production.py seal` (`review/artwork_pass_openairesets.json`, module + handoff
hashes); a lane that needs a change writes a note, it does not edit the module.

---

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/openairesets_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import openairesets_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_openairesets_proof.py --out <run>/review/proof_openairesets` (seeks the REAL timeline in Chromium) |
| proofs | `<run>/review/proof_openairesets/` (`00.png`, `01.png`, `02.png`, `frame_*.png`, `sheet_top.png`, `proofs.json`) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the whole 20.64 s scene: html to drop inside ONE
`transform: scale(k)` wrapper (`transform-origin: 0 0`, static), and a list of
`tl.*` javascript strings for your timeline. It reads no files and takes no
format argument.

**EASES the tweens reference — your page must define all three:**
`const POP="back.out(2.05)"; const SOFT="power3.out"; const SWING="power2.inOut";`
(`cutout_core.page()` defines only POP/SOFT/EXIT: add SWING.)

**Proof-harness gotcha:** `page.evaluate("tl.seek(t)")` returns the Timeline
object and Playwright hangs serialising it. Evaluate `"tl.seek(t); 0"`.

**SVG ids:** each hourglass carries two `<clipPath>` ids (`hgmct/hgmcb`,
`hg1ct` … `hg4cb`, `hgoct/hgocb`). Include the scene ONCE per page.

### `media` — the one raster the scene paints

```python
key = "openai"
CC.MARK_INK[key] = CC.measure_mark(key, LOGOS / SC.LOGO_FILES[key])
media["_openai_img"] = CC.mark_img("assets/<copied file>", key, SC.MARK_SIDE)   # 56.0 ink
```

`LOGOS = ~/Documents/Workspace/assets/logos`. Sizes are CORE px; do not rescale
for the cutout, the core's `scale(k)` carries them. Exact code:
`gen/_openairesets_proof.py::media_for`.

**THE FILE IS NAMED, NOT GUESSED** (`SC.LOGO_FILES`): `ai-models/openai.png`,
the OpenAI knot, black (the company the sentence names). Resolved by
`cutout_depthfield.assert_cast_resolves` in the proof run (`proofs.json` →
`cast.stage`).

No source-post assets: `pointing_cues.py` returned zero cues.

### `lockup` — the outro's handle block

```python
CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W) \
  + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W)
```

Seated in the scene's own `#o-slot` (core top 262). `handle_key` is the only
string that differs: `"yt"` on the split, `"tiktok_ig"` on the cutout.

---

## 2. THE UNITS

**CORE px = canvas px with y shifted by −192** (`SC.CANVAS_OFFSET`); x verbatim.

* `SC.CORE_W, SC.CORE_H = 1080.0, 600.0`
* `SC.CONTENT_Y0, SC.CONTENT_Y1 = 72.0, 564.0` — the band the core paints in
  (canvas 264 … 756 = 13.8 % … 39.4 %). Y0 = the RESETS key box top, Y1 = the
  KEEP BUILDING key box bottom. (The price tag and the tile sit inside it.)
* **Centred on x = 540 at every held instant** (asserted at import): beat 0's
  tile (270) … tag ink (813); the centred hourglass 450 … 630; the row
  232 … 847.6; the wall 330 … 750; all three lower keys centred on 540.
* Seat the core in a stage zone with `left = (1080 − 1080·k)/2` and
  `top = round(centre − (SC.CONTENT_Y0 + SC.CONTENT_Y1)/2 · k, 2)`.

**GATE SCALING.** Non-block gutters are authored at ≥ 24 core px (tile → hourglass
arrow 108, row key bottom 335 → wall 374 = 39). Everything tighter is a declared
block (`SC.DECLARED_BLOCKS`): the key term (bottom 130) over the top cap (150),
the tag hung on the cap, the `$200 / MONTH` key (top 446) under the emphasis box
(bottom 426), `4 ACCOUNTS` (top 291) under the row (bottom 271.2),
`KEEP BUILDING` (top 520) under the wall (bottom 500).

---

## 3. THE TIMELINE (`SC.CUE`, word starts from `cuts/openairesets/transcript_tight.json`)

| t | word | what happens |
|---|---|---|
| 0.10 | OpenAI | the hourglass pops in, alone, centred; its top bulb nearly empty |
| 0.30 → 1.00 | just started | the last sand pours through (stream visible), then holds |
| 1.06 | selling | hourglass slides right +40 (LAW 19); OpenAI tile pops in at left (1.12) |
| 1.40 | selling | terracotta arrow tile → hourglass draws (0.22 s) |
| 1.66 → 2.12 | resets | THE FLIP: 180° turn; at 2.12 the turn is zeroed and the sand swaps (full top) |
| 2.18 | for | KEY TERM `RESETS`, first type, above the hourglass |
| 2.40 | their | the price tag with `$` swings on from the top cap |
| 3.30 | because | tile, arrow, tag and RESETS fade out |
| 3.68 | now | hourglass back to the centre (x 0) |
| 4.50 / 5.36 | $200 / per | `$200`, then ` / MONTH` under the hourglass |
| 5.72 | subscription | half the sand falls (top 0.45) |
| 6.84 | no | the rest pours through (top 0) |
| 7.04 | longer | terracotta emphasis box pops round the hourglass (out 8.90) |
| 9.10 | which | `$200 / MONTH` fades |
| 10.26 | to | the empty hourglass shrinks (×0.62) into the row's left seat |
| 10.60 / 10.90 / 11.22 | four / different / accounts | hg-2, hg-3, hg-4 pop in, FULL, one per word |
| 10.68 | — | `#hourglass` hands over in place to `#hg-1` (same picture, same frame) |
| 11.62 | — | `4 ACCOUNTS` under the row |
| 11.96 | all | hg-2..4 pour TOGETHER (top 0.75) |
| 13.82 / 14.24 / 14.76 | keep / building / things | wall course 1 / 2 / 3 drops in brick by brick; each time hg-2..4 drop again (0.55 / 0.35 / 0.15) |
| 14.60 | — | `KEEP BUILDING` under the wall |
| 16.08 | Now | opaque cream sheet rises (0.46 s); board hidden at 16.56 |
| 16.56 → | — | small hourglass glyph, terracotta rule, lockup |

Nothing drifts: arrivals, displacements with a spoken reason, sand drains as
discrete events (the stream shows only while sand is falling), fades.

---

## 4. THE BESPOKE OBJECTS — self-checked, DO NOT REDRAW

`SC.BESPOKE` (core boxes at the held instants):

| i | name | t | core box | phone crop |
|---|---|---|---|---|
| 0 | hourglass price tag | 2.90 | 490, 150, 813, 410 | `review/proof_openairesets/00.png`, 121 x 98 |
| 1 | four hourglasses row | 12.70 | 232, 110, 847.6, 271.2 | `review/proof_openairesets/01.png`, 231 x 61 |
| 2 | rising brick wall | 15.40 | 330, 374, 750, 500 | `review/proof_openairesets/02.png`, 157 x 48 |

Own-eyes read at 405x720: 00 reads as an hourglass with a `$` price tag on a
string; 01 as four hourglasses in a row, three pouring; 02 as a brick wall
(brick-tinted fills in running bond; the pale first draft could pass for
keyboard rows and was tinted). None is a cylinder, gear, bell or magnifier; the
hourglass's own UI-glyph meaning (wait) is the same word as the object.
Map `core` through your own k/origin for crops.

---

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 40** — `SC.A_SELL_FROM = anchor_points(OPENAI_BOX, 1, "right")` = (382, 280)
  → `SC.A_SELL_TO = anchor_points(HG_SHIFTED, 1, "left")` = (490, 280): the
  hourglass's VIRTUAL rectangle at its displaced seat, level to 0 px, never on
  the curved glass. `data-connect-to="hourglass"` + `data-overlap-ok`; the head
  is pulled back 4 px so the round cap lands on the edge (LAW 7).
* **LAW 39 / 50** — `data-label-for="hourglass"` on `#key-term` (ABOVE, the key
  term) and `#key-200` (BELOW); `data-label-for="hg-row"` on `#key-accounts`
  (BELOW); `data-label-for="wall"` on `#key-building` (BELOW). Every object name
  sits under its object; only the key term sits above.
* **LAW 9** — `RESETS`, 48 px JetBrains Mono 800 uppercase, ls 2, first type on
  screen (2.18; the tag's `$` follows at 2.40).
* **LAW 41** — `SC.DECLARED_BLOCKS`, stamped as `data-block` (`hourglass`,
  `openai`, `row`, `wall`).
* **LAW 42** — `SC.LIFETIMES`: every mark has a finite window; the outro set
  (`o-glyph`, `o-rule`, `o-slot`) is `SC.SCENE_ANCHORS` with `hourglass`.
* **LAW 38** — ONE emphasis, BOXING a drawn object: `#emph-hourglass`, a 5 px
  terracotta rectangle (radius 14, `data-emphasis="box"`) 16 px round the
  hourglass, 7.04 → 9.18. No `<circle>` tag (the tag's hole is a path), no ring,
  no marker highlight (no raster text in the video).
* **LAW 51** — the sand rects are children of each hourglass SVG and scale from
  their own bottom edge (`transformOrigin "50% 100%"`, set in the timeline at
  t = 0): the sand flips, moves and shrinks with its glass in every lane. The
  whiteboard's drain must read the same way (top falls, bottom rises, together).

---

## 6. THE POINTING CUES

`pointing_cues.py --vid openairesets` → `No pointing cue in this take`
(`gen/_cues_openairesets.json`, cues []). Nothing answered, nothing waived.

## 7. WHAT THE CUTOUT OWNS

* The matte, the wing review and the stage-zone seating. At plan time:
  cut ok (63.7 s, master 20.64 s), plate ok (92.6 s, `overwide_applied` true),
  prompt0 ok with `wing_review: true`, selection ok, cues ok, **track RUNNING**
  (matanyone2), **ship NOT landed**. The cutout author reads the ship marker.
* `SC.CUTOUT_LOGO_LANES = ("chatgpt", "codex", "claude", "claude-code", "cursor")`,
  files in `SC.CUTOUT_LANE_FILES` (all resolve: `proofs.json` → `cast.lanes`).
  `claude-code` is `coding-tools/claudecode-color.png`, the outline-free mascot
  (MARK IDENTITY), NOT the registry's sticker file. None is the stage mark
  (openai). Fade them in after the hook has landed (after the flip, ~2.2 s).
* Your own k and origin. Everything in the stage zone comes from this file.

## 8. WHAT THE WHITEBOARD DOES

It does not import this module. It redraws the same argument per the plan's
`beats[].whiteboard`: the hourglass first, alone, running out; the OpenAI mark and
an arrow; the flip; `RESETS` above; the `$` tag. Chapter 0 carries the hourglass
through `$200 / MONTH` and the drain to empty with a `box_emphasis`; chapter 1
(erase at 9.10) redraws it small as the left of four, `4 ACCOUNTS` under the row,
the wall course by course, `KEEP BUILDING` under it.

## 9. WHERE THIS MODULE DEPARTS FROM THE PLAN'S LETTER

1. The OpenAI tile pops at 1.12 (0.06 s into 'selling') so it arrives while the
   hourglass is already moving aside, not before it.
2. `$200` shows alone for 0.86 s at its final seat (left of the centred pair)
   before ` / MONTH` joins it; the key's box is centred on 540 throughout.
3. The row's left hourglass (`#hg-1`) stays EMPTY for the rest of the video:
   it is the account that already hit its limit; only hg-2..4 pour.
