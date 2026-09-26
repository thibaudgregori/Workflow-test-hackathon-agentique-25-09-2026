# codexsiri: split author notes

The split imports the sealed `gen/codexsiri_scene.py` unchanged (artwork-check PASS,
module sha 84c6a200...) and seats it at the handoff placement (k 1.00, left 0, top 192).
Everything below is either a declaration the page adds, or a disagreement logged and built anyway.

## Declarations added to the emitted html (no ink, no timing)

1. **The tag string's target is the punched hole, not the tag box.** The scene's
   `#tag-string` ends at the hole's left rim (543, 246), 27 px inside the `#tag` box.
   Production's connector contract measures the end against a bbox side anchor and
   refused it (27.00 px, max 4). The plan says the string runs "to the tag's punched
   hole", so the page stamps `id="tag-hole"` on the tag's existing hole path and
   declares `data-connect-to="tag-hole"`, side left, fraction 0.5: end distance 0.
   **The cutout author will hit the same contract error on `#tag-string`.** The
   same two string edits in their page fix it.
2. `tag-free` gets `data-label-for="tag"` (FREE is the tag's own content). Without it,
   Gate 1 welded it to the stamped hole beside it and warned `sidelabel`.
3. `post-name` gets `data-label-for="post-card"`. The X header puts the name beside the
   avatar (that is X's own layout), and Gate 1 warned `sidelabel` post-name / post-avatar.
4. Connector contracts: line-a -> gh-tile left (16.00), line-b -> codex-tile left
   (17.40), charge-b -> gh-tile right (20.40), charge-a -> phone right (21.30),
   tag-string -> tag-hole left (28.50). Emphasis contracts: hl-post-1/2 -> post-text-1/2
   (4.80 / 5.00), and `#phone` declared `data-emphasis="border"`, target
   `phone-scr-codex`, checked 22.20 (the outline flip runs 21.62 to 22.76).

## Disagreements, built as planned

- **FREE lands 0.62 s before "free".** The tag with FREE on it swings in at 27.20, inside
  the long word "100%" (27.02-27.78); "free," starts at 27.82. It is one phrase ("100%
  free") and the value agrees, so I built it. If Miguel reads it as a peek-ahead (LAW 24),
  move the scene's `tag` cue to 27.82 so the tag lands on "free". That is a change to the
  design agent's module.
- **IN THE DESCRIPTION is written before its host.** The key lands on "description"
  (29.48) and the arrow it is declared `data-label-for` draws on "down" (29.88). The
  plan orders it this way (the arrow hangs from the words), so the generator exempts
  `key-desc` from its own "label after host" guard.
- **The caption and the key share words.** The pill "Siri sucks," would have repeated the
  live SIRI SUCKS key word for word (LAW 4), so the generator joins that phrase to the
  next before partitioning: the first pill reads "Siri sucks, so here's". The pill "bad
  out of the box," overlaps OUT OF THE BOX. It is not an exact echo, and the only exact
  split ("out of the box,") is forbidden.
