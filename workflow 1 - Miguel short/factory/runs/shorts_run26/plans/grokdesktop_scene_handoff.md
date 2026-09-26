# grokdesktop — SHARED LANE SCENE HANDOFF

**From the design agent, for the SPLIT author and for the CUTOUT author.** The plan
(`plans/grokdesktop_plan.json`) is the contract; this file is the convenience. If
they disagree, the plan wins. Neither lane redraws anything in this module: it is
sealed (`review/artwork_pass_grokdesktop.json`, production v4), and a lane that
builds on a changed module is refused.

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/grokdesktop_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import grokdesktop_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_grokdesktop_proof.py` (renders the real timeline, crops, frames, sheet) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the whole 34.76 s scene: html to drop inside ONE
`transform: scale(k)` wrapper (`transform-origin: 0 0`) and a list of `tl.*`
strings to append to your own paused GSAP timeline `tl`. It reads no files and
takes no format argument. **Eases are emitted as string literals**
(`"power3.out"`, `"back.out(2.05)"`, `"power2.inOut"`, `"power2.in"`), so the page
needs no SWING/EXIT constants. The page must give `.abs{position:absolute}` and
`.mono{font-family:'JetBrains Mono';text-transform:uppercase}` (the chassis already do).

### `media`: five rasters (three files)

```python
for key, rel in SC.LOGO_FILES.items():            # relative to ~/Documents/Workspace/assets/logos
    CC.MARK_INK[key] = CC.measure_mark(key, LOGOS / rel)
media = {
  "_grok_medal_img":  CC.mark_img(<grok src>,          "grok",          100.0),
  "_grok_img":        CC.mark_img(<grok src>,          "grok",          SC.MARK_SIDE["grok"]),      # 58
  "_grok_screen_img": CC.mark_img(<grok src>,          "grok",          SC.GROK_SCREEN_SIDE),       # 88
  "_chatgpt_img":     CC.mark_img(<chatgpt src>,       "chatgpt",       SC.MARK_SIDE["chatgpt"]),   # 58
  "_cowork_img":      CC.mark_img(<claude-cowork src>, "claude-cowork", SC.MARK_SIDE["claude-cowork"]),  # 66
}
```

Files (MARK IDENTITY, named, never guessed): `grok` ai-models/grok.png (the subject);
`chatgpt` ai-models/chatgpt-color.png (the ChatGPT app mark, because "ChatGPT Work"
is a ChatGPT product; never the OpenAI blossom); `claude-cowork`
ai-models/claude-cowork.png (the ORANGE Cowork mark; never claude, claude-code or
claude-cowork-pale). All three pass `cutout_depthfield.assert_cast_resolves`
(`review/proof_grokdesktop/proofs.json`). There is no source post or screenshot:
`pointing_cues.py` returned 0 cues.

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

* Declared content band `SC.CONTENT_Y0, SC.CONTENT_Y1 = 96, 552` (canvas 288..744):
  the medal ribbon / hourglass top plate to the TOP 3 key's box bottom. The
  lowest ink per chapter: medal 552 (TOP 3), bridge 486 (cliff floors), monitor
  530 (USER INTERFACE), hourglass 526 (WEEKS OR MONTHS). Clears LAW 30's top 10 %
  and sits ~40 px above the split's caption pill top (~787.7).
* Every chapter is **mirror-symmetric about x = 540** except the tiles on the
  cliffs (one Grok tile left at centre 179; ChatGPT 836 and Cowork 976 right),
  which is the argument (one versus two), on symmetric cliffs (36..314 / 766..1044).
* **Cutout seating:** `left = (1080 − 1080·k) / 2`,
  `top = round(stage_centre − (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 · k, 2)`, with k
  from YOUR matte envelope so the band (456·k tall) clears his crown. The bridge
  chapter is the widest (x 36..1044): at k < 1 it stays inside the frame. Every
  inked atom must clear the silhouette envelope (never occlude him).
* Tightest non-block gutters (core px): ChatGPT tile to Cowork tile 28; key term
  to the medal disc 28; DESKTOP APP to the arch 28; USER INTERFACE to the foot 34;
  WEEKS OR MONTHS to the bottom plate 30. Anything closer is inside a declared
  block (`SC.DECLARED_BLOCKS`, stamped `data-block`).

## 3. THE TIMELINE (`SC.CUE`, word starts from `cuts/grokdesktop/transcript_tight.json`)

| t | event |
|---|---|
| 0.10 | "Grok": the ribbon V draws, ALONE and centred (LAW 19/20 hook) |
| 0.26 / 0.30 | bail pops; the medal swings in from the ribbon with the Grok mark on its face |
| 2.10 | **TOP 3** written under the medal (first type, 48 px, LAW 9) |
| 4.16–4.46 | "Right now": chapter 1 leaves (fade up 14 px) |
| 4.32 | left cliff draws (overlaps the exit: the zone never blanks) |
| 4.80 | "working": Grok tile lands on the left cliff |
| 5.76 | "desktop": the left half of the bridge builds out over the gap |
| 6.20 | DESKTOP APP written under the bridge |
| 7.72 | "close": right cliff draws |
| 8.10 | "gap": the right half of the bridge swings across and meets it |
| 8.42–9.80 | "between": the deck outline flips terracotta (LAW 38 rule 2), back 9.80–10.04 |
| 10.46 / 11.96 | "ChatGPT" / "Claude": ChatGPT tile, then Cowork tile land on the right cliff |
| 12.90–13.20 | "People": chapter 2 leaves |
| 13.00 | the monitor pops (empty screen), stand 13.16 |
| 14.88 | "Grok": the Grok mark lands inside the screen |
| 17.76 | "nice": sidebar, message lines, input bar fade in; bezel flips terracotta (back 19.40) |
| 18.70 | USER INTERFACE written under the stand |
| 19.94–20.24 | "Now,": chapter 3 leaves |
| 20.40 | "we": the hourglass draws, top bulb full, small pile below |
| 22.52 | "given": sand pours 0.9 s, the top drops to 0.62 |
| 27.20 | "believe": sand pours again, the top drops to 0.20, the pile is full |
| 29.84 | WEEKS OR MONTHS written under it |
| 30.44 | "Now": opaque rising sheet (0.46 s); board cleared 30.92; outro medal 30.94, rule 31.24, lockup 31.34 |

Beat edges `SC.BEAT_EDGES`; chapters `SC.CHAPTERS` / `SC.BOARD_CHAPTERS`; `SC.DUR = 34.76`.

## 4. THE BESPOKE OBJECTS (`SC.BESPOKE`, core boxes, held instants)

| i | name | t | core box | own-eyes check at 405x720 |
|---|---|---|---|---|
| 0 | medal on ribbon | 2.80 | 430, 96, 650, 466 | `review/proof_grokdesktop/00.png`: a medal hanging from a V ribbon, Grok mark on the face |
| 1 | bridge between cliffs | 10.30 | 36, 184, 1044, 486 | `01.png`: an arch bridge spanning a gap between two rock cliffs, Grok tile on the left |
| 2 | sand hourglass timer | 24.20 | 440, 96, 640, 448 | `02.png`: an hourglass, top half-drained, pile below |

`SC.UI_OBJECTS`: the monitor (`03.png`, t 18.90, core 300, 100, 780, 452) is UI
chrome, not a bespoke object (A SCREEN IS NOT AN OBJECT). None of the three is on
the refused UI-glyph list (cylinder, gear, bell, magnifier). Map `core` through
your own k/origin for any crop.

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 39 / 50**: `data-label-for` on TOP 3 (→ `medal`), DESKTOP APP (→ `bridge`),
  USER INTERFACE (→ `monitor`), WEEKS OR MONTHS (→ `hourglass`). All four sit BELOW,
  centred on x = 540; the three plain labels share 28 px / 44 px row.
* **LAW 40**: no connectors at all.
* **LAW 41**: one `data-block` per chapter object (`medal`, `bridge`, `monitor`,
  `hourglass`), because Gate 1 compares `data-block` by equality; the whole bridge
  chapter is one block (tiles stand on the cliffs, the deck lands on both).
* **LAW 42 / 43**: chapters; every mark leaves with its chapter (`SC.LIFETIMES`),
  no mark is on screen for more than 30 % of the take. Only the outro atoms carry
  `data-anchor="1"`.
* **LAW 38**: two border flips on DRAWN objects (the bridge deck stroke
  `#bridge .deck`, the monitor bezel `#monitor` borderColor). No ring, ellipse,
  circle tag or highlight. The medal disc is a DIV with border-radius 50 % and a
  background; the outro medal disc is a two-arc path.
* **Ghost rule**: ribbon, cliffs, bridge, glass declare `pathLength="100"`, rest at
  stroke-opacity 0 and reveal one frame after the draw starts.
* **LAW 51**: the hourglass sand scales about its own SVG origins
  (`svgOrigin` neck 110 178 / pile base 110 328, set by the module's own tweens);
  do not re-tween the sand in a lane.

## 6. THE POINTING CUE

None (`gen/_cues_grokdesktop.json`, `cues: []`). Nothing to raise, nothing to waive.

## 7. CAPTIONS (all three lanes)

`transcript_tight.json` reads **"Claude Code Work."** at 11.96–12.52. The raw
Scribe transcript of the same take reads "Claude Cowork" and the intake keyterms
list "Claude Cowork": the pill must read **"Claude Cowork"** (plan open_questions 2,
PROPER-NOUN SPELLING). "ChatGPT Work" stays as spoken.

## 8. WHAT THE CUTOUT OWNS

* The matte: at design time `prompt0` landed with `wing_review: true` (instrument
  abstained, removed_px 0; look at `matting/grokdesktop/prompts/kf_overlay_00000.png`),
  `selection` errored and `track` is **REFUSED** by the chair audit (right side
  1830 px leak at mean luma 53.1, which reads as beard/jaw, not chair). The Astra
  matte step owns the re-review and the track; the ship marker had not landed.
  `plate_origin()` reads `left` from `plate_box` (plate is OVER-WIDE; crop
  2534x1810+597+232, scale_k 0.497238, head 451.1 px).
* `SC.CUTOUT_LOGO_LANES = ("gemini", "deepseek", "mistral", "meta", "perplexity",
  "kimi", "qwen")` with files in `SC.CUTOUT_LANE_FILES`; all resolve (proofs.json).
  Excluded on purpose: grok, chatgpt, claude-cowork (on stage). Lanes fade in once
  the hook has landed.
* Your own k and top per section 2.

## 9. THE WHITEBOARD

Does not import this module. Redraws the same argument per the plan's
`whiteboard_version` fields: medal + TOP 3 (first type, alone); erase; the two
cliffs, the Grok mark, the left half bridge + DESKTOP APP, the right cliff and
right half (retraced terracotta), ChatGPT and Cowork marks; erase; the monitor,
the Grok mark in its screen, the interface on "nice", USER INTERFACE; erase; the
hourglass with its sand redrawn lower on "given" and "believe", WEEKS OR MONTHS.

## 10. DEPARTURES FROM THE PLAN'S LETTER

1. The plan's normalised `bbox` values were written before the drawing; the
   `SC.BESPOKE` core boxes are authoritative (the bridge box grew to 36..1044 x
   184..486 when the cliffs were redrawn as canyon walls).
2. The plan's `blocks` list separate tile/cliff groups; the DOM stamps ONE
   `bridge` block for the chapter because `data-block` is compared by equality.

## 11. PROOF EVIDENCE

`review/proof_grokdesktop/`: `00.png`, `01.png`, `02.png` (bespoke crops at
405x720 scale), `03.png` (the UI monitor), `*_x4.png` (the same crops enlarged for
the author's eyes), `frame_*.png` / `frame_*_phone.png` (fourteen composed frames
0.70 to 32.50 s), `sheet.png` (contact sheet of the top zone), `proofs.json`
(boxes + mark resolution).
