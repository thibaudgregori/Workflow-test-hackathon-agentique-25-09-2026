#!/usr/bin/env python3
"""TAKEOVER SWITCH LAW — the deterministic check (Miguel, 2026-09-01).

Miguel rejected `perplexityprojects_takeover` on 2026-09-01 with:

    "the switches of the face are happening way too often, they should happen
     at transition moments ideally, right now you are cutting key
     visualizations."

Two separate faults hide inside that one sentence, and this module measures
both from the built page rather than by eye:

  1. **RATE.** The rejected cut switched the frame between his face and the
     scene 7 times in 30.02s = 13.99/min. The DEFINITIVE takeover switches 7
     times in 54.04s = 7.77/min. Nearly double.

  2. **PLACEMENT.** A switch is only allowed at a *beat transition* — a moment
     when the illustration has finished building and is holding, and the next
     idea has not started. Cutting away mid-build, or cutting away the instant
     a thing lands, destroys the visualization the takeover exists to show.

WHY THE TWO TOPOLOGIES. The chassis (`formats/takeover/chassis_gen.py`) draws
one continuous face plate and lays SCENE clips on top of it. The lane builds
(`(run 9) gen/*_diagram_gen.py`) do the opposite: one continuous scene
timeline with FACE clips on top, so that a cutaway samples a world that has
been developing all along. The two produce the same picture, but they fail
differently — in the second, a face window HIDES whatever the scene was
building underneath it, which is exactly how the rejected cut lost the
"local files" branch. The checker detects the topology and applies the law to
both.

THE LAW, as checked
-------------------
  D  DEPARTURE (scene -> face) may not land inside a build, and may not land
     within HOLD_MIN of a build finishing. A visualization lands, then holds,
     then you may cut. Arrivals (face -> scene) are exempt: format law 3,
     ARRIVE IN MOTION, *requires* the first visible frame to be mid-gesture.

  H  HIDDEN BUILD. On a continuous-scene page, no build may overlap a face
     RETURN window (any face window after the first takeover). The hook's own
     face window is exempt: before the first takeover the scene has not been
     revealed, and its establishing state is what the first cutaway arrives
     into.

  R  RATE. switches/minute <= RATE_CEILING, the DEFINITIVE's own rate plus the
     tolerance below.

Usage
-----
    python takeover_switch_law.py <index.html> [--json out.json] [--label L]

Exit code 0 = silent (lawful), 1 = defects found.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# --------------------------------------------------------------- constants
DEFINITIVE_SWITCHES = 7
DEFINITIVE_SECONDS = 54.04
DEFINITIVE_RATE = DEFINITIVE_SWITCHES / DEFINITIVE_SECONDS * 60.0   # 7.77/min
RATE_TOLERANCE = 1.30          # a short video cannot hit the rate exactly;
#                                a 30s cut at the ceiling gets 5 switches.
RATE_CEILING = DEFINITIVE_RATE * RATE_TOLERANCE                      # 10.10/min
LEAD = 0.18                    # the chassis's own arrive-in-motion lead
HOLD_MIN = 0.30                # seconds a build must be on screen, finished,
#                                before the frame may be taken away from it.
EPS = 1e-6

_TWEEN = re.compile(r'tl\.(set|to|fromTo)\("([^"]+)",(.+?)\);', re.S)
# ANY element carrying the timing attributes is a clip for our purposes: the
# chassis's full-length face plate is a bare <video data-start> with no
# `class="clip"`, and reading only class="clip" made the checker silent on the
# very reference it is calibrated against.
_CLIP = re.compile(r'<(section|video|div|img)\b([^>]*\bdata-start="[^"]*"[^>]*)>')
_ATTR = re.compile(r'(\w[\w-]*)="([^"]*)"')


def _attrs(blob: str) -> dict:
    return dict(_ATTR.findall(blob))


def _num(s: str, key: str) -> float | None:
    m = re.search(rf'\b{key}\s*:\s*(-?[\d.]+)', s)
    return float(m.group(1)) if m else None


# --------------------------------------------------------------- parsing
def parse_clips(html: str) -> list[dict]:
    out = []
    for m in _CLIP.finditer(html):
        a = _attrs(m.group(2))
        if "data-start" not in a or "data-duration" not in a:
            continue
        try:
            t0 = float(a["data-start"])
            d = float(a["data-duration"])
        except ValueError:
            continue
        out.append({"tag": m.group(1), "id": a.get("id", ""),
                    "class": a.get("class", ""), "src": a.get("src", ""),
                    "t0": round(t0, 3), "t1": round(t0 + d, 3)})
    return out


def _count(html: str, sel: str) -> int:
    """How many elements a `#id .cls` selector matches, so a stagger's real
    end can be computed instead of guessed."""
    m = re.match(r'#([\w-]+)\s+\.([\w-]+)$', sel.strip())
    if not m:
        return 1
    eid, cls = m.groups()
    i = html.find(f'id="{eid}"')
    if i < 0:
        return 1
    j = html.find('id="', i + 4)
    block = html[i:j if j > 0 else len(html)]
    n = len(re.findall(rf'class="[^"]*\b{cls}\b', block))
    return max(1, n)


def parse_tweens(html: str) -> list[dict]:
    """Every tl.* call, classified BUILD / EXIT / MOVE / SET.

    BUILD is the class the law protects: something coming into existence on
    screen — an opacity-0 entrance, a dash draw-on, a scaleX grow, or a
    `set(opacity:0)` + `to(opacity:1)` pair.
    """
    zeroed: set[str] = set()          # selectors parked at opacity 0 at t=0
    out: list[dict] = []
    for kind, sel, body in _TWEEN.findall(html):
        at = float(body.rsplit(",", 1)[-1].strip().rstrip(")"))
        if kind == "set":
            # a t=0 `set` that parks a property BELOW its resting value is the
            # first half of a build; the matching `to` is the build itself.
            parked = (_num(body, "opacity") == 0
                      or _num(body, "strokeDashoffset") == 100
                      or any((v := _num(body, k)) is not None and v < 1
                             for k in ("scaleX", "scaleY", "scale")))
            if parked:
                zeroed.add(sel)
            continue
        dur = _num(body, "duration") or 0.0
        stag = _num(body, "stagger") or 0.0
        n = _count(html, sel) if stag else 1
        end = at + dur + stag * max(0, n - 1)

        # a fromTo carries TWO object literals; reading `opacity` off the raw
        # body finds the FROM value and inverts every entrance. Split first.
        objs = re.findall(r'\{[^{}]*\}', body)
        frm = objs[0] if kind == "fromTo" and len(objs) >= 2 else ""
        dst = objs[1] if kind == "fromTo" and len(objs) >= 2 else (
            objs[0] if objs else body)
        opa = _num(dst, "opacity")
        opa0 = _num(frm, "opacity") if frm else None
        sx = _num(dst, "scaleX")
        sx0 = _num(frm, "scaleX") if frm else None
        dash = _num(dst, "strokeDashoffset")
        cls = "MOVE"
        if dash is not None:
            cls = "BUILD" if dash == 0 else "EXIT"
        elif opa0 == 0 and (opa is None or opa > 0):
            cls = "BUILD"                     # opacity-0 entrance
        elif opa is not None and opa == 0:
            cls = "EXIT"
        elif sel in zeroed and ((opa is not None and opa > 0)
                                or (sx is not None and sx >= 1)
                                or (_num(dst, "scale") or 0) >= 1):
            cls = "BUILD"                     # set(opacity:0) + to(opacity:1)
        elif sx0 is not None and sx is not None and sx0 < sx:
            cls = "BUILD"                     # a scaleX grow is a build
        elif opa is not None and 0 < opa < 1:
            cls = "EXIT"          # a dim-down (outro regroup) is a release
        out.append({"sel": sel, "kind": kind, "class": cls,
                    "t0": round(at, 3), "t1": round(end, 3),
                    "stagger_n": n})
    return out


def face_and_scene(html: str, duration: float) -> tuple[list, list, str]:
    """Return (face_windows, scene_windows, topology).

    topology 'face-on-top'  : one continuous scene, face clips over it
    topology 'scene-on-top' : one continuous face plate, scene clips over it
    """
    clips = [c for c in parse_clips(html)
             if not re.search(r'\bscap\b', c["class"])
             and not c["id"].startswith("cap")]
    face = [c for c in clips if "face" in c["id"] or "face" in c["src"]
            or "matte" in c["id"]]
    full_face = [c for c in face
                 if c["t1"] >= duration - 0.25 and c["t0"] <= 0.25]
    faces = [c for c in face if c not in full_face]
    if full_face and not faces:
        scenes = _merge(sorted(
            (c["t0"], c["t1"]) for c in clips
            if re.search(r'\btk\b', c["class"]) or c["id"].startswith("tk-")))
        return _complement(scenes, duration), scenes, "scene-on-top"
    fw = _merge(sorted((c["t0"], c["t1"]) for c in faces))
    return fw, _complement(fw, duration), "face-on-top"


def _merge(spans: list[tuple]) -> list[tuple]:
    out: list[list] = []
    for a, b in spans:
        if out and a - out[-1][1] <= 0.06:      # a 1-frame seam is not a gap
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return [(round(a, 3), round(b, 3)) for a, b in out]


def _complement(spans: list[tuple], duration: float) -> list[tuple]:
    out, cur = [], 0.0
    for a, b in spans:
        if a - cur > 0.06:
            out.append((round(cur, 3), round(a, 3)))
        cur = max(cur, b)
    if duration - cur > 0.06:
        out.append((round(cur, 3), round(duration, 3)))
    return out


# --------------------------------------------------------------- the law
def audit(html: str, duration: float, label: str = "") -> dict:
    faces, scenes, topo = face_and_scene(html, duration)
    tweens = parse_tweens(html)
    builds = [t for t in tweens if t["class"] == "BUILD"]

    # every face<->scene boundary in the interior of the video
    edges = sorted({round(x, 3) for span in faces + scenes for x in span
                    if EPS < x < duration - EPS})
    switches = []
    for t in edges:
        into_face = any(abs(t - a) < EPS for a, _ in faces)
        switches.append({"t": t, "direction": "scene->face" if into_face
                         else "face->scene"})

    rate = len(switches) / duration * 60.0
    defects = []

    # --- D: a departure may not cut a build, nor cut inside its hold
    for s in switches:
        if s["direction"] != "scene->face":
            continue
        for b in builds:
            if b["t0"] - EPS <= s["t"] < b["t1"] + HOLD_MIN - EPS:
                defects.append({
                    "law": "D", "t": s["t"], "element": b["sel"],
                    "build": [b["t0"], b["t1"]],
                    "detail": ("cuts away mid-build"
                               if s["t"] < b["t1"] - EPS
                               else f"cuts away {round(s['t'] - b['t1'], 2)}s "
                                    f"after it lands (hold min {HOLD_MIN}s)")})

    # --- H: on a continuous-scene page a face return hides what builds under it
    if topo == "face-on-top" and scenes:
        first_takeover = min(a for a, _ in scenes)
        for a, z in faces:
            if a < first_takeover - EPS:
                continue                       # the hook's own face window
            for b in builds:
                # ARRIVE IN MOTION (format law 3) buys a build up to LEAD of
                # overlap at the TRAILING edge: the chassis deliberately starts
                # an interior LEAD before its clip is on screen so the first
                # visible frame is mid-gesture. Anything else the face covers is
                # a build the viewer never sees.
                if b["t0"] >= z - LEAD - EPS:
                    continue
                if b["t0"] < z - EPS and b["t1"] > a + EPS:
                    defects.append({
                        "law": "H", "t": a, "element": b["sel"],
                        "build": [b["t0"], b["t1"]],
                        "face_window": [a, z],
                        "detail": "build happens behind the face and is never "
                                  "seen"})

    # --- R: rate ceiling
    if rate > RATE_CEILING + 1e-3:
        defects.append({
            "law": "R", "t": None, "element": None,
            "detail": f"{len(switches)} switches in {duration:.2f}s = "
                      f"{rate:.2f}/min, over the ceiling {RATE_CEILING:.2f}/min "
                      f"(DEFINITIVE {DEFINITIVE_RATE:.2f}/min "
                      f"x {RATE_TOLERANCE})"})

    face_s = sum(z - a for a, z in faces)
    return {"label": label, "topology": topo, "duration": round(duration, 3),
            "face_windows": faces, "scene_windows": scenes,
            "switches": switches, "switch_count": len(switches),
            "switches_per_min": round(rate, 2),
            "definitive_per_min": round(DEFINITIVE_RATE, 2),
            "ceiling_per_min": round(RATE_CEILING, 2),
            "face_seconds": round(face_s, 3),
            "face_pct": round(face_s / duration, 4),
            "builds": builds, "defects": defects, "ok": not defects}


def quiet_windows(html: str, duration: float) -> list[tuple]:
    """Where a switch is legal: gaps between builds, minus the hold margin.
    Reported so a cut map can be *placed* rather than guessed."""
    b = sorted((t["t0"], t["t1"]) for t in parse_tweens(html)
               if t["class"] == "BUILD")
    out, cur = [], 0.0
    for a, z in _merge(b):
        if a - (cur + HOLD_MIN) > 0.05:
            out.append((round(cur + HOLD_MIN, 2), round(a, 2)))
        cur = max(cur, z)
    if duration - (cur + HOLD_MIN) > 0.05:
        out.append((round(cur + HOLD_MIN, 2), round(duration, 2)))
    return out


def _duration_of(html: str) -> float:
    d = [float(x) for x in re.findall(r'data-duration="([\d.]+)"', html)]
    return max(d) if d else 0.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("--duration", type=float, default=None)
    ap.add_argument("--label", default="")
    ap.add_argument("--json", default=None)
    ap.add_argument("--quiet-windows", action="store_true")
    a = ap.parse_args()
    html = Path(a.page).read_text(encoding="utf-8")
    dur = a.duration or _duration_of(html)
    rep = audit(html, dur, a.label or Path(a.page).parent.name)
    if a.quiet_windows:
        rep["quiet_windows"] = quiet_windows(html, dur)
    if a.json:
        Path(a.json).write_text(json.dumps(rep, indent=2))
    print(f"[switch-law] {rep['label']}  topology={rep['topology']}  "
          f"{rep['switch_count']} switches / {rep['duration']}s = "
          f"{rep['switches_per_min']}/min "
          f"(DEFINITIVE {rep['definitive_per_min']}, ceiling "
          f"{rep['ceiling_per_min']})  face {rep['face_pct'] * 100:.1f}%")
    for s in rep["switches"]:
        print(f"    {s['t']:>6.2f}  {s['direction']}")
    if a.quiet_windows:
        print("  quiet windows (legal switch moments):")
        for q in rep["quiet_windows"]:
            print(f"    {q[0]:>6.2f} .. {q[1]:.2f}")
    if rep["ok"]:
        print("  OK — no switch-law defects")
        sys.exit(0)
    for d in rep["defects"]:
        loc = f"{d['t']:.2f}" if d["t"] is not None else "  -- "
        print(f"  DEFECT[{d['law']}] t={loc} {d.get('element') or ''} "
              f"{d.get('build') or ''} {d['detail']}")
    sys.exit(1)


if __name__ == "__main__":
    main()
