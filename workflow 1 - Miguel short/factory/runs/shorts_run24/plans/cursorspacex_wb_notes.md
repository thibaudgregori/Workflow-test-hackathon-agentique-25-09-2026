# cursorspacex — WHITEBOARD author's notes

The plan was built as written. No open doubt was found. Three departures from
the plan's LETTER are recorded here, all of them coordinate/grade choices the
board lane owns; the ORDER, the SIDES, the BOARD MODE, the INSTANTS, the one
bespoke object, the one written key and the three marks are the plan's.

## 1. The retired flag bottoms out at 0.62 ink, not 0.40

The plan (and the sealed DOM scene) steps the flag's ink 1.00 -> 0.74 -> 0.55
-> 0.40. That is right where there is exactly ONE flag on screen. This board
follows the plan's own whiteboard version and leaves a BROKEN GHOST at every
height the flag left, so at 0.40 the live flag was no darker than its own three
traces: the first check frames showed the descent reading as a lined box rather
than as a flag coming down. The grade still falls one step per spoken word
(1.00 -> 0.82 -> 0.72 -> 0.62); it simply bottoms out high enough that the
retired flag stays the solid object among faint ones. Nothing about the claim
changes: the brand dims once per step and ends muted at the foot of its mast.

What I would have done otherwise: nothing — the ghosts are the plan's, and the
ghosts are what make the descent read as time passing on this lane.

## 2. The emphasis boxes are drawn at pad 0

LAW 38 rule 2 gives the board lane the terracotta MARKER BOX and the DOM lane
the PANEL BORDER FLIP. The plan declares both emphases as border flips because
it was written for the DOM lane. `box_emphasis(..., pad=0.0)` lands the marker
box ON the card's own outline, which is the board's own reading of a border
flip, and it keeps the box off the connector that terminates at the card's top
edge. A padded box would have been crossed by that connector, which is the
exact defect LAW 38 records against rings.

## 3. Geometry is the board's, not the plan's coordinates

The plan's bbox for the one bespoke object is the shared core's canvas space
and cannot be copied onto a 576 x 460 board. Per DRAWN GEOMETRY IS ASSERTED
AGAINST THE PLAN (2026-09-05), this board's flag-on-pole is asserted against the
plan's order, side and instant, and its own box is recorded in
`gen/_wb_cursorspacex.json -> plan_geometry`. The Phone Test time is this lane's
own (2.60 s), per the 2026-09-15 whiteboard rule.

## Not a departure, recorded because a check names it

* `boards.mode == "single"` (LAW 43's exception, the plan's own choice with its
  own reason), so there is NO chapter seam, nothing is erased, `seam_check.py`
  is not run and `qc_pass` is given no `--seams`. A skip is not a pass — there
  is simply no seam on this board to measure.
* Zero pointing cues on this take, so nothing is answered and nothing is waived.
