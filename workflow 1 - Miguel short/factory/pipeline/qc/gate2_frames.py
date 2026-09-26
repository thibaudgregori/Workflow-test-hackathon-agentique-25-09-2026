"""Native frame review, token-burner by default: see EVERY distinct visual state.

Adapted from bradautomates/claude-video, tuned for this factory. Instead of scene
detection (which misses low-contrast cream-on-cream events), the default samples
the visual zone at a fixed 3 fps UNCAPPED, then collapses stillness with the
16x16-grayscale dedup (mean abs diff vs the last KEPT frame). Our shorts are
event-then-stillness by law, so uncapped capture converges to the true distinct-
state count (~20-40 frames for a 50s short, ~330 tokens each at 512w).

What Brad's skill doesn't have: Scribe word timings. With --video-id (or
--transcript), manifest.md interleaves each frame with the words spoken since
the previous kept frame, so claim-sync / highlight-match / key-term checks read
straight off the manifest. It also emits a stillness map: kept-frame gaps >= 3s
are confirmed stillness; windows > 6s where every sample survived dedup (nothing
still) are idle-motion candidates - corroborate with idle_motion_scan.py.

And a POP-IN map: a kept frame preceded by a drop, carrying a large-element diff,
and followed by a drop went from stillness to a finished element in one sample.
Those lines carry "[possible pop-in]" and the reviewer MUST look at the entrance
(grokpublish shipped a distributor tree that appeared in a single frame inside a
nominally 0.55s draw). It is a marker, not a gate: legitimate 0.4s pops trip it.

Usage:
  gate2_frames.py <video.mp4> [--video-id hermes] [--transcript words.json]   (pipeline/frame_review.py until 2026-09-20)
                  [--out DIR] [--fps 3] [--width 512] [--budget N] [--full]

Crop default: top 50% (coded visuals + caption chip at the seam). --full keeps
the whole frame (face rules). Frames + manifest are intermediates: the reviewing
agent Reads them, then deletes the dir.
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

# `media` lives in pipeline/, one level up from pipeline/qc/, and this file is
# run AS A SCRIPT by qc_pass (check 12), so sys.path[0] is pipeline/qc and the
# bare import cannot resolve.  Its two siblings — qc_pass.py:132 and
# gate3_gemini.py:52 — both insert pipeline/ before importing it; this one did
# not, so Gate 2 failed with ModuleNotFoundError on every lane it judged
# (found on run 24's cursorspacex split, 2026-09-21).
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # pipeline/
from media import probe_duration  # noqa: E402  shared (2026-09-20)

FACTORY = Path(__file__).resolve().parent.parent
DEDUP_THRESHOLD = 2.0    # mean abs diff on 16x16 grayscale, 0-255 scale
STILL_GAP = 3.0          # kept-frame gap that counts as confirmed stillness
IDLE_WINDOW = 6.0        # no-drop run this long = idle-motion candidate
# Pop-in candidates (Miguel, 2026-08-12). Stillness -> one big step -> stillness is the
# signature of an element switched on rather than built. Calibrated on the grokpublish v3
# encode: dedup noise sits at 2.0-3.1, real element arrivals at 4.0-16, and whole-ground
# section cuts at 148-166 (those are cuts, not pop-ins, hence the ceiling). This is a
# MARKER, not a verdict - a fast-but-legitimate 0.4s pop can trip it too, and the reviewer
# resolves it by looking at the entrance. It never fails anything.
POPIN_SPIKE = 4.0        # mean abs diff that counts as a large new element region
POPIN_CUT = 60.0         # above this the whole ground changed: a section cut, not a pop-in

STEMS = {"hackers": "2026-08-08_20-47-44", "grokbuild": "2026-08-08_20-54-32",
         "hermes": "2026-08-08_20-59-13", "grokprice": "2026-08-08_21-09-49",
         "deepresearch": "2026-08-08_21-14-48", "slop": "2026-08-08_21-19-39",
         "threed": "2026-08-08_21-35-36", "productivity": "2026-08-08_21-40-17",
         "meatwrapper": "2026-08-08_22-15-31", "fablevssol": "2026-08-08_22-21-45"}

TRANSCRIPTS = {
    # auto-discovered: any run's cuts/<id>/transcript_tight.json registers itself,
    # so concurrent sessions never need to edit this file (shadowing hazard, 2026-08-11)
    **{c.parent.name: c
       for c in sorted(FACTORY.glob("runs/shorts_run*/cuts/*/transcript_tight.json"))
       },
}


def gray16(path):
    with Image.open(path) as im:
        return list(im.convert("L").resize((16, 16)).getdata())


def mean_abs_diff(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


def load_words(args):
    tr = None
    if args.transcript:
        tr = Path(args.transcript)
    elif args.video_id:
        tr = TRANSCRIPTS[args.video_id]
    if not tr:
        return None
    if not tr.exists():
        sys.exit(f"transcript not found: {tr}")
    words = json.loads(tr.read_text())["words"]
    return [(w["start"], w["text"]) for w in words if w.get("type") == "word"]


def words_between(words, t0, t1):
    return " ".join(txt for (s, txt) in words if t0 <= s < t1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--video-id", choices=list(TRANSCRIPTS), default=None,
                    help="auto-load this video's word-timed transcript")
    ap.add_argument("--transcript", default=None, help="explicit words JSON path")
    ap.add_argument("--out", default=None)
    ap.add_argument("--fps", type=float, default=3.0)
    ap.add_argument("--width", type=int, default=512)
    ap.add_argument("--budget", type=int, default=None,
                    help="optional hard cap; default uncapped (token-burner)")
    ap.add_argument("--full", action="store_true",
                    help="full frame instead of the top 50%% visual zone")
    args = ap.parse_args()

    video = Path(args.video).resolve()
    if not video.exists():
        sys.exit(f"not found: {video}")
    duration = probe_duration(video)
    words = load_words(args)
    out = Path(args.out) if args.out else video.parent / f"frames_{video.stem}"
    out.mkdir(parents=True, exist_ok=True)

    tmp = Path(tempfile.mkdtemp(prefix="fr_"))
    try:
        crop = "" if args.full else "crop=iw:ih*0.5:0:0,"
        subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-vf",
                        f"{crop}fps={args.fps},scale={args.width}:-2",
                        "-q:v", "4", str(tmp / "u_%05d.jpg"), "-y"], check=True)
        cands = sorted(tmp.glob("u_*.jpg"))
        step = 1.0 / args.fps

        kept, last_sig, drops = [], None, []   # drops: (t, dropped?)
        for i, f in enumerate(cands):
            t = i * step
            sig = gray16(f)
            d = mean_abs_diff(sig, last_sig) if last_sig is not None else None
            if d is not None and d <= DEDUP_THRESHOLD:
                drops.append((t, True))
                continue
            drops.append((t, False))
            kept.append((t, f, i, d))
            last_sig = sig
        if cands and (not kept or kept[-1][1] != cands[-1]):
            kept.append(((len(cands) - 1) * step, cands[-1], len(cands) - 1, None))

        if args.budget and len(kept) > args.budget:
            idx = {round(i * (len(kept) - 1) / (args.budget - 1))
                   for i in range(args.budget)}
            kept = [kf for i, kf in enumerate(kept) if i in idx]

        # pop-in candidates: the sample before was a drop (nothing moving), this sample
        # jumps by a large-element amount, and the sample after is a drop again (already
        # static). An element that BUILDS spreads that change over >=2 samples.
        was_dropped = [dr for (_t, dr) in drops]
        popin_t = set()
        for (t, _f, i, d) in kept:
            if d is None or not (POPIN_SPIKE <= d < POPIN_CUT):
                continue
            if i - 1 >= 0 and not was_dropped[i - 1]:
                continue
            if i + 1 < len(was_dropped) and not was_dropped[i + 1]:
                continue
            popin_t.add(round(t, 3))

        # idle candidates: runs > IDLE_WINDOW where nothing was dropped
        idle_runs, run_start = [], None
        for (t, dropped) in drops:
            if dropped:
                if run_start is not None and t - run_start >= IDLE_WINDOW:
                    idle_runs.append((run_start, t))
                run_start = None
            elif run_start is None:
                run_start = t
        if run_start is not None and duration - run_start >= IDLE_WINDOW:
            idle_runs.append((run_start, duration))

        lines = [f"# Frame review: {video.name}",
                 f"{duration:.1f}s · {len(kept)} distinct states from "
                 f"{len(cands)} samples @ {args.fps:g}fps · "
                 f"{len(cands) - len(kept)} stillness frames collapsed",
                 ""]
        if idle_runs:
            lines.append("## IDLE-MOTION CANDIDATES (no still frame for >"
                         f"{IDLE_WINDOW:.0f}s - corroborate with idle_motion_scan.py)")
            for (a, b) in idle_runs:
                lines.append(f"- {a:.1f}s to {b:.1f}s ({b - a:.1f}s of continuous motion)")
            lines.append("")
        if popin_t:
            lines.append("## POSSIBLE POP-INS (still -> one big step -> still: READ the "
                         "entrance on each, an element must never arrive fully formed)")
            for t in sorted(popin_t):
                lines.append(f"- t={t:.2f}s")
            lines.append("")
        lines.append("## Frames")
        prev_t = 0.0
        manifest = []
        for (t, f, _i, _d) in kept:
            name = f"f_{int(t // 60):02d}{int(t % 60):02d}_{int((t % 1) * 1000):03d}.jpg"
            shutil.copy2(f, out / name)
            manifest.append((t, name))
            gap = t - prev_t
            still = f"  [still {gap:.1f}s before this]" if gap >= STILL_GAP else ""
            pop = "  [possible pop-in]" if round(t, 3) in popin_t else ""
            spoken = f'\n  says: "{words_between(words, prev_t, t + step)}"' if words else ""
            lines.append(f"- t={int(t // 60):02d}:{t % 60:04.1f}  {name}{still}{pop}{spoken}")
            prev_t = t
        (out / "manifest.md").write_text("\n".join(lines) + "\n")

        print(lines[1])
        if idle_runs:
            print(f"IDLE CANDIDATES: {['%.1f-%.1fs' % r for r in idle_runs]}")
        if popin_t:
            print(f"POSSIBLE POP-INS: {['%.2fs' % t for t in sorted(popin_t)]}")
        for t, name in manifest:
            print(f"  t={int(t // 60):02d}:{t % 60:04.1f}  {out / name}")
        print(f"\nManifest: {out / 'manifest.md'}  (delete dir after review)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
