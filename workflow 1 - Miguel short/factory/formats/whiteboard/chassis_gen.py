"""WHITEBOARD CHASSIS — the approved format, promoted out of the lab.

Round-6 winner, approved by Miguel ("amazing!", round 2; the calm camera lane
confirmed round 4).  Two variants, one board:

    whiteboard        the PLAN VIEW + the marker      (the anchor, "SUUUUUPER nice!")
    whiteboard_zoom   the CALM ZOOM LANE              (gentle follow + pull-backs)

Everything except the caption module is byte-frozen at the lab's round-6 state.
The caption canon comes from `pipeline/captions.py`, and the outro @handle is a
parameter: `--handle yt` (default, @migueltorrezai) or `--handle tiktok_ig`
(@migueltorrez.ai).  ONLY the outro differs between the two renders.

    ~/Documents/Workspace/.venv/bin/python chassis_gen.py
    ~/Documents/Workspace/.venv/bin/python chassis_gen.py --handle tiktok_ig
    ~/Documents/Workspace/.venv/bin/python chassis_gen.py --variant zoom --out /tmp/wb
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "lib"))
sys.path.insert(0, str(HERE.parent.parent / "pipeline"))

import captions as CAP                       # noqa: E402
import whiteboard_fix6_core as core          # noqa: E402

VARIANTS = ("fix", "zoom")                   # "fix" = the plan view (the anchor)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    CAP.add_handle_arg(ap)
    ap.add_argument("--variant", default="all", choices=(*VARIANTS, "all"))
    ap.add_argument("--out", default=None, help="project root (default: ./build)")
    args = ap.parse_args()

    core.HANDLE = CAP.handle(args.handle)     # the ONE parametrized constant
    out_root = Path(args.out) if args.out else core.OUT_ROOT
    wanted = VARIANTS if args.variant == "all" else (args.variant,)

    for variant in wanted:
        project, stats, cam = core.emit(variant, out_root=out_root)
        print(f"\n=== {project.name}  (handle {core.HANDLE}) ===")
        print(f"project={project}")
        print(json.dumps(stats, indent=1))
        if cam:
            print(f"  {'t':>6}  {'subject':11s} {'z':>5}  {'hold':>6}  "
                  f"{'lowest ink':>10}  {'clear':>7}  cap-band intruders")
            for r in cam:
                print(f"  {r['t']:6.2f}  {r['subject']:11s} {r['z']:5.2f}  "
                      f"{r['hold_s']:5.2f}s  {r['lowest_ink_px']:9.1f}px  "
                      f"{r['cap_clearance_px']:+6.1f}px  "
                      f"{r['cap_intruders'] or 'NONE'}  "
                      f"(top10 {r['top10_intruders'] or 'none'})")


if __name__ == "__main__":
    main()
