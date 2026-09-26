"""Quality-verification loop: compare rendered candidate against its reference.

Usage: qc_video.py <candidate.mp4> <faceless|split> [--label NAME]
Writes qc/<label>.json verdict. Model: gemini-3.5-flash-lite (bulk video QC).
Tool docs: tools/gemini.md
"""
import argparse
import json
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(Path.home() / "Documents/Workspace/.env")
import os as _os
_os.environ["GEMINI_API_KEY"] = _os.environ.get("GEMINI_API_KEY_GENIAL", _os.environ.get("GEMINI_API_KEY", ""))
FACTORY = Path.home() / "Documents/Workspace/projects/personal/content/shorts-factory"
REFS = {
    "faceless": Path.home() / "Desktop/VideoTests/Good Faceless Abik.mp4",
    "split": Path.home() / "Desktop/VideoTests/Good Split Abik.mp4",
}
CACHE = FACTORY / "qc/_ref_file_ids.json"
MODEL = "gemini-3.5-flash-lite"

client = genai.Client()

SCHEMA = {
    "type": "object",
    "properties": {
        "pass": {"type": "boolean"},
        "score_layout": {"type": "integer"},
        "score_captions": {"type": "integer"},
        "score_timing": {"type": "integer"},
        "score_audio": {"type": "integer"},
        "score_style_match": {"type": "integer"},
        "issues": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "severity": {"type": "string", "enum": ["critical", "major", "minor"]},
                    "at_seconds": {"type": "number"},
                    "description": {"type": "string"},
                },
                "required": ["severity", "description"],
            },
        },
        "summary": {"type": "string"},
    },
    "required": ["pass", "score_layout", "score_captions", "score_timing",
                 "score_audio", "score_style_match", "issues", "summary"],
}

PROMPT_R2 = """You are a strict video QC reviewer for a shorts factory.
The FIRST video is the brand REFERENCE. The SECOND video is a factory-produced CANDIDATE that uses
an INTENTIONALLY DIFFERENT layout — do NOT penalize different scene arrangements, different card
placements, or different backgrounds. The candidate must stay in the same BRAND FAMILY (cream/dark
canvases, terracotta+lime+yellow accents, same typography feel, clean professional energy) and be
internally flawless.

Judge the CANDIDATE on:
1. layout: internal quality of ITS OWN layout — no clipped or overlapping text, no elements
   touching each other awkwardly, balanced spacing, nothing important cut off by frame edges,
   captions never covered (score 0-10)
2. captions: legible, synced to the voiceover within ~0.3s, no long missing stretches (0-10)
3. timing: scene changes land on narration beats, animations intentional, no dead frames or
   flash glitches (0-10)
4. audio: voiceover clear, music under voice, SFX on entrances, no double audio or gaps (0-10)
5. style_match: brand-family fit ONLY — palette, typography feel, professional cleanliness vs the
   reference (0-10). Different layout structure is CORRECT here, not a defect.
6. ALSO check carefully: every real UI screenshot shown must be FULLY visible within the frame.
   Report cropping ONLY when a UI element is visibly cut by the video frame edge or by a card
   boundary. Do NOT report: text that wraps or breaks mid-word INSIDE the screenshot (e.g. JSON
   code line-wrapping — that is how the real UI renders), scrollable lists that naturally continue
   beyond a window, or small text that is merely low-resolution. When unsure, do not flag it.

pass = true only if there are NO critical issues, at most one major issue, and all scores >= 7.
List concrete issues with timestamps. Do NOT flag: intentional layout differences, content copy
variations, or font weight differences."""

PROMPT = """You are a strict video QC reviewer for a shorts factory.
The FIRST video is the golden REFERENCE. The SECOND video is a factory-produced CANDIDATE that must
match the reference's style and structure (content copy inside mock UI cards MAY legitimately differ;
that is a feature, not a bug).

Judge the CANDIDATE on:
1. layout: same scene structure/order, backgrounds, card/title/caption placement, no clipped or
   overlapping text, nothing important cut off (score 0-10)
2. captions: correct style for this format, legible, synced to the voiceover within ~0.3s, no
   missing long stretches (score 0-10)
3. timing: scenes change on the narration beats like the reference, animations feel intentional,
   no dead frames or flashing glitches (score 0-10)
4. audio: voiceover clear, background music present but quieter than voice, sound effects on
   entrances, no double audio/echo/silence gaps (score 0-10)
5. style_match: colors, fonts, energy vs the reference (score 0-10)

pass = true only if there are NO critical issues and at most one major issue and all scores >= 7.
List concrete issues with timestamps. Do NOT flag legitimate content variations (different sample
text in cards, different icon order) or small font substitutions as issues."""


def upload_with_retry(path: Path, attempts: int = 3):
    for i in range(attempts):
        try:
            f = client.files.upload(file=str(path))
            while f.state and f.state.name == "PROCESSING":
                time.sleep(2)
                f = client.files.get(name=f.name)
            if f.state and f.state.name == "ACTIVE":
                return f
        except Exception as e:
            print(f"upload attempt {i+1} failed: {e}", file=sys.stderr)
        time.sleep(3 * (i + 1))
    raise RuntimeError(f"upload failed: {path}")


def get_ref_file(fmt: str):
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    fid = cache.get(fmt)
    if fid:
        try:
            f = client.files.get(name=fid)
            if f.state and f.state.name == "ACTIVE":
                return f
        except Exception:
            pass
    f = upload_with_retry(REFS[fmt])
    cache[fmt] = f.name
    CACHE.write_text(json.dumps(cache))
    return f


def qc(candidate: Path, fmt: str, label: str, r2: bool = False):
    ref = get_ref_file(fmt)
    cand = upload_with_retry(candidate)
    resp = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Content(parts=[
                types.Part(file_data=types.FileData(file_uri=ref.uri, mime_type="video/mp4")),
                types.Part(file_data=types.FileData(file_uri=cand.uri, mime_type="video/mp4")),
                types.Part(text=PROMPT_R2 if r2 else PROMPT),
            ])
        ],
        config={
            "response_mime_type": "application/json",
            "response_schema": SCHEMA,
            "max_output_tokens": 8192,
        },
    )
    verdict = json.loads(resp.text)
    out = FACTORY / f"qc/{label}.json"
    out.write_text(json.dumps(verdict, indent=1))
    try:
        client.files.delete(name=cand.name)
    except Exception:
        pass
    return verdict


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate")
    ap.add_argument("fmt", choices=["faceless", "split"])
    ap.add_argument("--label", default=None)
    ap.add_argument("--r2", action="store_true")
    a = ap.parse_args()
    cand = Path(a.candidate)
    label = a.label or cand.stem
    v = qc(cand, a.fmt, label, r2=a.r2)
    print(json.dumps(v, indent=1))
    sys.exit(0 if v["pass"] else 1)
