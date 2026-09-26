# primeagent — SPLIT AUTHOR NOTES

Written by the SPLIT (YouTube) author on 2026-09-21, after building
`gen/primeagent_split_gen.py` -> `projects/primeagent_split` green on
`prerender_check.py` (7 checks, 0 errors) and `geometry_audit.py --strict`
(0 errors, 0 warnings).

The plan (`plans/primeagent_plan.json`) was built as written. Nothing below
changed a picture the plan decided, except item 1, where a LAW forbids what the
plan asked for. Items 2 to 6 are logged and built as found.

---

## 1. LAW 24 — `ONE SINGLE TOOL` now arrives at 12.32, not 11.62 (THE ONE REPAIR)

**The plan and the module both fire `#key-one-tool` at 11.62**, the start of the
spoken "one". At that instant he has said *one* and has not yet said *single*
(11.98) or *tool.* (12.32), so two thirds of the written key would be readable
before the words that license it. That is LAW 24, NO PEEK-AHEAD, in its plainest
form: content that has not been spoken yet is not visible.

**This page fires it at 12.32**, the START of "tool." — the first instant the
whole key is behind its words, and inside that word's own 1.0 s LABEL_WINDOW, so
LAW 39's time half still holds. The seat, the ink, the size, the 0.28 s entrance
and the 21.50 release are the module's, untouched.

The repair is made on the EMITTED tween string (`repair_tweens()` in the
generator), exactly as the sibling split lane in this run repaired its own two
DOM defects. **No byte of `gen/primeagent_scene.py` was moved.**

**THE CUTOUT LANE INHERITS THIS.** Astra builds the TikTok master from the same
module and will emit 11.62 unless it applies the same one-line repair. The
sibling recording in this run made the identical call on its own three-word key
("ONE SESSION lands on the spoken 'session' ... so the whole key is behind its
words"), so this is the run's settled reading, not a new opinion. Keeping the
two lanes on the same instant is also what LAW 51 asks for.

The exact string, as `build()` emits it:

```
tl.fromTo("#key-one-tool",{opacity:0,y:12},{opacity:1,y:0,duration:0.28,ease:SOFT,immediateRender:false},11.62);
```

replace the trailing `,11.62);` with `,12.32);`.

Verified by eye: `review/shots_primeagent_split/f_keyone_before_12p20.png` shows
the machine with NO key; `g_keyone_after_12p76.png` shows the key seated while
the pill reads "This tool allows it".

---

## 2. Plan beat 2 says the machine comes back LARGER; the module draws it SMALLER

Plan beat 2: *"the machine comes back, **larger**, centred and alone on the
board."* The module seats the hook at `MACH0` k = 1.35 and the chapter-2 machine
at `MACH1` k = 1.05, so the machine on the "only has one single tool" beat is
**22 % smaller** than the machine that opened the video.

Built as the module draws it: `SC.BESPOKE` and the placements are authoritative
for geometry by the handoff's own sentence, the scene is sealed, and re-scaling
it here would break parity with the cutout and the whiteboard.

What it costs, looking at the frame
(`review/shots_primeagent_split/g_keyone_after_12p76.png`): the chapter that
carries the video's central claim is its *emptiest* board — the machine occupies
canvas 318 to 516 of a zone that runs to 741, so roughly 225 px of cream sit
between the machine's feet and the caption pill. Chapter 0 fills the same zone
far better at k = 1.35. If a later pass wants one change to this scene, this is
the one: seat chapter 2's machine at the hook's own k.

---

## 3. `SC.DECLARED_BLOCKS` carries a stale `("shelf", "hammer", "screwdriver")`

No element with the id `shelf` is emitted — the shelf belonged to the draft
where the two tools stood side by side, before the crossed pair took the whole
board (handoff section 9 item 3). The entry therefore binds nothing. The block
that actually ships is `("toolpair", "hammer", "screwdriver")` beside it, and
both tools are additionally rotated and inside a `data-overlap-ok` wrapper, so
neither this build's own LAW 41 sweep nor `geometry_audit` ever needed the stale
row. Logged, not edited: the module belongs to the design seat.

## 4. The module docstring still carries the pre-Miguel HOLD text

`gen/primeagent_scene.py` opens with *"THIS MODULE IS NOT SEALED ... Object 2
(the crossed pair) has failed FOUR independent cold rounds ... and is the reason
this seat returned HOLD"*. That is superseded by
`review/artwork_pass_primeagent.json` (verdict PASS, sealed against the module
and handoff hashes) and by handoff section 4 (*"All three are sealed. Never
redraw them ... Miguel reviewed it himself on 2026-09-21 and accepted it"*).
Prose only — it changes no pixel — so it was left alone. Flagged so the next
reader of that file is not misled into reopening a closed object.

## 5. The machine floats 25 px above the RLM slab it is meant to stand on

Plan beat 5: *"a slab draws underneath it, **the machine standing on it**."*
Measured: `MACH2_BOX` bottom is core y 227.0 and `SLAB_BOX` top is core y 252.0,
so there are 25 core px of cream between the feet and the slab
(`review/shots_primeagent_split/k_keyrlm_29p80.png`). It reads as a machine
hovering over a bar rather than standing on a base. Built as found; the gap is
also what keeps the two elements out of `geometry_audit`'s cramp check without
leaning on their shared `data-block`, so closing it is a design-seat change, not
a format-side one.

## 6. The RLM slab is very low contrast

The slab is `MOUNT` (#EFE7DC) with a `rgba(17,17,17,0.16)` border on a #F6F1EA
cream ground. At phone scale it reads as a pale empty track rather than as a
solid base. It is legible with the `RLM` key under it, so it is not a rejection,
but it is the weakest ink on the board and the one element a stranger's eye
skips.

---

## What this lane did NOT touch

* No connector exists in this scene (`line_svg` is never called by `build()`),
  so nothing was anchored or stamped.
* Neither emphasis is an element — the machine's gantry outline and the three
  tile borders flip their own ink — so zero `data-emphasis` is stamped, which is
  the same reading `geminigems_split` recorded in this run.
* All four `data-label-for` attributes and all six `data-block` lockups are the
  module's; this page verifies them rather than rewriting them.
* The matte, the ship marker and `MATTES_FINAL` belong to the cutout lane. This
  build consumed the CUT and nothing else, and made no Modal call of any kind.
