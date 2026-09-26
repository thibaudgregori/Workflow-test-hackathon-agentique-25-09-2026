#!/usr/bin/env python
"""THE CHAIR AUDIT — measure the reviewed selection against the plate's own
chair BEFORE the paid track, and carve the leak the reviewer missed.

=============================================================================
WHY THIS EXISTS — run 24, `claudesessions`, 2026-09-21
=============================================================================
The frame-0 selection was signed `status: reviewed`, `edits: []`, with the note

    "the black chair back left of the head and behind the right shoulder is
     OUTSIDE; no edits needed"

and it was not.  The approved mask was byte-for-byte the raw BiRefNet mask
(`mask_sha256` differed from `base_mask_sha256` only because `approve`
re-encodes the PNG; both hold 490,995 person pixels), and 6,822 of those pixels
are the gaming chair's right headrest wing, plate luma mean 14.6, in rows
273-439 beside his head.  `pipeline/matting/client.py` hands that mask to
MatAnyone 2 as the ONLY prompt, so the model propagated the wedge through all
531 frames: matte review HOLD, "a large black slab ... immediately right of his
head ... a hard straight vertical cut edge ... over the cream ground it reads as
a solid black wedge", chair_band p50 2,993 / max 11,279 px.

The bug is not the reviewer's eyes.  The bug is that a SENTENCE about the chair
was the only thing standing between the run and a paid track, and nothing in the
pipeline ever measured the claim.  The detector that can measure it already
existed -- `pipeline/sam2/chairprompt.py` finds the headrest wing on frame 0 and
is darkness-gated -- but it was wired only into the SAM2 lane, which production
does not use.  So: run it on the REVIEWED MASK, and where a wing it found is
still inside that mask, subtract exactly that wing.

=============================================================================
WHAT IT WILL AND WILL NOT DO
=============================================================================
It carves only the detector's own accepted footprint (`rec["spans"]`, the
per-row runs of the component the wing test passed), intersected with the mask,
dilated `dilate_px` so the wedge's anti-aliased fringe goes with it.  Three
guards, each measured on this recording:

  leak_floor_px   a wing whose overlap with the mask is under this is already
                  excluded and the audit is a NO-OP.  (This recording's LEFT
                  wing: 157 px -- the reviewer's contour really did hold it out.
                  Its RIGHT wing: 6,822 px.)
  carve_luma_max  the carve's mean plate luma.  CHAIR BLACK IS THE WHOLE GUARD,
                  exactly as in `chairprompt.rescue_luma_max`: on this plate the
                  right wing reads 14.6 while his beard, jaw shadow and stubble
                  read 35-60.  Above this ceiling the audit REFUSES and blocks
                  the track instead of carving -- that is a body, not a wedge,
                  and run 14's lesson is that a third automatic carve on a
                  refusal is how an ear, a cheek and a jaw get eaten.
  carve_frac_max  a carve bigger than this share of the mask is not a headrest.
                  (This recording: 1.42 %.)

It never invents anatomy, never touches a mask whose wings are already out, and
never runs on anything but the exact plate/source/crop the selection is bound
to -- `selection.validate` still gates the result.

=============================================================================
AND THE CARVE IS NOT A CURE.  MEASURED, 2026-09-21.
=============================================================================
The obvious repair -- carve the wing out of the frame-0 prompt and re-track --
WAS TRIED ON THIS RECORDING AND DOES NOTHING.  MatAnyone 2 is a refinement
model: it re-grows a contiguous dark region that is welded to his black shirt
whether or not the prompt holds it.  The second paid track (mask a39d3252,
alpha 9dc321eb, a genuinely different track from abaa6210 / 7104076d) kept
9,077 of the 9,077 carved pixels on EVERY sampled frame, and the chair band
measured against the pre-carve reference came back 2,993 / 6,191 / 11,279 px --
the same three digits as the matte the viewer held.

So a chair leak is not a contour defect, and the audit does NOT pretend to fix
it.  It CORRECTS THE CONTOUR anyway -- because `matte_review.py`'s chair band
measures "dark pixels the matte kept more than 12 px outside the reviewed
contour", so a contour that contains the chair makes the one instrument that
could see the wedge blind to it -- and then it HOLDS: the production track does
not get paid for, and the recording goes to the chair-aware lane or to Miguel.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
F = HERE.parents[1]
sys.path.insert(0, str(F / "pipeline/sam2"))
import chairprompt  # noqa: E402

PY = sys.executable

CARVE = dict(
    leak_floor_px=1500,   # under this the wing is already outside the contour
    carve_luma_max=40,    # chair black; skin shadow reads 35-60 (chairprompt)
    chair_black_max=30,   # a pixel this dark is chair, never beard or jaw (chair 15-25, face 35-60)
    carve_frac_max=0.06,  # of the person mask
    dilate_px=2,          # take the wedge's anti-aliased fringe with it
)


def _footprint(rec: dict, shape: tuple[int, int]) -> np.ndarray:
    """The detector's accepted wing, filled per row, as a boolean image."""
    out = np.zeros(shape, bool)
    for r, (a, b) in rec.get("spans", {}).items():
        out[int(r), int(a):int(b) + 1] = True
    return out


def measure(frame_bgr: np.ndarray, mask: np.ndarray,
            cfg: dict = CARVE) -> dict:
    """Pure core: frame 0 + the reviewed person mask -> the verdict.

    `verdict` is one of:
      clean    no wing, or every wing already outside the contour.  No-op.
      hold     at least one wing leaks and every guard passes; `carve` is the
               boolean image to subtract so the chair-band instrument can see
               the wedge -- and the production track is NOT paid for, because
               the carve does not stop MatAnyone re-growing it (see above).
      refuse   the chair-black carve is too big to be a headrest.  The caller
               must NOT track.  (A leak that reads as body is NOT a refusal
               since 2026-09-23: it is his face or shirt, and the side reads
               action "body".)
    """
    luma = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    mask = mask.astype(bool)
    band = chairprompt.derive_band(mask)
    rec: dict = {"band": band, "sides": {}, "leak_px": 0,
                 "mask_px": int(mask.sum()), "thresholds": dict(cfg)}
    if band is None:
        return dict(rec, verdict="clean",
                    why="no head band on frame 0; nothing to audit")
    carve = np.zeros(mask.shape, bool)
    for side in ("left", "right"):
        w = chairprompt.find_wing(luma, mask, band, side)
        s: dict = {"found": bool(w.get("found"))}
        if not w.get("found"):
            s["why"] = w.get("why")
            rec["sides"][side] = s
            continue
        foot = _footprint(w, mask.shape)
        leak = foot & mask
        n = int(leak.sum())
        s.update(rows=w["rows"], cols=w["cols"], box=w["box"],
                 wing_px=int(foot.sum()), leak_px=n,
                 wing_luma_mean=w["luma"]["mean"])
        if n:
            s["leak_luma_mean"] = round(float(luma[leak].mean()), 1)
            s["leak_luma_p95"] = int(np.percentile(luma[leak], 95))
        if n < cfg["leak_floor_px"]:
            s["action"] = "none"
            s["note"] = (f"{n} px of this wing are inside the contour, under "
                         f"the {cfg['leak_floor_px']} px floor: the reviewer "
                         f"held it out")
        elif s["leak_luma_mean"] > cfg["chair_black_max"]:
            # A BODY IS NOT A CHAIR (run 26 + run 27, 2026-09-23). The wing footprint
            # overlapped his cheek, beard, temple or black cap on four recordings
            # (leak mean 39.7-53). Refusing blocked the track; carving (lunafree, mean
            # 39.7 just under the old 40 ceiling) bit his temple and cap, and Astra had
            # to restore the outline. His black cap is as dark as the chair, so darkness
            # alone cannot pick chair pixels out of a mixed leak. The only leak that is
            # carved is one that reads as chair as a WHOLE (claudesessions: 14.6).
            s["action"] = "body"
            s["note"] = (f"{n} px of the wing footprint are inside the contour but "
                         f"read mean luma {s['leak_luma_mean']} (chair reads 15-25, "
                         f"ceiling {cfg['chair_black_max']}): that is his face, cap "
                         f"or shirt. Nothing is carved; the track may run.")
        else:
            s["action"] = "hold"
            carve |= leak
        rec["leak_px"] += n
        rec["sides"][side] = s

    if any(s.get("action") == "refuse" for s in rec["sides"].values()):
        why = "; ".join(f"{k}: {v['note']}" for k, v in rec["sides"].items()
                        if v.get("action") == "refuse")
        return dict(rec, verdict="refuse", why=why)
    if not carve.any():
        return dict(rec, verdict="clean",
                    why="no headrest wing survives inside the reviewed contour")

    k = 2 * int(cfg["dilate_px"]) + 1
    grown = cv2.dilate(carve.astype(np.uint8), np.ones((k, k), np.uint8), 1) > 0
    grown &= mask
    frac = float(grown.sum()) / max(int(mask.sum()), 1)
    rec["carve_px"] = int(grown.sum())
    rec["carve_frac_of_mask"] = round(frac, 4)
    rec["carve_luma_mean"] = round(float(luma[grown].mean()), 1)
    if frac > cfg["carve_frac_max"]:
        return dict(rec, verdict="refuse",
                    why=(f"the carve is {frac:.1%} of the person mask (ceiling "
                         f"{cfg['carve_frac_max']:.0%}); a headrest wing is not "
                         f"that big, so this is his body"))
    rec["carve"] = grown
    rec["why"] = ("the reviewed contour holds the headrest wing; the contour is "
                  "corrected so the chair band can see it, and the production "
                  "track is held: a frame-0 carve does not stop MatAnyone 2 "
                  "re-growing a dark region welded to his shirt (measured "
                  "2026-09-21: 9,077 of 9,077 carved px kept on every frame)")
    return dict(rec, verdict="hold")


def polygons(carve: np.ndarray, epsilon: float = 2.0) -> list[dict]:
    """The carve as `selection.py` exclude polygons, so the heal is recorded in
    the reviewed selection in the SAME shape a human reviewer's edit has."""
    cnts, _ = cv2.findContours(carve.astype(np.uint8), cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)
    out = []
    for c in cnts:
        p = cv2.approxPolyDP(c, epsilon, True).reshape(-1, 2)
        if len(p) < 3:
            continue
        out.append({"operation": "exclude",
                    "points": [[int(x), int(y)] for x, y in p]})
    return out


def audit_selection(selection: Path, plate: Path, source: Path, crop: Path,
                    *, frame: Path | None = None, write: bool = True,
                    cfg: dict = CARVE) -> dict:
    """Measure, and when it is chair, heal the selection through `selection.py`.

    The heal re-runs `selection.py approve` with the previous mask kept as
    `selection.mask.png.pre_chaircarve` and the carve appended to the reviewed
    `edits`, so `mask_sha256`, `base_mask_sha256` and the edit list stay the
    authority they already are.  Nothing else writes the selection.
    """
    selection, plate = Path(selection), Path(plate)
    d = json.loads(selection.read_text())
    mask_path = Path(d["mask"])
    mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE) > 127
    bgr = (cv2.imread(str(frame)) if frame
           else chairprompt.plate_frame(plate, 0))
    rec = measure(bgr, mask, cfg)
    carve = rec.pop("carve", None)
    rec["selection"] = str(selection)
    # A HOLD IS STICKY.  The carve makes this recording's contour read `clean`
    # on the next pass, and a `clean` contour would let the very track this
    # audit just held get paid for on a rerun.  So a recording whose ledger
    # already carries a hold keeps holding until a human clears the ledger.
    if rec["verdict"] == "clean":
        prior = [h for h in _history(selection) if h.get("verdict") == "hold"]
        if prior:
            rec["verdict"] = "hold"
            rec["sticky"] = True
            rec["why"] = ("a previous chair audit carved the headrest out of "
                          "this contour; MatAnyone re-grows it, so the "
                          "production track stays held.  Delete "
                          "chair_audit.json to re-arm, and only after the "
                          "matte has been looked at.")
            _record(selection, rec)
            return rec
    if rec["verdict"] != "hold" or not write:
        _record(selection, rec)
        return rec

    edits = list(d.get("edits") or []) + polygons(carve)
    keep = mask_path.with_suffix(mask_path.suffix + ".pre_chaircarve")
    if not keep.exists():
        keep.write_bytes(mask_path.read_bytes())
    ed = selection.with_suffix(".chaircarve_edits.json")
    ed.write_text(json.dumps(edits))
    note = (f"CHAIR AUDIT (pipeline/matting/chair_audit.py): the reviewed "
            f"contour still held {rec['leak_px']} px of the headrest wing "
            f"(carved {rec['carve_px']} px, mean plate luma "
            f"{rec['carve_luma_mean']}, {rec['carve_frac_of_mask']:.2%} of the "
            f"mask).  MatAnyone is prompted with the frame-0 mask alone, so a "
            f"wing left inside it is propagated to every frame.  Previous mask "
            f"kept as {keep.name}.  Original review: "
            + (d.get("notes") or "")[:400])
    cmd = [PY, str(HERE / "selection.py"), "approve",
           "--plate", str(plate), "--source", str(source), "--crop", str(crop),
           "--selection", str(selection), "--mask", str(keep),
           "--edits", str(ed), "--reviewer",
           (d.get("reviewer") or "unknown") + " + chair_audit",
           "--notes", note]
    p = subprocess.run(cmd, capture_output=True, text=True)
    rec["approve_returncode"] = p.returncode
    if p.returncode != 0:
        rec["verdict"] = "refuse"
        rec["why"] = "selection.py approve refused the carve: " + p.stderr[-600:]
        return rec
    rec["edits_added"] = len(edits) - len(d.get("edits") or [])
    after = json.loads(selection.read_text())
    rec["mask_sha256"] = after["mask_sha256"]
    rec["pre_chaircarve_mask"] = str(keep)
    rec["healed"] = True
    _record(selection, rec)
    return rec


def _history(selection: Path) -> list:
    path = Path(selection).parent / "chair_audit.json"
    try:
        h = json.loads(path.read_text())
    except Exception:                                          # noqa: BLE001
        return []
    return h if isinstance(h, list) else [h]


def _record(selection: Path, rec: dict) -> None:
    """The audit's own ledger beside the selection.  `mark_stage` keeps only
    scalar fields, so the measurement has to live somewhere a reviewer can read
    it; this is that file, appended to, never overwritten."""
    path = Path(selection).parent / "chair_audit.json"
    hist = _history(selection)
    hist.append({k: v for k, v in rec.items()
                 if not isinstance(v, np.ndarray)})
    path.write_text(json.dumps(hist, indent=1))


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="audit a reviewed selection for "
                                             "a retained chair headrest wing")
    for n in ("selection", "plate", "source", "crop"):
        ap.add_argument("--" + n, type=Path, required=True)
    ap.add_argument("--frame", type=Path, default=None)
    ap.add_argument("--measure-only", action="store_true")
    a = ap.parse_args()
    rec = audit_selection(a.selection, a.plate, a.source, a.crop,
                          frame=a.frame, write=not a.measure_only)
    print(json.dumps({k: v for k, v in rec.items()
                      if not isinstance(v, np.ndarray)}, indent=1))
    return {"clean": 0, "hold": 5, "refuse": 4}[rec["verdict"]]


if __name__ == "__main__":
    raise SystemExit(main())
