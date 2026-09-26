# stripekai: split author notes

No disagreement with the plan. The split builds it as written. One format-side declaration differs from the plan's wording:

- **The emphasis target (LAW 38).** The plan names the target "toolbox-2 body outline". The page declares `data-emphasis="border"` on `#toolbox-2 .tbbody` and targets an inkless virtual rect, `#toolbox-2-body`. That rect sits inside the returning toolbox's scaled authoring div, so it moves and scales with the toolbox. The whole `#toolbox-2` cannot be the target. Its terracotta screwdriver handle paints `rgb(221,114,89)`, the same colour the outline flips to, so the strict colour-equality check would count the emphasis as target ink. The body is also what the plan actually emphasises. Nothing visible changes.
- **Phone-at boxes in the render job.** These use the plan's bboxes, as the brief says. The handoff's `SC.BESPOKE` core boxes differ from them by at most 0.013 of the frame, on the buildings and on the overflowing toolbox.
