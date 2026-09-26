#!/usr/bin/env python3
"""verify_flags_gemini.py — VERIFY A CLERK FLAG ON THE MOVING CLIP.

*Added 2026-09-02, after Miguel read the 21 clerk flags of daily batch 2 and
ruled MOST of them false positives.*

WHY THIS EXISTS
---------------
The Viewer Test clerk samples a STILL FRAME shortly after each visual boundary.
A still frame cannot tell a TRANSITION from a HELD STATE. Entry animations in
this factory run 1-2 s, so a frame grabbed ~0.3 s after a boundary is taken
*inside* the animation, and the clerk faithfully reports what it sees:

    "the bubble is empty"        -> it is 0.3 s into a 1.2 s fill
    "no Opus mark on screen"     -> the chip is 40 % through its entrance
    "the label lands late"       -> the label is mid-fade at the sampled frame

None of those is a defect; all three were written as NO-SENSE rows. Miguel's
ruling: "a still frame cannot judge a transition."

So every candidate flag now goes through THIS script before it may be written
as a NO-SENSE row. The script cuts the flag's neighbourhood out of the render
(t-2.5 s .. t+3.5 s, audio kept) and hands the MOVING CLIP to a visual model
with the clerk's claim, the words spoken in that window, and the STANDARD's
definition of a defect versus a transition. Three verdicts come back:

    CONFIRMED    a real defect, held or in motion, a phone viewer would notice
    TRANSITION   the element is arriving/leaving within ~2 s and lands correctly
    REFUTED      the claim is simply wrong about the pixels

Only CONFIRMED flags count. TRANSITION and REFUTED are logged in the clerk's
"dismissed" table with the model's reason, so the dismissal is auditable and the
procedure can be tuned against reality instead of against anybody's memory.

USAGE
-----
    verify_flags_gemini.py <render.mp4> <video_id> --flags flags.json \
        [--out verdicts.json] [--batch 6] [--label NAME] [--keep-clips]

flags.json is a list of objects:
    [{"t": 16.15, "claim": "a paper cup jammed into the phone's left edge",
      "caption": "This removes"}, ...]
"id" is optional and defaults to F<n>. "caption" is optional; when absent the
words are read out of the tight transcript anyway.

Flags are batched into as few model calls as the payload allows: every clip in a
batch is sent in ONE call, each preceded by a text part naming its flag, so the
model sees them as a labelled series. Token counts come back per call from
usage_metadata and are priced and totalled.

MODEL: gemini-3.5-flash-lite (Miguel's pick, 2026-09-03; was gemini-3.8-flash). Video analysis is the
approved Gemini lane (CLAUDE.md rule 6). Override with GEMINI_VERIFY_MODEL.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path.home() / "Documents/Workspace/.env")
os.environ["GEMINI_API_KEY"] = os.environ.get(
    "GEMINI_API_KEY_GENIAL", os.environ.get("GEMINI_API_KEY", ""))
from google import genai  # noqa: E402
from google.genai import types  # noqa: E402

FACTORY = Path.home() / "Documents/Workspace/projects/personal/content/shorts-factory"
MODEL = os.environ.get("GEMINI_VERIFY_MODEL", "gemini-3.5-flash-lite")

# gemini-3.5-flash-lite, per tools/gemini.md (2026-09-03): $0.30 / MTok in, $2.50 / MTok out.
# (3.8-flash was $0.75 / $3.75.) Output pricing includes thinking tokens.
# Output pricing includes thinking tokens. Override if the rate card moves.
PRICE_IN = float(os.environ.get("GEMINI_VERIFY_PRICE_IN", "0.30")) / 1e6
PRICE_OUT = float(os.environ.get("GEMINI_VERIFY_PRICE_OUT", "2.50")) / 1e6

MAX_OUT = int(os.environ.get("GEMINI_VERIFY_MAX_OUT", "24576"))  # thinking tokens count

PRE = 2.5   # seconds of run-up before the flagged instant
POST = 3.5  # seconds after it — long enough for a 2 s entrance to finish AND hold

VERDICT_SCHEMA = {
    "type": "object",
    "properties": {
        "verdicts": {"type": "array", "items": {"type": "object", "properties": {
            "flag_id": {"type": "string"},
            "verdict": {"type": "string", "enum": ["CONFIRMED", "TRANSITION", "REFUTED"]},
            "reason": {"type": "string"},
            "what_i_saw": {"type": "string"},
            "defect_from_seconds": {"type": "number"},
            "defect_to_seconds": {"type": "number"},
            "motion_defect": {"type": "boolean"},
        }, "required": ["flag_id", "verdict", "reason", "what_i_saw"]}},
    },
    "required": ["verdicts"],
}

PROMPT_HEAD = """You are the MOTION VERIFIER of a vertical-shorts QC chain. You are given short
CLIPS cut out of a finished 9:16 short, one clip per candidate defect that a
still-frame reviewer flagged. WATCH each clip. Your job is to say whether the
flagged thing is a real defect or an artefact of the reviewer having looked at a
single frame taken during an animation.

WHY YOU EXIST. The reviewer samples one still frame a fraction of a second after
each visual change. A still frame cannot tell a TRANSITION from a HELD STATE, so
elements caught mid-entrance get reported as missing, empty, late or broken. The
owner of this factory has ruled that class of report a FALSE POSITIVE. Entry and
exit animations of 1-2 seconds are NORMAL in this house style and are never a
defect on their own.

THE STANDARD'S DEFINITION - apply it literally.

A DEFECT (verdict CONFIRMED) is any of:
  * a HELD defect: the flagged wrongness is still true after the element has
    finished arriving, and persists for at least ~1.5 s of settled screen time;
  * a MOTION defect: an element visibly crosses into, over or through another
    object or a border WHILE MOVING - clipped by an object's outline, cut in half
    by a frame or card edge, a line drawn straight through printed type, two
    objects jammed together with no air - even if it is only there for a moment.
    Motion does not excuse a collision. Miguel confirmed this class explicitly:
    "the second logo is cut in half while moving - it has motion" is a DEFECT.
  * an EMPTY visual zone that stays empty for >= 1.5 s;
  * a NAMED TOOL whose mark is still absent >= 2 s after the word is spoken.

A TRANSITION (verdict TRANSITION) is: the flagged element is arriving or leaving
within roughly 2 seconds of the flagged instant and it LANDS CORRECTLY - the
bubble fills, the mark appears, the label settles into place, the outgoing mark
finishes clearing. The reviewer photographed the animation. Not a defect.

REFUTED is: the claim is factually wrong about the pixels - the thing said to be
missing is present the whole time, the thing said to overlap does not touch, the
label said to be misaligned is aligned.

RULES
  * Judge ONLY the flagged claim. Do not hunt for other defects and do not grade
    the video. If you would fail this clip for something else, ignore it.
  * Describe what you actually saw in "what_i_saw" BEFORE deciding - literal,
    plain, from the pixels, including whether the element was moving.
  * Alignment / baseline / margin claims are geometry, not timing: judge them on
    the settled part of the clip. If the labels really do sit on different
    baselines once everything has landed, that is CONFIRMED however small it is.
  * For CONFIRMED, fill "defect_from_seconds" and "defect_to_seconds" with the
    window IN ABSOLUTE VIDEO TIME (each clip's absolute start time is given
    below) over which the defect persists, and set "motion_defect" true when it
    is the moving-collision class rather than a held state.
  * A tie goes to the render: if you genuinely cannot resolve it from the clip,
    answer TRANSITION and say so in the reason.
  * One sentence in "reason". Blunt. No hedging language, no rubric talk.

Return one entry per flag, using the exact flag_id given.

THE FLAGS AND THEIR CLIPS FOLLOW."""


def salvage(text):
    """Recover whole verdict objects from a response the output cap cut short."""
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
    return {"verdicts": [o for o in out if "flag_id" in o and "verdict" in o]}


def flag_block(f):
    return (f"\n--- FLAG {f['id']} ---\n"
            f"Flagged instant: {f['t']:.2f} s of the full video "
            f"(that is {f['flag_offset']:.2f} s into the clip below).\n"
            f"Clip covers absolute video time {f['clip_start']:.2f}-{f['clip_end']:.2f} s.\n"
            f"Words spoken across the clip: \"{f['words_window']}\"\n"
            f"Caption at the flagged instant: \"{f.get('caption') or f['words_window']}\"\n"
            f"THE REVIEWER'S CLAIM: {f['claim']}\n"
            f"The clip for {f['id']} is the next video.")


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"{cmd[0]} failed: {p.stderr[-800:]}")
    return p.stdout


def find_transcript(video_id):
    """Any run's cuts/<id>/transcript_tight.json registers itself (qc_v3 pattern)."""
    hits = sorted(FACTORY.glob(f"shorts_run*/cuts/{video_id}/transcript_tight.json"))
    return hits[-1] if hits else None


def words_in(tr, t0, t1):
    if not tr:
        return "(no transcript)"
    out = [w["text"] for w in tr.get("words", [])
           if w.get("type") == "word" and w.get("start") is not None
           and w["start"] < t1 and w.get("end", w["start"]) > t0]
    return " ".join(out) if out else "(silence)"


def duration_of(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                      "-of", "default=nw=1:nk=1", str(path)]).strip())


def cut_clip(src, start, dur, dest):
    run(["ffmpeg", "-nostdin", "-v", "error", "-y",
         "-ss", f"{start:.3f}", "-i", str(src), "-t", f"{dur:.3f}",
         "-vf", "scale=720:-2", "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "30", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", str(dest)])
    return dest


def upload_retry(client, path, attempts=3):
    for i in range(attempts):
        try:
            f = client.files.upload(file=str(path))
            while f.state and f.state.name == "PROCESSING":
                time.sleep(1.5)
                f = client.files.get(name=f.name)
            if f.state and f.state.name == "ACTIVE":
                return f
        except Exception as e:  # noqa: BLE001
            print(f"upload retry {i+1} ({path.name}): {e}", file=sys.stderr)
        time.sleep(2 * (i + 1))
    raise RuntimeError(f"upload failed: {path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("video_id")
    ap.add_argument("--flags", required=True, help="JSON list of {t, claim, caption}")
    ap.add_argument("--out", default=None)
    ap.add_argument("--batch", type=int, default=6, help="clips per model call")
    ap.add_argument("--label", default=None)
    ap.add_argument("--keep-clips", action="store_true")
    a = ap.parse_args()

    src = Path(a.video)
    label = a.label or f"{a.video_id}_{src.stem}"
    flags = json.loads(Path(a.flags).read_text())
    for i, f in enumerate(flags, 1):
        f.setdefault("id", f"F{i}")
    tr_path = find_transcript(a.video_id)
    tr = json.loads(tr_path.read_text()) if tr_path else None

    total = duration_of(src)
    work = Path(tempfile.mkdtemp(prefix=f"verifyflags_{label}_"))
    client = genai.Client()

    # --- cut one clip per flag -------------------------------------------------
    for f in flags:
        t = float(f["t"])
        start = max(0.0, t - PRE)
        end = min(total, t + POST)
        f["clip_start"] = start
        f["clip_end"] = end
        f["flag_offset"] = t - start
        f["words"] = f.get("caption") or words_in(tr, start, end)
        f["words_window"] = words_in(tr, start, end)
        f["_clip"] = cut_clip(src, start, end - start, work / f"{f['id']}.mp4")

    verdicts, calls = {}, []
    try:
        for bi in range(0, len(flags), a.batch):
            batch = flags[bi:bi + a.batch]
            parts = [types.Part(text=PROMPT_HEAD)]
            for f in batch:
                parts.append(types.Part(text=flag_block(f)))
                up = upload_retry(client, f["_clip"])
                f["_uri"] = up.name
                f["_uri_full"] = up.uri
                parts.append(types.Part(file_data=types.FileData(
                    file_uri=up.uri, mime_type="video/mp4")))
            parts.append(types.Part(text=(
                "\nNow return one verdict object per flag, flag_ids exactly: "
                + ", ".join(f["id"] for f in batch) + ".")))

            resp = client.models.generate_content(
                model=MODEL, contents=[types.Content(parts=parts)],
                config={"response_mime_type": "application/json",
                        "response_schema": VERDICT_SCHEMA,
                        "max_output_tokens": MAX_OUT})

            um = resp.usage_metadata
            tin = getattr(um, "prompt_token_count", 0) or 0
            tout = ((getattr(um, "candidates_token_count", 0) or 0)
                    + (getattr(um, "thoughts_token_count", 0) or 0))
            cost = tin * PRICE_IN + tout * PRICE_OUT
            calls.append({"flags": [f["id"] for f in batch], "model": MODEL,
                          "input_tokens": tin, "output_tokens": tout,
                          "cost_usd": round(cost, 6)})

            # A truncated response (output cap, thinking tokens included) is not a
            # verdict. Never let a parse failure silently drop flags: parse what
            # arrived, and re-ask for whatever is still missing, one flag per call.
            try:
                data = json.loads(resp.text or "{}")
            except json.JSONDecodeError:
                data = salvage(resp.text or "")
                print(f"  ! truncated response, salvaged "
                      f"{len(data.get('verdicts', []))}/{len(batch)}", file=sys.stderr)
            for v in data.get("verdicts", []):
                if v.get("flag_id"):
                    verdicts[v["flag_id"]] = v
            print(f"[call {len(calls)}] {len(batch)} flags  in={tin} out={tout} "
                  f"${cost:.4f}", file=sys.stderr)

            missing = [f for f in batch if f["id"] not in verdicts]
            for f in missing:
                r2 = client.models.generate_content(
                    model=MODEL,
                    contents=[types.Content(parts=[
                        types.Part(text=PROMPT_HEAD),
                        types.Part(text=flag_block(f)),
                        types.Part(file_data=types.FileData(
                            file_uri=f["_uri_full"], mime_type="video/mp4")),
                        types.Part(text=f"\nReturn one verdict object for {f['id']}.")])],
                    config={"response_mime_type": "application/json",
                            "response_schema": VERDICT_SCHEMA,
                            "max_output_tokens": MAX_OUT})
                um2 = r2.usage_metadata
                t2i = getattr(um2, "prompt_token_count", 0) or 0
                t2o = ((getattr(um2, "candidates_token_count", 0) or 0)
                       + (getattr(um2, "thoughts_token_count", 0) or 0))
                c2 = t2i * PRICE_IN + t2o * PRICE_OUT
                calls.append({"flags": [f["id"]], "model": MODEL, "retry": True,
                              "input_tokens": t2i, "output_tokens": t2o,
                              "cost_usd": round(c2, 6)})
                try:
                    for v in json.loads(r2.text or "{}").get("verdicts", []):
                        verdicts[v.get("flag_id") or f["id"]] = v
                except json.JSONDecodeError:
                    for v in salvage(r2.text or "").get("verdicts", []):
                        verdicts[v.get("flag_id") or f["id"]] = v
                print(f"  [retry {f['id']}] in={t2i} out={t2o} ${c2:.4f}",
                      file=sys.stderr)
    finally:
        for f in flags:
            if f.get("_uri"):
                try:
                    client.files.delete(name=f["_uri"])
                except Exception:  # noqa: BLE001
                    pass
        if not a.keep_clips:
            shutil.rmtree(work, ignore_errors=True)

    total_cost = sum(c["cost_usd"] for c in calls)
    result = {
        "video": str(src), "video_id": a.video_id, "model": MODEL,
        "flags": [{k: v for k, v in f.items() if not k.startswith("_")} for f in flags],
        "verdicts": [verdicts.get(f["id"], {"flag_id": f["id"], "verdict": "REFUTED",
                                            "reason": "NO RESPONSE FROM MODEL",
                                            "what_i_saw": ""}) for f in flags],
        "calls": calls,
        "counts": {v: sum(1 for f in flags
                          if verdicts.get(f["id"], {}).get("verdict") == v)
                   for v in ("CONFIRMED", "TRANSITION", "REFUTED")},
        "cost_usd": round(total_cost, 6),
        "clip_window": {"pre": PRE, "post": POST},
    }
    from runs import newest_run  # noqa: E402
    out = Path(a.out) if a.out else (newest_run() / f"review/flagcheck_{label}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=1))

    # ── THE COST LEDGER (2026-09-04) ────────────────────────────────────────
    # Same rule as the watcher: the verifier books its own bill out of its own
    # token arithmetic, so a flag-check run by hand during a fix round is still
    # in the run's total.  Nothing is re-priced here.
    try:
        sys.path.insert(0, str(FACTORY / "pipeline"))
        import costs as COSTS                                    # noqa: E402
        _run = COSTS.resolve_run(os.environ.get("SHORTS_RUN") or None, out)
        COSTS.safe_record(
            _run, "gemini", "verify", float(result["cost_usd"]),
            video=a.video_id,
            units=(f"{sum(c.get('input_tokens') or 0 for c in calls):,} in / "
                   f"{sum((c.get('output_tokens') or 0) + (c.get('thinking_tokens') or 0) for c in calls):,}"
                   f" out tokens over {len(calls)} calls, {len(flags)} flags"),
            note=f"flag verification, {MODEL}",
            ref=COSTS.call_ref(_run, out, int(src.stat().st_mtime_ns)))
    except Exception as exc:                                     # noqa: BLE001
        print(f"[costs] verifier not recorded ({type(exc).__name__}: {exc})",
              file=sys.stderr)
    print(json.dumps({"out": str(out), "counts": result["counts"],
                      "cost_usd": result["cost_usd"]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
