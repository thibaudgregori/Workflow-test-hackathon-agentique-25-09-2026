# ccremote — SHARED LANE SCENE HANDOFF

**From the design agent, for the SPLIT author and for the CUTOUT author.** The plan
(`plans/ccremote_plan.json`) is the contract; this file is the convenience. If they
disagree, the plan wins. Neither lane redraws anything in this module: it is sealed
(`review/artwork_pass_ccremote.json`, production v4), and a lane that builds on a
changed module is refused.

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/ccremote_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import ccremote_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_ccremote_proof.py` (renders the real timeline, crops, frames, sheet, connector measurement) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the whole 34.92 s scene: html to drop inside ONE
`transform: scale(k)` wrapper (`transform-origin: 0 0`) and a list of `tl.*` strings to
append to your own paused GSAP timeline `tl`. It reads no files and takes no format
argument. **Eases are emitted as string literals** (`"power3.out"`, `"back.out(2.05)"`,
`"power2.inOut"`, `"power2.in"`). The page must give `.abs{position:absolute}` and
`.mono{font-family:'JetBrains Mono';text-transform:uppercase}` (the chassis already do).

### `media`: three rasters, one file

```python
for key, rel in SC.LOGO_FILES.items():            # relative to ~/Documents/Workspace/assets/logos
    CC.MARK_INK[key] = CC.measure_mark(key, LOGOS / rel)
media = {
  "_cc_tile_img": CC.mark_img(<claude-code src>, "claude-code", SC.TILE_MARK),  # 60, the three session tiles
  "_cc_row_img":  CC.mark_img(<claude-code src>, "claude-code", SC.ROW_MARK),   # 30, the phone's session rows
  "_cc_step_img": CC.mark_img(<claude-code src>, "claude-code", SC.TILE_MARK),  # 60, checklist row 1
}
```

File (MARK IDENTITY, named, never guessed): `claude-code` =
`coding-tools/claudecode-color.png`, the plain no-outline mascot; never
`claude-code-sticker` (`coding-tools/claude-code.png`). It passes
`cutout_depthfield.assert_cast_resolves` (`review/proof_ccremote/proofs.json`). There is
no source post or screenshot: `pointing_cues.py` returned 0 cues.

### `lockup`

```python
CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W) \
  + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W)
```
seated inside the scene's `#o-slot` (core top 250). `handle_key` is the only string that
differs between masters: `"yt"` on the split, `"tiktok_ig"` on the cutout.

## 2. THE UNITS

**CORE px = canvas px with y − 192** (`SC.CANVAS_OFFSET`); x verbatim. Core is
`SC.CORE_W x SC.CORE_H = 1080 x 600`.

* Declared content band `SC.CONTENT_Y0, SC.CONTENT_Y1 = 96, 546` (canvas 288..738): the
  REMOTE CONTROL key term's top to the ON/OFF BY DEFAULT key's box bottom. Lowest ink
  per chapter: circuit 546 (the key under the switch), note 430, checklist 450. Clears
  LAW 30's top 10 % and sits ~50 px above the split's caption pill top (~787.7).
* Chapter 1 is **mirror-symmetric about x = 540**: phone column 110..290, switch
  450..630, tile column 824..936 (the phone's mirror column is 790..970; the tile is
  centred in it at x 880). The note (400..680) and the checklist rows (168..912) are
  centred on 540.
* **Cutout seating:** `left = (1080 − 1080·k) / 2`,
  `top = round(stage_centre − (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 · k, 2)`, with k from
  YOUR matte envelope so the band (450·k tall) clears his crown. The widest chapter is
  the circuit (x 110..936) and the checklist (168..912): at k ≤ 1 both stay inside the
  frame. Every inked atom must clear the silhouette envelope (never occlude him).
* Tightest non-block gutters (core px): REMOTE CONTROL box bottom (154) to the top
  tile (148) are x-disjoint (key ink 325..755, tile 824); key term to the switch plate
  46; phone to switch 160; switch to tile column 194; tiles to each other 24; checklist
  tile to text 64, text to box 64. Anything closer is inside a declared block
  (`SC.DECLARED_BLOCKS`, stamped `data-block`).

## 3. THE TIMELINE (`SC.CUE`, word starts from `cuts/ccremote/transcript_tight.json`)

| t | event |
|---|---|
| 0.40 | "one": the switch plate draws, ALONE and centred (LAW 19/20 hook) |
| 0.66 | "setting": screws, base plate and the lever appear, lever DOWN (off) |
| 3.20 | "Claude": the middle Claude Code tile drops in on the right |
| 4.68 | "phone.": the phone pops in on the left |
| 5.14 | "remote": **REMOTE CONTROL** written across the top (first type, 48 px, LAW 9) |
| 7.44 / 7.92 | "Claude" / "sessions": top and bottom session tiles drop in |
| 8.56 | "from": terracotta wire phone -> switch draws and stops at the switch |
| 10.10–11.62 | "not": the switch plate's outline flips terracotta (LAW 38 rule 2), back 11.62–11.86 |
| 11.24 | "default.": OFF BY DEFAULT under the switch |
| 12.40–13.30 | "Claude": the middle tile's border flips terracotta, back 13.30–13.54 |
| 13.38 | "change": OFF BY DEFAULT leaves; the lever flips UP (0.40 s, back.out) |
| 14.36 | "on": the tape slaps across the lever (rotation −18 -> −8, scale 1.3 -> 1) |
| 14.68 | "default,": ON BY DEFAULT under the switch |
| 16.20 | "new": three wires fan out switch -> tiles (stagger 0.12) |
| 19.90 | "phone.": three session rows slide into the phone (stagger 0.08) |
| 20.46–20.76 | "You": chapter 1 leaves (fade up 14 px) |
| 20.50 / 20.56 | the sticky note draws; TURN / IT / ON written on it |
| 20.80 / 21.14 / 21.48 | "never" / "ever" / "ever": one terracotta strike per word |
| 25.60–25.90 | "Claude": the note leaves as checklist row 1's tile drops in (25.64) |
| 26.52 / 26.62 | "ask": ASK IT TO TURN IT ON, then its box |
| 27.26 | "on,": the tick draws, the box border flips terracotta |
| 28.30 / 28.40 / 28.50 | "keep": row 2 tile (drawn phone), WORK FROM YOUR PHONE, its box |
| 29.22 | "phone": the tick draws, the box border flips terracotta |
| 30.64 | "Now,": opaque rising sheet (0.46 s); board cleared 31.12; outro switch glyph 31.14, rule 31.44, lockup 31.54 |

Beat edges `SC.BEAT_EDGES`; chapters `SC.CHAPTERS` / `SC.BOARD_CHAPTERS`; `SC.DUR = 34.92`.

## 4. THE BESPOKE OBJECTS (`SC.BESPOKE`, core boxes, held instants)

| i | name | t | core box | own-eyes check at 405x720 |
|---|---|---|---|---|
| 0 | wall light switch | 2.60 | 450, 200, 630, 480 | `review/proof_ccremote/00.png`: a wall toggle switch plate, two slotted screws, lever down |
| 1 | taped light switch | 15.30 | 450, 200, 630, 480 | `01.png`: the same switch, lever up, a strip of tape with torn ends holding it |
| 2 | crossed-out sticky note | 22.60 | 400, 150, 680, 430 | `02.png`: a square note with a folded corner, TURN IT ON, each word struck through in terracotta |

`SC.UI_OBJECTS`: the smartphone (`03.png`, t 20.30, core 110, 170, 290, 510) is UI
chrome, not a bespoke object (A SCREEN IS NOT AN OBJECT). None of the three bespoke
objects is on the refused UI-glyph list (cylinder, gear, bell, magnifier); the switch is
a physical wall plate with a lever, not a settings gear or a UI toggle pill. Map `core`
through your own k/origin for any crop.

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 39 / 50**: `data-label-for="sw"` on OFF BY DEFAULT and ON BY DEFAULT; both sit
  BELOW the plate in the same seat (`SC.SW_KEY_BOX`), centred on x = 540, 28 px / 44 px
  row. REMOTE CONTROL is the key term (no `data-label-for`).
* **LAW 40 / connectors touch what they join**: four wires in `#wires` (`data-overlap-ok
  data-connector`), each path with `data-connect-to`: `wire-in` -> `sw`, `wire-tile-top`
  / `wire-tile-mid` / `wire-tile-bot` -> their tiles. Ends (`SC.CONNECTORS`):
  phone right edge (290, 340) -> plate outer left edge (450, 340); plate outer right edge
  `anchor_points(SC.SW_BOX, 3, "right")` = (630, 244.8 / 340 / 435.2) -> tile outer left
  edges (824, 204 / 340 / 476). Butt caps, measured in the DOM by the proof harness:
  **0.0 px gap at all eight ends**, every end on a straight edge segment clear of the
  corner radius (`proofs.json -> connectors`). At a cutout k the wires scale with the
  core, so they still touch.
* **LAW 41**: `data-block` = `sw` (plate, screws, lever, tape, both labels), `phone`
  (with its rows), `tiles` (the three tiles, an identical series), `note` (edge, fold,
  words, strikes), `step1`, `step2`.
* **LAW 42 / 43**: chapters; every mark leaves with its chapter (`SC.LIFETIMES`). The
  circuit is on screen 58 % of the take and carries a finite exit (20.76). Only the
  outro atoms carry `data-anchor="1"`.
* **LAW 38**: border flips on DRAWN objects only: `#sw-plate` stroke (10.10), `#tile-mid`
  borderColor (12.40), `#step1-box` / `#step2-box` borderColor (at their ticks). No
  ring, ellipse, circle tag or highlight; screws, knob, pivot and outro screws are
  two-arc paths.
* **LAW 45**: seam 1 hands over to the note (outline + TURN IT ON complete by 20.90);
  seam 2 hands over to row 1's Claude Code tile (complete 25.98).
* **LAW 51**: the lever rotates and the tape scales/rotates about their own `svgOrigin`
  (set by the module's own tweens: pivot 110 160, tape centre 110 138 in the switch
  svg); do not re-tween them in a lane.
* **Ghost rule**: plate, screws, note edge/fold, wires and ticks declare
  `pathLength="100"`, rest at stroke-opacity 0 and reveal one frame after the draw starts.

## 6. THE POINTING CUE

None (`gen/_cues_ccremote.json`, `cues: []`). Nothing to raise, nothing to waive.

## 7. CAPTIONS (all three lanes)

The tight transcript is clean; "Claude Code" is spelled as spoken everywhere. The
sentence at 12.00 reads "By using Claude Code, you can change it" (as spoken).

## 8. WHAT THE CUTOUT OWNS

* The matte: at seal time `plate` ok (crop 2600x1800+450+270, scale_k 0.5, head
  449.9 px, overwide_applied true, face_dx_pct 0.053), `prompt0` ok with
  `wing_review: true` (instrument abstained, removed_px 0; look at
  `matting/ccremote/prompts/kf_overlay_00000.png`), `selection` ok (inputs ready for the
  outline review), `track` **skipped** (backend matanyone2); the ship marker had not
  landed. The Astra matte step owns the review and the track. `plate_origin()` reads
  `left` from `plate_box` (plate is OVER-WIDE).
* `SC.CUTOUT_LOGO_LANES = ("claude", "codex", "cursor", "copilot", "opencode",
  "antigravity", "warp")` with files in `SC.CUTOUT_LANE_FILES`; all resolve
  (proofs.json). Excluded on purpose: `claude-code` (on stage). Lanes fade in once the
  hook has landed.
* Your own k and top per section 2.

## 9. THE WHITEBOARD

Does not import this module. Redraws the same argument per the plan's
`whiteboard_version` fields: the switch alone (lever down), the Claude Code mark right,
the phone left; REMOTE CONTROL first type across the top; two more marks; the wire phone
-> switch; plate retraced terracotta on "not", OFF BY DEFAULT; the lever redrawn up, the
tape, ON BY DEFAULT; three wires to the marks, rows sketched into the phone; erase; the
sticky note, TURN IT ON, one strike per "ever"; erase (carry the note until row 1's mark
lands); the two checklist rows ticked on "on" and "phone".

## 10. DEPARTURES FROM THE PLAN'S LETTER

None of substance. The plan's normalised `bbox` values were updated to the drawn boxes;
`SC.BESPOKE` core boxes are authoritative.

## 11. PROOF EVIDENCE

`review/proof_ccremote/`: `00.png`, `01.png`, `02.png` (bespoke crops at 405x720 scale),
`03.png` (the UI phone), `*_x4.png` (the same crops enlarged for the author's eyes),
`frame_*.png` / `frame_*_phone.png` (nineteen composed frames 0.80 to 32.50 s),
`sheet.png` (contact sheet of the top zone), `proofs.json` (boxes, connector gaps, mark
resolution, fan anchor points).
