#!/usr/bin/env python3
"""Run-15 intake: audio health gate + ElevenLabs Scribe v2 raw transcription.

Same contract as `shorts_run10/intake_run10.py`, but instrumented for the
end-to-end benchmark and run in PARALLEL (one thread per recording), because
this batch is four raws and the benchmark measures wall time.

  1. ffprobe the container (duration, audio stream present).
  2. ffmpeg `volumedetect` on the audio ONLY -- mean below -60 dBFS (or no
     audio stream at all) is a dead mic and is NEVER uploaded to a paid API.
  3. Extract mono 16 kHz s16le wav (the standard factory intake audio).
  4. Scribe v2 with the shared workspace keyterm vocabulary
     (`execution/transcription_vocabulary.json`). No batch-specific keyterms at
     intake; those land per-video at the tight-cut pass.
  5. Write the full response to intake/transcripts/<stem>.json (cached).

Every phase writes ISO start/end + wall seconds into intake/timings.json.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path.home() / "Documents" / "Workspace"
RUN = WORKSPACE / "projects/personal/content/shorts-factory/runs/shorts_run17"
MOVIES = Path.home() / "Movies"
TRANSCRIPTS = RUN / "intake" / "transcripts"
REPORT = RUN / "intake" / "audio_health.json"
TIMINGS = RUN / "intake" / "timings.json"
VOCAB = WORKSPACE / "execution" / "transcription_vocabulary.json"

sys.path.insert(0, str(WORKSPACE / "projects/personal/infra/agent-tools/video-use/helpers"))
import transcribe as vu  # noqa: E402

SILENCE_DB = -60.0

RAWS = [
    MOVIES / "2026-09-04 13-15-13.mp4",
    MOVIES / "2026-09-04 13-21-23.mp4",
    MOVIES / "2026-09-04 13-27-09.mp4",
    MOVIES / "2026-09-04 13-29-36.mp4",
    MOVIES / "2026-09-04 13-32-18.mp4",
    MOVIES / "2026-09-04 13-44-59.mp4",
    MOVIES / "2026-09-04 13-46-50.mp4",
    MOVIES / "2026-09-04 13-49-31.mp4",
    MOVIES / "2026-09-04 13-55-18.mp4",
    MOVIES / "2026-09-04 13-58-49.mp4",
    MOVIES / "2026-09-04 14-02-35.mp4",
    MOVIES / "2026-09-04 14-05-00.mp4",
    MOVIES / "2026-09-04 14-08-35.mp4",
    MOVIES / "2026-09-04 14-17-15.mp4",
    MOVIES / "2026-09-04 14-41-05.mp4",
    MOVIES / "2026-09-04 14-55-43.mp4",
    MOVIES / "2026-09-04 14-59-09.mp4",
    MOVIES / "2026-09-04 15-02-28.mp4",
    MOVIES / "2026-09-04 15-05-10.mp4",
    MOVIES / "2026-09-04 15-14-05.mp4",
]


def iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def probe(video: Path) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration:stream=codec_type,codec_name,channels,sample_rate",
         "-of", "json", str(video)],
        capture_output=True, text=True, check=True,
    ).stdout
    data = json.loads(out)
    audio = [s for s in data.get("streams", []) if s.get("codec_type") == "audio"]
    return {
        "duration": float(data["format"]["duration"]),
        "audio_streams": len(audio),
        "audio": audio[0] if audio else None,
    }


def volumedetect(video: Path) -> dict:
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(video),
         "-vn", "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    err = proc.stderr

    def grab(name: str) -> float | None:
        m = re.search(rf"{name}:\s*(-?[\d.]+) dB", err)
        return float(m.group(1)) if m else None

    return {"mean_db": grab("mean_volume"), "max_db": grab("max_volume")}


def health_one(video: Path) -> dict:
    t0 = time.time()
    info = probe(video)
    vol = volumedetect(video)
    healthy = (
        info["audio_streams"] > 0
        and vol["mean_db"] is not None
        and vol["mean_db"] > SILENCE_DB
    )
    t1 = time.time()
    row = {
        "recording": video.stem,
        "duration": round(info["duration"], 2),
        "audio_streams": info["audio_streams"],
        "mean_db": vol["mean_db"],
        "max_db": vol["max_db"],
        "healthy": healthy,
        "_t": {"start": iso(t0), "end": iso(t1), "wall_s": round(t1 - t0, 2)},
    }
    print(f"[probe] {video.stem}  {row['duration']}s  mean {vol['mean_db']} dB  "
          f"max {vol['max_db']} dB  healthy={healthy}  ({row['_t']['wall_s']}s)", flush=True)
    return row


def scribe_one(video: Path, key: str, keyterms: list[str]) -> dict:
    stem = video.stem
    out = TRANSCRIPTS / f"{stem}.json"
    t0 = time.time()
    cached = out.exists()
    if cached:
        payload = json.loads(out.read_text())
    else:
        with tempfile.TemporaryDirectory() as td:
            wav = Path(td) / f"{stem}.wav"
            ta = time.time()
            vu.extract_audio(video, wav)
            tb = time.time()
            print(f"[audio] {stem}  extracted in {tb - ta:.1f}s", flush=True)
            payload = vu.call_scribe(wav, key, language="en", num_speakers=1,
                                     keyterms=keyterms)
        out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    t1 = time.time()
    words = [w for w in payload.get("words", []) if w.get("type") == "word"]
    print(f"[scribe] {stem}  {len(words)} words -> {out.name}  ({t1 - t0:.1f}s, cached={cached})",
          flush=True)
    return {
        "recording": stem,
        "cached": cached,
        "words": len(words),
        "chars": len(payload.get("text", "")),
        "audio_duration_secs": payload.get("audio_duration_secs"),
        "_t": {"start": iso(t0), "end": iso(t1), "wall_s": round(t1 - t0, 2)},
    }


def main() -> None:
    from dotenv import load_dotenv
    load_dotenv(WORKSPACE / ".env")
    key = os.environ.get("ELEVENLABS_API_KEY") or vu.load_api_key()
    keyterms = list(vu.load_keyterms(VOCAB))

    timings: dict = {"keyterms": len(keyterms), "phases": {}}

    # --- Phase 1: mute check (parallel) ---------------------------------
    p0 = time.time()
    with ThreadPoolExecutor(max_workers=len(RAWS)) as ex:
        health = list(ex.map(health_one, RAWS))
    p1 = time.time()
    timings["phases"]["mute_check"] = {
        "start": iso(p0), "end": iso(p1), "wall_s": round(p1 - p0, 2),
        "per_recording": {r["recording"]: r["_t"] for r in health},
    }
    REPORT.write_text(json.dumps({"keyterms": len(keyterms), "recordings": health},
                                 indent=2), encoding="utf-8")

    ok = [v for v, r in zip(RAWS, health) if r["healthy"]]
    muted = [r["recording"] for r in health if not r["healthy"]]
    if muted:
        print(f"[GATE] MUTED, not transcribed: {muted}", flush=True)

    # --- Phase 2: Scribe (parallel, one thread per recording) -----------
    s0 = time.time()
    with ThreadPoolExecutor(max_workers=max(1, len(ok))) as ex:
        scribed = list(ex.map(lambda v: scribe_one(v, key, keyterms), ok))
    s1 = time.time()
    timings["phases"]["scribe"] = {
        "start": iso(s0), "end": iso(s1), "wall_s": round(s1 - s0, 2),
        "per_recording": {r["recording"]: r["_t"] for r in scribed},
    }

    by_stem = {r["recording"]: r for r in scribed}
    for row in health:
        s = by_stem.get(row["recording"])
        row["status"] = "OK" if s else "MUTED — not transcribed"
        if s:
            row["words"] = s["words"]
            row["chars"] = s["chars"]
            row["audio_duration_secs"] = s["audio_duration_secs"]
    REPORT.write_text(json.dumps({"keyterms": len(keyterms), "recordings": health},
                                 indent=2), encoding="utf-8")

    timings["total_script_wall_s"] = round(s1 - p0, 2)
    TIMINGS.write_text(json.dumps(timings, indent=2), encoding="utf-8")
    print("\nWROTE", REPORT)
    print("WROTE", TIMINGS)


if __name__ == "__main__":
    main()
