# eudisclosure — SHARED LANE SCENE HANDOFF

**From the design agent, for the SPLIT author and for the CUTOUT author.** The plan
(`plans/eudisclosure_plan.json`) is the contract. This file is a convenience. If the two
disagree, the plan wins. Neither lane redraws anything in this module. It is sealed
(`production.py seal`, production v4), and a lane that builds on a changed module is refused.

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/eudisclosure_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import eudisclosure_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_eudisclosure_proof.py` (renders the real timeline, crops, frames, sheet, stamp-press measurement) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the whole 27.64 s scene: html to drop inside ONE `transform: scale(k)`
wrapper (`transform-origin: 0 0`) and a list of `tl.*` strings to append to your own paused
GSAP timeline `tl`. It reads no files and takes no format argument. Eases are string
literals (`"power3.out"`, `"back.out(2.05)"`, `"power2.inOut"`, `"power2.in"`,
`"power3.in"`). The page must give `.abs{position:absolute}` and
`.mono{font-family:'JetBrains Mono';text-transform:uppercase}` (the chassis already do).

### `media`: none

This scene paints **no raster**. The script names no product and cites no post, so there is
no stage mark and no source card. Pass `{}`. `SC.LOGO_FILES` is empty on purpose.

### `lockup`

```python
CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W) \
  + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W)
```
It sits inside the scene's `#o-slot` (core top 250). `handle_key` is the only string that
differs between masters: `"yt"` on the split, `"tiktok_ig"` on the cutout.

## 2. THE UNITS

**CORE px = canvas px with y − 192** (`SC.CANVAS_OFFSET`); x is unchanged. Core is
`SC.CORE_W x SC.CORE_H = 1080 x 600`.

* Declared content band `SC.CONTENT_Y0, SC.CONTENT_Y1 = 96, 500` (canvas 288..692): the
  DISCLOSE key term's top to the flag pole's foot / the Polaroids' bottom edge. That is
  about 95 px above the split's caption pill top (~787.7).
* Every chapter is **mirror-symmetric about x = 540**: the two seats are x 138..408 and
  672..942 (`SC.L_X`, `SC.R_X`, 270 wide), and the stamp's rest seat is 440..640. A lone
  object starts centred at 405..675 and slides into the left seat (LAW 19).
* **Cutout seating:** `left = (1080 − 1080·k) / 2`,
  `top = round(stage_centre − (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 · k, 2)`, with k taken from
  YOUR matte envelope so that the band (404·k tall) clears his crown. The widest extent is
  138..942 (804 px). At k ≤ 1 it stays inside the frame. Every inked atom must clear the
  silhouette envelope.
* Tightest non-block gutters (core px): DISCLOSE box bottom (154) to a Polaroid/flag top
  (180/165) = 26 / 11 but x-disjoint for the flag finial (key ink 418..662, finial 396..418);
  stamp at rest to the Polaroids 32 each side; to the chat bubble 42, to the page 52. The
  stamp overlaps its target only while pressing (`data-overlap-ok`).

## 3. THE TIMELINE (`SC.CUE`, word starts from `cuts/eudisclosure/transcript_tight.json`)

| t | event |
|---|---|
| 0.44–1.30 | "in Europe": pole, flag field, then the twelve terracotta stars pop one by one (the hook, alone and centred) |
| 1.48 | "disclose": **DISCLOSE** across the top (first type, 48 px, LAW 9). It is the anchor and stays until the outro sheet |
| 3.62 | the flag leaves |
| 3.96 | "chatbot": the chat bubble pops in, centred |
| 4.98 | "AI": the bubble slides left; 5.08 the text page draws on the right |
| 5.20 | "generated": the stamp drops into its rest seat |
| 5.66 / 6.26 | "content" / "And": the stamp presses. AI is printed in the bubble, then on the page |
| 6.80 | chapter B leaves (bubble, page, stamp) |
| 7.16 | "AI generated images": a Polaroid drawn in terracotta ink, centred |
| 9.74 | "because": it slides left |
| 10.36 | "say": the stamp drops in; 10.94 "image": the ink Polaroid with a terracotta sun draws on the right |
| 11.46 / 12.80 | "AI" / "AI": AI GENERATED printed on the left strip, AI MODIFIED on the right strip |
| 13.98 | "So": chapter C leaves |
| 14.94 | "real": the all-ink Polaroid, centred; 16.18 it slides left; 16.28 the screenshot window drops in on the right |
| 20.30 | "color": the photo's sun and the screenshot's picture turn terracotta |
| 20.90 | "lighting": eight terracotta rays draw around the sun |
| 21.62 | "you": the stamp drops in |
| 22.64 / 23.10 | "disclose" / "that": AI MODIFIED printed on the photo strip, then on the screenshot footer (the stamp goes straight from one to the other) |
| 23.32 | "Now": the opaque cream sheet rises (0.46 s). Small stamp glyph 23.82, rule 24.12, lockup 24.22 |

At every press the pad lands on its imprint on the spoken word. The contact is the tween end,
and the imprint pops at the same instant (`proofs.json -> presses`: pad centre within 0.1 px
of the imprint centre).

## 4. THE BESPOKE OBJECTS (`SC.BESPOKE`, core boxes at held instants)

| crop | name | t | core box |
|---|---|---|---|
| `00.png` | European Union flag | 1.60 | 396, 165, 684, 505 |
| `01.png` | AI rubber stamp | 11.05 | 430, 186, 650, 368 |
| `02.png` | two stamped Polaroids | 13.60 | 138, 180, 942, 500 |
| `03.png` | stamped Polaroid photo | 23.28 | 138, 180, 408, 500 |

The UI objects (`SC.UI_OBJECTS`, chrome, not bespoke): chat bubble `04.png`, text page
`05.png`, screenshot window `06.png`. None of the bespoke silhouettes is on the refused
UI-glyph list (cylinder, gear, bell, magnifier). The flag is identified by its twelve-star
ring, the stamp by its knob, block and pad. Map `core` through your own k and origin for any crop.

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 39 / 50**: no free labels. DISCLOSE is a title with no host. Every imprint is a
  CHILD element of its object (`#imp-bub` in `#bubble`, `#imp-page` in `#page`,
  `#imp-pd-gen|mod|real` in their Polaroids, `#imp-shot` in `#shot`). All imprints share
  one size (24 px mono 800, 4 px terracotta box), one rotation (−2.5°) and one seat per
  kind (centred on the host axis, on the strip or footer at local y 280). Measured inside
  the host with margins ≥ 15 px (`proofs.json -> imprint_in_host`).
* **LAW 40 / connectors**: none. Nothing is joined by a line.
* **LAW 41**: `data-block` = `flag`, `bubble`, `page`, `pd-gen`, `pd-mod`, `pd-real`
  (with its rays), `shot`, `stamp`. `#stamp` also carries `data-overlap-ok` (it presses
  onto its target) and `z-index: 5`. The outro atoms carry `z-index: 9` over the sheet (8).
* **LAW 42 / 43**: four chapters. Every mark leaves with its chapter (`SC.LIFETIMES`). Only
  `#key-disclose` and the outro atoms carry `data-anchor="1"`.
* **LAW 38**: there is no emphasis stroke. No ring, ellipse, circle tag or highlight is
  used. The finial, knob, dots and suns are two-arc paths, and the stars are paths.
* **LAW 51**: the stamp is ONE element moved by the module's own x/y tweens, and each imprint
  moves with its host because it is the host's child. Do not re-tween them in a lane.
* **Ghost rule**: the flag pole and field, the bubble edge, the page edge and fold, the
  Polaroid frame, window, mountains and sun, the screenshot frame and rules, and the rays all
  declare `pathLength="100"`, rest at stroke-opacity 0 and reveal one frame after the draw starts.

## 6. THE POINTING CUE

None (`gen/_cues_eudisclosure.json`, `cues: []`). There is nothing to raise and nothing to waive.

## 7. CAPTIONS (all three lanes)

The tight transcript is clean (keep_words [[113, 212]]). No date is spoken, so none is shown.

## 8. WHAT THE CUTOUT OWNS

* The matte. At seal time only the `cut` marker had landed (ok, 60.3 s wall, master
  27.64 s, model-authored keep ranges). Plate, prompt0, track and ship had not landed.
  **Wing review: prompt0 had not landed at plan time, so the cutout author owns it.** The Astra
  matte step owns the review and the track. `plate_origin()` reads `left` from `plate_box`
  (the plate is OVER-WIDE).
* `SC.CUTOUT_LOGO_LANES = ("chatgpt", "claude", "gemini", "mistral", "grok",
  "perplexity", "flux", "midjourney")` with the files in `SC.CUTOUT_LANE_FILES`. All of them
  resolve (`proofs.json -> cutout_lanes_resolve`). They are the chatbots the rule covers
  (Mistral as the European one) and the image generators whose output must be labelled.
  The lanes fade in once the hook has landed.
* Your own k and top, per section 2.

## 9. THE WHITEBOARD

The whiteboard does not import this module. It redraws the same argument from the plan's
`whiteboard_version` fields, in this order:

1. The flag alone with its star ring, then DISCLOSE written across the top (DISCLOSE is a board anchor).
2. Erase. The chat bubble and the page, a small stamp between them, and a boxed AI written inside each.
3. Erase. A Polaroid drawn in terracotta, then a second one in ink with a terracotta sun, with AI GENERATED and AI MODIFIED written on their strips.
4. Erase. An all-ink Polaroid and a screenshot window. The sun is re-inked terracotta and its rays drawn, then AI MODIFIED is written on both.
5. The rising-sheet outro with a small stamp.

## 10. DEPARTURES FROM THE PLAN'S LETTER

None of substance. The plan's normalised `bbox` values were updated to the drawn boxes, and
the `SC.BESPOKE` core boxes are authoritative.

## 11. PROOF EVIDENCE

`review/proof_eudisclosure/` contains:

* `00.png` to `03.png`: the bespoke crops at 405x720 scale.
* `04.png` to `06.png`: the UI crops.
* `*_x4.png`: the same crops enlarged.
* `frame_*.png` / `frame_*_phone.png`: twenty composed frames from 0.80 s to 25.00 s.
* `sheet.png`: a contact sheet of the top zone.
* `proofs.json`: the stamp presses, imprint containment and lane resolution.
