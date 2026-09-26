# grokimagine2 split notes (author_split_grokimagine2, 2026-09-22)

## 1. Placement: k = 0.95, not the handoff's 1.00 (LAW 30, followed and logged)

At the handoff's k = 1.00, left 0, top 192, the chapter-1 key `VIDEOS`
(`#key-clapper`, seat centre core x 885, JetBrains Mono 800 26 px, ls 1.2) has
ink out to about x 934. That is readable type past the 918 right rail, at
canvas y 662..706 (34 % to 37 % of frame height, inside the rail's 30 % to 95 %
band). LAW 30's amendment keeps the COMPOSITION centred and symmetric but still
rails critical readable annotations, so a label there is a violation.

The split seats the unchanged core at k = 0.95 about x 540: left 27.0,
top 207.3. That keeps the content band centred where the handoff put it (canvas
498). The key's ink now ends at about x 915.6 (the generator's `guard_rail`
measures it). Content band on canvas: 283.3 to 712.7. That leaves 91.3 px
under the top-10 % line and 92.5 px above the rendering pill top (805.205).
Nothing in the module changed. The cutout sets its own k, but its author should
check the same key against the rail if its k puts x 885 core near 918.

What I would have done in the scene: pull the four output centres in to
210 / 430 / 650 / 870, or narrow `OUT_KEY_SEAT`. That is the design seat's
call, so I did not do it.

## 2. Format-side stamps on the emitted string (the module on disk is untouched)

* Connectors `conn-phone` / `conn-poster` / `conn-polaroid` / `conn-clapper`:
  `data-anchor-side="top" data-anchor-fraction="0.5" data-check-at="12.40"`.
  The ends are `SC.anchor_points(OUT_BOX[k], 1, "top")`.
* The one emphasis (the outline of podium step 2 flipping to terracotta): the
  `.pstep2` rect gets `id="emph-step2" data-emphasis="border"
  data-emphasis-target="podium" data-check-at="16.00" data-block="rank"`. The
  id is the plan's own lifetime name. `data-block="rank"` keeps it in the same
  lockup as the Grok tile that stands 4 px above it.

## 3. Captions

The phrase `infographics,` stood alone between two pauses, and on its own it
would repeat the live key INFOGRAPHICS (LAW 4). The window was re-partitioned
with every board key forbidden, giving `UX/UI` | `mockups, infographics,` |
`images, videos,`. `UX/UI` is a single-token pill for 0.82 s. No legal merge
fits the 756 px seat without making a pill that equals a live key.
