# claudesessions — SHARED LANE SCENE HANDOFF

**Written by the PLAN + ARTWORK author for the SPLIT and CUTOUT authors.** The
plan is the contract (`plans/claudesessions_plan.json`); this file is the
convenience. If anything below disagrees with the plan, the plan wins and you
write your own note. Section 9 lists the places this module departs from the
plan's letter, with the reason for each.

Neither lane redraws anything in this module. The scene is sealed
(`review/artwork_pass_claudesessions.json`); a lane that needs a change takes
`production.py scene-lock`, redraws, re-reads cold over three rounds and
re-seals.

---

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/claudesessions_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import claudesessions_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_claudesessions_proof.py` (`--set seal`, `--set compose`) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the WHOLE 21.24 s scene: html to drop inside one
`transform: scale(k)` wrapper, and a list of `tl.*` javascript strings to
concatenate into your own timeline tail. It authors nothing outside the core, it
reads no files, and it takes no format argument — every difference between the
two formats is in the PLACEMENT and in the `lockup` string.

### `media` — the ONE raster the scene paints

```python
{"_claudecode_img": CC.mark_img(LOGO_URL["claude-code"], "claude-code",
                                SC.MARK_SIDE["claude-code"])}   # 56.0
```

`CC.MARK_INK["claude-code"]` must be populated by
`CC.measure_mark("claude-code", src)` first, and `LOGO_URL` must be
page-relative (`assets/logos/<basename>`). The size is an INK side in CORE px —
do not rescale it for the cutout; the core's own `scale(k)` carries it. It is
0.50 of the 112 px tile, the chart's own ratio.

**THE FILE IS NAMED, NOT GUESSED** (`SC.LOGO_FILES`, MARK IDENTITY): the script
says "Claude Code", so the registry key is `claude-code`
(`assets/logos/coding-tools/claudecode-color.png`), the plain no-outline
mascot — **never** `claude-code-sticker` (`coding-tools/claude-code.png`), whose
die-cut white edge would halo on this cream tile. There is no second stage mark
and no source-post card anywhere in this video.

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
* `SC.CONTENT_Y0, SC.CONTENT_Y1 = 24.0, 529.0` — the band the core DECLARES it
  paints in (canvas 216 … 721). Y0 is the key term's box top in chapter 0, Y1 is
  TEAMMATES' box bottom in chapter 1. Both are REAL painted ink. Canvas 216 is
  11.25 % of frame height, clear of LAW 30's top-10 % line; canvas 721 is
  37.6 %, clear of the caption seat.
* The composition **is symmetric about x = 540 in every chapter**: the pair
  (217 + 863 = 1080), the middle slot (461 + 619 = 1080), the key term
  (270 + 810 = 1080), the trio's centres (270 / 540 / 810), the outro column
  (486 + 594 = 1080). So `left = (1080 − 1080·k) / 2`.
* Seat the core so its CONTENT BAND — not its box — is centred on your stage
  zone's centre:
  ```python
  top = round(centre - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 * k, 2)
  ```

**GATE-SCALING.** The cutout scales the core by ~0.95, so a 42 core-px gutter
arrives as ~40 canvas px. Every non-block gutter in this scene is authored at
**≥ 42 CORE px** (the stacked rows) or at **84 CORE px** (the middle slot to
each radio body); every gap smaller than that is inside a DECLARED block
(`SC.DECLARED_BLOCKS`), where Gate 1's cramp check does not bind.

**THE LAW 30 RAIL.** The only ink that enters the right 15 % column
(canvas x > 918) below canvas y 576 would be the ONE SESSION key; it does not.
Measured on the composed frame: the sibling-key row's ink runs x 164 … 905.
Do not widen that key, and if your k shifts it right, move the whole core, never
that one label (its baseline is a LAW 50 commitment).

---

## 3. THE TIMELINE

`SC.CUE` carries every instant, and each one is a word START from
`cuts/claudesessions/transcript_tight.json` unless its comment says `authored`;
an authored cue is inside its word's 1.0 s LABEL_WINDOW. `SC.BEAT_EDGES` is the
plan's own beat table. `SC.DUR = 21.24`, the cut master.

Two chapters, `SC.BOARD_MODE = "chapters"`, `SC.BOARD_CHAPTERS`:

| ch | t | what is on screen |
|---|---|---|
| 0 | 0.10–9.72 | the two radios (0.10, 0.30), the signal arc (0.94), a pulse on it at 1.32 / 4.56 / 5.58-back, the Claude Code tile in the middle slot (2.94–6.38), `SESSIONS TALK` (3.84), then the developer figure in that slot (6.94) with two dashed shuttle arrows (7.90), a terracotta box flip on him (7.90–9.30) and one terracotta strike through him (8.98) |
| 1 | 9.72–17.00 | three radios (10.04 / 10.26 / 12.54), the border flip on the right one (12.90–14.10), two arcs into the centre one (14.44), a pulse on both (15.24), `LONG-RUNNING` (10.60), `ONE SESSION` (13.20), `TEAMMATES` (16.26) |
| — | 17.00–21.24 | the opaque rising sheet, then the lockup on one small radio |

**The erase is a HANDOVER, never a blank** (`clear()`): chapter 0 fades over
0.22 s from 9.72 while chapter 1's first radio is already arriving at 10.04, so
the zone's ink never reaches zero across the seam. The seam lands on "If" — the
start of a new idea, not the end of a sentence (LAW 45).

**THE PULSE.** A message travelling a line is NOT a moving element: it is a
30-unit dash driven along the arc's own `pathLength="1000"`, so nothing drifts
and every travel is one word-synced event that ends (LAW 1). The draw-on dash
equals the path's declared length, never `getTotalLength()`.

---

## 4. THE TWO BESPOKE OBJECTS — SEALED, DO NOT REDRAW

`SC.BESPOKE` carries the boxes in CORE coordinates and the held instant of each.

| i | object | t | core box | cold reads (3 independent rounds) |
|---|---|---|---|---|
| 0 | two walkie talkies | 2.40 | 217, 128, 863, 482 | "walkie-talkies" ×3, all **sure**, 0 different |
| 1 | three walkie talkies | 16.00 | 205, 96, 875, 343 | "walkie-talkie" ×3, all **sure**, 0 different |

Six of six independent readers named the intended object with confidence and no
reader named anything else, so neither object is hedged and neither needs clerk
adjudication on the delivered render. Evidence:
`review/phone_reader_claudesessions_artwork_r{1,2,3}.json`, scoring
`review/artwork_scores_claudesessions.json`, seal
`review/artwork_pass_claudesessions.json`.

Object 0's instant is **2.40 on purpose**: the arc's first pulse has finished
(1.32 + 0.50) and the Claude Code tile does not take the middle slot until 2.94,
so the crop the readers saw is exactly the crop the real render gives.

One frame-normalised box cannot be right for both formats — the box is a
consequence of the placement — so map `SC.BESPOKE[i]["core"]` through your own
k and origin when you cut phone crops.

---

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 40** — `SC.TEAM_END_L = anchor_points(SC.TEAM_B_BOX, 1, "left")` and
  `SC.TEAM_END_R = anchor_points(..., 1, "right")`: the two arcs that terminate
  on the centre radio land on ITS OWN BOX SIDES, at the same fraction (0.5) of
  its height, never on a hand-placed point of an antenna outline. Both carry
  `data-connect-to="team-b"` and `data-overlap-ok`.
* **LAW 39 / LAW 50** — three keys, each with `data-label-for`, each entirely
  BELOW its host and centred on that host's own axis to 0.0 px: `LONG-RUNNING`
  below `team-a` (axis 270), `ONE SESSION` below `team-c` (axis 810),
  `TEAMMATES` below the row (axis 540). The two siblings take the SAME
  placement on the SAME baseline (`SC.KEY_ROW_Y = 385`).
* **LAW 41** — `SC.DECLARED_BLOCKS`, stamped as `data-block` in the DOM.
* **LAW 42** — `SC.LIFETIMES`, every mark finite except the outro lockup
  (`SC.SCENE_ANCHORS`).
* **LAW 38** — exactly two emphases, and BOTH are the panel border flip,
  because both targets are DRAWN objects and this video contains no raster text
  anywhere for a marker highlight to land on: `#you-emph` at 7.90 and
  `#team-c-emph` at 12.90. No ring, no ellipse, no circle exists anywhere in
  this module, and **no `<circle>` tag is emitted at all** — every rounded thing
  is a `<rect rx>` or a closed `<path>`, including the figure's head.
* **LAW 51** — the WALKIE-TALKIE is the object all three lanes share. Wherever
  it moves, its parts move with it: the antenna, the collar, the grille, the
  display and the buttons are one `<svg>` inside one positioned div, and the
  arc that leaves an antenna is blocked to that radio. A lane that animates a
  radio without its antenna is a cross-lane parity defect.
* **LAW 9** — `SESSIONS TALK` is the key term: 48 px JetBrains Mono uppercase,
  letter-spacing 2, centred on the axis, and it is the FIRST type on the board
  (3.84). Nothing typed precedes it; the tile at 2.94 is a mark, not type.

---

## 6. THE POINTING CUES

`pipeline/pointing_cues.py --vid claudesessions` returns **no cue in this take**
(`gen/_cues_claudesessions.json`, `cues: []`). There is nothing to answer and
nothing to waive. **No source-post card exists anywhere in this scene**, no
platform frame had to be chosen, and GLOBAL LAW 3 is satisfied by absence. If a
lane invents a tweet card here, it is inventing a claim the recording never
made.

---

## 7. WHAT THE CUTOUT OWNS

* The matte, the wing review and the stage-zone seating — at plan time the only
  marker on disk was `prep/stages/claudesessions.cut.json` (status ok, wall
  48.3 s, cut master 21.24 s, tight audio 21.23 s, `analysis_wav_written:
  false` by design). **prompt0 had not landed, so the cutout author owns the
  wing review.** plate, track, ship and cues have no marker either; read them
  when you start.
* `SC.CUTOUT_LOGO_LANES = ("codex", "cursor", "copilot", "opencode",
  "antigravity", "openclaw")` — topical to this short (coding agents in the
  category it names), mixed, no mark repeated, and deliberately WITHOUT
  `claude-code`, which is the stage mark (GRAPHIC CHART clause 7). The files are
  in `SC.LANE_FILES`, all real registry marks under
  `assets/logos/coding-tools/`.
* Your own k and origin. Everything else in the stage zone comes from this file.

## 8. WHAT THE WHITEBOARD DOES NOT DO

It does not import this module. It redraws the SAME argument in marker ink, with
the same objects, the same labels and the same key term, per beat
`whiteboard_version` in the plan. LAW 51 still binds: a radio's antenna moves
with its radio there too.

---

## 9. WHERE THIS MODULE DEPARTS FROM THE PLAN'S LETTER

1. **Object 1's bbox moved up.** The plan's first draft put the trio's box at
   core y 96…376; the drawn cluster is 96…343, because the bodies came out
   187 px tall rather than 220 once the 42 px label gutters were budgeted. The
   plan file carries the corrected norm box `[0.1898, 0.15, 0.8102, 0.2786]`;
   `SC.BESPOKE` is authoritative for geometry either way.
2. **The shuttle arrows are dashed, not solid.** The plan says "two dashed
   arrows"; this is only worth naming because the dash is the ARGUMENT — the
   thing about to be struck off is drawn as provisional from the moment it
   appears, so the strike at 8.98 reads as confirmation rather than as a
   contradiction.
3. **`SESSIONS TALK` outlives its chapter's first idea.** The plan gives it the
   lifetime 3.84–9.72, i.e. it is still on the board during the "you no longer
   switch" beat. That is deliberate and not an oversight: the struck figure
   argues against the OLD way, and the key term overhead is what it is being
   struck in favour of. Erasing it early would leave the beat arguing with
   nothing.
4. **Proof outputs are per-video.** `_claudesessions_proof.py` must be run with
   `--out <run>/review/proofs_claudesessions`. Every recording's proof harness
   in this batch writes `_c_<frame>.html` / `compose_<frame>.png` /
   `proofs_<set>.json` under identical names, and a shared `review/proofs`
   folder had the siblings overwriting each other's pages (geminigems' outro was
   briefly read here as this video's outro). The seal crops were re-rendered
   into the per-video folder and hash-compared byte-for-byte against what the
   readers saw, so no seal evidence is stale.

---

## 10. THE GRAPHIC-CHART CHECK

`review/proofs_claudesessions/chart_sidebyside.png` holds one composed frame of
this scene under one frame of the run-15 reference (`geminitools_scene.py`, its
own ink painted by its own code). Same cream ground `#F6F1EA`, same near-black
ink `#141416`, same terracotta `#C4573A` for the connectors, the emphasis flips
and the outro rule, same thin ink-line silhouette drawing with a card fill and
no gradient, shadow or 3-D, same JetBrains Mono uppercase keys at the chart's
own 28 px / 1.2 letter-spacing and 48 px / 2.0 key term, same 112 px 3 px-border
radius-18 tile with the mark's ink at 0.50 of the tile, same 1080 × 600 core at
offset 192. Every palette constant in this module is byte-identical to the
reference module's. A stranger files them under one channel because the two
frames use the same four colours, the same one line weight band, the same one
typeface in the same case, and the same habit of putting one everyday object on
an empty cream field with its name written under it.
