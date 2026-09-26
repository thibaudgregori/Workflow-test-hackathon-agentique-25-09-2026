# CLERK v3 — CALIBRATION

**Date:** 2026-09-02
**What was built:** `pipeline/clerk_video_gemini.py` + `pipeline/semantic_review.md` v3.
**What was run:** the new procedure on **all four batch-2 videos × all three staged
renders = 12 renders**, from `~/Movies/Shorts Factory/Daily/2026-09-02/`.
**Who adjudicated:** this clerk, against the law text and the known-and-accepted list.

---

## THE CHANGE IN ONE LINE

The still-frame clerk used to **find** the defects and Gemini used to **check**
them. That was backwards. Gemini now finds them and the clerk checks them.

| half of v2 | measured behaviour | v3 |
|---|---|---|
| still-frame clerk producing candidates | two runs on the same `codexvoice` render → **two different lists**; missed **4 of 6** defects Miguel confirmed; raised things the factory does on purpose | **retired as the source of candidates** |
| moving-clip Gemini verifier | **5/5** agreement with Miguel, cold | **promoted to the source of candidates** |

The reason is structural. Every defect class in STANDARD.md is defined over a
**window of time** — "empty >= 1.5 s", "still absent 2 s after the word", "held",
"while moving". A reviewer looking at one frame cannot evaluate one of them, so it
guesses; two honest guessers guess differently. A watcher that sees time does not
have to guess, and it hands the clerk a window the clerk can decode.

---

## 1. RECALL — the 7 known-real items

Ground truth = the seven flags Miguel and the moving-clip verifier agreed were
REAL (`batch2_flags_verified.md`).

| # | video · t | the real defect | v3 found it? | where |
|---|---|---|---|---|
| 1 | codexvoice 16.15 | cup colliding with the phone (motion) | ✅ | split C1 `15.67–16.20`, motion |
| 2 | codexvoice 18.55 | voice arcs overlapping the monitor (held 17.8–22.0) | ✅ | **cutout** C1 `18.00–28.00`, held |
| 3 | codexvoice 21.00 | labels on uneven baselines | ❌ | **missed on this run** |
| 4 | codexvoice 22.80 | labels on uneven baselines | ❌ | **missed on this run** |
| 5 | codexvoice 26.80 | two contradictory labels, held | ✅ | split C3 + cutout C3 `25.67–28.00` |
| 6 | codexvoice 38.80 | second logo clipped by the phone border while moving | ✅ | split C5 `38.50–38.80` + cutout C4, motion |
| 7 | codexnondev 22.50 | empty speech bubble ~1.7 s | ✅ | split C1 + cutout C2 `21.67–23.33` |

### **RECALL = 5 / 7 (71 %)**

Counting distinct *defects* rather than flags — items 3 and 4 are the same
uneven-baseline row seen twice — recall is **5 / 6 (83 %)**.

**About the miss.** Items 3/4 are not a blind spot, they are variance: during
development, a **chunked-only** configuration of the same script found exactly this
defect (`uneven_baselines 22.67–28.30`, "`YOUR PHONE` settles on a visibly higher
baseline than `ANYWHERE` and `THE FIRST PROMPT`") while missing the 38.8 s motion
clip that the whole-video call caught. That is why the shipped script sends **both
views and unions them** — and on the calibration run the union still dropped this
one. The clerk caught it during adjudication and logged it as **K2, a watcher
miss**, which is the honest accounting: the gate found it, the watcher did not.

For comparison, the still-frame clerk it replaces found **2 of these 7** (its own
v2 report confirmed 16.15 and 31.30-as-empty-monitor).

---

## 2. FALSE POSITIVES — the 8 known-false items

| # | video · t | the false claim Miguel rejected | v3 re-raised it? |
|---|---|---|---|
| 1 | deepseekflash 0.40 | "an EMPTY tag and no DeepSeek mark" | ❌ no |
| 2 | deepseekflash 4.15 | "'Opus' spoken and NO Opus mark anywhere" | ❌ no |
| 3 | deepseekflash 13.80 | "a completely blank cream field — dead slot" | ❌ no |
| 4 | deepseekflash 16.30 | "an UNLABELLED box — the shape needs a key" | ❌ no |
| 5 | deepseekflash 33.90 | "grey content lines strike through the word PRIVATE" | ❌ no |
| 6 | sparkchrome 1.30 | "DEAD SLOT — the wordmark is gone, the card has not arrived" | ❌ no |
| 7 | sparkchrome 1.48 | "LAW 2 — 'Chrome' spoken with no Chrome mark legible" | ❌ no |
| 8 | codexvoice 5.10 | "the second mark is a salmon pixel critter, not a Claude Code logo" | ❌ no |

### **FALSE POSITIVES = 0 / 8 (0 %)**

`sparkchrome` returned **zero candidates on all three renders** and
`deepseekflash` returned **zero of its five**. Two whole videos that v2 held on
nothing but animation frames now pass clean.

### Precision on the full v3 output

24 candidates across 12 renders. After adjudication:

| verdict | n | share |
|---|---|---|
| **CONFIRMED** | 14 (incl. 3 pending one ruling) | 58 % |
| **ACCEPTED-BEHAVIOUR** (dismissed) | 3 | 13 % |
| **REFUTED** (dismissed) | 1 | 4 % |
| clerk-originated CONFIRMED (not from the watcher) | 2 | — |

**v2 false-positive rate: 67 % (14 of 21). v3: 17 % (4 of 24).**

---

## 3. THE 31.3 s MONITOR — settled from the pixels

Miguel believed the monitor is **not** blank; the v2 clerk held the render on
"a `VERIFY` arrow points at a blank monitor". **Both are right about different
things**, and the measurement is not ambiguous.

A zone-ink scan of the drawn monitor's **screen interior** on
`codexvoice_split.mp4`, at 0.2 s steps:

| window | screen interior | duration |
|---|---|---|
| 18.0 – **28.6** | ink | — |
| **28.6 – 32.6** | **flat, std 0.00 — no content at all** | **4.0 s** |
| 32.6 – 35.6 | a grey application window enters and holds | 3.0 s |
| 35.6 – 38.0 | flat again | 2.4 s |
| 38.8 – 40.8 | flat again | 2.0 s |

**What is on that monitor between 29.8 s and 32.6 s:** the monitor's own black
rounded-rectangle **bezel**, its **stand**, the black **desk line** beneath it, the
printed label **`YOUR DESK`** directly below it, and the orange **`VERIFY` arrow**
terminating on its left edge. Inside the bezel: **nothing**.

**Verdict.** The v2 claim was mis-worded and Miguel's objection to it is correct:
the arrow does **not** point at a blank monitor — it points at a fully drawn,
correctly labelled desk monitor, and that picture argues its sentence ("you'll have
to come back to your desk to verify"). The accurate, narrower statement is: **the
monitor's *screen* is empty for 4.0 s**, three times over across the closing third.
Under the law as written (>= 1.5 s of an empty container is NO-SENSE) that is a
CONFIRMED row, and it is logged as CONFIRMED **with the dissent recorded**: whether
an idle screen on an unattended desk is a dead slot or the correct picture of an
unattended desk is a ruling only Miguel can give.

Note that the v3 watcher independently raised the 35.6 and 38.8 blanks but not the
28.6 one on this run (an earlier configuration did raise `29.66–32.33`). The clerk
added it as K1.

---

## 4. COST AND WALL CLOCK

`gemini-3.8-flash`, HIGH media resolution, 3 fps, `thinking_level=medium`, one
whole-video call plus overlapping 20 s windows (3 s overlap), audio kept.

| video | duration | calls | split | cutout | whiteboard | **per video** | wall clock (3 renders in parallel) |
|---|---|---|---|---|---|---|---|
| codexvoice | 45.8 s | 4 + 4 + 4 | $0.2602 | $0.2682 | $0.2398 | **$0.7682** | **211 s** |
| deepseekflash | 39.5 s | 4 + 4 + 4 | $0.2011 | $0.1862 | $0.2024 | **$0.5897** | **166 s** |
| codexnondev | 44.6 s | 4 + 4 + 4 | $0.1759 | $0.2088 | $0.1812 | **$0.5659** | **166 s** |
| sparkchrome | 25.3 s | 3 + 3 + 3 | $0.0809 | $0.1022 | $0.0894 | **$0.2725** | **90 s** |
| **BATCH** | | **45 calls** | | | | **$2.196** | **~11 min sequential / ~4 min if videos run in parallel too** |

**Mean: $0.18 per render, $0.55 per video, $2.20 for a four-video batch.**

The v2 procedure text claimed "a fraction of a cent per video". That was wrong by
**two orders of magnitude** and is corrected in `semantic_review.md` §7.

### The two dials that are NOT cost dials

Both were measured, both on `codexvoice_split`:

| change | cost | candidates found (5 known defects on this render) |
|---|---|---|
| `media_resolution` = LOW (SDK default) | $0.023 | **1** |
| `media_resolution` = HIGH | $0.064 | 1 |
| HIGH + required per-beat sweep fields | $0.108 | **3** |
| HIGH + sweep + chunked windows only | $0.213 | 3 (a *different* 3) |
| HIGH + sweep + chunks, `thinking` = **low** | $0.099 | **0** |
| **shipped: HIGH + sweep + whole-video call + chunks, `thinking` = medium** | $0.260 | **4** |

At LOW media resolution a 46 s short is ~10K tokens and the model cannot see a cup
touching a phone border. At `thinking=low` the model **stops looking before it
stops writing** — same five calls, half the money, zero candidates. If a batch has
to be cheaper, drop `--fps` to 2 or pass `--no-whole-pass`; never lower those two.

---

## 5. NEW CONFIRMED ITEMS NOT PREVIOUSLY KNOWN

Five defects that no previous pass had found, all adjudicated from decoded frames.

| # | render | window | class | the defect | evidence |
|---|---|---|---|---|---|
| N1 | codexvoice **split + cutout** | 19.10–20.00 (split) / 19.10–28.00 (cutout) | picture_contradicts_sentence · **blocking** | The label **`ANYWHERE` is welded under the monitor that has a diagonal strike through it**, so the block reads "ANYWHERE ✗" at the exact instant the sentence says *"you can work from **anywhere** that you want"* | word "anywhere" = 19.10–19.76 in the tight transcript; decoded 19.1 / 19.6 / 20.0 / 21.5 / 22.8 — the label sits directly under the struck-out monitor throughout. The watcher saw it in **3 of 5** windows on the cutout, its highest-agreement candidate of the batch. **This is the only `blocking` severity in the batch** |
| N2 | codexvoice **split** | 35.60–38.00 and 38.80–40.80 | empty_zone · held | the desk monitor's screen is blank twice more in the closing third, 2.4 s and 2.0 s | zone-ink scan, std 0.00 across both windows |
| N3 | codexvoice **whiteboard** | 25.75–26.10 | cramp_overlap_clipping · **motion** | the pencil body crosses the **finished** label `THE FIRST PROMPT` while its tip writes `A DISCUSSION` **below it** | decoded at 0.2 s steps 25.4→26.4: clean at 25.4/25.6, pencil on `THE`/`F` at 25.8, across `PROMPT` at 26.0, clear by 26.2. **Also settles the v2 dissent** — the old verifier said "the pencil does not overlap or touch the letters"; it does |
| N4 | codexvoice **split** | 21.00–23.50 | uneven_baselines · held | *(this is known-real #3/#4, but the **watcher** missed it and the **clerk** raised it)* — logged here so the watcher's recall stays honest | decoded 21.5 / 22.8 |
| N5 | **all three whiteboards** | codexvoice 4.40–7.00 · deepseekflash 6.20–17.00 · codexnondev 4.10–6.00 | named_tool_no_mark · held | **the whiteboard format systematically does not place a registry mark at the named word.** codexvoice: "Android" spoken 1.72–2.04, no Android mark ever. deepseekflash: three cards labelled `OPUS` / `FABLE` / `V4 FLASH` where **only `V4 FLASH` carries a mark** and the other two are empty outlines for 10.8 s. codexnondev: "Codex" spoken 2.0–2.4, board carries only `</>` glyphs | decoded on each board. **Reported as ONE chassis question, not three holds** (STOPPING RULE): the whiteboard has its own LABEL LAW ("the word is written beside the object") and **no written Law-2 exemption**. One ruling from Miguel closes all three and belongs in `formats/whiteboard/CHASSIS.md` |

### Two items added to KNOWN AND ACCEPTED as a result

Both were watcher candidates that adjudication killed, and both would have kept
killing candidates every run, so they are now in the list the watcher is given:

* **#11 — a cross-dissolve superimposes two pictures.** `codexnondev` split C2 /
  cutout C3 called a 0.45 s scene dissolve "a border cutting through four tool
  cards". Both layers were visibly at reduced opacity; a collision needs two
  objects both fully present in the *same* picture.
* **#12 — a company named as a possessive does not need its own mark.**
  `codexnondev` cutout C1 raised "OpenAI named, no OpenAI mark" on the sentence
  *"Codex, OpenAI's coding assistant"*. The tool named is Codex and the Codex mark
  is on screen; "OpenAI's" qualifies it.

---

## 6. VERDICTS FOR THE BATCH

| video | split | cutout | whiteboard | video verdict |
|---|---|---|---|---|
| **codexvoice** | HOLD (8 CONFIRMED) | HOLD (4) | HOLD (2, one pending) | **HOLD** |
| **deepseekflash** | PASS | PASS | HOLD (1, pending the whiteboard ruling) | **HOLD (pending)** |
| **codexnondev** | HOLD (1) | HOLD (1) | HOLD (1, pending) | **HOLD** |
| **sparkchrome** | PASS | PASS | PASS | **PASS** |

Per-video detail: `clerk_v3_codexvoice.md`, `clerk_v3_deepseekflash.md`,
`clerk_v3_codexnondev.md`, `clerk_v3_sparkchrome.md`.
Machine output: `cands_<id>_<fmt>.json` × 12.

**Evidence frames** (decoded during adjudication, kept because several rows turn
on them):

| file | shows |
|---|---|
| `clerkv3_evidence_codexvoice_monitor_29-33.png` | the desk monitor at 29.8 / 30.6 / 31.3 / 32.0 / 32.6 / 33.4 s — the §3 ruling |
| `clerkv3_evidence_codexvoice_split_windows.png` | the cup collision (15.6/15.8/16.0), the `ANYWHERE`-on-struck-monitor block (19.1/19.6/20.0), the uneven baselines (21.5/22.8), the double label (26.5), the clipped travelling mark (38.5/38.65/38.8) |
| `clerkv3_evidence_codexvoice_whiteboard_pencil.png` | the pencil crossing `THE FIRST PROMPT` at 0.2 s steps, 25.4 → 26.4 |
| `clerkv3_evidence_codexnondev_split.png` | the empty speech bubble 21.7–23.3 and the 34.15 s cross-dissolve |
| `clerkv3_evidence_codexnondev_cutout.png` | the Codex mark present through the "OpenAI's" possessive |
| `clerkv3_evidence_deepseekflash_whiteboard.png` | the `OPUS` / `FABLE` cards empty beside a marked `V4 FLASH` |
| `clerkv3_evidence_deepseekflash_split.png` | the anchor card re-labelling `OPUS` → `FABLE` under one Anthropic mark |

---

## 7. WHAT THIS SAYS ABOUT THE GATE

1. **The watcher is a good finder and a poor judge.** It over-states windows
   ("held to 28.0" for a 0.35 s pencil pass; "to 41.33" for a blank that ends at
   40.8) and mis-classes held vs motion. Every window in this report was re-measured
   before it was written down, and several were corrected. The split of labour is
   the right one: **it points, the clerk measures.**
2. **`seen_in_passes` is a usable confidence signal.** The batch's only `blocking`
   candidate (N1) was also its highest-agreement one — seen in 3 of 5 windows. Every
   candidate seen in ≥2 windows survived adjudication; every dismissal was a
   single-window candidate.
3. **The known-and-accepted list is the precision mechanism, and it must be fed.**
   Zero of the 8 known-false items came back, because the mascot, the entry
   animations, the occluding silhouette and the edge-faded tiles are all in the
   list. The two candidates that did need dismissing produced two new list items.
   Adding to that list is how this gate stops repeating itself.
4. **The remaining recall gap is variance, not blindness.** The one miss was found
   by a different view of the same script. If a future batch needs more recall
   before it needs cheaper, `--passes 2` doubles the views and roughly doubles the
   bill; that trade is now measurable instead of assumed.
