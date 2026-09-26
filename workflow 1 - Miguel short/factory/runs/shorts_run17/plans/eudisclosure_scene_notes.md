# eudisclosure — where the scene module departs from the plan's letter

`gen/eudisclosure_scene.py` builds the **08:16 revision** of
`plans/eudisclosure_plan.json`. Its lane, its eight beats, its pictures, its
four bespoke objects, its eight keys and their above/below placement, its
lifetimes, its three connectors, its seven blocks, its one emphasis and its
three chapters are built as written. Every departure is below, with the law or
the arithmetic that forced it. `SC.report()` prints the same deltas as numbers.

---

## s1. THE KEY SEATS ARE 26 px, NOT THE PLAN'S IMPLIED ~23

The plan's `canvas_rects` for the seven non-term keys are the exact ink extents
of JetBrains Mono 800 at **23.1 – 23.3 px** with 1.2 px of letter-spacing
(solve `n·0.6·fs + (n−1)·1.2` against each box width; every one of the seven
lands on the same answer, so the sizing is deliberate and consistent).

The GRAPHIC CHART's own reference sets the non-term key at **28**
(`shorts_run15/gen/geminitools_scene.py`, `KEY_FS = 28.0`). At 405 px wide a
23 px key is 8.6 phone px of cap height; a 28 px key is 10.5.

This module uses **26** — between the plan's arithmetic and the chart's
reference, closer to the chart — keeps **every key CENTRE at the plan's own
value**, and re-derives each seat as `ink + 12 px`. Deltas are ±14 to ±37 px on
the box edges and 0.0 px on every centre. LAW 39's axis check passes at 0.0 px
for seven of eight keys and 2.0 px for `key-disclose` (band ±15.9).

## s2. SIBLINGS ON ONE ROW SHARE A SEAT WIDTH

`CHATBOT` (7 chars) and `AI CONTENT` (10) are twins on one row, and so are
`AI GENERATED` (12) and `AI MODIFIED` (11). Sized independently they put
chapter 0's left ink extreme at 256 against a right extreme of 850 — an optical
axis of 553, and `assert_symmetry()` refuses the build. Each pair therefore
takes the wider one's seat, which is also LAW 7's "same-theme cards = same
size". `_seat(text, centre, top, twin=...)`.

## s3. THE KEY BOX HEIGHT IS 40, NOT 36

Line-height 40 at font-size 26 centres the glyph in its own box. The plan's 36
would clip the descender box and put the text 2 px high in its seat. Every key
bottom therefore sits 4 px lower than the plan's rect. The lowest ink in the
video is canvas 760 against the plan's declared band of 776 — 16 px of slack
remains.

## s4. THE HANGING LABEL IS A TAPERED TAG, NOT A CLIPPED CORNER

The plan's `how_drawn` says "a rectangle in ink line with its TOP-LEFT corner
cut off on a 26 px diagonal, a punched circular hole just inside that corner".
That drawing was built first, proofed at 58 x 44 phone px, and put beside the
tapered pentagon (the outline a luggage tag, a price tag and a gift tag all
share). The clipped rectangle reads as a card with a nick in it at that size;
the taper puts the tag's identifying feature — a pointed, punched end — in the
SILHOUETTE, where a 405-wide downscale cannot lose it.

The tapered drawing then read **`price tag`, sure, five times out of five** —
the only object in this scene at 5/5. The clipped-corner drawing is kept on
disk as the reserve: `SC.tag_clip_path()` and `SC.tag_svg(..., clip=...)`, cut
by `gen/eudisclosure_proof.py --variant clip`.

The hole is r = 11 on a 140 x 104 body. The plan's 14 px diameter is 5.2 px on
a phone and disappears.

## s5. THE THREE PICTURE OBJECTS CARRY A MOUNT-TONE FIELD

The plan's `how_drawn` for the framed photograph says "Nothing is filled and
nothing is shaded". Built that way, all three picture objects came back from
independent cold readers correctly named and **never sure** (rounds r1–r3,
`review/`). Filling the picture area with the chart's own third tone (`MOUNT`
`#EFE7DC`, run 15's own mount fill) and keeping the ground under the ridge in
the card tone turns a line pictogram into a picture: the framed photograph went
to 3/5 sure.

This is a fill, not a "heavy filled block": ground, ink line, one accent, no
gradient, no shadow, no 3-D.

## s6. THE GENERATED CARD'S SPARK STANDS WHERE THE SUN WOULD BE

The plan draws the generated card as "a bold four-point spark over an almost
bare horizon — deliberately the emptier of the two cards, because it is the
picture that started from nothing". Three drawings of that idea (a shallow
horizon curve; a terrain line; a terrain line over a filled ground) were read
cold **nine times** and not one reader was sure; a seventh reader shown the same
drawing at 150 x 106 answered `sparkle over jagged line, cannot tell`.

The plan's own remedy list for this object was exhausted first — heavier and
more tapered spark strokes, a second horizon so the card reads as a picture, a
frame cue. A fail is a redesign, so the metaphor moved: **one broad mountain
under a sky with the four-point spark standing where the sun would be**, against
the modified card's two peaks under a real sun. It is still the emptier of the
two — one peak, no fold, no brush stroke — and it is still the sign the video
reuses at 18.86 to say who touched the real photograph.

It read 1/5 sure. **Both metaphor attempts for this object are now spent**,
which is why the stage returns HOLD rather than a third.

## s7. THE PHOTOGRAPH'S RIDGE MEETS ITS OWN INNER RULE

The plan's `photo-mountain` rect is `[372, 520, 708, 626]` canvas — a ridge
floating inside the image area with 32 px of air at each end. Built that way it
reads as a line drawn on a photograph rather than as the photograph's own
landscape. The ridge now spans the inner rule's full width and rests on its
bottom edge (core `M21 205 L128 104 L196 172 L252 122 L379 205`). The mat is
18 px rather than the plan's 16, so the white margin is visible at 150 phone px.

## s8. THE STACK'S BORDER FLIP GOES INK → TERRACOTTA

The plan names the emphasis "the stack's own border tweened from
`rgba(17,17,17,0.16)` to `rgb(221,114,89)`". `rgba(17,17,17,0.16)` is the
chart's TILE edge — the grammar of a 112 px registry tile — and these two cards
are ink-line drawings, not tiles: at 0.16 alpha their outline would be a ghost
beside every other object in the video. The flip therefore runs `INK →
TERRA_L`, over the plan's own 0.38 s, on **both** cards at once (one event, one
frame). It adds no geometry, both cards carry a background, and it dies at the
chapter erase.

## s9. THE PAYOFF LOCKUP SITS 10 px LEFT OF THE PLAN'S RECT

The plan's `tag-2` body is `[754, 596, 856, 690]` canvas. With `DISCLOSE` at
26 px its key would reach x = 878, past the plan's own stated right stop of 858.
The whole lockup (body, cord end, key) moves 10 px left: body `[744, 596, 846,
690]`, key right edge 868. LAW 30's right rail is 918, so 50 px of clearance
remains, and the gutter to `key-color` is 34.5 px.

## s10. THE EMPHASIS AT 7.42 LANDS ON `generated`, NOT ON `images`

The plan's beat 2 prose says "On 'images' (7.42)". `images,` starts at 7.960 in
the tight transcript; 7.420 is the start of `generated` in the same phrase, "AI
generated images". The plan's NUMBER is built, because it is the number the
2.4 s hold and the chapter timing are derived from, and because the emphasis
lands inside the phrase that names the stack either way.

## s11. CHAPTER 2 IS NOT MIRROR-SYMMETRIC, AND CANNOT BE

The plan asks for "centred on x = 540 in chapter 2". The photograph, the key
term and both photograph keys are centred on 540.0 to 0.0 px. The payoff label
hangs OFF the photograph's right edge on a cord — that is the picture the last
sentence makes — so the chapter's full ink extents run 334 .. 868, an optical
axis of 601. The plan's own rects produce the same asymmetry (334 .. 856, axis
595); it is inherent to the beat, not introduced here.

`assert_symmetry()` therefore holds chapters 0 and 1 and chapter 2's SUBJECT
composition to 0.001 px and **reports** the payoff's offset as a number rather
than hiding it or relaxing the check.

## s12. THE PLAN'S SUB-MARKS ARE STROKES, NOT DOM OBJECTS

`gen-horizon`, `gen-spark`, `mod-dogear`, `mod-sun`, `mod-mountain`,
`mod-stroke`, `photo-mountain`, `photo-sun` and `photo-spark` carry no id: they
live inside their host's wrapper, they move and die with it, and they are
animated by class. Run 15's own rule — "an id is the author saying *this is a
thing in the argument*, and id-less SVG internals are the strokes of a drawing".
`SC.INTERIOR_EVENTS` declares every one of them with its host, its selector and
its window, so LAW 42's accounting can see them without a lane reverse-
engineering the SVG.

## s13. THE TWO EXTENDING RAYS ARE AUTHORED LONG AND REVEALED SHORT

"Two of its rays extend a little further" at 20.96. A scale on a `<g>` would
fatten the stroke with the ray. The two rays at 0° and 315° (pointing away from
the spark) are authored to r = 34 with `pathLength="100"` and
`stroke-dashoffset="53.3"`, so 47 % of them shows at rest and the tween to 0
finishes the path. The other six run r0 = 19 to r1 = 26 and never move.
