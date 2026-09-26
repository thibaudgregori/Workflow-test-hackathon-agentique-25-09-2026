# eudisclosure — WHITEBOARD author's notes

Where this board departs from `plans/eudisclosure_plan.json`, with the reason
and what I would have done otherwise. **The plan was built anyway everywhere it
did not collide with a law.** Two of the five notes are law overrides (the
brief's one sanctioned exception); the other three are the whiteboard's own
surface arithmetic, which the plan could not know because the plan's
`canvas_rects` were authored for the split/cutout core, not for a 576 x 460
board.

---

## 1. LAW OVERRIDE — the two declaration plates read `GENERATED` and `MODIFIED`, not `AI GENERATED` and `AI MODIFIED`

**The plan** (beat 3, `canvas_rects.tag-generated` / `tag-modified`): the two
plates read **AI GENERATED** and **AI MODIFIED**.

**The law that forbids it:** GLOBAL LAW 4, enforced as
`whiteboard_build.caption_identity_guard` — *"no drawn word may repeat a caption
pill that is on screen with it"*. Measured on this take's own chunker output,
caption beat 14 is the pill **`AI modified.`**, alive **12.88–14.04 s**. The
second plate is written at 12.98 s and lives to the 13.90 erase, so the pill and
the board word would share **every frame of their lives**. That is the exact
simultaneous double the guard exists to refuse, and it raises `SystemExit`
before a byte is written — the build cannot ship the plan's string.

**What I did:** dropped the `AI` from both plates so the pair stays a pair.
`generated` and `modified` are not pills anywhere in the take (the nearest are
`is AI generated or` and `AI modified.`), so the guard is silent and the
comparison still reads: the card above them is already named **AI IMAGES**, so
the board says *AI images: generated, or modified*. All four things the plan's
own `open_questions[2]` requires survive — both terms on the board, two visibly
different shapes (ink border vs terracotta border), one connector each into the
photo, and the border flip landing on the spoken word *modified* at 13.30.

**What I would have done instead** if the law allowed it: kept `AI GENERATED` /
`AI MODIFIED` verbatim; they are the sentence's own words.

## 2. DIVERGENCE FROM THE PLAN'S BEAT 6 — the outro carries no stamp glyph

**The plan** (beat 6): *"the chassis outro lockup starts on the video's own
themed object: the RUBBER STAMP, alone, with the terracotta rule, the JetBrains
Mono handle and the 'daily AI' micro-line under it."*

**Why it is not there:** the whiteboard's outro is not mine to compose. It is
authored by `whiteboard_build.outro_block()`, the shared harness — an opaque
cream sheet that rises over the board carrying the terracotta rule, the mono
`@migueltorrez.ai` and `daily AI` already printed on it. It takes no glyph
parameter and has no hook, and my brief forbids forking the harness
(*"Do NOT fork it and do NOT re-implement a board"*). Painting the stamp into
the board SVG cannot work either: the sheet is opaque and full-zone by
construction, which is the whole reason round 1 of that outro's double-exposure
defect is impossible.

Every approved whiteboard this factory has shipped — `geminitools`,
`shieldstral`, `harnessrace` — ships this same outro. **This is a harness
limitation to raise with the format owner, not a per-video fix**, and the split
and cutout lanes DO carry the themed stamp in their own outro (the scene module
authors `#o-glyph`), so the plan's intent is honoured on two of the three
platforms.

**What I would have done:** added an optional `glyph=` argument to
`outro_block()` that seats a caller-supplied SVG above `OUTRO_RULE_TOP_U` on the
sheet. That is a change to a shared law file and belongs to a deliberate task.

## 3. THE GEOMETRY IS THE BOARD'S OWN, NOT `plan.canvas_rects`

The plan's `shared_layout_note` says its rects are the ONE geometry for all
three platforms, and for the two DOM lanes it is. The whiteboard is a third
space: a 576 x 460 board scaled by S = 1.875 into the canvas, whose legal
surface is x 40..536 / y 150..425 and whose caption band, right rail and top
band are all measured in board units. So every rect here was re-derived on that
surface and the plan's numbers were used as the **structure** (what is beside
what, what is symmetric with what, what carries which mark), never as
coordinates. The plan's own artwork lane did the same thing for the same reason
and said so in `plans/eudisclosure_scene_handoff.md` §2 — *"a frame-normalised
box that is right for the split is wrong for you."*

Measured on this board: topmost ink **152.5 u** (band 102.4), marker top
**110.7 u**, lowest ink **775.7 px** against a caption band top of **799.2 px**
(23.5 px clear on line boxes, 35.3 px on glyph ink, 41.3 px to the pill's
painted edge), zero right-rail intrusions, tightest non-block gutter **13.1 u
(24.6 px)** — over Miguel's 24 px aim, not merely over the 15.9 px refusal line.

## 4. THE PHONE-TEST INSTANTS MOVED, AND ONE OF THEM SAVED THE TEST

The plan's `bespoke_objects` name held instants 1.20 / 8.60 / 19.70. On this
board 8.60 and 19.70 are instants at which **the marker sprite is still on the
object** — the pen was mid-stroke on the photo's sun and mid-stroke on the
slider's thumb — and round 1's crops came back with a pencil lying across both.
The pen fades 0.08 s after a stroke whose successor is more than 0.55 s away and
is hard-killed 0.16 s later, so each object is now cropped in its own first
settled, marker-free window: **1.20 / 10.50 / 20.20**. Nothing about the drawing
or its timing changed; only where the camera looks.

## 5. THE SLIDER WAS REDRAWN TWICE BEFORE A COLD READER WOULD NAME IT

Recorded, not laundered. The plan's `how_drawn` for the slider is *"a round knob
r=17 with a thicker stroke sitting on the track"*.

| version | what it was | four independent cold readers said |
|---|---|---|
| v1 | outlined rounded thumb, 12 x 38, the track drawn straight through it | `brightness dimmer slider` **unsure** |
| v2 | opaque thumb, 16 x 38, radius 7 (a wide rounded rectangle) | `light switch` **cannot tell** |
| v3 | slim capsule 11.2 x 29.8 at radius = half its width, interrupted track, small-sun-to-big-sun scale | `brightness slider control` sure / `dumbbell` unsure / `brightness slider (dimmer switch)` unsure / `brightness slider control` sure |

v1 read as a bead threaded on a wire because the track ran through the thumb;
v2 read as a rocker switch because a wide rounded rectangle on a bar IS one.
v3 is the artwork lane's own proven slider proportions (`gen/eudisclosure_scene.py
::slider_svg`, sealed 4/4 `brightness slider` sure) scaled by k = 164/264 onto
this board and drawn in marker ink. **The plan's round knob was never built** —
its own author had already found and recorded the same failure
(`eudisclosure_scene_notes` learning 3: *"a circle on a line is a node, not a
control"*), so building the plan's letter here would have been building a defect
the plan itself had superseded.

The plan's `open_questions[4]` is answered as it asked: the knob's travel stayed
at **14 canvas px** — the smallness IS the claim — and the fix went into the
knob's shape, never into its distance.

---

## Not departures — the plan built as written

The lane (diagram build, chaptered), the three chapters and their two erase
times (6.15 / 13.90), the anchor block that never leaves, the one 108 px block
displacement at 3.32 and the one 270 px photo displacement at 15.92, the five
identical terracotta impressions and their five hosts, both emphases as BOXES on
drawn objects (never a ring, never a highlight — there is no raster in this
video), the two mirrored connectors built with `anchor_points`, all seven written
keys on their spoken words, the key term first / alone / large, zero pointing
cues and therefore zero source cards, and no registry mark anywhere on the stage.
`plan.open_doubts` was empty and I found none.
