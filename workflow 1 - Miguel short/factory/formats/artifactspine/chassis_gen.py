"""ARTIFACT SPINE CHASSIS — the approved format, promoted out of the lab.

Round-6 winner, approved by Miguel (round 1: *"Super NICE representation"*;
round 2: `artifactspine_fix` **APPROVED** — *"nice!"*, do not touch; the
zoom-between-pages cut CONFIRMED as a variant of the same format, round 1).

    scroll   the spine scrolls; sections reveal on speech; face switch-ins
    zoom     the same spine, read page by page — the camera zooms BETWEEN pages

Everything except the caption module is byte-frozen at the lab's round-6 state.
The caption canon comes from `pipeline/captions.py`, and the outro @handle is a
parameter: `--handle yt` (default, @migueltorrezai) or `--handle tiktok_ig`
(@migueltorrez.ai).  ONLY the outro differs between the two renders.

    ~/Documents/Workspace/.venv/bin/python chassis_gen.py
    ~/Documents/Workspace/.venv/bin/python chassis_gen.py --variant zoom
    ~/Documents/Workspace/.venv/bin/python chassis_gen.py --handle tiktok_ig
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "lib"))
sys.path.insert(0, str(HERE.parent.parent / "pipeline"))

import captions as CAP                        # noqa: E402
import artifactspine_core as C                # noqa: E402
import artifactspine_fix_core as X            # noqa: E402
import artifactspine_fix3_core as L           # noqa: E402
import artifactspine_fix6_core as R           # noqa: E402
import artifactspine_fix3_gen as GS           # noqa: E402
import artifactspine_zoom_fix3_gen as GZ      # noqa: E402

VARIANTS = ("scroll", "zoom")
# The round-6 project names, kept so the emitted page is diff-able against the
# lab's approved output.
NAME = {"scroll": "artifactspine", "zoom": "artifactspine_zoom"}
TITLE_FROM = {"scroll": "ARTIFACT SPINE (fix round 3)",
              "zoom": "ARTIFACT SPINE ZOOM (fix round 3)"}
TITLE_TO = {"scroll": "ARTIFACT SPINE (fix round 6 — canonical caption)",
            "zoom": "ARTIFACT SPINE ZOOM (fix round 6 — canonical caption)"}


def restage_zoom() -> None:
    """Round 5's stage rect, re-derived from the same expressions the zoom gen
    snapshots at IMPORT time.  Nothing about the camera changes this round."""
    GZ.STAGE_W, GZ.STAGE_H = L.WIN_W, L.WIN_H
    GZ.FRAME_CX, GZ.FRAME_CY = GZ.STAGE_W / 2, GZ.STAGE_H / 2
    GZ.FIT_W = GZ.STAGE_W - 2 * GZ.MARGIN
    GZ.FIT_H = GZ.STAGE_H - 2 * GZ.MARGIN
    print(f"     stage {GZ.STAGE_W:.0f}x{GZ.STAGE_H:.0f} (round 5, kept)"
          f"   fit {GZ.FIT_W:.0f}x{GZ.FIT_H:.0f}"
          f"   at {L.WIN_X:.0f},{L.WIN_Y:.0f}..{L.WIN_X + L.WIN_W:.0f},"
          f"{L.WIN_Y + L.WIN_H:.0f}")


def emit(variant: str, out_root: Path) -> Path:
    R.apply()                                  # the round-5 window + top seat,
    #                                            and the canonical caption object
    gen = GS if variant == "scroll" else GZ
    if variant == "zoom":
        restage_zoom()
    gen.VAR = f"{variant}_fix6"                # the pacing-guard label
    project = out_root / NAME[variant]
    X.bind_assets(project)
    page = gen.build().replace(TITLE_FROM[variant], TITLE_TO[variant])
    print("\n".join(R.verify_page(page)))
    (project / "index.html").write_text(page, encoding="utf-8")
    return project


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    CAP.add_handle_arg(ap)
    ap.add_argument("--variant", default="all", choices=(*VARIANTS, "all"))
    ap.add_argument("--out", default=None, help="project root (default: ./build)")
    args = ap.parse_args()

    C.OUTRO_HANDLE = CAP.handle(args.handle)   # the ONE parametrized constant
    out_root = Path(args.out) if args.out else C.OUT_ROOT
    C.OUT_ROOT = out_root
    out_root.mkdir(parents=True, exist_ok=True)

    for variant in (VARIANTS if args.variant == "all" else (args.variant,)):
        print(f"\n=== {variant} ===")
        project = emit(variant, out_root)
        print(f"project={project}  handle={C.OUTRO_HANDLE}")


if __name__ == "__main__":
    main()
