# nextslide — SHARED LANE SCENE HANDOFF

**Written by the design agent (plan + artwork) for the SPLIT and CUTOUT authors.**
The plan is the contract (`plans/nextslide_plan.json`); this file is the
convenience. If anything below disagrees with the plan, the plan wins and you
write your own note. Section 9 lists where the module departs from the plan's
letter.

Neither lane redraws anything in this module. It is sealed by
`production.py seal` (`review/artwork_pass_nextslide.json`, module + handoff
hashes); a lane that needs a change writes a note, it does not edit the module.

---

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/nextslide_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import nextslide_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_nextslide_proof.py --out <run>/review/proof_nextslide` (seeks the REAL timeline in Chromium) |
| proofs | `<run>/review/proof_nextslide/` (`00.png`, `01.png`, `frame_*.png`, `sheet_top.png`, `proofs.json`) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the whole 33.2 s scene: html to drop inside ONE
`transform: scale(k)` wrapper (`transform-origin: 0 0`, static), and a list of
`tl.*` javascript strings for your timeline. It reads no files and takes no
format argument.

**EASES the tweens reference — your page must define all three:**
`const POP="back.out(2.05)"; const SOFT="power3.out"; const SWING="power2.inOut";`
(`cutout_core.page()` defines only POP/SOFT/EXIT: add SWING.)

**Proof-harness gotcha (for your own page checks):** `page.evaluate("tl.seek(t)")`
returns the Timeline object and Playwright hangs serialising it. Evaluate
`"tl.seek(t); 0"`.

### `media` — the six rasters the scene paints

```python
for key in ("openai", "chatgpt", "claude", "gemini", "grok"):
    CC.MARK_INK[key] = CC.measure_mark(key, LOGOS / SC.LOGO_FILES[key])
    media[f"_{key}_img"] = CC.mark_img(f"assets/<copied file>", key, SC.MARK_SIDE)   # 56.0 ink
media["_nextslide_img"] = ('<img src="assets/nextslide-wordmark.png" alt="" '
    'style="position:absolute;left:50%;top:50%;width:196px;height:64.4px;'
    'transform:translate(-50%,-50%);display:block"/>')
```

`LOGOS = ~/Documents/Workspace/assets/logos`. Sizes are CORE px; do not rescale
for the cutout, the core's `scale(k)` carries them. Exact code:
`gen/_nextslide_proof.py::media_for`.

**THE FILES ARE NAMED, NOT GUESSED** (`SC.LOGO_FILES`, `SC.NS_FILE`):

* `design-tools/nextslide-wordmark.png` — NEXTSLIDE lockup with its orange X,
  876 x 288 (3.04:1). NEW 2026-09-22: fetched from nextslide.ai (the official
  OpenAI x NextSlide og image, white keyed to alpha) and registered in
  `assets/logos/registry.json` as `nextslide-wordmark`; the bare orange X is
  `nextslide` (`design-tools/nextslide-mark.png`, not used on stage: nobody
  knows the X alone). Seated on a WIDE 236 x 112 card, never a square tile.
* `ai-models/openai.png` — the OpenAI knot, black (the company the sentence names).
* `ai-models/chatgpt-color.png` — the green ChatGPT app mark (the PRODUCT, LAW 35).
* `ai-models/claude-color.png`, `ai-models/gemini-color.png`, `ai-models/grok.png`
  — the "any AI model" roster.

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
* `SC.CONTENT_Y0, SC.CONTENT_Y1 = 10.0, 574.0` — the band the core paints in
  (canvas 202 … 766 = 10.5 % … 39.9 %). Y0 = key term box top, Y1 = the
  PRETTY + UNDERSTANDABLE box bottom.
* **Centred on x = 540 at every held instant**: beat 0 and beat 4 the easel alone
  (376 … 704); beats 1-3 the displaced easel + chain span 118 … 962 (centre 540).
* Seat the core in a stage zone with `left = (1080 − 1080·k)/2` and
  `top = round(centre − (SC.CONTENT_Y0 + SC.CONTENT_Y1)/2 · k, 2)`.

**GATE SCALING.** Non-block gutters are authored at ≥ 44 core px (tile column
rows 44 apart; OpenAI → ChatGPT 44; card → tile column 92; easel box → card 76,
board → card 90). Everything tighter is a declared block (`SC.DECLARED_BLOCKS`):
the key term (bottom 68) over the easel peg (top 110) and the verdict (top 530)
under the legs (ink bottom 508) are welded to the easel.

---

## 3. THE TIMELINE (`SC.CUE`, word starts from `cuts/nextslide/transcript_tight.json`)

| t | word | what happens |
|---|---|---|
| 0.14 | AI | the easel pops in, alone, centred (legs, ledge, peg, board) |
| 0.30 → 1.4 | sucks at creating | the MESSY slide scribbles on stroke by stroke |
| 1.80 | (presentations ends 1.78) | KEY TERM `AI PRESENTATIONS`, first type, alone |
| 3.94 | OpenAI | easel + key term slide LEFT together, −258 px (LAW 19 displacement) |
| 4.10 | OpenAI | OpenAI tile pops in at the right column |
| 5.20 | NextSlide | NEXTSLIDE card pops in between |
| 5.52 | — | arrow card → OpenAI (acquired) |
| 7.38 | built | arrow card → easel board (built for this) |
| 8.98 | The | OpenAI tile + its arrow leave |
| 9.78 | NextSlide | card border flips terracotta (emphasis), back at 10.60 |
| 13.02 / 13.26 / 13.50 | any / AI / model | Claude, Gemini, Grok tiles pop in, one per word |
| 13.82 | out | three arrows into the card's right edge (staggered 0.10) |
| 14.94 → 16.36 | presentations … things | the card → easel arrow brightens |
| 17.50 | They | model tiles, their arrows and the card → easel arrow leave |
| 18.92 / 19.10 | OpenAI | OpenAI tile returns, arrow card → OpenAI redraws |
| 20.72 / 20.90 | ChatGPT | ChatGPT tile under OpenAI, short arrow down into it |
| 21.62 | And | the whole chain leaves |
| 21.86 | honestly | easel + key term return to the centre (x 0) |
| 25.08 | presentations | the mess fades off the board |
| 25.24 / 25.72 | — / that | clean slide: title, subtitle, baseline; three flat-top bars rise (stagger 0.16) |
| 26.94 | pretty | `PRETTY` under the easel |
| 28.06 | understandable | `+ UNDERSTANDABLE`; the board frame flips terracotta |
| 29.14 | Now | opaque cream sheet rises (0.46 s); board hidden at 29.62 |
| 29.62 → | — | small easel glyph, terracotta rule, lockup |

Nothing drifts: arrivals, two displacements with a spoken reason, fades.

---

## 4. THE BESPOKE OBJECT — self-checked, DO NOT REDRAW

`SC.BESPOKE` (core boxes, held instants, both at the centred seat):

| i | name | t | core box | phone crop |
|---|---|---|---|---|
| 0 | slide on easel (messy) | 3.00 | 376, 110, 704, 508 | `review/proof_nextslide/00.png`, 123 x 149 |
| 1 | chart on easel (clean) | 28.50 | 376, 110, 704, 508 | `review/proof_nextslide/01.png`, 123 x 149 |

Own-eyes read at 405x720: 00 reads as a presentation easel with a scribbled,
crooked slide; 01 as a bar chart on an easel with a terracotta frame. Not a UI
glyph (no cylinder, gear, bell, magnifier); the tripod legs are what make the
rectangle a THING, not a screen. Map `core` through your own k/origin for crops.

---

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 40** — `SC.A_MODEL_TO = anchor_points(SC.NS_BOX, 3, "right")` = (758, 192.9),
  (758, 231), (758, 269.1): three arrows into ONE target, evenly spaced and
  mirror-symmetric about y 231. Sources `SC.A_MODEL_FROM` = tile left-edge centres
  (850, 75 / 231 / 387). Card → OpenAI: (758, 231) → (850, 231). Card → easel:
  (522, 231) → the displaced BOARD's right edge (432, 231), the board's virtual
  rectangle, never the tripod outline. OpenAI → ChatGPT: (906, 287) → (906, 331).
  Every connector carries `data-connect-to` + `data-overlap-ok`; heads are pulled
  back 4 px so the round cap lands on the edge (LAW 7).
* **LAW 39 / 28** — `data-label-for="easel"` on `#key-term` (ABOVE) and
  `#key-verdict` (BELOW), both centred on the easel's axis; `#key-term` moves with
  `#easel` in the same tween on both displacements. The verdict only exists at the
  centred seat.
* **LAW 9** — `AI PRESENTATIONS`, 48 px JetBrains Mono 800 uppercase, ls 2, first
  type on screen (1.80).
* **LAW 41** — `SC.DECLARED_BLOCKS`, stamped as `data-block`.
* **LAW 42** — `SC.LIFETIMES`: only the easel block is anchored
  (`SC.SCENE_ANCHORS`); every chain mark has a finite window. The OpenAI tile and
  the card → OpenAI arrow have TWO windows (4.10–9.26 and 18.92–21.90).
* **LAW 38** — two emphases, both BOXING on drawn objects: `#nextslide-card`'s own
  border flip (9.78 → 10.84) and the easel's `.bframe` stroke flip (28.06 →).
  No `<circle>` tag, no ring, no marker highlight (no raster text in the video).
* **LAW 51** — both slides are CHILDREN of `#easel` (`.messg`, `.cleang` inside
  its SVG): the slide moves with the easel in every lane.
* **LAW 34** — the three bars are flat-top rects, no line across their tops.

---

## 6. THE POINTING CUES

`pointing_cues.py --vid nextslide` → `no pointing cue in this take`
(`gen/_cues_nextslide.json`, cues []). Nothing answered, nothing waived.

## 7. WHAT THE CUTOUT OWNS

* The matte, the wing review and the stage-zone seating. At plan time only the
  **cut** marker existed (`prep/stages/nextslide.cut.json`: status ok, wall 78.4 s,
  cut master 33.2 s); plate, prompt0, track, ship and cues markers had NOT landed,
  so *wing review: prompt0 not landed at plan time - the cutout author owns it.*
* `SC.CUTOUT_LOGO_LANES = ("canva", "copilot", "google-workspace", "perplexity",
  "mistral")`, files in `SC.CUTOUT_LANE_FILES` (all resolve under
  `assets/logos`). None is a stage mark. Fade them in after the hook has landed.
* Your own k and origin. Everything in the stage zone comes from this file.

## 8. WHAT THE WHITEBOARD DOES

It does not import this module. It redraws the same argument per the plan's
`beats[].whiteboard`: the easel first, alone, then the mess, then
`AI PRESENTATIONS`; chapters per `plan.boards` (four, easel carried as anchor),
the clean slide on the same easel, `PRETTY + UNDERSTANDABLE` under it and a
`box_emphasis` around the easel.

## 9. WHERE THIS MODULE DEPARTS FROM THE PLAN'S LETTER

1. Plan beat 1 says the arrow into the easel lands on "the easel's board": it lands
   on the board's RIGHT-edge centre at its displaced seat (432, 231), level with the
   card row, so it is a horizontal arrow.
2. The mess "wipes" as a 0.26 s fade of the whole `.messg` group, not a directional
   wipe; the clean slide then draws on stroke by stroke.
3. The ChatGPT connector is 44 px long (the column gutter); it reads at phone size
   (verified on `frame_21.30.png`).
