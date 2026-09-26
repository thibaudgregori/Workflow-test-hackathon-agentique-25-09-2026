"""ARTIFACT SPINE — FIX ROUND 6, the ZOOM variant.  `artifactspine_zoom_fix6.mp4`.

The same one change as the scroll cut, because the canon is a factory-wide
object: the caption pill becomes the published factory's pill (56.2 px Nunito
800, padding 18.8/33.8, radius 22.5, #C4573A) and over-wide captions are SPLIT
at word boundaries rather than shrunk.

`restage()` is inherited from round 5 verbatim: `artifactspine_zoom_fix3_gen`
snapshots the stage rect into module constants at IMPORT time, and round 5's
rect (40,372 1000x1416) is what round 6 keeps, so the four derived constants
must be re-derived here from the same expressions the module uses.  Nothing
about the camera changes this round — the pill sits 27 px above the stage's top
edge, so no stop can put board ink under it.

Usage:  ~/Documents/Workspace/.venv/bin/python artifactspine_zoom_fix6_gen.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import artifactspine_core as C            # noqa: E402
import artifactspine_fix_core as X        # noqa: E402
import artifactspine_fix3_core as L       # noqa: E402
import artifactspine_fix6_core as R       # noqa: E402
import artifactspine_zoom_fix3_gen as G   # noqa: E402

VAR = "zoom_fix6"


def restage() -> None:
    G.STAGE_W, G.STAGE_H = L.WIN_W, L.WIN_H
    G.FRAME_CX, G.FRAME_CY = G.STAGE_W / 2, G.STAGE_H / 2
    G.FIT_W = G.STAGE_W - 2 * G.MARGIN
    G.FIT_H = G.STAGE_H - 2 * G.MARGIN
    print(f"     ROUND 6  stage {G.STAGE_W:.0f}x{G.STAGE_H:.0f} (round 5, kept)"
          f"   fit {G.FIT_W:.0f}x{G.FIT_H:.0f}"
          f"   at {L.WIN_X:.0f},{L.WIN_Y:.0f}..{L.WIN_X + L.WIN_W:.0f},"
          f"{L.WIN_Y + L.WIN_H:.0f}")


if __name__ == "__main__":
    R.apply()
    restage()
    G.VAR = VAR                            # the pacing-guard label
    project = C.OUT_ROOT / VAR
    X.bind_assets(project)
    page = G.build().replace(
        "ARTIFACT SPINE ZOOM (fix round 3)",
        "ARTIFACT SPINE ZOOM (fix round 6 — canonical caption)")
    print("\n".join(R.verify_page(page)))
    (project / "index.html").write_text(page, encoding="utf-8")
    print(f"project={project}")
