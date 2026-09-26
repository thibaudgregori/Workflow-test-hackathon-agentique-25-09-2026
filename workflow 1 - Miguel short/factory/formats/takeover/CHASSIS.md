# TAKEOVER (CUTAWAY) — chassis

**Status:** approved (Miguel, round 1: *"does this a lot better"*, visuals
*"remarkable"*; round 4 rebalanced to ~25/75; round 6 closed).
Promoted from the format lab (archived on Drive under Testing & Experiments) on 2026-09-01.
**Lab record:** `references/laws/takeover_NOTES.md` (6 rounds) — derivations live
there; this file is the operating manual.

---

## What the chassis does

**The frame belongs to exactly ONE thing at a time**: Miguel full-bleed, or a
full-bleed visual scene. A split never exists. When a visual earns it, it *takes*
the entire frame for a beat while the voice carries, then hands it back. The only
variable between cut maps is which claims earn a takeover, how many, and how long
— scenes, palette, type, captions, SFX and the outro are constant.

The shipped map is **GROWING**: cutaways get longer and denser as the argument
escalates, ~21% face / ~79% illustration frame time (round 4's rebalance — the
ceiling under the guards, not a preference). The HOOK stays his face; one short
face return lands before the final line.

---

## Running it

```bash
~/Documents/Workspace/.venv/bin/python chassis_gen.py                     # YouTube handle
~/Documents/Workspace/.venv/bin/python chassis_gen.py --handle tiktok_ig  # TikTok/IG
~/Documents/Workspace/.venv/bin/python chassis_gen.py --out /tmp/tk --quiet
```

| knob | default | what it does |
|---|---|---|
| `--handle` | `yt` | outro chip: `yt` = `@migueltorrezai`, `tiktok_ig` = `@migueltorrez.ai`. **Only the outro differs.** |
| `--out` | `./build` | project root. The lab is never written to. |

### Layout of the chassis

| file | what it is |
|---|---|
| `chassis_gen.py` | the cut map, the seat solver, caption build, SFX schedule, staging, the report |
| `lib/takeover_fix6_core.py` | the format: scenes, palette, ghost rule, geometry, Law 11 fills |
| `lib/takeover_fix6_pill.py` | the pill measurer + splitter; reads its canon from `pipeline/captions.py` |
| `lib/takeover_fix6_check.py` | the post-render checker (decodes the MP4 and re-measures) |
| `lib/takeover_fix6_contain.py` | mark-containment audit (Law 17) |
| `lib/takeover_switch_law.py` | the SWITCH LAW check (law 11): switch placement, hidden builds, switch rate — reads the built page |
| `lib/_centroid_baseline.json` | the fix4 measurement the scene seats were derived from |
| `lib/_pillwidths.json` | the measured pill-width cache (deterministic, offline after first build) |

### Geometry knobs that matter

- `CAP_Y = 1318` — the ONE caption band, pill 1260.7-1375.3, bottom 71.63% of
  frame height. Under Law 12's 72% line, off his mouth on every sampled frame.
- `PILL_TOP = 1258`, `REGION_MID = 629` — an illustration is centred in the space
  it actually owns, `[0, PILL_TOP)`, not in the old content band (`MID = 704`).
- `LEAD = 0.18` — takeover interiors start their entrance before the clip is on
  screen.
- `FPS = 25` (Global Law 6), audio mix: voice 1, bed 0.065, SFX 0.18.

---

## Format laws

1. **NO SPLIT, EVER.** The frame is his or the visual's. Mixing the two inside
   one video destroys the device.
2. **CUTS LAND ON WORDS.** Every entrance and exit sits on a Scribe word
   boundary — enforced at build time, not by eye. No dissolves anywhere.
3. **ARRIVE IN MOTION.** A takeover's first visible frame is mid-gesture. A scene
   whose entrance begins at its own `t0` is a defect. Cutting to a static pose
   reads as a slide, not a cutaway.
4. **THE BAND IS FIXED AND SACRED.** Captions sit at one `y` for the whole video
   and nothing — including elements in flight — enters within 112px of it. With
   no seam, the band is the only thing that survives every cut, which is what
   makes the alternation legible instead of jarring.
5. **SFX ARE THE GRAMMAR.** Entrance and exit take DIFFERENT sounds — `tk_in`
   seizes, `tk_out` releases. One family per video, reused.
6. **NO FACE RUN OVER ~7s.** Owning the whole frame means Miguel alone for 10+
   seconds is a hole. Punch-in cuts are minimum texture, not a substitute.
7. **PUNCH-INS ARE CUTS**, never zooms — instant step, then held. The footage
   never *expands*: a scale-up animation was rejected in round 2. Zooms are HARD
   CROP CUTS inside the 0% frame.
8. **THE PEAK NEEDS >= 6s.** A bespoke Law-13 object cannot be read in 3s of
   full-frame time.
9. **LAW 20, FACE-LED FORM.** The hook is Miguel plus the format's own device —
   a punch-in, or a sub-2s flash takeover. No gratuitous hook object.
10. **THE GHOST RULE.** Every dash-driven draw-on rests at `stroke-opacity:0` and
    reveals one frame after the draw starts. Skia paints a round linecap at
    progress 0, so an "un-drawn" glyph is a filled dot — it parked a visible dot
    on screen for 6.38s before this was caught.
11. **TAKEOVER SWITCH LAW (Miguel, 2026-09-01).** *"The switches of the face are
    happening way too often, they should happen at transition moments ideally,
    right now you are cutting key visualizations."* Three clauses, all checked:
    - **Switches only at beat transitions.** A face window covers a claim or an
      aside where nothing is being drawn; a scene run covers a visualization
      from its first build to its hold. The switch sits on the seam between two
      argument beats, never inside one.
    - **A visualization is never cut before it lands and holds.** A departure
      (scene → face) may not land inside a build window, nor within
      `HOLD_MIN = 0.30s` of one finishing. Arrivals are exempt — format law 3
      *requires* the first visible frame to be mid-gesture — but only up to
      `LEAD = 0.18s` of a build; anything more the face covers is a build the
      viewer never sees.
    - **Switch rate is bounded by the DEFINITIVE.** The reference cut switches
      **7 times in 54.04s = 7.77/min**. The ceiling is `7.77 x 1.30 =
      10.10/min`. The cut that broke this law ran 13.99/min.

    ### The check
    `lib/takeover_switch_law.py` — deterministic, offline, runs on the emitted
    page, not on a review of the video:

    ```bash
    ~/Documents/Workspace/.venv/bin/python \
      formats/takeover/lib/takeover_switch_law.py <project>/index.html \
      --duration <DUR> --quiet-windows
    ```

    It parses the clips and every `tl.*` call, classifies each tween
    BUILD / EXIT / MOVE, derives the face and scene windows, and exits 1 with a
    named defect per violation (`D` departure, `H` hidden build, `R` rate).
    `--quiet-windows` prints the legal switch moments so a cut map is **placed**
    rather than guessed. Calibration: it fires 10 build defects plus the rate
    ceiling on the rejected `perplexityprojects_takeover` v1 and is **silent** on
    `formats/takeover/build/takeover/index.html`, the DEFINITIVE.

    ### The two topologies
    The checker handles both, because they fail differently:
    - **scene-on-top** (this chassis): one continuous face plate, scene clips
      over it. A face window hides nothing — outside a scene clip there is no
      scene.
    - **face-on-top** (the lane builds, `(run 9) gen/*_diagram_gen.py`): ONE
      continuous scene timeline with face clips over it, so a cutaway samples a
      world that has been developing all along. Here a face window **erases**
      whatever was drawing underneath it. This is how v1 lost the b0 arrow
      payoff, the sheet swap and the whole third arm of a three-arm diagram —
      each built at full opacity behind his face. Clause H exists only for this
      topology, with the hook's own face window exempt (before the first
      takeover the scene has not been revealed yet).

- **THE FACE IS CENTRED, AND IT IS MEASURED (Miguel, 2026-09-02).** In every
  full-face segment the detected face centre must sit within **±4 % of the frame
  width** of the frame centre. This is a law, not a taste note: Miguel rejected
  the first daily takeover (`impossibletask_takeover` v1) specifically because his
  face was off-centre in the full-face beats, and every gate in the factory passed
  it — Gate 1 measures the authored DOM, Gate 3 is a rubric screener, and neither
  decodes the render and asks where the head is.

  **The check:** `pipeline/face_center_check.py <render.mp4> --fmt takeover
  --geom <_geom_<id>.json>` — segments come from `takeover.cut_map` (every entry whose `what` is `face`), frames are
  sampled every 0.5 s, faces are detected with BlazeFace and validated
  (confidence >= 0.70, >= 40 % skin-tone pixels, so a flat vector graphic cannot
  be scored as a head), and it exits 1 with the offending timestamps.

  Calibrated 2026-09-02: rejected takeover **-9.81 %** worst / 7.68 % mean (13 of
  13 face frames offend), approved `perplexityprojects_takeover` v2 -0.93 % /
  0.56 %, `takeover - DEFINITIVE.mp4` -2.87 % / 1.56 %. Threshold sits mid-gap.

  **The usual cause is the plate window, not the animation.** The full-bleed face
  crop is derived in `_faces_<id>.json` from a measured `face_cx_px`; if that
  measurement drifts, or a different window is used than the one it was measured
  for, every face frame in the video is off by the same amount — which is exactly
  the signature of a failure here (a near-constant dx across all samples).

---

## Known traps

- **Zoom execution killed round 2.** The footage expanding looks wrong. Since
  round 3 the face is ONE plate — the RAW 0% window, full-bleed — with punches
  deferred until the new lens. Do not reintroduce a zoom ladder.
- **Angle-change density is a watch item** (Morgane: *"limite toutes les
  secondes"*). Miguel is unsure it bothers anyone else — re-judge, do not
  overcorrect.
- **A release SFX on a takeover-to-takeover cut doubles up** with the next
  seize on the same frame. A release fires only where the frame actually returns
  to his face.
- **The width estimator is dead.** `len * 0.575 * font + pad` runs 0.71-1.00 of
  the truth; the pill is measured in Chromium via `pipeline/captions.py`. The
  splitter fired 0 times on the approved cut (widest pill 714.6px of a 756px
  seat) — the mechanism is the guarantee, the zero is the measurement.
- **Containment (Law 17)**: a logo must stay inside its box. `takeover_fix6_contain.py`
  is the audit; an obvious frame diff is not a substitute (see NOTES round 6 §6).
- The face plate and voice are **inherited** from the lab's frozen stage; the
  chassis copies them into its own `stage/` and never writes into the format lab (archived on Drive under Testing & Experiments).

---

## Proof of promotion

`chassis_gen.py` (default `--handle yt`) reproduces the approved round-6 page
**byte-for-byte**:

| chassis output | lab round-6 output | result |
|---|---|---|
| `build/takeover/index.html` | `references/builds/chassis/takeover/takeover_fix6/index.html` | identical |

`--handle tiktok_ig` changes the `#outro-chip` text only.

---

## ROUND-4 LAWS (Miguel, 2026-09-02) — global, enforced in Gate 1

Four laws added by round 4 bind this chassis. They are not format opinions; the
full text is `STANDARD.md → ROUND-4 LAWS`, and the instrument is
`pipeline/geometry_audit.py → check_layout()`, which walks the WHOLE subtree of
every active clip and judges every element that carries an `id` (in this factory
an id is the author saying "this is a thing"; id-less SVG internals are strokes
of a drawing, not objects in an argument).

| law | Gate 1 finding | the rule |
|---|---|---|
| 38 — emphasis matches its target | `enclose` | NEVER a ring, an ellipse or a circle, on any target. TEXT ON AN IMAGE (post card, screenshot, document, UI capture) takes the marker HIGHLIGHT: `rgba(198,103,72,0.32)`, radius 6 px, wiped open left-to-right over 0.34 s, ONE FILL PER LINE, `data-overlap-ok`. A DRAWN OBJECT or scene TYPE takes BOXING — the run-3-8 panel border flip (`.node.hero { border-color: TERRA_L }` tweened via `borderColor` over 0.38 s), which is explicitly fine and still owes `cramp` its 16 px gutter to NEIGHBOURS. ERROR: a ring around a thing; a box whose target is image text. WARNING: a highlight on a drawn object. Opt out with `data-container`; declare a raster the namer misses with `data-asset` |
| 39 — names | `sidelabel` | A name goes ABOVE or BELOW the thing it names, centre inside the object's horizontal extent ±15 %. Declare the pair with `data-label-for="<object id>"` (ERROR); an undeclared geometric weld is a WARNING |
| 40 — arrows | `anchorline` | Connectors into ONE target terminate on that target's VIRTUAL BOUNDING RECTANGLE, at the same height (±4 px) or mirror-symmetric about its axis. Declare with `data-connect-to="<target id>"` |
| 41 — spacing | `cramp`, `crossing` | Gutter aim 24 px, refusal floor **16 px**; a connector never crosses printed type (judged on the type's core band). Nothing overlaps unless authored as one block — `data-block="<name>"`. A welded label, a container's contents, a paragraph and a ≥3 identical-shape series are blocks automatically |

ROUND-4 LAW 37 (a pointing cue raises the source post, with the highlight) is a
SCRIPT law and is checked at plan time by `pipeline/pointing_cues.py`.

Escape hatches, used only with a written reason: `data-overlap-ok`,
`data-block`, `data-container`, `data-spacing-ok`.
