#!/usr/bin/env python
"""fallback_sam2.py — THE MATTE FALLBACK: a rejected MatAnyone2 matte is
re-tracked through the SAM2 lane from the reviewed frame-0 contour, with NO
chair object, and finished with a one-frame temporal window.

This is exactly the sequence that fixed geo on 2026-09-14 (run 19) after the
soft-alpha matte smeared the hands and welded the chair to the shirt, and
after the chair-as-second-object SAM2 pass carved the face.  Codex Astra ran
it by hand; this file makes it one command the workflow can call.

What it does, in order (every step leaves its records in the fresh session):
  1. <run>/matting_fallback/<vid>/ gets the plate files copied from the
     MatAnyone2 session and prompts/kf_00000.png = the REVIEWED selection mask
     (selection.py validate must pass on the plate/source/crop hashes).
  2. pipeline/sam2/track.py on the deployed `shorts-factory-sam2` app
     (--gpu h100, --no-chair-object, --tag <tag>) -> alpha_<tag>.mkv.
  3. ship.ship_all(temporal=1, rim 7, mirror pad, edge box from plate.json)
     -> the v5 triple + gates (protrusion, outline, edge).  A refusal stops here.
  4. soft-alpha validation and the headroom check, as the Modal finisher does.
  5. INSTALL into <run>/matting/<vid>: the triple, alpha_v1.mkv, ship_v5.json
     and matting.json rewritten truthfully (backend sam2, temporal 1, hashes,
     headroom re-measured), previous files kept as *.pre_fallback.  The ship
     marker <run>/prep/stages/<vid>.ship.json is re-stamped in the same shape
     with keys.fallback set, and the cutout band frames are re-measured.
  6. matte_review.py runs again on the installed matte so the review agent
     has fresh sheets to look at.

usage: fallback_sam2.py --run <run> --vid <id> [--tag fb1] [--gpu h100]
                        [--reuse-session <dir>]   # skip the track+ship and
                                                 # install an existing triple
                                                 # (tests, resumes)
prints one json line: {"status": "ok"|"REFUSED"|"error", ...}
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

F = Path(__file__).resolve().parents[1].parent
PY = sys.executable
sys.path.insert(0, str(F / "pipeline" / "sam2"))
sys.path.insert(0, str(F / "pipeline" / "matting"))
sys.path.insert(0, str(F / "pipeline" / "prep"))

PLATE_FILES = ("plate_wide_25.mp4", "plate.json", "plate_display_1584x990.mp4",
               "plate.prev_headparity.json", "measure.json", "_cadence_diffs.json")


def digest(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def soft_validate(alpha_webm: Path, w: int, h: int, frames: int) -> dict:
    raw = subprocess.Popen(["ffmpeg", "-v", "error", "-c:v", "libvpx-vp9", "-i", str(alpha_webm),
                            "-vf", "alphaextract", "-pix_fmt", "gray", "-f", "rawvideo", "pipe:1"],
                           stdout=subprocess.PIPE)
    size = w * h
    count, minimum, fractional = 0, 1.0, 0
    while True:
        b = raw.stdout.read(size)
        if not b:
            break
        a = np.frombuffer(b, np.uint8)
        minimum = min(minimum, float(np.mean(a > 127)))
        fractional += int(np.count_nonzero((a > 0) & (a < 255)))
        count += 1
    ok = raw.wait() == 0 and count == frames and minimum >= .02
    return {"ok": ok, "frames": count, "minimum_person_fraction": minimum,
            "fractional_alpha_pixels": fractional}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--vid", required=True)
    ap.add_argument("--tag", default="fb1", help="track tag; also the /vol/<session>/alpha_<tag> name, so a second fallback needs a new tag")
    ap.add_argument("--gpu", default="h100", choices=("a10", "h100"))
    ap.add_argument("--reuse-session", default=None, help="install this session's existing triple instead of tracking")
    ap.add_argument("--reuse-alpha", default=None, help="with --reuse-session: the raw alpha mkv that produced that triple (default: alpha_*.mkv in the session)")
    a = ap.parse_args()
    run = Path(a.run).resolve()
    vid = a.vid
    M = run / "matting" / vid
    S = Path(a.reuse_session).resolve() if a.reuse_session else run / "matting_fallback" / vid
    t0 = time.time()
    rec = {"status": "error", "vid": vid, "session": str(S), "tag": a.tag, "steps": []}

    def fail(msg):
        rec["error"] = msg
        rec["wall_s"] = round(time.time() - t0, 1)
        print(json.dumps(rec))
        return 1

    sel = M / "selection.json"
    if not sel.exists() or json.loads(sel.read_text()).get("status") != "reviewed":
        return fail("no reviewed selection in the MatAnyone2 session; the fallback starts from the reviewed contour")
    mask = Path(json.loads(sel.read_text())["mask"])
    if not mask.exists():
        return fail(f"selection mask missing: {mask}")
    from ship import ship_all, ShipRefused  # noqa: E402
    from headroom import check as check_headroom  # noqa: E402
    import platelib  # noqa: E402

    if not a.reuse_session:
        S.mkdir(parents=True, exist_ok=True)
        for name in PLATE_FILES:
            if (M / name).exists() and not (S / name).exists():
                shutil.copy2(M / name, S / name)
        v = subprocess.run([PY, str(F / "pipeline/matting/selection.py"), "validate",
                            "--plate", str(S / "plate_wide_25.mp4"), "--source", str(run / "cuts" / vid / "master.mp4"),
                            "--crop", str(S / "plate.json"), "--selection", str(sel)], capture_output=True, text=True)
        if v.returncode != 0:
            return fail("selection.py validate refused the reviewed selection against this plate: " + (v.stdout + v.stderr)[-400:])
        rec["steps"].append("selection validated")
        (S / "prompts").mkdir(exist_ok=True)
        shutil.copy2(mask, S / "prompts" / "kf_00000.png")
        (S / "prompts" / "_kf_00000_source.txt").write_text(f"{mask}\n{digest(mask)}\n")
        rec["steps"].append("prompt = reviewed selection mask")
        # 2. the track, no chair object.  An alpha already on disk under this
        #    tag means a previous call was interrupted after the paid track:
        #    resume from it instead of dispatching (and paying) again.
        alpha = S / f"alpha_{a.tag}.mkv"
        if alpha.exists():
            rec["steps"].append(f"track reused from disk ({a.tag})")
        cmd = [PY, "-u", str(F / "pipeline/sam2/track.py"), "--session", str(S), "--plate", str(S / "plate_wide_25.mp4"),
               "--prompts", str(S / "prompts"), "--tag", a.tag, "--gpu", a.gpu, "--no-chair-object"]
        log = run / "prep" / "logs" / f"track_{vid}_fallback_{a.tag}.log"
        log.parent.mkdir(parents=True, exist_ok=True)
        if not alpha.exists():
            with open(log, "w") as lf:
                r = subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT, text=True, timeout=3600)
            rec["track_log"] = str(log)
            if r.returncode != 0 or not alpha.exists():
                return fail(f"track.py failed (rc {r.returncode}); read {log}")
            rec["steps"].append(f"track ok ({a.tag})")
        # 3. finish, temporal 1
        try:
            srec, scan, edge = ship_all(alpha=alpha, plate=S / "plate_display_1584x990.mp4", plate_src=S / "plate_wide_25.mp4",
                                        out_stem=S / f"matte_{vid}_v5", temporal=1, rim_px=7, fps=25, crf=10, pad="mirror",
                                        emit="v5", workers=4, edge_canvas="1080x1920",
                                        edge_box=platelib.edge_box_arg(S / "plate.json"),
                                        plate_json_rec=json.loads((S / "plate.json").read_text()),
                                        display_plate=S / "plate_display_1584x990.mp4", display_crf=12,
                                        exclusion_guard=None)
        except ShipRefused as exc:
            (S / "REFUSED.json").write_text(json.dumps({"error": str(exc), "record": getattr(exc, "rec", None)}, indent=2, default=str))
            rec["status"] = "REFUSED"
            return fail(f"ship refused the fallback matte: {exc}")
        (S / f"matte_{vid}_v5_ship.json").write_text(json.dumps(srec, indent=2, default=str))
        (S / "protrusion_scan.json").write_text(json.dumps(scan, indent=2, default=str))
        rec["steps"].append("ship ok (temporal 1)")
    else:
        alpha = Path(a.reuse_alpha).resolve() if a.reuse_alpha else next(
            (p for p in sorted(S.glob("alpha_*.mkv")) if "exclude" not in p.name and "preheal" not in p.name), None)
        if alpha is None or not alpha.exists():
            return fail("no raw alpha for the reused session (pass --reuse-alpha)")
        rec["steps"].append(f"reused session {S}")

    triple = {k: S / f"matte_{vid}_v5_{k}.webm" for k in ("cut", "rim", "alpha")}
    if not all(p.exists() for p in triple.values()):
        return fail("the v5 triple is incomplete in the session")
    srec = json.loads((S / f"matte_{vid}_v5_ship.json").read_text()) if (S / f"matte_{vid}_v5_ship.json").exists() else {}
    W, H, frames = int(srec.get("width", 1584)), int(srec.get("height", 990)), int(srec.get("frames", 0))
    if not frames:
        frames = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
                                     "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(triple["alpha"])],
                                    capture_output=True, text=True).stdout.strip())
    # 4. validation + headroom on the fallback session
    val = soft_validate(triple["alpha"], W, H, frames)
    if not val["ok"]:
        return fail(f"finished alpha validation failed: {val}")
    display = S / "plate_display_1584x990.mp4" if (S / "plate_display_1584x990.mp4").exists() else M / "plate_display_1584x990.mp4"
    hr = check_headroom(alpha, display, expected_frames=frames, report=S / "headroom.json")
    if not hr.get("pass"):
        return fail(f"headroom failed on the fallback alpha: min {hr.get('min_top_clearance_px')} px")
    rec["steps"].append("validation + headroom ok")

    # 5. install
    stamp = dt.datetime.now().replace(microsecond=0).isoformat()
    for k, p in triple.items():
        dst = M / f"matte_{vid}_v5_{k}.webm"
        if dst.exists() and not (M / f"matte_{vid}_v5_{k}.webm.pre_fallback").exists():
            shutil.copy2(dst, M / f"matte_{vid}_v5_{k}.webm.pre_fallback")
        shutil.copy2(p, dst)
    if (M / "alpha_v1.mkv").exists() and not (M / "alpha_v1.mkv.pre_fallback").exists():
        shutil.copy2(M / "alpha_v1.mkv", M / "alpha_v1.mkv.pre_fallback")
    shutil.copy2(alpha, M / "alpha_v1.mkv")
    for src, name in ((S / f"run_{a.tag}.json", f"run_fallback_{a.tag}.json"),
                      (S / f"matte_{vid}_v5_ship.json", f"ship_fallback_{a.tag}.json"),
                      (S / "protrusion_scan.json", f"protrusion_fallback_{a.tag}.json")):
        if src.exists():
            shutil.copy2(src, M / name)
    hashes = {k: digest(M / f"matte_{vid}_v5_{k}.webm") for k in ("cut", "rim", "alpha")}
    outputs = {k: str(M / f"matte_{vid}_v5_{k}.webm") for k in ("cut", "rim", "alpha")}
    hr2 = check_headroom(M / "alpha_v1.mkv", M / "plate_display_1584x990.mp4", expected_frames=frames, report=M / "headroom.json")
    note = {"date": stamp, "lane": "sam2 fallback: reviewed frame-0 contour as the only prompt, --no-chair-object, "
                                  f"{a.gpu}, tag {a.tag}, ship temporal 1 / rim 7 / mirror pad, no exclusion guard",
            "why": "the MatAnyone2 matte was HELD by the matte viewer test (see review/matte_<id>/); this is the lane that "
                   "fixed geo on 2026-09-14 after the soft alpha smeared the hands and the chair object carved the face",
            "session": str(S), "prompt_mask_sha256": digest(mask), "gates": {
                "protrusion": (srec.get("law48") or {}).get("sides", {}) and {s: (srec["law48"]["sides"][s] or {}).get("verdict") for s in srec["law48"]["sides"]},
                "presenter_loss": (srec.get("presenter_loss") or {}).get("verdict"),
                "edge_clip": (srec.get("edge_clip") or {}).get("verdict")},
            "validation": val, "headroom_min_px": hr2.get("min_top_clearance_px")}
    ship_v5 = json.loads((M / "ship_v5.json").read_text()) if (M / "ship_v5.json").exists() else {}
    ship_v5.update({"status": "ok", "backend": "sam2", "alpha_mode": srec.get("alpha_mode", "sam2"), "temporal": 1,
                    "rim_px": 7, "frames": frames, "width": W, "height": H, "fps": 25, "hashes": hashes, "outputs": outputs,
                    "alpha_source": "alpha_v1.mkv (sam2 fallback)", "fractional_alpha_pixels": val["fractional_alpha_pixels"],
                    "minimum_person_fraction": val["minimum_person_fraction"], "review_status": "needs_final_visual_review",
                    "fallback": note})
    (M / "ship_v5.json").write_text(json.dumps(ship_v5, indent=2))
    mj = json.loads((M / "matting.json").read_text()) if (M / "matting.json").exists() else {"status": "ok"}
    mj.update({"backend": "sam2", "headroom": hr2, "outputs": outputs,
               "ship": {**(mj.get("ship") or {}), "backend": "sam2", "alpha_mode": ship_v5["alpha_mode"], "temporal": 1,
                        "hashes": hashes, "outputs": outputs, "alpha_source": ship_v5["alpha_source"]},
               "fallback": note})
    (M / "matting.json").write_text(json.dumps(mj, indent=2))
    rec["steps"].append("installed into matting/<vid> (previous files *.pre_fallback)")
    # the ship marker, same shape, so every gate downstream sees the fallback
    marker = run / "prep" / "stages" / f"{vid}.ship.json"
    old = json.loads(marker.read_text()) if marker.exists() else {"id": vid, "stage": "ship"}
    keys = {k: v for k, v in (old.get("keys") or {}).items() if isinstance(v, (str, int, float, bool)) or v is None}
    keys.update({"status": "ok", "backend": "sam2", "alpha_mode": ship_v5["alpha_mode"], "temporal": 1, "rim_px": 7,
                 "frames": frames, "width": W, "height": H, "fps": 25, "fallback": f"sam2_nochair_temporal1:{a.tag}",
                 "fractional_alpha_pixels": val["fractional_alpha_pixels"],
                 "minimum_person_fraction": val["minimum_person_fraction"], "review_status": "needs_final_visual_review",
                 "cut_sha256": hashes["cut"], "rim_sha256": hashes["rim"], "alpha_sha256": hashes["alpha"]})
    marker.write_text(json.dumps({"id": vid, "stage": "ship", "status": "ok", "wall_s": round(time.time() - t0, 1),
                                  "at": stamp, "keys": keys}, indent=1))
    rec["steps"].append("ship marker re-stamped")
    # band frames for the cutout chassis
    bf = run / "gen" / "_df" / f"bandframes_{vid}.json"
    if bf.exists():
        shutil.copy2(bf, bf.with_suffix(".json.pre_fallback"))
    bf.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([PY, str(F / "formats/cutout/lib/cutout_depthfield.py"), str(M / f"matte_{vid}_v5_alpha.webm"), str(bf)],
                   check=True, capture_output=True)
    rec["steps"].append("band frames re-measured")
    # 6. fresh evidence
    subprocess.run([PY, str(F / "pipeline/matting/matte_review.py"), "--run", str(run), "--vid", vid], capture_output=True)
    rec.update({"status": "ok", "installed": outputs, "hashes": hashes, "headroom_min_px": hr2.get("min_top_clearance_px"),
                "review_sheets": str(run / "review" / f"matte_{vid}"), "wall_s": round(time.time() - t0, 1)})
    print(json.dumps(rec))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
