"""Deep Gemini analysis of the two reference shorts (motion, timing, audio, style).

Tool docs: tools/gemini.md — google-genai SDK, Files API upload w/ retry,
VideoMetadata(fps=...) to raise sampling above the ~1fps default.
"""
import json
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(Path.home() / "Documents/Workspace/.env")

FACTORY = Path.home() / "Documents/Workspace/projects/personal/content/shorts-factory"
VIDEOS = {
    "faceless": Path.home() / "Desktop/VideoTests/Good Faceless Abik.mp4",
    "split": Path.home() / "Desktop/VideoTests/Good Split Abik.mp4",
}
MODEL = "gemini-3.6-flash"  # quality tier for the one-off deep style extraction (swapped from 3.1-pro-preview, Miguel 2026-08-08)

client = genai.Client()

PROMPT = """You are a motion-design forensic analyst. This is a ~50s vertical YouTube Short.
Reverse-engineer it EXHAUSTIVELY so a motion designer can rebuild it pixel-perfect and beat-perfect.

Report in markdown with these sections:

1. SCENE TIMELINE — every scene with start/end timestamps (to 0.1s), what is on screen, background color.
2. TYPOGRAPHY — every distinct text style: font family guess (serif/sans/mono, weight, italic), size relative to 576x1024 frame, color (hex estimate), letter spacing, case.
3. COLOR PALETTE — every color used with hex estimates and where it appears.
4. ANIMATION FORENSICS — for every element: entrance animation (type, direction, duration in ms, easing feel e.g. overshoot/spring/ease-out), idle motion (float/wobble/parallax), exit animation. Be precise about WHAT moves and HOW.
5. CAPTIONS — style (container, color, font), position on the 576x1024 frame, how they sync with the voiceover (word-by-word vs phrases), timing behavior, punctuation/case handling, any pop/scale animation per caption change.
6. TRANSITIONS — how scenes change (cut/slide/fade/wipe), durations.
7. AUDIO — background music (genre, energy, BPM feel), sound effects (whooshes, pops, clicks — at which moments), audio mixing vs voiceover; is the voiceover trimmed/tightened vs natural pauses?
8. LAYOUT SYSTEM — margins, safe areas, how cards/titles/captions are positioned and sized, rotation angles of cards/badges.
9. PACING RULES — how long scene elements hold, how animation timing relates to the narration beats.

Estimate timestamps carefully. Do not summarize; be exhaustive and specific with numbers."""


def upload_with_retry(path: Path, attempts: int = 3):
    for i in range(attempts):
        try:
            f = client.files.upload(file=str(path))
            while f.state and f.state.name == "PROCESSING":
                time.sleep(2)
                f = client.files.get(name=f.name)
            if f.state and f.state.name == "ACTIVE":
                return f
        except Exception as e:  # transient "Upload has already been terminated"
            print(f"upload attempt {i+1} failed: {e}", file=sys.stderr)
        time.sleep(3 * (i + 1))
    raise RuntimeError(f"upload failed for {path}")


for key, path in VIDEOS.items():
    out = FACTORY / f"analysis/gemini_deep_{key}.md"
    if out.exists():
        print(f"skip {key} (exists)")
        continue
    f = upload_with_retry(path)
    resp = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Content(parts=[
                types.Part(file_data=types.FileData(file_uri=f.uri, mime_type="video/mp4"),
                           video_metadata=types.VideoMetadata(fps=5)),
                types.Part(text=PROMPT),
            ])
        ],
        config={"max_output_tokens": 32768},
    )
    out.write_text(resp.text or "EMPTY")
    print(f"{key}: {len(resp.text or '')} chars -> {out}")
