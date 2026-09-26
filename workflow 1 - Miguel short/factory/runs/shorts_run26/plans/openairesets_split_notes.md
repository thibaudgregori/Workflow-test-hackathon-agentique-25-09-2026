# openairesets: split author notes

The split builds the plan and consumes the sealed scene unchanged on disk
(`gen/openairesets_scene.py`, sha256 422919c7...). Two departures are made on the
EMITTED page only, both because a law or a law's instrument forbids the letter of
the plan/module. The cutout author will meet both on the same module.

## 1. `/ MONTH` waits for "month" (LAW 24, NO PEEK-AHEAD)

- Plan and module: `$200` on "$200" (4.50), ` / MONTH` on "per" (5.36).
- "month" is spoken at 5.52, so for 0.16 s MONTH is on screen before its word.
- The split moves the ` / MONTH` tween to 5.52 (the start of "month", inside that
  word's own window). `$200` is unchanged. Same repair a run-24 sibling made on a
  multi-word key ("the whole key is behind its words").

## 2. The emphasis box is inked TERRA_L, not TERRA

- Module: `#emph-hourglass` is a 5 px border in TERRA `#C4573A`.
- The hourglass's sand is also TERRA, so `geometry_audit.py --strict`
  (`visual_laws`) refuses it: "Emphasis uses the same color as its target ink
  (rgb(196, 87, 58))".
- The split re-inks the box border to TERRA_L `rgb(221,114,89)`, the terracotta the
  GRAPHIC CHART and LAW 38 rule 2 name for emphasis flips. It is still the accent
  and no longer the sand. Geometry, timing, radius and target are unchanged.
- What I would have done at design time: keep the sand TERRA and draw the box in
  TERRA_L in the module itself, so every DOM lane gets it from one place.
