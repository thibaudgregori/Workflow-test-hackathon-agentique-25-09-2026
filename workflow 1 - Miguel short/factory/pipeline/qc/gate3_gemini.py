"""QC v3 — the STANDARD gate. THREE Gemini passes (describe + visual + semantic).

Usage: gate3_gemini.py <candidate.mp4> <video_id> [--run <run>] [--transcript <words.json>] [--label X] [--no-describe]
(pipeline/qc_v3.py until 2026-09-20; the verdict lands in <run>/review/qc/<label>.json)
video_id resolves the transcript (<run>/cuts/<stem>/transcript_tight.json, newest run wins).
pass requires ALL enabled passes clean. Deterministic adjudicators:
idle_motion_scan.py (run separately by the build agent before disputing motion
verdicts), face_center_check.py (face centring), phone_crops.py (legibility).

DESCRIBE BEFORE JUDGE (Miguel, 2026-09-02) — ON BY DEFAULT
-----------------------------------------------------------
Miguel shipped a bespoke "moon" object that was illegible and meaningless at
phone size, and this gate said PASS. The reason is structural: the VISUAL and
SEMANTIC prompts are **rubric screeners**. They ask "does this video break rule
X" and a model answering a rubric will happily answer "no" about a frame it never
actually parsed. Nothing forced it to say what it SAW.

The DESCRIBE pass forces it. Before any judging, the model writes a one-line,
plain, jargon-free description of each sampled frame - literally "a sheet of
paper stamped IMPOSSIBLE TASK; the Codex logo below it" - as a stranger scrolling
would see it, naming objects FROM THE PIXELS. Two mechanical findings follow from
those descriptions, and both are errors, not notes:

  unidentifiable_object  the description cannot name what an object IS
                         ("an orange blob", "some kind of shape", "unclear icon")
  beat_mismatch          the description does not match the transcript words
                         spoken at that timestamp

A description is much harder to fake than a rubric answer: to write "an orange
crescent" the model has to look, and once "an orange crescent" is on the page next
to the words "one night of compute", the mismatch is self-evident.

`--no-describe` restores the exact pre-2026-09-02 two-pass behaviour. The output
JSON is a superset of the old one (`pass`, `visual`, `semantic` unchanged), so
every existing reader keeps working.
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path.home() / "Documents/Workspace/.env")
os.environ["GEMINI_API_KEY"] = os.environ.get("GEMINI_API_KEY_GENIAL", os.environ.get("GEMINI_API_KEY", ""))
from google import genai
from google.genai import types

FACTORY = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(FACTORY / "pipeline"))
# MOVED OUT OF run 3 ON 2026-09-20 (Miguel: nothing permanent lives in a run); the verdict goes
# into the run it judges (<run>/review/qc/), resolved in main() from --run or the newest run.
MODEL = os.environ.get("GEMINI_GATE3_MODEL", "gemini-3.5-flash-lite")  # Miguel 2026-09-03, was gemini-3.6-flash
client = genai.Client()

STEMS = {"hackers": "2026-08-08_20-47-44", "grokbuild": "2026-08-08_20-54-32",
         "hermes": "2026-08-08_20-59-13", "grokprice": "2026-08-08_21-09-49",
         "deepresearch": "2026-08-08_21-14-48", "slop": "2026-08-08_21-19-39",
         "threed": "2026-08-08_21-35-36", "productivity": "2026-08-08_21-40-17",
         "meatwrapper": "2026-08-08_22-15-31", "fablevssol": "2026-08-08_22-21-45"}

# Video id -> its tight transcript. Run-1 ids keep resolving through STEMS exactly
# as before; later runs cut in their own directories, so they register their full
# path here instead of being assumed to live in the first run.
TRANSCRIPTS = {
    # auto-discovered: any run's cuts/<id>/transcript_tight.json registers itself,
    # so concurrent sessions never need to edit this file (shadowing hazard, 2026-08-11)
    **{c.parent.name: c
       for c in sorted(FACTORY.glob("runs/shorts_run*/cuts/*/transcript_tight.json"))
       },
}

SCHEMA = {
    "type": "object",
    "properties": {
        "pass": {"type": "boolean"},
        "errors": {"type": "array", "items": {"type": "object", "properties": {
            "kind": {"type": "string"}, "at_seconds": {"type": "number"},
            "description": {"type": "string"}}, "required": ["kind", "description"]}},
        "minor_notes": {"type": "array", "items": {"type": "string"}},
        "summary": {"type": "string"},
    },
    "required": ["pass", "errors", "minor_notes", "summary"],
}

DESCRIBE_SCHEMA = {
    "type": "object",
    "properties": {
        "frames": {"type": "array", "items": {"type": "object", "properties": {
            "at_seconds": {"type": "number"},
            "description": {"type": "string"},
            "spoken_words": {"type": "string"},
            "object_identifiable": {"type": "boolean"},
            "unidentifiable_reason": {"type": "string"},
            "matches_beat": {"type": "boolean"},
            "mismatch_reason": {"type": "string"},
        }, "required": ["at_seconds", "description", "spoken_words",
                        "object_identifiable", "matches_beat"]}},
        "summary": {"type": "string"},
    },
    "required": ["frames", "summary"],
}

DESCRIBE = """You are the DESCRIBE pass of a shorts QC gate. You are NOT judging yet and you
must not grade, score, or mention rules. Your only job is to SAY WHAT IS ON SCREEN.

Sample {n} frames spread evenly across the whole video (include one near 1s and one near the
end). For each frame:

1. "description": ONE line of plain, ordinary English describing what a stranger scrolling on a
   phone SEES. Name every object FROM THE PIXELS, never from what it was probably meant to be.
   Good: "a sheet of paper stamped IMPOSSIBLE TASK, the Codex logo below it, his face under the
   caption". Good: "a stack of seven orange bars next to a stack of four black bars".
   BAD: "the build-plate diagram" (that is a name from a plan, not from the pixels).
   If a shape has no honest everyday name, say exactly that: "an orange crescent, unclear what
   it represents". Never invent a meaning to fill the gap.
2. "spoken_words": the words being spoken AT that timestamp - read them off the caption pill on
   screen, which is what the viewer reads. If no caption is up, write "(none)".
3. "object_identifiable": false when any non-trivial object in the frame cannot be named as a
   real thing by looking at it (a blob, an abstract glyph, an unlabelled symbol, an icon you
   cannot identify, text too small to read at phone size). Put the offending object in
   "unidentifiable_reason". Faces, captions, plain background and the handle card are trivial and
   never make a frame unidentifiable on their own.
   SO IS THE CUTOUT'S DEPTH BAND. In the cutout format a receding grid of small, faded tool tiles
   sits BEHIND the presenter and travels sideways across the frame. That band is the format's own
   wallpaper: its chassis sizes it at 78/116/148px and 24-70% opacity precisely so it reads as
   TEXTURE rather than as content, and every tile in it is proved to be a real registered provider
   mark by two separate gates before a single frame is rendered. Naming it is not this pass's job.
   Never set "object_identifiable" false because of the background grid, the depth lanes, the rows
   of small icons behind him, or the wallpaper. Judge the objects on the STAGE - the things drawn
   in FRONT of him and ABOVE him, the cards, diagrams, plates and printed keys.
4. "matches_beat": does what you described argue what is being said at that instant? false when
   the picture is unrelated, is still showing the previous idea, is an empty zone, or names a
   different subject than the sentence. Put the reason in "mismatch_reason".

Be literal and be blunt. An honest "I cannot tell what this is" is the single most valuable thing
you can write here.
TRANSCRIPT (word: start-end):
{transcript}"""

VISUAL = """You are the visual QC gate for a shorts factory (STANDARD v1). Judge ONLY this video.
FAIL kinds (cite timestamps):
- idle_motion: any element levitating/floating/drifting/continuously zooming or panning while
  "held". Approved motion = discrete builds/ticks/highlight jumps followed by complete stillness.
- overlay: collisions, elements touching, clipped/overflowing text (incl. inside assets), arrows
  drawn on top of the boxes they point at (arrows must stop at box edges), unequal sizes for
  same-theme paired cards, off-center compositions where centering is clearly intended, blank or
  black zones (incl. first/last frames).
- caption: any text at the TOP of the frame that echoes the spoken words or duplicates the seam
  captions (top zone must never transcribe speech; short KEY TERMS of 1-3 words are allowed);
  seam captions drifting >0.5s or missing >5s; a stutter/partial word visible in captions.
- tweet: tweet on screen longer than ~4 seconds; tweet metrics (likes/reposts/views) visible at
  any moment.
- legibility: embedded screenshot/image whose text is unreadably small for a phone screen.
- cut: frozen frames, stutters/repeats, double-fired transitions, flash glitches (the speaker's
  intentional jump cuts between sentences are FINE).
- face: any zoom/punch-in on the speaker, or a full-frame face section (the split must hold to
  the end with an outro card).
- pop_in: a structural element (connector/arrow, bus/tree, card, rule) that you can SEE arrive
  MID-BEAT with no entrance at all - complete at full size and full opacity the instant it
  exists, with no partially drawn / smaller / fainter state anywhere - or a connector drawn
  AFTER the card it delivers instead of before it (arrows deliver cards, never trail them).
  Apply this strictly: if ANY frame shows the element partially formed, it HAS an entrance and
  is NOT an error however quick; if the sampling leaves the entrance unresolvable, do NOT
  report it. NEVER an error: the cast already on screen at a section's FIRST frame after a cut
  or ground change - openings are authored on-screen by design, and a blank opening frame is
  itself a failure.
pass=true only if errors is empty."""

SEMANTIC = """You are the semantic QC gate (STANDARD v1). You get the video and its word-timed
transcript. Judge whether the visuals SERVE the narration:
- value: for each stretch of ~5-10s, does the top zone add understanding BEYOND the seam captions
  (diagram/data/logos/highlight)? Text-only echo of the speech = FAIL (kind "no_added_value").
- highlight_match: every highlight/ring/underline must sit on the region matching what is being
  said at that moment; mismatch = FAIL.
- logo_use: when a named tool/model is spoken (Claude Code, Codex, Grok Build, ChatGPT, Gemini,
  Hermes/Nous, v0, Kimi...), the visual should show its LOGO (not a text pill) at least the first
  time; text-pill-only for a named tool = FAIL (kind "missing_logo").
- claim_sync: on-screen checkmarks/list items/numbers must correspond to what HE says (not
  unrelated copy), ticking in sync; numbers he says (percentages, prices, counts) shown wrong or
  absent where a data visual exists = FAIL.
- key_term: the video's key term should debut large/center near its first utterance.
pass=true only if errors is empty.
TRANSCRIPT (word: start-end):
{transcript}"""


def upload_retry(path, attempts=3):
    for i in range(attempts):
        try:
            f = client.files.upload(file=str(path))
            while f.state and f.state.name == "PROCESSING":
                time.sleep(2)
                f = client.files.get(name=f.name)
            if f.state and f.state.name == "ACTIVE":
                return f
        except Exception as e:
            print(f"upload retry {i+1}: {e}", file=sys.stderr)
        time.sleep(3 * (i + 1))
    raise RuntimeError(f"upload failed: {path}")


USAGE = {"in": 0, "out": 0, "thoughts": 0, "calls": 0}
# gemini-3.5-flash-lite (tools/gemini.md, 2026-09-03): $0.30 / MTok in, $2.50 / MTok out (thinking bills as output)
PRICE_IN = float(os.environ.get("GEMINI_GATE3_PRICE_IN", "0.30")) / 1e6
PRICE_OUT = float(os.environ.get("GEMINI_GATE3_PRICE_OUT", "2.50")) / 1e6


def _tally(resp):
    um = getattr(resp, "usage_metadata", None)
    if um is None:
        return
    USAGE["in"] += int(getattr(um, "prompt_token_count", 0) or 0)
    USAGE["out"] += int(getattr(um, "candidates_token_count", 0) or 0)
    USAGE["thoughts"] += int(getattr(um, "thoughts_token_count", 0) or 0)
    USAGE["calls"] += 1


def judge(cand, prompt, schema=SCHEMA, max_tokens=8192):
    resp = client.models.generate_content(
        model=MODEL,
        contents=[types.Content(parts=[
            types.Part(file_data=types.FileData(file_uri=cand.uri, mime_type="video/mp4")),
            types.Part(text=prompt)])],
        config={"response_mime_type": "application/json", "response_schema": schema,
                "max_output_tokens": max_tokens},
    )
    _tally(resp)
    return json.loads(resp.text)


def describe_findings(desc):
    """Turn the DESCRIBE pass's frame table into hard errors.

    A frame whose description cannot name an object, or whose description does not
    match the words spoken at that instant, is a finding. This is mechanical: the
    model already committed to a description, and the finding falls out of it.
    """
    errors = []
    for f in desc.get("frames", []):
        t = f.get("at_seconds")
        if not f.get("object_identifiable", True):
            errors.append({
                "kind": "unidentifiable_object", "at_seconds": t,
                "description": f'described as "{f.get("description","")}" - '
                               f'{f.get("unidentifiable_reason") or "no object name from the pixels"}',
            })
        if not f.get("matches_beat", True):
            errors.append({
                "kind": "beat_mismatch", "at_seconds": t,
                "description": f'picture "{f.get("description","")}" vs words '
                               f'"{f.get("spoken_words","")}" - '
                               f'{f.get("mismatch_reason") or "the picture does not argue the sentence"}',
            })
    return errors


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate")
    ap.add_argument("video_id")
    ap.add_argument("--run", type=Path, default=None, help="the run this render belongs to (default: newest run)")
    ap.add_argument("--transcript", type=Path, default=None, help="the tight words json (default: <run>/cuts/<video_id>/transcript_tight.json)")
    ap.add_argument("--label", default=None)
    ap.add_argument("--describe", dest="describe", action="store_true", default=True,
                    help="describe every sampled frame before judging (DEFAULT since 2026-09-02)")
    ap.add_argument("--no-describe", dest="describe", action="store_false",
                    help="pre-2026-09-02 two-pass behaviour")
    ap.add_argument("--describe-frames", type=int, default=14)
    a = ap.parse_args()
    cand_path = Path(a.candidate)
    label = a.label or cand_path.stem

    from runs import newest_run
    run = (a.run or newest_run()).resolve()
    tpath = a.transcript or (run / "cuts" / a.video_id / "transcript_tight.json")
    if not tpath.exists() and a.video_id in TRANSCRIPTS:
        tpath = TRANSCRIPTS[a.video_id]   # hand use only: any run's cuts/<id>
    tr = json.loads(tpath.read_text())
    qc_dir = run / "review" / "qc"; qc_dir.mkdir(parents=True, exist_ok=True)
    words = " ".join(f"{w['text']}[{w['start']:.1f}]" for w in tr["words"] if w["type"] == "word")

    cand = upload_retry(cand_path)
    desc, desc_errors = None, []
    if a.describe:
        desc = judge(cand, DESCRIBE.format(n=a.describe_frames, transcript=words[:12000]),
                     schema=DESCRIBE_SCHEMA, max_tokens=12288)
        desc_errors = describe_findings(desc)
    vis = judge(cand, VISUAL)
    sem = judge(cand, SEMANTIC.format(transcript=words[:12000]))
    verdict = {
        "pass": vis["pass"] and sem["pass"] and not desc_errors,
        "visual": vis, "semantic": sem,
        "describe": ({"enabled": True, "frames": desc.get("frames", []),
                      "summary": desc.get("summary", ""), "errors": desc_errors}
                     if a.describe else {"enabled": False}),
    }
    (qc_dir / f"{label}.json").write_text(json.dumps(verdict, indent=1))
    try:
        client.files.delete(name=cand.name)
    except Exception:
        pass
    cost = round(USAGE["in"] * PRICE_IN + (USAGE["out"] + USAGE["thoughts"]) * PRICE_OUT, 6)
    print(json.dumps({"pass": verdict["pass"],
                      "describe_errors": desc_errors,
                      "visual_errors": vis["errors"], "semantic_errors": sem["errors"],
                      "described_frames": len(desc.get("frames", [])) if desc else 0,
                      "model": MODEL, "usage": USAGE, "cost_usd": cost}, indent=1))
    sys.exit(0 if verdict["pass"] else 1)
