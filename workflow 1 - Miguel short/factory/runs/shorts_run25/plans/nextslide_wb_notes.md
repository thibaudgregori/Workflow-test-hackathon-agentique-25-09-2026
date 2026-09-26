# nextslide: whiteboard author notes

The whiteboard follows the plan. These are the places where it differs from the
plan's exact wording, and why.

1. **The three model arrows merge into one landing point (a law required this).** The plan
   asked for `anchor_points(CARD, 3, "right")`: three different heights on the card's
   right edge. The board check `assert_anchor_law` refuses that. On a vertical side,
   three arrows can be neither level nor mirrored. So each tile draws a short tick
   into one terracotta bus at x 402, and one arrow runs from the bus into the card's
   right-edge centre (382, 252). All three declared connectors land on that one point.
   The drawing now shows NextSlide as the funnel the plan describes.
2. **The verdict is written in two halves, each on its own word.** `PRETTY` is
   written at 26.94 on 'pretty'. `+ UNDERSTANDABLE` is written at 28.06 on
   'understandable'. The two halves form one centred line under the easel.
   `label_plan` has two entries so that neither half appears before its word is
   spoken (LAW 24). The captioner produced a lone pill, 'understandable.', at 28.06,
   the same moment the board writes UNDERSTANDABLE, which breaks LAW 4. I recut the
   pills on the same words: 'both pretty' | 'and also understandable.' (both under the
   756 px limit).
3. **Easel emphasis = the board frame retraced in terracotta**, at 28.06 and held until
   the outro. The plan said "box_emphasis around the easel". I used the board frame
   because it is still boxing a drawn object (LAW 38 rule 2), and the split does the
   same thing with its `.bframe` flip (LAW 51). A box around the whole tripod would
   put a second frame around the first.
4. **The easel stays on screen, still shifted left, through chapter 2.** The plan's
   list for chapter 2 leaves it out. But the plan's lifetimes make the easel an
   anchor, and the split handoff keeps it displaced until it slides home on
   'honestly' (21.86). I followed the lifetimes and the split.
5. **Beat 2's "the card's arrow into the easel brightens on 'create presentations'"
   is not drawn.** That arrow is already terracotta, and the board has no brighter ink.
6. **Outro.** The harness's opaque rising sheet carries the chassis lockup (rule,
   `@migueltorrez.ai`, daily AI). The plan's "small ink easel glyph" under the lockup
   is not drawn, because the harness forbids any ink at or after the outro anchor.
7. **Suggestion, not built:** a small handwritten `CHATGPT` under the green ChatGPT
   tile (20.72) would help separate it from the black OpenAI knot directly above it.
   The plan's labels are fixed, so it is not on the board.
8. **Chapter seams.** The erase at 8.98 removes only the OpenAI tile and its arrow
   (two rigids), so `chapter_seams()` does not count it as a registry seam. The QC
   `--seams` still lists it with 17.5 and 21.62. At all three seams, the easel and/or
   the NEXTSLIDE card stay fully drawn (LAW 45).
