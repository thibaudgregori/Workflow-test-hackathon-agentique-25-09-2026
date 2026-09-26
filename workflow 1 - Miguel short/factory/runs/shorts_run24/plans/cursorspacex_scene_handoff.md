# cursorspacex — SHARED LANE SCENE HANDOFF

**Written by the PLAN + ARTWORK author for the SPLIT and CUTOUT authors.** The
plan is the contract (`plans/cursorspacex_plan.json`); this file is the
convenience. If anything below disagrees with the plan, the plan wins and you
write your own note. Section 9 lists the places this module departs from the
plan's letter, with the reason for each.

Neither lane redraws anything in this module. The scene is sealed
(`review/artwork_pass_cursorspacex.json`); a lane that needs a change takes
`production.py scene-lock`, redraws, re-reads cold over three rounds and
re-seals.

---

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/cursorspacex_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import cursorspacex_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_cursorspacex_proof.py` (`--set seal`, `--set compose`) |
| proofs | `<run>/review/proofs_cursorspacex/` |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the WHOLE 22.12 s scene: html to drop inside one
`transform: scale(k)` wrapper, and a list of `tl.*` javascript strings to
concatenate into your own timeline tail. It authors nothing outside the core, it
reads no files, and it takes no format argument — every difference between the
two formats is in the PLACEMENT and in the `lockup` string.

### `media` — the three rasters the scene paints

```python
{"_cursor_img": CC.mark_img(LOGO_URL["cursor"], "cursor", SC.MARK_SIDE["cursor"]),  # 96.0
 "_grok_img":   CC.mark_img(LOGO_URL["grok"],   "grok",   SC.MARK_SIDE["grok"]),    # 56.0
 "_spacex_img": '<img src="assets/spacex-wordmark.svg" '
                'style="width:196px;height:24.5px;display:block">'}
```

`CC.MARK_INK[key]` must be populated by `CC.measure_mark(key, src)` first, and
the `LOGO_URL` values must be page-relative (`assets/logos/<basename>`). The
sizes are **ink sides in CORE px** — do not rescale them for the cutout; the
core's own `scale(k)` carries them.

**THE FILES ARE NAMED, NOT GUESSED** (`SC.LOGO_FILES`, `SC.SPX_FILE`, MARK
IDENTITY / LAW 35):

* `coding-tools/cursor.png` — the Cursor PRODUCT mark, printed on the flag.
* `ai-models/grok.png` — the Grok mark, in the 112 px chassis tile.
* `ai-models/spacex-wordmark.svg` — SpaceX publishes a WORDMARK and nothing
  else, so the acquirer's mark is the wordmark at 196 x 24.5 in a 236 x 112
  card. It measures 9.2 px tall at 405x720 and reads: verified on
  `review/proofs_cursorspacex/compose_final_phone.png`.

There are **no source-post assets**: `pointing_cues.py` returned zero cues on
this take, so there is no card, no highlight and no raster text anywhere in the
scene.

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
* `SC.CONTENT_Y0, SC.CONTENT_Y1 = 10.0, 564.0` — the band the core DECLARES it
  paints in (canvas 202 … 756). Y0 is the key term's box top, Y1 is the card
  row's bottom. Both are REAL painted ink. Canvas 202 is 10.5 % of frame
  height, clear of LAW 30's top-10 % line; canvas 756 is 39.4 %, clear of the
  caption seat.
* **The composition is centred on x = 540.** The hook's ink runs 401 … 675
  (optical centre 538) and the final frame's ink runs 342 … 738 (optical centre
  540). The one deliberate offset is beats 1–3, where the SpaceX card is
  already at its final row seat and the Grok tile has not been named yet: that
  group's centre is 508, i.e. 32 core px left of the axis, 12 px at phone
  scale. It is a seat, not a drift — nothing moves. Seat the core with
  `left = (1080 − 1080·k) / 2`.
* Seat the core so its CONTENT BAND — not its box — is centred on your stage
  zone's centre:
  ```python
  top = round(centre - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 * k, 2)
  ```

**GATE-SCALING.** The cutout scales the core by ~0.95, so a 44 core-px gutter
arrives as ~42 canvas px. Every non-block gutter in this scene is authored at
**≥ 44 CORE px**: key term bottom 68 → pole top 112 = 44; retired flag ink
bottom 380 → card row top 452 = 72; SpaceX card right 578 → Grok tile left 626
= 48. Everything tighter than that is inside a DECLARED block
(`SC.DECLARED_BLOCKS`), where Gate 1's cramp check does not bind.

---

## 3. THE TIMELINE

`SC.CUE` carries every instant, and each one is a word START from
`cuts/cursorspacex/transcript_tight.json` unless its comment says `authored`.
`SC.BEAT_EDGES` is the plan's own beat table. `SC.DUR = 22.12`, the cut master.

`SC.BOARD_MODE = "single"` — LAW 43's exception, declared in the plan with its
reason: one pole, one accumulating argument, and the finished frame IS the
claim. There is no chapter seam and no erase, so there is no zero-ink handover
to prove.

| t | word | what happens |
|---|---|---|
| 0.18 | One | the mast draws, alone, on the axis; the foot follows at 0.38 |
| 0.52 | most | the flag UNFURLS off the pole top (one scaleX from the hoist, then it holds) |
| 1.08 | loved | the heart prints on the flag |
| 5.08 | sunset | KEY TERM `SUNSET` writes in, first and alone (LAW 9) |
| 5.68 | Cursor | the heart fades out IN PLACE and the Cursor mark fades in on the same seat |
| 7.08 | SpaceX | the SpaceX card pops in below the mast |
| 9.84 | mapping | the flag's first step DOWN the pole; its ink drops to 0.74 |
| 12.00 | next | second step, 0.55 |
| 13.24 | months | third step, 0.40 — it is retired at the foot |
| 14.62 | absorbed | the first terracotta stroke draws into the SpaceX card |
| 15.82 | SpaceX | PANEL BORDER FLIP on the SpaceX card |
| 17.44 | Grok | the Grok tile pops in, the second stroke draws, its border flips at 17.78 |
| 18.30 | — | the opaque sheet rises (authored: the final frame is held ~0.9 s first) |
| 18.80 | — | the outro flag glyph, the terracotta rule, the lockup |

**Nothing drifts.** Every move is an arrival, a one-shot unfurl, a hard stepped
descent or a fade, and every one of them lands on its own spoken word (LAW 1 /
LAW 21 / LAW 25).

---

## 4. THE ONE BESPOKE OBJECT — SEALED, DO NOT REDRAW

`SC.BESPOKE` carries the box in CORE coordinates and the held instant.

| i | object | t | core box | cold reads (3 independent rounds) |
|---|---|---|---|---|
| 0 | flag on pole | 2.60 | 401, 112, 679, 404 | "flag with heart" ×3, **all sure**, 0 different |

Evidence: `review/phone_reader_cursorspacex_artwork_r{1,2,3}.json`; scoring
`review/artwork_scores_cursorspacex.json`; seal
`review/artwork_pass_cursorspacex.json`. Crop:
`review/proofs_cursorspacex/crop_seal_00_flag.png` (105 x 110 px at 405x720).

It is not a hedged pass and it needs no clerk adjudication: three of three
readers reached the object, all three were `sure`, all three answers were inside
the five-word cap.

**Why this metaphor and not a UI glyph.** The plan's checklist (a lone cylinder
is the registry's database drum, a gear is settings, a bell is a notification, a
magnifier is search) was run against it: a flag ON A POLE with a visible finial
above the cloth and a splayed foot below is not any of those, and the one glyph
it could collide with — the bare "flag" bookmark icon — IS the intended noun, so
a collision there is a pass, not a miss. The pole's 34 px of bare mast above the
flag and its foot are load-bearing: without them the shape reads as a bookmark.

One frame-normalised box cannot be right for both formats — the box is a
consequence of the placement — so map `SC.BESPOKE[0]["core"]` through your own k
and origin when you cut phone crops.

---

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 40** — `SC.FLAG_ENDS = anchor_points(SC.BANNER_LOW_INK, 2, "bottom")` =
  (463.3, 380.0) and (634.7, 380.0): level to 0.0 px and symmetric about the
  flag's own axis. `SC.SPX_END = anchor_points(SC.SPX_BOX, 1, "top")` =
  (460.0, 452.0); `SC.GROK_END = anchor_points(SC.GROK_BOX, 1, "top")` =
  (682.0, 452.0). Both connectors carry `data-connect-to` and
  `data-overlap-ok`, and both terminate AT the target's top edge, never on top
  of it (LAW 7). This is ONE source fanning into TWO targets, so the law's
  letter does not bind — the ends are built with its helper anyway. **Do not
  hand-place an end.**
* **LAW 39 / LAW 50** — exactly ONE written key, `SUNSET`, with
  `data-label-for="banner"`: entirely ABOVE the flag, centre 540 inside the
  flag's ink extent 423 … 675 ±15 % (511 … 587). There is no second key, so
  there is no sibling baseline to hold.
* **LAW 9** — `SUNSET` is the key term, `SC.KEY_TERM`, 48 px JetBrains Mono
  uppercase, letter-spacing 2, and **no other type exists on the board before
  5.08.**
* **LAW 41** — `SC.DECLARED_BLOCKS`, stamped as `data-block` in the DOM: the
  mast (`pole`, `foot`, `banner` physically hang off one another), the flag
  welded to whatever is printed on it (`heart`, then `mark-cursor`), the flag
  welded to its key, and each card welded to its own mark.
* **LAW 42** — `SC.LIFETIMES`. The board is SINGLE and therefore all-anchor by
  definition; `SC.SCENE_ANCHORS` declares them anyway so the law holds even if
  the outro wipe is read as a seam. The heart is the ONE finite mark
  (1.08 → 5.90) and declares its `t_to`.
* **LAW 38** — exactly two emphases, both matched to their target: PANEL BORDER
  FLIPS on `#card-spacex` (15.82) and `#tile-grok` (17.78), both drawn cards
  with their own background. **No ring, no ellipse, no circle exists anywhere
  in this module and no `<circle>` tag is emitted at all.** There is no marker
  highlight because there is no raster text in this video.
* **LAW 51** — the FLAG is the object all three lanes share, and whatever is
  printed on it is a CHILD of it in the DOM (`#heart` and `#mark-cursor` live
  inside `#banner`). When the flag steps down the pole, its face steps with it.
  A lane that animates the flag without its face is a cross-lane parity defect.
* **LAW 32 / LAW 36** — both cards take the same 18 px radius and the same 3 px
  ink-alpha border; each mark sits fully inside its card with visible margin
  (Cursor 96 px ink inside a 252 x 162 flag face; Grok 56 px ink = 0.50 of its
  112 px tile; the SpaceX wordmark 196 px wide inside a 236 px card, 20 px each
  side).

---

## 6. THE POINTING CUES

`pipeline/pointing_cues.py --vid cursorspacex` returns **`no pointing cue in
this take`** — zero cues. Nothing is answered and nothing is waived, there is no
source card, and GLOBAL LAW 3 is satisfied trivially: the acquisition is the
news, not anybody's post. Scan record: `<run>/gen/_cues_cursorspacex.json`.

---

## 7. WHAT THE CUTOUT OWNS

* The matte, the wing review and the stage-zone seating. At plan time only the
  **cut** marker existed for this recording (`prep/stages/cursorspacex.cut.json`,
  status ok, 59.5 s, cut master 22.12 s); **plate, prompt0, track, ship and cues
  markers did not exist yet**, so *wing review: prompt0 not landed at plan time
  — the cutout author owns it.*
* `SC.CUTOUT_LOGO_LANES = ("codex", "copilot", "antigravity", "lovable",
  "openai")` — topical to this short: the AI coding tools Cursor is measured
  against, plus the lab that ships one of them. Mixed, none repeated, and none
  of the three STAGE marks (cursor, spacex, grok) appears in a lane.
* Your own k and origin. Everything else in the stage zone comes from this file.

## 8. WHAT THE WHITEBOARD DOES NOT DO

It does not import this module. It redraws the SAME argument in marker ink, with
the same object, the same key term and the same three marks, per beat
`whiteboard` in the plan: the pole drawn first and alone on the axis, the flag,
the heart inside it, `SUNSET` written above, then the flag REDRAWN lower three
times, each drawing leaving its fainter predecessor behind so the descent reads
as time passing, then the two strokes into the two marks. LAW 51 still binds:
whatever is on the flag moves with it there too.

---

## 9. WHERE THIS MODULE DEPARTS FROM THE PLAN'S LETTER

1. **The retired flag is faded, not broken.** The plan's beats 2 and 3 call the
   lowered flag's outline "broken and muted". It is drawn with a solid stroke
   at falling opacity (1.00 → 0.74 → 0.55 → 0.40) instead of a dashed one,
   because a live `stroke-dasharray` removes an element from Gate 1's checks
   altogether and the dash law then owns the reveal. The argument is unchanged:
   the brand dims one grade per step and ends at 40 %.
2. **The whiteboard keeps the ghosts; the DOM lanes do not.** The plan's board
   version leaves a faint copy of the flag at each height it left. In the DOM
   scene the flag is ONE element that moves, so there is exactly one flag at any
   instant. The board may keep its ghosts — that is the format's own grammar and
   it is why the plan writes the board version separately.
3. **The SpaceX card is 236 x 112 and not a 112 px tile.** SpaceX publishes only
   a wordmark (8:1), and a wordmark inside a 112 px square is 7 px of ink at
   phone size, i.e. LAW 8 illegible. The card keeps the chassis tile's radius,
   border and row seat; only its width differs, and the row's two cards share
   one top (452) and one bottom (564) so they still sit as siblings. This is the
   plan's first open question, answered.
4. **The sheet rises at 18.30, not at 17.88.** The sign-off starts at 17.88 but
   the Grok tile only lands at 17.44, so raising the sheet on "Now" would cover
   the finished claim 0.44 s after it completed. The authored cue holds the
   final frame ~0.9 s first. The outro still runs 3.3 s.
5. **The plan's bbox for object 0 was written before the drawing existed.**
   `SC.BESPOKE[0]["core"]` = (401, 112, 679, 404) is the real one and is
   authoritative for geometry; the plan's normalised box was updated to match.
