# hermeshub - SHARED LANE SCENE HANDOFF

**From the design agent, for the SPLIT author and for Astra's CUTOUT.** The plan
(`plans/hermeshub_plan.json`) is the contract; this file is the convenience. If
they disagree, the plan wins. Neither lane redraws anything in this module: it is
sealed (`review/artwork_pass_hermeshub.json`, production v4), and a lane that
builds on a changed module is refused.

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/hermeshub_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import hermeshub_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_hermeshub_proof.py` (renders the real timeline, crops, frames, sheet, measured seats) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the whole 24.08 s scene (`SC.DUR`): html to drop inside ONE
`transform: scale(k)` wrapper (`transform-origin: 0 0`, 1080 x 600 core) and a
list of `tl.*` strings to append to your own paused timeline `tl`. It reads no
files and takes no format argument. Eases are emitted as string literals
(`"power3.out"`, `"back.out(2.05)"`, `"power2.inOut"`, `"power2.in"`), so the
page needs no ease constants. Labels carry their own inline JetBrains Mono /
uppercase style and the class `mono`; every element uses class `abs` (the page
must define `.abs{position:absolute}` and `box-sizing:border-box`, as the
chassis pages already do: the toolbar, windows and tiles are bordered boxes).

### `media`: five rasters (all `cutout_core.mark_img`)

```python
for key, rel in SC.LOGO_FILES.items():            # nous-girl-line, figma, notion, slack
    CC.MARK_INK[key] = CC.measure_mark(key, LOGOS / rel)
media = {
  "_hermes_img":    CC.mark_img("assets/nous-girl-line.png", "nous-girl-line", SC.MARK_SIDE),      # 74
  "_hermes_tb_img": CC.mark_img("assets/nous-girl-line.png", "nous-girl-line", SC.TB_MARK_SIDE,    # 54
                                eid="tb-mark", opacity=0),   # the id and opacity 0 are REQUIRED: 8.94 pops it
  "_figma_img":  CC.mark_img("assets/figma-color.png",  "figma",  SC.MARK_SIDE),
  "_notion_img": CC.mark_img("assets/notion-color.png", "notion", SC.MARK_SIDE),
  "_slack_img":  CC.mark_img("assets/slack-color.png",  "slack",  SC.MARK_SIDE),
}
```

`LOGO_FILES` paths are relative to `~/Documents/Workspace/assets/logos`; copy the
four files into your project's `assets/`. The app images are reused (no id) in
the laptop tiles and the window tiles. MARK IDENTITY: Hermes is the Nous girl
(Miguel's standing rule, never the Hermes H glyph), `nous-girl-line.png`.

## 2. UNITS AND PLACEMENT

* Core px, `canvas_y = core_y + 192` in the split. Content band
  `SC.CONTENT_Y0 .. SC.CONTENT_Y1` = 70 .. 570 (canvas 262 .. 762), horizontal
  ink 60 .. 1020 (the three windows, chapter C); every chapter is centred on
  x = 540.
* **Cutout:** seat the same core in the stage zone above the silhouette's crown:
  pick `k` so that core 70..570 lands between the frame's top-10 % line and the
  pill-clearance line derived from THIS session's matte envelope (the pill that
  renders = 114.59 px), and `left = (1080 - 1080 k) / 2` so x = 540 stays the
  axis. Nothing else changes. The chapter-C window row is the widest ink
  (60..1020 core): at k < 1 it stays inside the frame by construction.
* Tightest non-block gutters (core px): windows 30 apart; Hermes tile bottom to
  laptop lid top 32; HUB MODE box bottom to toolbar top 42; toolbar bottom to
  ALWAYS ON 34; toolbar to window row after the 12.56 step-up 56. Declared
  contacts (0 px, one block): the toolbar seated on a window's top edge, the
  toolbar inside the box while it rises (5.90-7.32).

## 3. THE TIMELINE (`SC.CUE`, word starts from `cuts/hermeshub/transcript_tight.json`)

| t | event |
|---|---|
| 0.10 | "Hermes": Hermes tile pops ALONE on x = 540, y 244 (LAW 19/20) |
| 1.34 | "any": the tile rises to y 70 (the one displacement) |
| 1.52 | "application": the laptop draws under it; Figma / Notion / Slack tiles pop on its screen 1.70 / 1.80 / 1.90 |
| 2.30 / 2.36 / 2.42 | "working on": three terracotta lines, Hermes tile bottom -> each app tile top |
| 5.34 | "shipped": chapter A leaves (0.30); the cardboard box pops 5.40 |
| 5.86 | "Hub": tape fades, the lid shows its dark inside; 5.90 the toolbar rises OUT of the box (0.50) |
| 6.10 | "mode": **HUB MODE**, 48 px, the first type in the video (LAW 9) |
| 6.98 | "allows": the empty box drops away (0.34) |
| 8.08 / 8.12 | "always-on": status light turns terracotta and stays; ALWAYS ON under the toolbar |
| 8.94 | "Hermes Agent": the Nous mark pops into the toolbar slot |
| 11.26 - 11.90 | "toolbar": toolbar border flips terracotta and back |
| 11.98 | "that": HUB MODE and ALWAYS ON leave |
| 12.56 | "you can": toolbar steps up 60 px; Figma / Notion / Slack windows pop 12.56 / 12.66 / 12.76 |
| 13.20 / 13.52 | "drag" / "drop": toolbar shrinks to 0.62, lifts onto the Figma window, seats |
| 14.34 / 15.10 | "your entire desktop": glides to the Slack window, seats |
| 15.86 | "and": Figma and Notion windows leave; 15.92 the Slack window + toolbar move to the centre as one block (window x1.35 about its top-centre, toolbar 0.837 about its bottom-centre) |
| 16.84 | "context": the three content rows are drawn up out of the window into the toolbar (stagger 0.14, 0.50 each); 17.44 the toolbar's status lines darken |
| 17.84 - 18.90 | "application": the Slack window's border flips terracotta and back |
| 18.96 | "sitting on top of": toolbar border flips terracotta, HELD |
| 19.98 | opaque rising sheet (0.46 s); board cleared 20.46; laptop glyph 20.48, rule 20.78, lockup 20.88 |

Beat edges `SC.BEAT_EDGES`.

## 4. THE TWO BESPOKE OBJECTS (`SC.BESPOKE`, core boxes, held instants)

| i | name | t | core box | own-eyes check at 405x720 |
|---|---|---|---|---|
| 0 | open laptop computer | 3.20 | 206, 214, 874, 540 | `review/proof_hermeshub/00.png`: lid, screen, wide base with thumb scoop, three app tiles, the three lines arriving from above; reads "laptop" |
| 1 | cardboard shipping box | 5.80 | 356, 337, 724, 570 | `01.png`: 3/4 box, tape over the lid and down the front, shipping label; reads "cardboard box" |

Map `core` through your own k/origin for any crop. Neither is on the refused
UI-glyph list (cylinder, gear, bell, magnifier). The toolbar, the status light,
the windows and the context rows are UI chrome, never bespoke.

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 9 / 39**: HUB MODE (above) and ALWAYS ON (below) carry
  `data-label-for="hub-toolbar"`, both centred on x = 540. They leave at 11.98,
  before the toolbar moves (LAW 28 holds: the toolbar never moves while its
  names are on screen, except the 5.90 rise under HUB MODE's entrance).
* **LAW 40 / CONNECTORS TOUCH**: the three chapter-A links start at
  `anchor_points(SC.HT_BOX, 3, "bottom")` = 501.92 / 540 / 578.08 at y 182 (the
  Hermes tile's bottom edge) and end at `anchor_points(app_tile, 1, "top")` =
  396 / 540 / 684 at y 290 (each app tile's top edge). The proof asserts both
  against `whiteboard_build.anchor_points` and MEASURED them on the live DOM
  (`proofs.json` -> `seat_gaps_px`: tile bottom 182.0, app tops 290.0). Each
  carries `data-connect-to="app-<key>"` and `data-overlap-ok`; round caps land
  on the tile borders, no gap.
* **THE SEAT**: the toolbar's bottom edge equals the window's top edge at
  every seated instant, measured 0 px at 13.90 (Figma), 15.60, 16.60 and 18.50
  (Slack), centre offset 0.0 px. Keep `transformOrigin` as emitted (toolbar
  `50% 100%`, Slack window `50% 0%`): the chapter-D move is exact only about
  those origins.
* **LAW 41**: `SC.DECLARED_BLOCKS` - `data-block="laptop"` (laptop + app tiles,
  `data-container` on the laptop), `data-block="hub"` (box, toolbar, three
  windows). The context rows are the Slack window's children.
* **LAW 42 / 43 / 45**: `SC.BOARD_MODE = "chapters"`, seams 5.34, 11.98, 15.86,
  outro 19.98 (`SC.BOARD_CHAPTERS`). The toolbar is the only anchor
  (`SC.SCENE_ANCHORS`, `data-anchor="1"`), complete on screen through the
  11.98 and 15.86 seams; the 5.34 seam lands on the box. `SC.LIFETIMES` has
  every window.
* **LAW 38**: three border flips on DRAWN objects (toolbar twice, Slack window
  once). No ring, ellipse, `<circle>` tag or highlight anywhere; the toolbar
  radius is 26 on a 104 bar (25 %, never a pill).
* **LAW 51**: the Slack window and its toolbar get the same start (15.92),
  duration (0.50) and ease for the centring move; each bespoke object is ONE
  wrapper div.
* **Ghost rule**: the three links declare `pathLength="100"`, rest at
  stroke-opacity 0 and reveal one frame after the draw starts.
* **DOM order matters**: windows, then the toolbar, then the box. The box hides
  the toolbar while it rises out of it; the toolbar paints over the rows it
  swallows. Do not reorder `html`.

## 6. THE POINTING CUE

None (`gen/_cues_hermeshub.json`, `cues: []`; cues marker cue_count 0).

## 7. WHAT THE CUTOUT OWNS

* The matte. Markers at design time: cut ok (24.08 s); plate ok (over-wide, crop
  2450x1750+729+226, scale_k 0.514286, head 451.9 px, face_dx 0.089 %); prompt0
  ok with `wing_review: true` (instrument abstained, no cut proposed); selection
  ok ("inputs ready for the outline review"); track `skipped` (matanyone2, no
  cost on the marker); ship not landed. Astra reviews
  `matting/hermeshub/prompts/kf_overlay_00000.png`. `plate_origin()` reads `left`
  from `plate_box`.
* `SC.CUTOUT_LOGO_LANES = ("chatgpt", "claude", "gemini", "perplexity",
  "copilot", "openclaw")`: the other AI assistants that live on your desktop
  next to your apps; all six resolve (`review/proof_hermeshub/proofs.json`).
  `nous-girl-line` is excluded (it is on the stage). Lanes fade in once the hook
  has landed.

## 8. THE WHITEBOARD

Does not import this module. Redraws the same argument per the plan's
`whiteboard_version` fields: the Hermes tile, the laptop with the three app
marks and the three terracotta lines; the box, HUB MODE first and large, the
toolbar out of the lid; ALWAYS ON, the lit light, the Nous mark in the slot; the
three windows with the toolbar docked on Figma, then on Slack; the Slack window
large with its rows redrawn inside the toolbar and the two outline retraces.

## 9. DEPARTURES FROM THE PLAN'S LETTER

None. Two plan fields were updated to the drawn result before the seal: the
box's bespoke bbox (to its ink box 356, 337, 724, 570) and beat 3's picture (the
toolbar steps up 60 px at 12.56 to make room for the windows; the first proof
showed its bottom 4 px into the window row).

## 10. PROOF EVIDENCE

`review/proof_hermeshub/`: `00.png` `01.png` (bespoke crops at 405x720 scale),
`zoom_NN.png` (the same at full size), `frame_*.png` / `frame_*_phone.png`
(sixteen composed frames 0.60 to 22.00 s), `sheet.png` (contact sheet of the
top zone), `proofs.json` (boxes, mark resolution, LAW 40 anchor equality,
measured seats).
