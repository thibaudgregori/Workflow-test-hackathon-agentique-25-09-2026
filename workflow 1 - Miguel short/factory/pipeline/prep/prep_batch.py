#!/usr/bin/env python3
"""THE PREP STAGE — the whole batch's mechanical work, once, in parallel.

WHAT IT REPLACES.  Before a run-9 builder could design anything it had to: cut
its raw, derive a plate, build a frame-0 prompt, dispatch a Modal track, wait
seven minutes for it, ship the matte, and scan for pointing cues.  Ten builders
did that ten times, each one waiting alone on its own GPU.  None of it needs a
model and none of it needs to be serial.

WHAT IT DOES.  One thread per recording, all of them at once:

    (a) CUT       take detection + the 4K master + 48 kHz audio + the tight
                  transcript                                        [cutlib]
    (b) PLATE     measure, the BiRefNet master sweep, and the plate built
                  OVER-WIDE from the start                          [platelib]
    (c) PROMPT0   the frame-0 silhouette and the wing cut           [promptlib]
    (b2) DISPLAY  the x264 crf 12 display plate, re-cut from the 4K master at
         PLATE    the chassis's paint size.  Started IN THE BACKGROUND the
                  moment the plate stage lands, so its ~10-20 s runs under
                  prompt0, cues and the track dispatch instead of inside ship
    (d) TRACK     SAM2 on the deployed Modal app — dispatched for EVERY
                  recording at once, so Modal runs the batch concurrently
                  instead of one video at a time.  Since 2026-09-03 the H100
                  lane is the default (2.73x faster per frame, 1.23x the cost
                  per frame) and the track ALSO SHIPS: the three VP9 layers and
                  both gates run in the container that made the alpha
    (e) SHIP      the matte set and its gates: the in-app self-healing leak
                  check, the protrusion gate, and LAW 44's edge clip, with the
                  over-wide plate's own box handed in as --edge-box.  With
                  `--ship-local` this is the old laptop-side ship.py run, kept
                  for parity measurements
    (f) CUES      pointing_cues.scan, and the source card for every cue whose
                  post was supplied                                [sourcelib]
    (g) PACKAGE   <run>/prep/<id>.json per video, <run>/prep/_batch.json for the
                  batch, both carrying per-stage wall-clock and the measured
                  Modal cost

NO LLM ANYWHERE.  Scribe is ASR, BiRefNet and SAM2 are segmenters, and every
other number is measured off a file.

A STAGE THAT FAILS DOES NOT KILL THE BATCH.  Each stage records its own status,
and the video carries on as far as it can — a package with `cut: ok` and
`track: error` is still worth having, because the cut is the expensive part to
redo and the builder can see exactly where to pick up.

THE INTAKE LIST.  A JSON array.  The rich shape is

    {"id": "sparkchrome",
     "recording": "2026-09-01 14-11-03",
     "opening_key": ["gemini", "spark", "can", "now"],
     "sign_off_key": ["catch", "you", "in", "the", "next"],
     "opening_families": [[...], [...]],          # instead of opening_key
     "expected": {"take_index": 209, ...},        # hand-verified pins, all asserted
     "keyterms": ["Gemini Spark"],
     "wings": {"wing_right": 718, "wing_right_rows": "400,620"},
     "cues": [{"cue_i": 0, "url": "https://x.com/.../status/...",
               "body": "<byte-identical prefix>", "claim": "<span inside body>"}]}

The daily-shorts shape `{id, recording, lane, transcript, topic}` is accepted
too and degrades gracefully: without an opening key the cut stage cannot run, so
it reports `SKIPPED_NEEDS_KEY` and the plate stage runs off an existing
`cuts/<id>/master.mp4` if one is already there.

    prep_batch.py --run <run dir> --intake <json> [--workers 5] [--skip track]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import shutil
import sys
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

WORKSPACE = Path.home() / "Documents" / "Workspace"
F = WORKSPACE / "projects/personal/content/shorts-factory"
PY = WORKSPACE / ".venv/bin/python"
MOVIES = Path.home() / "Movies"

sys.path.insert(0, str(F / "pipeline"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from prep import cutlib, platelib, promptlib, sourcelib          # noqa: E402
import costs as COSTS                                            # noqa: E402

TRACK = F / "pipeline/sam2/track.py"
SHIP = F / "pipeline/sam2/ship.py"
SAM2 = F / "pipeline/sam2"
SESSIONS = F / "pipeline/sam2/sessions"

_print_lock = threading.Lock()

# vid -> (Popen, out_path, t0).  The display-plate cut is the one piece of the
# old ship stage that CANNOT move into the container (it needs the 4K master),
# so it is started the moment the plate lands and runs under everything after
# it.  Measured 2026-09-03: 9.6 s for astramath's 706 frames, ~20 s for
# costpertask's 1300 — all of it off the critical path now.
_DISPLAY: dict[str, tuple] = {}
_display_lock = threading.Lock()


def log(vid: str, msg: str) -> None:
    with _print_lock:
        print(f"[{time.strftime('%H:%M:%S')}] {vid:20s} {msg}", flush=True)


# =============================================================================
# THE COST LEDGER (2026-09-04)
# =============================================================================
# The prep stage is where most of a run's Modal money is spent, and until now
# the only place it was written down was `_batch.json` — a file that exists when
# the WHOLE batch closes, that a `--skip` re-run can shadow, and whose totals
# had to be re-added by hand into every bench note.  Each of these helpers
# writes the number the stage ALREADY MEASURED into `<run>/costs.jsonl` the
# moment that stage lands.  Nothing is re-priced, and a ledger failure can
# never fail a stage (`COSTS.safe_record` swallows and prints).
def _lane_label(st: dict) -> str:
    lane = st.get("lane")
    if lane:
        return str(lane).upper()
    gpu = str(st.get("gpu") or "")
    parts = [p for p in gpu.split() if p.upper() != "NVIDIA"]
    return " ".join(parts[:1]).upper() if parts else ""


def _record_epoch(rec_path) -> float | None:
    """The container's own start epoch — what makes a re-track on the same tag
    a SECOND ledger row rather than a replacement of the first."""
    try:
        return json.loads(Path(rec_path).read_text()).get("t_import_epoch")
    except Exception:                                            # noqa: BLE001
        return None


def ledger_track(run, vid: str, st: dict, rec_path, *,
                 note: str = "SAM2 track") -> None:
    usd = float(st.get("cost_usd") or 0.0)
    if usd <= 0:
        return
    COSTS.safe_record(
        run, "modal", "track", usd, video=vid,
        units=(f"{st.get('billed_container_seconds')} container-s "
               f"{_lane_label(st)}").strip(),
        note=note,
        ref=COSTS.call_ref(run, rec_path, _record_epoch(rec_path)))


def ledger_ship(run, vid: str, st: dict, *, note: str = "matte ship") -> None:
    usd = float(st.get("cost_usd") or 0.0)
    if usd <= 0:                    # `--ship-local` is free; no row, by design
        return
    COSTS.safe_record(
        run, "modal", "ship", usd, video=vid,
        units=f"{st.get('billed_container_seconds')} container-s CPU",
        note=f"{note} ({st.get('where') or 'modal-cpu'})",
        # the ship json's NAME is the same for every tag, so the billed seconds
        # (falling back to the price itself) are what make one ship one row
        ref=COSTS.call_ref(run, st.get("ship_json"),
                           st.get("billed_container_seconds") or f"usd{usd}"))


def ledger_sweep(run, vid: str, pkg: dict) -> None:
    sweep = ((pkg.get("stages", {}).get("plate") or {}).get("sweep") or {})
    lane = sweep.get("lane") or {}
    usd = float(lane.get("measured_cost_usd") or 0.0)
    if usd <= 0:                    # the local CPU fallback costs nothing
        return
    COSTS.safe_record(
        run, "modal", "sweep", usd, video=vid,
        units=(f"{lane.get('billed_container_seconds')} container-s "
               f"{lane.get('gpu') or ''}").strip(),
        note="BiRefNet master sweep (the plate solve)",
        ref=COSTS.call_ref(run, sweep.get("file") or sweep.get("out"),
                           lane.get("container") or lane.get("t_import_epoch")))


def ledger_scribe(run, vid: str, tight: dict | None) -> None:
    """ElevenLabs Scribe v2 on the cut audio.  The ONLY paid call in this
    pipeline whose price is not measured by the caller — the API returns a
    duration and no cost — so `costs.scribe_usd` prices it by audio seconds and
    every row says in its note that it is an estimate."""
    if not tight:
        return
    secs = tight.get("audio_duration_secs")
    usd = COSTS.scribe_usd(secs)
    if usd <= 0:
        return
    COSTS.safe_record(
        run, "elevenlabs", "scribe", usd, video=vid,
        units=f"{secs} s audio",
        note=f"Scribe v2 on the cut audio, {COSTS.SCRIBE_RATE_SOURCE}",
        ref=COSTS.call_ref(run, tight.get("file"), secs))


def mark_stage(package: dict, stage: str, rec: dict) -> None:
    """Write the PER-RECORDING, PER-STAGE marker the workflow waits on.

    Added 2026-09-04 (Miguel: "we can make the split screen and whiteboard stop
    waiting for the cutout").  `_batch.json` only exists when the WHOLE batch is
    finished, and the package json is rewritten at the end too — so a workflow
    that wants to start a recording's plan the moment THAT recording's cut is
    done had nothing to watch.  Now every stage stamps
    `<run>/prep/stages/<vid>.<stage>.json` the instant it lands:

        {"id", "stage", "status", "wall_s", "at", "keys": {...the stage's
         own terminal fields, the paths a downstream agent needs...}}

    It is a MARKER, not a second source of truth: the package json and
    `_batch.json` stay exactly as they were.  A failure to write one is
    swallowed — a marker never kills a stage.

    A STAGE THIS RUN DID NOT EXECUTE CANNOT UN-PASS ONE (geo, run 19,
    2026-09-13).  The package json has obeyed that law since run 14 ("A RE-RUN
    MERGES, IT DOES NOT ERASE") but the marker — the file the GATES actually
    poll — was rewritten unconditionally, so a targeted repair rerun launched
    with `--skip track,ship` stamped `"status": "skipped"` over a `track`/`ship`
    marker that said `ok`, and the matte gate would then have polled a shipped,
    paid matte as if it had never run.  A `skipped`/`reused` record now leaves a
    PASSING marker alone; every real verdict this run measured still lands.
    """
    try:
        run = package.get("run")
        if not run:
            return
        d = Path(run) / "prep" / "stages"
        d.mkdir(parents=True, exist_ok=True)
        path = d / f"{package.get('id', 'unknown')}.{stage}.json"
        if rec.get("status") in ("skipped", "reused") and path.exists():
            try:
                prior = json.loads(path.read_text())
            except Exception:                  # noqa: BLE001 — truncated marker
                prior = None
            if isinstance(prior, dict) and prior.get("status") in ("ok", "reused"):
                return
        keys = {k: v for k, v in rec.items()
                if k not in ("traceback",) and isinstance(
                    v, (str, int, float, bool, type(None)))}
        path.write_text(
            json.dumps({"id": package.get("id"), "stage": stage,
                        "status": rec.get("status"),
                        "wall_s": rec.get("wall_s"),
                        "at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "keys": keys}, indent=1))
    except Exception:                      # noqa: BLE001 — a marker is never a gate
        pass


class Stage:
    """A stage's wall-clock and status, recorded whether it worked or not."""

    def __init__(self, package: dict, vid: str, name: str):
        self.package, self.vid, self.name = package, vid, name

    def __enter__(self):
        self.t0 = time.time()
        log(self.vid, f"{self.name} ...")
        self.rec = {"status": "running"}
        self.package["stages"][self.name] = self.rec
        return self.rec

    def __exit__(self, exc_type, exc, tb):
        self.rec["wall_s"] = round(time.time() - self.t0, 1)
        if exc is None:
            # the body may have set its own terminal status (reused, skipped,
            # SKIPPED_NEEDS_KEY, REFUSED); only the placeholder becomes "ok"
            if self.rec.get("status") == "running":
                self.rec["status"] = "ok"
            log(self.vid, f"{self.name} ok  {self.rec['wall_s']}s")
            mark_stage(self.package, self.name, self.rec)
            return False
        # a body that already ruled REFUSED (a gate) keeps that word: "error"
        # would let reconcile() mistake a refused render for a recoverable one
        # (run 12, 2026-09-03: two edge-clipped ships came back "ok" that way)
        if self.rec.get("status") != "REFUSED":
            self.rec["status"] = "error"
        self.rec["error"] = f"{exc_type.__name__}: {exc}"
        self.rec["traceback"] = traceback.format_exc()[-3000:]
        log(self.vid, f"{self.name} ERROR  {self.rec['wall_s']}s  {exc}")
        mark_stage(self.package, self.name, self.rec)
        return True                       # swallowed: a stage never kills a video


def _key(value):
    """['a', ['b','c']] -> ('a', ('b','c')) — a key with alternative tokens."""
    if value is None:
        return None
    return tuple(tuple(t) if isinstance(t, (list, tuple)) else t for t in value)


def _raw_path(row: dict) -> Path:
    rec = row.get("recording") or ""
    p = Path(rec)
    if p.suffix and p.exists():
        return p
    for cand in (MOVIES / f"{rec}.mp4", MOVIES / rec):
        if cand.exists():
            return cand
    return MOVIES / f"{rec}.mp4"


def _raw_transcript(row: dict, run: Path) -> Path:
    """The Scribe transcript for this recording, wherever it already exists.

    A TRANSCRIPT BELONGS TO A RECORDING, NOT TO A RUN (run 22, 2026-09-15).
    This used to look only in THIS run's intake folder, so a recording that was
    transcribed in an earlier run came back missing and every stage failed as a
    cascade - cut FileNotFoundError, plate "no cut master", cues "no tight
    transcript". Run 21 survived it only because its launcher agent happened to
    copy the files in by hand; run 22's did not, and the whole batch died in
    0.2 s. The same recording always has the same transcript, so find it in any
    sibling run and copy it in, which also keeps this run self-contained for
    delivery.
    """
    if row.get("transcript"):
        p = Path(row["transcript"])
        if p.exists():
            return p
    rec = row.get("recording")
    here = run / f"intake/transcripts/{rec}.json"
    if here.exists():
        return here
    for sib in sorted(run.parent.glob("shorts_run*/intake/transcripts"), reverse=True):
        cand = sib / f"{rec}.json"
        if cand.is_file():
            here.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(cand, here)
            print(f"[transcript] {rec}: copied from {sib.parent.parent.name}", flush=True)
            return here
    return here


# =============================================================================
# stage b2 - the display plate, in the background
# =============================================================================
def display_spec(session: Path, cut_dir: Path) -> dict | None:
    """The display size and the file it lands in, off the session's plate.json.

    THE DISPLAY SIZE IS NOT OPTIONAL.  Without it the layers come out at the
    PLATE's own size and the chassis upscales them in the browser — that is the
    v4 face-detail defect ship.py warns about (plate 6.98 -> 5.65 on the
    finished short, 19 % of the face smeared).  It also makes --edge-box
    unusable: the box must BE the encoded size, never a scale of it
    (cutout6_check check 23), and the box is the plate painted at PLATE_SCALE.
    So both are derived from plate.json together.
    """
    pj = session / "plate.json"
    master = cut_dir / "master.mp4"
    if not pj.exists() or not master.exists():
        return None
    rec = json.loads(pj.read_text())
    pw, ph = rec.get("plate_size", [1080, 900])
    w = int(round(pw * platelib.PLATE_SCALE))
    h = int(round(ph * platelib.PLATE_SCALE))
    return dict(w=w, h=h, display=f"{w}x{h}", master=str(master),
                plate_json=str(pj), file=str(session / f"plate_display_{w}x{h}.mp4"))


def start_display_plate(vid: str, session: Path, cut_dir: Path,
                        logs: Path) -> dict | None:
    """Kick `ship.build_display_plate` off in its own process and return.

    Same function the CLI calls, so the x264 line, the `plate.json` vf
    re-targeting and the up-to-date cache check are not duplicated here.
    """
    spec = display_spec(session, cut_dir)
    if spec is None:
        return None
    logs.mkdir(parents=True, exist_ok=True)
    code = (
        "import sys; from pathlib import Path\n"
        f"sys.path.insert(0, {str(SAM2)!r})\n"
        "import ship\n"
        f"p = ship.build_display_plate(Path({spec['master']!r}), "
        f"Path({str(session)!r}), ({spec['w']}, {spec['h']}), crf=12, fps=25)\n"
        "print(p)\n")
    handle = (logs / f"display_{vid}.log").open("w")
    proc = subprocess.Popen([str(PY), "-u", "-c", code],
                            stdout=handle, stderr=subprocess.STDOUT)
    with _display_lock:
        _DISPLAY[vid] = (proc, Path(spec["file"]), time.time(),
                         str(logs / f"display_{vid}.log"))
    log(vid, f"display plate {spec['display']} started in the background")
    return spec


def await_display_plate(vid: str, pkg: dict, timeout: float = 900) -> Path | None:
    """Join the background cut and record it as its own stage."""
    with _display_lock:
        item = _DISPLAY.pop(vid, None)
    if item is None:
        return _cached_display_plate(vid, pkg)
    proc, out, t0, logf = item
    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
    st = {"status": "ok" if (proc.returncode == 0 and out.exists()) else "error",
          "wall_s": round(time.time() - t0, 1), "file": str(out), "log": logf,
          "bytes": out.stat().st_size if out.exists() else 0}
    if st["status"] != "ok":
        st["error"] = f"display plate cut exited {proc.returncode}; see {logf}"
    pkg.setdefault("stages", {})["display_plate"] = st
    log(vid, f"display plate {st['status']}  {st['wall_s']}s")
    return out if st["status"] == "ok" else None


def _probe_display(path: Path) -> dict:
    """width/height/frame count of a plate file (packet count: exact, fast)."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
         "-show_entries", "stream=width,height,nb_read_packets", "-of", "json",
         str(path)], capture_output=True, text=True, check=True).stdout
    st = json.loads(out)["streams"][0]
    return {"width": int(st["width"]), "height": int(st["height"]),
            "frames": int(st["nb_read_packets"])}


def _cached_display_plate(vid: str, pkg: dict) -> Path | None:
    """Reuse a display plate that already sits on disk, validated, not trusted.

    `_DISPLAY` is process-local: a dispatcher started in a fresh process (the
    production-v2 matting handoff, run 16, 2026-09-06) found no entry even
    though every display MP4 existed, and matting died with 'Missing display
    plate' while recording 0.35 s.  The fallback accepts the file only when it
    is the one `display_spec` names for THIS session, is newer than plate.json
    (ship.build_display_plate's own currency rule), has exactly the spec's
    width/height and the same frame count as the tracked plate.  Anything else
    is a miss, never a silent re-cut: the caller decides.
    """
    session = Path(pkg.get("session") or "")
    cut_dir = Path(pkg.get("cut_dir") or "")
    spec = display_spec(session, cut_dir) if session.exists() else None
    if spec is None:
        return None
    out, pj = Path(spec["file"]), session / "plate.json"
    st = {"status": "error", "file": str(out), "cached": True}
    if not out.exists():
        st["error"] = "no display plate on disk and none in progress"
    elif out.stat().st_mtime <= pj.stat().st_mtime:
        st["error"] = "display plate on disk is older than plate.json"
    else:
        try:
            got = _probe_display(out)
            want_frames = None
            plate_file = (pkg.get("stages", {}).get("plate") or {}).get("plate")
            if plate_file and Path(plate_file).exists():
                want_frames = _probe_display(Path(plate_file))["frames"]
            ok = (got["width"], got["height"]) == (spec["w"], spec["h"]) and \
                (want_frames is None or got["frames"] == want_frames)
            # Source-hash proof: the reviewed selection binds source + crop by
            # sha256; the display plate is cut from that same master with that
            # same plate.json, so both must still hash to what was reviewed.
            sel = session / "selection.json"
            if sel.exists():
                import hashlib
                ident = json.loads(sel.read_text()).get("identity", {})
                def _sha(f):
                    h = hashlib.sha256()
                    with open(f, "rb") as fh:
                        for chunk in iter(lambda: fh.read(1 << 22), b""):
                            h.update(chunk)
                    return h.hexdigest()
                proof = {"source_sha256": _sha(cut_dir / "master.mp4"),
                         "crop_sha256": _sha(pj)}
                proof["matches_selection"] = (
                    proof["source_sha256"] == ident.get("source_sha256")
                    and proof["crop_sha256"] == ident.get("crop_sha256"))
                st["hash_proof"] = proof
                if not proof["matches_selection"]:
                    ok = False
                    st["error"] = "source/crop hash differs from the reviewed selection"
            st.update(got, plate_frames=want_frames, bytes=out.stat().st_size,
                      status="reused" if ok else "error")
            if not ok and "error" not in st:
                st["error"] = (f"display plate {got['width']}x{got['height']} "
                               f"{got['frames']}f does not match spec "
                               f"{spec['display']} / plate {want_frames}f")
        except (subprocess.CalledProcessError, KeyError, ValueError) as e:
            st["error"] = f"display plate probe failed: {e}"
    pkg.setdefault("stages", {})["display_plate"] = st
    log(vid, f"display plate {st['status']} (cached on disk)"
             + (f"  {st['error']}" if st["status"] != "reused" else ""))
    return out if st["status"] == "reused" else None


# =============================================================================
# stages a-c and f, per video
# =============================================================================
def prep_front(row: dict, run: Path, *, skip: set[str], stride: int,
               sessions: Path = SESSIONS, sweep_local: bool = False,
               display_plate: bool = True, no_chair: bool = False,
               reset_prompt: bool = False) -> dict:
    vid = row["id"]
    session = sessions / vid
    cuts = run / "cuts" / vid
    gen = run / "gen"
    gen.mkdir(parents=True, exist_ok=True)
    package: dict = {
        "id": vid, "run": str(run), "recording": row.get("recording"),
        "gpu": (row.get("gpu") or None),   # SAM2 lane override, see --gpu
        "session": str(session), "cut_dir": str(cuts), "stages": {},
        "no_chair_object": bool(no_chair or row.get("no_chair_object")),
        "started": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    # ---- (a) CUT -----------------------------------------------------------
    with Stage(package, vid, "cut") as st:
        if "cut" in skip or (cuts / "master.mp4").exists():
            st.update({"status": "reused",
                       "note": "cuts/<id>/master.mp4 already exists",
                       "master": str(cuts / "master.mp4")})
        elif not (row.get("keep_words") or row.get("opening_key") or row.get("opening_families")):
            st.update({"status": "SKIPPED_NEEDS_KEY",
                       "note": ("no opening_key / opening_families on the intake "
                                "row.  Take detection is decided by the CONTENT "
                                "rule and the content rule needs the script's own "
                                "opening; there is no model here to guess it.")})
        else:
            edl = cutlib.build_cut(
                vid=vid, raw=_raw_path(row),
                raw_transcript=_raw_transcript(row, run), out_dir=cuts,
                opening_key=_key(row.get("opening_key")),
                opening_families=[_key(k) for k in row["opening_families"]]
                if row.get("opening_families") else None,
                sign_off_key=_key(row.get("sign_off_key")),
                expected=row.get("expected"), keyterms=row.get("keyterms"),
                allow_uncorroborated=bool(row.get("allow_uncorroborated")),
                head_lead=float(row.get("head_lead", cutlib.HEAD_LEAD)),
                transcribe="transcribe" not in skip,
                keep_words=row.get("keep_words"))   # the model's cut, when the intake row carries one (2026-09-22)
            d = edl["take_detection"]
            st.update({
                "master": str(cuts / "master.mp4"),
                "audio": str(cuts / "audio.m4a"),
                "face_plates": [str(cuts / n) for n in
                                ("face_full_hd.mp4", "face_bottom_hd.mp4")],
                "edl": str(cuts / "edl.json"),
                "transcript_tight": edl.get("tight_transcript", {}).get("file"),
                "cut_master_duration_s": edl["cut_master_duration"],
                "take": {"word_index": d["take_word_index"],
                         "start_s": d["take_start_s"],
                         "words": d["take_words"],
                         "of_raw_words": d["raw_words"],
                         "openings": len(d["openings_found"])},
                "corroboration": d["corroboration"],
                "analysis_wav_written": False,
                # the Scribe pass's own billable quantity, so the ledger row
                # can be re-derived from the package alone (2026-09-04)
                "tight_audio_duration_s": (edl.get("tight_transcript") or {})
                .get("audio_duration_secs"),
            })
            ledger_scribe(run, vid, edl.get("tight_transcript"))

    master = cuts / "master.mp4"

    # ---- (b) PLATE ---------------------------------------------------------
    with Stage(package, vid, "plate") as st:
        if "plate" in skip:
            # A REPAIR RE-RUN MUST NOT REBUILD THE PLATE (grokemail, run 21,
            # 2026-09-15).  `build_plate` has no reuse path: it re-measures, re-
            # crops and re-encodes, so a matting re-run that merely corrected the
            # reviewed selection would replace plate_wide_25.mp4 and plate.json
            # and break the very identity the reviewed selection is bound to --
            # `selection.validate` would then refuse the contour and the repair
            # would need a whole fresh selection review.  A bare "skipped",
            # though, leaves the production matting adapter with no
            # `stages.plate.plate` and it dies with "No valid prepared plate".
            # So a skipped plate REUSES the one already on disk, validated the
            # way `_cached_display_plate` validates its own: plate.json present,
            # the file it names present, and the file's real geometry equal to
            # what plate.json recorded.  Anything else stays "skipped".
            pj = session / "plate.json"
            try:
                rec = json.loads(pj.read_text())
                f = Path(rec["file"])
                pw, ph = rec["plate_size"]
                probe = _probe_display(f) if f.exists() else {}
                assert probe.get("width") == int(pw) and probe.get("height") == int(ph), probe
                st.update({"status": "reused",
                           "note": "plate skipped; reusing the plate already on disk",
                           "plate": str(f), "crop": rec.get("crop"),
                           "plate_size": rec.get("plate_size"),
                           "scale_k": rec.get("scale_k"),
                           "head_px_on_canvas": rec.get("head_px_on_canvas"),
                           "plate_json": str(pj),
                           "reused_geometry": probe})
            except Exception as exc:                       # noqa: BLE001
                st["status"] = "skipped"
                st["note"] = f"no reusable plate on disk ({type(exc).__name__}: {exc})"
        elif not master.exists():
            raise RuntimeError("no cut master to derive a plate from")
        else:
            rec = platelib.build_plate(
                master=master, session=session,
                sweep_json=gen / f"_birefnet_master_{vid}.json", stride=stride,
                overwide=not row.get("no_overwide"),
                sweep_local=sweep_local)
            ow = rec.get("overwide") or {}
            st.update({
                "plate": rec["file"], "crop": rec["crop"],
                "plate_size": rec["plate_size"], "scale_k": rec["scale_k"],
                "head_px_on_canvas": rec["head_px_on_canvas"],
                "overwide_applied": bool(ow.get("applied")),
                "extension_master_px": (ow.get("extension") or {}),
                "plate_box": (ow.get("plate_box") or {}),
                "face_dx_pct": (ow.get("nothing_on_canvas_moves") or {}).get("face_dx_pct"),
                "visible_window_drift_master_px":
                    (ow.get("nothing_on_canvas_moves") or {}).get("visible_window_drift_master_px"),
                "sweep": ow.get("sweep"),
                "plate_json": str(session / "plate.json"),
            })

    # ---- (b2) DISPLAY PLATE, in the background ------------------------------
    # It only needs plate.json and the master, so it can run under prompt0, the
    # cue scan and the whole GPU track instead of inside ship.
    # The display plate depends on the PLATE, not on whether matting ships:
    # a --skip ship run (selection review before any GPU) still needs the exact
    # final display geometry (2026-09-06, run 16 audit).  It is skipped only when
    # the plate itself failed or was skipped.
    plate_ok = (package["stages"].get("plate") or {}).get("status") in ("ok", "reused")
    if display_plate and plate_ok:
        try:
            start_display_plate(vid, session, cuts, run / "prep" / "logs")
        except Exception as exc:                       # never kill the batch
            package["stages"]["display_plate"] = {
                "status": "error", "wall_s": 0.0,
                "error": f"{type(exc).__name__}: {exc}"}

    # ---- (c) PROMPT0 -------------------------------------------------------
    with Stage(package, vid, "prompt0") as st:
        if not plate_ok and "prompt0" not in skip:
            # DEPENDENCY GUARD (2026-09-06): no plate, no frame to prompt on.
            # Mark it blocked without retries or paid work instead of crashing
            # BiRefNet twice on a missing file.
            st["status"] = "blocked"
            st["error"] = "blocked: plate stage is not ok"
        elif "prompt0" in skip:
            st["status"] = "skipped"
        else:
            # ONE RETRY FOR A CRASHED STAGE (Miguel, 2026-09-03, run 12): the
            # BiRefNet subprocess died with "recursive_mutex lock failed" when
            # four prompt0s ran at once on the laptop, and the same take ran
            # in 7.5 s on the resume.  A native flake is not a verdict, so the
            # stage gets a second attempt after a short pause; a second crash
            # is the real error and is reported as before.
            rec = None
            PROMPT0_RETRIES = 2                       # Miguel: "up to two retries"
            st["retries"] = []
            for attempt in range(1, PROMPT0_RETRIES + 2):
                try:
                    rec = promptlib.build_prompt0(
                        session=session,
                        plate=session / "plate_wide_25.mp4",
                        wings=row.get("wings"),
                        reset_prompt=bool(reset_prompt
                                          or row.get("reset_prompt")))
                    break
                except Exception as exc:              # noqa: BLE001
                    st["retries"].append({"attempt": attempt,
                                          "error": f"{type(exc).__name__}: {exc}"[:400]})
                    if attempt > PROMPT0_RETRIES:
                        raise
                    log(vid, f"prompt0 crashed (attempt {attempt}, {type(exc).__name__}); "
                             f"retrying in 5 s")
                    time.sleep(5)
            w = rec["wings"]
            st["prompt_guard"] = rec.get("prompt_guard")
            st["prompt0_status"] = rec.get("status")
            if rec.get("status") == "kept":
                log(vid, "prompt0 KEPT the repaired frame-0 prompt "
                         f"(differs from prompts/_original/: "
                         f"{(rec.get('prompt_guard') or {}).get('removed_px')} px removed); "
                         "pass --reset-prompt to re-derive and lose the repair")
            st.update({
                "prompt_png": rec["prompt_png"], "overlay_png": rec["overlay_png"],
                "wings_source": rec["wings_source"],
                "wing_right": w.get("wing_right"), "wing_left": w.get("wing_left"),
                "wing_cut_applied": bool(w.get("wing_cut_applied")),
                "wing_review": bool(w.get("wing_review")),
                "wing_review_note": w.get("wing_review_note"),
                "removed_px": rec["kf_report"]["removed"]["px"]
                if isinstance(rec["kf_report"].get("removed"), dict) else None,
                "prompt_area_px": rec["kf_report"]["prompt"]["area"],
            })

            # ── THE CHAIR IS A SECOND OBJECT (Miguel, 2026-09-04) ──────────
            # The standard cleaning pass.  `chairprompt` looks for a headrest
            # wing beside the head on frame 0, on BOTH sides, and writes the box
            # and the clicks next to the prompt.  `build_track_cmd` picks the
            # file up and hands it to the tracker as `exclude=`.  No wing found
            # on a side means no exclusion object for that side, i.e. exactly
            # the old single-object behaviour.  `--no-chair-object` forces it.
            st["chair_prompt"] = chair_prompt_stage(
                session, no_chair=bool(package["no_chair_object"]),
                override=row.get("chair_prompt"))

    # ---- (f) CUES ----------------------------------------------------------
    with Stage(package, vid, "cues") as st:
        if "cues" in skip:
            st["status"] = "skipped"
        else:
            import pointing_cues                                  # noqa: PLC0415
            tt = cuts / "transcript_tight.json"
            if not tt.exists():
                raise RuntimeError("no tight transcript to scan for cues")
            words = [w for w in json.loads(tt.read_text())["words"]
                     if w.get("type") == "word"]
            cues = pointing_cues.scan(words)
            (gen / f"_cues_{vid}.json").write_text(
                json.dumps({"vid": vid, "cues": cues}, indent=1))
            answered = sourcelib.answer_cues(
                vid=vid, cues=cues, spec=row.get("cues"), run=run,
                assets=run / "assets", plans=run / "plans")
            st.update({
                "cue_count": len(cues), "cues_json": str(gen / f"_cues_{vid}.json"),
                "answered": answered,
                "needs_source": [c["cue_i"] for c in answered
                                 if c["status"] == "NEEDS_SOURCE"],
                "cards": [c["card"]["file"] for c in answered
                          if c["status"] == "CARD"],
            })
    return package


# =============================================================================
# stage d - the fleet track, and stage e - ship
# =============================================================================
CHAIR_JSON = "chair_prompt.json"
MODAL = Path(PY).parent / "modal"          # the venv's own CLI


def chair_prompt_stage(session: Path, *, no_chair: bool = False,
                       override: dict | None = None) -> dict:
    """Find the headrest wing on frame 0, both sides, and write the prompt.

    Never raises: a detector that throws must not cost a paid GPU run, and a
    miss is a legitimate answer (no exclusion object, old behaviour).  The
    record carries the side, the box, the clicks and the luma stats, and the
    proof overlay lands in the session next to prompt0's own.
    """
    import sys as _sys                                          # noqa: PLC0415
    _sam2 = str(Path(__file__).resolve().parent.parent / "sam2")
    if _sam2 not in _sys.path:
        _sys.path.insert(0, _sam2)
    out = session / CHAIR_JSON
    if no_chair:
        out.unlink(missing_ok=True)
        return {"status": "skipped", "why": "--no-chair-object", "found": []}
    try:
        import chairprompt                                      # noqa: PLC0415
        rec = chairprompt.chair_prompt(
            session / "plate_wide_25.mp4",
            session / "prompts" / "birefnet_00000.png",
            overlay_png=session / "prompts" / "chair_overlay_00000.png")
        # ── AN EXPLICIT INTAKE ROW OUTRANKS THE INSTRUMENT ─────────────────
        # Same rule `derive_wings` already follows for `wings`.  A side the
        # detector cannot see safely can be supplied by hand — measured need:
        # `hermesdesktop`'s RIGHT wing, which the sandwich test loses because
        # his hair touches it, and which the only window that finds it also
        # finds on seven faces.  The override records its own `source` so the
        # record never pretends a hand prompt was measured.
        for side in ("left", "right"):
            o = (override or {}).get(side)
            if not o:
                continue
            was = dict(rec.get(side) or {})
            rec[side] = dict(found=True, side=side,
                             box=[int(v) for v in o["box"]],
                             points=[[int(x) for x in pt] for pt in o["points"]],
                             n_positive=sum(1 for pt in o["points"] if pt[2] == 1),
                             n_negative=sum(1 for pt in o["points"] if pt[2] == 0),
                             source=o.get("source", "hand (intake row)"),
                             replaced_detector_verdict=was.get("found", False),
                             detector_why=was.get("why"))
        rec["found"] = [s for s in ("left", "right") if (rec.get(s) or {}).get("found")]
        if override:
            rec["overridden_sides"] = sorted(override)
            chairprompt.overlay(chairprompt.plate_frame(
                session / "plate_wide_25.mp4", 0), rec,
                session / "prompts" / "chair_overlay_00000.png")
        out.write_text(json.dumps(rec, indent=1))
        return {"status": "ok", "json": str(out),
                "overlay": rec.get("overlay"),
                "band": rec.get("band"), "found": rec.get("found", []),
                "overridden_sides": rec.get("overridden_sides"),
                "left": {k: v for k, v in (rec.get("left") or {}).items()
                         if k in ("found", "why", "box", "points", "rows",
                                  "cols", "area_px", "luma", "rows_with_run",
                                  "run_width", "source",
                                  "replaced_detector_verdict",
                                  "detector_why")},
                "right": {k: v for k, v in (rec.get("right") or {}).items()
                          if k in ("found", "why", "box", "points", "rows",
                                   "cols", "area_px", "luma", "rows_with_run",
                                   "run_width", "source",
                                   "replaced_detector_verdict",
                                   "detector_why")}}
    except Exception as exc:                                    # noqa: BLE001
        out.unlink(missing_ok=True)
        return {"status": "error", "found": [],
                "error": f"{type(exc).__name__}: {exc}"[:400]}


def build_track_cmd(pkg: dict, *, session: Path, plate: Path, prompts: Path,
                    tag: str, lane: str, limit: int | None, remote_ship: bool,
                    emit: str, display_plate: Path | None) -> tuple[list, str]:
    """The `track.py` argv, in ONE place, so a repair round re-tracks with
    exactly the command the first dispatch used — same lane, same ship flags,
    same edge box.  `display_plate` is the file `await_display_plate` joined;
    None means this machine has nothing for the container to paint at."""
    cmd = [str(PY), "-u", str(TRACK), "--session", str(session),
           "--plate", str(plate), "--prompts", str(prompts), "--tag", tag,
           "--gpu", lane]
    # THE STANDARD PASS CARRIES THE CHAIR.  The file only exists when
    # `chair_prompt_stage` found a wing, so an absent file is the old
    # single-object path and needs no flag.
    chair = session / CHAIR_JSON
    if chair.exists() and not pkg.get("no_chair_object"):
        cmd += ["--exclude-json", str(chair)]
    if limit:
        cmd += ["--limit", str(limit)]
    ship_where = "laptop"
    if remote_ship:
        spec = display_spec(session, Path(pkg["cut_dir"]))
        box = platelib.edge_box_arg(session / "plate.json") \
            if (session / "plate.json").exists() else None
        if display_plate is None or spec is None:
            pkg["stages"]["ship"] = {
                "status": "error", "wall_s": 0.0,
                "error": ("no display plate, so the container cannot ship "
                          "at the chassis's paint size (that is the v4 "
                          "face-detail defect); shipped nothing")}
        else:
            cmd += ["--ship", "--emit", emit, "--pad", "mirror",
                    "--display", spec["display"],
                    "--display-plate", str(display_plate),
                    "--plate-json", str(session / "plate.json")]
            if box:
                cmd += ["--edge-box", box]
            ship_where = "modal"
    return cmd, ship_where


def dispatch_tracks(packages: dict, run: Path, *, tag: str, limit: int | None,
                    gpu: str = "h100", remote_ship: bool = True,
                    emit: str = "v5") -> dict[str, subprocess.Popen]:
    """Fire every ready track at the deployed app AT ONCE and return the handles.

    `track.py` hydrates the deployed function by name, so N local processes mean
    N Modal containers, not a queue.  This is the whole point of prepping a batch
    rather than a video: the GPU minutes overlap instead of stacking.

    Since 2026-09-03 the call also carries the SHIP: `--ship` plus the display
    plate the background stage cut, so the three VP9 layers and both gates run
    in the container that produced the alpha instead of on this machine after a
    26-52 MB download.  `--ship-local` (remote_ship=False) keeps the old lane.
    """
    procs: dict[str, subprocess.Popen] = {}
    logs = run / "prep" / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    for vid, pkg in packages.items():
        session = Path(pkg["session"])
        plate = session / "plate_wide_25.mp4"
        prompts = session / "prompts"
        if not (plate.exists() and any(prompts.glob("kf_*.png"))):
            pkg["stages"]["track"] = {
                "status": "skipped",
                "reason": "no plate or no frame-0 prompt to track from"}
            continue
        # -u: the log is a FILE, so a buffered child prints nothing until it
        # exits, and a seven-minute stage looks like a hang
        lane = str(pkg.get("gpu") or gpu).lower()   # the intake row may override
        dp = await_display_plate(vid, pkg) if remote_ship else None
        cmd, ship_where = build_track_cmd(
            pkg, session=session, plate=plate, prompts=prompts, tag=tag,
            lane=lane, limit=limit, remote_ship=remote_ship, emit=emit,
            display_plate=dp)
        handle = (logs / f"track_{vid}.log").open("w")
        procs[vid] = subprocess.Popen(cmd, stdout=handle, stderr=subprocess.STDOUT)
        pkg["stages"]["track"] = {"status": "running", "tag": tag, "lane": lane,
                                  "cmd": " ".join(cmd), "ship_where": ship_where,
                                  "log": str(logs / f"track_{vid}.log"),
                                  "_t0": time.time()}
        log(vid, f"track dispatched (tag {tag}, ship {ship_where})")
    return procs


def track_fields(rec_path: Path) -> dict:
    """The stage fields a finished `run_<tag>.json` supplies, in ONE place, so
    a repair round's re-track is recorded exactly like the first one."""
    rec = json.loads(Path(rec_path).read_text())
    return {
        "status": "ok", "run_record": str(rec_path),
        "alpha": rec.get("alpha_local"),
        "frames_tracked": rec.get("frames_tracked"),
        "gpu": rec.get("gpu"),
        "track_seconds": rec.get("track_seconds"),
        "billed_container_seconds": rec.get("billed_container_seconds"),
        "cost_usd": rec.get("measured_cost_usd"),
        "cost_breakdown_usd": rec.get("cost_breakdown_usd"),
        "seams": rec.get("seams"),
        "seam_warning": rec.get("seam_warning"),
        "ship_seconds": rec.get("ship_seconds"),
        "ship_cost_usd": rec.get("ship_cost_usd"),
        "total_cost_usd": rec.get("total_cost_usd"),
        "leak_check": {k: v for k, v in (rec.get("leak_check") or {}).items()
                       if k in ("verdict", "healed", "needs_human")},
    }


def collect_tracks(packages: dict, procs: dict, *, tag: str, poll: float = 10.0,
                   timeout: float = 5400) -> None:
    t0 = time.time()
    pending = dict(procs)
    while pending and time.time() - t0 < timeout:
        for vid, proc in list(pending.items()):
            if proc.poll() is None:
                continue
            del pending[vid]
            pkg = packages[vid]
            st = pkg["stages"]["track"]
            st["wall_s"] = round(time.time() - st.pop("_t0"), 1)
            rec_path = Path(pkg["session"]) / f"run_{tag}.json"
            # 3 is track.py's "the track succeeded, a SHIP GATE refused".  The
            # alpha is on disk and is exactly what bolsterfix/wingfix need, so
            # it is not an error on the track.
            if proc.returncode not in (0, 3) or not rec_path.exists():
                st["status"] = "error"
                st["error"] = (f"track exited {proc.returncode}; see "
                               f"{st['log']}")
                log(vid, f"track ERROR after {st['wall_s']}s")
                continue
            st.update(track_fields(rec_path))
            # THE TRACK'S OWN MONEY ONLY.  The ship the GPU container spawned
            # on the CPU lane is on this same record (`ship_cost_usd`), but it
            # is booked by `collect_remote_ship`, which is the stage that owns
            # it — booking it twice is how a ledger starts lying.
            ledger_track(pkg.get("run"), vid, st, rec_path)
            log(vid, f"track ok  {st['wall_s']}s  ${st.get('cost_usd')}")
        if pending:
            time.sleep(poll)
    for vid, proc in pending.items():
        proc.kill()
        st = packages[vid]["stages"]["track"]
        st["status"] = "timeout"
        st["wall_s"] = round(time.time() - st.pop("_t0", t0), 1)
        log(vid, "track TIMED OUT — killed")


def _probe_wh(path: Path) -> tuple[int, int] | None:
    try:
        o = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "csv=p=0",
             str(path)], capture_output=True, text=True,
            timeout=60).stdout.strip().split(",")
        return int(o[0]), int(o[1])
    except Exception:
        return None


def _edge_summary(rec: dict) -> dict:
    edge = rec.get("edge_clip") or {}
    return {
        "windows": edge.get("windows"),
        "box": edge.get("box"),
        "defects": {k: v.get("defect_frames")
                    for k, v in (edge.get("edges") or {}).items()},
        "min_limb_margin_canvas_px": {
            k: v.get("min_limb_margin_canvas_px")
            for k, v in (edge.get("edges") or {}).items()},
    }


def collect_remote_ship(pkg: dict, *, tag: str, emit: str = "v5") -> None:
    """The layers came back WITH the track.  This only checks and records them.

    No encoding, no gates, no download: the container ran `ship.ship_all` and
    `track.py` wrote the three webms and the ship json into the session.  What
    is left is the paperwork — the display plate this machine cut, the files'
    own dimensions, and the two gate verdicts.  A REFUSAL is an `error` with the
    gate's sentence, exactly as the laptop ship was: the remedy is
    bolsterfix/wingfix plus a re-track, never an `--allow-*`.
    """
    vid = pkg["id"]
    with Stage(pkg, vid, "ship") as st:
        session = Path(pkg["session"])
        rec_path = session / f"run_{tag}.json"
        if not rec_path.exists():
            # THE PAID TRACK IS NOT LOST BECAUSE THE LAST LINE CRASHED.
            # `track.py` writes the record after downloading the alpha and
            # collecting the ship, so a crash there leaves every artifact on
            # disk and only the record missing.  Pull the container's own copy
            # off the volume and carry on (trycrm/run 14).
            recover_run_record(session, tag, vid=vid)
        if not rec_path.exists():
            raise RuntimeError(f"no run record to read the ship out of: "
                               f"{rec_path}")
        run_rec = json.loads(rec_path.read_text())
        ship = run_rec.get("ship") or {}
        st["where"] = ship.get("where") or "modal-cpu"
        st["ship_seconds"] = ship.get("ship_seconds")
        st["client_wall_s"] = ship.get("client_wall_seconds")
        st["cost_usd"] = ship.get("measured_cost_usd")
        st["billed_container_seconds"] = ship.get("billed_container_seconds")
        st["cpu_cores"] = ship.get("cpu_cores")
        st["workers"] = ship.get("workers")
        st["ffmpeg"] = ship.get("ffmpeg")
        st["display"] = ship.get("display")
        st["protrusion_verdict"] = (ship.get("protrusion") or {}).get("verdict")
        st["gate_log"] = (ship.get("log") or "")[-2500:]
        if not ship:
            raise RuntimeError("the track ran without --ship, so there is no "
                               "matte to collect; re-run without --skip ship")
        if ship.get("status") == "refused":
            st["status"] = "REFUSED"
            st["gate"] = ship.get("gate")
            st["gate_refusal"] = ship.get("verdict")
            raise RuntimeError(
                f"the container's {ship.get('gate')} gate refused the matte — "
                "read gate_refusal; the fix is bolsterfix/wingfix + a re-track, "
                "never --allow-protrusion")
        sj = Path(ship.get("ship_json_local") or
                  (session / f"matte_{vid}_{emit}_ship.json"))
        if not sj.exists():
            raise RuntimeError(f"the ship json did not land: {sj}")
        rec = json.loads(sj.read_text())
        # the three files exist AND are the size the chassis will paint
        want = (rec.get("width"), rec.get("height"))
        bad = []
        for k, v in (rec.get("outputs") or {}).items():
            p = Path(v)
            if not p.exists() or p.stat().st_size == 0:
                bad.append(f"{k}: missing or empty ({p})")
                continue
            got = _probe_wh(p)
            if got and tuple(got) != want:
                bad.append(f"{k}: {got[0]}x{got[1]}, expected "
                           f"{want[0]}x{want[1]}")
        if bad:
            raise RuntimeError("the layers the container returned are wrong: "
                               + "; ".join(bad))
        st.update({
            "ship_json": str(sj), "outputs": rec.get("outputs"),
            "frames": rec.get("frames"),
            "display_plate": rec.get("display_plate"),
            "edge_box": (rec.get("edge_clip") or {}).get("box"),
            "layer_bytes": {k: Path(v).stat().st_size
                            for k, v in (rec.get("outputs") or {}).items()},
            "edge_clip": _edge_summary(rec),
        })
        ledger_ship(pkg.get("run"), vid, st)


def ship_matte(pkg: dict, run: Path, *, tag: str, emit: str = "v5",
               allow_outline: str | None = None) -> None:
    """ship.py on the alpha, ON THIS MACHINE: protrusion, outline, LAW 44.

    `allow_outline` is intentionally narrow: the anatomy-veto path may re-ship
    an UNCHANGED alpha only after the refusal proves that straight-p95 is the
    sole failing instrument while persistence and retained-dark stay inside
    their ceilings.  No other repair path passes it.

    THE PARITY LANE.  Since 2026-09-03 the default is `collect_remote_ship` —
    the container that tracked also ships — and this stays reachable through
    `--ship-local` so the two can be measured against each other.
    """
    vid = pkg["id"]
    with Stage(pkg, vid, "ship") as st:
        st["where"] = "laptop"
        session = Path(pkg["session"])
        alpha = session / f"alpha_{tag}.mkv"
        if not alpha.exists():
            raise RuntimeError(f"no alpha to ship: {alpha}")
        out = session / f"matte_{vid}_{emit}"
        # THE DISPLAY SIZE IS NOT OPTIONAL.  Without --master/--display, ship.py
        # emits the layers at the PLATE's own size and the chassis upscales them
        # in the browser — that is the v4 face-detail defect ship.py warns about
        # (plate 6.98 -> 5.65 on the finished short, 19 % of the face smeared).
        # It also makes --edge-box unusable: the box must BE the encoded size,
        # never a scale of it (cutout6_check check 23), and the box is the plate
        # painted at PLATE_SCALE.  So both are derived from plate.json together.
        plate_json = session / "plate.json"
        rec = json.loads(plate_json.read_text())
        pw, ph = rec.get("plate_size", [1080, 900])
        disp_w = int(round(pw * platelib.PLATE_SCALE))
        disp_h = int(round(ph * platelib.PLATE_SCALE))
        master = Path(pkg["cut_dir"]) / "master.mp4"
        cmd = [str(PY), str(SHIP), "--alpha", str(alpha),
               "--plate", str(session / "plate_wide_25.mp4"),
               "--out", str(out), "--emit", emit, "--pad", "mirror"]
        # Tracks made by the temporal-support lane label their diagnostic as the
        # EFFECTIVE exclusion union.  Pass that exact aligned video back through
        # ship so generic fill_holes/median/polish cannot resurrect the chair.
        # Old run records wrote raw logits under the same filename and carry no
        # label, so they are deliberately not promoted to guards retroactively.
        run_rec = session / f"run_{tag}.json"
        if run_rec.exists():
            rr = json.loads(run_rec.read_text())
            guard = session / f"alpha_{tag}_exclude.mkv"
            if str(rr.get("exclude_alpha_kind") or "").startswith("effective") \
                    and guard.exists():
                cmd += ["--exclusion-guard", str(guard)]
                st["exclusion_guard"] = str(guard)
        if master.exists():
            cmd += ["--master", str(master), "--display", f"{disp_w}x{disp_h}"]
            st["display"] = f"{disp_w}x{disp_h}"
        box = platelib.edge_box_arg(plate_json)
        if box:
            cmd += ["--edge-box", box]
        if allow_outline:
            cmd += ["--allow-outline", allow_outline]
            st["allow_outline"] = allow_outline
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        st["cmd"] = " ".join(cmd)
        st["edge_box"] = box
        ship_json = Path(f"{out}_ship.json")
        st["stdout_tail"] = proc.stdout[-1500:]
        if proc.returncode != 0:
            st["status"] = "REFUSED"
            st["gate_refusal"] = (proc.stdout + proc.stderr)[-2500:]
            raise RuntimeError("ship.py refused the matte — read gate_refusal; "
                               "the fix is bolsterfix/wingfix + a re-track, "
                               "never --allow-protrusion")
        rec = json.loads(ship_json.read_text()) if ship_json.exists() else {}
        st.update({
            "ship_json": str(ship_json),
            "outputs": rec.get("outputs"),
            "frames": rec.get("frames"),
            "protrusion_verdict": (rec.get("protrusion") or {}).get("verdict",
                                                                    "clean"),
            "edge_clip": _edge_summary(rec),
        })


# =============================================================================
# THE AUTO-REPAIR LOOP — two verification rounds inside the main loop
# =============================================================================
# Miguel, 2026-09-03, after run 12 refused three of four recordings and every
# refusal needed a human to run a KNOWN MECHANICAL REPAIR:
#
#     "we should auto-detect it and fix it.  I wanted to have at least two
#      verification loops inside of the main loop so we don't lose so much
#      time."
#
# So the ship verdict is no longer the end of the batch.  A REFUSAL that names
# one of the two repairable gates is fixed the way a human fixes it, re-tracked
# on the same GPU lane and re-shipped through the same lane — up to TWO rounds,
# and only then reported as a failure.  Nothing here weakens a gate: there is no
# `--allow-*` anywhere in this file, the gates run unchanged on every round, and
# a matte still only ships when both of them pass on their own terms.
#
#   PROTRUSION with `wings` in the scan  ->  wingfix.py   (the headrest wing
#       hanging beside the head; the columns and the row band come from the
#       gate's OWN verdict — `x0`/`x1`, the ledge's top row and the shoulder row
#       it hangs above — not from a guess)
#   PROTRUSION with no wings             ->  bolsterfix.py (furniture above the
#       shoulder line; it derives its own window from `protrusion.scan()`)
#   OUTLINE (LAW 48)                     ->  wingfix.py, on the side the gate
#       refused, with the window the gate MEASURED: the rows of its own head
#       band plus a margin, and the cut column set from the deepest inward
#       column of retained plate-dark pixels.  A wedge is not a rectangle, so
#       one window rarely takes all of it — round 2 re-measures round 1's alpha
#       and cuts again, which is the two-window chain the hermeskanban repair
#       had to be driven by hand (`references/evidence/hermeskanban_outline_repair/review/`
#       `repair_hermeskanban_outline.md`), now done by the loop.
#   EDGE CLIP                            ->  a WIDER PLATE.  Under LAW 44's
#       2026-09-03 ruling this can only fire when the plate border is ON SCREEN,
#       so the remedy the law itself prescribes is the whole fix: take the
#       gate's worst negative margin on that side, add the 24 px aim, convert to
#       master px through the plate's own scale, add the extension that side
#       already has, and hand it to `solve_overwide` as `need_floor_master_px`.
#       Then rebuild the plate, re-run prompt0 on it, re-track, re-ship.  A side
#       whose border is already off screen is NEVER widened — it does not gate.
#   anything else                        ->  no retry, reported verbatim.
REPAIR_MAX_ROUNDS = 2
REPAIRABLE_GATES = ("protrusion", "outline", "edge_clip")
# THE CORRECTIVE KEYFRAME CADENCE FOR A LAW 48 REPAIR.  `wingfix`'s default
# leaves gaps of up to 60 frames between corrective masks and SAM2 regrows the
# wedge inside them, which is the flicker half of Miguel's complaint.  40 gave
# hermeskanban 72 masks at a max gap of 10 frames and took its shoulder-row edge
# jitter from 15.2 px p95 to 3, matching the accepted costpertask matte.
OUTLINE_CHUNK = 40


def _tag_at(base: str, r: int) -> str:
    """`v1` + round 2 -> `v3`.  The round's alpha, run record and prompts all
    carry it, and every earlier tag STAYS ON DISK: a refused alpha is the input
    the next fix reads, and it is the evidence for the refusal."""
    m = re.match(r"^(.*?)(\d+)$", base)
    if m:
        return f"{m.group(1)}{int(m.group(2)) + r}"
    return f"{base}_r{r}"


def refusal_gate(pkg: dict) -> str | None:
    """Which gate refused this ship, or None when it is not a gate refusal.

    Both lanes mark the stage `REFUSED` before raising: `collect_remote_ship`
    also carries the container's own `gate` field, and `ship_matte` carries
    ship.py's printed sentence.  A refusal on `edge_box` (a stale plate.json) is
    deliberately NOT repairable — it means two files disagree, and re-tracking
    would only pay for the same disagreement again."""
    st = (pkg.get("stages") or {}).get("ship") or {}
    if st.get("status") != "REFUSED":
        return None
    if st.get("gate") in REPAIRABLE_GATES:
        return st["gate"]
    txt = " ".join(str(st.get(k) or "")
                   for k in ("gate_refusal", "stdout_tail", "gate_log"))
    if "PROTRUSION: this alpha carries furniture" in txt:
        return "protrusion"
    if "OUTLINE (LAW 48)" in txt:
        return "outline"
    if "EDGE CLIP: this matte's trim is CUT BY THE PLATE" in txt:
        return "edge_clip"
    # a refusal recovered off disk carries no sentence, only the report the
    # gate wrote before refusing — gated windows in it ARE the edge refusal
    if ((st.get("edge_clip") or {}).get("windows")):
        return "edge_clip"
    return None


def refusal_verdict(pkg: dict) -> str:
    """The gate's own sentence, quoted verbatim for the round record."""
    st = (pkg.get("stages") or {}).get("ship") or {}
    for k in ("gate_refusal", "stdout_tail", "gate_log", "error"):
        if st.get(k):
            return str(st[k]).strip()
    return "(no verdict recorded)"


def gate_scan(session: Path, alpha: Path, out_json: Path, logf: Path) -> dict:
    """`ship.protrusion_gate` on this alpha, in its own process.

    The SAME function the ship lane calls, so the windows this reads are the
    windows that refused.  It runs out of process for two reasons: it decodes a
    whole alpha into RAM, and `ship.py` is importable but not re-entrant-cheap.
    The printed line carries the columns but NOT the row band, and wingfix needs
    the band, so the full scan is written to JSON instead of parsed."""
    code = (
        "import json, sys\n"
        f"sys.path.insert(0, {str(SAM2)!r})\n"
        "import ship\n"
        f"scan = ship.protrusion_gate({str(alpha)!r}, "
        f"{str(session / 'plate_wide_25.mp4')!r})\n"
        "def _j(o):\n"
        "    return o.item() if hasattr(o, 'item') else str(o)\n"
        f"open({str(out_json)!r}, 'w').write(json.dumps(scan, default=_j))\n")
    with open(logf, "a") as h:
        h.write(f"\n--- protrusion re-scan {alpha.name} ---\n")
        h.flush()
        subprocess.run([str(PY), "-u", "-c", code], stdout=h,
                       stderr=subprocess.STDOUT, timeout=3600, check=True)
    return json.loads(Path(out_json).read_text())


def wing_args(wings: list) -> tuple[list, dict]:
    """The wingfix CLI window, derived from the gate's own wing records.

    A wing's `side` is the shoulder segment it hangs off, `x0`/`x1` are its
    measured columns, `rows[0]` is the top of the ledge and `shoulder_ref` is
    the row where his own shoulder arrives — which is exactly the pair a human
    reads off `--measure` (`codexnondev`: `--wing-right 886 --rows 195,478`)."""
    args, detail = [], {}
    for side in ("right", "left"):
        mine = [w for w in wings if w.get("side") == side]
        if not mine:
            continue
        r0 = min(int(w["rows"][0]) for w in mine)
        r1 = max(int(round(float(w.get("shoulder_ref") or w["rows"][1])))
                 for w in mine)
        if r1 <= r0:
            r1 = max(int(w["rows"][1]) for w in mine)
        if side == "right":
            col = min(int(w["x0"]) for w in mine)      # INNER column
            args += ["--wing-right", str(col), "--rows", f"{r0},{r1}"]
            detail["right"] = {"inner_col": col, "rows": [r0, r1]}
        else:
            col = max(int(w["x1"]) for w in mine)      # OUTER column
            args += ["--wing-left", str(col), "--rows-left", f"{r0},{r1}"]
            detail["left"] = {"outer_col": col, "rows": [r0, r1]}
    return args, detail


def outline_report(pkg: dict, tag: str, emit: str) -> dict | None:
    """The LAW 48 report the outline gate wrote when it refused.

    The gate runs on the ALPHA, before any encode, so there are no layers and
    no full ship record to hang it on: `ship.ship_all` raises with
    `rec = {"law48": ...}` instead, which the laptop lane writes to the ship
    json (`ship.py` main writes `exc.rec` before re-raising) and the Modal lane
    hands back inside `run_<tag>.json`'s `ship.record`.  Read whichever lane
    shipped first, exactly as `edge_report` does, so a stale json from an
    earlier round is never mistaken for this round's verdict.
    """
    session = Path(pkg["session"])
    sj = session / f"matte_{pkg['id']}_{emit}_ship.json"
    rp = session / f"run_{tag}.json"
    where = ((pkg.get("stages") or {}).get("ship") or {}).get("where") or ""
    order = [sj, rp] if where == "laptop" else [rp, sj]
    for p in order:
        if not p.exists():
            continue
        rec = json.loads(p.read_text())
        law = rec.get("law48") or \
            (((rec.get("ship") or {}).get("record") or {}).get("law48"))
        if law:
            return law
    return None


def outline_args(law: dict) -> tuple[list, dict]:
    """The wingfix CLI window, derived from the outline gate's own numbers.

    The gate reports, per refusing side, the rows of the head band it measured
    (already carrying `row_margin`) and a `wing_column` — the deepest inward
    column that still holds plate-dark pixels, plus `wing_margin`.  That pair
    IS the window a human reads off `wingfix --measure`: hermeskanban's working
    second pass was `--wing-left 510 --rows-left 300,464`, and on that same
    alpha this gate measures a cut column within a few px of 510 over the same
    band.  `wingfix` cuts DARK pixels only inside it, which is what lets the
    column sit inboard of his real body edge without taking any of him.
    """
    args, detail = [], {}
    for r in (law.get("refusals") or []):
        side, col = r.get("side"), r.get("wing_column")
        if col is None:
            continue
        r0, r1 = int(r["rows"][0]), int(r["rows"][1])
        if side == "right":
            args += ["--wing-right", str(int(col)), "--rows", f"{r0},{r1}"]
            detail["right"] = {"inner_col": int(col), "rows": [r0, r1],
                               "reach_col": r.get("reach_column")}
        else:
            args += ["--wing-left", str(int(col)), "--rows-left", f"{r0},{r1}"]
            detail["left"] = {"outer_col": int(col), "rows": [r0, r1],
                              "reach_col": r.get("reach_column")}
    return args, detail


def edge_report(pkg: dict, tag: str, emit: str) -> dict | None:
    """The edge-clip report the gate that refused actually wrote.

    The laptop lane writes the record BEFORE refusing (`ship.py` main), so it is
    in the ship json.  The Modal lane never downloads the webms of a refused
    ship, but it does hand the whole record back inside `run_<tag>.json`'s
    `ship.record`.  Read whichever lane shipped, so a stale json from an earlier
    round can never be mistaken for this round's verdict."""
    session = Path(pkg["session"])
    sj = session / f"matte_{pkg['id']}_{emit}_ship.json"
    rp = session / f"run_{tag}.json"
    where = ((pkg.get("stages") or {}).get("ship") or {}).get("where") or ""
    order = [sj, rp] if where == "laptop" else [rp, sj]
    for p in order:
        if not p.exists():
            continue
        rec = json.loads(p.read_text())
        ec = rec.get("edge_clip") or \
            (((rec.get("ship") or {}).get("record") or {}).get("edge_clip"))
        if ec:
            return ec
    return None


def edge_floors(edge: dict, session: Path) -> tuple[dict, dict]:
    """`need_floor_master_px` for `solve_overwide`, from the gate's own numbers.

    Per gated side: the worst NEGATIVE limb margin the gate measured, plus
    `WANT_MARGIN_CANVAS` (the 24 px aim the solver already uses), converted from
    canvas px to master px through `k * PLATE_SCALE`, then ADDED to the
    extension that side already carries — because the floor is an absolute
    extension, not an increment.  A side whose border sits off screen by more
    than the rim is not gated and is never widened: that is the LAW 44 ruling,
    and widening it would move the plate for a touch nobody can see."""
    pj = json.loads((session / "plate.json").read_text())
    ow = pj.get("overwide") or {}
    k = float(((ow.get("k") or {}).get("float")) or 0.0)
    ext = ow.get("extension") or {}
    gated = ((edge.get("law") or {}).get("plate_border_gated") or {})
    per_px = k * platelib.PLATE_SCALE            # canvas px per master px
    if per_px <= 0:
        raise RuntimeError("plate.json carries no over-wide k; the edge repair "
                           "cannot convert canvas px to master px")
    floors, detail = {}, {}
    for w in (edge.get("windows") or []):
        etag = str(w.get("edge") or "")
        if not etag.startswith("plate_"):
            continue                              # frame edges never gate
        if gated.get(etag) is False:
            continue                              # off-screen border: not ours
        side = etag.split("_", 1)[1]
        m = w.get("worst_margin_canvas_px")
        if m is None:
            m = ((edge.get("edges") or {}).get(etag) or {}) \
                .get("min_limb_margin_canvas_px")
        worst = float(m) if m is not None else 0.0
        need_canvas = max(0.0, -worst) + platelib.WANT_MARGIN_CANVAS
        prev = float(ext.get(f"{side}_master_px") or 0.0)
        cand = round(prev + need_canvas / per_px, 1)
        if cand > floors.get(side, 0.0):
            floors[side] = cand
            detail[side] = {
                "worst_margin_canvas_px": round(worst, 1),
                "aim_canvas_px": platelib.WANT_MARGIN_CANVAS,
                "canvas_px_per_master_px": round(per_px, 6),
                "extension_already_master_px": prev,
                "need_floor_master_px": cand,
                "window": {kk: w.get(kk) for kk in
                           ("edge", "t", "n_frames", "isolated_limb_frames")}}
    return floors, detail


def _run_fix(cmd: list, logf: Path, title: str) -> str:
    """A repair tool, its whole output appended to the recording's track log."""
    with open(logf, "a") as h:
        h.write(f"\n--- {title} ---\n{' '.join(cmd)}\n")
        h.flush()
        proc = subprocess.run(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, text=True, timeout=3600)
        h.write(proc.stdout or "")
    if proc.returncode != 0:
        raise RuntimeError(f"{title} exited {proc.returncode}: "
                           f"{(proc.stdout or '')[-800:]}")
    return proc.stdout or ""


def recover_run_record(session: Path, tag: str, *, vid: str) -> dict | None:
    """Rebuild a missing local run record from what is on disk and on the volume.

    Miguel, 2026-09-04: "every time you encounter bugs like this fix them".
    `track.py` writes the run record LAST, after the alpha is downloaded and the
    remote ship has been collected, so a crash on that line loses the whole
    paid track even though every artifact survived — trycrm/run 14 died there on
    a stray bytes field and the ship stage then reported "no run record to read
    the ship out of".  The record is not precious: the CONTAINER already wrote
    its own copy to `/vol/<session>/run_<tag>.json` before returning, and the
    alpha is on disk.  So pull the container's copy, stamp it as recovered, and
    let the ship stage carry on.
    """
    local = session / f"run_{tag}.json"
    alpha = session / f"alpha_{tag}.mkv"
    if local.exists() or not alpha.exists():
        return None
    try:
        out = subprocess.run(
            [str(MODAL), "volume", "get", "shorts-factory-sam2",
             f"{session.name}/run_{tag}.json", str(local), "--force"],
            capture_output=True, text=True, timeout=300)
        if not local.exists():
            log(vid, f"run-record recovery: modal volume get failed "
                     f"({out.stderr.strip()[-200:]})")
            return None
        rec = json.loads(local.read_text())
        rec["recovered_from_volume"] = True
        rec["recovered_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        rec["alpha_local"] = str(alpha)
        local.write_text(json.dumps(rec, indent=1))
        log(vid, f"run-record RECOVERED from the volume: {local.name} "
                 f"({alpha.stat().st_size:,} B alpha already on disk) — no "
                 "re-track needed")
        return rec
    except Exception as exc:                                  # noqa: BLE001
        log(vid, f"run-record recovery failed: {type(exc).__name__}: {exc}")
        return None


def chair_from_gate(pkg: dict, *, gate: str, law: dict | None,
                    scan: dict | None) -> dict:
    """THE SELF-HEAL: an exclusion prompt derived from the gate's own refusal.

    The detector's known blind spot is the RIGHT side (his hair touches the
    wing, so the sandwich test fails), and until now a refusal on a side with
    no chair object meant a rectangle — or a human.  Both gates hand back the
    window they are complaining about, so that window is the seed for a chair
    object and the repair loop can try the RIGHT TOOL before the blunt one.

    It refuses to guess.  `chairprompt.from_refusal` measures the window and
    calls it "not a wing" when it is wider than a wedge can be — grokbuild/run
    14's outline refusal names a 275 px window because the gate fired on HIS
    OWN JAW-TO-SHOULDER LINE, and deriving a chair object there would have
    carved his neck automatically.  A rejection is a finding: it says the
    refusal is a false positive and the remedy is a reasoned `--allow-outline`.
    """
    import sys as _sys                                          # noqa: PLC0415
    _sam2 = str(Path(__file__).resolve().parent.parent / "sam2")
    if _sam2 not in _sys.path:
        _sys.path.insert(0, _sam2)
    session = Path(pkg["session"])
    body = session / "prompts" / "_original" / "birefnet_00000.png"
    if not body.exists():
        body = session / "prompts" / "birefnet_00000.png"
    have = set((json.loads((session / CHAIR_JSON).read_text()).get("found") or [])
               if (session / CHAIR_JSON).exists() else [])
    out: dict = {"gate": gate, "already_excluded": sorted(have), "sides": {}}
    try:
        import chairprompt                                      # noqa: PLC0415
    except Exception as exc:                                    # noqa: BLE001
        out["error"] = f"{type(exc).__name__}: {exc}"
        return out
    todo = []
    if gate == "outline" and law:
        for ref in (law.get("refusals") or []):
            side = ref.get("side")
            rows = ref.get("rows") or []
            if side and len(rows) == 2:
                todo.append((side, tuple(rows), ref.get("wing_column"), None))
    elif gate == "protrusion" and scan:
        for w in (scan.get("wings") or []):
            side, rows = w.get("side"), (w.get("rows") or [])
            if side and len(rows) == 2:
                todo.append((side, tuple(rows),
                             None, (w.get("x0"), w.get("x1"))))
    for side, rows, cut, wcols in todo:
        if side in have:
            out["sides"][side] = {"skipped": "already has an exclusion object"}
            continue
        try:
            rec = chairprompt.from_refusal(
                session / "plate_wide_25.mp4", body, side=side, rows=rows,
                cut_column=cut, wing_cols=wcols, gate=gate,
                overlay_png=(session / "prompts" /
                             f"chair_from_{gate}_{side}.png"))
        except Exception as exc:                                # noqa: BLE001
            rec = {"found": False, "why": f"{type(exc).__name__}: {exc}"}
        rec.pop("band", None)
        out["sides"][side] = rec
    out["derived"] = sorted(k for k, v in out["sides"].items()
                            if isinstance(v, dict) and v.get("found"))
    # A detector answer of "not a wing" is a VETO, never merely a failed
    # derivation.  The distinction is load-bearing: grokbuild's 275 px window
    # was anatomy, and treating `found=False` as permission to fall back carved
    # 7,719-8,174 px/frame out of its neck.  `verified_anatomy` is the stronger
    # over-wide verdict; narrower/under-measured misses remain unresolved, but
    # both still veto the rectangle.
    out["not_a_wing"] = sorted(
        k for k, v in out["sides"].items()
        if isinstance(v, dict) and v.get("verdict") == "not a wing")
    out["verified_anatomy"] = sorted(
        k for k, v in out["sides"].items()
        if isinstance(v, dict) and v.get("outcome") == "verified anatomy")
    out["unresolved"] = sorted(
        k for k, v in out["sides"].items()
        if isinstance(v, dict) and not v.get("found")
        and v.get("outcome") == "unresolved")
    return out


def outline_anatomy_decision(law: dict, chair: dict) -> dict:
    """Whether an anatomy veto may preserve the alpha with `--allow-outline`.

    The exception is grokbuild's exact shape: the detector independently says
    the refusal window is anatomy, straight-run p95 is the ONLY refusing
    instrument, and the persistence (`at-line`) and retained-dark instruments
    both remain inside their own ceilings.  Anything less is `needs_miguel`.
    """
    anatomy = set(chair.get("verified_anatomy") or [])
    vetoed = set(chair.get("not_a_wing") or [])
    refs = list(law.get("refusals") or [])
    refusing = {str(r.get("side")) for r in refs if r.get("side")}
    cfg = law.get("cfg") or {}
    required = ("straight_p95_max", "straight_persist_max",
                "dark_frac_p95_max")
    if not anatomy:
        return {"eligible": False,
                "reason": "the detector vetoed the cut but did not verify anatomy"}
    if vetoed != anatomy:
        return {"eligible": False,
                "reason": ("at least one not-a-wing side is unresolved rather than "
                           "verified anatomy"),
                "verified_anatomy": sorted(anatomy),
                "vetoed": sorted(vetoed)}
    if refusing != anatomy:
        return {"eligible": False,
                "reason": ("the outline refusal includes a side not independently "
                           "verified as anatomy"),
                "verified_anatomy": sorted(anatomy),
                "refusing": sorted(refusing)}
    if any(k not in cfg for k in required):
        return {"eligible": False,
                "reason": "the LAW 48 report does not carry all three ceilings"}

    rows = []
    for ref in refs:
        side = str(ref["side"])
        measured = dict((law.get("sides") or {}).get(side) or {})
        measured.update({k: ref.get(k) for k in
                         ("straight_rows_p95", "straight_frac_at_line",
                          "dark_frac_p95") if ref.get(k) is not None})
        why = list(ref.get("why") or measured.get("why") or [])
        p95 = measured.get("straight_rows_p95")
        at_line = measured.get("straight_frac_at_line")
        dark = measured.get("dark_frac_p95")
        only_p95 = (len(why) == 1 and "straight run's p95" in why[0])
        inside = (p95 is not None and at_line is not None and dark is not None
                  and float(p95) >= float(cfg["straight_p95_max"])
                  and float(at_line) <= float(cfg["straight_persist_max"])
                  and float(dark) <= float(cfg["dark_frac_p95_max"]))
        rows.append({"side": side, "only_straight_p95": only_p95,
                     "straight_rows_p95": p95,
                     "straight_p95_ceiling": cfg["straight_p95_max"],
                     "straight_frac_at_line": at_line,
                     "straight_persist_ceiling": cfg["straight_persist_max"],
                     "dark_frac_p95": dark,
                     "dark_frac_p95_ceiling": cfg["dark_frac_p95_max"]})
        if not (only_p95 and inside):
            return {"eligible": False,
                    "reason": (f"{side} is not the straight-p95-only anatomy case; "
                               "at-line and retained-dark must both be inside "
                               "their ceilings"),
                    "measurements": rows}

    reason = "verified anatomy; preserve the unchanged alpha, no carve: " + "; ".join(
        f"{r['side']} refusal window exceeds the chair-wing ceiling, only "
        f"straight p95 {float(r['straight_rows_p95']):.1f} >= "
        f"{float(r['straight_p95_ceiling']):.1f} refuses, at-line "
        f"{float(r['straight_frac_at_line']):.1%} <= "
        f"{float(r['straight_persist_ceiling']):.1%} and dark p95 "
        f"{float(r['dark_frac_p95']):.1%} <= "
        f"{float(r['dark_frac_p95_ceiling']):.1%} are inside"
        for r in rows)
    return {"eligible": True, "reason": reason, "measurements": rows}


def finish_not_a_wing_round(pkg: dict, run: Path, *, rd: dict, gate: str,
                            law: dict | None, chair: dict, prev_tag: str,
                            emit: str) -> dict:
    """End a detector veto without ever reaching `wingfix`.

    A verified straight-p95-only anatomy case is re-shipped locally from the
    unchanged alpha with a measured `--allow-outline` reason.  Every other veto
    is terminal for automation and stamps the recording `needs_miguel`.
    """
    vid = pkg["id"]
    verified = sorted(chair.get("verified_anatomy") or [])
    vetoed = sorted(chair.get("not_a_wing") or [])
    rd["tag"] = prev_tag                   # no re-track happened
    rd["fix"] = "none (not-a-wing veto; zero carve)"
    rd["outcome"] = "verified anatomy" if verified else "not a wing"
    rd["verified_anatomy_sides"] = verified
    rd["vetoed_sides"] = vetoed
    decision = (outline_anatomy_decision(law or {}, chair)
                if gate == "outline" else
                {"eligible": False,
                 "reason": ("a protrusion refusal is not eligible for an outline "
                            "override; anatomy is preserved for Miguel")})
    rd["anatomy_decision"] = decision

    if decision.get("eligible"):
        reason = str(decision["reason"])
        rd["allow_outline"] = reason
        pkg["stages"].pop("ship", None)
        log(vid, "VERIFIED ANATOMY: zero carve; re-shipping the unchanged alpha "
                 "locally with a straight-p95-only --allow-outline reason")
        ship_matte(pkg, run, tag=prev_tag, emit=emit,
                   allow_outline=reason)
        ship_st = pkg["stages"].get("ship") or {}
        rd["ship_status"] = ship_st.get("status")
        rd["ship_verdict"] = (ship_st.get("gate_refusal")
                              or ship_st.get("stdout_tail")
                              or ship_st.get("protrusion_verdict"))
        rd["resolution"] = ("shipped unchanged alpha with reasoned "
                            "--allow-outline" if rd["ship_status"] == "ok"
                            else "the reasoned local re-ship did not pass")
    else:
        old = rd.get("refused_verdict") or refusal_verdict(pkg)
        ship_st = {"status": "needs_miguel", "gate": gate,
                   "outcome": rd["outcome"], "vetoed_sides": vetoed,
                   "gate_refusal": old,
                   "reason": str(decision.get("reason") or "not a wing")}
        pkg["stages"]["ship"] = ship_st
        mark_stage(pkg, "ship", ship_st)
        rd["ship_status"] = "needs_miguel"
        rd["ship_verdict"] = ship_st["reason"]
        rd["resolution"] = "needs_miguel; unchanged alpha preserved, zero carve"
        log(vid, f"{rd['outcome'].upper()}: zero carve; needs_miguel ({ship_st['reason']})")

    rd["cost_usd"] = 0.0
    rd["cost_breakdown_usd"] = {"track": 0.0, "ship": 0.0}
    return rd


def merge_chair_prompt(session: Path, derived: dict) -> list[str]:
    """Fold derived exclusion prompts into `<session>/chair_prompt.json`."""
    p = session / CHAIR_JSON
    rec = json.loads(p.read_text()) if p.exists() else {"left": {"found": False},
                                                        "right": {"found": False}}
    added = []
    for side, blk in (derived.get("sides") or {}).items():
        if not (isinstance(blk, dict) and blk.get("found")):
            continue
        rec[side] = blk
        added.append(side)
    rec["found"] = [s for s in ("left", "right")
                    if (rec.get(s) or {}).get("found")]
    rec["derived_sides"] = sorted(set((rec.get("derived_sides") or []) + added))
    p.write_text(json.dumps(rec, indent=1))
    return added


def repair_round(pkg: dict, row: dict, run: Path, *, r: int, base_tag: str,
                 gate: str, gpu: str, emit: str, remote_ship: bool,
                 limit: int | None, stride: int, sweep_local: bool) -> dict:
    """ONE repair round: fix -> re-track -> re-ship, and its own record."""
    vid = pkg["id"]
    session = Path(pkg["session"])
    cuts = Path(pkg["cut_dir"])
    logs = run / "prep" / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    logf = logs / f"track_{vid}.log"
    prev_tag = _tag_at(base_tag, r - 1)
    tag = _tag_at(base_tag, r)
    t0 = time.time()
    rd: dict = {"round": r, "gate": gate, "fix": None, "tag": tag,
                "previous_tag": prev_tag, "track_seconds": None,
                "ship_status": None, "cost_usd": 0.0,
                "refused_verdict": refusal_verdict(pkg)}

    plate = session / "plate_wide_25.mp4"
    prompts = session / "prompts"
    alpha = session / f"alpha_{prev_tag}.mkv"

    if gate == "protrusion":
        if not alpha.exists():
            raise RuntimeError(f"no alpha to repair: {alpha}")
        scan_json = logs / f"protrusion_{vid}_{prev_tag}.json"
        scan = gate_scan(session, alpha, scan_json, logf)
        rd["scan_json"] = str(scan_json)
        rd["scan_verdict"] = scan.get("verdict")
        wings = scan.get("wings") or []
        out_dir = session / f"prompts_{tag}"
        # ── THE CHAIR OBJECT FIRST, THE RECTANGLE ONLY IF IT CANNOT ────────
        ch = chair_from_gate(pkg, gate="protrusion", law=None, scan=scan)
        rd["chair_from_gate"] = ch
        if ch.get("derived"):
            added = merge_chair_prompt(session, ch)
            rd["fix"] = "chair-object (derived from the protrusion window)"
            rd["chair_added_sides"] = added
            log(vid, f"protrusion refused on {added}: derived an exclusion "
                     f"object from the gate's own window instead of cutting "
                     f"— re-tracking with it")
            out = ("chair object derived for "
                   + ", ".join(added) + "; no cut was made")
        elif ch.get("not_a_wing"):
            # AUDIT A1.  `found=False` is not one outcome.  "Not a wing" is a
            # positive veto against the rectangle, so this round ends without
            # creating prompts, invoking wingfix, or re-tracking.
            rd = finish_not_a_wing_round(
                pkg, run, rd=rd, gate="protrusion", law=None, chair=ch,
                prev_tag=prev_tag, emit=emit)
            rd["wall_s"] = round(time.time() - t0, 1)
            return rd
        elif wings:
            args, detail = wing_args(wings)
            if not args:
                raise RuntimeError("the scan reported wings with no usable "
                                   "side; nothing to cut")
            rd["fix"] = "wingfix"
            rd["wings"] = [{k: w.get(k) for k in
                            ("side", "x0", "x1", "width", "rows",
                             "shoulder_ref", "slope", "sd_in", "persistence",
                             "dark_frac", "best_window")} for w in wings]
            rd["wing_window"] = detail
            out = _run_fix([str(PY), str(SAM2 / "wingfix.py"),
                            "--session", str(session), "--alpha", str(alpha),
                            "--plate", str(plate), "--out", str(out_dir)] + args,
                           logf, f"wingfix {vid} {prev_tag} -> {tag}")
        else:
            rd["fix"] = "bolsterfix"
            rd["protrusion_windows"] = [
                {k: w.get(k) for k in ("x0", "x1", "width", "lift_mean",
                                       "lift_local", "persistence", "dark_frac",
                                       "best_window")}
                for w in (scan.get("windows") or [])]
            out = _run_fix([str(PY), str(SAM2 / "bolsterfix.py"),
                            "--session", str(session), "--alpha", str(alpha),
                            "--plate", str(plate), "--out", str(out_dir)],
                           logf, f"bolsterfix {vid} {prev_tag} -> {tag}")
        rd["fix_tail"] = out.strip().splitlines()[-4:]
        # A CHAIR-OBJECT FIX WRITES NO PROMPTS DIR.  It changes `exclude=`, not
        # the frame-0/keyframe masks, so the re-track must reuse the prompts
        # this round started from — pointing it at an empty `prompts_<tag>/`
        # would drop the frame-0 prompt and re-segment from nothing.
        prompts = out_dir if out_dir.exists() and any(
            out_dir.glob("kf_*.png")) else prompts
        rd["prompts"] = str(prompts)
        dp = await_display_plate(vid, pkg) if remote_ship else None
        if remote_ship and dp is None:
            # the plate did not change, so the display plate this batch already
            # cut is still the right one
            spec = display_spec(session, cuts)
            if spec and Path(spec["file"]).exists():
                dp = Path(spec["file"])
    elif gate == "outline":
        # LAW 48.  The gate ran on the alpha and measured the window itself:
        # the rows of its own head band (top lifted, bottom AT the shoulder
        # arrival, because wingfix cuts dark and his shirt is black) and a cut
        # column set from the deepest inward column of retained plate-dark
        # pixels.  A wedge is not a rectangle, so if one window leaves an upper
        # band, round 2 re-measures THIS round's alpha and cuts again — the
        # two-window chain the hermeskanban repair had to be driven by hand.
        if not alpha.exists():
            raise RuntimeError(f"no alpha to repair: {alpha}")
        law = outline_report(pkg, prev_tag, emit)
        if law is None:
            raise RuntimeError("the outline gate refused but wrote no LAW 48 "
                               "report to read the window out of")
        out_dir = session / f"prompts_{tag}"
        # ── THE CHAIR OBJECT FIRST, THE RECTANGLE ONLY IF IT CANNOT ────────
        ch = chair_from_gate(pkg, gate="outline", law=law, scan=None)
        rd["chair_from_gate"] = ch
        chair_first = bool(ch.get("derived"))
        rd["outline"] = {"verdict": law.get("verdict"),
                         "refusals": law.get("refusals"),
                         "cfg": law.get("cfg"),
                         "sides": {k: {kk: v.get(kk) for kk in
                                       ("straight_rows_p95",
                                        "straight_rows_max",
                                        "straight_frac_at_line",
                                        "dark_px_p95", "dark_frac_p95",
                                        "dark_frac_max", "band_rows_median",
                                        "dark_reach_column", "verdict")}
                                   for k, v in (law.get("sides") or {}).items()}}
        if not chair_first and ch.get("not_a_wing"):
            # AUDIT A1.  An anatomy verdict is the end of the destructive
            # ladder.  The helper may re-ship the SAME alpha under the one
            # measured straight-p95 exception; otherwise it stamps
            # needs_miguel.  Neither path can reach `_run_fix`.
            rd = finish_not_a_wing_round(
                pkg, run, rd=rd, gate="outline", law=law, chair=ch,
                prev_tag=prev_tag, emit=emit)
            rd["wall_s"] = round(time.time() - t0, 1)
            return rd
        args, detail = ([], {}) if chair_first else outline_args(law)
        if not chair_first and not args:
            raise RuntimeError(
                "the outline gate refused with no usable cut column — its "
                "reach walk found no retained plate-dark column to cut to, so "
                "there is nothing for wingfix to take")
        rd["fix"] = ("chair-object (derived from the outline window)"
                     if chair_first else "wingfix")
        rd["wing_window"] = detail
        if chair_first:
            added = merge_chair_prompt(session, ch)
            rd["chair_added_sides"] = added
            log(vid, f"outline refused on {added}: derived an exclusion object "
                     "from the gate's own window instead of cutting — "
                     "re-tracking with it")
            out = ("chair object derived for " + ", ".join(added)
                   + "; no cut was made")
        else:
            log(vid, "outline refused; the chair detector neither derived an "
                     "object nor vetoed the cut; falling back to wingfix: "
                     + "; ".join(f"{k}: {(v or {}).get('why', '')[:90]}"
                                 for k, v in (ch.get("sides") or {}).items()))
            out = _run_fix([str(PY), str(SAM2 / "wingfix.py"),
                            "--session", str(session), "--alpha", str(alpha),
                            "--plate", str(plate), "--out", str(out_dir),
                            "--chunk", str(OUTLINE_CHUNK)] + args,
                           logf, f"wingfix(outline) {vid} {prev_tag} -> {tag}")
        rd["fix_tail"] = out.strip().splitlines()[-4:]
        # A CHAIR-OBJECT FIX WRITES NO PROMPTS DIR.  It changes `exclude=`, not
        # the frame-0/keyframe masks, so the re-track must reuse the prompts
        # this round started from — pointing it at an empty `prompts_<tag>/`
        # would drop the frame-0 prompt and re-segment from nothing.
        prompts = out_dir if out_dir.exists() and any(
            out_dir.glob("kf_*.png")) else prompts
        rd["prompts"] = str(prompts)
        dp = await_display_plate(vid, pkg) if remote_ship else None
        if remote_ship and dp is None:
            spec = display_spec(session, cuts)
            if spec and Path(spec["file"]).exists():
                dp = Path(spec["file"])
    else:                                          # gate == "edge_clip"
        edge = edge_report(pkg, prev_tag, emit)
        if edge is None:
            raise RuntimeError("the edge gate refused but wrote no report to "
                               "read the per-side need out of")
        floors, detail = edge_floors(edge, session)
        if not floors:
            raise RuntimeError(
                "the edge gate refused with no GATED plate-border window — "
                "every window it found is at a border that is off screen by "
                "more than the rim, and LAW 44's ruling does not widen those")
        rd["fix"] = "widen_plate"
        rd["need_floor_master_px"] = floors
        rd["edge_need"] = detail
        rd["edge_windows"] = edge.get("windows")
        prev_box = ((json.loads((session / "plate.json").read_text())
                     .get("overwide") or {}).get("plate_box") or {})
        with open(logf, "a") as h:
            h.write(f"\n--- widen plate {vid} {prev_tag} -> {tag}: "
                    f"need_floor_master_px {floors} ---\n")
        rec = platelib.build_plate(
            master=cuts / "master.mp4", session=session,
            sweep_json=run / "gen" / f"_birefnet_master_{vid}.json",
            stride=stride, overwide=not row.get("no_overwide"),
            sweep_local=sweep_local, need_floor_master_px=floors)
        ow = rec.get("overwide") or {}
        rd["plate"] = {"before_box": prev_box,
                       "after_box": ow.get("plate_box"),
                       "plate_size": rec.get("plate_size"),
                       "extension_master_px": ow.get("extension"),
                       "crop": rec.get("crop")}
        # THE PLATE CHANGED SIZE, so the old prompt's pixels are in the wrong
        # coordinate system and keeping it would be worse than losing the
        # repair: reset unconditionally here.
        pr = promptlib.build_prompt0(session=session, plate=plate,
                                     wings=row.get("wings"),
                                     reset_prompt=True)
        rd["prompt0"] = {"wings_source": pr.get("wings_source"),
                         "wing_cut_applied":
                             bool((pr.get("wings") or {}).get("wing_cut_applied"))}
        # THE PLATE CHANGED SIZE, so every plate coordinate the chair prompt
        # carries is stale.  Re-derive it or the exclusion box lands on his
        # cheek.  (Same reason the display plate is re-cut two lines down.)
        rd["chair_prompt"] = chair_prompt_stage(
            session, no_chair=bool(pkg.get("no_chair_object")),
            override=row.get("chair_prompt"))
        prompts = session / "prompts"
        dp = None
        if remote_ship:
            # the plate CHANGED size, so the display plate must be re-cut
            start_display_plate(vid, session, cuts, logs)
            dp = await_display_plate(vid, pkg)

    # ---- re-track, same lane, same ship flags -------------------------------
    lane = str(pkg.get("gpu") or gpu).lower()
    cmd, ship_where = build_track_cmd(
        pkg, session=session, plate=plate, prompts=prompts, tag=tag, lane=lane,
        limit=limit, remote_ship=remote_ship, emit=emit, display_plate=dp)
    rd["track_cmd"] = " ".join(cmd)
    rd["lane"] = lane
    rd["ship_where"] = ship_where
    t_track = time.time()
    with open(logf, "a") as h:
        h.write(f"\n--- re-track {vid} tag {tag} (ship {ship_where}) ---\n")
        h.flush()
        proc = subprocess.run(cmd, stdout=h, stderr=subprocess.STDOUT,
                              timeout=5400)
    rd["track_wall_s"] = round(time.time() - t_track, 1)
    rec_path = session / f"run_{tag}.json"
    if proc.returncode not in (0, 3) or not rec_path.exists():
        raise RuntimeError(f"the repair re-track exited {proc.returncode}; "
                           f"see {logf}")
    st_track = track_fields(rec_path)
    st_track.update({"tag": tag, "lane": lane, "cmd": " ".join(cmd),
                     "ship_where": ship_where, "log": str(logf),
                     "wall_s": rd["track_wall_s"], "repair_round": r})
    pkg["stages"]["track"] = st_track
    rd["track_seconds"] = st_track.get("track_seconds")
    track_cost = float(st_track.get("cost_usd") or 0.0)
    # A REPAIR ROUND IS A SECOND CONTAINER, and it writes its own tag's run
    # record — so it is its own ledger row, never a replacement of round 0's.
    ledger_track(pkg.get("run"), vid, st_track, rec_path,
                 note=f"SAM2 re-track, repair round {r} ({gate})")

    # ---- re-ship, the same lane the first ship used -------------------------
    pkg["stages"].pop("ship", None)
    if remote_ship:
        collect_remote_ship(pkg, tag=tag, emit=emit)
    else:
        ship_matte(pkg, run, tag=tag, emit=emit)
    st_ship = pkg["stages"].get("ship") or {}
    st_ship["repair_round"] = r
    rd["ship_status"] = st_ship.get("status")
    rd["ship_verdict"] = (st_ship.get("gate_refusal")
                          or st_ship.get("gate_log")
                          or st_ship.get("protrusion_verdict"))
    rd["edge_clip"] = st_ship.get("edge_clip")
    ship_cost = float(st_ship.get("cost_usd") or 0.0)
    rd["cost_usd"] = round(track_cost + ship_cost, 4)
    rd["cost_breakdown_usd"] = {"track": round(track_cost, 4),
                                "ship": round(ship_cost, 4)}
    rd["wall_s"] = round(time.time() - t0, 1)
    return rd


def auto_repair(pkg: dict, row: dict, run: Path, *, base_tag: str, gpu: str,
                emit: str, remote_ship: bool, limit: int | None, stride: int,
                sweep_local: bool, max_rounds: int = REPAIR_MAX_ROUNDS) -> None:
    """Up to TWO rounds of fix -> re-track -> re-ship, then report.

    `stages.track` and `stages.ship` end up pointing at the FINAL tag's records
    so every downstream station reads the alpha and the layers that actually
    passed, and `stages.repair.round0` keeps the first attempt's records so the
    money it spent is still in the batch's arithmetic."""
    vid = pkg["id"]
    gate = refusal_gate(pkg)
    if gate is None:
        return
    rep = {"rounds": [], "final_tag": base_tag, "total_extra_cost_usd": 0.0,
           "total_extra_wall_s": 0.0,
           "round0": {"tag": base_tag,
                      "track": dict(pkg["stages"].get("track") or {}),
                      "ship": dict(pkg["stages"].get("ship") or {})}}
    pkg["stages"]["repair"] = rep
    t0 = time.time()
    for r in range(1, max_rounds + 1):
        log(vid, f"REPAIR round {r}: the {gate} gate refused tag "
                 f"{_tag_at(base_tag, r - 1)}")
        try:
            rd = repair_round(pkg, row, run, r=r, base_tag=base_tag, gate=gate,
                              gpu=gpu, emit=emit, remote_ship=remote_ship,
                              limit=limit, stride=stride,
                              sweep_local=sweep_local)
        except Exception as exc:                       # never kill the batch
            rep["rounds"].append({
                "round": r, "gate": gate, "fix": None,
                "tag": _tag_at(base_tag, r), "track_seconds": None,
                "ship_status": "REPAIR_ERROR", "cost_usd": 0.0,
                "error": f"{type(exc).__name__}: {exc}",
                "traceback": traceback.format_exc()[-3000:]})
            log(vid, f"REPAIR round {r} FAILED  {exc}")
            break
        rep["rounds"].append(rd)
        rep["final_tag"] = rd["tag"]
        rep["total_extra_cost_usd"] = round(
            sum(x.get("cost_usd") or 0.0 for x in rep["rounds"]), 4)
        if rd["ship_status"] == "ok":
            log(vid, f"REPAIR round {r} PASSED ({rd['fix']}, tag {rd['tag']})")
            break
        if rd["ship_status"] == "needs_miguel":
            log(vid, f"REPAIR round {r} stopped safely: needs_miguel "
                     f"({rd.get('outcome')}; zero carve)")
            break
        log(vid, f"REPAIR round {r} still refused ({rd['ship_status']})")
        nxt = refusal_gate(pkg)
        if nxt is None:
            break                       # not a repairable gate any more
        gate = nxt
    rep["total_extra_wall_s"] = round(time.time() - t0, 1)
    ship_st = pkg["stages"].setdefault(
        "ship", {"status": "error",
                 "error": "the repair round left no ship record"})
    ship_ok = ship_st.get("status") == "ok"
    needs_miguel = ship_st.get("status") == "needs_miguel"
    n = len([x for x in rep["rounds"] if x.get("fix")])
    if not ship_ok and not needs_miguel and len(rep["rounds"]) >= max_rounds:
        ship_st["status"] = "REFUSED_AFTER_2_ROUNDS"
        ship_st["rounds_verdicts"] = [
            {"round": x["round"], "gate": x["gate"], "fix": x.get("fix"),
             "refused_verdict": x.get("refused_verdict"),
             "ship_verdict": x.get("ship_verdict")} for x in rep["rounds"]]
    rep["repaired"] = bool(ship_ok and n)
    rep["rounds_run"] = len(rep["rounds"])
    # the loop is a STAGE like any other: its wall belongs in the package's own
    # total and in the batch's serial equivalent, or the repair looks free
    rep["wall_s"] = rep["total_extra_wall_s"]
    rep["status"] = ("ok" if ship_ok else
                     "needs_miguel" if needs_miguel else "exhausted")


def final_tag(pkg: dict, base_tag: str) -> str:
    """The tag whose alpha and layers this package's stages point at."""
    rep = (pkg.get("stages") or {}).get("repair") or {}
    return str(rep.get("final_tag") or base_tag)


def summary_line(pkg: dict) -> str:
    """One line per recording, the last thing the console says about it."""
    vid = pkg.get("id", "?")
    st = (pkg.get("stages") or {}).get("ship") or {}
    if pkg.get("backend") == "matanyone2" and st.get("status") == "ok":
        return f"{vid:20s} PREPARED; final visual review required"
    rep = (pkg.get("stages") or {}).get("repair") or {}
    rounds = rep.get("rounds") or []
    if st.get("status") == "ok" and not rounds:
        return f"{vid:20s} PASS in round 0"
    if st.get("status") == "ok":
        fixes = ", ".join(str(x.get("fix") or x.get("gate")) for x in rounds)
        n = len(rounds)
        return (f"{vid:20s} PASS after {n} repair"
                f"{'s' if n != 1 else ''} ({fixes})")
    if st.get("status") == "needs_miguel":
        outcomes = ", ".join(str(x.get("outcome") or x.get("gate"))
                             for x in rounds) or str(st.get("outcome") or "review")
        return f"{vid:20s} NEEDS_MIGUEL ({outcomes}; zero carve)"
    if rounds:
        gates = ", ".join(str(x.get("gate")) for x in rounds)
        n = len(rounds)
        return (f"{vid:20s} REFUSED after {n} round{'s' if n != 1 else ''} "
                f"({gates})")
    if str(st.get("status", "")).startswith("REFUSED"):
        g = refusal_gate(pkg) or st.get("gate") or "unknown"
        return f"{vid:20s} REFUSED in round 0, no repair run ({g})"
    return f"{vid:20s} {st.get('status', 'no ship')}"


def sweep_cost_usd(pkg: dict) -> float:
    """The BiRefNet master sweep's own Modal bill, out of the plate stage.

    It lives at `stages.plate.sweep.lane.measured_cost_usd` because the sweep is
    an implementation detail of building the plate.  It is still Modal money —
    $0.0585 on costpertask, $0.0339 on astramath — and `_batch.json` counted
    only the track until 2026-09-03, so every run 11 total had to be re-added by
    hand in the bench notes.
    """
    lane = (((pkg.get("stages", {}).get("plate") or {}).get("sweep") or {})
            .get("lane") or {})
    try:
        return float(lane.get("measured_cost_usd") or 0.0)
    except (TypeError, ValueError):
        return 0.0


def reconcile(pkg: dict, tag: str, emit: str = "v5") -> None:
    """THE PACKAGE IS DERIVED FROM THE ARTEFACTS, not from what this invocation
    happened to run.  A resumed batch recovers the track Modal already paid for
    and the ship already on disk, instead of reporting them as missing."""
    if pkg.get("backend") == "matanyone2":
        return  # Never resurrect a historical SAM2 result over a reviewed selection.
    session = Path(pkg.get("session", ""))
    stages = pkg.setdefault("stages", {})

    rec_path = session / f"run_{tag}.json"
    if rec_path.exists() and (stages.get("track") or {}).get("status") != "ok":
        rec = json.loads(rec_path.read_text())
        stages["track"] = {
            "status": "ok", "recovered_from_disk": True, "tag": tag,
            "run_record": str(rec_path), "alpha": rec.get("alpha_local"),
            "frames_tracked": rec.get("frames_tracked"), "gpu": rec.get("gpu"),
            "track_seconds": rec.get("track_seconds"),
            "billed_container_seconds": rec.get("billed_container_seconds"),
            "cost_usd": rec.get("measured_cost_usd"),
            "cost_breakdown_usd": rec.get("cost_breakdown_usd"),
            "seams": rec.get("seams"),
            "leak_check": {k: v for k, v in (rec.get("leak_check") or {}).items()
                           if k in ("verdict", "healed", "needs_human")},
            **{k: v for k, v in (stages.get("track") or {}).items()
               if k in ("wall_s", "log", "cmd")},
        }

    ship_json = session / f"matte_{pkg['id']}_{emit}_ship.json"
    cur = (stages.get("ship") or {}).get("status")
    # a REFUSAL is never "recovered" away by an older ship json sitting next to
    # it — that is precisely the file the gate is disagreeing with
    if ship_json.exists() and cur not in ("ok", "REFUSED", "error",
                                          "REFUSED_AFTER_2_ROUNDS"):
        rec = json.loads(ship_json.read_text())
        # ship.py writes the record BEFORE refusing so a refusal is auditable;
        # a record whose edge gate found windows is a refused render, not a
        # finished one, and is never promoted to "ok" (run 12, 2026-09-03)
        if (rec.get("edge_clip") or {}).get("windows") and not (rec.get("edge_clip") or {}).get("allowed_by"):
            stages["ship"] = {"status": "REFUSED", "recovered_from_disk": True,
                              "ship_json": str(ship_json),
                              "gate_refusal": "edge clip: " + "; ".join(
                                  f"{w.get('edge')} {w.get('t')}" for w in rec["edge_clip"]["windows"])}
            return
        stages["ship"] = {
            "status": "ok", "recovered_from_disk": True,
            "ship_json": str(ship_json), "outputs": rec.get("outputs"),
            "frames": rec.get("frames"),
            "protrusion_verdict": (rec.get("protrusion") or {}).get("verdict",
                                                                    "clean"),
            "edge_clip": _edge_summary(rec),
            **{k: v for k, v in (stages.get("ship") or {}).items()
               if k in ("wall_s", "display", "edge_box", "cmd", "where",
                        "ship_seconds", "ffmpeg", "gate_log", "cost_usd",
                        "client_wall_s", "billed_container_seconds",
                        "cpu_cores", "workers")},
        }


# =============================================================================
# preflight
# =============================================================================
MODAL_STAGES = ("plate", "track", "ship")   # the stages that upload to Modal


def vpn_preflight(allow: bool = False, skip: set[str] | None = None,
                  sweep_local: bool = False) -> None:
    """Refuse to launch a Modal-heavy batch through ProtonVPN.

    Run 10 (2026-09-03) spent 3 to 62 minutes per Modal call BEFORE Modal even
    received it: every 25 MB upload crawled through a WireGuard tunnel to a
    server in Queretaro, Mexico.  Modal's own startup on those calls was 2 s.
    `scutil --nc list` is the system's view of the VPN services; Tailscale is
    fine and is not checked.

    IT ONLY REFUSES WHAT IT PROTECTS (geo, run 19, 2026-09-13).  The guard is
    about Modal UPLOADS: `plate` (the BiRefNet master sweep, local under
    --sweep-local), `track` and `ship`.  A batch that skips all of them — a cut
    repair, a cue rescan, a selection-review front — uploads nothing to Modal
    and was still refused at launch, which cost a held lane a whole round.  The
    refusal stands, unchanged, the moment one Modal stage is actually planned.
    """
    try:
        out = subprocess.run(["scutil", "--nc", "list"], capture_output=True,
                             text=True, timeout=10).stdout
    except Exception:
        return
    bad = [ln for ln in out.splitlines()
           if "(Connected)" in ln and "proton" in ln.lower()]
    planned = [s for s in MODAL_STAGES if s not in (skip or set())]
    if sweep_local and "plate" in planned:
        planned.remove("plate")
    if bad and not planned:
        print("PREFLIGHT: ProtonVPN is connected, but this batch plans no Modal "
              f"stage ({'/'.join(MODAL_STAGES)} are skipped or local) - there is "
              "no upload to protect, launching", flush=True)
        return
    if bad and not allow:
        raise SystemExit("PREFLIGHT: ProtonVPN is CONNECTED - every Modal upload "
                         "will crawl (run 10: 45-62 min per render call). "
                         "Disconnect it, or pass --allow-vpn to measure the "
                         "damage on purpose.\n  " + "\n  ".join(bad))
    if bad:
        print("PREFLIGHT: ProtonVPN connected, launching anyway (--allow-vpn)",
              flush=True)


# =============================================================================
# the batch
# =============================================================================
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--run", required=True, type=Path)
    ap.add_argument("--intake", required=True, type=Path)
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--backend", choices=("matanyone2", "sam2"), default="matanyone2")
    ap.add_argument("--tag", default="v1")
    ap.add_argument("--track-limit", type=int, default=None,
                    help="frames; the cents-priced probe uses 40")
    ap.add_argument("--stride", type=int, default=6,
                    help="master-sweep frame stride")
    ap.add_argument("--sweep-local", action="store_true",
                    help="run the BiRefNet master sweep on this machine's CPU "
                         "instead of the shorts-factory-birefnet A10G lane "
                         "(the fallback: ~30x slower)")
    ap.add_argument("--skip", default="",
                    help="comma-separated stages: cut,transcribe,plate,prompt0,"
                         "track,ship,cues")
    ap.add_argument("--out", type=Path, default=None)
    # THE MATTE BELONGS TO THE RUN (run 22, 2026-09-15): defaulting to the shared
    # factory-wide sessions folder shipped run 22's matte to
    # pipeline/sam2/sessions/aieducation while matte_review.py only ever looks in
    # <run>/matting, so the viewer reported "no matte exists", held the cutout, and
    # the repair round could not find it either. None here means <run>/matting.
    ap.add_argument("--sessions", type=Path, default=None,
                    help="SAM2 session root; a scratch run wants its own")
    ap.add_argument("--gpu", choices=("a10", "h100"), default="h100",
                    help="SAM2 track lane for every row; an intake row's own "
                         "`gpu` field overrides it.  h100 since 2026-09-03: "
                         "2.73x faster per frame for 1.23x the cost per frame")
    ap.add_argument("--emit", default="v5",
                    help="matte emit name.  Only `legacy` is special (it "
                         "reproduces the v4 pair); every other value writes "
                         "the v5 triple under that name, which is how a parity "
                         "run (v5b, v5c, ...) stays off a shipped v5")
    ap.add_argument("--ship-local", action="store_true",
                    help="run ship.py on THIS machine after the track, the "
                         "pre-2026-09-03 lane, for parity measurements")
    ap.add_argument("--repair-rounds", type=int, default=REPAIR_MAX_ROUNDS,
                    help="how many auto-repair rounds a refused ship gets "
                         "before it is reported (default 2: wingfix/bolsterfix "
                         "for the protrusion gate, a wider plate for the edge "
                         "gate, each followed by a re-track and a re-ship)")
    ap.add_argument("--no-repair", action="store_true",
                    help="report a refused ship instead of repairing it — the "
                         "pre-2026-09-03 behaviour, for measuring the loop")
    ap.add_argument("--allow-vpn", action="store_true",
                    help="launch even if ProtonVPN reports Connected (see "
                         "vpn_preflight)")
    ap.add_argument("--reset-prompt", action="store_true",
                    help="re-derive the frame-0 prompt even when this session's "
                         "is a REPAIRED one.  Without it prompt0 KEEPS a prompt "
                         "that differs from prompts/_original/, because "
                         "re-deriving throws a repair away — measured on "
                         "hermesdesktop 2026-09-04.  Per-recording: "
                         "`reset_prompt: true` on the intake row")
    ap.add_argument("--no-chair-object", action="store_true",
                    help="do NOT track the chair as a second SAM2 object.  "
                         "Reproduces the pre-2026-09-04 single-object pass "
                         "exactly; the wingfix auto-repair is then the only "
                         "remedy for a LAW 48 refusal.  Per-recording, put "
                         "`no_chair_object: true` on the intake row")
    a = ap.parse_args()
    run = a.run.resolve()
    skip = {s.strip() for s in a.skip.split(",") if s.strip()}
    # the preflight needs the PLAN: it guards Modal uploads, not the batch
    vpn_preflight(allow=a.allow_vpn, skip=skip, sweep_local=a.sweep_local)

    rows = json.loads(a.intake.read_text())
    if isinstance(rows, dict):
        rows = rows.get("videos") or rows.get("intake") or []
    prep_dir = a.out or (run / "prep")
    prep_dir.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    print(f"PREP {len(rows)} recordings -> {run}   "
          f"({a.workers} workers, tag {a.tag})", flush=True)

    packages: dict[str, dict] = {}
    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        futures = {pool.submit(prep_front, row, run, skip=skip,
                               stride=a.stride, sweep_local=a.sweep_local,
                               sessions=(a.sessions.resolve() if a.sessions else (a.run.resolve() / "matting")),
                               no_chair=a.no_chair_object,
                               reset_prompt=a.reset_prompt,
                               display_plate=("plate" not in skip)): row["id"]
                   for row in rows}
        for fut, vid in futures.items():
            try:
                packages[vid] = fut.result()
            except Exception as exc:                    # never kill the batch
                packages[vid] = {"id": vid, "stages": {},
                                 "fatal": f"{type(exc).__name__}: {exc}",
                                 "traceback": traceback.format_exc()[-3000:]}

    if a.backend == "matanyone2":
        if not (run / "production-policy.json").exists():   # never overwrite a run's own policy (v4 runs say no phone test; run 25, 2026-09-22)
            (run / "production-policy.json").write_text(json.dumps({"version":2,"require_phone_approval":True,"final_delivery_requires_clerk":True}))
        if a.track_limit is not None:
            raise ValueError("Production matting never truncates a recording")
        sys.path.insert(0, str(F / "pipeline/matting"))
        from matting.prep_adapter import finish_package
        def production_mark(pkg, stage, rec):
            pkg.setdefault("stages", {})[stage] = rec
            mark_stage(pkg, stage, rec)
        rows_by_id = {row["id"]: row for row in rows}
        def production_finish(pkg):
            pkg["backend"] = "matanyone2"
            if "track" in skip or "ship" in skip:
                production_mark(pkg, "track", {"status":"skipped", "backend":"matanyone2"})
                # V4 (run 25, 2026-09-22): Astra reviews the outline and runs the matte, so prep
                # skips the track - but the selection-INPUTS marker used to be stamped only inside
                # the track (finish_package), and the workflow's selection watcher waited forever.
                st_, sess_ = pkg.get("stages", {}), Path(pkg["session"])
                if (st_.get("plate") or {}).get("status") in ("ok", "reused") and (st_.get("prompt0") or {}).get("prompt_png"):
                    production_mark(pkg, "selection", {"status": "ok", "note": "selection inputs ready for the outline review",
                        "selection": str(sess_ / "selection.json"), "plate": st_["plate"]["plate"],
                        "source": st_["cut"]["master"], "crop": str(sess_ / "plate.json"),
                        "initial_mask": st_["prompt0"]["prompt_png"]})
                return
            finish_package(pkg, run, rows_by_id[pkg["id"]],
                await_display=await_display_plate, mark=production_mark)
        with ThreadPoolExecutor(max_workers=min(3,a.workers)) as pool:
            list(pool.map(production_finish, packages.values()))
    else:
        # ---- (d) the fleet track, all at once — and, since 2026-09-03, the ship --
        remote_ship = ("ship" not in skip) and not a.ship_local
        if "track" not in skip:
            procs = dispatch_tracks(packages, run, tag=a.tag, limit=a.track_limit,
                                    gpu=a.gpu, remote_ship=remote_ship,
                                    emit=a.emit)
            if not remote_ship:
                # `--ship-local`: the container is not going to paint, so nothing
                # joined the background display cut.  Join it HERE, under the track,
                # so `ship.py` finds a finished file instead of racing the same
                # ffmpeg into the same path.
                for vid in list(_DISPLAY):
                    await_display_plate(vid, packages[vid])
            collect_tracks(packages, procs, tag=a.tag)
        else:
            # `--skip track` still wants the display plate joined and recorded: a
            # local re-ship needs the file, and a resumed batch needs the timing
            for vid, pkg in packages.items():
                await_display_plate(vid, pkg)
    
        # ---- (e) ship ------------------------------------------------------------
        if "ship" not in skip:
            def shippable(p: dict) -> bool:
                if (p.get("stages", {}).get("track") or {}).get("status") == "ok":
                    return True
                # a re-run with --skip track still ships, as long as the alpha the
                # earlier track wrote is on disk — re-shipping is free, re-tracking
                # is seven minutes and a GPU
                return (Path(p.get("session", "")) / f"alpha_{a.tag}.mkv").exists()
            todo = [p for p in packages.values() if shippable(p)]
            with ThreadPoolExecutor(max_workers=a.workers) as pool:
                if remote_ship and "track" not in skip:
                    list(pool.map(lambda p: collect_remote_ship(p, tag=a.tag,
                                                                emit=a.emit), todo))
                else:
                    list(pool.map(lambda p: ship_matte(p, run, tag=a.tag,
                                                       emit=a.emit), todo))
    
            # ---- (e2) THE AUTO-REPAIR LOOP -------------------------------------
            # A refused ship is not the end of the batch any more.  Every refusal
            # that names a repairable gate gets up to TWO rounds of the fix a human
            # would run, a re-track on the same lane and a re-ship through the same
            # lane, before it is reported.  The rounds run per recording in the
            # same pool, so N repairs still overlap on Modal.
            rows_by_id = {row["id"]: row for row in rows}
            needs = [p for p in packages.values() if refusal_gate(p)]
            if needs and not a.no_repair:
                print(f"AUTO-REPAIR: {len(needs)} refused ship(s) — up to "
                      f"{a.repair_rounds} round(s) each", flush=True)
                with ThreadPoolExecutor(max_workers=a.workers) as pool:
                    list(pool.map(
                        lambda p: auto_repair(
                            p, rows_by_id.get(p["id"], {}), run, base_tag=a.tag,
                            gpu=a.gpu, emit=a.emit, remote_ship=remote_ship,
                            limit=a.track_limit, stride=a.stride,
                            sweep_local=a.sweep_local,
                            max_rounds=a.repair_rounds), needs))
            elif needs:
                print(f"AUTO-REPAIR DISABLED (--no-repair): {len(needs)} refused "
                      f"ship(s) left as they are", flush=True)
    

    # ---- (g) the packages ----------------------------------------------------
    # A RE-RUN MERGES, IT DOES NOT ERASE.  `--skip track` after a track already
    # ran must not throw away the cost and the leak verdict that track recorded:
    # those measurements are the package, and re-measuring them costs a GPU.
    for vid, pkg in packages.items():
        prior_path = prep_dir / f"{vid}.json"
        if prior_path.exists():
            prior = json.loads(prior_path.read_text())
            merged = dict(prior.get("stages") or {})
            for name, st in pkg.get("stages", {}).items():
                # a stage this run did not actually EXECUTE never overwrites a
                # stage an earlier run measured
                if st.get("status") in ("skipped", "reused") and name in merged:
                    continue
                merged[name] = st
            pkg["stages"] = merged
        # THE FINAL TAG, NOT THE LAUNCH TAG.  After a repair the alpha and the
        # layers downstream must read are the LAST round's, so reconcile is
        # pointed at that tag; without this it would recover `run_v1.json` over
        # a `v2` that passed and hand the builder a refused matte.
        reconcile(pkg, final_tag(pkg, a.tag), emit=a.emit)
        # ---- the ledger, from the RECONCILED package ------------------------
        # The stage helpers already booked what THIS invocation ran; this pass
        # books what the package HOLDS — the BiRefNet sweep (whose money lives
        # inside the plate stage, which is why every run-11 total had to be
        # re-added by hand), plus a track or a ship this invocation recovered
        # from disk instead of running.  Both write the same ref as the live
        # call, so a recovered stage REPLACES its row instead of doubling it.
        ledger_sweep(run, vid, pkg)
        _st = (pkg.get("stages") or {})
        _tr = _st.get("track") or {}
        if _tr.get("status") == "ok" and _tr.get("run_record"):
            ledger_track(run, vid, _tr, _tr["run_record"],
                         note="SAM2 track" + (" (recovered from disk)"
                                              if _tr.get("recovered_from_disk")
                                              else ""))
        _sh = _st.get("ship") or {}
        if _sh.get("status") == "ok":
            ledger_ship(run, vid, _sh)
        _cut = _st.get("cut") or {}
        if _cut.get("transcript_tight") and _cut.get("tight_audio_duration_s"):
            ledger_scribe(run, vid,
                          {"file": _cut["transcript_tight"],
                           "audio_duration_secs": _cut["tight_audio_duration_s"]})
        pkg["finished"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        pkg["wall_s"] = round(sum(s.get("wall_s", 0)
                                  for s in pkg.get("stages", {}).values()), 1)
        (prep_dir / f"{vid}.json").write_text(json.dumps(pkg, indent=1))

    stages = ("cut", "plate", "display_plate", "prompt0", "track", "ship",
              "cues", "repair")
    # THE FIRST ATTEMPT'S MONEY IS STILL MONEY.  After a repair `stages.track`
    # and `stages.ship` point at the FINAL round, so the round-0 numbers would
    # vanish from the arithmetic; `stages.repair.round0` keeps them, and the
    # rounds' own spend is reported on its own line instead of being folded in.
    def _round0_cost(p: dict, which: str) -> float:
        rep = (p.get("stages") or {}).get("repair") or {}
        src = (rep.get("round0") or {}).get(which) if rep else None
        if src is None:
            src = (p.get("stages") or {}).get(which) or {}
        try:
            return float(src.get("cost_usd") or 0.0)
        except (TypeError, ValueError):
            return 0.0

    track_cost = round(sum(_round0_cost(p, "track")
                           for p in packages.values()), 4)
    sweep_cost = round(sum(sweep_cost_usd(p) for p in packages.values()), 4)
    ship_cost = round(sum(_round0_cost(p, "ship")
                          for p in packages.values()), 4)
    repair_cost = round(sum(
        float(((p.get("stages") or {}).get("repair") or {})
              .get("total_extra_cost_usd") or 0.0)
        for p in packages.values()), 4)
    repairs = {vid: len((((p.get("stages") or {}).get("repair") or {})
                         .get("rounds") or []))
               for vid, p in packages.items()
               if (p.get("stages") or {}).get("repair")}
    lines = [summary_line(p) for p in packages.values()]
    summary = {
        "run": str(run), "intake": str(a.intake), "videos": len(rows),
        "sessions_root": str(a.sessions.resolve() if a.sessions else (a.run.resolve() / "matting")),
        "workers": a.workers, "tag": a.tag, "emit": a.emit,
        "backend": a.backend, "gpu": "l4" if a.backend == "matanyone2" else a.gpu,
        "cost_basis": "runtime estimates, not provider invoice",
        "ship_where": ("laptop" if a.ship_local else "modal"),
        "batch_wall_s": round(time.time() - t0, 1),
        # EVERY Modal dollar this batch spent, not just the track's.  Until
        # 2026-09-03 this field counted the track alone and the BiRefNet master
        # sweep's $0.03-$0.06 per video had to be added by hand out of the plate
        # stage — which is exactly the kind of arithmetic a report gets wrong.
        "modal_cost_usd": round(track_cost + sweep_cost + ship_cost
                                + repair_cost, 4),
        "modal_cost_breakdown_usd": {"sweep": sweep_cost, "track": track_cost,
                                     "ship": ship_cost, "repair": repair_cost},
        # how many auto-repair rounds each recording needed; absent = none
        "repairs": repairs,
        "repair_rounds_max": a.repair_rounds,
        "repair_detail": {
            vid: {"final_tag": r.get("final_tag"),
                  "total_extra_cost_usd": r.get("total_extra_cost_usd"),
                  "total_extra_wall_s": r.get("total_extra_wall_s"),
                  "rounds": [{k: x.get(k) for k in
                              ("round", "gate", "fix", "tag", "track_seconds",
                               "ship_status", "cost_usd")}
                             for x in (r.get("rounds") or [])]}
            for vid, p in packages.items()
            if (r := ((p.get("stages") or {}).get("repair") or {}))},
        "summary_lines": lines,
        "ship_seconds": {
            vid: (p.get("stages", {}).get("ship") or {}).get("ship_seconds")
            for vid, p in packages.items()},
        "per_stage_wall_s": {
            vid: {s: (p.get("stages", {}).get(s) or {}).get("wall_s")
                  for s in stages}
            for vid, p in packages.items()},
        "status": {
            vid: {s: (p.get("stages", {}).get(s) or {}).get("status", "-")
                  for s in stages}
            for vid, p in packages.items()},
        "stage_totals_s": {
            s: round(sum((p.get("stages", {}).get(s) or {}).get("wall_s") or 0.0
                         for p in packages.values()), 1) for s in stages},
        "serial_equivalent_s": round(sum(
            p.get("wall_s", 0) for p in packages.values()), 1),
        "needs_source": {vid: (p.get("stages", {}).get("cues") or {}).get("needs_source")
                         for vid, p in packages.items()},
        "wing_review": [vid for vid, p in packages.items()
                        if (p.get("stages", {}).get("prompt0") or {}).get("wing_review")],
        "packages": {vid: str(prep_dir / f"{vid}.json") for vid in packages},
    }
    (prep_dir / "_batch.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))
    # ONE LINE PER RECORDING, LAST.  The batch json is the record; this is the
    # thing a human reads off the terminal without opening anything.
    print("\n=== PREP SUMMARY " + "=" * 44, flush=True)
    for ln in lines:
        print("  " + ln, flush=True)
    print("=" * 61, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
