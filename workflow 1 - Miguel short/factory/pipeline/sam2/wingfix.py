#!/usr/bin/env python
"""wingfix.py — THE MANUAL HEAL FOR A HEADREST WING, beside the head.

`bolsterfix.py`'s sibling, and the reason it needed one (codexnondev, run 9,
2026-09-02).

WHAT BOLSTERFIX CANNOT DO.  `bolsterfix` heals furniture that stands ABOVE THE
SHOULDER LINE: it fits a quadratic through the anchor columns either side of the
gap and removes plate-dark pixels between the current silhouette top and that
line.  Everything about it — the sweep's segments, `protrusion.scan()`'s
windows, `heal_frame`'s anchors, the depth cap read off `lift_max` — is stated
in terms of a top-y profile measured against a shoulder.

`codexnondev` shipped a defect that has no shoulder under it.  The chair's
image-RIGHT headrest WING stands BESIDE HIS HEAD, from y ~195 (just under the
cap) down to y ~478 where his own shoulder starts: 60 columns wide, ~280 rows
tall, plate luma 2-25, welded to his jaw by a black-on-black strip.  There is no
"line" it rises above.  Its left neighbours are his HEAD, which is HIGHER than
it, so a local re-fit reads NEGATIVE lift; its right neighbours are background,
which is not measurable at all.  Every instrument in the shoulder lane is
looking at the wrong axis.

    the shipped alpha, top-y per column at t = 20 s
        x  860   870   880   890   900   910   920   930   940   950
        y   71    80    91   115   202   216   248   313   504   508
                                   \\______ the wing ______/  \\_ him _/

WHAT THIS FILE DOES INSTEAD.  It re-uses `prompt0.cmd_cut`'s rule — the one the
factory already trusts to take the wings out of a frame-0 prompt — and applies
it to EVERY corrective keyframe of an already-tracked alpha:

    inside the wing ROWS, at or beyond the wing's measured inner COLUMN,
    any mask pixel darker than DARK is furniture

  * dark-only (`--dark`, default 60, well under `heal_frame`'s luma guard of
    70), so an ear, a jaw or a hand can never be removed — his ear reads 100-105
    where the wing beside it reads 16-18
  * column-bounded, so the black t-shirt to the LEFT of the wing is untouched
  * row-bounded ABOVE by the cap (the cap is black and it is his) and BELOW by
    the row where his own shoulder arrives, so the shoulder is never carved
  * subtractive only, keep-largest then CLOSE then re-subtract, exactly as
    `heal_frame` and `prompt0` finish

and then writes them as prompt masks for one re-propagation, which is the same
second half `bolsterfix` performs.  Frame 0 is included, so the memory bank is
seeded with a chair-free silhouette instead of being corrected after the fact.

MEASURING THE BAND, because the numbers are not free.  `--measure` prints, per
column, the rows the plate is dark in EVERY sampled frame (furniture never
moves) against the rows the current mask claims, so the inner column and the two
row bounds are read off the plate rather than guessed.  On `codexnondev`:

    x 885-935 dark from y 192-204 in every frame        <- the wing
    x 943+    mask top-y 505, rising 0.6 px/col to the right   <- his shoulder
    -> --wing-right 886 --rows 195,478

VERIFY BEFORE YOU SPEND.  `--dry` renders the proposed cut over the plate at N
sampled frames and writes a strip: red is what would go, green is the silhouette
that would remain.  Look at it.  A wing cut is cheap to get wrong in a way no
scalar reports, because the pixels it must not take are the same colour as the
ones it must.

    # 1. look
    $V wingfix.py --session sessions/codexnondev \
                  --alpha sessions/codexnondev/alpha_v2.mkv \
                  --plate sessions/codexnondev/plate_wide_25.mp4 --measure
    # 2. propose, and look again
    $V wingfix.py ... --wing-right 886 --rows 195,478 --dry /tmp/wing.png
    # 3. write the corrective keyframes
    $V wingfix.py ... --wing-right 886 --rows 195,478 \
                  --out sessions/codexnondev/prompts_v3
    # 4. re-propagate on the deployed app  (~$0.17, ~7 min)
    $V track.py --session sessions/codexnondev \
                --plate sessions/codexnondev/plate_wide_25.mp4 \
                --prompts sessions/codexnondev/prompts_v3 --tag v3
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def read_indices(path: Path, w: int, h: int, wants: set[int]):
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path),
                        "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                       capture_output=True)
    n = len(r.stdout) // (w * h)
    a = np.frombuffer(r.stdout, np.uint8)[:n * w * h].reshape(n, h, w)
    return {g: a[g] for g in sorted(wants) if g < n}, n


def cut_wing(mask: np.ndarray, luma: np.ndarray, *, x0: int, x1: int,
             r0: int, r1: int, dark: int, side: str = "right"):
    """The rule, once.  Returns (healed_mask, cut_mask)."""
    import cv2
    cut = np.zeros_like(mask)
    sl = (slice(r0, r1), slice(x0, x1 + 1))
    cut[sl] = mask[sl] & (luma[sl] <= dark)
    out = mask & ~cut
    n, lab, st, _ = cv2.connectedComponentsWithStats(out.astype(np.uint8), 8)
    if n > 1:
        k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        out = lab == k
    out = cv2.morphologyEx(out.astype(np.uint8), cv2.MORPH_CLOSE,
                           np.ones((5, 5), np.uint8)).astype(bool)
    out &= ~cut          # CLOSE can bridge the strip back shut
    return out, cut


def main() -> None:
    import cv2

    ap = argparse.ArgumentParser()
    ap.add_argument("--session", required=True)
    ap.add_argument("--alpha", required=True)
    ap.add_argument("--plate", required=True)
    ap.add_argument("--out", default=None, help="prompt dir to write")
    ap.add_argument("--wing-right", type=int, default=None,
                    help="INNER column of the image-right wing")
    ap.add_argument("--wing-left", type=int, default=None,
                    help="OUTER column of the image-left wing")
    ap.add_argument("--rows", default=None, help="r0,r1 for the right wing")
    ap.add_argument("--rows-left", default=None, help="r0,r1 for the left wing")
    ap.add_argument("--dark", type=int, default=60)
    ap.add_argument("--chunk", type=int, default=350)
    ap.add_argument("--stride", type=int, default=46)
    ap.add_argument("--measure", action="store_true")
    ap.add_argument("--dry", default=None, help="write a proof strip here")
    a = ap.parse_args()

    ma = _load("modal_app")
    prot = _load("protrusion")
    alpha_p, plate_p = Path(a.alpha), Path(a.plate)
    W, H = prot.probe_wh(alpha_p)
    if prot.probe_wh(plate_p) != (W, H):
        raise SystemExit("plate and alpha differ in size")

    if a.measure:
        L = prot.read_gray(plate_p, W, H, a.stride)
        A = prot.read_gray(alpha_p, W, H, a.stride)
        stable = (L < a.dark).all(0)
        m = A > 127
        print(f"{len(L)} frames sampled (stride {a.stride})\n"
              f"{'x':>6} {'always-dark rows':>22} {'mask top-y (median)':>21}")
        for x in range(0, W, 10):
            col = np.flatnonzero(stable[:, x])
            tops = [np.flatnonzero(f[:, x])[0] if f[:, x].any() else np.nan
                    for f in m]
            t = np.nanmedian(tops) if np.any(~np.isnan(tops)) else float("nan")
            if col.size:
                print(f"{x:>6} {f'{col.min()}..{col.max()} ({col.size})':>22} "
                      f"{t:>21.0f}")
        return

    wins = []
    if a.wing_right is not None:
        r0, r1 = (int(v) for v in (a.rows or "195,478").split(","))
        wins.append(("right", a.wing_right, W - 1, r0, r1))
    if a.wing_left is not None:
        r0, r1 = (int(v) for v in (a.rows_left or "195,478").split(","))
        wins.append(("left", 0, a.wing_left, r0, r1))
    if not wins:
        raise SystemExit("nothing to cut: pass --wing-right and/or --wing-left")
    print("WINDOWS: " + ", ".join(f"{s} x{x0}-{x1} rows {r0}-{r1}"
                                  for s, x0, x1, r0, r1 in wins))

    n_all = int(round(float(subprocess.run(
        ["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
         "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0",
         str(alpha_p)], capture_output=True, text=True).stdout.strip())))

    if a.dry:
        from PIL import Image
        want = sorted({int(round(i * (n_all - 1) / 5)) for i in range(6)})
        A_n, _ = read_indices(alpha_p, W, H, set(want))
        L_n, _ = read_indices(plate_p, W, H, set(want))
        tiles = []
        for g in want:
            m, lum = A_n[g] > 127, L_n[g]
            out = m.copy()
            cut = np.zeros_like(m)
            for _s, x0, x1, r0, r1 in wins:
                out, c = cut_wing(out, lum, x0=x0, x1=x1, r0=r0, r1=r1,
                                  dark=a.dark)
                cut |= c
            im = np.dstack([lum] * 3).astype(np.uint8)
            im[cut] = [255, 40, 40]
            e = out ^ np.roll(out, 1, 1)
            im[e] = [0, 255, 60]
            x0 = max(0, min(w[1] for w in wins) - 100)
            x1 = min(W, max(w[2] for w in wins if w[2] < W - 1) + 100) \
                if any(w[2] < W - 1 for w in wins) else min(W, x0 + 320)
            tiles.append(im[max(0, min(w[3] for w in wins) - 80):
                            min(H, max(w[4] for w in wins) + 160), x0:x1])
            print(f"  f{g}  cut {int(cut.sum())} px  "
                  f"max luma {int(lum[cut].max()) if cut.any() else -1}")
        Image.fromarray(np.concatenate(tiles, 1)).save(a.dry)
        print(f"-> {a.dry}")
        return

    if not a.out:
        raise SystemExit("--out is required to write corrective keyframes")

    kf = ma.heal_keyframes(n_all, a.chunk, ma.LEAK)
    print(f"{n_all} frames, {len(kf)} corrective keyframes")
    A_need, _ = read_indices(alpha_p, W, H, set(kf))
    L_need, _ = read_indices(plate_p, W, H, set(kf))

    out_d = Path(a.out)
    if out_d.exists():
        shutil.rmtree(out_d)
    out_d.mkdir(parents=True)

    cuts, lmax, areas = [], -1, []
    for g in kf:
        m0 = A_need.get(g)
        if m0 is None:
            continue
        m, lum = m0 > 127, L_need[g]
        before = int(m.sum())
        out = m.copy()
        cut = np.zeros_like(m)
        for _s, x0, x1, r0, r1 in wins:
            out, c = cut_wing(out, lum, x0=x0, x1=x1, r0=r0, r1=r1,
                              dark=a.dark)
            cut |= c
        cv2.imwrite(str(out_d / f"kf_{g:05d}.png"),
                    (out * 255).astype(np.uint8))
        cuts.append(int(cut.sum()))
        areas.append((before, int(out.sum())))
        if cut.any():
            lmax = max(lmax, int(lum[cut].max()))

    frac = [1 - b / a_ for a_, b in areas]
    print(f"CUT n={len(cuts)} min={min(cuts)} max={max(cuts)} "
          f"median={int(np.median(cuts))}  |  max luma of any removed pixel "
          f"{lmax} (guard {a.dark})  |  silhouette lost "
          f"{100*min(frac):.2f}-{100*max(frac):.2f} %")
    if lmax > a.dark:
        raise SystemExit("DARK GUARD BREACHED — refusing to write this heal")
    if np.median(cuts) < ma.LEAK["min_cut_px"]:
        raise SystemExit("the heal had nothing removable to cut")

    rep = dict(session=str(a.session), alpha=str(alpha_p), plate=str(plate_p),
               rule="prompt0 wing cut, applied to every corrective keyframe",
               dark=a.dark, windows=[dict(side=s, x0=x0, x1=x1, r0=r0, r1=r1)
                                     for s, x0, x1, r0, r1 in wins],
               frames=n_all, keyframes=kf,
               cut_px=dict(n=len(cuts), min=int(min(cuts)), max=int(max(cuts)),
                           median=int(np.median(cuts))),
               max_luma_of_cut=int(lmax),
               silhouette_lost_pct=[round(100 * min(frac), 3),
                                    round(100 * max(frac), 3)])
    (out_d / "wingfix.json").write_text(json.dumps(rep, indent=1))
    print(f"\n{len(cuts)} prompt masks -> {out_d}")
    print(f"next: track.py --prompts {out_d} --tag v3")


if __name__ == "__main__":
    main()
