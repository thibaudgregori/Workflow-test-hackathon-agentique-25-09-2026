# ARTIFACT SPINE — format lab notes

Source: `format_lab/hermesinfinite` (shipped cut, 54.167s, 369-word Scribe timeline).
Three variants, all 1080x1920, all driven by the same transcript and the same
seven-region artifact.

## The format in one line

One document is the whole video. A mock **Hermes Agent tool-registry panel** —
real chrome, real registry marks, an always-present context meter — is the only
subject. The spine advances through it (scroll or zoom) and annotations land on
the line being spoken. Miguel's face appears only in the hook and the sign-off,
and it occupies **exactly the same window rect as the panel**, so the frame
never changes shape: the window's *content* changes, not the composition.

## The artifact

`hermes-agent · tools.config`, a settings panel with a sticky status bar and
seven document sections:

| # | section | what it is | its beat |
|---|---|---|---|
| 01 | TOOL REGISTRY | 8 server rows (Drive, GitHub, Notion, Slack, Gmail, Airtable, Figma, ElevenLabs) + `+3 more · 118 tools` = 247 | rows cascade, chips flip READY→LOADED on "loads every tool", claim struck on "they don't" |
| 02 | PROCEDURAL DISCLOSURE | the key term as a real setting row with a switch + `hermes.tools.disclosure = procedural` | the switch flips ON on the word, and *reveals* three sub-steps + the 1,200-token result band |
| 03 | LOADED THIS TURN | 3 lit tool rows over a dashed "244 tools · not loaded · 0 tokens" strip | rows pop on "see the tools", counter runs 0→3 |
| 04 | CONTEXT BUDGET | a 200,000 bar labelled **IF EVERY TOOL LOADS**, plus a 4-segment stacked "fully loaded" bar | fill grows on "consume", a hard end-stop snaps in on "finite" |
| 05 | TOOL ACCESS | 6 checkbox chips | three actually *uncheck* on "very picky", sub-line 6 granted → 3 granted |
| 06 | NOUS RESEARCH | dark card: REGISTRY SIZE vs CONTEXT USED | 247 → 21,400 → ∞ while 6% does not move, and a flat "0 growth" line draws |
| 07 | MCP SERVERS | 8 rows with switches + an ALL SERVERS ∞ band | switches cascade on "all of the MCP servers", ∞ lands on "and all of the tools" |

The **context meter in the status bar is the spine's through-line**: withheld
until "loads every tool" (so it is never an empty vessel), filled to 92% /
184,000, collapsed to 6% / 12,000 on "they don't", and then it never moves again
— which is exactly what the last annotation of the video lands on.

## What each variant does differently

- **v1 PURE SCROLL** — one continuous top-to-bottom journey. Face hook (0–2.80),
  then the artifact for 47s, then the sign-off. Six scroll moves, each 0.62s
  `power3.inOut`, each landing on a word and then **holding still**.
- **v2 FACE-FRAMED** — identical spine plus two full-window face returns at
  13.15–15.05 ("What does that mean? It's very simple.") and 38.85–40.42
  ("...and we no longer have to actually worry about that.").
- **v3 ZOOM SPINE** — the seven regions become cards on one 2640x4426 board
  (status bar, section rail, two-column grid) and the camera moves between them.
  Adds three motivated wides (establishing assembly, a pull-back pairing THIS
  TURN with the payoff card on "all the tools we will ever need", and a final
  wide on "unbelievable") plus one punch onto the context meter on "without
  bloating your context".

## What I believe works

1. **The context meter as a persistent spine device.** It is the single best
   thing here. Because it is chrome rather than content, it survives every move,
   and the video's thesis ("infinite tools, finite context") can be *proved on
   one surface*: registry → ∞ while the same bar stays at 6%. The final
   annotation returning to the bar the video opened on is the strongest beat in
   all three cuts.
2. **The face and the panel sharing one rect.** Every cut between them is a
   content swap inside a fixed window, not a layout change. It removed the whole
   class of "the frame jumped" problems and gave the format a signature.
3. **Discrete, word-synced advancement.** Scrolling is normally the enemy of
   Law 1 and Law 5. Advance-then-hold keeps both laws intact and, subjectively,
   is *more* satisfying than a continuous crawl because each move is an answer
   to a word.
4. **Chrome pre-painted, items painted on arrival.** This solved two things at
   once: no move ever lands on an inert surface, and a section peeking at the
   bottom of the viewport no longer spoils itself.
5. **Real UI beats coded diagrams for credibility.** Colored registry marks +
   plausible tool names (`fs.read_file`, `github.create_pr`,
   `notion.search_pages`) + honest controls made the artifact read as a product
   rather than an illustration, at zero extra motion cost.

## What fought me

- **Where a face return can legally sit (v2).** A return cannot land on a beat
  where the voice names something on the artifact — the annotation would be
  spoken to a face. Both returns had to be pushed onto *connective* lines. This
  is the format's real constraint: the artifact owns the naming beats, so the
  face can only have the joins. That is also why v2's returns feel like
  transitions rather than moments.
- **Empty-card framing in v3.** The first pull-back paired the payoff card with
  SERVERS *below* it — a card whose rows do not exist for another three seconds,
  so the wide framed a void. Repointing it at THIS TURN *above* fixed it. Lesson:
  in a zoom format, any framing that includes two cards must be checked against
  the paint schedule of both.
- **Two numbers, one artifact, one contradiction.** Section 04's bar (124,000)
  contradicted the status bar (12,000) until 04 was relabelled **IF EVERY TOOL
  LOADS**. On a single-artifact format every number is on screen with every
  other number, so the artifact has to be internally consistent as a *document*,
  not just per beat.
- **A "punch-in" in a zoom format is capped by legibility.** The meter close-up
  could only reach 1.035x before the readout clipped, versus 0.926x for the
  cards. The drama comes from the travel and the tight ring, not the scale.
- **Engineering:** GSAP's TextPlugin is not loaded and callback-driven text is
  not seek-safe, so every changing string is authored as stacked atoms and
  cross-faded (`swap()`); only numeric readouts use an `onUpdate` proxy. Also:
  Google Fonts and the GSAP CDN are now vendored into `stage/`, and viewport
  edge fades needed no `z-index` (they were painting over the face window).

## Laws this format would need if adopted

1. **ONE WINDOW.** The face and the artifact occupy the same rect for the whole
   piece. A face-led format may change what is in the window; it may not change
   the window. Corollary, found the hard way in v3: when the artifact is NOT
   confined to that rect (a board wider than the frame), it must be switched off
   with the face — otherwise its chrome leaks around the face card.
2. **ADVANCE, THEN HOLD.** The spine never moves continuously. Every move is
   discrete, word-synced, ≤0.9s, and followed by a hold. Annotations land only
   on a held surface (this is Law 5 restated for a moving spine).
3. **THE ARTIFACT IS INTERNALLY CONSISTENT.** Every number, count and label on
   the document must agree with every other one, because they are all on the
   same surface. Hypothetical figures must be labelled as hypothetical.
4. **CHROME PAINTED, CONTENT ON ARRIVAL.** Section frames, titles and tracks are
   authored painted; rows, chips and marks paint when the spine arrives. No move
   lands on an inert region and no section spoils itself while peeking.
5. **ONE PERSISTENT INSTRUMENT.** The artifact carries exactly one always-visible
   state device (here the context meter). It is withheld until the beat that
   fills it (Law 20 corollary), it changes only on events, and the video's last
   annotation lands on it.
6. **THE ARTIFACT OWNS THE NAMING BEATS.** The face may only take connective
   lines. If the voice names a thing that is on the document, the document is on
   screen.
7. **EDGES DISSOLVE.** A scrolling or zooming spine fades its content at the
   viewport edge; content is never sliced by a hard clip line (that reads as a
   rendering bug, not as a document).

## Files

- generators: `artifactspine_v1_gen.py`, `_v2_`, `_v3_`, shared `artifactspine_core.py`
- SFX (ElevenLabs, cached and reused across all three): `sfx/as_scroll|as_ring|as_snap|as_toggle.mp3`
- probe tool: `artifactspine_peek.py <variant> <t> ...` — drives the real GSAP
  timeline headless and screenshots it (strips the video element, which blocks a
  bare Chromium over `file://`)
- projects: `v1/ v2/ v3/` · renders: `out/artifactspine_v{1,2,3}.mp4`

---

# Fix round 1 — 2026-08-30

Authority: `format_lab/REVIEW_2026-08-30.md`. Two videos shipped, both 1080x1920
at **25 fps**: `out/artifactspine_fix.mp4` (scroll) and
`out/artifactspine_zoom_fix.mp4` (zoom, promoted from lab v3).
Generators: `artifactspine_fix_core.py` + `artifactspine_fix_gen.py` +
`artifactspine_zoom_fix_gen.py`. Projects: `fix/`, `zoom_fix/`.
The three lab generators and `artifactspine_core.py` are untouched — the fix core
imports the old core and patches it, so v1/v2/v3 still build.

## What the review asked for, and what was done

### PACING — "sometimes the animation goes too fast and people cannot see everything"

Three interventions, in order of how much they mattered:

1. **The paint model was inverted.** The old build painted a region's chrome and
   then popped every item in on arrival: 48 entrance tweens for region 01 alone,
   42 individual ticks for 03, 20 for 05, 40 for 07. Every landing was a wall of
   entrances competing with the voice. Now the document is a **document** —
   static content is authored painted, and the timeline only ever shows things
   **changing** (a chip flips, a switch turns on, a box unchecks, a meter fills,
   a claim is struck). ~90 entrance tweens became ~30 state tweens. Nothing is
   lost, because a region is physically off-screen until the spine brings it in
   (scroll) or sits under a veil until the camera lands (zoom). This is the fix
   that actually changes how the video feels; the other two are hygiene.
2. **Everything that still moves, moves ~25% slower.** Entrances 0.34 -> 0.42,
   pops 0.34 -> 0.40, spine move 0.62 -> 0.72, registry rows 0.075 -> 0.085,
   the three lit tools 0.30 -> 0.34, the uncheck 0.22 -> 0.28, server toggles
   0.075 -> 0.085.
3. **A machine guard** (`fix_core.audit`) parses the emitted timeline and fails
   the build on: any tween starting inside a spine move, less than 0.38 s of
   stillness before a move, less than 0.16 s before a face cut, an annotation
   ring held under 0.80 s, or a `-fill` driven by `scaleX`. The old build broke
   four of those: rings up for 0.40 s, `hd-ring` and `r1-ring` firing 40 ms apart
   on "all at once", ring exits running during the next scroll, and only 0.20 s
   between the last registry chip going cold and the spine leaving.

Consequence worth naming: **annotations are now strictly sequential and each
holds >= 0.80 s.** The peak card (06) lost its ring entirely — the video's
homecoming annotation is the header meter, and two rings on the peak beat was
exactly the stacking that made the format feel rushed.

### NO PEEK-AHEAD (Global Law 4) — solved as geometry, not as a schedule

Miguel's example was the 05 -> 06 Nous Research join. Measured on the old build
(flat 150 px gaps, 60 px lead), while resting on a region you could read the top
of the next one at **52 / 176 / 272 / 316 / 396 / 414 px**. The 396 px one is his.

The fix is two decisions that interlock:

* a region rests **centred** in the window (`lead_k = (VIEW_H - h_k) / 2` =
  135/197/245/267/307/316/96 px), which also kills the up-to-430 px of dead white
  the old top-pinned layout left under short sections;
* the gap is solved from the two leads it sits between:
  `gap_k >= max(lead_k, lead_{k+1}) + 8`, giving 205/253/275/315/324/324.

Both halves are needed. Solving only forward lets **54 px of 01's footer** hang
above 02 once 02 is centred, because 02 is shorter and therefore leads deeper.
`layout_scroll` asserts both directions; the build prints 0 px on all six joins.

In the zoom variant geometry cannot do this (a wide sees everything), so each
region's content sits under a veil that lifts as the camera sets off. The card
**frames** stay outside the veil, so the establishing wide still shows the
artifact's architecture — and not one word that has not been spoken. The rail
went the same way: the wide shows `01`..`07`, the section NAME lands with the
camera. ("06  NOUS" used to be legible at t=3.10, 28 s before the word.)

### NO UNMOTIVATED MOVES (Global Law 5) — and what the face returns are for

The scroll variant's six visible moves became **four**, the zoom variant's
eleven became **seven**. The saving is the same trick in both: **two moves run
hidden behind the face returns.**

    return 1  13.12 - 15.12  "What does that mean?  It's very simple."
              (02 -> 03 runs underneath)
    return 2  38.92 - 40.56  "...have to actually worry about that."
              (06 -> 07 runs underneath)

Both are v2's placements, both are connective lines (format law 6: the artifact
owns the naming beats), and both cut on real pauses. This is the round's best
find: it makes the face returns **structural** instead of decorative. v2's own
note was that its returns "feel like transitions rather than moments" — that is
now the point rather than the complaint.

In the zoom variant it also removes the two moves Miguel flagged: the
`payoff_pair` pull-back on "all of the tools that we will ever need" (which
reframed 06 together with the card above it) and the `nolonger` move that
immediately undid it. Nothing in the narration asks the camera to leave 06 —
the beat being spoken is happening inside it — so the camera simply holds.

### THE LOADER OVERFLOW (zoom bug 1)

Not a layout bug. `count_to` drove a **float** proxy straight into
`v.toLocaleString('en-US')`, whose default `maximumFractionDigits` is 3, so the
0 -> 3 counter painted `2.844` — four glyphs at 84 px in a one-glyph slot —
across its own `/ 247`. Confirmed by decoding `out/artifactspine_v3.mp4` at
**t=17.25**. The same defect ran in `hd-num` (0 -> 184,000) and `r6-num`
(247 -> 21,400); it just had room to hide there. Fixed by rounding before
formatting, so the glyph count can never exceed the glyph count of the end value.

### The other global laws

* **25 fps (6).** Both projects author and render at 25. The face plate is
  `_shared/face_std_25.mp4` (duplicates removed), not `face_full.mp4`.
* **Zoom cap (1).** The plate change is the whole story: `face_std_25` is
  1080x1350, and `object-fit:cover` in the format's 1000x1516 window scales it
  by 1516/1350 = **1.123**, inside FRAMING.md's 1.15 within-mode cap, landing at
  face_frac **0.338** / head_frac 0.435. The old `face_full.mp4` in the same
  window measured face_frac 0.396 / head_frac 0.510 — the reference reel's
  full-face median. A 15% reduction with the window untouched, which matters
  because the window is this format's signature (ONE WINDOW).
* **SFX v2 (2).** The tamed palette on its class constants (structure 0.120,
  detail 0.077), 14 cues in 54 s, every one quantised to a real 25 fps frame,
  and **all the old lead/lag offsets deleted** — the new files are onset-trimmed,
  so `data-start` means what it says. Grammar: `soft_whoosh` = seize (into the
  artifact), `reverse_air` = release (to the face), `low_thump` = a hard state
  change, `page_turn` = a section change, `tick` = the switch, `pop` = the
  infinity glyph landing.
* **Rounded fills (3).** Inherited already-fixed from `artifactspine_core`; the
  guard re-asserts that no `-fill` element is ever driven by `scaleX`.

## Two engineering findings worth keeping

* **`tl.fromTo` must carry `opacity` in BOTH ends.** Three elements
  (`r1-strike`, `r6-flat`, `ol-rule`) carry a CSS `transform: scaleX(0.001)`, so
  they have to be driven with `fromTo` or GSAP clobbers the authored transform.
  Revealing them only in the *from*-vars renders fine in a sequential preview and
  can encode **invisible**, because cold render workers restore the authored
  hidden state. The renderer's lint catches it; the peek probe does not.
* **Delete `_peek.html` before rendering.** `artifactspine_peek.py` writes a
  stripped copy of `index.html` next to it, and it still carries
  `data-composition-id` — the renderer discovers two root compositions and can
  play the audio twice. Caught by lint on the first render attempt.

## Open, deliberately not done

* The zoom variant's meter punch still only reaches **1.035x** — the readout
  clips beyond that, as v3 already found. The drama is the travel, not the scale.
  Framing a narrower rect would buy scale at the cost of the "CONTEXT WINDOW"
  label, which is the thing the punch is about.
* The punch necessarily frames the top of the board, so region 01 sits under the
  status bar during the close-up. It is spoken content (history), so Law 4 is
  satisfied, but a board layout with the status bar on its own row would compose
  better if the zoom variant is ever rebuilt.

---

# FIX ROUND 2 — the zoom variant rebuilt (task `azoom2`)

Authority: `format_lab/REVIEW_2026-08-30.md` **ROUND 2** and its global laws
7-11, `_shared/ZOOM_STANDARD.md`, `STANDARD.md` underneath. `artifactspine_fix`
(the scroll cut) is **APPROVED and untouched** — this round rebuilds only the
page-zoom variant, as `artifactspine_zoom_fix2.mp4`, from
`artifactspine_zoom_fix2_gen.py`.

Miguel, round 2:

> the Hermes Agent card is WIDER than the other cards. LAW: all cards identical
> width, all respect the screen margins; a card touching the frame edge is a
> violation — at ANY camera stop, so recompose the board so every stop keeps
> its margins.

## What was actually wrong (measured on `artifactspine_zoom_fix.mp4`)

Three card widths were on that board and the camera had two framings:

| element | width |
|---|---|
| top card (HERMES AGENT) | **1040 px** |
| column A — 01, 04, 05 | 980 px |
| column B — 02, 03, 06, 07 | 1080 px |

so the header card was 60 px wider than the cards under it and 40 px narrower
than the ones beside it — "the wide one" wherever two shared a frame. Two
further edge violations fell out of the same geometry:

* **the meter punch cropped the header card on both sides.** It framed the
  976 px meter at scale **1.2686**, so the 1040 px card it lives in painted
  **1319 px inside a 1080 px frame** for the whole climax beat.
* **the header card was in shot during the arrival on 01.** With `COL_GAP=64`
  it sat 42 px above region 01, well inside the viewport, overhanging right.

## The rebuild — three decisions

**1. ONE CARD WIDTH.** `CARD_W = 1000` for all **eight** cards, header included.
The header is no longer a banner: it is a card in a column like the rest, and it
absorbed the free-floating "TOOL REGISTRY / one panel · seven sections" title,
so nothing on the board sits outside a card. (Round 1's own open note — "a board
layout with the status bar on its own row would compose better if the zoom
variant is ever rebuilt" — is what this is.)

**2. ONE CAMERA FRAMING.** `cam()` has no per-stop caps left. Every stop fits
its subject into `1080 - 2*40` x `1660 - 2*40`, capped at scale 1. A 1000 px
card at scale 1 paints 1000 px in a 1080 px frame: **40 px of air on both sides
at all nine stops, by construction**. The meter punch became a stop on the
header CARD, so the climax now shows the whole instrument instead of a cropped
strip of it — and it is framed identically to every section card.

**3. THE BOARD IS RECOMPOSED, because margins are only real if nothing else
reaches the edge either.** At scale 1 the frame shows 1080 x 1660 of board and a
card is at most 1216 tall, so up to 222 px of the neighbour above and below used
to be in shot. The layout now solves, per pair,

```
gap >= (1660/2 + CLEAR) - min(h_i, h_j)/2 + BREATH        CLEAR 40, BREATH 40
```

giving 403-720 px gaps, and the same condition horizontally gives the column
pitch (1120) and the rail's gutter (120). `_guard_margins()` re-derives all of
it from the emitted geometry and **fails the build** if any of the nine stops
puts an element inside the 40 px border or leaves a foreign element intersecting
the frame. Global Law 8 needs no edge fade here: nothing is ever cut.

## Two things the recompose broke, and how they were fixed

* **Sparse, scattered establishing wide.** First attempt centred each column
  vertically; eight cards with 500 px gaps and three different centres read as
  rectangles thrown on a table. Columns now share **one top line** (single-card
  columns excepted), which is what makes it read as a document.
* **A 3190 px whip.** The obvious 3/3/2 split puts a column change on a visible
  arrival, and bottom-of-column to top-of-next travels ~3100 px — 2.8x the
  longest move in the approved scroll cut, i.e. 200+ px per frame of dense type
  at 25 fps with no motion blur. **The column breaks are now placed where the
  face is**: the two returns already hide arrivals 2 and 6, so the columns are
  **3 / 4 / 1** (header+01+02 / 03+04+05+06 / 07). Every visible move is a
  1307-1479 px step *down* a column, both long diagonals happen behind Miguel's
  face, and the camera never travels upward. `WHIP` guard fails the build above
  1600 px. 07 CONNECT EVERYTHING gets the last column to itself, centred — the
  payoff card, isolated.

## Law 11 — continuous pill fills, no detached ticks or end markers

`fill_to()` already reaches by `width` with a one-diameter floor, so `hd-fill`
and `r4-fill` are true pills at every value (round 1, Global Law 3). What was
still on the board was **`r4-stop`**: an 8 px INK tick floating past the end of
the rounded 04 CONTEXT BUDGET track, snapping in on "finite." — exactly the
detached end-marker artifact Miguel screenshotted. Round 1's audit had
watch-listed it as a wipe transient; Law 11 settles it. It is **deleted**, and
the "finite." beat is now the card's own border going hard INK, with the
existing HARD LIMIT label and ring carrying the meaning. The 4-segment "fully
loaded" bar also lost its 2 px inter-segment seams, so it reads as one pill with
colour bands rather than square chunks inside a rounded container.

Both edits are applied by `patch_region4()` / `patch_r4_stop_tween()` **inside
the round-2 generator**, with match-count guards — `artifactspine_core.py` is
deliberately not edited, because the approved scroll cut is built from it.

## Kept, unchanged, from round 1

Pacing (state-only schedule, the `audit` guard), the per-region veil that
enforces no peek-ahead in a format where geometry cannot (Global Law 4), the two
face switch-ins, exactly two non-arrival moves and both spoken for, the rounded
counter formatting that killed the loader overflow, 25 fps native, SFX v2, the
same seven regions, voice, annotations and captions.

## Board, before and after

| | round 1 | round 2 |
|---|---|---|
| card widths | 1040 / 980 / 1080 | **1000 x 8** |
| board | 2640 x 4426, 2 columns | 3720 x 5050, 3 columns (3/4/1) |
| stop scales | 0.343 wide, 0.926-1.020 cards, **1.269 punch** | 0.269 wide, **1.000 everywhere else** |
| side margin at a card stop | 40 px (col B) / 30 px (col A) | **40 px, all nine stops** |
| header card at the punch | 1319 px wide in a 1080 px frame | 1000 px, 40 px margins |
| longest visible move | 1115 px | 1479 px (guard fails > 1600) |
| vertical gaps | flat 64 px | solved 403-720 px |

## Still open

* The establishing wide is architecture only (eight empty frames), so it is
  sparser than round 1's — the price of the clearance the law requires. It is on
  screen for 0.46 s and every frame is legal.
* The closing wide finishes at 50.02 and the outro cut is at 50.20, so it rests
  for 0.18 s. Inherited from round 1; lengthening it means moving the outro.

## Verified on the render, not on the plan

`zoom_fix2_check.py` decodes the finished MP4 and measures the 40 px border of
the board area at all **ten** rests (the establishing wide, seven card stops,
the header-card punch, the closing wide). Cards are WHITE (#FFFDF9) on a CREAM
(#F6F1EA) page and their borders are much darker, so both are separable from the
one thing that legitimately reaches the edge — each card's
`0 20px 52px rgba(20,20,22,0.10)` drop shadow.

Measured profile beside a card at a stop: the card edge lands on **x = 40.0**
exactly; the shadow ramps from **11 levels** of darkening right beside it to
**2 levels** at the frame edge, i.e. a soft alpha ramp that is Global Law 8's
edge fade rather than a clip. Card surface in the border: **0 of 10 rests**.
The same script confirms the face plate is not frozen (3/3 sampled pairs move),
which the renderer's `video_nested_in_timed_element` lint always warns about in
this format.

Render: 1080x1920, 25/1 CFR, 1354 frames, 54.165 s, 17.3 MB, 31 s on 2 workers.
Staged: `~/Movies/Shorts Factory/Format Lab/Fixed2/artifactspine_zoom_fix2.mp4`.

Files: `artifactspine_zoom_fix2_gen.py` (generator + both guards),
`zoom_fix2_check.py` (render self-check), project `zoom_fix2/`, log
`render_zoom_fix2.log`, contact sheets `zoom_fix2_snaps/`.

---

# FIX ROUND 3 — Global Law 12, both cuts (task `artifact3`)

**Both artifact-spine videos failed the caption law.** Round 2's scroll cut was
APPROVED on content ("nice!") and round 2's zoom rebuild fixed the card widths —
and both put their captions where no phone can show them. Measured on
`Fixed/artifactspine_fix.mp4`, the terracotta pill runs **y 1663..1776, bottom at
92.5 % of frame height**; `Fixed2/artifactspine_zoom_fix2.mp4` is the same.
Against the S26 Ultra measurements in the review that is under TikTok's creator
block (75 %), under Shorts' title row (81 %) and under Reels' description (92 %).
Morgane was right, and the calculation made it a law.

## The one change: WHERE the piece is painted

Nothing in the composition was redesigned. The document, its seven regions,
their solved gaps, the 30 state tweens, the two face switch-ins, the two hidden
moves, all ten SFX cues, the counter formatting and every pacing guard are the
approved build. What moved is the rect they are painted into.

| | round 2 | round 3 |
|---|---|---|
| caption pill centre | 1720 (89.6 %) | **1292 (67.3 %)** |
| caption pill bottom | 1776 (92.5 %) | **1349 (70.2 %)** |
| the ONE WINDOW | 40,84 · 1000×1516 | **40,192 · 872×1018.5** |
| artifact ink, scroll | x ..1008 · y 116..1600 | **x 58..898 · y 217..1208** |
| artifact ink, zoom | x ..1040 · y 0..1660 | **x 90..862 · y 232..1171** |
| spine travel on screen | 1328 px (uniform) | **698-850 px** (same 0.72 s) |
| face | head_frac 0.435 | **head_frac 0.313** |

The safe window is **solved, not chosen**:

```
pill height        115 px      (measured 112-114 on the rendered round-2 file)
pill bottom    <=  1382        (law)  ->  centre 1292, 24 px of air above it
window bottom  =   1210.5      (pill top - CAP_GAP)
window top     =   192         (the top-10 % line is the window's own edge)
window right   =   912         (the right-15 % rail starts at 918)
```

## Why a SCALE and not a redesign

The window lost 128 px of width and 498 px of height, and the tallest region
(07 MCP SERVERS, 1128 px) plus its centring air needs 1220 px of viewport. There
is no arrangement of the approved document that fits 1416 px of panel into
1018.5 px of safe height. So the panel is authored at exactly the approved
geometry inside one `#pscale` wrapper and painted through
`transform: scale(0.71928)`; the zoom variant's camera does the same job with
`S_UNI`.

That is what makes "nothing else changed" literally true: GSAP tweens on the
children are in the approved coordinate system, so no tween, no `fill_to`
geometry, no ring rect and no scroll stop needed a single number changed. The
solver still reports **0 px of peek-ahead and 0 px of bleed-back** at all six
joins, and the pacing guard still passes on 351 events.

Type lands at 0.719× — 27 px row names render at 19.4 px, the 19 px registry
chips at 13.7 px. Verified legible on the render; that is the price of the law
and it is cheaper than a caption nobody can read.

## The zoom variant: one scale for every card stop

Round 2's law was "all cards identical width, all respect the margins". Round 2
achieved it because every card happened to be **width**-bound in a 1000×1580 fit
box. In the smaller safe frame the tallest card (1216 px) becomes **height**-bound
and would have painted 9 px narrower than its neighbours — Miguel's exact
complaint, re-introduced by the new rect. So round 3 solves the scale once,

```
S_UNI = min(FIT_W / CARD_W, FIT_H / max_card_h) = 0.77179
```

and uses it at all eight card stops. Measured by the guard on the emitted
geometry: **every card stop paints its subject at 771.8 px wide with 50.1 px of
air on each side.** Only the two establishing wides fit their own subject. The
gap solver was re-derived too — round 2 packed the board assuming scale 1, but
at S_UNI the frame sees 1130×1320 of board, so the minimum gap is computed in
board units from the real visible window.

## The face got WIDER for free

`face_std_25` (the approved plate, unchanged) was `object-fit: cover` **scaled
up 1.123×** in the old 1000×1516 window — head_frac 0.435, tighter than the 0 %
standard allows for a punch. The same plate in 872×1018.5 fits at **0.807×** ->
**head_frac 0.313**, cap clearing the top of the window by ~80 px, chin by
~239 px, and **shoulders in frame for the first time in this format**. Global
Law 1 and Miguel's round-3 ruling (full-face is the RAW 0 % crop, no punches, no
virtual set, no matte-on-ground) are satisfied by geometry, with no new asset
and no zoom program.

Checked first: the 0 % plate `face_zoom00_25` in the same window computes to
head_frac 0.455 — *tighter* than what Miguel approved — and simulating the crop
on real frames clipped the cap on the frames where his head sits highest. The
window is not 9:16 any more, so cover-fitting the 0 % plate is a zoom-in, not a
zoom-out. `face_std_25` is the wider, law-compliant choice.

## The caption's WIDTH was the second half of Law 12

The pill is centred on x=540, so the rail column caps how wide it may grow.
Round 2's `cap_font` sized to 907 px of ink (pill up to 975 px, x 52..1028) and
**15 of the 52 captions crossed x=918** — the tail of every long line sat under
the like / comment / share icons. `cap_font` is now solved against the rail:

```
ink <= 2*(918 - 540) - 2*34 = 688 px      fs = clamp(32, 688/(0.600*len), 56)
```

The 0.600 is **calibrated on rendered pixels**, not guessed: measured pills give
ink/(len·fs) = 0.437 (`and context is finite.`) to 0.556 (`Hermes Agent managed
to` — wide caps, no descenders). A first pass at 0.530 shipped one pill to
x=931 and was caught by sweeping **all 52 caption midpoints** as snapshots and
measuring the terracotta bbox on each: x 187..892, centre 1291.5 on every single
frame. Only the four longest lines drop below 40 px; the median caption is still
at the 56 px ceiling.

## Verified on the rendered files

`fix3_check.py` decodes 18 timestamps per cut — artifact beats, both face
returns and the outro — and asserts Law 12 on real pixels. The content threshold
is 150 on summed |rgb − cream|, which sits above every piece of chrome the
palette can paint (PAPER 15, LINE_2 28, WHITE card 36, LINE hairline 40, the
window's `0 26px 64px` drop shadow 86) and below every piece of content
(MUTED_D 296, TERRA 380, MUTED 402, INK 659). Chrome peaks are reported, never
failed — Global Law 8 explicitly allows a soft alpha ramp at an edge.

```
artifactspine_fix3        caption bottom 1331..1348 = 69.32 %..70.21 %  (law <= 72 %)
                          caption centre 1291.5 = 67.27 %   STABLE on all 18 samples
                          caption right  x max 891          (rail 918)
                          right-rail ink 0 px · top-10 % ink 0 px · bottom-28 % ink 0 px
                          chrome peak: rail column 86, top band 51   (threshold 150)
                          face motion 3/3 sampled pairs changed
artifactspine_zoom_fix3   identical caption numbers (same window, same pill)
                          chrome peak: rail column 51, top band 27
```

Renders: 1080×1920, 25/1 CFR, 1354 frames, 54.165 s — 12.0 MB scroll (31 s) and
13.3 MB zoom (31 s), 2 workers.
Staged: `~/Movies/Shorts Factory/Format Lab/Fixed3/artifactspine_fix3.mp4` and
`.../artifactspine_zoom_fix3.mp4`.

## Still open

- The bottom 28 % and the right 15 % are now genuinely empty cream. On a phone
  the platform fills them; in a bare preview the piece reads smaller than round
  2. That is the law working, but it is worth showing Miguel side by side with a
  phone-UI overlay before it becomes the house default.
- The establishing wide is now 0.205× instead of 0.269×, so the eight empty card
  frames are smaller. Content is veiled there, so nothing is unreadable that was
  readable — but if the wide ever needs to carry type, the board has to lose a
  column.

Files: `artifactspine_fix3_core.py` (Law 12 geometry + the caption solver),
`artifactspine_fix3_gen.py`, `artifactspine_zoom_fix3_gen.py`,
`fix3_check.py` (render self-check), projects `fix3/` and `zoom_fix3/`, logs
`render_fix3.log` / `render_zoom_fix3.log`, contact sheets `fix3_snaps/` and
`zoom_fix3_snaps/`.

---

# FIX ROUND 4 — the RECENTRE, both cuts (task `artifact4`)

Round 4's only verdict on this format: **"why are they not centered? they look
so bad like this"** — with the root cause named in the review itself. Round 3
read Law 12's right-15 % rail as a wall for the WHOLE composition and solved it
by narrowing the ONE WINDOW from 1000 px to 872 px **without moving its left
edge**, so the piece sat at x 40..912 with 168 px of dead cream on the right.
The round-4 amendment: the composition stays centred and symmetric; only
CAPTIONS and critical readable annotations avoid the rail, because content is
allowed to sit under the platform's translucent icons.

## The one change

```
WIN_X   40.0  ->  104.0        (1080 - 872) / 2
```

That is the entire diff. `WIN_W`, `WIN_Y`, `WIN_H` and `CAP_Y` are untouched, so
the scale (`s = 0.71928`), the virtual panel, `doc_w`, the region heights, the
leads, the solved gaps, the scroll stops, the screen travel, `S_UNI`, the card
widths, the board packing, all ten camera stops, the caption solver and all 52
captions are computed from identical inputs.

Proof that nothing else moved — the emitted HTML, diffed against round 3:

| cut | changed lines |
|---|---|
| scroll | 3 — `<title>`, `#panel` `left:`, `#facewin` `left:` |
| zoom | 3 — `<title>`, `#stage` `left:`, `#facewin` `left:` |

Every tween, every fill, every SFX cue, both face switch-ins (13.12 / 38.92),
both hidden moves, the pacing guard's 351 (scroll) and 386 (zoom) events and the
0 px peek-ahead / 0 px bleed-back solve are the same objects in the same module:
the round-4 generators import the round-3 generators and call their `build()`.

## Measured on the rendered files (`fix4_check.py`)

Margins are measured on the SURFACE, not on its shadow: on an artifact frame the
panel (scroll) / card (zoom) is the only thing brighter than the cream page, on a
face frame the window is the only thing far darker. Six artifact/face samples per
cut, plus a stop-by-stop sweep of the zoom camera.

```
artifactspine_fix4        t= 4.51 art   L 106  R 106  delta 0
                          t=11.02 art   L 106  R 106  delta 0
                          t=17.31 art   L 106  R 106  delta 0
                          t=27.91 art   L 106  R 106  delta 0
                          t=39.16 face  L 104  R 104  delta 0
                          t=52.33 face  L 104  R 104  delta 0
                          (t=14.20 face L 104  R 104  delta 0)
artifactspine_zoom_fix4   t= 4.51 card  L 156  R 156  delta 0
                          t=11.02 card  L 156  R 156  delta 0
                          t=17.31 card  L 156  R 156  delta 0
                          t=27.91 card  L 156  R 156  delta 0
                          t=39.16 face  L 104  R 104  delta 0
                          t=52.33 face  L 104  R 104  delta 0
                          (t=14.20 face L 104  R 104  delta 0)
zoom camera, every stop   wide/face 104/104 · stop0..5 156/156, width 768 px
                          identical at all six card stops (round-2 uniform-card
                          law still holds), stop6 behind the face 104/104
```

Round 3, for comparison, measured on the same threshold: scroll L 22 / R 150,
zoom L 83 / R 209 — **128 px lopsided at every sample**.

The caption seat is unchanged and still legal on all three platforms:

```
pill centre 1291.5 on every sample, both cuts   (STABLE — Morgane)
pill bottom max 1348 = 70.21 % of frame height  (law <= 72 %)
pill right  max 859                             (rail 918)
top 10 % ink 0 px · bottom 28 % ink 0 px
```

The one thing the amendment deliberately buys: composition ink now reaches into
the rail column (0..20.5 k px across the samples, vs 0 in round 3). That is the
ruling — "content may sit under the translucent platform icons like every major
channel's shorts do" — and `fix4_check.py` reports the number rather than
failing on it, so the trade stays visible.

## Why not simply widen the window back to 1000 px

That would also have been symmetric (40 / 40, the round-2 rect) and it was
considered. Rejected: `WIN_W` feeds `vw = WIN_W / s`, so a 1000 px window
re-lays the document at `doc_w` 1304 instead of 1148, which re-solves the region
heights, the leads, the gaps and therefore the screen travel of every spine move
— i.e. it would have changed the pacing Miguel approved, in the round whose
brief was "geometry and rhythm only, do not redesign anything". Translating the
rect changes nothing but the rect.

Files: `artifactspine_fix4_core.py` (the recentre + Law 12 as amended),
`artifactspine_fix4_gen.py`, `artifactspine_zoom_fix4_gen.py`,
`fix4_check.py` (render self-check), projects `fix4/` and `zoom_fix4/`, logs
`render_fix4.log` / `render_zoom_fix4.log`.
Staged: `~/Movies/Shorts Factory/Format Lab/Fixed4/artifactspine_fix4.mp4` and
`.../artifactspine_zoom_fix4.mp4` (1080x1920, 25/1 CFR, 1354 frames, 54.165 s,
12.0 MB and 13.3 MB).

---

# Fix round 5 — FULL-SIZE DOCUMENT + TOP CAPTION SEAT

Miguel, round 5, on both artifact spines ("do the same changes for each other"):

1. **document back to full size** — "restore the layout that you had in the first
   version": the document fills the frame width minus normal margins, killing
   the white space. Round 3's viewport shrink (872 px, `scale(0.719)`) is dead.
2. **captions move to a top seat** — one stable pill seat in the upper zone,
   fully below the top-10 % line, because a scroll shows already-read content at
   the top.
3. **new law: ONE caption font size per video**, verified by measuring rendered
   pills rather than trusting the generator.

## What changed, in numbers

```
                    round 4                     round 5
window          40,192  872 x 1018.5        40,372  1000 x 1416
margins         104 / 104 (recentred)       40 / 40      (round-1 margins)
scale           0.7193                      1.000000     (identity transform)
document        1130 virtual x0.72           936 virtual x1.00
                = 825 screen px             = 936 screen px   (round 1: 936)
caption         y 1292, bottom 70.3 %       y 288 TOP SEAT, 12.56..17.44 %
caption size    43.8 / 49.3 / 52.6 /        41.0 px, every caption
                54.4 / 56.0 px
zoom stage      872 x 1034.5                1000 x 1416
zoom card       785 px wide                 920 px wide (uniform-card law holds)
```

`WIN_H = 1416` is not taste: `virt_view_h = max(region heights) + 2*LEAD_MIN` is
1220 and `HEAD_H` is 196, so 1416 is the ONLY window height at which the
composition paints at its authored size. The generator asserts `s == 1.000000`
and `doc_w == 936.00` and refuses to build otherwise — that assertion IS "the
round-1 layout", mechanised.

## White space, measured on six decoded frames

Metric: background tones (page cream + the paper-toned row fills) as a share of
the frame. The artifact's own white panel, and every glyph / rule / chip / card,
counts as artifact.

```
scroll        t=6     t=12    t=18    t=26    t=34    t=44    MEAN
round 4      72.7 %  61.1 %  52.1 %  63.5 %  51.4 %  70.2 %  61.8 %
round 5      56.0 %  38.2 %  25.9 %  43.2 %  25.3 %  53.3 %  40.3 %
delta       -16.7   -23.0   -26.2   -20.3   -26.1   -16.9   -21.5 pt
                                        artifact 38.2 % -> 59.7 % of the frame

zoom          t=6     t=12    t=18    t=26    t=34    t=44    MEAN
round 4      81.5 %  75.4 %  70.1 %  83.5 %  73.2 %  77.5 %  76.9 %
round 5      75.3 %  65.6 %  59.3 %  78.8 %  64.6 %  69.7 %  68.9 %
delta        -6.3    -9.8   -10.7    -4.7    -8.6    -7.8    -8.0 pt
                                        artifact 23.1 % -> 31.1 % of the frame
```

Geometrically: the scroll's dead frame area outside the artifact goes 56.5 % ->
31.7 %. The zoom moves less because that variant has no panel — it is floating
cards on cream by design — but its cards grew 785 -> 920 px wide (+37 % area)
and every stop still paints its subject at ONE width with 40 px of air each side.

## Pill-over-fresh-content check

The seat is **above** the artifact, not on it, and that is forced rather than
chosen: the panel header is 196 px tall and the top-10 % line is at 192, so any
pill seated in the 12-18 % band would land on the persistent context meter. The
seat that satisfies the band therefore has to clear the presentation rect.

```
pill              y 241.2 .. 334.8      (12.56 % .. 17.44 % of frame height)
top-10 % line     192                   -> 49.2 px of clearance
artifact top      372                   -> 37.2 px of air below the pill
rail band starts  576                   -> pill is 241 px above it
widest pill       x 166 .. 914          (rail 918)
```

Verified on decoded frames, one frame at the midpoint of every caption, both
cuts: in the pill's y-band, every pixel that is not the pill (or its antialiased
/ codec halo, +12 px) is page background.

```
                       captions sampled   masking document ink
scroll  round 5              52                   0        52/52 CLEAN
zoom    round 5              52                   0        52/52 CLEAN
```

Overlap is 0 px at every frame, fresh or consumed — the strongest form of
"nothing FRESH is ever under the pill". For the zoom cut this also settles
"every camera stop keeps the pill over consumed/neutral area" structurally: no
stop — wide, header or card — can put board ink under a pill that sits outside
the stage. No stop had to be recomposed.

## ONE font size, measured

The pill BOX is `font-size * 1.357 + 2*19` and does not depend on the string, so
its rendered height is the string-independent witness. Measured across all 52
captions:

```
round 4   pill height 80..114 px   10 distinct   80x1 86x1 88x1 92x1 98x1
                                                 102x1 104x3 108x6 112x2 114x35
round 5   pill height 92..92 px     1 distinct   92x52                ONE SIZE
```

Secondary read, size recovered from each pill's WIDTH minus 68 px of padding,
divided by that caption's exact Nunito-800 advance in em (read out of the
shipped `stage/fonts/61025e3c21.woff2`):

```
round 4   31.8 .. 56.6 px   spread 24.8 px   30 distinct
round 5   39.6 .. 41.2 px   spread  1.6 px   10 distinct
```

The 1.6 px of residual spread is kerning, not size: the low readings are the
short, kern-heavy strings (`'You see,'` 39.6, `'single day.'` 40.1) and the high
ones are long lowercase runs (`'What does that mean?'` 41.2). Pill height is 92
for all 52.

**How the one size is chosen.** Not guessed: the widest caption
(`'context, which is just unbelievable.'`, 16.607 em) against LAW 12's ink
budget `2*(918 - 540) - 2*34 = 688 px` gives 41.4 px, taken down to 41.0 for
kerning safety. The widest pill then measures x 166..914, inside the 918 rail.

## What did NOT change

Schedule (CUT_IN 2.84, CUT_OUT 50.20, face returns 13.12/15.12 and 38.92/40.56,
seven arrivals, two hidden moves), the no-peek-ahead solver (peek 0 px and
bleed-back 0 px on all six transitions, re-derived), the 30 state tweens, the
pacing guard (351 events / 4 visible moves / 6 face cuts on the scroll, 386 / 7 /
6 on the zoom), counter formatting, Law 11 fills, 25 fps, all ten SFX cues at
their pinned class levels. Both generators are still the round-3 generators
called unmodified; round 5 only repoints the shared geometry.

Two consequences worth naming rather than hiding:

* **Screen travel.** The spine moves 971..1182 screen px per beat instead of
  835..864, because the document is no longer being shrunk. That is still below
  round 2's 1328 px, and round 2 is the build Miguel approved on pacing.
* **The face is tighter than round 4, wider than round 2.** `face_std_25`
  cover-fitted to 1000x1416 lands at head_frac ~0.406, between round 4's 0.313
  and the 0.435 Miguel approved in round 2. No punch, no new asset — the ONE
  WINDOW simply changed shape.
* **The composition's bottom edge is 1788 (93.1 %).** This is the round-4
  amendment being spent deliberately: at rest every region is centred in the
  viewport, so what occupies the frame's bottom band is the region's lead air
  and the panel's own edge, not readable ink — and the alternative is the dead
  30 % cream band Miguel just rejected. Captions are the thing Law 12 protects,
  and they are now at 12-18 %.

Files: `artifactspine_fix5_core.py` (the window, the top seat, the one-size
solver, LAW 12 r5), `artifactspine_fix5_gen.py`, `artifactspine_zoom_fix5_gen.py`
(+ `restage()`, because the zoom generator snapshots the stage rect at import
time and round 5 changes its width AND height), `fix5_check.py` (render
self-check), `fix5_measure.py` (frame rig), projects `fix5/` and `zoom_fix5/`,
logs `render_fix5.log` / `render_zoom_fix5.log`, results
`fix5_check_scroll.txt` / `fix5_check_zoom.txt`, frames in `fix5_snaps/`.
Staged: `~/Movies/Shorts Factory/Format Lab/Fixed5/artifactspine_fix5.mp4` and
`.../artifactspine_zoom_fix5.mp4` (1080x1920, 25/1 CFR, 1354 frames, 54.16 s,
15.7 MB and 16.8 MB).

---

# Fix round 6 — THE CANONICAL CAPTION (closing captions round)

One job: this format's caption pill stops being a lab invention and becomes the
object the factory has already published 7,614 times. Nothing else in either
video is touched — the window, the seat centre, the schedule, the solver, the
pacing guard, the SFX and 25 fps are round 5's.

## The canon, read out of the published factory

`shorts_run8/projects/mcpupgrade_icon/index.html` is authored in a 576-wide
design space and painted into a 1080-wide root, so every number in that file is
the design number x 1.875. Its `.scappill` rule and all 38 of its caption clips
read:

```
.scappill { display:inline-block; transform:translateY(-50%);
            background:#C4573A; color:#fff;
            font-family:Nunito,sans-serif; font-weight:800;
            padding:18.8px 33.8px; border-radius:22.5px;
            white-space:nowrap; }
<span class="scappill" style="font-size:56.2px">            x38, ONE size

56.2 / 1.875 = 29.97 -> 30 px    18.8 / 1.875 = 10.03 -> 10 px
33.8 / 1.875 = 18.03 -> 18 px    22.5 / 1.875 = 12.00 -> 12 px
```

So in the 1080-wide space these two videos are authored in, the canonical pill
is **56.2 px Nunito 800, padding 18.8/33.8, radius 22.5, #C4573A on white**.

## What changed, in numbers

```
                         round 5                 round 6
font-size                41.0 px (solved)        56.2 px (the canon, fixed)
padding                  19 / 34                 18.8 / 33.8
border-radius            22                      22.5
pill box                 92 px measured          114 px measured (114.3 authored)
glyph x-height           ~19.8 px predicted      26-27 px measured (27.2 predicted)
seat centre              y 288                   y 288           UNCHANGED
pill band                12.55 .. 17.45 %        12.02 .. 17.98 %
gap to the artifact      37 px                   26.9 px
captions                 52 phrases              58 beats (6 phrases split)
widest pill              749 px, x 165..915      726 px, x 177..903
```

Pill height is not a taste number: Nunito's hhea is ascent 1011 / descent -353 /
lineGap 0 on a 1000 upem, so `normal` line-height is 1.364 em and the box is
`56.2 * 1.364 + 2 * 18.8 = 114.3`.

## SPLIT, never shrink

The published `cap_font()` shrink-with-length formula is dead, and so is round
5's "solve one size from the widest caption" — both make the pill a function of
the phrase. The canon is the other way round: the SIZE is fixed and the PHRASE
is cut to fit.

```
ink budget   2 * (918 - 540) - 2 * 33.8  =  688.4 px       (LAW 12 rail)
at 56.2 px   688.4 / 56.2               =  12.249 em       per caption
```

Six of 52 phrases exceeded it and were cut at word boundaries. The cut is a
minimax partition over the phrase's words (exact DP), not a greedy fill, so a
split reads as two balanced beats rather than a full line plus an orphan:

```
'have literally infinite tools.'        -> 'have literally'    | 'infinite tools.'
'Hermes Agent managed to'               -> 'Hermes Agent'      | 'managed to'
"They introduced something that's"      -> 'They introduced'   | "something that's"
'called procedural disclosure.'         -> 'called procedural' | 'disclosure.'
'need without bloating your'            -> 'need without'      | 'bloating your'
'context, which is just unbelievable.'  -> 'context, which is' | 'just unbelievable.'
```

Each beat starts on the real `start` of its first word and ends where the next
beat begins, so the caption track is still gapless (0 discontinuities across all
58 beats) and the shortest split beat runs 0.44 s — nothing flashes.

Note the budget is deliberately stricter than LAW 12 requires HERE: at the top
seat the pill sits at y 231..345, above the rail band's 30 % line, so the 918
column is not even in play. Keeping it anyway holds this format inside the same
width envelope as the published factory (published widest pill 808 px, ours cap
at 726 px).

## Verified on the renders (`fix6_check.py`)

Three claims, all measured on decoded pixels of the shipped files:

**1. Containment.** The delivered mp4s are the wrong instrument for this — h264
re-quantises the whole frame when one band changes — so containment is measured
on a CRF-0 LOSSLESS pair of the same two projects. The pipeline is
bit-deterministic (rendering `fix5` twice gives 0 differing pixels at CRF 0 and
0 at delivery quality), so every difference below is real.

```
                 frames   caption-band     out-of-band       strongest
                 sampled  share of change  residue           out-of-band delta
scroll  r5 -> r6   40      99.776 %        3 frames, 4518 px   6/255  = 2.4 %
zoom    r5 -> r6   40      98.988 %        7 frames, 20546 px  20/255 = 7.8 %
```

Geography: every structural change is inside y 224..353 — the caption band. The
out-of-band residue is confined to soft gradients (the panel's bottom viewfade,
y 1664..1791) and to glyph-antialiasing hairlines, never exceeds 24/255 (the
delivery codec's own noise floor on this palette), and moves no edge: crops of
the worst frame (zoom t=19.28) are identical to the eye and the difference mask
is thin hairlines on existing glyph borders, not shifted shapes. Cause: Chrome
re-layerises when the caption node count changes from 52 to 58, so gradients
dither and glyph edges resample a hair differently.

In the SHIPPED mp4s the same comparison shows only 125 isolated pixels outside
the band over 14 frames (8.9 px/frame of 2,073,600), 125/125 of them on
pre-existing high-contrast edges.

**2. The canonical pill, on pixels.**

```
                 pill box height          glyph x-height
scroll fix6      113..114 px (114 x50)    26..27 px (27 x39)
zoom  fix6       113..114 px (114 x54)    26..27 px (27 x37)
authored         114.3 px                 27.2 px (Nunito sxHeight 0.484 em)
```

Two adjacent integer readings are the terracotta/white antialiasing boundary
landing on either side of a pixel, not two sizes: the authored box is a single
number and the width-recovered size is constant. ONE SIZE, ZERO DRIFT, both
cuts.

**3. Nothing under the pill.** 58/58 captions in each cut sit over ZERO document
ink — re-derived on the resized pill, not inherited. It is structural rather
than statistical: the pill's bottom edge (345) is 26.9 px above the artifact's
top edge (372), so on the scroll cut no scroll position and on the zoom cut no
camera stop — wide, header or card — can put ink under it.

## Reproducing the containment proof

```
CLI=projects/personal/infra/agent-tools/HyperFrames/packages/cli/dist/cli.js
for p in fix5 fix6 zoom_fix5 zoom_fix6; do
  node $CLI render $p -o /tmp/${p}_ll.mp4 --fps 25 --quality high --crf 0 --workers 2
done
python fix6_check.py out/artifactspine_fix5.mp4 out/artifactspine_fix6.mp4 \
       /tmp/fix5_ll.mp4 /tmp/fix6_ll.mp4
python fix6_check.py out/artifactspine_zoom_fix5.mp4 out/artifactspine_zoom_fix6.mp4 \
       /tmp/zoom_fix5_ll.mp4 /tmp/zoom_fix6_ll.mp4
```

The lossless pair is ~75 MB per file and is intentionally NOT kept in the repo.

## What did NOT change

The emitted HTML differs from round 5 in exactly three places, verified by diff:
the `<title>`, the `.scappill` padding/radius, and the caption clips. Window
(40,372 1000x1416, margins 40/40, scale 1.000000, doc 936), seat centre 288,
schedule (CUT_IN 2.84, CUT_OUT 50.20, face returns, seven arrivals, two hidden
moves), the no-peek-ahead solver (0 px peek and 0 px bleed-back on all six
transitions), the 30 state tweens, the pacing guard (351 events / 4 visible
moves / 6 face cuts on the scroll; 386 / 7 / 6 on the zoom), the ten camera
stops at one card width, counter formatting, Law 11 fills, all ten SFX cues and
25 fps are untouched.

Files: `artifactspine_fix6_core.py` (the canon, the splitter, page verification,
LAW 12 r6), `artifactspine_fix6_gen.py`, `artifactspine_zoom_fix6_gen.py`,
`fix6_ship.sh`, `fix6_check.py`, projects `fix6/` and `zoom_fix6/`, logs
`render_fix6.log` / `render_zoom_fix6.log`, results `fix6_check_scroll.txt` /
`fix6_check_zoom.txt`, frames in `fix6_snaps/`. Staged:
`~/Movies/Shorts Factory/Format Lab/Fixed6/artifactspine_fix6.mp4` and
`.../artifactspine_zoom_fix6.mp4` (1080x1920, 25/1 CFR, 1354 frames, 54.16 s,
15.9 MB and 16.9 MB).

The generator also refuses to emit a page that is not the canon:
`verify_page()` re-reads the produced HTML and fails the build unless the
`.scappill` rule carries every canonical declaration and every caption clip
carries font-size 56.2 at seat top 288.
