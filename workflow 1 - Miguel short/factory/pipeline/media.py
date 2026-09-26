"""ffprobe, once. 2026-09-20: the same four probes were re-implemented in thirteen files."""
from __future__ import annotations
import json, os, subprocess
from pathlib import Path


def ffprobe_bin() -> str:
    return os.environ.get("SHIP_FFPROBE", "ffprobe")


def probe(path: Path | str, entries: str, stream: str | None = None) -> str:
    """Raw csv=p=0 value(s) of `entries`, e.g. probe(p, "format=duration")."""
    cmd = [ffprobe_bin(), "-v", "error"]
    if stream:
        cmd += ["-select_streams", stream]
    cmd += ["-show_entries", entries, "-of", "csv=p=0", str(path)]
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout.strip()


def probe_duration(path: Path | str) -> float:
    return float(probe(path, "format=duration"))


def probe_wh(path: Path | str) -> tuple[int, int]:
    w, h = probe(path, "stream=width,height", "v:0").split(",")[:2]
    return int(w), int(h)


def probe_fps(path: Path | str) -> float:
    o = probe(path, "stream=r_frame_rate", "v:0")
    try:
        a, b = o.split("/")
        return float(a) / float(b)
    except Exception:                                             # noqa: BLE001
        return float(o) if o else 0.0


def probe_video_stream(path: Path | str, count_frames: bool = True) -> dict:
    """The first video stream as ffprobe's json (nb_read_frames, r_frame_rate, width, height, duration)."""
    cmd = [ffprobe_bin(), "-v", "error"] + (["-count_frames"] if count_frames else []) + \
          ["-select_streams", "v:0", "-show_entries", "stream=nb_read_frames,r_frame_rate,width,height,duration", "-of", "json", str(path)]
    return json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)["streams"][0]
