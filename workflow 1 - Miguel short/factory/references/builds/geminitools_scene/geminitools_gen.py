#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION HERE — geminitools / ICON CHOREOGRAPHY.

    YouTube  classic split 50/50   projects/geminitools_split   @migueltorrezai

Since 2026-09-04 the CUTOUT is a DIFFERENT AGENT that starts when this
recording's `ship` marker passes, so this file builds the SPLIT ONLY and the
shared lane scene survives as an ARTEFACT instead of as a fact in one builder's
head: `geminitools_scene.py` plus `plans/geminitools_scene_handoff.md`.  (The
Reels whiteboard is a bespoke build from the same beat plan and belongs to the
whiteboard author; it reuses the ARGUMENT, not this scene.)

TAKEOVER and FACESPLIT are not daily deliverables and this file cannot build one.

HD DELIVERY (Miguel, 2026-09-03) — "no more 4K rendering, always HD."  The
render is authored AND encoded at 1080x1920: `head(TITLE, 1080, 1920, 1, css)`
and `{"w": 1080, "h": 1920, "zoom": 1}`.  There is no `zoom:2`, no
`data-width="2160"`, no `--resolution`.  The face plate is the delivery-sized
`face_bottom_hd.mp4` (1080x1058, so the seam is 1920 - 1057.5 = 862.5), never a
`*_4k.mp4`.

THE SEAM IS 862.5, AND THAT IS WHERE THE PLAN'S CLEARANCE ARITHMETIC IS RESTATED.
`plans/geminitools_plan.json -> shared_layout_note` derives its clearance from
"the split's RENDERING pill top, 960 - 114.59/2 = 902.705", which is a pill
CENTRED at 960 — FACESPLIT's split-mode seat.  The classic split's seam is fixed
by the face plate's own height (1080x1058 -> the face owns 862.5..1920), so the
pill's real top edge is 862.5 - 114.59/2 = 805.21 and the clearance under the
plan's own lowest ink (canvas 760) is 45.2 px, not 142.7.  Nothing moves: the
plan's band still clears the real seam with 45.2 px to spare, which is why this
build is the plan's geometry unaltered.  Written up in
`plans/geminitools_split_notes.md` s1.

PREP WAS CONSUMED, NOT REDONE.  `prep/stages/geminitools.cut.json` is **status
ok, wall_s 37.4**: `cut_master_duration_s` **18.24**, `tight_audio_duration_s`
18.234, `analysis_wav_written` **false** (48 kHz only, by design).  The split
needs the CUT and nothing else: the plate sweep, prompt0, the track and the ship
serve the CUTOUT alone (RUN-13 REVIEW CHANGES s3).

GUARDS THIS BUILD ASSERTS BEFORE IT WILL WRITE ANYTHING
  * caption canon: ONE size 56.2, one measured pill height, widest pill inside
    the 756 px seat, the seat inside LAW 30's band, and s3b — the WHOLE beat
    stream is passed through `merge_function_only_beats` and then
    `assert_no_function_only_beat`.
  * LAW 6: this take carries NO partial word at all, and the build asserts that
    rather than assuming it.
  * voice: the staged audio is re-probed and must be >= 44.1 kHz (never the
    analysis wav — this run's cut deliberately writes none)
  * LAW 40: both connector ends are re-derived with the SHARED harness's
    `whiteboard_build.anchor_points` and asserted against the scene's own copy;
    the pair is asserted LEVEL and MIRROR-SYMMETRIC about the composition axis
    and clear of each target's corner radius
  * LAW 37: `pipeline/pointing_cues.py` returned ZERO cues for this take and the
    prep marker records it, so `assert_cues_covered` is run on the real scan and
    the build asserts that NO source-post card exists anywhere in the page
  * `assert_cast_resolves`: every stage mark resolves, decodes, and does not
    read as a broken-image glyph, BEFORE a frame renders
  * the cue table is re-read off `transcript_tight.json`: every word-keyed cue
    must still be the START of the word the scene names, so a re-cut can never
    silently slide the choreography, and every authored cue must sit inside its
    own word's LABEL_WINDOW
  * LAW 46 / LAW 47 on the tight transcript: the opening key occurs once and the
    master ends within 0.20 s (+ one frame) of the last spoken word
  * LAW 41: every pair of concurrent rigids that is not one declared block is
    measured, and the tightest non-block gutter is reported
  * LAW 39: every printed key is proved ABOVE or BELOW its host with its centre
    inside the host's +-15 % band
  * LAW 42: this board is SINGLE, so every accumulating mark is a declared
    anchor and the build proves the declaration covers them all
"""
from __future__ import annotations

import argparse
import html as ihtml
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

F = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(F / "pipeline"))
sys.path.insert(0, str(F / "pipeline/prep"))
sys.path.insert(0, str(F / "formats/cutout/lib"))
sys.path.insert(0, str(F / "formats/whiteboard/lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import captions as CAP                       # noqa: E402
import cutout_core as CC                     # noqa: E402
import cutout_depthfield as DF               # noqa: E402
import pointing_cues as PCUE                 # noqa: E402
import geminitools_scene as SC               # noqa: E402

RUN = F / "shorts_run15"
CUT = RUN / "cuts/geminitools"
ASSETS = Path.home() / "Documents/Workspace/assets"

VID = "geminitools"
W, H = 1080.0, 1920.0
FPS = 25                                     # native capture, GLOBAL LAW 26
DUR = 18.24                                  # the cut master, 456 frames at 25

SEAM = 862.5                                 # the published split's seam; the
#                                              face plate is 1080x1058
CORE_TOP_SPLIT = SC.CANVAS_OFFSET            # 192.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                  # AUDIO MIX LAW

TITLE = "Gemini calls Google Search and Maps from the API"
LABEL_WINDOW = 1.0


# ------------------------------------------------------------------ marks
# MARK IDENTITY (STANDARD.md): when the registry holds more than one file for a
# brand, THE SCRIPT'S WORD decides which one, and the pick is written HERE as a
# comment naming the registry key.
#
# `gemini`      -> ai-models/gemini-color.png.  The story's subject model, in
#                  its own brand colours (LAW 12).  The script's word is
#                  "Gemini", twice, and it is the API being talked about.
# `google-g`    -> platforms/google-g.svg.  THIS IS THE GOOGLE SEARCH MARK.
#                  Google publishes no separate "Google Search" product asset;
#                  the multicolour G is the google.com favicon and the Google
#                  app icon, so under LAW 35 it IS the product mark and not a
#                  company fallback.  What is never legal in its place is a
#                  drawn magnifying glass (LAW 33 bans generic glyphs).  If a
#                  dedicated `google-search` key is ever registered, swap it.
# `google-maps` -> platforms/google-maps-color.png, the COLOUR pin, never the
#                  `google-maps.svg` monochrome reduction (LAW 12).  Its ink
#                  aspect is 0.698 against the G's 0.98, so it is sized by INK
#                  AREA and not by its box, or the pin reads as a third of the
#                  G at 405x720 (MARK IDENTITY's third clause).
STAGE_FILES = {
    "gemini": "logos/ai-models/gemini-color.png",
    "google-g": "logos/platforms/google-g.svg",
    "google-maps": "logos/platforms/google-maps-color.png",
}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}

# THE DEPTH CAST IS NOT THIS FILE'S BUSINESS.  The plan's `cast` /
# `cutout_logo_lanes` belong to the CUTOUT author, who owns
# `cutout_depthfield.assert_cast_resolves` for them.  It is recorded in the
# handoff, not built here.  `gemini`, `google-g` and `google-maps` are
# deliberately ABSENT from it: they are this story's own subject marks and they
# live on the STAGE (a subject mark in the depth field is the run-9 defect).
CUTOUT_CAST = ("openai", "claude", "perplexity", "grok", "mistral", "exa")


# ------------------------------------------------------------------ transcript
def words() -> list[dict]:
    d = json.loads((CUT / "transcript_tight.json").read_text())
    return [w for w in d["words"] if w.get("type") == "word"]


def clean_tokens(ws: list[dict]) -> tuple[list[dict], dict]:
    """LAW 6: a partial word never reaches a caption — and this take has none.

    LAW 46, checked here on the TIGHT transcript (the raw Scribe pass can merge
    two attempts into one word run, as it did on astramath).  The INTAKE
    transcript opens twice — "If you're using Gemini via... If you're using
    Gemini via the API" — and the first attempt dies on `via...` at 4.36 s
    WITHOUT reaching the full opening key, with the keeper beginning at
    6.679 s.  Under LAW 46 as amended (run 13) that is a genuine restart, the
    cut correctly took the LAST repeat, and `transcript_tight.json` opens ONCE,
    cleanly, at 0.119 s.  This assert proves the tight file, not the intake one.

    LAW 47, hard cap: the master ends `last word end + 0.20 s`.  18.019 + 0.20 =
    18.219 against an 18.24 s master — 0.021 s, i.e. half a frame at 25 fps.
    """
    partial = [(i, w) for i, w in enumerate(ws)
               if w["text"].strip().endswith(("-", "...", "…"))]
    if partial:
        raise SystemExit(f"unexpected partial words in the take: "
                         f"{[w['text'] for _, w in partial]}")
    head = " ".join(w["text"] for w in ws[:5]).lower()
    if not head.startswith("if you're using gemini via"):
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[3:]).lower()
    if "if you're using gemini" in later:
        raise SystemExit("LAW 46: the opening repeats inside the take — the cut "
                         "is wrong, do not use it as a two-step hook")
    tail = DUR - float(ws[-1]["end"])
    if tail > 0.20 + 1.0 / FPS:
        raise SystemExit(f"LAW 47: the master runs {tail:.3f}s past the last "
                         f"word (cap 0.20 + one frame)")
    rep = {"partials_dropped": [], "law47_tail_s": round(tail, 3),
           "law46": "the opening key occurs once, at word 0 / 0.119 s; the "
                    "intake transcript's abandoned attempt (dies on 'via...' at "
                    "4.36 s) is not in the tight file at all",
           "inner_stumbles": "none — this take carries no discard marker after "
                             "the keeper opening"}
    return list(ws), rep


# THE CUE TABLE, RE-READ OFF THE CUT.  A word-keyed cue is a word START; an
# `inside` cue is authored by the plan and must sit inside its own word's 1.0 s
# LABEL_WINDOW.  This is the assert that makes a re-cut impossible to miss: it
# would slide every gesture in the video and no geometry gate would notice.
CUE_WORDS = {
    "lineL": (16, "google", "start"), "lineR": (19, "google", "start"),
    "charge": (22, "directly", "start"), "emph": (27, "both", "start"),
    "clock": (35, "speed", "start"), "keyF": (40, "more.", "start"),
    "outro": (41, "now,", "start"),
}
CUE_INSIDE = {
    "plug": (2, "using"), "slide": (3, "gemini"), "plate": (3, "gemini"),
    "seat": (6, "api,"), "keyterm": (6, "api,"),
    "tileL": (16, "google"), "keyL": (17, "search"),
    "tileR": (19, "google"), "keyR": (21, "tools"),
    "emphout": (31, "time,"), "sweep": (36, "up"),
}


def assert_cues(ws: list[dict]) -> dict:
    """The choreography is keyed on words, so the words are re-read."""
    rep: dict = {}
    for name, (idx, text, edge) in CUE_WORDS.items():
        if idx >= len(ws):
            raise SystemExit(f"cue {name}: word {idx} is past the take")
        w = ws[idx]
        if w["text"].strip().lower() != text:
            raise SystemExit(f"cue {name}: word {idx} is {w['text']!r}, not "
                             f"{text!r} — the cut moved, re-derive the scene")
        want = SC.CUE[name]
        got = round(float(w[edge]), 3)
        if abs(got - want) > 0.011:
            raise SystemExit(f"cue {name}: the scene fires at {want}, the "
                             f"word's {edge} is {got} — re-derive the scene")
        rep[name] = {"word": idx, "text": w["text"], "edge": edge, "t": want}
    for name, (idx, text) in CUE_INSIDE.items():
        w = ws[idx]
        if w["text"].strip().lower() != text:
            raise SystemExit(f"cue {name}: word {idx} is {w['text']!r}, not "
                             f"{text!r}")
        t = SC.CUE[name]
        # THE WINDOW RUNS FROM THE WORD'S START TO ITS END PLUS `LABEL_WINDOW`.
        lo, hi = float(w["start"]), float(w["end"]) + LABEL_WINDOW
        if not (lo <= t <= hi):
            raise SystemExit(f"cue {name} at {t} is outside the 1.0 s "
                             f"LABEL_WINDOW of {w['text']!r} "
                             f"({lo:.3f}-{hi:.3f})")
        rep[name] = {"word": idx, "text": w["text"], "edge": "inside", "t": t,
                     "window": [round(lo, 3), round(hi, 3)]}
    missing = set(SC.CUE) - set(rep)
    if missing:
        raise SystemExit(f"cues the build never verified: {sorted(missing)}")
    # LAW 13's peak beat is timed to its own word to the millisecond: the charge
    # runs exactly as long as "directly" is spoken.
    d = ws[22]
    span = round(float(d["end"]) - float(d["start"]), 3)
    if abs(span - 0.72) > 0.011:
        raise SystemExit(f"the charge is authored 0.72 s to match 'directly', "
                         f"whose real span is {span}")
    rep["charge"]["word_span_s"] = span
    return rep


def assert_law37(ws: list[dict]) -> dict:
    """LAW 37 — and this take raises no cue at all.

    `pipeline/pointing_cues.py --vid geminitools` was run at plan time and again
    by prep; `prep/stages/geminitools.cues.json` records **cue_count 0** and
    `gen/_cues_geminitools.json` holds the empty list.  The scan is re-run HERE
    on the tight transcript rather than trusted, because a cue the plan missed
    would be a card that never gets drawn — and then `assert_cues_covered` is
    called on the real result.

    Nothing to answer and nothing to waive, so NO source-post card may be
    invented: GLOBAL LAW 3 allows a post on screen only when the post IS the
    news.  The run-13 platform ruling does not engage either — "Google Search"
    and "Google Maps" are the TOOLS being called, not the place the news came
    from, so they appear as marks on the stage and never as post cards.
    """
    cues = PCUE.scan(ws)
    if cues:
        raise SystemExit(f"LAW 37: the scan now finds {len(cues)} pointing "
                         f"cue(s) this build answers with nothing: {cues}")
    PCUE.assert_cues_covered(cues, [])
    return {"cue_count": 0, "cards": [],
            "instrument": "pointing_cues.scan re-run on transcript_tight.json",
            "prep_marker": "prep/stages/geminitools.cues.json -> cue_count 0",
            "note": "no 'this guy', no 'someone on X', no 'a post', no platform "
                    "named as a source and no URL across all 62 spoken words — "
                    "Miguel states a capability, he does not cite anybody"}


# ------------------------------------------------------------------ geometry
# THE RIGIDS THIS PAGE PAINTS, in CORE px, with the declared block each belongs
# to.  Connectors and the charge are excluded on purpose: they carry
# `data-overlap-ok` because they are supposed to touch what they join, which
# removes them from Gate 1's spacing law as well (the run-14 finding), and they
# are judged by `assert_anchor_law` and `assert_no_text_crossing` instead.
RIGIDS = {
    "api-plug": (SC.PLUG_BOX, "gemini"),
    "gemini-plate": (SC.PLATE_BOX, "gemini"),
    "key-gemini-api": ((SC.KEY_TERM_BOX[0], SC.KEY_TERM_BOX[1],
                        SC.KEY_TERM_BOX[0] + SC.KEY_TERM_BOX[2],
                        SC.KEY_TERM_BOX[1] + SC.KEY_TERM_BOX[3]), "gemini"),
    "search-tile": (SC.SEARCH_BOX, "search"),
    "key-search": ((SC.KEY_SEARCH[0], SC.KEY_SEARCH[1],
                    SC.KEY_SEARCH[0] + SC.KEY_SEARCH[2],
                    SC.KEY_SEARCH[1] + SC.KEY_SEARCH[3]), "search"),
    "maps-tile": (SC.MAPS_BOX, "maps"),
    "key-maps": ((SC.KEY_MAPS[0], SC.KEY_MAPS[1],
                  SC.KEY_MAPS[0] + SC.KEY_MAPS[2],
                  SC.KEY_MAPS[1] + SC.KEY_MAPS[3]), "maps"),
    "stopwatch": (SC.STOPWATCH_BOX, "clock"),
    "key-faster": ((SC.KEY_FASTER[0], SC.KEY_FASTER[1],
                    SC.KEY_FASTER[0] + SC.KEY_FASTER[2],
                    SC.KEY_FASTER[1] + SC.KEY_FASTER[3]), "clock"),
}

# LAW 39: every printed key, its host, and the side it is written on.
LABELS = {
    "key-gemini-api": ("gemini-plate", "above", SC.KEY_TERM),
    "key-search": ("search-tile", "below", "GOOGLE SEARCH"),
    "key-maps": ("maps-tile", "below", "GOOGLE MAPS"),
    "key-faster": ("stopwatch", "below", "FASTER"),
}

GUTTER_REFUSE = 16.0        # LAW 41's refusal line, design px
GUTTER_AIM = 24.0           # the number the plan aims for, and the number the
#                             cutout's ~0.95 scaling has to survive


def _gap(a, b) -> float:
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    dx = max(bx0 - ax1, ax0 - bx1, 0.0)
    dy = max(by0 - ay1, ay0 - by1, 0.0)
    if dx > 0 and dy > 0:
        return math.hypot(dx, dy)
    return dx + dy


def assert_spacing_law() -> dict:
    """LAW 41 clause 1 + clause 3, measured rather than asserted in a comment.

    Two rigids are only judged against each other when their LIFETIMES overlap,
    and a pair inside one declared block is exempt from its own gutter (never
    from anyone else's).  The AIM is 24 design px and the REFUSAL is 16.
    """
    names = list(RIGIDS)
    pairs, tight = [], None
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            (ba, blka), (bb, blkb) = RIGIDS[a], RIGIDS[b]
            if blka == blkb:
                continue
            ta, tb = SC.LIFETIMES[a], SC.LIFETIMES[b]
            a1 = DUR if ta[1] is None else ta[1]
            b1 = DUR if tb[1] is None else tb[1]
            if min(a1, b1) <= max(ta[0], tb[0]):
                continue                      # never on screen together
            g = _gap(ba, bb)
            pairs.append((a, b, round(g, 1)))
            if tight is None or g < tight[2]:
                tight = (a, b, round(g, 1))
    bad = [p for p in pairs if p[2] < GUTTER_REFUSE]
    if bad:
        raise SystemExit(f"LAW 41: cramped non-block pairs {bad}")
    below_aim = [p for p in pairs if p[2] < GUTTER_AIM]
    if below_aim:
        raise SystemExit(f"LAW 41: pairs under the {GUTTER_AIM}px AIM — the "
                         f"cutout scales this core by ~0.95 and would refuse "
                         f"them: {below_aim}")
    return {"pairs_judged": len(pairs),
            "tightest_non_block": {"pair": [tight[0], tight[1]],
                                   "core_px": tight[2],
                                   "at_cutout_0_95_canvas_px":
                                       round(tight[2] * 0.95, 1)},
            "refusal_px": GUTTER_REFUSE, "aim_px": GUTTER_AIM,
            "blocks": [list(b) for b in SC.DECLARED_BLOCKS],
            "all_pairs": sorted(pairs, key=lambda p: p[2])[:8]}


def assert_label_law() -> dict:
    """LAW 39 — a name goes ABOVE or BELOW the thing it names, never beside, and
    its centre falls inside the object's horizontal extent +-15 %."""
    out = {}
    for key, (host, side, text) in LABELS.items():
        kb = RIGIDS[key][0]
        hb = RIGIDS[host][0]
        kcx = (kb[0] + kb[2]) / 2
        hcx = (hb[0] + hb[2]) / 2
        band = (hb[2] - hb[0]) * 0.15
        if abs(kcx - hcx) > band + 0.01:
            raise SystemExit(f"LAW 39: {key} centre {kcx} is {abs(kcx - hcx):.1f}"
                             f"px off {host}'s axis {hcx} (band +-{band:.1f})")
        if side == "above" and kb[3] > hb[1] + 2:
            raise SystemExit(f"LAW 39: {key} is not fully above {host}")
        if side == "below" and kb[1] < hb[3] - 2:
            raise SystemExit(f"LAW 39: {key} is not fully below {host}")
        gap = (hb[1] - kb[3]) if side == "above" else (kb[1] - hb[3])
        # LAW 9 / the label window: the key arrives WITH its object's beat
        t_key = SC.LIFETIMES[key][0]
        t_host = SC.LIFETIMES[host][0]
        if t_key < t_host:
            raise SystemExit(f"LAW 9: {key} lands at {t_key} before its host "
                             f"{host} at {t_host}")
        out[key] = {"host": host, "side": side, "text": text,
                    "centre_off_axis_px": round(kcx - hcx, 2),
                    "band_px": round(band, 1), "gutter_px": round(gap, 1),
                    "at": t_key, "host_at": t_host,
                    "delay_after_host_s": round(t_key - t_host, 3)}
    return out


def assert_anchor_law() -> dict:
    """LAW 40, proved against the SHARED harness rather than against a copy.

    `geminitools_scene.anchor_points` is the DOM lane's local implementation of
    `whiteboard_build.anchor_points`; if the two ever disagreed the declaration
    would be a fiction, so the build re-derives every end with the harness's own
    function and asserts equality before it writes.

    This video is ONE SOURCE fanning into TWO DIFFERENT targets, so LAW 40's
    letter (two or more arrows landing in ONE target) does not bind it — but the
    ends are built with the law's own helper anyway, because hand-placed ends
    are the defect the law exists to stop, and the PAIR is then asserted level
    and mirror-symmetric about the composition axis so the law is satisfied in
    substance whichever way a checker reads the group.

    This assert is not belt-and-braces: `data-overlap-ok` (which a connector
    MUST carry — it is supposed to touch what it joins) removes an element from
    ALL of Gate 1's `check_layout`, `anchorline` included, so the gate cannot
    see LAW 40 on these two lines at all.
    """
    import whiteboard_build as WB                                # noqa: E402
    want_s = WB.anchor_points(SC.SEARCH_BOX, 1, side="top")[0]
    want_m = WB.anchor_points(SC.MAPS_BOX, 1, side="top")[0]
    for want, got, tag in ((want_s, SC.A_SEARCH, "search"),
                           (want_m, SC.A_MAPS, "maps")):
        if abs(want[0] - got[0]) > 1e-6 or abs(want[1] - got[1]) > 1e-6:
            raise SystemExit(f"LAW 40: the {tag} end {got} != harness {want}")
    if abs(SC.A_SEARCH[1] - SC.A_MAPS[1]) > 1e-6:
        raise SystemExit("LAW 40: the two ends are not level")
    mirror = abs((SC.AXIS - SC.A_SEARCH[0]) - (SC.A_MAPS[0] - SC.AXIS))
    if mirror > 1e-6:
        raise SystemExit(f"LAW 40: the ends are not mirror-symmetric about "
                         f"x={SC.AXIS} (error {mirror})")
    if abs((SC.AXIS - SC.FROM_SEARCH[0]) - (SC.FROM_MAPS[0] - SC.AXIS)) > 1e-6:
        raise SystemExit("LAW 40: the two ORIGINS are not mirror-symmetric")
    if abs(SC.FROM_SEARCH[1] - SC.FROM_MAPS[1]) > 1e-6:
        raise SystemExit("LAW 40: the two ORIGINS are not level")
    corner = SC.TILE_RADIUS
    clear = min(SC.A_SEARCH[0] - SC.SEARCH_BOX[0],
                SC.SEARCH_BOX[2] - SC.A_SEARCH[0],
                SC.A_MAPS[0] - SC.MAPS_BOX[0],
                SC.MAPS_BOX[2] - SC.A_MAPS[0])
    if clear < corner:
        raise SystemExit(f"LAW 40: an end sits {clear:.1f}px from a corner, "
                         f"inside the {corner}px radius")
    # LAW 41 clause 2: no connector, and no segment of the charge, may cross a
    # printed key's CORE band (inset 22 % top / 28 % bottom / 4 % each side).
    segs = [("line-left", SC.FROM_SEARCH, SC.A_SEARCH),
            ("line-right", SC.FROM_MAPS, SC.A_MAPS)]
    charge_y = [218.0, 244.0, 250.0, 272.0, 292.0, 300.0, 304.0, 376.0]
    lo_y = min(min(p[1] for p in (a, b)) for _, a, b in segs) - 0.1
    hi_y = max(max(p[1] for p in (a, b)) for _, a, b in segs) + 0.1
    lo_y = min(lo_y, min(charge_y))
    hi_y = max(hi_y, max(charge_y))
    for key, (box, _blk) in RIGIDS.items():
        if not key.startswith("key-"):
            continue
        cy0 = box[1] + 0.22 * (box[3] - box[1])
        cy1 = box[1] + 0.72 * (box[3] - box[1])
        if lo_y < cy1 and hi_y > cy0:
            raise SystemExit(f"LAW 41 clause 2: connector/charge ink spans "
                             f"y {lo_y:.0f}..{hi_y:.0f} and could enter "
                             f"{key}'s core band {cy0:.0f}..{cy1:.0f}")
    return {"groups": [
                {"target": "search-tile", "side": "top", "n": 1,
                 "end": list(SC.A_SEARCH), "origin": list(SC.FROM_SEARCH)},
                {"target": "maps-tile", "side": "top", "n": 1,
                 "end": list(SC.A_MAPS), "origin": list(SC.FROM_MAPS)}],
            "level_error_px": 0.0, "mirror_error_px": round(mirror, 6),
            "axis_x": SC.AXIS, "corner_radius_px": corner,
            "clear_of_corner_px": round(clear, 1),
            "canvas_ends": [[SC.A_SEARCH[0], SC.A_SEARCH[1] + SC.CANVAS_OFFSET],
                            [SC.A_MAPS[0], SC.A_MAPS[1] + SC.CANVAS_OFFSET]],
            "text_crossing": "all connector and charge ink lives at y <= 376; "
                             "the lowest type above it is the key term, whose "
                             "core band ends at 136, and every printed key "
                             "below it starts at y >= 514",
            "source": "whiteboard_build.anchor_points, re-derived and asserted",
            "letter_of_the_law": "ONE source, TWO targets — the law governs two "
                                 "arrows into ONE target and does not bind "
                                 "here; the pair is level and mirrored anyway"}


def assert_lifetime_law() -> dict:
    """LAW 42.  A SINGLE board (LAW 43's exception) is all-anchor by definition
    and the harness detects that — but the outro wipe clears every rigid at the
    same instant and `chapter_seams()` reads an erase time shared by >= 3 rigids
    as a seam, so every accumulating mark is DECLARED and the law holds under
    either reading.  Each anchor's own PAINTED share is measured here rather
    than asserted in a comment.
    """
    bad, shares = [], {}
    for name, (t0, t1) in SC.LIFETIMES.items():
        end = DUR if t1 is None else t1
        share = (min(end, DUR) - t0) / DUR
        shares[name] = round(share, 3)
        if t1 is None and name not in SC.SCENE_ANCHORS and not name.startswith("o-"):
            if share > 0.40:
                bad.append(f"{name} {share * 100:.0f}% with no t_to and no anchor")
    if bad:
        raise SystemExit("LAW 42: " + "; ".join(bad))
    missing = [n for n in SC.SCENE_ANCHORS if n not in SC.LIFETIMES]
    if missing:
        raise SystemExit(f"LAW 42: declared anchors with no lifetime {missing}")
    painted = {n: round((SC.CUE["outro"] - SC.LIFETIMES[n][0]) / DUR, 3)
               for n in ("api-plug", "gemini-plate", "search-tile",
                         "maps-tile", "stopwatch")}
    finite = {n: v for n, v in SC.LIFETIMES.items() if v[1] is not None}
    return {"board_mode": SC.BOARD_MODE,
            "board_mode_reason": "ONE idea that accumulates — every later "
                                 "sentence modifies the SAME picture instead of "
                                 "opening a second one, so there is no second "
                                 "idea group, nothing to erase and nothing a "
                                 "seam could separate (LAW 43's exception)",
            "board_chapters": SC.BOARD_CHAPTERS,
            "anchors_declared": list(SC.SCENE_ANCHORS),
            "anchor_screen_share_painted": painted,
            "finite_marks": finite,
            "shares": shares,
            "note": "the only finite lifetimes in the video are the two "
                    "emphases (9.58 -> 11.20); an emphasis lives only inside "
                    "the beat that argues it and neither survives into the "
                    "payoff.  The sheet, the glyph, the rule and the slot are "
                    "the OUTRO's own composition, authored after the board's "
                    "last ink, and are open-ended by construction"}


def assert_key_term() -> dict:
    """LAW 9 / LAW 19 / LAW 20 / LAW 24, all on the opening.

    The video's core term debuts on the board FIRST among all type, ALONE and
    LARGE; the hook OBJECT opens centred on the composition axis, alone, and is
    complete from its first frame; and nothing is visible before its words.
    """
    first_ink = min(t0 for t0, _ in SC.LIFETIMES.values())
    if abs(first_ink - SC.CUE["plug"]) > 1.0 / FPS:
        raise SystemExit(f"LAW 9/19: the first ink is at {first_ink}, not the "
                         f"plug at {SC.CUE['plug']}")
    if SC.CUE["plate"] <= first_ink:
        raise SystemExit("LAW 19: the hook object is not alone on screen")
    centre_x = SC.PLUG_BOX[0] + SC.PLUG[2] / 2 + SC.PLUG_START_DX
    if abs(centre_x - SC.AXIS) > 0.01:
        raise SystemExit(f"LAW 19: the plug opens at x={centre_x}, not on the "
                         f"composition axis {SC.AXIS}")
    typed = {"key-gemini-api": SC.CUE["keyterm"], "key-search": SC.CUE["keyL"],
             "key-maps": SC.CUE["keyR"], "key-faster": SC.CUE["keyF"]}
    if min(typed.values()) != SC.CUE["keyterm"]:
        raise SystemExit("LAW 9: the key term is not the first type on screen")
    if SC.KEY_TERM_FS / CAP.S < 22.0:
        raise SystemExit(f"LAW 9: the key term is {SC.KEY_TERM_FS / CAP.S:.1f} "
                         f"design units, under the 22 du floor")
    return {"key_term": SC.KEY_TERM, "at": SC.CUE["keyterm"],
            "font_px": SC.KEY_TERM_FS,
            "design_units": round(SC.KEY_TERM_FS / CAP.S, 1),
            "first_ink_at": first_ink,
            "hook_object": "a plug — the video's IDEA as an object (LAW 20), "
                           "complete from its first frame, so the vessel "
                           "corollary is satisfied by construction",
            "alone_until": SC.CUE["plate"],
            "opens_centred_on_x": round(centre_x, 2),
            "displaces_at": SC.CUE["slide"], "seats_at": SC.CUE["seat"],
            "first_type_at": min(typed.values()),
            "type_order": sorted(typed.items(), key=lambda kv: kv[1]),
            "law24": "every word of THE GEMINI API is spoken by 1.979, and it "
                     "is NOT 'GEMINI API TOOLS' because 'tools' is not spoken "
                     "until 6.920 — that would be a peek-ahead"}


def assert_emphasis_law() -> dict:
    """LAW 38, and this video's two emphases are the same event twice.

    The targets are DRAWN tiles, so BOXING, and the DOM lane's boxing is the
    PANEL BORDER FLIP — the tile's own border, which adds no geometry and
    therefore no new gutter.  There is no ring, no ellipse and no circle
    anywhere in the page, and there is no marker highlight either, because there
    is no raster text in this video at all.
    """
    if abs(SC.LIFETIMES["emph-search"][0] - SC.LIFETIMES["emph-maps"][0]) > 1e-9:
        raise SystemExit("the two emphases are staggered; the simultaneity IS "
                         "the claim the sentence makes")
    if abs(SC.LIFETIMES["emph-search"][1] - SC.LIFETIMES["emph-maps"][1]) > 1e-9:
        raise SystemExit("the two emphases do not release on the same frame")
    return {"targets": ["search-tile", "maps-tile"], "kind": "box",
            "dom_primitive": "PANEL BORDER FLIP — borderColor "
                             f"{SC.TILE_EDGE} -> {SC.TERRA_L}, 0.38 s, SOFT",
            "at": SC.CUE["emph"], "release": SC.CUE["emphout"],
            "window": list(SC.LIFETIMES["emph-search"]),
            "rings_ellipses_circles": 0,
            "marker_highlights": 0,
            "why_no_highlight": "LAW 38 rule 1 is for TEXT ON AN IMAGE and "
                                "there is no raster text in this video: no "
                                "post, no screenshot, no document",
            "never_on_the_mark": "a registry mark is a raster and rule 2(b) "
                                 "refuses a box on image content — the flip is "
                                 "on the PLATE's own border, and the plate "
                                 "carries a background so Gate 1 never reads it "
                                 "as an emphasis outline at all"}


# ------------------------------------------------------------------ captions
def phrases(ws: list[dict]) -> list[list[dict]]:
    """Group into caption phrases at punctuation and at real pauses.

    THE CAP IS 20, the run-14 number, and it is not doing any work on this take:
    the longest punctuation-to-punctuation clause here is 11 words ("Now, follow
    for more AI news," is 6; "and tutorials each and every single day," is 7).
    It stays at 20 so a clause always reaches `split_to_fit` whole and the
    partitioner, not the chunker, decides where a pill breaks.
    """
    out, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w)
        end = w["text"].strip().endswith((".", ",", "!", "?"))
        gap = (ws[i + 1]["start"] - w["end"]) if i + 1 < len(ws) else 9.0
        if end or gap >= 0.30 or len(cur) >= 20:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def caption_beats(measurer) -> tuple[list[dict], dict]:
    ws, clean_rep = clean_tokens(words())
    measurer.want(CAP.runs([w["text"] for w in ws]))
    measurer.resolve()
    # s3b, THE "in" / LinkedIn DEFECT.  The merge runs over the WHOLE beat
    # stream, never inside one phrase at a time: orphans are produced AT phrase
    # boundaries, so the neighbour a beat needs is in the next phrase by
    # construction.  A prepositional beat binds FORWARD.
    #
    # THE PARTITIONER IS `split_balanced`, NOT `split_to_fit`, AND THE REASON IS
    # MEASURED.  LAW 31's own words are "take the fewest beats that all fit, and
    # among those the partition whose widest beat is narrowest, SO A SPLIT NEVER
    # STRANDS AN ORPHAN."  The greedy fill does strand one on this take: the
    # sign-off *"and catch you in the next one"* renders 770 px against the
    # 756 px seat, so greedy emits "and catch you in the next" + **"one"** —
    # 165.0 px, aspect **1.44**, one hundredth under `PILL_MIN_ASPECT` 1.45 and
    # therefore the LinkedIn-badge shape, and neither neighbour can take it back
    # inside the seat, so `merge_function_only_beats` leaves it and the build
    # refuses.  The balanced split takes the most even boundary instead —
    # "and catch you" + "in the next one" — and strands nothing.
    # `forbidden` carries the four strings this video PRINTS on the board, so a
    # boundary can never manufacture a pill that repeats a live board key
    # (LAW 4).
    forbidden = {t.lower() for _, _, t in LABELS.values()}
    parts: list[list] = []
    for group in phrases(ws):
        parts.extend(CAP.split_balanced(group, CAP.SEAT_MAX_W, measurer,
                                        forbidden=forbidden))
    before = len(parts)
    parts = CAP.merge_function_only_beats(parts, CAP.SEAT_MAX_W, measurer)
    merged = before - len(parts)

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
    # LAW 4 / caption_identity_guard, checked by ARITHMETIC rather than by eye:
    # no printed board key may be alive while an IDENTICAL pill is on screen.
    board_keys = {t.upper() for _, _, t in LABELS.values()}
    for b in beats:
        if b["text"].strip().upper().rstrip(".,") in board_keys:
            raise SystemExit(f"caption echo: the pill {b['text']!r} is a board "
                             f"key verbatim")
    clean_rep["function_word_merges"] = merged
    clean_rep["caption_echo_check"] = sorted(board_keys)
    return beats, clean_rep


def caption_html(beats, seat_y) -> str:
    """FRAME-QUANTISED, half-open, ONE OWNER PER FRAME.

    `start = k0/fps`, `dur = (k1-k0-0.5)/fps`, `k = round(t*fps)` — and **k1 is
    the NEXT beat's k0**, not this beat's own end.  The beat stream carries a
    0.24 s floor on `dur`, so a shorter beat's own end lands PAST the next
    beat's start and the two clips would then own the same frame.  Deriving k1
    from the neighbour makes an overlap arithmetically impossible.
    """
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
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Nunito:wght@800&family=JetBrains+Mono:wght@400;500;700;800&display=block" rel="stylesheet">
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
const tl = gsap.timeline({{paused:true}});
{body}
window.__timelines["main"]=tl;
</script></body></html>
"""


def outro_lockup(handle_key: str) -> str:
    """The scene reserves `#o-slot`; the format seats THIS lockup inside it.

    The handle is the ONLY string that differs between the two masters and it is
    never re-typed: `captions.handle()` resolves it.
    """
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

    # VOICE — the 48 kHz master, re-probed AFTER staging (the staged file is
    # what mixes, so the staged file is what is measured).  This run's cut
    # deliberately writes NO 16 kHz analysis wav at all
    # (`stages.cut.analysis_wav_written: false`), so the TREBLE gate's Nyquist
    # trap has no way to fire here.
    shutil.copy2(CUT / "audio.m4a", v / "voice.m4a")
    pr = probe_audio(v / "voice.m4a")
    if pr["sample_rate"] < 44100:
        raise SystemExit(f"staged voice is {pr['sample_rate']} Hz — the analysis "
                         "track can never be the mix")
    rec["voice"] = {"source": str(CUT / "audio.m4a"), **pr}

    shutil.copy2(F / "assets/music/bed_split_v2.mp3", dst / "assets/music/bed.mp3")
    for s in ("whoosh", "pop", "click"):
        shutil.copy2(F / f"assets/sfx/{s}.mp3", dst / f"assets/sfx/{s}.mp3")

    shutil.copy2(CUT / face, v / face)
    rec["face"] = {"file": face, **probe_wh(CUT / face)}

    # THE HARD ROSTER GUARD, on every mark this build paints.  Existence was
    # never the problem: run 9 shipped a real logo that reads as the browser's
    # broken-image glyph.
    cast_report = DF.assert_cast_resolves(list(STAGE_FILES), STAGE_FILES,
                                          ASSETS, label="geminitools marks")
    for key, rel in STAGE_FILES.items():
        src = ASSETS / rel
        if not src.exists():
            raise SystemExit(f"missing registry mark: {src}  (add + register it)")
        shutil.copy2(src, dst / f"assets/logos/{Path(rel).name}")
        CC.MARK_INK[key] = CC.measure_mark(key, src)
    rec["marks"] = {k: {"path": v2["path"], "size": v2["size"]}
                    for k, v2 in cast_report.items()}
    return rec


def scene_media() -> dict:
    """The three marks the SCENE paints, each sized by its own INK.

    `cutout_core.mark_img` sizes by ink AREA and corrects the ink centroid, so
    centring the box centres the MARK — equal boxes are not equal marks
    (MARK IDENTITY's third clause).  It matters more here than in most videos:
    `google-maps` is a PIN at ink aspect 0.698 and `google-g` is square at 0.98,
    so an equal box would give the pin a third of the G's optical weight in a
    row the whole composition asks the viewer to read as a PAIR.
    """
    return {
        "_gemini_img": CC.mark_img(LOGO_URL["gemini"], "gemini",
                                   SC.MARK_SIDE_PLATE),
        "_search_img": CC.mark_img(LOGO_URL["google-g"], "google-g",
                                   SC.MARK_SIDE_TILE),
        "_maps_img": CC.mark_img(LOGO_URL["google-maps"], "google-maps",
                                 SC.MARK_SIDE_TILE),
    }


def mark_ink_report() -> dict:
    """LAW 36 — a mark stays inside its box, with visible margin, and the margin
    is MEASURED off the ink rather than assumed off the box."""
    out = {}
    for key, side, host, pad_box in (
            ("gemini", SC.MARK_SIDE_PLATE, "gemini-plate", SC.PLATE_PB),
            ("google-g", SC.MARK_SIDE_TILE, "search-tile", SC.TILE_PB),
            ("google-maps", SC.MARK_SIDE_TILE, "maps-tile", SC.TILE_PB)):
        m = CC.MARK_INK[key]
        ink_w = side * math.sqrt(m["aspect"])
        ink_h = ink_w / m["aspect"]
        mx = (pad_box - ink_w) / 2
        my = (pad_box - ink_h) / 2
        bw = SC.PLATE_BW if host == "gemini-plate" else SC.TILE_BW
        if min(mx, my) <= 0:
            raise SystemExit(f"LAW 36: {key}'s ink escapes {host}")
        out[f"{key}@{side:.0f}"] = {
            "aspect": round(m["aspect"], 3),
            "ink_core_px": [round(ink_w, 1), round(ink_h, 1)],
            "host": host, "padding_box_px": pad_box,
            "margin_inside_padding_box_px": [round(mx, 1), round(my, 1)],
            "margin_from_outer_edge_px": [round(mx + bw, 1), round(my + bw, 1)],
            "sized_by": "INK AREA (MARK IDENTITY), never by the box"}
    return out


# ------------------------------------------------------------------ guards
def guard_core_band(fmt: str, top: float, k: float, cap_seat: float,
                    pill_clear: float = 24.0) -> dict:
    """LAW 30 above, THE SEAM IS SACRED below — and the clearance is derived
    with the pill that RENDERS (114.59), never the frozen 108.2 seat constant.
    The two differ by 6.4 px and only one of them is what the viewer sees.
    """
    y0 = top + SC.CONTENT_Y0 * k
    y1 = top + SC.CONTENT_Y1 * k
    pill_top = cap_seat - CAP.CAP_PILL_HEIGHT / 2
    if y0 < 0.10 * H:
        raise SystemExit(f"{fmt}: core content starts at y={y0:.1f}, inside the "
                         f"top 10% ({0.10 * H:.0f}) — LAW 30")
    if y1 > pill_top - pill_clear:
        raise SystemExit(f"{fmt}: core content ends at y={y1:.1f}, within "
                         f"{pill_clear}px of the pill top {pill_top:.1f} — the "
                         "seam is sacred")
    return {"content_top": round(y0, 1), "content_bottom": round(y1, 1),
            "law30_top_10pct": 0.10 * H, "pill_top": round(pill_top, 2),
            "pill_height_used": CAP.CAP_PILL_HEIGHT,
            "clear_above_pill": round(pill_top - y1, 2),
            "plan_said": "142.7 px, derived from a pill CENTRED at 960 "
                         "(facesplit's split-mode seat).  The classic split's "
                         "seam is 862.5, fixed by the 1080x1058 face plate, so "
                         "the real clearance is the number above.  The ink does "
                         "not move: the plan's band clears the real seam too.",
            "note": "content_bottom is the FASTER key's box bottom, the lowest "
                    "ink authored anywhere in the video"}


def guard_rail(fmt: str, left: float, k: float) -> dict:
    """LAW 30's RIGHT RAIL, as amended in round 4.

    The rail (x > 918) is reserved for CAPTIONS and critical readable
    annotations; the COMPOSITION stays centred and symmetric.  This composition
    is mirror-symmetric about x = 540 at every instant, so the test is the
    widest READABLE TYPE — `GOOGLE MAPS`, whose box ends at core 887.
    """
    type_right = left + max(RIGIDS[k2][0][2] for k2 in RIGIDS
                            if k2.startswith("key-")) * k
    ink_left = left + min(b[0] for b, _ in RIGIDS.values()) * k
    ink_right = left + max(b[2] for b, _ in RIGIDS.values()) * k
    if type_right > CAP.LAW12_RAIL_X + 0.6:
        raise SystemExit(f"LAW 30: readable type reaches x={type_right:.1f}, "
                         f"inside the {CAP.LAW12_RAIL_X} rail")
    if ink_left < 20.0 or (W - ink_right) < 20.0:
        raise SystemExit(f"the composition's ink runs {ink_left:.1f}.."
                         f"{ink_right:.1f}, inside the 20px frame margin")
    axis = (ink_left + ink_right) / 2
    if abs(axis - W / 2) > 0.01:
        raise SystemExit(f"LAW 15: the composition's ink axis is {axis}, not "
                         f"the frame's own {W / 2}")
    return {"ink_left_x": round(ink_left, 1), "ink_right_x": round(ink_right, 1),
            "readable_type_right_x": round(type_right, 1),
            "law30_rail_x": CAP.LAW12_RAIL_X,
            "composition_axis_x": round(axis, 2),
            "margins": [round(ink_left, 1), round(W - ink_right, 1)],
            "note": "the FINISHED composition's ink extents are symmetric about "
                    "x=540 to 0.00 px, with 176 px of margin each side and no "
                    "readable annotation anywhere in the rail.  The ONE "
                    "deliberately off-axis element is the plug in beats 0-2: it "
                    "OPENS centred on 540 and displaces left to seat into the "
                    "plate, which is LAW 19's own prescribed choreography and "
                    "not a LAW 15 drift (LAW 15 governs an element MEDIATING "
                    "between two anchors, and the plug mediates nothing)."}


def sfx_levels() -> dict:
    out = {}
    for s in ("whoosh", "pop", "click"):
        r = subprocess.run(
            ["ffmpeg", "-v", "info", "-i", str(F / f"assets/sfx/{s}.mp3"),
             "-af", "volumedetect", "-f", "null", "-"],
            capture_output=True, text=True)
        mean = next((ln.split("mean_volume:")[1].strip()
                     for ln in r.stderr.splitlines() if "mean_volume:" in ln), "?")
        out[s] = {"mean_volume": mean}
    out["_gains"] = {"structure": SFX_STRUCTURE, "detail": SFX_DETAIL,
                     "published_corpus_flat": 0.18,
                     "note": "the run-9/12/13/14 shipped values for THESE "
                             "FILES: a gain constant means nothing without its "
                             "source loudness (SFX LAW v2)"}
    return out


# EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22).  The two
# emphases take ONE soft sound between them, because they are ONE event.
SFX = [("pop", SC.CUE["plug"], SFX_STRUCTURE),           # THE PLUG
       ("whoosh", SC.CUE["slide"], SFX_DETAIL),          # the displacement
       ("pop", SC.CUE["plate"], SFX_STRUCTURE),          # the Gemini plate
       ("click", SC.CUE["seat"], SFX_DETAIL),            # THE SEAT
       ("click", SC.CUE["keyterm"], SFX_DETAIL),         # THE GEMINI API
       ("click", SC.CUE["lineL"], SFX_DETAIL),           # the left line
       ("pop", SC.CUE["tileL"], SFX_DETAIL),             # the Google mark
       ("click", SC.CUE["keyL"], SFX_DETAIL),            # GOOGLE SEARCH
       ("click", SC.CUE["lineR"], SFX_DETAIL),           # the right line
       ("pop", SC.CUE["tileR"], SFX_DETAIL),             # the Maps pin
       ("click", SC.CUE["keyR"], SFX_DETAIL),            # GOOGLE MAPS
       ("whoosh", SC.CUE["charge"], SFX_STRUCTURE),      # THE CHARGE
       ("pop", SC.CUE["emph"], SFX_STRUCTURE),           # BOTH borders flip
       ("pop", SC.CUE["clock"], SFX_STRUCTURE),          # the stopwatch
       ("click", SC.CUE["sweep"], SFX_DETAIL),           # the hand sweeps
       ("click", SC.CUE["keyF"], SFX_DETAIL),            # FASTER
       ("whoosh", SC.CUE["outro"], SFX_STRUCTURE)]       # the rising sheet


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


# ------------------------------------------------------------------ placement
def phone_objects(left: float, top: float, k: float) -> list[dict]:
    """The scene's TWO bespoke objects, mapped into THIS format's frame.

    The Phone Test crops each of these alone at 405x720 and a fresh judge names
    it.  The BOXES are measured off the placement, never guessed: only this file
    knows where the core landed on the canvas.  On the classic split k = 1 and
    left = 0, so they come out identical to the plan's own normalised bboxes —
    and the build asserts exactly that, because a silent divergence would mean
    the cold namer was shown something the plan never designed.
    """
    out = []
    for o in SC.BESPOKE:
        x0, y0, x1, y1 = o["core"]
        out.append({
            "name": o["name"], "t": o["t"], "space": "norm",
            "bbox": [round((left + x0 * k) / W, 4), round((top + y0 * k) / H, 4),
                     round((left + x1 * k) / W, 4), round((top + y1 * k) / H, 4)],
        })
    return out


def assert_phone_boxes(objs: list[dict]) -> dict:
    """The plan's own `bespoke_objects` bboxes, re-derived from the placement.

    `phone_test_page.py --plan` crops from the PLAN; this build crops the same
    pixels only if the placement puts the plan's canvas rects where the plan
    said.  Asserting it is what makes `--plan` safe to pass.
    """
    plan = json.loads((RUN / "plans/geminitools_plan.json").read_text())
    want = plan["bespoke_objects"]
    if len(want) != len(objs):
        raise SystemExit(f"the plan declares {len(want)} bespoke objects, the "
                         f"scene declares {len(objs)}")
    rep = []
    for a, b in zip(want, objs):
        if a["name"] != b["name"]:
            raise SystemExit(f"bespoke object name drift: {a['name']!r} vs "
                             f"{b['name']!r}")
        d = [round(abs(x - y) * (W if i % 2 == 0 else H), 2)
             for i, (x, y) in enumerate(zip(a["bbox"], b["bbox"]))]
        if max(d) > 1.0:
            raise SystemExit(f"{a['name']}: the built box is {d} px off the "
                             f"plan's — the cold namer would see a crop the "
                             f"plan never designed")
        rep.append({"name": a["name"], "t": b["t"], "plan_bbox": a["bbox"],
                    "built_bbox": b["bbox"], "max_delta_px": max(d)})
    return {"objects": rep,
            "note": "k = 1.0 and left = 0 on the classic split, so the plan's "
                    "canvas rects ARE this format's canvas rects"}


def build_split(out: Path, handle: str) -> dict:
    staged = stage(out, face="face_bottom_hd.mp4")
    if (staged["face"]["w"], staged["face"]["h"]) != (1080, 1058):
        raise SystemExit(f"the face plate is {staged['face']} — the split's "
                         "seam is derived from a 1080x1058 HD plate")
    ws = words()
    anchors = assert_anchor_law()
    lifetimes = assert_lifetime_law()
    keyterm = assert_key_term()
    emphasis = assert_emphasis_law()
    spacing = assert_spacing_law()
    labels = assert_label_law()
    cues = assert_cues(ws)
    law37 = assert_law37(ws)
    scene_html, tweens = SC.build(scene_media(), outro_lockup(handle))
    k = 1.0
    left = (W - SC.CORE_W * k) / 2
    top = CORE_TOP_SPLIT
    m = CAP.PillMeasurer(RUN / "gen/_pillwidths.json")
    beats, cap_rep = caption_beats(m)
    CAP.assert_law12(SEAM, max(b["w"] for b in beats))
    band = guard_core_band("split", top, k, SEAM)
    rail = guard_rail("split", left, k)
    objs = phone_objects(left, top, k)
    phone = assert_phone_boxes(objs)

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
            "law40": anchors, "law40_charge": SC.assert_charge_clearance(),
            "law42": lifetimes, "law9": keyterm,
            "law38": emphasis, "law41": spacing, "law39": labels,
            "law37": law37, "cues": cues,
            "transcript": cap_rep, "marks_ink": mark_ink_report(),
            "phone_test_objects": objs, "phone_test_parity": phone,
            "render": {"w": 1080, "h": 1920, "zoom": 1}}


# ------------------------------------------------------------------ main
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="split", choices=("split",))
    ap.parse_args()

    dst = RUN / "projects/geminitools_split"
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
    report = {"video": VID, "lane": "icon choreography", "fps": FPS,
              "duration": DUR, "seam": SEAM, "sfx": sfx_levels(),
              "cutout_cast_for_the_other_author": list(CUTOUT_CAST),
              "formats": {"split": rep}}
    (RUN / "gen/_build_geminitools.json").write_text(json.dumps(report, indent=1))
    # the geometry record every downstream tool reads, so a contact sheet or a
    # phone test never has to re-derive a box this file already measured
    geom = {"video": VID, "fps": FPS, "duration": DUR,
            "shared": {"beat_edges": SC.BEAT_EDGES,
                       "phone_test_objects": rep["phone_test_objects"]},
            "formats": {"split": {"phone_test_objects": rep["phone_test_objects"],
                                  "core": rep["core"], "scale": rep["scale"],
                                  "seat": rep["seat"],
                                  "voice": rep["staged"]["voice"]}}}
    (RUN / f"gen/_geom_{VID}.json").write_text(json.dumps(geom, indent=1))
    print(f"split: {dst}")
    print(json.dumps({k: v for k, v in report.items() if k != "sfx"}, indent=1))


if __name__ == "__main__":
    main()
