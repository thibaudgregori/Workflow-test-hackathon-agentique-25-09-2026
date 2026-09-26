# kimifable — where the shared scene departs from the plan, and why

The plan (`plans/kimifable_plan.json`) is the contract and this module does not
re-plan it. Its lane, its nine beats, its four chapters and their seams, every
cue, the key term, all six written keys and their BELOW placement, both
emphases, the lifetimes, the blocks, the cast and the 1-of-3 that runs through
every chapter are built as written.

There are **three** departures. None of them is a preference and none changes
what the video CLAIMS; all three were forced by independent cold readers looking
at phone-size stills of the drawing, which is the instrument the plan's own open
question 5 said would decide these objects. Evidence:
`review/artwork_scoring_kimifable.json` and the reader files listed in §8 of the
handoff.

---

## 1. The two cords are gone; the price tags lie flat

**The plan** (`connectors`, beat 0): each tag hangs off its tile by a cord that
originates on `anchor_points(TILE_BOX, 1, "bottom")` and terminates on
`anchor_points(TAG_BOX, 1, "top")`, mirror-symmetric about x = 540.

**What happened.** Three drawings of a hanging tag were rendered at 405×720 and
read by independent readers who saw nothing but a blind crop:

| drawing | reads |
|---|---|
| chamfered top, hung by a 34 px cord | "hanging pendant lamp", unsure |
| pointed apex (87°), hung by a 34 px cord | "price tag" ×4 … then "birdhouse" ×2, "handbag hanging by strap" |
| the same, scaled up 27 % | "hanging birdhouse", unsure |
| the same, cord lengthened to 50 px | "birdhouse", "birdhouse", "handbag hanging by strap" |

A peaked box with a punched hole on a string **is** a birdhouse. It does not stop
being one at a heavier stroke, at a bigger crop, or with more string — the third
and fourth rows of that table are two attempts to fix it by adding more of the
cue, and both made it worse.

**What this file does instead.** The tag lies FLAT: a body whose left end runs to
a point, a hole punched in that point, sitting under its tile as its price and
welded to it in one declared block. It has been named *"price tag"* on every read
since, twice `sure` out of three in the seal. **There is now no connector
anywhere in the scene** — `SC.CONNECTORS` is empty and
`SC.assert_no_connectors(html)` refuses a `data-connect-to` that reappears, so a
lane that wants one back has to re-derive its ends with `anchor_points` and
re-seal the artwork.

**What is preserved.** Both tags are the SAME tag at the SAME size (LAW 7's
same-theme-same-size, which the plan's two different tag heights would have
broken), and the claim is the COUNT inside them: one terracotta coin under Kimi
against three under Fable, landing on their own words exactly as the plan
schedules them. LAW 19's single displacement is intact — the tag still opens
centred on x = 540 and moves once.

## 2. The scorecard is on a clipboard

**The plan** (bespoke object 3): "A cream card, 3 px ink-alpha border, radius 18,
with a full-width ink header rule near its top and three square-ended horizontal
bars sitting on three OPEN ruled baselines beneath it… the top bar terracotta and
longest."

**What happened.** Drawn exactly that way it was named *"bar chart"* or
*"horizontal bar chart"* by seven independent readers and **not one of them could
commit** — five `unsure`, two `cannot tell`. One reader wrote the reason into its
own answer: **"bar chart (not an object)"**. The instrument asks for *the single
everyday object drawn in the picture*, and a chart is not a thing a person has
held. Redrawing it as a dog-eared sheet of paper fixed the category and lost the
argument: three readers then said *"sheet of paper"*, naming the medium instead
of the measurement.

**What this file does instead.** The same card, the same header rule, the same
three square-ended bars on three open ruled baselines, the same single terracotta
row — clipped to a board, with the clip standing above its top edge. Three
readers, three times *"clipboard"*, all three `sure`. That is the object the
picture is: a scorecard on a clipboard.

## 3. "A lot of designs" is a folder, not a stack of windows

**The plan** (bespoke object 4): "The website-layout glyph drawn three times,
each copy offset 14 px up and to the right of the one beneath it… so only the
front card shows its hero and columns."

**What happened.** Every reader named it correctly — *"stacked browser windows"*,
*"stack of browser windows"* — and only **three of nine** could commit. At a
20 px offset one reader called it *"stack of credit cards"*, which is a different
object and on its own would fail the seal. Widening the offset to 30 px so each
copy shows its own title bar and dots killed the credit-card read but not the
hedging, and replacing the stack with one window holding a grid of six pages did
not fix it either (*"web browser window"*, unsure).

The cause is structural, not legibility: the reader is asked for **the single**
everyday object in the picture, and a stack of three is not one.

**What this file does instead.** A FOLDER, with pages standing out of it and the
top page carrying this video's own window chrome, so the folder is unmistakably
full of the thing chapter 2 just drew. Three readers, three times *"file
folder"*, all three `sure`. The claim is unchanged — a container of many designs
is "running a lot of designs" — and the chapter's key, `YOUR DESIGNS`, still
names it, still sits BELOW it, and is still parented to it through the LAW 19
displacement.

---

## Not a departure, and recorded so a clerk does not read it as one

* **The composition is at a different scale to the plan's `canvas_rects`.** The
  plan's own numbers put the hook object on a phone at 66 × 39 px, under every
  crop that has ever passed a cold read in this factory, and the plan's open
  question 5(a) ranks it the run's likeliest Phone-Test failure. Each object is
  drawn at the size its reader needs; the band grammar, the axis, the seams, the
  cues and the gutters are the plan's. `SC.canvas_rects()` is the machine-
  readable twin of what is actually drawn, and `SC.self_check()` proves the
  spacing, the axis and the band before a lane seats it.
* **`build-fill` is authored at the CUT width and tweened out to full on
  entrance, then cut back on the word *cut*.** That is LAW 23's clause built the
  way the plan asks (one pill, clipped to the track's radius, `min-width` = track
  height, remaining progress is empty track and nothing else) — the authoring
  order is inverted only so the authored HTML is the held frame, which is what
  makes still proofs possible with no GSAP and no render.
* **The reader model is `opus`, not the pipeline's configured default.** The
  default refused every dispatch with a usage cap ("You've reached your Fable
  limit"), which `cold_read.py` records as a dispatch failure and refuses to
  score. A `haiku` control was run on the same four crops and named three of them
  wrong with full confidence — *"light bulb"*, *"smartphone"*, *"microwave"* — so
  it was not used. Every round in the seal is the same model.
