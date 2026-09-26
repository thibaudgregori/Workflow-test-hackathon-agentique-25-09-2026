"""CUTOUT FIX ROUND 6 — the closing captions round, proven on decoded pixels.

Round 6 changes the caption pill onto the PUBLISHED factory's canonical spec and
nothing else, in a video Miguel has already approved.  Two claims therefore have
to survive the render rather than the generator:

 18  ONE CANONICAL PILL   the round-5 instrument, re-pointed at the canon.  Pill
                          height is swept over the whole video and must be ONE
                          value; that value must be the height the canonical
                          published pill measures in a browser (114.59 -> 114/115
                          decoded); and the glyph ink is measured inside the
                          SOLID pill (the round-5 flood-fill, without which the
                          measurement reads the antialiased fringe) so the law is
                          proven on letters and not only on the box around them.

 19  CONTAINMENT          fix5 -> fix6 decoded-pixel diff, frame by frame.  fix5
                          is the approved standard, so ONLY the caption band is
                          allowed to have changed.  The diff is not summarised
                          into a pass/fail number: the rows and columns that
                          moved are reported as a geography, and every changed
                          pixel outside the pill's own band (plus the halo the
                          retired drop shadow used to occupy) is a failure.

 20  SEAT + LAW 12        the seat did not move: pill centre over the sweep, its
                          spread, the bottom edge against Law 12's 72 % line, and
                          the widest right edge against the right rail — fix5 and
                          fix6 side by side.

Run:  python cutout6_check.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import cutout_facehf as FH                                            # noqa: E402
import cutout_media as CM                                            # noqa: E402
from cutout3_check import CREAM_BGR, grab, pill_component, pill_box  # noqa: E402
from cutout5_check import glyphs                                     # noqa: E402

NEW = HERE / "out/cutout_fix6.mp4"
OLD = HERE / "out/cutout_fix5.mp4"           # the approved standard
GEOM = HERE / "_geom_cutout_fix6.json"
GEOM_OLD = HERE / "_geom_cutout_fix5.json"
# the rendered project, for re-probing the staged layers the box must match
PROJECT = HERE / "build/cutout_fix6"
W, H = 1080, 1920
DUR = 54.16

# the canonical pill, measured in the render browser on the PUBLISHED factory
# (references/builds/mcpupgrade_icon, 38 pills, one distinct height)
CANON_H = 114.59
CANON_FS = 56.2
CANON_PAD_Y = 18.8


# ======================================================== 18 ONE CANONICAL PILL
def check_pill(geom: dict, fails: list[str], n: int = 140) -> dict:
    times = [round((i + 0.5) * DUR / n, 3) for i in range(n)]
    ph, gh = [], []
    for t in times:
        r = glyphs(grab(NEW, t), geom["meters"])
        if r is None:
            continue
        ph.append(r[0]); gh.append(r[1])
    P, G = np.array(ph), np.array(gh)
    vals, counts = np.unique(P, return_counts=True)
    # a decoded pill edge is antialiased, so 114.59 can land on 114 or 115; what
    # may NOT happen is two clusters, which is what a second font size looks like
    implied = round((float(P.max()) - 2 * CANON_PAD_Y) / 1.3699, 1)
    out = {"pills_measured": int(P.size), "declared_font_px": CANON_FS,
           "canonical_pill_height_browser": CANON_H,
           "pill_height": {"distinct": [int(v) for v in vals],
                           "counts": [int(c) for c in counts],
                           "min": int(P.min()), "max": int(P.max()),
                           "spread": int(P.max() - P.min())},
           "glyph_ink_height": {"min": int(G.min()), "p50": float(np.median(G)),
                                "p95": float(np.percentile(G, 95)),
                                "max": int(G.max()),
                                "distinct": int(np.unique(G).size)},
           "implied_font_px": implied,
           "fix5_pill_height": 112}
    print(f"18 ONE PILL   {P.size} pills swept on the render "
          f"(declared: ONE size, {CANON_FS}px — the published canon)")
    print(f"              pill height  distinct {out['pill_height']['distinct']}  "
          f"spread {out['pill_height']['spread']}px   canon 114.59  fix5 was 112")
    print(f"              implied font {implied:.1f}px from a 1.3699em line box "
          f"+ 2x{CANON_PAD_Y}px padding")
    print(f"              glyph ink    {out['glyph_ink_height']['min']}.."
          f"{out['glyph_ink_height']['max']}px (p50 "
          f"{out['glyph_ink_height']['p50']:.0f}, p95 "
          f"{out['glyph_ink_height']['p95']:.0f}) — one cluster")
    if out["pill_height"]["spread"] > 1:
        fails.append(f"caption pill height varies by "
                     f"{out['pill_height']['spread']}px — more than one size")
    if not (CANON_H - 1.5 <= P.max() <= CANON_H + 1.5):
        fails.append(f"the rendered pill is {P.max()}px tall; the canonical "
                     f"published pill measures {CANON_H}px")
    if abs(implied - CANON_FS) > 2.0:
        fails.append(f"the rendered pill implies a {implied}px font, "
                     f"canon is {CANON_FS}px")
    if not 0.80 * CANON_FS <= out["glyph_ink_height"]["max"] <= 1.10 * CANON_FS:
        fails.append(f"the tallest glyph run is {out['glyph_ink_height']['max']}px, "
                     f"not one {CANON_FS}px font's ascender-to-descender extent")
    return out


# ============================================================== 19 CONTAINMENT
def check_containment(geom: dict, fails: list[str], n: int = 90,
                      thresh: int = 12) -> dict:
    """fix5 -> fix6 decoded diff, and what it can and cannot prove.

    The allowed band is the pill's own extent at the frozen seat, widened by the
    halo the RETIRED drop shadow occupied (`0 6px 22px`, so 22px of blur and 6px
    of downward offset), because removing that shadow legitimately repaints
    cream where it used to darken.

    A DECODED diff cannot settle containment on its own: H.264 allocates bits
    across the whole frame, so changing the caption perturbs the silhouette's
    macroblocks with no content change whatsoever.  This measures the SIZE of
    that coupling (it must stay at noise level — a few hundred px per frame at a
    delta the eye cannot see) and then defers the verdict to
    `cutout6_containment.py`, which diffs the two LOSSLESS png-sequences frame by
    frame, where a differing pixel means a differing pixel.
    """
    lossless = HERE / "logs/containment_fix6.json"
    if not lossless.exists():
        fails.append("run cutout6_containment.py — the lossless png diff is the "
                     "only test that can prove containment")
    cap = geom["caption"]
    band = (int(cap["top"] - 22 - 6 - 2), int(cap["bottom"] + 22 + 6 + 2))
    ever = np.zeros((H, W), bool)
    worst_out, per_frame = 0, []
    for i in range(n):
        t = round((i + 0.5) * DUR / n, 3)
        a, b = grab(OLD, t), grab(NEW, t)
        d = np.abs(a.astype(int) - b.astype(int)).max(axis=2)
        hit = d > thresh
        ever |= hit
        out_mask = hit.copy()
        out_mask[band[0]:band[1], :] = False
        per_frame.append({"t": t, "changed_px": int(hit.sum()),
                          "outside_band_px": int(out_mask.sum()),
                          "max_delta_outside": int(d[out_mask].max())
                          if out_mask.any() else 0})
        worst_out = max(worst_out, int(out_mask.sum()))
    rows = np.where(ever.any(axis=1))[0]
    cols = np.where(ever.any(axis=0))[0]
    outside = ever.copy()
    outside[band[0]:band[1], :] = False
    out = {"frames": n, "threshold": thresh, "allowed_band": list(band),
           "changed_rows": [int(rows.min()), int(rows.max())] if rows.size else None,
           "changed_cols": [int(cols.min()), int(cols.max())] if cols.size else None,
           "changed_px_union": int(ever.sum()),
           "outside_band_px_union": int(outside.sum()),
           "worst_frame_outside_px": worst_out,
           "caption_band": [cap["top"], cap["bottom"]],
           "top_rows_touched": int(ever[:192].sum()),
           "bottom28_rows_touched": int(ever[1382:].sum()),
           "worst_frames": sorted(per_frame, key=lambda r: -r["outside_band_px"])[:5]}
    worst_delta = max(r["max_delta_outside"] for r in per_frame)
    out["max_delta_outside_band"] = worst_delta
    if lossless.exists():
        L = json.loads(lossless.read_text())
        out["lossless"] = {k: L[k] for k in
                           ("frames", "changed_rows", "changed_cols",
                            "changed_px_union", "outside_band_px_union",
                            "outside_row_groups", "worst_outside_cluster",
                            "null_control", "untouched", "fails")}
        fails += [f"LOSSLESS: {f}" for f in L["fails"]]
    print(f"19 CONTAINMENT  fix5 -> fix6, {n} decoded frames (delta > {thresh}/255)")
    print(f"                rows that ever changed  {out['changed_rows']}   "
          f"allowed {band[0]}..{band[1]}  (pill {cap['top']}..{cap['bottom']} "
          f"+ the retired shadow's 22px halo)")
    print(f"                union {out['changed_px_union']:,}px, of which "
          f"{out['outside_band_px_union']:,}px outside the band, worst delta "
          f"there {worst_delta}/255 — reported, NOT asserted: this is the "
          f"encoder's rate coupling and no threshold on it means anything")
    if "lossless" in out:
        L = out["lossless"]
        C = L["null_control"]
        print(f"                LOSSLESS png diff, all {L['frames']} frames: "
              f"rows {L['changed_rows']}  cols {L['changed_cols']}  "
              f"{L['changed_px_union']:,}px changed, "
              f"{L['outside_band_px_union']}px outside the band "
              f"(worst cluster {L['worst_outside_cluster']}px)")
        print(f"                NULL CONTROL, fix5 rendered twice: "
              f"{C['outside_band_px']}px outside the band "
              f"(worst cluster {C['worst_outside_cluster']}px) with ZERO content "
              f"difference — the renderer's own floor")
        print(f"                untouched: Law-12 top band "
              f"{L['untouched']['law12_top_band_0_192']}px, stage zone "
              f"{L['untouched']['stage_zone_192_869']}px, depth band "
              f"{L['untouched']['depth_band_1120_1560']}px")
    return out


# ============================================================ 20 SEAT + LAW 12
def check_seat(geom: dict, geom_old: dict, fails: list[str], n: int = 90) -> dict:
    def sweep(mp4, g):
        tops, bots, cs, rights, lefts = [], [], [], [], []
        for i in range(n):
            box = pill_box(grab(mp4, round((i + 0.5) * DUR / n, 3)), g["meters"])
            if not box:
                continue
            x, y, w, h = box
            tops.append(y); bots.append(y + h); cs.append(y + h / 2)
            rights.append(x + w); lefts.append(x)
        return {"seen": len(tops), "top_min": int(min(tops)),
                "bottom_max": int(max(bots)), "bottom_frac": round(max(bots) / H, 4),
                "centre_min": float(min(cs)), "centre_max": float(max(cs)),
                "centre_med": float(np.median(cs)),
                "centre_frac": round(float(np.median(cs)) / H, 4),
                "right_max": int(max(rights)), "left_min": int(min(lefts))}
    old, new = sweep(OLD, geom_old), sweep(NEW, geom)
    times = [1.6, 8.4, 18.0, 24.0, 33.0, 44.0, 52.0]
    top = bot = rail_pill = 0
    for t in times:
        bgr = grab(NEW, t)
        dev = np.abs(bgr.astype(int) - CREAM_BGR).max(axis=2) > 26
        pill = pill_component(bgr, geom["meters"])
        top += int(dev[:192].sum())
        if pill is not None:
            bot += int(pill[1382:].sum())
            rail_pill += int(pill[:, 918:].sum())
    print(f"20 SEAT        pill swept over {n} frames "
          f"({old['seen']} / {new['seen']} carried a pill)")
    print(f"               centre   fix5 {old['centre_med']:.1f} "
          f"({old['centre_frac']:.1%})  ->  fix6 {new['centre_med']:.1f} "
          f"({new['centre_frac']:.1%})   spread {new['centre_max'] - new['centre_min']:.1f}px")
    print(f"               bottom   fix5 {old['bottom_max']}  ->  fix6 "
          f"{new['bottom_max']} ({new['bottom_frac']:.1%})   limit 1382 (72%)")
    print(f"               widest   fix5 x{old['right_max']}  ->  fix6 "
          f"x{new['right_max']}   rail line x918")
    print(f"               zones: top10 {top}px  bottom28-pill {bot}px  "
          f"rail-pill {rail_pill}px")
    if abs(new["centre_med"] - old["centre_med"]) > 1.5:
        fails.append(f"the seat moved: fix5 centre {old['centre_med']:.1f} -> "
                     f"fix6 {new['centre_med']:.1f}")
    if new["centre_max"] - new["centre_min"] > 8:
        fails.append(f"the caption seat is not stable: centres span "
                     f"{new['centre_max'] - new['centre_min']:.1f}px")
    if new["bottom_max"] > 1382:
        fails.append(f"caption bottom {new['bottom_max']} below the 72% line")
    if new["right_max"] > 921:
        fails.append(f"a pill reaches x={new['right_max']}, into the right rail")
    if bot or rail_pill:
        fails.append("caption pixels in a forbidden zone")
    return {"fix5": old, "fix6": new,
            "zones": {"top10_px": top, "bottom28_pill_px": bot,
                      "rail_pill_px": rail_pill, "frames": len(times)}}


def check_face_hf(mp4: Path, geom: dict, fails: list[str],
                  tol: float = 0.12) -> dict:
    """21  FACE HF — his face carries the detail the source plate carries.

    Measured on the SKIN-ONLY crop (`cutout_facehf.K_SKIN`), never the 1.6x
    audit crop, which is wider than his head and lands on the die-cut edge.  The
    reference is the plate the matte was cut from, so the gate reads "the render
    did not lose (or invent) face detail relative to its own source" and does
    not depend on any other video.

    The defective v4 chain failed this in the SOFT direction: plate 6.98 ->
    matte 6.88 -> a 1.10 browser upscale -> 5.65 on the finished short, 19 %
    of the face's detail smeared away.  v5 measures 6.62 -> 6.60 -> 6.63.
    """
    ref = geom.get("plate", {}).get("hf_reference")
    out = dict(k=FH.K_SKIN, mix=str(mp4))
    r = FH.face_hf(str(mp4), k=FH.K_SKIN)
    out["face_hf"] = r["face_hf"]
    out["rows"] = r["rows"]
    if not ref:
        out["note"] = ("no plate reference in _geom_*.json -> reported, not "
                       "gated.  Record plate.hf_reference to gate it.")
        print(f"C  FACE HF     {out['face_hf']} on the {FH.K_SKIN}x skin crop "
              f"(no plate reference recorded, not gated)")
        return out
    out["plate_hf"] = ref
    out["ratio"] = round(out["face_hf"] / ref, 4)
    ok = abs(out["ratio"] - 1.0) <= tol
    out["tol"] = tol
    out["ok"] = ok
    print(f"C  FACE HF     {out['face_hf']} vs plate {ref} "
          f"(x{out['ratio']}, tol {tol:.0%}) {'OK' if ok else 'FAIL'}")
    if not ok:
        fails.append(f"face HF {out['face_hf']} is {out['ratio']:.2f}x the "
                     f"plate's {ref} on the {FH.K_SKIN}x skin crop — the face "
                     f"gained or lost detail between the plate and the render")
    return out


def check_plate_box(geom: dict, fails: list[str],
                    project: Path | None = None) -> dict:
    """23  PLATE BOX — the cutout layer is painted 1:1 into whole pixels.

    THE ASSERTION THAT WOULD HAVE CAUGHT grokprice BEFORE ITS RENDER
    (2026-09-01).  Twelve of the thirteen remakes reached parity with their own
    plate; `grokprice` stopped at 0.869 because its layer box was
    `1143.9 x 953.3` at `top:966.7` against 1144x954 encoded layers.  Chromium
    bilinear-resamples a fractional box at a sub-pixel offset, so 13 % of the
    face detail the plate carried was destroyed at composite time — with SAM2,
    the trim, the plate (7.470) and the VP9 cut layer (7.401, 0.991) all clean.
    Emulating that exact transform on the plate reproduced the render's deficit
    to 0.4 %, which is what makes this a geometry defect and not an encode one.

    Face HF (check 21) catches it only AFTER a 90-second render, and only just:
    0.869 is 0.131 off parity against a 0.12 tolerance.  This check is the cheap
    one, and it is decidable from the geometry record alone:

        box w, box h, left, top   must all be WHOLE PIXELS
        box                       must equal the ENCODED w x h of every layer
                                  staged under `assets/v/` (matte + rim)

    `guard_plate_box` in the chassis already refuses such a build; this re-reads
    what the build recorded, so a geom file from any port can be audited without
    re-running its generator, and re-probes the staged files when they are
    reachable.
    """
    pl = geom.get("plate") or {}
    rec = pl.get("box")
    out: dict = {"recorded": rec}
    if isinstance(rec, (list, tuple)):
        # THE PER-VIDEO GENERATORS RECORD THE BOX AS `[w, h]` PLUS `left`/`top`,
        # not as the lab's `{box, origin, layers}` envelope.  Both say the same
        # thing; normalise rather than special-case, so a geom from any port can
        # be audited.  `mode` comes along because an over-wide plate is still a
        # v5 LAYERED build and the equality half of this check applies to it.
        rec = {"box": [float(v) for v in rec],
               "origin": [float(pl.get("left")), float(pl.get("top"))],
               "layers": {}, "mode": pl.get("matte_mode") or "layered"}
        out["normalised_from"] = "plate.box list + plate.left/top"
    if rec is None:
        # older geom files: fall back to the four numbers they do carry
        rec = {"box": [pl.get("w"), pl.get("h")],
               "origin": [pl.get("left"), pl.get("top")], "layers": {}}
        out["note"] = ("no plate.box record — checked from plate w/h/left/top "
                       "only; the encoded-layer half could not be verified")
    box, origin = rec.get("box") or [], rec.get("origin") or []
    if len(box) != 2 or len(origin) != 2 or any(v is None for v in box + origin):
        fails.append("plate box geometry is not recorded in _geom_*.json — the "
                     "resample gate cannot run")
        out["ok"] = False
        return out
    bad = []
    for v, label in zip(box + origin, ("width", "height", "left", "top")):
        if abs(float(v) - round(float(v))) > 1e-9:
            bad.append(f"{label} {v} is not a whole pixel")
    layers = dict(rec.get("layers") or {})
    if project is not None and (project / "assets/v").is_dir():
        import cutout_media as _CM
        for p in sorted((project / "assets/v").glob("matte*.webm")):
            layers[p.name] = list(_CM.probe_wh(p))
    # The equality half is scoped to the v5 LAYER SET, as in `guard_plate_box`:
    # `--matte-mode baked` reproduces v4's deliberate 1.10 upscale for the
    # promotion diff, and that upscale is defect 1 itself, not a new finding.
    if (rec.get("mode") or pl.get("matte_mode") or "layered") == "layered":
        for n, wh in layers.items():
            if [float(x) for x in wh] != [float(x) for x in box]:
                bad.append(f"box {box[0]}x{box[1]} != {n}'s encoded "
                           f"{wh[0]}x{wh[1]} — the layer is resampled")
    out.update(box=box, origin=origin, layers=layers, ok=not bad, bad=bad)
    print(f"E  PLATE BOX   {box[0]}x{box[1]} at ({origin[0]}, {origin[1]}) vs "
          + (", ".join(f"{n} {w}x{h}" for n, (w, h) in layers.items())
             or "no layers probed")
          + f" {'OK' if not bad else 'FAIL'}")
    if bad:
        fails.append("the cutout layer box is not integral and 1:1 against its "
                     "encoded plate, so his face is resampled every frame: "
                     + "; ".join(bad))
    return out


def check_treble(mp4: Path, geom: dict, fails: list[str]) -> dict:
    """22  TREBLE — the mix kept the voice master's top octave.

    Defect 2, 2026-09-01: ten of the thirteen cutout remakes mixed from the
    16 kHz mono ANALYSIS wav, whose Nyquist limit is 8 kHz, so the 8-16 kHz band
    of the finished short sat 18.4 dB below the voice master's instead of 0.2 dB
    below it.  The gate is 6 dB, wide enough that the music bed, the AAC encode
    and loudness normalisation never trip it and narrow enough that an amputated
    octave always does.
    """
    src = (geom.get("voice") or {}).get("source")
    if not src or not Path(src).exists():
        fails.append("no voice.source in _geom_*.json — the build did not record "
                     "which audio file it mixed, so the treble gate cannot run")
        return {"ok": False, "reason": "no voice source recorded"}
    m, v = CM.band_db(mp4), CM.band_db(Path(src))
    out = dict(mix_8_16k_db=m, master_8_16k_db=v, delta_db=round(m - v, 2),
               tol_db=CM.TREBLE_TOL_DB, master=src,
               ok=abs(m - v) <= CM.TREBLE_TOL_DB)
    print(f"D  TREBLE      mix {m} dB vs master {v} dB "
          f"({out['delta_db']:+} dB, tol {CM.TREBLE_TOL_DB}) "
          f"{'OK' if out['ok'] else 'FAIL'}")
    if not out["ok"]:
        fails.append(f"the mix's 8-16 kHz band is {out['delta_db']:+} dB off the "
                     f"voice master's — almost certainly mixed from the 16 kHz "
                     f"mono analysis track")
    return out


def check_edge_fade(project: Path, fails: list[str]) -> dict:
    """24  GLOBAL LAW 8 — EDGE FADE, ON THE EMITTED HTML.

    Added 2026-09-01 after run 9 shipped two cutouts whose depth lanes were
    hard-chopped at x=0 and x=1080 with all three gates green.  The chassis has
    had a `guard_edge_fade` the whole time; it never fired, because a guard only
    fires if the code path that built the page CALLS it, and both generators had
    rolled their own lane code.  So the check now lives DOWNSTREAM of the
    generator, on the file it wrote:

      a) every clipping container in the page carries a mask (the string guard,
         which catches a wrapper someone forgot to fade), and
      b) Gate 1's own `edgefade` sweep reported zero violations (the geometric
         one, which catches painted content straddling a frame edge with no
         wrapper at all — the defect the string guard is blind to).

    (b) is the load-bearing half.  It is read from the Gate 1 report rather than
    re-measured, so this check stays cheap and Gate 1 stays the single place the
    DOM is swept.
    """
    out: dict = {"project": str(project)}
    html_path = project / "index.html"
    if not html_path.exists():
        fails.append(f"no emitted HTML at {html_path} — Law 8 cannot be checked")
        return {"ok": False, "reason": "no index.html"}
    import cutout_core as C                                          # noqa: PLC0415
    try:
        out["masks"] = C.guard_edge_fade(html_path.read_text())
    except SystemExit as e:
        fails.append(str(e))
        out["masks"] = {"ok": False, "error": str(e)}
    rep = project / "geometry_audit/report.json"
    if not rep.exists():
        fails.append("no Gate 1 report next to the project — run geometry_audit.py "
                     "first; its `edgefade` sweep is the half of Law 8 that a "
                     "string guard cannot see")
        out["gate1"] = {"ok": False, "reason": "no report.json"}
        return out
    viol = [v for v in json.loads(rep.read_text())["violations"]
            if v["type"] == "edgefade"]
    out["gate1"] = {"edgefade_violations": len(viol),
                    "elements": [e for v in viol for e in v["elements"]],
                    "ok": not viol}
    if viol:
        fails.append(f"GLOBAL LAW 8: {len(viol)} painted box(es) cut by a frame "
                     f"edge with no alpha fade — {out['gate1']['elements']}")
    ok = out["masks"].get("ok", True) is not False and out["gate1"]["ok"]
    print(f"E  EDGE FADE   {out['gate1']['edgefade_violations']} frame-edge chops, "
          f"{out['masks'].get('masked_containers', '?')} masked containers "
          f"{'OK' if ok else 'FAIL'}")
    out["ok"] = ok
    return out


def check_edge_clip(project: Path, geom: dict, fails: list[str],
                    alpha: Path | None = None) -> dict:
    """26  EDGE CLIP — the silhouette never touches a side edge above the bust.

    Added 2026-09-02, after a full-take sweep found his LEFT hand sliced flat at
    the frame edge on the staged `kimiram` cutout in two windows of 0.80 s and
    0.20 s, and the same class on `impossibletask` in two windows of 1.08 s and
    0.16 s.  Every one of those windows had been signed off by a clerk on 2.5 s
    spot checks: three of the four are under 0.8 s, so **sampling cannot clear
    this defect** and no amount of clerk diligence would have.

    The gate is `pipeline/edge_clip_check.py`, run on the SHIPPED alpha the
    project stages, with the plate box read from this build's own `_geom`.  It
    is structural, not proportional: the bust base is excluded because it is the
    run that touches the bottom row, and a defect is an opaque run at the edge
    column DETACHED from that base, or that base climbing more than 30 canvas px
    above the take's own shoulder baseline.  A percentage-of-height exclusion
    was tried first and flags 100 % of frames in every take, because the
    shoulder occupies 16.8 % of the silhouette at the edge column.

    Calibrated on three staged cutouts: it fires 2 windows on kimiram, 2 on the
    retired impossibletask, and is silent on perplexityprojects.
    """
    import sys as _sys                                              # noqa: PLC0415
    _F = HERE.parents[2]
    _sys.path.insert(0, str(_F / "pipeline"))
    import edge_clip_check as ECC                                   # noqa: PLC0415

    out: dict = {"project": str(project)}
    if alpha is None:
        vd = project / "assets/v"
        cand = [vd / "matte.webm"]
        src = vd / "_matte.webm.src"
        if src.exists():
            cand.insert(0, Path(src.read_text().splitlines()[0].strip()))
        # the alpha-only sibling is the measurement surface; fall back to the
        # cut layer, whose alpha plane is the same trim
        for c in list(cand):
            a = c.with_name(c.name.replace("_cut.webm", "_alpha.webm"))
            if a != c:
                cand.insert(0, a)
        alpha = next((c for c in cand if c.exists()), None)
    if alpha is None:
        fails.append("EDGE CLIP: no staged matte alpha to sweep — the gate "
                     "cannot run, and a sampled review cannot replace it")
        out["ok"] = False
        return out
    try:
        box = ECC.box_from_geom_dict(geom)
    except Exception as e:                                          # noqa: BLE001
        fails.append(f"EDGE CLIP: no plate box in _geom ({e})")
        out["ok"] = False
        return out
    rep = ECC.sweep(Path(alpha), box)
    out.update(alpha=str(alpha), frames=rep["frames"],
               edges={t: {k: v for k, v in rep["edges"][t].items()
                          if k in ("shoulder_baseline_alpha_row",
                                   "defect_frames", "isolated_limb_frames",
                                   "contact_rise_frames",
                                   "min_limb_margin_canvas_px")}
                      for t in rep["edges"]},
               windows=rep["windows"],
               frame_edge_windows=rep["frame_edge_windows"],
               overwide=rep["overwide"], verdict=rep["verdict"],
               ok=not rep["windows"])
    print(f"E  EDGE CLIP   {rep['frames']} frames, "
          f"{len(rep['windows'])} plate-border window(s), plate limb margin "
          f"L {rep['edges']['plate_left']['min_limb_margin_canvas_px']} / "
          f"R {rep['edges']['plate_right']['min_limb_margin_canvas_px']} px "
          f"{'OK' if not rep['windows'] else 'FAIL'}")
    if rep["windows"]:
        fails.append(
            "EDGE CLIP: the trim is CUT BY THE PLATE'S OWN BORDER above the bust "
            "in " + ", ".join(f"{w['edge']} {w['t'][0]}-{w['t'][1]}s "
                              f"({w['n_frames']}f)" for w in rep["windows"])
            + " — the rim is cut with it, so the shape enters the frame with no "
              "outline on that side.  The remedy is an OVER-WIDE PLATE, not a "
              "repaint (CHASSIS.md)")
    return out


def check_depth_field(project: Path, fails: list[str]) -> dict:
    """25  THE DEPTH FIELD IS THE FOUNDATION'S, MEASURED ON THE EMITTED HTML.

    Added 2026-09-01, the same afternoon and for the same reason as check 24:
    Miguel rejected all three run-9 cutouts because "we used to have a beautiful
    regular background ... you changed the perspective and you changed the
    space".  Every one of those numbers was decidable from the page:

      tile sizes 78/116/148, gaps 30/36/44 (pitch 108/152/192), 26 px of cream
      between lanes, a 394 px band, and a step schedule with a real pulse.

    Run 9 shipped 78/116/**168** at 0.72 x tile gaps with the mid and near lanes
    OVERLAPPING by 2 px and ONE step event for a 41-second take — and all three
    gates were green, because the geometry laws only ever asked whether atoms
    collided, never whether the format still looked like itself.  A guard inside
    `cutout_depthfield` cannot catch this either: a builder who writes their own
    `depth_lanes()` never calls it.  So the measurement lives DOWNSTREAM, on the
    file the generator wrote, exactly like Law 8's.
    """
    import re                                                        # noqa: PLC0415
    import cutout_depthfield as DF                                   # noqa: PLC0415

    out: dict = {"project": str(project), "foundation": {
        "tiles": [t for _n, t, _g, _o, _d in DF.FOUNDATION_LANES],
        "gaps": [g for _n, _t, g, _o, _d in DF.FOUNDATION_LANES],
        "inter_lane_gap": DF.INTER_LANE_GAP, "band_h": DF.BAND_H}}
    html_path = project / "index.html"
    if not html_path.exists():
        fails.append(f"no emitted HTML at {html_path} — the depth field cannot "
                     "be measured")
        return {"ok": False, "reason": "no index.html"}
    html = html_path.read_text()
    names = [n for n, _t, _g, _o, _d in DF.FOUNDATION_LANES]
    lanes, bad = {}, []

    for name, tile, gap, _op, _dist in DF.FOUNDATION_LANES:
        wrap = re.search(
            rf'id="lw-{name}"\s+style="[^"]*top:([0-9.]+)px;'
            rf'width:([0-9.]+)px;height:([0-9.]+)px', html)
        if not wrap:
            bad.append(f"lane {name!r} has no canvas-wide wrapper `lw-{name}` — "
                       "the field is not the foundation's")
            continue
        top, wrap_w, wrap_h = (float(wrap.group(i)) for i in (1, 2, 3))
        xs = sorted(float(m) for m in re.findall(
            rf'id="ln-{name}\d+"\s+style="left:(-?[0-9.]+)px', html))
        ws = {float(m) for m in re.findall(
            rf'id="ln-{name}\d+"\s+style="left:-?[0-9.]+px;top:[0-9.]+px;'
            rf'width:([0-9.]+)px', html)}
        if len(xs) < 4:
            bad.append(f"lane {name!r} carries {len(xs)} tiles — a depth lane is "
                       "wider than the canvas by design and cannot be that short")
            continue
        pitches = {round(b - a, 1) for a, b in zip(xs, xs[1:])}
        lanes[name] = {"y": top, "wrapper": [wrap_w, wrap_h], "tiles": len(xs),
                       "tile_w": sorted(ws), "pitches": sorted(pitches)}
        if ws != {tile}:
            bad.append(f"lane {name!r} tile is {sorted(ws)} px, the foundation's "
                       f"is {tile} px — that is the PERSPECTIVE changing")
        if abs(wrap_h - tile) > 0.51:
            bad.append(f"lane {name!r} wrapper is {wrap_h} px tall against a "
                       f"{tile} px tile")
        if abs(wrap_w - DF.W) > 0.51:
            bad.append(f"lane {name!r} wrapper is {wrap_w} px wide — the fade "
                       f"must sit on a container exactly {DF.W} px across")
        if pitches != {round(tile + gap, 1)}:
            bad.append(f"lane {name!r} pitch is {sorted(pitches)} px, the "
                       f"foundation's is {tile + gap} px — that is the SPACE "
                       "changing")

    if len(lanes) == len(names):
        ys = [lanes[n]["y"] for n in names]
        tiles = [t for _n, t, _g, _o, _d in DF.FOUNDATION_LANES]
        gutters = [round(ys[i + 1] - (ys[i] + tiles[i]), 1) for i in range(2)]
        band_h = round(ys[-1] + tiles[-1] - ys[0], 1)
        out["band"] = [ys[0], round(ys[0] + band_h, 1)]
        out["inter_lane_gutters"] = gutters
        out["band_h"] = band_h
        for i, g in enumerate(gutters):
            if abs(g - DF.INTER_LANE_GAP) > 0.51:
                bad.append(f"the cream between lane {names[i]!r} and "
                           f"{names[i + 1]!r} is {g} px, the foundation's is "
                           f"{DF.INTER_LANE_GAP} px"
                           + (" — the lanes OVERLAP" if g < 0 else ""))
        if abs(band_h - DF.BAND_H) > 0.51:
            bad.append(f"the depth band is {band_h} px tall, the foundation's is "
                       f"{DF.BAND_H} px")

    steps = len(re.findall(r'tl\.to\("#ln-near",\{x:', html))
    out["step_events"] = steps
    if steps < 4:
        bad.append(f"the field steps {steps} time(s) in the whole take — the "
                   "foundation steps once per spoken beat, and a field that "
                   "never moves reads as wallpaper, not as depth")
    out["pop_behind"] = bool(re.search(r'id="pop(behind)?-?\w*-w"', html))
    out["lanes"] = lanes
    out["violations"] = bad
    out["ok"] = not bad
    fails.extend(bad)
    print(f"F  DEPTH FIELD  {len(lanes)}/3 lanes, band {out.get('band_h', '?')}px, "
          f"gutters {out.get('inter_lane_gutters', '?')}, {steps} steps "
          f"{'OK' if not bad else 'FAIL'}")
    return out


def main() -> None:
    for p in (NEW, OLD, GEOM, GEOM_OLD):
        if not p.exists():
            raise SystemExit(f"missing {p}")
    geom = json.loads(GEOM.read_text())
    geom_old = json.loads(GEOM_OLD.read_text())
    fails: list[str] = []
    rep = {"18_one_canonical_pill": check_pill(geom, fails),
           "19_containment": check_containment(geom, fails),
           "20_seat_law12": check_seat(geom, geom_old, fails),
           # THE TWO DEFECT GATES (2026-09-01).  Face pixels and voice band —
           # the two things that were quietly wrong in the 13 remakes and that
           # no geometry check could ever have caught.
           "21_face_hf": check_face_hf(NEW, geom, fails),
           "22_treble": check_treble(NEW, geom, fails),
           # THE CHEAP HALF OF DEFECT 1 (grokprice, 2026-09-01).  Face HF is the
           # outcome; the box is the cause, and it is decidable before a frame
           # is rendered.
           "23_plate_box": check_plate_box(geom, fails, PROJECT),
           # THE GUARD THAT WAS BYPASSABLE (run 9, 2026-09-01).  Measured on the
           # HTML the generator actually wrote, so it holds for any code path.
           "24_edge_fade": check_edge_fade(PROJECT, fails),
           # THE LOOK ITSELF (run 9, 2026-09-01).  Three cutouts passed every
           # gate above and were still rejected on sight; this is the number
           # that would have caught them.
           "25_depth_field": check_depth_field(PROJECT, fails),
           # THE DEFECT SPOT CHECKS CANNOT SEE (run 9, 2026-09-02).  Full take,
           # every frame; three of the four known windows are under 0.8 s.
           "26_edge_clip": check_edge_clip(PROJECT, geom, fails),
           # THE DEFECT THE SEAT DERIVATION CANNOT SEE (supergrokplus, run 10,
           # 2026-09-03).  Every seat gate above compares the pill to the
           # ENVELOPE's crown; this one compares it to HIS crown, on the
           # delivered pixels.
           "27_crown_clearance": check_crown_clearance(
               NEW, fails,
               plate_top=float(geom.get("plate", {}).get("box", {}).get("top"))
               if isinstance(geom.get("plate", {}).get("box"), dict) else None)}
    rep["fails"] = fails
    (HERE / "logs/check_fix6.json").write_text(json.dumps(rep, indent=2))
    print()
    if fails:
        print("FAIL")
        for f in fails:
            print("  - " + f)
        raise SystemExit(1)
    print("ROUND 6 CHECKS PASS — one canonical pill, seat unmoved, nothing "
          "outside the caption band changed, face HF at the plate's level, "
          "treble at the voice master's level")


# =================================================== 27 CROWN-TO-PILL CLEARANCE
# ADDED 2026-09-03, from the `supergrokplus_cutout` rejection.
#
# WHAT IT CATCHES.  The caption seat is derived from the matte envelope's crown
# (`CAP_Y = union_top - CAP_MIN_CLEAR - CAP_H/2`), and every gate downstream
# checks the seat against the DERIVATION rather than against his head.  So when
# the derivation's input is wrong — the plate crop CUT his cap, so the envelope's
# "crown" was the plate's own top row and not the top of his head — the pill
# lands on a flat horizontal slice across his cap and no check fires.  That is
# exactly what shipped: crown at canvas y 930 (the plate top), pill bottom at
# 906.7, 23.3 px of clearance under a ~490 px wide FLAT cut, and Miguel's read
# was "the cutout video is clipping my head".
#
# WHY IT IS MEASURED ON THE RENDER.  The envelope, the geometry report and the
# plate record all agreed with each other and all of them were wrong together,
# because they share one input.  The delivered mp4 shares nothing: it is the only
# artefact that is downstream of every one of them.  So this check decodes the
# file and finds the two things the viewer actually sees — the bottom edge of the
# terracotta pill, and the first row of him underneath it.
#
# HOW.  Every `every` seconds:
#   crown   scanning DOWN from the pill's bottom, inside the pill's own column
#           span, the first row with a contiguous run of >= CROWN_MIN_RUN DARK px
#           that is still dark CROWN_PERSIST rows later (a head, not a speck)
#   clear   crown - pill_bottom, in DESIGN px (the frame is normalised to 1920)
# Nothing else can be in that gap by construction: the stage zone ends above the
# caption (ZY1 < CAP_Y) and the depth band's top lane starts below the crown.
#   pill    `cutout3_check.pill_component` — the caption's own connected
#           component of #C4573A (captions.py CAP_BG), which is what separates it
#           from the stage's rules, rungs and card headers in the same accent
CROWN_DARK_L = 110              # cap / hair against a cream ground
CROWN_MIN_RUN = 60              # design px of contiguous dark on a row
CROWN_PERSIST = 10              # rows later it must still be dark
# THE TWO NUMBERS, CALIBRATED ON THE CORPUS RATHER THAN CHOSEN — the eleven
# approved run-9 cutouts, the two run-10 builds, every 0.5 s, in
# `logs/crown_calibration.json`:
#
#   file                     min clear   median   samples with crown ON the plate top
#   ----------------------------------------------------------------------------
#   chatgptchrome  APPROVED       31.0     33.0    0 %
#   codexnondev    APPROVED       32.0     42.0    0 %
#   codexvoice     APPROVED       25.0     38.0    1 %   <- the corpus minimum
#   deepseekflash  APPROVED       37.0     58.0    0 %
#   lunacheaper    APPROVED       33.0     40.0    0 %
#   minimaxh3      APPROVED       29.0     50.0    0 %
#   sparkchrome    APPROVED       38.0     48.0    0 %
#   kimiram        APPROVED       35.0     36.0    0 %
#   impossibletask APPROVED       34.0     37.0    0 %
#   perplexityprojects APPROVED   31.0     33.0    0 %
#   supergrokplus  REJECTED       25.0     25.0  100 %
#   moleculezoom   (same plate)   25.0     25.0  100 %
#
# CLEARANCE ALONE CANNOT SEPARATE THEM — the rejected build sits at 25 px and so
# does the approved `codexvoice`, because the seat solver puts the pill the same
# canon distance above whatever it believes the crown to be.  The thing that
# actually separates a head from a cut is WHERE the crown is: an approved
# cutout's topmost row is a rounded arc somewhere inside the plate and touches
# the plate's top edge on 0-1 % of frames, while both run-10 builds put it on the
# plate's top edge on 100 % of them.  So the CUT test is the discriminator and
# the clearance floor is the backstop, set just under the corpus minimum so no
# approved cutout is retro-failed by it.
CROWN_MIN_CLEAR = 24.0          # design px, backstop
CROWN_CUT_FRAC = 0.25           # of samples with the crown ON the plate's top row


def _norm_frame(bgr: np.ndarray) -> tuple[np.ndarray, float]:
    """The frame plus the DESIGN-px scale (rows / 1920)."""
    return bgr, bgr.shape[0] / 1920.0


def crown_clearance(mp4: Path, every: float = 0.5, *,
                    plate_top: float | None = None) -> dict:
    """Per-sample crown-to-pill clearance on the delivered file, in design px."""
    cap = cv2.VideoCapture(str(mp4))
    if not cap.isOpened():
        raise RuntimeError(f"cannot decode {mp4}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    step = max(1, int(round(every * fps)))
    samples: list[dict] = []
    i = 0
    while True:
        ok, bgr = cap.read()
        if not ok:
            break
        if i % step:
            i += 1
            continue
        i += 1
        f, s = _norm_frame(bgr)
        h, w = f.shape[:2]
        # THE PILL IS A CONNECTED COMPONENT, NOT A COLOUR.  Terracotta is the
        # brand accent: the stage carries rules, rungs and card headers in the
        # same #C4573A, and a row-wise colour count picks the LOWEST of them
        # (1 px "clearances" on every approved run-9 cutout) while a contiguous
        # row run splits the pill itself in two wherever a wide word starves a
        # row of terracotta (a 9 px false floor).  `cutout3_check.pill_component`
        # is the format's own instrument for exactly this and it is reused here.
        m = pill_component(f, {})
        if m is None:                           # between words: no pill, no law
            continue
        ys, xs = np.where(m)
        p_top, p_bot = int(ys.min()), int(ys.max())
        c0, c1 = int(xs.min()), int(xs.max())
        gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        dark = (gray[:, c0:c1 + 1] < CROWN_DARK_L).astype(np.uint8)
        need = CROWN_MIN_RUN * s
        crown = None
        for y in range(p_bot + 1, h - CROWN_PERSIST):
            row = dark[y]
            if row.sum() < need:
                continue
            # the longest contiguous run on this row
            d = np.diff(np.concatenate(([0], row, [0])))
            runs = np.where(d == -1)[0] - np.where(d == 1)[0]
            if runs.size == 0 or runs.max() < need:
                continue
            if dark[y + CROWN_PERSIST].sum() < need:
                continue                        # a speck, not a head
            crown = y
            break
        if crown is None:
            continue
        samples.append({
            "t": round((i - 1) / fps, 2),
            "pill_bottom": round(p_bot / s, 1),
            "crown": round(crown / s, 1),
            "clear": round((crown - p_bot) / s, 1)})
    cap.release()
    if not samples:
        # not a failure and not a pass: a file with no pill/crown pair has
        # nothing for this law to measure, and raising here would take the whole
        # cutout check block down with it.
        return {"file": str(mp4), "frames": n, "fps": round(fps, 3),
                "every_s": every, "samples": 0, "pass": True,
                "note": "no sample carried both a caption pill and a crown "
                        "beneath it — nothing for this law to measure"}
    clears = np.array([x["clear"] for x in samples])
    worst = samples[int(clears.argmin())]
    out = {"file": str(mp4), "frames": n, "fps": round(fps, 3),
           "every_s": every, "samples": len(samples),
           "min_clear_px": float(clears.min()),
           "p05_clear_px": round(float(np.percentile(clears, 5)), 1),
           "median_clear_px": round(float(np.median(clears)), 1),
           "max_clear_px": float(clears.max()),
           "worst": worst, "floor_px": CROWN_MIN_CLEAR}
    if plate_top is not None:
        crowns = np.array([x["crown"] for x in samples])
        at_top = int((crowns <= plate_top + 1.5).sum())
        out["plate_top"] = plate_top
        out["samples_with_crown_at_plate_top"] = at_top
        out["crown_at_plate_top_frac"] = round(at_top / len(samples), 3)
        out["crown_cut_frac_floor"] = CROWN_CUT_FRAC
        out["crown_is_a_cut"] = at_top >= CROWN_CUT_FRAC * len(samples)
    out["pass"] = bool(clears.min() >= CROWN_MIN_CLEAR
                       and not out.get("crown_is_a_cut", False))
    return out


def check_crown_clearance(mp4: Path, fails: list[str], every: float = 0.5,
                          plate_top: float | None = None) -> dict:
    out = crown_clearance(Path(mp4), every, plate_top=plate_top)
    if out.get("crown_is_a_cut"):
        fails.append(
            f"the crown is a CUT, not a head: {out['samples_with_crown_at_plate_top']}"
            f" of {out['samples']} samples put his topmost row on the plate's own "
            f"top edge ({out['plate_top']}).  The plate crop is eating his cap — "
            f"fix the PLATE (pipeline/sam2/plate.py::window headroom), not the seat")
    if not out["samples"]:
        print("F  CROWN CLEARANCE  no pill/crown sample — NOT MEASURED")
        return out
    if out["min_clear_px"] < CROWN_MIN_CLEAR:
        w = out["worst"]
        fails.append(
            f"the caption pill clears his crown by only {out['min_clear_px']} px "
            f"(floor {CROWN_MIN_CLEAR}) at t={w['t']}s — pill bottom {w['pill_bottom']}, "
            f"crown {w['crown']}.  The pill reads as sitting ON his head")
    print(f"F  CROWN CLEARANCE  min {out['min_clear_px']} px, median "
          f"{out['median_clear_px']} px over {out['samples']} samples "
          f"{'OK' if out['pass'] else 'FAIL'}")
    return out


if __name__ == "__main__":
    main()
