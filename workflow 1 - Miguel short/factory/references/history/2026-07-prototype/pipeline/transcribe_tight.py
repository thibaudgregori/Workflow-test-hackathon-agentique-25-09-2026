"""Word-level Scribe transcript of the tightened master audio (caption source of truth)."""
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path.home() / "Documents/Workspace/.env")
FACTORY = Path.home() / "Documents/Workspace/projects/personal/content/shorts-factory"
OUT = FACTORY / "analysis/transcript_tight.json"

resp = requests.post(
    "https://api.elevenlabs.io/v1/speech-to-text",
    headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"]},
    data=[("model_id", "scribe_v2"), ("timestamps_granularity", "word"), ("tag_audio_events", "false")],
    files={"file": ("audio_tight.wav", open(FACTORY / "assets/audio_tight.wav", "rb"), "audio/wav")},
    timeout=300,
)
resp.raise_for_status()
data = resp.json()
OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False))
words = [w for w in data["words"] if w["type"] == "word"]
print(f"words={len(words)} span={words[0]['start']:.2f}-{words[-1]['end']:.2f}")
for w in words:
    print(f"{w['start']:6.2f} {w['end']:6.2f}  {w['text']}")
