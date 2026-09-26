#!/usr/bin/env python3
"""PRERENDER CHECK — every rejection this factory can see BEFORE a frame exists.

WHY THIS EXISTS (Miguel, 2026-09-03)
------------------------------------
A run-9 render that fails Gate 1 has already cost a Modal render, a qc_pass
decode and a Gemini watcher call.  Every one of the laws Gate 1 enforces is a
property of the PAGE — the DOM boxes, the caption pills, the clipping
containers, the asset files — and not one of them needs a rendered pixel.  So
they run here, on the emitted `index.html`, and a project that fails does not
reach the render lane at all.

**Nothing here is re-implemented.**  Every check is an existing module's own
function called on the project directory:

    gate1_geometry_audit    pipeline/geometry_audit.py (all round-4 classes)
    page_audit              whiteboard_build.audit_page      (dup ids, dead tweens)
    caption_canon_page      captions.assert_no_function_only_beat on the
                            MEASURED pills (offsetWidth/offsetHeight in design
                            px), plus the canon pill height and PILL_MIN_ASPECT
    refs_resolve            modal_render.refs — the packer's own reference list;
                            a ref that does not resolve is the one packing bug
                            that produces a plausible-looking wrong video
    assets_not_placeholder  cutout_depthfield._reads_as_placeholder on every
                            raster the page points at — the generic form of
                            `assert_cast_resolves`, which only ever guarded the
                            depth cast (run 9 shipped Exa's mark, which is
                            stroke-for-stroke the broken-image glyph)
    cutout_edge_fade_guard  cutout_core.guard_edge_fade(html)        (cutout)
    cutout_checks_24_25     cutout6_check.check_edge_fade / check_depth_field
                            (cutout) — these were always HTML checks living in
                            the POST-render pass; they belong here

EXIT CODES
----------
    0   every applicable check passed
    1   at least one ERROR — the project does not go to the render lane
    2   the tool itself could not run a check it was asked to run

CLI
---
    prerender_check.py <project> [--fmt split|cutout|whiteboard] [--step 0.25]
        [--out <json>] [--skip gate1,captions,...] [--allow-warnings]

A check reported SKIPPED is never a pass; the report says what it was missing.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

F = Path(__file__).resolve().parents[2]
for _p in (
           F / "formats/cutout/lib", F / "formats/whiteboard/lib",
           F / "pipeline", F / "pipeline/render"):
    sys.path.insert(0, str(_p))

PY = str(Path.home() / "Documents/Workspace/.venv/bin/python")

PILL_H_TOL_DESIGN_PX = 3.0        # qc_pass's own rendered tolerance, in design px
RASTER_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".svg"}
# A capture of a UI or a post is a raster full of type; the placeholder heuristic
# is about *marks*.  Anything larger than this on the long side is a screenshot,
# not a glyph, and is only checked for "decodes at all".
GLYPH_MAX_SIDE = 900


# ---------------------------------------------------------------------------
# the measured page: one headless load, every DOM-side number taken off it
# ---------------------------------------------------------------------------
PILL_JS = r"""
() => {
  // The canon is a SUB-PIXEL number (114.59), so `offsetHeight` — which Chrome
  // rounds to an integer — cannot measure it: it reports 115 and a 0.41 px
  // error would be indistinguishable from a real one.  `getBoundingClientRect`
  // is sub-pixel but lives in ZOOMED space (the split sets `zoom:2` on the
  // body), so each pill carries its own scale factor: rect.width/offsetWidth.
  // The widest pill has the smallest relative rounding error, so its factor is
  // the one used for the whole page.
  const els = Array.from(document.querySelectorAll('.scappill'));
  if (!els.length) return {zoom: null, pills: []};
  let ref = els[0];
  for (const el of els) if (el.offsetWidth > ref.offsetWidth) ref = el;
  const zoom = ref.getBoundingClientRect().width / Math.max(ref.offsetWidth, 1);
  const pills = els.map(el => {
    const r = el.getBoundingClientRect();
    return {text: (el.textContent || '').trim(),
            w: r.width / zoom, h: r.height / zoom,
            w_offset: el.offsetWidth, h_offset: el.offsetHeight};
  });
  return {zoom: zoom, pills: pills};
}
"""

# Every selector a `tl.set/to/fromTo` call targets, resolved against the LIVE
# page.  `whiteboard_build.audit_page` does the same job with a string test that
# only understands `#id`, so a DOM-lane page's descendant selectors
# (`"b1-open .shead"`) read as dead targets there; the browser is the only thing
# that can answer the question for an arbitrary selector.
TWEEN_JS = r"""
(sels) => sels.filter(s => {
  try { return document.querySelectorAll(s).length === 0; }
  catch (e) { return true; }
})
"""

TWEEN_RE = re.compile(r'tl\.(?:set|to|fromTo)\(\s*["\']([^"\']+)["\']')


def tween_selectors(html: str) -> list[str]:
    """Selectors named in the composition's own timeline calls, deduped.

    The raw capture is a comma list in GSAP's own shorthand, where a bare token
    is an id (`"b1-open"` means `#b1-open`) and a token with a space or a dot is
    already a CSS selector.
    """
    out, seen = [], set()
    for m in TWEEN_RE.finditer(html):
        for raw in m.group(1).split(","):
            s = raw.strip()
            if not s:
                continue
            if not s.startswith((".", "#", "[")) and not s[0].isupper():
                # a bare id, or an id followed by a descendant part
                head, sep, tail = s.partition(" ")
                s = "#" + head + (sep + tail if sep else "")
            if s not in seen:
                seen.add(s)
                out.append(s)
    return out


def measure_page(project: Path, timeout_ms: int = 20000) -> dict:
    """Load the composition once and read back what only a browser knows."""
    from playwright.sync_api import sync_playwright

    html = project / "index.html"
    rec: dict = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1920})
        page.goto(html.as_uri())
        for _ in range(int(timeout_ms / 250)):
            if page.evaluate('!!(window.__timelines && window.__timelines["main"])'):
                break
            page.wait_for_timeout(250)
        else:
            browser.close()
            raise RuntimeError("timeline never registered")
        # bounded font wait — the same one geometry_audit uses, for the same
        # reason (fonts.ready hangs forever behind a stalled CDN fetch)
        page.evaluate("Promise.race([document.fonts.ready,"
                      " new Promise(r => setTimeout(r, 6000))])")
        page.wait_for_timeout(400)
        rec["duration"] = float(page.locator("#root").get_attribute("data-duration"))
        pm = page.evaluate(PILL_JS)
        rec["pills"], rec["zoom"] = pm["pills"], pm["zoom"]
        sels = tween_selectors(html.read_text(encoding="utf-8", errors="replace"))
        rec["tween_selectors"] = len(sels)
        rec["dead_tween_targets"] = page.evaluate(TWEEN_JS, sels)
        browser.close()
    return rec


# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------
def _timed(fn):
    t0 = time.time()
    try:
        out = fn()
        out.setdefault("pass", True)
    except SystemExit as exc:                       # the factory's own refusals
        out = {"pass": False, "error": str(exc)}
    except Exception as exc:                        # noqa: BLE001
        out = {"pass": False, "error": f"{type(exc).__name__}: {exc}"}
    out["wall_s"] = round(time.time() - t0, 2)
    return out


def check_refs_resolve(project: Path) -> dict:
    import modal_render as MR                                        # noqa: E402
    index = project / "index.html"
    wanted = MR.refs(index)
    missing = [r for r in wanted if not (project / r).exists()]
    return {"referenced": len(wanted), "missing": missing,
            "pass": not missing,
            "error": (f"{len(missing)} referenced file(s) do not resolve: {missing}"
                      if missing else None)}


def check_assets_not_placeholder(project: Path) -> dict:
    import modal_render as MR                                        # noqa: E402
    import cutout_depthfield as CD                                   # noqa: E402
    bad, dead, seen = [], [], {}
    for r in MR.refs(project / "index.html"):
        p = project / r
        if p.suffix.lower() not in RASTER_SUFFIXES or not p.exists():
            continue
        try:
            img = CD._raster(p)
        except Exception as exc:                                     # noqa: BLE001
            dead.append(f"{r}: {type(exc).__name__}: {exc}")
            continue
        if max(img.size) > GLYPH_MAX_SIDE:
            seen[r] = {"size": list(img.size), "judged": "decode only (capture)"}
            continue
        is_bad, info = CD._reads_as_placeholder(img)
        seen[r] = {"size": list(img.size), **info}
        if is_bad:
            bad.append(f"{r} {info}")
    ok = not bad and not dead
    return {"rasters": len(seen), "placeholder_shaped": bad, "undecodable": dead,
            "report": seen, "pass": ok,
            "error": (None if ok else
                      f"{len(bad)} mark(s) read as a MISSING-IMAGE ICON, "
                      f"{len(dead)} do not decode: {bad + dead}")}


def check_page_audit(project: Path, dead: list[str] | None,
                     n_selectors: int | None) -> dict:
    """`whiteboard_build.audit_page`'s two laws, both measured correctly.

    The duplicate-id half is a pure string property and is taken from the module
    itself.  The dead-tween half is NOT: `audit_page`'s membership test only
    understands `#id`, and every DOM-lane page in this factory tweens descendant
    selectors, so running it there reports fourteen live targets as dead.  The
    same law, asked of the browser, is exact — so the selectors are resolved on
    the loaded page and the result is handed in here.
    """
    from collections import Counter
    html = (project / "index.html").read_text(encoding="utf-8", errors="replace")
    ids = re.findall(r'\sid="([^"]+)"', html)
    dupes = sorted(k for k, v in Counter(ids).items() if v > 1)
    if dead is None:
        return {"pass": False, "skipped": True, "ids": len(ids),
                "duplicate_ids": dupes,
                "error": "the page would not load, so tween targets could not "
                         "be resolved"}
    ok = not dupes and not dead
    return {"ids": len(ids), "unique_ids": len(set(ids)),
            "duplicate_ids": dupes,
            "tween_selectors": n_selectors, "dead_tween_targets": dead,
            "pass": ok,
            "error": (None if ok else
                      f"duplicate ids {dupes}; tween targets that do not "
                      f"exist {dead}")}


def check_caption_canon_page(pills: list[dict]) -> dict:
    import captions as C                                             # noqa: E402
    if not pills:
        return {"pass": False, "skipped": True,
                "error": "no .scappill elements on the page — the caption canon "
                         "cannot be measured, and a page with no captions is not "
                         "a daily deliverable"}
    heights = sorted({round(p["h"], 2) for p in pills})
    modal_h = max(heights, key=lambda h: sum(1 for p in pills
                                             if abs(p["h"] - h) < 0.51))
    spread = round(max(p["h"] for p in pills) - min(p["h"] for p in pills), 2)
    off = [p for p in pills if abs(p["h"] - C.CAP_PILL_HEIGHT) > PILL_H_TOL_DESIGN_PX]
    square = [f"{p['text']!r} {p['w']:.0f}x{p['h']:.0f} aspect "
              f"{p['w'] / max(p['h'], 1):.2f}"
              for p in pills if p["w"] / max(p["h"], 1) < C.PILL_MIN_ASPECT]
    # The §3b law itself, fed the MEASURED width so `is_orphan_beat` uses the
    # real aspect instead of the <4-character fallback.  The raise is CAUGHT so
    # the measured numbers survive into the report: a failing check that prints
    # nothing but its exception is a check you cannot act on.
    law_error = None
    try:
        C.assert_no_function_only_beat(
            [{"text": p["text"], "w": p["w"]} for p in pills])
    except SystemExit as exc:
        law_error = str(exc)
    ok = not off and not square and law_error is None
    return {"pills": len(pills), "modal_height_px": modal_h,
            "canon_height_px": C.CAP_PILL_HEIGHT, "height_spread_px": spread,
            "tolerance_design_px": PILL_H_TOL_DESIGN_PX,
            "heights_off_canon": [f"{p['text']!r} {p['h']:.2f}px" for p in off],
            "squarer_than_min_aspect": square,
            "min_aspect": C.PILL_MIN_ASPECT,
            "function_only_beat_law": law_error, "pass": ok,
            "error": (None if ok else
                      (law_error or "")
                      + f" | {len(off)} pill(s) off the canon height, "
                        f"{len(square)} squarer than {C.PILL_MIN_ASPECT}")}


# ---------------------------------------------------------------------------
# ONE named waiver, and the measurement that earns it.
#
# `geometry_audit`'s SNAPSHOT_JS lane measures RAW `getBoundingClientRect`
# against FRAME_W = 1080.  A split page is authored 2160 wide with `zoom:2` on
# the body (the LAYOUT_JS lane normalises by `1080 / root.dataset.width`; the
# older sample lane does not), so a pill that IS centred reports its centre at
# 1080 and the `offcenter` warning fires at exactly FRAME_W/2 = 540.0 px, every
# time, on every split — including the two Miguel approved on 2026-09-02.
#
# So the waiver is pinned to that arithmetic and to nothing else: type
# `offcenter`, on a page whose zoom is > 1, whose measured offset is 540 +/- 1.
# A genuinely off-centre box does not land on exactly half the frame width.
# Everything else in Gate 1 still has to be 0/0.  The instrument bug itself is
# logged in LEARNINGS.md; it is not patched here, because normalising that lane
# moves every threshold on every split at once.
# ---------------------------------------------------------------------------
WAIVER_OFFCENTER_ZOOM = re.compile(r"centered-text box center off by (\d+)px")


def _waivable(v: dict, zoom: float | None) -> str | None:
    if v.get("type") != "offcenter" or not zoom or zoom <= 1.0:
        return None
    m = WAIVER_OFFCENTER_ZOOM.search(v.get("detail", ""))
    if m and abs(float(m.group(1)) - 540.0) <= 1.0:
        return (f"zoom:{zoom:g} page measured in the un-normalised SNAPSHOT_JS "
                f"lane: the offset IS FRAME_W/2 (540px), which is the artefact, "
                f"not a defect")
    return None


def check_gate1(project: Path, step: float, copy_to: Path | None,
                allow_warnings: bool, zoom: float | None) -> dict:
    """Gate 1, ALWAYS written into the project's own `geometry_audit/`.

    `cutout6_check.check_edge_fade` reads `<project>/geometry_audit/report.json`
    by a hard-coded path — that report is the geometric half of Law 8, the half
    a string guard cannot see — so redirecting Gate 1's output elsewhere would
    silently turn check 24 into a fail.  `--gate1-out` therefore takes a COPY;
    it never moves the canonical report.  Gate 1 runs BEFORE the cutout checks
    for the same reason.
    """
    out_dir = project / "geometry_audit"
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [PY, str(F / "pipeline/geometry_audit.py"), str(project),
           "--step", str(step), "--out", str(out_dir)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    errors = warnings = None
    m = re.search(r"(\d+) errors, (\d+) warnings", r.stdout)
    if m:
        errors, warnings = int(m.group(1)), int(m.group(2))

    report_path = out_dir / "report.json"
    waived, live_warnings = [], warnings
    if report_path.exists():
        rep = json.loads(report_path.read_text())
        live = []
        for v in rep.get("violations", []):
            if v.get("severity") != "warning":
                continue
            why = _waivable(v, zoom)
            if why:
                waived.append({**v, "waived_because": why})
            else:
                live.append(v)
        live_warnings = len(live)
        if copy_to:
            copy_to.mkdir(parents=True, exist_ok=True)
            (copy_to / "report.json").write_text(report_path.read_text())

    ok = (errors == 0 and (allow_warnings or live_warnings == 0))
    return {"returncode": r.returncode, "errors": errors,
            "warnings": warnings, "warnings_after_waivers": live_warnings,
            "waived": waived, "report": str(report_path),
            "stdout": r.stdout[-4000:], "stderr": r.stderr[-2000:],
            "bar": "0 errors, 0 warnings" if not allow_warnings else "0 errors",
            "pass": bool(ok),
            "error": (None if ok else
                      f"gate 1: {errors} error(s), {live_warnings} live "
                      f"warning(s) ({len(waived)} waived, exit {r.returncode})")}


def check_cutout_edge_fade(project: Path) -> dict:
    import cutout_core as CC                                         # noqa: E402
    html = (project / "index.html").read_text(encoding="utf-8", errors="replace")
    return dict(CC.guard_edge_fade(html))              # raises SystemExit on a fail


def check_cutout_24_25(project: Path) -> dict:
    # Import order is the documented trap: the PROMOTED cutout_core must be in
    # sys.modules before cutout6_check pulls in the lab's cutout3_check.
    import cutout_core                                               # noqa: F401
    import cutout6_check as C6                                       # noqa: E402
    fails: list[str] = []
    out = {"check24_edge_fade": C6.check_edge_fade(project, fails),
           "check25_depth_field": C6.check_depth_field(project, fails),
           "fails": fails}
    out["pass"] = not fails
    out["error"] = None if not fails else f"{len(fails)} fail(s): {fails}"
    return out


# ---------------------------------------------------------------------------
def infer_fmt(project: Path) -> str:
    name = project.name.lower()
    for f in ("whiteboard", "cutout", "facesplit", "artifactspine", "takeover",
              "split"):
        if name.endswith("_" + f) or f in name:
            return f
    return ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("--fmt", default=None,
                    help="split | cutout | whiteboard | ... (inferred from the "
                         "project name when omitted)")
    ap.add_argument("--step", type=float, default=0.25,
                    help="geometry_audit sample step (the daily default is 0.25)")
    ap.add_argument("--out", type=Path, default=None, help="write the report here")
    ap.add_argument("--gate1-out", type=Path, default=None, metavar="DIR",
                    help="COPY Gate 1's report.json here as well. The canonical "
                         "report always stays in <project>/geometry_audit/ "
                         "because cutout check 24 reads it from there.")
    ap.add_argument("--skip", default="", metavar="NAMES",
                    help="comma-separated checks to skip: refs_resolve, "
                         "assets_not_placeholder, page_audit, captions "
                         "(= caption_canon_page), gate1_geometry_audit, "
                         "cutout_edge_fade_guard, cutout_checks_24_25")
    ap.add_argument("--allow-warnings", action="store_true",
                    help="Gate 1 warnings do not fail the run. The daily bar is "
                         "0/0; this exists for lab work and must be stated.")
    a = ap.parse_args()

    project = a.project.resolve()
    if not (project / "index.html").exists():
        print(f"no index.html in {project}", file=sys.stderr)
        return 2
    fmt = (a.fmt or infer_fmt(project)).lower()
    skip = {s.strip() for s in a.skip.split(",") if s.strip()}
    t0 = time.time()
    rec: dict = {"project": str(project), "fmt": fmt, "step": a.step,
                 "checks": {}, "skipped": {}}

    def run(name: str, fn) -> None:
        if name in skip:
            rec["skipped"][name] = "named in --skip"
            return
        rec["checks"][name] = _timed(fn)

    run("refs_resolve", lambda: check_refs_resolve(project))
    run("assets_not_placeholder", lambda: check_assets_not_placeholder(project))

    # ONE page load serves both DOM-side checks.
    t_page = time.time()
    page: dict = {}
    page_err = None
    try:
        page = measure_page(project)
        rec["duration_s"] = page["duration"]
        rec["page_zoom"] = page.get("zoom")
    except Exception as exc:                                         # noqa: BLE001
        page_err = f"the page would not load: {type(exc).__name__}: {exc}"
    rec["page_load_wall_s"] = round(time.time() - t_page, 2)

    run("page_audit", lambda: check_page_audit(
        project, page.get("dead_tween_targets"), page.get("tween_selectors")))
    if "captions" in skip:
        rec["skipped"]["caption_canon_page"] = "named in --skip"
    elif page_err:
        rec["checks"]["caption_canon_page"] = {"pass": False, "wall_s": 0.0,
                                               "error": page_err}
    else:
        rec["checks"]["caption_canon_page"] = _timed(
            lambda: check_caption_canon_page(page["pills"]))

    # GATE 1 RUNS BEFORE THE CUTOUT CHECKS: check 24 reads Gate 1's own report
    # out of <project>/geometry_audit/report.json, and without it the geometric
    # half of Law 8 reports a fail that is really a missing input.
    run("gate1_geometry_audit",
        lambda: check_gate1(project, a.step, a.gate1_out, a.allow_warnings,
                            page.get("zoom")))

    if fmt == "cutout":
        run("cutout_edge_fade_guard", lambda: check_cutout_edge_fade(project))
        run("cutout_checks_24_25", lambda: check_cutout_24_25(project))
    else:
        rec["skipped"]["cutout_edge_fade_guard"] = "cutout only"
        rec["skipped"]["cutout_checks_24_25"] = "cutout only"

    failed = [k for k, v in rec["checks"].items() if not v.get("pass")]
    rec["failed"] = failed
    rec["verdict"] = "PASS" if not failed else "FAIL"
    rec["total_wall_s"] = round(time.time() - t0, 2)

    print(f"\nPRERENDER CHECK  {project.name}  ({fmt or 'fmt?'})")
    print("-" * 74)
    for k, v in rec["checks"].items():
        mark = "PASS" if v.get("pass") else "FAIL"
        extra = ""
        if k == "gate1_geometry_audit":
            extra = (f"  {v.get('errors')} errors / "
                     f"{v.get('warnings_after_waivers')} warnings"
                     + (f" ({len(v.get('waived') or [])} waived)"
                        if v.get("waived") else ""))
        elif k == "caption_canon_page" and v.get("pills") is not None:
            extra = (f"  {v.get('pills')} pills, modal h "
                     f"{v.get('modal_height_px')}px, spread {v.get('height_spread_px')}")
        elif k == "assets_not_placeholder" and v.get("rasters") is not None:
            extra = f"  {v.get('rasters')} rasters"
        print(f"  {mark}  {k:<26} {v['wall_s']:>6.2f}s{extra}")
        if not v.get("pass"):
            print(f"        -> {str(v.get('error'))[:600]}")
    for k, why in rec["skipped"].items():
        print(f"  SKIP  {k:<26}        ({why})")
    print("-" * 74)
    print(f"  {rec['verdict']}  in {rec['total_wall_s']}s")

    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps(rec, indent=1, default=str))
        print(f"  report -> {a.out}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
