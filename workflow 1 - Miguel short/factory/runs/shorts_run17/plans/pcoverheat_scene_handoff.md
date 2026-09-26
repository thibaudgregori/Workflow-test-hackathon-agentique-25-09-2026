# pcoverheat — SHARED LANE SCENE HANDOFF

**Written by the ARTWORK author for the SPLIT and CUTOUT authors.** The plan is
the contract (`plans/pcoverheat_plan.json`); this file is the convenience. If
anything below disagrees with the plan, the plan wins **except** where this file
names a `DEVIATION` — those are the places the plan's letter was changed on
purpose, each with the law or the cold-read that forced it, and they are also in
`gen/pcoverheat_scene.py → DEVIATIONS` in machine-readable form.

**The whiteboard does NOT import this module.** It redraws the same argument as
marker ink on its own board, in the same four chapters, with the same objects
and the same keys — but it must use the **sealed** objects below, not the plan's
superseded ones (a speech bubble, not a text field; an arrow over a baseline,
not a browser and a tray). Its own drawing style is its own.

---

## 0. THE SEAL, AND WHY YOU MAY NOT REDRAW ANY OF IT

`review/artwork_pass_pcoverheat.json` binds this module and this file to a cold
read of every bespoke object in it. Six independent rounds, four objects,
**24 reads, zero readers naming a different object.**

| # | sealed object | what six independent readers called it | sure |
|---|---|---|---|
| 0 | **an open laptop** with heat coming off it | `laptop computer` ×3, `laptop` ×3 | 5/6 |
| 1 | **a download arrow** over its baseline | `download arrow` ×3, `download icon arrow`, `download icon`, `download arrow icon` | 3/6 |
| 2 | **a speech bubble** with the instruction inside it as ink | `speech bubble` ×6 | 5/6 |
| 3 | **a process list** | `table` ×3, `task manager …` ×3 | 3/6 |

**Two of the plan's four drawings did not survive the phone, and the readers are
why they changed:**

* **The plan's TEXT FIELD is now A SPEECH BUBBLE.** The authored field (a wide
  rounded input with a heavy chevron prompt glyph, a caret and terracotta
  word-runs) was read six times as `Terminal command prompt` / `pencil` /
  `command line terminal prompt` / `none — abstract chevron and dashes` /
  **`play button`** / `terminal command prompt with cursor`, at **0 of 6 sure**.
  Per STANDARD.md's run-15 rule two candidates were then built and read: the
  best refinement (the same field, narrower, ink-outlined, chevron removed) came
  back `cannot identify object` and **`thumbs up`**; the different metaphor — a
  speech bubble carrying the instruction as terracotta ink — came back
  `speech bubble`, **sure**, from every reader that has ever seen it. LAW 4 is
  untouched: what is inside the bubble is INK, never the spoken words.
* **The plan's DOWNLOAD KIT is now the canonical arrow over a baseline.** Four
  drawings were read for this one object. The browserless arrow *into an open
  tray* read right but hedged; with a filled head and a deeper tray three
  readers named it **`inbox` / `inbox tray`** — a tray you drop things into *is*
  an inbox. A cloud with an arrow was named **`rain` / `cloud with raindrop`**
  by two of six. The sealed drawing has no container to be an inbox and no cloud
  to rain.

If a reader of **yours** refuses one of these four, this is a repair round and
the module **has an owner**: take
`production.py scene-lock --run <run> --vid pcoverheat --holder <your lane>`,
redraw that one object, re-read it cold over three rounds, re-run
`artwork-pass`, and republish the module and this file with a note. *"Not mine
to change" is not a terminal reason on a repair round.* Do not fork a copy.

---

## 1. THE MODULE

| | |
|---|---|
| path | `shorts_run17/gen/pcoverheat_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import pcoverheat_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |
| proof harness | `gen/_pcoverheat_proof.py --out <run>/review/proofs --set seal\|compose` |

`build()` returns the WHOLE 37.16 s scene: html to drop inside one
`transform: scale(k)` wrapper, and a list of `tl.*` javascript strings to
concatenate into your own timeline tail. It authors nothing outside the core, it
reads no files, and it takes no format argument — every difference between the
two formats is in the PLACEMENT and in the `lockup` string.

### The CSS the core assumes its host defines
```css
.abs  { position:absolute; }
.mono { font-family:'JetBrains Mono',monospace; text-transform:uppercase; }
```
Nothing else. Both DOM chassis already ship both rules.

### `media` — the rasters the scene paints
```python
{"_codex_img":  CC.mark_img(LOGO_URL["codex"],         "codex",  SC.MARK_SIDE[0]),  # 62.0
 "_cowork_img": CC.mark_img(LOGO_URL["claude-cowork"], "cowork", SC.MARK_SIDE[1]),  # 74.0
 "_grok_img":   CC.mark_img(LOGO_URL["grok"],          "grok",   SC.MARK_SIDE[2]),  # 78.0
 "_x_mark":     <a 30 px INK X mark for the post card's header row>,
 "_post_shot":  <the <img> of the screenshot the @XFreeze post carried>}
```
`CC.MARK_INK[key]` must be populated by `CC.measure_mark(key, src)` first, and
the `LOGO_URL` values must be page-relative (`assets/logos/<basename>`). The
sizes are **ink sides in CORE px** — do not rescale them for the cutout; the
core's own `scale(k)` carries them.

### `lockup` — the outro's handle block
```python
CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W) \
  + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W)
```
It is seated inside the scene's own `#o-slot`. `handle_key` is the ONLY string
that differs between the masters: `"yt"` on the split, `"tiktok_ig"` on yours.

---

## 2. THE UNITS

**CORE px = the plan's CANVAS px with y shifted by −192.**

```
canvas_y = core_y + SC.CANVAS_OFFSET      # 192.0
canvas_x = core_x                          # every core x survives verbatim
```

* `SC.CORE_W, SC.CORE_H = 1080.0, 600.0`
* `SC.CONTENT_Y0, SC.CONTENT_Y1 = 94.0, 566.0` — the band the core DECLARES it
  paints in (canvas **286 … 758** on the split, the plan's own band to the
  pixel). Y0 is the top of `THREE APPS` and of the speech bubble; Y1 is the
  `OVERHEATING` key's box bottom, the lowest ink authored anywhere in the video.
  Both are REAL painted ink, not a reserved envelope, so there is no hidden
  slack here.
* The composition is **symmetric about x = 540 at every instant it is
  complete**, so `left = (1080 − 1080·k) / 2`. Ink extents 208 … 872, margins
  208 each side.
* Seat the core so its **CONTENT BAND — not its box** — is centred on your stage
  zone's centre:
  ```python
  top = round(centre - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 * k, 2)
  ```
  Centring the 600-tall BOX is the wrong sum and a LAW 15 defect.

**GATE-SCALING (run 12).** Gate 1 measures canvas px and the cutout scales this
core by ~0.95, so a 16 core-px gutter arrives as 15.2 canvas px and is refused
on the cutout while passing on the split. **Every concurrent non-block pair in
this scene is authored at ≥ 32 CORE px**; `SC.assert_gutters()` measures all 29
of them and raises before a byte of HTML is written. The tightest:

| pair | core px | at k = 0.95 |
|---|---|---|
| `download-kit` ⟷ `key-codex` / `key-cowork` / `key-grok` | **32.0** | 30.4 |
| `key-ask` ⟷ `process-list` | **32.0** | 30.4 |
| `key-codex` ⟷ `key-cowork` ⟷ `key-grok` | **32.0** | 30.4 |
| `key-overheating` ⟷ `post-card` | 40.0 | 38.0 |

**Declared blocks (`data-block`), exempt from each other's gutter only:**
`hot` = hot-laptop + heat-waves + key-overheating · `post` = the whole card and
everything it holds · `apps` = key-three-apps + the three tiles ·
`codex`/`cowork`/`grok` = each tile with its key · `install` = download-kit +
key-install · `ask` = prompt-field + key-ask + conn-ask-list + the five ink runs
· `list` = the window and everything inside it, plus HOT/RAM/CPU ·
`culprit` = key-culprit + close-x, welded to the row.

---

## 3. EVERY ASSET KEY IT RESOLVES

| registry key | file | where it lands | ink side (core px) |
|---|---|---|---|
| `codex` | `assets/logos/coding-tools/codex-color.png` | `#tile-codex` | 62 |
| `claude-cowork` | `assets/logos/ai-models/claude-cowork.png` | `#tile-cowork` | 74 |
| `grok` | `assets/logos/ai-models/grok.png` | `#tile-grok` | 78 |
| `x-logo` | `assets/logos/platforms/x-logo.svg`, in INK | `#post-header` | 30 |

**MARK IDENTITY, and these are FILE choices, not design choices:**

* **`claude-cowork.png`, the ORANGE mark** — never `claude-cowork-pale`, which
  is invisible on cream, and never `claude-code` / `claude-code-sticker`. The
  plan's open question 1 carries the transcript evidence that the spoken token
  is *Claude Cowork*: the raw Scribe pass of the same keeper take renders it
  `Claude Cowork` word for word, and a second abandoned take says it too. The
  written key reads **CLAUDE COWORK**. Merge caption tokens 30–32 into the
  single token `Cowork,` the same way the cut stage already merged `Groq → Grok`;
  if your lane cannot make that merge, build the visual as written anyway — a
  pill reading "Claude Code Work" beside a tile keyed CLAUDE COWORK is a
  near-miss, while the wrong logo is a real LAW 2 defect.
* **`grok` is the pick for Grok Build.** There is no Grok Build asset anywhere
  under `assets/logos/` (checked: ai-models, coding-tools, platforms,
  automation, shorts-factory-imports). Under LAW 35 the mark says WHAT KIND OF
  THING and the written key says WHICH ONE — the supergrokplus precedent
  (`shorts_run10/gen/supergrokplus_scene.py:617`). A drawn terminal glyph or a
  text pill in its place is never legal (LAW 2, LAW 33).
* **THE THREE MARKS ARE SIZED BY THEIR INK, NOT BY THEIR BOXES, AND NOT ONLY BY
  THEIR ASPECT.** `mark_img` equalises ink AREA across differing aspects; it
  cannot know that a glyph is sparse *inside* its own bounding box. Measured on
  the three files at alpha > 16: **codex-color covers 0.971 of its bbox,
  claude-cowork 0.322, grok 0.238.** Equalising painted area exactly would put
  grok at 113 px, wider than the 106 px padding box, so the correction is the
  fourth root of the coverage ratio, trimmed to leave a visible margin inside
  the tile (LAW 36): **62 / 74 / 78**, i.e. margins of 25 / 19 / 17 px. The
  plan's "scale Cowork ~1.35×" is the same instinct with one of the two sparse
  marks missed.
* All three tiles share ONE rounded-square treatment (112 px, radius 18, border
  3 px `rgba(17,17,17,0.16)`, fill `#FFFDF9`) — LAW 32, no odd one out.

### THE SOURCE CARD, AND THE ONE ASSET THIS MODULE CANNOT MAKE

`pointing_cues.scan` returns **one** cue on this take — `"like this guy"` at
**3.240 s** (`gen/_cues_pcoverheat.json`) — so LAW 37 binds and the card is not
optional. The card's chrome, its handle row, its three text lines and both
marker fills are **built by this module**. The one thing it cannot invent is the
photo the post carried, so `media["_post_shot"]` is a **required** slot:

* **Source:** `x.com/XFreeze/status/2084122084297359607` — the exact Source URL
  on this recording's Notion inbox row (`3b431704-6eeb-81bc-9ddf-cf4829d5dc2f`).
* **What to capture:** the image the post carried, a Grok Build session on a Mac.
* **THE CROP IS SCOPED, AND THE SCOPE IS DELIBERATE:** a title strip, the line
  `Verdict: Ghostty is the heat source`, and the metric row
  `CPU  ~700-830% (several full cores)`. The screenshot's next line,
  `#1 culprit: Ghostty (terminal)`, is **CROPPED OUT** — he does not say the word
  *culprit* until 30.219 s, and putting the payoff word on screen at 4 s is a
  LAW 24 peek-ahead of this video's own ending.
* **Aspect 2.1594 : 1** (e.g. 1192 × 552). The module paints it at width 564 /
  height 261.2 inside a 564 × 142 window that reveals only its top band, then
  grows the window to 596 × 276 at 3.86 s and the image with it. Both states
  paint the image at its own aspect, so the zoom is a real scale-up and never a
  stretch. Give the `<img>` `style="position:absolute;left:0;top:0;width:564px;
  height:261.18px;display:block"` and `data-asset`.
* **`SC.HL_VERDICT_FRAC` is a guess until you measure it.** It is the verdict
  line's box as fractions of the zoomed window, `(0.055, 0.375, 0.760, 0.135)`
  for the crop specified above. **Re-measure it against your actual capture** —
  one marker fill on one line, and the line has to be the one that carries the
  claim (LAW 38 rule 1, GLOBAL LAW 5).
* **NO METRICS CHROME ANYWHERE ON THE CARD** — no likes, no reposts, no views
  (GLOBAL LAW 3). The metric row *inside the screenshot* is the post's content,
  not engagement chrome, and it stays. The handle appears here and **nowhere
  else in the video** (the ATTRIBUTION law).
* The post's first clause is elided with the post's own ellipsis and nothing is
  added (plan open question 2); the trailing emoji is dropped because this
  factory's render harness has no emoji font and a tofu box on a source card is
  worse than no emoji.

**THE DEPTH CAST IS YOURS, NOT THE SCENE'S.** `SC.CUTOUT_LOGO_LANES` =
`cursor, copilot, opencode, antigravity, openclaw, github` — the category this
short's three named programs belong to, coding agents you install on your own
machine. `codex`, `claude-cowork` and `grok` are deliberately ABSENT: they are
this story's own subject marks and they live on the STAGE (a subject mark in the
depth field is the run-9 defect). Run
`cutout_depthfield.assert_cast_resolves()` before a frame renders; a mark that
reads as a hollow single-colour box crossed by both diagonals is refused as
ARTWORK, not as a missing file.

---

## 4. THE GEOMETRY, IN CANVAS px (the plan's own space)

`SC.canvas_rects_built()` returns this table at runtime and
`SC.assert_plan_geometry(plan)` checks it against the plan within 2 px, raising
on any deviation this module has not declared. **Build these rects and assert
them.**

| element | canvas rect | note |
|---|---|---|
| `hot-laptop` | 430, 392, 650, 536 | plan |
| `heat-waves` | 468, 300, 612, 380 | plan |
| `key-overheating` | 316, 700, 764, 758 | plan · 48 px / ls 2 · lowest ink in the video |
| `post-card` | 230, 296, 850, 660 | plan |
| `post-header` | 258, 308, 822, 356 | plan |
| `post-text-a/b/c` | 258, 374/412/450, 822, +32 | plan · JetBrains Mono 400, 24 px, sentence case |
| `post-inner-small` | 258, 498, 822, 640 | plan |
| `post-inner-zoom` | 242, 372, 838, 648 | plan |
| `key-three-apps` | 400, 286, 680, 330 | plan · 44 px / ls 1.0 |
| `tile-codex/cowork/grok` | 252/484/716, **342**, +112, **454** | **DEVIATION** — up 44 px |
| `key-codex/cowork/grok` | **208/440/672, 470, +200, 508** | **DEVIATION** — one size, equal seats |
| `download-kit` | **390, 540, 690, 700** | **DEVIATION** — 300 × 160 |
| `key-install` | **470, 712, 610, 750** | **DEVIATION** — seat widened |
| `prompt-field` (the bubble) | **310, 286, 770, 402** | **DEVIATION** — metaphor changed |
| `key-ask` | **452, 412, 628, 448** | **DEVIATION** — follows its host |
| `process-list` (ch 2) | **246, 480, 834, 756** | **DEVIATION** — 4 taller rows |
| `process-list-ch3` | **246, 300, 834, 576** | **DEVIATION** — same top edge, new height |
| `row-culprit` | **258, 480, 822, 524** | **DEVIATION** — row 3 of 4 |
| `close-x` | **770, 486, 802, 518** | **DEVIATION** — inside the row |
| `key-culprit` | **408, 608, 672, 658** | **DEVIATION** — follows its host · 36 px |
| `emph-culprit` | — | **DEVIATION** — no DOM geometry; the border flip is the boxing |

The list's interior, in **list-local** px (the window's own origin):
title strip 0…44 with `PROCESSES` at 28 px left-aligned at x 22 · hairline at 44
· header band 44…84 carrying HOT / RAM / CPU at 28 px, each centred on its own
column · four rows at pitch **48**, height **44**, from y 84, separated by
hairlines · each row: a 30 px glyph square at x 22, a name bar at x 64, three
56 × 30 measuring cells at x 268 / 352 / 436, and a 32 px close-button seat at
x 512. Row 3 (zero-based **2**) is the culprit; its three bars are the longest
in all three columns, planted silently in beat 5.

**The one connector.** `data-connect-to="process-list"`, `data-overlap-ok`,
terracotta, no arrowhead. It leaves the speech bubble 4 px under its own tail
tip at core **(376, 212)**, drops to core y **272** — 16 px below `TELL THEM`'s
box bottom, so it never crosses printed type (LAW 41 clause 2) — runs right to
x 540 and terminates at `anchor_points(LIST_BOX_CH2, 1, "top")` = core
**(540, 288)**, a point on the target's VIRTUAL bounding rectangle, AT the edge
and not on top of the box (LAW 7 / LAW 40). It draws 17.10–17.50 and the list it
reaches draws 17.44–18.50, so the stroke never precedes its node by more than a
stroke.

**The one move.** The list is the only mark carried across a chapter seam. At
**25.10** it translates `y` by **−180** in 0.30 s: same size, same rows, nothing
reflowed, no ink redrawn. That is LAW 45's own sanctioned handover and the
reason `process-list` carries `data-anchor="1"`.

---

## 5. WHAT YOU MUST CHANGE TO SEAT IT IN THE STAGE ZONE (cutout)

1. **`k`** = `(ZY1 − ZY0) / (SC.CONTENT_Y1 − SC.CONTENT_Y0)` off YOUR session's
   envelope — the content band is **472 core px** tall, not the 600 px box;
   `top` from the `seat_core` formula in §2; `left = (1080 − 1080·k)/2`.
2. **`plate_origin()` MUST READ `left` FROM `plate.json → plate_box`** and never
   compute `(1080 − box_w)/2`. **This session's plate IS over-wide**:
   `stages.plate` reports crop `3258x1810+16+238`, `scale_k 0.497238`,
   `head_px_on_canvas 451.8`, `face_dx_pct 0.041`,
   `visible_window_drift_master_px 0.0`, **`overwide_applied true`**, shipped
   1782 × 990.
3. **Derive the caption clearance with the pill that RENDERS (114.59)**, never
   the frozen 108.2 seat constant. The lowest ink here is canvas **758** against
   the split's RENDERING pill top at `960 − 114.59/2 = 902.705`, i.e. **144.7 px**
   of clearance.
4. **NEVER OCCLUDE HIM.** His cap top sits at ~44 % of frame height (y ≈ 845)
   and the lowest ink is 758, so nothing in this scene comes near the silhouette
   and **no element should ever need a `behind` declaration** — but re-derive it
   from YOUR envelope, because your `top` is not mine.
5. **THE MATTE.** `shorts_run17/MATTES_FINAL.md` governs. While it exists, every
   `matting/pcoverheat/matte_pcoverheat_v5_{cut,rim,alpha}.webm` and its
   `plate.json` / `selection.json` are approved as they are: no re-track, no
   re-selection, no repair pass, **no Modal matting call of any kind**. The only
   Modal calls in this run are the renders. `stages.selection` is `approved` /
   `reviewed` with `edits []`; `stages.ship` is ok, 929 frames at 1782 × 990,
   25 fps, soft alpha, 7 px rim. Stamp the staged matte **by content** (path +
   size + mtime), never by name.
   **The wing review is YOURS**: `stages.prompt0` reports `wing_review true`,
   `wings_source "MEASURED on this plate's frame 0"`, `wing_left/right null`,
   `wing_cut_applied false`, `removed_px 0` — the instrument ABSTAINED rather
   than guessed. Look at
   `matting/pcoverheat/prompts/kf_overlay_00000.png` and, if a headrest wing
   sits inside the green prompt, measure its inner column and pass an explicit
   `wings` block. The protrusion gate inside `ship.py` is the net.
6. **Declarations to keep.** The scene emits `data-anchor`, `data-block`,
   `data-label-for`, `data-connect-to`, `data-overlap-ok`, `data-container`,
   `data-asset` and `data-bleed`; do not strip any of them. `#o-sheet` is the one
   deliberate bleed.
7. **THE POP-BEHIND.** The plan spends no beat on one. If your format's best
   detail belongs anywhere here it is on the three tile arrivals (8.38 / 9.14 /
   10.06) — suppress the scene's own `popin("#tile-…")` and hand the seat to the
   tile; nothing else touches those elements before the chapter erase at 13.65.
8. **GATE 1 ONLY SEES THE DIRECT CHILDREN OF A CLIP.** This format wraps the
   whole scene in one `#core` div, so `check_layout` measures one box. Every
   spacing, label and anchor law on this page is proved by the generator's own
   asserts — carry `SC.assert_gutters()` and `SC.assert_plan_geometry()` into
   your build. **A green Gate 1 on this shape is not evidence about geometry.**

---

## 6. WHAT I LEARNED BUILDING IT (so you do not learn it twice)

1. **THE COLD READER IS A STOCHASTIC INSTRUMENT, AND THIS RUN MEASURED IT
   AGAIN.** On the *byte-identical* crop `29c5146a…`, the same configured reader
   answered `download icon` **sure** and, minutes later, `download icon`
   **unsure**. On the identical list crop `bd4317293c…`, twelve reads split
   `data table` / `table` / `process table` / `spreadsheet` / `task manager …`
   **and** `computer monitor` ×3. Never gate a binary on one draw, and never
   re-read a drawing until it passes — the fix is always the drawing.
2. **THE CONFIGURED READER MODEL WAS OVER ITS USAGE LIMIT FOR THIS ENTIRE
   SESSION**, and `cold_read.py dispatch` exits non-zero and records
   `dispatch_failures` when that happens, which is exactly right — those rows are
   refused rather than scored. The six seal rounds therefore alternate two other
   session-capacity models via `--model`: `opus` (s1/s3/s5) and `haiku`
   (s2/s4/s6), and **both families count in every scoring row**. If you dispatch
   your own lane's readers and get `You've reached your … limit`, pass `--model`
   rather than scoring an empty read. Note the systematic difference so you can
   read your own results: the `opus` reader hedges on anything that looks like
   UI — it marked `laptop computer` *unsure* on a crop five other readers called
   *sure* — while the `haiku` reader is decisive and is the one that caught
   `mailbox`, `play button`, `thumbs up`, `inbox` and `rain`. Every one of those
   five findings forced a redesign, so neither model was picked for being
   agreeable.
3. **A UI CONTROL IS A BAD ANSWER TO "NAME THE EVERYDAY OBJECT".** The reader's
   prompt asks for an everyday object; a text field, a toolbar or an input can
   never answer it well however cleanly it is drawn. When a beat's meaning can
   be carried by a household shape — a bubble, a laptop, an arrow — draw the
   household shape. That single change took object 2 from 0/6 sure to 17/17 reads
   naming it correctly.
4. **A CONTAINER GETS NAMED INSTEAD OF ITS CONTENT WHEN THE CONTAINER IS THE
   LOUDEST THING.** Ruling the process list with MUTE row and cell borders made
   three readers call the whole object a **computer monitor** — they named the
   bezel, not the rows. The sealed list separates its rows with **hairlines** on
   a card body, and the loudest ink inside it is the measured bars.
5. **THE EMPHASIS NEEDS SOMETHING TO LAND ON.** The DOM lane's boxing is the
   row's own border flipped to terracotta, and the row has no visible border, so
   it carries a **2 px fully transparent** border that the flip animates. That is
   invisible until 28.96, adds nothing to any gutter, and keeps the row a
   background-bearing div — which Gate 1 can never read as an emphasis outline
   (`bg = backgroundColor !== transparent || borderTopWidth > 0`).
6. **NO `<circle>` ANYWHERE.** Gate 1's `_lring` returns true on the TAG whatever
   the fill, and LAW 38 rule 3 has no legal use for a ring in this video. The
   close button is a rounded SQUARE with an X through it.
7. **OPACITY BELONGS IN THE `to`, NEVER ONLY IN THE `from`.** Every entrance in
   this module is a `fromTo` whose `to` states `opacity:1`, because a later
   `to(..., {opacity:0})` records 0 as its start value under the timeline PRIME
   (`progress(1); progress(0)`) every seek-based tool performs — and Gate 1 drops
   any atom under 0.15 opacity, so an invisible element reads as an absent one.
8. **THE GHOST RULE.** Every dash draw-on rests at `stroke-opacity 0` and reveals
   one frame (0.04 s at 25 fps) after the draw starts: Skia paints a round
   linecap at progress 0, and an "un-drawn" path is otherwise a visible dot.
9. **THE PLAN'S OWN GUTTER FLOOR IS THE BINDING CONSTRAINT IN CHAPTER 1.** Three
   200 px key seats, a 32 px gutter between them and a 32 px gutter down to the
   download kit is what forced the tiles up 44 px; there is no arrangement of
   the plan's original rects in which `GROK BUILD` fits its own box at the type
   size its siblings use.
10. **THE PROOF HARNESS IS REUSABLE.** `gen/_pcoverheat_proof.py --set seal`
    paints this module's own ink at the split's placement, downscales the frame
    to 405 × 720 and cuts each bespoke object out alone with `phone_crops`'
    arithmetic — no project and no render needed. `--set compose` paints the four
    chapters' finished states in the top zone with the real marks resolved
    through `cutout_core.mark_img`, which is also how the media contract in §1
    was verified. Use it before you spend a Modal render.

---

## 7. THE PROOF EVIDENCE ON DISK

| what | path |
|---|---|
| the seal | `review/artwork_pass_pcoverheat.json` |
| the scoring, one judgement per read | `review/artwork_scores_pcoverheat.json` |
| the six seal rounds | `review/phone_reader_pcoverheat_artwork_s{1..6}.json` |
| every superseded round and candidate pair | `review/phone_reader_pcoverheat_artwork_{round1..3,r2a..c,r3a..c,r4a..c,r5a..c,f1..f6,cand,cand2,cand2b,cand3_*,cand4_*}.json` |
| the blind copies the readers actually saw | `review/cold/<tag>-<token>/NN.png` |
| the sealed crops, at 405 × 720 phone pixels | `review/proofs/crop_seal_0{0..3}_*.png` |
| the four composed chapter frames | `review/proofs/compose_ch{0..3}.png` |
| this scene beside a run-15 frame | `review/proofs/chart_compare.png` |

---

## 8. REPAIR ROUND — 8 September 2026, held by the SPLIT (YouTube) AUTHOR

`production.py scene-lock --run shorts_run17 --vid pcoverheat --holder "split
(YouTube) author"` was taken before a byte moved, and the module was republished
and re-sealed under it. **Nothing about the four sealed metaphors, the palette,
the geometry, the cues, the lifetimes or the plan rects changed.** Three
STATE bugs did — each of them a thing that made the built video wrong in a way
no still proof of the artwork stage could see, because the seal proofs render
every object with `hidden=False` on its own page and the bugs all live in the
hidden->visible transition.

**1. The whole source post was painted from frame 0.** `post_block` gave the
`hidden` opacity to `post-card` and to nothing else, so `post-header`,
`post-hair`, `post-text-a/b/c` and `post-inner` had no initial opacity at all.
A `fromTo` with `immediateRender:false` does not back-fill a from-value the
playhead has not reached — this module's own lesson 6.7, applied to the one
block that missed it — so @XFREEZE's handle, the post's three lines and the
screenshot were on screen from 0.00 s. The phone crop of bespoke object 0 came
back with the post's text showing straight through the laptop at t = 1.90.
Every child now takes `o`.

**2. Bespoke object 1 was never painted at all.** `download_bar_svg` hides its
three paths with `opacity="0"` — it has to, because the arrowhead is a FILLED
triangle and `stroke-opacity` cannot hide a fill — but the scene reveals it with
`draw()`, which animates `strokeDasharray` / `strokeDashoffset` /
`strokeOpacity` and never touches `opacity`. Nothing ever returned those paths
to 1. **The download arrow does not exist in any frame of the video as sealed**,
and its phone crop at its own held instant 13.30 was an empty cream rectangle.
`build()` now runs `fadeink("#download-kit .dlk", CUE["dlkit"], 0.26,
stagger=0.06)` beside the draw, exactly as `#hot-laptop .lpk` does. Same cue,
same duration budget, no new element.

**3. The same three paths carried no `pathLength`.** `draw()` writes
`strokeDasharray:100`; on a baseline 220 user units long that is 100 on, 100
off, 20 on, so the finished baseline painted as a bar, a hole and a stub. It was
invisible while the paths were stuck at opacity 0 and appeared the moment the
ink came back. Both other `draw()` targets in the module (`.hwk`, `.sline`)
already declared it; these three now do too.

**And one legibility repair, which is a drawing change and is declared as one.**
The sealed arrow used x 80..220 of its own 300-wide authoring box, so at the
phone's 0.375 it was 47 px of ink inside the 112 px crop its declared rect
reserves — 42 % of the width, the rest cream. It is redrawn at the size the rect
always claimed (shaft `M150 8 L150 78` sw 54, head `M52 70 L248 70 L150 134 Z`,
baseline `M40 150 L260 150` sw 18): the SAME shape, the same proportions, the
same tip-to-baseline gap, larger. **`DL_BOX` does not move**, so no gutter, no
label seat, no plan rect and no `DEVIATIONS` entry changes, and
`assert_gutters()` / `assert_plan_geometry()` both still pass unchanged.

### What the cutout author must do about it

Nothing except **rebuild from this module**. Its `build()`, its entry points,
its units, its asset keys, its placement formulae and its declarations are all
unchanged. The seal was re-run: `review/artwork_pass_pcoverheat.json` now binds
this module over six fresh independent rounds on the SAME panel the first seal
used (three `haiku`, three `opus` — see section 6 clause 2), scored in
`review/phone_scores_pcoverheat_split.json`. On the repaired drawings the panel
returns 12 of 12 haiku reads `sure` and 6 of 12 opus reads `sure`, with **one**
answer in the whole panel naming a different object (`toaster oven` for the open
laptop, once, unsure).

### And the one thing this lane measured that section 3 could not

`SC.HL_VERDICT_FRAC` is still the artwork stage's stated GUESS and it is still
wrong for any real capture — the module keeps it, because the handoff's own
instruction is that each lane re-measures it. **The capture now exists**:
`assets/source_pcoverheat/post_shot_pcoverheat.png` (1775 x 822, aspect
2.159367, sha256 in `post_shot_pcoverheat.json`), fetched through
`pipeline/prep/sourcelib.fetch_source` against the X API from the exact Source
URL, and the measured verdict-line box on THAT crop is
**`(0.09070, 0.83455, 0.35944, 0.04501)`**. Read it from
`post_shot_pcoverheat.json → hl_verdict_frac` and assign
`SC.HL_VERDICT_FRAC` in your own process, as the split does; do not re-crop and
do not re-fetch.

**The crop is one item short of section 3's contract and the shortfall is a
LAW, not a choice.** Section 3 asks for a title strip, the `Verdict:` line AND
the `CPU ~700-830%` metric row, while also requiring that
`#1 culprit: Ghostty (terminal)` be cropped out. In the source photo the culprit
line sits BETWEEN the verdict line (ink rows 704-731) and the metric table (CPU
row at ~1074) and spans the same x range as both, so **no rectangle contains the
verdict line and the CPU row without containing the payoff word**. LAW 24 is the
binding half; the metric row is the wish. The crop keeps the macOS window's
title strip, the session header, the task line, the user's own prompt bubble and
the `Verdict:` line — which is also the highlight's target and the claim the
card exists to carry — and stops 22 px above the culprit line's first ink.
