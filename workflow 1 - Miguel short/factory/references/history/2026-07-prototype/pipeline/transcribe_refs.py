"""Word-level transcripts of the two reference audio tracks (edit-map vs raw)."""
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path.home() / "Documents/Workspace/.env")
FACTORY = Path.home() / "Documents/Workspace/projects/personal/content/shorts-factory"

for name in ["good_faceless", "good_split"]:
    out = FACTORY / f"analysis/transcript_{name}.json"
    if out.exists():
        continue
    resp = requests.post(
        "https://api.elevenlabs.io/v1/speech-to-text",
        headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"]},
        data=[("model_id", "scribe_v2"), ("timestamps_granularity", "word"), ("tag_audio_events", "false")],
        files={"file": (f"{name}.wav", open(FACTORY / f"audio/{name}.wav", "rb"), "audio/wav")},
        timeout=300,
    )
    resp.raise_for_status()
    out.write_text(json.dumps(resp.json(), indent=2, ensure_ascii=False))
    print(name, "ok")

# Edit-map: compare word sequences raw vs faceless reference
raw = json.loads((FACTORY / "analysis/transcript.json").read_text())
ref = json.loads((FACTORY / "analysis/transcript_good_faceless.json").read_text())
rw = [w for w in raw["words"] if w["type"] == "word"]
fw = [w for w in ref["words"] if w["type"] == "word"]
print(f"raw words={len(rw)} span={rw[0]['start']:.2f}-{rw[-1]['end']:.2f}")
print(f"ref words={len(fw)} span={fw[0]['start']:.2f}-{fw[-1]['end']:.2f}")
# print aligned offsets every 10 words
for i in range(0, min(len(rw), len(fw)), 10):
    print(f"  [{i:3d}] raw '{rw[i]['text']}'@{rw[i]['start']:.2f}  ref '{fw[i]['text']}'@{fw[i]['start']:.2f}  offset={rw[i]['start']-fw[i]['start']:+.2f}")
