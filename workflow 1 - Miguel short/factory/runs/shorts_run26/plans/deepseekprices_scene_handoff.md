# deepseekprices — SHARED LANE SCENE HANDOFF

**From the design agent, for the SPLIT author and for Astra's CUTOUT.** The plan
(`plans/deepseekprices_plan.json`) is the contract; this file is the convenience. If
they disagree, the plan wins. Neither lane redraws anything in this module: it is
sealed (`review/artwork_pass_deepseekprices.json`, production v4), and a lane that
builds on a changed module is refused.

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/deepseekprices_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import deepseekprices_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_deepseekprices_proof.py` (renders the real timeline, crops, frames, sheet) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the whole 33.58 s scene: html to drop inside ONE
`transform: scale(k)` wrapper (`transform-origin: 0 0`) and a list of `tl.*`
strings to append to your own paused timeline `tl`. It reads no files and takes
no format argument. **Eases are emitted as string literals** (`"power3.out"`,
`"back.out(2.05)"`, `"power2.inOut"`), so the page needs no `SWING` constant.
The page must provide `.abs{position:absolute}` and
`.mono{font-family:'JetBrains Mono';text-transform:uppercase}` (both chassis do).

### `media`: six rasters, four files

```python
for key, rel in SC.LOGO_FILES.items():            # relative to ~/Documents/Workspace/assets/logos
    CC.MARK_INK[key] = CC.measure_mark(key, LOGOS / rel)
media = {mkey: CC.mark_img(f"assets/<basename of LOGO_FILES[key]>", key, side)
         for mkey, (key, side) in SC.MEDIA_SIDES.items()}
```

`SC.MEDIA_SIDES` (ink side, core px): `_tag_ds_img` deepseek 88; `_col_ds_img`,
`_col_claude_img`, `_col_openai_img`, `_col_gemini_img` 56 each (0.50 of the 112
tile); `_badge_ds_img` deepseek 44.

Files (MARK IDENTITY, named, never guessed): `deepseek` ai-models/deepseek.png (the
blue whale, registry `deepseek`, aliases include "deepseek v4 flash"); `claude`
ai-models/claude-color.png (Anthropic's product mark); `openai` ai-models/openai.png
(the provider blossom, NOT the ChatGPT app); `gemini` ai-models/gemini-color.png.
All four pass `cutout_depthfield.assert_cast_resolves` (`review/proof_deepseekprices/proofs.json`).
No source post, screenshot or other raster: `pointing_cues.py` returned 0 cues.

### `lockup`

```python
CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W) \
  + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W)
```
seated inside the scene's `#o-slot` (core top 250). `handle_key` is the only string
that differs between masters: `"yt"` on the split, `"tiktok_ig"` on the cutout.

## 2. THE UNITS

**CORE px = canvas px with y − 192** (`SC.CANVAS_OFFSET`); x verbatim. Core is
`SC.CORE_W x SC.CORE_H = 1080 x 600`.

* Declared content band `SC.CONTENT_Y0, SC.CONTENT_Y1 = 86, 568` (canvas 278..760):
  the tallest bar's top (Claude, 86) to the PRICE PER TOKEN box bottom (568). The
  tag's string top is 96; V4 FLASH box 496..554; AI EMPLOYEE box 480..524. Clears
  LAW 30's top 10 % and sits ~28 px above the split's caption pill top (~787.7).
* **Mirror-symmetric about x = 540** at every settled instant: chapter 1 tag
  230..430 and gauge 550..850; chapter 2 chart 196..884 with columns at
  276 / 452 / 628 / 804; chapter 3 computer 430..650.
* **Cutout seating:** `left = (1080 − 1080·k) / 2`,
  `top = round(stage_centre − (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 · k, 2)`, with k
  from YOUR matte envelope so the band (482·k tall) clears his crown. Every inked
  atom must clear the envelope (NEVER OCCLUDE HIM).
* Tightest non-block gutters (core px): tag to gauge 120; column to column 64
  (tiles), 80 (bars); column wrappers (80..506) to PRICE PER TOKEN 18; computer
  feet (454) to AI EMPLOYEE 26; tag bottom (472) to V4 FLASH 24. Everything
  closer is a DECLARED block (`SC.DECLARED_BLOCKS`, stamped `data-block`).

## 3. THE TIMELINE (`SC.CUE`, word starts from `cuts/deepseekprices/transcript_tight.json`)

| t | event |
|---|---|
| 0.18 | "DeepSeek": the price tag lands ALONE on x = 540, complete (string, hole, whale, drawn $) — LAW 19/20 hook |
| 0.72 | "victim": ONE swing about the string top, then still |
| 3.20 | "increasing": the tag slides left (dx −210, the one displacement); 3.24 the demand gauge draws at right |
| 3.74 | "demand": the needle swings once from low into the terracotta zone |
| 6.16 | "V4": **V4 FLASH** written under the tag (first type, 48 px) |
| 9.06 | "increase": terracotta up-arrow draws on the tag beside the $ |
| 9.70 | "prices": the tag outline flips terracotta (held) |
| 12.18 | "Now,": chapter 1 erases (0.20 s); 12.22 baseline + DeepSeek column (tile + 1X bar) open ALONE on x = 540 |
| 14.70 | "two": bar to 2X, counter **2X** appears on its top |
| 15.36 | "four": bar to 4X, counter rides up and reads **4X** (terracotta) |
| 16.92 | "one": DeepSeek column + counter slide right (dx +264) to x = 804 |
| 17.06 / 17.30 / 17.52 | Claude / OpenAI / Gemini columns rise, all taller than the 4X bar |
| 19.76 | "price per token": **PRICE PER TOKEN** under the chart |
| 21.28 | "price per task": the DeepSeek bar border flips terracotta (held) |
| 24.30 | "buy": chapter 2 erases; 24.32 the computer tower draws ALONE on x = 540 |
| 27.30 | "locally": the power button fills terracotta |
| 28.68 | "AI employee": lanyard + badge (whale photo) drop over the case, one swing; **AI EMPLOYEE** 28.72 |
| 29.54 | "follow": opaque rising sheet (0.46 s); board cleared 30.02; outro tag 30.04, rule 30.34, lockup 30.44 |

Beat edges `SC.BEAT_EDGES`. `SC.DUR = 33.58`. Chapter seams `SC.CHAPTER_SEAMS`.

## 4. THE TWO BESPOKE OBJECTS (`SC.BESPOKE`, core boxes, held instants)

| i | name | t | core box | own-eyes check at 405x720 |
|---|---|---|---|---|
| 0 | DeepSeek price tag | 2.60 | 440, 96, 640, 472 | `review/proof_deepseekprices/00.png`: a hanging price tag with the whale and a $, no competing reading |
| 1 | computer wearing badge | 29.30 | 430, 104, 650, 454 | `review/proof_deepseekprices/01.png`: a desktop PC tower wearing a lanyard ID badge with the whale |

Map `core` through your own k/origin for any crop. Neither is on the refused
UI-glyph list (cylinder, gear, bell, magnifier); no window/card/screen is declared bespoke.
The gauge and the chart are furniture (counter+meter lane), not bespoke objects.

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 39 / 50**: `data-label-for` on V4 FLASH (→ price-tag, below), the counter
  (→ bar-deepseek, above, it rides the bar), PRICE PER TOKEN (→ price-chart, the
  baseline wrapper, below) and AI EMPLOYEE (→ computer-badge, below). Every NAME in
  the video sits below what it names, at 28 px except the 48 px key term.
* **LAW 40**: no connectors. The up-arrow is ink inside the tag.
* **LAW 41**: `SC.DECLARED_BLOCKS`.
* **LAW 42 / 43**: CHAPTERS, `SC.BOARD_MODE = "chapters"`, `SC.BOARD_CHAPTERS`;
  every mark is finite (`SC.LIFETIMES`), `SC.SCENE_ANCHORS = ()`, no `data-anchor`.
  Longest lifetime: the tag 0.18–12.38 (36 % of the take).
* **LAW 38**: two border flips on DRAWN objects (tag outline path stroke, DeepSeek
  bar border). No ring, ellipse, `<circle>` tag or highlight anywhere.
* **LAW 34 / 23**: flat-top bars with no top line; bars are square divs, no radius.
* **LAW 28 / 51**: the tag is ONE wrapper (`#price-tag`) and swings about its string
  top; `#counter-ds` moves with `#bar-deepseek` (same tween times); `#lanyard` holds
  strap, clip, card and whale and drops/swings as one.
* **Ghost rule**: drawn paths declare `pathLength="100"`, rest at stroke-opacity 0
  and reveal one frame after the draw starts.

## 6. THE POINTING CUE

None (`gen/_cues_deepseekprices.json`, `cues: []`). Nothing to raise, nothing to waive.

## 7. WHAT THE CUTOUT OWNS

* The matte and wing review: prompt0 landed with `wing_review: true` (instrument
  abstained, removed_px 0) — look at `matting/deepseekprices/prompts/kf_overlay_00000.png`.
  Track marker: `skipped` (matanyone2); ship marker not landed at design time.
  `plate_origin()` reads `left` from `plate_box` (plate is OVER-WIDE; crop
  2492x1780+620+242, scale_k 0.505618).
* `SC.CUTOUT_LOGO_LANES = ("qwen", "kimi", "mistral", "minimax", "ollama", "nvidia")`
  with explicit files `SC.CUTOUT_LOGO_FILES` (qwen, mistral, minimax and ollama are
  library files not listed in registry.json; the file map is authoritative, and all
  six pass `assert_cast_resolves`, see proofs.json). Excluded on purpose: deepseek,
  claude, openai, gemini (on stage). Lanes fade in once the hook has landed.
* Your own k and top per section 2.

## 8. THE WHITEBOARD

Does not import this module. Redraws the same argument per the plan's
`whiteboard_version` fields, three chapters: the tag (whale + drawn $) centred then
redrawn left, the gauge and its needle, V4 FLASH under the tag, the terracotta
arrow and outline retrace; the DeepSeek column growing 2X then 4X under a counter,
the three taller columns, PRICE PER TOKEN, the bar retraced terracotta; the tower,
the terracotta button, the lanyard badge with the whale, AI EMPLOYEE.

## 9. DEPARTURES FROM THE PLAN'S LETTER

1. The plan's normalised `bbox` values were written before the drawing; `SC.BESPOKE`
   core boxes are authoritative.
2. The power button sits upper-right on the case (not centred) so the lanyard's V
   never crosses it.

## 10. PROOF EVIDENCE

`review/proof_deepseekprices/`: `00.png`, `01.png` (bespoke crops at 405x720 scale),
`frame_*.png` / `frame_*_phone.png` (16 composed frames from 0.60 to 31.50 s),
`sheet.png` (contact sheet of the top zone), `proofs.json` (boxes, mark and lane
resolution, page errors: none).
