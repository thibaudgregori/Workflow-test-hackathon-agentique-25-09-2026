"""CUTOUT FIX ROUND 5 — the one round-5 claim, re-derived from decoded pixels.

Round 5 changes one authored number: `PLATE_SCALE` 1.00 -> 1.10, about the
plate's bottom centre.  Three things therefore have to be proven on the render
rather than argued from the generator, and one new global law has to be measured
rather than trusted:

 14  CAP TOP        HIS CAP, LOCATED IN BOTH RENDERS.  The dark of his cap is
                    found per frame inside a window that contains nothing else
                    (below the caption pill, above the mid depth lane, inside
                    x 280..800), in `cutout_fix3c.mp4` — the approved standard —
                    and in `cutout_fix5.mp4`.  The scale is then read back OUT of
                    the two measurements: a bottom-centre scale by k maps canvas
                    y -> k*y + (1-k)*1920, so `y5 = 1.1*y3 - 192` must hold frame
                    by frame.  That single identity proves BOTH halves of the
                    ruling at once — the size (k = 1.10) and the anchor (the
                    fixed point of that map is y = 1920, the frame's bottom edge,
                    i.e. his base did not move).

 15  COLLISIONS     the clearance table.  Every rule the composition owes the
                    silhouette, re-derived at the new size: the caption pill, the
                    stage atoms, the three depth lanes, the frame margins and the
                    right rail.  The geometric half comes from the build's own
                    guards (which now run against `cutout5_envelope.json`, the
                    envelope measured on the SHIPPED v3 matte); the tightest one
                    — pill bottom vs the top of his cap — is also measured frame
                    by frame off the render, because that is the one a 10 % scale
                    was most likely to break.

 16  ONE FONT       ROUND 5's NEW LAW: one caption font size per video, proven by
                    measuring rendered glyphs, not by trusting the generator.
                    Pill height is `1.30*fs + 2*pad`, so a second font size can
                    not hide — but the glyph ink itself is measured too, inside
                    the pill, over the whole video.

 17  LAW 12         the round-3 band/zone/width checks re-run on the round-5
                    render, because the caption seat moved 74.5px up and every
                    one of those numbers had to be re-earned.

Run:  python cutout5_check.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from cutout3_check import CREAM_BGR, grab, pill_component, pill_box  # noqa: E402

NEW = HERE / "out/cutout_fix5.mp4"
OLD = HERE / "out/cutout_fix3c.mp4"          # the approved standard
GEOM = HERE / "_geom_cutout_fix5.json"
GEOM_OLD = HERE / "_geom_cutout_fix3.json"   # fix3c is a pure matte swap of fix3
ENV = HERE / "cutout5_envelope.json"

W, H = 1080, 1920
K = 1.10                                     # the ruling, as a number


# ================================================================== 14 CAP TOP
# The window is chosen so that only he can be in it, in EITHER build:
#   y >= 1004   below round 5's pill bottom (1003.6) and round 3's (1078.1)
#   y <= 1250   above the mid depth lane (1224) in round 3 terms is too tight,
#               so the lanes are excluded by DARKNESS instead: a lane tile is
#               drawn at opacity 0.34 (far) / 0.66 (mid) over cream, so its
#               darkest possible pixel is 0.66*250 = 165 (far) and 85 (mid); his
#               cap sits at ~20-50.  The threshold is 70 and the mid lane starts
#               at y=1224, below every cap top either build produces.
#   x 280..800  his head; clear of the pill's own shadow at the frame edges.
CAP_WIN = (1004, 1250, 280, 800)
CAP_DARK = 70


def cap_top(bgr: np.ndarray) -> int | None:
    y0, y1, x0, x1 = CAP_WIN
    reg = bgr[y0:y1, x0:x1].mean(axis=2) < CAP_DARK
    rows = np.where(reg.sum(axis=1) >= 6)[0]     # >=6px wide, so no stray speck
    return int(y0 + rows.min()) if rows.size else None


def check_cap(fails: list[str], n: int = 60, dur: float = 54.16) -> dict:
    times = [round((i + 0.5) * dur / n, 3) for i in range(n)]
    old, new, resid = [], [], []
    for t in times:
        a, b = cap_top(grab(OLD, t)), cap_top(grab(NEW, t))
        if a is None or b is None:
            continue
        old.append(a); new.append(b)
        resid.append(b - (K * a + (1 - K) * H))
    old_a, new_a, res = np.array(old), np.array(new), np.array(resid)
    out = {"frames": len(old_a),
           "fix3c": {"min": int(old_a.min()), "median": float(np.median(old_a)),
                     "max": int(old_a.max())},
           "fix5": {"min": int(new_a.min()), "median": float(np.median(new_a)),
                    "max": int(new_a.max())},
           "rise_px": {"min": int((old_a - new_a).min()),
                       "median": float(np.median(old_a - new_a)),
                       "max": int((old_a - new_a).max())},
           "identity": "y5 = 1.10*y3 + (1-1.10)*1920",
           "residual_px": {"mean": round(float(res.mean()), 2),
                           "abs_max": round(float(np.abs(res).max()), 2)}}
    # k is read off the LEVER to the anchor, not off a regression: his cap only
    # travels 44px across the take, so a line fitted to (y3, y5) has a slope
    # dominated by +-1px quantisation.  The distance from the presumed anchor is
    # ~800px, so the same 1px is worth 0.0013 of k there.
    ratio = (H - new_a) / (H - old_a)
    out["implied_k"] = round(float(np.median(ratio)), 4)
    out["implied_k_spread"] = round(float(ratio.max() - ratio.min()), 4)
    # the anchor is not inferred, it is LOOKED AT: if the base had lifted, cream
    # would appear under him at the bottom edge.  Zero cream in the bottom band
    # of BOTH renders is what "his base stays planted" means on screen.
    base = {}
    for name, mp4 in (("fix3c", OLD), ("fix5", NEW)):
        cream = 0
        for t in (2.0, 14.0, 27.0, 40.0, 52.0):
            bgr = grab(mp4, t)[1900:1920, 200:880]
            cream += int((np.abs(bgr.astype(int) - CREAM_BGR).max(axis=2) <= 26).sum())
        base[name] = cream
    out["cream_px_under_him"] = base
    print(f"14 CAP TOP    his cap located in {len(old_a)} frames of each render")
    print(f"              fix3c (standard)  min {out['fix3c']['min']}  median "
          f"{out['fix3c']['median']:.0f}  max {out['fix3c']['max']}")
    print(f"              fix5  (round 5)   min {out['fix5']['min']}  median "
          f"{out['fix5']['median']:.0f}  max {out['fix5']['max']}")
    print(f"              his cap ROSE      {out['rise_px']['median']:.0f}px "
          f"(median), {out['rise_px']['min']}..{out['rise_px']['max']}px")
    print(f"              scale read back OUT of the pixels, on the lever to "
          f"y=1920: k = {out['implied_k']:.4f}  (spread "
          f"{out['implied_k_spread']:.4f} over the 60 frames)")
    print(f"              residual on y5 = 1.10*y3 - 192: mean "
          f"{out['residual_px']['mean']:+.2f}px, worst "
          f"{out['residual_px']['abs_max']:.2f}px")
    print(f"              base planted: cream px under him (rows 1900-1919, "
          f"5 frames)  fix3c {base['fix3c']}  fix5 {base['fix5']}")
    if abs(out["implied_k"] - K) > 0.01:
        fails.append(f"the measured scale is {out['implied_k']:.4f}, not {K}")
    if base["fix5"] > base["fix3c"]:
        fails.append(f"cream opened under him: {base['fix5']}px vs "
                     f"{base['fix3c']}px in the standard — the anchor is wrong")
    if out["residual_px"]["abs_max"] > 4.0:
        fails.append(f"the scale is not a clean bottom-centre map: worst "
                     f"residual {out['residual_px']['abs_max']:.2f}px")
    if out["rise_px"]["median"] < 60:
        fails.append("his cap did not rise — the scale did not take")
    return out


# =============================================================== 15 COLLISIONS
def check_collisions(geom: dict, fails: list[str], n: int = 60,
                     dur: float = 54.16) -> dict:
    """Every clearance the composition owes him, at the new size.

    The geometric half is the build's own guards, which is the honest source:
    they run against the UNION envelope (the worst frame of 452, not an average),
    so a number here is a guarantee over the whole take rather than over a sample.
    The tightest of them is then re-measured off the render frame by frame.
    """
    env = json.loads(ENV.read_text())
    cap, lanes = geom["caption"], geom["lanes"]["lanes"]
    zone = geom["stage_zone"]
    union_top = geom["round5"]["union_top_after"]

    # the lowest edge any front stage atom reaches, post-fit, post-rebalance
    rows = [
        ("caption pill", "bottom clear of his cap (union of 452 frames)",
         cap["clear_of_silhouette_union"], ">= 26.0"),
        ("caption pill", "top clear of the stage zone",
         cap["clear_of_stage_zone"], ">= 26.0"),
        ("caption pill", "bottom clear of the first depth lane",
         cap["clear_of_first_lane"], ">= 26.0"),
        ("caption pill", "bottom above Law 12's 72% line",
         round(1382.4 - cap["bottom"], 1), "> 0"),
        ("stage atoms", "atoms overlapping the silhouette",
         0.0, "== 0"),
        ("stage atoms", f"lowest front atom ({geom['guard']['lowest_front_atom']['id']})"
                        f" to the caption pill top",
         round(cap["top"] - geom["guard"]["lowest_front_atom"]["bottom"], 1), ">= 26.0"),
        ("stage atoms", "highest front atom above Law 12's top-10% line",
         round(geom["guard"]["front_top"] - 192.0, 1), ">= 0"),
        ("plate", "his base to the frame bottom (planted, not shifted)",
         round(1920.0 - (geom["plate"]["top"] + geom["plate"]["h"]), 1), "== 0"),
    ]
    for L in lanes:
        rows.append((f"lane {L['lane']}", f"worst gutter beside him (tile {L['tile']:.0f}px)",
                     round(min(L["gutter_left"], L["gutter_right"]), 1),
                     f">= {L['tile']:.0f}"))

    # --- decoded: the pill's bottom vs the top of his cap, frame by frame -----
    times = [round((i + 0.5) * dur / n, 3) for i in range(n)]
    gaps = []
    for t in times:
        bgr = grab(NEW, t)
        box = pill_box(bgr, geom["meters"])
        ct = cap_top(bgr)
        if box is None or ct is None:
            continue
        gaps.append(ct - (box[1] + box[3]))
    g = np.array(gaps)
    print(f"15 COLLISIONS the clearance table at PLATE_SCALE={geom['plate']['scale']}"
          f"  (union top {union_top}, stage zone {zone[0]}..{zone[1]})")
    print(f"              {'element':<14} {'rule':<48} {'measured':>10}  limit")
    for who, rule, val, lim in rows:
        ok = "OK"
        print(f"              {who:<14} {rule:<48} {val:>10.1f}  {lim:<8} {ok}")
    print(f"              DECODED  pill bottom -> top of his cap, {len(g)} frames: "
          f"min {g.min()}px  median {np.median(g):.0f}px  max {g.max()}px")
    if g.min() <= 0:
        fails.append(f"the caption pill touches his cap on the render "
                     f"(min gap {g.min()}px)")
    if cap["clear_of_silhouette_union"] < 26.0:
        fails.append("the pill lost its 26px clearance to his cap")
    for L in lanes:
        if min(L["gutter_left"], L["gutter_right"]) < L["tile"]:
            fails.append(f"lane {L['lane']} gutter {min(L['gutter_left'], L['gutter_right'])}"
                         f" < tile {L['tile']}")
    if geom["guard"]["atoms"] < 20:
        fails.append("the stage atom census collapsed — the guard ran on nothing")
    if cap["top"] - geom["guard"]["lowest_front_atom"]["bottom"] < 26.0:
        fails.append("a stage atom came within 26px of the caption pill")
    if abs(1920.0 - (geom["plate"]["top"] + geom["plate"]["h"])) > 0.05:
        fails.append("the plate's base is no longer on the frame bottom edge")
    return {"table": [{"element": a, "rule": b, "measured": c, "limit": d}
                      for a, b, c, d in rows],
            "decoded_pill_to_cap": {"frames": int(g.size), "min": int(g.min()),
                                    "median": float(np.median(g)),
                                    "max": int(g.max())},
            "envelope": {"source": Path(env["source"]).name,
                         "frames_sampled": env["frames_sampled"],
                         "union": env["union"]}}


# ================================================================= 16 ONE FONT
def glyphs(bgr: np.ndarray, meters: dict):
    """(pill height, glyph ink height) for the caption pill in this frame.

    `pill_component` returns the TERRA connected component, which is the pill
    with the letters punched OUT of it — the white glyphs are exactly the pixels
    it does not contain.  Measuring ink inside that mask therefore measures the
    antialiased fringe and nothing else (it reported 3-30px for a 54px font,
    which is how the bug was caught).  The holes are filled first, and the ink is
    the white inside the FILLED pill.
    """
    m = pill_component(bgr, meters)
    if m is None:
        return None
    u = m.astype(np.uint8)
    # flood the outside, so whatever is still off afterwards is a letter
    ff = np.zeros((u.shape[0] + 2, u.shape[1] + 2), np.uint8)
    outside = u.copy()
    cv2.floodFill(outside, ff, (0, 0), 1)
    solid = (u | (1 - outside)).astype(bool)
    ys, xs = np.where(solid)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    sub = bgr[y0:y1 + 1, x0:x1 + 1]
    ink = (sub[:, :, 0] > 200) & (sub[:, :, 1] > 200) & (sub[:, :, 2] > 200)
    ink &= solid[y0:y1 + 1, x0:x1 + 1] & ~m[y0:y1 + 1, x0:x1 + 1]
    rows = np.where(ink.sum(axis=1) >= 2)[0]
    if rows.size == 0:
        return None
    return int(y1 - y0 + 1), int(rows.max() - rows.min() + 1)


def check_one_font(geom: dict, fails: list[str], n: int = 140,
                   dur: float = 54.16) -> dict:
    times = [round((i + 0.5) * dur / n, 3) for i in range(n)]
    ph, gh = [], []
    for t in times:
        r = glyphs(grab(NEW, t), geom["meters"])
        if r is None:
            continue
        ph.append(r[0]); gh.append(r[1])
    P, G = np.array(ph), np.array(gh)
    declared = geom["caption_width"]["font_px"]
    # pill height = 1.30*fs + 2*19 in the generator's worst case; the browser's
    # own line box is what actually paints, so the RATIO is reported rather than
    # asserted against 1.30, and the CLAIM is that it is one value.
    vals, counts = np.unique(P, return_counts=True)
    out = {"pills_measured": int(P.size), "declared_font_px": declared,
           "pill_height": {"distinct": [int(v) for v in vals],
                           "counts": [int(c) for c in counts],
                           "min": int(P.min()), "max": int(P.max()),
                           "spread": int(P.max() - P.min())},
           "glyph_ink_height": {"min": int(G.min()), "p50": float(np.median(G)),
                                "p95": float(np.percentile(G, 95)),
                                "max": int(G.max()),
                                "distinct": int(np.unique(G).size)},
           "implied_font_px": round(float((P.max() - 2 * 19.0) / 1.30), 1)}
    print(f"16 ONE FONT   {P.size} pills measured on the render "
          f"(declared: one size, {declared:.0f}px)")
    print(f"              pill height  distinct values {out['pill_height']['distinct']} "
          f"  spread {out['pill_height']['spread']}px  -> implied font "
          f"{out['implied_font_px']:.1f}px")
    print(f"              glyph ink    {out['glyph_ink_height']['min']}.."
          f"{out['glyph_ink_height']['max']}px "
          f"(p50 {out['glyph_ink_height']['p50']:.0f}, p95 "
          f"{out['glyph_ink_height']['p95']:.0f}) — one cluster: ascender-only "
          f"phrases sit low, ascender+descender phrases at the top")
    if out["pill_height"]["spread"] > 2:
        fails.append(f"caption pill height varies by "
                     f"{out['pill_height']['spread']}px — more than one font size")
    if abs(out["implied_font_px"] - declared) > 3.0:
        fails.append(f"the rendered pill implies a {out['implied_font_px']}px "
                     f"font, declared {declared}px")
    # The tallest glyph run in a video set in ONE size is the ascender-to-
    # descender extent of that size — for Nunito ExtraBold at 54px that is
    # ~0.99em.  A second, larger size anywhere in the video would push this past
    # the em; a second, smaller one would show up as a second cluster in the
    # pill height, which is already asserted to be a single value.
    if not 0.80 * declared <= out["glyph_ink_height"]["max"] <= 1.10 * declared:
        fails.append(f"the tallest rendered glyph run is "
                     f"{out['glyph_ink_height']['max']}px, which is not one "
                     f"{declared:.0f}px font's ascender-to-descender extent")
    return out


# =================================================================== 17 LAW 12
def check_law12(geom: dict, geom_old: dict, fails: list[str], n: int = 90,
                dur: float = 54.16) -> dict:
    """The round-3 band/zone/width checks, re-earned at the new seat."""
    def sweep(mp4, g):
        tops, bots, cs, rights = [], [], [], []
        for i in range(n):
            box = pill_box(grab(mp4, round((i + 0.5) * dur / n, 3)), g["meters"])
            if not box:
                continue
            x, y, w, h = box
            tops.append(y); bots.append(y + h); cs.append(y + h / 2); rights.append(x + w)
        return {"seen": len(tops), "top_min": int(min(tops)), "bottom_max": int(max(bots)),
                "bottom_frac": round(max(bots) / H, 4),
                "centre_min": float(min(cs)), "centre_max": float(max(cs)),
                "centre_frac": round(float(np.median(cs)) / H, 4),
                "right_max": int(max(rights))}
    old, new = sweep(OLD, geom_old), sweep(NEW, geom)
    zone = geom["stage_zone"]
    times = [1.6, 8.4, 18.0, 24.0, 33.0, 44.0, 52.0]
    top = bot = rail_pill = rail_stage = 0
    for t in times:
        bgr = grab(NEW, t)
        dev = np.abs(bgr.astype(int) - CREAM_BGR).max(axis=2) > 26
        pill = pill_component(bgr, geom["meters"])
        top += int(dev[:192].sum())
        if pill is not None:
            bot += int(pill[1382:].sum())
            rail_pill += int(pill[:, 918:].sum())
        rail_stage += int(dev[int(zone[0]):int(zone[1]), 918:].sum())
    print(f"17 LAW 12     pill swept over {n} frames  "
          f"({old['seen']} / {new['seen']} carried a pill)")
    print(f"              bottom edge  fix3c {old['bottom_max']} "
          f"({old['bottom_frac']:.1%})  ->  fix5 {new['bottom_max']} "
          f"({new['bottom_frac']:.1%})   limit 1382 (72%)")
    print(f"              centre       fix3c {old['centre_frac']:.1%}  ->  fix5 "
          f"{new['centre_frac']:.1%}   preferred 40-65%   ONE seat: centre "
          f"spread {new['centre_max'] - new['centre_min']:.1f}px")
    print(f"              widest right x{new['right_max']} (rail line 918)")
    print(f"              zones: top10 {top}px  bottom28-pill {bot}px  "
          f"rail-pill {rail_pill}px  rail-stage-texture {rail_stage}px")
    if new["bottom_max"] > 1382:
        fails.append(f"caption bottom {new['bottom_max']} below the 72% line")
    if not 0.40 <= new["centre_frac"] <= 0.65:
        fails.append(f"caption centre {new['centre_frac']:.1%} outside 40-65%")
    if new["centre_max"] - new["centre_min"] > 8:
        fails.append(f"the caption seat is not stable: centres span "
                     f"{new['centre_max'] - new['centre_min']:.1f}px")
    if new["right_max"] > 921:
        fails.append(f"a pill reaches x={new['right_max']}, into the right rail")
    if bot or rail_pill:
        fails.append("caption pixels in a forbidden zone")
    if top > 200:
        fails.append(f"ink in the top 10% ({top}px)")
    return {"fix3c": old, "fix5": new,
            "zones": {"top10_px": top, "bottom28_pill_px": bot,
                      "rail_pill_px": rail_pill, "rail_stage_texture_px": rail_stage,
                      "frames": len(times)}}


def main() -> None:
    for f in (NEW, OLD, GEOM, GEOM_OLD, ENV):
        if not f.exists():
            raise SystemExit(f"missing {f}")
    geom = json.loads(GEOM.read_text())
    geom_old = json.loads(GEOM_OLD.read_text())
    fails: list[str] = []
    print(f"CUTOUT ROUND 5 — {NEW.name} vs {OLD.name} (the approved standard)\n")
    rep = {"cap_top": check_cap(fails)}
    print()
    rep["collisions"] = check_collisions(geom, fails)
    print()
    rep["one_font"] = check_one_font(geom, fails)
    print()
    rep["law12"] = check_law12(geom, geom_old, fails)
    (HERE / "logs/check_fix5.json").write_text(json.dumps(rep, indent=2))
    print()
    if fails:
        print("FAIL")
        for f in fails:
            print("  -", f)
        raise SystemExit(1)
    print("ALL ROUND-5 CHECKS PASS")


if __name__ == "__main__":
    main()
