---
name: project_shorts_draw_on_dash_law
description: "Shorts factory: the SVG draw-on dash must equal the path's own length, and a declared pathLength wins over getTotalLength"
metadata:
  node_type: memory
  type: project
---

Shorts-factory scene modules reveal ink with a GSAP dash animation. The `draw()`
helper copied across run 17 and run 18 wrote a literal `strokeDasharray:100`,
which is a 100-unit dash plus a 100-unit gap, repeating. Miguel spotted the
result on 2026-09-08 in the delivered hermesdoctor short: the warning triangle's
apex was open and the stethoscope's tubes stopped short of the Y junction.

**Why:** run 17 had quietly solved it by declaring `pathLength="100"` on every
drawn path, which renormalises the path so the literal dash is exactly its
length. Run 18's authors declared it on some paths and not others, so the defect
was live only on the undeclared ones and nothing flagged it.

**How to apply:** every draw-on uses
`strokeDasharray:(i,t)=>t.getAttribute("pathLength")||t.getTotalLength()+1`.
A declared pathLength is the unit the dash is measured in, and getTotalLength
still returns the geometric length there, so using it doubles the dash and pops
the drawing on instead of drawing it. The Phone Test and the clerk both look at
the drawing at rest, after the animation, so neither can see either failure.
Written as a law in the factory's STANDARD.md and its LEARNINGS ledger.
See [[project_fable5_video_factory]].

## Index notes (moved from MEMORY.md 2026-09-23)

- a declared pathLength wins over getTotalLength, and no gate sees a broken draw-on
