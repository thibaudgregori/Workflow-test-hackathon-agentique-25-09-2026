# claudemanaged — SHARED LANE SCENE HANDOFF

**From the design agent, for the SPLIT author and for the CUTOUT author.** The plan
(`plans/claudemanaged_plan.json`) is the contract; this file is the convenience. If
they disagree, the plan wins. Neither lane redraws anything in this module: it is
sealed (`review/artwork_pass_claudemanaged.json`, production v4), and a lane that
builds on a changed module is refused.

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/claudemanaged_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import claudemanaged_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_claudemanaged_proof.py` (renders the real timeline, crops, connector contacts, frames, sheet) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the whole 38.44 s scene: html to drop inside ONE
`transform: scale(k)` wrapper (`transform-origin: 0 0`) and a list of `tl.*`
strings to append to your own paused timeline `tl`. It reads no files and takes
no format argument. **Eases are emitted as string literals** (`"power3.out"`,
`"back.out(2.05)"`, `"power2.inOut"`, `"power2.out"`, `"power2.in"`), so the page
needs no `SWING` constant. The page must provide `.abs{position:absolute}` and
`.mono{font-family:'JetBrains Mono';text-transform:uppercase}` (both chassis do).
The knife's tools are SVG `<g>` elements rotated by GSAP with `svgOrigin` (GSAP 3
core, no plugin).

### `media`: four rasters, one file

```python
for key, rel in SC.LOGO_FILES.items():            # relative to ~/Documents/Workspace/assets/logos
    CC.MARK_INK[key] = CC.measure_mark(key, LOGOS / rel)
media = {mkey: CC.mark_img(f"assets/<basename of LOGO_FILES[key]>", key, side)
         for mkey, (key, side) in SC.MEDIA_SIDES.items()}
```

`SC.MEDIA_SIDES` (ink side, core px): `_knife_img` claude 46; `_piggy_img` claude
58; `_tile2_img`, `_tile3_img` claude 56 each (0.50 of the 112 tile).

File (MARK IDENTITY, named, never guessed): `claude` → `ai-models/claude-color.png`
(registry `claude`, the orange Claude mark). Claude Managed Agents is a Claude
platform feature: NOT the Claude Code mascot, NOT the Cowork bolt. It passes
`cutout_depthfield.assert_cast_resolves` (`review/proof_claudemanaged/proofs.json`).
No source post, screenshot or other raster: `pointing_cues.py` returned 0 cues.

### `lockup`

```python
CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W) \
  + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W)
```
seated inside the scene's `#o-slot` (core top 250). `handle_key` is the only string
that differs between masters: `"yt"` on the split, `"tiktok_ig"` on the cutout.

## 2. THE UNITS

**CORE px = canvas px with y − 192** (`SC.CANVAS_OFFSET`); x verbatim. Core is
`SC.CORE_W x SC.CORE_H = 1080 x 600`.

* Declared content band `SC.CONTENT_Y0, SC.CONTENT_Y1 = 104, 548` (canvas
  296..740): the knife's open blade tip to the INFERENCE name's bottom (496..540).
  Per chapter: knife 102..354 + MANAGED AGENTS 374..430; piggy 152..366 + SESSION
  BUDGET 384..428, meter 150..374; brain 138..374 + ADVISOR 400..444, tile 194..306
  + SESSION 330..374; shelf 114..384 + SKILLS 408..452, tile 194..306; signpost
  112..454 + INFERENCE 496..540. All clear LAW 30's top 10 % and sit well above the
  split's caption pill (~595 core).
* **Mirror-symmetric about x = 540** at every settled instant: knife 264..790
  (handle 350..730); piggy content 216..464 vs meter 702..778 (centres 340 / 740);
  brain + connector + tile 250..830; shelf + cable + tile 259..821; signpost
  336..744.
* **Cutout seating:** `left = (1080 − 1080·k) / 2`,
  `top = round(stage_centre − (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 · k, 2)`, with k
  from YOUR matte envelope so the band (444·k tall) clears his crown. Every inked
  atom must clear the envelope (NEVER OCCLUDE HIM).
* Tightest non-block gutters (core px): piggy to meter 238; brain to tile (the
  connector's span) 188; shelf to tile 150. Everything closer is a DECLARED block
  (`SC.DECLARED_BLOCKS`, stamped `data-block`).

## 3. THE TIMELINE (`SC.CUE`, word starts from `cuts/claudemanaged/transcript_tight.json`)

| t | event |
|---|---|
| 0.10 | "Claude": the pocket knife lands ALONE on x = 540, complete: handle, rivets, Claude mark, ONE blade standing up (LAW 19/20 hook) |
| 1.62 | "managed": **MANAGED AGENTS** under the knife (first type, 44 px) |
| 3.30 / 3.44 / 3.58 / 3.72 | "four new features": file, screwdriver, saw, corkscrew rotate out of the handle |
| 4.44 | "Number": chapter 0 erases (0.20 s); 4.46 the piggy bank draws ALONE on x = 540 |
| 7.70 | "session": **SESSION BUDGET** under the piggy |
| 8.06 | "budget": a coin drops into the slot |
| 8.62 | "meaning": the piggy + its name slide left (dx −200, the one displacement); 8.66 the meter pops in at right |
| 9.08 | "no": the meter's fill (one pill) rises to full |
| 9.50 | "overspending": the meter's track border flips terracotta (held) |
| 11.92 | "Number": chapter 1 erases; 11.94 the Claude session tile opens ALONE on x = 540 |
| 12.88 | "session": **SESSION** under the tile |
| 13.96 | "advisor": tile + name slide right (dx +234); 14.00 the brain draws left; **ADVISOR** 14.10 |
| 16.36 | "intelligent": the brain outline flips terracotta (held) |
| 18.18 | "help": terracotta connector brain → tile draws (0.36 s) |
| 19.78 | "Number": chapter 2 erases; 19.80 the bookshelf draws ALONE on x = 540 |
| 21.22 | "load": one book's outline flips terracotta |
| 21.82 | "skills": **SKILLS** under the shelf |
| 22.44 | "from": shelf + name slide left (dx −131); 22.50 the Claude agent tile pops in at right |
| 24.22 | "connect": terracotta cable shelf → tile draws |
| 25.12 | "And": chapter 3 erases; 25.14 the signpost draws ALONE on x = 540 |
| 27.32 | "inference": **INFERENCE** under the signpost |
| 32.94 | "US": US typed into the west board |
| 33.98 | "Europe": EUROPE typed into the east board |
| 34.80 | "more": opaque rising sheet (0.46 s); board cleared 35.28; outro knife 35.30, rule 35.60, lockup 35.70 |

Beat edges `SC.BEAT_EDGES`. `SC.DUR = 38.44`. Chapter seams `SC.CHAPTER_SEAMS`.

## 4. THE FIVE BESPOKE OBJECTS (`SC.BESPOKE`, core boxes, held instants)

| i | name | t | core box | own-eyes check at 405x720 |
|---|---|---|---|---|
| 0 | Claude pocket knife | 4.20 | 264, 102, 790, 354 | `review/proof_claudemanaged/00.png`: a Swiss-army knife with five tools out and the Claude mark on the handle |
| 1 | Claude piggy bank | 8.00 | 410, 152, 670, 368 | `01.png`: a piggy bank (snout, ear, legs, curly tail, slot) with the Claude mark on its flank |
| 2 | brain wired to agent | 19.40 | 248, 138, 830, 374 | `02.png`: a terracotta-outlined brain joined by a line to a Claude tile |
| 3 | bookshelf cabled to agent | 24.90 | 259, 114, 821, 384 | `03.png`: a bookshelf (one book terracotta) joined by a line to a Claude tile |
| 4 | US Europe signpost | 34.60 | 336, 112, 744, 454 | `04.png`: a signpost, US pointing left, EUROPE pointing right |

Map `core` through your own k/origin for any crop. None is on the refused UI-glyph
list (cylinder, gear, bell, magnifier); no window/card/screen is declared bespoke.
The budget meter and the tiles are furniture.

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 39 / 50**: `data-label-for` on MANAGED AGENTS (→ pocket-knife), SESSION
  BUDGET (→ piggy-bank), SESSION (→ session-tile), ADVISOR (→ advisor-brain),
  SKILLS (→ skill-shelf), INFERENCE (→ signpost). Every NAME sits BELOW what it
  names, at 28 px except the 44 px key term. US and EUROPE are content INSIDE the
  signpost's boards (`#sp-us`, `#sp-eu`), not labels.
* **LAW 40 / connectors touch**: `SC.CONNECTORS`, two, one per target, both level
  at core y 250, `data-connect-to` = `session-tile` / `agent-tile`, stamped
  `data-overlap-ok`, butt caps, no arrowhead.
  - `conn-advice`: (530, 250) → (718, 250). 530 is the brain outline's rightmost
    VERTEX (stroke centre, vertical tangent); 718 is the session tile's left edge.
  - `conn-skills`: (555, 250) → (709, 250). 555 is the shelf frame's right stroke
    centre; 709 the agent tile's left edge.
  Checked at 2x on the proof render (`review/proof_claudemanaged/conn_*_{a,b}.png`):
  both ends sit on the stroke / border, no gap, no overshoot. **Do not move the
  tiles or the brain/shelf independently of their connector**; if your k scales the
  core, the whole core scales together, so contact is preserved.
* **LAW 41**: `SC.DECLARED_BLOCKS`.
* **LAW 42 / 43**: CHAPTERS, `SC.BOARD_MODE = "chapters"`, `SC.BOARD_CHAPTERS`;
  every mark is finite (`SC.LIFETIMES`), `SC.SCENE_ANCHORS = ()`, no `data-anchor`.
  Longest lifetime: the signpost 25.14–35.28 (26 % of the take).
* **LAW 38**: three border/outline flips on DRAWN objects (`#budget-meter` border,
  `#brain-outline` stroke, `#book-hero` stroke). No ring, ellipse, `<circle>` tag
  or highlight anywhere; rivets, eye, coin are two-arc paths.
* **LAW 23**: `#meter-fill` is ONE pill, min height = its width (48), rising to
  196 (full). **LAW 28 / 51**: the knife's tools rotate inside `#pocket-knife`
  about its rivets; the coin is inside `#piggy-bank`; `#label-session` is parented
  in `#session-group`; SESSION BUDGET and SKILLS are tweened with their objects on
  the same times.
* **Ghost rule**: drawn paths declare `pathLength="100"`, rest at stroke-opacity 0
  and reveal one frame after the draw starts. The four new knife tools are fully
  inked at 3.26 but hidden BEHIND the handle until they rotate out.

## 6. THE POINTING CUE

None (`gen/_cues_claudemanaged.json`, `cues: []`). Nothing to raise, nothing to waive.

## 7. WHAT THE CUTOUT OWNS

* The matte and wing review: prompt0 landed with `wing_review: true` (instrument
  abstained, no cut) — look at `matting/claudemanaged/prompts/kf_overlay_00000.png`.
  Selection: chair audit clean. Track marker: `running` (matanyone2) at design
  time; ship marker not landed. `plate_origin()` reads `left` from `plate_box`
  (plate is OVER-WIDE; crop 3620x1810+68+270, scale_k 0.497238).
* `SC.CUTOUT_LOGO_LANES = ("claude-code", "claude-cowork", "github", "mcp",
  "openai", "gemini", "langchain")` with explicit files `SC.CUTOUT_LOGO_FILES`
  (`claude-code` → `coding-tools/claudecode-color.png`, the no-outline mascot: the
  registry key points at the sticker, so the file map is authoritative;
  `claude-cowork` → the ORANGE bolt). All seven pass `assert_cast_resolves`
  (proofs.json). Excluded on purpose: `claude` (on stage). Lanes fade in once the
  hook has landed.
* Your own k and top per section 2.

## 8. THE WHITEBOARD

Does not import this module. Redraws the same argument per the plan's
`whiteboard_version` fields, five chapters: the knife (one blade, then four tools
drawn out) with MANAGED AGENTS; the piggy with the Claude mark, SESSION BUDGET, the
coin, the meter filled to its top and retraced terracotta; the Claude tile with
SESSION, the brain with ADVISOR retraced terracotta, the line brain → tile; the
bookshelf with one terracotta book, SKILLS, the Claude tile, the cable; the
signpost with INFERENCE, then US and EUROPE in the boards.

## 9. DEPARTURES FROM THE PLAN'S LETTER

None. The plan's `bbox` values were computed from `SC.BESPOKE` after the drawing.

## 10. PROOF EVIDENCE

`review/proof_claudemanaged/`: `00.png`..`04.png` (bespoke crops at 405x720
scale), `conn_conn-advice_{a,b}.png`, `conn_conn-skills_{a,b}.png` (2x contact
crops), `frame_*.png` / `frame_*_phone.png` (21 composed frames from 0.60 to
37.00 s), `sheet.png` (contact sheet of the top zone), `proofs.json` (boxes, DOM
boxes, mark and lane resolution, page errors: none).
