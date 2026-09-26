#!/usr/bin/env python3
"""THE REGRESSION TEST for the run-9 "in" / LinkedIn caption defect.

    ~/Documents/Workspace/.venv/bin/python pipeline/test_captions_function_words.py

WHAT SHIPPED, AND WHY IT WAS A BUG
----------------------------------
`perplexityprojects_split.mp4` and `_cutout.mp4` painted a caption beat whose
whole text was the word "in" (from "You can now store them | in | dedicated
folders").  The canonical pill is `white-space:nowrap` with fixed 33.8px
horizontal padding, so a two-letter beat collapses a 264px pill into a 42px
rounded square carrying a bold white lowercase "in" — the LinkedIn badge.  The
independent viewer test named it from the pixels and held both renders.

No code substituted a logo.  The CHUNKER produced the orphan and the pill's own
geometry did the rest.  These tests pin the law that prevents it.

The three canonical strings, from the fix brief:
    "store them in dedicated folders"   the defect itself
    "log in to Notion"                  "in" and "to" adjacent, mid-sentence
    "LinkedIn is down"                  a real brand token must still be allowed

The measurer is a deterministic stub — this test is about CHUNKING, not about
Chromium.  `pipeline/captions.py` is measured for real by the builds.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import captions as CAP  # noqa: E402


class StubMeasurer:
    """Width model: 30px per character + the canonical 2 x 33.8px padding.

    Monotonic in length, which is all the splitter and the merger need.  A seat
    is passed explicitly per test so the merge's fit branch can be exercised.
    """

    def width(self, text: str) -> float:
        return len(text) * 30.0 + 2 * CAP.CAP_PAD_X


M = StubMeasurer()
WIDE = 10_000.0          # a seat nothing can overflow
FAILURES: list[str] = []


def check(name: str, got, want) -> None:
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {name}\n"
          f"        got  {got!r}\n        want {want!r}")
    if not ok:
        FAILURES.append(name)


def beats(phrase: str) -> list[list[str]]:
    return [[w] for w in phrase.split()]


def texts(bs) -> list[str]:
    return [" ".join(b) for b in bs]


# =============================================================================
print("1. is_function_only / is_orphan_beat — the predicate")
# =============================================================================
check("'in' is function-only", CAP.is_function_only("in"), True)
check("'in' is an orphan beat", CAP.is_orphan_beat("in"), True)
check("'of the' at 270px is NOT refused — two tokens, and it reads as text",
      CAP.is_orphan_beat("of the", 270.0), False)
check("... but 'of the' squeezed square IS refused",
      CAP.is_orphan_beat("of the", 120.0), True)
check("'store them' is NOT function-only", CAP.is_function_only("store them"), False)
check("'store them' is not an orphan", CAP.is_orphan_beat("store them"), False)
check("'folders' is not an orphan", CAP.is_orphan_beat("folders"), False)
check("'AI' alone IS an orphan (sub-4 solo, no measured width)",
      CAP.is_orphan_beat("AI"), True)
# the same predicate, now with the pill actually measured
check("a SQUARE pill is an orphan whatever it says",
      CAP.is_orphan_beat("day.", 116.0), True)
check("a pill past the aspect floor is fine",
      CAP.is_orphan_beat("day.", 174.8), False)
check("the shipped 'in' pill: 116.1px on a 114.59px pill = square",
      CAP.is_badge_pill(116.1), True)
check("'you can' (270.3px measured) is NOT an orphan — it reads as text",
      CAP.is_orphan_beat("you can", 270.3), False)
check("punctuation does not hide it ('in,')", CAP.is_orphan_beat("in,"), True)
check("case does not hide it ('In')", CAP.is_orphan_beat("In"), True)

# =============================================================================
print("\n2. \"store them in dedicated folders\" — THE SHIPPED DEFECT")
# =============================================================================
# The exact shape the split render produced: the phrase chunker flushed after
# "store them" and left "in" standing alone.
shipped = [["store", "them"], ["in"], ["dedicated", "folders"]]
check("the shipped chunking is caught",
      [t for t in texts(shipped) if CAP.is_orphan_beat(t)], ["in"])

fixed = CAP.merge_function_only_beats(shipped, WIDE, M)
check("'in' binds FORWARD into 'in dedicated folders'",
      texts(fixed), ["store them", "in dedicated folders"])
check("no orphan survives",
      [t for t in texts(fixed) if CAP.is_orphan_beat(t)], [])

# and the assert is what actually stops a build
try:
    CAP.assert_no_function_only_beat(texts(shipped))
    check("assert_no_function_only_beat raises on the shipped chunking",
          "no exception", "SystemExit")
except SystemExit as e:
    check("assert_no_function_only_beat raises on the shipped chunking",
          "in" in str(e), True)
try:
    CAP.assert_no_function_only_beat(texts(fixed))
    check("assert passes on the fixed chunking", "no exception", "no exception")
except SystemExit as e:                                    # pragma: no cover
    check("assert passes on the fixed chunking", str(e), "no exception")

# a narrow seat forces the BACKWARD fallback rather than shipping the orphan
narrow = CAP.merge_function_only_beats(shipped, len("in dedicated folders") * 30.0,
                                       WIDE and M)
check("with no room forward, 'in' binds BACKWARD",
      texts(narrow), ["store them in", "dedicated folders"])

# =============================================================================
print("\n3. \"log in to Notion\" — adjacent function words, mid-sentence")
# =============================================================================
li = [["log"], ["in"], ["to"], ["Notion"]]
# "log" is a content word but only 3 characters, so it is refused on WIDTH —
# a 3-glyph pill is a badge whatever the grammar says.
check("'in', 'to' AND the sub-4 'log' are all orphans",
      [t for t in texts(li) if CAP.is_orphan_beat(t)], ["log", "in", "to"])
li_fixed = CAP.merge_function_only_beats(li, WIDE, M)
check("one left-to-right pass leaves two readable pills",
      texts(li_fixed), ["log in", "to Notion"])
check("no orphan survives",
      [t for t in texts(li_fixed) if CAP.is_orphan_beat(t)], [])
check("'log' alone is refused (sub-4 solo)", CAP.is_orphan_beat("log"), True)
check("'log in' is a legal pill (2 tokens, one of them content)",
      CAP.is_orphan_beat("log in"), False)

# =============================================================================
print("\n4. \"LinkedIn is down\" — a real brand token must survive")
# =============================================================================
lb = [["LinkedIn"], ["is"], ["down"]]
check("'LinkedIn' is NOT an orphan", CAP.is_orphan_beat("LinkedIn"), False)
check("'is' IS an orphan", CAP.is_orphan_beat("is"), True)
lb_fixed = CAP.merge_function_only_beats(lb, WIDE, M)
check("'is' binds forward, 'LinkedIn' stands alone as a brand pill",
      texts(lb_fixed), ["LinkedIn", "is down"])
check("'down' is NOT a stopword — it carries this sentence",
      CAP.is_function_word("down"), False)
check("no orphan survives",
      [t for t in texts(lb_fixed) if CAP.is_orphan_beat(t)], [])

# =============================================================================
print("\n5. brand_token_ok — the gate on any FUTURE mark substitution")
# =============================================================================
REG = ["linkedin", "notion", "perplexity", "claude", "chatgpt"]
check("'in' is refused (function word, and 2 chars)",
      CAP.brand_token_ok("in", REG), False)
check("'to' is refused", CAP.brand_token_ok("to", REG), False)
check("'LinkedIn' is allowed (exact registry entry)",
      CAP.brand_token_ok("LinkedIn", REG), True)
check("'LinkedIn.' is allowed (punctuation normalised)",
      CAP.brand_token_ok("LinkedIn.", REG), True)
check("'Notion' is allowed", CAP.brand_token_ok("Notion", REG), True)
check("'link' is refused — a prefix is not an exact token",
      CAP.brand_token_ok("link", REG), False)
check("'perplexityprojects' is refused — a superstring is not an exact token",
      CAP.brand_token_ok("perplexityprojects", REG), False)
check("a word absent from the registry is refused",
      CAP.brand_token_ok("folders", REG), False)

# =============================================================================
print("\n6. the merge never invents or loses a word")
# =============================================================================
for src in (shipped, li, lb):
    flat_in = [w for b in src for w in b]
    flat_out = [w for b in CAP.merge_function_only_beats(src, WIDE, M) for w in b]
    check(f"word stream preserved for {' '.join(flat_in)!r}", flat_out, flat_in)

# =============================================================================
print()
if FAILURES:
    raise SystemExit(f"{len(FAILURES)} FAILED: {FAILURES}")
print("ALL CAPTION FUNCTION-WORD TESTS PASS")
