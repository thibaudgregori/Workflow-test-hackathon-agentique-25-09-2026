# FORMAT LAB — WHITEBOARD FIRST

Source: `format_lab/hermesinfinite` (the shipped cut of *"Hermes Agent can now
have literally infinite tools"*, 54.17 s, 369 word timings).
Format id: `whiteboard`. Three variants, all 1080x1920, all the full 54 s.

Generators: `whiteboard_v1_gen.py` / `_v2_` / `_v3_` (thin) over
`whiteboard_core.py` (the whole format). `whiteboard_sfx_gen.py` generated the
ElevenLabs cast ONCE into `sfx/` and all three variants reuse it.
`whiteboard_preview.py` drives the real GSAP timeline headless and screenshots
named seconds — the loop that caught every defect below before a single render.

---

## What the format is

The visual zone is ONE drawing for the whole video. No scenes, no swaps, no
transitions: a single 576x460 board (in factory design units) that only ever
gains ink. Every shape draws itself on with a marker stroke
(`stroke-dashoffset` over a hand-jittered Catmull-Rom path) at the moment its
words are spoken, and nothing ever leaves. At 49.5 s four terra corner brackets
close the board and the argument is one readable diagram:

```
   TOOLBOX ══╳══════ the bulk route, crossed out ═══════▶ AGENT   (nous mark)
      │                                                     │
      └──────────[ VALVE ]──────────────────────────────────┘
             PROCEDURAL DISCLOSURE                    CONTEXT ▮▮░░░░░ ‖
      ∞  the toolbox does not end                     finite, and never fills
```

Beat-to-ink map (all anchors are pinned to word INDEX **and** word text in
`ANCHOR` / `ANCHOR_TEXT`, so a re-transcription fails the build instead of
silently sliding the choreography):

| words | ink |
|---|---|
| "Hermes Agent…" 0.22 | the agent node draws, CENTRED, mark + name |
| "literally" 1.50 | the agent DISPLACES right; the toolbox draws in the space it left |
| "infinite" 2.08 | the toolbox's bottom edge sprouts a trail — the box does not end |
| "tools / loads / every" 2.52–4.58 | 3 + 3 + 3 cells; the box is full exactly on "every tool all at once" |
| "tool … all at once" 4.84 | the fat bulk route elbows over the top, crowded with tools |
| "they don't" 7.00 | terra ╳ across it; the whole route drops to 26 % and stays as evidence |
| "crack the code" 9.56 | the real route draws, with a GAP left in the middle |
| "introduced" 10.70 | the valve seats into the gap |
| "procedural disclosure" 11.88 | the key term writes under it, ON the composition axis |
| "it's very simple" 14.62 | the valve handle turns — it opens |
| "the tools it needs / when it needs them" 17.1, 19.2 | packets leave named cells, run the route through the valve, land inside the agent |
| "tools consume context" 20.0 | the meter draws under the agent; the fill jumps to 42 % |
| "finite" 22.36 | the end wall, drawn heavy then doubled |
| "very picky" 25.94 | 3 cells get rings, 6 go quiet, the fill drops to 26 % |
| "Nous Research" 30.78 | a terra ring lands on the mark that was already there |
| "all of the tools we will ever need" 35.64 | the 6 quiet cells come back; the ∞ draws; ghost cells appear on the trail |
| "no longer have to worry" 38.10 | rings appear on the other 6 — the constraint is released, not contradicted |
| "MCP servers" 44.06 | MCP takes a cell of its own |
| "without bloating your context" 47.48 | a terra ceiling draws; the fill nudges 26 → 31 % and stops well short |
| "unbelievable" 49.50 | four corner brackets close the board |
| outro 50.74 | a 94 % cream scrim reads the drawing down, chip centred over it |

---

## The three variants

**v1 PLAN VIEW** — `out/whiteboard_v1.mp4`
The camera never moves. The whole board is in frame from frame 0 and the viewer
watches the map fill in. Structural SFX only (displacement whoosh, valve click,
∞ thump, packet arrivals).

**v2 CAMERA FOLLOW** — `out/whiteboard_v2.mp4`
Identical drawing at 1.6x, on a board larger than the zone. The camera CUTS
between framings at beat boundaries and holds (Law 1: it never drifts), then
pulls WIDE at 49.4 s over 0.95 s to reveal the whole structure — the vertical
RSA-Animate move. Eleven moves, seven distinct framings.

**v3 INK + HAND** — `out/whiteboard_v3.mp4`
v1's board plus a marker object whose tip leads every stroke, riding the exact
point list the stroke was generated from, resampled to equal arc-length steps so
it can never race its own ink. It fades out between strokes more than 0.55 s
apart and taps for pop-in elements. Adds the ElevenLabs felt-pen layer
(`marker_short` / `marker_long` / `marker_squeak`) that v1 and v2 deliberately
do not have — so the hand and its sound are tested together, as one device.

---

## My ranking

**1st — v3 (INK + HAND).** The hand is what makes "whiteboard" read as a
whiteboard rather than as a diagram that happens to fade in. The pen also fixes
the format's structural weakness for free: on a board where nothing ever leaves,
the viewer's eye has no idea where to look, and the pen is a permanent, diegetic
attention pointer. The marker SFX pays for itself at the same moment. Cost: the
pen is a large opaque object and it occludes the ink it is drawing (unavoidable
— real hands do too), and it makes every stroke's timing visible, so any stroke
whose pacing is slightly off is now obvious rather than merely felt.

**2nd — v1 (PLAN VIEW).** The most legible and the most honest to the brief:
you can see the whole argument accumulating, which is the entire point of the
format. It is also the safest — no crop, no ambiguity, every element phone-legible
at all times. It loses to v3 only because 54 s of a fixed wide frame with small
increments is calm to the point of passive; the events are all real but they are
small on screen.

**3rd — v2 (CAMERA FOLLOW).** The best individual frames of the three — the
toolbox and agent close-ups are genuinely handsome, and the final pull-wide is
the strongest single moment in the whole experiment. But it fights the format's
own premise: the promise of "nothing ever leaves" is only cashed if you can SEE
that nothing left, and a camera that has to crop keeps taking the accumulated
board off screen. It also makes type size a function of the camera, so the same
label is 2.3x bigger at one stop than another. If it were adopted it would need
its own airier board, not a scaled copy of the plan-view one.

---

## What fought me

**The round-cap dot (the real bug of this build).** `stroke-dasharray:1000` +
`stroke-dashoffset:1000` reads as "not drawn yet", but the dash BOUNDARY lands
exactly on the path origin and `stroke-linecap:round` paints a zero-length dash
as a dot. Every undrawn stroke on the board was therefore leaving a coloured
pinprick at its start point from frame 0 — two terra specks beside the agent's
mark at t=1 s that were actually the valve triangles arriving 10 s early. Fix:
`stroke-dasharray:1000 3000` with the offset parked at 1005, which puts the
whole path strictly inside the gap with no boundary on it.

**CSS transform beats the SVG transform attribute.** GSAP animates SVG targets
by writing the `transform` ATTRIBUTE, and an inline `style="transform:scaleX(0)"`
silently wins over it — the element GSAP thinks it is animating never moves.
All initial transform state now comes from `tl.set(...)` at time 0 and initial
visibility from the `opacity` presentation attribute.

**`page.evaluate` on a GSAP call.** `evaluate("tl.progress(1).progress(0)")`
returns the Timeline, and Playwright then tries to serialise it — the preview
harness hung for minutes with no error. Every timeline call in
`whiteboard_preview.py` is wrapped in an arrow function that returns nothing.

**The camera cuts through type.** The first v2 schedule sliced the terra key
term at six stops out of twelve, which reads as a broken render rather than a
camera. The layout has exactly two vertical gaps (164..190 and 386..396) and the
schedule is now solved so every horizontal cut lands in one of them or off the
board. This is the transferable lesson: on a camera lane, framings are computed
from the layout's gaps, never hand-eyeballed.

**A hand-listed lemniscate smooths into a bowtie.** The ∞ was authored as a
control ring and Catmull-Rom turned it into a vertical butterfly. Replaced with
sampled Bernoulli — a figure-eight by construction, and it traces in one
continuous stroke from its right tip, which is exactly how a hand draws it.

**Type inside a card is sized by the card, not by taste.** "HERMES AGENT" on one
line in a 152 u card forces fs ≤ 15.7 u, under the phone-legibility floor; at 19 u
it hung off both card edges. Set on two lines at 18 u it fits with margin. Same
arithmetic capped the key term at 26 u — the largest size that still leaves a
10 u channel to the agent card.

---

## Laws this format would need if adopted

1. **ONE BOARD, ONE COORDINATE SPACE.** A whiteboard short is a single SVG in
   one user space for the whole duration. No clip swaps in the visual zone —
   the format's entire claim is that the viewer is watching one artefact grow.
2. **INK ARRIVES ON ITS WORD, AND NEVER LEAVES.** Every element's draw start is
   anchored to a word index AND its text (the build fails if the transcript
   moves). Removing ink is banned; a superseded idea is struck through or
   dimmed and STAYS as evidence, the way the crossed bulk route does here.
3. **THE FINAL FRAME IS THE DELIVERABLE.** The board must be composed as a
   still first and animated second: it has to survive a squint test at 49 s as
   one coherent diagram. Practically that means the board's bounding box is
   centred on AX and declared in the generator (`BOARD_BOX`), and the generator
   asserts it never reaches the caption band.
4. **GAPS ARE STRUCTURE.** The layout must publish its vertical gaps, because
   they are what any camera, ring, or annotation is allowed to cut through.
   No framing, highlight, or scrim edge may land inside a word.
5. **NO EMPTY VESSEL, EVEN HERE.** Law 20 still binds: the opening object draws
   with its mark and its name inside 1.3 s. An outline drawn and left blank for
   a beat is the same failure it is everywhere else.
6. **THE PEN IS AN OBJECT, NOT A HAND.** If the hand device is adopted, it ships
   as a marker/pen with its tip at the path origin, driven by the same point list
   that generated the stroke — never a drawn hand, never a floating cursor with
   its own idea of where the ink is. It fades out between strokes rather than
   sliding across empty board (Law 1).
7. **CAMERA MOVES ARE EVENTS.** On the camera variant, every move starts on a
   beat boundary, lasts ≤ 1 s, and is followed by a hold. No continuous drift,
   no easing that never settles. The wide reveal is allowed exactly once.

---

# FIX ROUND 1 — 2026-08-30

Authority: `format_lab/REVIEW_2026-08-30.md`. Two deliverables, one module
(`whiteboard_fix_core.py`), thin entry points `whiteboard_fix_gen.py` and
`whiteboard_zoom_fix_gen.py`. Both render **1080x1920 @ 25 fps, 1354 frames,
54.165 s** into `out/`, staged to
`~/Movies/Shorts Factory/Format Lab/Fixed/`.

| deliverable | what it is |
|---|---|
| `whiteboard_fix.mp4` | v1's approved PLAN VIEW + v3's pen, squeak solved |
| `whiteboard_zoom_fix.mp4` | v2's CAMERA FOLLOW, both defects fixed |

## Global laws applied to both

**Law 6 — 25 fps.** `whiteboard_band_25.py` cuts a fourth face derivative from
the 4K master with the 273 conform duplicates dropped (the same `RUNS` /
`setpts` / kept-splice-dupes model as `_shared/build_face_crops.py`, so it is
frame-locked to the three shared plates). Both variants render at
`data-fps="25"`.

**Law 1 — the zoom cap, for a band and not a canvas.** The whiteboard's face is
a 1080x1057.5 px band, not a full canvas, so none of the three shared plates is
a drop-in. The band's own physical floor is a **2204x2160** master window
(`2160 * 1080/1058`); anything wider cannot fill 1080x1058 from a 2160-tall
master. That lands head_frac at **0.304** against the lab's measured **0.311** —
i.e. v1 was already within 2 % of the widest framing this geometry can support,
and the fix banks the remaining 2 % rather than pretending there was more.
Filling the band from `face_wide_25.mp4` with `object-fit:cover` is the same
window arithmetically (2592 x 1080/1269 = 2206); cutting it from the master
instead just scales once instead of twice.

**Law 2 — the tamed palette.** Every cue now comes from `_shared/sfx/` at its
pinned class volume, with no hand-tuned lead offsets (the palette is
onset-trimmed, so the old offsets would double-count). The cue POSITIONS are
v1's exactly — this is a level and character swap, not a re-scoring:

| beat | was | now | class |
|---|---|---|---|
| "literally" (the agent displaces) | `whoosh` | `soft_whoosh` | structure `0.120` |
| the valve seats / the valve opens | `valve_click` x2 | `tick` x2 | detail `0.077` |
| "finite" (the end wall) | `valve_click` | `tick` | detail `0.077` |
| the infinity | `ink_thump` | `low_thump` | structure `0.120` |
| 5 packet arrivals | `pop` | `pop` | detail `0.077` |
| the brackets close | `marker_long` | `soft_whoosh` | structure `0.120` |
| **`marker_squeak`** | 4 cues | **deleted** | — |

11 cues over 54 s after the 0.42 s de-dup.

**Law 3 — rounded fills.** The context meter still drives its `width`
ATTRIBUTE with `rx` constant. Do not put it back on `scaleX` under a
`userSpaceOnUse` clipPath: the transform scales the clip with the rect and the
rounded cap collapses to a straight edge.

## (a) `whiteboard_fix` — the pen, and what happened to the squeak

Nothing about v1's drawing moved: `LAYOUT_A` is v1's geometry to the unit, the
camera is identity, and the pen is v3's object driven by the same arc-length
resampled point list.

**The pen KEEPS a sound**, and it is `pen_loop.mp3` at the pinned loop volume
`0.038`. Judged, not assumed — `whiteboard_penproof.py` rebuilds the exact
layer this variant schedules over the real voice and bed and measures it on the
factory's pinned instrument:

| | old `marker_squeak` @0.18 | new `pen_loop` @0.038 |
|---|---|---|
| layer peak | **-30.47 dBFS** | **-45.57 dBFS** (15.1 dB quieter) |
| in-window body (p85) | -37.58 | **-48.07** (10.5 dB quieter) |
| vs bed presence (-34.47) | 4.0 dB **OVER** | 13.6 dB **UNDER** |
| lift over the bed in its own windows | **+1.85 dB** | **+0.14 dB** |
| harshness `hf6k` | 0.548 | **0.203** |
| speech-margin cost | 0.51 dB | **0.05 dB** |

Silence was the other legal answer and it was the wrong one: the pen is a large
opaque object whose whole job is to say "a hand is doing this", and a silent
hand reads as a floating graphic. The palette's `pen_loop` is the same gesture
with the squeak filtered out (6.5 kHz low-pass) and the body 12.5 dB down, so it
removes exactly the thing Miguel rejected and keeps the thing he liked. 13
instances, 7.67 s of pen sound over 54 s — a **14.2 % duty cycle**, which is
what "ration them" means for a sustained layer.

## (b) `whiteboard_zoom_fix` — the camera, solved instead of typed

### The safe-margin law (defect 1)

Stated so a build can check it. Every element that reads as a **container** or
as **type** registers its design-unit bbox and its on-screen window
(`Board.rigid`). At every stop, for every element on screen:

> **No edge of a box may sit within `MARGIN_PX = 44` of any frame edge.** It may
> be entirely off camera, or entirely inside with margin, or cut through its own
> body — never grazing. **Type is never cut**: fully inside with margin, or not
> on screen. A box that IS cut must keep **>= 40 %** of its area, otherwise it is
> a fragment (a stray corner in the corner of the frame — the exact thing that
> was wrong at v2 t=32). Boxes are measured with **3u of ink padding**, because
> hand-drawn stroke plus wobble lands outside the construction rectangle.

Marks (<= 12u — the bulk-route dots, the delivered-tool squares) and connectors
(routes, risers, the trail, the key-term leader) are exempt: a line or a stream
of dots running off the frame edge is the drawing continuing, which is true.

### Why the board had to be recomposed (and not just the stops)

Miguel offered both ("recompose the board or the stops"). The solver settles it:
on LAYOUT_A the terra key term (x 190..386) sits at the **same height** as both
cards (y 104..252), so it spans the only vertical lane a camera could cut
through. Work the constraints and every framing that neither cuts a card nor
cuts a word collapses to `z <= 0.62` — the plan view. **Every close-up the
shipped v2 attempted was illegal by construction**, which is precisely what the
clipped agent card at t=32 and the grazed toolbox at t=27 look like.

`LAYOUT_B` therefore moves the key term into a band of its own below the cards
(2 lines, fs 20, y 296..355), opens a real centre lane by pulling the cards
outward (toolbox 34..176, agent 400..542, both 150 tall), and drops the
ghosts / infinity / meter row onto a clean 36u gap. Same elements, same drawing
code, same argument — only the numbers move, and `LAYOUT_A` is untouched next to
it so the approved variant cannot drift.

Two collisions LAYOUT_B introduced and the solver did not catch (they are
element-vs-element, not element-vs-frame, so they were caught by eye on the
preview): the terra Nous ring's bottom edge ran through "HERMES", and the
delivered-tool squares ran into the second name line. Fixed by
`NAME_DY1 98 / NAME_DY2 118 / GOT_DY 128`. **A frame gate is not a layout gate.**

### The schedule (defect 2 — centring)

`solve_stop()` searches z in 0.02 steps over 0.50..1.86 and offsets in 5u steps
to +/-40u, scoring `|z/z_pref - 1| * 3 + (|dx|+|dy|)/60`, and returns the
cheapest framing that passes the gate AND holds the subject with 60 px of its
own margin. **The view centre IS the subject centre**; the offset is bought, not
free, and 11 of 12 stops came back at exactly `(0, 0)`:

```
  0.00  AGENT0      z 1.30  offset 0,0    the agent opens, alone, on the axis
  1.50  WIDE_EARLY  z 0.62  offset 0,0    it displaces; toolbox draws and fills
  9.56  VALVE       z 1.80  offset 0,0    the real route; the valve seats
 11.88  KEYTERM     z 1.80  offset 0,0    PROCEDURAL DISCLOSURE writes
 14.62  VALVE       z 1.80  offset 0,0    "very simple" — the valve opens
 17.14  AGENT       z 1.38  offset 0,0    the packets arrive
 20.00  METER       z 1.80  offset 0,10   the meter draws, fills, walls
 26.30  TOOLBOX     z 1.34  offset 0,0    "very picky"
 30.78  AGENT       z 1.38  offset 0,0    Nous Research
 35.64  INFINITY    z 1.82  offset 0,0    the toolbox does not end
 38.10  TOOLBOX     z 1.34  offset 0,0    every cell rings; MCP takes cell 0
 47.48  METER       z 1.80  offset 0,10   the ceiling it never reaches
 49.40  PULL WIDE   z 0.56  offset 0,0    the reveal, 0.95 s, the only long move
```

The one offset (10u down on the meter) is forced: without it the frame's top
edge lands on the agent card's bottom edge. Written to
`whiteboard_zoom_fix/camera_plan.json` on every build. Every hold is >= 1.37 s
after its move (asserted >= 1.20 s); every t is a spoken beat.

**One stop was deleted rather than shipped off-centre.** A framing on the
crossed bulk route only passes the gate 25u off the X's centre (it has to push
the agent card fully out of frame), and an off-centre component is the whole
defect this round exists to fix. The wide framing already owns the crossed
route, so the camera simply does not move for it — Global Law 5.

The pull-wide is the only move longer than 0.62 s and it comes off the tightest
framing in the piece (METER at z 1.80), so the reveal is a **3.2x pull** even
though the wide itself is only 0.62 -> 0.56.

## Laws this adds to the format

8. **A CAMERA STOP IS SOLVED, NOT TYPED.** Framings come from a subject bbox
   plus a gate over a registry of the drawing's own boxes and type. A hand-typed
   stop table cannot be checked, and this one was wrong at 5 stops out of 11.
9. **THE VIEW CENTRE IS THE SUBJECT CENTRE.** Offsets are a last resort, are
   scored, and are reported per stop in `camera_plan.json`.
10. **A CAMERA VARIANT OWNS ITS OWN LAYOUT.** A board composed for a fixed wide
    frame packs edge to edge and leaves a camera nowhere legal to cut. The
    camera lane gets bands with real gaps; the plan-view lane keeps its own.

---

# FIX ROUND 2 — 2026-08-30

Authority: `REVIEW_2026-08-30.md` **ROUND 2**. Verdicts for this format:

> **whiteboard: "amazing!"** One bug: the pencil is not at the Hermes box while
> the box draws at the start. Fix only that.
> **whiteboard_zoom**: improved; add PERIODIC PULL-BACKS to the whole diagram so
> the big picture is refreshed — "from time to time", not constant.

Both deliverables come out of the same module (`whiteboard_fix_core.py`), still
1080x1920 @ 25 fps, 1354 frames, 54.165 s, staged to
`~/Movies/Shorts Factory/Format Lab/Fixed2/`.

| deliverable | what changed against round 2 |
|---|---|
| `whiteboard_fix2.mp4` | the named pen bug, and nothing else |
| `whiteboard_zoom_fix2.mp4` | three periodic pull-backs to the whole board |

## (a) `whiteboard_fix2` — the pen bug, root-caused

**It was not the pen's path. It was the pen's coordinate space.**

The agent card is authored at its FINAL x (`AG_X 396`) and lives inside
`<g id="agent" transform="translate(-345px 0)">`, because the format's opening
beat puts it alone on the composition axis and only DISPLACES it right on
"literally" (1.50 s). The pen is a sibling of that group, in raw board space.
Every stroke recorded its point list at authoring coordinates, so for the first
1.5 s the pen was driven to where the ink *would eventually be*, not where it
was being drawn:

```
dx = AX - AG_CX = 288 - 472 = -184 u  =  -345 px of a 1080 px frame
```

Four events were affected, all of them in the opening: the card outline
(0.30 s), the Nous mark tap (0.56 s), and both name lines (0.90 / 1.08 s). The
pen sat 345 px to the RIGHT of the box it was drawing — a third of the frame.
Everything after 1.50 s tracked correctly because the group is back at x:0 and
authored coordinates ARE live coordinates from then on, which is exactly the
asymmetry Miguel described ("the rest of the video tracks fine").

**The fix is a live-offset publication, not a special case.** `Board` now carries
`pen_shift` / `pen_shift_until`; a group that is translated while its ink draws
declares its offset for exactly as long as the displacement lasts, and the three
stroke-recording sites (`stroke`, `pop`, `label`) apply it through `_pen_pts`.
It is guarded by TIME, not by group membership, so the same group's later ink
(the terra Nous ring at 30.78 s, the delivered-tool squares) is untouched.

Measured before/after on the opening card stroke (pen x range, px):

| | pen | the ink it is drawing |
|---|---|---|
| before | 741 .. 1029 | 396 .. 684 |
| after | **396 .. 684** | 396 .. 684 |

**Nothing else moved.** The board, the choreography, the captions, the outro and
the camera identity are byte-for-byte round 1's. The pen SOUND is unchanged too:
`pen_intervals` reads only `t`/`d` and the degenerate-point test, and shifting
both endpoints of a segment equally preserves all three — the layer is still 13
instances / 7.67 s / 14.2 % duty cycle, so round 1's `whiteboard_penproof.py`
measurements still hold without re-running them.

**The transferable law** (new format law 11 below): a pen that rides a point list
rides the LIVE position of the ink. Authored geometry and live geometry are the
same thing only for elements that are never transformed, and this format
displaces its opening object by design.

## (b) `whiteboard_zoom_fix2` — periodic pull-backs

Three, not "from time to time" as a mood but as a solved rhythm: **24.20 s,
33.54 s, 40.58 s**, plus the final reveal at 49.40 s. Gaps of 9.3 / 7.0 / 8.8 s
against a 54 s piece, and the video already opens on a wide (WIDE_EARLY holds
1.50 → 9.56). That is one big-picture refresh roughly every 8 seconds and
nothing tighter — "not constantly", checked as a number rather than felt.

**Each pull-back is a CHAPTER SEAM, not a timer.** The brief asked for moments
where a chapter of the drawing completes; all three are the first word of the
sentence that opens the *next* chapter, so no ink is ever left mid-draw behind a
camera move (Global Law 5 — the move has a spoken reason):

| t | word | the chapter that just finished |
|---|---|---|
| 24.20 | *"…best way to **handle** your context"* | the cost: meter drawn, 42 % fill, the doubled end wall |
| 33.54 | *"the lab behind Hermes have **managed** to…"* | Nous: the terra ring has landed on the mark |
| 40.58 | *"**If** you have a Hermes agent…"* | the release: rings on all 12 cells, the ∞, the ghosts |

They are added to `ANCHOR` / `ANCHOR_TEXT` like every other beat, so a
re-transcription fails the build instead of sliding the camera.

**They are solved by the same gate as everything else.** No new machinery: the
pull-backs are `WIDE` stops through `solve_stop()`, and all three came back at
**z 0.560, offset (0,0)** — identical to the final reveal, which is correct,
because "the full diagram" is a solved framing and there is only one of it. The
z is bounded by width, not height: `BOARD_BOX` is 556 u wide, so
`278 + 60/(3z) <= 180/z` gives `z <= 0.5755`, and the solver's 0.02 grid lands
on 0.56.

**The final reveal is still the reveal.** It is distinguished by DURATION, not by
framing — the three refreshes move in **0.52 s** (a glance) and the reveal in
**0.95 s** (a settle), it comes off the tightest stop in the piece (METER at
z 1.80, a 3.2x pull), and it is the frame the corner brackets close on and the
outro scrim reads down.

The schedule went from 13 stops to 17. One stop is genuinely new rather than
inserted: the TOOLBOX return at `a["mcp"]` 44.06, because pull-back 3 now sits
inside what used to be a single 9.4 s TOOLBOX hold and MCP still needs its
close-up. Every hold is re-asserted `>= 1.20 s` after its move; the tightest is
now 1.37 s (METER at 47.48, unchanged from round 1) and the pull-backs hold
1.58 / 1.58 / 2.96 s.

```
  0.00  AGENT0      z 1.30  the agent opens, alone, on the axis
  1.50  WIDE_EARLY  z 0.62  it displaces; the toolbox draws and fills
  9.56  VALVE       z 1.80  the real route; the valve seats
 11.88  KEYTERM     z 1.80  PROCEDURAL DISCLOSURE writes
 14.62  VALVE       z 1.80  "very simple" — the valve opens
 17.14  AGENT       z 1.38  the packets arrive
 20.00  METER       z 1.80  the meter draws, fills, walls   (offset 0,10)
 24.20  WIDE        z 0.56  ** PULL-BACK 1 **               0.52 s / hold 1.58
 26.30  TOOLBOX     z 1.34  "very picky"
 30.78  AGENT       z 1.38  Nous Research
 33.54  WIDE        z 0.56  ** PULL-BACK 2 **               0.52 s / hold 1.58
 35.64  INFINITY    z 1.82  the toolbox does not end
 38.10  TOOLBOX     z 1.34  every cell gets a ring
 40.58  WIDE        z 0.56  ** PULL-BACK 3 **               0.52 s / hold 2.96
 44.06  TOOLBOX     z 1.34  MCP takes a cell of its own
 47.48  METER       z 1.80  the ceiling it never reaches    (offset 0,10)
 49.40  WIDE        z 0.56  THE REVEAL                      0.95 s
```

Round 1's fixes are intact and were re-checked on the preview, not assumed:
`MARGIN_PX 44` still passes at all 17 stops, 16 of 17 sit at offset (0,0) with
the one forced 10 u meter nudge unchanged, and the final pull-wide is still the
last move in the piece.

## Face band and the 0 % standard

`_shared/ZOOM_STANDARD.md` §1 is explicit that the 0 % window is the **full-face**
reference and that shoulders-in framing stays on its own canvas. This format has
no full-face beat and no punch-ins: its face is a fixed **1080 x 1057.5 px band**
under the drawing zone, cut once from the 4K master at `crop=2204:2160:772:0`
(`whiteboard_band_25.py`), head at **30.4 % of band height**. That is the band's
PHYSICAL floor — a 1080-wide, 1058-tall full-bleed window of a 2160-tall master
cannot exceed 2204 px of master — and it is a long way wider than the 0 % window
(1216 px of master, head 56.3 % of frame height). So the standard is **not
applicable here and the band is unchanged**: there is nothing to punch into, and
nothing to pull back from. If a future whiteboard variant ever wants a full-face
beat, it cuts to `face_zoom00_25.mp4` as a mode switch, at 0 % or 5 %, per
ZOOM_STANDARD §3-4 — it does not scale this band.

Global Law 11 (continuous-pill fills) needed no work in this format: the context
meter has always driven its `width` ATTRIBUTE with `rx` constant, which is one
continuous pill by construction. The two terra verticals near it are the *end
wall* ("finite") and the *ceiling* ("without bloating your context") — named
elements of the argument, not fill ticks or end markers.

## Laws this adds to the format

11. **THE PEN RIDES LIVE INK, NOT AUTHORED GEOMETRY.** A stroke inside a group
    that is transformed while it draws must publish that transform to the pen for
    exactly the duration of the displacement. Authored coordinates equal live
    coordinates only for untransformed elements, and this format's opening beat
    is a displacement by design.
12. **A PULL-BACK IS A CHAPTER SEAM.** On a camera lane over a board that only
    ever gains ink, the camera returns to the whole diagram when a chapter's ink
    is complete — anchored to the first word of the next sentence, never to a
    timer, and never mid-draw.
13. **THE REVEAL IS DISTINGUISHED BY DURATION, NOT BY FRAMING.** "The full
    diagram" is a single solved framing; if the refreshes and the finale share
    it, the finale earns its weight from a slower move off a tighter stop, not
    from a wider z that does not exist.

---

# FIX ROUND 3 — Morgane's review (task: whiteboard3)

Authority: `REVIEW_2026-08-30.md`, all three rounds. Morgane's two whiteboard
notes ("pen SFX too loud vs voice at the start AND inconsistent across the
video"; "diagram TOO COMPLEX for a small phone screen — the symbol above
*procedural disclosure* is not self-evident"; "possible top-of-screen collision
with phone UI"), Miguel's rulings (zoom program deferred until the new lens: no
punches, no virtual set, no matte, no blur pad), and **Global Law 12**.

Deliverables, both 1080x1920 @ 25 fps, both 54.17 s:

| file | staged |
|---|---|
| `out/whiteboard_fix3.mp4` | `~/Movies/Shorts Factory/Format Lab/Fixed3/whiteboard_fix3.mp4` |
| `out/whiteboard_zoom_fix3.mp4` | `~/Movies/Shorts Factory/Format Lab/Fixed3/whiteboard_zoom_fix3.mp4` |

Generator: `whiteboard_fix3_gen.py` over `whiteboard_fix3_core.py`.
Gates: `whiteboard_fix3_pen.py` (the SFX asset), `whiteboard_fix3_penproof.py`
(the mix), `whiteboard_fix3_law12.py` (pixels of the finished files).

## ONE BOARD, BOTH LANES

Round 2 needed two layouts because the key term sat in the only vertical lane a
camera could cut through. The round-3 recomposition drops the term into a clear
band BELOW the road, which opens the lane again — so `LAYOUT_A` / `LAYOUT_B` are
gone and there is a single `L`. That is also literally what Miguel asked for:
*"the same simplified board on the camera lane"*.

## (a) THE BOARD, BOILED DOWN

**The symbol is now a BOOM GATE.** The bowtie valve Morgane could not read is
deleted. In its place, on the road between the toolbox and the agent, is a post
with an arm lying across the road; at *"it's very simple"* the arm lifts and the
tool packets run through. Nobody has to be taught what a barrier that lifts
means, and it says the right thing — the agent sees the tools **when it needs
them**, not before.

The lift is BOUNDED, and the bound is geometric rather than taste: an arm of
length L on a pivot at y=238 reaches `238 - L*sin(open)` when it lifts, and the
crossed dump lane sits at y=170. A 74u arm opening to 45 deg tops out at y=186 —
clear of the lane, clear of the X, steep enough to read as OPEN. The first two
attempts (98u at -45 deg, 106u at -58 deg) swung the arm straight through the
crossed lane above it, which is why the X also moved off the axis to x=215: it
clears the arc.

**Everything else that went.** Same pass, same reason (one idea per glyph):

| gone | why |
|---|---|
| the overhead bulk detour (4 bends + 8 dots + a chevron) | now a straight second lane in the channel: 5 tool squares, one X. It was also the only thing that sat under the phone's top UI. |
| the 3 ghost cells + 2 trail ticks | the ∞ already says "it does not end". Two glyph groups for one idea. |
| the 5 "got" tiles inside the agent | the context bar IS the receipt for an arriving tool. |
| the free-floating CONTEXT meter, its caption, its DOUBLED end wall, its ceiling tick | one slim capacity bar inside the agent card, with a single terra end mark on "finite". A bar with an empty track needs no caption to say "this fills up and it ends". |
| the 4 corner brackets | decorative, and their bottom-right corner sat in the platforms' right rail. "unbelievable" now pulses the ∞ instead — an existing glyph. |

**Drawn elements 59 → 39.** Board text is down to four blocks: TOOLBOX,
HERMES / AGENT, PROCEDURAL DISCLOSURE. One technical name, as the rule asks.

Both cards are now captioned INSIDE themselves, low. That is not a style choice:
a caption ABOVE a card puts the marker's body in the phone's top UI every time it
writes it, and a caption at the TOP of a card lands there itself on any close-up.

## (b) THE PEN SOUND — root-caused, not turned down

Morgane's two complaints have one cause and it is measurable. The shared
`_shared/sfx/pen_loop.mp3` is normalised as a FILE (its p85 body sits on the
palette's -19.0 dBFS unity) but it is not stationary INSIDE itself: on the pinned
instrument its body swings **-16.0 to -36.7 dBFS**. The builder schedules it per
stroke and truncates it at the stroke length, so a 0.16 s stroke plays whatever
five frames sit at the head of the file and a 0.7 s stroke plays twenty of them.
Two instances of "the same" sound differed by up to 20 dB. That is the
inconsistency, and the loud frames are what "too loud at the start" heard — the
opening is the densest writing in the piece.

`whiteboard_fix3_pen.py` builds a format-local `sfx3/pen_soft3.mp3`:

1. **FLATTEN** — divide by the file's own smoothed envelope, twice, so the body
   has constant RMS. A loop is heard as its body; a loop whose body moves is not
   one sound, it is a random sequence of them.
2. **TAME** — a -7 dB high shelf at 4.5 kHz. `pen_loop` was the brightest member
   of the palette; this pulls it toward the soft/tactile family Global Law 2 asks
   for without touching the scrape.
3. **RE-NORMALISE** to the palette's own -19.0 dBFS unity, iterating on the
   ENCODED mp3 (lossy encoding moves the level, and the law's claim is about the
   file the composition actually loads), so the PINNED class constant
   `V_LOOP = 0.038` still delivers exactly what SFX.md says it does.

The shared palette was **not modified** — siblings were rendering off it.

| | round 2 | round 3 |
|---|---|---|
| body spread inside the file | **25.59 dB** | **3.92 dB** |
| hf6k (harshness) | 0.203 | **0.074** |
| centroid | 2 747 Hz | **1 433 Hz** |
| unity (p85) | -19.10 | -19.00 (target -19.0) |
| delivered body at `V_LOOP` | — | **-47.40 dBFS** (loop class -47.30) |

Plus RATIONING (SFX.md rule 3): only strokes of >= 0.26 s sound, runs closer than
0.20 s merge, a new instance needs 0.30 s of silence in front of it, and every
instance gets the SAME 0.08 s in / 0.14 s out envelope so none can start on a
transient. **10 instances / 10.9 % duty -> 7 instances / 8.8 % duty.**

Measured in the real mix (`whiteboard_fix3_penproof.py`, voice + bed + layer):

| | round 2 | round 3 |
|---|---|---|
| within-instance swing, worst | **18.71 dB** | **3.92 dB** |
| within-instance swing, mean | 17.85 dB | 3.82 dB |
| per-instance body spread | 0.90 dB | **0.15 dB** |
| speech margin, whole piece | 21.09 dB | **21.09 dB** (band 15.85-23.70) |
| speech margin, first 10 s | 22.45 dB | **22.61 dB** (voice+bed alone: 22.62) |
| lift over voice+bed, first 10 s | 0.04 dB | **0.03 dB** |

The pen now costs the opening **0.01 dB** of speech margin against no pen at all.

## GLOBAL LAW 12 — measured on the pixels

`whiteboard_fix3_law12.py` decodes 452 sampled frames of each finished file.

**Caption band (the binding item).** Identical in both: pill **top 808 px
(42.08 %), bottom 917 px (47.76 %)**, centre **44.90 %**. The law's limit is a
bottom edge at or above **1382 px (72 %)** — **465 px of headroom** — and the
preferred centre band is 40-65 %, which 44.90 % sits in the middle of.

The pill is now EXACTLY stable: `translateY(-50%)` alone left it sitting on the
line-box baseline, so its centre drifted 58 px (3.0 % of frame height) with each
phrase's own font size. `line-height:0` on the row plus `vertical-align:top` on
the pill puts the pill's top on the seam before the transform, so the transform
lands its CENTRE there — measured in the DOM across all 52 phrases: centre
**862.5 px, zero variance**; measured on the plan render's pixels: **0.5 px**.

> Do NOT reach for a zero-height flex row for this. It is correct in a browser
> and wrong in a render: the producer gives clip elements a full-frame height, so
> `align-items:center` silently recentres the pill on the middle of the FRAME —
> measured at y=1810, inside the bottom 28 % the law forbids. Caught on the
> render, not on the preview.

**Top 10 % (y < 192 px).** Plan view: **0 of 452 frames carry any ink** — the
band is board background, always. That drove three layout decisions: the cards
start at y=148u, the toolbox is captioned below its own grid rather than above
it, and the marker is drawn at `PEN_SCALE = 0.70` because its body reaches 41.3u
above its own tip (topmost marker pixel: **105.2u**, the line is 102.4u).

Camera lane: the gate is per-stop and structural — **no TYPE may intersect the
top 192 px at any stop, and no container may sit entirely inside it**. All 15
stops pass, and `camera_plan.json` names every intrusion so the claim can be read
instead of trusted: what does enter the band is card top edges, the top row of
the toolbox grid, and the top of the Nous mark — chrome, never a word. Ink that
is merely CUT by the frame top is allowed on this lane by construction: a
close-up fills the frame, and a translucent "For You" tab over a line is not a
collision the way a word under it is.

**Right rail (x > 918, y 576+).** Plan view: **0 frames** of board ink in it. The
only thing that reaches into that column is the caption pill on the longest
phrases (widest right edge **967 px**, 49 px in), which is exactly what the
PUBLISHED split format does — the format the review itself cites as compliant.

## THE CAMERA, ROUND 3

15 stops (round 2 had 17), **every one solved at offset (0,0)** — the framing IS
its subject's centre, with no nudge anywhere in the piece. The three periodic
pull-backs Miguel approved are kept at the same chapter seams (24.20 / 33.54 /
40.58) and the reveal is still distinguished by duration, not framing.

```
  0.00  AGENT0      z 1.16   the agent opens, alone, on the axis
  1.50  WIDE_EARLY  z 0.60   it displaces; the toolbox draws and the dump lane is crossed
  9.56  GATE        z 1.56   the real road; the boom seats across it
 11.88  GATETERM    z 1.60   the term writes under it; the boom lifts inside this hold
 17.14  AGENT       z 1.56   the tools arrive
 20.00  CONTEXT     z 1.72   the bar draws, fills, and gets its end
 24.20  WIDE        z 0.58   ** PULL-BACK 1 **
 26.30  TOOLBOX     z 1.56   "very picky"
 30.78  AGENT       z 1.56   Nous Research
 33.54  WIDE        z 0.58   ** PULL-BACK 2 **
 35.64  TOOLBOX     z 1.56   all of the tools; the ∞ is drawn
 40.58  WIDE        z 0.58   ** PULL-BACK 3 **
 44.06  TOOLBOX     z 1.56   MCP takes a cell of its own
 47.48  CONTEXT     z 1.72   the level it never reaches
 49.40  WIDE        z 0.58   THE REVEAL (0.95 s, off the tightest stop)
```

Two stops were REMOVED rather than re-solved, both under Global Law 5: there is
no stop on the X (the wide already owns the whole crossed lane) and no second
stop on the gate at "simple" (the framing already holds the boom AND the term;
the arm lifting is a change in the drawing, not a reason to move the camera).

## Face and the zoom program

Nothing done, and nothing to do. This format has no full-face beat and no
punch-ins; its face is the unchanged 1080x1058 `face_band_25.mp4` plate, a window
far wider than the 0 % standard (see round 2's note). Miguel's ruling — no zooms,
no virtual set, no matte, no blur pad until the wider lens — costs this format
nothing.

## Laws this adds to the format

14. **A CAPTION ABOVE A CARD IS A MARKER PROBLEM, NOT A TYPOGRAPHY ONE.** The pen
    body reaches `59u * PEN_SCALE` above its own tip, so the topmost ink any
    stroke visits sets the top of the safe area — not the topmost ink itself.
    Caption cards from inside, low.
15. **A ROTATING ELEMENT'S CLEARANCE IS ITS ARM LENGTH, NOT ITS BOX.** A boom on
    a pivot sweeps a circle of radius L; the rigid registry only knows the
    rectangle it was drawn in. Compute `pivot - L*sin(open)` against whatever
    sits above it, or the open state lands on top of another object.
16. **TYPE IS FULLY IN OR FULLY OUT AT A STOP, AND ONLY AT A STOP.** The gate
    validates stops; a camera MOVE transits framings that cut a word (measured:
    "DISCLOSURE" is clipped for part of the 0.58 s move at 17.14). That is
    cinematic and accepted — but any audit that samples frames must know it, or
    it will report a caption that never moved as having drifted.
17. **A PIXEL AUDIT NEEDS A DISCRIMINATOR, NOT A THRESHOLD.** Finding the caption
    pill by "wide terracotta rows" found the key term instead, three different
    ways. What actually identifies it: it is the only terracotta that STRADDLES
    THE SEAM, and it is one rectangle, so its left and right edges hold still.

---

# FIX ROUND 4 — 2026-08-30 (task: whiteboard4) — THE CLOSING ROUND

Authority: `format_lab/REVIEW_2026-08-30.md`, **ROUND 4**. Miguel, on
`whiteboard_zoom_fix3`: *"regressed. zooms in and out too often, a bit too all
over the place, sometimes the content gets slightly hidden by the captions."*

Two fixes, both geometry and rhythm. Nothing content-level moved: the simplified
39-element board, the boom gate, the levelled pen sound, the tamed SFX at their
pinned class constants, 25 fps, and every approved beat are the round-3 objects,
untouched.

| deliverable | what it is |
|---|---|
| `whiteboard_zoom_fix4.mp4` | the CALM camera + the caption clearance band |
| `whiteboard_fix4.mp4` | the plan view, unchanged, re-verified (one bug fix, below) |

Generator `whiteboard_fix4_gen.py` over `whiteboard_fix4_core.py`; proof
`whiteboard_fix4_capproof.py` (writes `out/capband_fix4.json`). Both render
1080x1920 @ 25 fps, 1354 frames, staged to
`~/Movies/Shorts Factory/Format Lab/Fixed4/`.

## (1) THE CAMERA, CALMED

One rule produced the whole schedule, and it is the one Miguel gave:

> **A STOP LASTS UNTIL THE NARRATION MOVES TO A DIFFERENT ELEMENT.**

Not until the drawing changes, not until a sentence ends — until the *thing being
talked about* is a different object on the board. Everything round 3 spent a move
on that was really still the same subject got folded into the stop it belongs to.

```
  0.00  AGENT0      z 1.16  hold 1.50s   the agent opens, alone, on the axis
  1.50  WIDE_EARLY  z 0.60  hold 7.46s   it displaces; toolbox draws, cells load,
                                         the dump lane is crossed — one hold
  9.56  GATETERM    z 1.52  hold 6.86s   the road, the boom, the term, the lift
 17.14  AGENT       z 1.52  hold 6.34s   the tools arrive; the bar fills inside it
 24.20  WIDE        z 0.58  hold 8.49s   ** SEAM 1 — the wide rest **
 33.54  TOOLBOX     z 1.52  hold 6.32s   ** SEAM 2 — all the tools **
 40.58  WIDE        z 0.58  hold 7.97s   ** SEAM 3 — the closing chapter **
 49.40  WIDE        z 0.50  hold 3.81s   THE REVEAL — settle wider
```

| | round 3 | round 4 |
|---|---|---|
| camera stops | 15 | **8** |
| camera MOVES | 14 | **7** (exactly half) |
| median hold | 2.84 s | **6.60 s** |
| shortest hold | 1.37 s | **1.50 s** |
| tightest z | 1.72 | **1.52** |
| stops centred on their subject | 15/15 | **8/8** |

**What was merged, and why each was not a camera move in the first place**

| round-3 stops | round-4 | reason |
|---|---|---|
| `GATE` @9.56 + `GATETERM` @11.88 | one stop @9.56 | "crack the code / procedural disclosure / it's very simple" is one thought about one object, and the 11.88 framing already contained the boom. The move changed nothing but the scale. |
| `AGENT` @17.14 + `CONTEXT` @20.00 | one stop @17.14 | the context bar is drawn INSIDE the agent card. The close-up already holds it. |
| `WIDE` @24.20 + `TOOLBOX` @26.30 + `AGENT` @30.78 + `WIDE` @33.54 | one wide rest @24.20 | "handle your context / be picky / Nous Research, the lab behind Hermes" is chapter talk about the whole picture. Two 2-3 s excursions inside a 9 s chapter is precisely the "all over the place". |
| `TOOLBOX` @44.06 + `CONTEXT` @47.48 | folded into seam 3 | the closing sentence names BOTH cards ("give up all of the MCP servers and all of the tools ... without bloating your context"). No single card is its subject, so the camera does not pick one. |

**The seams.** The camera pulls wide only at the three chapter seams round 2
approved (24.20 / 33.54 / 40.58) and at the reveal (49.40). At 33.54 it is
*already* wide — it has been resting there since 24.20 — so that seam is honoured
by STAYING, not by moving: a wide-to-wide move is a move with no reason, which
Global Law 5 forbids. The seam instead ends the wide rest at the moment the
narration finally names an object again.

**A rejected option, with the arithmetic rather than a taste call.** The seam-2
chapter's payoff is the ∞ under the toolbox, and a card+∞ subject was tried so it
would be on camera. Holding both needs `sc*z <= 3.60` (206u of subject plus two
60 px subject margins inside an 862.5 px zone); keeping PROCEDURAL DISCLOSURE off
screen from the toolbox's own centre needs `sc*z >= 3.93`. The two ranges are
disjoint, so every solution is off-centre — the solver returns `dx = -35` — and
gate 2, *every stop's centre IS its subject's centre*, is not something this round
gets to spend. The ∞ draws inside that hold and is revealed by the seam-3
pull-back, which is a reveal, not a peek-ahead.

Move durations also grew (0.52-0.60 s -> 0.72 / 0.85 / 0.95 s). Fewer moves AND
slower ones is what "gently" means.

## (2) THE CAPTION CLEARANCE BAND

The pill's CENTRE is pinned to the seam at y = 862.5 px, so its **upper half
hangs into the board zone**. Its height is not a constant — `cap_font()` sizes it
from the phrase — so the band is DERIVED from the worst case the typographic rule
can produce, never chosen:

```
font   max(cap_font)      = 30.0 u  -> px(30)  = 56.25 px
body   font * 1.32 line-height               =  74.25 px
pad    px(10) top + bottom                   =  37.50 px
pill height                                  = 111.75 px
half                                         =  55.88 px
CAP_CLEAR_PX = half + 6 px hairline          =  61.88 px
```

so the reserved band is **rows 800.6 -> 862.5 px, full width**. It is a clearance
for the CAPTION only — Law 12's round-4 amendment is respected in full: the
composition stays centred and symmetric, every stop still lands on its subject's
centre, and nothing was shoved sideways for the right rail.

The band is now a hard gate in the solver, stricter than gate 1: it exempts
nothing (a connector or a 12 u mark under a caption is exactly as hidden as a card
is), and `camera_plan.json` reports the lowest ink on camera at every stop.

### PER-STOP CLEARANCE — measured on decoded frames, captions switched OFF

A pill is opaque, so the shipped mp4 can never show what is under it. The proof
re-snapshots the SAME composition with `.scap {display:none}` and reads the band
on real pixels.

| stop | subject | z | sampled | lowest ink | clearance | pixels in band | verdict |
|---|---|---|---|---|---|---|---|
| 0.00 | AGENT0 | 1.16 | 1.20 s | 699.2 px | +101.4 px | **0** | PASS |
| 1.50 | WIDE_EARLY | 0.60 | 5.98 s | 569.9 px | +230.8 px | **0** | PASS |
| 9.56 | GATETERM | 1.52 | 13.80 s | 729.9 px | +70.7 px | **0** | PASS |
| 17.14 | AGENT | 1.52 | 21.12 s | 782.4 px | +18.3 px | **0** | PASS |
| 24.20 | WIDE | 0.58 | 29.32 s | 613.9 px | +186.7 px | **0** | PASS |
| 33.54 | TOOLBOX | 1.52 | 37.51 s | 782.4 px | +18.3 px | **0** | PASS |
| 40.58 | WIDE | 0.58 | 45.44 s | 613.9 px | +186.7 px | **0** | PASS |
| 49.40 | WIDE | 0.50 | 50.44 s | 588.8 px | +211.9 px | **0** | PASS |

The pill's own top edge, located on the SHIPPED mp4 by the round-3 discriminator
(the only terracotta that STRADDLES THE SEAM), measures **808-816 px** across the
video — 7.4 px *inside* the 800.6 px band top, which is the 6 px hairline plus
rounding. The derived band bounds the real pill, as claimed.

**Whole-video sweep, both lanes, captions off, every 0.32 s (158 frames each):**

* plan view: **0 frames** with ink in the band.
* camera lane: 3 frames, at 17.58 / 24.62 / 40.94 s — **all three inside a camera
  MOVE**, none inside a hold. That is this format's law 16 (type is fully in or
  fully out at a STOP, and only at a stop); a 0.32 s sample inside a 0.72-0.85 s
  transit is the key term or the ∞ sweeping past, not content parked under a pill.

## (3) A BUG THE SWEEP CAUGHT — the ∞ was not pulsing, it was jumping

The first fix-4 sweep failed at **37.11 s, inside a HOLD**: 6 337 band pixels, and
the crop showed the ∞ cut in half by the seam. Root cause, and it is a general
one:

> **`transformOrigin` in px on an SVG element resolves against that element's own
> BOUNDING BOX, not against SVG user space.**

`#inf` was pulsed with `transformOrigin:"261px 956px"` — user-space coordinates —
which put the pivot roughly a frame and a half away, so the 8 % scale *translated*
the glyph instead of growing it in place. Measured on the shipped
`whiteboard_fix3.mp4` plan view, the ∞ bbox jumps **y 614-659 -> 564-612**: a
**50 px lurch up and 14 px left**, twice (36.98 s and 49.50 s). On the camera lane
the ∞ sits just below the visible board at the toolbox stop, so the lurch lifted
it up into the caption band for the 0.52 s of the pulse.

Fix: `svgOrigin`, which takes user-space coordinates — which is what those numbers
always were. After it, the same measurement reads **614-659 -> 613-661**: a
symmetric 8 % grow about its own centre, in place.

This is the ONE change to the plan view, and it is deliberate: the plan view had
no caption-band violation (0/158 frames, before and after), but the same
unmotivated 50 px jump was in it, and an element that moves for no reason is a
Global Law 5 defect wherever it appears. Everything else in `whiteboard_fix4.mp4`
is byte-for-byte the round-3 composition.

## Laws this adds to the format

18. **THE CAPTION BAND IS DERIVED FROM THE TYPE RULE, NOT PICKED.** A pill whose
    font size is computed per phrase has no fixed height; the reserved band is the
    worst case that rule can produce, plus a hairline. Pin the pill's CENTRE and
    reserve `max_font * line-height / 2 + padding` above it.
19. **A CLEARANCE FOR THE CAPTION IS NOT A CLEARANCE FOR THE COMPOSITION.** Reserve
    rows, never columns, and never move the artwork off the axis to buy them. Law
    12's right-rail rule is about captions and readable annotations; the drawing
    stays centred and symmetric (round-4 amendment).
20. **AN OPAQUE ELEMENT CANNOT BE AUDITED THROUGH.** To prove nothing hides under
    a caption you must re-render the composition with the caption layer OFF. A
    sweep of the shipped file measures the pill, not the board.
21. **`transformOrigin` IN PX IS BBOX-RELATIVE ON SVG; `svgOrigin` IS USER SPACE.**
    A pulse authored with the wrong one does not fail loudly — it silently becomes
    a translation, and the size of the translation scales with how far the intended
    pivot is from the element. Audit any `scale` tween on an SVG group whose origin
    was written in the drawing's own coordinates.
22. **HOLD UNTIL THE SUBJECT CHANGES, NOT UNTIL THE DRAWING DOES.** A new stroke,
    a filling bar, or a lifting arm inside the current framing is a reason to keep
    watching, not a reason to move. Half of round 3's moves were the drawing
    changing, not the subject.

---

# CLOSING CAPTIONS ROUND — 2026-08-31 (task: whiteboard captions, fix6)

One goal, lab-wide: **every definitive format video carries the IDENTICAL caption
specification.** For this format that is a minimum-touch round. The board, the
marker, the camera schedule, the pull-backs, the SFX, the outro — frozen, and
proved frozen on decoded pixels (pass D below). The only authored change is the
caption itself, at the seat it already had.

Files: `whiteboard_fix6_core.py`, `whiteboard_fix6_gen.py`,
`whiteboard_fix6_capproof.py`. Deliverables `out/whiteboard_fix6.mp4` and
`out/whiteboard_zoom_fix6.mp4`, staged to
`~/Movies/Shorts Factory/Format Lab/Fixed6/`.

## THE CANONICAL PILL — read off the published factory, not invented

The de facto brand standard is what actually shipped:
`shorts_run8/projects/mcpupgrade_icon/index.html`.

```
.scappill { display:inline-block; transform:translateY(-50%);
            background:#C4573A; color:#fff;
            font-family:Nunito,sans-serif; font-weight:800;
            padding:18.8px 33.8px; border-radius:22.5px; white-space:nowrap; }
<span class="scappill" style="font-size:56.2px">
```

Measured across all 13 published projects: **507 pills, 486 of them (95.9 %) at
font-size 56.2px** — the other 21 are the shrink formula's residue. Decoded out
of the published 4K masters (`mcpupgrade_icon`, `skillssh_counter`) the pill body
is **228 px at 2x = 114 px in the 1080-wide design space, centred at y = 862.4 px
(44.91 % of frame height)**. In a browser at the canon spec the CSS box measures
**114.59 px**. That is the number every format must now report.

Round 4 shipped 110 px (`CAP_FS_MAX_U * S * 1.32 + 2 * px(10)` = 111.75 CSS).
Two deltas closed it: the font is 56.2px flat, not `px(30)` = 56.25, and the
line-height is Nunito's own `normal` (1.37), not the invented 1.32. Padding and
radius were already canon in disguise — `px(10)`/`px(18)`/`px(12)` = 18.75 /
33.75 / 22.5 — and are now written as the published literals.

The seat did not move: **862.5 px, 44.92 %**, exactly where round 4 put it.

## ONE FONT SIZE — the shrink formula is dead, phrases SPLIT instead

`cap_font()` is gone. Round 4 emitted **five** distinct font sizes (43.88, 49.31,
52.69, 54.38, 56.25). fix6 emits **one**: 56.2px.

A phrase that does not fit is cut at a word boundary, never shrunk and never
squeezed. Every word in `transcript_words.json` carries its own start/end, so
each beat gets real in/out times off the transcript rather than a proportional
guess. The splitter takes the FEWEST beats that all fit and, among those, the
partition whose widest beat is narrowest — so a split never strands an orphan
word alone on the seam.

Result: **52 captions -> 58**, 6 phrases split into 12 beats, text unchanged.
The two that split at the earlier 864 px budget were "They introduced something
that's" and "context, which is just unbelievable."

**The width budget is Law 12's, not the corpus's.** The rail owns x > 918 and the
pill is symmetric about x = 540, so the pill cannot exceed `2 * (918 - 540)` =
**756 px**. The published corpus does not honour this (its widest pill is 861.9
px, `hermesbuzz_kinetic`, overhanging by 47 px) but Law 12 postdates the publish,
and the cutout format — round 4's APPROVED STANDARD — already ships 756. The
lab's definitive formats agree. Widest whiteboard pill after splitting: **692 px
decoded / 725.2 px measured pre-render**.

**Widths are MEASURED, never estimated.** `pill_widths()` lays the real
`.scappill` box out in Chromium with the Nunito 800 webfont and caches the answer
in `.capwidths6.json`. The `0.575 * len` advance estimate rounds 2-5 used is
wrong by double digits of pixels on the same string; the cutout sibling
independently hit the same wall this round. An empty pill never triggers the
webfont download, so the measurement page calls `document.fonts.load()` by name
and refuses to measure if `document.fonts.check()` still says no — otherwise the
whole corpus is measured on Helvetica and every number is a lie.

## THE CLEARANCE BAND, RE-DERIVED

The canon pill is 2.84 px taller, so the reserved band grows by 1.42 px:
`CAP_CLEAR_PX` 61.88 -> **63.30**, band top 800.62 -> **799.20 px**. The board did
not move to pay for it. Tightest camera stop clearance falls 18.3 -> **16.8 px**,
still positive at every stop; `cap_intruders` is NONE at all eight.

## THE PROOFS (`whiteboard_fix6_capproof.py`, `out/capband_fix6.json`)

**A/B — the pill and its glyphs, every 0.40 s of both videos, decoded.**
126 caption frames each: pill height `[114]` px, one value, zero variance; centre
`[862.5]` px, one value; widest 692 px. Glyph x-height (white-ink row profile,
half-max crossings interpolated to sub-pixel) **27.46 +- 0.88 px, min 26.56**.
NEGATIVE CONTROL, the same instrument on round 4's `whiteboard_fix4.mp4`: **five
pill heights (94, 102, 106, 108, 110) and x-height down to 22.44 px**. The
instrument can see the defect, so its silence on fix6 means something.

**C — the board with the captions switched OFF.** All eight camera stops: pill
top 806.0 px vs band top 799.21 px (margin +6.79), and **zero** non-background
pixels in the reserved band. Full 0.32 s sweep, 158 frames: 3 frames carry ink
through the band (17.58, 24.62, 40.94 s) and **all three are inside a camera
transit, none inside a hold** — the format's law 16 (stops are the law, moves are
transits) is intact.

**D — containment against the round-4 definitive files.** 49 frames per video.
Material difference (per-pixel channel-sum > 60): **647 836 px inside the pill
band (rows 803-921), 104 px outside (0.016 %)** for the plan view;
**647 727 in / 819 out (0.126 %)** for the camera lane. The out-of-band pixels
are not an element that moved — the densest 20x20 tile anywhere outside the band
holds **12/400** (plan) and **20/400** (camera) pixels, i.e. speckle on the
highest-contrast ink edges of two independent H.264 encodes, concentrated on the
two camera-move frames. Below a threshold of 10 the diff covers the whole frame
at a mean of 1.5-1.9 out of 765: that is the encoder, not the composition.

## Laws this adds to the format

23. **THE PILL IS COPIED, NOT DESIGNED.** The caption specification comes off the
    published factory verbatim — font size, padding, radius, colour, family,
    weight, nowrap — and every format reports its rendered pill HEIGHT (114 px)
    so cross-format uniformity can be audited by one number instead of by eye.
24. **ONE FONT SIZE. LONG PHRASES SPLIT, NEVER SHRINK.** Word timestamps make any
    word-boundary split exactly timeable, so there is never a reason to resize
    type. Fewest beats first, then the narrowest widest beat, so no orphans.
25. **A WIDTH IS MEASURED IN THE ENGINE THAT WILL RENDER IT.** Average-advance
    estimates are wrong by tens of pixels and fail in the direction that forces
    bad splits. Lay the real box out in Chromium, prove the webfont loaded
    first, and cache the answer.
26. **A CAPTION INSTRUMENT NEEDS A NEGATIVE CONTROL.** Run the same measurement
    on the previous round's file. If it cannot show the defect that round had,
    it is not evidence that this round fixed it.
27. **TWO INDEPENDENT ENCODES ALWAYS DIFFER.** Containment is not "no pixel
    changed outside the region" — it is "nothing outside the region is
    CLUSTERED". Report the densest tile, not the bounding box.
