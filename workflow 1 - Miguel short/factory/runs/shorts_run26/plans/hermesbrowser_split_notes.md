# hermesbrowser split: notes from the split author

The split builds the plan as written. No disagreement with the plan. One declaration detail differs from the plan's wording:

## The browser's border flip is not declared in the DOM

- The plan gives both emphases `kind: "box"` and explains them as LAW 38 rule 2 border flips: the drawn object's own outline turns terracotta. The split keeps both flips exactly as the sealed scene draws them.
- The Hermes tile flip (21.38) is declared on `#hb-tile-c` as `data-emphasis="border"`, with the Nous mark `#hb-mark-c` as its target and a check at 21.90. `border` is the kind sibling splits use for a flip on the object itself. Declaring `box` there would make geometry_audit read a box around a raster mark as image text and flag it.
- The browser flip (9.92 to 11.40) is **left undeclared**. The emphasis contract in `visual_laws.py` checks every descendant stroke of the emphasis element, and `#hb-browser` contains the task tick (`.tk`). The tick stays legitimately undrawn (dashoffset 100, stroke-opacity 0) until 20.38. With the browser stamped, `geometry_audit --strict` fails with "Completed emphasis still has an unfinished stroke", measured on this build. The failing stroke is the tick, not the emphasis. Fixing it would mean changing the sealed module's tick or adding tweens that exist only to satisfy the check. I did neither.
- The flip is still a plain border-colour tween on a drawn object. The generator asserts it completes and holds inside its beat, and the 10.60 and 11.20 screenshots show it clearly (`review/split_hermesbrowser_look/sheet_b.png`).
- What I would have done: make the tick a separate element outside `#hb-browser`, on top of the page, so the browser can carry the declaration. That is a change to the design agent's scene, so it is theirs to make if Miguel wants it.
