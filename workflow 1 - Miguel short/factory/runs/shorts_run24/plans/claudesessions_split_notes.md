# claudesessions - SPLIT LANE NOTES

Written by the SPLIT author. The plan was built as written; nothing here changed
the argument, the metaphor, the beats, the labels or the timing. These are three
things the CUTOUT author inherits, because it reads the same scene module.

## 1. `#team-c-emph` had to be grown from the radio's BODY to the WHOLE radio

`claudesessions_scene.py` seats the second emphasis at core
`(735, 146, 885, 353)` - the radio's body box - while its declared target
`#team-c` is the whole element with the antenna in it, core `(745, 96, 875, 343)`.

`pipeline/visual_laws.py` measures an emphasis box's clearance against the
TARGET ELEMENT's own rect:

    gaps = [b.left - r.left, r.right - b.right, b.top - r.top, r.bottom - b.bottom]
    if min(gaps) - strokeWidth/2 < 4  ->  "Emphasis box needs at least 4px clearance"

With the module's box the top gap is **-50 px** and the emphasis is refused
before a frame renders.

LAW 51 is the reason the fix is the obvious one rather than a shrink of the
target: *the antenna moves with its radio*, so the thing being emphasised is the
radio, antenna included. The repair is made on the EMITTED string only
(`repair_dom()` in `gen/claudesessions_split_gen.py`), never on the module, and
the new box is core `(731, 82, 889, 357)` - 14 px clear on every side, 12 px
after the 4 px border's half width. The instant (12.90), the release (14.10),
the ink (`#C4573A`), the radius and the scale-in are untouched.

**The cutout lane has the same defect** and will need the same repair, scaled by
its own k. Core y 82 is still inside the declared content band (`CONTENT_Y0` is
24), so the seating arithmetic does not move.

## 2. `data-label-for="team-row"` is not a DOM id

The module labels TEAMMATES with `data-label-for="team-row"` and no element of
that id exists, so LAW 39's instrument has no host to measure against. This lane
repoints it to `team-b` on the emitted string. `team-b` IS the row's own axis
(centre x 540, to 0.0 px), which is what TEAMMATES is centred on, so nothing the
viewer sees and nothing the law measures changes. The cutout inherits this too.

## 3. `plans/claudesessions_plan.md` is stale against `plans/claudesessions_plan.json`

Handoff section 9 item 1 says object 1's norm box was corrected to
`[0.1898, 0.15, 0.8102, 0.2786]`. **`claudesessions_plan.json` carries the
corrected box** and it matches the drawn cluster to 0.1 px, so the Phone Test's
`--plan` crops are exactly the sealed ink. The readable copy
`claudesessions_plan.md` still prints the first draft `0.2958` at line 131. No
tool reads the markdown, so no picture is affected; it is recorded here so the
next reader does not trust the prose over the contract.

## Nothing else

No disagreement with the plan's lane, beats, metaphor, cast, labels, blocks,
lifetimes, chapters or emphasis kinds. `open_doubts` was empty and stayed empty.
`pointing_cues` is empty in the take, the plan and the prep marker, so this lane
invents no source-post card and chooses no platform frame (GLOBAL LAW 3 by
absence).
