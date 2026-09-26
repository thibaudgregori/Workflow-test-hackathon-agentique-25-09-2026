"""Build the tightened master (video+audio) from Raw Video Abik.

Caps every detected pause at KEEP seconds, mirroring the reference edit
(raw 55.2s -> ~51s). Outputs master_tight.mp4 + face crops + tight audio.
"""
import subprocess
from pathlib import Path

FACTORY = Path.home() / "Documents/Workspace/projects/personal/content/shorts-factory"
RAW = Path.home() / "Desktop/VideoTests/Raw Video Abik.mp4"
ASSETS = FACTORY / "assets"
ASSETS.mkdir(exist_ok=True)

# (silence_start, silence_end) from ffmpeg silencedetect noise=-35dB d=0.35
SILENCES = [
    (2.352354, 2.741979), (5.300083, 5.680875), (7.029229, 7.554125),
    (12.239333, 12.608417), (19.308438, 19.667687), (24.052771, 24.501771),
    (26.946875, 27.3325), (29.128875, 29.622604), (32.622208, 33.044),
    (34.362, 34.719833), (36.312542, 36.912146), (40.323625, 40.739792),
    (42.667125, 43.061708), (44.189667, 44.551875), (48.749125, 49.108208),
    (51.851417, 52.231208),
]
KEEP = 0.15  # seconds of pause to keep at each cut
END = 55.15  # just after last word (55.04)

segments = []
cursor = 0.0
for s, e in SILENCES:
    mid_in = s + KEEP / 2
    mid_out = e - KEEP / 2
    segments.append((cursor, mid_in))
    cursor = mid_out
segments.append((cursor, END))

total = sum(b - a for a, b in segments)
print(f"{len(segments)} segments, tightened duration = {total:.2f}s")

# frame-accurate single-pass trim+concat
vparts, aparts, filters = [], [], []
for i, (a, b) in enumerate(segments):
    filters.append(f"[0:v]trim=start={a:.4f}:end={b:.4f},setpts=PTS-STARTPTS[v{i}]")
    filters.append(f"[0:a]atrim=start={a:.4f}:end={b:.4f},asetpts=PTS-STARTPTS[a{i}]")
    vparts.append(f"[v{i}]")
    aparts.append(f"[a{i}]")
filters.append("".join(vparts) + f"concat=n={len(segments)}:v=1:a=0[vout]")
filters.append("".join(aparts) + f"concat=n={len(segments)}:v=0:a=1[aout]")

out = ASSETS / "master_tight.mp4"
subprocess.run([
    "ffmpeg", "-v", "error", "-i", str(RAW),
    "-filter_complex", ";".join(filters),
    "-map", "[vout]", "-map", "[aout]",
    "-c:v", "libx264", "-preset", "fast", "-crf", "18",
    "-c:a", "aac", "-b:a", "192k", "-r", "30",
    str(out), "-y",
], check=True)

# derived assets
# face bottom crop for split (bottom zone 576x512 => 9:8 aspect => crop 810x720 from 1280x720)
subprocess.run(["ffmpeg", "-v", "error", "-i", str(out),
                "-vf", "crop=810:720:235:0,scale=576:512", "-an",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                str(ASSETS / "face_bottom.mp4"), "-y"], check=True)
# full-screen face crop 9:16 => crop 405x720 centered on face
subprocess.run(["ffmpeg", "-v", "error", "-i", str(out),
                "-vf", "crop=405:720:437:0,scale=576:1024", "-an",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                str(ASSETS / "face_full.mp4"), "-y"], check=True)
# tight audio for transcription + muxing
subprocess.run(["ffmpeg", "-v", "error", "-i", str(out), "-vn",
                "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
                str(ASSETS / "audio_tight.wav"), "-y"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-i", str(out), "-vn",
                "-c:a", "aac", "-b:a", "192k",
                str(ASSETS / "audio_tight.m4a"), "-y"], check=True)
print("done")
