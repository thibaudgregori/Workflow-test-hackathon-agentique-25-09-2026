#!/usr/bin/env python
"""Carry the v5 two-defect fix into the rest of the cutout backfill fleet.

`deepresearch` is the proof; the other twelve remakes carry the same generator
pattern, copied per video, so the same three edits apply verbatim to each. This
script performs them, reports what it could not do, and CHANGES NOTHING unless
`--write` is passed.

    ../../../.venv/bin/python cutout_v5_migrate.py                # dry run, all
    ../../../.venv/bin/python cutout_v5_migrate.py --write --only grokprice

WHAT IT DOES, per backfill/port directory:

 1  SOURCE      renames `src/source_audio.wav` to
                `src/analysis_16k_mono_DO_NOT_MIX.wav`, and reports (it cannot
                guess) that `src/voice_master_48k.m4a` must be copied in from the
                run's `cuts/<id>/audio.m4a`.  THE RENAME IS THE FORCING
                FUNCTION: an un-migrated generator dies on a missing file
                instead of quietly shipping an 8 kHz-ceilinged mix.
 2  GENERATOR   swaps the `source_audio.wav` transcode for
                `cutout_media.stage_voice`, and adds the `cutout_media` import.
 3  REPORT      prints, per video, what still needs a human: the voice file, and
                the `ship.py --master --display` re-run that produces the v5
                matte set (which needs the session's alpha and cut master and so
                cannot be done from here).

The VIDEO half is deliberately NOT auto-patched. It needs a new matte set per
session and a per-video `--matte` argument, and a generator whose matte still has
no `_rim.webm` twin resolves `--matte-mode auto` to `baked` — the v4 picture,
correct but unfixed. Auto-editing the markup without the assets would produce a
build that references a matte layer that does not exist.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FACTORY = HERE.parents[2]
ROOTS = [FACTORY / "the format lab (archived on Drive under Testing & Experiments)", FACTORY / "the format lab (archived on Drive under Testing & Experiments)"]

# The voice block comes in at least three shapes across the fleet — the source is
# `C.SRC/source_audio.wav` in most, bare `SRC/source_audio.wav` in some, and
# `CUT/audio.wav` in `erdos` (which reaches past the package straight into the
# cut's 16 kHz analysis wav).  All of them are the same defect, so the pattern
# matches the STRUCTURE — stage a voice.m4a by transcoding something — and
# records which source it found rather than assuming.
OLD_VOICE = re.compile(
    r'[ \t]*voice = stage_dir / "v/voice\.m4a"\n'
    r'[ \t]*if not voice\.exists\(\):\n'
    r'(?P<body>(?:[ \t]*(?:subprocess\.run|str\(|"|\)).*\n)+?)'
    r'(?=[ \t]*(?:shutil|for |media|return|#))',
    re.MULTILINE)

SRC_IN_BODY = re.compile(r'(?:C\.)?(?:SRC|CUT)\s*/\s*"([^"]+)"')

NEW_VOICE = (
    '    # DEFECT 2 (2026-09-01): this used to transcode the 16 kHz MONO ANALYSIS\n'
    '    # track into the mix — an 8 kHz Nyquist ceiling, so the top octave of his\n'
    '    # voice was gone before the encoder saw it.  `resolve_voice` picks the\n'
    '    # 48 kHz master and refuses a low-rate file by name.\n'
    '    CM.stage_voice(C.SRC, stage_dir)\n')

IMPORT_ANCHOR = "import cutout_core as C                                        # noqa: E402\n"
IMPORT_ADD = "import cutout_media as CM                                      # noqa: E402\n"


def generators(d: Path):
    for q in sorted(d.rglob("*_cutout_gen.py")) + sorted(d.rglob("*_gen.py")):
        if q.is_file() and "cutout" in q.name:
            yield q


def migrate(d: Path, write: bool) -> dict:
    rec = dict(video=d.name, actions=[], todo=[])
    src = d / "src"
    wav = src / "source_audio.wav"
    new_wav = src / "analysis_16k_mono_DO_NOT_MIX.wav"
    if wav.exists():
        rec["actions"].append(f"rename {wav.name} -> {new_wav.name}")
        if write:
            shutil.move(str(wav), str(new_wav))
    voices = [n for n in ("voice_master_48k.m4a", "voice_master.m4a", "audio.m4a",
                          "source_cut_master.mp4", "master.mp4")
              if (src / n).exists()]
    if not voices:
        rec["todo"].append(
            f"copy the 48 kHz voice in:  cp <run>/cuts/<id>/audio.m4a "
            f"{src}/voice_master_48k.m4a")
    else:
        rec["actions"].append(f"voice already present: {voices[0]}")
    seen = set()
    for g in generators(d):
        if g in seen:
            continue
        seen.add(g)
        s = g.read_text()
        if "CM.stage_voice" in s:
            rec["actions"].append(f"{g.name}: already migrated")
            continue
        m = OLD_VOICE.search(s)
        if not m:
            rec["todo"].append(f"{g.name}: voice block not recognised — patch by hand")
            continue
        found = SRC_IN_BODY.findall(m.group("body"))
        rec["actions"].append(
            f"{g.name}: was mixing {found[0] if found else '(unknown source)'}")
        s2 = s[:m.start()] + NEW_VOICE + s[m.end():]
        if IMPORT_ADD not in s2 and IMPORT_ANCHOR in s2:
            s2 = s2.replace(IMPORT_ANCHOR, IMPORT_ANCHOR + IMPORT_ADD, 1)
        rec["actions"].append(f"{g.name}: voice -> cutout_media.stage_voice")
        if write:
            g.write_text(s2)
    rec["todo"].append(
        "VIDEO (by hand, needs the session): ship.py --alpha <alpha.mkv> --plate "
        "<plate.mp4> --master <cut master.mp4> --display 1188x990 --out "
        "<stem>_v5, then re-run the generator with --matte <stem>_v5_cut.webm "
        "--matte-mode layered")
    return rec


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", action="store_true", help="apply (default: dry run)")
    ap.add_argument("--only", default=None, help="one video directory name")
    a = ap.parse_args()
    dirs = [d for r in ROOTS if r.is_dir() for d in sorted(r.iterdir())
            if d.is_dir() and not d.name.startswith("_")]
    if a.only:
        dirs = [d for d in dirs if d.name == a.only]
        if not dirs:
            raise SystemExit(f"no backfill or port directory named {a.only}")
    print("DRY RUN — nothing written (pass --write)" if not a.write else "WRITING")
    for d in dirs:
        rec = migrate(d, a.write)
        print(f"\n{rec['video']}")
        for x in rec["actions"]:
            print(f"  do   {x}")
        for x in rec["todo"]:
            print(f"  TODO {x}")


if __name__ == "__main__":
    sys.exit(main())
