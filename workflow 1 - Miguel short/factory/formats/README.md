# formats/ — the approved format chassis

The format lab closed on 2026-09-01 with seven definitive videos approved by
Miguel. This directory is where those formats became first-class citizens of the
factory: one chassis per format, each a promoted copy of its round-6 winner.

the format lab (archived on Drive under Testing & Experiments) is now **read-only history**. Nothing here writes into it; the
chassis read the frozen plates, transcripts and SFX from there and produce
everything else under their own directory.

## The catalog

| chassis | variants | verdict |
|---|---|---|
| (classic split — the existing factory, `pipeline/build_hyperframes_r2.py`) | — | 32 shipped shorts |
| [`facesplit/`](facesplit/CHASSIS.md) | dynamic FACE <-> exact 50/50, two caption seats | *"really fantastic work!"* |
| [`takeover/`](takeover/CHASSIS.md) | full-bleed cutaways, ~25/75 face/illustration | *"does this a lot better"* |
| [`artifactspine/`](artifactspine/CHASSIS.md) | `scroll`, `zoom` (page-to-page) | **APPROVED — "nice!"** |
| [`whiteboard/`](whiteboard/CHASSIS.md) | `fix` (plan view), `zoom` (calm lane) | *"amazing!"* |
| [`cutout/`](cutout/CHASSIS.md) | SAM2 matte + cream rim + depth parallax | **"this is the standard!"** |

`pureface` is **DEAD** (round 2: *"I hate it. Throw this format to the trash."*).
It is not promoted and must not be revived.

## The shared contract

Every chassis follows the same three rules:

1. **`chassis_gen.py` is the entry point**, run on the workspace venv:
   `~/Documents/Workspace/.venv/bin/python chassis_gen.py`
2. **`--handle` is the ONE platform parameter.** `yt` (default) renders
   `@migueltorrezai` for the YouTube master; `tiktok_ig` renders
   `@migueltorrez.ai`. Only the outro chip differs — verified per build.
3. **The caption canon is imported, never re-typed**, from
   [`../pipeline/captions.py`](../pipeline/captions.py): 56.2px Nunito 800,
   padding 18.8/33.8, radius 22.5, `#C4573A`, no shadow, pill height 114.59.
   ONE size — a phrase too wide for its seat is SPLIT at a word boundary,
   measured against real Chromium layout, never shrunk.

Other shared knobs: `--out DIR` (project root, default `./build`), and
`--variant` where a format has more than one.

## Post-render gates

Each `lib/` also carries its format's round-6 **checkers** (`*_check.py`,
`*_containment.py`, `*_capproof.py`, `*_matteswap_check.py`). They decode a
finished MP4 and re-measure what the build claimed. They were promoted verbatim
and still default to the lab's `out/*.mp4` render paths, because nothing here
renders video — point them at a new render explicitly when you run one.

## Proof

```bash
~/Documents/Workspace/.venv/bin/python verify_chassis.py
```

Rebuilds all five chassis and diffs the eight emitted `index.html` files against
the lab's approved round-6 projects. All eight are **byte-identical**, and each
`--handle tiktok_ig` rebuild touches exactly one line — the outro chip. Nothing
is re-rendered; the build is the proof.
