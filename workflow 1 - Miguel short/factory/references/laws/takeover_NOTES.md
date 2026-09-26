# Fix round 6 — `takeover_fix6.mp4` (2026-08-31, task id `takeover6`)

**The closing captions round.** One goal across every definitive format: the
IDENTICAL caption specification. Two changes here, both about the pill, and
nothing else in the picture moves.

```
out/takeover_fix6.mp4   pill 56.2px / 18.8x33.8 pad / 22.5 radius / #C4573A
                        pill height 114.59px authored, 116px measured
                        seat 1318 unchanged -> pill 1260.7-1375.3, bottom 71.63%
                        58 phrases, 0 split, widest pill 714.6px of a 756px seat
                        every changed pixel in rows 1260-1375. Nothing else.
```
Staged to `~/Movies/Shorts Factory/Format Lab/Fixed6/takeover_fix6.mp4`.

## 1. The shrink formula is dead — and it was already inert

`cap_font` carried the published factory's length-based sizing:

```python
round(max(35.6, min(56.25, 1578.3 / len(text))), 1)
```

That makes the pill a variable-size object, which is a second type size in the
same video. It is gone. There is ONE size, `P.CAP_FONT = 56.2px` — px(30) in the
published 576-wide design space times the factory's S = 1.875 — and a phrase too
wide for its seat is SPLIT at a word boundary, never squeezed.

Round 6 does not *assert* that nothing was being shrunk here, it proves it two
ways:

* **Algebraically.** `build_captions` closes a group the moment the next word
  would push the width estimate past the 756px seat. `len * 0.575 * 56.2 + 67.6
  <= 756` breaks at **21 characters**; the formula only starts shrinking past
  **28**. The shrink branch was unreachable.
* **In pixels.** Round 5's render measures a single type size across 134
  captioned frames (x-height band spread 2px; exact pill height spread 0px).

So the approved round-5 caption track survives this round **byte-for-byte** —
all 58 caption clips are set-identical between the two `index.html` files, same
text, same in/out times. The splitter logged **0 splits**, with the widest pill
measured at **714.6px against a 756px seat** (41.4px of headroom).

That is the right outcome, not a missed one: Miguel approved this phrasing, and
the round was asked to change the type SPEC, not his words.

## 2. The splitter is real even though it fired zero times

`split_phrases()` measures every finished phrase as a rendered pill and, if one
misses the seat, cuts it at word boundaries into as many beats as it takes,
handing each beat the transcript's own word timestamps rather than interpolating
them. A single word too wide to split fails the build instead of being shrunk.
The mechanism is the guarantee; the zero is the measurement.

Phrases now carry the word list they were built from (`p["words"]`), which is
what makes an honest split possible at all.

## 3. The pill is now the canonical pill

Round 5 shipped a near-copy of the published geometry. The two, side by side:

| property | round 5 | published (canonical) | round 6 |
|---|---|---|---|
| font-size | 56.2px (inline only) | 56.2px = px(30) | 56.2px, CSS **and** inline |
| padding | 19px 34px | 18.8px 33.8px = px(10) px(18) | 18.8px 33.8px |
| border-radius | 22px | 22.5px = px(12) | 22.5px |
| background | #C4573A | #C4573A | #C4573A |
| family / weight | Nunito 800 | Nunito 800 | Nunito 800 |

Source of truth: `pipeline/build_hyperframes_r2.py` (`.scappill`, authored in
576-wide units) and `shorts_run8/projects/mcpupgrade_icon/index.html` (the same
CSS after the 1.875 scale, read off a published video).

The numbers now live in **`takeover_fix6_pill.py`** and are imported, never
retyped — so any format importing that module is pill-identical by construction.

**Pill height 114.59px** = 56.2px Nunito 800 at `line-height: normal` (78.99px
content box) + 2 x 18.8px padding. At the unchanged seat `CAP_Y = 1318` (the
pill's CENTRE, because of `translateY(-50%)`) the pill occupies **1260.7 -
1375.3**, bottom **71.63%** of frame height — inside LAW 12's 72%. **THE SEAT
DID NOT MOVE.**

## 4. Measuring the pill instead of estimating it

Every generator in the lab estimates pill width as `len * 0.575 * font + pad`.
Measured against all 58 rendered pills of fix5, that estimate runs **0.71-1.00**
of the truth (mean 0.86). It is a bound, not a measurement, so it cannot answer
"did this pill actually fit".

`takeover_fix6_pill.PillMeasurer` lays the pill out in headless Chromium with
the real Nunito 800 webfont at 56.2px and caches the result to
`_pillwidths_fix6.json`. Validated against the decoded TERRA span of all 58
pills in the finished fix5 MP4: **delta -2.6 .. +1.3px, mean -0.7px** (the
antialiased rounded ends read a hair narrow in pixels). The model IS the
renderer, so LAW 12's horizontal clause is now judged on a measurement.

The estimate stays as the CHUNKER's rule, deliberately: it is conservative by
construction, and keeping it is what makes the approved caption text survive.

## 5. Verified, not trusted

`takeover_fix6_check.py` — **ALL CHECKS PASS**. The caption readings, all
decoded out of the finished MP4:

```
x-height band      [26, 27, 28]px over 134 captioned frames   spread 2px
exact pill height  [116]px over 64 dark-ground frames         spread 0px
pill bottom        [1375]px                     (LAW 12 limit 1382)
pill width         276 .. 712px                 (seat budget 756)
pill centre x      539.5 .. 540.0               (frame centre 540)
```

One size, zero drift. **Pill height for the cross-format audit: 114.59px
authored / 116px measured** (the extra row is the antialiased top and bottom
edge; it reads the same in fix5, so the 0.4px padding change does not move the
integer row count).

## 6. Containment — and why the obvious diff is a lie

The first containment pass diffed the decoded pixels of `takeover_fix5.mp4`
against `takeover_fix6.mp4` and reported **98.9% of the frame changed, bbox rows
0-1919**. That reading is worthless, and the control proves it: re-rendering
**fix5 against its own unmodified project** produces the same picture —

| | mean delta | "significant" (>24) pixels | rows | frames w/ ink outside band |
|---|---|---|---|---|
| fix5 vs **fix6** | 0.704 | 21.87% | 199-1387 | 1156 |
| fix5 vs **fix5 re-rendered** | 0.694 | 21.57% | 199-1379 | 1158 |

H.264 is lossy and rate-controlled: changing one region re-allocates bits across
the whole frame, and two encodes of *identical* content already differ by this
much. **A decoded-pixel diff of two separate encodes cannot isolate a content
change.**

The honest instrument is a lossless one. Both projects were snapshot to PNG at
17 timestamps spanning the video and diffed exactly:

```
17 pairs, byte-exact comparison
every differing pixel:  rows 1260 .. 1375   (65.6% .. 71.6% of H)
                        cols inside the pill's own width, every frame
changed pixels/frame:   804 .. 1456  of 2,073,600   (0.04% .. 0.07%)
nothing above row 1260, nothing below row 1375
```

**Diff geography: the caption pill's own rows, and nothing else.** The changed
pixels are the pill's rounded ends and its 0.4px-narrower edges — the geometry
correction, exactly and only.

The HTML says the same thing: outside the caption clips, `takeover_fix6/
index.html` differs from `takeover_fix5/index.html` in **two places** — the
`<title>` and the `.scappill` rule.

## What fought me

* **A pixel diff of two encodes is not a pixel diff of two pictures.** The
  98.9% reading looked like a catastrophic regression and was pure rate-control
  noise. The fix is not a threshold — it is a CONTROL (render the unchanged
  project twice) plus a lossless comparison. Any future "only X may differ"
  claim needs both.
* **A dead formula still has to be killed.** The temptation was to leave
  `cap_font` alone because it never fired. But an inert shrink is one
  transcript away from firing, and the point of the round is that the size is
  not a function of anything.
* **The conservative estimate is a feature, not a bug — but only for the
  chunker.** Switching the chunker to measured widths was tried and rejected:
  it re-chunks 48 of 58 phrases to save 2 beats, i.e. it rewrites Miguel's
  approved caption track for nothing. The measurement belongs on the GUARD.
* **`translateY(-50%)` means the seat is the pill's CENTRE**, not its top. Every
  bottom-of-pill number in this format derives from that.

## Not touched

The 21/79 face/illustration balance, the growing beat curve, the seven
compositions centred on 629, the RAW 0% full-bleed face with zero punches, the
SFX schedule and gains, the ghost rule, 25fps, the palette, every scene interior
and every content beat. `takeover_fix5_*.py` are unmodified, so fix5 still
reproduces.

## Files

```
takeover_fix6_pill.py      THE CANONICAL PILL — spec constants + Chromium measurer + splitter
takeover_fix6_core.py      chassis copy: CAP_FONT constant, canonical CSS, split_phrases()
takeover_fix6_gen.py       generator: splitter wired in, LAW 12 judged on measured widths
takeover_fix6_check.py     self-check + ROUND 6 pill readings in the finished pixels
takeover_fix6_contain.py   decoded-pixel containment diff (with the noise threshold + control)
takeover_fix6/             HyperFrames project (assets -> stage_fix6)
stage_fix6/                face plate carried over from stage_fix5, digest asserted
out/takeover_fix6.mp4      the render
_report_takeover_fix6.json round6_caption_spec block: the deliverable numbers
_check_takeover_fix6.json  round6_pill block: the measured numbers
_pillwidths_fix6.json      cached Chromium pill widths (deterministic rebuilds, offline)
_contain_lossless_fix5_vs_fix6.json   the containment proof
_contain_fix5_vs_fix6.json / _contain_control_fix5_vs_fix5.json   treatment + control
logs/render_fix6.log  logs/check_fix6.log  logs/contain_fix6.log
```

---

# Fix round 5 — `takeover_fix5.mp4` (2026-08-31, task id `takeover5`)

Round 5 brief: **one change.** Miguel: *centre the illustrations in the space
above the captions.* The caption seat does not move — round 4 put the pill at
1258-1378, bottom **71.6%** of frame height, and 72% is the platform-safety
limit, so it cannot go lower. Everything else is inherited from fix round 4
untouched: the 20.7/79.3 balance, the growing beat curve, the RAW 0% full-bleed
face with zero punches, the tamed SFX palette at its pinned class gains, the
fixed lemniscate, 25fps, the palette, the scene interiors, every content beat.

```
out/takeover_fix5.mp4   7 compositions, all seated on 629 (worst error 0.5px)
                        worst margin imbalance 1.0px   (fix4: 167px)
                        caption seat, balance, cuts, SFX, mix: UNCHANGED
```
Staged to `~/Movies/Shorts Factory/Format Lab/Fixed5/takeover_fix5.mp4`.

## 1. The region — and the 75px that were never there

An illustration owns everything above the pill: **[0, 1258), centre 629**.

Every round up to 4 seated its scenes on `C.MID = 704`, the centre of the LAW 12
*content band* [192, 1214] — the region minus the top-10% platform strip minus
44px of clearance above the pill. Those two subtractions are not symmetric, so
the band's centre sits **75px below the region's**, and a picture centred in the
band is a picture pushed down onto the captions.

Measured, not asserted. `takeover_fix5_centroid.py` decodes every frame of a
unit at native 1080x1920, takes each section's ground as its modal luma, calls
everything more than 18 levels away from it ink, and reports the empty ground
above and below the picture:

| unit | fix4 above/below | fix4 optical centre | fix5 above/below | fix5 optical centre |
|---|---|---|---|---|
| flash | 568 / 429 | 698.5 | 499 / 498 | **629.5** |
| toolwall | 300 / **143** | 707.5 | 222 / 221 | **629.5** |
| term card | 588 / 421 | 712.5 | 505 / 505 | **629.0** |
| ON DEMAND field | 289 / **168** | 689.5 | 229 / 228 | **629.5** |
| finite | 402 / 245 | 707.5 | 324 / 323 | **629.5** |
| portal | 231 / 211 | 639.0 | 221 / 221 | **629.0** |
| outro card | 389 / 274 | 686.5 | 332 / 331 | **629.5** |

Six of the seven carried roughly **twice** the empty ground above them as below.
That is Miguel's note, stated in pixels. Worst offset from the region centre
goes 83.5px -> **0.5px**; worst margin imbalance 167px -> **1.0px**.

## 2. Why the seat is NOT driven by the ink-mass centroid

Round 5 asked for a measured vertical centroid, and the instrument reports one —
but the measurement itself shows the ink-mass centroid is the wrong ruler:

```
outro card    ink spans 389-991 (centre 690)     ink MASS at 812   gap 122px
finite        ink spans 402-1013 (centre 708)    ink MASS at 792   gap  84px
```

The outro's 122px gap is one element: the solid INK `@migueltorrezai` chip, the
only filled black shape on a cream card. Equalising ink mass would have driven
the card 122px too high and left a 450px hole under it — trading the complaint
for its mirror image. So the seat is driven by `optical_centre`, the
median-per-frame ink bounding-box midpoint, which is what equalises the
whitespace an eye actually reads. Both numbers are reported before and after
(`_centroid_before_fix4.json`, `_centroid_after_fix5.json`).

## 3. The seats are derived, never typed

`takeover_fix5_core.py` makes the vertical seat a per-scene parameter (`mid`,
plus `mid_field` for the term takeover — ONE takeover but TWO pictures either
side of its internal hard cut, 249px of cream type and then an 800px dark field;
they cannot share a seat). `C.MID` survives as the default, so fix4's geometry
still reproduces through the same functions.

The generator reads the baseline measurement and computes

```
seat = 704 (what fix4 used) - (that unit's measured offset from 629)
```

| unit | seat | moved up |
|---|---|---|
| flash | 634.5 | 69.5px |
| toolwall | 625.5 | 78.5px |
| term card | 620.5 | 83.5px |
| ON DEMAND field | 643.5 | 60.5px |
| finite | 625.5 | 78.5px |
| portal | 694.0 | 10.0px |
| outro card | 646.5 | 57.5px |

A translation moves an optical centre by exactly the translation, so one pass
lands every unit on 629 — and the check re-measures the finished MP4 rather than
assuming it. **The portal only needed 10px**: `pcy = mid - 40` plus its
asymmetric mark-above/rail-below structure already had it near centre, which is
also why nothing had to be shrunk to keep its in-flight feed out of the top 10%
(narrowest clearance after the move: y=199, 7px inside the line).

Guards added in `audit()`: seven seats must be declared and reach their scene,
none may fall back to `C.MID`, and none may be quantised — a seat is a
COORDINATE, and fix4's `fq()` sweep would have snapped 634.5 onto the 25fps grid
and silently reseated the video. `TIME_KW` now names the kwargs that are times.

## 4. What did NOT change — proven, not claimed

Both index.html files were diffed with every numeric literal replaced by `#`:

```
structural diff after stripping ALL numbers:      0 lines
timing / duration / volume / SFX / font-size:     1151 tokens, IDENTICAL
visible text nodes:                               70, IDENTICAL
horizontal coordinates:                           IDENTICAL
vertical coordinates:  moved by exactly one of
   -83.5  -78.5  -69.5  -60.5  -57.5  -10.0  0.0   (the seven measured offsets)
```

And on the finished files: the decoded audio of fix4 and fix5 is **bit-identical**
(sha256 `a5298144…` both) — voice, bed and all 18 SFX untouched. The face plate
is carried over from fix4's stage with its sha256 asserted both ways.

## 5. LAW: ONE caption type size, measured on rendered glyphs

New this round, and deliberately not read off the generator. Two readings, after
two rejected ones:

* the glyph **bounding box** is content-dependent, not size-dependent — it lands
  in two clusters, 41-42px for a phrase with neither cap nor descender and
  50-52px for one with both. Asserting on it fails a video whose type never
  changed. Reported, never asserted.
* `pill_box()`'s height wobbles 112-116px. Checked against pill width, ground
  and phrase: it correlates with none of them. It is the per-row TERRA test
  meeting a rounded cap and antialiasing at the pill's edge — an artefact.

What is content-independent and linear in font size:

```
X-HEIGHT BAND      rows holding >= half the peak glyph ink, inset past the
                   rounded ends and the antialiased edge
                   26-28px over 134 captioned frames        spread 2px
EXACT PILL HEIGHT  dark-ground frames only, where the pill's mask is exactly
                   "not the ground" and no threshold is involved
                   116px over 64 frames                     spread 0px
```

Cream sections are excluded from the exact reading on purpose: a white glyph on
cream is within a hair of the ground and the run breaks mid-pill. **64 of 64
dark-ground samples measure exactly 116px.** One type size, proven on pixels.

## 6. Everything else, re-verified on the render

```
container      1080x1920  25/1  1351 frames  54.04s
LAW 12 pill    top 1260-1262  bottom 1373-1375 = 71.6% of H  seat stable
               x 184-895 = 82.9% of W        widest pill 712px
LAW 12 content every settled scene inside 192-1214 and 162-918
no zoom        face_frac 0.410-0.430 on the 0.430 standard; every face frame
               within 2.80 of the RAW 0% plate, 6.1-6.9x closer than to a 5% punch
no punches     8 frame pairs inside the four face runs, picture unchanged
ghost rule     0/576 TERRA_2 px at (477, 654) on all four pre-draw samples
balance        face 11.20s / 20.7%   illustration 42.84s / 79.3%   4 runs
picture changes 10, matching the authored map, 5.1x clear of the loudest motion
mix            speech margin 20.77 dB
ALL CHECKS PASS
```

Contact sheet (fix4 above, fix5 below, magenta = 629, cyan = pill top):
`out/_contact_fix4_vs_fix5.png`.

## Files

```
takeover_fix5_centroid.py   the instrument (before + after)
takeover_fix5_core.py       chassis: the seat is a per-scene parameter
takeover_fix5_gen.py        seats derived from the baseline + round-5 guards
takeover_fix5_check.py      seats + type law re-measured on the MP4
_centroid_before_fix4.json  _centroid_after_fix5.json
_report_takeover_fix5.json  _check_takeover_fix5.json
```

---

# Fix round 4 — `takeover_fix4.mp4` (2026-08-30, task id `takeover4`)

Round 4 brief: **one change.** Miguel: *"I would rather have more time for the
illustrations than my face, they're more important... maybe a 25/75 split."*
Two guards agreed with it — the HOOK stays his face, and ONE short face return
(~2s) lands before the final line. Everything else is inherited from fix round 3
untouched: RAW 0% full-bleed face with zero punches, the LAW 12 caption seat, the
tamed SFX palette at its pinned class gains, the fixed lemniscate, 25fps, the
palette, the scene interiors, every approved content beat.

```
out/takeover_fix4.mp4   face 11.20s / 20.7%   illustration 42.84s / 79.3%
                        (fix3: 24.28s / 44.9%  and  29.76s / 55.1%)
                        6 takeovers  10 picture changes (fix3: 13, fix2: 33)
                        4 face runs (fix3: 6)  longest 6.20s (fix3: 6.32s)
                        beats 1.64 -> 2.40 -> 6.80 -> 9.72 -> 19.00, coda 3.28
```
Staged to `~/Movies/Shorts Factory/Format Lab/Fixed4/takeover_fix4.mp4`.

## 1. The balance — 20.7 / 79.3, and why not 25.0 / 75.0

The two guards bound the answer arithmetically, so the number was derived rather
than chosen. The term card must debut at 13.20 (its approved seat: it lands on
*"What does that mean?"* so the plate never carries the words the pill is
carrying, LAW 4), which makes the hook block 0.00-13.20. That block contains the
format's two hook illustrations, the flash and the toolwall:

```
hook face   = 13.20 - 1.64 (flash) - 2.40 (toolwall) = 9.16s
return face = 2.04s   ("which is just unbelievable", 48.72-50.76)
face total  = 11.20s = 20.7% of 54.04
```

**20.7% is the ceiling under the guards, not a preference.** Landing exactly on
25.0% needs 13.51s of face — 2.3s more — and there are only three places to find
it, all of them forbidden by this round's own brief:

| where the 2.3s could come from | why not |
|---|---|
| a third face beat mid-video | *"between those, the illustrations own the video"* |
| a ~4s return instead of ~2s | the return is specified as ~2s |
| drop the toolwall takeover, hook face runs 3.16-13.20 in one 10.06s block | lands on **25.2%** — and deletes an approved scene; *"everything content-level is approved"* |

The brief's direction is MORE illustration, so the ceiling is the right side of
25% to miss on. The third row is the one to reach for if Miguel wants the exact
number: it is a one-line change to the cut map and it costs the toolwall.

Measured off the finished MP4, not off the cut map — every frame of the render
and of `face_z00.mp4` decoded at 135x240 and differenced:

```
  face frames         differ from the plate by at most   2.67
  illustration frames differ from the plate by at least  82.39     31x apart
  face      11.20s  20.7%      runs 1.52 / 1.44 / 6.20 / 2.04
  illustr.  42.84s  79.3%      longest face run 6.20s
```

## 2. Where the reclaimed 13.08s went — scenes, not stillness

Four face runs were deleted (fix3's 6.20s, 2.86s, 5.98s and 6.32s runs became
two). The brief's clause was *"extend the approved takeover scenes... let each
scene breathe and complete its motion arc rather than padding with stillness"*,
and three of the six scenes had a motion arc sized for a takeover under 2s. They
now derive their pacing from the span they are handed (`takeover_fix4_core.py`):

| scene | fix3 | fix4 | what the extra seconds do |
|---|---|---|---|
| term / ON DEMAND | 3.94s | **6.80s** | the field answers **4** times at 1.17s apart, not 3 at 0.62s — the request/answer exchange is legible instead of a flicker |
| finite | 5.94s | **9.72s** | the stack climbs for 2.62s and hits its ceiling ON *"finite"* (22.68 vs the word at 22.36-22.76); the picky DRAIN then falls **top row first** over 4.39s, resolving under *"give access to your AI agent"* |
| portal | 8.66s | **19.00s** | opens ON *"the people over at Nous Research"* (fix3 opened 2.22s late), 7 waves of radial traffic, the lemniscate resolves at 38.28, then a SECOND phase of traffic marches through the same door from the left |

Nothing was padded: measured on the render, the only holds longer than 1.5s are
the 1.7s after the infinity resolves (the payoff line, *"and we no longer have to
worry about that"*) and the 1.3s the finite vessel sits on its four keepers.

The ON DEMAND count and the drain stagger are DERIVED, not typed —
`ondemand_lit()` returns 3 plates at fix3's 2.10s span and 4 at fix4's 4.96s, so
the short-takeover behaviour still reproduces exactly.

## 3. The two portals had to become one — found by measuring, not by looking

Round 4's first pass gave the give-up beat its own takeover at 40.60, and the
cut detector said the picture did not change there:

```
  frame-to-frame jump at every real cut   82 .. 193
  frame-to-frame jump at 40.60             1.36
```

Two portals back to back tear the same door down and rebuild it: `sc_portal`
re-pops the Nous mark, re-grows the stem and REDRAWS the ring, on a frame whose
picture is already that exact object. So the "cut" was invisible — and it was
carrying a seize whoosh AND a low_thump, i.e. two SFX scoring a frame with no
visual event, which is precisely what SFX LAW v2 forbids.

Fix: `sc_portal` gained `stack=(from, to, waves)` — a second traffic PHASE
through the same door. Nothing rebuilds, the door stays open for 19s, and the
reading is better than the cut was: first the world's tools arrive radially and
pass through, then the infinity resolves, then his own MCP servers march through
the same opening in a stack while the context rail never moves off its sliver.
With `stack=None` the function is byte-identical to fix3's.

Second defect from the same measurement: the outro's first frame. `cut_on` is a
0.03s `fromTo`, so a card authored at the clip boundary paints one frame LATE —
50.76 rendered as the section's bare INK_2 ground and 50.80 as the cream card, a
one-frame dark flash between his face and the outro. The outro section's ground
is now CREAM (fix3's outro opened on an INK_2 prelude; fix4's opens on the card),
so the frame that used to flash is the card's own colour.

## 4. Pacing — Morgane's note, answered a second time

```
cut times  1.52 3.16 4.60 7.00 13.20 15.20 20.00 29.72 48.72 50.76
gaps       1.64 1.44 2.40 6.20  2.00  4.80  9.72 19.00  2.04
magnitudes 85.4 85.0 90.1 92.2 135.5 189.1 191.8 192.9  82.2 139.6
```
10 picture changes in 54.04s, against fix3's 13 and fix2's 33 — *"limite toutes
les secondes"* is now a 5.4s average gap. The count is measured, not asserted:
the smallest cut (82.2) is **5.1x** the loudest non-cut frame in the whole video
(16.13, his head moving on the face plate), so the detector is reading cuts and
not a threshold artefact.

SFX follows: 18 hits, down from 20. A release (`reverse_air`) now fires only
where the frame actually goes back to HIM — 3 releases, at 3.16, 7.00 and 48.72 —
because the other takeover exits are handovers to another takeover whose seize
whoosh already owns that frame. The three `low_thump`s still mark the three
longest takeovers' entrances (13.20, 20.00, 29.72). Speech margin **20.77 dB**
against fix3's 20.78: the mix did not move.

## 5. Proof

`takeover_fix4_check.py` decodes the finished MP4. **ALL CHECKS PASS.**

* container 1080x1920, `25/1`, 1351 frames, 54.04s;
* full bleed — top-12-row variance 4.92-5.16 on every face sample;
* NO ZOOM — face_frac 0.409-0.430 against the 0.430 standard, and the pixel
  proof: 2.74-2.86 against the plate 1:1 vs 16.81-18.59 against a 5% punch,
  6.0-6.8x;
* NO PUNCHES — 8 adjacent-frame pairs inside the four face runs, both frames of
  every pair within 2.88 of the plate. (The landmark ratio is printed but NOT
  asserted: it reads 1.035 on a pair the pixels prove identical — round 3's
  learning, that a landmark measure cannot prove a negative, applied here);
* LAW 12 caption — 134 samples, one seat, bottom 71.6%, x 184-895, widest 712px,
  centre stable to 1px across the whole video;
* LAW 12 content — all seven settled takeover frames inside 192-1214 / 162-918;
* ghost rule — 0 TERRA_2 px in the 24x24 box at (477, 664) at 30.50 / 33.50 /
  35.00 / 37.00, the four pre-draw samples of the video's one lemniscate;
* BALANCE — 20.7 / 79.3, 4 face runs, longest 6.20s, classes 31x apart;
* PACING — 10 cuts, all within one frame of the authored map, 5.1x separation;
* mix — speech margin 20.77 dB.

## What fought me

* **The rebalance is not a cut-map edit, it is a pacing problem.** Deleting four
  face runs is one line. Handing the 13.08s to scenes that finish moving in under
  two seconds produces six held pictures, which is LAW 16 with extra steps. Every
  scene that grew needed its arc re-derived from its span, and the two scenes
  that could not grow (flash, toolwall) had to stay exactly where they were.
* **A cut you cannot see is worse than a cut you did not make.** The 40.60
  handover looked fine in the cut map, sounded fine in the SFX schedule, and was
  invisible on the render. It took a frame-to-frame difference sweep of all 1351
  frames to catch it — the same class of instrument round 3 needed to prove the
  face was not punched. **Measure picture CHANGE, not picture content.**
* **`cut_on` lands one frame after the clip boundary.** A 0.03s `fromTo` starting
  at t paints nothing at t. Harmless inside a section (fix3 always had something
  underneath); a one-frame flash when the element IS the section. The general
  rule for this chassis: a section's ground must be the colour of whatever cuts
  on at its first frame.
* **The 25% could not be hit without breaking a guard, and that is a finding,
  not a failure.** Writing the arithmetic down (section 1) was more useful than
  quietly landing on 20.7 and calling it "~25".

## Not touched

`takeover_core.py`, `takeover_fix2_core.py` and `takeover_fix3_core.py` are
unmodified, so v1/v2/v3, `takeover_fix`, `takeover_fix2` and `takeover_fix3`
still reproduce byte-for-byte. The scene interiors, the palette, the caption text
pipeline, the SFX palette and class gains, the ghost rule, LAW 11 fills, LAW 12
geometry and the 25fps de-conform are all inherited unchanged.

## Files

```
takeover_fix4_core.py      chassis copy + span-derived pacing (term / finite / portal phase 2)
takeover_fix4_gen.py       generator: the round-4 cut map, derived waves, release-only-to-face SFX
takeover_fix4_check.py     self-check: + measured balance and measured cut count
takeover_fix4/             HyperFrames project (assets -> stage_fix4)
stage_fix4/v/face_z00.mp4  the RAW 0% plate, full-bleed 1080x1920 @ 25/1
out/takeover_fix4.mp4      the render
out/frames_fix4/           decoded self-check frames + _sheet_fix4.png (portal handover, outro)
_report_takeover_fix4.json cut map, beats, balance, law12 budget, pacing, ghost, SFX
_check_takeover_fix4.json  the measured numbers above
logs/render_fix4.log  logs/check_fix4.log
```

---

# Fix round 3 — `takeover_fix3.mp4` (2026-08-30, task id `takeover3`)

Round 3 brief: **three changes, nothing else.** The face becomes the RAW 0%
crop and stays there, the caption moves into the platform-safe band, and
Morgane's pacing note is judged rather than obeyed. The growing shape, the six
scenes and their interiors, the palette, the tamed SFX palette at its pinned
class gains and the fixed lemniscate are all carried over from fix round 2.

```
out/takeover_fix3.mp4   RAW 0% face, ZERO punches, 25fps
                        6 takeovers  29.76s  55.1% of frame time
                        beats 1.64 -> 2.40 -> 3.96 -> 5.96 -> 8.68  (+7.12 coda)
                        13 cuts in 54.04s (fix2: 33)   caption pill bottom 71.6%
```
Staged to `~/Movies/Shorts Factory/Format Lab/Fixed3/takeover_fix3.mp4`.

## 1. The face — one plate, and no way to add a second

Miguel: *"ZOOM DROPPED until the new lens. No virtual set, no matte-on-ground,
no blur-pad: full-face = the regular RAW 0% crop, punches deferred."*

fix2 shipped a three-rung ladder (0/5/10%) and 20 crop cuts. fix3 builds ONE
plate — `crop=1216:2160:1270:0` scaled to 1080x1920, the 0% window of
`_shared/ZOOM_STANDARD.md` — and shows it for all 24.28s of face time. The
level is no longer a table anyone can edit: it is DERIVED from the face runs,
and four build guards make a punch unrepresentable rather than merely absent —
exactly one `fw-` window may exist, it must be the full-bleed 0% frame, only
one `<video>` element may be authored, and its source must be `face_z00.mp4`.

**Proving a negative needed a better instrument than round 2's.** MediaPipe's
`face_frac` wobbles ~2% on head tilt alone: the eight frames where fix2 used to
cut measure ratios of 0.997-1.021 in fix3 even though the picture is provably
untouched, and one sample (t=43.00, 0.393) sits outside the 0% standard's
absolute tolerance for the same reason. Landmarks cannot police "no change".
Pixels can. Each face frame is now differenced against `face_z00.mp4` at the
same timestamp:

```
                         vs the plate 1:1     vs the plate at 5%
  8 face samples         2.74 - 2.88          16.68 - 18.23        6.1-6.3x
```
2.8 is h264 re-encode noise. A 5% punch — the *smallest* fix2 ever used — is
six times further away. The render IS the RAW 0% plate.

## 2. GLOBAL LAW 12 — the caption, measured against the real platforms

fix2's pill was decoded off the finished MP4 across 106 samples: **1454-1569,
bottom 81.7% of frame height, widest instance x 112-967 = 89.5% of width.**
TikTok's creator block starts at 75% and its right rail owns x>85% from y
34-82%. The caption was underneath both, on both axes.

fix3 measured over 134 samples of the whole 54s:

| | fix2 | **fix3** | law |
|---|---|---|---|
| pill top | 1454-1464 | **1260-1262** | — |
| pill BOTTOM | 1559-1569 (**81.7%**) | **1374-1375 (71.6%)** | <= 72% / 1382 |
| pill centre | 78.7% | **68.6-68.7%** | one stable seat |
| pill x | 112-967 (**89.5%**) | **184-895 (82.9%)** | inside 162-918 |
| widest pill | 856px | **712px** | <= 756px |

The centre varies by 1px across the entire video (anti-aliasing on the pill's
cap), so the seat is stable across face and takeover alike — Morgane's "not a
fan of the captions drastically changing position between modes" is satisfied by
construction: there is only one `top:` value in the whole document, asserted at
build time.

**Why 68.6% and not the "preferred" 40-65% band.** His RAW 0% face fills the
frame from y=192 to y=1447, and his chin sits at canvas y 1281 (min) / 1381
(median) / 1447 (max) with his mouth ~213px above that (measured from
`_shared/zoom_standard.json`'s 64-frame landmark sweep). Every seat inside
40-65% prints the pill across his MOUTH. 1318 is the highest seat that clears
the platform furniture AND stays off his mouth; going higher would fix a
cosmetic preference by breaking a talking head. Deliberate, documented,
overridable if Miguel disagrees.

**The width fix is a character budget, not a smaller font.** `cap_font`
plateaus at ~908px of ink for anything past 28 characters, so long phrases all
rendered at the same too-wide 856px. Rather than shrink the factory's pill
sizing (and its 35.6px legibility floor), the chunker now closes a caption
group before the next word would push the pill out of the 162-918 column:
52 phrases became 58, max length 21 characters, and the measured widest pill
dropped to 712px. The estimator the guard uses runs ~14% wide of the rendered
pill (975 predicted vs 856 measured on fix2's widest), so the budget is
conservative by construction.

**Everything the takeovers draw was re-seated into what the pill left behind.**
MID 810 -> 704, content band 192-1214. The tool field — the widest object in the
video — was narrowed from 922px to 746px (plate 132->106, gap 26->22) so the
field AND the context rail that shares its width sit inside the safe column;
`PROCEDURAL / DISCLOSURE` dropped 116->104px for the same reason; the portal's
feed ellipse went 820x560 -> 740x400, 740 being the one radius at which no seat
in the 45-degree angle set lands in the dead band between "inside the safe
column" and "off the frame entirely". Measured on the render:

```
  t= 2.40  flash              y  561..935    x  232..841
  t= 6.20  toolwall flooded   y  296..1118   x  160..919
  t=14.20  term on cream      y  584..838    x  192..888
  t=16.60  ON DEMAND field    y  288..1091   x  166..912
  t=23.00  context is finite  y  400..1021   x  190..889
  t=52.00  outro card         y  385..937    x  248..831
```
Nothing in the top 10%, nothing in the bottom 28%, nothing in the right 15%.
The portal's in-flight feed tiles do cross the edges — they enter from
off-frame, which no entrance can avoid — and are reported, not asserted.

## 3. Pacing — Morgane was right, and the punches were the cause

Her note ("limite toutes les secondes") was a watch item, not an order, so it
was measured rather than obeyed. fix2 fired 33 picture changes in 54s: 13
takeover cuts plus 20 crop cuts, and four of the crop cuts landed within half a
second of a takeover entrance (1.12 before the 1.50 entrance; 4.16 before 4.58;
19.24 before 20.00; 44.08 into the 45.36 return). **Dropping the punches removes
every one of them** — fix3 changes the picture 13 times, all of it takeover
punctuation.

With the punches gone the brief's merge-or-lengthen clause fires on nothing:

```
cut times  1.52 3.16 4.60 7.00 13.20 15.16 17.16 20.00 25.96 31.92 40.60 46.92 50.76
gaps       1.64 1.44 2.40 6.20  1.96  2.00  2.84  5.96  5.96  8.68  6.32  3.84
```
Minimum gap **1.44s**; no gap is under a second. The one takeover shorter than
2s is `flash` (1.64s), and it has 1.50s of face before it and 1.44s after it —
lengthening it would have to eat one of those neighbours and CREATE the
sub-second adjacency the note is about. **Nothing merged, nothing lengthened,
by measurement.** Re-judge on the render.

## 4. What the SFX had to do

`low_thump` was spent, in fix2, on crop cuts into the 10% ceiling. Round 3 has
no crop cuts, and an SFX with no visual event under it is precisely what SFX
LAW v2 forbids — so it could not simply stay. It was not deleted either: the
escalation has to stay audible. It is repointed onto the escalation itself, the
entrance of the three LONGEST takeovers (20.00 finite, 31.92 portal, 46.92
outro), layered under the seize whoosh already on that frame. Same palette,
same pinned class gains, 22 hits -> 20. Speech margin measured **20.78 dB**,
against fix2's 20.79 — the mix did not move.

## 5. Proof

`takeover_fix3_check.py` decodes the finished MP4. **ALL CHECKS PASS.**

* container 1080x1920, `25/1`, 1351 frames, 54.04s;
* full bleed — top-12-row variance 4.97-5.17 on every face sample;
* NO ZOOM — face_frac 0.393-0.429 against the 0.430 standard, and the pixel
  proof above (2.8 vs the plate, 16.7-18.2 vs a 5% punch);
* LAW 12 caption — 134 samples, one seat, bottom 71.6%, x 184-895;
* LAW 12 content — the six settled takeovers inside 192-1214 / 162-918;
* ghost rule — 0 TERRA_2 px in the 24x24 box at the lemniscate's new seat
  (477, 664) at 33.50 / 35.00 / 48.50 / 49.80;
* mix — speech margin 20.78 dB.

## What fought me

* **A landmark measure cannot prove a negative.** Round 2 policed a 5% ladder
  with `face_frac` ratios and it worked because the signal was a step. Round 3's
  signal is *no step*, and head tilt alone moves the same measure by 2% — so the
  instrument reported "a punch survived" on a video that has one video element
  and no transform. The fix is to stop measuring the face and start comparing
  pictures: difference the render against the source plate, and against a
  deliberately-punched version of the same plate, and read the ratio.
* **Measuring the caption pill out of the render took three attempts.** The
  first detector merged the toolwall's TERRA context rail (which reaches y=1116)
  into the pill and reported a 275px-tall caption. The second, seeded on the
  pill's own centre row, broke on `See you` — a 276px pill whose white glyphs
  drop the TERRA pixel count below any fixed threshold. The third still cut
  short at t=8.40, where the busiest glyph row is 208 TERRA px inside a 712px
  span, i.e. 29% coverage. What finally works: qualify a row on its TERRA SPAN
  with a 15% coverage floor, then take the LONGEST RUN of qualifying rows and
  require it to be at least 90 rows tall. Worth keeping — every format has to
  measure this pill now.
* **The caption move is not a caption move, it is a re-layout.** Lifting the
  pill by 194px took 22 px off the top of the content band and 186 off the
  bottom, which the toolwall's 970px block did not fit into. Every other scene
  followed from that: the field's plate size, the term's font size, the portal's
  feed radius and stem gap, the outro's centre. A caption law is a layout law.
* **The right-hand 15% is the constraint nobody budgets for.** The vertical
  band gets all the attention, but the tool field was 922px wide and ran to
  x=1001 — 92.7% — straight under every platform's like/comment rail, and so did
  the caption at 967. Both had to shrink. The general rule for this factory:
  **1080-wide content actually has 756 usable pixels**, centred.

## Not touched

`takeover_core.py` and `takeover_fix2_core.py` are unmodified, so v1/v2/v3,
`takeover_fix` and `takeover_fix2` still reproduce byte-for-byte. The cut map,
the scene interiors, the SFX palette and class gains, the caption text pipeline
(other than the width budget), the ghost rule and the 25fps de-conform are all
inherited unchanged.

## Files

```
takeover_fix3_plates.py    builds the ONE 0% plate from the 4K master (25fps, GOP-dense)
takeover_fix3_core.py      chassis copy + LAW 12 geometry (CAP_Y, MID, field, safe column)
takeover_fix3_gen.py       generator: single plate, LAW 12 guards, repointed thumps
takeover_fix3_check.py     self-check: container, pixel proof, LAW 12 sweep, ghost, mix
takeover_fix3/             HyperFrames project (assets -> stage_fix3)
stage_fix3/v/face_z00.mp4  the RAW 0% plate, full-bleed 1080x1920 @ 25/1
out/takeover_fix3.mp4      the render
out/frames_fix3/           the 17 decoded self-check frames
_report_takeover_fix3.json cut map, beats, face levels, law12 budget, pacing, ghost, SFX
_check_takeover_fix3.json  the measured numbers above
logs/plates_fix3.log  logs/render_fix3.log  logs/check_fix3.log
```

---

# TAKEOVER (CUTAWAY) — format lab prototype

Source: `format_lab/hermesinfinite` — the shipped 54.06s cut of *"Hermes Agent
can now have literally infinite tools"*. Three full renders, same video, same
scenes, same palette, same SFX. **The only variable is the cut map.**

```
out/takeover_v1.mp4   SPARSE    3 story takeovers   38% of the frame-time
out/takeover_v2.mp4   DENSE     7 story takeovers   46%
out/takeover_v3.mp4   GROWING   5 story takeovers   55%
```

---

## What the format is

The frame belongs to exactly ONE thing at a time. Miguel full-bleed, or a
full-bleed visual scene. **A split never exists.** When a visual earns it, it
takes the entire frame for a beat while the voice carries, then the frame is
handed back.

Three rules make it work, and all three are load-bearing:

1. **Every entrance and exit is a hard cut on a word boundary.** The generator
   refuses to build if a cut edge is not a Scribe word start or end
   (`build()` → "cut edge is not a word boundary"). No dissolves anywhere.
2. **The visual is already moving when it appears.** Every takeover's interior
   tweens start `LEAD = 0.18s` BEFORE the clip is on screen, so the first
   visible frame is mid-gesture. Cutting to a static pose is the one thing that
   instantly kills the device — it reads as a slide, not a cutaway.
3. **The caption band never moves.** With no seam, the pill at y=1512 is the
   only element that survives every cut. It is what makes the alternation
   legible instead of jarring; take it away and the cuts feel like glitches.

An SFX family carries the grammar audibly: `tk_in` (whoosh into an impact) on
every entrance, `tk_out` (airy release, no impact) on every exit, so seize and
release are different sounds. `punch` (dry sub thump) is rationed to 4-5 face
punch-ins per variant, `tick` to the plates that answer a request, `swarm` to
the peak's traffic. All five generated once via ElevenLabs and shared by the
three variants (`sfx/`, `takeover_sfx_gen.py`).

Face beats are carried by **punch-in CUTS**, not zooms: an instant 0.05s scale
step (1.00 → 1.10/1.18) that then holds. A continuous zoom would be idle motion.

## The one object

Everything visual is one thing seen three ways — a **field of 30 real tool
plates** and a **context rail** under it:

* **FLOODED** (`THE OLD WAY`) — all 30 plates land at once, the rail drowns to
  100%.
* **ON DEMAND** — the field goes dark, a request pulse goes out, exactly ONE
  plate answers and the last one that answered goes dark again. The rail fills
  to a 7% sliver and then never moves.
* **CONSUMED** (`THE PORTAL`, the Law-13 peak) — the plates stop being a wall
  and become traffic: they stream in from every edge and pass THROUGH a portal
  the Nous mark opened, accumulating nothing, while the rail below sits dead
  still. The stillness of that rail while dozens of tools pour past it *is* the
  argument. The ∞ resolves inside the portal at the end.

Plus two supports: the key term on cream (`PROCEDURAL DISCLOSURE`, LAW 9) and
the context window as a vessel that fills to a hard ceiling (`CONTEXT IS
FINITE`).

All 30 grid plates carry a **real registry mark**. An earlier pass mixed in
anonymous plates and a whole row of them read as unfinished slots, not as
unnamed tools — the wall is only worth building if every plate is something the
viewer could actually have connected.

## What each variant does differently

### v1 SPARSE — the takeover as a rare dramatic event
Three story takeovers, at the three biggest claims, nothing else.
`13.20-19.70` term→mechanism (6.50s, one takeover with two movements and a hard
internal cut) · `20.00-23.60` finite (3.60s) · `33.38-40.58` the portal
(7.20s) · outro. Face runs of 13.2s, 9.8s and 10.2s, carried entirely by
punch-ins.

### v2 DENSE — the standard big-channel cadence
Seven story takeovers, 2.6-3.9s each, roughly a visual event every six seconds.
Nothing is merged: the term and the mechanism are two separate takeovers, the
Nous attribution gets its own beat, and the portal appears twice (radial feed at
35.22, then a marching stack at 43.68 for the "give up all the MCP servers"
line). Longest face run: 6.9s.

### v3 GROWING — an escalation grammar
Five story takeovers, each longer and more elaborate than the last:
**1.64s → 2.42s → 3.94s → 5.94s → 8.66s**, then a 7.16s coda that carries the
give-up beat as a stack feeding the same portal before hard-cutting to the outro
card. The first is a 1.6s ∞ flash you barely register; the last owns the video.
The term takeover gains its mechanism movement, and the finite takeover gains a
second movement where the vessel is picked back down to a single clean bottom
course.

---

## Ranking (mine, honest)

**1. v3 GROWING.** The escalation is a real grammar and not a gimmick: because
the first cutaway is over before you can settle into it, the 8.7s peak lands as
an event rather than as "another graphic". It also happens to solve the format's
hardest scheduling problem — the peak beat gets the room a bespoke Law-13 scene
actually needs, without the rest of the video going quiet. Its 1.6s flash is the
best answer I found to the face-led hook: Miguel plus the format's own device,
no bolted-on hook object. Weakest point: the coda is a coda, not a sixth growth
step, and a viewer paying close attention will feel the curve break.

**2. v2 DENSE.** The most immediately "YouTube" of the three and the one I'd bet
on for retention — the frame is never Miguel's for long, and the rhythm is
genuinely pleasant. But it costs the thing the factory cares most about: the
peak scene gets 3.9s, which is barely enough to read a bespoke object at all, so
the portal registers as a nice transition rather than as the idea. It also
forces the portal to appear twice, and the second appearance has no ∞ to pay
off, so it reads as a repeat.

**3. v1 SPARSE.** The individual takeovers are the best-looking of the three —
the 6.5s two-movement term→mechanism scene is the single best beat in the whole
experiment, and the 7.2s portal breathes. But a 13.2-second unbroken face run at
the top of a short is indefensible in 2026, punch-ins or not, and there are two
more nearly-10-second runs after it. Sparse proves the takeover is powerful; it
does not survive as a whole-video grammar.

Reading across all three: **the format wants v3's shape with v2's floor** —
escalating beats, but with a hard rule that no face run exceeds ~7s.

## What fought me

* **"Already moving" is the whole ballgame.** The first build cut to takeovers
  whose entrance began at t0, and the result read as a slide deck. Pre-rolling
  every interior by 0.18s behind the still-hidden clip fixed it completely and
  costs nothing. Same trick makes hard INTERNAL cuts work (cream term → dark
  field inside one takeover).
* **Flying elements versus the sacred caption band.** The portal's radial feed
  originally spawned plates on a circle whose lowest point put a plate edge at
  y=1469 — 14px into the caption pill. Fixed by making the spawn an ellipse
  (rx 820 off-frame, ry 560) and adding a build-time guard that refuses to
  emit any feed plate that could reach `CAP_Y - 112`.
* **The key term wanted to double the caption.** Miguel says "procedural
  disclosure" at 11.88-13.00 and Law 9 wants the term centre stage. The fix is
  scheduling, not design: the takeover starts at 13.20 on "What does that
  mean?", so the cut *answers* the line instead of echoing it. The build has a
  caption-echo guard (exact-atom and 3-gram) that scans only the takeover
  sections.
* **`nous-girl.png` carries an opaque white field.** Dropped bare on a dark
  ground it paints an accidental white square. Plated it (rounded white card,
  same language as the tool tiles) so the white is deliberate.
* **A "picked clean" state must be a decision, not a scatter.** v3's second
  finite movement first kept five random blocks and read as a half-loaded bug.
  Keeping one clean bottom course reads as a choice.
* **Outro composition drifts in a full frame.** The split format's outro fills a
  460px zone; here it has 1920px and the first pass floated high in a field of
  cream. It needed its own optical centre (y=880, not the scene band's 810) and
  ~20% more scale.

## Laws this format would need if adopted

1. **NO SPLIT, EVER.** The frame is Miguel's or the visual's. A split is a
   different format; mixing the two inside one video destroys the device.
2. **CUTS LAND ON WORDS.** Every takeover entrance and exit sits on a Scribe
   word boundary. Enforced at build time, not by eye.
3. **ARRIVE IN MOTION.** A takeover's first visible frame is mid-gesture. Any
   scene whose entrance begins at its own t0 is a defect. (This is Law 20's
   spirit applied to every cutaway, not only the hook.)
4. **THE BAND IS FIXED AND SACRED.** Captions sit at one y for the whole video
   and nothing — including elements in flight — enters within 112px of it.
   Law 4's "seam" clause becomes "band"; the seam law's don't-touch rule carries
   over unchanged.
5. **SFX ARE THE GRAMMAR.** Entrance and exit take DIFFERENT sounds (seize vs
   release). One family per video, reused; a takeover without its signature
   reads as a rendering error.
6. **NO FACE RUN OVER ~7s.** The corollary of owning the whole frame is that
   Miguel alone for 10+ seconds is a hole. Punch-in cuts are the minimum
   texture, not a substitute for a cutaway.
7. **PUNCH-INS ARE CUTS.** Instant scale step then held. Never a zoom (Law 1).
8. **THE PEAK NEEDS >=6s.** A bespoke Law-13 object cannot be read in 3s of
   full-frame time. If the cut map cannot afford six seconds somewhere, the
   video should not claim a bespoke peak.
9. **LAW 20, FACE-LED FORM.** The hook is Miguel plus the format's own device —
   a punch-in, or a sub-2s flash takeover. No gratuitous hook object.

## Files

```
takeover_core.py        chassis: palette, atoms, tween grammar, captions,
                        scenes, page assembly, lab guards
takeover_v1_gen.py      SPARSE  cut map + punch map
takeover_v2_gen.py      DENSE
takeover_v3_gen.py      GROWING
takeover_sfx_gen.py     the five-member SFX family (ElevenLabs, cached in sfx/)
takeover_mix_check.py   speech margin on the factory's pinned instrument
takeover_v{1,2,3}/      HyperFrames projects (assets/ symlinks to stage/)
out/takeover_v{1,2,3}.mp4
_report_takeover_v*.json   cut map, beat lengths, face runs, caption count
```

---

# Fix round 1 — `takeover_fix.mp4` (2026-08-30, task id `takeover`)

Miguel's verdict was **KEEP, fix sound**: *"Does this a lot better"* (the
switching), preferred zoom grammar, visuals "remarkable" — but the SFX were
**unpleasant, louder than voice and bed, and slightly out of sync**. So the cut
grammar is untouched and four things changed.

```
out/takeover_fix.mp4     GROWING, 25fps, tamed palette, derived framing
                         6 takeovers  29.76s  55.1% of frame time
                         beats 1.64 -> 2.40 -> 3.96 -> 5.96 -> 8.68  (+7.12 coda)
                         longest face run 6.32s
```
Staged to `~/Movies/Shorts Factory/Format Lab/Fixed/takeover_fix.mp4`.

## 1. Shape — v3's GROWING map with v2's floor

v3's cut map already satisfied the ≤7s face-run rule, so it survives as the
flagship shape rather than being re-cut: the escalation (1.64 → 8.68s) is what
makes the portal land as an event, and the longest unbroken face run is 6.32s.
Every edge was re-quantised onto the 25fps grid and re-validated against the
Scribe boundaries; the build refuses a map whose first five beats are not
monotonically increasing, and refuses any face run over 7s.

## 2. Sound — the tamed palette at the pinned class levels

| was | now | class | `data-volume` |
|---|---|---|---|
| `tk_in` (hf6k 0.30, peak -24.13) | `soft_whoosh` | structure | 0.120 |
| `tk_out` (peak -21.78, **492 ms of dead air**) | `reverse_air` | structure | 0.120 |
| `punch` | `low_thump` | structure | 0.120 |
| `tick` (harsh) | `tick` | detail | 0.077 |
| `swarm` (**hf6k 0.993**, centroid 10 094 Hz) | **DELETED** | — | — |
| — | `pop`, once, on the ∞ resolving | detail | 0.077 |

The single `SFX_VOLUME = "0.18"` is gone. Gain is now a **class constant** and
the files are normalised, so the delivered level dropped far more than the
constant suggests: `tk_in` -24.13 → **-37.40 dBFS**, i.e. from **10.3 dB OVER**
bed presence to **3.0 dB UNDER** it. 22 events in 54s, and every one of them
scores a hard cut or a discrete arrival — nothing decorates.

`_shared/sfxpalette_verify.py` re-derives all of it from the shipped files:
**PASS, 0 files off spec.** Speech margin on the pinned instrument is **20.79 dB**
(v1 20.81, v3 20.73; approved run-7 corpus 15.85-23.70) — the effects are quieter
without costing any speech separation.

## 3. Sync — frame lock, proven by decode

The old builder scheduled entrances at `t0 - 0.06` and exits at `t1 - 0.04`.
Those were **compensation for leading silence inside the old mp3s** (up to
492 ms), not placement decisions. The new files start on the transient (3.0 ms),
so the offsets are deleted and one integer frame number drives both the picture
and its sound.

The three ON DEMAND ticks were the audible offender: hand-typed at
15.31 / 16.02 / 16.73 against plate lights that actually fire at
15.33 / 15.95 / 16.56 — up to **170 ms (4 frames) late**. They are now **derived
from `takeover_core.field_ondemand`'s own arithmetic** and asserted at build time
against the emitted tween; if the core's scheduling ever moves, the build fails
instead of shipping a desync.

`takeover_fix_check.py` decodes the finished MP4 and shows every mode cut landing
on exactly the frame its `low_thump` is scheduled at — **0 frames of error**, not
the ±1 the law allows:

```
4.16  wide->max  f103 0.193 -> f104 0.422      30.80 std->max  f769 0.298 -> f770 0.421
11.88 wide->max  f296 0.192 -> f297 0.418      44.08 std->max  f1101 0.286 -> f1102 0.418
19.24 std->max   f480 0.295 -> f481 0.424
```

## 4. Framing — Global Law 1, and the punch table is gone

The face is no longer one full-bleed plate scaled 1.00 → 1.18. It is **three
derived plates, cut between and never scaled** (`_shared/FRAMING.md` §5):

| mode | plate | seat | measured `face_frac` | share of face time |
|---|---|---|---|---|
| REST | `face_wide_25` 1080×900 | y=230 | **0.197** | 11.96s (49%) |
| MID | `face_std_25` 1080×1350 | y=50 | 0.304 / 0.284 | 6.72s (28%) |
| CEILING | `face_max_25` 1080×1920 | y=0, full bleed | 0.424 | 5.60s (23%) |

The lab shipped 0.409-0.509 at rest with a worst frame of **0.72 head_frac**.
Rest is now **0.197** — half the head, shoulders and torso in frame, which is what
Miguel asked for and lands at the wide end of his own reference reel's card band
(0.196-0.238). Nothing in the video exceeds **0.427** against the 0.43 ceiling.

Two decisions worth keeping:

* **The wide and std plates are seated so their EYE LINES coincide at y=590.**
  Both are full-height master slices, so the eye sits at 40.05% of plate height;
  choosing tops of 230 and 50 makes the wide↔std cut a pure size step with **no
  vertical jump**. `max` is full-bleed and cannot be moved, so its eye drops to
  770 — and that jolt is exactly what the `low_thump` is spent on.
* **Every size change is a cut between plates; no scale is animated anywhere.**
  A build guard rejects any tween touching `scale` on a face element. The 0.72
  head_frac frames are therefore unreachable by construction, not by discipline.
  `low_thump` is spent on ONE rule — a cut INTO the ceiling that is not already
  carrying a takeover exit's release — which is 5 of the 20 mode cuts.

The rest state is now a **letterboxed portrait on an INK ground** rather than a
full bleed (FRAMING hard rule 2: a full-bleed face is never the rest state). The
surplus canvas is left as clean negative space; the caption band at y=1512 is
unchanged and the std plate stops exactly on the 112px keep-out line.

## 5. 25 fps (Global Law 6)

Rendered natively at 25 with the conform duplicates removed (16.8% → 0.15%). The
three plates were re-encoded into `stage_fix/v/` with `-g 25 -keyint_min 25`;
the source derivatives carry keyframes every 10s, which triggers HyperFrames'
`sparse keyframes … seek failures and frame freezing` warning. With the dense GOP
the warning is gone and extraction of all three plates takes 5.4s.

## What fought me

* **`ffmpeg -ss T` returns the first frame with `pts >= T`.** The first frame-lock
  probe asked for `f/25 + 0.02` and got frame `f+1` every time, which read as an
  off-by-one in the *composition*. It was an off-by-one in the *measurement*. Ask
  for `f/25 - 0.02`.
* **`head_frac` is not trustworthy on this format any more.** The cap-top scan in
  `_shared/measure_head.py` walks up the head column looking for the black-cap /
  warm-wall luminance edge. On the new INK ground it walks straight off the plate
  into the letterbox and returns ~0.43 where the true value is ~0.26. `face_frac`
  is pure landmark geometry, is the metric the law is written in, and is the only
  one to read for a face-on-a-dark-ground composition.
* **Float noise on the frame grid.** `38.30 * 25 = 957.4999999…`, so the ∞ resolve
  quantises to frame 957 (38.28) rather than 958. Harmless — the visual is
  quantised from the same expression, so picture and sound still share one frame —
  but worth knowing before someone "fixes" a 1-frame discrepancy that is not one.
* **`cut_on()`'s 0.03s duration is safer at 25 than at 30.** A 0.03s tween is
  shorter than one 25fps frame, so a hard internal cut can never paint an
  intermediate opacity. No change needed; it just gets better.

## Not touched

`takeover_core.py` is **unmodified** by this round — v1/v2/v3 still reproduce
byte-for-byte. Everything new lives in `takeover_fix_gen.py`,
`takeover_fix_check.py` and `stage_fix/`. The Global Law 3 meter fix the
round-fill sweep applied to `takeover_core.meter()` is inherited and verified in
the render (rounded lozenge caps on the ON DEMAND and portal rails at their 7-8%
readings).

## Files

```
takeover_fix_gen.py        the fix generator (cut map, mode map, SFX schedule, guards)
takeover_fix_check.py      self-check: container, framing, frame lock, mix
takeover_fix/              HyperFrames project (assets -> stage_fix)
stage_fix/                 25fps GOP-dense plates, tamed sfx, bed, logos
out/takeover_fix.mp4       the render
out/frames_fix/            the 10 decoded self-check frames
_report_takeover_fix.json  cut map, beats, face runs, mode budget, SFX schedule
logs/render_fix.log
```

---

# Fix round 2 — `takeover_fix2.mp4` (2026-08-30, task id `takeover2`)

Round 2 verdict: **the growing shape, the visuals and the sound are right; the
FACE treatment is wrong.** Verbatim: *"idea good, zoom execution poor — the
footage EXPANDING (scale animation) looks off. Zooms must be CROP CUTS within
the 0% frame. Lemniscate draw-on began as a visible dot (ghost-rule violation)
— start state invisible."* Plus, from the brief: he wants his **full face on
screen (the 0% standard) with SMALL zooms on it**.

So the cut map, the scenes, the palette, the tamed SFX palette and the
escalation are carried over **byte-identical**. Two things changed.

```
out/takeover_fix2.mp4    GROWING, 25fps, 0/5/10% zoom ladder, ghost rule clean
                         6 takeovers  29.76s  55.1% of frame time
                         beats 1.64 -> 2.40 -> 3.96 -> 5.96 -> 8.68  (+7.12 coda)
                         longest face run 6.32s
                         20 crop cuts   z00 11.96s / z05 7.40s / z10 4.92s
```
Staged to `~/Movies/Shorts Factory/Format Lab/Fixed2/takeover_fix2.mp4`.

## 1. The face — the "expansion" was the PLATE GEOMETRY, not a tween

Round 1 already refused to animate `scale` (there is a build guard for it), so
what Miguel saw was never a scale animation. It was the plates. Round 1's three
face states were three **different canvas windows** — 1080×900 seated at y=230,
1080×1350 at y=50, 1080×1920 at y=0 — each holding a differently-scaled slice of
the master on an INK ground. A REST→CEILING cut therefore grew a 900px
letterbox band into a full bleed: the footage genuinely did expand, just in one
frame instead of over a tween. Side by side with round 2 the diagnosis is
obvious — round 1's rest state is a small picture-in-picture floating in black.

Round 2 makes every face state **the same object**: a full-bleed 1080×1920
frame. The only difference between the three is *which window of the 4K master
was cut* (`ZOOM_STANDARD.md` §3, THE CROP-CUT RULE):

| level | master crop | head % of frame h | role | face time |
|---|---|---|---|---|
| **z00** | `crop=1216:2160:1270:0` | **56.3 %** | REST — the 0 % standard | 11.96s (49 %) |
| **z05** | `crop=1154:2052:1300:44` | 59.4 % | MID — default punch | 7.40s (31 %) |
| **z10** | `crop=1094:1944:1332:88` | 62.6 % | CEILING — accent, hard cap | 4.92s (20 %) |

The three-tier REST / MID / CEILING grammar Miguel approved is preserved
exactly — **same cut times, same escalation, same five `low_thump` accents** —
it is simply expressed as crop levels instead of as canvas windows. 5 % is the
default punch and 10 % the ceiling per `ZOOM_STANDARD.md` §4; nothing above 10 %
is built, because 15 %/20 % re-enter the 66-72 % head band round 1 was rejected
for. Windows are the ladder's union-centred ones, held static — no per-cut
re-centring, because a window that chases his face is a camera move (Global Law
5), and the static windows clip the head on 0 of 64 sampled frames anyway.

This deliberately overrides `FRAMING.md` hard rule 2 (*"a full-bleed face is
never the rest state"*), which Global Law 7 supersedes: the 0 % window is the
**widest** 9:16 full-bleed crop a 2160-tall master can physically give, so
full-bleed at 0 % *is* the zoomed-out state.

Three new build guards make the old failure unreachable: no `scale` on a face
element (inherited), **all three face windows must have identical seat and
size** (a cut that resizes the picture cannot be emitted), and no two
consecutive levels may be equal (a cut that changes nothing is not a cut).

## 2. The ghost rule — and it was worse than the one he caught

`infinity()` authored its path with `stroke-linecap="round"` and a rest state of
`stroke-dasharray:100; stroke-dashoffset:100`. Skia paints the round cap of the
fully-offset dash at path position 0, so an **un-drawn lemniscate is a filled
TERRA_2 dot**. Decoded out of `takeover_fix.mp4` at t=33.50 to confirm before
touching anything. Three instances, not one:

| where | dot on screen | why |
|---|---|---|
| portal | **6.38 s** (31.92 → 38.30) | glyph authored at section start, drawn at `inf_at` |
| outro stack prelude | **3.84 s** (46.90 → 50.74) | `sc_portal` emits the glyph with `inf_at=None` and **never draws it** — the dot was the only thing that element ever showed |
| outro card | 0.16 s | card `cut_on` precedes its `draw` |

Fixed at the helper, for all 6 draw-on call sites rather than the one he saw:
the rest state carries `stroke-opacity:0` (unconditionally no ink, cap artefact
or not), and `draw()` switches the stroke on **half a frame into** the draw, so
frame `t` — the only frame where a dash draw can paint nothing but its own cap —
is empty and frame `t+1` already carries 7 % of the path. `ring()` gained
`stroke-linecap="round"` too, safe now that the rest state is invisible, which
closed the hairline butt-to-butt seam visible at 3 o'clock in that same decoded
frame. `guard_ghost_rule` asserts all of it at build time: 7 draw-ons authored,
6 drawn with a matching reveal, 1 never drawn and now invisible for the whole
video.

## 3. Proof

`takeover_fix2_check.py` decodes the finished MP4. **ALL CHECKS PASS.**

* container 1080×1920, `25/1`, 1351 frames, 54.04 s;
* **full bleed** — top-12-row variance 4.8-5.0 on every face sample, i.e. real
  picture, not the flat ground strip a letterboxed plate would give;
* **the ladder is a step, not a ramp.** Absolute `face_frac` is a blunt
  instrument here — the levels are only 5 % apart, inside landmark noise — so
  the discriminating test is the **ratio across each cut**, measured on two
  adjacent frames of the same face:

```
1.12  z00->z05   f27  0.427 -> f28   0.446   ratio 1.044 (ladder 1.054)
4.16  z00->z10   f103 0.422 -> f104  0.467   ratio 1.107 (ladder 1.112)
7.68  z05->z00   f191 0.445 -> f192  0.424   ratio 0.953 (ladder 0.949)
11.88 z00->z10   f296 0.415 -> f297  0.462   ratio 1.114 (ladder 1.112)
19.24 z05->z10   f480 0.441 -> f481  0.473   ratio 1.073 (ladder 1.055)
30.80 z05->z10   f769 0.444 -> f770  0.466   ratio 1.050 (ladder 1.055)
44.08 z05->z10   f1101 0.430 -> f1102 0.457  ratio 1.063 (ladder 1.055)
45.36 z10->z00   f1133 0.475 -> f1134 0.432  ratio 0.908 (ladder 0.900)
```
  One frame, the exact ladder step, nothing in between — which is what makes it
  a crop cut and not an expansion;
* **ghost rule** — a 24×24 box on the old dot's coordinates (477, 770) at
  33.50 / 35.00 / 48.50 / 49.80: **0 TERRA_2 pixels** at all four, against a
  clean INK_2 mean;
* mix unchanged: speech margin **20.79 dB** (identical to round 1 — the sound
  was approved and nothing in it moved).

## What fought me

* **"No scale animation" was already true, so the complaint had to mean
  something else.** The temptation was to hunt for a stray tween. The actual
  culprit was static geometry: three windows of three different sizes make every
  cut between them a resize by definition. Worth remembering as a class of bug —
  *a hard cut between two differently-scaled framings of the same subject reads
  as a zoom*, and the only cure is to make the framings the same size.
* **Absolute `face_frac` cannot police a 5 % ladder.** Predicted 0.430 / 0.454 /
  0.478; measured samples land 0.415-0.475 depending on head tilt. The levels
  overlap inside the noise. Ratios between adjacent frames do not, because the
  pose barely changes across one frame — that is the metric a small-step ladder
  has to be checked with.
* **`stroke-dashoffset:100` is not "invisible".** It is "invisible unless the
  cap says otherwise". Any element whose only hiding mechanism is a dash offset
  needs a second, unconditional one.
* **A glyph that is never animated is still on screen.** `sc_portal` emits the
  lemniscate unconditionally and only *draws* it when `inf_at` is set. Nothing
  in the build was wrong; the element was simply authored and forgotten. The
  ghost guard now reports "never drawn" as a first-class count so an element in
  that state has to be a decision.

## Not touched

`takeover_core.py` is **unmodified**; the ghost fix lives in
`takeover_fix2_core.py`, a copy, so v1/v2/v3 and `takeover_fix` still reproduce
byte-for-byte. The cut map, mode-cut times, SFX schedule, captions, caption band
and all scene interiors are inherited from fix round 1 unchanged.

## Files

```
takeover_fix2_plates.py    builds the 3 ladder plates from the 4K master (25fps, GOP-dense)
takeover_fix2_core.py      chassis copy + THE GHOST RULE (GHOST_REST, draw(), ring caps)
takeover_fix2_gen.py       generator: zoom ladder, crop-cut guards, ghost guard
takeover_fix2_check.py     self-check: container, full bleed, ladder ratios, ghost, mix
takeover_fix2/             HyperFrames project (assets -> stage_fix2)
stage_fix2/v/face_z{00,05,10}.mp4   the ladder, full-bleed 1080x1920 @ 25/1
out/takeover_fix2.mp4      the render
out/frames_fix2/           the 14 decoded self-check frames
_report_takeover_fix2.json cut map, beats, zoom ladder budget, ghost audit, SFX
logs/plates_fix2.log  logs/render_fix2.log
```
