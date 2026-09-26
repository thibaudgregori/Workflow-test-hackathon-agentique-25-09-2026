# warpgrok — SHARED LANE SCENE HANDOFF

**From the design agent, for the SPLIT author and for Astra's CUTOUT.** The plan
(`plans/warpgrok_plan.json`) is the contract; this file is the convenience. If
they disagree, the plan wins. Neither lane redraws anything in this module: it is
sealed (`review/artwork_pass_warpgrok.json`, production v4), and a lane that
builds on a changed module is refused.

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/warpgrok_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import warpgrok_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_warpgrok_proof.py` (renders the real timeline, crops, frames) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the whole 26.32 s scene: html to drop inside ONE
`transform: scale(k)` wrapper (`transform-origin: 0 0`) and a list of `tl.*`
strings to append to your own paused timeline `tl`. It reads no files and takes
no format argument. **Eases are emitted as string literals** (`"power3.out"`,
`"back.out(2.05)"`, `"power2.inOut"`), so the page does not need a `SWING`
constant (the cutout chassis defines only POP/SOFT/EXIT).

### `media`: the five rasters

```python
for key, rel in SC.LOGO_FILES.items():            # relative to ~/Documents/Workspace/assets/logos
    CC.MARK_INK[key] = CC.measure_mark(key, LOGOS / rel)
media = {f"_{k}_img": CC.mark_img(f"assets/<basename>", k, side) for k ...}
# sides (INK, core px): warp SC.WMARK_SIDE = 54; SC.MARK_SIDE = claude 50, openai 50, gemini 50, grok 48
```

Files (MARK IDENTITY, named, never guessed): `warp` coding-tools/warp.png (added to
the library 2026-09-22, registry key `warp`, official warp.dev silhouette, black is
Warp's own colour); `claude` ai-models/claude-color.png (Anthropic product mark);
`openai` ai-models/openai.png (the provider's black blossom, NOT the ChatGPT app
tile); `gemini` ai-models/gemini-color.png; `grok` ai-models/grok.png. All five
pass `cutout_depthfield.assert_cast_resolves` (see `review/proof_warpgrok/proofs.json`).
There is no source post, screenshot or other raster: `pointing_cues.py` returned 0 cues.

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

* Declared content band `SC.CONTENT_Y0, SC.CONTENT_Y1 = 88, 562` (canvas 280..754):
  the plank's top to the label row's box bottom. Lowest real ink is the key tips
  (~core 500) and the PROVIDERS/GROK labels (box 518..562). Clears LAW 30's top
  10 % and sits ~34 px above the split's caption pill top (~787.7).
* The composition is **mirror-symmetric about x = 540** at every settled instant:
  the plank is 140..940; three keys hang at 330/540/750; after the 16.84 slide the
  four keys hang at 225/435/645/855 (ink extents 177..903, centre 540).
* **Cutout seating:** `left = (1080 − 1080·k) / 2`,
  `top = round(stage_centre − (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 · k, 2)`, with k
  from YOUR matte envelope so the band (474·k tall) clears his crown. Nothing is
  drawn outside the band, so the core may overlap his silhouette only in its empty
  area; every inked atom must clear the envelope (NEVER OCCLUDE HIM).
* Tightest non-block gutters (core px): loose keys to each other ~37 (hook);
  hung keys 114; hook stem to screw 26; label to neighbour key > 70. Everything
  closer is a DECLARED block (`SC.DECLARED_BLOCKS`, stamped `data-block`): each key
  hangs THROUGH its hook (loop over curl), the Warp mark + WARP are the plank's face.

## 3. THE TIMELINE (`SC.CUE`, word starts from `cuts/warpgrok/transcript_tight.json`)

| t | event |
|---|---|
| 0.30 | Claude key lands ALONE on x = 540, tilted (LAW 19/20 hook) |
| 1.06 | "multiple": it slides left |
| 1.50 / 1.76 | "AI" / "agents": OpenAI and Gemini keys drop in, crooked |
| 3.38 | "same time": ONE jangle of all three, then still |
| 5.62 | "Warp": plank draws; screws 5.92; Warp mark 5.80; **WARP** 5.92 (first type, 48 px) |
| 6.48 | "centralize": three hooks draw (stagger 0.10) |
| 7.06 / 7.42 / 7.74 | "all" / "different" / "providers": each key flies up, hangs, one swing |
| 8.16 | PROVIDERS written under the group |
| 9.62–11.00 | "one simple application": plank outline flips terracotta |
| 12.26–13.70 | "everything": the three key heads flip terracotta together |
| 16.84 | "released": keys + hooks 1-3 + PROVIDERS slide −105 together |
| 17.24 | "new feature": hook 4 draws at x 855 |
| 19.42 | "Grok": Grok key drops onto hook 4, one swing; GROK 19.60 (same baseline) |
| 19.70 | "subscription": Grok head flips terracotta (held) |
| 21.36 | "Warp agent": plank flips terracotta (held) |
| 22.30 | opaque rising sheet (0.46 s); board cleared at 22.78; outro key 22.80, rule 23.10, lockup 23.20 |

Beat edges `SC.BEAT_EDGES`. `SC.DUR = 26.32`.

## 4. THE TWO BESPOKE OBJECTS (`SC.BESPOKE`, core boxes, held instants)

| i | name | t | core box | own-eyes check at 405x720 |
|---|---|---|---|---|
| 0 | three loose keys | 2.60 | 300, 250, 790, 530 | `review/proof_warpgrok/00.png`: reads "three keys" with logo heads, no competing reading |
| 1 | wall key rack | 9.20 | 140, 88, 940, 503 | `review/proof_warpgrok/01.png`: reads "keys hanging on a key rack" labelled WARP |

Map `core` through your own k/origin for any crop. Key is not on the refused
UI-glyph list (cylinder, gear, bell, magnifier); no window/card/screen is declared bespoke.

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 39 / 50**: `data-label-for` on WARP (→ key-rack, contained in the plank),
  PROVIDERS (→ key-openai, the group axis) and GROK (→ key-grok). The two sibling
  labels: same size (28 px), same 184 px seat, same baseline `SC.LABEL_ROW_Y = 518`.
* **LAW 40**: no connectors at all.
* **LAW 41**: `SC.DECLARED_BLOCKS`.
* **LAW 42 / 43**: single board, `SC.BOARD_MODE = "single"`; accumulating marks carry
  `data-anchor="1"` (`SC.SCENE_ANCHORS`); the Grok key/hook/label are finite
  (19.42–22.78, 11 % of the take). `SC.LIFETIMES` has every window.
* **LAW 38**: five border flips on DRAWN objects only (plank stroke, key-head
  borders). No ring, ellipse, circle tag or highlight anywhere.
* **LAW 28 / 51**: every key is ONE wrapper div (`#key-<name>`) holding loop,
  head, mark, collar, shaft and teeth; swings rotate the wrapper about the loop
  (`transform-origin: 48px 14px`). Do not tween a key's parts separately.
* **Ghost rule**: hooks and plank declare `pathLength="100"`, rest at
  stroke-opacity 0 and reveal one frame after the draw starts.

## 6. THE POINTING CUE

None (`gen/_cues_warpgrok.json`, `cues: []`). Nothing to raise, nothing to waive.

## 7. WHAT THE CUTOUT OWNS

* The matte and wing review: prompt0 landed with `wing_review: true` (instrument
  abstained, removed_px 0) — look at `matting/warpgrok/prompts/kf_overlay_00000.png`.
  Track marker: `skipped` (matanyone2); ship marker not landed at design time.
  `plate_origin()` reads `left` from `plate_box` (plate is OVER-WIDE; crop
  2440x1830+642+280, scale_k 0.491803).
* `SC.CUTOUT_LOGO_LANES = ("codex", "cursor", "opencode", "copilot", "kimi",
  "deepseek")` — all resolve (proofs.json). Excluded on purpose: warp, grok, claude,
  openai, gemini (on stage) and claude-code (registry path is the sticker file).
  Lanes fade in once the hook has landed.
* Your own k and top per section 2.

## 8. THE WHITEBOARD

Does not import this module. Redraws the same argument per the plan's
`whiteboard_version` fields: the same crooked keys with the same marks, WARP written
first on the plank, the keys redrawn hanging, PROVIDERS, the three-key erase-and-redraw
one step left on "released", hook 4, the Grok key, GROK on the PROVIDERS baseline.

## 9. DEPARTURES FROM THE PLAN'S LETTER

1. The plan's normalised `bbox` values were written before the drawing; `SC.BESPOKE`
   core boxes are authoritative.
2. WARP's `place` is `inside` (the plank's face), as the plan records.

## 10. PROOF EVIDENCE

`review/proof_warpgrok/`: `00.png`, `01.png` (bespoke crops at 405x720 scale),
`frame_*.png` / `frame_*_phone.png` (ten composed frames from 0.90 to 24.50 s),
`sheet.png` (contact sheet of the top zone), `proofs.json` (boxes + mark resolution).
