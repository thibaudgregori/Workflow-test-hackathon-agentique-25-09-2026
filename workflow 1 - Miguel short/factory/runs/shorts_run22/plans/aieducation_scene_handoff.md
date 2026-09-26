# aieducation — SHARED LANE SCENE HANDOFF

**Written by the ARTWORK author for the SPLIT and CUTOUT authors.** The plan is
the contract (`plans/aieducation_plan.json`); this file is the convenience. If
anything below disagrees with the plan, the plan wins and you write your own
note. Section 9 lists the three places this module departs from the plan's
letter, with the reason for each.

Neither lane redraws anything in this module. The scene is sealed
(`review/artwork_pass_aieducation.json`); a lane that needs a change takes
`production.py scene-lock`, redraws, re-reads cold over three rounds and
re-seals.

---

## 1. THE MODULE

| | |
|---|---|
| path | `shorts_run22/gen/aieducation_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import aieducation_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `shorts_run22/gen/_aieducation_proof.py` (`--set seal`, `--set compose`) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the WHOLE 32.12 s scene: html to drop inside one
`transform: scale(k)` wrapper, and a list of `tl.*` javascript strings to
concatenate into your own timeline tail. It authors nothing outside the core, it
reads no files, and it takes no format argument — every difference between the
two formats is in the PLACEMENT and in the `lockup` string.

### `media` — the five rasters the scene paints

```python
{"_chatgpt_img": CC.mark_img(LOGO_URL["chatgpt"], "chatgpt", SC.MARK_SIDE["chatgpt"]),  # 74.0
 "_claude_img":  CC.mark_img(LOGO_URL["claude"],  "claude",  SC.MARK_SIDE["claude"]),
 "_gemini_img":  CC.mark_img(LOGO_URL["gemini"],  "gemini",  SC.MARK_SIDE["gemini"]),
 "_xmark_img":   '<img src="assets/x-logo.svg" style="width:34px;height:34px;display:block">',
 "_shot_img":    '<img src="assets/quoted_video_poster.jpg" '
                 'style="width:460px;height:288px;object-fit:cover;'
                 'object-position:50% 46%;display:block">'}
```

`CC.MARK_INK[key]` must be populated by `CC.measure_mark(key, src)` first, and
the `LOGO_URL` values must be page-relative (`assets/logos/<basename>`). The
sizes are **ink sides in CORE px** — do not rescale them for the cutout; the
core's own `scale(k)` carries them.

**THE FILES ARE NAMED, NOT GUESSED** (`SC.LOGO_FILES`, MARK IDENTITY):
`ai-models/chatgpt-color.png` is the PRODUCT mark for ChatGPT and never the
`openai` wordmark (LAW 35); `ai-models/claude-color.png` is Anthropic's product
mark and never `claude-code`, never the outlined sticker;
`ai-models/gemini-color.png`. The X mark is `platforms/x-logo.svg` and it is
CARD CHROME inside the source post, not a cast tile.

### the source-post assets

`shorts_run22/assets/source_aieducation/` — `syndication.json` (the genuine post),
`quoted_video_poster.jpg` (1200x752, the first frame of the video the post
carried: the Anatomy Atelier app with its 3D heart), `quoted_video.mp4`,
`avatar_thebuggeddev.jpg`. Copy the poster next to your page as
`assets/quoted_video_poster.jpg`.

### `lockup` — the outro's handle block

```python
CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W) \
  + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W)
```

Seated inside the scene's own `#o-slot`. `handle_key` is the ONLY string that
differs between the masters: `"yt"` on the split, `"tiktok_ig"` on the cutout.

---

## 2. THE UNITS

**CORE px = the plan's CANVAS px with y shifted by −192.**

```
canvas_y = core_y + SC.CANVAS_OFFSET      # 192.0
canvas_x = core_x                          # every core x survives verbatim
```

* `SC.CORE_W, SC.CORE_H = 1080.0, 600.0`
* `SC.CONTENT_Y0, SC.CONTENT_Y1 = 20.0, 572.0` — the band the core DECLARES it
  paints in (canvas 212 … 764). Y0 is the tool-tile row's top in chapter 4, Y1
  is ONE AFTERNOON's box bottom in chapter 1. Both are REAL painted ink.
  Canvas 212 is 11.0 % of frame height, clear of LAW 30's top-10 % line; canvas
  764 is 39.8 %, clear of the caption seat.
* The composition **is symmetric about x = 540** in every chapter: the book
  (330 + 210), the heart (370 + 170), the card (140 + 400), the tile row
  (300/540/780), the easel (350 + 190), the copies (470/540/610). Chapter 2 is
  the one deliberate pair — book centre 280, head centre 770 — and it is
  mirror-symmetric about 525, i.e. its ink extents are 120 … 910 for an optical
  axis of 515. So `left = (1080 − 1080·k) / 2`.
* Seat the core so its CONTENT BAND — not its box — is centred on your stage
  zone's centre:
  ```python
  top = round(centre - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 * k, 2)
  ```

**GATE-SCALING.** The cutout scales the core by ~0.95, so a 42 core-px gutter
arrives as ~40 canvas px. Every non-block gutter in this scene is authored at
**≥ 42 CORE px**; every gap smaller than that is inside a DECLARED block
(`SC.DECLARED_BLOCKS`), where Gate 1's cramp check does not bind.

---

## 3. THE TIMELINE

`SC.CUE` carries every instant, and each one is a word START from
`cuts/aieducation/transcript_tight.json` unless its comment says `authored`; an
authored cue is inside its word's 1.0 s LABEL_WINDOW. `SC.BEAT_EDGES` is the
plan's own beat table. `SC.DUR = 32.12`, the cut master.

Five chapters, `SC.BOARD_MODE = "chapters"`, `SC.BOARD_CHAPTERS`:

| ch | t | what is on screen |
|---|---|---|
| 0 | 0.10–3.00 | the open book; the heart prints on its page at 0.86 and LEAVES it at 1.48, with a dashed ghost staying behind |
| 1 | 3.00–13.40 | the X source post (3.32–6.86, closer move into the screenshot at 5.92), then the heart, the hotspots, the arc, `3D ANATOMY`, `ONE AFTERNOON`, the interior vessels at 11.88 |
| 2 | 13.40–17.94 | the flat book (border flip 15.54–16.34), the thinking head, `FLAT PAGE`, `GUESSWORK` |
| 3 | 17.94–21.74 | the heart, opened on its hinge at 19.26; the cursor; `INSIDE` |
| 4 | 21.74–27.76 | three tool tiles, three connectors, the easel, the heart on its board (border flip 25.54–26.30), three copies on the brace |
| — | 27.76–32.12 | the opaque rising sheet, then the lockup on the small heart |

**The erase is a HANDOVER, never a blank** (`clear()`): the outgoing chapter
fades over 0.22 s while the incoming chapter's first object is already arriving,
so the zone's ink never reaches zero across a seam.

---

## 4. THE FOUR BESPOKE OBJECTS — SEALED, DO NOT REDRAW

`SC.BESPOKE` carries the boxes in CORE coordinates and the held instant of each.

| i | object | t | core box | cold reads (3 independent rounds) |
|---|---|---|---|---|
| 0 | open book heart | 2.40 | 330, 74, 750, 468 | "open book" ×3, all sure |
| 1 | 3D anatomy heart | 12.60 | 370, 160, 710, 500 | "heart" ×3 (1 sure) — after the redraw |
| 2 | thinking head profile | 17.40 | 630, 170, 910, 460 | "head profile with heart" ×3, all hedged |
| 3 | classroom easel board | 25.00 | 350, 176, 730, 536 | "easel" / "easel with canvas" ×3, all sure |

Object 2 is a **hedged pass** and is routed, not refused (the 2026-09-08
ruling): three of three readers named the intended object and none named a
different one. **The clerk must adjudicate it on the delivered render**, where
it carries its `GUESSWORK` key and lands on the word "imagine".

One frame-normalised box cannot be right for both formats — the box is a
consequence of the placement — so map `SC.BESPOKE[i]["core"]` through your own
k and origin when you cut phone crops.

---

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 40** — `SC.EASEL_ENDS = anchor_points(SC.EASEL_BOARD_BOX, 3, "top")` =
  (451.6, 240.0), (540.0, 240.0), (628.4, 240.0): level to 0.0 px, symmetric
  about x = 540. The three connectors carry `data-connect-to="easel-board"` and
  `data-overlap-ok`. Do not hand-place an end.
* **LAW 39 / LAW 50** — four keys, each with `data-label-for`: `3D ANATOMY`
  ABOVE `heart`, `ONE AFTERNOON` BELOW `heart`, `FLAT PAGE` BELOW `book2`,
  `GUESSWORK` BELOW `head`, `INSIDE` BELOW `heart3`. The two siblings in
  chapter 2 take the SAME placement on the SAME baseline (`KEY_ROW_Y = 506`).
* **LAW 41** — `SC.DECLARED_BLOCKS`, stamped as `data-block` in the DOM.
* **LAW 42** — `SC.LIFETIMES`, every mark finite except the outro lockup
  (`SC.SCENE_ANCHORS`).
* **LAW 38** — exactly two emphases, each matched to its target: the MARKER
  HIGHLIGHT (`#post-hl`) on the claim line inside the raster post card, and the
  PANEL BORDER FLIP on two drawn objects (`#book2` at 15.54, `#easel-board` at
  25.54). No ring, no ellipse, no circle exists anywhere in this module, and no
  `<circle>` tag is emitted at all.
* **LAW 51** — the heart is the object all three lanes share. Wherever it moves,
  its parts move with it: the hotspots and the arc are children of the same
  block and the opened front half is a `<g>` inside the heart's own svg. A lane
  that animates the heart without them is a cross-lane parity defect.

---

## 6. THE POINTING CUE

`pointing_cues.py` returns exactly one cue: `{i: 22, t: 3.32, kind: person,
phrase: "this guy", window: [2.32, 4.32]}`. It is answered by `#card-wrap` at
3.32 — inside its own window, one block — held 3.54 s (GLOBAL LAW 3's 2–4 s),
with the marker on the claim line and **no metrics chrome**.

The card wears the frame of the platform the sentence names: X. The post is the
genuine one, `https://x.com/thebuggeddev/status/2083884856531177942`, recovered
from the recording's Notion inbox row whose Source URL
(`https://x.com/gdb/status/2083934330146197989`) quotes it. What the viewer must
read is the post's own claim line; what it carried is the app screenshot, and
`CUE["zoom"]` at 5.92 moves closer into that screenshot (ZOOM_K 1.92 about the
3D heart) so the read target is comfortable at phone size.

---

## 7. WHAT THE CUTOUT OWNS

* The matte, the wing review and the stage-zone seating — the prompt0 marker was
  `blocked` at plan time, so the cutout author owns the wing review.
* `SC.CUTOUT_LOGO_LANES = ("chatgpt", "claude", "gemini", "cursor", "grok",
  "lovable")` — topical to this short (the marks it names plus their obvious
  neighbours in the same category), mixed, no mark repeated, and never the
  story's own stage object.
* Your own k and origin. Everything else in the stage zone comes from this file.

## 8. WHAT THE WHITEBOARD DOES NOT DO

It does not import this module. It redraws the SAME argument in marker ink, with
the same objects, the same labels and the same key term, per beat
`whiteboard_version` in the plan. LAW 51 still binds: the heart's parts move
together there too.

---

## 9. WHERE THIS MODULE DEPARTS FROM THE PLAN'S LETTER

1. **Chapter 3 has no app frame.** The plan's beat 3 lists an "app frame (ui
   chrome)" around the opened heart. It is not drawn: a rounded rectangle around
   the object adds a screen the Phone Test would have to ignore and the beat's
   argument (the model opens up) is carried by the heart alone. The cursor
   arrow stays, and it is the thing that says "interactive".
2. **Chapter 4 has no desks.** The plan's beat 4 drops three copies onto a row
   of three school desks. At this core height the desk row could not clear the
   easel's legs by the 42 px gutter without shrinking the easel back into the
   television it read as, so the three copies land in a row on the easel's own
   cross-brace — the same argument (one for every student), inside the easel's
   block, and the composition stays centred.
3. **The lift line became a ghost.** The plan's hook ends with the heart settled
   above the book. The module also leaves a dashed MUTE outline of the heart on
   the page it came off (`#page-ghost`), because without it the lift reads as a
   second heart drawn higher up rather than as a departure.

The plan's bbox values for objects 0, 1 and 3 were written before the drawings
existed; `SC.BESPOKE` carries the real ones and is authoritative for geometry.
