# lunafree: SHARED LANE SCENE HANDOFF

**Written by the design agent (plan + artwork) for the SPLIT and CUTOUT authors.**
The plan is the contract (`plans/lunafree_plan.json`); this file is the
convenience. If anything below disagrees with the plan, the plan wins and you
write your own note. Section 9 lists where the module departs from the plan's
letter.

Neither lane redraws anything in this module. It is sealed by
`production.py seal` (`review/artwork_pass_lunafree.json`, module + handoff
hashes); a lane that needs a change writes a note, it does not edit the module.

---

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/lunafree_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import lunafree_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_lunafree_proof.py --out <run>/review/proof_lunafree` (seeks the REAL timeline in Chromium) |
| proofs | `<run>/review/proof_lunafree/` (`00.png` … `03.png`, `frame_*.png`, `conn_start.png`, `conn_end.png`, `_sheet_top.png`, `proofs.json`) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the whole 21.12 s scene: html to drop inside ONE
`transform: scale(k)` wrapper (`transform-origin: 0 0`, static), and a list of
`tl.*` javascript strings for your timeline. It reads no files and takes no
format argument.

**EASES the tweens reference: your page must define all three:**
`const POP="back.out(2.05)"; const SOFT="power3.out"; const SWING="power2.inOut";`
(`cutout_core.page()` defines only POP/SOFT/EXIT: add SWING.)

**Proof-harness gotcha:** `page.evaluate("tl.seek(t)")` returns the Timeline
object and Playwright hangs serialising it. Evaluate `"tl.seek(t); 0"`.

**SVG ids:** the amp's grille carries one `<clipPath id="lfgr">`. Include the
scene ONCE per page.

### `media`: the three rasters the scene paints

```python
for key in ("openai", "chatgpt"):
    CC.MARK_INK[key] = CC.measure_mark(key, LOGOS / SC.LOGO_FILES[key])
media["_openai_img"]       = CC.mark_img("assets/openai.png",        "openai",  SC.MARK_SIDE)   # 56.0 ink
media["_chatgpt_img"]      = CC.mark_img("assets/chatgpt-color.png", "chatgpt", SC.MARK_SIDE)   # 56.0 ink
media["_openai_badge_img"] = CC.mark_img("assets/openai.png",        "openai",  SC.BADGE_MARK)  # 38.0 ink
```

`LOGOS = ~/Documents/Workspace/assets/logos`. Sizes are CORE px; do not rescale
for the cutout, the core's `scale(k)` carries them. Exact code:
`gen/_lunafree_proof.py::media_for`. `_openai_img` is used TWICE (the tile that
rises out of the gift, and the tile hung on the pegboard); that is two `<img>`
of one file, fine.

**THE FILES ARE NAMED, NOT GUESSED** (`SC.LOGO_FILES`):
`ai-models/openai.png` (the black OpenAI knot: 'GPT Luna' is an OpenAI GPT
model with no mark of its own) and `ai-models/chatgpt-color.png` (the green
ChatGPT tile: 'the ChatGPT application', LAW 35 product over company). Both
resolve through `cutout_depthfield.assert_cast_resolves` (`proofs.json` →
`cast.stage`).

No source-post assets: `pointing_cues.py` returned zero cues.

### `lockup`: the outro's handle block

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
* `SC.CONTENT_Y0, SC.CONTENT_Y1 = 64.0, 506.0`: the band the core paints in
  (canvas 256 … 698 = 13.3 % … 36.4 %). Y0 = the GPT LUNA key box top, Y1 =
  the FREE + GO USERS / CHATGPT key box bottom. Transients inside it: the
  rising OpenAI tile (top 170), the lid's exit (fades while it travels up-left
  of the gift, never above y 126), the amp handle (126).
* **Centred on x = 540 at every held instant** (asserted at import): the gift
  alone 418 … 662; chapter 0 after the move 268 … 812; the amp with its waves
  260 … 820; the piggy alone 420 … 660; piggy + pegboard 170 … 910.
* Seat the core in a stage zone with `left = (1080 − 1080·k)/2` and
  `top = round(centre − (SC.CONTENT_Y0 + SC.CONTENT_Y1)/2 · k, 2)`.

**GATE SCALING.** Non-block gutters are authored at ≥ 24 core px (key term
bottom 122 → bow top 194 = 72, → risen tile top 170 = 48; FREE + GO USERS right
552 → CHATGPT left 672 = 120; piggy right 410 → pegboard left 470 = 60).
Everything tighter is a declared block (`SC.DECLARED_BLOCKS`): the keys 20-22 px
under their objects, the waves 2 px off the amp's cabinet, the tile on the
pegboard, the badge and MAX inside the amp.

---

## 3. THE TIMELINE (`SC.CUE`, word starts from `cuts/lunafree/transcript_tight.json`)

| t | word | what happens |
|---|---|---|
| 0.12 | GPT | the wrapped gift pops in, alone, centred (hook: LAW 19 / 20) |
| 0.90 | is | KEY TERM `GPT LUNA`, first type, above the gift ('Luna' ends 0.84) |
| 2.34 | free | the lid + bow pop off up-left and fade (0.46 s) |
| 2.40 | free | the OpenAI tile rises out of the open box (0.42 s, POP) |
| 3.16 / 3.60 / 3.88 | free / Go / users | `FREE`, ` + GO`, ` USERS` under the gift |
| 4.58 | ChatGPT | gift, key term and users key move left −130 (0.38 s, LAW 19) |
| 4.66 | ChatGPT | the ChatGPT tile pops at right (686, 330) |
| 4.80 → 5.02 | ChatGPT | terracotta arrow gift → ChatGPT draws, head at 5.00 |
| 4.96 | ChatGPT | `CHATGPT` under the tile |
| 5.84 | — | chapter 0 fades (0.22 s) |
| 6.04 | This | the amp pops in, alone, centred (knob pointer at −135°) |
| 8.00 | mighty | one terracotta wave each side |
| 9.04 / 9.66 / 10.18 / 10.50 / 11.00 | turn / reasoning / all / way / max | knob steps −80° / −25° / 35° / 90° / 135° |
| 9.66 | reasoning | `REASONING` under the amp |
| 11.10 | max | the MAX tick goes terracotta, `MAX` printed; waves 2 and 3 each side (11.06 / 11.16) |
| 11.96 | — | chapter 1 fades (0.22 s) |
| 12.06 | if | the piggy bank pops in, alone, centred |
| 12.56 | budget | a coin drops into the slot (0.30 s) and is gone |
| 12.62 | budget | `BUDGET` under the piggy |
| 13.14 | this | piggy + BUDGET move left −250 (0.38 s) |
| 13.18 | this | the pegboard pops in at right (470, 160) |
| 13.60 | one | the OpenAI tile hangs on the centre hook (hook appears with it) |
| 14.12 → 16.30 | best | the tile's border flips terracotta (LAW 38 boxing) |
| 14.42 / 14.52 | tools | hammer, then wrench, on the board |
| 16.00 | arsenal | `ARSENAL` under the board, level with BUDGET |
| 16.74 | Now | opaque cream sheet rises (0.46 s); board hidden at 17.22 |
| 17.22 → | — | small closed-gift glyph, terracotta rule (17.52), lockup (17.62) |

Nothing drifts: arrivals, two displacements with a spoken reason, knob steps as
discrete events, one coin drop, fades.

---

## 4. THE BESPOKE OBJECTS: self-checked, DO NOT REDRAW

`SC.BESPOKE` (core boxes at the held instants):

| i | name | t | core box | phone crop |
|---|---|---|---|---|
| 0 | wrapped gift box | 1.80 | 418, 190, 662, 442 | `review/proof_lunafree/00.png`, 91 x 95 |
| 1 | loud little speaker | 11.70 | 260, 126, 820, 440 | `review/proof_lunafree/01.png`, 210 x 118 |
| 2 | piggy bank coin | 13.02 | 420, 196, 660, 376 | `review/proof_lunafree/02.png`, 90 x 67 |
| 3 | tool pegboard wall | 15.20 | 470, 160, 910, 376 | `review/proof_lunafree/03.png`, 165 x 81 |

Own-eyes read at 405x720: 00 is a wrapped present (ribbon cross, bow); 01 a
small amp / radio with its knob on MAX and sound waves either side (amp, radio
and speaker are the same idea); 02 a piggy bank (the coin slot carries it); 03
a pegboard with a hammer, a wrench and the OpenAI tile hung between them (the
hammer's first draw was a flat-headed T and was redrawn with a curved claw).
None is a cylinder, gear, bell or magnifier. Map `core` through your own
k/origin for crops.

---

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 40 + CONNECTORS TOUCH WHAT THEY CONNECT** — `#conn-app`
  `data-connect-to="chatgpt-tile"` + `data-overlap-ok`. `SC.CONN_FROM` =
  (523.5, 386): the gift body's OUTER ink edge after the move (stroke 7 on the
  650 − 130 = 520 centre line). `SC.CONN_TO` = (686, 386) =
  `anchor_points(CHATGPT_BOX, 1, "left")`: the tile's left border. The body
  starts half a stroke inside the start edge so its round cap sits on the
  outline; the head's tip is pulled back half a stroke so its round join lands
  on the tile edge. `SC.assert_connector_contact()` re-derives both at import;
  `review/proof_lunafree/conn_start.png` / `conn_end.png` show both ends
  touching at 3x, no gap, no overshoot. Your placement scales both ends with
  the core, so contact survives any k.
* **LAW 39 / 50** — `data-label-for="gift"` on `#key-term` (ABOVE, the key
  term) and `#key-users` (BELOW); `"chatgpt-tile"` on `#key-chatgpt`; `"amp"`
  on `#key-reason`; `"piggy"` on `#key-budget`; `"board"` on `#key-arsenal`.
  Siblings share baselines: 462 in chapter 0, 398 in chapter 2.
* **LAW 9** — `GPT LUNA`, 48 px JetBrains Mono 800 uppercase, ls 2, first type
  on screen (0.90).
* **LAW 41** — `SC.DECLARED_BLOCKS`, stamped as `data-block` (`gift`,
  `chatgpt`, `amp`, `piggy`, `arsenal`).
* **LAW 42** — `SC.LIFETIMES`: every mark has a finite window; the outro set
  (`o-glyph`, `o-rule`, `o-slot`) is `SC.SCENE_ANCHORS`.
* **LAW 38** — ONE emphasis, BOXING a drawn plate: `#luna-hung`'s own border
  tweens `TILE_EDGE` → `TERRA_L` at 14.12 and back at 16.30. No `<circle>` tag
  anywhere (knobs, coin, holes and the hook are two-arc paths), no ring, no
  marker highlight (no raster text in the video).
* **LAW 51** — the knob pointer (`#amp .kp`, `svgOrigin "220 118"`), the coin
  (`#piggy .coin`) and the rising tile (`#luna-tile`, a child of `#gift`) are
  children of their object: they move with it in every lane.

---

## 6. THE POINTING CUES

`pointing_cues.py --vid lunafree` → `No pointing cue in this take`
(`gen/_cues_lunafree.json`, cues []). Nothing answered, nothing waived.

## 7. WHAT THE CUTOUT OWNS

* The matte, the wing review and the stage-zone seating. Markers read at the
  seal: plate ok (106.3 s, `overwide_applied` true, crop 2848x1780+254+262);
  prompt0 ok with **`wing_review: true`** (the instrument proposed no cut:
  look at `matting/lunafree/prompts/kf_overlay_00000.png`); selection ERROR and
  track REFUSED on a chair-audit hold (headrest wing in the reviewed contour);
  **ship ok through the SAM2 fallback** (`backend sam2`, no-chair, temporal 1,
  528 frames 1584x990, min person fraction 0.366,
  `review_status: needs_final_visual_review`). Structurally ok is not approval.
* `SC.CUTOUT_LOGO_LANES = ("gemini", "claude", "deepseek", "mistral", "qwen",
  "kimi")`, files in `SC.CUTOUT_LANE_FILES` (all resolve: `proofs.json` →
  `cast.lanes`): the small, cheap reasoning-model families a viewer compares
  Luna with. Neither `openai` nor `chatgpt` travels the lanes (they are the
  story's subject, on the stage). Fade them in after the hook has landed
  (after the tile rises, ~2.9 s).
* Your own k and origin. Everything in the stage zone comes from this file.

## 8. WHAT THE WHITEBOARD DOES

It does not import this module. It redraws the same argument per the plan's
`beats[].whiteboard`: chapter 0, the wrapped gift first, alone, `GPT LUNA`
above it, the lid off and the OpenAI mark half out on 'free', `FREE + GO USERS`
under it, the ChatGPT mark to the right with an arrow from the box's right side
to the mark's left edge (touching both), `CHATGPT` under it. Chapter 1 (erase
~5.84), the small amp alone with its big knob, one wave each side on
'mighty', the pointer stepping to the MAX tick, `REASONING` under it, two more
waves each side on 'max'. Chapter 2 (erase ~11.96), the piggy bank, a coin into
its slot, `BUDGET`; then the pegboard to its right with the OpenAI mark on a
hook, a terracotta `box_emphasis` round it on 'best', hammer and wrench on
'tools', `ARSENAL` level with `BUDGET`.

## 9. WHERE THIS MODULE DEPARTS FROM THE PLAN'S LETTER

1. The lid exit ends at +(−150, −50) px with −28° rotation while fading, so it
   never crosses the key term (a first pass sent it to −84 px, into the key
   term's band).
2. `MAX` and the MAX tick land at 11.10 (0.10 s into 'max') so the pointer has
   visibly arrived first; the extra waves follow at 11.06 / 11.16.
3. The pegboard's hook appears with the tile at 13.60 (not with the board at
   13.18), so the board never shows an empty hook.
