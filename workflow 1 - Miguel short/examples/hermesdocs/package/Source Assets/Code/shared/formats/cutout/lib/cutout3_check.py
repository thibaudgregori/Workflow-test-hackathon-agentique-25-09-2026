"""CUTOUT FIX ROUND 3 — the two round-3 claims, re-derived from decoded pixels.

Round 1's nine checks and round 2's four surviving checks run unmodified on the
new file (via the same symlink shim round 2 used, so no file belonging to
another task is edited).  This file adds the round-3 measurements, and each one
is a BEFORE/AFTER against the file Miguel and Morgane were actually looking at:

 10  MATTE STABILITY  FLICKER = matte motion without picture motion.  On the
                      quietest 20% of consecutive plate frames, how many pixels
                      each render's own composited alpha changed its mind about
                      (`stage_fix2/v/matte.webm` vs `stage_fix3/v/matte.webm`).
                      Morgane: "the head cutout is not stable".
 11  LAW 12 BAND      the terracotta caption pill's bounding box, swept across
                      the render.  Bottom edge as a % of frame height (the law's
                      hard 72% line), centre as a % (the 40-65% preference), and
                      the number of DISTINCT pill centres, which is Morgane's
                      "caption position stable" turned into an integer.
 12  LAW 12 ZONES     ink in the three danger zones, measured on the render:
                      any ink in the top 10%, CAPTION pixels in the bottom 28%,
                      and caption + stage-zone ink in the right 15% column.
                      See `check_zones` for what is excluded and why.
 13  CAPTION WIDTH    the widest pill's right edge vs the rail line at x=918.

Run:  python cutout3_check.py --r1
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

NEW = HERE / "out/cutout_fix3.mp4"
OLD = HERE / "out/cutout_fix2.mp4"          # what Morgane reviewed
R1 = HERE / "out/cutout_fix.mp4"            # round 1, the discriminating baseline
MATTE_NEW = HERE / "stage_fix3/v/matte.webm"
MATTE_OLD = HERE / "stage_fix2/v/matte.webm"
GEOM = HERE / "_geom_cutout_fix3.json"
GEOM_OLD = HERE / "_geom_cutout_fix2.json"

W, H = 1080, 1920
PLATE_TOP, PLATE_H = 1020, 900
CREAM_BGR = np.array([234, 241, 246])       # #FFFDF9 seen as BGR
TERRA_RGB = (196, 84, 46)                   # the pill fill


def grab(mp4: Path, t: float) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4),
                          "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                         check=True, capture_output=True).stdout
    return cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)


# =========================================================== 10 MATTE STABILITY
def alpha_stream(webm: Path):
    cmd = ["ffmpeg", "-v", "error", "-c:v", "libvpx-vp9", "-i", str(webm),
           "-vf", "alphaextract,format=gray", "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    n = W * PLATE_H
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=n * 4)
    while True:
        buf = proc.stdout.read(n)
        if len(buf) < n:
            break
        yield np.frombuffer(buf, np.uint8).reshape(PLATE_H, W)
    proc.stdout.close()
    proc.wait()


def plate_stillness(plate: Path, n: int = 1354) -> np.ndarray:
    """Mean |luma delta| between consecutive PLATE frames — how much the picture
    itself moved.  Nothing to do with the matte."""
    cmd = ["ffmpeg", "-v", "error", "-i", str(plate), "-vf", "format=gray",
           "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    sz = W * PLATE_H
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=sz * 4)
    prev, out = None, []
    while True:
        buf = proc.stdout.read(sz)
        if len(buf) < sz:
            break
        f = np.frombuffer(buf, np.uint8).reshape(PLATE_H, W).astype(np.int16)
        if prev is not None:
            out.append(float(np.abs(f - prev).mean()))
        prev = f
    proc.stdout.close()
    proc.wait()
    return np.array(out)


def trim_motion(webm: Path, still: np.ndarray) -> dict:
    """FLICKER IS MATTE MOTION WITHOUT PICTURE MOTION.

    The first version of this check measured the XOR between consecutive alphas
    on EVERY frame and reported that round 3 was worse.  It is the same trap
    `_shared/sam2_flicker.py` documents and `SAM2.md` warns about in its own
    verdict: round 2's exclusion rectangle AMPUTATED his raised hand, so on
    every frame he raises it round 2's matte holds a static hole and scores a
    small delta, while round 3 correctly tracks a moving hand and scores a large
    one.  Tracking is not flickering, and a metric that cannot tell them apart
    measures the wrong thing.

    So the metric is the one Morgane's complaint actually implies, and it is
    `sam2_flicker.py`'s, re-run here on the two files that were COMPOSITED into
    the two renders rather than on lab intermediates: take the quietest 20% of
    consecutive PLATE frames, and on exactly those, ask how many pixels the
    matte changed its mind about.  Head band = plate rows 150-560, where no hand
    ever reaches.
    """
    HEAD = slice(150, 560)
    thr = float(np.quantile(still, 0.20))
    keep = np.where(still <= thr)[0]        # index i means the pair (i, i+1)
    keepset = set(int(k) for k in keep)
    prev, tot, head = None, [], []
    for i, a in enumerate(alpha_stream(webm)):
        occ = a > 127
        if prev is not None and (i - 1) in keepset:
            d = occ ^ prev
            tot.append(int(d.sum()))
            head.append(int(d[HEAD].sum()))
        prev = occ
    t, hd = np.array(tot, float), np.array(head, float)
    return {"still_frames": len(t), "motion_threshold_luma": round(thr, 4),
            "xor_mean": round(float(t.mean()), 1),
            "xor_p95": int(np.percentile(t, 95)), "xor_max": int(t.max()),
            "head_xor_mean": round(float(hd.mean()), 1),
            "head_xor_p95": int(np.percentile(hd, 95)),
            "head_xor_max": int(hd.max())}


def check_matte(fails: list[str]) -> dict:
    plate = HERE.parent / "_shared/face_wide_25.mp4"
    if not plate.exists():
        raise SystemExit(f"missing plate {plate}")
    still = plate_stillness(plate)
    old, new = trim_motion(MATTE_OLD, still), trim_motion(MATTE_NEW, still)
    print(f"10 MATTE      flicker = matte motion WITHOUT picture motion, "
          f"on the quietest 20% of frames ({new['still_frames']} pairs, "
          f"luma delta <= {new['motion_threshold_luma']})")
    for k in ("xor_mean", "xor_p95", "xor_max",
              "head_xor_mean", "head_xor_p95", "head_xor_max"):
        print(f"              {k:>14}  round2 {old[k]:>9,}   ->  round3 {new[k]:>9,}   "
              f"{100 * (new[k] / max(1e-9, old[k]) - 1):+6.1f}%")
    if new["head_xor_max"] >= old["head_xor_max"]:
        fails.append(f"worst-case head-band edge jump on still frames did not "
                     f"improve ({old['head_xor_max']} -> {new['head_xor_max']})")
    if new["xor_max"] >= old["xor_max"]:
        fails.append(f"worst-case whole-plate edge jump on still frames did not "
                     f"improve ({old['xor_max']} -> {new['xor_max']})")
    if new["head_xor_mean"] >= old["head_xor_mean"] * 1.20:
        fails.append("mean head-band edge motion got materially worse")
    return {"round2": old, "round3": new}


# ============================================================== 11 LAW 12 BAND
def terra(bgr: np.ndarray) -> np.ndarray:
    """Solid terracotta, tight enough to exclude skin.

    SKIN passes a naive terra test: a cheek reads about (200,160,130), which
    clears `r - b > 60`.  The separating channel is r - g — terra #C4542E has
    r - g = 112, skin has ~40 — and the first version of this detector, which
    did not use it, reported the pill "at 100% of frame height" because it had
    found his face.  The thresholds are also deliberately tight on the core so
    the bbox is the PILL, not the pill plus its antialiased fringe.
    """
    b, g, r = (bgr[:, :, 0].astype(int), bgr[:, :, 1].astype(int),
               bgr[:, :, 2].astype(int))
    return (r - b > 90) & (r - g > 70) & (r > 150)


def pill_component(bgr: np.ndarray, meters: dict) -> np.ndarray | None:
    """The caption pill as a MASK, or None if no pill is up.

    Two other families of terra exist in this composition and both had to be
    handled by construction rather than by a threshold:

      * METER FILLS are terra, wide, and flat — `b1-met` is 756px across, wider
        than most pills, so an area ranking picks it over the caption and the
        sweep reports the wrong y.  Their track rectangles are published in the
        geometry file, so they are erased from the mask by coordinate, per build.
      * LOGO MARKS in the depth lanes are red and orange (YouTube, Zapier, Gmail)
        and land in the bottom 28% by design.  A raw colour count therefore
        reported ~2,100px of "caption" per frame down there.  Taking the pill's
        own CONNECTED COMPONENT instead of the colour makes the question the
        right one: not "is anything terra low in the frame" but "is the CAPTION
        low in the frame".
    """
    m = terra(bgr).astype(np.uint8)
    for g in meters.values():
        x, y = int(g["x"]) - 6, int(g["y"]) - 6
        m[max(0, y):int(y + g["h"]) + 12, max(0, x):int(x + g["w"]) + 12] = 0
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    ncc, lab, st, _c = cv2.connectedComponentsWithStats(m, 8)
    best = None
    for i in range(1, ncc):
        x, y, w, h, area = st[i]
        if w < 150 or h < 40 or w <= h or area < 0.45 * w * h:
            continue
        if best is None or area > st[best][4]:
            best = i
    return (lab == best) if best is not None else None


def pill_box(bgr: np.ndarray, meters: dict):
    m = pill_component(bgr, meters)
    if m is None:
        return None
    ys, xs = np.where(m)
    return int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), \
        int(ys.max() - ys.min() + 1)


def sweep_pill(mp4: Path, meters: dict, n: int = 90, dur: float = 54.16) -> dict:
    tops, bots, cxs, rights, lefts, seen = [], [], [], [], [], 0
    for i in range(n):
        t = round((i + 0.5) * dur / n, 2)
        box = pill_box(grab(mp4, t), meters)
        if not box:
            continue
        x, y, w, h = box
        seen += 1
        tops.append(y)
        bots.append(y + h)
        cxs.append(round(y + h / 2))
        lefts.append(x)
        rights.append(x + w)
    return {"samples": n, "pills_seen": seen,
            "top_min": int(min(tops)), "bottom_max": int(max(bots)),
            "bottom_frac": round(max(bots) / H, 4),
            "centre_min": int(min(cxs)), "centre_max": int(max(cxs)),
            "centre_frac": round(float(np.median(cxs)) / H, 4),
            "distinct_centres_5px": len({c // 5 for c in cxs}),
            "left_min": int(min(lefts)), "right_max": int(max(rights))}


def check_band(geom: dict, geom_old: dict, fails: list[str]) -> dict:
    old = sweep_pill(OLD, geom_old["meters"])
    new = sweep_pill(NEW, geom["meters"])
    print(f"11 LAW 12     caption pill swept over {new['samples']} frames "
          f"({new['pills_seen']} carried a pill)")
    print(f"              bottom edge   round2 {old['bottom_max']:>5}px "
          f"({old['bottom_frac']:.1%})  ->  round3 {new['bottom_max']:>5}px "
          f"({new['bottom_frac']:.1%})   limit 1382px (72.0%)")
    print(f"              centre        round2 {old['centre_frac']:.1%}"
          f"  ->  round3 {new['centre_frac']:.1%}   preferred band 40-65%")
    print(f"              stability     centre spread round2 "
          f"{old['centre_max'] - old['centre_min']}px  ->  round3 "
          f"{new['centre_max'] - new['centre_min']}px")
    if new["bottom_max"] > 1382:
        fails.append(f"caption bottom {new['bottom_max']}px "
                     f"({new['bottom_frac']:.1%}) is below the 72% line")
    if not 0.40 <= new["centre_frac"] <= 0.65:
        fails.append(f"caption centre {new['centre_frac']:.1%} outside the "
                     f"preferred 40-65% band")
    if new["centre_max"] - new["centre_min"] > 8:
        fails.append(f"caption position is not stable: centres span "
                     f"{new['centre_max'] - new['centre_min']}px")
    if old["bottom_max"] <= 1382:
        fails.append("round 2's pill was already inside the band — the "
                     "measurement is not discriminating")
    return {"round2": old, "round3": new, "limit_px": 1382}


# ============================================================= 12 LAW 12 ZONES
def check_zones(geom: dict, geom_old: dict, fails: list[str]) -> dict:
    """The three danger zones, measured on the render.

      top 10%       ALL non-cream ink.  Nothing of ours is up there in either
                    build, and nothing of his is either — his union top is 1110.
      bottom 28%    CAPTION PILL pixels.  His body is in the bottom 28% of every
                    short this factory has published and the depth lanes are
                    texture; the pill is the thing Morgane could not read.
      right column  CAPTION PILL pixels (asserted 0) plus, reported separately,
                    all stage-zone ink there — which is dominated by the shelf
                    tile field, deliberately left at 912px wide (NOTES §3).
    """
    times = [1.6, 4.0, 8.4, 12.6, 18.0, 24.0, 30.0, 33.0, 38.0, 44.0, 48.0, 52.0]
    out = {}
    for name, mp4, g in (("round2", OLD, geom_old), ("round3", NEW, geom)):
        top = bot = rail_pill = rail_stage = 0
        for t in times:
            bgr = grab(mp4, t)
            dev = np.abs(bgr.astype(int) - CREAM_BGR).max(axis=2) > 26
            pill = pill_component(bgr, g["meters"])
            top += int(dev[:192].sum())
            if pill is not None:
                bot += int(pill[1382:].sum())
                rail_pill += int(pill[:, 918:].sum())
            rail_stage += int(dev[192:940, 918:].sum())
        out[name] = {"top10_px": top, "bottom28_pill_px": bot,
                     "rail_pill_px": rail_pill, "rail_stage_ink_px": rail_stage,
                     "frames": len(times)}
    print(f"12 LAW 12     ink inside the danger zones, summed over "
          f"{len(times)} frames")
    for zone, label in (("top10_px", "top 10% (any ink)"),
                        ("bottom28_pill_px", "bottom 28% (pill)"),
                        ("rail_pill_px", "right col (pill)"),
                        ("rail_stage_ink_px", "right col (stage texture)")):
        print(f"              {label:<26} round2 {out['round2'][zone]:>8,}  ->  "
              f"round3 {out['round3'][zone]:>8,}")
    if out["round3"]["top10_px"] > 200:
        fails.append(f"ink in the top 10% ({out['round3']['top10_px']}px)")
    if out["round3"]["bottom28_pill_px"] > 0:
        fails.append(f"caption pixels in the bottom 28% "
                     f"({out['round3']['bottom28_pill_px']}px)")
    if out["round3"]["rail_pill_px"] > 0:
        fails.append(f"caption pixels in the right rail column "
                     f"({out['round3']['rail_pill_px']}px)")
    if out["round2"]["bottom28_pill_px"] <= 200:
        fails.append("round 2 had no caption in the bottom 28% either — the "
                     "measurement is not discriminating")
    return out


# ============================================================ 13 CAPTION WIDTH
def check_width(geom: dict, fails: list[str], band: dict) -> dict:
    g = geom["caption_width"]
    measured_right = band["round3"]["right_max"]
    old_right = band["round2"]["right_max"]
    print(f"13 PILL WIDTH declared widest {g['widest_px']:.0f}px -> x"
          f"{g['pill_x'][1]:.0f};  MEASURED widest right edge  round2 "
          f"x{old_right}  ->  round3 x{measured_right}   (rail line x918)")
    # 918 is the rail line; the measured bbox carries up to ~3px of antialiased
    # fringe that the declared geometry does not, so the assertion is the rail
    # line plus that fringe, stated rather than absorbed.
    if measured_right > 921:
        fails.append(f"a caption pill reaches x={measured_right}, "
                     f"{measured_right - 918}px into the right rail")
    if old_right <= 921:
        fails.append("round 2's pills already cleared the rail — the "
                     "measurement is not discriminating")
    return {"declared": g, "measured_right_round2": old_right,
            "measured_right_round3": measured_right}


# ================================================================== inherited
def run_inherited() -> None:
    """Round 1's checks 1..9 and round 2's checks 11..14, unmodified.

    Same shim trick round 2 used: a directory of symlinks so `cutout_fix_check`
    and `cutout2_check` resolve their own `HERE` onto this build's render and
    geometry without either file being edited.  The BEFORE side of round 2's
    before/after pairs stays round 1's render, which is the file those checks
    were built to discriminate against.
    """
    import cutout_fix_check as R1M
    import cutout2_check as R2M
    shim = HERE / "cutout3/shim"
    (shim / "frames").mkdir(parents=True, exist_ok=True)
    for link, target in (("out", HERE / "out"), ("_geom_cutout_fix.json", GEOM)):
        p = shim / link
        if p.is_symlink() or p.exists():
            p.unlink()
        p.symlink_to(target)
    R1M.HERE = shim
    R1M.MATTE = MATTE_NEW
    print("=== round-1 checks 1..9, re-run on cutout_fix3 ===")
    R1M.main("cutout_fix3")
    print()

    print("=== round-2 checks 11..14, re-run on cutout_fix3 ===")
    R2M.NEW, R2M.OLD, R2M.GEOM = NEW, R1, GEOM
    geom = json.loads(GEOM.read_text())
    geom_old = json.loads((HERE / "_geom_cutout_fix.json").read_text())
    fails: list[str] = []
    rep = {"blanks": R2M.check_blanks(fails),
           "label_block": R2M.check_label_block(geom, fails),
           "edge_fade": R2M.check_edge_fade(geom, geom_old, fails),
           "law11": R2M.check_law11(geom, geom_old, fails)}
    if fails:
        for f in fails:
            print("  - INHERITED FAIL:", f)
        raise SystemExit(1)
    print()
    return rep


def main() -> None:
    for p in (NEW, OLD, R1, MATTE_NEW, MATTE_OLD, GEOM, GEOM_OLD):
        if not p.exists():
            raise SystemExit(f"missing: {p}")
    inherited = run_inherited() if "--r1" in sys.argv else None
    geom = json.loads(GEOM.read_text())
    fails: list[str] = []
    geom_old = json.loads(GEOM_OLD.read_text())
    band = check_band(geom, geom_old, fails)
    rep = {"matte": check_matte(fails),
           "law12_band": band,
           "law12_zones": check_zones(geom, geom_old, fails),
           "caption_width": check_width(geom, fails, band),
           "inherited": inherited}
    (HERE / "cutout3/round3_checks.json").parent.mkdir(parents=True, exist_ok=True)
    (HERE / "cutout3/round3_checks.json").write_text(json.dumps(rep, indent=1))
    if fails:
        print("\nFAIL:")
        for f in fails:
            print("  -", f)
        raise SystemExit(1)
    print("\nROUND-3 CHECKS PASS")


if __name__ == "__main__":
    main()
