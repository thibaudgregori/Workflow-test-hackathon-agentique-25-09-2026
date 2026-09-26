# nextslide split notes (author_split_nextslide, 2026-09-22)

The split builds the plan and the sealed scene as given: k = 1.00, left 0,
core top 192 (the handoff's own placement). The module on disk is unchanged
(`production.py artwork-check` hashes still match the seal). The notes below
cover what the split adds to the emitted string, and one disagreement.

## 1. Where the card -> easel arrow lands (LAW 40, followed and logged)

The plan's connector says `to: "easel"`. Its note says the arrow lands on the easel
BOARD's right-edge centre, meaning the board's virtual rectangle and not the tripod.
The module draws it that way: the tip is at the displaced board's outer right edge,
(432, 231) core. But `data-connect-to="easel"` points production's anchor check at
the whole `#easel` box (118..446 at the displaced seat), which puts the anchor 14 px
to the right of where the arrow lands. The board's `.bframe` rect has the same
problem, because its SVG bbox leaves out the 8 px stroke and ends at 428.

So the split inserts one inkless box, `#easel-board`, inside `#easel` at
`BOARD_REL` (14,16 to 314,226 easel-local). It moves with the easel. The connector
declares `data-connect-to="easel-board"`, right side, fraction 0.5, check-at 8.40.
The box has no background, no border and no text, so nothing new is painted.

## 2. Declared anchor fractions of the three model arrows

`line_svg` rounds the tip to 0.1 px. That leaves `conn-grok`'s painted tip at
(760.5, 272.3), which is 4.08 px from the planned anchor (758, 269.08). The strict
limit is 4.0 px. The split therefore declares each diagonal's anchor at the point
on the card's right edge nearest its painted tip: claude 0.1321, gemini 0.5,
grok 0.8688. The planned values are 0.16 / 0.5 / 0.84. All three stay mirror-
symmetric about the card's centre row to within 0.1 px, and each is less than
4 px from its planned end. A fix in the scene would round `back` to 0.01 px, or
pull the tip back by 3.9 px.

## 3. Emphasis declarations

* The NextSlide card's border flip: `data-emphasis="border"` on `#nextslide-card`,
  targeting its wordmark raster. The raster is stamped `id="mark-nextslide"`,
  the plan's own block name. Check-at is 10.30, held from 10.16 to 10.60.
* The board frame flip: the `.bframe` rect gets `id="easel-frame"`,
  `data-emphasis="border"`, target `easel`, check-at 28.60.

## 4. What I would have done differently (built as sealed)

The verdict is one centred string, `PRETTY` + ` + UNDERSTANDABLE`, and the second
span is invisible until 28.06. So from 26.94 to 28.06, PRETTY sits about 150 px
left of the easel's axis (visible on `review/split_nextslide_look/phone_27.00.png`).
It is also the smallest type in the video (28 px, about 15 du) and it carries the
payoff. My version: PRETTY lands centred, slides left as + UNDERSTANDABLE arrives,
and the verdict runs at 34 to 36 px. That change belongs to the design seat, so the
split leaves it alone.
