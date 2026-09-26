# THE VIEWER TEST — the semantic gate (procedure **v3.1**, 2026-09-04)

*v1 added 2026-09-01, after Miguel rejected `impossibletask`: "The visualization
makes literally no freaking sense. Were there even clerks in this loop?"*

> ## WHAT CHANGED IN v3.1 — THE CLERK STOPS RE-WATCHING THE SAME FILE
>
> *Miguel, 2026-09-04, on the run-13 debrief: **"remove the pure duplication in
> the second watch"**.*
>
> `render_and_check.py` already runs the Gemini watcher on **each staged file the
> moment it lands** — same script (`clerk_video_gemini.py`), same model, same 720×1280
> encode, same media resolution, same prompt, same beat-log-before-accusation
> discipline — and writes the candidates to **`<run>/review/cands_<id>_<fmt>.json`**.
> The clerk then ran that identical call on those identical bytes again, into
> `clerk_cands_<id>_<fmt>.json`, at **$0.10–0.15 a video**. It was not a second
> opinion; two runs of one deterministic-enough pipeline on the same file is one
> opinion billed twice.
>
> **So in v3.1 the clerk READS `cands_<id>_<fmt>.json` instead of producing it.**
> Step 1 becomes a read, not a call. Everything else about the clerk is unchanged:
> it is still fresh, still cold, still forbidden the plan, it still adjudicates
> every row against the law text and the known-and-accepted list, and **its own
> frame decode is still mandatory** — because that is the half that works. Run-13
> recall: the watcher found **0 of the 2** real defects and the clerk's own eyes
> found **both**, plus one watcher false positive. The watcher is a cheap first
> filter over a file nobody has looked at yet; the ruling has always been the
> clerk's.
>
> Two handling rules come with it:
>
> * **Read the watcher's BEAT LOG, not just its candidate rows.** It is the
>   watcher's account of what is on screen against what is said, and a defect it
>   did not accuse frequently sits in its own description.
> * **A missing `cands` file is reported, never backfilled.** If a staged render
>   has no candidate file, that render was watched by nothing: say so and
>   adjudicate it on your own decode alone. Do not run the watcher to fill the
>   hole — that is the duplication coming back through the side door.
>
> The one place a fresh watch is still legitimate is a render **no
> `render_and_check` ever watched** (a hand-render, a repair staged outside the
> driver). Then it is not a second watch, it is the first one.
>
> ### And the Phone Test now runs TWICE, at two different costs
>
> A **COLD PHONE NAMER** (`prerender/phone_test_page.py` → a fresh cheap agent that
> receives only the crop images) names every bespoke object **before any render is
> paid for**, and the author scores those names against the sealed key and
> redesigns on a failure — at most two rounds, then it renders anyway and flags the
> file. See STANDARD.md → *RUN-13 REVIEW CHANGES*. The clerk's Phone Test in §3
> below is unchanged and still binding: it judges the **delivered file**, at three
> words, and it does not read the pre-render scoring or the flag file until its own
> answers are written. A cold-read failure that survived two redesigns is a
> different animal from a fresh one, and the clerk says which it is looking at.

There was a clerk. It measured edge fades, audio bands, pixel ratios, pill
heights, face high-frequency ratios and sync lag, and every one of them was
green. The render argued nothing. **Every gate the factory had was an
instrument, and no instrument decodes a picture against the sentence it is
supposed to be arguing.** This file is the gate that does.

---

## WHAT CHANGED IN v3 — THE ROLES ARE FLIPPED

v2 had the clerk sample still frames, produce candidates, and send them to a
Gemini verifier for a CONFIRMED / TRANSITION / REFUTED ruling. Both halves were
measured on 2026-09-02 and they measured very differently.

| half | evidence | verdict |
|---|---|---|
| the still-frame clerk producing candidates | two independent runs on the same `codexvoice` render returned **two different lists**; it missed **4 of the 6** defects Miguel confirmed by eye; it raised several things the factory does **on purpose** (the Claude Code pixel mascot, tiles occluded by the cutout silhouette, the whiteboard pencil on the type it writes) | **unstable — retired as the source of candidates** |
| the moving-clip Gemini verifier | agreed with Miguel **5 / 5** on the flags he ruled, cold, never told his rulings | **reliable — promoted** |

The reason is structural, not a matter of one agent being sloppy. **Every defect
class in the STANDARD is defined over a window of time** — "empty for >= 1.5 s",
"still absent 2 s after the word", "held", "while moving". A reviewer looking at
one frame cannot evaluate a single one of them; it has to guess, and two honest
guessers guess differently.

So in v3:

> **The watcher model (STANDARD -> VISUAL VERIFICATION MODEL; pinned in `clerk_video_gemini.py`) WATCHES THE WHOLE VIDEO and produces the candidate list.
> The Opus clerk ADJUDICATES that list against the laws, and runs the Phone
> Test.**

The clerk stops guessing *where to look*. It starts doing the two things it is
genuinely better at: applying the law text to a **named window** it can decode
frame by frame, and knowing what this factory does **on purpose**.

Still-frame sampling is **not** the source of candidates any more. It survives
only as an **optional spot-check** (§5) when the clerk wants to see a specific
instant for itself.

---

## The one question

> **Does the picture argue the sentence being spoken?**

Not "is it well made", not "is it on brand", not "does it follow the laws" —
those are the other gates' jobs. This gate asks whether a stranger holding a
phone, seeing this for the first time, at speed, with no plan document, receives
the thing the sentence is saying.

## When it runs

**On EVERY video of a daily batch, and on ALL THREE staged renders of each
video** (2026-09-02: the batch-2 clerk had to ask). Instruments can be sampled
because a defect in one build's geometry is usually a defect in the chassis.
Meaning cannot be sampled: every video argues a different thing, and every format
argues it differently. The evidence is in the file — the whiteboard's only
confirmed defect did not exist on the split, and the cutout carried one that no
other format had.

**One video = three Gemini calls (split, cutout, whiteboard) and one clerk report.**
Since v3.1 those three calls are the ones `render_and_check` already made as each
file landed; the clerk adds none.

**The builder does NOT run it** (THE INDEPENDENCE RULE below). A fresh clerk per
video runs it, and it is the FIRST thing that clerk does — a render that fails
the Viewer Test is held, and no instrument reading is worth collecting on a video
that does not make sense.

## THE INDEPENDENCE RULE (Miguel, 2026-09-02)

**Self-review is not a gate.**

The Viewer Test is administered by a FRESH agent that has never seen the plan,
the generator, the beat map, or the builder's reasoning. It receives exactly
three things:

* the **staged MP4s**,
* the **tight transcript** (`cuts/<id>/transcript_tight.json`), and
* the **Phone Test crop sheets** plus their blank manifests.

Nothing else. It is explicitly forbidden from opening the project's `index.html`,
its `*_gen.py`, its plan markdown, its paperwork, any autopsy the builder wrote,
or a Phone Test **answer key** before it has written its own answers. If it reads
them, the test is void and must be re-run by a different agent.

**Why.** On 2026-09-02 Miguel rejected a bespoke "moon" object that was
illegible and ugly at phone size. The Gemini gate never judges that class of
defect, and the Viewer Test did not catch it either — because the BUILDER ran the
Viewer Test on its OWN work. A builder cannot un-know its plan. It looks at an
orange crescent and its own intent supplies the word "moon", so the frame reads
as SENSE to the one agent in the world for whom it is guaranteed to.

A builder is of course free to LOOK at its own render and fix what it sees —
that is craft, and it is encouraged. It just does not count as a gate, it is never
reported as a Viewer Test verdict, and it never substitutes for the clerk's pass.

---

## Procedure

### 1. READ THE WATCHER'S CANDIDATES — DO NOT RE-RUN THE WATCHER (v3.1)

**Since 2026-09-04 the clerk's step 1 is a READ.** `render_and_check.py` watched
every staged file as it landed and left the list at

```
<run>/review/cands_<id>_<fmt>.json      # one per staged render
```

Read all of them, rows **and beat logs**, and quote each file's own `cost_usd` and
wall clock — money the clerk did not spend. A staged render with no `cands` file
was watched by nothing: report that and rule on your own decode alone. **Do not
run `clerk_video_gemini.py` on a file `render_and_check` already watched** — same
script, same model, same encode, same prompt, same bytes, twice the bill (v3.1,
above).

The rest of this section is how the watcher *behaves*, and it still matters:
it is what produced the list you are reading, and it is what you run when a
render exists that **no driver ever watched** (a hand-render, a repair staged
outside `render_and_check`). In that case only:

**Run the batch runner. Do not loop over the renders.**

```bash
$PY $F/pipeline/clerk_video_batch.py <id> --day <date>
# -> cands_<id>_{split,cutout,whiteboard}.json + one combined summary
```

It reads the three staged renders out of `<run>/staging/{youtube,tiktok,reels}/`,
runs them **concurrently** (`--render-jobs`, default 3), and each of them runs its
own four windows **concurrently** (`--jobs`, default 4). Twelve independent calls
are in flight instead of twelve laid end to end. To watch one render on its own,
`clerk_video_gemini.py` still takes a single file and parallelises its windows:

```bash
$PY $F/pipeline/clerk_video_gemini.py \
    "<run>/staging/youtube/<id>_split.mp4" <id> \
    --fmt split --out <run>/review/cands_<id>_split.json
# --jobs 1 reproduces the pre-2026-09-02 serial behaviour; nothing else does
```

#### WHY IT IS PARALLEL (measured 2026-09-02, and the reason this rule exists)

Every window is its own encode, its own upload, its own prompt and its own
response, and the union happens afterwards in `merge_passes`. **Nothing in this
procedure ever required them to be serial** — two nested `for` loops did. Each
unit spends 30-60 s waiting on the network, and a serial runner spends that time
doing nothing.

| what was measured | serial (`--jobs 1`) | parallel (`--jobs 4`) |
|---|---|---|
| `codexvoice_split`, 4 windows | **236.5 s** | — |
| `codexvoice_cutout`, 4 windows | **611.0 s** | — |
| `codexnondev_split`, 4 windows | 158 s *(batch-2 report)* | **96.8 s** |
| `codexnondev_cutout`, 4 windows | 166 s *(batch-2 report)* | **57.6 s** |
| `codexnondev`, 2 renders / 8 windows | 324 s (sum) | **97.7 s — 3.3x** |
| the 5-render clerk-v3 repair pass | **> 50 min, still unfinished** | — |

**Cost is identical.** Concurrency changes *when* the tokens are spent, not how
many: the same renders, the same windows, the same media resolution, the same
model. `codexnondev`'s two renders cost $0.3242 either way.

The one thing concurrency does introduce is simultaneous 429/503s, and
`clerk_video_gemini.generate_retry` absorbs those with a bounded back-off that
re-uses the file already uploaded — a retry costs one call's input tokens, never
a re-encode or a re-upload.

*(Written after the 2026-09-02 repair pass: five renders watched one after another
took over fifty minutes of wall clock for about seventeen minutes of billed work,
and the clerk spent the difference waiting.)*

The script re-encodes the render to 720x1280 **with audio**, uploads it, and asks
`gemini-3.5-flash-lite` (Miguel's pick 2026-09-03; the v3 calibration below was measured on 3.8-flash) — at **HIGH media resolution, 3 fps** — to do two things in
order:

1. **the BEAT LOG**: walk the whole duration and write what is on screen, what is
   said, which marks are visible and which labels are printed, in ~2-5 s rows with
   no gaps. *Describe before you judge* (STANDARD, VISUAL QUALITY CHECKS §5): a
   model asked only for violations will answer "none" about a frame it never
   parsed.
2. **the CANDIDATES**: one row per problem, each carrying
   `{t_start, t_end, on_screen, said, claim, klass, severity, motion_or_held}`.

It is given the compact defect definitions (each stated as a **window test**) and
the **KNOWN AND ACCEPTED** list — the behaviours this factory ships on purpose.
Both lists live in the script and are the single source of truth for them.

**Media resolution is the parameter that decides recall.** At the SDK default
(LOW) a 46 s short goes up as ~10K tokens and the model cannot see a cup touching
a phone border: measured recall on the calibration video was **1/5**. At HIGH the
same render is ~41K tokens and the collisions become visible. Do not "save money"
by lowering it; the saving is a few cents and the cost is the gate.

`t_start..t_end` is the **window over which the wrongness is true** — not the beat,
not the instant. That is the whole point: the clerk gets a window it can decode,
instead of a guess it has to re-derive.

### 2. ADJUDICATE EVERY CANDIDATE — this is the clerk's job

For each candidate row, in order:

1. **Decode the window.** `t_start..t_end` is a real window, so sample it
   properly — at least the two ends and the middle, and more where the claim is
   about motion:

   ```bash
   ffmpeg -nostdin -v error -ss <t> -i <render.mp4> -frames:v 1 -vf scale=500:-1 f_<t>.png
   ```

   Judge **whole frames**. Do not crop the visual zone — a cropped extraction
   silently mis-registers on rotated/anamorphic MP4s and you will decode a blank
   field and call it a dead slot.

2. **Apply the law text**, which for every class is a duration test:

   | klass | the test |
   |---|---|
   | `empty_zone` | the zone carries nothing for **>= 1.5 s of settled screen time**. Measure first and last empty frame. A zone bare for 0.3 s between two beats is a transition. |
   | `named_tool_no_mark` | the mark is **still absent >= 2 s after the word ends**. Quote the word's end time and the time the mark becomes legible. |
   | `cramp_overlap_clipping` | either a **HELD** collision (objects stopped, collision still there) **or** a **MOTION** collision (an element crossing into / over / through another object or a border while travelling). Motion never excuses a collision. The row says which. |
   | `contradictory_labels` | both labels settled together for **>= 1.5 s**. |
   | `lingering_mark` | the mark is still on screen while the speech has moved on, and it is not a declared anchor. |
   | `side_label`, `uneven_baselines`, `unaligned_arrows`, `ring_or_box_on_image_text` | geometry, not timing — **no duration test**. Judge them on the settled frame. |
   | `missing_source_post` | cross-check the cue against `$PY $F/pipeline/pointing_cues.py --vid <id>`. |
   | `picture_contradicts_sentence` | the picture must say something DIFFERENT from `said`, not merely add nothing. |

3. **Apply the KNOWN AND ACCEPTED list** (the same list the watcher was given —
   read it out of `clerk_video_gemini.py`, it is one block of text). The watcher
   is told to suppress these, and it mostly does; a row that slips through is
   dismissed here, not argued with.

4. **Mark the row.** Three verdicts, no fourth:

   | verdict | meaning | consequence |
   |---|---|---|
   | **CONFIRMED** | the window holds up against the law text | goes in the NO-SENSE table; **holds the render** |
   | **ACCEPTED-BEHAVIOUR** | real in the pixels, but it is something the factory does on purpose | dismissed table, with the accepted-list item number |
   | **REFUTED** | the claim is wrong about the pixels, or fails its duration test | dismissed table, with the measurement that killed it |

   Every verdict carries a **reason** and, for CONFIRMED and REFUTED, the number
   you measured. "It looked fine" is not a reason.

**A failed duration test IS a dismissal.** (v2 friction #1: §3a said "DISMISSED"
and §3b said "every candidate goes to the model anyway", which cost real money on
candidates already known to be dead.) In v3 there is no second model call at all —
the clerk measures and rules. If the emptiness is 1.2 s, the row is REFUTED with
"1.2 s < 1.5 s" written in it, and nothing else happens.

**Never re-word a claim to chase a CONFIRMED.** If you dismiss a candidate you
privately believe in, say so in the dismissed table's notes and let Miguel
arbitrate — that disagreement is data.

### 3. THE PHONE TEST — object legibility at real size

Unchanged from v2 in substance, tightened in handling.

Every **Law-13 bespoke object** — anything drawn for this video that is not a real
registry logo, a caption, or the face — must survive it.

1. The **builder** emits the crops (it owns the bounding boxes):

   ```bash
   $F/pipeline/phone_crops.py <staged render.mp4> --out <run>/review \
       --label <id>_<fmt> --at "12.4:0.30,0.22,0.70,0.55:moon"
   ```

   The script downscales the frame to **405x720** (a real phone's rendered size
   for a 9:16 short), crops each object **alone**, pastes the crops 1:1 with no
   resampling, and writes three things: `phone_<label>.png` (the sheet),
   `phone_<label>.json` (**the judge's manifest: geometry and a blank answer slot,
   and NO intended name**), and `phone_<label>.key.json` (**the sealed answer
   key**).

   *(v2 friction #7: the manifest used to carry `builder_intended_name` in the
   same file as the blank answer slot — an answer key one `cat` away from the
   judge. Split into two files on 2026-09-02.)*

2. The **fresh clerk** judges. It is shown the crops and nothing else. For each
   crop it writes a name **in five words or fewer** (three until 2026-09-14), into `judge_answer`.
   **It opens `phone_<label>.key.json` only after every answer is written.**

3. **Scoring**, against the key:

   | clerk's answer | verdict |
   |---|---|
   | names the intended thing ("a stack of RAM sticks" for RAM) | PASS |
   | names a different thing ("a stack of pancakes") | **FAIL** |
   | hedges ("some kind of chart?", "an orange shape") | **FAIL** |
   | "I cannot tell" | **FAIL** |
   | needs more than three words to get there | **FAIL** |

4. **A failure is a REDESIGN, not a note.** The object is rebuilt bigger, simpler,
   or labelled, and the render is remade. There is no "add a caption to explain
   it" fix — an object that needs a sentence to be identified has already lost the
   viewer it was drawn for.

**Why three words and no context.** A viewer scrolling gives an object roughly the
time it takes to think one noun. If the honest answer needs a clause, the object
did not communicate; it was decoded. And context is withheld on purpose: with the
sentence in hand a judge will retro-fit any shape to any meaning, which is exactly
the failure mode that let the moon ship.

### 4. Verdict

**PASS = zero CONFIRMED rows. A render with ANY CONFIRMED row is HELD.**

There is no warning tier and no budget. A single frame that argues nothing is a
second of a viewer's attention spent confused, in a format where the whole asset
is forty seconds long. ACCEPTED-BEHAVIOUR and REFUTED rows hold nothing.

A **minor**-severity CONFIRMED row still holds the render. Severity is the
watcher's hint about what a phone viewer would notice; it orders the fix list, it
does not create a pass tier.

### 5. Optional spot-check — still frames, demoted

The clerk may decode any frame it likes, at any time, to settle its own question.
What it may **not** do is turn that frame into a candidate row of its own without
the window test in §2. If the clerk sees something the watcher missed, it raises
it as a new candidate **and adjudicates it under the same rules**, with the
measured window written into the row — and it says in the report that this row is
clerk-originated, so the watcher's recall can be tracked honestly.

If a still frame is sampled to orient, sample it at **boundary + 2.5 s**, not
+1.5 s. (v2 friction #2: three of eleven dismissals in the last run were
animations still landing at +1.5 s; one arrived **2.2 s** after its boundary. The
old number bought less than it claimed.) The clerk does **not** need a beat
boundary list to work any more — the watcher hands it windows — which retires v2
friction #8.

### 6. Write it down

**One file per video: `shorts_run<N>/review/clerk_v3_<id>.md`**, with **one
section per render** (split / cutout / whiteboard) — because three formats ship
and they fail differently. *(v2 frictions #5 and #6.)* Per-render machine output
is `review/cands_<id>_<fmt>.json`, one per Gemini call.

Each render's section carries **two tables**:

1. **The NO-SENSE table — CONFIRMED rows only.** On a hold, this table IS the fix
   list: each row names the window to rebuild and the measurement that convicted
   it.
2. **The DISMISSED table — every candidate that did not survive**, with
   ACCEPTED-BEHAVIOUR (plus the accepted-list item) or REFUTED (plus the
   measurement). Nothing is deleted silently: a dismissal that was wrong has to be
   findable later.

The clerk's return reports, per render: **CONFIRMED n / dismissed m**, the Phone
Test result, the **cost** (the `cost_usd` field of each `cands_*.json`) and the
**wall clock**.

### 7. Cost — the real numbers

*(v2 friction #4: the old text said "typically a fraction of a cent per video",
which was wrong by two orders of magnitude.)*

Measured 2026-09-02 across the full 12-render calibration
(`clerk_v3_calibration.md`), on `gemini-3.8-flash` at HIGH media resolution, 3 fps,
`thinking_level=medium`, whole-video call + overlapping 20 s windows:

| unit | measured |
|---|---|
| one render (25 s short) | **$0.08 – $0.10** |
| one render (40-46 s short) | **$0.18 – $0.27** |
| one video (three renders) | **$0.27 – $0.77**, mean **$0.55** |
| the four-video batch, 45 calls | **$2.20** |
| wall clock, three renders in parallel | **90 – 211 s per video** |

Input is the video (~17K per 20 s window, ~41K for a whole-video call at HIGH /
3 fps); output is dominated by the beat log and by **thinking, which bills as
output** at $3.75/MTok and is most of the bill.

**Two of the knobs are recall dials and must not be used to save money**, both
measured on `codexvoice_split` against its five known defects: at the SDK default
`media_resolution` (LOW) it found **1**; at `thinking_level=low` it found **0** for
half the price. If a batch has to be cheaper, drop `--fps` to 2 or pass
`--no-whole-pass`, in that order.

---

## The rules that make the answers honest

1. **Never use the plan as the answer key.** Decode the frames cold. If you
   re-read the beat plan before judging, you will see what you meant instead of
   what you drew.
2. **Name the object from the pixels.** If the plan says "a 3D-printer build
   plate" and the shapes are stacked black bars, it is **"a stack of pancakes"**.
   This is the single highest-yield rule in the file, and it is why the watcher is
   made to write a beat log before it is allowed to accuse anything.
3. **A symbol that needs a key is NO-SENSE.** Square brackets for restraint, a
   34 px crescent for night, a grey dot for dawn, an unlabelled nozzle for a
   printer — every one of those needed the plan to explain it, and every one of
   them shipped.
4. **Two things compared must be on the SAME axis.** "ONE NIGHT" (a duration)
   next to "WHAT THEY CAN DO" (a capability) is noise however well it is animated.
5. **The key term must be somewhere.** Law 9 is a semantic law: if the video's
   core term is never on screen, the video has no thesis.
6. **A named tool must be on screen AT its word — with a 2 s grace for its
   entrance.** Law 2 failures are almost always timing failures, not omissions.
7. **An empty visual zone that persists >= 1.5 s is always NO-SENSE.** Stillness
   is fine and is explicitly not a defect; *emptiness* is a dead slot.
8. **Judge the story object, not the scenery.** If the sentence's noun is a
   *monitoring system*, drawing the *printer* is drawing the wrong thing.
9. **A candidate is not a defect until a window says so.** The watcher gives you
   the window; measure it before you write the row.

## KNOWN AND ACCEPTED — what this factory does on purpose

The authoritative list is the `KNOWN_ACCEPTED` block in
`pipeline/clerk_video_gemini.py`; it is sent to the watcher verbatim and the clerk
adjudicates against the same text. In summary, none of these is ever a defect:

1. **Entry and exit animations run 1-2 s.** An element arriving is not an element
   missing. Judge where it lands.
2. **The Claude Code pixel mascot IS the Claude Code mark.** Miguel: people
   recognise it. It satisfies Law 2 on its own.
3. **Cutout: the silhouette occludes the world.** Tiles and cards passing behind
   his body and being hidden by it are the format's depth cue.
4. **Cutout: tiles are edge-faded at the frame edges** so the wall reads as
   continuing past the frame. *(A tile sliced hard with no fade, mid-frame, is
   still reportable.)*
5. **Whiteboard: the pencil sits on the type it is writing.** The marker tip is AT
   the ink at the moment the ink is drawn — that is the format's whole mechanic,
   not "a line through printed type". *(A pencil crossing a DIFFERENT, already
   finished block while drawing something else is still reportable.)* — *this
   settles v2 friction #3, which asked for the exemption in writing.*
6. **Whiteboard: ink accumulates and holds.** Held board ink is not a lingering
   mark unless a new chapter has started on top of it.
7. **The caption pill**, one per seam, one size.
8. **The outro handle card** (`@migueltorrezai` on YouTube, `@migueltorrez.ai` on
   TikTok and Reels).
9. **The split seam and the cream palette.** Cream behind an object is background,
   not an empty zone.
10. **The die-cut cream rim** on the cutout, and salmon/cream outlines on drawn
    objects, are house style — not misregistration or a double stroke.
11. **A cross-dissolve superimposes two pictures.** Both scenes are on screen at
    partial opacity for a few tenths of a second and their shapes overlap. A
    collision needs two objects both fully present and both belonging to the same
    picture. *(Added 2026-09-02, when the watcher raised a 0.45 s dissolve on
    `codexnondev` as "a border cutting through four tool cards".)*
12. **A company named as a possessive does not need its own mark.** "Codex,
    OpenAI's coding assistant" names ONE tool. If the Codex mark is on screen,
    Law 2 is satisfied. *(Added 2026-09-02.)*

Adding an item to this list is a decision with a date and a reason, exactly like a
law. Removing one is the same. It is not a place to park an inconvenient flag.

## What this gate does NOT do

It does not check geometry (Gate 1), state coverage or idle motion (Gate 2),
format-law compliance or visual defects (Gate 3), or any instrument (the guards).
It is orthogonal to all of them, which is the point: `impossibletask` was green on
every one of those and scored **10 SENSE / 17 NO-SENSE**.

## Worked examples

* `references/evidence/clerk_v3_calibration/review/clerk_v3_calibration.md` — v3's calibration against seven
  known-real and eight known-false items, with the recall and false-positive
  numbers. **Read this first.**
* `references/evidence/clerk_v3_calibration/review/clerk_v3_codexvoice.md` — a full v3 report over three
  renders.
* the last v2 run (codexvoice, run 9, not archived) is described in the calibration report above; kept
  because its "Friction" section is what v3 was written to fix.
* `references/evidence/clerk_v3_calibration/review/impossibletask_autopsy.md` — the v1 procedure run twice on
  the same video, before and after a rebuild; the "before" table is what an honest
  NO-SENSE row looks like.

## Known watcher false-positive classes for the CLERK (run 12, 2026-09-03)

The watcher's four candidates on run 12 changed nothing; every real fix came from a
pre-render refusal, a contact sheet or Miguel. Two classes recur and the clerk should
adjudicate them with the plan in hand rather than re-flag them:

1. `named_tool_no_mark` when the PLAN delays the mark on purpose (hermeskanban: the Nous
   mark is beat 3's picture and inks once at readable size instead of twenty times at
   7 px; both hermeskanban files flagged it). Check the plan's `lifetimes` / `boards`
   before ruling; a mark held for its own beat is not missing.
2. `ring_or_box_on_image_text` on a BOX over a DRAWN object (astramath's ticked worksheet).
   LAW 38 as amended allows a box on drawn objects and scene type; only a ring, an ellipse
   or a circle, or a box on a RASTER, is a defect. `assert_no_enclosure` on the page
   reports `rasters: []` when there is nothing a highlight could legally target.

Gate 3 (still frames) was RIGHT twice on run 12 (a headless arrow read as "a diagonal
line"; an app window that "appears instantly at full size") and unstable once (a finding
that did not reproduce on a byte-identical re-render). Treat a Gate 3 finding as a
question to decode the frame for, not a verdict.
