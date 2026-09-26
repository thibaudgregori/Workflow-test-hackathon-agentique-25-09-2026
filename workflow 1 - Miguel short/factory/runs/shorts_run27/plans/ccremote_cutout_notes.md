# ccremote cutout: author notes

The cutout matches the plan with no disagreement. Two build details went beyond the sibling pattern.

1. **The depth field would have repeated one logo per lane.** `cutout_depthfield.field()` picks
   `cast[(7j + 5i) % len(cast)]`. The plan's `cutout_logo_lanes` has seven marks, so `7j % 7 == 0`
   and each lane repeated one mark. The page showed only claude, antigravity and copilot, and each lane
   was one logo over and over. The GRAPHIC CHART (clause 7) forbids that. The shared tool was left
   alone. The generator gives `field()` the same seven marks in an eight-entry list
   (`claude, codex, cursor, copilot, claude, opencode, antigravity, warp`). Because eight is coprime
   with seven, every lane now carries all seven marks. The Claude app appears twice, four places apart,
   and the build fails if a lane misses a mark or places a mark next to itself. The roster, and
   `DEPTH_FILES == plan.cutout_logo_lanes`, stay as the plan wrote them.
   A later run with a seven-mark cast will hit the same issue in `field()`.
2. **Depth mark "claude" vs the spoken "Claude Code".** The sibling rejects any depth mark whose
   name is spoken. "claude" (the Claude app) matched inside every "Claude Code" token. The check now
   removes "claude code" from the spoken text before it searches. The Claude app is never named on
   its own in the take, and the stage mark `claude-code` stays banned from the lanes.

Emphasis declarations: the sealed module flips the outlines of `#sw-plate`, `#tile-mid`,
`#step1-box` and `#step2-box` (LAW 38 rule 2). The lane adds `data-emphasis="border"`,
`data-emphasis-target` (the object itself) and a `data-check-at` at the finished state to the
emitted page only. The module on disk is unchanged.
