"""Transcribe raw Abik audio with ElevenLabs Scribe v2, word-level timestamps.

Tool docs: tools/elevenlabs.md
"""
import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path.home() / "Documents/Workspace/.env")

FACTORY = Path.home() / "Documents/Workspace/projects/personal/content/shorts-factory"
AUDIO = FACTORY / "audio/raw_abik.wav"
OUT = FACTORY / "analysis/transcript.json"

resp = requests.post(
    "https://api.elevenlabs.io/v1/speech-to-text",
    headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"]},
    data=[
        ("model_id", "scribe_v2"),
        ("timestamps_granularity", "word"),
        ("tag_audio_events", "false"),
    ],
    files={"file": ("raw_abik.wav", open(AUDIO, "rb"), "audio/wav")},
    timeout=300,
)
resp.raise_for_status()
data = resp.json()
OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False))
print("TEXT:\n", data.get("text", ""))
words = [w for w in data.get("words", []) if w.get("type") == "word"]
print(f"\nWORDS: {len(words)}, span {words[0]['start']:.2f}-{words[-1]['end']:.2f}s" if words else "no words")
