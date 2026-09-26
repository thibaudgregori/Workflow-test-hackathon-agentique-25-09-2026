# primeagent — SHARED LANE SCENE HANDOFF

**Written by the PLAN + ARTWORK author for the SPLIT and CUTOUT authors.** The
plan is the contract (`plans/primeagent_plan.json`); this file is the
convenience. If anything below disagrees with the plan, the plan wins and you
write your own note. Section 9 lists the places this module departs from the
plan's first draft, with the reason for each.

---

## 1. THE MODULE

| | |
|---|---|
| path | `runs/shorts_run24/gen/primeagent_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import primeagent_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `runs/shorts_run24/gen/_primeagent_proof.py` (`--set seal`, `--set compose`) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the WHOLE 43.175 s scene: html to drop inside one
`transform: scale(k)` wrapper, and a list of `tl.*` javascript strings to
concatenate into your own timeline tail. It authors nothing outside the core, it
reads no files, and it takes no format argument — every difference between the
two formats is in the PLACEMENT and in the `lockup` string.

### `media` — the three rasters the scene paints

```python
{f"_{k}_img": CC.mark_img(LOGO_URL[k], k, SC.MARK_SIDE)   # MARK_SIDE = 74.0
 for k in SC.MARK_KEYS}                 # ("claude-code", "codex", "cursor")
```

`CC.MARK_INK[key]` must be populated by `CC.measure_mark(key, src)` first, and
the `LOGO_URL` values must be page-relative (`assets/logos/<basename>`). The size
is an **ink side in CORE px** — do not rescale it for the cutout; the core's own
`scale(k)` carries it.

**THE FILES ARE NAMED, NOT GUESSED** (`SC.LOGO_FILES`, MARK IDENTITY):
`coding-tools/claudecode-color.png` is the plain no-outline Claude Code mascot
and NEVER `claude-code.png`, the white-outlined sticker; `codex-color.png` and
`cursor.png` are the product marks, never a parent company's (LAW 35).

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
* `SC.CONTENT_Y0, SC.CONTENT_Y1 = 60.0, 549.0` — the band the core DECLARES it
  paints in (canvas 252 … 741). Y0 is `ONE SINGLE TOOL`'s box top in chapter 2,
  Y1 is the crossed pair's lowest ink in chapter 3. Both are REAL painted ink.
  Canvas 252 is 13.1 % of frame height, clear of LAW 30's top-10 % line; canvas
  741 is 38.6 %, far above the caption seat.
* The composition **is symmetric about x = 540 in every chapter, by
  construction**: every machine placement is seated with
  `left = 540 − 148 k` (148 is the machine's own authoring ink centre), the
  toolbox with `left = 540 − 160 k`, the crossed pair's two tool centres are
  ±30 px about 540, the slab and the rule are centred, and the tile row is
  320/484/648 (centre 540). So `left = (1080 − 1080·k) / 2`.
* Seat the core so its CONTENT BAND — not its box — is centred on your stage
  zone's centre:
  ```python
  top = round(centre - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 * k, 2)
  ```

**GATE-SCALING.** The cutout scales the core by ~0.95, so a 42 core-px gutter
arrives as ~40 canvas px. Every non-block gutter in this scene is authored at
**≥ 42 CORE px**; every gap smaller than that is inside a DECLARED block
(`SC.DECLARED_BLOCKS`), where Gate 1's cramp check does not bind.

---

## 3. THE TIMELINE

`SC.CUE` carries every instant, and each one is a word START from
`cuts/primeagent/transcript_tight.json` unless its comment says `authored`; an
authored cue is inside its word's 1.0 s LABEL_WINDOW. `SC.BEAT_EDGES` is the
plan's own beat table. `SC.DUR = 43.175`, the cut master.

Five chapters, `SC.BOARD_MODE = "chapters"`, `SC.BOARD_CHAPTERS`:

| ch | t | what is on screen |
|---|---|---|
| 0 | 0.10–2.36 | the machine, complete, a part already on its bed; `PRIME AGENT` above it at 1.10 |
| 1 | 2.36–8.58 | the open toolbox; `REGULAR AGENTS` at 3.06; the wrench and the saw stand up at 3.80 / 4.18; one tool lifts clear and drops back at 4.70, 6.38 and 7.32 |
| 2 | 8.72–21.50 | the machine again, larger, bed EMPTY; `ONE SINGLE TOOL` at 11.62; the part grows on the bed at 14.06; the gantry outline flips terracotta 17.62–18.94 |
| 3 | 21.62–25.34 | the crossed pair alone on the whole board — the hammer at 21.62, the screwdriver crossing it at 22.28 |
| 4 | 25.42–38.60 | the machine small at 25.42, the RLM slab at 27.02, `RLM` at 29.40, three agent tiles 32.80/32.96/33.12, the terracotta rule at 33.28, the tile borders flipping together 33.28–34.94 |
| — | 38.78–43.175 | the opaque rising sheet, then the lockup on the small machine |

**The erase is a HANDOVER, never a blank** (`clear()`): the outgoing chapter
fades over 0.22 s while the incoming chapter's first object is already arriving,
so the zone's ink never reaches zero across a seam, and every seam lands on the
object the next sentence is about (LAW 45).

**There is no camera move and no element move anywhere in this scene** — only
arrivals, the toolbox's three word-synced tool lifts, two emphases and four
erases (LAW 1 / LAW 25).

---

## 4. THE THREE BESPOKE OBJECTS — ALL THREE SEALED

`SC.BESPOKE` carries the boxes in CORE coordinates and the held instant of each.
Proof crops: `review/proof_primeagent/00.png`, `01.png`, `02.png` (405x720
phone scale, each object alone). Earlier record: `review/artwork_scores_primeagent.json`.

| i | object | t | core box | phone crop |
|---|---|---|---|---|
| 0 | open toolbox with tools | 8.20 | 364.5, 176.6, 715.5, 453.5 | 131 x 104 |
| 1 | tool printing machine | 1.80 | 356.4, 203.1, 723.6, 456.9 | 137 x 95 |
| 2 | two crossed tools | 24.40 | 310.0, 123.0, 770.0, 549.0 | 173 x 160 |

**All three are sealed. Never redraw them.** Object 2 is the round-4 drawing:
a claw hammer and a flat-blade screwdriver laid across each other at +/-34
degrees, 350 core px each, alone on the whole board. **Miguel reviewed it
himself on 2026-09-21 and accepted it**; its name is **"two crossed tools"**,
which is what a stranger produces from the crop. The earlier reader rounds that
argued about the second tool's identity are history, not a live objection, and
no lane may reopen them.

One frame-normalised box cannot be right for both formats — the box is a
consequence of the placement — so map `SC.BESPOKE[i]["core"]` through your own k
and origin when you cut crops.

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 40** — **no connector exists in this scene.** Every relationship here is
  CONTAINMENT (the tools in the box, the part on the bed, the machine on the
  slab) and is carried by the declared blocks. `SC.anchor_points` is kept in the
  module so a lane that later adds a connector cannot hand-place its end.
* **LAW 39 / LAW 50** — four written keys, each with `data-label-for`:
  `PRIME AGENT` ABOVE `machine-hook`, `REGULAR AGENTS` ABOVE `toolbox`,
  `ONE SINGLE TOOL` ABOVE `machine-main`, `RLM` BELOW `rlm-slab`. The three keys
  of chapters 0, 1 and 2 all sit the same way; `RLM` is alone in its chapter.
  Every key is centred on its host's own ink axis to within 2.4 px.
* **LAW 41** — `SC.DECLARED_BLOCKS`, stamped as `data-block` in the DOM.
* **LAW 42** — `SC.LIFETIMES`, every mark finite except the outro lockup. The
  machine is on screen for more than 40 % of the take across its three
  instances, so all three are also named in `SC.SCENE_ANCHORS`.
* **LAW 38** — exactly two emphases, each matched to its target and each BOXING
  a DRAWN object: the machine's own gantry outline flipping ink → terracotta at
  17.62, and the three tile borders flipping together at 33.28. **No `<circle>`
  tag is emitted anywhere in this module** — the machine's filament spool and its
  hub are `<path>` arcs — so nothing in the scene can be read as a ring.
* **LAW 51** — the machine is the object all three lanes share. Its spool, rail,
  nozzle, bed and part are one SVG, so they move together by construction; a
  lane that animates any of them separately is a cross-lane parity defect.
* **THE DRAW-ON DASH LAW** — every drawn path carries `pathLength="100"`, so a
  `strokeDasharray:100` reveal is always the path's own length.

---

## 6. THE POINTING CUE

There is none. `pipeline/pointing_cues.py --vid primeagent` returned
`no pointing cue in this take` (`gen/_cues_primeagent.json`, `cues: []`). The
script names no platform, no post and no person, so no source card is built,
nothing is waived, and GLOBAL LAW 3 never engages.

---

## 7. WHAT THE CUTOUT OWNS

* The matte, the wing review and the stage-zone seating — the `prompt0` marker
  did not exist at plan time, so **the cutout author owns the wing review**.
* `SC.CUTOUT_LOGO_LANES = ("claude-code", "codex", "cursor", "opencode",
  "copilot", "antigravity")` — topical to this short (the category the script
  compares Prime Agent against), mixed, no mark repeated, and never the story's
  own stage object, which is drawn and has no mark.
* Your own k and origin. Everything else in the stage zone comes from this file.
* **Check the spool hole at your k.** The small ring inside the filament spool is
  what stops the machine's frame reading as a plain box; if it closes up below
  ~0.90, widen the hole rather than enlarging the machine.

---

## 8. WHAT THE WHITEBOARD DOES NOT DO

It does not import this module. It redraws the SAME argument in marker ink, with
the same objects, the same written keys and the same key term, per the
`whiteboard` field on each beat in the plan. LAW 51 still binds: the machine's
parts move together there too.

---

## 9. WHERE THIS MODULE DEPARTS FROM THE PLAN'S FIRST DRAFT

The plan in `plans/primeagent_plan.json` has been updated to match, so these are
recorded as history rather than as live disagreements.

1. **The pegboard rack became an OPEN TOOLBOX.** The first draft hung three thin
   tools on a perforated board. At 405x720 the perforations vanished and the
   three tools came back as three vertical scratches
   (`review/proofs/round0/crop_seal_00_rack.png`). The metaphor — a fixed set you
   pick from — was kept; the drawing was rebuilt with fewer, fatter objects and a
   strap handle, and read "toolbox" 3/3 sure.
2. **`ONE SINGLE TOOL` moved from below the machine to above it.** Below it, the
   key sat exactly where the part grows on the bed at 14.06 and where the beat-4
   connectors would have had to leave. Above it, the three written keys of
   chapters 0, 1 and 2 also sit the same way (LAW 50).
3. **Chapter 2 split into two chapters, and the two connectors went.** Beat 4's
   two tools shared the board with the full-size machine and were 180 core px
   tall; two cold rounds refused them. The pair now owns its own chapter and the
   whole board at 350 core px each — which leaves no machine on screen for a
   connector to leave, so the scene has none.
4. **The plan's bbox values** for all three objects were written before the
   drawings existed. `SC.BESPOKE` carries the real ones and is authoritative for
   geometry; the plan's `bbox` fields have been refreshed from it.
