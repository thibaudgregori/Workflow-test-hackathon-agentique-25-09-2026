# claudeconcise — SHARED LANE SCENE HANDOFF

**Written by the design agent (plan + artwork) for the SPLIT and CUTOUT authors.**
The plan is the contract (`plans/claudeconcise_plan.json`); this file is the
convenience. If anything below disagrees with the plan, the plan wins and you
write your own note. Section 9 lists where the module departs from the plan's
letter.

Neither lane redraws anything in this module. It is sealed by
`production.py seal` (`review/artwork_pass_claudeconcise.json`, module + handoff
hashes); a lane that needs a change writes a note, it does not edit the module.

---

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/claudeconcise_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import claudeconcise_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_claudeconcise_proof.py --out <run>/review/proof_claudeconcise` (seeks the REAL timeline in Chromium) |
| proofs | `<run>/review/proof_claudeconcise/` (`00-03.png`, `00-03_tight.png`, `frame_*.png`, `proofs.json`) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the whole 41.774 s scene: html to drop inside ONE
`transform: scale(k)` wrapper (`transform-origin: 0 0`, static), and a list of
`tl.*` javascript strings for your timeline. It reads no files and takes no
format argument.

**EASES the tweens reference — your page must define all three:**
`const POP="back.out(2.05)"; const SOFT="power3.out"; const SWING="power2.inOut";`
(`cutout_core.page()` defines only POP/SOFT/EXIT: add SWING.) Other eases are
emitted as quoted GSAP strings (`"power1.inOut"`, `"power2.in"`).

**The page must load JetBrains Mono 800** (the dial prints `CONCISE` in an SVG
`<text>` with `font-family="JetBrains Mono, monospace"`), and a `.mono` class
(`font-family:'JetBrains Mono'; text-transform:uppercase`) for the labels.

**Proof-harness gotcha:** evaluate `"tl.seek(t); 0"`, never `"tl.seek(t)"`
(Playwright hangs serialising the Timeline).

### `media` — the two rasters the scene paints

```python
key = "claude-code"
src = LOGOS / SC.LOGO_FILES[key]                       # coding-tools/claudecode-color.png
CC.MARK_INK[key] = CC.measure_mark(key, src)
media["_claudecode_img"] = CC.mark_img("assets/claudecode-color.png", key, SC.MARK_SIDE)  # 56.0 ink
media["_anthropic_img"] = ('<img src="assets/anthropic-wordmark.png" alt="" '
    'style="position:absolute;left:50%;top:50%;width:240px;height:27.0px;'
    'transform:translate(-50%,-50%);display:block"/>')
```

`LOGOS = ~/Documents/Workspace/assets/logos`. Sizes are CORE px; do not rescale
for the cutout, the core's `scale(k)` carries them. Exact code:
`gen/_claudeconcise_proof.py::media_for`. The mascot raster is painted by three
tiles (`#mascot-a`, `#mascot-b`, `#mascot-c`), one per chapter.

**THE FILES ARE NAMED, NOT GUESSED** (`SC.LOGO_FILES`, `SC.ANTH_FILE`):

* `coding-tools/claudecode-color.png` — Claude Code, the plain NO-OUTLINE
  mascot (MARK IDENTITY). Careful: in `assets/logos/registry.json` the key
  `claude-code` points at the OUTLINED sticker file `coding-tools/claude-code.png`;
  use the FILE named here, never the registry lookup.
* `ai-models/anthropic-wordmark.png` — ANTHROPIC wordmark (3840 x 432, 8.89:1),
  seated on a WIDE 300 x 80 card, never a square tile.

Both resolve (`cutout_depthfield.assert_cast_resolves`, run at seal time).
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
  (canvas 202 … 766 = 10.5 % … 39.9 %). Y0 = the bubble's top, Y1 = the scroll's
  bottom roll.
* **Centred on x = 540 at every held instant**: chapter 0 note 125…255 /
  tile 484…596 / scroll 790…990 (centres 190 / 540 / 890); chapter 1 the dial
  alone (360…720), then dial + tile 204…876; chapter 2 dial 100…280 / tile
  484…596 / scroll 790…990.
* Seat the core in a stage zone with `left = (1080 − 1080·k)/2` and
  `top = round(centre − (SC.CONTENT_Y0 + SC.CONTENT_Y1)/2 · k, 2)`.
* After the snip (33.8 s →) chapter 2 paints only 40 … 360 (the scroll's lower
  half is gone). That is the picture, not a seating error.

**GATE SCALING.** Non-block gutters are authored ≥ 24 core px; every key sits
20-24 px from its object and is a declared block (`SC.DECLARED_BLOCKS`).

---

## 3. THE TIMELINE (`SC.CUE`, word starts from `cuts/claudeconcise/transcript_tight.json`)

| t | word | what happens |
|---|---|---|
| 0.12 | Claude | Claude Code tile pops in, alone, centred (row y 310) |
| 0.34 | no | the speech bubble grows up out of it (tail on the tile) |
| 0.78 → 1.6 | speaks English | gibberish glyphs scribble into the bubble (stagger 0.045) |
| 1.40 | (English, ends 1.34) | KEY TERM `NO LONGER ENGLISH` under the tile, first type |
| 6.36 | notice | bubble + key term leave |
| 7.40 | ask | the SIMPLE note (folded paper, one line, big ?) at the left |
| 7.72 | it | arrow note → Claude Code |
| 8.84 | simple | `SIMPLE` above the note |
| 9.84 | give | arrow Claude Code → scroll paper |
| 10.04 → 12.80 | you two to three pages worth of text to read | the scroll unrolls down to the zone's bottom, lines inking in |
| 11.12 | pages | `2-3 PAGES` above the scroll |
| 13.22 | Now | chapter 0 clears |
| 13.54 | Anthropic | ANTHROPIC card, top centre |
| 14.90 | feature | the dial (knob, ridge on the left tick, five ticks) |
| 15.20 | that | arrow card → dial |
| 17.20 | Output | `OUTPUT STYLES` under the dial |
| 18.26 | Output | card + arrow leave |
| 20.08 | AI | dial + its key slide left −156 (SWING 0.42) |
| 20.16 / 20.56 | AI / how | Claude Code tile at right; arrow dial → tile |
| 24.60 | Concise | `CONCISE` printed at the dial's right tick, tick turns terracotta |
| 28.96 → 29.48 | Concise | the knob TURNS −48° → +48°; ridge fills terracotta at 29.26 |
| 29.78 | now | tile, arrow, OUTPUT STYLES leave; dial shrinks (0.5) to the left seat |
| 29.94 | — | `CONCISE` label above the small dial |
| 30.16 / 30.48 | AI / agent | Claude Code tile centre; arrow dial → tile |
| 31.20 | always | arrow tile → scroll paper (row y 220) |
| 31.48 → 32.48 | reply | the long scroll unrolls again |
| 32.62 | a | scissors slide in from the left, open, at the cut line (y 300) |
| 33.20 | short | blades CLOSE (0.14 s); `SHORT` above the scroll |
| 33.32 → 33.82 | — | the lower half + bottom roll fall 70 px and fade; the cut edge is inked |
| 34.96 | also | scissors slide out |
| 36.10 | understand | `UNDERSTOOD` under the short note; paper edge turns terracotta |
| 37.76 | Now | opaque cream sheet rises (0.46 s); everything hidden at 38.24 |
| 38.24 → | — | small short-note glyph, terracotta rule, lockup |

Nothing drifts: arrivals, one unroll per chain, two displacements with a
spoken reason (20.08, 29.78), the knob turn, the snip.

---

## 4. THE BESPOKE OBJECTS — self-checked, DO NOT REDRAW

`SC.BESPOKE` (core boxes, held instants):

| i | name | t | core box | phone crop |
|---|---|---|---|---|
| 0 | jargon speech bubble | 2.60 | 330, 10, 750, 234 | `review/proof_claudeconcise/00.png`, 157 x 84 |
| 1 | long paper scroll | 12.95 | 790, 96, 990, 574 | `01.png`, 75 x 179 |
| 2 | style selector dial | 29.50 | 204, 150, 564, 390 | `02.png`, 136 x 90 |
| 3 | scissors cut scroll | 34.40 | 680, 96, 990, 344 | `03.png`, 116 x 93 |

Own-eyes read at 405x720: 00 a speech bubble full of symbol gibberish; 01 a long
paper scroll of text; 02 a selector knob turned to CONCISE; 03 scissors that just
cut a paper short. None is a refused UI glyph (no cylinder, gear, bell,
magnifier). Map `core` through your own k/origin for crops.

---

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 40** — every connector carries `data-connect-to` + `data-overlap-ok`;
  one arrow per target, all level or vertical: note → `mascot-a` (255,310) →
  (484,310); `mascot-a` → `scroll-a` (596,310) → (806,310) on the PAPER's left
  edge (`SC.PAPER_BOX`); card → `dial` (540,96) → (540,150); `dial` → `mascot-b`
  from the KNOB box (480,290) → (764,290); small `dial` → `mascot-c`
  (238,220) → (484,220); `mascot-c` → `scroll-b` (596,220) → (806,220), above
  the cut so it still lands on the short note. Heads pulled back 4 px (LAW 7).
* **LAW 39 / 50 / 28** — `data-label-for` on every key. Left-slot keys
  (`SIMPLE`, `CONCISE`) and scroll keys (`2-3 PAGES`, `SHORT`) all sit ABOVE;
  `NO LONGER ENGLISH` sits under the tile it names, `OUTPUT STYLES` under the
  dial, `UNDERSTOOD` under the short note. `#lbl-styles` moves with `#dial` in the
  same tween.
* **LAW 9** — `NO LONGER ENGLISH`, 48 px JetBrains Mono 800 uppercase, ls 2,
  first type on screen (1.40).
* **LAW 41** — `SC.DECLARED_BLOCKS`, stamped as `data-block`. The bubble is
  welded to `mascot-a`; the scissors (`data-overlap-ok`) to `scroll-b`.
* **LAW 42** — `SC.LIFETIMES`; anchors (`SC.SCENE_ANCHORS`) only on the dial
  (14.90 → sheet) and the payoff chain. Everything in chapters 0-1 has a finite
  window.
* **LAW 38** — two emphases, both on DRAWN objects, neither a ring: the dial's
  grip `.ridge` fills terracotta (29.26 →) — the round knob outline is never
  recoloured; the short note's `.frm` paper edge strokes terracotta (36.10 →).
  No `<circle>`/`<ellipse>` tag anywhere: round shapes are `<path>` arcs.
* **LAW 51** — the pointer turns inside `#dial` (`.ptr`, svgOrigin 180 140);
  the scroll's halves are children of `#scroll-b` and fall together with the
  bottom roll. Whatever moves, moves the same in every lane.

---

## 6. THE POINTING CUES

`pointing_cues.py --vid claudeconcise` → `no pointing cue in this take`
(`gen/_cues_claudeconcise.json`, cues []). Nothing answered, nothing waived.

## 7. WHAT THE CUTOUT OWNS

* The matte and the stage-zone seating. Prep at plan time: all markers landed
  (cut ok 41.774 s; plate ok over-wide, crop 2360x1800+636+264; prompt0 ok,
  `wing_review: true`, instrument proposed no cut — Astra's matte step owns the
  look at `kf_overlay_00000.png`; selection ok, chair audit clean; track ok
  MatAnyone 2 $0.025; ship ok, 1044 frames, min person fraction 0.441,
  `review_status: needs_final_visual_review`).
* `SC.CUTOUT_LOGO_LANES = ("codex", "cursor", "gemini", "chatgpt", "copilot",
  "opencode")`, files in `SC.CUTOUT_LANE_FILES` (all resolve under
  `assets/logos`). None is a stage mark. Fade them in after the hook has landed.
* Your own k and origin. Everything in the stage zone comes from this file.
  The scroll reaches core y 574 during both unrolls: check it against his
  crown at your k.

## 8. WHAT THE WHITEBOARD DOES

It does not import this module. It redraws the same argument per the plan's
`beats[].whiteboard`: the bubble first, alone, then the gibberish, the Claude
Code mark and `NO LONGER ENGLISH`; chapters per `plan.boards` (three, the dial
carried across the second seam); a `box_emphasis` around the dial at the turn
and around the short note at `UNDERSTOOD`.

## 9. WHERE THIS MODULE DEPARTS FROM THE PLAN'S LETTER

1. The `CONCISE` label above the small dial lands at 29.94, 0.98 s after
   'Concise,' (28.96), while the dial is finishing its 0.36 s move to that seat
   (ends 30.14); it arrives at the dial's final seat.
2. The scroll's text rows leave a small gap around the cut line in both
   scrolls (the rows are split into the upper and lower halves).
3. The dial's printed `CONCISE` becomes ~10 px at the small seat; the readable
   `CONCISE` there is the label above it.
