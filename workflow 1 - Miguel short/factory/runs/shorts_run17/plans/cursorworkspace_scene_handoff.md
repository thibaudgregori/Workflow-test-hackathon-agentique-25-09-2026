# cursorworkspace — SHARED LANE SCENE HANDOFF

**Written by the ARTWORK AUTHOR for the SPLIT author and the CUTOUT author.**
The plan is the contract (`plans/cursorworkspace_plan.json`); this file is the
convenience. If anything below disagrees with the plan, the plan wins and you
write your own note.

Read `plans/cursorworkspace_scene_notes.md` too: it lists the eleven places this
scene departs from the plan's letter, with the law, the arithmetic or the cold
read that forced each. **Six of them change what you will see when you seat this
scene** — the bridge's three arches, its waves, the chapter-1 erase at 11.46,
the four app keys' shared seat, the three chapter-0 keys that moved up, and the
settings card's filled title bar with a 152 x 60 switch.

The Reels **whiteboard does NOT import this module**: it redraws the same
argument as marker ink from the same plan. It should, however, read section 5
before it draws its own bridge and its own settings object — the same two
drawings that cost four rounds here will cost them there.

**THIS MODULE IS SEALED.** `review/artwork_pass_cursorworkspace.json` binds it to
six independent cold-read rounds of its two bespoke objects. No lane may redraw
it. If a reader refuses one of its objects on your round, that is a repair round
and it HAS an owner: take
`production.py scene-lock --run shorts_run17 --vid cursorworkspace --holder <your lane>`,
redraw, re-read cold over three rounds and re-run `artwork-pass`. "Not mine to
change" is not a terminal reason on a repair round.

---

## 1. THE MODULE

| | |
|---|---|
| path | `shorts_run17/gen/cursorworkspace_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import cursorworkspace_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| geometry gate | `SC.assert_geometry() -> dict` — **call it before you write a byte** |
| proof harness | `shorts_run17/gen/cursorworkspace_proof.py` (the page, the phone frames, the crops) |
| cold readers | `pipeline/cold_read.py dispatch` — the pipeline instrument, not a scene-local harness |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the WHOLE 21.532 s scene: html to drop inside one
`transform: scale(k)` wrapper, and a list of `tl.*` javascript strings to
concatenate into your own timeline tail. It authors nothing outside the core, it
reads no files, and it takes no format argument — every difference between the
two formats is in the PLACEMENT and in the `lockup` string.

The page must define the three eases the scene emits by name:
`SOFT = "power2.out"`, `SWING = "power2.inOut"`, `POP = "back.out(2.05)"`.

### `media` — the eight rasters the scene paints

```python
t = SC.MARK_SIDE_TILE                       # 56.0 — the chart's own 0.50 of a 112 px tile
media = {
  "_cursor_img":       CC.mark_img(LOGO_URL["cursor"],           "cursor",           t),
  "_ws_img":           CC.mark_img(LOGO_URL["google-workspace"], "google-workspace", t),
  "_gmail_img":        CC.mark_img(LOGO_URL["gmail"],            "gmail",            t),
  "_calendar_img":     CC.mark_img(LOGO_URL["google-calendar"],  "google-calendar",  t),
  "_drive_img":        CC.mark_img(LOGO_URL["google-drive"],     "google-drive",     t),
  "_sheets_img":       CC.mark_img(LOGO_URL["google-sheets"],    "google-sheets",    t),
  "_panel_cursor_img": CC.mark_img(LOGO_URL["cursor"],           "cursor",
                                   SC.MARK_SIDE_HEAD),          # 34.0
  "_row_ws_img":       CC.mark_img(LOGO_URL["google-workspace"], "google-workspace",
                                   SC.MARK_SIDE_ROW),           # 42.0
}
```

`CC.MARK_INK[key]` must be populated by `CC.measure_mark(key, src)` first, and the
`LOGO_URL` values must be page-relative (`assets/logos/<basename>`). The sizes are
**ink sides in CORE px** — do not rescale them for the cutout; the core's own
`scale(k)` carries them. `cursorworkspace_proof.py` has the whole block, staging
included, and it is the copy to lift.

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
* `SC.CONTENT_Y0, SC.CONTENT_Y1 = 98.0, 566.5` — the band the core DECLARES it
  paints in (**canvas 290 … 758.5** on the split). Y0 is READ AND WRITE's box
  top, the highest ink in the video; Y1 is the trough of the lowest water wave,
  the lowest. Both are REAL painted ink, not a reserved envelope, and
  `assert_geometry()` re-measures them off `RECTS` on every build.
* The composition **IS mirror-symmetric about x = 540** at every settled instant:
  axis error **0.00 px on all fourteen probes**. So `left = (1080 − 1080·k) / 2`.
* Seat the core so its CONTENT BAND — not its box — is centred on your stage
  zone's centre:
  ```python
  top = round(centre - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 * k, 2)
  ```
  Centring the 600-tall BOX is the wrong sum and a LAW 15 defect.

**GATE-SCALING (run 12).** Gate 1 measures canvas px and the cutout scales the
shared core by ~0.95, so a 16 core-px gutter arrives at 15.2 and is refused on
the cutout while passing on the split. `assert_geometry()` measures **all 66
concurrent non-block pairs** across fourteen settled instants and prints the
tightest; the whole board clears the 24 px AIM, not just the 16 px refusal:

| pair | core px | at k = 0.95 | at t |
|---|---|---|---|
| `key-cursor` ⟷ `read-arrow` | **27.92** | 26.52 | 5.10 / 5.30 / 6.30 |
| `key-ws` ⟷ `read-arrow` | 27.92 | 26.52 | 5.10 / 5.30 / 6.30 |
| `key-ws` ⟷ `key-readwrite` | 30.15 | 28.64 | 6.30 |
| `key-calendar` ⟷ `key-drive` | 36.00 | 34.20 | 9.90 |

**An arrow's ink box is the CHEVRON's extent (±16 px), not the shaft's (±4).**
`SC.ARROW_HALF` is that number. Measuring the shaft alone hides 8 px of real
ink and was what put the plan's own key seats 13.92 px off the read arrow. If
you re-derive anything about the arrows, re-derive this too.

**Declared blocks (`SC.DECLARED_BLOCKS`), exempt from each other's gutter
only.** Thirteen of them. Chapter 0 is ONE assembled drawing — the tiles STAND
ON the deck (gutter 0 by construction) and each arrow LANDS ON a tile's edge
(gutter 0 by law), so each arrow is declared in the block of the tile it leaves
AND the tile it reaches. `data-block` holds one value, so in the DOM the arrows
carry `data-overlap-ok` instead and their double membership lives in the module.

---

## 3. EVERY ASSET KEY IT RESOLVES

| registry key | file | where it lands | ink side (core px) |
|---|---|---|---|
| `cursor` | `assets/logos/coding-tools/cursor.png` | `#cursor-tile`, `#panel-cursor-tile` | 56 / **34** |
| `google-workspace` | `assets/logos/platforms/google-workspace.png` | `#ws-tile`, `#row-ws-tile` | 56 / **42** |
| `gmail` | `assets/logos/platforms/gmail-color.png` | `#gmail-tile` | 56 |
| `google-calendar` | `assets/logos/platforms/google-calendar.png` | `#calendar-tile` | 56 |
| `google-drive` | `assets/logos/platforms/google-drive.svg` | `#drive-tile` | 56 |
| `google-sheets` | `assets/logos/platforms/google-sheets.png` | `#sheets-tile` | 56 |

**THREE OF THESE DID NOT EXIST AT PLAN TIME AND THIS STAGE REGISTERED THEM**
(the plan's open question 1, and it was a procedure, not a decision):
`google-workspace`, `google-calendar` and `google-sheets` are now in
`assets/logos/registry.json` with full provenance, their files are in
`assets/logos/platforms/`, and `execution/rebuild_asset_catalog.py` has been
refreshed (2,309 assets indexed).

**MARK IDENTITY, and these are FILE choices, not design choices:**

* **`google-workspace` IS THE MARK GOOGLE WORKSPACE ITSELF WEARS.** It is the
  icon `workspace.google.com` declares in its own `<link rel="icon">`: the
  **gradient** Google G, 256 x 256, served by Google from gstatic for that
  property. Google publishes no single-glyph Workspace mark — *Google Workspace
  Logo.svg* is a 3995 x 512 wordmark and *Google Workspace product icons* is a
  horizontal strip of the individual app icons, and neither can sit in a 112 px
  tile without becoming a text pill (LAW 2) or a collage. So this is the
  PRODUCT's own icon under LAW 35, **not** a company fallback, and it is a
  deliberately different file from `google-g` (the flat four-colour G whose
  provenance is google.com / Search, which the plan correctly bans). The written
  key ABOVE the tile says GOOGLE / WORKSPACE — the same construction that let
  kimiwork put the `claude` mark under the written key ANTHROPIC.
* **THE FOUR APP MARKS ARE ONE GENERATION, ON PURPOSE.** Google shipped a
  refreshed Workspace icon family in 2026 and `workspace.google.com` serves
  `gmail_2026`, `drive_2026`, `calendar_2026` and `sheets_2026q3` today. The
  registry's own `gmail` and `google-drive` are the **2020** family and are
  consumed by other videos, so the two new keys were registered in the 2020
  family too. Four marks in one level row have to read as siblings, and a row
  that is half old-style and half new-style is a defect a still frame can see.
  Refreshing all four to 2026 is a deliberate registry task for someone who owns
  the registry, not a per-video choice — the finding is written into both new
  registry entries so it is not lost.
* **Marks are sized BY THEIR INK, never by their box.** Gmail's envelope is
  aspect 1.333, Calendar 1.000, Drive 1.093, Sheets 0.727, the gradient G 0.980.
  `mark_img`'s ink-area sizing is what makes the four-tile row read as equals at
  405 x 720; equal boxes would not.
* Tiles are the chart's own: **112 px, radius 18, 3 px `rgba(17,17,17,0.16)`
  border, `#FFFDF9` fill**. The panel's two inner tiles are the same grammar at
  smaller radii (`row-ws-tile` 84 px / r 14). The card's HEADER mark is
  deliberately **not** in a tile — see §5.

**THE DEPTH CAST IS YOURS, NOT THE SCENE'S.** The plan's `cast` /
`cutout_logo_lanes` are `claude-code, codex, copilot, notion, slack, airtable` —
Cursor's peer coding agents and the workspaces people connect them to. `cursor`,
`google-workspace`, `gmail`, `google-calendar`, `google-drive` and
`google-sheets` are deliberately ABSENT from it: they are this story's own
subject marks and they live on the STAGE. `claude-code` is the plain no-outline
mascot (`assets/logos/coding-tools/claudecode-color.png`), **never**
`claude-code-sticker`. You still own
`cutout_depthfield.assert_cast_resolves()` before a frame renders.

**THERE IS NO SOURCE CARD AND NO POST ANYWHERE IN THIS VIDEO.** The plan ran
`pointing_cues.py` itself and it returned **zero** cues
(`gen/_cues_cursorworkspace.json`). Nothing to answer, nothing to waive, and no
platform frame to get wrong. Do not invent one.

---

## 4. WHAT YOU MUST CHANGE TO SEAT IT IN THE STAGE ZONE

1. **`k`** = `(ZY1 − ZY0) / (SC.CONTENT_Y1 − SC.CONTENT_Y0)` off YOUR session's
   envelope (the content band is **468.5** core px tall, not the 600 px box);
   `top` from the `seat_core` formula in §2; `left = (1080 − 1080·k)/2`.
2. **`plate_origin()` MUST READ `left` FROM `matting/cursorworkspace/plate.json →
   plate_box`** and never compute `(1080 − box_w)/2`. The plan records the plate
   as over-wide by default for this run.
3. **Derive the caption clearance with the pill that RENDERS (114.59)**, never
   the frozen 108.2 seat constant. On the split the lowest ink is core 566.5 →
   canvas 758.5, which leaves **144.2 px** under the rendering pill's top at
   902.705, and 261.5 px above the seam at 960.
4. **NEVER OCCLUDE HIM.** The plan's arithmetic: his cap top sits at ~44 % of
   frame height (y ≈ 845) and the lowest ink is canvas 758.5, so nothing here
   comes near the silhouette and **nothing is ever declared `behind`** — but
   re-derive it from YOUR envelope, because your `top` is not the split's.
5. **If `shorts_run17/MATTES_FINAL.md` exists, the shipped v5 layers are consumed
   as they are** — no re-track, no re-selection, no repair pass, no Modal matting
   call of any kind. It did not exist when this stage ran.
6. **Declarations to keep.** The scene emits `data-block`, `data-label-for`,
   `data-connect-to`, `data-overlap-ok` and `data-bleed`; do not strip any of
   them. It emits **no `data-anchor`**, on purpose: this board is CHAPTERED
   (LAW 43's default), so LAW 42 wants a finite `t_to` on every mark and
   `SC.LIFETIMES` declares one for all 31 of them. The two arrows carry
   `data-overlap-ok` because they are supposed to touch what they join — which
   also removes them from Gate 1's `anchorline` and `cramp` checks, so
   `SC.assert_geometry()` is the only thing that sees LAW 40 and LAW 41 on this
   page. **Call it; do not trust the gate.**
7. **GLOBAL LAW 8 / the edge-fade guard.** Nothing in this core touches a frame
   edge (ink extents 208 … 872 at the widest instant, margins 208 both sides), so
   `cutout_core.guard_edge_fade` has no target inside the scene; your lane
   wrappers still need theirs. `#o-sheet` is the one deliberate bleed and it is
   declared `data-bleed`.
8. **THE POP-BEHIND.** The plan spends no beat on one. The three arrivals that
   could carry it are the chapter-1 tiles at 7.70 / 8.86 / 10.76; if you spend
   the format's best detail there, suppress the scene's own
   `popin("#<app>-tile", …)` and hand the seat to your device. Nothing else
   touches those elements before their erase.
9. **THE CUE TABLE IS RE-READ, NOT TRUSTED.** `SC.CUE` has 22 entries; ten of
   them are word STARTs read to the millisecond out of
   `cuts/cursorworkspace/transcript_tight.json` (`tileR` 2.639, `read` 4.500,
   `write` 5.239, `emph` 16.279, `outro` 17.319 …) and the rest are authored
   inside their own word's 1.0 s LABEL_WINDOW. Re-read the tight transcript and
   refuse to write on a mismatch — a re-cut would slide every gesture in the
   video and no geometry gate would notice.

---

## 5. THE PHONE TEST — WHAT IT COST AND WHAT IT CHANGED

Two bespoke objects, `SC.BESPOKE`, each with a HELD instant (never inside an
entrance) and its core box. Cut off the PAGE at 405 x 720 by
`cursorworkspace_proof.py`, then blind-copied under a random token and named by
**one independent `claude -p` per crop**, launched from `/tmp` on absolute
paths — no plan, no page, no transcript, no sealed key, no path naming the video.

**FINAL SET — six independent rounds, two reader models, twelve reads, ZERO
readers naming a different object:**

| # | intended | held t | phone px | what the readers said |
|---|---|---|---|---|
| 0 | an arch bridge | 2.30 | 249 x 67 | *bridge* · *arched bridge over water* · *bridge* · *bridge* · *arch bridge* · *bridge* — **6/6 sure** |
| 1 | a settings panel | 14.20 | 210 x 100 | *toggle switch* ×6 — **3/6 sure**, the three hedges all one reader model |

**It took four drawings and it changed two things.** The whole history is in
`review/proofs_cursorworkspace/history/` with the crop each reader saw, and the
losing drawings are still on disk as `crops/round{1..4}_*.png`. What you need
from it:

* **A STRAIGHT DASH UNDER A STRUCTURE IS AN UNDERLINE; A WAVE IS WATER.** The
  first bridge read *"arched bridge"*, **unsure**, with two straight ripple
  dashes. Three wavy strokes, one under each arch, and every read after that was
  sure — two readers volunteering *"over water"* unprompted. **If you draw water
  in this video, draw waves.**
* **A REPEATED ARCH IS WHAT MAKES *bridge* THE HEAD NOUN.** One shallow segmental
  arch between two legs is a bench at 249 x 67. Three near-semicircular arches on
  four piers is a bridge. The whiteboard should draw three arches too.
* **THE SETTINGS OBJECT IS THE SWITCH.** Twelve reads across four drawings named
  it *toggle switch* and nothing else — never *a receipt*, *a calculator*, *a
  keyboard* or *a card*, which are the plan's named failures. Growing the toggle
  from 96 x 40 to 152 x 60 and giving the card a **filled title bar with the
  Cursor mark PLAIN on it** (no tile of its own — run 16's finding: a rounded
  card inside a rounded frame is the shape readers hedge on) is what moved the
  confidence. **Draw the switch big and let it be the subject.**
* **THE SECOND, EMPTY CONNECTOR ROW WAS NOT DRAWN.** The plan offers it as a
  remedy; an anonymous plate in a row is LAW 29's own named defect, and the plan
  itself says to enlarge the toggle instead. If your lane wants a settings LIST,
  that is a repair round with the scene lock, not a quiet edit.
* **THE READER MODEL IS PART OF THE EVIDENCE.** The configured reader hit its
  usage cap mid-seal; the fallback (`opus`) hedged on the settings panel in every
  round, **including on a control crop of the connector row alone**
  (`review/proofs_cursorworkspace/diag/diag_row.json`). That control is what says
  the hedge is about UI mocks as a class, not about this drawing. A third model
  (`haiku`) returned *toggle switch* sure three times out of three. All six
  rounds are in the seal, hedges included.

`SC.BESPOKE` carries the final names and the held instants; feed it straight to
`phone_test_page.py --geom` / `phone_crops.py`. **The plan's own `t` values are
entrance-completion times and are NOT used** — a crop taken on the last frame of
an entrance judges the animation, not the object.

---

## 6. THE GRAPHIC CHART, PROVEN SIDE BY SIDE

`review/proofs_cursorworkspace/chart_comparison_run15_vs_cursorworkspace.png`
puts this scene's 6.30 s frame next to `shorts_run15/output/geminitools_split.mp4`
at 12.90 s.

Same cream ground `#F6F1EA`; same near-black `#141416` and the same single
terracotta `#C4573A`; the same JetBrains Mono 800 UPPERCASE key term above its
subject with smaller labels beside their tiles; the same 112 px tiles at radius
18 with a 3 px `rgba(17,17,17,0.16)` border and real registry marks sized by
ink; the same thin ink-line SVG drawings at stroke 5–13 with round caps, no
fills, no gradients, no shadows; the same terracotta connectors terminating on a
virtual rectangle; the same chassis mono outro lockup on the video's own themed
object. **A stranger files them under one channel because every constant in this
module's palette, type, tile and outro blocks was copied out of
`geminitools_scene.py` rather than chosen.** What is new is the metaphor and the
objects: an arch bridge over water, and a connectors page with one row and one
switch.

---

## 7. WHAT I LEARNED BUILDING IT (so you do not learn it twice)

1. **A DASH-DRAWN PATH RESTS AT `stroke-opacity="0"`, NOT `opacity="0"`.** The
   first build painted a completely invisible bridge: `draw()` animates
   `strokeOpacity`, so an element hidden with `opacity` never comes back. Every
   `.brk` path carries `pathLength="100"` and `stroke-opacity="0"`; the plain
   fades (`#panel-bar`, `#panel-stripe`) carry `opacity="0"` and use `fadeink`.
2. **OPACITY BELONGS IN THE `to`, NEVER ONLY IN THE `from`.** Inherited from the
   run-14 and run-15 handoffs and honoured here: every entrance is a `fromTo`
   whose `to` states `opacity:1`, because a later `to(..., {opacity:0})` records
   0 as its start value under the timeline PRIME (`progress(1); progress(0)`)
   that every seek-based tool performs, and `prerender_check` cannot see it. The
   bridge's own wrapper was the one place this bit.
3. **A CHAPTER THAT ERASES WHILE A KEY IS STILL ARRIVING WIPES A NAME
   MID-STROKE.** SHEETS finished at 11.32 against an erase at 11.30. Check every
   chapter's LAST entrance against its own `erase_at` before you trust the plan's
   seam times.
4. **AN ARROW IS AS TALL AS ITS HEAD.** Declaring a connector's box as the shaft
   is an 8 px lie per side and it is exactly the kind of lie a geometry gate
   cannot catch, because `data-overlap-ok` removes connectors from Gate 1's
   cramp check.
5. **SIBLING SEATS ARE EQUAL, AND THAT IS WHAT PUTS THE AXIS AT 540.** Four app
   keys at four different widths move the optical axis. One 140 px seat for all
   four, sized by the widest requirement (CALENDAR, 133.2 px of ink).
6. **A CHAPTERED BOARD DECLARES NO ANCHORS.** Every one of the 31 elements has a
   finite `t_to` in `SC.LIFETIMES`, and both chapter seams overlap their fade-out
   with the incoming object's entrance (ch0 fades 6.50 + 0.22 while the Gmail
   tile enters at 6.68; ch1 fades 11.46 + 0.22 while the card enters at 11.62),
   so the zone's ink never reaches zero and LAW 45's handover lands on a
   complete, nameable object **0.26 s and 0.22 s** after each erase completes.
7. **THE OUTRO GLYPH IS THE BRIDGE, DRAWN SMALL AND ONE STEP HEAVIER.** 300 x 79
   at (390, 96) core, stroke multiplier `k = 1.6`, so the 0.452 downscale lands
   at roughly the board's own optical weight. No third-party mark survives into
   the outro (the ATTRIBUTION law), and the whole exit screen is one centred
   layout on x = 540: glyph → rule → handle → `daily AI`.
8. **THE CAPTION PARTITION IS YOURS.** This take carries
   `as well as Google Sheets.` and the sign-off `and catch you in the next one`.
   Use `CAP.split_balanced(..., forbidden=<the board's printed keys>)` — the
   board prints CURSOR, GOOGLE WORKSPACE, READ AND WRITE, GMAIL, CALENDAR,
   DRIVE, SHEETS, WORKSPACE and CUSTOMIZED PAGE — and run
   `merge_function_only_beats()` over the whole beat stream before
   `assert_no_function_only_beat()`.
9. **LAW 47, REPORTED NOT PLANNED AROUND.** The plan records the cut's tail at
   0.252 s against the 0.20 s cap — 0.05 s of container-rounding overshoot. It is
   the cut's, not the scene's; the scene's last authored ink ends at 16.66 and
   the outro anchor is 17.319, so `assert_outro_clear()` has 0.66 s of margin.
