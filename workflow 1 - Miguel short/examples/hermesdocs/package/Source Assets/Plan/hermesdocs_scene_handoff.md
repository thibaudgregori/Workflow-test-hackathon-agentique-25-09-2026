# hermesdocs — SHARED LANE SCENE HANDOFF

**From the design agent, for the SPLIT author and for the CUTOUT author.** The plan
(`plans/hermesdocs_plan.json`) is the contract; this file is the convenience. If they
disagree, the plan wins. Neither lane redraws anything in this module: it is sealed
(`production.py seal`, production v4), and a lane that builds on a changed module is
refused.

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/hermesdocs_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import hermesdocs_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_hermesdocs_proof.py` (renders the real timeline, crops, frames, sheet, connector measurement) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the whole 28.28 s scene: html to drop inside ONE
`transform: scale(k)` wrapper (`transform-origin: 0 0`) and a list of `tl.*` strings to
append to your own paused GSAP timeline `tl`. It reads no files and takes no format
argument. Eases are string literals (`"power3.out"`, `"back.out(2.05)"`,
`"power2.inOut"`, `"power2.in"`). The page must give `.abs{position:absolute}` and
`.mono{font-family:'JetBrains Mono';text-transform:uppercase}` (the chassis already do).

### `media`: two rasters

```python
for key, rel in SC.LOGO_FILES.items():            # relative to ~/Documents/Workspace/assets/logos
    CC.MARK_INK[key] = CC.measure_mark(key, LOGOS / rel)
media = {
  "_hermes_img": CC.mark_img(<nous-girl-line src>, "nous-girl-line", SC.HERMES_MARK),  # 74, the Hermes tile
  "_fc_img":     CC.mark_img(<firecrawl src>, "firecrawl", SC.FC_MARK),               # 60, the Firecrawl tile
}
```

Files (MARK IDENTITY, named, never guessed):
* `nous-girl-line` = `ai-models/nous-girl-line.png`: Hermes is the Nous girl line art,
  NEVER the Hermes "H" glyph (`automation/hermes-agent.png`), Miguel's standing rule.
* `firecrawl` = `tool-web-icons-20260914/firecrawl-product.png`: the orange flame. It is in
  the central library but not a `registry.json` key; the factory addresses marks by path.
* AnyDoc has no mark of its own (github.com/firecrawl/anydoc uses Firecrawl branding): it
  is the drawn PDF page with ANYDOC written under it.

Both pass `cutout_depthfield.assert_cast_resolves` (`review/proof_hermesdocs/proofs.json`).
No source post: `pointing_cues.py` returned 0 cues.

### `lockup`

```python
CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W) \
  + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W)
```
seated inside the scene's `#o-slot` (core top 250). `handle_key`: `"yt"` on the split,
`"tiktok_ig"` on the cutout.

## 2. THE UNITS

**CORE px = canvas px with y − 192** (`SC.CANVAS_OFFSET`); x verbatim. Core is
`SC.CORE_W x SC.CORE_H = 1080 x 600`.

* Declared content band `SC.CONTENT_Y0, SC.CONTENT_Y1 = 60, 544` (canvas 252..736): the
  LOCALLY key term's top to the CONFIDENTIAL / ZERO RISK key's box bottom. Chapter 2's
  lowest ink is OPEN SOURCE at 502. Clears LAW 30's top 10 % and sits ~50 px above the
  split's caption pill top.
* Every composed state is centred on x = 540: safe alone 380..700 (hook); with the
  sources 244..838 (tiles 244..356, safe shifted +74 to 454..774, open door slab to 838);
  with the cloud ~222..868 (safe shifted +160 to 540..860, hinges to 868); the page alone
  440..640; page + Firecrawl 319..761.
* **The scene moves its own objects** (`x` tweens on `#safe`, `#pages`, `#hermes`,
  `#key-conf`, `#key-zero`, then `#bigpage`, `#pdf-tag`, `#key-anydoc`, `#key-os`). These
  are LAW 19 displacements on spoken words; do not re-tween `x` on them in a lane.
* **Cutout seating:** `left = (1080 − 1080·k) / 2`,
  `top = round(stage_centre − (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 · k, 2)`, with k from
  YOUR matte envelope so the band (484·k tall) clears his crown. The widest state is the
  cloud beat (~222..868) and the sources beat (244..838): at k ≤ 1 both stay inside the
  frame. Every inked atom must clear the silhouette envelope (never occlude him).
* Tightest non-block gutters (core px): LOCALLY bottom (118) to the safe top (160) 42;
  source tile to safe 98 (the arrows fill it); BUSINESS key bottom (316) to the client tile
  top (356) 40; building/client column to CONFIDENTIAL are x-disjoint; FIRECRAWL (341) vs
  ANYDOC (418) are x-disjoint. Anything closer is inside a declared block
  (`SC.DECLARED_BLOCKS`, stamped `data-block`).

## 3. THE TIMELINE (`SC.CUE`, word starts from `cuts/hermesdocs/transcript_tight.json`)

| t | event |
|---|---|
| 0.10 | "Hermes": the safe body draws, ALONE and centred (LAW 19/20 hook) |
| 0.36 | door, dial, handle, hinges, feet appear |
| 0.44 | "Agent": the Hermes (Nous girl) tile drops LEFT of the safe |
| 2.22 | "privacy.": the dial turns −270° (0.60 s): locked |
| 2.88 | "Now": the door collapses about its right edge; the open slab swings out (3.08–3.40) |
| 3.30 | "read": the Hermes tile moves INTO the safe (0.46 s) |
| 3.70 | "documents": a page pops in beside him |
| 4.50 | "locally,": **LOCALLY** across the top (first type, 48 px, LAW 9) |
| 7.70 | "confidential": CONFIDENTIAL under the safe |
| 9.62 | "business": the safe and its contents slide +74; building tile 9.82, BUSINESS 9.88, arrow 10.08, second page 10.32 |
| 10.46 | "clients": client tile, CLIENTS 10.72, arrow 10.92, third page 11.16 |
| 11.30–11.60 | "and": sources, labels and arrows leave |
| 11.86–12.80 | "Hermes": the Hermes tile's border flips terracotta (back 12.80–13.04) |
| 13.18 | "now": the slab folds away, the door swings shut (13.34–13.68) over Hermes and the pages, the dial turns back (13.68) |
| 14.12 | "zero": the safe outline flips terracotta and holds; CONFIDENTIAL leaves; ZERO RISK 14.22 |
| 15.28 | "data": the safe slides to +160; the cloud draws on the left (15.38) |
| 15.70 | "actually": the terracotta line safe -> cloud draws |
| 16.28 | "leaking": a terracotta X on the line (two strokes, 0.12 apart) |
| 16.88–17.18 | "They": chapter 1 leaves (fade up 14 px) |
| 16.92 | the big PDF page outline draws, complete 17.14; lines and PDF tag by 17.34 (LAW 45) |
| 18.00 | "AnyDoc,": ANYDOC under the page |
| 19.72 | "open": OPEN SOURCE under ANYDOC |
| 20.44 | "PDF": the PDF tag's border flips terracotta (holds) |
| 21.00–21.80 | "analyzer": the scan bar sweeps top to bottom; each line turns grey -> ink as it passes; bar fades 21.80 |
| 21.78 | "built": page, tag and labels slide −121 |
| 22.34 | "team": the Firecrawl tile drops on the right |
| 22.70 | "over": the terracotta line page -> tile draws |
| 23.18 | "Firecrawl.": FIRECRAWL under the tile |
| 23.88 | "Now": opaque rising sheet (0.46 s); board cleared 24.36; outro safe glyph 24.38, rule 24.68, lockup 24.78 |

Beat edges `SC.BEAT_EDGES`; chapters `SC.CHAPTERS` / `SC.BOARD_CHAPTERS`; `SC.DUR = 28.28`.

## 4. THE BESPOKE OBJECTS (`SC.BESPOKE`, core boxes, held instants)

| i | name | t | core box | own-eyes check at 405x720 |
|---|---|---|---|---|
| 0 | locked steel safe | 1.60 | 372, 160, 708, 482 | `review/proof_hermesdocs/00.png`: a safe with a combination dial, a handle bar, hinges, two feet |
| 1 | open safe documents | 8.60 | 380, 148, 764, 482 | `01.png`: the same safe, door swung open on the right, the Nous girl tile and a page with folded corner inside |
| 2 | scanned PDF page | 21.50 | 420, 130, 660, 400 | `02.png`: a page with a folded corner and a PDF tag, a terracotta bar crossing it, the lines above it black and below it grey |

None is on the refused UI-glyph list (cylinder, gear, bell, magnifier); the safe is a
physical safe, not a padlock icon. The cloud in beat 3 is a supporting prop, not a
bespoke object. Map `core` through your own k/origin for any crop.

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 39 / 50**: every name BELOW what it names, one size (28 px / 44 px row):
  CONFIDENTIAL and ZERO RISK `data-label-for="safe"` (same seat `SC.SAFE_KEY_BOX`, moving
  with the safe); BUSINESS / CLIENTS under their tiles; ANYDOC and OPEN SOURCE
  `data-label-for="bigpage"`; FIRECRAWL `data-label-for="fc"`. LOCALLY is the key term.
* **LAW 40 / connectors touch what they join**: `#arrows` (`arw-0`, `arw-1`,
  `data-connect-to="safe"`): tile outer right edge (356, 208 / 412) -> arrowhead tip on the
  safe's outer left edge = `anchor_points(SC.SAFE_BOX_S1, 2, "left")` = (454, 208 / 412).
  `#leak` (`leak-l`, `data-connect-to="safe"`): cloud outer right (382, 322) -> safe outer
  left (540, 322). `#fcwire` (`fc-l`, `data-connect-to="fc"`): page outer right (519, 265)
  -> Firecrawl tile outer left (649, 265). Measured in the DOM by the proof harness:
  **0.0 px gap at all eight ends**, each on a straight edge clear of the corner radius
  (`proofs.json -> connectors`, verdict PASS). At a cutout k they scale with the core.
* **LAW 41**: `data-block` = `safe` (body, door, slab, Hermes tile, pages, both safe
  labels), `src-biz`, `src-cli` (tile + label), `cloud` (cloud + leak line + X), `page`
  (page, tag, scan bar, ANYDOC, OPEN SOURCE), `fc` (tile + label).
* **LAW 42 / 43**: two chapters; every mark leaves with its chapter (`SC.LIFETIMES`); the
  safe is on screen 60 % of the take and exits at 17.18. Only the outro atoms carry
  `data-anchor="1"`.
* **LAW 38**: border flips on DRAWN objects only: `#hermes` borderColor (11.86), the safe
  body stroke (14.12), `#pdf-tag` borderColor (20.44). No ring, ellipse, circle tag or
  highlight; the dial, knob and client head are two-arc paths.
* **LAW 45**: the chapter-2 page outline is complete at 17.14, inside the erase.
* **LAW 51**: the door, slab and dial rotate/scale about their own `svgOrigin` (set by the
  module); the Hermes tile and pages move with the safe via the module's own `x` tweens.
* **Ghost rule**: safe body, cloud, page edge/fold, lines, wires and the X declare
  `pathLength="100"`, rest at stroke-opacity 0 and reveal one frame after the draw starts.

## 6. THE POINTING CUE

None (`gen/_cues_hermesdocs.json`, `cues: []`). Nothing to raise, nothing to waive.

## 7. CAPTIONS (all three lanes)

The tight transcript is clean. Spell "AnyDoc" and "Firecrawl" as written here (the
transcript's own spelling, matching the product names). "high confidential" is spoken as
is.

## 8. WHAT THE CUTOUT OWNS

* The matte, at seal time: `plate` ok (crop 2632x1880+578+240, scale_k 0.4787, head
  449.9 px, overwide_applied true, face_dx_pct −0.01), `prompt0` ok with
  **wing_review: true** (instrument abstained, removed_px 0; look at
  `matting/hermesdocs/prompts/kf_overlay_00000.png`), `selection` ok (chair audit clean,
  leak 110 px), `track` ok (MatAnyone 2, 83.0 s, est. $0.0209), `ship` ok (707 frames
  1386x990, soft alpha, rim 7, minimum_person_fraction 0.416, est. $0.0264), both
  `needs_final_visual_review`. The Astra matte step owns that review. `plate_origin()`
  reads `left` from `plate_box` (plate is OVER-WIDE).
* `SC.CUTOUT_LOGO_LANES = ("ollama", "openclaw", "notebooklm", "claude", "chatgpt",
  "mistral", "huggingface")`, files in `SC.CUTOUT_LANE_FILES`; all resolve (proofs.json).
  Excluded on purpose: `nous-girl-line` and `firecrawl` (on stage). Lanes fade in once the
  hook has landed.
* Your own k and top per section 2.

## 9. THE WHITEBOARD

Does not import this module. Redraws the same argument per the plan's
`whiteboard_version` fields: the safe alone and centred, the Nous girl mark left of it,
a terracotta turn arrow on the dial at "privacy"; the door redrawn open as a slab, the
mark inside with a page; LOCALLY first type across the top; CONFIDENTIAL under the safe;
building + BUSINESS and person bust + CLIENTS on the left with two level arrows into the
safe, two more pages stacked; sources erased, door redrawn shut, outline retraced
terracotta, ZERO RISK in the same seat; a cloud left of the safe, a terracotta line, an X
on it; erase (draw the page inside the erase); the big page with PDF tag and lines,
ANYDOC and OPEN SOURCE under it, the tag retraced terracotta, one sweep line down the
page; the Firecrawl flame stamped right with a line to it and FIRECRAWL under it.

## 10. DEPARTURES FROM THE PLAN'S LETTER

None of substance. `SC.BESPOKE` core boxes are authoritative for crops.

## 11. PROOF EVIDENCE

`review/proof_hermesdocs/`: `00.png`, `01.png`, `02.png` (bespoke crops at 405x720
scale), `*_x4.png` (the same enlarged), `frame_*.png` / `frame_*_phone.png` (21 composed
frames 0.30 to 25.50 s), `sheet.png` (contact sheet of the top zone), `proofs.json`
(boxes, connector gaps, mark resolution, arrow anchor points).
