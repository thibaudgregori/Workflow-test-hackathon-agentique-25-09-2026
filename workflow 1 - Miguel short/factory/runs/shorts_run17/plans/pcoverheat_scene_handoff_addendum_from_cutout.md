# pcoverheat — ADDENDUM to the scene handoff, from the CUTOUT lane

A NEW FILE, not an edit of `pcoverheat_scene_handoff.md` and not an edit of
`gen/pcoverheat_scene.py`. The module is the artwork author's and it is sealed;
this is the cutout lane telling the SPLIT lane and the artwork author what it
found while consuming it. Everything below is measured, and the full account is
`plans/pcoverheat_cutout_notes.md`.

## 1. THREE THINGS THE SPLIT'S PAGE NEEDS TOO

The shared module has three defects that only appear in an ANIMATED build, so
the artwork proof harness could not see any of them. The cutout stamps all three
on its OWN emitted page; the split's page has the identical three.

| # | what | the stamp |
|---|---|---|
| 1 | **the download arrow is never painted.** `download_bar_svg` hides its three paths with `opacity="0"` and the scene reveals it with `draw(…)`, which lifts `strokeOpacity` and never touches `opacity`. INSTALL is written at 12.90 under an empty rectangle of cream. | `tl.set("#download-kit .dlk",{opacity:1},12.50)` — one frame after the draw starts, the same instant the GHOST RULE lifts the stroke |
| 2 | **the source card's contents are on screen from frame 0.** `post_block` gives the CARD `opacity:0` but not `#post-header`, `#post-hair`, `#post-text-a/b/c` or `#post-inner`; with `immediateRender:false` they render at 1 until 2.60. The post's own words, including `It found the culprit`, are painted at t = 0.04 over the opening laptop — a LAW 24 peek-ahead of the video's own ending and a LAW 19 breach of the hook opening alone. | `tl.set("#<id>",{opacity:0},0)` for each of the six. Derive them (an id in `SC.LIFETIMES` whose emitted inline style has no `opacity:`) rather than typing the list. **`#o-sheet` is exempt**: it is parked by a transform, and zeroing it deletes the outro wipe |
| 3 | **`ease:none` is not defined by the host.** The scene emits it on the scan sweep. Without a `const none = "none";` beside `SOFT`/`SWING`/`POP` the page throws `none is not defined` before the timeline registers and every page check reports "the page would not load". | add the const to the tail |

Two instruments the cutout lane wrote that catch (1) and (2) downstream of
whoever built the page, both in `gen/pcoverheat_cutout_gen.py`:

* `verify_bespoke_ink()` — screenshots the page at each bespoke object's own
  proof instant, crops its phone box and counts raster ink. A box the cold namer
  will be handed must contain ink; "the element exists in the DOM" is not that.
* `verify_no_peek_ahead()` — primes the timeline the way every seek-based tool
  does and asserts no mark with a declared lifetime is painted before it starts
  or more than a fade after it ends.

## 2. THE SOURCE CARD'S PHOTO EXISTS NOW — USE THIS EXACT RASTER

`media["_post_shot"]` had never been produced. The cutout lane fetched it with
`pipeline/prep/sourcelib.fetch_source` against the Source URL on this
recording's Notion row and cropped it to the plan's scope.

```
assets/source_pcoverheat/2084122084297359607_0.jpg   the post's photo, 1896x2324
assets/source_pcoverheat/shot_pcoverheat_crop.png    THE CROP, 1192x552, aspect 2.1594
assets/source_pcoverheat/crop_pcoverheat.json        provenance, bands, hashes
```

The crop is a three-band montage of the photograph's OWN pixels in their
original order (native y 62-400, 668-768, 953-1140), because the plan's scope
asks for a title strip, the verdict line and the CPU metric row while cropping
out `#1 culprit: Ghostty (terminal)`, which sits BETWEEN the last two. The two
gaps are the screenshot's own blank rows (native y 640 and 930) repeated, so the
window's side borders stay continuous and no pixel is drawn by this factory.
Both DOM lanes must paint the same raster: two captures would put two different
receipts on two platforms.

## 3. `SC.HL_VERDICT_FRAC` — THE MEASURED VALUE

The handoff's §3 says the module's `(0.055, 0.375, 0.760, 0.135)` is a guess
until the lane measures it against the actual capture. Measured on the crop
above, off the verdict line's own ink bbox plus a 10 x 8 output-px pad:

```
HL_VERDICT_FRAC = (0.0603, 0.5647, 0.3907, 0.0638)
```

It is published in `crop_pcoverheat.json → hl_verdict_frac_measured`. Seat it at
RUNTIME (`SC.HL_VERDICT_FRAC = …` before `SC.build`), never by editing the
sealed module. The module's own value puts the marker fill 39 % of the crop's
height above the line it is supposed to scope.

## 4. THE COLD READ, FOR THE ARTWORK AUTHOR

Eleven independent rounds in the cutout lane, 44 reads, on two seats. **Not one
reader named a different object** for any of the four. Objects 0 and 2 pass the
confidence rule outright (5/6 and 6/6 sure at the final seat). Objects 1 and 3
sit at 2/6 sure and `production.py phone-pass` refuses them.

The pattern is worth carrying into the next run: three of object 3's four
`cannot tell` answers begin with the word **"none"** and then name the thing
anyway (`none — UI table, not object`). The reader is refusing the prompt's
"name the single everyday OBJECT", which is what a UI panel always draws — the
same finding the handoff's §6.3 already records for the prompt field. A process
list can be named by every reader and still never be called an everyday object.
Reseating the core 14 % larger (k 1.0 → 1.138) moved neither number, so size is
not the variable.
