# Batch 2 clerk flags — VERIFIED ON THE MOVING CLIP

**Date:** 2026-09-02
**Why:** Miguel read the 21 NO-SENSE flags the four fresh clerks returned for daily
batch 2 and ruled **most of them false positives**. The clerks sample a still frame
~0.3 s after each visual boundary, which is *inside* the 1-2 s entry animation, so
"empty bubble", "no Opus mark yet" and "the label lands late" are the picture still
arriving. **A still frame cannot tell a transition from a held state.**

**Method:** `pipeline/verify_flags_gemini.py` cuts each flag's neighbourhood out of
the staged YouTube split — **t-2.5 s .. t+3.5 s, audio kept, 720x1280** — and hands
the MOVING clip to **`gemini-3.8-flash`** with the clerk's claim verbatim, the words
spoken across that window, and the STANDARD's defect-vs-transition definition:

* **CONFIRMED** — a real defect: the wrongness is still true after the element has
  landed and persists >= 1.5 s, **or** it is a motion defect (an element crossing
  into / over / through another object or a border while moving). Motion never
  excuses a collision.
* **TRANSITION** — the element is arriving or leaving within ~2 s and lands
  correctly. The clerk photographed the animation.
* **REFUTED** — the claim is wrong about the pixels.

The model was **never told Miguel's rulings** and the prompt was not tuned against
them. Raw verdicts: `flagcheck_{codexvoice,deepseekflash,codexnondev,sparkchrome}_*_split.json`.

---

## VERDICT TABLE — all 21 flags

| # | video | t (s) | clerk's claim (abridged) | Gemini verdict | Gemini's reason | Miguel's ruling | agreement |
|---|---|---|---|---|---|---|---|
| 1 | codexvoice | 5.10 | the second mark is a salmon pixel critter, not a readable Claude Code logo (LAW 2) | **REFUTED** | "the pixel-art mascot is the official Claude Code terminal character and represents the named tool" | **FALSE** — people recognise it | ✅ agrees |
| 2 | codexvoice | 16.15 | CRAMP — a paper cup jammed into the phone's left edge, handle occluded | **CONFIRMED** *(motion)* 14.90–15.80 | "the coffee cup graphic collides directly against the phone edge with zero clearance" | **REAL** | ✅ agrees |
| 3 | codexvoice | 17.20 | "two frictions" but only one thing on screen, prior beat's picture still standing | **TRANSITION** | "the graphics are actively transitioning to introduce the first point as the phrase is spoken" | — | — |
| 4 | codexvoice | 18.10 | blank unlabelled monitor, arcs pointing phone → desk, the opposite of the sentence | **TRANSITION** | "the monitor is caught mid-animation before the strike-through slash and ANYWHERE label fully land" | — | — |
| 5 | codexvoice | 18.55 | CRAMP — the outer voice arc touches the monitor's edge, the lower arc crosses the stand | **CONFIRMED** *(held)* 17.80–22.05 | "the sound arcs collide with the monitor bezel and stand throughout the held state" | **REAL** | ✅ agrees |
| 6 | codexvoice | 19.45 | the slash's lower tail runs straight through the voice arcs | **REFUTED** | "the slash stays contained on the monitor screen and does not touch the sound arcs" | — | — |
| 7 | codexvoice | 21.00 | labels on different baselines — YOUR PHONE a full line below ANYWHERE | **CONFIRMED** *(held)* 19.50–24.50 | "the settled text labels sit on visibly uneven vertical baselines" | **REAL** ("odd but not the worst") | ✅ agrees |
| 8 | codexvoice | 22.80 | three labels unaligned; THE FIRST PROMPT crowds the right margin | **CONFIRMED** *(held)* 20.30–26.30 | "the labels remain on staggered baselines across the settled display" | **REAL** ("odd but not the worst") | ✅ agrees |
| 9 | codexvoice | 25.40 | the chat bubbles are labelled THE FIRST PROMPT — the label names the wrong object | **TRANSITION** | "the orange 'A DISCUSSION' label is actively fading in to label the expanded conversation bubbles" | — | — |
| 10 | codexvoice | 26.80 | two stacked contradictory labels on one object: THE FIRST PROMPT + A DISCUSSION | **CONFIRMED** *(held)* 25.30–27.50 | "both contradictory labels remain settled together under the chat bubbles for over two seconds" | not ruled | — |
| 11 | codexvoice | 35.60 | a half-erased ghost VERIFY word and arrow stub still floating on the phone's edge | **TRANSITION** | "the outgoing VERIFY text and arrow completely cleared during their exit animation and left no residue" | — | — |
| 12 | codexvoice | 38.80 | CRAMP — a second Codex logo jammed half-on / half-off the phone's right border | **CONFIRMED** *(motion)* 38.50–39.10 | "the moving logo is clipped by the phone's border as it travels across the frame" | **REAL** ("cut in half while moving — it has motion") | ✅ agrees |
| 13 | deepseekflash | 0.40 | an EMPTY tag and no DeepSeek mark while the word "DeepSeek" is said | **TRANSITION** | "the tag drops in empty as an entry animation and the DeepSeek logo fills it within approximately one second" | — | — |
| 14 | deepseekflash | 4.15 | "Opus" spoken and NO Opus mark anywhere on screen (LAW 2) | **TRANSITION** | "the Opus mark and comparison card arrive and settle less than half a second after the word is spoken" | — | — |
| 15 | deepseekflash | 13.80 | a completely blank cream field — dead slot | **TRANSITION** | "the cream background is clear for roughly one second during an ordinary transition between two graphical scenes" | — | — |
| 16 | deepseekflash | 16.30 | an UNLABELLED box — the shape needs a key, nothing says what it is | **TRANSITION** | "the identifying label appears underneath the illustration within approximately 1.5 seconds" | — | — |
| 17 | deepseekflash | 33.90 | the box's grey content lines strike straight through the word PRIVATE | **REFUTED** | "the horizontal lines sit entirely to the left of the word with clear spacing and do not cross any text" | — | — |
| 18 | codexnondev | 22.50 | an EMPTY speech balloon and nothing else, 21.60 → 23.40 s | **CONFIRMED** *(held)* 21.50–23.20 | "the speech bubble remains completely empty for roughly 1.7 seconds before any graphic appears" | not ruled | — |
| 19 | codexnondev | 29.80 | the OVER 40% card lingers while the caption says "these four tools" | **TRANSITION** | "the outgoing graphic clears within one second of the flagged instant as the new tool cards enter" | — | — |
| 20 | sparkchrome | 1.30 | DEAD SLOT — the wordmark is gone and the browser card has not arrived | **TRANSITION** | "the brief 0.25-second gap between elements is a standard transition, well below the 1.5-second empty threshold" | — | — |
| 21 | sparkchrome | 1.48 | LAW 2 — "Chrome" spoken with no Chrome mark legible | **TRANSITION** | "the Chrome logo appears less than half a second after the word is spoken, well within the 2-second tolerance" | — | — |

---

## PRECISION

| | count | share |
|---|---|---|
| flags reviewed | **21** | 100 % |
| **CONFIRMED** (real defects) | **7** | **33 %** |
| dismissed — TRANSITION | 11 | 52 % |
| dismissed — REFUTED | 3 | 14 % |
| **false-positive rate of the old still-frame procedure** | **14 / 21** | **67 %** |

Per video: codexvoice **6 / 12** confirmed · codexnondev **1 / 2** · deepseekflash
**0 / 5** · sparkchrome **0 / 2**. Two whole videos — `deepseekflash` and
`sparkchrome` — were held on nothing but animation frames.

**Every dismissal in the TRANSITION column is the same failure**: the clerk sampled
the frame while the picture was still arriving. Not one of them describes a picture
that was actually wrong once it landed.

## AGREEMENT WITH MIGUEL — 5 / 5

He ruled six flags (five items; the label-baseline ruling covers two flags). The
model, cold and unprompted, matched him on every one:

| his ruling | flag | Gemini | match |
|---|---|---|---|
| REAL — cup jammed into the phone | codexvoice 16.15 | CONFIRMED, motion | ✅ |
| REAL — sound arcs overlapping the monitor | codexvoice 18.55 | CONFIRMED, held 17.8–22.05 | ✅ |
| REAL — "odd but not the worst": label baselines | codexvoice 21.00 + 22.80 | CONFIRMED both, held | ✅ |
| REAL — second Codex logo cut in half **while moving** | codexvoice 38.80 | CONFIRMED, `motion_defect: true` | ✅ |
| FALSE — Claude Code mascot, people recognise it | codexvoice 5.10 | REFUTED | ✅ |

**No disagreements with Miguel.** The prompt was not tuned toward his answers: it
carries the general definition (held >= 1.5 s, or a motion collision) and it was run
once, cold, on every flag at the same time.

### Two CONFIRMED flags Miguel did not rule on

He said *most* were false positives and named five; these two survived the clip and
are not covered by his ruling. They are the honest remainder of the hold, and they
are cheap to fix:

* **codexvoice 26.80** — the chat bubbles carry `THE FIRST PROMPT` (black) and
  `A DISCUSSION` (orange) at once, settled, for 2.2 s. One object, two names that
  contradict each other. (Note the pairing: the same defect flagged 1.4 s earlier at
  25.40 is a TRANSITION — the second label was still fading in.)
* **codexnondev 22.50** — the speech balloon is genuinely empty for **1.7 s**, over
  the 1.5 s bar. This is the one emptiness claim in the whole batch that was real.

## COST

| video | flags | model calls | in tokens | out tokens | cost |
|---|---|---|---|---|---|
| codexvoice | 12 | 3 | 11,145 | 22,335 | $0.0921 |
| deepseekflash | 5 | 1 | 4,282 | 3,152 | $0.0146 |
| codexnondev | 2 | 1 | 2,330 | 2,198 | $0.0100 |
| sparkchrome | 2 | 1 | 2,127 | 470 | $0.0034 |
| **total** | **21** | **6** | **19,884** | **28,046** | **$0.1201** |

`gemini-3.8-flash` at $0.75 / $3.75 per MTok (standard tier through 2026-12-31,
thinking tokens billed as output). **~3 cents per video**, against a 4K re-render
that costs minutes of machine time each — and 14 of which would have been run
against animations that were working.

## PROCEDURE CHANGES SHIPPED FROM THIS

1. `pipeline/semantic_review.md` — new section *A STILL FRAME CANNOT JUDGE A
   TRANSITION*; §1 samples at boundary **+1.5 s** (was +0.2-0.4 s); new §3a
   duration tests; new §3b mandatory moving-clip verification; §4/§5 split the
   autopsy into a CONFIRMED **NO-SENSE table** and a **DISMISSED table**; rules 6
   and 7 gained their 2 s and 1.5 s thresholds.
2. `STANDARD.md` — VISUAL QUALITY CHECKS §7 (the four rules) and a STOPPING RULE
   clause: a clerk flag is not a defect until the moving clip says so.
3. `.claude/workflows/daily-shorts.js` — the clerk brief carries the +1.5 s
   sampling, the duration tests, the mandatory verifier command, the two-table
   autopsy, and the Gemini cost in the clerk's return.
4. Both skill mirrors (`.claude/` and `.agents/skills/shorts-factory/SKILL.md`) —
   Gate 0 text and a new check-list row 15b.
5. `LEARNINGS.md` — the false-positive lesson with these counts.
