# stripekai — SHARED LANE SCENE HANDOFF

**Written by the design agent for the SPLIT author and Astra's CUTOUT.** The plan
(`plans/stripekai_plan.json`) is the contract; this file is the convenience. If
anything here disagrees with the plan, the plan wins and you write your own note.
Section 9 lists where this module departs from the plan's letter.

Neither lane redraws anything in this module. The scene is sealed with
`production.py seal` (v4: module + handoff hashes, `review/artwork_pass_stripekai.json`);
a lane that builds on a changed module is refused.

---

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/stripekai_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import stripekai_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_stripekai_proof.py` (`--set seal`, `--set compose`) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the WHOLE 35.82 s scene: html to drop inside one
`transform: scale(k)` wrapper, and a list of `tl.*` JavaScript strings for your own
timeline (70 tweens). It reads no files and takes no format argument; every
difference between the two formats is PLACEMENT plus the `lockup` string. It calls
`SC.assert_anchor_law()` before it writes a byte. The eases it names are the
chassis' own: `SOFT`, `POP`, `SWING`. Labels and counters use class `mono` (the
chassis' JetBrains Mono uppercase rule, weight 800 set inline), so the page must
load that face (the chassis does).

### `media` — the one raster the scene paints

```python
CC.MARK_INK["stripe"] = CC.measure_mark("stripe", <assets/logos/platforms/stripe-color.png>)
{"_stripe_img": CC.mark_img(LOGO_URL["stripe"], "stripe", SC.STRIPE_SIDE)}   # 96.0
```

The URL must be page-relative (`assets/logos/<basename>`). The same `<img>` string is
used by BOTH toolboxes (`#toolbox` in chapters 0-1, `#toolbox-2` in chapter 4); it sits
inside a nameplate that is itself inside the toolbox's statically scaled inner div, so
pass the side in AUTHORING units (96.0) and let the toolbox scale carry it.

**THE FILE IS NAMED, NOT GUESSED** (`SC.LOGO_FILES`): `stripe` =
`platforms/stripe-color.png` (the purple Stripe wordmark, aspect 2.40). The registry has
no `stripe` entry and the library has no square Stripe app icon, so the key is resolved
through `SC.LOGO_FILES` (it passes `cutout_depthfield.assert_cast_resolves`). Kai has no
public mark: it is the key term.

There is no source post, no screenshot and no other raster in this video
(`pointing_cues.py` returned zero cues).

### `lockup` — the outro's handle block

```python
CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W) \
  + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W)
```

Seated inside the scene's own `#o-slot` (core top 358). `handle_key` is the only string
that differs between masters: `"yt"` on the split, `"tiktok_ig"` on the cutout.

---

## 2. THE UNITS

**CORE px = the plan's CANVAS px with y shifted by -192.** `canvas_y = core_y + 192`,
x untouched. `SC.CORE_W, SC.CORE_H = 1080.0, 600.0`.

* `SC.CONTENT_Y0, SC.CONTENT_Y1 = 76.0, 538.0`: the band the core really paints in
  (canvas 268 … 730, 14.0 % … 38.0 % of frame height). Y0 is the `83%` counter's box
  top; Y1 is the `150+ SKILLS` key's box bottom. The outro lives inside it (glyph top
  150, slot bottom 500). At k = 1 the lowest ink clears the caption pill's top (~787.7)
  by ~57 px.
* Every chapter is symmetric about x = 540 (ink extents: ch0 60 … 1020 with the
  counters, ch1 266 … 814, ch2 185 … 895, ch3 265 … 815, ch4 ~318 … 762). So
  `left = (1080 − 1080·k) / 2`.
* Seat the core so its CONTENT BAND is centred on your stage zone:
  `top = round(centre - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 * k, 2)`.
* The right counter (`500` / `INTERNAL TOOLS`, x 760 … 1020) sits at core y 194 … 312
  = canvas 386 … 504, above the rail band (canvas ≥ 576) on the split. On the cutout
  check it against your own stage-zone mapping; it is a counter, so keep it out of the
  x > 918 rail at y ≥ 30 % of the frame if your k and top put it there.

**GATE-SCALING.** Non-block gutters are authored at ≥ 24 core px: KAI under the toolbox
24, counters to toolbox 40, person to toolbox 80 (the connector spans it), toolbox /
person to week strip 42, 83% to the group 24, group to OF THE WORKFORCE 24, buildings to
ORGANIZATIONS 24, toolbox-2 ink to 150+ SKILLS ~28. The crowd figures are 34 px apart
(a series), the week cells 10 px (a series inside one element).

---

## 3. THE TIMELINE

`SC.CUE` carries every instant (word STARTS from `cuts/stripekai/transcript_tight.json`
unless marked `authored`, each inside its word's 1.0 s window). `SC.BEAT_EDGES` is the
plan's beat table; `SC.DUR = 35.82`.

| ch | t | on screen |
|---|---|---|
| 0 | 0.10–10.10 | the toolbox pops alone on the axis (0.10), the Stripe nameplate lands on its front (0.24); on "revealed" the wrench, screwdriver and hammer rise out of it (0.56, stagger 0.08); `KAI` under it (4.14); `1,000` left (7.10) + `SKILLS` (7.60); `500` right (8.72) + `INTERNAL TOOLS` (9.58) |
| 1 | 10.10–13.72 | KAI + counters fade; the toolbox slides right and shrinks to 0.8 (10.10, origin 0 0) — the ONE displacement; the person pops left (10.76); the terracotta line person → toolbox draws (12.22); the seven-cell week strip pops (12.30) and fills terracotta cell by cell (12.46, stagger 0.11); `1 WEEK` (13.20) |
| 2 | 13.72–20.56 | toolbox, line, strip and key fade; the person shrinks to 0.5 and walks into seat 0 (13.72, origin 0 0); the other eleven figures pop (13.80, stagger 0.035); `83%` above (15.34); ten figures fill terracotta, person first (15.40, 0.07 apart); `OF THE WORKFORCE` below (16.70); holds through "extremely interesting to see" |
| 3 | 20.56–24.40 | the group fades while the three office buildings pop INSIDE the erase (20.56); on "AI" a terracotta spark pops over each roof (22.54, 0.12 apart); `ORGANIZATIONS` (23.40) |
| 4 | 24.40–31.82 | buildings fade while the same Stripe toolbox pops back centred (24.40); on "loading" ten extra tools drop in and pile over the handle, two landing outside its sides (27.72, stagger 0.06); on "150" the body outline flips terracotta and six strain ticks burst from the top corners (28.48); `150+ SKILLS` (29.18); outline back to ink on "everyone" (30.00) |
| 5 | 31.82–35.82 | opaque rising sheet (31.82); the small toolbox glyph without the plate (32.30), rule (32.60), lockup (32.70) |

Every erase is a handover, never a blank (LAW 43 / LAW 45): the toolbox crosses seam 1,
the person crosses seam 2, the buildings pop inside the seam-3 erase, the toolbox pops
inside the seam-4 erase. The last board event (the outline back to ink) settles by
30.30, 1.52 s before the outro anchor.

---

## 4. THE FOUR BESPOKE OBJECTS — DO NOT REDRAW

`SC.BESPOKE` carries CORE boxes and the held instant of each. Self-checked at phone
size (405x720) by the design agent, v4 (no cold readers).

| i | object | t | core box | proof |
|---|---|---|---|---|
| 0 | an open toolbox | 3.00 | 360, 110, 720, 410 | `review/proof_stripekai/00.png` |
| 1 | a group of people | 16.40 | 185, 172, 895, 438 | `01.png` |
| 2 | three office buildings | 23.80 | 265, 88, 815, 420 | `02.png` |
| 3 | an overflowing toolbox | 30.20 | 306, 129, 774, 471 | `03.png` (outline flipped, as at 28.8) |

`04.png` is the builder figure alone (chapter 1), not a bespoke object. Map `core` boxes
through your own k and origin when you cut phone crops.

---

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 40**: ONE connector, `#conn-built`, person → toolbox. `SC.CONN_FROM =
  anchor_points(PERSON_BOX, 1, "right")` = (446, 210), `SC.CONN_TO =
  anchor_points(TB1_BOX1, 1, "left")` = (526, 210), level to 0 px. It is drawn at 12.22,
  AFTER the toolbox has finished its 10.10-10.56 move, against the MOVED box.
  `data-connect-to="toolbox"` + `data-overlap-ok`.
* **LAW 39 / 50**: six keys, each `data-label-for`: `KAI` below `toolbox`, `1 WEEK` below
  `week-strip`, `83%` ABOVE `crowd`, `OF THE WORKFORCE` below `crowd`, `ORGANIZATIONS`
  below `buildings`, `150+ SKILLS` below `toolbox-2`. All centred on x 540 = their
  host's axis. The two toolbox keys (KAI, 150+ SKILLS) sit the same way (below).
  The counters `1,000`/`SKILLS` and `500`/`INTERNAL TOOLS` are NOT labels of the toolbox
  (they carry no `data-label-for`); each number+unit pair is one `data-block`
  (`cnt-skills`, `cnt-tools`). If Gate 1's geometric weld warns `sidelabel` on them
  (it is a WARNING inside 60 px only; they sit 40 px off the toolbox box), that is the
  counter grammar, not a name beside its object.
* **LAW 41**: `SC.DECLARED_BLOCKS`, stamped as `data-block`. `#crowd` is a transparent
  container (`data-container`) holding eleven `.fig` divs; the person is a sibling
  element in the same block.
* **LAW 42**: `SC.LIFETIMES`. Chaptered board: every board mark has a finite window;
  only the four outro marks are anchors (`SC.SCENE_ANCHORS`). The longest board mark is
  `#toolbox`, 13.62 s = 38 % of the take.
* **LAW 38**: exactly ONE emphasis, `#toolbox-2 .tbbody` stroke → `rgb(221,114,89)` at
  28.48 and back to ink at 30.00. The strain ticks are part of the drawing (the strain),
  not emphasis. No `<circle>` tag anywhere; round shapes are two-arc paths.
* **LAW 51**: the tools, the plate and the overflow are INSIDE the toolbox element, and
  the fill flips are inside each figure, so they move with their object. Any lane that
  draws these must do the same.
* **THE GHOST RULE**: the connector declares `pathLength="100"`, rests at
  `stroke-opacity:0` and reveals 0.04 s after its draw starts.
* **HIDDEN-AT-0 SETS**: `#toolbox .plate`, `#toolbox .tl`, `#crowd .fig` and
  `#toolbox-2 .ov` are set to opacity 0 at t = 0 by `tl.set` (their HTML is visible so
  the proof harness can paint the settled state). Prime the timeline (progress 1 → 0)
  as Gate 1 does before you sample it.

---

## 6. THE POINTING CUE

None. `pointing_cues.py --vid stripekai`: "No pointing cue in this take";
`gen/_cues_stripekai.json` has `cues: []`; the prep `cues` marker agrees (cue_count 0).

---

## 7. WHAT THE CUTOUT OWNS

* The matte and stage-zone seating. At plan time `cut` (35.82 s, "model-authored keep
  ranges"), `plate` (over-wide, crop 2492x1780+577+256, scale_k 0.5056, face_dx 0.041 %),
  `prompt0` (wing_review true, the instrument abstained, no cut) and `cues` had landed;
  `track` said `running` (matanyone2) and no `ship` marker existed. The Astra matte step
  owns the selection and the matte. `plate_origin()` must read `left` from `plate_box`.
* `SC.CUTOUT_LOGO_LANES = ("claude", "claude-code", "chatgpt", "cursor", "slack", "notion")`,
  files in `SC.CUTOUT_LOGO_FILES` (relative to `assets/logos/`): the assistants and skill
  runners an internal AI platform plugs into plus the internal tools it reaches. Mixed,
  none repeated, never `stripe` (it is on the stage). `claude-code` is
  `coding-tools/claudecode-color.png`, the plain mascot (MARK IDENTITY), never the
  sticker. All seven files (stage + lanes) pass `cutout_depthfield.assert_cast_resolves`
  (checked 2026-09-23).
* Your own k and origin. The logo lanes fade in after the hook lands (after 0.90, when
  the tools have risen), never later.

## 8. WHAT THE WHITEBOARD DOES NOT DO

It does not import this module. It redraws the same argument in marker ink per beat
`whiteboard_version` in the plan: same toolbox with the Stripe wordmark pasted on its
front, same counters, the person + line + seven cells, the twelve figures with ten
hatched, the three buildings with sparks, the overloaded toolbox with its terracotta
retrace, same keys at the same words.

---

## 9. WHERE THIS MODULE DEPARTS FROM THE PLAN'S LETTER

1. The plan's `bbox` values are normalised canvas boxes; `SC.BESPOKE` carries the real
   CORE boxes and is authoritative for geometry.
2. The Stripe mark sits on a 204 x 96 authoring-unit nameplate (card tile, 3 px
   ink-alpha border, radius 18), not a 112 px square tile: the only Stripe file in the
   library is the wide wordmark (plan open question 2).
3. The plan's `stripe-plate` / `stripe-plate-2` are the `.plate` children of `#toolbox`
   / `#toolbox-2`, not separate ids; `sparks`, `overflow` and `strain` likewise are
   classes inside their objects (`.spk`, `.ov`, `.str`). Same windows as the plan.
4. The plan's counter ids `counter-skills` / `counter-tools` are emitted as
   `cnt-skills-num` + `cnt-skills-unit` and `cnt-tools-num` + `cnt-tools-unit`.

---

## 10. PROOF EVIDENCE

| what | where |
|---|---|
| phone-size crops, one object alone per 405x720 frame | `review/proof_stripekai/00.png` … `04.png` |
| tight crops | `review/proof_stripekai/NN_tight.png` |
| crop manifest | `review/proof_stripekai/proofs_seal.json` |
| composed chapter frames (GRAPHIC CHART clause 9) | `review/proof_stripekai/compose_{ch0,ch1,ch2,ch3,ch4a,ch4,outro}.png` and `*_phone.png` |
| the seal record | `review/artwork_pass_stripekai.json` |
