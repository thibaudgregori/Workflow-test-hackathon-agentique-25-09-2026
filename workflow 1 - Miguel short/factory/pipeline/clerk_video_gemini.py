#!/usr/bin/env python3
"""clerk_video_gemini.py — GEMINI WATCHES THE WHOLE SHORT AND PRODUCES THE CANDIDATE LIST.

*Added 2026-09-02, after the still-frame clerk proved unstable and the moving-clip
verifier proved reliable. THE ROLES ARE FLIPPED.*

WHY THIS EXISTS
---------------
Two clerk runs on the same render (`codexvoice`) returned two different candidate
lists. The still-frame clerk missed 4 of the 6 defects Miguel confirmed by eye,
and raised several things the factory does ON PURPOSE (the Claude Code pixel
mascot, tiles occluded by the cutout silhouette, the whiteboard pencil sitting on
the type it is writing). Meanwhile the moving-clip verifier — the same Gemini
model, watching motion instead of a frame — agreed with Miguel 5 out of 5.

A still frame cannot see time. Every defect class in this factory's STANDARD is
defined over a WINDOW: ">= 1.5 s empty", ">= 2 s after the word", "held", "while
moving". Asking a still-frame reviewer to produce candidates for time-defined
laws is asking it to guess, and it guessed differently each run.

So: **Gemini watches the whole video and produces the candidates. The Opus clerk
adjudicates them.** The clerk stops guessing where to look and starts doing the
one thing it is better at — applying the law text to a NAMED WINDOW it can decode
frame by frame, and dismissing what the factory does on purpose.

WHAT THIS SCRIPT DOES
---------------------
One model call per render:

  * re-encodes the staged render to 720x1280 (audio KEPT — the spoken sentence is
    half of every semantic judgement) and uploads it via the Files API;
  * sends the TIGHT TRANSCRIPT as a timed word list, so the model never has to
    trust its own ASR (the 2026-07-12 lesson: a model that mishears its own audio
    then reports its guess as a caption defect);
  * sends the COMPACT DEFECT DEFINITIONS distilled from STANDARD.md, each one
    stated as a window test;
  * sends the KNOWN AND ACCEPTED list — the behaviours this factory ships on
    purpose, which a cold reviewer reliably mistakes for defects;
  * returns a candidate list: {t_start, t_end, on_screen, said, claim, klass,
    severity, motion_or_held}.

It does NOT adjudicate. Every row it returns is a CANDIDATE. The clerk decodes
t_start..t_end, applies the law text, and marks CONFIRMED / ACCEPTED-BEHAVIOUR /
REFUTED. See `pipeline/semantic_review.md` v3.

DETERMINISM
-----------
Gemini 3.5+ deprecates `temperature` / `top_p` / `top_k`; passing them is a
validation error on some models and a no-op on others, so this script does NOT
pass them by default (`--temperature` exists as an escape hatch and is only sent
when explicitly given). Stability comes from structure instead: a fixed frame
rate, a fixed schema, an explicit window per row, and a bounded thinking level.
Run `--passes 2` to measure the residual variance yourself; the union is written
with a `seen_in_passes` count per candidate so the clerk can weight them.

USAGE
-----
    clerk_video_gemini.py <render.mp4> <video_id> --fmt split|cutout|whiteboard \\
        [--out cands.json] [--fps 3] [--chunk 16] [--passes 1] [--thinking medium]

MODEL: gemini-3.5-flash-lite (Miguel, 2026-09-03; was gemini-3.8-flash). Video analysis is the approved Gemini lane (CLAUDE.md
rule 6). Override with GEMINI_CLERK_MODEL.
"""
import argparse
import concurrent.futures as cfutures
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path.home() / "Documents/Workspace/.env")
os.environ["GEMINI_API_KEY"] = os.environ.get(
    "GEMINI_API_KEY_GENIAL", os.environ.get("GEMINI_API_KEY", ""))
from google import genai  # noqa: E402
from google.genai import types  # noqa: E402

FACTORY = Path.home() / "Documents/Workspace/projects/personal/content/shorts-factory"
MODEL = os.environ.get("GEMINI_CLERK_MODEL", "gemini-3.5-flash-lite")

# gemini-3.5-flash-lite, per tools/gemini.md (2026-09-03): $0.30 / MTok in, $2.50 / MTok out.
# (3.8-flash was $0.75 / $3.75.)
# THINKING TOKENS BILL AS OUTPUT — keep the thinking level bounded.
PRICE_IN = float(os.environ.get("GEMINI_CLERK_PRICE_IN", "0.30")) / 1e6
PRICE_OUT = float(os.environ.get("GEMINI_CLERK_PRICE_OUT", "2.50")) / 1e6

MAX_OUT = int(os.environ.get("GEMINI_CLERK_MAX_OUT", "32768"))
DEFAULT_FPS = float(os.environ.get("GEMINI_CLERK_FPS", "3"))
# THINKING IS THE RECALL DIAL, NOT A COST DIAL. Thinking bills as OUTPUT at
# $3.75/MTok and IS most of the bill — but measured 2026-09-02 on
# `codexvoice_split`: at "medium" the five windows returned 3 candidates for
# ~$0.21; at "low" the SAME five windows returned **zero** candidates for ~$0.10.
# The model stops looking before it stops writing. Do not lower this to save
# money; lower --fps or drop --no-whole-pass instead.
DEFAULT_THINKING = os.environ.get("GEMINI_CLERK_THINKING", "medium")
DEFAULT_CHUNK = float(os.environ.get("GEMINI_CLERK_CHUNK", "20"))
DEFAULT_OVERLAP = float(os.environ.get("GEMINI_CLERK_OVERLAP", "3"))
# THE WINDOWS OF ONE RENDER RUN CONCURRENTLY (2026-09-02).  A window is an
# independent upload + call whose result is unioned afterwards, so nothing
# about the procedure requires them to be serial — only the `for` loop did.
# Default 4 = the standard window count (one whole-video pass + three chunks),
# so a render costs ONE call's latency instead of four.
DEFAULT_JOBS = int(os.environ.get("GEMINI_CLERK_JOBS", "4"))

CAND_SCHEMA = {
    "type": "object",
    "properties": {
        "video_summary": {"type": "string"},
        # DESCRIBE BEFORE JUDGE (STANDARD.md, VISUAL QUALITY CHECKS §5). A model
        # asked only for violations answers "none" about frames it never parsed.
        # Writing the beat log first forces it to actually look at every second.
        "beat_log": {"type": "array", "items": {"type": "object", "properties": {
            "t_start": {"type": "number"},
            "t_end": {"type": "number"},
            "on_screen": {"type": "string"},
            "said": {"type": "string"},
            "marks_visible": {"type": "string"},
            "labels_visible": {"type": "string"},
            # THE SWEEP. These four are inspection questions, not description, and
            # they are REQUIRED. Measured 2026-09-02: with description alone the
            # watcher returned 1 candidate on a render with 5 known defects; the
            # defects were all visible in its own beat log. A model that is not
            # made to look for a class does not find that class.
            "touching_or_clipped": {"type": "string"},
            "empty_regions": {"type": "string"},
            "label_placement": {"type": "string"},
            "picture_vs_sentence": {"type": "string"},
        }, "required": ["t_start", "t_end", "on_screen", "said", "marks_visible",
                        "labels_visible", "touching_or_clipped", "empty_regions",
                        "label_placement", "picture_vs_sentence"]}},
        "candidates": {"type": "array", "items": {"type": "object", "properties": {
            "t_start": {"type": "number"},
            "t_end": {"type": "number"},
            "on_screen": {"type": "string"},
            "said": {"type": "string"},
            "claim": {"type": "string"},
            "klass": {"type": "string", "enum": [
                "empty_zone", "named_tool_no_mark", "cramp_overlap_clipping",
                "side_label", "uneven_baselines", "contradictory_labels",
                "lingering_mark", "ring_or_box_on_image_text",
                "missing_source_post", "picture_contradicts_sentence",
                "unaligned_arrows", "other"]},
            "severity": {"type": "string", "enum": ["blocking", "minor"]},
            "motion_or_held": {"type": "string", "enum": ["motion", "held"]},
        }, "required": ["t_start", "t_end", "on_screen", "said", "claim",
                        "klass", "severity", "motion_or_held"]}},
    },
    "required": ["video_summary", "beat_log", "candidates"],
}

DEFECT_DEFS = """DEFECT DEFINITIONS. These are the factory's own laws, distilled. Every one of them
is defined over a WINDOW OF TIME, which is why you are watching and not sampling.
Report a candidate ONLY if it matches one of these classes.

  empty_zone
      A visual zone that carries NOTHING for >= 1.5 s of settled screen time.
      Stillness is not emptiness: a picture that is finished and simply holds is
      correct. A zone that is briefly bare BETWEEN two beats, while one element
      leaves and the next arrives, is a transition and is NOT this class.

  named_tool_no_mark
      A tool, product or company is NAMED in the speech and its logo / wordmark is
      still absent >= 2 s AFTER the word ends. A mark that lands within 2 s of the
      word is arriving, not missing.

  cramp_overlap_clipping
      Two objects jammed together with no air; one object's outline cutting
      through another; an element sliced by a card, phone or frame border; a line,
      arrow or stroke drawn straight through printed type. TWO SUB-CASES, and you
      must say which in motion_or_held:
        held   — the objects have stopped moving and the collision is still there;
        motion — the collision happens WHILE the element travels. Motion never
                 excuses a collision. A logo cut in half by a border as it flies
                 past IS this class even if it lasts a third of a second.

  side_label
      A name sitting to the LEFT or the RIGHT of the object it names. Names go
      ABOVE or BELOW the thing they name, never beside it.

  uneven_baselines
      Two or more labels in one row settling on visibly different vertical
      baselines, or with visibly different margins, once everything has landed.

  contradictory_labels
      One object carrying two labels that say different things at the same time,
      held together for >= 1.5 s.

  lingering_mark
      A logo, glyph or card still on screen long after the beat that put it there
      stopped being the subject, while the speech has moved on to something else.

  ring_or_box_on_image_text
      A ring / ellipse / circle drawn around ANYTHING (always wrong), or a BOX
      drawn around text that lives on an image — a post, a screenshot, a document,
      a UI capture. Those words take a translucent marker highlight instead.
      A box around a DRAWN object or a piece of scene type is CORRECT and is not
      this class.

  missing_source_post
      He says "like this guy" / "someone on X" / "this post" / "I saw a post" and
      NO post or tweet card appears within ~1 s of the cue.

  picture_contradicts_sentence
      The picture argues something DIFFERENT from the sentence being spoken —
      arrows pointing the opposite way, the scenery drawn instead of the
      sentence's actual subject, two compared quantities on different axes, a
      label naming the wrong object. A picture that is merely COMPATIBLE with the
      sentence and adds nothing is not this class; a picture that says the
      opposite is.

  unaligned_arrows
      Two or more arrows into ONE target landing at visibly different spots or
      heights.
"""

KNOWN_ACCEPTED = """KNOWN AND ACCEPTED — the factory does all of this ON PURPOSE. Never report any of
it as a candidate. Every item below was raised by a previous reviewer and ruled a
FALSE POSITIVE by the owner.

  1. ENTRY AND EXIT ANIMATIONS RUN 1-2 SECONDS. An element arriving, filling,
     fading in, sliding in or being drawn on is not missing, empty or late. Judge
     every element on where it LANDS, never on where it is mid-flight.
  2. THE CLAUDE CODE PIXEL MASCOT IS THE REAL LOGO. The small orange/salmon
     pixel-art creature IS the mark for Claude Code. It satisfies
     named_tool_no_mark on its own. It also appears on the speaker's cap; that is
     normal.
  3. CUTOUT FORMAT — THE SILHOUETTE OCCLUDES THE WORLD. The speaker is a
     full-bleed cut-out standing IN FRONT of the scene. Background tiles, logos
     and cards passing BEHIND his body and being hidden by it is the format's
     depth cue, not a collision, and not clipping.
  4. CUTOUT FORMAT — TILES FADE OUT AT THE FRAME EDGES. The parallax logo lanes
     are edge-faded on purpose so the wall reads as continuing past the frame. A
     tile partly outside the canvas at the left or right edge is the design.
     (A tile sliced hard with no fade, mid-frame, is still reportable.)
  5. WHITEBOARD FORMAT — THE PENCIL SITS ON THE TYPE IT IS WRITING. The marker
     tip is AT the ink at the moment the ink is drawn, for every stroke including
     letters. The pencil body crossing the glyphs it is currently drawing or has
     just drawn is the mechanic of the format, not a line through printed type.
     (A pencil crossing type from a DIFFERENT, already-finished block, while
     drawing something else entirely, is still reportable.)
  6. WHITEBOARD FORMAT — INK ACCUMULATES AND HOLDS. A whiteboard drawing stays on
     the board after its beat; that is the format ("one drawing, gaining ink").
     Do not report held board ink as a lingering mark unless the board has moved
     to a new chapter and the old chapter's ink is still standing on top of it.
  7. THE CAPTION PILL. One caption pill on the seam, one size, changing with the
     speech, is the house caption. It is never a defect.
  8. THE OUTRO HANDLE CARD. The short ends on a handle card
     (@migueltorrezai on YouTube, @migueltorrez.ai on TikTok and Reels). A quiet
     final card with the handle and a subtitle is complete by design.
  9. THE SPLIT SEAM AND THE CREAM PALETTE. A cream visual zone above a talking
     head with a hard seam between them is the classic split format. The cream
     background behind objects is not an empty zone; only a zone with no content
     is.
 10. THE DIE-CUT CREAM RIM. A cream keyline traced around the speaker's
     silhouette (cutout) and salmon/cream outlines on drawn objects are the house
     style, not misregistration or a double stroke.
 11. A CROSS-DISSOLVE SUPERIMPOSES TWO PICTURES. When one scene hands over to
     the next, both are on screen at partial opacity for a few tenths of a second
     and their shapes overlap. That is a dissolve, not a collision: a collision
     needs two objects that are BOTH fully present and BOTH belong to the same
     picture. If the two overlapping things are visibly at reduced opacity and one
     of them is leaving, it is a transition. (Added 2026-09-02 after the watcher
     raised a 0.45 s dissolve on `codexnondev` as a border cutting through four
     tool cards.)
 12. A COMPANY NAMED AS A POSSESSIVE DOES NOT NEED ITS OWN MARK. "Codex, OpenAI's
     coding assistant" names ONE tool — Codex — and qualifies it. If the Codex
     mark is on screen, LAW 2 is satisfied; OpenAI does not need a second logo.
     The same goes for "Claude Code, Anthropic's agent". Only a tool the sentence
     is actually introducing needs a mark. (Added 2026-09-02.)
"""

PROMPT = """You are the CANDIDATE FINDER of a vertical-shorts quality chain. You are given ONE
finished 9:16 short — the whole thing, with its audio — plus the exact transcript
of what is said, with word timings.

WATCH THE WHOLE VIDEO. Your job is to return a list of CANDIDATE DEFECTS: moments
where the picture is wrong, in one of the named classes below. You are NOT the
judge. A human clerk will decode every window you name and rule on it. Your job is
to MISS NOTHING and to INVENT NOTHING.

WHY YOU AND NOT A STILL-FRAME REVIEWER. Every law in this factory is defined over
a window of time — "empty for >= 1.5 s", "still absent 2 s after the word",
"held", "while moving". A reviewer looking at one frame cannot evaluate any of
them and has to guess; two such reviewers guessed differently on the same render.
You can see time. Use it: for every candidate you return, give the window over
which the wrongness is ACTUALLY TRUE, not the instant you noticed it.

{defect_defs}

{known_accepted}

HOW TO WORK — TWO STAGES, IN THIS ORDER. Do not skip stage one.

STAGE ONE — THE BEAT LOG, AND THE SWEEP INSIDE IT. Walk the video from 0 s to the
end and write one row per visual beat. A beat is a stretch where the picture is
doing one thing — typically **2 to 4 seconds**, so a 45 s short is **12 to 20
rows**, with NO GAPS: the rows must cover the whole duration end to end. Fewer
than ten rows for a 40 s short means you skimmed and the log is not usable.

Every row has ten fields. The first six are DESCRIPTION:

  on_screen        every object you can see, named from its SHAPE, with where it
                   sits in the frame (left / right / centre / top / bottom).
  said             the words from the transcript across that stretch. From the
                   transcript given to you, never from your own hearing.
  marks_visible    every brand logo or wordmark you can identify, or "none".
  labels_visible   every word of printed type on the picture, VERBATIM, or "none".

The next four are THE SWEEP. They are inspection questions, not description, and
you answer every one on every row. This is the part that makes you look:

  touching_or_clipped
      Go object by object across this beat. Name EVERY pair that touches,
      overlaps, has one outline crossing the other, is jammed together with no
      visible air, or is sliced by a card / phone / panel / frame border —
      INCLUDING a collision that only happens for a moment while one of them is
      travelling, and INCLUDING a line, arrow, stroke or pen crossing printed
      type. Say which pair and roughly when. If genuinely nothing touches, write
      "none" — but check the moving elements before you write it, because a
      travelling object that grazes a border for half a second is the single most
      common defect in this factory and it is invisible if you only look at the
      beat's settled frame.
  empty_regions
      Is any region of the frame carrying NOTHING across this beat — a blank
      screen inside a drawn monitor, an empty speech bubble, a bare half of the
      visual zone, a card with no content? Name the region and say for how long.
      Otherwise "none". Background colour is not emptiness; a container with no
      content is.
  label_placement
      For every printed label in this beat: is it ABOVE, BELOW or BESIDE the thing
      it names? Do labels sitting in one row share a baseline and a margin, or do
      they sit at visibly different heights? Does any object carry two labels at
      once? Answer concretely, naming the labels. "none" only if there is no
      printed type at all.
  picture_vs_sentence
      In one sentence: does the picture argue what `said` says, say nothing, or say
      something DIFFERENT? Name the mismatch if there is one.

Describe and inspect. Do not accuse yet.

STAGE TWO — THE CANDIDATES. Now read back your OWN beat log — not the video, your
log — and turn every non-"none" answer in the four sweep fields into a decision:
is that thing a defect under the class definitions above, or is it on the KNOWN
AND ACCEPTED list? Also check, across rows: every tool NAMED in `said` has its
mark in `marks_visible` within 2 s of the word; nothing in `marks_visible` is
still there long after the speech left it behind.

Write one candidate row per real problem. **If your beat log recorded a collision,
an empty container, a beside-label, an uneven baseline row or a double label and
you do NOT raise it as a candidate, you must have a reason from the KNOWN AND
ACCEPTED list.** Silently dropping your own observation is the failure mode this
whole two-stage structure exists to prevent.

HOW TO REPORT

  * ONE ROW PER DISTINCT PROBLEM. If the same collision recurs three times in one
    beat, that is one row with a window covering it, not three rows.
  * t_start / t_end are ABSOLUTE SECONDS IN THE FULL SHORT — add the clip offset
    given above to whatever your own playhead says — and they bound the window
    over which the wrongness is TRUE — not the whole beat, and not one instant.
    For a motion defect, t_start..t_end is the span of the collision even if it is
    only 0.3 s long. For a held defect, it is the settled span.
  * on_screen: what is literally on the screen across that window, described from
    the pixels, naming shapes not intentions. If a shape is ambiguous, say what it
    looks like, not what it probably is.
  * said: the words spoken across that window, from the transcript given to you.
    Never from your own hearing.
  * claim: ONE blunt sentence stating what is wrong. No hedging, no rubric talk,
    no suggested fix.
  * klass: exactly one of the class names above.
  * severity: "blocking" if a first-time viewer on a phone would notice it and be
    confused or put off; "minor" if it is real but small.
  * motion_or_held: "motion" if the wrongness only exists while something is
    travelling; "held" if it is true of a settled picture.

RULES

  * Report ONLY what you actually saw. A candidate you are not sure you saw is a
    candidate you do not return. The clerk cannot un-see a fabricated window; it
    costs a decode and it poisons the list.
  * Do not grade the video, do not score it, do not praise it, do not suggest
    improvements. No taste notes. No "could be tighter". Defects only.
  * Do not report the ABSENCE of something you would have liked to see. Only the
    presence of something wrong.
  * Do not report audio, music, voice, pacing, script or subject-matter issues.
    This is a picture gate.
  * If the video has no defects, return an empty candidates array. That is a valid
    and expected answer. Do not manufacture a row to look thorough.
  * video_summary: two sentences, cold, describing what the video shows and what
    it argues — written from the pixels, as a first-time viewer.

CONTEXT FOR THIS RENDER

  video id: {vid}
  format:   {fmt} — {fmt_note}
  full duration of the short: {dur:.2f} s

{chunk_note}

TRANSCRIPT (word: start-end, seconds):
{transcript}
"""

FMT_NOTES = {
    "split": ("classic split — a cream visual zone on top, the speaker's face below, "
              "a hard seam between them, the caption pill on the seam."),
    "cutout": ("cutout — the speaker is a background-removed full-bleed silhouette "
               "standing IN FRONT of the scene, with a cream die-cut rim; logo tiles "
               "parallax behind him and are occluded by his body ON PURPOSE."),
    "whiteboard": ("whiteboard — ONE board that gains ink; every shape is drawn on by a "
                   "marker at the moment its words are spoken, and the pencil is AT the "
                   "ink it draws. Ink accumulates and holds; that is the format."),
}


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"{cmd[0]} failed: {p.stderr[-800:]}")
    return p.stdout


def duration_of(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                      "-of", "default=nw=1:nk=1", str(path)]).strip())


def resolve_transcript(render, video_id, explicit=None, factory=None):
    """The tight transcript of THIS render's run, never another run's.

    `explicit` (--transcript) wins and must exist.  Otherwise the run is read
    off the render's own path (.../shorts_runNN/...) and the transcript must be
    at <run>/cuts/<video_id>/transcript_tight.json.  There is no cross-run
    fallback: the old `find_transcript` globbed every shorts_run* and took the
    lexically last one, so a run-16 MiniMax render was watched against run 9's
    transcript (parent audit, 2026-09-06).
    """
    from pathlib import Path as _P
    factory = _P(factory) if factory else FACTORY
    if explicit:
        p = _P(explicit)
        if not p.is_file():
            raise SystemExit(f"--transcript does not exist: {p}")
        return p
    render = _P(render).resolve()
    run = next((q for q in render.parents if q.name.startswith("shorts_run")), None)
    if run is None:
        raise SystemExit(f"cannot infer the run from the render path {render}; pass --transcript")
    p = run / "cuts" / video_id / "transcript_tight.json"
    if not p.is_file():
        raise SystemExit(f"no tight transcript for {video_id} in {run.name}: {p} (no cross-run fallback)")
    return p


def find_transcript(video_id):  # retired: cross-run lexical pick; kept only as a name
    raise SystemExit("find_transcript is retired: use resolve_transcript(render, video_id, --transcript)")


def transcript_lines(tr, max_chars=14000):
    """Word list with timings, chunked into readable lines. The model must read the
    words here, never its own ASR of the audio track."""
    if not tr:
        return "(no transcript available)"
    words = [w for w in tr.get("words", [])
             if w.get("type") == "word" and w.get("start") is not None]
    out, line, t0 = [], [], None
    for w in words:
        if t0 is None:
            t0 = w["start"]
        line.append(w["text"])
        if len(line) >= 10:
            out.append(f"  [{t0:6.2f}-{w.get('end', w['start']):6.2f}] " + " ".join(line))
            line, t0 = [], None
    if line:
        out.append(f"  [{t0:6.2f}-{words[-1].get('end', t0):6.2f}] " + " ".join(line))
    text = "\n".join(out)
    return text[:max_chars]


def encode_720(src, dest, start=None, dur=None):
    """720x1280, audio kept. The re-encode exists so a 2160x3840 YouTube master
    does not go up the wire at ten times the tokens it is worth. With start/dur it
    cuts one chunk (accurate seek: -ss before -i, re-encoded, so the timestamps in
    the chunk start at zero and the caller adds the offset back)."""
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y"]
    if start is not None:
        cmd += ["-ss", f"{start:.3f}"]
    cmd += ["-i", str(src)]
    if dur is not None:
        cmd += ["-t", f"{dur:.3f}"]
    cmd += ["-vf", "scale=720:-2", "-c:v", "libx264", "-preset", "veryfast",
            "-crf", "28", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "64k",
            "-movflags", "+faststart", str(dest)]
    run(cmd)
    return dest


def chunk_windows(dur, chunk, overlap):
    """Contiguous windows with a shared overlap, covering the whole duration.

    WHY CHUNK AT ALL. Measured 2026-09-02 on `codexvoice_split` (45.8 s): asked
    about the whole render in one call, the watcher wrote a beat log that
    RECORDED the collisions and then raised 3 candidates against 5 known defects.
    Attention over ~140 frames is the bottleneck, not resolution and not frame
    rate. Cut into ~16 s windows the same model sees ~48 frames per call and its
    own sweep fields stop going quiet. One prompt is re-sent per chunk; that is
    ~3K tokens, which is cheaper than the recall it buys."""
    if not chunk or chunk <= 0 or dur <= chunk:
        return [(0.0, dur)]
    out, t = [], 0.0
    while t < dur - 0.05:
        end = min(dur, t + chunk)
        out.append((t, end))
        if end >= dur:
            break
        t = end - overlap
    return out


def upload_retry(client, path, attempts=3):
    for i in range(attempts):
        try:
            f = client.files.upload(file=str(path))
            while f.state and f.state.name == "PROCESSING":
                time.sleep(2.0)
                f = client.files.get(name=f.name)
            if f.state and f.state.name == "ACTIVE":
                return f
        except Exception as e:  # noqa: BLE001
            print(f"upload retry {i+1} ({path.name}): {e}", file=sys.stderr)
        time.sleep(2 * (i + 1))
    raise RuntimeError(f"upload failed: {path}")


def generate_retry(client, prompt, video_part, cfg, attempts=3):
    """One model call, with a back-off on the transient failures concurrency buys.

    Running the windows in parallel means several calls can land on a 429 or a
    503 at the same instant; a serial loop hid that by construction.  The retry
    is bounded and it re-uses the SAME uploaded file, so a retry costs one call's
    input tokens, never a re-encode or a re-upload.
    """
    last = None
    for i in range(attempts):
        try:
            return client.models.generate_content(
                model=MODEL,
                contents=[types.Content(parts=[types.Part(text=prompt), video_part])],
                config=cfg)
        except Exception as e:                                      # noqa: BLE001
            last = e
            msg = str(e)
            transient = any(k in msg for k in ("429", "503", "500", "RESOURCE_EXHAUSTED",
                                               "UNAVAILABLE", "deadline", "timeout"))
            print(f"generate retry {i+1}/{attempts}"
                  f"{' (transient)' if transient else ''}: {msg[:180]}", file=sys.stderr)
            if not transient and i == attempts - 1:
                break
            time.sleep(4 * (i + 1))
    raise RuntimeError(f"generate_content failed after {attempts} attempts: {last}")


def salvage(text):
    """Recover whole candidate objects from a response the output cap cut short."""
    out, depth, start = [], 0, None
    body = text[text.find("["):] if "[" in text else text
    for i, ch in enumerate(body):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                try:
                    out.append(json.loads(body[start:i + 1]))
                except json.JSONDecodeError:
                    pass
                start = None
    return {"video_summary": "(salvaged from a truncated response)",
            "candidates": [o for o in out if "claim" in o and "t_start" in o]}


def merge_passes(pass_lists):
    """Union across passes; two rows are the same candidate when their classes match
    and their windows overlap. Keeps the widest window and counts the passes."""
    merged = []
    for cands in pass_lists:
        for c in cands:
            hit = None
            for m in merged:
                if m["klass"] != c.get("klass"):
                    continue
                if (c["t_start"] <= m["t_end"] + 0.6
                        and c["t_end"] >= m["t_start"] - 0.6):
                    hit = m
                    break
            if hit:
                hit["t_start"] = min(hit["t_start"], c["t_start"])
                hit["t_end"] = max(hit["t_end"], c["t_end"])
                hit["seen_in_passes"] += 1
                hit.setdefault("alt_claims", []).append(c.get("claim", ""))
            else:
                c = dict(c)
                c["seen_in_passes"] = 1
                merged.append(c)
    merged.sort(key=lambda c: c["t_start"])
    for i, c in enumerate(merged, 1):
        c["id"] = f"C{i}"
    return merged


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("video_id")
    ap.add_argument("--fmt", default=None,
                    help="split|cutout|whiteboard (inferred from the filename if omitted)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--fps", type=float, default=DEFAULT_FPS,
                    help="frames per second Gemini samples (default 3; at 1 fps a "
                         "0.6 s motion collision falls between samples)")
    ap.add_argument("--no-whole-pass", dest="whole_pass", action="store_false",
                    help="skip the extra whole-video call (cheaper, lower recall)")
    ap.add_argument("--chunk", type=float, default=DEFAULT_CHUNK,
                    help="seconds per window; 0 sends the whole render in one call. "
                         "Default 20 — measured to roughly double recall over a "
                         "single whole-video call (see chunk_windows).")
    ap.add_argument("--chunk-overlap", type=float, default=DEFAULT_OVERLAP,
                    help="seconds of overlap between windows so a defect straddling "
                         "a cut is seen whole by at least one call")
    ap.add_argument("--passes", type=int, default=1,
                    help="run the same call N times and union the candidates")
    ap.add_argument("--transcript", default=None,
                    help="the tight transcript of THIS render's run (explicit; must exist). "
                         "Without it the run is read off the render path; no cross-run fallback.")
    ap.add_argument("--thinking", default=DEFAULT_THINKING,
                    help="minimal|low|medium|high — thinking bills as OUTPUT")
    ap.add_argument("--temperature", type=float, default=None,
                    help="only sent when given; Gemini 3.5+ deprecates it")
    ap.add_argument("--jobs", type=int, default=DEFAULT_JOBS,
                    help="how many (pass, window) calls run CONCURRENTLY for this "
                         f"render (default {DEFAULT_JOBS}). Windows are independent "
                         "uploads whose candidate lists are unioned afterwards, so "
                         "this changes wall clock only, never cost or output. Use "
                         "--jobs 1 to reproduce the old serial behaviour.")
    ap.add_argument("--keep-encode", action="store_true")
    a = ap.parse_args()

    src = Path(a.video)
    fmt = a.fmt or next((f for f in ("split", "cutout", "whiteboard")
                         if f in src.stem), "split")
    label = f"{a.video_id}_{fmt}"

    # `src`, not `a.render`: the positional argument is named `video`, so the
    # 2026-09-06 run-scoping fix crashed with AttributeError on every call
    # (run-16 minimaxh3_split, 2026-09-06).  resolve_transcript reads the run
    # off THIS render's own path, which is exactly `src`.
    tr_path = resolve_transcript(src, a.video_id, a.transcript)
    tr = json.loads(tr_path.read_text()) if tr_path else None
    dur = duration_of(src)

    work = Path(tempfile.mkdtemp(prefix=f"clerkvid_{label}_"))
    client = genai.Client()
    windows = chunk_windows(dur, a.chunk, a.chunk_overlap)
    # TWO VIEWS OF THE SAME RENDER, UNIONED. Measured 2026-09-02 on
    # `codexvoice_split` against its 5 known defects: the WHOLE-VIDEO call found
    # the 38.8 s motion clip and missed the 21-23 s uneven baselines; the CHUNKED
    # calls found the baselines and missed the motion clip. Neither view dominates
    # — the wide view sees an object's whole trajectory, the narrow view has the
    # attention to read type. The union found both. This is the same aggregation
    # the 2026-07-26 Gemini learning prescribes for high-variance vision judging:
    # run more than one view and combine, because a single call is a sample.
    if a.whole_pass and len(windows) > 1:
        windows = [(0.0, dur)] + windows

    # MEDIA RESOLUTION MATTERS MORE THAN ANYTHING ELSE HERE. At the default LOW,
    # a 46 s short goes up as ~10K tokens and the model cannot see a cup touching a
    # phone border; recall measured 1/5 on the calibration video. At HIGH the same
    # render is ~3x the tokens (still ~2 c) and the collisions become visible.
    cfg = {"response_mime_type": "application/json",
           "response_schema": CAND_SCHEMA,
           "max_output_tokens": MAX_OUT,
           "media_resolution": types.MediaResolution.MEDIA_RESOLUTION_HIGH,
           "thinking_config": {"thinking_level": a.thinking}}
    if a.temperature is not None:
        cfg["temperature"] = a.temperature

    calls, summaries, beat_log = [], [], []
    uploaded = []
    pass_bins: dict[int, list] = {p: [] for p in range(a.passes)}
    _lock = threading.Lock()
    t_wall = time.time()

    # =====================================================================
    # ONE UNIT OF WORK = ONE (PASS, WINDOW) CALL, AND THEY DO NOT DEPEND ON
    # EACH OTHER.  Run them CONCURRENTLY.
    # ---------------------------------------------------------------------
    # WHY THIS IS NOT A MICRO-OPTIMISATION.  Every unit is
    # ffmpeg-encode -> upload -> wait for Gemini, and the last of those three is
    # 30-60 s of pure network latency during which this process did nothing at
    # all.  Run serially, a four-window render is ~236 s and a three-render video
    # is ~11 min; a five-render repair pass was measured at **50+ minutes of wall
    # clock for ~17 minutes of billed work**.  The calls are independent by
    # construction — each window is its own upload, its own prompt and its own
    # response, and the union happens afterwards in `merge_passes` — so the only
    # thing serialising them was the `for` loop.
    #
    # THE COST IS IDENTICAL.  Concurrency changes when the tokens are spent, not
    # how many: the same windows, the same media resolution, the same model.
    # =====================================================================
    def one_call(p: int, wi: int, w0: float, w1: float) -> dict:
        note = (f"  You are watching THE WHOLE SHORT (0.00-{dur:.2f} s). "
                f"Your playhead IS absolute video time."
                if len(windows) == 1 else
                f"  YOU ARE WATCHING ONE WINDOW OF THIS SHORT, NOT THE WHOLE THING.\n"
                f"  This clip is window {wi} of {len(windows)} and covers ABSOLUTE VIDEO\n"
                f"  TIME {w0:.2f}-{w1:.2f} s. Your own playhead starts at 0.00 for this\n"
                f"  clip, so ADD {w0:.2f} s TO EVERY TIMESTAMP YOU REPORT — in the beat\n"
                f"  log and in the candidates. Cover this window and only this window;\n"
                f"  an element already on screen at the first frame arrived before the\n"
                f"  window began, so do not report it as arriving now.")
        prompt = PROMPT.format(
            defect_defs=DEFECT_DEFS, known_accepted=KNOWN_ACCEPTED,
            vid=a.video_id, fmt=fmt,
            fmt_note=FMT_NOTES.get(fmt, "unknown format"),
            dur=dur, chunk_note=note, transcript=transcript_lines(tr))

        # each unit owns its own encode path, so two threads never write one file
        enc = encode_720(src, work / f"{label}_p{p+1}_w{wi}.mp4", w0, w1 - w0)
        up = upload_retry(client, enc)
        with _lock:
            uploaded.append(up.name)
        video_part = types.Part(
            file_data=types.FileData(file_uri=up.uri, mime_type="video/mp4"),
            video_metadata=types.VideoMetadata(fps=a.fps))

        resp = generate_retry(client, prompt, video_part, cfg)
        um = resp.usage_metadata
        tin = getattr(um, "prompt_token_count", 0) or 0
        tout = ((getattr(um, "candidates_token_count", 0) or 0)
                + (getattr(um, "thoughts_token_count", 0) or 0))
        cost = tin * PRICE_IN + tout * PRICE_OUT
        call = {"pass": p + 1, "window": [round(w0, 2), round(w1, 2)],
                "model": MODEL, "fps": a.fps, "thinking": a.thinking,
                "input_tokens": tin, "output_tokens": tout,
                "thinking_tokens": getattr(um, "thoughts_token_count", 0) or 0,
                "cost_usd": round(cost, 6)}
        try:
            data = json.loads(resp.text or "{}")
        except json.JSONDecodeError:
            data = salvage(resp.text or "")
            print(f"  ! truncated response, salvaged "
                  f"{len(data.get('candidates', []))}", file=sys.stderr)
        cands_w = data.get("candidates", [])
        for c in cands_w:
            c["window"] = [round(w0, 2), round(w1, 2)]
        beats = data.get("beat_log", [])
        for b in beats:
            b["from_window"] = [round(w0, 2), round(w1, 2)]
        print(f"[pass {p+1} win {wi}/{len(windows)} {w0:.1f}-{w1:.1f}s] "
              f"{len(beats)} beats / {len(cands_w)} candidates "
              f" in={tin} out={tout} ${cost:.4f}", file=sys.stderr)
        return {"p": p, "wi": wi, "call": call, "cands": cands_w,
                "beats": beats, "summary": data.get("video_summary", "")}

    units = [(p, wi, w0, w1)
             for p in range(a.passes)
             for wi, (w0, w1) in enumerate(windows, 1)]
    jobs = max(1, min(a.jobs, len(units)))
    try:
        with cfutures.ThreadPoolExecutor(max_workers=jobs) as pool:
            results = list(pool.map(lambda u: one_call(*u), units))
        # DETERMINISTIC ORDER, WHATEVER ORDER THEY FINISHED IN.  The report is
        # an artefact a clerk re-derives from; it may not depend on which
        # network call came back first.
        results.sort(key=lambda r: (r["p"], r["wi"]))
        for r in results:
            calls.append(r["call"])
            pass_bins[r["p"]] += r["cands"]
            if r["p"] == 0:
                beat_log += r["beats"]
                summaries.append(r["summary"])
        pass_lists = [pass_bins[p] for p in range(a.passes)]
    finally:
        for name in uploaded:
            try:
                client.files.delete(name=name)
            except Exception:  # noqa: BLE001
                pass
        if not a.keep_encode:
            shutil.rmtree(work, ignore_errors=True)

    cands = merge_passes(pass_lists)
    beat_log.sort(key=lambda b: b.get("t_start", 0))
    total_cost = sum(c["cost_usd"] for c in calls)
    result = {
        "video": str(src), "video_id": a.video_id, "fmt": fmt, "model": MODEL,
        "duration_s": round(dur, 3), "fps_sampled": a.fps,
        "windows": [[round(w0, 2), round(w1, 2)] for w0, w1 in windows],
        "whole_pass": a.whole_pass,
        "thinking": a.thinking, "media_resolution": "HIGH",
        "jobs": jobs,
        "transcript": str(tr_path) if tr_path else None,
        "video_summary": " ".join(summaries[:1]),
        "beat_log": beat_log,
        "all_summaries": summaries,
        "candidates": cands,
        "counts": {"candidates": len(cands),
                   "blocking": sum(1 for c in cands if c.get("severity") == "blocking"),
                   "motion": sum(1 for c in cands if c.get("motion_or_held") == "motion")},
        "calls": calls,
        "cost_usd": round(total_cost, 6),
        "wall_clock_s": round(time.time() - t_wall, 1),
    }
    from runs import newest_run  # noqa: E402  (pipeline/ is this file's own dir)
    out = Path(a.out) if a.out else (newest_run() / f"review/cands_{label}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=1))

    # ── THE COST LEDGER (2026-09-04) ────────────────────────────────────────
    # The watcher books ITSELF, out of the token arithmetic it just did, so the
    # same call is counted once whether `render_and_check` made it, a clerk
    # made it on a render nobody watched, or a hand-run made it.  The run comes
    # from `--out` (which lives in `<run>/review/`) or $SHORTS_RUN; the stage
    # comes from the file it was asked to write, so a clerk re-watch and a
    # post-render watch never land on the same line.  The ref carries the
    # WATCHED FILE's mtime, which is what makes a fix round's watch its own row.
    try:
        sys.path.insert(0, str(FACTORY / "pipeline"))
        import costs as COSTS                                    # noqa: E402
        _stage = ("clerk_watch" if out.name.startswith("clerk_")
                  else "draft" if "draft" in out.name else "watch")
        _run = COSTS.resolve_run(os.environ.get("SHORTS_RUN") or None, out)
        COSTS.safe_record(
            _run, "gemini", _stage, float(result["cost_usd"]),
            video=a.video_id, fmt=fmt or None,
            units=(f"{sum(c.get('input_tokens') or 0 for c in calls):,} in / "
                   f"{sum((c.get('output_tokens') or 0) + (c.get('thinking_tokens') or 0) for c in calls):,}"
                   f" out tokens over {len(calls)} calls"),
            note=f"{'clerk re-watch' if _stage == 'clerk_watch' else 'video watcher'}"
                 f", {MODEL}, {result['counts']['candidates']} candidates",
            ref=COSTS.call_ref(_run, out, int(src.stat().st_mtime_ns)))
    except Exception as exc:                                     # noqa: BLE001
        print(f"[costs] watcher not recorded ({type(exc).__name__}: {exc})",
              file=sys.stderr)
    print(json.dumps({"out": str(out), "counts": result["counts"],
                      "cost_usd": result["cost_usd"],
                      "wall_clock_s": result["wall_clock_s"]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
