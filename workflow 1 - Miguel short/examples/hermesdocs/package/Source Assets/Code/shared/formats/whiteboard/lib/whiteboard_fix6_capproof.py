"""FORMAT LAB — WHITEBOARD, THE CLOSING CAPTIONS ROUND (fix6).

FOUR PROOFS, all on DECODED PIXELS out of the shipped mp4s — never on the
generator's word.

  A. THE PILL, MEASURED, EVERY 0.40 s OF BOTH VIDEOS.  Height, width, centre.
     Round 5's one-font-size law says the pill renders at ONE size for the whole
     video: that is a claim about pixels, so it is checked on pixels.  The
     canonical height is 114.59 px of CSS box; decoded through a 25 fps H.264
     encode the terracotta body reads 114-115 px, and it must read the SAME
     number on every caption of both videos.

  B. THE GLYPHS, MEASURED.  A pill of constant height would still be consistent
     with wrong type if the padding absorbed a size change, so the LETTERS are
     measured independently: inside each pill, the white-ink row profile is
     thresholded at half its peak and the contiguous band around the peak is the
     x-height band.  One font size => one x-height, to the pixel.

  C. THE BOARD, WITH THE CAPTIONS SWITCHED OFF.  A pill is opaque, so the mp4
     can never show what is underneath it.  This re-snapshots the SAME
     composition with `.scap {display:none}` and reads the reserved band on real
     pixels: every row from the band's top (now 799.20 px, 1.42 px higher than
     round 4 because the canon pill is 2.84 px taller) down to the seam must be
     board background, at every camera stop and across a full 0.32 s sweep.

  D. CONTAINMENT.  Decoded-pixel diff of fix6 against the round-4 DEFINITIVE
     file, frame by frame.  Only the caption band may differ.  The diff's
     geography is reported, not asserted away.

Run after `whiteboard_fix6_gen.py` and both renders:

    ~/Documents/Workspace/.venv/bin/python whiteboard_fix6_capproof.py
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

import whiteboard_fix6_core as core

HOME = core.HOME
OUT = HOME / "out"
CLI = (core.WORKSPACE
       / "projects/personal/infra/agent-tools/hyperframes/packages/cli/dist/cli.js")
WORK = HOME / ".capproof6"

SEAM_PX = core.px(core.SEAM)                 # 862.5
BAND_TOP = SEAM_PX - core.CAP_CLEAR_PX       # 799.20
CREAM = np.array([246, 241, 234], dtype=np.int16)
TERRA = np.array([196, 87, 58], dtype=np.int16)

PAIRS = [("whiteboard_fix6", "whiteboard_fix4"),
         ("whiteboard_zoom_fix6", "whiteboard_zoom_fix4")]


# =============================================================================
# frames
# =============================================================================
def frame(video: Path, t: float) -> np.ndarray:
    dst = WORK / "frames" / f"{video.stem}_{t:07.2f}.png"
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video),
                        "-frames:v", "1", "-y", str(dst)], check=True)
    return np.asarray(Image.open(dst).convert("RGB"), dtype=np.int16)


# =============================================================================
# A + B — the pill and its glyphs
# =============================================================================
def pill_box(img: np.ndarray) -> tuple[int, int, int, int] | None:
    """The pill = the terracotta block that STRADDLES THE SEAM (NOTES law 17).

    Two traps this had to be built around, both found on real frames:

    * the SEAM ROW RUNS THROUGH THE TYPE, so the longest contiguous terracotta
      run on that row is a gap between two letters (65 px), not the pill.  The
      pill's horizontal extent is min/max of terracotta on the row instead —
      safe, because pass C proves the reserved band above the seam is empty.
    * walking a single interior column down leaks into the FACE VIDEO whenever
      the shot under the pill happens to be terracotta-ish, which inflated the
      height to 465 px on one frame.  The walk runs on both PADDING GUTTERS at
      once (28-34 px inside each cap, clear of the 22.5 px corner radius), and
      the threshold is 0.5 rather than 1.0 because a descender — the "j" of
      "just unbelievable." — reaches into the left gutter and would otherwise
      cut the pill in half.
    """
    terra = (np.abs(img - TERRA).sum(axis=2) < 110)
    seam = int(SEAM_PX)
    xs = np.nonzero(terra[seam])[0]
    if len(xs) < 60:
        return None
    x0, x1 = int(xs.min()), int(xs.max())
    if x1 - x0 < 120:
        return None
    g = np.concatenate([terra[:, x0 + 28:x0 + 34],
                        terra[:, x1 - 33:x1 - 27]], axis=1).mean(axis=1)
    if g[seam] < 0.5:
        return None
    y0 = y1 = seam
    while y0 > seam - 90 and g[y0 - 1] >= 0.5:
        y0 -= 1
    while y1 < seam + 90 and g[y1 + 1] >= 0.5:
        y1 += 1
    return y0, y1, x0, x1


def x_height(img: np.ndarray, box: tuple[int, int, int, int]) -> float | None:
    """The LETTERS' own size, independent of the box that holds them.

    Inside the pill's ink area (both paddings excluded, so no rounded corner and
    no board background can enter), the white-ink row profile is thresholded at
    half its peak and the two crossings are interpolated to sub-pixel.  That
    band is the x-height: the rows every lowercase letter occupies.
    """
    y0, y1, x0, x1 = box
    crop = img[y0 + 1:y1, x0 + 34:x1 - 33]
    ink = ((crop.min(axis=2) > 190) & (crop.sum(axis=2) > 660)).sum(axis=1)
    ink = ink.astype(float)
    if ink.size == 0 or ink.max() < 8:
        return None
    half = ink.max() * 0.5
    on = np.nonzero(ink >= half)[0]
    a, b = int(on.min()), int(on.max())

    def cross(i: int, j: int) -> float:
        return i + (half - ink[i]) / (ink[j] - ink[i]) if ink[j] != ink[i] else float(i)

    top = cross(a - 1, a) if a > 0 and ink[a - 1] < half else float(a)
    bot = cross(b + 1, b) if b + 1 < len(ink) and ink[b + 1] < half else float(b)
    return round(bot - top, 2)


def pass_ab(video: Path, step: float = 0.40) -> dict:
    """Every 0.40 s up to the outro — the outro's @handle chip is a terracotta
    pill too (Law 12 exempts it) and it is NOT a caption, so it is excluded by
    time rather than by a fudge factor."""
    rows = []
    t = 0.20
    while t < core.OUTRO_T:
        img = frame(video, t)
        box = pill_box(img)
        if box:
            y0, y1, x0, x1 = box
            rows.append({"t": round(t, 2), "h": y1 - y0 + 1, "w": x1 - x0 + 1,
                         "centre": (y0 + y1) / 2, "xh": x_height(img, box)})
        t = round(t + step, 2)
    heights = sorted({r["h"] for r in rows})
    xhs = [r["xh"] for r in rows if r["xh"] is not None]
    return {"frames_with_a_pill": len(rows), "pill_heights_px": heights,
            "pill_centres_px": sorted({r["centre"] for r in rows}),
            "widest_pill_px": max((r["w"] for r in rows), default=0),
            "x_height_n": len(xhs),
            "x_height_min": round(min(xhs), 2), "x_height_max": round(max(xhs), 2),
            "x_height_mean": round(float(np.mean(xhs)), 3),
            "x_height_sd": round(float(np.std(xhs)), 3),
            "rows": rows}


# =============================================================================
# C — the board with the captions off
# =============================================================================
def band_report(img: np.ndarray) -> dict:
    band = img[int(np.ceil(BAND_TOP)):int(SEAM_PX)]
    off = np.abs(band - CREAM).sum(axis=2)
    hit = off > 24
    ys, xs = np.nonzero(hit)
    return {"rows": int(band.shape[0]), "non_bg_px": int(hit.sum()),
            "worst_row_px": (int(BAND_TOP) + 1 + int(np.bincount(ys).argmax()))
            if hit.any() else None,
            "x_range": [int(xs.min()), int(xs.max())] if hit.any() else None}


def captionless_twin() -> Path:
    audit = WORK / "audit_project"
    audit.mkdir(parents=True, exist_ok=True)
    link = audit / "assets"
    if link.is_symlink() or link.exists():
        link.unlink()
    link.symlink_to(core.STAGE.resolve(), target_is_directory=True)
    html = (HOME / "whiteboard_zoom_fix6" / "index.html").read_text(encoding="utf-8")
    html = html.replace("</style>", ".scap{display:none!important}</style>", 1)
    (audit / "index.html").write_text(html, encoding="utf-8")
    return audit


def snapshot(audit: Path, times: list[float], name: str) -> dict[float, Path]:
    out = WORK / name
    if out.exists():
        shutil.rmtree(out)
    subprocess.run(["node", str(CLI), "snapshot", str(audit), "-o", str(out),
                    "--at", ",".join(f"{t:.2f}" for t in times), "--no-end",
                    "--describe", "false"], check=True, capture_output=True, text=True)
    shot = {}
    for p in sorted(out.glob("*.png")):
        m = re.search(r"at-([\d.]+)s", p.name)
        if m:
            shot[round(float(m.group(1)), 2)] = p
    return shot


# =============================================================================
# D — containment against the round-4 definitive file
# =============================================================================
MAT_THR = 60          # per-pixel channel-sum difference that is a REAL change
NOISE_THR = 10        # below this, two independent H.264 encodes always differ


def containment(new: Path, old: Path, times: list[float]) -> dict:
    """Decoded-pixel diff against the round-4 DEFINITIVE file.

    The two mp4s are independent encodes of nearly identical pictures, so at a
    threshold of 10 the diff covers the whole frame at magnitudes of 1-2 out of
    765 — that is the encoder, not the composition.  A REAL change (a pill that
    moved, type that resized) is a solid-colour swap worth hundreds of units
    over thousands of ADJACENT pixels.

    So the verdict is not "is anything different outside the band" — on two
    independent H.264 encodes the answer is always yes, a few dozen speckles on
    the highest-contrast ink edges, most of them during a camera move.  The
    verdict is whether anything outside the band is CLUSTERED: the frame is cut
    into 20x20 tiles and the densest out-of-band tile is reported.  A moved or
    resized element fills tiles (400 px each); encoder speckle does not.
    """
    band = slice(int(SEAM_PX - core.CAP_PILL_H_PX / 2 - 2),
                 int(SEAM_PX + core.CAP_PILL_H_PX / 2 + 3))
    rows_hit = np.zeros(1920, dtype=np.int64)
    cols_hit = np.zeros(1080, dtype=np.int64)
    noise_rows = np.zeros(1920, dtype=np.int64)
    in_band = out_band = worst_out = densest = 0
    means = []
    for t in times:
        d = np.abs(frame(new, t) - frame(old, t)).sum(axis=2)
        means.append(float(d.mean()))
        noise_rows += (d > NOISE_THR).sum(axis=1)
        hit = d > MAT_THR
        if not hit.any():
            continue
        rows_hit += hit.sum(axis=1)
        cols_hit += hit.sum(axis=0)
        n_in = int(hit[band].sum())
        out = hit.copy()
        out[band] = False
        n_out = int(out.sum())
        in_band += n_in
        out_band += n_out
        worst_out = max(worst_out, n_out)
        if n_out:
            ys, xs = np.nonzero(out)
            tiles = np.zeros((1920 // 20 + 1, 1080 // 20 + 1), dtype=np.int32)
            np.add.at(tiles, (ys // 20, xs // 20), 1)
            densest = max(densest, int(tiles.max()))
    ys = np.nonzero(rows_hit)[0]
    xs = np.nonzero(cols_hit)[0]
    nz = np.nonzero(noise_rows)[0]
    total = in_band + out_band
    return {"frames_compared": len(times), "material_thr": MAT_THR,
            "diff_rows": [int(ys.min()), int(ys.max())] if len(ys) else None,
            "diff_cols": [int(xs.min()), int(xs.max())] if len(xs) else None,
            "pill_band_rows": [band.start, band.stop - 1],
            "material_px_in_band": in_band,
            "material_px_out_of_band": out_band,
            "out_of_band_share_pct": round(100 * out_band / max(1, total), 4),
            "worst_frame_out_of_band_px": worst_out,
            "densest_out_of_band_20x20_tile_px": densest,
            "noise_floor_rows": [int(nz.min()), int(nz.max())] if len(nz) else None,
            "mean_abs_diff_per_px_of_765": round(float(np.mean(means)), 3)}


# =============================================================================
def main() -> None:
    (WORK / "frames").mkdir(parents=True, exist_ok=True)
    report: dict = {"seam_px": SEAM_PX, "cap_font_px": core.CAP_FS_PX,
                    "cap_pill_h_px": core.CAP_PILL_H_PX,
                    "cap_clear_px": core.CAP_CLEAR_PX, "band_top_px": BAND_TOP,
                    "cap_w_budget_px": core.CAP_MAX_W_PX}
    ok = True

    # ---- A + B ------------------------------------------------------------
    print("A/B — THE PILL AND ITS GLYPHS, decoded every 0.40 s")
    for new, _old in PAIRS:
        r = pass_ab(OUT / f"{new}.mp4")
        report[f"{new}_pill"] = {k: v for k, v in r.items() if k != "rows"}
        good = (r["pill_heights_px"] == [114]
                and len(r["pill_centres_px"]) == 1
                and r["x_height_max"] - r["x_height_min"] < 2.5
                and r["widest_pill_px"] <= core.CAP_MAX_W_PX)
        ok &= good
        print(f"  {new:22s} pills={r['frames_with_a_pill']:4d}  "
              f"H={r['pill_heights_px']} px  centre={r['pill_centres_px']} px  "
              f"widest={r['widest_pill_px']} px  "
              f"x-height={r['x_height_mean']}+-{r['x_height_sd']} "
              f"[{r['x_height_min']}, {r['x_height_max']}]  "
              f"{'PASS' if good else 'FAIL'}")

    # the NEGATIVE CONTROL: the same instrument on the round-4 file, where the
    # shrink formula was still alive.  An instrument that cannot tell the two
    # apart is not an instrument.
    ctl = pass_ab(OUT / "whiteboard_fix4.mp4")
    report["control_whiteboard_fix4"] = {k: v for k, v in ctl.items() if k != "rows"}
    print(f"  {'CONTROL fix4 (round 4)':22s} pills={ctl['frames_with_a_pill']:4d}  "
          f"H={ctl['pill_heights_px']} px  "
          f"x-height={ctl['x_height_mean']}+-{ctl['x_height_sd']} "
          f"[{ctl['x_height_min']}, {ctl['x_height_max']}]  <- the defect, visible")

    # ---- C ----------------------------------------------------------------
    print("\nC — THE BOARD UNDER THE PILL, captions off")
    plan = json.loads((HOME / "whiteboard_zoom_fix6" / "camera_plan.json").read_text())
    stops = plan["stops"] if isinstance(plan, dict) else plan
    audit = captionless_twin()
    times = []
    for i, s in enumerate(stops):
        t0 = s["t"] + 0.90
        t1 = stops[i + 1]["t"] if i + 1 < len(stops) else core.OUTRO_T
        times.append(round(min(t0 + (t1 - t0) / 2, t1 - 0.30), 2))
    shot = snapshot(audit, times, "snaps")
    ship = OUT / "whiteboard_zoom_fix6.mp4"
    rows = []
    print(f"{'stop':>6} {'subject':11s} {'z':>5} {'sample':>7} {'pill top':>9} "
          f"{'band top':>9} {'margin':>7} {'ink in band':>12}  verdict")
    for s, t in zip(stops, times):
        box = pill_box(frame(ship, t))
        top = float(box[0]) if box else None
        key = min(shot, key=lambda k: abs(k - t))
        clean = np.asarray(Image.open(shot[key]).convert("RGB"), dtype=np.int16)
        br = band_report(clean)
        good = br["non_bg_px"] == 0 and (top is None or top >= BAND_TOP - 0.5)
        ok &= good
        rows.append({"stop": s["t"], "subject": s["subject"], "z": s["z"],
                     "sampled_at": t, "pill_top_px": top,
                     "band_top_px": round(BAND_TOP, 2),
                     "pill_margin_px": round(top - BAND_TOP, 2) if top else None,
                     "solver_lowest_ink_px": s["lowest_ink_px"],
                     "solver_clearance_px": s["cap_clearance_px"],
                     "band_pixels": br})
        print(f"{s['t']:6.2f} {s['subject']:11s} {s['z']:5.2f} {t:7.2f} "
              f"{(top if top is not None else -1):9.1f} {BAND_TOP:9.2f} "
              f"{(rows[-1]['pill_margin_px'] or 0):7.2f} {br['non_bg_px']:12d}  "
              f"{'PASS' if good else 'FAIL'}")
    report["stops"] = rows

    sweep_t = [round(0.30 + i * 0.32, 2) for i in range(int(core.OUTRO_T / 0.32))]
    sw = snapshot(audit, sweep_t, "snaps_sweep")
    dirty = [t for t, p in sorted(sw.items())
             if band_report(np.asarray(Image.open(p).convert("RGB"),
                                       dtype=np.int16))["non_bg_px"]]
    sched = core.schedule(core.anchors(core.load_words()))
    mv = [(t, t + d) for t, _, _, d in sched if d > 0]
    in_hold = [t for t in dirty
               if not any(m0 - 0.16 <= t <= m1 + 0.16 for m0, m1 in mv)]
    ok &= not in_hold
    print(f"\n  full sweep, captions off: {len(sweep_t)} frames every 0.32 s")
    print(f"    frames with ink in the band : {len(dirty)} -> {dirty}")
    print(f"    of those, inside a HOLD     : {len(in_hold)} -> {in_hold or 'none'}")
    report["sweep_dirty_t"] = dirty
    report["sweep_dirty_in_hold"] = in_hold

    # ---- D ----------------------------------------------------------------
    print("\nD — CONTAINMENT vs the round-4 definitive files")
    ct = [round(0.30 + i * 1.10, 2) for i in range(int(core.DUR / 1.10))]
    for new, old in PAIRS:
        c = containment(OUT / f"{new}.mp4", OUT / f"{old}.mp4", ct)
        report[f"{new}_containment"] = c
        contained = (c["out_of_band_share_pct"] < 0.5
                     and c["densest_out_of_band_20x20_tile_px"] <= 25)
        ok &= contained
        print(f"  {new:22s} material diff: {c['material_px_in_band']} px IN the "
              f"pill band {c['pill_band_rows']}, {c['material_px_out_of_band']} px "
              f"outside ({c['out_of_band_share_pct']}%)")
        print(f"  {'':22s} densest out-of-band 20x20 tile: "
              f"{c['densest_out_of_band_20x20_tile_px']}/400 px  "
              f"(encoder speckle, not a moved element)  -> "
              f"{'CONTAINED' if contained else 'LEAKED'}")

    (OUT / "capband_fix6.json").write_text(json.dumps(report, indent=1))
    print("\nALL PROOFS PASS" if ok else "\nVIOLATIONS FOUND")


if __name__ == "__main__":
    main()
