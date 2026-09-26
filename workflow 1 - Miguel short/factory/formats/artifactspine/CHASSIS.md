# ARTIFACT SPINE — chassis

**Status:** approved (Miguel, round 1: *"Super NICE representation"*; round 2:
`artifactspine_fix` **APPROVED — "nice!", do not touch**; the zoom-between-pages
cut confirmed as a variant of the same format). Promoted from
the format lab (archived on Drive under Testing & Experiments) on 2026-09-01.
**Lab record:** `references/laws/artifactspine_NOTES.md` (6 rounds) — derivations live
there; this file is the operating manual.

---

## What the chassis does

**One document is the whole video.** A mock tool-registry panel — real chrome,
real registry marks, an always-present context meter — is the only subject. The
spine advances through it and annotations land on the line being spoken. Miguel's
face appears only in the hook, the switch-ins and the sign-off, and it occupies
**exactly the same window rect as the panel**, so the frame never changes shape:
the window's *content* changes, not the composition.

### Two variants, one artifact

| variant | what it is |
|---|---|
| `artifactspine` (`--variant scroll`) | **the scroll.** One continuous top-to-bottom journey through seven document sections. Face switch-ins are part of the format (round 1: *"extra nice"*). |
| `artifactspine_zoom` (`--variant zoom`) | **the page-zoom.** The seven regions become cards on one board and the camera moves between them, with motivated wides. Confirmed as a variant, round 1. |

The **context meter in the status bar is the spine's through-line**: withheld
until the beat that fills it, filled, collapsed on the counter-claim, and then it
never moves again — which is exactly what the last annotation lands on.

---

## Running it

```bash
~/Documents/Workspace/.venv/bin/python chassis_gen.py                     # both variants
~/Documents/Workspace/.venv/bin/python chassis_gen.py --variant zoom
~/Documents/Workspace/.venv/bin/python chassis_gen.py --handle tiktok_ig
```

| knob | default | what it does |
|---|---|---|
| `--handle` | `yt` | outro chip: `yt` = `@migueltorrezai`, `tiktok_ig` = `@migueltorrez.ai`. **Only the outro differs.** |
| `--variant` | `all` | `scroll`, `zoom`, or both |
| `--out` | `./build` | project root. The lab is never written to. |

### Layout

| file | what it is |
|---|---|
| `chassis_gen.py` | variant selection, the round-6 apply, the zoom restage, the page verify |
| `lib/artifactspine_core.py` | the artifact: seven sections, chrome, marks, the meter, the outro |
| `lib/artifactspine_fix_core.py` | round-1 fixes + asset binding |
| `lib/artifactspine_fix3_core.py` + `_fix3_gen.py` / `_zoom_fix3_gen.py` | the geometry and the two builders |
| `lib/artifactspine_fix6_core.py` | the round-6 caption swap; reads its canon from `pipeline/captions.py` |
| `lib/fix6_check.py` | the post-render checker |

### Geometry knobs

- window `40,372 1000x1416` — **centred**, 40px margins both sides (Law 12 as
  amended in round 4: only captions and readable annotations avoid the right rail;
  the composition stays symmetric).
- `CAP_Y = 288` — the TOP caption seat. Pill 230.8..345.1 = 12.0..18.0% of frame
  height, 26.9px of clearance to the artifact, zero overlap at every frame.
- `MIN_BEAT = 0.20` — a split caption beat never flashes.
- 25 fps (Global Law 6).

---

## Format laws

1. **ONE WINDOW.** The face and the artifact occupy the same rect for the whole
   piece. A face-led format may change what is in the window; it may not change
   the window. Corollary, found the hard way: when the artifact is NOT confined to
   that rect (a board wider than the frame), it must be switched off with the face
   — otherwise its chrome leaks around the face card.
2. **ADVANCE, THEN HOLD.** The spine never moves continuously. Every move is
   discrete, word-synced, <= 0.9s, and followed by a hold. Annotations land only
   on a held surface.
3. **THE ARTIFACT IS INTERNALLY CONSISTENT.** Every number, count and label must
   agree with every other one — they are all on the same surface. Hypothetical
   figures are labelled as hypothetical.
4. **CHROME PAINTED, CONTENT ON ARRIVAL.** Section frames, titles and tracks are
   authored painted; rows, chips and marks paint when the spine arrives.
5. **ONE PERSISTENT INSTRUMENT** (the context meter). Withheld until the beat that
   fills it, changed only on events, and the video's last annotation lands on it.
6. **THE ARTIFACT OWNS THE NAMING BEATS.** The face may only take connective
   lines. If the voice names a thing that is on the document, the document is on
   screen.
7. **EDGES DISSOLVE.** A scrolling or zooming spine fades its content at the
   viewport edge; content is never sliced by a hard clip line — that reads as a
   rendering bug, not as a document.
8. **ALL CARDS IDENTICAL WIDTH** (Law, round 2): every card stop paints its
   subject at 920px wide with 40px of air each side. Cards never touch the frame
   edge.
9. **NO PEEK-AHEAD** (Global Law 4): content that has not been spoken yet is not
   visible. No section spoils itself while peeking at the bottom edge.
10. **NO UNNECESSARY MOVES** (Global Law 5): a camera or scroll move with no
    spoken reason does not happen.
11. **PACE TO COMPREHENSION**, not just to the word timings — round 1: it
    sometimes animates too fast for the viewer to take everything in.

---

## Known traps

- **Do not shove the composition to clear the right rail.** Round 4: *"why are
  they not centered? they look so bad like this"* — Law 12's rail clearance had
  been applied to the WHOLE composition, leaving 168px of dead space. Only
  captions and critical readable annotations avoid the right 15%.
- **Counter overflow:** the "loaded this turn" loader once overflowed into its
  `/247` limit. Any counter that animates must be width-guarded against its own
  suffix.
- **The zoom gen snapshots its stage rect at IMPORT time.** `restage_zoom()` in
  `chassis_gen.py` re-derives the four constants from the same expressions.
  Changing the window without re-running that derivation silently desyncs the
  camera.
- **`fix6/` reproducibility depends on `R.apply()` running first** — it repoints
  the shared geometry and swaps the caption object before any build.
- The staged plates are the lab's, **symlinked read-only**; the chassis writes
  only into `build/`.

---

## Proof of promotion

`chassis_gen.py` (default `--handle yt`) reproduces both approved round-6 pages
**byte-for-byte**:

| chassis output | lab round-6 output | result |
|---|---|---|
| `build/artifactspine/index.html` | `references/builds/chassis/artifactspine/fix6/index.html` | identical |
| `build/artifactspine_zoom/index.html` | `references/builds/chassis/artifactspine/zoom_fix6/index.html` | identical |

`--handle tiktok_ig` differs on **exactly one line**: the `#ol-handle` div.

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
