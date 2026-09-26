"""Generate music beds + SFX with ElevenLabs (music.compose + sound-generation).

Tool docs: tools/elevenlabs.md
"""
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path.home() / "Documents/Workspace/.env")
KEY = os.environ["ELEVENLABS_API_KEY"]
SFX_DIR = Path.home() / "Documents/Workspace/assets/audio/sfx/shorts-factory"
MUSIC_DIR = Path.home() / "Documents/Workspace/assets/audio/music/shorts-factory"
SFX_DIR.mkdir(parents=True, exist_ok=True)
MUSIC_DIR.mkdir(parents=True, exist_ok=True)

MUSIC = {
    "bed_faceless": ("Upbeat playful lo-fi hip hop instrumental, 118 BPM, bouncy plucks, light "
                     "swung percussion, warm bass, positive energetic vibe for a fast-paced tech "
                     "explainer short. No vocals, no melody lead that fights speech, consistent "
                     "energy start to finish.", 52000),
    "bed_split": ("Laid-back jazzy lo-fi hip hop instrumental, 87 BPM, muted Rhodes chords, dusty "
                  "relaxed snare, soft vinyl texture, chill confident vibe under a voiceover. No "
                  "vocals, consistent energy start to finish.", 52000),
}
SFX = {
    "pop": ("Single soft rubbery UI pop, short, clean, subtle, like a bubble tap in a modern app", 0.6),
    "whoosh": ("Quick smooth low air whoosh transition, short, soft, cinematic UI swipe", 0.7),
    "boom": ("Deep soft cinematic sub bass impact thud, short, muffled, weighty", 0.9),
    "click": ("Tiny crisp digital toggle switch click, very short, clean UI sound", 0.5),
    "ding": ("Soft pleasant success chime, single gentle high bell note, short, subtle", 0.8),
}

for name, (prompt, ms) in MUSIC.items():
    out = MUSIC_DIR / f"{name}.mp3"
    if out.exists():
        print("skip", name); continue
    r = requests.post("https://api.elevenlabs.io/v1/music",
                      headers={"xi-api-key": KEY},
                      json={"prompt": prompt, "music_length_ms": ms}, timeout=600)
    r.raise_for_status()
    out.write_bytes(r.content)
    print(name, len(r.content), "bytes")

for name, (prompt, dur) in SFX.items():
    out = SFX_DIR / f"{name}.mp3"
    if out.exists():
        print("skip", name); continue
    r = requests.post("https://api.elevenlabs.io/v1/sound-generation",
                      headers={"xi-api-key": KEY},
                      json={"text": prompt, "duration_seconds": dur}, timeout=300)
    r.raise_for_status()
    out.write_bytes(r.content)
    print(name, len(r.content), "bytes")
print("done")
