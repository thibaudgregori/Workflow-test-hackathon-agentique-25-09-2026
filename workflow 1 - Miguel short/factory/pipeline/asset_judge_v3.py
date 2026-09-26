"""Asset judge v3 — Gemini VISUALLY inspects every candidate asset before production.

For each video: sends the actual images (x card, photos, demo-video still) + transcript
summary. Rules per asset: use | crop (with region) | reject; plus per-beat visual plan
(real asset vs coded_2d) honoring STANDARD tweet discipline & phone legibility.
Writes <run>/plans/asset_verdicts_v3.json.  usage: asset_judge_v3.py [<run folder>]
"""
import json
import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path.home() / "Documents/Workspace/.env")
os.environ["GEMINI_API_KEY"] = os.environ.get("GEMINI_API_KEY_GENIAL", os.environ.get("GEMINI_API_KEY", ""))
from google import genai
from google.genai import types

FACTORY = Path.home() / "Documents/Workspace/projects/personal/content/shorts-factory"
# MOVED OUT OF run 3 ON 2026-09-20: the run is an argument (default: the newest
# shorts_run* on disk); plans and verdicts are read from and written to THAT run.
import sys
_runs = sorted((p for p in (FACTORY / "runs").glob("shorts_run*") if p.is_dir()), key=lambda p: int("".join(c for c in p.name if c.isdigit()) or 0))
R1 = R3 = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else _runs[-1]
(R3 / "plans").mkdir(parents=True, exist_ok=True)
MODEL = "gemini-3.6-flash"
client = genai.Client()

plans = json.loads((R1 / "plans/content_plans.json").read_text())["videos"]

SCHEMA = {
    "type": "object",
    "properties": {
        "assets": {"type": "array", "items": {"type": "object", "properties": {
            "name": {"type": "string"},
            "ruling": {"type": "string", "enum": ["use", "crop", "reject"]},
            "phone_legible": {"type": "boolean"},
            "crop_region": {"type": "string"},
            "value_reason": {"type": "string"},
            "max_seconds": {"type": "number"}},
            "required": ["name", "ruling", "phone_legible", "value_reason"]}},
        "beats": {"type": "array", "items": {"type": "object", "properties": {
            "n": {"type": "integer"},
            "use": {"type": "string", "enum": ["x_card", "photo", "video", "coded_2d"]},
            "asset_name": {"type": "string"},
            "visual_concept": {"type": "string"}},
            "required": ["n", "use", "visual_concept"]}},
    },
    "required": ["assets", "beats"],
}

PROMPT = """You are the ASSET judge for a shorts factory (STANDARD v1). You are given the actual
candidate images for one short, plus its narration. VISUALLY inspect each asset and rule:

- "use": genuinely adds value shown as-is; readable on a PHONE (vertical video, asset occupies
  roughly the top 40% of a 6-inch screen — dense screenshots usually are NOT readable).
- "crop": valuable but only a region matters or full version is illegible — name the crucial
  region precisely in crop_region.
- "reject": low visual value, redundant with speech, dense/unreadable, or generic (a tweet that
  is just text restating the idea is usually reject or <=3s use — the creator adds value ON TOP,
  he does not recycle tweets; NEVER rely on tweet metrics for value).
For every used/cropped asset set max_seconds (tweets <=4s; only the beat where it IS the news).

Then output the per-beat plan: which beat (if any) shows which real asset, everything else
coded_2d with a one-line visual_concept that matches what is SPOKEN in that beat (diagrams,
counters, logos, checklists — never text-echo of the narration).

Narration beats:
{beats}
Full narration: {narration}"""

out = {}
for v in plans:
    stem = v["stem"]
    tr = json.loads((R1 / "cuts" / stem / "transcript_tight.json").read_text())
    words = [w for w in tr["words"] if w["type"] == "word"]
    narration = " ".join(w["text"] for w in words)[:1600]
    beats_desc = "\n".join(f"  {b['n']}. {b['title']} (starts: \"{b['anchor']}\")" for b in v["beats"])

    parts = []
    names = []
    xc = R1 / v["x_card"]
    if xc.exists():
        parts.append(types.Part.from_bytes(data=xc.read_bytes(), mime_type="image/png"))
        names.append(f"x_card ({v['x_handle']} tweet embed)")
    for j, ph in enumerate(v.get("photos", [])):
        p = R1 / ph
        if p.exists():
            parts.append(types.Part.from_bytes(data=p.read_bytes(), mime_type="image/jpeg"))
            names.append(f"photo:{j}")
    if v.get("video_asset"):
        still = Path(f"/tmp/aj3_{v['id']}.jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-ss", "3", "-i", str(R1 / v["video_asset"]),
                        "-frames:v", "1", str(still), "-y"])
        if still.exists():
            parts.append(types.Part.from_bytes(data=still.read_bytes(), mime_type="image/jpeg"))
            names.append("video (still frame of demo footage)")

    listing = "\n".join(f"Image {i+1} = {n}" for i, n in enumerate(names))
    parts.append(types.Part(text=listing + "\n\n" + PROMPT.format(beats=beats_desc, narration=narration)))
    resp = client.models.generate_content(
        model=MODEL, contents=[types.Content(parts=parts)],
        config={"response_mime_type": "application/json", "response_schema": SCHEMA,
                "max_output_tokens": 6144},
    )
    out[v["id"]] = json.loads(resp.text)
    rulings = {a["name"]: a["ruling"] for a in out[v["id"]]["assets"]}
    print(v["id"], rulings, "->", [b["use"] for b in out[v["id"]]["beats"]])

(R3 / "plans/asset_verdicts_v3.json").write_text(json.dumps(out, indent=1))
print("ASSET JUDGE V3 DONE")
