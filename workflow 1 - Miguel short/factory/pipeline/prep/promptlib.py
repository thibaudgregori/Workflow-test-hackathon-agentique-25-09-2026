#!/usr/bin/env python3
"""THE FRAME-0 PROMPT — BiRefNet silhouette, and the WING CUT.

`prompt0.py` already does both halves.  What it cannot do is decide the wing
columns: its README says they are "measured on this frame, at zoom with a
coordinate grid, not guessed", and run 9 measured them by eye, session by
session — six of fifteen sessions needed a cut, nine did not, and the columns
that were needed ranged from 410 to 855.

WHAT THIS MODULE DOES, AND WHAT IT DELIBERATELY DOES NOT
--------------------------------------------------------
It runs stage 1 (BiRefNet, in the bake-off venv) and stage 2 (the cut) for a
session, and it measures the wings when it can prove one is there.  It is built
to ABSTAIN rather than to guess, and it abstains often.

That is a deliberate outcome, not an unfinished one.  Replayed against the
fifteen sessions that carry a human `kf_report_*.json` (`--validate`), the
instrument agrees with the human on all NINE sessions that needed no cut and
proposes nothing on the FOUR that did.  Zero false positives, zero recall.  The
asymmetry is the point:

  * A FALSE POSITIVE amputates a shoulder.  The README's own worked example is a
    left band widened "symmetrically for its own sake" reaching y 580-600, where
    the mask's left edge is his shoulder coming into frame.  That is a NEW MATTE
    — the envelope has to be re-derived and every guard re-verified — and it
    costs a whole second SAM2 track to discover.
  * A FALSE NEGATIVE is caught downstream, by instruments that already exist and
    already fire: `track.py`'s own frozen-column leak sweep, and the protrusion
    gate inside `ship.py`, which is precisely a detector for "a headrest that
    propagated".  `wingfix.py` and `bolsterfix.py` are the documented heals.

Measured separability, on the plates themselves: the dark-fraction and
column-height profiles of a real headrest wing (deepresearch 0.96/0.97,
grokprice 0.99/1.00) overlap the profiles of sessions with NO wing at all
(sparkchrome 0.82/0.96, grokpublish 0.62/1.00).  A single threshold cannot
separate them, which is exactly what `pipeline/sam2/README.md` predicts when it
leaves the corrective-keyframe tooling in the lab: "per-plate regime detection
that needs re-deriving for a different chair, a lighter cap or a different key
light".  So this file does not pretend otherwise.

WHAT THE PREP STAGE DOES WITH THAT.  When the instrument abstains it sets
`wing_review` on the package and hands over `kf_overlay_00000.png` — one PNG,
green prompt, red cut — so a builder spends ten seconds looking instead of
re-deriving a prompt.  An explicit `wings` block on the intake row ALWAYS wins:
a human who has zoomed in with a coordinate grid outranks this instrument, and
the package records which of the two decided.

THE GUARDS, when it does propose:
  * DARK-ONLY.  A wing is furniture at luma < DARK.  A bright jaw or neck can
    never be removed, whatever the columns say.
  * OUTSIDE THE HEAD.  Candidate columns start beyond the head band's own
    extreme plus HEAD_GAP, so the cut can never eat into the face.
  * A SOLID VERTICAL STRUCTURE, at least MIN_COLS wide with COVER_MIN dark
    coverage.  A stray dark speckle is not a wing.
  * ROW-BOUNDED TO ITS OWN EXTENT, never a nominal constant, and never at or
    below SHIRT_GUARD_FRAC of the plate, where the black t-shirt lives.
  * AREA-BOUNDED.  A proposal removing more than MAX_REMOVE_FRAC of the
    silhouette is REFUSED as a mis-detection rather than applied as a big fix.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

WORKSPACE = Path.home() / "Documents" / "Workspace"
F = WORKSPACE / "projects/personal/content/shorts-factory"
BIREFNET_PY = Path(os.environ.get("SHORTS_BIREFNET_PY") or (F / "pipeline/prep/.venv-birefnet/bin/python"))  # the BiRefNet interpreter (moved out of the format lab (archived) 2026-09-20; requirements in birefnet-requirements.txt)
PROMPT0 = F / "pipeline/sam2/prompt0.py"
PY = WORKSPACE / ".venv/bin/python"

DARK = 60                    # prompt0.py's own threshold: chair/cap read 2-30
HEAD_GAP = 16                # px beyond the head band before a column can be a wing
COVER_MIN = 0.35             # dark-and-masked fraction of the search rows
MIN_COLS = 10                # a wing is a structure, not a speckle
MIN_AREA = 400               # px it must remove to be worth cutting
MAX_REMOVE_FRAC = 0.12       # a proposal bigger than this is a mis-detection
SEARCH_ROWS = (0.16, 0.78)   # fraction of plate height the wings may occupy
SHIRT_GUARD_FRAC = 0.78      # never cut at or below this fraction of the plate


def plate_frame(plate: Path, idx: int = 0) -> np.ndarray:
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(plate), "-vf",
         f"select=eq(n\\,{idx})", "-frames:v", "1", "-f", "image2pipe",
         "-vcodec", "png", "-"], capture_output=True, check=True).stdout
    return cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)


def _band_extreme(mask: np.ndarray, rows: slice, side: str) -> int:
    w = mask.shape[1]
    cols = np.arange(w)[None, :]
    b = mask[rows]
    if not b.any():
        return 0 if side == "left" else w - 1
    return int(np.where(b, cols, w).min()) if side == "left" \
        else int((cols * b).max())


def derive_wings(plate: Path, birefnet_png: Path, *, dark: int = DARK) -> dict:
    """Measure the headrest wings on THIS plate's frame 0, or abstain."""
    bgr = plate_frame(plate, 0)
    luma = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    bi = cv2.imread(str(birefnet_png), cv2.IMREAD_GRAYSCALE) > 127
    if bi is None or not bi.any():
        raise RuntimeError(f"no BiRefNet mask at {birefnet_png}")
    h, w = bi.shape
    if luma.shape != bi.shape:
        raise RuntimeError(f"plate {luma.shape} and mask {bi.shape} disagree")

    r0, r1 = int(h * SEARCH_ROWS[0]), int(h * SEARCH_ROWS[1])
    guard_row = int(h * SHIRT_GUARD_FRAC)
    furniture = bi & (luma < dark)
    band = furniture[r0:r1]
    cover = band.mean(axis=0)

    # the head's own extremes, on prompt0's own head band (rows 340..520 of 900)
    head_rows = slice(int(h * 0.378), int(h * 0.578))
    head_left = _band_extreme(bi, head_rows, "left")
    head_right = _band_extreme(bi, head_rows, "right")

    rec: dict = {
        "plate": str(plate), "frame": 0, "dark_threshold": dark,
        "search_rows": [r0, r1], "shirt_guard_row": guard_row,
        "head_band_cols": [head_left, head_right],
        "silhouette_area_px": int(bi.sum()),
        "furniture_px_in_search_band": int(band.sum()),
        "thresholds": {"cover_min": COVER_MIN, "min_cols": MIN_COLS,
                       "min_area": MIN_AREA, "head_gap": HEAD_GAP,
                       "max_remove_frac": MAX_REMOVE_FRAC},
    }

    def solid_run(side: str):
        """The outermost contiguous column run with coverage >= COVER_MIN."""
        if side == "right":
            lo, hi = head_right + HEAD_GAP, w
        else:
            lo, hi = 0, max(0, head_left - HEAD_GAP)
        ok = np.zeros(w, bool)
        ok[lo:hi] = cover[lo:hi] >= COVER_MIN
        runs, start = [], None
        for c in range(w):
            if ok[c] and start is None:
                start = c
            elif not ok[c] and start is not None:
                runs.append((start, c - 1))
                start = None
        if start is not None:
            runs.append((start, w - 1))
        runs = [r for r in runs if r[1] - r[0] + 1 >= MIN_COLS]
        if not runs:
            return None
        # the OUTERMOST run is the wing; anything inboard of it is his own body
        return runs[-1] if side == "right" else runs[0]

    for side in ("right", "left"):
        run = solid_run(side)
        blk: dict = {"candidate_run_cols": list(run) if run else None}
        if run is None:
            blk.update({"verdict": "no wing",
                        "why": (f"no contiguous run of >= {MIN_COLS} columns "
                                f"outside the head band reaches {COVER_MIN} dark "
                                f"coverage; max coverage outboard is "
                                f"{round(float(cover[head_right + HEAD_GAP:].max()) if side == 'right' and head_right + HEAD_GAP < w else float(cover[:max(0, head_left - HEAD_GAP)].max()) if side == 'left' and head_left > HEAD_GAP else 0.0, 3)}")})
            rec[side] = blk
            continue

        c0, c1 = run
        inner = c0 if side == "right" else c1
        sel = np.zeros_like(furniture)
        if side == "right":
            sel[:, inner:] = furniture[:, inner:]
        else:
            sel[:, :inner + 1] = furniture[:, :inner + 1]
        sel[:r0] = False
        sel[r1:] = False
        rws = np.nonzero(sel.any(axis=1))[0]
        if rws.size:
            # tighten to the run's OWN rows (never a nominal band, never widened
            # symmetrically for its own sake)
            lo_r, hi_r = int(rws[0]), int(rws[-1]) + 1
            hi_r = min(hi_r, guard_row)
            sel[:lo_r] = False
            sel[hi_r:] = False
        else:
            lo_r, hi_r = r0, r1

        area = int(sel.sum())
        frac = area / max(1, int(bi.sum()))
        med = float(np.median(luma[sel])) if area else -1.0
        blk.update({
            "inner_column": int(inner),
            "rows": [int(lo_r), int(hi_r)],
            "removed_px": area,
            "removed_frac_of_silhouette": round(frac, 4),
            "removed_median_luma": round(med, 1),
            "coverage_at_inner_column": round(float(cover[inner]), 3),
        })
        if area < MIN_AREA:
            blk.update({"verdict": "no wing",
                        "why": f"the run removes only {area}px, under the "
                               f"{MIN_AREA}px floor"})
        elif frac > MAX_REMOVE_FRAC:
            blk.update({"verdict": "REFUSED",
                        "why": f"the proposal removes {frac:.1%} of the "
                               f"silhouette, over the {MAX_REMOVE_FRAC:.0%} "
                               "ceiling — that is a mis-detection, not a wing"})
        elif hi_r > guard_row:
            blk.update({"verdict": "REFUSED",
                        "why": f"rows reach {hi_r}, at or below the shirt guard "
                               f"{guard_row}"})
        else:
            blk["verdict"] = "cut"
        rec[side] = blk

    rec["wing_right"] = rec["right"].get("inner_column") if rec["right"]["verdict"] == "cut" else None
    rec["wing_right_rows"] = ",".join(str(v) for v in rec["right"]["rows"]) \
        if rec["right"]["verdict"] == "cut" else "400,620"
    rec["wing_left"] = rec["left"].get("inner_column") if rec["left"]["verdict"] == "cut" else None
    rec["wing_left_rows"] = ",".join(str(v) for v in rec["left"]["rows"]) \
        if rec["left"]["verdict"] == "cut" else "400,520"
    rec["wing_cut_applied"] = bool(rec["wing_right"] is not None
                                   or rec["wing_left"] is not None)
    rec["wing_review"] = not rec["wing_cut_applied"]
    rec["wing_review_note"] = (
        "the instrument proposed no cut.  It abstains rather than guesses (see "
        "the module docstring: zero false positives, zero recall on the run-9 "
        "corpus).  Look at kf_overlay_00000.png; if a headrest wing is inside "
        "the green prompt, measure its inner column and pass an explicit "
        "`wings` block on the intake row.  If you miss one, the protrusion gate "
        "inside ship.py is the net."
        if not rec["wing_cut_applied"] else
        "a wing was measured and cut; the overlay shows it in red")
    return rec


# =============================================================================
# the stage
# =============================================================================
ORIGINAL_DIR = "_original"


def preserve_original(session: Path) -> Path | None:
    """Snapshot `prompts/kf_00000.png` to `prompts/_original/` the FIRST time
    anything is about to change it, and never again.

    THE STANDARD BACKUP NAME (2026-09-04).  Before this, every repair invented
    its own: `prompts_v1`, `prompts_v1_backup`, `prompts_v2`... and on
    `hermesdesktop` and `dgxspark` the repair OVERWROTE `prompts/` and archived
    the original under a name that reads like a version, so "the original
    frame-0 prompt" was not recoverable from the session's shape alone.  One
    name, written once, never overwritten.
    """
    src = session / "prompts" / "kf_00000.png"
    if not src.exists():
        return None
    dst = session / "prompts" / ORIGINAL_DIR / "kf_00000.png"
    if dst.exists():
        return dst
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    for extra in ("birefnet_00000.png", "kf_report_00000.json"):
        e = session / "prompts" / extra
        if e.exists():
            shutil.copy2(e, dst.parent / extra)
    return dst


def prompt_is_repaired(session: Path) -> dict:
    """Has this session's frame-0 prompt been changed since prompt0 wrote it?

    A repair round (`wingfix`, `bolsterfix`) rewrites `prompts/kf_00000.png`,
    and re-running `prompt0` would silently throw that work away — which is
    exactly what happened on `hermesdesktop` on 2026-09-04: the standard pass
    restored the UNCUT BiRefNet prompt, obj 1 went back to tracking him plus
    both wings, and the matte came out holding more chair than the file it was
    replacing.  So the comparison is against `prompts/_original/`, and when the
    live prompt differs from it the live one is the repaired one and it WINS.
    """
    live = session / "prompts" / "kf_00000.png"
    orig = session / "prompts" / ORIGINAL_DIR / "kf_00000.png"
    if not live.exists():
        return {"repaired": False, "why": "no frame-0 prompt yet"}
    if not orig.exists():
        return {"repaired": False, "why": "no _original snapshot to compare against"}
    a, b = live.read_bytes(), orig.read_bytes()
    if a == b:
        return {"repaired": False, "why": "the live prompt is the original"}
    import cv2 as _cv2
    import numpy as _np
    la = _cv2.imread(str(live), _cv2.IMREAD_GRAYSCALE) > 127
    lo = _cv2.imread(str(orig), _cv2.IMREAD_GRAYSCALE) > 127
    return {"repaired": True,
            "why": "the live prompt differs from prompts/_original/",
            "original_area_px": int(lo.sum()), "live_area_px": int(la.sum()),
            "removed_px": int((lo & ~la).sum()), "added_px": int((la & ~lo).sum())}


def build_prompt0(*, session: Path, plate: Path, wings: dict | None = None,
                  timeout: int = 1800, reset_prompt: bool = False) -> dict:
    """Stage 1 (BiRefNet, bake-off venv) then stage 2 (the wing cut).

    `wings` overrides the measurement entirely — an explicit intake row outranks
    the instrument.  Otherwise the wings are derived and the cut runs with them.

    THE GUARD (2026-09-04).  If this session's frame-0 prompt has been REPAIRED
    — it differs from `prompts/_original/kf_00000.png` — it is KEPT and nothing
    is rewritten, because re-deriving it throws away a hand or auto repair.
    `reset_prompt=True` is the explicit way to say "yes, really, start over".
    """
    session, plate = Path(session), Path(plate)
    out: dict = {"session": str(session), "plate": str(plate)}

    guard = prompt_is_repaired(session)
    out["prompt_guard"] = guard
    if guard["repaired"] and not reset_prompt:
        out["status"] = "kept"
        out["wings_source"] = "N/A — the repaired frame-0 prompt was KEPT"
        out["wings"] = {"wing_right": None, "wing_left": None,
                        "wing_cut_applied": False, "wing_review": False,
                        "wing_review_note": (
                            "the frame-0 prompt in this session is a REPAIRED one "
                            "(it differs from prompts/_original/).  prompt0 kept it "
                            "and re-derived nothing; pass --reset-prompt to start "
                            "from a fresh BiRefNet prompt and lose the repair.")}
        out["prompt_png"] = str(session / "prompts/kf_00000.png")
        ov = session / "prompts/kf_overlay_00000.png"
        out["overlay_png"] = str(ov) if ov.exists() else None
        rep = session / "prompts/kf_report_00000.json"
        out["kf_report"] = (json.loads(rep.read_text()) if rep.exists()
                            else {"prompt": {"area": guard["live_area_px"]},
                                  "removed": None})
        return out
    if reset_prompt and guard.get("repaired"):
        out["reset_prompt"] = True
    preserve_original(session)

    b = subprocess.run([str(BIREFNET_PY), str(PROMPT0), "birefnet",
                        "--session", str(session), "--plate", str(plate),
                        "--frames", "0"],
                       capture_output=True, text=True, timeout=timeout)
    if b.returncode != 0:
        raise RuntimeError(f"prompt0 birefnet failed:\n{b.stderr[-2000:]}")
    out["birefnet"] = json.loads((session / "prompts/birefnet_report.json").read_text())

    if wings is None:
        wings = derive_wings(plate, session / "prompts/birefnet_00000.png")
        out["wings_source"] = "MEASURED on this plate's frame 0"
    else:
        out["wings_source"] = "OVERRIDE from the intake row"
    out["wings"] = wings

    cmd = [str(PY), str(PROMPT0), "cut", "--session", str(session),
           "--plate", str(plate), "--frame", "0"]
    if wings.get("wing_right") is not None:
        cmd += ["--wing-right", str(wings["wing_right"]),
                "--wing-right-rows", wings.get("wing_right_rows", "400,620")]
    if wings.get("wing_left") is not None:
        cmd += ["--wing-left", str(wings["wing_left"]),
                "--wing-left-rows", wings.get("wing_left_rows", "400,520")]
    c = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if c.returncode != 0:
        raise RuntimeError(f"prompt0 cut failed:\n{c.stderr[-2000:]}")
    out["kf_report"] = json.loads(
        (session / "prompts/kf_report_00000.json").read_text())
    out["prompt_png"] = str(session / "prompts/kf_00000.png")
    out["overlay_png"] = str(session / "prompts/kf_overlay_00000.png")
    # the prompt prompt0 just wrote IS the original; snapshot it so a later
    # repair has something to be different from
    o = session / "prompts" / ORIGINAL_DIR / "kf_00000.png"
    if not o.exists():
        preserve_original(session)
        out["original_snapshot"] = str(o)
    out["status"] = out.get("status", "ok")
    return out


def _validate() -> int:
    """Replay the instrument against every session that carries a human verdict."""
    sessions = sorted((F / "pipeline/sam2/sessions").glob("*/prompts/kf_report_00000.json"))
    agree = disagree = 0
    print(f"{'session':24s} {'human':>22s}   {'measured':>22s}   verdict")
    for rep in sessions:
        sess = rep.parent.parent
        plate = sess / "plate_wide_25.mp4"
        png = sess / "prompts/birefnet_00000.png"
        if not (plate.exists() and png.exists()):
            continue
        human = json.loads(rep.read_text())
        try:
            got = derive_wings(plate, png)
        except Exception as e:
            print(f"{sess.name:24s} ERROR {e}")
            continue
        hr, hl = human.get("wing_right"), human.get("wing_left")
        gr, gl = got["wing_right"], got["wing_left"]
        same = (hr is None) == (gr is None) and (hl is None) == (gl is None)
        band = True
        for hv, gv, rows in ((hr, gr, human.get("wing_right_rows")),
                             (hl, gl, human.get("wing_left_rows"))):
            if hv is not None and gv is not None and abs(hv - gv) > 60:
                band = False
        ok = same and band
        agree += ok
        disagree += (not ok)
        print(f"{sess.name:24s} {str((hl, hr)):>22s}   {str((gl, gr)):>22s}   "
              f"{'AGREE' if ok else 'DIFFER'}")
    print(f"\nagree {agree}  differ {disagree}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--plate", type=Path)
    ap.add_argument("--birefnet", type=Path)
    a = ap.parse_args()
    if a.validate:
        sys.exit(_validate())
    print(json.dumps(derive_wings(a.plate, a.birefnet), indent=1))
