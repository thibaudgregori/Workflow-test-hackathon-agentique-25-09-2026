#!/usr/bin/env python3
"""POINTING CUES -> THE SOURCE POST.  ROUND-4 LAW 1 (Miguel, 2026-09-02).

    "When I say 'like this person, or guy on X' I usually point up, that means
     that the tweet related to that post should appear with the highlight."

Miguel points at the ceiling when he cites someone.  The gesture is on camera in
every take, and it is the ONE moment the audience is being told "this is not me
talking, this is a thing somebody posted".  If the source post is not on screen
at that word, the gesture points at nothing.

This module finds those moments DETERMINISTICALLY, from the tight transcript,
before anything is drawn — so the PLAN can list every cue and the card it
raises, and the clerk can check the list against the frames.

It is deliberately format-agnostic: the cue is a property of the SCRIPT, not of
the chassis.  The card it demands is still bound by GLOBAL LAW 3's tweet
discipline — 2-4 s, no metrics chrome, and only when the post IS the news.

    from pointing_cues import scan, assert_cues_covered
    cues = scan(words)                       # [{i, t, phrase, cue, kind}]
    assert_cues_covered(cues, plan_cards)    # refuses a plan that ignores one

CLI:
    pointing_cues.py --vid <vid> [--run <shorts_runN>] [--json out.json]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

F = Path.home() / "Documents/Workspace/projects/personal/content/shorts-factory"
def _latest_run(root: Path) -> Path:
    """The newest shorts_run* on disk.  A PINNED default (it was run 9)
    reads a dead run the day the next one starts, and the failure is a
    FileNotFoundError on somebody else's transcript rather than a clear miss."""
    runs = sorted((d for d in (root / "runs").glob("shorts_run*") if d.is_dir()),
                  key=lambda d: int("".join(c for c in d.name if c.isdigit()) or 0))
    if not runs:
        raise FileNotFoundError(f"no shorts_run<N> folder under {root}; set SHORTS_RUN")
    return runs[-1]


RUN = Path(os.environ.get("SHORTS_RUN") or _latest_run(F))

# The card must be up WITH the word, not after it: the same one-block rule the
# label law uses (GLOBAL LAW 9).
CUE_WINDOW = 1.0          # seconds either side of the cue word
CARD_MIN = 2.0            # GLOBAL LAW 3: a real post holds 2-4 s
CARD_MAX = 4.0

# Every pattern is anchored on a DEMONSTRATIVE or an INDEFINITE plus a person or
# a post — the two grammars Miguel actually uses when he points.  Ordered most
# specific first; the first match at a position wins, so "this guy on X" is a
# person cue, not a bare "this post".
PATTERNS: tuple[tuple[str, str], ...] = (
    ("person",
     r"\b(?:like\s+)?th(?:is|at)\s+(?:guy|girl|person|dude|man|woman|founder|"
     r"engineer|researcher|dev|developer|account)\b"),
    ("person",
     r"\b(?:some|a)\s?(?:one|body|guy|girl|person|dude|man|woman|founder|"
     r"engineer|researcher|dev|developer)\s+(?:on|from)\s+"
     r"(?:x|twitter|linkedin|reddit|hacker\s?news|hn|github)\b"),
    ("person",
     r"\b(?:a|this|that)\s+(?:guy|girl|person|dude|man|woman)\s+who\b"),
    ("person",
     r"\b(?:someone|somebody)\s+(?:just\s+)?(?:posted|tweeted|shared|wrote)\b"),
    ("post",
     r"\bth(?:is|at)\s+(?:post|tweet|thread|screenshot|reply|comment)\b"),
    ("post",
     r"\b(?:saw|read|found|came\s+across)\s+(?:a|this|the)\s+"
     r"(?:post|tweet|thread|screenshot|comment)\b"),
    ("post",
     r"\b(?:a|this|the)\s+(?:post|tweet|thread)\s+(?:on|from)\s+"
     r"(?:x|twitter|linkedin|reddit|hacker\s?news|hn|github)\b"),
    ("person",
     r"\b(?:guy|girl|person|dude)\s+on\s+(?:x|twitter|linkedin|reddit)\b"),
)
_COMPILED = tuple((kind, re.compile(rx, re.I)) for kind, rx in PATTERNS)


def _norm(w: str) -> str:
    return re.sub(r"[^a-z0-9' ]", "", w.lower()).strip()


def scan(words: list[dict]) -> list[dict]:
    """Every pointing cue in a tight transcript, in order.

    `words` is the factory's tight-transcript shape: {"word"|"text", "start",
    "end"}.  Returns, per cue: the word INDEX the card must be up on, that
    word's time, the matched phrase, and the window the card must open in.
    """
    toks = [_norm(w.get("word") or w.get("text") or "") for w in words]
    # a character-offset map so a phrase match resolves back to a word index
    offs, buf = [], []
    pos = 0
    for tk in toks:
        offs.append(pos)
        buf.append(tk)
        pos += len(tk) + 1
    line = " ".join(buf)
    hits: list[dict] = []
    taken: list[tuple[int, int]] = []
    for kind, rx in _COMPILED:
        for m in rx.finditer(line):
            a, b = m.span()
            if any(a < y and x < b for x, y in taken):
                continue
            taken.append((a, b))
            i = max(k for k, o in enumerate(offs) if o <= a)
            j = max(k for k, o in enumerate(offs) if o < b)
            t = float(words[i].get("start", 0.0))
            hits.append({
                "i": i, "j": j, "t": round(t, 2), "kind": kind,
                "phrase": re.sub(r"\s+", " ", m.group(0)).strip(),
                "word": (words[i].get("word") or words[i].get("text") or "").strip(),
                "window": [round(max(0.0, t - CUE_WINDOW), 2),
                           round(t + CUE_WINDOW, 2)],
                "card_hold_s": [CARD_MIN, CARD_MAX],
            })
    hits.sort(key=lambda h: h["i"])
    return hits


def assert_cues_covered(cues: list[dict], cards: list[dict]) -> dict:
    """ROUND-4 LAW 1, at plan time.

    `cards` is what the PLAN declares: [{"at": <seconds>, "asset": <path|id>,
    "highlight": <the line the marker scopes>, "cue_i": <word index>}].  Every
    cue must have a card whose entry lands inside the cue's window, and that
    card must declare the highlighted line — a source post with no highlight
    scopes nothing, which is the one job GLOBAL LAW 5 gives it.

    A cue may be answered by `{"at": ..., "waived": "<why>"}` when the post is
    NOT the news (GLOBAL LAW 3) — the waiver is written down, never silent.
    """
    bad = []
    for c in cues:
        lo, hi = c["window"]
        m = [k for k in cards
             if k.get("cue_i") == c["i"] or (lo <= float(k.get("at", -99)) <= hi)]
        if not m:
            bad.append(f"{c['phrase']!r} at {c['t']:.2f}s ({c['kind']}) raises "
                       f"no source card in {lo:.2f}-{hi:.2f}s")
            continue
        k = m[0]
        if k.get("waived"):
            continue
        if not k.get("asset"):
            bad.append(f"{c['phrase']!r} at {c['t']:.2f}s: the card names no asset")
        if not k.get("highlight"):
            bad.append(f"{c['phrase']!r} at {c['t']:.2f}s: the card carries no "
                       "highlighted line — a post with nothing scoped argues nothing")
    if bad:
        raise SystemExit("ROUND-4 LAW 1 — a pointing cue with no source post:\n  "
                         + "\n  ".join(bad))
    return {"cues": len(cues), "cards": len(cards), "verdict": "PASS"}


def load_words(vid: str, run: Path | None = None) -> list[dict]:
    run = run or RUN
    p = run / f"cuts/{vid}/transcript_tight.json"
    d = json.loads(p.read_text())
    return d["words"] if isinstance(d, dict) else d


def main() -> None:
    ap = argparse.ArgumentParser(description="ROUND-4 LAW 1 — pointing cues")
    ap.add_argument("--vid", required=True)
    ap.add_argument("--run", type=Path, default=None)
    ap.add_argument("--json", type=Path, default=None)
    a = ap.parse_args()
    cues = scan(load_words(a.vid, a.run))
    out = {"vid": a.vid, "cues": cues, "cue_window_s": CUE_WINDOW,
           "card_hold_s": [CARD_MIN, CARD_MAX]}
    if a.json:
        a.json.write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))
    if not cues:
        print("no pointing cue in this take", file=sys.stderr)


if __name__ == "__main__":
    main()
