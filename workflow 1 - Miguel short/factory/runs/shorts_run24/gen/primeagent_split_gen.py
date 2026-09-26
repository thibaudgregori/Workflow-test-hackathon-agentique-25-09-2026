#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION — primeagent / DIAGRAM BUILD.

    YouTube   classic split 50/50   projects/primeagent_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/primeagent_scene.py` plus
`plans/primeagent_scene_handoff.md` are the design author's artefacts, sealed by
`review/artwork_pass_primeagent.json` (three bespoke objects; object 2, the
crossed hammer and screwdriver, was reviewed by MIGUEL HIMSELF on 2026-09-21 and
accepted under the name "two crossed tools").  This file IMPORTS the module and
SEATS it; it does not mutate a byte of the file on disk, because the CUTOUT
author is a different agent reading the same file for TikTok.  The Reels
WHITEBOARD redraws the same ARGUMENT in marker and does not import it at all.

TAKEOVER and FACESPLIT are not daily deliverables and this file cannot build one.

HD DELIVERY: authored AND encoded 1080x1920.  No zoom:2, no data-width 2160.
The face plate is `face_bottom_hd.mp4` (1080x1058), so the seam is
1920 - 1057.5 = 862.5 and the RENDERING pill top is 862.5 - 114.59/2 = 805.205 —
derived from the pill that RENDERS, never from the frozen 108.2 seat constant.

THE TWO PLACEMENT DECISIONS THIS LANE OWNS
------------------------------------------
  k    = 1.00    the artwork's sealed size, untouched.
  top  = 192.0   the handoff's own number.  CONTENT_Y0 60 lands at canvas 252,
                 60 px under LAW 30's top-10% line (192); CONTENT_Y1 549 lands
                 at canvas 741, 64.2 px above the rendering pill top 805.205.

PREP WAS CONSUMED, NOT REDONE.  The split needs the CUT and nothing else and
makes no Modal call of any kind.  All SEVEN prep markers for this recording are
"ok" and their numbers are quoted in the build sheet.  MATTES_FINAL / the ship
marker belong to the cutout lane, not to this one.

NO EMPHASIS ELEMENT IS STAMPED, AND THAT IS THE INSTRUMENT'S READING.
This video prints NO raster-borne type at all (no source card, no screenshot, no
pointing cue), so LAW 38 rule 1 has nothing to highlight.  BOTH emphases are
rule 2 on a DRAWN target and both are a BORDER/OUTLINE FLIP of the target's own
ink — the machine's gantry outline at 17.62, the three tile borders at 33.28.
No element is added, so there is nothing to carry `data-emphasis`, and declaring
a target as its own `data-emphasis-target` would make `visual_laws.CHECK_JS`
compare an element's ink with itself.  This is the `geminigems_split` reading of
the same shape, one recording earlier in this run.  Rule 3: the module emits no
`<circle>` tag at all — the filament spool's disc and hub are two-arc `<path>`s.

NO CONNECTOR EXISTS IN THIS SCENE.  `line_svg` is never called by `build()`, so
the emitted page carries zero `data-connect-to`.  Every relationship here is
CONTAINMENT (the tools in the box, the part on the bed, the machine on the slab)
and is carried by the declared blocks.  LAW 40 binds connectors that exist; it
does not require any.

THE ONE FORMAT-SIDE REPAIR, MADE ON THE EMITTED STRING ONLY
-----------------------------------------------------------
`#key-one-tool` ("ONE SINGLE TOOL") arrives at 12.32 instead of the plan's and
the module's 11.62.  LAW 24 (NO PEEK-AHEAD): at 11.62 he has spoken "one"
(11.62) but not "single" (11.98) or "tool." (12.32), so two thirds of the key
would be on screen before the words that license it.  12.32 is the START of
"tool.", the first instant at which the whole key has been spoken, and it is
inside that word's own 1.0 s LABEL_WINDOW.  The sibling recording in this run
made the same call on its own three-word key ("ONE SESSION lands on the spoken
'session' ... so the whole key is behind its words").  Nothing else changes: the
seat, the ink, the size and the release are the module's.  Written up in
`plans/primeagent_split_notes.md` so the CUTOUT lane inherits the same repair
and the two lanes stay in parity (LAW 51).
"""
from __future__ import annotations

import argparse
import html as ihtml
import json
import shutil
import subprocess
import sys
from pathlib import Path

F = Path(__file__).resolve().parents[3]           # the factory root
sys.path.insert(0, str(F / "pipeline"))
sys.path.insert(0, str(F / "pipeline/prep"))
sys.path.insert(0, str(F / "formats/cutout/lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import captions as CAP                          # noqa: E402
import cutout_core as CC                        # noqa: E402
import cutout_depthfield as DF                  # noqa: E402
import pointing_cues as PCUE                    # noqa: E402
import primeagent_scene as SC                   # noqa: E402

RUN = Path(__file__).resolve().parents[1]
CUT = RUN / "cuts/primeagent"
PLAN = RUN / "plans/primeagent_plan.json"
ASSETS = Path.home() / "Documents/Workspace/assets"
MUSIC = ASSETS / "audio/music/shorts-factory"
SFXLIB = ASSETS / "audio/sfx/shorts-factory"

VID = "primeagent"
W, H = 1080.0, 1920.0
FPS = 25
DUR = 43.175                                     # the cut master, prep's own

SEAM = 862.5                                     # the published split's seam
CORE_TOP_SPLIT = SC.CANVAS_OFFSET                # 192.0, the handoff's number
CORE_K = 1.00
LEFT = (W - SC.CORE_W * CORE_K) / 2               # 0.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "Prime Agent is the first AI agent that builds its own tools"
LABEL_WINDOW = 1.0

# THE LAW 24 REPAIR — see the module docstring.  w48 'tool.' starts here.
KEYONE_REPAIRED = 12.32

# ------------------------------------------------------------------ marks
# MARK IDENTITY (STANDARD.md): the FILE is named, never "the logo".
# `claude-code` is the plain no-outline mascot
# (coding-tools/claudecode-color.png) and NEVER `claude-code.png`, the die-cut
# white-outlined sticker whose edge would halo on cream.  `codex-color.png` and
# `cursor.png` are the PRODUCT marks, never a parent company's (LAW 35).
STAGE_FILES = {k: f"logos/{v}" for k, v in SC.LOGO_FILES.items()}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}
CUTOUT_LANES = SC.CUTOUT_LOGO_LANES


# ------------------------------------------------------------------ geometry
def _rect(xywh) -> tuple:
    """`label()` takes (x, y, w, h); every judged box here is (x0,y0,x1,y1)."""
    x, y, w, h = xywh
    return (x, y, x + w, y + h)


def _part_rect() -> tuple:
    """The part on the bed: `part_paths` rows in authoring units, mapped
    through MACH1's own placement, plus the stroke's half width."""
    rows = ((155, 215, 182), (155, 215, 172), (163, 207, 162),
            (163, 207, 152), (171, 199, 142))
    left, top, k = SC.MACH1
    half = (9.6 - 2.0) / 2.0
    x0 = left + k * min(r[0] for r in rows) - half
    x1 = left + k * max(r[1] for r in rows) + half
    y0 = top + k * min(r[2] for r in rows) - half
    y1 = top + k * max(r[2] for r in rows) + half
    return (round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1))


# Every box this page judges, in CORE px, normalised HERE off the module's own
# numbers, so a change inside the scene cannot silently pass.  These are INK
# rectangles; `geometry_audit --strict` is the independent measurement on the
# rendered DOM (where the machine and toolbox wrappers are their full authoring
# boxes and the module's `data-block` / `data-overlap-ok` carry the exemptions).
RECTS: dict[str, tuple] = {
    "machine-hook": SC.MACH0_BOX,
    "key-prime-agent": _rect(SC.KEY_TERM_BOX),
    "toolbox": SC.TOOLBOX_BOX,
    "key-regular-agents": _rect(SC.KEY_REG_BOX),
    "machine-main": SC.MACH1_BOX,
    "key-one-tool": _rect(SC.KEY_ONE_BOX),
    "bed-part": _part_rect(),
    "toolpair": SC.PAIR_BOX,
    "machine-out": SC.MACH2_BOX,
    "rlm-slab": SC.SLAB_BOX,
    "key-rlm": _rect(SC.KEY_RLM_BOX),
    "vs-rule": (SC.RULE_X0, SC.RULE_Y, SC.RULE_X1, SC.RULE_Y + SC.RULE_H),
}
for _k, _x in zip(SC.MARK_KEYS, SC.TILE_X):
    RECTS[f"tile-{_k}"] = (_x, SC.TILE_Y, _x + SC.TILE, SC.TILE_Y + SC.TILE)


def canvas(box):
    """core px -> the canvas this page actually paints (top 192, k 1.00)."""
    return (CORE_K * box[0] + LEFT, CORE_TOP_SPLIT + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP_SPLIT + CORE_K * box[3])


def lifetime(name: str) -> tuple:
    """SC.LIFETIMES with THIS lane's one repaired arrival applied."""
    t0, t1 = SC.LIFETIMES[name]
    if name == "key-one-tool":
        t0 = KEYONE_REPAIRED
    return (t0, t1)


# --------------------------------------------------------------- label plan
# LAW 39 / LAW 50 / LAW 9: FOUR written keys, each centred on its host's own ink
# axis, each welded to its host in `SC.DECLARED_BLOCKS` and stamped
# `data-label-for` by the module itself.
LABEL_PLAN = {
    "key-prime-agent": ("machine-hook", "above", SC.KEY_TERM),
    "key-regular-agents": ("toolbox", "above", "REGULAR AGENTS"),
    "key-one-tool": ("machine-main", "above", "ONE SINGLE TOOL"),
    "key-rlm": ("rlm-slab", "below", "RLM"),
}
LABEL_AT = {
    "key-prime-agent": SC.CUE["keyterm"],
    "key-regular-agents": SC.CUE["keyreg"],
    "key-one-tool": KEYONE_REPAIRED,
    "key-rlm": SC.CUE["keyrlm"],
}
HOST_AT = {"machine-hook": SC.CUE["machine0"], "toolbox": SC.CUE["rack"],
           "machine-main": SC.CUE["machine1"], "rlm-slab": SC.CUE["slab"]}
# what the PILLS must never repeat while it is on the board (LAW 4).
PRINTED_KEYS = {k: v[2] for k, v in LABEL_PLAN.items()}
PRINTED_LIFETIME = {k: lifetime(k) for k in PRINTED_KEYS}

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.  A re-cut
# would slide every gesture in the video and no geometry gate would notice.
#   (tight word index, spoken text, which edge the cue must EQUAL)
CUE_WORDS = {
    "keyterm": (5, "type", "start"),
    "clear0": (9, "regular", "start"),
    "keyreg": (11, "agents", "start"),
    "tool1": (14, "list", "start"),
    "tool2": (16, "tools", "start"),
    "lift1": (19, "decide", "start"),
    "lift2": (26, "read", "start"),
    "lift3": (30, "write", "start"),
    "machine1": (34, "now,", "start"),
    "keyone": (46, "one", "start"),
    "part": (54, "build", "start"),
    "emph": (68, "workshop,", "start"),
    "hammer": (81, "hammer", "start"),
    "screw": (84, "screwdriver", "start"),
    "machine_out2": (94, "now,", "start"),
    "slab": (101, "built", "start"),
    "keyrlm": (110, "rlm,", "start"),
    "tiles": (123, "against", "start"),
    "rule": (124, "regular", "start"),
    "emph2": (124, "regular", "start"),
    "outro": (142, "now", "start"),
}
# AUTHORED instants: each must sit inside its own word's 1.0 s LABEL_WINDOW
CUE_INSIDE = {
    "machine0": (0, "prime"),
    "rack": (9, "regular"),
    "tool3": (18, "they"),
    "lift3b": (31, "code,"),
    "clear1": (33, "example."),
    "emphout": (69, "and"),
    "clear2a": (76, "able"),
    "clear2": (93, "settle."),
    "emph2out": (126, "agents,"),
    "clear3": (141, "forward."),
    "chip": (144, "for"),
}
CUE_FREE: tuple[str, ...] = ()

# THE CUES THE EMITTED PAGE NEVER USES.  `tool3` is in the module's table but
# `build()` never fires it: the toolbox carries TWO tools (the wrench and the
# saw), not three, after the pegboard rack was rebuilt.  It is still verified
# against the transcript above so nothing silently rots.
CUE_UNUSED = ("tool3",)

# ----------------------------------------------------- emphasis declarations
# LAW 38.  BOTH targets are DRAWN objects and neither emphasis is an ELEMENT:
# each is the target's OWN outline/border flipping ink -> terracotta.  Nothing
# can carry `data-emphasis`, so nothing is stamped (see the module docstring).
#   target -> (kind, the DOM primitive, cue, release cue, settle)
BORDER_FLIPS = {
    "machine-main": ("box", "#machine-main .mkf1 stroke: the gantry's own "
                     "outline, ink -> terracotta over 0.38 s and back",
                     "emph", "emphout", 0.38),
    "tile-claude-code": ("box", "#tile-claude-code borderColor: the tile's own "
                         "3 px border, ink-alpha -> terracotta",
                         "emph2", "emph2out", 0.38),
    "tile-codex": ("box", "#tile-codex borderColor: the tile's own 3 px "
                   "border, ink-alpha -> terracotta",
                   "emph2", "emph2out", 0.38),
    "tile-cursor": ("box", "#tile-cursor borderColor: the tile's own 3 px "
                    "border, ink-alpha -> terracotta",
                    "emph2", "emph2out", 0.38),
}
EMPHASIS_CHECK: dict[str, tuple] = {}     # nothing to stamp


# ------------------------------------------------------------------ transcript
def words() -> list[dict]:
    d = json.loads((CUT / "transcript_tight.json").read_text())
    return [w for w in d["words"] if w.get("type") == "word"]


def clean_tokens(ws: list[dict]) -> tuple[list[dict], dict]:
    """LAW 6 / LAW 46 / LAW 47, all measured on the TIGHT transcript."""
    partial = [(i, w) for i, w in enumerate(ws)
               if w["text"].strip().endswith(("-", "...", "…"))]
    if partial:
        raise SystemExit(f"unexpected partial words in the take: "
                         f"{[w['text'] for _, w in partial]}")
    head = " ".join(w["text"] for w in ws[:8]).lower()
    if not head.startswith("prime agent is a new type of"):
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[8:]).lower()
    if "prime agent is a new type of" in later:
        raise SystemExit("LAW 46: the opening repeats inside the take")
    tail = DUR - float(ws[-1]["end"])
    cap = 0.20 + 1.0 / FPS
    if tail > 0.30:
        raise SystemExit(f"LAW 47: the master runs {tail:.3f}s past the last word")

    edl = json.loads((CUT / "edl.json").read_text())
    td = edl["take_detection"]
    marker = td["cross_check_marker_rule"]
    gap = td["cross_check_transcript_gap_rule"]
    rep = {"partials_dropped": [], "token_merges": [],
           "law47_tail_s": round(tail, 3), "law47_cap_s": round(cap, 3),
           "law47_overshoot_s": round(max(0.0, tail - cap), 3),
           "law47_verdict": (f"PASS - the master runs {tail:.3f}s past the last "
                             f"word against a {cap:.3f}s cap"
                             if tail <= cap else
                             f"REPORTED - {tail:.3f}s against a {cap:.3f}s cap"),
           "law46": ('the scripted opening "Prime Agent is a new type of AI '
                     'agent" occurs ONCE inside the keeper take, at word 0 / '
                     "0.10 s; the raw carries ten openings and the cut keeps "
                     "the last one that reaches the sign-off"),
           "take_corroboration": {
               "source": "cuts/primeagent/edl.json -> take_detection",
               "method": td["method"],
               "raw_word_index": td["take_word_index"],
               "raw_start_s": td["take_start_s"],
               "words": td["take_words"], "of_raw_words": td["raw_words"],
               "openings": len(td["openings_found"]),
               "sign_offs_found": td["sign_offs_found"],
               "marker_rule": marker["verdict"],
               "marker_answer": marker["answer"],
               "markers_before_take": marker["markers_before_take"],
               "marker_note": marker["note"],
               "gap_rule": gap["verdict"],
               "gap_correct_thresholds": gap["correct_thresholds"],
               "corroboration": td["corroboration"],
               "silence_before_take_s":
                   td["head_measurement"]["silence_before_take_s"]},
           "words": len(ws)}
    if marker["verdict"] not in ("equality", "bound"):
        raise SystemExit(f"the keeper take's marker cross-check is "
                         f"{marker['verdict']!r}")
    if marker["verdict"] == "bound" and marker["answer"] > td["take_word_index"]:
        raise SystemExit("the marker BOUND answers past the keeper take")
    if not td["corroboration"]["witnessed"]:
        raise SystemExit("the keeper take is uncorroborated")
    return list(ws), rep


def assert_cues(ws: list[dict]) -> dict:
    """THE CUE TABLE IS RE-READ, NOT TRUSTED."""
    rep: dict = {}
    for name, (idx, text, edge) in CUE_WORDS.items():
        if idx >= len(ws):
            raise SystemExit(f"cue {name}: word {idx} is past the take")
        w = ws[idx]
        if w["text"].strip().lower() != text:
            raise SystemExit(f"cue {name}: word {idx} is {w['text']!r}, not "
                             f"{text!r} - the cut moved, re-derive the scene")
        want = SC.CUE[name]
        got = round(float(w[edge]), 3)
        if abs(got - want) > 0.011:
            raise SystemExit(f"cue {name}: the scene fires at {want}, the "
                             f"word's {edge} is {got}")
        rep[name] = {"word_spoken": idx, "text": w["text"], "edge": edge,
                     "t": want, "word_edge": got}
    for name, (idx, text) in CUE_INSIDE.items():
        w = ws[idx]
        if w["text"].strip().lower() != text:
            raise SystemExit(f"cue {name}: word {idx} is {w['text']!r}, not "
                             f"{text!r}")
        t = SC.CUE[name]
        lo, hi = float(w["start"]), float(w["end"]) + LABEL_WINDOW
        if not (lo <= t <= hi):
            raise SystemExit(f"cue {name} at {t} is outside the 1.0 s "
                             f"LABEL_WINDOW of {w['text']!r} ({lo:.3f}-{hi:.3f})")
        rep[name] = {"word_spoken": idx, "text": w["text"], "edge": "inside",
                     "t": t, "window": [round(lo, 3), round(hi, 3)]}

    free: dict = {}
    free["law24_repair"] = {
        "mark": "key-one-tool", "module_fires_at": SC.CUE["keyone"],
        "this_page_fires_at": KEYONE_REPAIRED,
        "word": ws[48]["text"],
        "word_window": [float(ws[48]["start"]),
                        round(float(ws[48]["end"]) + LABEL_WINDOW, 3)],
        "why": "LAW 24 - at 11.62 only 'one' has been spoken; 'single' lands "
               "at 11.98 and 'tool.' at 12.32, so two thirds of ONE SINGLE "
               "TOOL would be on screen before the words that license it.  "
               "12.32 is the start of 'tool.', the first instant the whole key "
               "is behind its words, and it is inside that word's own 1.0 s "
               "LABEL_WINDOW.  The repair is made on the EMITTED tween string; "
               "the module on disk is untouched."}
    free["cues_declared_unused"] = {
        "cues": {n: SC.CUE[n] for n in CUE_UNUSED},
        "why": "`tool3` survives in the module's table from the pegboard draft; "
               "`build()` fires only tool1 and tool2 because the rebuilt "
               "toolbox carries TWO tools.  It is verified against the "
               "transcript so the table cannot silently rot, and it emits "
               "nothing."}

    # LAW 43 / LAW 45: the board is CHAPTERED and each erase HANDS OVER.
    FADE = 0.22
    seams = []
    for ch in SC.BOARD_CHAPTERS:
        t = ch["erase_at"]
        end_word = max(float(w["end"]) for w in ws if float(w["end"]) <= t)
        born = sorted(((lifetime(n)[0], n) for n in SC.LIFETIMES
                       if lifetime(n)[0] >= t), key=lambda p: p[0])
        if not born:
            raise SystemExit(f"LAW 45: the seam at {t} hands over to nothing")
        first_at, first = born[0]
        lag = first_at - (t + FADE)
        if lag > 0.30 + 1e-9:
            raise SystemExit(f"LAW 45: the seam at {t} completes at "
                             f"{t + FADE:.2f} and the next object ({first}) "
                             f"only arrives at {first_at}")
        if t < end_word - 1e-9:
            raise SystemExit(f"LAW 45: the seam at {t} cuts a spoken word "
                             f"(ending {end_word})")
        seams.append({"erase_at": t, "last_word_ends": round(end_word, 3),
                      "fade_s": FADE, "erase_completes": round(t + FADE, 2),
                      "hands_over_to": first, "incoming_arrives_at": first_at,
                      "lag_after_erase_s": round(max(0.0, lag), 3)})
    free["law45"] = {"board_mode": SC.BOARD_MODE, "erases": len(seams),
                     "seams": seams,
                     "verdict": "PASS - every one of the five seams lands on "
                                "the first word of the next idea ('Regular', "
                                "'Now,', 'hammer', 'Now,', 'Now') and every "
                                "one hands over to the object that sentence is "
                                "about while the outgoing ink is still fading, "
                                "so the zone never goes empty."}
    arrivals = [SC.CUE[n] for n in
                ("machine0", "keyterm", "rack", "keyreg", "tool1", "tool2",
                 "machine1", "part", "hammer", "screw", "machine_out2",
                 "slab", "keyrlm", "tiles", "rule")] + [KEYONE_REPAIRED]
    last_board_arrival = max(arrivals) + 0.30
    if last_board_arrival >= SC.CUE["outro"]:
        raise SystemExit(f"board ink still arriving at {last_board_arrival}, "
                         f"not clear of the outro anchor {SC.CUE['outro']}")
    free["outro"] = {"t": SC.CUE["outro"],
                     "last_board_arrival_completes": round(last_board_arrival, 2),
                     "clear_s": round(SC.CUE["outro"] - last_board_arrival, 2),
                     "sheet": {"d": SC.SHEET_D, "lockup_in": SC.CHIP_IN,
                               "kind": "OPAQUE RISING SHEET, never a fade and "
                                       "never a scrim"},
                     "note": "the chapter-4 erase at 38.60 deliberately "
                             "overlaps the sheet rising at 38.78: the sheet IS "
                             "the handover and is itself opaque ink."}
    missing = set(SC.CUE) - set(rep) - set(CUE_FREE)
    if missing:
        raise SystemExit(f"cues the build never verified: {sorted(missing)}")
    rep["_free"] = free
    return rep


def assert_word_sync(ws: list[dict]) -> dict:
    """WORD-SYNC.  Every typed key on this board is a STATE that changes on the
    page, so each one's FIRST visible state must agree with the word it lands
    on.  No number is typed and nothing counts in this video: the four written
    keys are the whole typed population."""
    rows = []
    pairs = {
        "key-prime-agent": (5, "type",
                            "PRIME AGENT lands on the spoken 'type' of 'a new "
                            "type of AI agent'; BOTH of its own words were "
                            "already spoken - 'Prime' at 0.10 and 'Agent' at "
                            "0.44, complete by 0.70 - so nothing peeks ahead "
                            "(LAW 24)"),
        "key-regular-agents": (11, "agents",
                               "REGULAR AGENTS lands on the spoken 'agents' of "
                               "'Regular AI agents'; 'Regular' was spoken at "
                               "2.36, so the whole key is behind its words"),
        "key-one-tool": (48, "tool.",
                         "ONE SINGLE TOOL lands on the spoken 'tool.' of 'one "
                         "single tool.'; 'one' was spoken at 11.62 and "
                         "'single' at 11.98, so the whole key is behind its "
                         "words.  THIS IS THE LAW 24 REPAIR - the module fires "
                         "at 11.62, this page at 12.32"),
        "key-rlm": (110, "rlm,",
                    "RLM lands on the spoken 'RLM,' (29.40-30.00), the only "
                    "written key in its chapter"),
    }
    for key, (idx, text, why) in pairs.items():
        w = ws[idx]
        if w["text"].strip().lower() != text:
            raise SystemExit(f"word-sync: {key} expects {text!r} at word {idx}, "
                             f"the take says {w['text']!r}")
        t = LABEL_AT[key]
        lo, hi = float(w["start"]), float(w["end"]) + LABEL_WINDOW
        if not (lo <= t <= hi):
            raise SystemExit(f"word-sync: {key} first shows at {t}, outside the "
                             f"window of {w['text']!r} ({lo:.3f}-{hi:.3f})")
        rows.append({"state": key, "first_visible_text": PRINTED_KEYS[key],
                     "at": t, "word": w["text"],
                     "word_window": [round(lo, 3), round(hi, 3)],
                     "agrees": True, "why": why})
    return {"states_checked": len(rows), "disagreements": 0, "states": rows,
            "digits_that_tick": 0,
            "note": "no number is typed on this board and nothing counts up.  "
                    "The other state changes are the two border flips, the "
                    "three tool lifts and the part growing on the bed, and "
                    "each is cut on the word the cue table verifies."}


def assert_law37(ws: list[dict]) -> dict:
    """LAW 37 - ZERO pointing cues in this take, so nothing to answer."""
    cues = PCUE.scan(ws)
    plan = json.loads(PLAN.read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / "prep/stages/primeagent.cues.json").read_text())
    if marker["keys"]["cue_count"] != len(cues):
        raise SystemExit("LAW 37: the prep marker disagrees with the re-run")
    if cues or declared:
        raise SystemExit(f"LAW 37: {len(cues)} cues found, the plan declares "
                         f"{len(declared)} - this take was planned with none")
    return {"scan_cue_count": 0, "plan_declared_cards": 0,
            "prep_marker": "prep/stages/primeagent.cues.json -> cue_count 0",
            "source_post_cards": 0, "platform_frames_chosen": 0,
            "verdict": "GLOBAL LAW 3 is satisfied BY ABSENCE.  The recording "
                       "names no platform, no post and no person, so this lane "
                       "invents no source card and no platform frame.",
            "instrument": "pointing_cues.scan re-run on transcript_tight.json"}


# ------------------------------------------------------------------ geometry
GUTTER_REFUSE = 16.0        # LAW 41's refusal line, design px
GUTTER_AIM = 24.0           # the number the plan aims for and the clerk reads


def assert_anchor_law() -> dict:
    """LAW 40 - there is NO connector in this scene, so the law has nothing to
    bind.  Stated as a measurement rather than as a silence."""
    return {"connectors": {}, "connectors_in_dom": 0, "arrowheads": 0,
            "line_svg_called_by_build": False,
            "law40_letter": "LAW 40 binds connectors that EXIST and does not "
                            "require any.  The plan's first cut ran two "
                            "terracotta lines from the machine to the two "
                            "finished tools; the crossed pair then took the "
                            "WHOLE board (handoff section 9 item 3), which "
                            "leaves no machine on screen for a line to leave, "
                            "and a connector to nothing is worse than none.  "
                            "Every remaining relationship here is CONTAINMENT "
                            "- the tools in the box, the part on the bed, the "
                            "machine on the slab - and containment is carried "
                            "by the declared blocks (LAW 41).  "
                            "`SC.anchor_points` stays in the module so a lane "
                            "that later adds a connector cannot hand-place its "
                            "end."}


def assert_emphasis_law() -> dict:
    """LAW 38, read off the TWO emphases rather than off a preference.

    Rule 2 (a drawn object) takes BOXING, and in the GRAPHIC CHART's DOM lane
    boxing a drawn object is the object's OWN outline or border flipping to
    terracotta: it adds no geometry, so it opens no new gutter.  Rule 1's
    marker highlight has nothing to highlight - this video prints no
    raster-borne type at all.  Rule 3: no ring, no ellipse, no circle.
    """
    flips = []
    for target, (kind, prim, cue, out, dur) in BORDER_FLIPS.items():
        t0, t1 = lifetime(target)
        t1 = DUR if t1 is None else t1
        at = SC.CUE[cue]
        rel = SC.CUE[out]
        if not (t0 <= at <= t1 and t0 <= rel <= t1):
            raise SystemExit(f"LAW 38: the flip on {target} fires at {at} and "
                             f"releases at {rel}, outside its life {t0}..{t1}")
        if rel < at + dur:
            raise SystemExit(f"LAW 38: {target}'s flip releases at {rel} "
                             f"before it has settled ({at + dur:.2f})")
        flips.append({"target": target, "kind": kind, "fires_at": at,
                      "settles_at": round(at + dur, 2), "releases_at": rel,
                      "held_s": round(rel - (at + dur), 2),
                      "ink": SC.TERRA_L, "rest_ink": SC.INK,
                      "separate_element": False, "dom_primitive": prim,
                      "target_life": [t0, t1]})
    return {"groups": [], "border_flips": flips,
            "rings_ellipses_circles": 0, "highlights": 0,
            "separate_emphasis_elements": 0, "data_emphasis_stamped": 0,
            "emphasis_events": 2,
            "why": "LAW 38 rule 1 gives TEXT IN A RASTER the marker highlight, "
                   "and this video prints NO raster-borne type at all - no "
                   "post, no screenshot, no UI capture, and pointing_cues "
                   "returned nothing.  So both emphases fall under rule 2 (a "
                   "DRAWN target takes boxing), and in both the box IS the "
                   "target's own outline: the machine's gantry strokes at "
                   "17.62 ('workshop') and the three tile borders together at "
                   "33.28 ('regular').  NO ELEMENT IS ADDED, so there is "
                   "nothing to carry `data-emphasis`, and pointing a target at "
                   "itself would make visual_laws compare an element's ink "
                   "with itself - the geminigems_split reading, one recording "
                   "earlier in this run.  Rule 3: the module emits no "
                   "`<circle>` tag anywhere; the filament spool's disc and hub "
                   "are two-arc `<path>`s."}


def assert_label_law() -> dict:
    """LAW 39 / LAW 50 / LAW 9 - the SPACE half off the boxes, the TIME half
    off the cues."""
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    out: dict = {}
    for key, (host, side, text) in LABEL_PLAN.items():
        kb, hb = RECTS[key], RECTS[host]
        if side == "above" and kb[3] > hb[1] + 0.01:
            raise SystemExit(f"LAW 39: {key} (bottom {kb[3]}) is not entirely "
                             f"above {host} (top {hb[1]})")
        if side == "below" and kb[1] < hb[3] - 0.01:
            raise SystemExit(f"LAW 39: {key} (top {kb[1]}) is not entirely "
                             f"below {host} (bottom {hb[3]})")
        kc, hc = (kb[0] + kb[2]) / 2, (hb[0] + hb[2]) / 2
        band = 0.15 * (hb[2] - hb[0])
        if abs(kc - hc) > band:
            raise SystemExit(f"LAW 39: {key} centre {kc} is outside {host}'s "
                             f"+-15% band ({hc} +- {band})")
        if not any(key in b and host in b for b in blocks):
            raise SystemExit(f"LAW 41: {key} is not blocked with {host}")
        t_key = LABEL_AT[key]
        t_host = HOST_AT[host]
        if t_key < t_host - 1e-9:
            raise SystemExit(f"LAW 39: {key} lands at {t_key} before its host "
                             f"{host} at {t_host}")
        gap = (hb[1] - kb[3]) if side == "above" else (kb[1] - hb[3])
        out[key] = {"host": host, "side": side, "text": text,
                    "key_box_core": list(kb), "host_box_core": list(hb),
                    "key_box_canvas": [round(v, 1) for v in canvas(kb)],
                    "centre_error_px": round(kc - hc, 3),
                    "band_px": round(band, 2), "gap_px": round(gap, 2),
                    "at": t_key, "host_at": t_host,
                    "delay_after_host_s": round(t_key - t_host, 3)}

    # LAW 50: no two written keys are ever co-alive here (each lives inside its
    # own chapter), so the law's sibling clause has no pair to bind.  The three
    # keys of chapters 0, 1 and 2 nevertheless all sit the SAME way - above
    # their object - which is the reading the handoff records.
    co_alive = []
    for a in LABEL_PLAN:
        for b in LABEL_PLAN:
            if a >= b:
                continue
            a0, a1 = lifetime(a)
            b0, b1 = lifetime(b)
            a1 = DUR if a1 is None else a1
            b1 = DUR if b1 is None else b1
            if a0 < b1 and b0 < a1:
                co_alive.append(sorted((a, b)))
    above = [k for k, v in LABEL_PLAN.items() if v[1] == "above"]
    out["_law50"] = {"co_alive_key_pairs": co_alive,
                     "keys_above": above, "keys_below": ["key-rlm"],
                     "verdict": "PASS - no two written keys share the board at "
                                "any instant, so LAW 50's sibling clause has "
                                "no pair to bind.  The three keys of chapters "
                                "0, 1 and 2 still sit the same way (ABOVE "
                                "their object); RLM is alone in its chapter "
                                "and sits BELOW its slab, where the slab's own "
                                "meaning - the thing underneath - puts it."}

    # LAW 9: the key term is the FIRST type in the video and it is ALONE.
    first = min(LABEL_AT.values())
    if abs(first - SC.CUE["keyterm"]) > 1e-9:
        raise SystemExit("LAW 9: the key term is not the first type on screen")
    second = sorted(LABEL_AT.values())[1]
    if second <= SC.CUE["keyterm"]:
        raise SystemExit("LAW 9: the key term is not ALONE when it lands")
    du = SC.KEY_TERM_FS / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} design units")
    if SC.KEY_TERM_FS <= SC.KEY_FS:
        raise SystemExit("LAW 9: the key term is not the largest KEY")
    kb = RECTS["key-prime-agent"]
    if abs((kb[0] + kb[2]) / 2 - SC.AXIS) > 0.01:
        raise SystemExit("LAW 9/39: the key term does not debut on the axis")
    out["_key_term"] = {
        "text": SC.KEY_TERM, "at": SC.CUE["keyterm"],
        "font_px": SC.KEY_TERM_FS, "design_units": round(du, 2),
        "other_key_font_px": SC.KEY_FS,
        "seat_canvas": [round(v, 1) for v in canvas(kb)],
        "debut_axis": "x = 540, the composition's own axis to 0.0 px.  It is "
                      "the FIRST type in the video and there is no mark on the "
                      f"board before it, so it is alone for {second - first:.2f} s.",
        "first_type_at": first, "alone_until": second,
        "type_order": sorted(LABEL_AT.items(), key=lambda kv: kv[1])}

    # LAW 19 / LAW 20: the hook object arrives ALONE, CENTRED and COMPLETE.
    hb = RECTS["machine-hook"]
    hook_axis = (hb[0] + hb[2]) / 2
    if abs(hook_axis - SC.AXIS) > 2.5:
        raise SystemExit(f"LAW 19: the hook opens off the axis ({hook_axis})")
    out["_hook"] = {"object": "the tool printing machine - the video's claim "
                              "(one tool whose output is other tools) as ONE "
                              "everyday object, drawn COMPLETE from its first "
                              "settled frame: frame, spool, rail, nozzle, bed "
                              "AND a part already on that bed, so LAW 20's "
                              "vessel corollary is satisfied by construction",
                    "first_ink_at": SC.CUE["machine0"],
                    "opens_centred_on_x": round(hook_axis, 2),
                    "alone_until": SC.CUE["keyterm"],
                    "one_displacement": "none - the machine never moves.  The "
                                        "scale-in of its arrival is an "
                                        "entrance, not a move (LAW 1 / LAW 25)."}
    return out


def assert_lifetime_law() -> dict:
    """LAW 42 on a CHAPTERED board."""
    plan = json.loads(PLAN.read_text())
    anchors, leaves = [], []
    for n in SC.LIFETIMES:
        if n.startswith("o-"):
            continue
        (anchors if lifetime(n)[1] is None else leaves).append(n)
    if anchors:
        raise SystemExit(f"LAW 42: {sorted(anchors)} never leave the board")
    for n in SC.SCENE_ANCHORS:
        if n.startswith("o-"):
            if SC.LIFETIMES[n][1] is not None:
                raise SystemExit(f"LAW 42: {n} is an outro anchor but dies")
    seams = {c["erase_at"] for c in SC.BOARD_CHAPTERS}
    for n in leaves:
        t1 = lifetime(n)[1]
        if t1 not in seams:
            raise SystemExit(f"LAW 42: {n} leaves at {t1}, not at a chapter "
                             f"seam {sorted(seams)}")
    shares = {n: round(((DUR if lifetime(n)[1] is None else lifetime(n)[1])
                        - lifetime(n)[0]) / DUR, 3)
              for n in SC.LIFETIMES if not n.startswith("o-")}
    worst = max((v, k) for k, v in shares.items())
    machine_share = round(sum(
        lifetime(n)[1] - lifetime(n)[0]
        for n in ("machine-hook", "machine-main", "machine-out")) / DUR, 3)
    over40 = [k for k, v in shares.items() if v > 0.40]
    return {"board_mode": SC.BOARD_MODE, "chapters": len(SC.BOARD_CHAPTERS),
            "anchors": list(SC.SCENE_ANCHORS),
            "marks_that_leave": sorted(leaves), "shares": shares,
            "longest_lived_mark": {"mark": worst[1], "share": worst[0]},
            "machine_share_across_its_three_instances": machine_share,
            "plan_boards_mode": plan["boards"]["mode"],
            "board_mode_reason": plan["boards"]["why"],
            "over_40pct_without_declaration": over40,
            "note": "every board mark carries a finite t_to, which is exactly "
                    "the declaration LAW 42 asks a CHAPTERED build for, and "
                    "every one of those t_to values IS a chapter seam.  No "
                    "single element holds more than 30.5% of the runtime; the "
                    "MACHINE as an object holds 64.9% across its three "
                    "instances, which is why all three also carry "
                    "`data-anchor=\"1\"` and are named in SC.SCENE_ANCHORS.  "
                    "The only marks that never leave are the four outro ones."}


def assert_spacing_law() -> dict:
    """LAW 41, measured on the CO-ALIVE pairs of this build's own INK rects."""
    series = [{f"tile-{k}" for k in SC.MARK_KEYS}]
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    # the part sits ON the bed and the pair's two tools cross each other: both
    # carry `data-overlap-ok` in the module and both are composition, not a
    # gutter.  `vs-rule` is a 7 px thin bar, which geometry_audit excludes from
    # its gutter body for the same reason.
    overlap_ok = {"bed-part", "toolpair", "vs-rule"}

    def alive(n, t):
        t0, t1 = lifetime(n)
        return t0 <= t and (t1 is None or t < t1)

    names = [n for n in RECTS if n in SC.LIFETIMES]
    pairs, judged, worst = 0, 0, (1e9, None)
    under_aim = []
    ts = [round(0.25 * i, 2) for i in range(int(DUR / 0.25) + 1)]
    for t in ts:
        if t >= SC.CUE["outro"]:
            break
        live = [n for n in names if alive(n, t)]
        for i in range(len(live)):
            for j in range(i + 1, len(live)):
                a, b = live[i], live[j]
                pairs += 1
                if a in overlap_ok or b in overlap_ok:
                    continue
                if any({a, b} <= s for s in series):
                    continue
                if any({a, b} <= s for s in blocks):
                    continue
                ax0, ay0, ax1, ay1 = RECTS[a]
                bx0, by0, bx1, by1 = RECTS[b]
                dx = max(bx0 - ax1, ax0 - bx1, 0.0)
                dy = max(by0 - ay1, ay0 - by1, 0.0)
                if dx <= 0.0 and dy <= 0.0:
                    raise SystemExit(f"LAW 41: {a} and {b} overlap at t={t} "
                                     "with no declared exemption")
                g = (dx * dx + dy * dy) ** 0.5
                judged += 1
                if g < worst[0]:
                    worst = (g, (a, b, t))
                if g < GUTTER_AIM:
                    under_aim.append({"pair": [a, b], "t": t,
                                      "gutter_px": round(g, 2)})
    if worst[1] is not None and worst[0] < GUTTER_REFUSE:
        raise SystemExit(f"LAW 41: the tightest judged pair {worst[1]} is "
                         f"{worst[0]:.2f} px, under the {GUTTER_REFUSE} line")
    return {"pairs_measured": pairs, "judged": judged,
            "tightest_core_px": None if worst[1] is None else round(worst[0], 2),
            "tightest_pair": None if worst[1] is None
                             else list(worst[1][:2]) + [worst[1][2]],
            "floor": GUTTER_AIM, "refusal_line": GUTTER_REFUSE,
            "split_scale_k": CORE_K,
            "tightest_on_this_page_px": None if worst[1] is None
                                        else round(worst[0] * CORE_K, 2),
            "under_aim": under_aim,
            "blocks": [list(b) for b in SC.DECLARED_BLOCKS],
            "series": [sorted(s) for s in series],
            "overlap_ok": sorted(overlap_ok),
            "stale_block_declared": ["shelf", "hammer", "screwdriver"],
            "stale_block_note": "SC.DECLARED_BLOCKS still carries a 'shelf' "
                                "block from the draft where the two tools "
                                "stood on a shelf.  No element with that id is "
                                "emitted, so the entry binds nothing; the pair "
                                "that shipped is the ('toolpair','hammer',"
                                "'screwdriver') block beside it.  Logged, not "
                                "edited - the module is the design seat's.",
            "gate_scaling_note": "every non-block gutter here is authored at "
                                 ">= 42 CORE px so the cutout's ~0.95 seat "
                                 "still clears 40 canvas px; this lane's k is "
                                 "1.00, so the core number IS the page number",
            "instrument": "this build's own co-alive sweep at 0.25 s over the "
                          "module's ink rects; geometry_audit --strict is the "
                          "independent measurement on the rendered DOM"}


def assert_cast_law() -> dict:
    """THE CAST RESOLVE, before a frame renders."""
    rep = DF.assert_cast_resolves(list(STAGE_FILES), STAGE_FILES, ASSETS,
                                  label="primeagent stage marks")
    ink = {k: CC.MARK_INK[k] for k in STAGE_FILES if k in CC.MARK_INK}
    if len(ink) != len(STAGE_FILES):
        raise SystemExit("a stage mark was never measured")
    plan = json.loads(PLAN.read_text())
    if list(plan["cast"]) != list(STAGE_FILES):
        raise SystemExit(f"the plan's cast {plan['cast']} is not the scene's "
                         f"{list(STAGE_FILES)}")
    return {"stage_marks": len(STAGE_FILES), "assert_cast_resolves": rep,
            "ink_aspects": {k: round(v["aspect"], 4) for k, v in ink.items()},
            "size_core_px": SC.MARK_SIDE, "tile_px": SC.TILE,
            "cutout_lanes_not_ours": list(CUTOUT_LANES),
            "raster_cards": 0,
            "why": "LAW 2 binds a NAMED product to its own registry logo.  The "
                   "script names no product at all - Prime Agent is the stage "
                   "object, drawn, and it has no mark - so the three marks on "
                   "this board are the TOPICAL field the script does name "
                   "('regular AI agents'): Claude Code, Codex and Cursor, the "
                   "agents this channel actually names, in the chart's own "
                   "112 px tiles (LAW 33: real marks, never generic glyphs; "
                   "LAW 29: no placeholder tiles).  MARK IDENTITY: the FILE is "
                   "claudecode-color.png, the plain no-outline mascot, never "
                   "the die-cut claude-code.png sticker whose white edge would "
                   "halo on cream.  The six cutout lane marks belong to the "
                   "OTHER author."}


def assert_axis_law() -> dict:
    """LAW 15 / LAW 19, measured PER BEAT on the boxes alive at the END of it."""
    rows, empty = [], []
    edges = SC.BEAT_EDGES
    for i, (t0, t1) in enumerate(zip(edges, edges[1:])):
        # the LAST held instant inside the beat that still has board ink.  A
        # beat that ENDS inside a chapter handover (the outgoing chapter
        # released, the incoming object a few frames away) is walked back to
        # its own settled board rather than skipped.
        t = t1 - 0.01
        boxes: dict = {}
        while t > t0:
            boxes = {n: RECTS[n] for n in RECTS
                     if n in SC.LIFETIMES and lifetime(n)[0] <= t
                     and (lifetime(n)[1] is None or t <= lifetime(n)[1])}
            if boxes:
                break
            t = round(t - 0.05, 2)
        if not boxes:
            empty.append({"beat": i, "window": [t0, t1],
                          "why": "this beat holds no board mark at any instant "
                                 "- it is the OUTRO beat, whose marks are the "
                                 "sheet and the lockup and are excluded from "
                                 "this sweep by design."})
            continue
        if t < t1 - 0.02:
            empty.append({"beat": i, "sampled_at": t, "beat_end": t1,
                          "why": "the beat's own end instant falls inside a "
                                 "chapter handover, so the sweep walked back "
                                 "to the last instant the beat's board was "
                                 "settled.  The board is never empty on screen "
                                 "- the outgoing ink is still fading (LAW 45)."})
        left = min(v[0] for v in boxes.values())
        right = max(v[2] for v in boxes.values())
        if left < 40.0 or (SC.CORE_W - right) < 40.0:
            raise SystemExit(f"beat {i} ink runs {left}..{right}, inside the "
                             f"40 px frame margin")
        rows.append({"beat": i, "window": [t0, t1], "at": round(t, 2),
                     "ink_left": left, "ink_right": right,
                     "axis": round((left + right) / 2, 2),
                     "offset_from_540": round((left + right) / 2 - SC.AXIS, 2),
                     "margins": [left, round(SC.CORE_W - right, 1)],
                     "marks": sorted(boxes)})
    worst = max(rows, key=lambda r: abs(r["offset_from_540"]))
    return {"beats": rows, "mode": "REPORTED", "beats_sampled_empty": empty,
            "worst": {"beat": worst["beat"],
                      "offset_px": worst["offset_from_540"]},
            "frame_margin_floor_px": 40.0,
            "note": "the composition is symmetric about x = 540 in EVERY "
                    "chapter by construction: each machine placement is seated "
                    "at left = 540 - 148k, the toolbox at 540 - 160k, the "
                    "crossed pair's two tool centres are +-30 px about 540, "
                    "the slab and the rule are centred, and the tile row is "
                    "320 / 484 / 648 (centre 540).  Every written key is "
                    "centred on 540 too."}


def assert_sfx(sfx) -> dict:
    """No two sounds inside 0.30 s of each other: that is a flam, not a score."""
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30:
        raise SystemExit(f"SFX flam: two sounds {worst[0]:.2f}s apart at "
                         f"{worst[1]} and {worst[2]}")
    silenced = {
        "lift3b@7.840": "the wrench DROPS BACK; a return to rest is the tail "
                        "of the lift that was already struck at 7.32",
        "lift2/lift3 returns": "each lift's drop-back shares its word with the "
                               "NEXT tool's lift, which is the event the ear "
                               "is given - one sound per gesture, not two",
        "emph@17.620 / emphout@18.600 / emph2@33.280 / emph2out@34.600":
            "a border or outline flip is not an arrival; nothing appears and "
            "nothing leaves, so nothing is struck",
        "the four chapter erases": "a chapter erase HANDS OVER rather than "
                                   "clearing; the incoming object on the far "
                                   "side of the seam is what the ear is given",
        "tiles@32.960 / 33.120": "the three agent tiles are ONE arrival with a "
                                 "0.16 s stagger, not three events; the 32.80 "
                                 "pop is the whole gesture",
        "chip@39.260": "the outro lockup rides the sheet's whoosh at 38.78",
    }
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "tightest_pair_s": [worst[1], worst[2]],
            "kinds": {"pop": sum(1 for n, _t, _v in sfx if n == "pop"),
                      "click": sum(1 for n, _t, _v in sfx if n == "click"),
                      "whoosh": sum(1 for n, _t, _v in sfx if n == "whoosh")},
            "rule": "an OBJECT arriving takes a pop at structure gain; a "
                    "written KEY takes a click at detail gain; the machine "
                    "ACTING (a tool standing up, a tool lifting off, the part "
                    "growing on the bed, the rule drawing) takes a click; the "
                    "outro sheet takes a whoosh",
            "deliberately_silent": silenced}


# ------------------------------------------------------------------ captions
def phrases(ws: list[dict]) -> list[list[dict]]:
    out, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w)
        end = w["text"].strip().rstrip('"').endswith((".", "!", "?"))
        gap = (ws[i + 1]["start"] - w["end"]) if i + 1 < len(ws) else 9.0
        if end or gap >= 0.30 or len(cur) >= 20:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def _joined(part) -> str:
    return " ".join(w["text"] for w in part)


def _is_board_key(text: str) -> str | None:
    norm = text.strip().upper().rstrip('.,!?"').lstrip('"')
    for key, t in PRINTED_KEYS.items():
        if norm == t.upper():
            return key
    return None


SOLO_WORD_PENALTY = 250_000.0     # ~ one pill's worth of slack, in px^2


def _repartition(union, max_w, measurer, forbidden):
    n = len(union)
    texts = {}
    for i in range(n):
        for j in range(i + 1, n + 1):
            texts[(i, j)] = _joined(union[i:j])
    measurer.want(sorted(set(texts.values())))
    measurer.resolve()
    INF = (10 ** 9, 0.0)
    best = [INF] * (n + 1)
    back = [-1] * (n + 1)
    best[0] = (0, 0.0)
    for j in range(1, n + 1):
        for i in range(j):
            if best[i] == INF:
                continue
            txt = texts[(i, j)]
            w = measurer.width(txt)
            if w > max_w:
                continue
            if txt.strip().lower() in forbidden:
                continue
            if CAP.is_orphan_beat(txt, w):
                continue
            solo = SOLO_WORD_PENALTY if j - i == 1 else 0.0
            cand = (best[i][0] + 1, best[i][1] + (max_w - w) ** 2 + solo)
            if cand < best[j]:
                best[j] = cand
                back[j] = i
    if best[n] == INF:
        return None
    out, j = [], n
    while j > 0:
        i = back[j]
        out.append(union[i:j])
        j = i
    return list(reversed(out))


def repair_orphan_beats(parts, max_w, measurer, forbidden) -> tuple[list, list]:
    """SS3b's LAST resort, after `merge_function_only_beats` and before
    `assert_no_function_only_beat`."""
    log = []
    i = 0
    guard = 0
    while i < len(parts):
        guard += 1
        if guard > 5000:                                    # pragma: no cover
            raise SystemExit("orphan repair did not converge")
        txt = _joined(parts[i])
        if not CAP.is_orphan_beat(txt, measurer.width(txt)):
            i += 1
            continue
        fixed = None
        for lo, hi in ((max(0, i - 1), min(len(parts), i + 2)),
                       (max(0, i - 1), i + 1), (i, min(len(parts), i + 2))):
            if hi - lo < 2:
                continue
            union = [w for p in parts[lo:hi] for w in p]
            got = _repartition(union, max_w, measurer, forbidden)
            if got is None:
                continue
            fixed = (lo, hi, got)
            break
        if fixed is None:
            raise SystemExit(
                f"SS3b: the orphan beat {txt!r} has no legal repartition")
        lo, hi, got = fixed
        log.append({"orphan": txt,
                    "window": [_joined(p) for p in parts[lo:hi]],
                    "repartitioned_to": [_joined(p) for p in got]})
        parts[lo:hi] = got
        i = lo
    return parts, log


def merge_board_key_beats(parts, max_w, measurer, forbidden) -> tuple[list, list]:
    """LAW 4 / caption_identity_guard, at the CHUNKER rather than at the eye."""
    log = []
    i = 0
    while i < len(parts):
        offending = _joined(parts[i])
        key = _is_board_key(offending)
        if key is None:
            i += 1
            continue
        k0, k1 = PRINTED_LIFETIME[key]
        t0 = float(parts[i][0]["start"])
        t1 = float(parts[i + 1][0]["start"]) if i + 1 < len(parts) \
            else float(parts[i][-1]["end"])
        if not (t0 < (k1 or DUR) and k0 < t1):
            i += 1
            continue
        moved = None
        if i > 0:
            u = parts[i - 1] + parts[i]
            measurer.want([_joined(u)])
            measurer.resolve()
            if measurer.width(_joined(u)) <= max_w:
                parts[i - 1:i + 1] = [u]
                moved = ("backward-merge", [_joined(u)])
                i -= 1
        if moved is None and i + 1 < len(parts):
            u = parts[i] + parts[i + 1]
            measurer.want([_joined(u)])
            measurer.resolve()
            if measurer.width(_joined(u)) <= max_w:
                parts[i:i + 2] = [u]
                moved = ("forward-merge", [_joined(u)])
        if moved is None and i > 0:
            u = parts[i - 1] + parts[i]
            re_split = CAP.split_balanced(u, max_w, measurer,
                                          forbidden=forbidden)
            if any(_is_board_key(_joined(p)) for p in re_split):
                raise SystemExit(f"LAW 4: the pill {_joined(parts[i])!r} "
                                 f"repeats the live board key {key}")
            parts[i - 1:i + 1] = re_split
            moved = ("re-partition", [_joined(p) for p in re_split])
            i -= 1
        if moved is None:
            raise SystemExit(f"LAW 4: the pill {offending!r} repeats the live "
                             f"board key {key} and has no neighbour")
        log.append({"offending_pill": offending, "board_key": key,
                    "key_window": [k0, k1], "action": moved[0],
                    "replaced_by": moved[1]})
        i += 1
    return parts, log


def merge_solo_word_beats(parts, max_w, measurer) -> tuple[list, list]:
    log = []
    i = 0
    while i < len(parts):
        if len(parts[i]) != 1:
            i += 1
            continue
        best = None
        for direction, lo, hi in (("backward", i - 1, i + 1),
                                  ("forward", i, i + 2)):
            if lo < 0 or hi > len(parts):
                continue
            u = [w for p in parts[lo:hi] for w in p]
            txt = _joined(u)
            measurer.want([txt])
            measurer.resolve()
            wpx = measurer.width(txt)
            if wpx > max_w or CAP.is_orphan_beat(txt, wpx):
                continue
            key = _is_board_key(txt)
            if key is not None:
                k0, k1 = PRINTED_LIFETIME[key]
                if float(u[0]["start"]) < (k1 or DUR) and k0 < float(u[-1]["end"]):
                    continue
            best = (direction, lo, hi, [u])
            break
        if best is None:
            i += 1
            continue
        direction, lo, hi, got = best
        log.append({"solo": _joined(parts[i]), "direction": direction,
                    "merged_to": _joined(got[0])})
        parts[lo:hi] = got
        i = max(0, lo)
    return parts, log


def caption_beats(measurer, ws, clean_rep) -> tuple[list[dict], dict]:
    measurer.want(CAP.runs([w["text"] for w in ws]))
    measurer.resolve()
    # SS3b runs over the WHOLE beat stream, never inside one phrase at a time.
    forbidden = {t.lower() + suf for t in PRINTED_KEYS.values()
                 for suf in ("", ".", ",", "!", "?")}
    parts: list[list] = []
    repartitioned = 0
    for group in phrases(ws):
        got = _repartition(group, CAP.SEAT_MAX_W, measurer, forbidden)
        if got is None:
            got = CAP.split_balanced(group, CAP.SEAT_MAX_W, measurer,
                                     forbidden=forbidden)
        else:
            repartitioned += 1
        parts.extend(got)
    before = len(parts)
    parts = CAP.merge_function_only_beats(parts, CAP.SEAT_MAX_W, measurer)
    merged = before - len(parts)
    parts, orphan_log = repair_orphan_beats(parts, CAP.SEAT_MAX_W, measurer,
                                            forbidden)
    parts, key_log = merge_board_key_beats(parts, CAP.SEAT_MAX_W, measurer,
                                           forbidden)
    parts, solo_log = merge_solo_word_beats(parts, CAP.SEAT_MAX_W, measurer)

    beats: list[dict] = []
    for part in parts:
        text = " ".join(w["text"] for w in part)
        beats.append({"text": text, "start": float(part[0]["start"]),
                      "end": float(part[-1]["end"]),
                      "w": measurer.width(text)})
    for i, b in enumerate(beats):                       # gapless
        nxt = beats[i + 1]["start"] if i + 1 < len(beats) else b["end"] + 0.26
        b["dur"] = round(max(0.24, min(nxt, DUR) - b["start"]), 3)
    CAP.assert_no_function_only_beat(beats)
    widest = max(b["w"] for b in beats)
    if widest > CAP.SEAT_MAX_W + 0.6:
        raise SystemExit(f"pill {widest:.1f}px exceeds the {CAP.SEAT_MAX_W} seat")
    echoes = []
    for b in beats:
        norm = b["text"].strip().upper().rstrip('.,!?"').lstrip('"')
        for key, text in PRINTED_KEYS.items():
            if norm != text.upper():
                continue
            k0, k1 = PRINTED_LIFETIME[key]
            if b["start"] < (k1 or DUR) and k0 < b["start"] + b["dur"]:
                raise SystemExit(f"caption echo: the pill {b['text']!r} is "
                                 f"alive while the board key {key} is")
            echoes.append({"pill": b["text"], "key": key,
                           "pill_window": [b["start"],
                                           round(b["start"] + b["dur"], 3)],
                           "key_window": [k0, k1]})
    clean_rep["phrase_groups_repartitioned"] = repartitioned
    clean_rep["function_word_merges"] = merged
    clean_rep["beats_before_merge"] = before
    clean_rep["board_keys_forbidden_at_split"] = sorted(forbidden)
    clean_rep["orphan_repartitions"] = orphan_log
    clean_rep["board_key_echo_repairs"] = key_log
    clean_rep["solo_word_merges"] = solo_log
    clean_rep["caption_echoes_not_overlapping"] = echoes
    return beats, clean_rep


def caption_html(beats, seat_y) -> str:
    """FRAME-QUANTISED, half-open, ONE OWNER PER FRAME."""
    ks = [round(b["start"] * FPS) for b in beats]
    last_k = round(min(beats[-1]["start"] + beats[-1]["dur"], DUR) * FPS)
    out = []
    for i, b in enumerate(beats):
        k0 = ks[i]
        k1 = ks[i + 1] if i + 1 < len(beats) else last_k
        if k1 <= k0 + 1:
            raise SystemExit(
                f"caption beat {i} ({b['text']!r}) is under two frames long "
                f"(k0={k0}, k1={k1}); the chunker put two pills on one frame")
        out.append(
            f'<div id="cap{i}" class="clip scap" style="top:{seat_y}px" '
            f'data-start="{k0 / FPS:.3f}" '
            f'data-duration="{(k1 - k0 - 0.5) / FPS:.4f}" '
            f'data-track-index="25"><span class="scappill">'
            f'{ihtml.escape(b["text"], quote=False)}</span></div>')
    return "\n".join(out)


# ------------------------------------------------------------------ page shell
def head(title: str, w: int, h: int, zoom: int, extra_css: str) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width={int(W)}, height={int(H)}"/>
<title>{ihtml.escape(title)}</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Nunito:wght@800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700;800&display=block" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:{int(W)}px; height:{int(H)}px; overflow:hidden;
  font-family:Poppins,sans-serif; zoom:{zoom}; }}
.clip {{ position:absolute; }} .abs {{ position:absolute; }}
.disp {{ font-family:Poppins,sans-serif; }}
.mono {{ font-family:'JetBrains Mono',monospace; text-transform:uppercase; }}
.core {{ transform-origin:0 0; }}
{CAP.pill_rule()}
{extra_css}
</style></head>
<body><div id="root" data-composition-id="main" data-start="0"
 data-width="{w}" data-height="{h}" data-duration="{DUR}" data-fps="{FPS}">
"""


def tail(tweens: list[str]) -> str:
    body = "".join(tweens)
    return f"""
</div>
<script>
window.__timelines = window.__timelines || {{}};
const SOFT = "power2.out";
const SWING = "power2.inOut";
const POP = "back.out(2.05)";
const none = "none";
// the shared module writes `visibility:hidden` as a BARE token inside its
// chapter-erase set(); the chassis names it, exactly as it names `none`.
const hidden = "hidden";
const tl = gsap.timeline({{paused:true}});
{body}
window.__timelines["main"]=tl;
</script></body></html>
"""


def outro_lockup(handle_key: str) -> str:
    """The scene reserves `#o-slot`; the format seats THIS lockup inside it."""
    return (CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W)
            + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W))


# ------------------------------------------------------------------ probes
def probe_wh(p: Path) -> dict:
    o = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height", "-of", "json", str(p)],
        capture_output=True, text=True, check=True).stdout)["streams"][0]
    return {"w": int(o["width"]), "h": int(o["height"])}


def probe_audio(p: Path) -> dict:
    o = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
         "stream=sample_rate,channels", "-of", "json", str(p)],
        capture_output=True, text=True, check=True).stdout)["streams"][0]
    return {"sample_rate": int(o["sample_rate"]), "channels": int(o["channels"])}


# ------------------------------------------------------------------ staging
def stage(dst: Path, *, face: str) -> dict:
    v = dst / "assets/v"
    v.mkdir(parents=True, exist_ok=True)
    for sub in ("music", "sfx", "logos"):
        (dst / f"assets/{sub}").mkdir(parents=True, exist_ok=True)
    rec: dict = {}

    shutil.copy2(CUT / "audio.m4a", v / "voice.m4a")
    pr = probe_audio(v / "voice.m4a")
    if pr["sample_rate"] < 44100:
        raise SystemExit(f"staged voice is {pr['sample_rate']} Hz")
    rec["voice"] = {"source": str(CUT / "audio.m4a"), **pr}

    shutil.copy2(MUSIC / "bed_split_v2.mp3", dst / "assets/music/bed.mp3")
    for s in ("whoosh", "pop", "click"):
        shutil.copy2(SFXLIB / f"{s}.mp3", dst / f"assets/sfx/{s}.mp3")
    rec["audio_library"] = {"bed": str(MUSIC / "bed_split_v2.mp3"),
                            "sfx_root": str(SFXLIB)}

    shutil.copy2(CUT / face, v / face)
    rec["face"] = {"file": face, **probe_wh(CUT / face)}

    marks = {}
    for key, rel in STAGE_FILES.items():
        src = ASSETS / rel
        if not src.exists():
            raise SystemExit(f"registry key {key!r} does not resolve: {src}")
        shutil.copy2(src, dst / "assets/logos" / src.name)
        CC.MARK_INK[key] = CC.measure_mark(key, src)
        marks[key] = {"source": str(src), "url": LOGO_URL[key],
                      "bytes": src.stat().st_size}
    rec["marks"] = marks
    return rec


def media() -> dict:
    """The THREE rasters the scene paints - the handoff's section 1.  The KEY
    KEEPS ITS HYPHEN: the module reads `media[f"_{k}_img"]` with k straight out
    of SC.MARK_KEYS."""
    return {f"_{k}_img": CC.mark_img(LOGO_URL[k], k, SC.MARK_SIDE)
            for k in SC.MARK_KEYS}


# EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22).
def sfx_plan() -> list[tuple]:
    C = SC.CUE
    return [("pop", C["machine0"], SFX_STRUCTURE),      # THE MACHINE arrives
            ("click", C["keyterm"], SFX_DETAIL),        # PRIME AGENT
            ("pop", C["rack"], SFX_STRUCTURE),          # THE TOOLBOX
            ("click", C["keyreg"], SFX_DETAIL),         # REGULAR AGENTS
            ("click", C["tool1"], SFX_DETAIL),          # the wrench stands up
            ("click", C["tool2"], SFX_DETAIL),          # the saw stands up
            ("click", C["lift1"], SFX_DETAIL),          # a tool is chosen
            ("click", C["lift2"], SFX_DETAIL),          # and another
            ("click", C["lift3"], SFX_DETAIL),          # and another
            ("pop", C["machine1"], SFX_STRUCTURE),      # THE ONE TOOL returns
            ("click", KEYONE_REPAIRED, SFX_DETAIL),     # ONE SINGLE TOOL
            ("click", C["part"], SFX_DETAIL),           # the part grows
            ("pop", C["hammer"], SFX_STRUCTURE),        # THE HAMMER
            ("pop", C["screw"], SFX_STRUCTURE),         # THE SCREWDRIVER
            ("pop", C["machine_out2"], SFX_STRUCTURE),  # the machine, small
            ("pop", C["slab"], SFX_STRUCTURE),          # THE RLM SLAB
            ("click", C["keyrlm"], SFX_DETAIL),         # RLM
            ("pop", C["tiles"], SFX_STRUCTURE),         # THE THREE AGENTS
            ("click", C["rule"], SFX_DETAIL),           # the terracotta rule
            ("whoosh", C["outro"], SFX_STRUCTURE)]      # the rising sheet


def sfx_levels() -> dict:
    out = {}
    for s in ("whoosh", "pop", "click"):
        r = subprocess.run(
            ["ffmpeg", "-v", "info", "-i", str(SFXLIB / f"{s}.mp3"),
             "-af", "volumedetect", "-f", "null", "-"],
            capture_output=True, text=True)
        mean = next((ln.split("mean_volume:")[1].strip()
                     for ln in r.stderr.splitlines() if "mean_volume:" in ln), "?")
        out[s] = {"mean_volume": mean}
    out["_gains"] = {"structure": SFX_STRUCTURE, "detail": SFX_DETAIL,
                     "published_corpus_flat": 0.18,
                     "note": "a gain constant means nothing without its source "
                             "loudness (SFX LAW v2); these are the run-9 to "
                             "run-23 shipped values for THESE files"}
    return out


def audio_html(sfx) -> str:
    rows = [f'<audio id="vo" src="assets/v/voice.m4a" data-start="0" '
            f'data-duration="{DUR}" data-track-index="30" data-volume="1"></audio>',
            f'<audio id="bg0" src="assets/music/bed.mp3" data-start="0" '
            f'data-duration="{DUR}" data-track-index="31" '
            f'data-volume="{BED}"></audio>']
    for i, (name, at, vol) in enumerate(sfx):
        rows.append(f'<audio id="sfx{i}" src="assets/sfx/{name}.mp3" '
                    f'data-start="{at:.2f}" data-duration="0.62" '
                    f'data-track-index="{70 + i}" data-volume="{vol}"></audio>')
    return "\n".join(rows)


# ------------------------------------------------------------------ guards
def guard_core_band(fmt: str, top: float, k: float, cap_seat: float,
                    pill_clear: float = 24.0) -> dict:
    """LAW 30 above, THE SEAM IS SACRED below - the clearance derived with the
    pill that RENDERS (114.59), never the frozen 108.2 seat constant."""
    y0 = top + SC.CONTENT_Y0 * k
    y1 = top + SC.CONTENT_Y1 * k
    pill_top = cap_seat - CAP.CAP_PILL_HEIGHT / 2
    if y0 < 0.10 * H:
        raise SystemExit(f"{fmt}: core content starts at y={y0:.1f}, inside the "
                         f"top 10% ({0.10 * H:.0f}) - LAW 30")
    if y1 > pill_top - pill_clear:
        raise SystemExit(f"{fmt}: core content ends at y={y1:.1f}, within "
                         f"{pill_clear}px of the pill top {pill_top:.1f}")
    return {"content_top": round(y0, 2), "content_bottom": round(y1, 2),
            "law30_line": 0.10 * H, "clear_below_law30": round(y0 - 0.10 * H, 2),
            "pill_top_rendered": round(pill_top, 3),
            "pill_height_rendered": CAP.CAP_PILL_HEIGHT,
            "pill_centre_used": cap_seat,
            "clear_above_pill": round(pill_top - y1, 2),
            "core_top_used": top, "core_top_in_handoff": SC.CANVAS_OFFSET,
            "core_raised_px": round(SC.CANVAS_OFFSET - top, 1),
            "note": "content_top is the core's declared CONTENT_Y0 (ONE SINGLE "
                    "TOOL's box top in chapter 2) and content_bottom its "
                    "CONTENT_Y1 (the crossed pair's lowest ink in chapter 3).  "
                    "NOTHING IS RAISED: this lane seats the core exactly where "
                    "the handoff put it, so the cutout's boxes and this page's "
                    "differ by scale alone."}


def guard_rail(fmt: str) -> dict:
    """LAW 30's RIGHT RAIL, measured rather than assumed."""
    boxes = [canvas(b) for b in RECTS.values()]
    keys = [canvas(RECTS[n]) for n in LABEL_PLAN]
    type_right = max(b[2] for b in keys)
    type_left = min(b[0] for b in keys)
    ink_left = min(b[0] for b in boxes)
    ink_right = max(b[2] for b in boxes)
    if ink_left < 12.0 - 0.01 or (W - ink_right) < 12.0:
        raise SystemExit(f"the composition's boxes run {ink_left:.1f}.."
                         f"{ink_right:.1f}, outside the frame margin")
    if type_right > CAP.LAW12_RAIL_X + 0.01:
        raise SystemExit(f"a readable key reaches x={type_right:.1f}, past the "
                         f"{CAP.LAW12_RAIL_X} rail")
    return {"ink_left_x": round(ink_left, 1), "ink_right_x": round(ink_right, 1),
            "union_axis_x": round((ink_left + ink_right) / 2, 2),
            "readable_type_left_x": round(type_left, 1),
            "readable_type_right_x": round(type_right, 1),
            "law30_rail_x": CAP.LAW12_RAIL_X, "rail_overshoot_px": 0.0,
            "margins": [round(ink_left, 1), round(W - ink_right, 1)],
            "note": "the widest readable key is PRIME AGENT, whose 400 px seat "
                    "stops at x 740, 178 px inside the 918 rail.  The widest "
                    "INK on the board is the crossed pair (310..770), which is "
                    "drawing, not readable type, and the amendment to LAW 30 "
                    "keeps the composition centred and symmetric.  No caption "
                    "pill crosses the rail (CAP.assert_law12 on the widest)."}


# ------------------------------------------------------------- placement
def phone_objects() -> list[dict]:
    """The plan's THREE bespoke objects, mapped into THIS format's frame."""
    out = []
    for o in SC.BESPOKE:
        x0, y0, x1, y1 = canvas(o["core"])
        out.append({
            "name": o["name"], "t": o["t"], "space": "norm",
            "bbox": [round(x0 / W, 5), round(y0 / H, 5),
                     round(x1 / W, 5), round(y1 / H, 5)],
            "canvas": [round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1)],
            "phone_px": [round((x1 - x0) * 405 / W),
                         round((y1 - y0) * 720 / H)],
        })
    return out


PLAN_BBOX_TOLERANCE_PX = 40.0


def compare_phone_boxes(objs: list[dict]) -> dict:
    """The plan's own bbox fields against the DRAWN boxes.  `SC.BESPOKE` is
    authoritative for geometry by the handoff's own sentence; the plan's values
    were refreshed from it, so this is a re-measurement, not a negotiation."""
    plan = json.loads(PLAN.read_text())
    want = plan["bespoke_objects"]
    if len(want) != len(objs):
        raise SystemExit(f"the plan declares {len(want)} bespoke objects, the "
                         f"scene declares {len(objs)}")
    by_name = {o["name"]: o for o in objs}
    rows = []
    for a in want:
        name = a["name"]
        # the plan names object 0 "open toolbox with tools"; the module's
        # BESPOKE list uses the same names, so this is an exact match.
        if name not in by_name:
            raise SystemExit(f"the plan's object {name!r} is not in SC.BESPOKE "
                             f"({sorted(by_name)})")
        b = by_name[name]
        if abs(float(a["t"]) - float(b["t"])) > 1e-9:
            raise SystemExit(f"{name}: plan t {a['t']}, scene t {b['t']}")
        d = [round(abs(x - y) * (W if i % 2 == 0 else H), 2)
             for i, (x, y) in enumerate(zip(a["bbox"], b["bbox"]))]
        rows.append({"plan_name": name, "built_name": b["name"],
                     "plan_t": a["t"], "built_t": b["t"],
                     "plan_bbox": a["bbox"], "built_bbox": b["bbox"],
                     "plan_phone_px": [round((a["bbox"][2] - a["bbox"][0]) * 405),
                                       round((a["bbox"][3] - a["bbox"][1]) * 720)],
                     "built_phone_px": b["phone_px"],
                     "delta_px": d, "max_delta_px": max(d)})
    worst = max(r["max_delta_px"] for r in rows)
    if worst > PLAN_BBOX_TOLERANCE_PX:
        raise SystemExit(f"a bespoke box differs from the plan's by {worst}px")
    return {"objects": rows, "worst_delta_px": worst,
            "source_used_for_the_render_job": "SC.BESPOKE mapped through this "
                                              "format's k and origin",
            "seal": "review/artwork_pass_primeagent.json - verdict PASS, sealed "
                    "by the design seat against the module and handoff hashes.  "
                    "Object 2 ('two crossed tools') was accepted by MIGUEL "
                    "HIMSELF on 2026-09-21; the four earlier reader rounds are "
                    "history and no lane may reopen them."}


def assert_plan_lane() -> dict:
    plan = json.loads(PLAN.read_text())
    return {"lane": plan["lane"], "lane_reason": plan["lane_reason"],
            "beats": len(plan["beats"]),
            "beat_edges_scene": SC.BEAT_EDGES,
            "beat_edges_plan": [plan["beats"][0]["t_start"]]
                               + [b["t_end"] for b in plan["beats"]],
            "open_doubts": plan["open_doubts"]}


# ---------------------------------------------- the format-side DOM repairs
KEYONE_TWEEN_OLD = ('tl.fromTo("#key-one-tool",{opacity:0,y:12},'
                    '{opacity:1,y:0,duration:0.28,ease:SOFT,'
                    'immediateRender:false},11.62);')
KEYONE_TWEEN_NEW = KEYONE_TWEEN_OLD.replace(",11.62);", f",{KEYONE_REPAIRED:.2f});")


def repair_tweens(tweens: list[str]) -> tuple[list[str], dict]:
    """ONE repair, on the EMITTED tween list.  No module byte is moved: the
    cutout author is reading the same file for TikTok and inherits this repair
    through `plans/primeagent_split_notes.md`."""
    hits = [i for i, t in enumerate(tweens) if t == KEYONE_TWEEN_OLD]
    if len(hits) != 1:
        raise SystemExit(f"the module no longer emits #key-one-tool's arrival "
                         f"where this lane measured it ({len(hits)} matches) - "
                         f"re-read it before repairing it")
    tweens = list(tweens)
    tweens[hits[0]] = KEYONE_TWEEN_NEW
    return tweens, {"key_one_tool_arrival": {
        "was": SC.CUE["keyone"], "now": KEYONE_REPAIRED,
        "word_it_now_lands_on": "tool. (12.32-12.48)",
        "why": "LAW 24 NO PEEK-AHEAD.  At 11.62 only 'one' has been spoken; "
               "'single' arrives at 11.98 and 'tool.' at 12.32, so two thirds "
               "of ONE SINGLE TOOL would have been readable before the words "
               "that license it.  12.32 is the first instant the whole key is "
               "behind its words and it is inside that word's own 1.0 s "
               "LABEL_WINDOW, so LAW 39's time half still holds.  The seat, "
               "the ink, the size, the 0.28 s entrance and the 21.50 release "
               "are the module's, untouched."}}


def declare_contracts(html: str) -> tuple[str, dict]:
    """There is nothing for this page to stamp: no connector exists and neither
    emphasis is an element.  Stated as a measurement, not as a silence."""
    if "data-connect-to" in html:
        raise SystemExit("the emitted scene carries a connector this lane "
                         "never declared an anchor for")
    return html, {"connectors": {}, "emphases": {},
                  "connectors_stamped": 0, "emphases_stamped": 0}


def build_split(out: Path, handle: str) -> dict:
    staged = stage(out, face="face_bottom_hd.mp4")
    if (staged["face"]["w"], staged["face"]["h"]) != (1080, 1058):
        raise SystemExit(f"the face plate is {staged['face']} - the split's "
                         "seam is derived from a 1080x1058 HD plate")
    ws = words()
    ws, clean_rep = clean_tokens(ws)
    lane = assert_plan_lane()
    spacing = assert_spacing_law()
    anchors = assert_anchor_law()
    lifetimes = assert_lifetime_law()
    emphasis = assert_emphasis_law()
    labels = assert_label_law()
    cast = assert_cast_law()
    axis = assert_axis_law()
    cues = assert_cues(ws)
    wordsync = assert_word_sync(ws)
    law37 = assert_law37(ws)
    SFX = sfx_plan()
    sfx_guard = assert_sfx(SFX)

    scene_html, tweens = SC.build(media(), outro_lockup(handle))
    tweens, repairs = repair_tweens(tweens)
    scene_html, declared = declare_contracts(scene_html)
    if scene_html.count("data-emphasis=") != 0:
        raise SystemExit("no element in this scene may carry data-emphasis")
    if scene_html.count("data-label-for") != 4:
        raise SystemExit("the emitted scene does not carry four labelled keys")
    for shape in ("<circle", "<ellipse"):
        if shape in scene_html:
            raise SystemExit(f"LAW 38 rule 3: {shape} appears in the emitted "
                             "scene - rings/ellipses/circles are retired")
    if 'pathLength="100"' not in scene_html:
        raise SystemExit("the draw-on dash law: a drawn path has no pathLength")

    k = CORE_K
    left = LEFT
    top = CORE_TOP_SPLIT
    m = CAP.PillMeasurer(RUN / "gen/_pillwidths.json")
    beats, cap_rep = caption_beats(m, ws, clean_rep)
    CAP.assert_law12(SEAM, max(b["w"] for b in beats))
    band = guard_core_band("split", top, k, SEAM)
    rail = guard_rail("split")
    objs = phone_objects()
    phone = compare_phone_boxes(objs)

    body = [
        f'<video id="facebot" src="assets/v/face_bottom_hd.mp4" data-start="0" '
        f'data-duration="{DUR}" data-media-start="0" data-track-index="1" muted '
        f'playsinline style="position:absolute;top:{SEAM}px;left:0;width:{int(W)}px;'
        f'height:{H - SEAM}px;object-fit:cover"></video>',
        f'<section id="tz" class="clip tz" data-start="0" data-duration="{DUR}" '
        f'data-track-index="2">',
        f'<div class="abs core" id="core" style="left:{left}px;top:{top}px;'
        f'width:{SC.CORE_W}px;height:{SC.CORE_H}px;transform:scale({k})">',
        scene_html, "</div></section>",
        caption_html(beats, SEAM),
        audio_html(SFX),
    ]
    css = (f".tz {{ left:0; top:0; width:{int(W)}px; height:{SEAM}px; "
           f"overflow:hidden; background:{SC.CREAM}; }}")
    (out / "index.html").write_text(
        head(TITLE, 1080, 1920, 1, css) + "\n".join(body) + tail(tweens),
        encoding="utf-8")
    return {"staged": staged, "beats": beats, "seat": SEAM, "scale": k,
            "core": {"left": left, "top": top}, "band": band, "rail": rail,
            "axis": axis, "plan_lane": lane,
            "law40": anchors, "law42": lifetimes, "law38": emphasis,
            "law41": spacing, "law39": labels, "law37": law37, "law2": cast,
            "law22": sfx_guard, "cues": cues, "word_sync": wordsync,
            "tween_repairs": repairs,
            "production_v2_declarations": {
                "connectors_stamped": 0, "emphases_stamped": 0,
                "labels_repointed": 0,
                "contracts": declared,
                "why": "NOTHING IS STAMPED ON THIS PAGE, and that is the "
                       "instrument's reading rather than an omission.  The "
                       "module draws NO connector (`line_svg` is never called "
                       "by `build()`), so there is no anchor to derive and no "
                       "`data-check-at` to place.  Neither emphasis is an "
                       "ELEMENT: both are the target's OWN outline or border "
                       "flipping ink -> terracotta, so there is nothing to "
                       "carry `data-emphasis`, and pointing a target at itself "
                       "would make visual_laws compare an element's ink with "
                       "itself.  All four `data-label-for` attributes and all "
                       "six `data-block` lockups are stamped by the MODULE and "
                       "are verified here rather than re-written."},
            "phone_objects": objs, "phone_objects_vs_plan": phone,
            "transcript": cap_rep,
            "render": {"w": 1080, "h": 1920, "zoom": 1}}


# ------------------------------------------------------------------ main
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="split", choices=("split",))
    ap.parse_args()

    dst = RUN / "projects/primeagent_split"
    dst.mkdir(parents=True, exist_ok=True)
    rep = build_split(dst, "yt")
    rep["handle_key"] = "yt"
    rep["handle"] = CAP.handle("yt")
    rep["captions"] = {
        "n": len(rep["beats"]),
        "widest_px": round(max(b["w"] for b in rep["beats"]), 1),
        "font_px": CAP.CAP_FONT, "pill_height_px": CAP.CAP_PILL_HEIGHT,
        "sizes": 1,
        "function_word_merges": rep["transcript"]["function_word_merges"],
        "texts": [b["text"] for b in rep["beats"]],
        "aspects": [round(b["w"] / CAP.CAP_PILL_HEIGHT, 2)
                    for b in rep["beats"]],
        "min_aspect": round(min(b["w"] for b in rep["beats"])
                            / CAP.CAP_PILL_HEIGHT, 2),
    }
    rep.pop("beats")
    report = {"video": VID, "lane": "diagram build", "fps": FPS,
              "duration": DUR, "seam": SEAM, "sfx": sfx_levels(),
              "cutout_lanes_for_the_other_author": list(CUTOUT_LANES),
              "formats": {"split": rep}}
    (RUN / "gen/_build_primeagent_split.json").write_text(
        json.dumps(report, indent=1))
    geom = {"video": VID, "fps": FPS, "duration": DUR,
            "shared": {"beat_edges": SC.BEAT_EDGES,
                       "phone_objects": rep["phone_objects"]},
            "formats": {"split": {"phone_objects": rep["phone_objects"],
                                  "core": rep["core"], "scale": rep["scale"],
                                  "seat": rep["seat"],
                                  "voice": rep["staged"]["voice"]}}}
    (RUN / f"gen/_geom_{VID}_split.json").write_text(json.dumps(geom, indent=1))
    print(f"split: {dst}")
    print(json.dumps({"video": VID, "lane": report["lane"],
                      "captions": rep["captions"],
                      "law41": rep["law41"]["tightest_pair"],
                      "law22": {k: v for k, v in rep["law22"].items()
                                if k != "deliberately_silent"},
                      "law38": rep["law38"]["border_flips"],
                      "word_sync": rep["word_sync"]["states_checked"],
                      "repairs": rep["tween_repairs"],
                      "band": rep["band"], "rail": rep["rail"]}, indent=1)[:9000])


if __name__ == "__main__":
    main()
