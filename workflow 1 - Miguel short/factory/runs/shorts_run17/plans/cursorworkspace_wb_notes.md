# cursorworkspace — WHITEBOARD (Reels) author notes

Every item below is a DEPARTURE from `plans/cursorworkspace_plan.json` or a
statement of a law that forced one. The plan was built anyway in all cases.

## 1 — The chapter-1 erase is at 11.46, which is the plan's own number

Not a departure. Recorded because the plan's prose reasons about 11.279 and then
sets 11.46: SHEETS is written at 11.04 and its 0.24 s entrance finishes at 11.28,
so an 11.30 erase would wipe the chapter's last name mid-stroke. 11.46 sits in
the gap between `Now,` (ends 11.439) and `you` (11.639). The board matches.

## 2 — DEPARTURE: the bridge's internal anatomy, and its stroke mass

The plan describes "a thick horizontal deck, four piers dropping to the water,
three equal near-semicircular arches between the pier feet, a waterline running a
little past the structure on both sides and three wavy strokes under the arches".
This board draws exactly that. What departed, and then came back, is the WEIGHT.

Four cold rounds failed on this one drawing, each on the same axis:

| round | read | cause |
|---|---|---|
| 1 | "scallop shells", sure | a 38 u arch rise is a scalloped edge, not a structure |
| 2 | "egg carton", sure | deck and piers drawn as OUTLINED bars — a black lattice of cream cells |
| 3 | "clothes drying rack" / "shower head" | the deck stopped dead on its outermost leg |
| 4 | "donuts", sure | an 11 u deck, 9 u piers and a 7.4 u arch close each span into a thick black RING around a cream hole |

The metaphor was never the problem, and changing it was not an option worth
taking: `gen/cursorworkspace_scene.py::bridge_svg` draws the same four members
and is SEALED 6/6 `sure` across six independent rounds and two reader models
(`review/artwork_pass_cursorworkspace.json`), and swapping the Reels object would
put a different picture on Instagram than the one YouTube and TikTok ship.

**The fix, round 5: every bridge constant on this board is now the sealed scene
module's own canvas number divided by S = 1.875.** Deck 13 -> 6.933 u (was 11),
piers 11 -> 5.867 u (was 9), arches 10 -> 5.333 u (was 7.4), pier pitch and arch
rx/ry taken from `PIER_XS` / `ARCH_RX` / `ARCH_RY`, waterline and the three waves
at the sealed y and mass. The deck overhangs its end piers by 8.53 u, which is
the sealed drawing's own proportion — round 3's "drying rack" was a THIN OUTLINED
deck on thin legs, not this one. The displacement is now the plan's own 139 px
(`canvas_rects.bridge_predisplace`), not the 124 px the earlier board used.

Result: four independent readers, four reads of `bridge`, three of them `sure`.

## 3 — DEPARTURE: the second bank is written on TWO lines, and the connector row writes WORKSPACE

Both are forced by laws, not chosen.

* `GOOGLE WORKSPACE` on one line at a legible 26 px is 162.8 u of ink and its
  right edge lands at 497.4 u, past the 489.6 u right rail (LAW 30). It is
  written `GOOGLE` over `WORKSPACE`. The PLANNED key declared to
  `assert_label_law` is the first line, `GOOGLE`: the assert keys `written` by
  TEXT, so declaring `WORKSPACE` would be measured against the connector row's
  own `WORKSPACE` at 12.76 s and fail LABEL_WINDOW by 9.8 s.
* The connector row writes `WORKSPACE`, which is the plan's own open question 3,
  and the caption chunker independently forces it: the pill `Google Workspace.`
  is emitted twice and the second is alive across the row's last second, so a
  board word reading GOOGLE WORKSPACE is LAW 4's double and
  `caption_identity_guard` refuses the build. The row still carries the real
  Google Workspace mark beside the word.

## 4 — DEPARTURE: the arrow anchor inset is 0.28, not the plan's 0.16

The plan's own note says an arrow's ink box is the CHEVRON's extent, never the
shaft's. At the helper's default 0.16 the read arrow's head sits 5.2 u under
`type:CURSOR`, inside LAW 41's 8.5 u refusal on THIS board (the board is 1/1.875
of canvas, so the plan's 27.92 core px of clearance is not what this lane
measures). The ends still come off `anchor_points()` on the tiles' own facing
edges, level to 0.0000 u and mirror-symmetric about the tiles' own axis.

## 5 — DEPARTURE: the plan's overlapping per-object blocks are merged per picture

`assert_spacing_law` indexes a name into ONE block, so the plan's fourteen
overlapping blocks are collapsed into one block per chapter picture. The intent
is identical: chapter 0 is ONE assembled drawing (two tiles standing ON a deck
with two lanes of traffic between them) and chapter 2 is a container and its
contents.

## 6 — Not a departure: the settings panel's filled title bar

The plan's `how_drawn` already specifies the filled mount bar with the Cursor
mark plain on it, and this board draws it. Recorded because it is the remedy that
turned run 16's hedge into a read, and because the plan's OTHER remedy — a second
unfilled hairline row — was deliberately not taken: an anonymous plate in a row is
LAW 29's named defect.

## 7 — FLAGGED FOR THE CLERK: what `google-workspace` actually is

The registered artwork under registry key `google-workspace` is the gradient
Google G that `workspace.google.com` declares as its own `<link rel="icon">`. The
plan (marks, open question 1) documents this and calls it the PRODUCT's own icon
under LAW 35, deliberately distinct from `google-g` (the flat four-colour Search
mark). It is nonetheless a Google COMPANY glyph rather than a distinct Workspace
product mark, because Google publishes no single-glyph Workspace mark. This board
paints the SAME file the sealed scene module paints, so the three platforms
cannot argue three different marks. Substituting anything else here would put a
mark on Reels that YouTube and TikTok do not carry, so the disagreement is logged
rather than improvised.

## 8 — Reader-model hedging on the settings panel

`toggle switch` is the only name any reader has ever returned for bespoke object
1 — five reads on this board and twelve in the artwork stage across four
drawings, zero naming a different object — but confidence oscillates between
`sure` and `unsure` between rounds. The plan's open question 9 already
root-caused this: the fallback reader model hedges on UI mocks as a class, and
hedged on a CONTROL crop of the connector row alone
(`review/proofs_cursorworkspace/diag/diag_row.json`). Round 6 returned `sure` on
the shipped crop. Recorded rather than answered with a fifth redrawing.

## 9 — DEPARTURE: the settings card is 212 canvas px tall, not the plan's 268, and the switch is 180x70, not 152x60

The plan's `how_drawn` for bespoke object 1 specifies a 560 x 268 card and a
152 x 60 toggle, and its open question 6 names the remedy for a hedged read on
this object: **"a bigger toggle relative to the card"**. Six independent readers
on the plan-sized card returned `toggle switch` and nothing else, but only a
minority were `sure`, so the remedy was applied: the card body loses 30 canvas
px of dead height (408..620 instead of 408..650, header 74 instead of 78) and the
switch grows to 180 x 70 with a 28 px knob. At the phone crop the control is now
68 x 26 device px inside a 216 x 85 card, against 57 x 23 inside 210 x 100.

Consequence, and it is deliberate: the phone-test crop for this object is derived
from the card THIS board draws (`CARD` +/- 4 u) rather than copied from
`bespoke_objects[1].bbox`, because the plan's rect is its 268 px card and would
have handed the reader 56 canvas px of empty board underneath the object. The
plan's own bbox is still recorded beside it as `plan_bbox`.

## 10 — The phone evidence, and why six rounds on two models

`review/scores_cursorworkspace_whiteboard.json`. Six independent rounds on the
shipped crops, three on the inherited configured reader and three pinned to the
haiku fallback, declared before they were run and all six scored; the earlier
rounds (4haiku, 5, 6, 7, 8) read superseded drawings and are kept on disk as the
redesign's record, not submitted as evidence.

* object 0, **an arch bridge** — six reads of the intended object, five `sure`,
  zero naming a different thing (`bridge over water`, `bridge`, `arch bridge over
  water`, `bridge`, `bridge`, `aqueduct`). An aqueduct is an arched bridge that
  carries water: a sibling noun, and the plan's pass list already covers viaduct
  and overpass while its named failures are a bench, a fence and a table.
* object 1, **a settings panel** — six reads of `toggle switch`, three `sure`.
  The hedging model hedged 3/3 both BEFORE and AFTER the card was tightened while
  the second model returned `sure` 3/3 after it, which is what says the hedge is
  the instrument and not the drawing (note 8).

## 11 — The outro carries no bridge glyph, and the harness is why

The plan's beat 4 picture asks for "THE BRIDGE drawn small and one step heavier
directly above [the handle] on the same centre axis". The canonical harness's
`outro_block()` takes exactly one parameter beyond its timing - the handle - and
emits the chassis lockup: terracotta rule, handle, `daily AI`. There is no glyph
hook, and forking `whiteboard_build.py` is forbidden. The plan's OWN per-lane
instruction for this format asks only for the rising sheet and the handle card
("Outro: opaque rising sheet 17.319-17.78, handle card @migueltorrez.ai from
17.800"), so the themed glyph is the SPLIT's and the CUTOUT's move, taken from
`cursorworkspace_scene.py::OGLYPH`. Recorded, not improvised around.

## 12 — The Gemini watcher did not run on this render

`render_and_check` reported `watch_unavailable: Gemini API 429 RESOURCE_EXHAUSTED
(monthly spending cap); $0`, staged the file on `qc_pass` alone and wrote no
`review/cands_cursorworkspace_whiteboard.json`. That is the tool's own handling,
not a `watch_waiver` written into the spec. The clerk therefore has no watcher
candidate list to adjudicate for this composition and has to decode the staged
file itself.
