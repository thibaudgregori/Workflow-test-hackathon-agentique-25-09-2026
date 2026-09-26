#!/usr/bin/env python
"""cut_plan.py - the agent's view of a raw transcript, for choosing what to keep.

The cut is decided by a MODEL reading the transcript (Miguel, 2026-09-22), not by
word-matching rules. This tool only shows the words with their indexes and checks
the agent's choice; it decides nothing.

  cut_plan.py show  <raw transcript.json>                 numbered words, one sentence per line
  cut_plan.py check <raw transcript.json> --keep '[[a,b],...]'   validates and prints the kept text

keep = [[first_word, last_word], ...] indexes as printed by `show`, ascending, non-overlapping.
Put the result on the intake row as "keep_words"; prep_batch.py cuts exactly that.
"""
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cutlib import load_words


def show(words):
    line, first = [], 0
    for i, w in enumerate(words):
        if not line: first = i
        line.append(w["text"])
        if w["text"].endswith((".", "?", "!", "-", "…")) or i == len(words) - 1:
            print(f"[{first:4d}-{i:4d}] {float(words[first]['start']):7.2f}s  {' '.join(line)}")
            line = []


def check(words, keep):
    n, prev, kept, dur = len(words), -1, [], 0.0
    for a, b in keep:
        if not (0 <= a <= b < n) or a <= prev:
            raise SystemExit(f"REFUSED: [{a}, {b}] out of order or out of range (0..{n - 1})")
        prev = b
        kept += words[a:b + 1]
        dur += float(words[b]["end"]) - float(words[a]["start"])
    print(json.dumps({"ranges": keep, "kept_words": len(kept), "dropped_words": n - len(kept),
                      "spoken_seconds": round(dur, 1)}))
    print(" ".join(w["text"] for w in kept))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", choices=["show", "check"])
    ap.add_argument("transcript", type=Path)
    ap.add_argument("--keep", default=None)
    a = ap.parse_args()
    words = load_words(a.transcript)
    if a.action == "show":
        show(words)
    else:
        check(words, json.loads(a.keep))
