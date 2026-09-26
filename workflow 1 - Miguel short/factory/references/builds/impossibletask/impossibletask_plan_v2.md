# impossibletask — PLAN v2, the semantic rebuild

*Written BEFORE any code, 2026-09-01, after Miguel rejected v1 and the frame-by-frame
autopsy scored it 10 SENSE / 17 NO-SENSE (`review/impossibletask_autopsy.md`).*

## The design rule this rebuild is under

**Every beat is a picture of the sentence being spoken.** Not a mood, not a
motif, not a decorated instrument. If you pause the video anywhere and read the
caption, the top half must be showing you that caption. Everything below follows
from that single test, and nothing in this plan exists because it looked good.

## What v1 got wrong, in one line each

1. The hook object (a 3D-printer build plate as stacked bars) read as **pancakes**.
2. The subject of the story is a **monitoring system**; v1 drew the **printer**.
3. The **key term never appeared** — "impossible task" is spoken at 0.9 s and printed nowhere.
4. The big comparison put a **duration** ("ONE NIGHT") next to a **capability** ("WHAT THEY CAN DO").
5. Restraint was drawn as **square brackets**; night as a **34 px speck**; dawn as a **grey dot**.

## The cast of v2 — five objects, all plain, all self-evident

| object | what it is | why it exists |
|---|---|---|
| **THE JOB CARD** | a sheet of paper with a job written on it, stamped **IMPOSSIBLE TASK** | the thing you hand over. Law 9's key term IS the object (Law 20: it arrives already written on, never blank) |
| **THE MOON** | a big crescent, r = 62 px, not a speck | "before you head to bed" / "before he even got to bed". Plain, literal, one meaning |
| **CODEX** | the real product mark (Law 2, Law 35) | who you handed it to |
| **THE SCREEN** | a rounded panel with two labelled readout rows, wired to a small printer | **the thing Codex actually built.** The story's noun is *monitoring system*, so the picture is a screen that watches, and the printer is the thing it watches |
| **THE TWO BARS** | same width, same baseline, flat tops (Law 34) — `WHAT WE ASKED FOR` short, `WHAT IT CAN DO` tall, held down by a **lid** | the widening. Both bars measure the same thing (how much work), so their heights are comparable — v1's fatal defect, fixed |
| **THE RAIL + FLAG** | a track, a flag at the end, and the Codex mark riding it as the agent | "goes all the way to the end of its mission". `/goal` is what gets the marker to the flag |

The X mark appears at the word "X", the Codex mark at the word "Codex" — Law 2 is
satisfied at the syllable, not somewhere nearby. **Zero third-party assets**
(no tweet): the take quotes nothing from the post, so Law 3 permits none and the
grokpublish precedent applies.

## Beat map — every edge is a word start from `transcript_tight.json`

**12 beats, up from 10.** `b0` and `b11` are new, and they exist for a reason
that is now a law: *the takeover may only switch at a beat boundary*, so any beat
the face wants to take must be a whole beat. Splitting b1 and b10 is what lets
the face own the personal instruction and the sign-off without ever cutting a
visualization mid-build.

| # | in | out | spoken words | what is on screen | why it argues the sentence |
|---|---|---|---|---|---|
| **b0** | 0.00 | 0.92 | "Start giving AI" | the JOB CARD lands centre stage, already carrying three written lines | you are being handed a *written job*. It arrives loaded, never an empty outline (Law 20) |
| **b1 HOOK** | 0.92 | 2.72 | "impossible tasks before you head to bed." | at `impossible` (0.92) a terracotta band stamps **IMPOSSIBLE TASK** across the card; at `bed.` (2.22) a big moon rises top-right and the card displaces left to make room | the key term debuts centre stage, large, on its own word (Law 9). The displacement IS the story: night arrives, the job moves aside for it (Law 19) |
| **b2** | 2.72 | **4.64** | "Like this guy right here on X," | card left, moon top-right; at `X,` (3.76) the **real X mark** docks under the moon | he names the platform, the platform appears (Law 2) |
| **b3** | **4.64** | 8.54 | "who asked Codex to build a full-blown monitoring system for his 3D printer." | the beat OPENS on the word `Codex` with the **Codex mark already visible, centred and alone** (the cut is the entrance); `build` (5.16) it displaces left as the panel settles beside it, then a wire draws from the mark and terminates AT the panel's left edge (Law 7); `monitoring#1` (6.42) the two labelled readout rows arrive inside the panel, tracks still empty; `3D#1` (7.62) a small **printer** appears at the right and a short link joins screen → printer | the sentence read left to right: *Codex → built → a screen that watches → this printer*. Law 19: the mark appears centred, then MOVES because the next item needs the room. The screen's empty tracks are a promise b5 keeps (Law 16) |
| **b4 PEAK** | 8.54 | 11.96 | "And before he even got to bed, the system was already built," | screen + printer, centred; `before#2` (8.78) the moon travels one short arc left→right overhead; `bed,` (9.98) it lands; `built,` (11.48) a big terracotta **check stamps onto the screen** and its border goes solid | night passes over the thing being built, and when the night lands the thing is done. Hook object and payoff object are the same screen (Law 13) |
| **b5** | 11.96 | 16.70 | "fully integrated with temperature monitoring, as well as progress monitoring on his 3D printer." | `temperature` (13.14) the TEMPERATURE track fills; `progress` (14.72) the PROGRESS track fills to full; `printer.#2` (16.24) the screen→printer link and the printer tick together | the readings he names appear in the readouts he can see, and the tick says where the numbers come from. Meters complete (Law 23: one continuous pill, no square ends) |
| **b6** | 16.70 | 20.62 | "Now, the capacities of these models are way beyond anything that we can imagine," | `Now,#1` (16.70) the finished screen contracts into a short flat-top bar labelled **WHAT WE ASKED FOR**; `capacities` (16.98) a far taller bar grows on the same baseline, stopping inside the frame; `models` (17.92) its label **WHAT IT CAN DO** lands | two bars, one baseline, one axis — *how much work*. What we asked for was one night's job; what it can do is the taller bar. v1 compared a duration to a capability; this compares like with like |
| **b7** | 20.62 | 25.38 | "so it's always good to let them loose every once in a while to see their true potential." | both bars inherited at their exact seats; `so` (20.62) a heavy ink **LID** fades in sitting on top of the tall bar; `let` (21.64) the lid lifts clear and fades; `loose` (22.06) the bar **surges past the top of the block** behind an alpha fade (Law 27 — the only edge-cut element in the build) | a lid on top of something is self-evidently holding it down; taking it off is self-evidently letting go. No symbol needs a key |
| **b8** | 25.38 | 29.44 | "If you want to make sure your AI goes all the way to the end of its mission," | `If` (25.38) a rail with **THE JOB** at its head and a **flag** at its far end; `your` (26.26) the **Codex mark** appears on the rail as the agent; it steps at `goes` (26.82) → 30 %, `way#2` (27.52) → 56 %, `end` (27.98) → 76 % and **STOPS SHORT of the flag** | the agent walking a track toward a flag is a journey with an end. Stopping short is the exact problem the next beat solves (Law 16: the gap is a promise) |
| **b9** | 29.44 | 37.92 | "you have to use the /goal command that will make sure that it will actually verify all of the work that it did for you, as well as test all of the applications that it built." | `/goal` (30.26) the mono chip debuts **centre stage and alone**, large; `command` (30.90) the rail returns below it, inherited at 76 % with its marker and flag; `verify` (33.12) a VERIFY card ticks; `test` (35.84) a TEST card ticks; `built.` (37.32) the marker runs to the flag, the fill completes and the flag goes solid | the payload term gets the Law-9 treatment of its own. Then the two things the command does are shown doing them, and the rail that stopped short finishes — the command is visibly what closed the gap |
| **b10** | 37.92 | 39.36 | "Now, follow for more AI news" | the finished screen, small, centred, both readouts full, check on it; a terracotta rule grows under it | the outro object is the video's own payoff, not chassis furniture (Law 10) |
| **b11** | 39.36 | 41.64 | "and tutorials each and every single day. See you" | mark + rule inherited; the handle chip and "daily AI" arrive beneath, one centred column on the axis | outro alignment law: nothing points at anything that is not there. The handle is the **platform parameter** — `@migueltorrezai` for YouTube, `@migueltorrez.ai` for TikTok/Reels |

## The three renders

| format | zone | placement | notes |
|---|---|---|---|
| **split** (YouTube, `HANDLE_YT`) | top zone `0..862.5` | block at the derived `SPLIT_BLK_Y`, scale 1.00 | 12 sections, one per beat |
| **takeover** (Reels, `HANDLE_TIKTOK_IG`) | full frame above the 1318 pill seat | block centred, scale 1.08 | see the cut map below |
| **cutout** (TikTok, `HANDLE_TIKTOK_IG`) | the derived stage zone | block centred, scale 1.00 | **stage content only** — the lanes, depth band, matte and background belong to the sibling rebuild |

### NEW LAW (2026-09-01): the takeover switches ONLY at beat boundaries

v1's cut map switched from face to scene at **0.92 s**, which sits *inside* beat 1 —
so the Reels viewer never saw the job card arrive, only the second half of a build
already in progress. From now on every entry in a takeover cut map is a whole
scene beat. Beats are split at the plan stage if the face wants a shorter unit.

```
face  0.00–0.92   (b0)   |  b1  0.92–2.72   |  b2  2.72–4.64  |  b3  4.64–8.54
b4    8.54–11.96         |  b5  11.96–16.70 |  face 16.70–20.62 (b6)
b7    20.62–25.38        |  face 25.38–29.44 (b8)             |  b9  29.44–37.92
face  37.92–39.36 (b10)  |  b11 39.36–end
```
Face 10.34 s = **24.8 %**, longest run 4.06 s, every edge a word start AND a beat edge.
The two dropped beats are safe to drop because **b7 inherits both bars from b6 at
their exact seats and b9 inherits the rail from b8 at 76 %** — the cast carries
forward across the cut instead of being re-staged, which is the same mechanism
that let v1 drop b6.

## Audio (unchanged)

Voice = `cuts/impossibletask/audio.m4a` (48 kHz stereo, the cut master's own track);
`analysis_16k_mono_DO_NOT_MIX.wav` is never a mix source. Bed
`assets/music/bed_split_v2.mp3` at 0.065. SFX at the Law-22 classes
(structure 0.120 / detail 0.077 / loop 0.038), every cue frame-locked to its event.


---

## Amendments made during the build (all found by the Viewer Test, not by a gate)

The first v2 render was decoded frame by frame before staging, and it failed its
own gate. Five changes, each one a defect class worth naming:

1. **b2 now runs to 4.64, not 4.06.** b3's first element popped on "Codex"
   (4.64) while the beat opened at 4.06 — 0.58 s of empty stage under "who
   asked". **A beat edge must land on the word its first element answers.**
2. **b3 opens with the Codex mark ALREADY VISIBLE, centred.** A beat that starts
   exactly on its anchor cannot also pop its first element from opacity 0: the
   cut is the entrance, and the tween only scales.
3. **b9 inherits b8's rail at its exact seat** (same y, same fill, same marker)
   instead of fading it in at "command" — that fade left 0.82 s of nothing under
   "you have to use the". The rail now holds one seat from 25.38 s to 37.92 s and
   `/goal` drops in above it.
4. **An unstarted track shows nothing.** LAW 23's `min-width` anti-sliver floor
   renders a 26 px terracotta dot on a track that has not begun, and the Viewer
   Test read it as a rendering artifact — on the rejected render AND on this one.
   The fill now carries `opacity:0` until its own word.
5. **The tall bar grows on "capacities" (16.98), not "beyond" (18.92)**, and is
   named on "models" (17.92). The original timing left half a comparison alone in
   an empty field for 2.2 s while he described the thing it was a picture of.

Plus: the outro mark drops its 14 px row labels (LAW 8 — at 0.62 scale a 23 px
label is decoration, not a label) and thickens the two bars instead. It is a MARK
of the finished screen, not a readable dashboard.

---

## AMENDMENT v3 (2026-09-01) — THE MOON IS DEAD, AND THE RULE THAT KILLED IT

Miguel, on the v2 renders: *"for every single impossible task video, the moon
makes no sense. It's not clear, it's ugly as shit."*

### What replaced it

| | v2 | v3 |
|---|---|---|
| the overnight object | a crescent MOON, r = 62 px, rising at `bed.` and traversing left-to-right at `before#2` | an **ANALOG CLOCK**, r = 94 px, with a face, twelve ticks, two hands and a terracotta pin — plus the hour **written under it**, `11 PM` -> `7 AM` |
| the motion | the moon crossed the frame | the **hands sweep**: the hour hand runs 11 -> 7 (240 deg), the minute hand turns three times under it, over 1.16 s, and it LANDS on the word `bed,` |
| why | a crescent is a CONVENTION — the viewer has to accept "crescent = night" before the picture means anything, and at 405 px of phone width a 124 px crescent is a grey comma | a clock is an OBJECT. Nobody is taught it. And the label says the half a clock cannot: which night, and that it ended |

### The rule this rebuild makes standing

**A bespoke object ships only after it has been rendered ALONE at phone scale
and named cold.** Phone scale = the finished frame downscaled to 405x720, the
object then cropped out of *that* downscaled frame — never re-rendered at a
convenient size. The crop is written to disk and travels with the build.

For this object: `review/legibility_impossibletask_overnight.png`
(83 x 104 px at 1:1, shown beside the same pixels at 4x, for three states:
`11 PM` in the split, `7 AM` in the split, `11 PM` in the cutout).
The word it draws cold is **"a clock"**.

### The knock-on geometry

The clock owns the right column (778..966 px in the scene block) from `bed.`
onward, so **b4 and b5 re-seat the rig at the content column's left margin**
(x = 90, spanning 90..694). v2 centred the rig and flew the moon over it; with a
188 px clock face standing still, a centred rig's printer would collide with it.
Every other beat of v2 is untouched — Miguel rejected the moon, not the build.

### One defect found while shooting the evidence

The v3 contact sheet caught a **clip-boundary ghost** that has been in every
render this factory ever shipped: the producer holds a clip on screen INCLUSIVE
at both ends, so two back-to-back clips both render on the frame their shared
boundary lands on. Decoded: frame 706 of the split read
`"tl  of its mission,  d"` (two caption pills stacked), and frame 116 of the
cutout still showed the job card, the clock and the X mark standing behind b3's
Codex mark. Cured with `CLIP_EPS = 0.02` — every clip that hands over to another
ends half a frame early, which cannot open a hole because a 0.02 s window inside
a 0.04 s grid can never contain a frame time.

### Reels is no longer a takeover

The **takeover renders for Reels are retired** (moved to
`projects/impossibletask_takeover/_retired/`). Reels now ships the
**WHITEBOARD**, the lab's definitive plan view — see
`gen/impossibletask_whiteboard.py`.
