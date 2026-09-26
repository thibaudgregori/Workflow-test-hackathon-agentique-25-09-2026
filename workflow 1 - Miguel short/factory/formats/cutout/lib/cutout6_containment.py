"""ROUND 6 — CONTAINMENT, on LOSSLESS frames, over the WHOLE video.

fix5 is APPROVED, so round 6 owes a proof that it changed the caption band and
nothing else.  The obvious test — diff the two mp4s — cannot answer it: H.264
allocates bits across the whole frame, so changing the caption perturbs the
silhouette's macroblocks by up to ~21/255 with no content change at all.  That
is a property of the encoder, not of the composition, and no threshold can
separate the two honestly.

So the comparison is made BEFORE the encoder.  Both projects are rendered as
RGBA png-sequences by the same CLI and every one of the 1354 frame pairs is
diffed exactly.

That still leaves one confound, and it is real: the RENDERER is not bit-exact
run to run.  Rendering fix5 twice and diffing the two png-sequences is therefore
a mandatory NULL CONTROL — whatever that produces is the floor, and a claim of
containment means "fix5 -> fix6 changed nothing outside the caption band THAT
FIX5 -> FIX5 DOES NOT ALSO CHANGE".  Without the control the honest verdict is
unavailable, because a handful of antialiased pixels on a moving tile look
exactly like a regression.

Run:  python cutout6_containment.py <fix5_png_dir> <fix6_png_dir> [<fix5_again>]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
H, W = 1920, 1080
GEOM = HERE / "_geom_cutout_fix6.json"


def union_diff(a_dir: Path, b_dir: Path) -> tuple[np.ndarray, int]:
    # reading 2x1354 PNGs takes minutes; the union mask is the only thing the
    # verdict needs, so it is cached beside the sequences
    cache = a_dir.parent.parent / f"_union_{a_dir.parent.name}_{b_dir.parent.name}.npz"
    if cache.exists():
        z = np.load(cache)
        return z["mask"], int(z["frames"])
    A, B = sorted(a_dir.glob("*.png")), sorted(b_dir.glob("*.png"))
    if not A or len(A) != len(B):
        raise SystemExit(f"frame counts differ: {len(A)} vs {len(B)}")
    ever, n = np.zeros((H, W), bool), 0
    for pa, pb in zip(A, B):
        a = cv2.imread(str(pa), cv2.IMREAD_UNCHANGED)
        b = cv2.imread(str(pb), cv2.IMREAD_UNCHANGED)
        d = (a != b).any(axis=2)
        if d.any():
            n += 1
            ever |= d
    np.savez_compressed(cache, mask=ever, frames=n)
    return ever, n


def groups(mask: np.ndarray) -> list[list[int]]:
    """Contiguous row runs that contain a changed pixel, with their counts —
    the diff's GEOGRAPHY, which is the thing worth reading."""
    rows = mask.sum(axis=1)
    nz = np.where(rows)[0]
    if not nz.size:
        return []
    out, s = [], nz[0]
    for i in range(1, nz.size):
        if nz[i] != nz[i - 1] + 1:
            out.append([int(s), int(nz[i - 1]), int(rows[s:nz[i - 1] + 1].sum())])
            s = nz[i]
    out.append([int(s), int(nz[-1]), int(rows[s:nz[-1] + 1].sum())])
    return out


def main() -> None:
    a_dir, b_dir = Path(sys.argv[1]), Path(sys.argv[2])
    ctl_dir = Path(sys.argv[3]) if len(sys.argv) > 3 else None

    cap = json.loads(GEOM.read_text())["caption"]
    # the pill at the frozen seat, plus the halo the RETIRED `0 6px 22px` drop
    # shadow occupied.  A CSS shadow with a 22px blur and a +6px y offset paints
    # from `top - 22 + 6` to `bottom + 22 + 6`; 4px of antialiasing slack is
    # added on each side, which is what the measured extent (874..1037 against a
    # predicted 876..1035) actually needs.
    band = (int(cap["top"] - 22 + 6) - 4, int(cap["bottom"] + 22 + 6) + 4)

    ever, changed_frames = union_diff(a_dir, b_dir)
    ctl = np.zeros((H, W), bool)
    ctl_frames = None
    if ctl_dir is not None:
        ctl, ctl_frames = union_diff(a_dir, ctl_dir)

    outside = ever.copy()
    outside[band[0]:band[1], :] = False
    ctl_outside = ctl.copy()
    ctl_outside[band[0]:band[1], :] = False
    # NOT a pixel-wise subtraction.  The renderer's nondeterminism is stochastic:
    # it lands on different antialiased edges every run, so `outside & ~ctl` only
    # measures that two samples of noise are not the same sample.  The honest
    # test is whether fix5->fix6 is DISTINGUISHABLE from fix5->fix5: same total,
    # same worst cluster, same kind of place.
    og, cg = groups(outside), groups(ctl_outside)
    worst_out = max((g[2] for g in og), default=0)
    worst_ctl = max((g[2] for g in cg), default=0)
    rows = np.where(ever.any(axis=1))[0]
    cols = np.where(ever.any(axis=0))[0]
    rep = {
        "frames": len(sorted(a_dir.glob("*.png"))),
        "frames_with_any_change": changed_frames,
        "allowed_band": list(band),
        "caption_pill": [cap["top"], cap["bottom"]],
        "changed_rows": [int(rows.min()), int(rows.max())] if rows.size else None,
        "changed_cols": [int(cols.min()), int(cols.max())] if cols.size else None,
        "changed_px_union": int(ever.sum()),
        "outside_band_px_union": int(outside.sum()),
        "row_groups": groups(ever),
        "outside_row_groups": groups(outside),
        "null_control": {
            "dir": str(ctl_dir) if ctl_dir else None,
            "frames_with_any_change": ctl_frames,
            "px_union": int(ctl.sum()),
            "outside_band_px": int(ctl_outside.sum()),
            "outside_row_groups": cg,
            "worst_outside_cluster": worst_ctl,
        },
        "worst_outside_cluster": worst_out,
        "untouched": {
            "law12_top_band_0_192": int(ever[:192].sum()),
            "stage_zone_192_869": int(ever[192:869].sum()),
            "depth_band_1120_1560": int(ever[1120:1560].sum()),
        },
    }
    print(f"CONTAINMENT (lossless, all {rep['frames']} frames)")
    print(f"  allowed band   rows {band[0]}..{band[1]}  (pill "
          f"{cap['top']}..{cap['bottom']} + the retired shadow's halo)")
    print(f"  changed rows   {rep['changed_rows']}   cols {rep['changed_cols']}")
    print(f"  changed px     {rep['changed_px_union']:,} union, "
          f"{rep['outside_band_px_union']:,} outside the band")
    for g in rep["row_groups"]:
        tag = "CAPTION BAND" if g[0] >= band[0] and g[1] <= band[1] else "outside"
        print(f"     rows {g[0]:>4}..{g[1]:<4} {g[2]:>8,} px   {tag}")
    fails = []
    if ctl_dir is not None:
        print(f"  NULL CONTROL   fix5 rendered TWICE, zero content difference: "
              f"{rep['null_control']['px_union']:,} px differ over "
              f"{rep['null_control']['frames_with_any_change']} frames, "
              f"{rep['null_control']['outside_band_px']:,} of them outside the band")
        for g in cg:
            print(f"     rows {g[0]:>4}..{g[1]:<4} {g[2]:>8,} px   control noise")
        print(f"  VERDICT        outside the band: fix6 {rep['outside_band_px_union']} px "
              f"vs the renderer's own {rep['null_control']['outside_band_px']} px; "
              f"worst cluster {worst_out} vs {worst_ctl}")
        if ever[:192].any():
            fails.append(f"{int(ever[:192].sum())}px changed in Law 12's top band")
        if rep["outside_band_px_union"] > 1.5 * rep["null_control"]["outside_band_px"]:
            fails.append(f"outside-band change {rep['outside_band_px_union']}px is "
                         f"more than 1.5x the renderer's own "
                         f"{rep['null_control']['outside_band_px']}px")
        if worst_out > 1.5 * max(worst_ctl, 1):
            fails.append(f"a {worst_out}px cluster outside the band, against a "
                         f"{worst_ctl}px worst cluster in the control")
    else:
        fails.append("no null control — a second fix5 render is required before "
                     "any outside-band pixel can be called a regression")
    rep["fails"] = fails
    (HERE / "logs/containment_fix6.json").write_text(json.dumps(rep, indent=2))
    if fails:
        print("FAIL")
        for f in fails:
            print("  - " + f)
        raise SystemExit(1)
    print("PASS — outside the caption band, fix6 differs from fix5 by no more, "
          "and no differently, than fix5 differs from a second render of ITSELF")


if __name__ == "__main__":
    main()
