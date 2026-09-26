# pcoverheat — WHITEBOARD author's notes

Where this board departs from `plans/pcoverheat_plan.json`, with the reason and
what I would have done otherwise. **The plan was built anyway everywhere it did
not collide with a law, a sealed object or a missing asset.** The plan's
`open_doubts` list is empty and I found no new doubt that changes what the
viewer sees.

---

## 1. THE TWO SUPERSEDED DRAWINGS — a SPEECH BUBBLE, not a text field; an ARROW OVER A BASELINE, not a browser and a tray

**The plan** (`bespoke_objects` 1 and 2, `canvas_rects.download-kit`,
`canvas_rects.prompt-field`): a browser window with an arrow dropping into an
open tray, and a wide rounded input with a chevron prompt glyph and a caret.

**Why this board does not draw them:** the ARTWORK author's seal
(`review/artwork_pass_pcoverheat.json`, six rounds, 24 reads) replaced both, and
`plans/pcoverheat_scene_handoff.md` says so in as many words: *"it must use the
sealed objects below, not the plan's superseded ones."* The plan's text field
was read `play button`, `pencil`, `Terminal command prompt`, `none — abstract
chevron and dashes` at **0 of 6 sure**; the plan's tray was named `inbox` by
three readers, and a cloud-and-arrow was named `rain` by two.

**What I did:** drew the sealed metaphors in the board's own marker language — a
speech bubble carrying the instruction as terracotta ink runs, and a solid
download arrow over a solid baseline. Not a copy of the scene module: the
whiteboard redraws the argument, it does not import the lane scene.

## 2. THE SOURCE CARD CARRIES THE POST, NOT THE SCREENSHOT IT LINKED

**The plan** (`pointing_cues[0].inner`, `canvas_rects.post-inner-small` /
`post-inner-zoom`, `emphasis[1]`): the card shows the photo the post carried —
a Grok Build session on a Mac — small at first, then scaled up to fill the card
at 3.86 s, with a second marker fill on the line `Verdict: Ghostty is the heat
source`. The crop is scoped to a title strip, that verdict line and the metric
row `CPU ~700-830%`, with the next line `#1 culprit: Ghostty (terminal)`
**cropped out**.

**Why it is not there:** I fetched the real post
(`pipeline/prep/sourcelib.fetch_source`, record
`assets/source_pcoverheat_2084122084297359607.json`, photo 1896x2324 on disk)
and measured the capture. **The plan's scoped crop is not a contiguous region of
it.** In the actual screenshot the order is: verdict line, one sentence, then
`#1 culprit: Ghostty (terminal)`, and only then the metric table with the CPU
row. Any single crop that holds both the verdict and the CPU row also holds the
word **culprit** — which the plan's own `open_questions[6]` forbids on screen at
4 s, because this video's whole payoff is that word landing on a boxed row at
30.22 (LAW 24, no peek-ahead). The second reason is scale: at the whiteboard's
own surface the card is 388 board units wide, and the screenshot's 11 px
terminal type inside it is not legible on a phone (chassis format law 7, *boil
the diagram down*). The chassis' own card renderer agrees on the principle —
`sourcelib.render_card` reports `media_in_card: null` and records the photo
under `media_rejected`; it never paints a post's image.

**What the card still does, in full:** it is the REAL post, on X's own frame,
with the real handle `@XFREEZE`, the post's own three lines, and ONE marker fill
on the line that carries the claim — `so I asked Grok Build to investigate` —
landing on the cue word *like* at 3.24 s. LAW 37 is answered, not waived; GLOBAL
LAW 3 holds (2.70–6.56 s = 3.86 s, and no likes, reposts or views anywhere).

**What I would have done instead:** if the capture had put the verdict and the
metric row together, I would have pasted the scoped crop inside the card and
zoomed it exactly as the plan describes.

## 3. THE CARD IS RENDERED BY THIS LANE, NOT BY `sourcelib.render_card`

`sourcelib._render` **refuses** a shipped body that is not a byte-identical
PREFIX of the post text. The plan's `open_questions[2]` elides the post's first
clause with the post's own ellipsis (*"...nearly cooking my balls"* is off-brand
for a channel that ships to YouTube, TikTok and Instagram every day), and an
elision is not a prefix — so building the plan means rendering the card here.
The renderer is `gen/_pcoverheat_wb_card.py`: a LOCAL `file://` page, no
live-site automation, the claim line's ink box measured with per-character
Ranges off the real DOM (sourcelib's own method, never a union box and never a
guess), ASCII asserted, every kept word checked against the fetched post, and
the full post text plus every dropped fragment recorded in
`gen/_wb_assets/card_pcoverheat_wb.json`. It also wears the GRAPHIC CHART rather
than the DOM chassis' Poppins-on-white card, which is what the plan asks the
whiteboard for: cream `#FFFDF9`, a 3 px ink-alpha border at radius 18, the X
mark in INK beside `@XFREEZE` in JetBrains Mono uppercase, a hairline, then the
post's own words in JetBrains Mono 400.

The header reads `@XFREEZE` beside the X mark, not the plan's literal
`@XFREEZE - X`: the mark already says which platform, and the script says *on X*
0.9 s later. Nothing else about the header changed.

## 4. THE OUTRO CARRIES NO COOL LAPTOP

**The plan** (beat 8, `outro-laptop-cool`): the chassis lockup sits on the
video's own themed object — the laptop again, small, in ink line, with no heat
waves.

**The law that forbids it:** `whiteboard_build.assert_outro_clear` refuses any
ink authored at or after the outro anchor (*"Nothing may be drawn into the
region the handle card occupies"*), and the outro itself is authored by the
shared harness `outro_block()` — an OPAQUE, full-zone cream sheet that rises
over the board carrying the terracotta rule, the mono `@migueltorrez.ai` and
`daily AI`. It takes no glyph parameter, and my brief forbids forking the
harness. Painting the laptop into the board SVG cannot work either: the sheet is
opaque by construction, which is exactly why round 1's double-exposure defect is
impossible.

This is a harness limitation to raise with the format owner, not a per-video
fix. Every approved whiteboard this factory has shipped carries this same outro.

## 5. THE BOARD'S GEOMETRY IS ITS OWN, and the plan's `canvas_rects` are not

The plan's rects were authored for the split/cutout's shared 1080x600 core. The
whiteboard is a third layout — a 576x460 board whose legal surface is
x 40..536 / y 150..425 — so every rect here is authored and asserted here, as
the plan's own `per_lane_notes.whiteboard_reels` expects (*"it redraws THIS
ARGUMENT as marker ink on its own 576x460 board"*). The plan's four chapters,
its beat order, its labels and their above/below placement, its lifetimes, its
one connector, its blocks and its two emphasis KINDS are built exactly as
written.

## 6. THREE TIMES WERE MOVED, AND EACH MOVE IS A LAW

* **`CLAUDE COWORK` is written at 9.98, not 9.72.** GLOBAL LAW 4, enforced as
  `caption_identity_guard`: the pill **`Claude Cowork,`** is alive 9.14–9.94 and
  the identical board word at 9.72 would share every frame of it. 9.98 is still
  0.84 s from its spoken word, inside `LABEL_WINDOW`.
* **`TELL THEM` is written at 15.42, not 15.30.** The same law: the pill
  `tell them,` is alive 14.84–15.38.
* **The speech bubble completes at 14.11, not 14.25.** LAW 45 is a FRAME COUNT:
  `seam_check.PERSIST_FRAMES` = 3, landing is claimed from the FIRST of three
  consecutive qualifying frames, and that frame must fall inside 0.30 s of the
  erase completing at 13.95. The plan's own arithmetic (13.99–14.25) puts the
  first qualifying frame at 14.28 and the seam reads DEAD. The entrance keeps
  the plan's start on the plan's own word; only the draw is shortened.

## 7. THE COLUMNS ARE THE LIST'S OWN CONTENT, not three registered marks

The plan's `lifetimes` name `col-hot` / `col-ram` / `col-cpu` as marks. On this
board the three columns are cells of the window the viewer is already reading,
so they are drawn ink inside a declared container rather than three more rigids
in the registry — which is what `canvas_rects_note` and the plan's own beat 5
describe (*"three COLUMNS of the same table"*). `HOT`, `RAM` and `CPU` are
written inside the window's header band under LAW 39's carve-out, exactly as the
plan's `labels` and `open_questions[5]` require for `PROCESSES`.

## 8. WHAT THE COLD READERS MADE ME REDRAW

Two redesign rounds, both on the objects the artwork seal itself carried at 3 of
6 sure, and both recorded in `review/phone_scores_pcoverheat_whiteboard.json`
with every read:

* the download arrow was first drawn at **half** the sealed footprint, then with
  a chevron head; it ships as the canonical solid glyph;
* the process list's window frame was cold-tested at five weights because the
  decisive reader family kept naming its CONTAINER (`computer monitor`) — the
  exact defect the artwork author threw a whole list drawing away for. At the
  shipped weight (3.4 u on a narrowed 288 u window with a 4 u corner) that
  family says `system monitor` and the other says `task manager process list`.

Across all six sealed rounds, 24 reads, **no reader ever named a different
object.**
