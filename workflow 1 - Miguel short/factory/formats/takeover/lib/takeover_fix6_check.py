"""Self-check for takeover_fix6.mp4 (task id: takeover6, closing captions round).

Decodes real frames out of the finished MP4 and re-derives, from the picture
itself, what round 5 changed and everything it promised not to change.

  SEATS        ROUND 5's deliverable.  Every one of the seven compositions is
               re-measured with `takeover_fix5_centroid.py` and must land its
               optical centre on 629 — the centre of [0, 1258), the space above
               the caption pill — with the empty ground above and below it equal.
  ONE TYPE SIZE  ROUND 5's new law, measured on RENDERED GLYPHS rather than read
               off the generator: the pill's own height and the cap-height of
               its type are swept across the whole video and must not vary.
  CONTAINER    size / fps / frame count — Global Law 6 (native 25).
  NO ZOOM      Miguel: "full-face = the regular RAW 0% crop, punches deferred".
               face_frac is measured on every face sample and must sit on the
               0% standard, AND the ratio across each of fix2's eight former
               crop-cut frames must be 1.000 — the picture does not change.
  FULL BLEED   the 0% plate fills the frame (a letterbox would be a flat strip).
  LAW 12       the caption pill's real bounding box, swept every 0.4s over the
               whole video: one stable seat, bottom above 72% of frame height,
               and never outside the 162-918 safe column.  Plus the takeover
               content's own bounding box against the 192-1214 band.
  GHOST RULE   the portal's un-drawn lemniscate cap dot, at its new seat.
  MIX          speech margin on the factory's pinned instrument.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HOME = Path(__file__).resolve().parent
sys.path.insert(0, str(HOME.parents[1] / "pipeline"))  # measure_head.py
sys.path.insert(0, str(HOME))
import takeover_fix6_core as C                                    # noqa: E402

OUT = HOME / "out/takeover_fix6.mp4"
PLATE = HOME / "stage_fix6/v/face_z00.mp4"
FRAMES = HOME / "out/frames_fix6"
W, H = 1080, 1920
FPS = 25
ZSTD = json.loads((HOME.parent / "_shared/zoom_standard.json").read_text())
Z00 = {lv["level_pct"]: lv for lv in ZSTD["levels"]}[0]
ABS_TOL = 0.045          # MediaPipe landmark noise across head tilt
RATIO_TOL = 0.030

CAP_Y = C.CAP_Y
TERRA = np.array([0xC4, 0x57, 0x3A], dtype=np.int16)
TERRA_2 = np.array([0xE6, 0x85, 0x69], dtype=np.int16)
GROUNDS = {"ink": (0x14, 0x14, 0x16), "ink2": (0x24, 0x24, 0x27),
           "cream": (0xF6, 0xF1, 0xEA)}

# ROUND 4 — the face runs are (0.00,1.52) (3.16,4.60) (7.00,13.20) (48.72,50.76).
FACE_RUNS = [(0.00, 1.52), (3.16, 4.60), (7.00, 13.20), (48.72, 50.76)]
FACE_SAMPLES = [
    (0.60, "face — the HOOK, RAW 0%"),
    (1.28, "face — hook, where fix2 punched to 5%"),
    (3.60, "face — 'You think an AI agent'"),
    (4.20, "face — 'loads'"),
    (8.40, "face — 'You see,'"),
    (10.40, "face — 'they introduced'"),
    (12.40, "face — where fix2 punched to the 10% ceiling"),
    (49.60, "face — THE RETURN, 'unbelievable'"),
]
# Adjacent-frame pairs INSIDE the four face runs.  The picture must not change
# across any of them: fix3's four surviving fix2 punch seats, plus four fresh
# seats inside the runs round 4 kept.
FORMER_PUNCHES = [("1.12", 28), ("4.16", 104), ("7.68", 192), ("11.88", 297),
                  ("8.40", 210), ("10.00", 250), ("12.80", 320), ("49.60", 1240)]

# takeover moments where the scene has SETTLED (no feed tiles in flight)
SETTLED = [(2.40, "flash", "ink"), (6.20, "toolwall flooded", "ink2"),
           (14.20, "term on cream", "cream"), (19.40, "ON DEMAND field", "ink2"),
           (23.00, "context is finite", "cream"),
           (29.00, "finite, drained to the keepers", "cream"),
           (52.00, "outro card", "cream")]
IN_FLIGHT = [(35.00, "portal peak, edge feed"),
             (39.20, "portal, infinity resolved"),
             (45.00, "portal, phase 2 — the give-up stack")]

# ROUND 5 — the seats the generator derived, read back so the probes that sit
# ON a scene (the ghost box) follow it instead of being retyped.
SEATS = {u: v["seat"] for u, v in
         json.loads((HOME / "_report_takeover_fix6.json").read_text())
         ["seats"]["units"].items()}
# The un-drawn lemniscate's cap dot: `infinity()` puts path position 0 at
# viewBox (50,50) of a 250x125 glyph centred on the portal's pcy = seat - 40,
# i.e. x = 540 - 125 + 250*0.25 = 477.5, y = pcy exactly.
GHOST_XY = (477, int(SEATS["portal"] - 40))
# ROUND 4 — the two portals were merged, so there is exactly ONE lemniscate in
# the body of the video and it is drawn at 38.28.  These are the pre-draw
# samples: the un-drawn glyph must paint nothing at all.
GHOST_TIMES = [(30.50, "portal opens"), (33.50, "portal, pre-draw"),
               (35.00, "portal peak, pre-draw"), (37.00, "portal, pre-draw")]


def probe() -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
         "-show_entries", "stream=width,height,r_frame_rate,nb_read_frames,duration",
         "-of", "json", str(OUT)], check=True, capture_output=True, text=True).stdout
    return json.loads(out)["streams"][0]


def frame(t: float) -> np.ndarray:
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(OUT), "-frames:v", "1",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.uint8).reshape(H, W, 3).astype(np.int16)


def pill_box(img: np.ndarray) -> tuple[int, int, int, int] | None:
    """The caption pill's real bounding box, measured out of the picture.

    Three traps, all hit while writing this, all worth remembering:
      * "widest TERRA blob below y=1100" merges the toolwall's context rail
        (also TERRA, reaching y=1116) into the pill and reports a 275px caption;
      * counting TERRA pixels per row breaks on a SHORT pill — "See you" is
        276px wide and its white glyphs eat most of the row;
      * a coverage floor set for the pill's flat ends is too strict for the rows
        the GLYPHS cross: at t=8.40 the busiest row is 208 TERRA px inside a
        712px span, i.e. 29% coverage.
    So a row qualifies on its TERRA SPAN with a loose 15% coverage floor, and
    the pill is the LONGEST RUN of qualifying rows in the caption zone, which
    has to be at least 90 rows tall to be a pill at all.
    """
    m = np.abs(img - TERRA).sum(axis=2) < 40
    lo, hi = 1150, 1500
    spans: dict[int, tuple[int, int]] = {}
    for y in range(lo, hi):
        cols = np.flatnonzero(m[y])
        if cols.size == 0:
            continue
        a, b = int(cols[0]), int(cols[-1])
        w = b - a + 1
        if w >= 150 and cols.size >= 0.15 * w:
            spans[y] = (a, b)
    best: list[int] = []
    cur: list[int] = []
    for y in range(lo, hi):
        if y in spans:
            cur.append(y)
            if len(cur) > len(best):
                best = list(cur)
        else:
            cur = []
    if len(best) < 90:
        return None
    return (best[0], best[-1],
            min(spans[y][0] for y in best), max(spans[y][1] for y in best))


def plate_frame(t: float, vf: str | None = None) -> np.ndarray:
    args = ["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(PLATE),
            "-frames:v", "1"]
    if vf:
        args += ["-vf", vf]
    args += ["-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(args, check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.uint8).reshape(H, W, 3).astype(np.int16)


def content_box(img: np.ndarray, ground: str) -> tuple[int, int, int, int] | None:
    """Everything that is not the section's flat ground, ignoring the caption."""
    g = np.array(GROUNDS[ground], dtype=np.int16)
    d = np.abs(img - g).sum(axis=2)
    m = d > 26
    m[1240:1400, :] = False                      # the pill's own band
    ys = np.where(m.sum(axis=1) >= 6)[0]
    xs = np.where(m.sum(axis=0) >= 6)[0]
    if ys.size == 0 or xs.size == 0:
        return None
    return int(ys.min()), int(ys.max()), int(xs.min()), int(xs.max())


SMALL = (135, 240)                      # w, h for the two full-video decodes


def decode_small(path: Path, n_expect: int | None = None) -> np.ndarray:
    """Every frame of a video at 135x240, as one array.  Two of these fit in
    memory comfortably (1351 x 240 x 135 x 3 = 131 MB each) and they are what
    makes the round-4 numbers MEASURED rather than reported: the balance and
    the cut count both come out of the finished picture."""
    w, h = SMALL
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"scale={w}:{h}",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        check=True, capture_output=True).stdout
    a = np.frombuffer(raw, dtype=np.uint8).reshape(-1, h, w, 3).astype(np.int16)
    if n_expect is not None and len(a) < n_expect:
        raise SystemExit(f"{path.name}: decoded {len(a)} frames, expected {n_expect}")
    return a[:n_expect] if n_expect else a


def runs_from_mask(mask: np.ndarray) -> list[tuple[int, int]]:
    """Contiguous True runs as [start, end) frame indices."""
    out, start = [], None
    for i, v in enumerate(mask):
        if v and start is None:
            start = i
        elif not v and start is not None:
            out.append((start, i))
            start = None
    if start is not None:
        out.append((start, len(mask)))
    return out


def margin(path: Path) -> float:
    n = int(0.033 * 16000)
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "16000",
         "-f", "s16le", "-"], check=True, capture_output=True).stdout
    x = np.frombuffer(raw, dtype="<i2").astype(np.float64) / 32768.0
    k = len(x) // n
    db = 20 * np.log10(np.sqrt((x[:k * n].reshape(k, n) ** 2).mean(axis=1)) + 1e-12)
    return float(np.percentile(db, 85) - np.percentile(db, 15))


def main() -> int:
    FRAMES.mkdir(parents=True, exist_ok=True)
    fails: list[str] = []
    report: dict = {}

    st = probe()
    print(f"container: {st['width']}x{st['height']}  {st['r_frame_rate']}  "
          f"{st['nb_read_frames']} frames  {float(st['duration']):.2f}s")
    if (st["width"], st["height"]) != (1080, 1920):
        fails.append(f"size {st['width']}x{st['height']}")
    if st["r_frame_rate"] != "25/1":
        fails.append(f"fps {st['r_frame_rate']} — Global Law 6 wants native 25")
    if int(st["nb_read_frames"]) != 1351:
        fails.append(f"frame count {st['nb_read_frames']} (want 1351)")

    for t, what in FACE_SAMPLES + [(t, w) for t, w, _ in SETTLED] + IN_FLIGHT:
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(OUT),
                        "-frames:v", "1", str(FRAMES / f"t{t:05.2f}.png")], check=True)

    # ---- FULL BLEED --------------------------------------------------------
    print("\nFULL BLEED (top 12 rows of each face frame must be picture, not ground):")
    for t, what in FACE_SAMPLES:
        sd = float(frame(t)[:12].std())
        print(f"  t={t:5.2f}  top-band sd {sd:6.2f}   {what}")
        if sd < 3.0:
            fails.append(f"t={t} top band sd {sd:.2f} — flat ground strip")

    # ---- NO ZOOM -----------------------------------------------------------
    import measure_head as MH
    print(f"\nNO ZOOM (every face second is the 0% standard, "
          f"face_frac {Z00['face_frac_of_1920']:.3f}):")
    res = MH.batch(str(OUT), [t for t, _ in FACE_SAMPLES])
    fracs = []
    for (t, what), r in zip(FACE_SAMPLES, res):
        if not r:
            fails.append(f"no face found at t={t}")
            continue
        fracs.append(r["face_frac"])
        print(f"  t={t:5.2f}  face_frac {r['face_frac']:.3f}   {what}")
        if abs(r["face_frac"] - Z00["face_frac_of_1920"]) > ABS_TOL:
            fails.append(f"t={t} face_frac {r['face_frac']:.3f} off the 0% standard")
    report["face_frac"] = {"min": round(min(fracs), 4), "max": round(max(fracs), 4),
                           "standard": Z00["face_frac_of_1920"]}

    # The decisive test: the rendered face IS the plate, pixel for pixel.  A
    # landmark ratio can wobble 2% on head tilt alone; a pixel comparison
    # cannot.  Each face frame is differenced against face_z00.mp4 at the same
    # timestamp (1:1) and against a 5%-tighter crop of it — the smallest punch
    # fix2 ever used.  If 1:1 is small and 5% is large, the render is the RAW
    # 0% plate and no zoom of any size is present.
    print("\nNO ZOOM, PIXEL PROOF (render vs the RAW 0% plate, rows 0-1200):")
    vf5 = "crop=1026:1824:26:40,scale=1080:1920"
    ident, punched = [], []
    for t, what in FACE_SAMPLES:
        a = frame(t)[:1200]
        b = plate_frame(t)[:1200]
        c = plate_frame(t, vf5)[:1200]
        d0 = float(np.abs(a - b).mean())
        d5 = float(np.abs(a - c).mean())
        ident.append(d0)
        punched.append(d5)
        print(f"  t={t:5.2f}  vs plate 1:1 {d0:5.2f}   vs plate at 5% {d5:5.2f}"
              f"   ({d5/max(d0,0.01):4.1f}x)   {what}")
        if d0 > 6.0:
            fails.append(f"t={t} differs from the RAW 0% plate by {d0:.2f}")
        if d5 < 3 * d0:
            fails.append(f"t={t} is as close to a 5% punch as to the 0% plate")
    report["pixel_proof"] = {"vs_plate_max": round(max(ident), 2),
                             "vs_5pct_min": round(min(punched), 2)}

    # ROUND 3's learning, applied: a LANDMARK measure cannot prove a negative.
    # MediaPipe's face_frac wobbles ~2-3% on head tilt alone, so the ratio
    # across a frame pair is printed for information and ASSERTED on pixels —
    # both frames of every pair must be the plate.
    print("\nNO PUNCHES (frame pairs inside the four face runs):")
    pairs = []
    for label, f in FORMER_PUNCHES:
        a = MH.measure(str(OUT), (f - 1) / FPS - 0.02)
        b = MH.measure(str(OUT), f / FPS - 0.02)
        ratio = (b["face_frac"] / a["face_frac"]) if (a and b) else float("nan")
        da = float(np.abs(frame((f - 1) / FPS + 0.001)[:1200]
                          - plate_frame((f - 1) / FPS + 0.001)[:1200]).mean())
        db_ = float(np.abs(frame(f / FPS + 0.001)[:1200]
                           - plate_frame(f / FPS + 0.001)[:1200]).mean())
        pairs.append({"at": label, "frame": f, "landmark_ratio": round(ratio, 3),
                      "px_vs_plate": [round(da, 2), round(db_, 2)]})
        print(f"  seat {label:6s} f{f-1:<5d}/f{f:<5d}  landmark ratio {ratio:.3f}"
              f"   px vs the plate {da:.2f} -> {db_:.2f}")
        if max(da, db_) > 6.0:
            fails.append(f"frame {f}: {max(da, db_):.2f} from the plate — the "
                         f"picture changed")
    report["no_punches"] = pairs

    # ---- GLOBAL LAW 12: the caption -----------------------------------------
    print("\nLAW 12 — CAPTION PILL, swept every 0.4s over the whole video:")
    rows = []
    t = 0.4
    while t < float(st["duration"]) - 0.4:
        b = pill_box(frame(t))
        if b:
            rows.append((round(t, 2), *b))
        t += 0.4
    if len(rows) < 120:
        fails.append(f"only {len(rows)} caption samples resolved of ~134 swept")
    tops = [r[1] for r in rows]
    bots = [r[2] for r in rows]
    x0s = [r[3] for r in rows]
    x1s = [r[4] for r in rows]
    ctrs = [(r[1] + r[2]) / 2 for r in rows]
    law12 = {
        "samples": len(rows),
        "pill_top_min": min(tops), "pill_top_max": max(tops),
        "pill_bottom_min": min(bots), "pill_bottom_max": max(bots),
        "pill_bottom_max_pct": round(max(bots) / H, 4),
        "pill_centre_min_pct": round(min(ctrs) / H, 4),
        "pill_centre_max_pct": round(max(ctrs) / H, 4),
        "pill_x_min": min(x0s), "pill_x_max": max(x1s),
        "pill_x_max_pct": round(max(x1s) / W, 4),
        "pill_width_max": max(r[4] - r[3] + 1 for r in rows),
    }
    report["law12_caption"] = law12
    print(f"  samples            {law12['samples']}")
    print(f"  pill top           {law12['pill_top_min']} .. {law12['pill_top_max']}")
    print(f"  pill BOTTOM        {law12['pill_bottom_min']} .. "
          f"{law12['pill_bottom_max']}  = {law12['pill_bottom_max_pct']*100:.1f}% of H"
          f"   (law: <= 72.0% / 1382)")
    print(f"  pill centre        {law12['pill_centre_min_pct']*100:.1f}% .. "
          f"{law12['pill_centre_max_pct']*100:.1f}% of H   (STABLE seat)")
    print(f"  pill x             {law12['pill_x_min']} .. {law12['pill_x_max']}"
          f"  = {law12['pill_x_max_pct']*100:.1f}% of W   (law: <= 85.0% / 918)")
    print(f"  widest pill        {law12['pill_width_max']}px")
    if max(bots) > 0.72 * H:
        fails.append(f"LAW 12: pill bottom {max(bots)} is below 72% ({0.72*H:.0f})")
    if max(ctrs) - min(ctrs) > 4:
        fails.append(f"LAW 12: the pill seat moves {max(ctrs)-min(ctrs):.0f}px")
    if max(x1s) > C.SAFE_R or min(x0s) < C.SAFE_L:
        fails.append(f"LAW 12: pill spans {min(x0s)}-{max(x1s)}, outside the "
                     f"{C.SAFE_L:.0f}-{C.SAFE_R:.0f} column")

    # ---- GLOBAL LAW 12: the takeover content --------------------------------
    print("\nLAW 12 — TAKEOVER CONTENT bounding box (settled frames):")
    content = []
    for t, what, ground in SETTLED:
        b = content_box(frame(t), ground)
        if not b:
            fails.append(f"no content found at t={t}")
            continue
        y0, y1, x0, x1 = b
        content.append({"t": t, "scene": what, "y": [y0, y1], "x": [x0, x1]})
        print(f"  t={t:5.2f}  y {y0:4d}..{y1:4d}   x {x0:4d}..{x1:4d}   {what}")
        if y0 < C.TOP - 2 or y1 > C.BOT + 2:
            fails.append(f"t={t} content y {y0}-{y1} leaves the {C.TOP:.0f}-"
                         f"{C.BOT:.0f} band")
        if x0 < C.SAFE_L - 2 or x1 > C.SAFE_R + 2:
            fails.append(f"t={t} content x {x0}-{x1} leaves the safe column")
    report["law12_content"] = content

    print("\n  (in-flight frames, reported not asserted — feed tiles enter "
          "from off-frame):")
    flight = []
    for t, what in IN_FLIGHT:
        b = content_box(frame(t), "ink2")
        if b:
            y0, y1, x0, x1 = b
            flight.append({"t": t, "scene": what, "y": [y0, y1], "x": [x0, x1]})
            print(f"  t={t:5.2f}  y {y0:4d}..{y1:4d}   x {x0:4d}..{x1:4d}   {what}")
    report["law12_in_flight"] = flight

    # ---- ROUND 5: THE SEATS -------------------------------------------------
    # The deliverable, re-measured on the finished MP4 by the same instrument
    # that measured the fix4 baseline the seats were derived from.
    import takeover_fix5_centroid as CT
    before = {u["unit"]: u for u in
              json.loads((HOME / "_centroid_before_fix4.json").read_text())["units"]}
    after = {u["unit"]: u for u in CT.measure(OUT)["units"]}
    print(f"\nROUND 5 — SEATS.  Every composition centred in [0, {CT.PILL_TOP:.0f}), "
          f"whose centre is {CT.REGION_MID:.0f}:")
    print(f"  {'unit':16} {'was':>7} {'now':>7} {'off':>6}   "
          f"{'margins before':>16}   {'margins after':>15}   {'ink top':>7}")
    seats = []
    for u in before:
        x, y = before[u], after[u]
        seats.append({
            "unit": u, "seat": SEATS[u],
            "optical_before": x["optical_centre"], "optical_after": y["optical_centre"],
            "offset_after": y["optical_offset"],
            "mass_before": x["mass_centroid"], "mass_after": y["mass_centroid"],
            "margins_before": [x["margin_above"], x["margin_below"]],
            "margins_after": [y["margin_above"], y["margin_below"]],
            "ink_top_ever": y["ink_top_ever"], "ink_bottom_ever": y["ink_bottom_ever"],
            "ink_between_band_and_pill": y["ink_between_band_and_pill"],
        })
        print(f"  {u:16} {x['optical_centre']:7.1f} {y['optical_centre']:7.1f} "
              f"{y['optical_offset']:+6.1f}   "
              f"{x['margin_above']:7.0f}/{x['margin_below']:<8.0f}   "
              f"{y['margin_above']:7.0f}/{y['margin_below']:<7.0f}   "
              f"{y['ink_top_ever']:7d}")
        # a unit is centred when its optical centre is on the region's centre...
        if abs(y["optical_offset"]) > 2.0:
            fails.append(f"ROUND 5: {u} sits {y['optical_offset']:+.1f}px off "
                         f"the region centre")
        # ...and, independently, when the ground above equals the ground below
        if abs(y["margin_above"] - y["margin_below"]) > 4.0:
            fails.append(f"ROUND 5: {u} margins {y['margin_above']:.0f}/"
                         f"{y['margin_below']:.0f} are not equal")
        # the move may not have pushed anything into the platform's top strip
        if y["above_top10_violation"]:
            fails.append(f"ROUND 5: {u} reaches y={y['ink_top_ever']}, inside "
                         f"the top 10%")
        # nor into the clearance the pill wants under it
        if y["ink_between_band_and_pill"]:
            fails.append(f"ROUND 5: {u} paints {y['ink_between_band_and_pill']}px "
                         f"between the band floor and the pill")
        # and the move must be REAL: fix4's own defect was ~+70px, so a unit
        # that did not move is a unit whose seat never took effect
        if u != "portal" and abs(x["optical_centre"] - y["optical_centre"]) < 20:
            fails.append(f"ROUND 5: {u} barely moved ({x['optical_centre']} -> "
                         f"{y['optical_centre']})")
    report["round5_seats"] = seats
    worst = max(abs(s["offset_after"]) for s in seats)
    imbal = max(abs(s["margins_after"][0] - s["margins_after"][1]) for s in seats)
    print(f"  worst offset from {CT.REGION_MID:.0f}: {worst:.1f}px      "
          f"worst margin imbalance: {imbal:.1f}px      "
          f"(fix4: {max(abs(b['optical_offset']) for b in before.values()):.1f}px / "
          f"{max(abs(b['margin_above']-b['margin_below']) for b in before.values()):.0f}px)")
    report["round5_summary"] = {
        "region": [0.0, CT.PILL_TOP], "region_mid": CT.REGION_MID,
        "worst_offset_after": round(worst, 1),
        "worst_offset_before": round(max(abs(b["optical_offset"])
                                         for b in before.values()), 1),
        "worst_margin_imbalance_after": round(imbal, 1),
        "worst_margin_imbalance_before": round(
            max(abs(b["margin_above"] - b["margin_below"]) for b in before.values()), 1),
    }

    # ---- ROUND 5's NEW LAW: ONE CAPTION TYPE SIZE, MEASURED ON GLYPHS -------
    # Not "the generator emitted one font-size" — the RENDERED type is measured,
    # two independent ways, because the obvious readings are both traps:
    #
    #   * the glyph BOUNDING BOX is content-dependent, not size-dependent.  It
    #     is measured and reported below and lands in two clusters, 41-42px for
    #     a phrase with neither cap nor descender and 50-52px for one with both.
    #     Asserting on it would fail a video whose type never changed.
    #   * `pill_box()`'s height wobbles 112-116 because its per-row TERRA test
    #     is a rounded-cap-and-antialiasing measurement at the pill's edge, and
    #     the wobble does not track pill width, ground or phrase.
    #
    # What IS content-independent and linear in font size:
    #
    #   X-HEIGHT BAND (every frame that carries a caption) — the rows inside the
    #     pill holding at least half the peak glyph ink.  Ascenders and
    #     descenders are a few pixels wide; the x-height band is where every
    #     lowercase letter contributes, so its depth is set by the type size.
    #   EXACT PILL HEIGHT (dark-ground frames only) — with a flat INK/INK_2
    #     ground the pill's mask is exactly "not the ground", so its height is
    #     read without a threshold at all.  Cream sections are excluded on
    #     purpose: a white glyph on cream is within a hair of the ground and the
    #     run breaks mid-pill, which is a measurement artefact, not a defect.
    print("\nROUND 5 — ONE CAPTION TYPE SIZE (measured on rendered glyphs):")
    DARK = {"ink": C.INK, "ink2": C.INK_2}
    xband, gbox, pill_h = [], [], []
    pill_w, pill_cy, pill_bot = [], [], []          # ROUND 6
    t = 0.4
    while t < float(st["duration"]) - 0.4:
        img = frame(t)
        b = pill_box(img)
        if b:
            y0, y1, x0, x1 = b
            pill_w.append(x1 - x0 + 1)
            pill_cy.append((x0 + x1) / 2.0)
            # inset past the rounded ends and the antialiased top/bottom edge
            inner = img[y0 + 6:y1 - 5, x0 + 45:x1 - 44]
            ink = (inner.sum(axis=2) - int(TERRA.sum())) > 180      # lighter than TERRA
            prof = ink.sum(axis=1)
            if prof.max() >= 8:
                xband.append(int((prof >= 0.5 * prof.max()).sum()))
                r = np.flatnonzero(prof >= 3)
                gbox.append(int(r[-1] - r[0] + 1))
            corner = img[300:340, 20:60].reshape(-1, 3).mean(axis=0)
            for hexv in DARK.values():
                g = np.array([int(hexv[i:i + 2], 16) for i in (1, 3, 5)])
                if np.abs(corner - g).sum() < 24:
                    col = np.abs(img[:, (x0 + x1) // 2] - g).sum(axis=1) > 40
                    a = b2 = (y0 + y1) // 2
                    while a > 0 and col[a - 1]:
                        a -= 1
                    while b2 < H - 1 and col[b2 + 1]:
                        b2 += 1
                    pill_h.append(b2 - a + 1)
                    pill_bot.append(b2)            # ROUND 6: exact bottom row
                    break
        t += 0.4
    type_law = {
        "samples": len(xband),
        "x_height_band_values": sorted(set(xband)),
        "x_height_band_spread": max(xband) - min(xband),
        "dark_ground_samples": len(pill_h),
        "exact_pill_height_values": sorted(set(pill_h)),
        "exact_pill_height_spread": (max(pill_h) - min(pill_h)) if pill_h else None,
        "glyph_bbox_values_content_dependent": sorted(set(gbox)),
        "authored_font_px": 56.2,
    }
    report["round5_type"] = type_law
    print(f"  x-height band      {type_law['x_height_band_values']}px over "
          f"{type_law['samples']} captioned frames   spread "
          f"{type_law['x_height_band_spread']}px")
    print(f"  exact pill height  {type_law['exact_pill_height_values']}px over "
          f"{type_law['dark_ground_samples']} dark-ground frames   spread "
          f"{type_law['exact_pill_height_spread']}px")
    print(f"  glyph bbox         {type_law['glyph_bbox_values_content_dependent']}px "
          f"— content-dependent (cap/descender), reported not asserted")
    # A second font size anywhere would move the x-height band several px and
    # the pill height by (56.2 - x) * line-height.
    if type_law["x_height_band_spread"] > 3:
        fails.append(f"ROUND 5: the caption x-height band varies by "
                     f"{type_law['x_height_band_spread']}px — more than one type size")
    if len(type_law["exact_pill_height_values"]) != 1:
        fails.append(f"ROUND 5: exact pill height takes "
                     f"{type_law['exact_pill_height_values']} — more than one type size")
    if type_law["dark_ground_samples"] < 40:
        fails.append(f"ROUND 5: only {type_law['dark_ground_samples']} dark-ground "
                     f"caption frames — the exact reading is not representative")

    # ---- ROUND 6: THE CANONICAL PILL, MEASURED IN THE FINISHED PIXELS ------
    # The generator asserts the CSS; this asserts the picture.  Three readings,
    # each independent of the phrase on screen:
    #   HEIGHT  — the pill box on a flat dark ground, threshold-free.  The
    #             canonical pill is 56.2px Nunito 800 at line-height normal
    #             (78.99px content) plus 2 x 18.8px padding = 114.59px, which
    #             lands on 115-116 rows once the antialiased edge is counted.
    #   BOTTOM  — must sit at or above LAW 12's 0.72 * 1920 = 1382.
    #   WIDTH   — must stay inside the 756px column the platform UI leaves
    #             alone; this is the number the splitter exists to protect.
    P = C.P
    exp_h = P.CAP_PILL_HEIGHT
    canon = {
        "authored": {"font_px": P.CAP_FONT, "padding_px": [P.CAP_PAD_Y, P.CAP_PAD_X],
                     "radius_px": P.CAP_RADIUS, "background": P.CAP_BG,
                     "family": P.CAP_FAMILY, "weight": P.CAP_WEIGHT},
        "expected_pill_height_px": exp_h,
        "measured_pill_height_px": sorted(set(pill_h)),
        "measured_pill_bottom_px": sorted(set(pill_bot)),
        "law12_bottom_limit_px": round(0.72 * H, 1),
        "measured_pill_width_px": [min(pill_w), max(pill_w)] if pill_w else None,
        "seat_budget_px": C.CAP_MAX_W,
        "measured_pill_centre_x": [round(min(pill_cy), 1), round(max(pill_cy), 1)]
        if pill_cy else None,
        "captioned_frames": len(pill_w),
    }
    report["round6_pill"] = canon
    print("\nROUND 6 — THE CANONICAL PILL (measured in the finished pixels):")
    print(f"  pill height        {canon['measured_pill_height_px']}px  "
          f"(authored {exp_h}px = {P.CAP_FONT}px type + 2 x {P.CAP_PAD_Y}px pad)")
    print(f"  pill bottom        {canon['measured_pill_bottom_px']}px  "
          f"(LAW 12 limit {canon['law12_bottom_limit_px']}px)")
    print(f"  pill width         {canon['measured_pill_width_px']}px  "
          f"(seat budget {C.CAP_MAX_W:.0f}px)")
    print(f"  pill centre x      {canon['measured_pill_centre_x']}  (frame centre 540)")
    if any(abs(h - exp_h) > 2 for h in pill_h):
        fails.append(f"ROUND 6: pill height {sorted(set(pill_h))} is not the "
                     f"canonical {exp_h}px")
    if pill_bot and max(pill_bot) > 0.72 * H:
        fails.append(f"ROUND 6: pill bottom {max(pill_bot)} breaks LAW 12's "
                     f"{0.72 * H:.0f}px")
    if pill_w and max(pill_w) > C.CAP_MAX_W:
        fails.append(f"ROUND 6: pill {max(pill_w)}px wide — outside the "
                     f"{C.CAP_MAX_W:.0f}px safe column")
    if pill_cy and (max(pill_cy) - min(pill_cy) > 2 or abs(
            sum(pill_cy) / len(pill_cy) - 540) > 2):
        fails.append(f"ROUND 6: the pill is not centred: {canon['measured_pill_centre_x']}")

    # ---- GHOST RULE ---------------------------------------------------------
    print(f"\nGHOST RULE (24x24 box at {GHOST_XY} — un-drawn lemniscate):")
    gx, gy = GHOST_XY
    for t, what in GHOST_TIMES:
        px = frame(t)[gy - 12:gy + 12, gx - 12:gx + 12]
        d = np.abs(px - TERRA_2).sum(axis=2)
        hits = int((d < 90).sum())
        print(f"  t={t:5.2f}  {what:32s} TERRA_2 px {hits:4d}/576  "
              f"mean rgb {px.reshape(-1,3).mean(axis=0).round(1)}")
        if hits:
            fails.append(f"t={t} paints {hits} TERRA_2 px — ghost dot alive")

    # ---- ROUND 4: THE BALANCE, measured off the picture ---------------------
    # Every frame of the render and of the RAW 0% plate is decoded at 135x240
    # and differenced.  A frame is FACE when it is the plate; anything else is
    # illustration.  Nothing here reads the cut map, so the split, the runs and
    # the longest run are re-derived from the video rather than restated.
    n = int(st["nb_read_frames"])
    vid = decode_small(OUT, n)
    plate = decode_small(PLATE, n)
    d = np.abs(vid[:, :150] - plate[:, :150]).mean(axis=(1, 2, 3))   # rows 0-1200
    is_face = d < 8.0
    gap = float(np.sort(d)[np.argmax(np.diff(np.sort(d)))])          # widest gap
    fr = runs_from_mask(is_face)
    face_frames = int(is_face.sum())
    balance = {
        "frames": n,
        "face_frames": face_frames,
        "face_seconds": round(face_frames / FPS, 2),
        "face_share": round(face_frames / n, 3),
        "illustration_seconds": round((n - face_frames) / FPS, 2),
        "illustration_share": round((n - face_frames) / n, 3),
        "face_runs": [[round(a / FPS, 2), round(b / FPS, 2)] for a, b in fr],
        "face_run_seconds": [round((b - a) / FPS, 2) for a, b in fr],
        "longest_face_run": round(max(b - a for a, b in fr) / FPS, 2),
        "separation": {"max_face_diff": round(float(d[is_face].max()), 2),
                       "min_illustration_diff": round(float(d[~is_face].min()), 2),
                       "widest_gap_at": round(gap, 2)},
        "fix3": {"face_share": 0.449, "longest_face_run": 6.32, "face_runs": 6},
    }
    report["balance"] = balance
    print("\nROUND 4 — FACE / ILLUSTRATION BALANCE (per-frame, vs the RAW 0% plate):")
    print(f"  face          {balance['face_seconds']:6.2f}s  "
          f"{balance['face_share']*100:5.1f}%   (fix3: 24.28s / 44.9%)")
    print(f"  illustration  {balance['illustration_seconds']:6.2f}s  "
          f"{balance['illustration_share']*100:5.1f}%   (fix3: 29.76s / 55.1%)")
    print(f"  face runs     {balance['face_run_seconds']}  "
          f"longest {balance['longest_face_run']}s   (fix3: 6 runs, longest 6.32s)")
    print(f"  separation    face frames differ from the plate by at most "
          f"{balance['separation']['max_face_diff']}, illustration frames by at "
          f"least {balance['separation']['min_illustration_diff']}")
    if not (0.16 <= balance["face_share"] <= 0.30):
        fails.append(f"face share {balance['face_share']:.1%} is outside 16-30%")
    if len(fr) != 4:
        fails.append(f"{len(fr)} face runs measured, the map authors 4")
    if balance["separation"]["min_illustration_diff"] < 30:
        fails.append("face/illustration classes are not cleanly separated")
    if fr[0][0] != 0:
        fails.append("the video does not open on his face (the HOOK guard)")

    # ---- ROUND 4: THE CUT COUNT, measured off the picture --------------------
    # A hard cut is a frame-to-frame jump far above anything motion produces.
    step = np.abs(vid[1:] - vid[:-1]).mean(axis=(1, 2, 3))
    thr = 18.0
    spikes = list(np.flatnonzero(step > thr) + 1)
    # `cut_on` is a 0.03s fromTo, so a cut authored on frame f paints on f+1;
    # consecutive spike frames are ONE cut event, not two.
    events: list[list[int]] = []
    for f in spikes:
        if events and f - events[-1][-1] <= 1:
            events[-1].append(int(f))
        else:
            events.append([int(f)])
    detected = [round(e[0] / FPS, 2) for e in events]
    authored = [1.52, 3.16, 4.60, 7.00, 13.20, 15.16, 20.00, 29.72, 48.72, 50.76]
    gaps = [round(b - a, 2) for a, b in zip(detected, detected[1:])]
    off = [(d, a) for d, a in zip(detected, authored) if abs(d - a) > 1.0 / FPS + 1e-6]
    report["pacing"] = {
        "threshold": thr,
        "detected_cuts": detected, "n_detected": len(detected),
        "authored_cuts": authored, "n_authored": len(authored),
        "fix3_cuts": 13, "min_gap": min(gaps) if gaps else None,
        "loudest_non_cut": round(float(np.sort(step[step <= thr])[-1]), 2),
        "cut_magnitudes": [round(float(step[e[0] - 1:e[-1]].max()), 1) for e in events],
    }
    report["pacing"]["separation"] = round(
        min(report["pacing"]["cut_magnitudes"]) / report["pacing"]["loudest_non_cut"], 1)
    print(f"\nROUND 4 — PICTURE CHANGES (frame-to-frame jump > {thr:.0f}):")
    print(f"  detected      {len(detected)}  {detected}")
    print(f"  magnitudes    {report['pacing']['cut_magnitudes']}")
    print(f"  authored      {len(authored)}  (fix3: 13, fix2: 33)")
    print(f"  min gap       {min(gaps):.2f}s   loudest NON-cut frame "
          f"{report['pacing']['loudest_non_cut']} (his head moving on the face "
          f"plate)   separation {report['pacing']['separation']}x")
    if len(detected) != len(authored) or off:
        fails.append(f"detected cuts {detected} do not match authored {authored}")
    if len(detected) >= 13:
        fails.append(f"{len(detected)} picture changes — fix3 had 13, round 4 "
                     f"wants fewer")
    # The detector has to be unambiguous: the SMALLEST cut must stand well clear
    # of the loudest frame of ordinary motion, or "10 cuts" is a threshold
    # artefact rather than a measurement.
    if report["pacing"]["separation"] < 3.0:
        fails.append(f"cuts are only {report['pacing']['separation']}x the "
                     f"loudest motion frame — not a clean measurement")

    m = margin(OUT)
    print(f"\nMIX: speech margin {m:.2f} dB (s16le, 33ms)  "
          f"approved run-7 corpus 15.85-23.70")
    report["speech_margin_db"] = round(m, 2)
    if m < 15.85:
        fails.append(f"speech margin {m:.2f} dB is below the approved corpus")

    report["fails"] = fails
    (HOME / "_check_takeover_fix6.json").write_text(json.dumps(report, indent=2))
    print("\n" + ("FAIL: " + "; ".join(fails) if fails else "ALL CHECKS PASS"))
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
