# ccremote: notes from the split author

The plan is built as written. There is no disagreement with it. Two lane-side declarations were added to the EMITTED html, not to the sealed module (its sha256 is unchanged, and `artwork-check` passes after the build):

1. **Connector check declarations.** The sealed scene emits `data-connect-to` on its four wires, but not `data-anchor-side`, `data-anchor-fraction` or `data-check-at`. `visual_laws.py` (strict gate 1) needs all three. `ccremote_split_gen.py::declare_connectors` adds `left / 0.5 / 18.00` to each wire. At 18.00 all four wires are drawn and chapter 1 is on screen.
2. **The phone wire names the plate, not the switch's svg box.** `wire-in` ended on the plate's outer edge at x 450, and the handoff measured that as 0.0 px. The id `sw` is the 220 px svg box, which starts at x 430, so the strict anchor check would have measured a 20 px miss. The lane therefore declares `data-connect-to="sw-plate"`, the drawn plate itself. The line is unchanged and still ends on the plate's outline. Strict geometry reports 0 errors.

**Emphasis.** All four emphases are border flips of the drawn object's own outline (plate stroke, middle tile, the two check boxes), and no separate emphasis element exists. So there is no `data-emphasis` node to declare. Adding one on the target itself would compare the target with itself.

**Captions.** "Claude" and "Code" are never split across two pills (`_splits_name`). "ask it to turn it on," would echo the live ASK IT TO TURN IT ON row word for word (LAW 4), so the captions split it as "ask it" / "to turn it on,".
