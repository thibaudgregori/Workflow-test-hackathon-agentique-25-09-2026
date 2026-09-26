"""ARTIFACT SPINE — FIX ROUND 6, the scroll variant.  `artifactspine_fix6.mp4`.

The closing captions round.  ONE change: the caption pill becomes the published
factory's pill — 56.2 px Nunito 800, padding 18.8/33.8, radius 22.5, #C4573A —
and captions too wide for that fixed size are SPLIT at word boundaries instead
of being shrunk.  The seat centre (y 288), the window, the schedule, the solver,
the pacing guard, the SFX and 25 fps are round 5's, untouched.

Like rounds 3, 4 and 5 this generator IS the round-3 generator: it imports
`artifactspine_fix3_gen` and calls its `build()` unmodified after
`artifactspine_fix6_core.apply()` repoints the shared geometry and swaps the
caption object.

Usage:  ~/Documents/Workspace/.venv/bin/python artifactspine_fix6_gen.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import artifactspine_core as C            # noqa: E402
import artifactspine_fix_core as X        # noqa: E402
import artifactspine_fix6_core as R       # noqa: E402
import artifactspine_fix3_gen as G        # noqa: E402

VAR = "fix6"

if __name__ == "__main__":
    R.apply()
    G.VAR = VAR                            # the pacing-guard label
    project = C.OUT_ROOT / VAR
    X.bind_assets(project)
    page = G.build().replace(
        "ARTIFACT SPINE (fix round 3)",
        "ARTIFACT SPINE (fix round 6 — canonical caption)")
    print("\n".join(R.verify_page(page)))
    (project / "index.html").write_text(page, encoding="utf-8")
    print(f"project={project}")
