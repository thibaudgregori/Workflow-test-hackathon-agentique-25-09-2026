# WHITEBOARD — chassis

**Status:** approved (Miguel, round 2: *"amazing!"*; v1 anchor, round 1:
*"SUUUUUPER nice!"*). Promoted from the format lab (archived on Drive under Testing & Experiments) on 2026-09-01.
**Lab record:** `references/laws/whiteboard_NOTES.md` (6 rounds, 1,060 lines) —
read it for derivations; this file is the operating manual.

---

## What the chassis does

The visual zone is **ONE drawing for the whole video**. No scenes, no swaps, no
transitions: a single 576x460 board (factory design units) that only ever *gains*
ink. Every shape draws itself on with a marker stroke (`stroke-dashoffset` over a
hand-jittered Catmull-Rom path) at the moment its words are spoken, and nothing
ever leaves. At the payoff, four terracotta corner brackets close the board and
the whole argument is one readable diagram.

Ink is anchored to word **index AND word text** (`ANCHOR` / `ANCHOR_TEXT`), so a
re-transcription **fails the build** instead of silently sliding the choreography.

### Two variants, one board

| variant | what it is |
|---|---|
| `whiteboard` (`--variant fix`) | **plan view.** Camera never moves; the whole board is in frame from frame 0 and the viewer watches the map fill in. The anchor. |
| `whiteboard_zoom` (`--variant zoom`) | **calm zoom lane.** Gently follows the pen, pulls wide only at approved chapter seams, holds each stop until the narration moves on. |

The marker/pen object is part of the format (round 2 fixed the "pencil not at the
box while the box draws" bug). Its **sound** is not: see traps.

---

## Running it

```bash
~/Documents/Workspace/.venv/bin/python chassis_gen.py                    # both variants, YouTube handle
~/Documents/Workspace/.venv/bin/python chassis_gen.py --handle tiktok_ig # TikTok/IG variant
~/Documents/Workspace/.venv/bin/python chassis_gen.py --variant zoom --out /tmp/wb
```

| knob | default | what it does |
|---|---|---|
| `--handle` | `yt` | outro chip: `yt` = `@migueltorrezai`, `tiktok_ig` = `@migueltorrez.ai`. **Only the outro differs.** |
| `--variant` | `all` | `fix` (plan view), `zoom` (calm lane), or both |
| `--out` | `./build` | project root. The lab is never written to. |

Inside `lib/whiteboard_fix6_core.py`, the knobs that matter: `ANCHOR` /
`ANCHOR_TEXT` (the beat-to-ink map), the camera schedule (`zoom` lane stops and
holds), `CAP_CLEAR_PX` (the reserved band above the caption seat), `PALETTE` /
`PEN_FILE` (SFX cast), `DUR` / `OUTRO_T`, and `FPS = 25` (Global Law 6).

Captions: **imported**, never re-typed — `CAP_FS_PX`, `CAP_PAD_V_PX`,
`CAP_PAD_H_PX`, `CAP_RADIUS_PX`, `CAP_PILL_H_PX` all read
`pipeline/captions.py`. The pill's centre is pinned to the seam
(`px(SEAM)` = 862.5px, 44.92% of frame height) — well inside Law 12.

---

## Format laws

1. **CHAPTERS ARE THE DEFAULT; ONE BOARD IS THE EXCEPTION.** *(rewritten
   2026-09-02, ROUND-4 LAW 43 — Miguel: "Not necessary to keep everything in a
   single screen unless it's a video that you think can work (like the hermes
   one)... if there's too many different ideas don't bother. Change the rules of
   the format.")*
   The original law read "the board only gains ink; nothing is erased". That was
   true of a board holding one idea. It is false for a take that makes three
   arguments, and trying to hold three arguments in one frame is what produced
   `impossibletask_whiteboard`: a 210 u strip in the top quarter, too small to
   read and too full to keep drawing.
   * **Chapters (default).** The board CLEARS between idea groups. Each chapter
     is planned to FIT its ideas at legible scale on the WHOLE legal surface
     (x 40..536, y 150..425), and the Phone Test decides whether it fits — not
     the author. ROUND-4 LAW 41's spacing is applied PER BOARD.
   * **One board (exception).** Only for a script with ONE idea that
     accumulates, where the finished frame IS the argument (the Hermes journey;
     `kimiram_whiteboard`). Choosing it goes in the plan, with its reason.
   * An erase HANDS OVER, it never blanks: `assert_zone_never_blank()` holds at
     every chapter seam exactly as it holds at the outro.
   * **AND IT HANDS OVER TO AN IDEA** *(STANDARD LAW 45, added 2026-09-02 after
     the round-5 Viewer Test).* Within **0.30 s of the erase COMPLETING**, at
     least one complete, nameable object — or the board's key word — must be
     FULLY DRAWN. A bare stroke does not count. Four of this format's seams
     shipped holding one line for up to 0.68 s, with ZERO-INK green the whole
     time (minimum ink 0.27 %, never 0), because no ink threshold can tell a
     6,960 px baseline that argues nothing from a 1,612 px key word that argues
     everything. Satisfy it by starting the incoming board's identifying object
     INSIDE the erase and drawing it fast (`SEAM_LAP` 0.04 / `SEAM_DRAW` 0.28
     against a 0.30 s `ERASE`), or by carrying the outgoing board's anchor
     object across the seam until the first new object completes. A chapter may
     state its SUBJECT instead of an object — writing `THE JOB` before drawing
     its track is the native whiteboard order.
     **The check:** `formats/whiteboard/lib/seam_check.py` (a NEW module; it
     does not touch `whiteboard_build.py`) decodes every frame of each seam's
     window and reports DEAD TIME. It removes the marker sprite by template
     match, then accepts a blob as an OBJECT (ink >= 2,600 px, box minor >= 46,
     major >= 118, ink-weighted sigma_minor >= 18 px) or as a WORD (height
     26-80 px, width >= 80, ink >= 900, >= 3 separate marks), and requires 3
     consecutive qualifying frames. Run it on every chaptered whiteboard:
     `seam_check.py --video <render>.mp4 --seams <erase start times>`.
2. **LAW 2 ON THE WHITEBOARD: A DRAWN OBJECT MAY BE NAMED IN THE HAND; A NAMED
   MODEL OR TOOL WITH A REGISTRY MARK MUST CARRY IT.** *(Miguel, 2026-09-02,
   reviewing the batch-2 `deepseekflash` whiteboard: the OPUS and FABLE tags
   "carry no Claude mark". This SUPERSEDES the blanket exemption written the
   same day — "a handwritten name IS the mark, registry logos are OPTIONAL" —
   which was too wide and let three boards ship model tags with nothing in
   them.)*

   The line is drawn on WHAT IS BEING NAMED, not on the format:

   * **A DRAWN OBJECT** — a machine, a boat, a queue, a globe, a page, a box the
     board itself invented — is named by the LABEL LAW, in the marker's hand,
     and owes no logo. Nothing in a registry depicts it, so a handwritten name
     is the only mark it can have. This half of the old ruling stands.
   * **A NAMED MODEL, PRODUCT OR TOOL THAT HAS A REGISTRY MARK** — Opus, Fable,
     Claude Code, Claude Cowork, Codex, ChatGPT, DeepSeek, Android, Grok — gets
     that mark **inked in with its tag**, beside or inside the object that
     stands for it, in addition to its handwritten name. The name says *which
     one*; the mark says *what kind of thing this is*, and a phone-sized viewer
     reads the mark first. A model tag with a written name and no mark reads as
     an empty price tag, which is the defect Miguel found.

   Ink it, do not paste it: use the build's own `mark()` helper against a
   `MARKS` entry so it pops in on the beat and registers a rigid, and put the
   mark in the same `blocks=` lockup as its tag and its written key — they are
   ONE object and are exempt from each other's gutter, never from anyone
   else's. `mark:` names stay DECORATIONS under LAW 39 and never host a label.
   **Colour, always** (GLOBAL LAW 12): the brand's own palette, never a
   monochrome or pale reduction, and never at a size that cannot be read at
   405x720 — the mark exists to be recognised. Where a family ships one mark for
   many models (Opus and Fable are both Claude), every member carries that
   family mark and the handwritten name does the separating.

   Consequence for the watcher: `named_tool_no_mark` on a whiteboard is
   ACCEPTED-BEHAVIOUR only when the thing named is a DRAWN OBJECT or has no
   registry entry. On a model or tool that has one, it is a **defect**.
3. **Ink lands on the spoken word.** Anchors are pinned to word index *and* text.
4. **The camera never drifts** (zoom lane): it CUTS or eases between framings at
   beat boundaries and then HOLDS. Round 4: *"regressed — zooms in and out too
   often, all over the place"*. Calm is the requirement, not a preference.
5. **Periodic pull-backs** (round 2): refresh the whole diagram "from time to
   time", at chapter seams only — never constantly.
6. **Reserved clearance band above the caption seat.** No drawn board element may
   enter `CAP_CLEAR_PX` (= pill half-height + 6px hairline) at ANY camera stop.
   The chassis reports `cap_intruders` per stop; a non-`NONE` entry is a bug.
7. **Boil the diagram down** (Morgane, round 3): a phone screen is small. Fewer
   glyphs, plainer marks, no symbol that is not self-evident.
8. **Composition stays centred and symmetric** (Law 12 as amended round 4). The
   right-rail clearance applies to CAPTIONS and readable annotations only — the
   board is never shoved sideways.
9. **25 fps** (Global Law 6): source face footage is 25fps conformed to 30 by
   duplicating 1 frame in 6. Face-led formats render native 25 until recordings
   are 30/60.

---

## Known traps

- **The pen squeak is a hard NO at shipped volume.** Both Miguel (round 1: *"a big
  no-go"*) and Morgane (round 3: too loud vs voice at the start, and inconsistent
  across the video) rejected it. The pen stays as a variant with the sound
  fixed/removed — it was root-caused, not turned down. Never re-raise the gain.
- **SFX LAW v2:** soft/tactile family, clearly under the voice, frame-locked to
  the visual event. Never hand-set a gain — the palette carries the levels.
- **The `∞` was jumping, not pulsing** (round 4 sweep). Any looped element needs
  its rest state proved on decoded frames, not assumed from the timeline.
- **No square-ended fills in rounded containers** (Global Law 3). The context
  meter's fill is a continuous pill, min-width = track height, no detached ticks.
- **The top 10% collides with phone UI.** `top10_intruders` in the per-stop report
  is advisory for board furniture; captions and readable annotations must be clear.
- Re-staging: the face plate and the voice are **inherited** from the lab's frozen
  stage (round 6 touched captions only). The chassis copies them into its own
  `stage/`; it never rebuilds them and never writes into the format lab (archived on Drive under Testing & Experiments).

---

## Proof of promotion

`chassis_gen.py` (default `--handle yt`) reproduces the approved round-6 pages
**byte-for-byte**:

| chassis output | lab round-6 output | result |
|---|---|---|
| `build/whiteboard/index.html` | `references/builds/chassis/whiteboard/whiteboard_fix6/index.html` | identical |
| `build/whiteboard_zoom/index.html` | `references/builds/chassis/whiteboard/whiteboard_zoom_fix6/index.html` | identical |

`--handle tiktok_ig` differs from the YouTube master on **exactly one line**: the
`#o-handle` div in the outro.

---

## THE LABEL LAW (run 9, append-only — added 2026-09-02)

An independent Viewer Test held `perplexityprojects_whiteboard` at 11 SENSE
against 13 NO-SENSE, the worst score the factory has recorded. Every structural
defect in it was one defect said five ways: **things were drawn and never named.**

| beat | what the pixels showed | what was missing |
|---|---|---|
| 0.50 s | "a half-drawn black corner stroke" | a nameable object in the hook frame |
| 3.50 s | one PROJECTS folder | **SPACES was never drawn** — the sentence "the evolution of Perplexity Spaces" had no picture |
| 10.60 s | the same static folder | **RESEARCH DESK, the key term, was never written** |
| 16.4-17.4 s | a marker hovering over blank board | the globe and the deep glyph arrive 0.6-0.9 s AFTER the words that name them |
| 22.40 s | three unlabelled glyphs feeding a folder | **ONLINE / DEEP / LOCAL were never written**; the middle glyph read cold as "stacked squares" — a Phone Test FAIL |
| 26.6-30.0 s | the handle printed over ghost folder outlines | the diagram never left |

The sibling SPLIT render draws the *same argument from the same scene module* and
passed every one of those beats, because it PRINTS all seven keys. The difference
was never the drawing. It was the writing — and writing the word is a
whiteboard's most native move. A whiteboard that draws without writing is using
half the format.

**THE LAW.** For this format, and enforced deterministically at build time:

1. **Every drawn object gets its key word handwritten beside it, at the beat that
   word is spoken.** Label and object are ONE BLOCK, within `LABEL_WINDOW` (1.0 s)
   of each other. An object that arrives without its key is not "a note", it is a
   beat that argues nothing.
2. **A comparison the script SPEAKS must be DRAWN as a comparison.** Both terms on
   the board, in different shapes, with a connector between them. "The evolution
   of X" with only the successor on screen is not a comparison, it is an assertion.
3. **The key term (Global Law 9) is written FIRST, alone, and LARGE** —
   `KEY_TERM_MIN_FS` = 22 design units, and no other type may reach the board
   before it.
4. **The outro never overprints the diagram.** The board EXITS — a wipe, which is
   a whiteboard's own erase — and the handle card starts only after that wipe has
   finished. A translucent scrim is a veil, not an erase; the 0.94-opacity scrim
   this format shipped with is why the last 3.4 s of the short was a double
   exposure.
5. **A bespoke glyph must pass the Phone Test cold, unlabelled, before its label
   is allowed to rescue it.** Three overlapping outlined squares are "stacked
   squares", not "deep research". The replacement is a document with visible
   ruled page lines under a magnifier: "a magnifying glass on a document."

### The check

`formats/whiteboard/lib/whiteboard_build.py` (the canonical harness; promoted
out of `(run 9) gen/` on 2026-09-02, where a thin re-export shim remains):

- **`assert_label_law(b, a, plan, board_text, key_term=, comparisons=)`** — reads
  the AUTHORED board (`Board.rigids`, kind `"type"`), not a rendered frame. Every
  entry of the per-video `LABEL_PLAN` (anchor -> key word) must correspond to a
  `Board.label()` whose text matches and whose write time is inside
  `LABEL_WINDOW` of that anchor. Declared comparisons must have both terms on the
  board. The key term must be first and at least `KEY_TERM_MIN_FS` tall.
- **`assert_outro_clear(rep, b, a, outro_key)`** — the outro region is
  diagram-free: the wipe completes before the handle card starts, and no ink may
  be authored at or after the outro anchor.
- **`caption_identity_guard(b, board_text, beats)`** — Law 4 restated as an
  OVERLAP test. A board word is illegal only if an identical pill is still on
  screen when it is written. Time-blind, the old form made "write the key term"
  and "never repeat a pill" contradictory whenever the script speaks its own key
  term; as an overlap test it still refuses every simultaneous double, which is
  every case the law was aimed at.

Both asserts are called from `whiteboard_build.build()` — EVERY daily whiteboard
builds through it, which is what makes these laws unskippable — and it requires
`label_plan=`, `key_term=` and accepts `comparisons=`. A per-video board cannot
be built without declaring what it writes.

### An erase is now a legal move

The approved chassis stated "nothing is erased and nothing is swapped". That was
true of a board that never had to free a column or leave a frame. Run 9 needs two
erases (the SPACES half of a comparison, and a key that has been superseded) and
one wipe (the outro). An erase is authored as an opacity swap on the element's own
id — see `ERASE` / `wipe()` in
`(run 9) gen/perplexityprojects_whiteboard.py` — and `audit_page` verifies
every id it targets exists. It stays a deliberate, named move, not a default.

---

## THE ROUND-4 LAWS ON THIS FORMAT (2026-09-02, append-only)

The whiteboard's visual zone is ONE `<svg>` canvas whose paths are drawn with
`stroke-dashoffset`, so every path's bounding box is its FINAL shape from frame
zero. A DOM audit reading those boxes measures ink that is not on screen yet, and
Gate 1 therefore SKIPS this format on purpose (it skips any clip containing
`#cam > svg`, and any element with a live `stroke-dasharray`).

So the whiteboard proves the round-4 geometry on its **AUTHORED BOARD**, in board
design units, at build time — `formats/whiteboard/lib/whiteboard_build.py`, all
called from `build()`, none skippable:

| law | check | what it refuses |
|---|---|---|
| 38 — emphasis matches its target | `assert_no_enclosure(b)` | REFUSES: any `kind="ring"` rigid (a ring/ellipse/circle is never emphasis, on any target), and a `box_emphasis()` whose target is a RASTER. TEXT ON AN IMAGE takes `highlight()` / `highlight_lines()` / `highlight_label()` — the marker fill, `rgba(198,103,72,0.32)`, radius 3.2 u, wiped open from its left edge over 0.34 s, ONE FILL PER LINE. A DRAWN OBJECT or board TYPE takes `box_emphasis(b, box, t, target=...)` — the terracotta marker box, `fill:none`, `stroke:TERRA`, `stroke-width:SW_THIN`, popped over 0.34 s from scale 0.55, kind `"boxemph"`, judged by `assert_spacing_law` against every neighbour it does not hold. Declare a pasted capture with `note_asset(b, "<name>")`. A `highlight()` with no raster under it is reported in `wrong_tool_advisory` and never gates |
| 39 — names above or below | `assert_label_side(b, label_plan)` | a planned key whose centre falls outside its object's horizontal extent ±15 %, or that is neither above nor below it. `LABEL_WELD_U = 40`; `mark:`/`logo:`/`check:`/`bullet:`/`tick:`/`hl:` names are decorations and never host a label |
| 40 — aligned anchors | `assert_anchor_law(b, connectors)` | connectors into one target landing at different heights. Build the ends with `anchor_points(box, n, side)`; declare them `connectors=[{"to": <rigid name>, "end": (x, y)}]` |
| 41 — spacing / no cramp | `assert_spacing_law(b, blocks=…)` | a gutter under **8.5 u (16 px)** between objects that are not one block. Blocks form automatically for a welded key, a container's contents, a paragraph and a stack; anything else is declared |
| 41 — no line through a name | `assert_no_text_crossing(b)` | a pen path through a type rigid's CORE band (inset 22 %/28 % vertically, 4 % horizontally). An underline grazes the edge; a crossing goes through the letters |
| 42 — marks leave | `assert_lifetime_law(b, dur, anchors=…)` | on a CHAPTERED board, any mark visible for >40 % of the take with `t_to` left at infinity and no `board_anchors=` entry. A single board (no chapter seam) is all-anchor by definition and is exempt automatically |

### New `build()` keywords (all optional, all additive)

```python
WB.build(..., blocks=(("brick0","brick1","brick2"),),      # LAW 41
             connectors=[{"to": "folder", "end": (x, y)}],  # LAW 40
             board_anchors=("job-card", "road"))            # LAW 42
```

A board that declares nothing is still judged — the laws only ask you to declare
what the geometry cannot infer.

### The chapter clamp

`chapter_seams(b)` reads the seams off the rigid registry itself: an erase time
shared by ≥3 rigids IS a seam. `effective_windows(b)` then clamps every
open-ended mark to the next seam after it is drawn, and every geometry law above
reads those windows. Without the clamp a chapter-1 key is compared against a
chapter-3 bar and the audit invents violations no viewer can see. LAW 42 alone
reads the RAW window — otherwise a board could hide a lingering mark behind a
seam it never uses.

### Calibration (2026-09-02)

| board | verdict |
|---|---|
| `impossibletask_whiteboard` (Miguel rejected it) | LAW 38 fires ×2 (`clock-ring`, `system-ring`), LAW 39 fires (`THE JOB` beside `agent`), LAW 41 fires (`job-card ⟷ monitor-card = 0.0 u`; a stroke at 6.42 s crosses `type:CODEX` — the arrow Miguel named), LAW 42 fires ×6 (`11 PM` 95 %, `CODEX` 88 %, `TEMP` 84 %, `PROGRESS` 83 %, `ASKED FOR` 59 %, `IT CAN DO` 56 %) |
| `kimiram_whiteboard` (approved) | all six SILENT |

### Pointing cues

ROUND-4 LAW 37 is not a whiteboard law but it lands here first, because the
Reels render is a whiteboard every day: run `pipeline/pointing_cues.py --vid
<id>` at PLAN time, list every cue, and raise the source post card with the
marker highlight on the claim line inside the cue's ±1.0 s window.
