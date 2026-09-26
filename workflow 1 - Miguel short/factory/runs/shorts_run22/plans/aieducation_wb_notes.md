# aieducation — WHITEBOARD author notes

The plan (`plans/aieducation_plan.json`) was built as written. Everything below
is either a place where a LAW overrode a line of the plan, or a place where the
plan's coordinates could not survive the change of surface. Nothing here changes
what the video argues.

## 1. The plan's bboxes are the shared core's, not this board's

`bespoke_objects[*].bbox` / `core_box` are in the 1080-wide core the SPLIT and
CUTOUT share. The whiteboard's surface is the chassis' own 576 x 460 board
(1 u = 1.875 frame px), so those numbers cannot be copied onto it. Every object,
key and connector is re-seated here and asserted against the plan's ORDER,
SIDES, CHAPTERS and INSTANTS instead — same four bespoke objects, same five
written keys, same above/below placement, same five chapters with the same four
erases, same three connectors into one target, same one pointing-cue card.
`gen/_wb_aieducation.json -> plan_geometry` carries this board's numbers.

## 2. The phone-test TIMES are this lane's, not the plan's

2026-09-15 whiteboard rule: the plan's `t` is the instant an object ARRIVES, and
on a marker board the pen tip is still inside the box then. Each object is cut at
the first instant at which its drawing is COMPLETE and the marker has been hard-
killed: 2.55 / 12.80 / 17.72 / 25.30.

## 3. The easel's BOARD is inked before its legs (LAW 45 over the plan's letter)

The plan's beat-4 `whiteboard_version` asks for "the easel drawn legs first with
its board propped on the ledge". LAW 45 requires a complete, nameable object
within 0.30 s of the chapter erase completing (22.04), and the legs alone are not
one — `seam_check`'s OBJECT test wants a blob of major axis >= 118 px and
sigma_minor >= 18 px, which three thin diagonals do not make. So the board face
is inked 21.78-22.10 (a 300 x 187 px rectangle, 0.06 s after the erase finishes)
and the ledge, legs and brace follow. The law wins; the picture is identical
0.8 s later.

## 4. The three tool tiles arrive after the easel, not before it

Same cause. The plan's picture reads "three tool tiles sit in a row and send
connectors down into a classroom easel", which is the FINISHED frame and is
exactly what the board holds from 23.98 onward; only the drawing ORDER is
reversed, because the seam has to land on the easel.

## 5. The board has no screenshot inside the source card

The plan's beat 1 moves the camera closer into the screenshot the post carried
(Anatomy Atelier). A marker board cannot paste a raster, and the plan's own
`whiteboard_version` for that beat says so: the post is inked as a bordered card
with X's mark, the handle written, the claim line written inside it and the
marker run under that line. The card carries the post's own words and NO metrics
chrome; the zoom belongs to the split and the cutout.

## 6. Chapter 3 draws no app frame, chapter 4 has no desks, the hook leaves a ghost

Inherited from the shared module's three declared departures (`plan.
departures_from_this_plan`, handoff §9) so the three lanes argue the same thing:
the opened heart has a cursor instead of a screen; the three copies land on the
easel's own cross-brace instead of on three desks; the lifted heart leaves a
dashed ghost on the page it came off.

## 7. The card's departure is registered as a seam

Three rigids leave at 6.46 — the card, X's mark and the card's hairline — so
`chapter_seams()` can see it. Without the third rigid the seam is invisible to
the registry, the card's own border stroke is then judged against `3D ANATOMY`
(written 2.8 s after the card has gone), and LAW 41's crossing check invents a
violation no viewer can see.

## 8. The open book was redesigned once, after a cold-read failure

Round 1 of the cold read returned **"greeting card", sure/unsure x3** on object 0
— and that is the drawing, not the instrument: a single folded sheet with a heart
on it IS a greeting card. It was redrawn with a PAGE BLOCK (two repeated contours
under each bottom edge) and ruled lines that tilt with the leaf, which is what
separates a book from a card in line art. Three fresh independent rounds then
returned **"open book", sure x3**. Only that crop was re-dispatched; objects 1, 2
and 3 were never re-read, because an unchanged crop read again is a copy, not a
measurement.

## 9. Hedged flags on objects 1 and 2, recorded and routed

Object 1 read `heart` x3 (`unsure`), object 2 read `head with heart thought
bubble` x3 (`cannot tell`). Zero readers named a different thing on either, and
`production.py::consensus` no longer lets the confidence flag veto a noun that
reached the object. The hedge is the reader questioning whether an anatomical
heart is an "everyday object", not whether it can see one. Both are recorded as
hedged passes for the clerk to adjudicate on the delivered render, where they
move, carry their keys (`3D ANATOMY` / `GUESSWORK`) and land on the words Miguel
is saying — the same routing the artwork seat gave object 2.
