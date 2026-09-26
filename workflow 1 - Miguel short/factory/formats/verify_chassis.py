"""PROOF OF PROMOTION — every chassis reproduces its approved round-6 page.

The format lab closed on 2026-09-01 with seven definitive videos approved.  This
script is the standing evidence that promoting those generators into `formats/`
changed the CODE and not the OUTPUT: each chassis is rebuilt with the default
YouTube handle and its `index.html` is diffed against the lab's round-6 project.

    ~/Documents/Workspace/.venv/bin/python verify_chassis.py
    ~/Documents/Workspace/.venv/bin/python verify_chassis.py --only cutout

It also proves the handle really is one parameter: each chassis is rebuilt with
`--handle tiktok_ig` into a throwaway directory and the diff against the YouTube
master must touch ONLY the outro chip's line.

Exit code 0 = every chassis reproduced.  Nothing here renders video.
"""
from __future__ import annotations

import argparse
import difflib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FACTORY = HERE.parent
LAB = FACTORY / "references/builds/chassis"  # the approved round-6 pages, frozen out of the format lab (archived) 2026-09-20
PY = str(Path.home() / "Documents/Workspace/.venv/bin/python")

# chassis -> [(built project index.html, the approved round-6 page it must equal)]
CASES = {
    "facesplit": [("facesplit", LAB / "facesplit/fix6/index.html")],
    "takeover": [("takeover", LAB / "takeover/takeover_fix6/index.html")],
    "artifactspine": [
        ("artifactspine", LAB / "artifactspine/fix6/index.html"),
        ("artifactspine_zoom", LAB / "artifactspine/zoom_fix6/index.html"),
    ],
    "whiteboard": [
        ("whiteboard", LAB / "whiteboard/whiteboard_fix6/index.html"),
        ("whiteboard_zoom", LAB / "whiteboard/whiteboard_zoom_fix6/index.html"),
    ],
    "cutout": [("cutout", LAB / "cutout/fix6/index.html")],
}
EXTRA = {"takeover": ["--quiet"]}


def build(name: str, out: Path | None = None) -> None:
    cmd = [PY, "chassis_gen.py", *EXTRA.get(name, [])]
    if out is not None:
        cmd += ["--out", str(out), "--handle", "tiktok_ig"]
    r = subprocess.run(cmd, cwd=HERE / name, capture_output=True, text=True)
    if r.returncode:
        print(r.stdout[-2000:], r.stderr[-2000:], sep="\n")
        raise SystemExit(f"{name}: chassis_gen.py failed")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", default=None, choices=sorted(CASES))
    args = ap.parse_args()
    names = [args.only] if args.only else list(CASES)

    bad = 0
    for name in names:
        print(f"\n=== {name} ===")
        build(name)
        for project, approved in CASES[name]:
            got = HERE / name / "build" / project / "index.html"
            if not approved.exists():
                print(f"  ?  {project:22s} no lab reference at {approved}")
                continue
            same = got.read_bytes() == approved.read_bytes()
            print(f"  {'OK' if same else 'FAIL':4s} {project:22s} "
                  f"{'byte-identical to' if same else 'DIFFERS from'} "
                  f"{approved.relative_to(FACTORY)}")
            if not same:
                bad += 1
                for line in list(difflib.unified_diff(
                        approved.read_text().splitlines(),
                        got.read_text().splitlines(), "approved", "chassis",
                        lineterm=""))[:20]:
                    print("      " + line)

        tmp = Path(tempfile.mkdtemp(prefix=f"{name}_tt_"))
        try:
            build(name, tmp)
            for project, _ in CASES[name]:
                a = (HERE / name / "build" / project / "index.html").read_text()
                b = (tmp / project / "index.html").read_text()
                changed = [l for l in difflib.unified_diff(
                    a.splitlines(), b.splitlines(), lineterm="")
                    if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]
                ok = (len(changed) == 2
                      and all("@migueltorrez" in l for l in changed))
                print(f"  {'OK' if ok else 'FAIL':4s} {project:22s} "
                      f"--handle tiktok_ig touches {len(changed)} line(s) "
                      f"{'(the outro chip only)' if ok else '- EXPECTED ONLY THE OUTRO'}")
                bad += 0 if ok else 1
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    print(f"\n{'ALL CHASSIS REPRODUCE' if not bad else f'{bad} FAILURE(S)'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
