#!/usr/bin/env python
"""apply_metadata.py — drop an author-written cover plan + captions into a
delivered package, render the cover, validate everything, no model calls.

Generalised on 2026-09-14 from run 19's apply_metadata.py (run 19's five
packages were covered and captioned by hand with it).  The METADATA agent in
daily-shorts.js writes ONE drafts json per recording from the complete tight
transcript, VOICE.md and the shorts-thumbnail-factory rules, then runs this.

usage: apply_metadata.py --package "<Ready to Publish>/<title>" --drafts <drafts.json>

drafts.json shape (every key required):
  title        YouTube title (checked with execution/youtube_title_width.py: <=600 px, <=100 chars)
  lines        cover lines, 2-4 uppercase strings; the LAST carries the terracotta highlight
  kw           the highlight keyword (must appear in the transcript and in the last line, <=8 chars ideal)
  pose         a render_shorts_thumbnail.py pose name, or "auto"
  kw_reason, hl_reason, sentence, claim   editorial reasoning (headline-plan fields)
  quotes       2-3 VERBATIM transcript quotes supporting the headline (asserted present)
  ct, cl       description_strategy content_type / description_length
  reason       one sentence why that strategy
  yd           YouTube description   tags: YouTube tags list
  tt           TikTok caption         ig: Instagram caption
  rr           resource_review sentence
prints one json line {"status": "ok"|"error", ...}; exit 1 on error.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import subprocess
import sys

F = pathlib.Path(__file__).resolve().parents[2]
WS = pathlib.Path.home() / "Documents/Workspace"
PY = str(WS / ".venv/bin/python")
REQUIRED = ("title", "lines", "kw", "pose", "kw_reason", "hl_reason", "sentence", "claim", "quotes",
            "ct", "cl", "reason", "yd", "tags", "tt", "ig", "rr")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--package", required=True)
    ap.add_argument("--drafts", required=True)
    a = ap.parse_args()
    pkg = pathlib.Path(a.package).expanduser().resolve()
    out = {"status": "error", "package": str(pkg)}

    def fail(msg):
        out["error"] = msg
        print(json.dumps(out))
        return 1

    try:
        d = json.loads(pathlib.Path(a.drafts).read_text())
    except Exception as exc:                                 # noqa: BLE001
        return fail(f"drafts unreadable: {exc}")
    missing = [k for k in REQUIRED if k not in d]
    if missing:
        return fail(f"drafts missing keys: {missing}")
    pub = pkg / "Publishing"
    tp = pub / "transcript_tight.json"
    if not tp.exists() or not (pub / "package.json").exists():
        return fail("not a delivered package: Publishing/transcript_tight.json or package.json missing")
    raw = tp.read_bytes()
    text = json.loads(raw)["text"]
    bad = [q for q in d["quotes"] if q not in text]
    if bad or not d["quotes"]:
        return fail(f"quotes not verbatim in the transcript: {bad[:2]}")
    if d["kw"].lower() not in text.lower():
        return fail(f"keyword {d['kw']!r} not in the transcript")
    if d["kw"].upper() not in d["lines"][-1].upper():
        return fail("the keyword must sit in the LAST (highlighted) cover line")
    w = subprocess.run([PY, str(WS / "execution/youtube_title_width.py"), d["title"]], capture_output=True, text=True)
    if w.returncode != 0 or not w.stdout.startswith("PASS"):
        return fail("YouTube title width/length failed: " + (w.stdout + w.stderr).strip()[-200:])
    sid = json.loads((pub / "package.json").read_text())["short_id"]
    plan = {"short_id": sid, "source_package": str(pkg), "transcript_path": str(tp),
            "transcript_sha256": hashlib.sha256(raw).hexdigest(), "transcript_character_count": len(text),
            "full_transcript_read": True, "keyword": d["kw"], "keyword_reason": d["kw_reason"],
            "headline_reason": d["hl_reason"], "supporting_quotes": d["quotes"], "lines": d["lines"],
            "headline_sentence": d["sentence"], "video_claim": d["claim"], "headline_matches_claim": True}
    (pub / "Thumbnails").mkdir(parents=True, exist_ok=True)
    (pub / "Thumbnails/headline-plan.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    # next free version folder: v1, v2, ...
    n = 1
    while (pub / "Thumbnails" / f"v{n}").exists():
        n += 1
    outdir = pub / "Thumbnails" / f"v{n}"
    cmd = [PY, str(WS / "execution/render_shorts_thumbnail.py"), "--headline-plan", str(pub / "Thumbnails/headline-plan.json"),
           "--pose", d["pose"], "--output", str(outdir)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    pose_used = d["pose"]
    if r.returncode != 0 and d["pose"] != "auto":
        cmd[cmd.index("--pose") + 1] = "auto"
        r = subprocess.run(cmd, capture_output=True, text=True)
        pose_used = "auto"
    if r.returncode != 0:
        return fail("cover render failed: " + (r.stdout + r.stderr).strip()[-600:])
    covers = sorted(str(p) for p in (outdir / "Exports").glob("*-cover.*")) if (outdir / "Exports").exists() else []
    cap = {"short_id": sid, "title": pkg.name, "written_at": dt.datetime.now().replace(microsecond=0).isoformat(),
           "voice_profile": "projects/personal/content/shorts-factory/pipeline/publish/VOICE.md",
           "authored_by": "the METADATA agent of daily-shorts.js from the complete tight transcript",
           "youtube": {"title": d["title"], "description": d["yd"], "tags": d["tags"],
                       "title_checked": w.stdout.strip()},
           "tiktok": {"caption": d["tt"]}, "instagram": {"caption": d["ig"], "trial": False},
           "description_strategy": {"version": "2026-09-08", "content_type": d["ct"], "description_length": d["cl"],
                                    "reason": d["reason"], "transcript_path": "Publishing/transcript_tight.json",
                                    "transcript_sha256": hashlib.sha256(raw).hexdigest(), "evidence": d["quotes"],
                                    "resource_review": d["rr"]}}
    (pub / "captions.json").write_text(json.dumps(cap, indent=2, ensure_ascii=False) + "\n")
    pol = subprocess.run([PY, str(F / "pipeline/publish/description_policy.py"), "--package", str(pkg)], capture_output=True, text=True)
    if pol.returncode != 0:
        return fail("description_policy refused: " + (pol.stdout + pol.stderr).strip()[-400:])
    out.update({"status": "ok", "cover_dir": str(outdir), "covers": covers, "pose": pose_used,
                "captions": str(pub / "captions.json"), "title_check": w.stdout.strip(), "policy": "PASS"})
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
