# CLERK v3 — codexvoice

* **Procedure**: `pipeline/semantic_review.md` v3 — Gemini 3.8 Flash watches each
  render and produces the candidates; this clerk adjudicates them.
* **Date**: 2026-09-02. **Renders**: 45.76 s, 25 fps, all three.
* **Watcher output**: `cands_codexvoice_{split,cutout,whiteboard}.json`
* **Cost**: split $0.2602 · cutout $0.2682 · whiteboard $0.2398 = **$0.7682**
* **Wall clock**: 211 s / 205 s / 205 s (run in parallel → **~211 s for the video**)

| render | candidates | CONFIRMED | dismissed | verdict |
|---|---|---|---|---|
| youtube / **split** | 6 (+2 clerk-originated) | **8** | 0 | **HOLD** |
| tiktok / **cutout** | 4 | **4** | 0 | **HOLD** |
| reels / **whiteboard** | 2 | **2** (1 pending a ruling) | 0 | **HOLD** |

---

## youtube / split — HOLD

### NO-SENSE table (CONFIRMED)

| id | window | klass | claim | what I measured |
|---|---|---|---|---|
| C1 | **15.75–16.20** | cramp_overlap_clipping · **motion** | the takeaway cup and the phone collide; the phone's left border truncates the cup | decoded 15.60 / 15.80 / 16.00: at 15.60 there is a visible gap, at 15.80 the cup's right edge **touches** the phone border, at 16.00 the phone body **cuts the cup's right side off**. Zero clearance. Watcher said "held"; it is a motion collision — **class corrected** |
| C2 | **19.10–20.00** | picture_contradicts_sentence · held | the label `ANYWHERE` is welded under a monitor with a diagonal strike through it, so the block reads "ANYWHERE ✗" | the word "anywhere" is spoken 19.10–19.76 and the label lands under the **struck-out** monitor. Held on the split to 20.0 and, on the cutout, to 28.0 (watcher saw it in 3 of 5 windows). The sentence argues *you can work anywhere*; the picture crosses that word out |
| C3 | **25.67–28.00** | contradictory_labels · held | the chat-bubble stack carries `THE FIRST PROMPT` and `A DISCUSSION` at once | both labels settled together for **2.3 s** ≥ 1.5 s. Decoded at 26.5: two labels, one object |
| C4 | **35.60–38.00** | empty_zone · held | the desk monitor's screen is blank | zone-ink scan of the screen interior: flat (std 0.00) **35.6→38.0 = 2.4 s** ≥ 1.5 s |
| C5 | **38.50–38.80** | cramp_overlap_clipping · **motion** | a second Codex mark travels out of the phone and is cut by the phone's right border | decoded 38.50 / 38.65 / 38.80: at 38.65 the travelling mark straddles the border; at 38.80 two marks are present, one clipped. This is the class Miguel named explicitly ("cut in half while moving — it has motion") |
| C6 | **38.80–40.80** | empty_zone · held | the desk monitor's screen is blank again | ink scan: flat **38.8→40.8 = 2.0 s**. Watcher said "to 41.33"; **window corrected** |
| **K1** *(clerk-originated)* | **28.60–32.60** | empty_zone · held | the desk monitor's screen is blank for **4.0 s** while the `VERIFY` arrow lands on it | ink scan: flat 28.6→32.6, content enters at 32.6. **See the note below — this is the disputed 31.3 s item and it carries a dissent** |
| **K2** *(clerk-originated)* | **21.00–23.50** | uneven_baselines · held | `YOUR PHONE` sits a full line below `ANYWHERE`, and later below `THE FIRST PROMPT` | decoded 21.50 and 22.80: the three labels in one row settle on visibly different baselines. **The watcher missed this on this run** (it found it in a chunked-only configuration during calibration) — recorded as a watcher miss, not as a clerk win |

### DISMISSED table

*(none — every candidate on this render survived adjudication)*

### Note on K1 — what is actually on the monitor between 29.8 and 32.6 s

The measurement is not ambiguous: the **screen interior** of the drawn desk
monitor is perfectly flat, std 0.00, from **28.6 s to 32.6 s** — 4.0 s — and the
first content (a grey application window) enters at **32.6 s**.

What IS on that monitor across that window: its own black rounded-rectangle
**bezel**, its **stand**, the black **desk line** under it, the printed label
**`YOUR DESK`** directly below it, and the orange **`VERIFY` arrow** terminating
on its left edge. So the arrow does **not** point at nothing — it points at a
fully drawn, correctly labelled desk monitor, and the picture argues the sentence
("you'll have to come back to your desk to verify") perfectly well.

Both readings are true and they are about different things: the **object** is not
blank, the **screen** is. The v2 clerk wrote "points at a blank monitor", which
overstates it; the honest row is "the monitor's screen is empty for 4.0 s".
Whether an idle screen on an unattended desk is a dead slot or the correct picture
of an unattended desk is Miguel's call, not this clerk's — it is logged as
CONFIRMED because the law as written says >= 1.5 s of an empty container is
NO-SENSE, with the dissent stated here.

---

## tiktok / cutout — HOLD

| id | window | klass | claim | what I measured |
|---|---|---|---|---|
| C1 | 18.00–28.00 | cramp_overlap_clipping · held | the outer voice arc from the phone overlaps and is clipped by the monitor's left bezel and stand | held for 10 s. Same defect Miguel confirmed on the split at 18.55 ("arcs overlapping the monitor", held 17.8–22.0) |
| C2 | 19.10–28.00 | picture_contradicts_sentence · **blocking** | `ANYWHERE` labels the struck-out monitor | as split C2, but held here for 8.9 s. Seen in **3 of 5** watcher windows |
| C3 | 25.67–28.00 | contradictory_labels · held | two labels on the chat bubbles | as split C3 |
| C4 | 38.45–38.85 | cramp_overlap_clipping · **motion** | the travelling Codex mark collides with the stationary one and crosses the phone border | as split C5 |

**DISMISSED**: none.

---

## reels / whiteboard — HOLD

| id | window | klass | claim | what I measured |
|---|---|---|---|---|
| C2 | **25.75–26.10** | cramp_overlap_clipping · **motion** | the pencil body is drawn straight across the finished label `THE FIRST PROMPT` | decoded at 0.2 s steps 25.4→26.4: clean at 25.4 and 25.6; at **25.8** the pencil sits on `THE`/`F`; at **26.0** its body crosses `PROMPT` while its tip writes `A DISC…` **below**; clear by 26.2. Duration **~0.35 s**. Watcher claimed "held to 28.0" — **window corrected**. Not covered by accepted-behaviour #5: the pencil is drawing `A DISCUSSION`, a *different, already-finished* block is the one it crosses. **This also settles the v2 dissent**, where the old verifier said "the pencil does not overlap or touch the letters" — it does, at 25.8–26.0 |
| C1 | 4.40–7.00 | named_tool_no_mark · held | "Android" is spoken at 1.72–2.04 and no Android mark is ever drawn | confirmed from the pixels: the board carries the heading `CODEX VOICE`, a phone with the Codex mark, and later a monitor with the Codex and Claude Code marks. **No Android mark at any point.** Grace expired at 4.04 s. **CONFIRMED — PENDING A RULING**, see below |

**DISMISSED**: none.

### The whiteboard Law-2 question (raised on three of four videos)

The watcher raised `named_tool_no_mark` on the whiteboard of **three separate
videos** — `codexvoice` (Android), `deepseekflash` (Opus), `codexnondev` (Codex).
That is not three defects, it is one chassis question:

> On the whiteboard, does the **handwritten name** satisfy LAW 2, or does the beat
> still need the real registry **mark**?

The whiteboard chassis has its own LABEL LAW ("every drawn object gets its word
written beside it") and there is **no written Law-2 exemption for the board**.
Applied literally, LAW 2 is violated on every whiteboard that names a tool it does
not draw a logo for. One ruling from Miguel closes all three rows at once, and the
answer belongs in `formats/whiteboard/CHASSIS.md`, not in three separate autopsies.
Recorded here rather than chased (STOPPING RULE).

---

## PHONE TEST

The batch-2 crop sheets `phone_codexvoice_{split,cutout,whiteboard}.png` were
produced under the **old** manifest contract, which carried
`builder_intended_name` in the same file as the blank answer slot. That contract
was changed on 2026-09-02 (`phone_crops.py` now writes a sealed
`phone_<label>.key.json`), and these sheets predate the change, so this clerk did
not re-run a Phone Test it could not run blind. The v2 clerk's cold answers on the
same ten crops stand at **10/10 PASS**; nothing in this pass touched a bespoke
object's design, so no re-judgement is owed. The next batch is judged under the
sealed-key contract.

## Fix list

1. **split + cutout, 15.75–16.20** — give the coffee cup real clearance from the phone's bounding box.
2. **split + cutout, 19.10–28.00** — `ANYWHERE` must not label the struck-out monitor. Move the label to the phone, or strike the desk without naming the new state on it.
3. **split + cutout, 25.67–28.00** — one object, one label. `A DISCUSSION` replaces `THE FIRST PROMPT`; it does not join it.
4. **split + cutout, 38.45–38.85** — route the travelling mark clear of the phone's border.
5. **cutout, 18.00–28.00** — separate the voice arcs from the monitor bezel and stand.
6. **split, 28.60–32.60 / 35.60–38.00 / 38.80–40.80** — put something on the desk monitor's screen, or rule that an idle screen is the intended picture (see K1).
7. **split, 21.00–23.50** — put the three friction labels on one baseline.
8. **whiteboard, 25.75–26.10** — route the pencil so it does not cross a finished block while writing a new one.
9. **whiteboard, Law-2 question** — awaiting Miguel's ruling, not a fix.
