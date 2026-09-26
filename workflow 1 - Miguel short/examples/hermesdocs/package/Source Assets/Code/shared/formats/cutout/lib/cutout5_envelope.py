"""cutout5 — silhouette envelope on the SHIPPED v3 matte (task id: cutout5).

FIX ROUND 5.  Two debts are settled in one measurement:

  1. `_shared/SAM2.md` shipped `matte_sam2_rim_v3.webm` but `cutout3c_matteswap.sh`
     deliberately did NOT re-measure the envelope ("the brief is a matte swap and
     not a new layout").  SAM2.md flags the re-derivation as owed.  The envelope
     still in use, `cutout3_envelope.json`, was measured on the **v1** SAM2 matte.

  2. Round 5 scales the silhouette 1.10x about its bottom-centre.  A bigger
     silhouette moves every gutter, every lane crossing and the caption's
     clearance, so guarding round 5 against a v1-matte envelope would be guarding
     against a shape that is neither the shipped matte nor the shipped size.

The envelope itself is measured in PLATE space (1080x900) and is therefore
scale-free: `FixStage` maps it onto the canvas with `k = PLATE_SCALE` and the
round-5 origin, so the SAME json describes the bigger silhouette correctly.

Same measurement code as rounds 1-3 (`cutout_fix_envelope.measure`).

Run:  python cutout5_envelope.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from cutout_fix_envelope import LAB, SHARED, measure

MATTE = SHARED / "matte_sam2_rim_v3.webm"
OUT = LAB / "cutout5_envelope.json"
PREV = LAB / "cutout3_envelope.json"          # measured on matte_sam2_rim.webm (v1)


def main() -> None:
    if not MATTE.exists():
        raise SystemExit(f"missing {MATTE}")
    env = measure(MATTE, "best")
    env["source"] = str(MATTE)
    OUT.write_text(json.dumps(env))
    u, hd = env["union"], env["head"]
    print(f"cutout5: {env['frames_sampled']} frames  union y{u['y0']}..{u['y1']} "
          f"x{u['x0']:.0f}..{u['x1']:.0f}  head y{hd['y0']}..{hd['y1']} "
          f"x{hd['x0']:.0f}..{hd['x1']:.0f}")
    if PREV.exists():
        prev = json.loads(PREV.read_text())
        pu = prev["union"]
        print(f"  vs cutout3 (v1 matte): union y0 {pu['y0']} -> {u['y0']}  "
              f"y1 {pu['y1']} -> {u['y1']}")
        for side, sign in (("row_x1", +1), ("row_x0", -1)):
            p = np.array(prev[side], float)
            n = np.array(env[side], float)
            live = (p >= 0) & (n >= 0) & (p < 1080) & (n < 1080) if side == "row_x0" \
                else (p >= 0) & (n >= 0)
            d = (p[live] - n[live]) * sign
            print(f"  {side} vs cutout3: mean {d.mean():+.1f}px  max {d.max():+.0f}px  "
                  f"min {d.min():+.0f}px  rows narrowed {int((d > 0).sum())} / "
                  f"{int(live.sum())}")


if __name__ == "__main__":
    main()
