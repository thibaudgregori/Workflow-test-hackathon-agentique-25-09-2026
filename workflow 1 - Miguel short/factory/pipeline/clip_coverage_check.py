#!/usr/bin/env python3
"""CLIP COVERAGE — every frame belongs to exactly one clip, and no frame is blank.

WHY THIS EXISTS
---------------
Run 9's `impossibletask` shipped with a **single fully blank cream frame** at
20.60 s and again at 25.36 s, in both the split and the cutout.  The independent
Viewer Test decoded them; no gate in the factory could see them, because Gate 1
samples at 0.25 s, Gate 2 at 3 fps and Gate 3 looks at a handful of described
frames.  A one-frame hole is invisible to every sampled instrument and perfectly
visible on a phone, where it reads as a flicker at a beat seam.

The hole came from a "cure" for the OPPOSITE defect.  The producer's runtime is
half-open — `p >= start && p < start + duration` — so a clip whose authored end
lands EXACTLY on a frame time has that frame decided by one ulp of double
arithmetic.  `16.70 + 3.900 = 20.599999999999998` loses frame 515; a different
beat's `20.62 + 4.740 = 25.360000000000003` keeps it.  Same code, opposite
outcomes, both wrong to rely on.

So this check does not trust arithmetic, and it does not trust sampling:

  A. THE PAGE (static, exact).  Read the emitted `index.html`, snap the composition
     to its own frame grid, and for every frame ask which clips of each track
     GROUP are live under the producer's exact rule.  Report every frame owned by
     two clips (a ghost) and every interior frame owned by none (a hole).
  B. THE RENDER (decoded, every frame).  Decode the finished mp4 frame by frame
     and measure the ink in the visual zone.  Any INTERIOR frame whose zone is
     empty — bounded on both sides by frames that are not — is a hole that
     reached the file.  Leading and trailing empties are reported, never failed:
     a composition is allowed to open on cream before its first stroke.

Both halves are cheap and neither samples.

USAGE
-----
    clip_coverage_check.py <render.mp4> [--html <project>/index.html]
                           [--zone-bottom 862.5] [--groups stage,tz,scap]
                           [--json OUT.json] [--ink-floor 0.0006]

Exit code 1 on any failure, 0 when clean.  With `--json` the full record is
written for the run's paperwork.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

DEFAULT_GROUPS = ("stage", "tz", "scap")
CREAM = (0xF6, 0xF1, 0xEA)          # RGB — the factory ground


# =============================================================================
# A.  THE PAGE
# =============================================================================
CLIP_RE = re.compile(
    r'<(?P<tag>section|div|video|img)\b[^>]*?\bclass="(?P<cls>[^"]*\bclip\b[^"]*)"[^>]*?>',
    re.I)


def _attr(tag_html: str, name: str) -> str | None:
    m = re.search(rf'\b{name}="([^"]*)"', tag_html)
    return m.group(1) if m else None


def parse_clips(html: str, groups: tuple[str, ...]) -> tuple[dict, float, int]:
    root = re.search(r'<div[^>]*\bid="root"[^>]*>', html) or \
        re.search(r'<div[^>]*data-composition-id[^>]*>', html)
    if not root:
        raise SystemExit("no #root element in the page")
    dur = float(_attr(root.group(0), "data-duration") or 0.0)
    fps = int(float(_attr(root.group(0), "data-fps") or 25))
    by_group: dict[str, list[dict]] = {g: [] for g in groups}
    for m in CLIP_RE.finditer(html):
        tag = m.group(0)
        cls = set(m.group("cls").split())
        hit = [g for g in groups if g in cls]
        if not hit:
            continue
        s = _attr(tag, "data-start")
        d = _attr(tag, "data-duration")
        if s is None or d is None:
            continue
        by_group[hit[0]].append({"id": _attr(tag, "id") or "?",
                                 "start": float(s), "dur": float(d)})
    return by_group, dur, fps


def page_coverage(by_group: dict, dur: float, fps: int) -> dict:
    """The producer's own rule, applied to every frame of the composition."""
    n = int(math.floor(round(dur * fps, 6) + 1e-9))
    out: dict[str, dict] = {}
    for g, clips in by_group.items():
        if len(clips) < 2:
            out[g] = {"clips": len(clips), "checked": False,
                      "note": "fewer than two clips — nothing can hand over"}
            continue
        first = min(c["start"] for c in clips)
        last = max(c["start"] + c["dur"] for c in clips)
        holes, ghosts = [], []
        for k in range(n):
            p = k / fps
            # THE PRODUCER'S OWN RULE, verbatim: p >= start && p < start + dur
            live = [c["id"] for c in clips
                    if p >= c["start"] and p < c["start"] + c["dur"]]
            if len(live) > 1:
                ghosts.append({"frame": k, "t": round(p, 4), "clips": live})
            elif not live and first - 1e-9 <= p < last - 1e-9:
                holes.append({"frame": k, "t": round(p, 4)})
        out[g] = {"clips": len(clips), "checked": True, "frames": n,
                  "span": [round(first, 4), round(last, 4)],
                  "holes": holes, "ghosts": ghosts,
                  "pass": not holes and not ghosts}
    return out


# =============================================================================
# B.  THE RENDER
# =============================================================================
def zone_ink_series(mp4: Path, zone_bottom: float
                    ) -> tuple[float, int, int, list[float]]:
    """THE INK SCAN — every decoded frame, no sampling.

    Returns `(fps, zone_bottom_px, zone_width_px, per-frame ink fraction)` for the
    visual zone `0..zone_bottom` given in 1080x1920 design px and scaled to
    whatever the encode actually is (the split ships at portrait-4k).

    Factored out of `decoded_coverage` so other checks can reuse the SAME
    instrument instead of writing a second one that measures ink slightly
    differently — `whiteboard_build.assert_zone_never_blank` is the first caller.
    """
    cap = cv2.VideoCapture(str(mp4))
    if not cap.isOpened():
        raise SystemExit(f"cannot open {mp4}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # the zone is given in the 1080x1920 design space; scale it to the encode
    y1 = int(round(zone_bottom * h / 1920.0))
    y1 = max(1, min(h, y1))
    ground = np.array(CREAM[::-1], dtype=np.int16)          # BGR
    frac: list[float] = []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        zone = frame[0:y1, 0:w].astype(np.int16)
        dev = np.abs(zone - ground).max(axis=2)
        # 18 levels of tolerance: JPEG/h264 ringing on flat cream measures <8
        ink = int((dev > 18).sum())
        frac.append(ink / float(zone.shape[0] * zone.shape[1]))
    cap.release()
    return fps, y1, w, frac


def decoded_coverage(mp4: Path, zone_bottom: float, ink_floor: float) -> dict:
    fps, y1, w, frac = zone_ink_series(mp4, zone_bottom)
    k = len(frac)
    empty = [i for i, f in enumerate(frac) if f < ink_floor]
    inked = [i for i, f in enumerate(frac) if f >= ink_floor]
    interior: list[dict] = []
    if inked:
        lo, hi = inked[0], inked[-1]
        interior = [{"frame": i, "t": round(i / fps, 4), "ink_frac": round(frac[i], 6)}
                    for i in empty if lo < i < hi]
    return {"frames": k, "fps": round(fps, 3), "zone": [0, y1, w, y1],
            "ink_floor": ink_floor,
            "min_ink_frac": round(min(frac), 6) if frac else None,
            "empty_frames_total": len(empty),
            "leading_trailing_empty": len(empty) - len(interior),
            "interior_blank_frames": interior,
            "pass": not interior}


# =============================================================================
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mp4", type=Path)
    ap.add_argument("--html", type=Path, default=None,
                    help="the project's index.html (the static half)")
    ap.add_argument("--zone-bottom", type=float, default=862.5,
                    help="bottom of the visual zone in 1080x1920 design px")
    ap.add_argument("--groups", default=",".join(DEFAULT_GROUPS))
    ap.add_argument("--ink-floor", type=float, default=0.0006)
    ap.add_argument("--json", type=Path, default=None)
    a = ap.parse_args()

    rec: dict = {"render": str(a.mp4)}
    ok = True

    if a.html:
        by_group, dur, fps = parse_clips(a.html.read_text(encoding="utf-8"),
                                         tuple(a.groups.split(",")))
        rec["page"] = {"html": str(a.html), "duration_s": dur, "fps": fps,
                       "groups": page_coverage(by_group, dur, fps)}
        for g, r in rec["page"]["groups"].items():
            if not r.get("checked"):
                print(f"  page  {g:8s} skipped ({r['note']})")
                continue
            good = r["pass"]
            ok &= good
            print(f"  page  {g:8s} {r['clips']:>3d} clips  {r['frames']} frames  "
                  f"holes={len(r['holes'])} ghosts={len(r['ghosts'])}  "
                  f"{'OK' if good else 'FAIL'}")
            for hlist, kind in ((r["holes"], "HOLE"), (r["ghosts"], "GHOST")):
                for x in hlist[:8]:
                    print(f"          {kind} frame {x['frame']} @ {x['t']}s "
                          f"{x.get('clips', '')}")

    d = decoded_coverage(a.mp4, a.zone_bottom, a.ink_floor)
    rec["decoded"] = d
    ok &= d["pass"]
    print(f"  film  {d['frames']} frames @ {d['fps']}fps  "
          f"min ink {d['min_ink_frac']}  "
          f"blank(lead/tail)={d['leading_trailing_empty']}  "
          f"blank(interior)={len(d['interior_blank_frames'])}  "
          f"{'OK' if d['pass'] else 'FAIL'}")
    for x in d["interior_blank_frames"][:12]:
        print(f"          BLANK frame {x['frame']} @ {x['t']}s ink={x['ink_frac']}")

    rec["pass"] = bool(ok)
    if a.json:
        a.json.parent.mkdir(parents=True, exist_ok=True)
        a.json.write_text(json.dumps(rec, indent=1))
    print(f"  => {'PASS' if ok else 'FAIL'}  {a.mp4.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
