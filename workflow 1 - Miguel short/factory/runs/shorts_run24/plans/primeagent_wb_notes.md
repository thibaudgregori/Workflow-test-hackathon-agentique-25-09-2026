# primeagent — WHITEBOARD author notes

The plan was built as written. These are the places this board differs from the
plan's LETTER, each with the law or the measurement that forced it. Nothing here
changes what the argument says: the three bespoke objects, the four written
keys, the sides, the five chapters, the four erases, the absence of connectors
and the two emphases are the plan's own.

## 1. `ONE SINGLE TOOL` is written at 12.78, not at 11.62 (LAW 4, the caption identity guard)

The plan puts the third key on the word "one" (11.62). The caption canon chunks
that sentence into a pill whose whole text is **"one single tool."**, alive
11.62-12.74. `whiteboard_build.caption_identity_guard` refuses a board word that
is on screen while an identical pill is on screen, and it refused this build:

    LAW 4 — double caption:
      board text 'one single tool.' is on the board 11.62-21.50s while the
      identical pill is on screen (11.62-12.74s)

So the key is anchored to the word **"tool."** (w48, 12.32) instead and written
at 12.78, 0.46 s after that word starts — inside `LABEL_WINDOW` (1.0 s), 0.04 s
after the pill leaves, and still the same beat and the same sentence. The plan's
own reason for the key ("it is alone on the board in its chapter") is untouched;
only the instant moved, and it moved because two surfaces would otherwise have
carried the identical words at the identical moment.

What I would have done instead: nothing. The board word is the plan's, the side
is the plan's, and the law's remedy is exactly this shift.

## 2. The plan's beat-4 whiteboard line asks for a terracotta OUTLINE REDRAW; this board uses the marker BOX (LAW 38)

`plan.beats[4].whiteboard` reads "the emphasis is the machine's outline redrawn
in terracotta rather than a border flip". `plan.emphasis[0]` for the same beat
declares `"kind": "box"` with the reason "LAW 38 rule 2: the machine is a DRAWN
object, so it takes boxing".

LAW 38's board lane names exactly one primitive for a drawn object —
`whiteboard_build.box_emphasis()`, the terracotta marker box — and the chassis'
own LAW 38 table lists no third option. A terracotta redraw of the gantry is
neither of the law's two tools, and it would also put a second set of strokes on
top of an object that is already drawn. The board therefore boxes the gantry, as
the plan's own JSON `emphasis` entry says. The prose line and the JSON disagreed;
the JSON is the plan's declaration and the law agrees with it.

## 3. The machine's emphasis box is popped with `pen=False` (RUN-13 CLERK FINDING, applied to its own cause)

`box_emphasis` taps the marker on the box's TOP-LEFT CORNER, which is the run-13
fix. On this board that corner is (226.0, 207.0) u, and the marker sprite reaches
41.3 u up and left of its tip, so it covers x 184.7-226.0, y 165.7-207.0 —
straight across `ONE SINGLE TOOL` (205.5-370.5, 172.0-195.1) for the 0.34 s pop.
That is the run-13 defect itself ("the pencil lay across the VISUALS row for
0.58 s"), reproduced by the fix for it. The key cannot move (it is welded above
its machine) and the box cannot move (it hugs the gantry), so the pen is left out
of this one pop. Every other pop and every stroke on the board keeps its marker.
The three tile emphases keep theirs: their sprites land on blank board and on the
terracotta rule, never on type.

## 4. The tool shafts run on INTO the box, 28 authoring units past the rim

The sealed DOM lane fills the toolbox body (`fill=CARD`), which hides the wrench
shaft and the saw blade below the rim. The GRAPHIC CHART forbids a filled
silhouette on this lane, so the whiteboard body is `fill:none` — and with the
shafts stopped at the rim (the sealed geometry, y 96) the wrench read as a flag
on a pole balanced on the box's edge, not as a tool standing in it. The shafts now
run to y 124, so the tools are visibly inside the box and still cross the rim
while they are lifted. Same objects, same outer silhouette, same bboxes bar the
two tool sub-marks; only the hidden part of each shaft is now drawn, which is
what an unfilled box shows.

## 5. The three tool lifts are 14 board units, not the plan's 26

`plan.beats[1].whiteboard` asks for "the tool redrawn 26 board-units higher and
back". Two things forced a smaller number. A REDRAW would author a second copy of
the tool's ink (more strokes, a placement twin, and a second marker gesture on a
beat that has three of them); a translate of the tool's own group is the same
event with no new ink and is what `LAW 28` describes ("a tool that lifts is a
child of the box it lifts out of"). And at 26 u the wrench head reaches y 188.6 u,
1.4 u under `REGULAR AGENTS`'s line box — it would have touched the key. At 14 u
(26 frame px, a plainly visible lift) the head stops at 199.5 u, 10.3 u clear of
the key, and the shaft still crosses the rim so the tool never looks detached.

## 6. Chapter 0's machine starts at 0.30, where the sealed scene starts it

Not a deviation — recorded because it is the earliest ink on the board and the
zero-ink law reads it. First stroke 0.30, machine complete 0.96, key term written
1.10-1.52. The first spoken word is at 0.10, so frames 0-7 are the composition's
LEADING empty run, which `assert_zone_never_blank` excludes by name; from frame 8
on the zone always holds ink.

## 7. The pair's two tool boxes are seated 13.65 u right of the axis so the pair's INK is centred

The sealed pair mirrors two 160-wide TOOL BOXES about the pair centre. The hammer's
claw sticks 26 authoring units out to the left of its box and the screwdriver is
only 56 wide inside its own, so mirroring the BOXES puts the finished INK 13.65 u
left of the composition axis. The two boxes are therefore both shifted right by
that amount: the drawn pair is symmetric about x = 288 (179.6 + 398.2 = 577.8),
which is what a viewer sees, and the two tools keep the sealed 52 u splay and the
sealed +/-34 degrees.

## 8. No outro object is authored on the board (LAW — `assert_outro_clear`)

`plan.lifetimes` gives the outro lockup `t_to: null` and beat 7's whiteboard line
asks for "the same lockup on the same small machine glyph, drawn in marker".
`whiteboard_build.assert_outro_clear` refuses any ink authored at or after the
outro anchor, and the chassis' own `outro_block()` owns the sign-off: an opaque
cream sheet rises over the board already carrying the terracotta rule, the handle
and the `daily AI` micro-line. There is no glyph slot in that lockup and no legal
instant at which the board could draw one. `board_anchors=()`, and the last ink is
the terracotta rule, complete at 33.58 — 5.20 s before the wipe starts at 38.78.
The split and cutout lanes carry the small machine in their own `#o-slot`, which
is where the plan's `o-glyph` anchor actually lives.

## 9. The phone boxes are this board's, not the plan's

The plan's `bespoke_objects[i].bbox` values are normalised against the SHARED
core's 1080 x 600 canvas placement and cannot be copied onto a 576 x 460 board.
The names and the INSTANTS are the plan's (8.20 / 1.80 / 24.40); the boxes are
this board's own seats, measured off the authored geometry and normalised to the
1080 x 1920 frame in `gen/_wb_primeagent.json -> phone_test_objects`.

## 10. Word sync

This take contains no number, no count and no metric anywhere, so the run-20
class (a typed count disagreeing with the spoken one) cannot occur here. The four
typed strings were each screenshotted at the instant they finish and read against
the pill under them: `PRIME AGENT` complete 1.52 over "new type of AI agent.";
`REGULAR AGENTS` complete 3.36 over "Regular AI agents have"; `ONE SINGLE TOOL`
complete 13.08 over "This tool allows it", one beat after he says "one single
tool"; `RLM` complete 29.68 over "which is called RLM,". All four agree with the
word they land on.
