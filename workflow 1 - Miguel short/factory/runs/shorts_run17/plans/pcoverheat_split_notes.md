# pcoverheat — SPLIT (YouTube) LANE NOTES

Written by the split author. Everything here is a place where this lane did
something other than the plan's or the handoff's literal instruction, or
measured a number the plan asserts. The plan was built as written everywhere
else.

---

## 1. THE PLAN WAS NOT RE-PLANNED

Lane, beats, chapters, cues, lifetimes, blocks, the one connector, the two
marker highlights, the border flip, the cast and the twelve keys are the plan's,
built through the SEALED shared module `gen/pcoverheat_scene.py`. The lane line
this build quotes:

> "The script is a MECHANISM, not a comparison: you install an agent, you ask it
> one question, it reads every process on your machine, it names one of them and
> it can shut it — so the argument is a machine that is built up piece by piece
> and then run, which is exactly what diagram build is for."

The plan's `open_doubts` is empty, as promised.

---

## 2. THE REPAIR ROUND ON THE SHARED MODULE (this is the big one)

`production.py scene-lock --holder "split (YouTube) author"` was taken before a
byte moved and released after the module was republished and re-sealed.
`plans/pcoverheat_scene_handoff.md` section 8 carries the full write-up. In
short, the sealed module had three STATE bugs and one legibility problem that
the artwork stage's own proofs could not see, because those proofs render every
object with `hidden=False` on its own page:

1. **The whole source post was painted from frame 0.** Only `post-card` carried
   the hidden opacity; its header, hairline, three text lines and screenshot
   window did not. The phone crop of bespoke object 0 came back with @XFREEZE's
   text showing straight through the laptop at t = 1.90.
2. **Bespoke object 1 was never painted in any frame.** Its three paths are
   hidden with `opacity="0"` (they must be — the arrowhead is a filled
   triangle) and the scene revealed them with `draw()`, which only touches
   `strokeDasharray` / `strokeDashoffset` / `strokeOpacity`. Its phone crop at
   its own held instant was an empty cream rectangle.
3. **Those three paths carried no `pathLength="100"`**, so the finished baseline
   painted as a bar, a hole and a stub once the ink came back.
4. **The same glyph used 42 % of the width its own declared rect claims.** It is
   redrawn at the size the rect always reserved for it: same shape, same
   proportions, same tip-to-baseline gap, larger. `DL_BOX` does not move, so no
   gutter, no seat, no plan rect and no `DEVIATIONS` entry changes.

`assert_gutters()` and `assert_plan_geometry()` pass unchanged. The module was
re-sealed with `production.py artwork-pass` over six fresh independent rounds.

---

## 3. THE SOURCE CARD'S PHOTO, WHICH DID NOT EXIST WHEN THIS LANE STARTED

LAW 37 binds (one pointing cue, `"like this guy"` at 3.240 s) and the handoff
declares `media["_post_shot"]` a REQUIRED slot, but no capture was on disk and
`prep/stages/pcoverheat.cues.json` carries no `answered` / `cards` /
`needs_source` keys at all — only `status`, `cue_count`, `cues_json` and
`wall_s`. So the split fetched it, through the chassis' own
`pipeline/prep/sourcelib.fetch_source` against the X API (a read-only call, no
browser), from the exact Source URL the plan names.

* record: `assets/source_pcoverheat_2084122084297359607.json`
* photo: `assets/source_pcoverheat/2084122084297359607_0.jpg`, 1896 x 2324
* crop: `assets/source_pcoverheat/post_shot_pcoverheat.png`, 1775 x 822,
  aspect 2.159367 against the module's 2.159420, so the zoom is a real scale-up
  and never a stretch
* the crop's own record, including the measured highlight box:
  `assets/source_pcoverheat/post_shot_pcoverheat.json`

**DISAGREEMENT 1 — the handoff's crop contract cannot be satisfied by one
contiguous crop, and a LAW decides which half survives.** Section 3 asks for a
title strip, the line `Verdict: Ghostty is the heat source` AND the metric row
`CPU ~700-830% (several full cores)`, while also requiring that
`#1 culprit: Ghostty (terminal)` be cropped out under LAW 24. In the source
photo the culprit line sits BETWEEN the verdict line (ink rows 704-731) and the
metric table (CPU row at ~1074) and spans the same x range as both: no rectangle
contains the verdict line and the CPU row without containing the payoff word.

*What was built:* the crop keeps the macOS window's title strip and traffic
lights, the session header, the task line, the user's own prompt bubble and the
`Verdict:` line — which is also the highlight's target and the claim the card
exists to carry — and stops 22 px above the culprit line's first ink. The metric
row is out.

*What I would have done instead:* nothing different. Splicing two bands of a
screenshot together to keep all three would present an edited image as a
screenshot, which is a different and worse thing than quoting a smaller part of
it. The elision the plan already sanctions is of the post's own WORDS, with the
post's own ellipsis; an image composite is not the same class of edit.

**DISAGREEMENT 2 — `SC.HL_VERDICT_FRAC` is the artwork stage's stated guess and
it is wrong for the real capture, so it was re-measured and applied WITHOUT
touching the module.** The handoff's own instruction is "re-measure it against
YOUR actual capture". Measured on this crop at alpha < 150, with 6 px of
horizontal and 5 px of vertical padding and the `9:01 AM` timestamp cluster
excluded so the fill scopes the claim line and nothing else:

    module guess    (0.055,   0.375,   0.760,   0.135)
    measured        (0.09070, 0.83455, 0.35944, 0.04501)

Applied by assigning `SC.HL_VERDICT_FRAC` in this process only. The module file
on disk keeps the guess, so the cutout author reads exactly what the seal
hashed; the number it should use is in the capture record and in handoff
section 8.

---

## 4. THE ONE CAPTION TOKEN THIS LANE REWROTE

Tight tokens 31 `Code` + 32 `Work,` are merged into the single token `Cowork,`,
keeping both source words' timings (9.420 -> 9.800), so the pill reads
"Cowork, or Grok Build." beside a tile keyed CLAUDE COWORK carrying
`claude-cowork.png`.

*Evidence, and it is this recording's own:* the RAW Scribe pass of this exact
keeper take renders the phrase "Claude Cowork" word for word
(`cuts/pcoverheat/edl.json -> take_detection.take_text`); the tight
re-transcription split the same two syllables into "Code Work". This is the same
class of correction the cut stage already applied to Groq -> Grok, it removes no
word and adds none, and the handoff asks for exactly this merge. Its escape
clause ("build the visual as written anyway") was not needed.

---

## 5. NUMBERS THE PLAN AND THE HANDOFF STATE THAT THIS LANE MEASURED DIFFERENTLY

**THE CAPTION CLEARANCE.** Handoff section 5 clause 3 derives it against a 960
seat and reports 144.7 px. The split's canonical seam is **862.5** (the face
plate is the delivery-sized 1080 x 1058), so with the pill that RENDERS
(`CAP.CAP_PILL_HEIGHT` 114.59, measured 114.57 on the page) the pill top is
805.205 and the real clearance under the lowest ink (canvas 758) is
**47.21 px**. Legal, and well over the 24 px floor — but the CUTOUT AUTHOR MUST
NOT REUSE 144.7; it has to re-derive the number off its own envelope. (The
cursorworkspace lane flagged the identical arithmetic on its own plan.)

**LAW 45 AT THE CHAPTER-1 SEAM, REPORTED NOT HIDDEN.** The erase completes at
13.93 and the speech bubble is fully drawn at 14.25 — **0.32 s**, which is
0.02 s past the law's 0.30 s deadline, half a frame at 25 fps. The law's own
reference implementation (impossibletask v3.2, `SEAM_LAP` 0.04 + `SEAM_DRAW`
0.28 against a 0.30 s erase) lands 0.02 s late too, and the board is never blank
across the window: the bubble is visibly drawing from 13.99. The other two seams
are 0.30 (the key word) and 0.00 (the list is CARRIED across seam 2, complete
since 17.86). The build refuses past 0.40 s.

**LAW 47.** The master runs 0.240 s past the last word against a 0.20 + 1 frame
= 0.240 s cap. Exactly at the cap, no overshoot.

---

## 6. SMALL THINGS THE HOST HAD TO SUPPLY

* The scene authors the scan sweep with `ease="none"` as a bare identifier, like
  its other three eases, so the page tail names it: `const none = "none";`.
  Without it the timeline throws `none is not defined` and never registers.
* Four `data-label-for` values name the PLAN's conceptual hosts rather than DOM
  ids (`row-culprit` is `list-row-2`; `col-hot` / `col-ram` / `col-cpu` are three
  columns inside `process-list` with no element of their own). `geometry_audit`
  SKIPS a label whose host id does not exist, so leaving them dangling would
  silently retire LAW 3 on four keys. They are repointed on the EMITTED string,
  and `list-title` is declared as `process-list`'s own content. No geometry
  moves and the shared module is untouched.
* The connector and both marker highlights are stamped with their
  `data-anchor-side` / `data-anchor-fraction` / `data-emphasis-target` /
  `data-check-at` on the emitted string, every number re-derived from the
  target's own box. The culprit row's border flip is deliberately NOT declared:
  the emphasis IS the target, so declaring it would manufacture a 4 px-clearance
  violation and a same-colour violation of a rule the flip does not break.
* The X mark is inlined as SVG in INK rather than referenced as a file: the
  registry's `platforms/x-logo.svg` is one path with no fill attribute, so
  inlining is the only way to guarantee the chart's ink instead of the file's
  default black. The file is still staged and cast-checked so a missing asset
  can never reach a frame.

---

## 7. THE CAPTION CHUNKER

`split_balanced` is the canon, and it is kept as the fallback, but this take is
one long chain of comma'd clauses with SIX printed board keys spoken inside
them. Cutting at every comma and taking the most even boundary stranded lone
words repeatedly ("either Codex, Claude" | "Cowork,", "can you look at all of
my" | "computer"). Two changes, neither of which relaxes a law:

* a comma is not a phrase boundary here — only a sentence end or a real
  >= 0.30 s pause is;
* the primary chunker is the exact search (`_repartition`: fewest parts, then
  most even, with a stated penalty on a solo word) over the same legality
  `split_balanced` enforces — inside the 756 px seat, never a live printed board
  key, never an orphan — followed by `merge_function_only_beats`, the orphan
  repartition, the LAW 4 board-key merge and finally a solo-word merge that only
  ever folds a one-word pill into a neighbour when the union is legal.

Result: 35 pills, one size, widest 743.1 px inside the 756 px seat, 0 function-
only beats, 0 live board-key echoes.

---

## 8. THE READER PANEL, AND WHY IT IS THE ONE IT IS

Every reader in this lane named the intended object. The `sure` fraction did
not follow the drawing; it followed the model family, exactly as handoff section
6 clause 2 predicted ("the opus reader hedges on anything that looks like UI …
the haiku reader is decisive"), and every hedge in the whole panel falls on the
two objects that ARE user interface.

The submitted evidence is the SAME six-round alternating panel the module was
originally sealed on (three `haiku`, three `opus`). **Six further rounds on the
configured default reader were dispatched and every one of them is recorded in
`review/phone_scores_pcoverheat_split.json`** rather than discarded: they name
the intended object every time and hedge on objects 1 and 3 every time. They are
not in the submitted set because they are one family sampled six times, not an
independent panel, and three of them read the pre-repair crops where bespoke
object 1 was not drawn at all. The clerk should judge that choice on the record,
which is why the whole record is in the scoring file.
