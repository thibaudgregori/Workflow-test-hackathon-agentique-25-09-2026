# FACESPLIT — chassis

**Status:** approved (Miguel, round 2: *"really fantastic work!"*; round 4 fixed
the 50/50 regression; round 6 closed the two-seat caption). Promoted from
the format lab (archived on Drive under Testing & Experiments) on 2026-09-01.
**Lab record:** `references/laws/facesplit_NOTES.md` (6 rounds) — derivations live
there; this file is the operating manual.

---

## What the chassis does

Two modes, one camera, switching **whenever what's relevant changes**:

| mode | what the frame is |
|---|---|
| **FACE** | Miguel full-bleed, the RAW 0% crop, no graphics except the sign-off lockup |
| **SPLIT** | exact 50/50 — his band above the seam at y=960, the visual zone below |

The switch is the format. It is a **hard cut on a word boundary** by default; the
animated compress/expand is reserved for the two beats where the switch is itself
the statement. The shipped cut runs 12 switches: ~21s face, ~33s split.

**50/50 IS the format** (round 4: *"no longer 50/50… not good for us"* — the
builder had re-proportioned the zones to solve the caption seat; wrong trade).
The seam is 960 exactly, and it is **asserted**, not intended.

The back half is ONE persistent zone object — AVAILABLE TOOLS (a shelf of real
brand marks that later extends until it bleeds off both frame edges = infinite)
over a CONTEXT WINDOW card with a CONTEXT USED meter. Its state survives every
face excursion; nothing inside it animates while it is hidden.

---

## Running it

```bash
~/Documents/Workspace/.venv/bin/python chassis_gen.py                     # YouTube handle
~/Documents/Workspace/.venv/bin/python chassis_gen.py --handle tiktok_ig  # TikTok/IG
~/Documents/Workspace/.venv/bin/python chassis_gen.py --out /tmp/fs
```

| knob | default | what it does |
|---|---|---|
| `--handle` | `yt` | outro chip: `yt` = `@migueltorrezai`, `tiktok_ig` = `@migueltorrez.ai`. **Only the outro differs.** |
| `--out` | `./build` | project root. The lab is never written to. |

| file | what it is |
|---|---|
| `chassis_gen.py` | the switch map, the scene interiors, the SFX schedule, the sign-off |
| `lib/facesplit_fix6_lib.py` | the format: geometry, plate, seats, caption machinery, compose/write guards |
| `lib/facesplit_fix6_check.py` | the post-render checker |
| `lib/facesplit_type_cache.json` | the measured pill-width cache (offline + deterministic after the first build) |

### The two caption seats (round 6, confirmed by Miguel)

The pill has **one home per mode** and it SWAPS as a hard cut on the switch frame.
It never slides, and it is never alive while the layout under it is moving (the
two animated moves are caption blackouts).

| mode | seat | pill span |
|---|---|---|
| SPLIT | centred ON THE SEAM, 960 — exactly like the 32 published shorts | 902.7 .. 1017.3 |
| FACE | pinned by its BOTTOM edge at 1380 (71.88%, Law 12's line) | 1265.4 .. 1380.0 |

Both derived from `CAP_PILL_HEIGHT` in `pipeline/captions.py`. Holding round 5's
top edge instead would push the bottom to 73.3% — past the law.

---

## Format laws

1. **SWITCH WHENEVER RELEVANCE CHANGES.** Face for claims, questions, asides,
   second person and the sign-off; split only while a visual is earning the zone.
   Segments may be as short as ~1s.
2. **EVERY SWITCH LANDS ON A WORD**, and every switch time is a frame time.
3. **HARD CUT IS THE DEFAULT SWITCH.** The compress/expand is for the two beats
   where the switch is the statement.
4. **NO ZOOM.** Both modes render at their derived plate scale. The switch *is*
   the punch (2.133x head height); a punch-in inside a mode is redundant and
   re-breaks Global Law 1.
5. **ONE CAMERA.** A single plate authored at its largest on-screen size, with
   `transform-origin: 50% 100%`. No source swaps, ever.
6. **THE FULL-FACE MODE CARRIES NO GRAPHICS** except the sign-off lockup, which
   keeps 100px of air below the caption pill.
7. **ONE PERSISTENT ZONE OBJECT** across every split segment.
8. **EXACTLY 50/50.** The seam is 960 and the build asserts it.
9. **CAPTION POSITION IS STABLE** (Morgane, Law 12): two fixed seats, swapped as
   a cut — never a drifting or sliding pill.
10. **Law 20 applies to the SPLIT's opening**: the card lands ON the cut frame and
    is full ~1.4s later — never an empty vessel.

- **THE FACE IS CENTRED, AND IT IS MEASURED (Miguel, 2026-09-02).** In every
  full-face segment the detected face centre must sit within **±4 % of the frame
  width** of the frame centre. This is a law, not a taste note: Miguel rejected
  the first daily takeover (`impossibletask_takeover` v1), and the same instrument then caught `kimiram_facesplit` at +7.69 % in its closing full-face lockup specifically because his
  face was off-centre in the full-face beats, and every gate in the factory passed
  it — Gate 1 measures the authored DOM, Gate 3 is a rubric screener, and neither
  decodes the render and asks where the head is.

  **The check:** `pipeline/face_center_check.py <render.mp4> --fmt facesplit
  --geom <_geom_<id>.json>` — segments come from `facesplit.switches` (a `to: face` window until the next `to: split`), frames are
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

- **Zooms were the format's original sin.** Round 1 and round 2 both rejected the
  full-face framing as too tight. Since round 3, full-face = the regular RAW 0%
  crop, punches deferred until the new lens. Do not reintroduce them.
- **Do not solve a caption problem by re-proportioning the zones.** Round 4's
  regression came from exactly that. If the pill does not fit a seat, move the
  pill or split the phrase — never the seam.
- **A plate is authored at the resolution of its largest on-screen size** (round-1
  finding). Authoring smaller and scaling up shows.
- **The chest seat is not reachable** in FACE mode — round 5 proved it
  arithmetically. The seat that exists is the one shipped.
- **The pill grew 27.6px** when the canon replaced the format's own pill; the
  lower-lip landmark passes behind the pill's top edge on 18 of 617 FACE frames
  (0.60s), all decoded and confirmed as beard/neck with the mouth clear.
- **A one-frame bug hides in mode switches** (round 6 found one). Visibility is
  toggled on the exact switch frames; check `HALF_FRAME` handling before touching
  the switch map.
- `HANDLE` inside `lib/facesplit_fix6_lib.py` is this format's outro **type size**
  (30.0du). The handle TEXT is `OUTRO_HANDLE`. Do not confuse them.
- The face plate and voice are **inherited** from the lab's frozen stage; the
  chassis copies them into its own `stage/` and never writes into the format lab (archived on Drive under Testing & Experiments).

---

## Proof of promotion

`chassis_gen.py` (default `--handle yt`) reproduces the approved round-6 page
**byte-for-byte**:

| chassis output | lab round-6 output | result |
|---|---|---|
| `build/facesplit/index.html` | `references/builds/chassis/facesplit/fix6/index.html` | identical |

`--handle tiktok_ig` differs on **exactly one line**: the `#fo-handle` div.

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
