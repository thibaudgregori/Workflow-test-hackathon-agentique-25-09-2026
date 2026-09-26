# claudesessions — WHITEBOARD author notes

The plan was built as written. These are the places this board differs from the
plan's LETTER, each with the law or the measurement that forced it. Nothing here
changes what the argument says; the objects, the keys, the sides, the chapters,
the erase, the connectors and the two emphases are the plan's own.

## 1. The outro objects cannot be authored on the board (LAW — assert_outro_clear)

The plan's `lifetimes` declare three outro marks — `outro walkie talkie`
(anchor `o-glyph`), `outro rule` (`o-rule`) and `outro handle lockup` (`o-slot`)
— with `t_to: null`, and beat 4's `whiteboard_version` asks for "the same
centred lockup on the same small radio".

`formats/whiteboard/lib/whiteboard_build.py::assert_outro_clear` refuses any ink
authored AT OR AFTER the outro anchor, and the whiteboard chassis' own
`outro_block()` owns the sign-off: an opaque cream sheet rises over the board
carrying the terracotta rule, the handle and the `daily AI` micro-line already
printed on it. There is no glyph slot in that lockup and no legal instant at
which the board could draw one.

So this board draws no outro object, `board_anchors=()` and the last ink is
TEAMMATES at 16.26 (complete 16.56), 0.44 s before the wipe starts at 17.00.
What I would have done instead: nothing different — the chassis outro is the
approved one and the split/cutout lane carries the small radio in its own
`#o-slot`, which is where the plan's `o-glyph` anchor actually lives.

## 2. Chapter 1's first radio starts 0.26 s earlier than the plan's lifetime
(LAW 45 — the erase hands over to an IDEA)

The plan's lifetime for `team radio left` is `t_from: 10.04`. The erase at 9.72
completes at 10.02, and LAW 45 requires a complete, nameable object within
0.30 s of that, i.e. by 10.32. A whole walkie-talkie — body, antenna, collar,
grille, display and four buttons — takes 0.44 s of marker, so a 10.04 start
finishes at 10.48 and the seam holds nothing but strokes for 0.46 s.

This board therefore starts `team-a` at 9.78, INSIDE the erase, complete at
10.22 — the law's first sanctioned method, and the same move the plan's own
`why_together` describes ("the first team radio is already arriving while the
pair fades"). Every other instant in chapter 1 is the plan's, to the frame.

## 3. The pulse is a struck dash, not a travelling one (LAW 1)

The plan's beat 0/1 pictures have the pulse "run the arc left-to-right and then
right-to-left". The plan's own `bespoke_objects[0].how_drawn` describes it as
"a small terracotta pulse marker riding it", and the whiteboard's ink is
`stroke-dashoffset` reveal — the dash channel is already spoken for by the
draw-on, so a second dash driven along the same path is not available without
forking the harness. The board strikes ONE short terracotta dash on the arc at
1.32 ("itself") and two on the team arcs at 15.24 ("work"), each a word-synced
event that ends. The split and the cutout keep the travelling pulse; the
whiteboard's version of "a message crossed the line" is the mark it left.

## 4. The plan's bboxes are canvas-space and cannot be copied here

`bespoke_objects[*].bbox` is the shared core's geometry (1080-wide canvas). This
board is 576 x 460 design units at 1.875 frame px per unit, so every seat was
re-laid out on the board's own legal surface (x 40..536, y 150..425) while
keeping the plan's ORDER, SIDES, SYMMETRY and INSTANTS. The phone-test TIMES are
this lane's own as well (2026-09-15 whiteboard rule): the plan's `t` is the
instant the object ARRIVES and the marker tip is still inside the box then.

## 5. No comparison is declared

The plan declares none and the script speaks none: this take makes one claim
that gains a third node, not an "X versus Y". `comparisons=()`. Drawing a
comparison here would be drawing an argument the recording never made.

## open_doubts

The plan's `open_doubts` is empty, as expected, and I found none. The plan's two
`open_questions` are both answered by this board without a decision reaching the
viewer: (a) the two sibling keys are authored at 14.93 board units = 28 frame px,
well over the 23 px floor, because this lane has no `k`; (b) the middle slot is
used twice and the TILE is the one that leaves (2.94–6.38), exactly as the plan
resolves it, so the figure never has to move.
