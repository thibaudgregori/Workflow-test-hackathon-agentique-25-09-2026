# geminigems — SHARED LANE SCENE HANDOFF

**Written by the PLAN + ARTWORK author for the SPLIT and CUTOUT authors.** The
plan is the contract (`plans/geminigems_plan.json`); this file is the
convenience. If anything below disagrees with the plan, the plan wins and you
write your own note. Section 9 lists the places this module departs from the
plan's letter, with the reason for each.

Neither lane redraws anything in this module. The scene is sealed
(`review/artwork_pass_geminigems.json`); a lane that needs a change takes
`production.py scene-lock`, redraws, re-reads cold over three rounds and
re-seals.

---

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/geminigems_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import geminigems_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_geminigems_proof.py` (`--set seal`, `--set compose`) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the WHOLE 20.92 s scene: html to drop inside one
`transform: scale(k)` wrapper, and a list of `tl.*` javascript strings to
concatenate into your own timeline tail. It authors nothing outside the core, it
reads no files, and it takes no format argument — every difference between the
two formats is in the PLACEMENT and in the `lockup` string. It calls
`SC.assert_anchor_law()` before it writes a byte.

It emits 19 identified elements and 64 tweens. The eases it names are the
chassis' own: `SOFT`, `POP`, `SWING`.

### `media` — the two rasters the scene paints

```python
{"_gemini_img": CC.mark_img(LOGO_URL["gemini"], "gemini", SC.MARK_SIDE["gemini"]),  # 74.0
 "_claude_img": CC.mark_img(LOGO_URL["claude"], "claude", SC.MARK_SIDE["claude"])}  # 74.0
```

`CC.MARK_INK[key]` must be populated by `CC.measure_mark(key, src)` first, and
the `LOGO_URL` values must be page-relative (`assets/logos/<basename>`). The
sizes are **ink sides in CORE px** — do not rescale them for the cutout; the
core's own `scale(k)` carries them.

**THE FILES ARE NAMED, NOT GUESSED** (`SC.LOGO_FILES`, MARK IDENTITY):
`ai-models/gemini-color.png` is the product mark for Gemini;
`ai-models/claude-color.png` is Anthropic's PRODUCT mark and takes precedence
over the `anthropic-wordmark` company lockup (LAW 35). It is never
`claude-code`, never the white-outlined `claude-code-sticker`, and never
`claude-cowork`.

There are no other assets. **There is no source post, no screenshot and no
raster of any kind in this video** — `pointing_cues.py` returned zero cues — so
there is nothing to copy next to your page.

### `lockup` — the outro's handle block

```python
CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W) \
  + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W)
```

Seated inside the scene's own `#o-slot`. `handle_key` is the ONLY string that
differs between the masters: `"yt"` on the split, `"tiktok_ig"` on the cutout.

---

## 2. THE UNITS

**CORE px = the plan's CANVAS px with y shifted by −192.**

```
canvas_y = core_y + SC.CANVAS_OFFSET      # 192.0
canvas_x = core_x                          # every core x survives verbatim
```

* `SC.CORE_W, SC.CORE_H = 1080.0, 600.0`
* `SC.CONTENT_Y0, SC.CONTENT_Y1 = 80.0, 568.0` — the band the core DECLARES it
  paints in (canvas 272 … 760). Y0 is the chapter-2 parcel's box top, Y1 is the
  `SUNSET OCT 20` key's box bottom in chapter 0. Both are REAL painted ink.
  Canvas 272 is 14.2 % of frame height, clear of LAW 30's top-10 % line; canvas
  760 is 39.6 %, and the caption pill's own top sits at ~787.7 (seat centre
  ~44 %, pill height 114.59), so the lowest ink clears the pill by ~28 px.
  The outro composition also lives inside this band: the outro gem's top is core
  84 and the lockup slot's bottom is core 500.
* The composition **is symmetric about x = 540** in every chapter: chapter 0 is
  one centred stack (gem centre 540, tile centre 540, both keys centred 540);
  chapter 1's ink extents are 160 … 920 for an optical axis of 540.0; chapter
  2's are 135 … 945, again 540.0. So `left = (1080 − 1080·k) / 2`.
* Seat the core so its CONTENT BAND — not its box — is centred on your stage
  zone's centre:
  ```python
  top = round(centre - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 * k, 2)
  ```

**GATE-SCALING.** The cutout scales the core by ~0.95, so a 45 core-px gutter
arrives as ~43 canvas px. Every non-block gutter in this scene is authored at
**≥ 20 CORE px** and the tight ones are listed here so you can check them after
your own scale: gem-to-arrow 20 (chapter 1); parcel-to-trio and parcel-to-crowd
45 (chapter 2); trio-to-`SKILLS` key 113. Every gap smaller than that is inside
a DECLARED block (`SC.DECLARED_BLOCKS`), where Gate 1's cramp check does not
bind.

---

## 3. THE TIMELINE

`SC.CUE` carries every instant, and each one is a word START from
`cuts/geminigems/transcript_tight.json` unless its comment says `authored`; an
authored cue sits inside its word's 1.0 s LABEL_WINDOW. `SC.BEAT_EDGES` is the
plan's own beat table. `SC.DUR = 20.92`, the cut master.

Four chapters, `SC.BOARD_MODE = "chapters"`, `SC.BOARD_CHAPTERS`:

| ch | t | what is on screen |
|---|---|---|
| 0 | 0.12–5.52 | the gem alone on the axis (0.30), the crack on "killed" (0.52), the Gemini tile above it (2.94), `GEMINI GEMS` (3.32), `SUNSET OCT 20` (5.10) |
| 1 | 5.52–10.46 | the gem and its tile travel left; the terracotta arrow draws on "replaced" (6.40); the parcel lands on "Skills" (7.16) with the Claude tile and `SKILLS`; the tile's border flips terracotta 8.26–10.62; the lid tilts open on "sharing" (9.08) |
| 2 | 10.46–17.52 | the parcel and its key travel to the axis and up; two terracotta connectors (10.90); the pair (11.14) and `TEAMMATES` (11.56); the crowd (12.86) and `COMMUNITY` (13.32). Beat 5's call to action adds NO ink and holds this frame |
| 3 | 17.52–20.92 | the opaque rising sheet (17.52), the small open parcel (18.05), the gem dropping into it on "migrate" (18.68), the terracotta rule (19.30), the lockup (19.45) |

**Every erase is a HANDOVER, never a blank** (LAW 43's zero-ink clause): at 5.52
the two keys fade over 0.22 s while the gem and its tile are ALREADY travelling
left; at 10.46 the gem, the Gemini tile, the arrow AND the Claude tile fade
(the script turns off whose standard Skills is and onto who you hand it to, so
no third-party mark survives the seam) while the parcel and its key are already
travelling to the axis. The last board ink is `COMMUNITY`, finishing
at 13.60 — 3.92 s before the outro anchor — so nothing is authored at or after
the wipe.

---

## 4. THE FOUR BESPOKE OBJECTS — SEALED, DO NOT REDRAW

`SC.BESPOKE` carries the boxes in CORE coordinates and the held instant of each.
Twelve independent reads across three concurrent rounds
(`review/phone_reader_geminigems_artwork_r{1,2,3}.json`), **zero readers naming
a different object**.

| i | object | t | core box | cold reads (3 independent rounds) |
|---|---|---|---|---|
| 0 | cracked gem | 2.00 | 410, 230, 670, 445 | "diamond" ×3, all **sure** |
| 1 | tied parcel | 8.60 | 660, 230, 920, 445 | "gift box" ×3, all **sure** |
| 2 | two people together | 12.00 | 135, 318, 365, 508 | "two people icon" / "two people" / "Two people icon" ×3, all hedged |
| 3 | a crowd of people | 14.60 | 715, 318, 945, 508 | "group of people icon" ×3, all hedged |

Objects 2 and 3 are **hedged passes** and are routed, not refused (the
2026-09-08 ruling): three of three readers reached the intended noun and none
named a different one; what they hedged on is whether a drawn person answers the
prompt's "everyday object" premise. **The clerk must adjudicate both on the
delivered render**, where each carries its own key and lands on the word being
spoken.

One frame-normalised box cannot be right for both formats — the box is a
consequence of the placement — so map `SC.BESPOKE[i]["core"]` through your own k
and origin when you cut phone crops.

**The seal is bound to the CURRENT module.** After the outro constants were
reseated, all four seal crops were re-rendered from the module as it stands and
are byte-identical (sha256) to the crops the readers saw. Nothing on the board
changed after the reads.

---

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 40** — `SC.A_PARCEL = anchor_points(SC.PARCEL_BOX, 1, "left")` =
  (660.0, 337.5); `SC.A_TRIO = anchor_points(SC.TRIO_BOX, 1, "top")` =
  (250.0, 318.0); `SC.A_CROWD = anchor_points(SC.CROWD_BOX, 1, "top")` =
  (830.0, 318.0). The two fan-out ends are level to 0.0 px and mirror-symmetric
  about x = 540; `SC.assert_anchor_law()` proves it and runs inside `build()`.
  The three connectors carry `data-connect-to` and `data-overlap-ok`. Do not
  hand-place an end.
* **LAW 39 / LAW 50** — five keys, each with `data-label-for`, each entirely
  BELOW its host and centred on its axis to 0.0 px: `GEMINI GEMS` and
  `SUNSET OCT 20` below `gem`, `SKILLS` below `parcel`, `TEAMMATES` below
  `trio`, `COMMUNITY` below `crowd`. The two siblings in chapter 2 take the SAME
  placement, the SAME 176 px seat and the SAME baseline (`SC.KEY_ROW_Y = 520`).
* **LAW 41** — `SC.DECLARED_BLOCKS`, stamped as `data-block` in the DOM.
* **LAW 42** — `SC.LIFETIMES`. The board is CHAPTERED, so every mark carries a
  finite window except `SC.SCENE_ANCHORS`: the parcel is on screen 10.36 s of
  20.92 (49.5 %) and is DECLARED, with its key welded to it, plus the five
  outro marks.
* **LAW 38** — exactly ONE emphasis: the PANEL BORDER FLIP on `#claude-tile` at
  8.26, back at 10.32. No ring, no ellipse and no circle exists anywhere in this
  module, and **no `<circle>` tag is emitted at all** — even the heads in the
  two people drawings are two-arc `<path>`s (`SC._circle_path`). There is no
  marker highlight because there is no raster text in this video.
* **LAW 28 / LAW 51** — the parcel's lid and bow are ONE `<g class="pclid">` with
  `transform-origin: 16px 48px`. Wherever the parcel moves, its lid, bow, bands
  and tag move with it; when the lid opens, the bow opens with it. A lane that
  moves the box without them is a cross-lane parity defect. The `SKILLS` key
  travels with the parcel across the chapter-2 move as one block.
* **THE GHOST RULE** — every drawn path declares `pathLength="100"`, rests at
  `stroke-opacity: 0` and reveals one frame (0.04 s) after its draw starts, so
  the dash always equals the path's own declared length (the draw-on dash law).

---

## 6. THE POINTING CUE

There is none. `pipeline/pointing_cues.py --vid geminigems` printed *"no
pointing cue in this take"* and wrote `gen/_cues_geminigems.json` with
`"cues": []`. He cites nobody and points at nothing, so no source card is raised
and there is nothing to waive.

---

## 7. WHAT THE CUTOUT OWNS

* The matte, the wing review and the stage-zone seating — **only the `cut`
  marker existed at plan time** (`prep/stages/geminigems.cut.json`, status ok,
  58.7 s, cut master 20.92 s, tight audio 20.883 s), so the plate, prompt0,
  track, ship and cues markers had not landed: *wing review: prompt0 not landed
  at plan time — the cutout author owns it.*
* `SC.CUTOUT_LOGO_LANES = ("chatgpt", "grok", "perplexity", "copilot", "kimi",
  "deepseek")` — six assistant marks in the same category as the Gemini this
  short is about, mixed, none repeated, and deliberately excluding `gemini` and
  `claude` because those two are on the stage (GRAPHIC CHART clause 7).
* Your own k and origin, and `plate_origin()` must read `left` from
  `plate_box` — the plate is OVER-WIDE by default and its box is deliberately
  not centred.
* Beat 5 (14.18–17.52) adds no ink by design. If 3.3 s of a held stage zone is
  too static behind a moving silhouette, the sanctioned move is a
  behind-the-silhouette crossing of one lane mark, never new diagram ink.

## 8. WHAT THE WHITEBOARD DOES NOT DO

It does not import this module. It redraws the SAME argument in marker ink, with
the same objects, the same labels and the same key term, per beat
`whiteboard_version` in the plan. LAW 51 still binds: the parcel's lid and bow
move together there too, and the gem still travels into the parcel on "migrate".

---

## 9. WHERE THIS MODULE DEPARTS FROM THE PLAN'S LETTER

1. **The gem is not re-labelled in chapter 1.** The plan's chapter-1 picture
   leaves the gem un-named and this module does the same: the only word for it
   is "Gems", spoken at 3.32, and re-typing a key at 5.7 s would sit 2.2 s
   outside its own 1.0 s LABEL_WINDOW. The viewer has just seen the stone named
   and it is the same drawing.
2. **TEAMMATES is TWO figures, not three.** The plan says "two people standing
   shoulder to shoulder"; an earlier sketch had three. At 86 × 71 phone px three
   figures in a 230 px box are 24 px wide each and collapse into a comb. Two
   read as two people at that size, and the contrast with the seven-figure crowd
   opposite is what the beat needs.
3. **The outro composition was reseated after the seal.** `OGLYPH`, `OGEM`,
   `ORULE_Y` and `OSLOT_TOP` moved down so the outro's own ink stays inside the
   declared content band (the gem's top is core 84, the slot's bottom core 500).
   No board geometry and no bespoke drawing changed; the four seal crops
   re-render byte-identical.
4. **The plan's `bbox` values are normalised canvas boxes written before the
   drawings existed.** `SC.BESPOKE` carries the real CORE boxes and is
   authoritative for geometry.

---

## 10. PROOF EVIDENCE

| what | where |
|---|---|
| phone-size seal crops (405×720 scale) | `review/proofs/crop_seal_0{0..3}_*.png` |
| the frames they were cut from | `review/proofs/frame_seal_0{0..3}.png` |
| crop manifest (boxes, norm boxes, phone sizes) | `review/proofs/proofs_seal.json` |
| three concurrent cold-read rounds | `review/phone_reader_geminigems_artwork_r{1,2,3}.json` |
| blind reader folders | `review/cold/round_r{1,2,3}-*/` |
| the author's scoring | `review/artwork_scores_geminigems.json` |
| composed full frames (GRAPHIC CHART clause 9) | `review/proofs/compose_{ch0,ch1,ch2,outro}.png` and `*_phone.png` |
| the seal record | `review/artwork_pass_geminigems.json` |
