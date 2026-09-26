# codexappshots: shared lane scene handoff

**From the design agent, for the SPLIT author and the CUTOUT author.** The plan
(`plans/codexappshots_plan.json`) is the contract; this file is the convenience. If
they disagree, the plan wins. Neither lane redraws anything in this module: it is
sealed (`review/artwork_pass_codexappshots.json`, production v4), and a lane that
builds on a changed module is refused.

## 1. The module

| | |
|---|---|
| path | `<run>/gen/codexappshots_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import codexappshots_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_codexappshots_proof.py` (renders the real timeline, crops, frames, sheet, connector contact) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the whole 34.12 s scene: html to drop inside ONE
`transform: scale(k)` wrapper (`transform-origin: 0 0`) and a list of `tl.*`
strings to append to your own paused GSAP timeline `tl`. It reads no files and
takes no format argument. Eases are emitted as string literals
(`"power3.out"`, `"back.out(2.05)"`, `"power2.inOut"`, `"power2.in"`), so the page
needs no SWING/EXIT constants. The page must give `.abs{position:absolute}` and
`.mono{font-family:'JetBrains Mono';text-transform:uppercase}` (the chassis already do).

### `media`: five rasters (two files)

```python
for key, rel in SC.LOGO_FILES.items():            # relative to ~/Documents/Workspace/assets/logos
    CC.MARK_INK[key] = CC.measure_mark(key, LOGOS / rel)
media = {
  "_chatgpt_img":     CC.mark_img(<chatgpt src>, "chatgpt", SC.MARK_SIDE),        # 66, hat tile
  "_codex_img":       CC.mark_img(<codex src>,   "codex",   SC.MARK_SIDE),        # 66, hat tile
  "_codex1_img":      CC.mark_img(<codex src>,   "codex",   SC.MARK_SIDE),        # 66, chapter 2 tile
  "_codex4_img":      CC.mark_img(<codex src>,   "codex",   SC.MARK_SIDE),        # 66, chapter 4 tile
  "_codex_title_img": CC.mark_img(<codex src>,   "codex",   SC.TITLE_MARK_SIDE),  # 26, window title bar
}
```

Files (MARK IDENTITY, named, never guessed): `chatgpt` ai-models/chatgpt-color.png
(the ChatGPT app mark, because "ChatGPT Work" is a ChatGPT product; never the OpenAI
blossom); `codex` coding-tools/codex-color.png (the Codex app mark). Both pass
`cutout_depthfield.assert_cast_resolves` (`review/proof_codexappshots/proofs.json`).
No source post or screenshot: `pointing_cues.py` returned 0 cues.

### `lockup`

```python
CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W) \
  + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W)
```
seated inside the scene's `#o-slot` (core top 250). `handle_key` is the only string
that differs between masters: `"yt"` on the split, `"tiktok_ig"` on the cutout.

## 2. The units

**CORE px = canvas px with y - 192** (`SC.CANVAS_OFFSET`); x verbatim. Core is
`SC.CORE_W x SC.CORE_H = 1080 x 600`.

* Declared content band `SC.CONTENT_Y0, SC.CONTENT_Y1 = 108, 520` (canvas 300..712):
  the two tiles out of the hat to the APPSHOTS key's box bottom. Lowest ink per
  chapter: hat 520 (APPSHOTS), trail 384 (AI ASSISTANT), keys 436 (TWO COMMAND KEYS),
  screenshot 452 (SCREENSHOT), piggy 480 (MORE TIME). Chapter 4's window reaches
  x 1020 and its polaroid peaks at y 146. Clears LAW 30's top 10 % and the split
  pill top (~787.7) by ~75 px.
* Chapters 1, 3 and 5 are mirror-symmetric about x = 540; chapters 2 and 4 put the
  laptop at centre 240 and Codex at centre 840 (mirror pair), which is the argument
  (where you work versus your AI).
* **Cutout seating:** `left = (1080 - 1080*k) / 2`,
  `top = round(stage_centre - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 * k, 2)`, with k
  from YOUR matte envelope so the band (412*k tall; 146..520 = 374 with the window
  top) clears his crown. Chapters 2 and 4 are the widest (x 80..1020); at k < 1 they
  stay inside the frame. No inked atom may occlude the silhouette.
* Tightest non-block gutters (core px): APPSHOTS to the brim 32; tile bottoms to the
  crown top 36; label gutters 28 everywhere else. Anything closer is inside a
  declared block (`SC.DECLARED_BLOCKS`, stamped `data-block`).

## 3. The timeline (`SC.CUE`, word starts from `cuts/codexappshots/transcript_tight.json`)

| t | event |
|---|---|
| 0.10 | "Here": the top hat draws, ALONE and centred (LAW 19/20 hook) |
| 0.60 / 0.88 | "simple": the wand swings in; "trick": it taps, three sparkles pop (gone 3.20-3.44) |
| 3.52 | "ChatGPT": the ChatGPT tile pops out of the hat to the upper left |
| 4.68 | "Codex": the Codex tile pops out to the upper right |
| 6.36 | **APPSHOTS** written under the hat (first type, 48 px, LAW 9) |
| 7.24-7.54 | "you": chapter 1 leaves (fade up 14 px) |
| 7.42 / 7.66 | the laptop draws left; the Codex tile lands right |
| 8.34 | "switch": three footprints walk right (0.16 s apart) |
| 9.32 | "where": three footprints walk back left |
| 10.30 | "from": the trail fades |
| 10.64 | "give": the terracotta line draws laptop -> Codex (0.50 s), touching both |
| 12.74 | AI ASSISTANT under the Codex tile |
| 13.52-13.82 | "Simply": chapter 2 leaves |
| 13.58 | the key row draws: spacebar, then both command keys, then the command symbols |
| 14.90 | "two": both command keycaps flip terracotta (LAW 38 rule 2), back 16.62 |
| 15.28 | "command": both keys press down 9 px and spring back, once |
| 15.72 | TWO COMMAND KEYS under the row |
| 17.48-17.78 | "and": chapter 3 leaves |
| 17.56 | the laptop draws CENTRED |
| 18.44 | "screenshot": white flash on the screen, bezel flips terracotta (back 19.60), the laptop slides left 300 px |
| 18.70 | the polaroid slides out of the screen to the centre, settles at -5 deg |
| 18.94 | SCREENSHOT under it |
| 21.34 | "send": SCREENSHOT leaves; the Codex tile pops at the right |
| 21.50-22.08 | the polaroid flies into the Codex tile and is absorbed; the tile bumps |
| 23.18 | "open": the tile opens into the Codex desktop app window, photo attached inside |
| 23.90 | DESKTOP APP under the window |
| 24.94-25.24 | "meaning": chapter 4 leaves |
| 25.00 | the piggy bank draws centred |
| 25.80 / 26.62 | "save" / "more": a clock coin appears above the slot, hangs 0.16 s, drops in; the pig bumps |
| 26.94 | MORE TIME under the piggy bank |
| 29.94 | "Now,": opaque rising sheet (0.46 s); board cleared 30.42; outro hat 30.44, rule 30.74, lockup 30.84 |

Beat edges `SC.BEAT_EDGES`; chapters `SC.CHAPTERS` / `SC.BOARD_CHAPTERS`; `SC.DUR = 34.12`.

## 4. The bespoke objects (`SC.BESPOKE`, core boxes, held instants)

| i | name | t | core box | own-eyes check at 405x720 |
|---|---|---|---|---|
| 0 | magician's top hat | 5.60 | 300, 108, 830, 520 | `review/proof_codexappshots/00.png`: an upright top hat with a wand, the ChatGPT and Codex tiles above it |
| 1 | trail of footprints | 10.10 | 80, 176, 896, 366 | `01.png`: bare footprints walking out and back between a laptop and the Codex tile |
| 2 | keyboard command keys | 16.00 | 172, 214, 908, 364 | `02.png`: two command keys either side of a spacebar, caps terracotta |
| 3 | instant polaroid photo | 20.40 | 434, 146, 646, 390 | `03.png`: a tilted polaroid print with a screen in its picture |
| 4 | piggy bank coins | 26.10 | 390, 108, 690, 408 | `04.png`: a piggy bank with a clock coin over its slot |

`SC.UI_OBJECTS`: the laptop (`05.png`) and the Codex desktop app window (`06.png`) are
UI chrome (A SCREEN IS NOT AN OBJECT). None of the bespoke objects is on the refused
UI-glyph list (cylinder, gear, bell, magnifier). The first hat draft (upturned) read as
a bucket at phone size and was redrawn upright; the first footprints read as grey
blobs and were enlarged 1.4x with separated toes; the first polaroid read as a framed
picture and got the thick bottom margin and a tilt. Map `core` through your own
k/origin for any crop.

## 5. The declarations you inherit

* **LAW 39 / 50**: `data-label-for` on APPSHOTS (-> `top-hat`), AI ASSISTANT
  (-> `c1-codex`), TWO COMMAND KEYS (-> `cmd-keys`), SCREENSHOT (-> `polaroid`),
  DESKTOP APP (-> `codex-window`), MORE TIME (-> `piggy-bank`). All sit BELOW, centred
  on their host; the plain labels share 28 px / 44 px row.
* **LAW 40**: one connector, `#c1-line` (`data-connect-to="c1-codex"`, `data-overlap-ok`),
  level at core y 256. Its ink spans exactly x 370..784: measured on the proof render,
  **0.0 px gap and 0.0 px overshoot at both ends** (`proofs.json -> connector`,
  `contact_left_x4.png`, `contact_right_x4.png`). At k != 1 it scales with the core and
  stays touching; do not re-seat either end.
* **LAW 41**: one `data-block` per chapter (`hat`, `trail`, `keys`, `shot`, `piggy`).
* **LAW 42 / 43**: chapters; every mark leaves with its chapter (`SC.LIFETIMES`). Only
  the outro atoms carry `data-anchor="1"`.
* **LAW 38**: border flips on DRAWN objects only (both command keycaps' `.kcap` stroke;
  `#c4-laptop-screen` borderColor). No ring, ellipse, circle tag or highlight. Round dots
  are two-arc paths; the coins are DIVs with border-radius 50 %.
* **Ghost rule**: hat, keycaps, command symbols, pig, tail, slot and the line declare
  `pathLength="100"`, rest at stroke-opacity 0 and reveal one frame after the draw starts.
* **LAW 51**: the polaroid flies and the coins drop with the module's own tweens; the
  whiteboard's arc arrow and erased coins are its drawing of the same moves. Do not
  re-tween them in a lane.

## 6. The pointing cue

None (`gen/_cues_codexappshots.json`, `cues: []`). Nothing to raise, nothing to waive.

## 7. Captions (all three lanes)

Follow `transcript_tight.json` as spoken ("send that as Codex" stays as heard;
"ChatGPT Work", "Codex", "Appshots" per the intake keyterms).

## 8. What the cutout owns

* The matte: at design time only `cut` and `plate` had landed (plate ok: crop
  3222x1790+239+264, scale_k 0.502793, head 450.8 px, over-wide, face_dx 0.046).
  Wing review: prompt0 not landed at plan time - the cutout author owns it; track and
  ship not landed. `plate_origin()` reads `left` from `plate_box`.
* `SC.CUTOUT_LOGO_LANES = ("claude-code", "cursor", "copilot", "gemini",
  "antigravity", "warp", "claude")` with files in `SC.CUTOUT_LANE_FILES`; all resolve
  (proofs.json). Excluded on purpose: chatgpt, codex (on stage). Lanes fade in once the
  hook has landed.
* Your own k and top per section 2.

## 9. The whiteboard

Does not import this module. Redraws the same argument per the plan's
`whiteboard_version` fields: top hat + wand + sparkles, ChatGPT and Codex marks above
it, APPSHOTS (first type); erase; laptop, Codex mark, footprints out and back, erased,
one straight terracotta line, AI ASSISTANT; erase; command key, spacebar, command key,
caps retraced terracotta, TWO COMMAND KEYS; erase; laptop, flash strokes, polaroid,
SCREENSHOT, arc into Codex, Codex redrawn as a window holding the polaroid, DESKTOP
APP; erase; piggy bank, two clock coins into the slot, MORE TIME.

## 10. Departures from the plan's letter

None. The plan was written after the proof crops, so its bboxes are the drawn ones.

## 11. Proof evidence

`review/proof_codexappshots/`: `00.png`-`04.png` (bespoke crops at 405x720 scale),
`05.png`, `06.png` (UI objects), `*_x4.png` (4x enlargements), `contact_*_x4.png`
(the connector's two contacts), `frame_*.png` / `frame_*_phone.png` (25 composed
frames 0.70 to 32.00 s), `sheet.png` (contact sheet of the top zone), `proofs.json`.
