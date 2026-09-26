# codexsiri: SHARED LANE SCENE HANDOFF

**Written by the design agent for the SPLIT author and the CUTOUT author.** The plan
(`plans/codexsiri_plan.json`) is the contract and this file is the convenience. If
anything here disagrees with the plan, the plan wins and you write your own note.
Section 9 lists where this module departs from the plan's letter.

Neither lane redraws anything in this module. The scene is sealed with
`production.py seal` (v4: module + handoff hashes, `review/artwork_pass_codexsiri.json`).
A lane that builds on a changed module is refused.

---

## 1. THE MODULE

| | |
|---|---|
| path | `<run>/gen/codexsiri_scene.py` |
| import | `sys.path.insert(0, str(Path(__file__).resolve().parent)); import codexsiri_scene as SC` |
| entry point | `SC.build(media: dict, lockup: str) -> (html, tweens)` |
| proof harness | `<run>/gen/_codexsiri_proof.py` (see its `media()` for the exact media calls) |
| the split's placement | k = 1.0, `left = 0.0`, `top = 192.0` |

`build()` returns the WHOLE 36.16 s scene: the html to drop inside one
`transform: scale(k)` wrapper (`transform-origin: 0 0`) and a list of `tl.*` JavaScript
strings for your own `tl` timeline. It reads no files and takes no format argument.
Every difference between the two formats is PLACEMENT plus the `lockup` string. It
calls `SC.assert_anchor_law()` before it writes a byte.

**Eases are string literals** (`"power3.out"`, `"back.out(2.05)"`, `"power2.inOut"`).
The tweens need no `SOFT`/`POP`/`SWING` constants on your page. Labels use class
`mono` (JetBrains Mono uppercase; weight 800 is set inline), and the post's text lines
set their own `font` inline (JetBrains Mono 400, NOT uppercase). Your page must load
JetBrains Mono 400/500/800. Elements use class `abs`: give it `position:absolute;
box-sizing:border-box` as the chassis already does.

### `media`: the rasters the scene paints

```python
for key, rel in SC.LOGO_FILES.items():            # names, never guesses (MARK IDENTITY)
    CC.MARK_INK[key] = CC.measure_mark(key, LOGOS / rel)   # copy the file into assets/logos/
media = {mkey: CC.mark_img(f"assets/logos/{Path(SC.LOGO_FILES[k]).name}", k, side)
         for mkey, (k, side) in SC.MEDIA_SIDES.items()}
# the two source-post rasters, copied from the run into your project:
media["_avatar_src"] = "assets/source/avatar_sharifshameem.jpg"   # <run>/assets/source_codexsiri/
media["_post_src"]   = "assets/source/video_poster.jpg"
```

| media key | logo | ink side (CORE px) | where |
|---|---|---|---|
| `_siri_img` | `siri` = `ai-models/siri-color.png` | 88 | phone screen, chapters 0-3 |
| `_codex_scr_img` | `codex` = `coding-tools/codex-color.png` | 88 | phone screen after the swap |
| `_github_img` | `github` = `coding-tools/github-mark.png` | 74 | GitHub tile (used twice, ch 3 and ch 5) |
| `_codex_img` | `codex` | 84 | Codex tile |
| `_openai_img` | `openai` = `ai-models/openai.png` | 32 | the maker badge on the Codex tile |
| `_x_mark` | `x-logo` = `platforms/x-logo.svg` | 28 | the post card header |

Sizes are ink sides in CORE px. Do not rescale them for the cutout: the core's own
`scale(k)` carries them. `SC.POST_ASSETS` names the two post rasters relative to the run.

### `lockup`: the outro's handle block

```python
CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W) \
  + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W)
```

It is seated inside the scene's own `#o-slot` (core top 358). `handle_key` is the only
string that differs between masters: `"yt"` on the split, `"tiktok_ig"` on the cutout.

---

## 2. THE UNITS

**CORE px = the plan's CANVAS px with y shifted by -192.** `canvas_y = core_y + 192`,
and x is untouched. `SC.CORE_W, SC.CORE_H = 1080.0, 600.0`.

* `SC.CONTENT_Y0, SC.CONTENT_Y1 = 76.0, 538.0` is the band the core really paints
  (canvas 268 to 730, 14.0 % to 38.0 % of frame height). Y0 is the SIRI SUCKS key's top
  and the post card's top. Y1 is the OUT OF THE BOX key's bottom (the arrow tip reaches
  534 + cap). The outro lives inside it. At k = 1 the lowest ink clears the caption
  pill's top (~787.7) by ~57 px.
* Every chapter is symmetric about x = 540 (ink extents: hook 365 to 715, post 220 to 860,
  box 380 to 700, diagram 190 to 890, talk 255 to 825, repo 344 to 736). So
  `left = (1080 - 1080*k) / 2`.
* For the cutout, seat the core so its CONTENT BAND is centred on your stage zone:
  `top = round(centre - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 * k, 2)`.
* Rightmost ink: the OpenAI badge at core x 916 (chapter 3, y 180 to 232) and CODEX key
  to 894. Both are below 918, so the rail is clear at k = 1. Recheck under your k.

---

## 3. THE TIMELINE

`SC.CUE` carries every instant (word STARTS from `cuts/codexsiri/transcript_tight.json`
unless marked `authored`). `SC.BEAT_EDGES` is the plan's beat table. `SC.DUR = 36.16`.

| ch | t | on screen |
|---|---|---|
| 0 | 0.10-3.82 | the phone pops ALONE on the axis with the Siri mark on its screen (0.10); it slides left (0.42) and the "?" bubble pops at its right (0.62); `SIRI SUCKS` above (0.95); all fade at 3.62 |
| 1 | 3.70-7.56 | the X post card (Sharif Shameem) rises in (3.70); marker fills wipe under lines 1 and 2 (4.12, 4.22; cue word "This" 4.12); the card leaves at 7.30 |
| 2 | 7.40-10.52 | the SAME phone pops back centred, 46 px higher (7.40); the open box rises around it on "so bad" (8.62): flaps BEHIND the phone, front panel IN FRONT; `OUT OF THE BOX` (9.20); box and key fade 10.30 |
| 3 | 10.32-23.52 | the phone slides to the left seat (10.32, "took"); GitHub tile (13.24) + `GITHUB REPO` (13.60); line phone to GitHub (15.00, "connect"); line GitHub to Codex (16.50) + Codex tile (16.58) + `CODEX` (16.80); OpenAI badge (18.94). THE PEAK: terracotta charge Codex to GitHub (19.92) then GitHub to phone (20.28); the screen swaps Siri to Codex (20.94, "improves"); the phone's outline flips terracotta (21.62) and back (22.76); everything but the phone fades 23.30 |
| 4 | 23.34-26.32 | the phone slides to its talk seat (23.34); the speech bubble with three lines pops at its right (23.74, "communicate"); the clipboard pops (24.58); ticks draw on "get" 24.86, "stuff" 25.40, "done" 25.68; `GET STUFF DONE` (24.90); all fade 26.10 |
| 5 | 26.10-32.34 | GitHub tile 2 pops CENTRED inside the erase (26.10) + `GITHUB REPO` (26.40); on "100%" tile and key slide left 140 together (27.02); the price tag reading FREE swings in (27.20) and its string draws (27.40); `IN THE DESCRIPTION` (29.48); the terracotta arrow draws down (29.88, "down") |
| 6 | 31.86-36.16 | opaque rising sheet (31.86); the small blank phone glyph (32.34), rule (32.64), lockup (32.74) |

Every erase hands over to an idea (LAW 45). The card rises as the hook fades. The phone
pops back 0.10 s after the card leaves. The phone crosses seams 3 and 4, and the repo tile
pops inside seam 5. The last board event (the arrow) settles by 30.18, which is 1.68 s
before the outro anchor.

---

## 4. THE FOUR BESPOKE OBJECTS: DO NOT REDRAW

`SC.BESPOKE` carries CORE boxes and the held instant of each. The design agent checked
every one at phone size (405x720) in v4 (no cold readers).

| i | object | t | core box | proof |
|---|---|---|---|---|
| 0 | phone with Siri (+ "?" bubble) | 1.60 | 365, 158, 715, 458 | `review/proof_codexsiri/00.png` |
| 1 | phone in box | 9.90 | 380, 112, 700, 470 | `01.png` |
| 2 | clipboard with checkmarks | 26.02 | 665, 202, 825, 412 | `02.png` |
| 3 | free price tag | 28.50 | 456, 186, 736, 306 | `03.png` |

Map `core` boxes through your own k and origin when you cut phone crops.

---

## 5. THE DECLARATIONS YOU INHERIT

* **LAW 40 / CONNECTORS TOUCH WHAT THEY CONNECT.** Each end lands exactly on the joined
  outline, with a 0.0 px gap. `SC.assert_anchor_law()` checks this, and
  `whiteboard_build.anchor_points` gives the same points (`proofs.json`):
  * `#line-a` phone to GitHub: (360, 262) to (484, 262). The phone's body stroke is inset
    by half its width, so its OUTER ink is the phone's box edge. `data-connect-to="gh-tile"`.
  * `#line-b` GitHub to Codex: (596, 262) to (778, 262). `data-connect-to="codex-tile"`.
  * `#charge-b` / `#charge-a`: the terracotta re-trace of the same two segments, drawn
    Codex to phone. It never crosses the GitHub mark.
  * `#tag-string`: the tile's right edge (456, 246, after the slide) into the tag's hole
    rim (543, 246). It sags 10 px and the tag body sits over its last 27 px, so the string
    reads as threaded through the tag. It is drawn at 27.40, AFTER the 27.02 slide.
  All connectors carry `data-overlap-ok` and rest at `stroke-opacity:0` (THE GHOST RULE).
  Zooms of every end: `review/proof_codexsiri/end_*.png`, `ends_sheet.png`.
* **LAW 39 / 50.** Seven keys, each with `data-label-for`: `SIRI SUCKS` ABOVE `phone`
  (the key term), and `OUT OF THE BOX` below `box`. `GITHUB REPO` and `CODEX` sit below
  their tiles on ONE baseline (core 342). `GET STUFF DONE` is below `clipboard`,
  `GITHUB REPO` below `gh-tile-2` (it moves with it), and `IN THE DESCRIPTION` sits
  above `arrow-down`. `FREE` is the tag's own content (a child).
* **LAW 41**: `SC.DECLARED_BLOCKS`, stamped as `data-block`. The phone and its box
  overlap on purpose (`data-overlap-ok` on both box halves). So do the OpenAI badge and
  the Codex tile's corner, and the post card's children (`data-container`).
* **LAW 42**: `SC.LIFETIMES`. Chaptered board: every board mark has a finite window, and
  only the four outro marks are anchors (`SC.SCENE_ANCHORS`). The phone has two windows
  (0.10-3.82, 7.40-26.32).
* **LAW 38**: exactly ONE box emphasis, `#phone .phbody` stroke to `rgb(221,114,89)` at
  21.62 and back to ink at 22.76. It uses the phone's own outline, never a ring, and no
  `<circle>` tag appears anywhere (the tag hole is a two-arc path). There are TWO marker
  highlights (`#hl-post-1`, `#hl-post-2`, `data-emphasis="highlight"`) on the post's
  text lines.
* **LAW 28 / 51**: the screen marks (`#phone-scr-siri`, `#phone-scr-codex`) are
  CHILDREN of `#phone`, and the ticks are part of the clipboard's SVG. Every post part is
  a child of `#post-card`. The phone is ONE element moved only by `x`/`y` transforms
  (`SC.PHONE_AT`).
* **HIDDEN-AT-0**: every element is authored at `opacity:0` and revealed by its tween.
  The proof page primes the timeline (`tl.progress(1).progress(0)`) before sampling.

---

## 6. THE POINTING CUE

There is one: "this guy" at 4.12 (`gen/_cues_codexsiri.json`). The card is the X post
the Notion row points to. Its Source URL `x.com/jxnlco/status/2085827690909822991` is a
repost, and X syndication resolves it to the original post by **Sharif Shameem
(@sharifshameem), 2026-08-07**, `x.com/sharifshameem/status/2085801979863826926`. The
sentence names no platform, so the card wears X, the platform the post lives on. The
highlight goes under "Siri sucks. So I made a way for Codex / to act as my iPhone's voice
assistant." The strip under the text is the poster frame of the video the post carried.
The card has no metrics chrome and stays up 3.60 s. Sources are in
`<run>/assets/source_codexsiri/`.

## 7. WHAT THE CUTOUT OWNS

* The matte and stage-zone seating. At plan time these stages had landed: `cut` (36.16 s,
  "model-authored keep ranges") and `plate` (over-wide, crop 2848x1780+561+274, scale_k
  0.5056, face_dx 0.036 %). `prompt0` had also landed (wing_review true; the instrument
  abstained and made no cut). So had `selection` (inputs ready, not yet reviewed) and
  `cues`. `track` said `skipped` (matanyone2) and no `ship` marker existed. The Astra
  matte step owns the selection and the matte. `plate_origin()` must read `left` from
  `plate_box`.
* `SC.CUTOUT_LOGO_LANES = ("chatgpt", "gemini", "claude", "perplexity", "grok", "meta")`,
  with files in `SC.CUTOUT_LOGO_FILES`. These are the other AI assistants competing to be
  the voice in your phone. The set is mixed, with nothing repeated, and never Siri or
  Codex (both are on the stage). All six pass `cutout_depthfield.assert_cast_resolves`,
  and so do the five stage marks.
* Your own k and origin. The logo lanes fade in after the hook lands (after 0.95, when
  SIRI SUCKS is written), never later.

## 8. WHAT THE WHITEBOARD DOES NOT DO

It does not import this module. It redraws the same argument in marker ink per beat
`whiteboard_version` in the plan: the same phone, "?" bubble, post card with the same
two highlights, box, tiles and lines, the terracotta re-trace with the screen swap, the
talk bubble, the clipboard with three ticks, and the tag with FREE and the arrow. The
keys are the same and land on the same words.

## 9. WHERE THIS MODULE DEPARTS FROM THE PLAN'S LETTER

1. The plan's `bbox` values are normalised canvas boxes at the split's placement.
   `SC.BESPOKE` carries the real CORE boxes and is authoritative for geometry.
2. Plan ids map to DOM ids as follows: `siri-screen` = `#phone-scr-siri`,
   `codex-screen` = `#phone-scr-codex`, `github-tile` = `#gh-tile`,
   `key-github` = `#key-gh`, `line-phone-github` = `#line-a`,
   `line-github-codex` = `#line-b`, `key-codex` = `#key-codex`, `bubble-talk` =
   `#bubble-t`, `github-tile-2` = `#gh-tile-2`, `key-github-2` = `#key-gh-2`. The box is
   two elements, `#box-back` (flaps) and `#box` (front panel).
3. The plan puts the OUT OF THE BOX label `at` 9.08 ("out"). The key lands at 9.20,
   inside the word's window.

---

## 10. PROOF EVIDENCE

| what | where |
|---|---|
| phone-size crops, one object alone per 405x720 frame | `review/proof_codexsiri/00.png` to `03.png` |
| 1x zooms | `review/proof_codexsiri/zoom_NN.png` |
| composed frames at every beat (GRAPHIC CHART clause 9) | `review/proof_codexsiri/frame_*.png`, `*_phone.png`, `sheet.png` |
| connector-end zooms | `review/proof_codexsiri/end_*.png`, `ends_sheet.png` |
| manifest (crops, mark resolution, anchors, page errors: none) | `review/proof_codexsiri/proofs.json` |
| the seal record | `review/artwork_pass_codexsiri.json` |
