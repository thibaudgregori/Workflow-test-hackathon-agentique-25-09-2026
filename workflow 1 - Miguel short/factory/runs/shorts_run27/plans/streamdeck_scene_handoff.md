# streamdeck — SHARED LANE SCENE HANDOFF

**From the design agent, for the SPLIT author and for the CUTOUT author.** The plan
(`plans/streamdeck_plan.json`) is the contract; this file is the convenience. If
they disagree, the plan wins. Neither lane redraws anything in this module: it is
sealed (`production.py seal`, production v4), and a lane that builds on a changed
module is refused.

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/streamdeck_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import streamdeck_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_streamdeck_proof.py` (renders the real timeline, crops, frames, sheet, connector measurements) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the whole 30.48 s scene: html to drop inside ONE
`transform: scale(k)` wrapper (`transform-origin: 0 0`) and a list of `tl.*`
strings to append to your own paused GSAP timeline `tl`. It reads no files and
takes no format argument. **Eases are emitted as string literals**
(`"power3.out"`, `"back.out(2.05)"`, `"power2.inOut"`, `"power2.in"`), so the page
needs no SWING/EXIT constants. The page must give `.abs{position:absolute}` and
`.mono{font-family:'JetBrains Mono';text-transform:uppercase}` (the chassis already do).

### `media`: four rasters (two files)

```python
for key, rel in SC.LOGO_FILES.items():            # relative to ~/Documents/Workspace/assets/logos
    CC.MARK_INK[key] = CC.measure_mark(key, LOGOS / rel)
media = {
  "_claude_key_img":    CC.mark_img(<claude src>,      "claude",      SC.MARK_SIDE["key"]),     # 46
  "_cc_tile_img":       CC.mark_img(<claude-code src>, "claude-code", SC.MARK_SIDE["tile"]),    # 64
  "_cc_torch_img":      CC.mark_img(<claude-code src>, "claude-code", SC.MARK_SIDE["torch"]),   # 44
  "_claude_prompt_img": CC.mark_img(<claude src>,      "claude",      SC.MARK_SIDE["prompt"]),  # 36
}
```

Files (MARK IDENTITY, named, never guessed): `claude` ai-models/claude-color.png (the
orange Claude mark: he says "accessory for Claude"); `claude-code`
coding-tools/claudecode-color.png (the plain no-outline mascot; NEVER
coding-tools/claude-code.png, the sticker). Both pass
`cutout_depthfield.assert_cast_resolves` (`review/proof_streamdeck/proofs.json`).
The Stream Deck is DRAWN (the keypad): the registry holds no Elgato/Stream Deck
mark. There is no source post or screenshot: `pointing_cues.py` returned 0 cues.

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

* Declared content band `SC.CONTENT_Y0, SC.CONTENT_Y1 = 96, 514` (canvas 288..706):
  the beam's top edge / the mini devices to EVERY DEVICE's box bottom. Lowest ink per
  chapter: keypad + STREAM DECK 447, flashlight scene 514 (label box), mapping 513
  (keypad body with stroke), button 492 (ONE CLICK). Clears LAW 30's top 10 % and
  sits ~80 px above the split's caption pill top (~787.7).
* Chapter 1 opens centred on x = 540 and the keypad slides +131 on "Claude Code";
  the finished group (tile 235..347, cable, keypad 497..845) spans 235..845, centre 540.
  Chapter 2's flashlight opens centred (400..680) and slides −356; the whole
  flashlight + beam object spans 40..~1063. Chapters 3 is centred on 540. Chapter 4
  opens centred (prompt 345..735) and ends as prompt 110..500 + key 720..970 (centre 540).
* **Cutout seating:** `left = (1080 − 1080·k) / 2`,
  `top = round(stage_centre − (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 · k, 2)`, with k
  from YOUR matte envelope so the band (418·k tall) clears his crown. The beam
  chapter is the widest (x 40..~1063): at k < 1 it stays inside the frame. Every
  inked atom must clear the silhouette envelope (never occlude him).
* Tightest non-block gutters (core px): STREAM DECK to the keypad body 28; ONE CLICK
  to the key base 28; mini fridge to mini TV 36; bulb to fridge in the beam 100.
  Anything closer is inside a declared block (`SC.DECLARED_BLOCKS`, stamped `data-block`).

## 3. THE TIMELINE (`SC.CUE`, word starts from `cuts/streamdeck/transcript_tight.json`)

| t | event |
|---|---|
| 0.12 | "The": the six-key keypad draws ALONE and centred (LAW 19/20 hook) |
| 0.44–1.09 | "accessory for Claude": a Claude mark pops onto each keycap in turn (sixth on "Claude" 1.00) |
| 1.90 | **STREAM DECK** written under it (first type, 48 px, LAW 9) |
| 3.30 | "Claude": keypad + name slide right 131 px (LAW 19 displacement) |
| 3.62 | "Code": the Claude Code tile lands on the left |
| 4.70 | "combination": the terracotta cable draws tile -> keypad |
| 5.90–6.20 | chapter 1 leaves (fade up 14 px) |
| 6.08 | "you": the flashlight draws, centred |
| 7.26 | "Claude": the Claude Code mark pops onto its handle |
| 8.80 | "look": the flashlight slides left; 9.10 the beam opens |
| 9.82 / 10.24 / 10.52 | "every" / "single" / "connected": bulb, fridge, TV draw inside the beam |
| 10.94 | EVERY DEVICE written under the scene |
| 13.38 | "lights": the bulb's glass turns terracotta and five rays draw (it stays on) |
| 14.34–15.14 | "fridge": fridge outline flips terracotta and back |
| 15.04–15.84 | "anything": TV outline flips terracotta and back |
| 16.34–16.64 | chapter 2 leaves |
| 16.40 | the keypad returns, centred, lower, with its six Claude keys |
| 16.86 | "map": mini bulb, fridge, TV pop above it, one over each key column |
| 17.72 | "actions": three terracotta arrows draw down onto the keypad's top edge |
| 19.50 | "directly": the top-row Claude marks give way to the bulb, fridge, TV |
| 21.16 | "buttons": the keypad body's outline flips terracotta |
| 21.78–22.08 | chapter 3 leaves |
| 21.84 | the prompt window pops, centred (Claude mark in its header) |
| 23.70 | "telling": four text lines type in, 0.26 s apart |
| 25.14 | "Literally": the window slides left to 38 % opacity; the big key lands at 25.20 |
| 25.68 | "clicking": the cap drops 14 px, its border flips terracotta, the bulb lights |
| 25.80 | ONE CLICK written under the key |
| 26.52 | "Now": opaque rising sheet (0.46 s); board cleared 27.00; outro keypad 27.02, rule 27.32, lockup 27.42 |

Beat edges `SC.BEAT_EDGES`; chapters `SC.CHAPTERS` / `SC.BOARD_CHAPTERS`; `SC.DUR = 30.48`.

## 4. THE BESPOKE OBJECTS (`SC.BESPOKE`, core boxes, held instants)

| i | name | t | core box | own-eyes check at 405x720 |
|---|---|---|---|---|
| 0 | Claude button keypad | 2.60 | 350, 96, 730, 452 | `review/proof_streamdeck/00.png`: a six-key button pad, a Claude mark on every keycap, STREAM DECK under it |
| 1 | flashlight finding devices | 14.10 | 40, 96, 1080, 514 | `01.png`: a flashlight whose beam holds a lit bulb, a fridge and a TV |
| 2 | devices wired to keypad | 20.90 | 350, 100, 730, 522 | `02.png`: three small devices, arrows down onto the pad, the devices on the top keys |
| 3 | pressed light button | 26.30 | 665, 190, 1025, 492 | `03.png`: one big key on its base, terracotta, a lit bulb on it, ONE CLICK |

`SC.UI_OBJECTS`: the prompt window (`04.png`, t 24.95) is UI chrome, not a bespoke
object. The first draft gave the keypad a trapezoid foot and it read as a monitor on
a stand; it was redrawn as a flat pad with keycaps (a skirt and a top face per key).
None of the objects is on the refused UI-glyph list (cylinder, gear, bell,
magnifier). Map `core` through your own k/origin for any crop.

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 39 / 50**: `data-label-for` on STREAM DECK (→ `deck1`), EVERY DEVICE
  (→ `scan`), ONE CLICK (→ `bigkey`). All sit BELOW; the two plain labels share
  28 px / 44 px row.
* **LAW 40 + CONNECTORS TOUCH WHAT THEY CONNECT** (`SC.CONNECTORS`, measured in
  `proofs.json` -> `connectors`, and enlarged in `review/proof_streamdeck/_joins_x3.png`):
  the cable (`#cable`, `data-connect-to="deck1"`) runs from x 345.5 (inside the tile's
  3 px border, 344..347) to x 497 (the keypad body's left stroke centre after the
  slide) at y 233, butt caps, so no gap and no overshoot. The three arrows
  (`#arrows`, `data-connect-to="deck2"`) start ON each mini device's base (bulb and
  fridge base y 196, the TV body's bottom edge y 190) and their heads' tips sit at
  y 257, the keypad body's top stroke outer edge, at
  `anchor_points(body, 3, "top", inset=SC.ANCHOR_INSET = 0.2069)` = 438 / 540 / 642:
  level, symmetric about 540 and each exactly over a key column.
* **LAW 41**: one `data-block` per chapter object (`deck1`, `scan`, `deck2`,
  `prompt`, `bigkey`), because Gate 1 compares `data-block` by equality.
  The cable and the arrows carry `data-overlap-ok` (they land on their targets).
* **LAW 42 / 43**: chapters; every mark leaves with its chapter (`SC.LIFETIMES`);
  only the outro atoms carry `data-anchor="1"`.
* **LAW 38**: four flips on DRAWN objects (`#fridge .fro` stroke, `#tv .tvvo`
  stroke, `#deck2 .d2b` stroke, `#bigcap` borderColor). No ring, ellipse, circle tag
  or highlight; the bulb's glass is a path. The bulb turning terracotta with rays at
  13.38 is a STATE (the light is on), not an emphasis, and it stays.
* **Ghost rule**: every drawn path declares `pathLength="100"`, rests at
  stroke-opacity 0 and reveals 0.04 s after its draw starts. Objects that enter
  whole (the chapter-3 keypad, the mini devices, the key glyphs, the big bulb) set
  their paths fully inked at t 0 inside a parent that is opacity 0 until it enters.
* **LAW 51**: the keypad is the same object in chapters 1 and 3 (same module
  function, same keycaps, same Claude marks); do not restyle it per lane.

## 6. THE POINTING CUE

None (`gen/_cues_streamdeck.json`, `cues: []`). Nothing to raise, nothing to waive.

## 7. CAPTIONS (all three lanes)

`transcript_tight.json` spells everything as spoken ("Claude Code", "Stream Deck").
No proper-noun correction is needed.

## 8. WHAT THE CUTOUT OWNS

* The matte: at design time `prompt0` landed with `wing_review: true` (instrument
  abstained, removed_px 0; look at `matting/streamdeck/prompts/kf_overlay_00000.png`);
  `track` and `ship` had not landed. The Astra matte step owns the review and the
  track. `plate_origin()` reads `left` from `plate_box` (plate is OVER-WIDE: crop
  2640x1800+494+264, scale_k 0.5, head 450.1 px, face_dx_pct −0.019).
* `SC.CUTOUT_LOGO_LANES = ("codex", "cursor", "openclaw", "hermes-agent", "chatgpt",
  "gemini", "mcp", "obs-studio")` with files in `SC.CUTOUT_LANE_FILES`; all resolve
  (proofs.json). Excluded on purpose: claude, claude-code (on stage). Lanes fade in
  once the hook has landed (after STREAM DECK, 1.90).
* Your own k and top per section 2.

## 9. THE WHITEBOARD

Does not import this module. Redraws the same argument per the plan's
`whiteboard_version` fields: the six-key pad, a Claude mark per key, STREAM DECK
(first type, alone); the pad shifts right, the Claude Code mark and a terracotta
cable; erase; the flashlight with the Claude Code mark, the beam, the bulb, fridge
and TV, EVERY DEVICE, rays on the bulb, terracotta retraces on fridge and TV; erase;
the pad again, three small devices, three arrows onto its top edge, the devices
redrawn in the top keys; erase; the prompt window with scribbled lines, the big key
on its base, pressed (retraced lower in terracotta) with a lit bulb, ONE CLICK.

## 10. DEPARTURES FROM THE PLAN'S LETTER

None. The plan's keypad bbox, beat-0 picture and how_drawn were updated to the
flat keycap pad after the first proof (section 4); `SC.BESPOKE` core boxes and the
plan's normalised boxes describe the same drawing.

## 11. PROOF EVIDENCE

`review/proof_streamdeck/`: `00.png`–`03.png` (bespoke crops at 405x720 scale),
`04.png` (the UI prompt window), `*_x4.png` (the same crops enlarged for the
author's eyes), `frame_*.png` / `frame_*_phone.png` (seventeen composed frames
1.30 to 28.50 s), `sheet.png` (contact sheet of the top zone), `_joins_x3.png`
(the cable and arrow joins enlarged), `proofs.json` (boxes, connector measurements,
mark resolution).
