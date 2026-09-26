"""TAKEOVER — FIX ROUND 6.  THE CLOSING CAPTIONS ROUND.  Task id: takeover6.

TWO changes, both about the caption pill, and NOTHING else in the picture.

1. THE SHRINK FORMULA IS DEAD.  `cap_font` inherited the published factory's
   length-based sizing, `round(max(35.6, min(56.25, 1578.3/len(text))), 1)`.  It
   is replaced by the single canonical size, `P.CAP_FONT` = 56.2px = px(30) in
   the published 576-wide design space, and by a real SPLITTER: a phrase too
   wide for its seat is cut at a word boundary into more beats, using the
   transcript's own word timestamps.  Nothing is ever squeezed or widened.

   The formula was already INERT in this format and round 6 proves it instead of
   claiming it.  Algebraically: `build_captions` closes a group as soon as the
   next word would push the estimate past 756px, which happens at 21 characters,
   and the formula only starts shrinking past 28.  Empirically: round 5's render
   measures ONE type size across 134 captioned frames.  So the approved round-5
   caption track survives this round byte-for-byte — 58 phrases, same text, same
   timings — and `split_phrases` logs ZERO splits, with the widest pill measured
   at 714.6px against a 756px seat (41.4px of headroom).

2. THE PILL IS THE CANONICAL PILL.  Round 5 carried a near-copy of the published
   geometry: `padding:19px 34px; border-radius:22px`.  The published object is
   `font-size:56.2px; padding:18.8px 33.8px; border-radius:22.5px` on #C4573A,
   Nunito 800, white, nowrap, `translateY(-50%)` — i.e. px(30)/px(10)/px(18)/
   px(12) at the factory's S=1.875.  Round 6 imports those numbers from
   `takeover_fix6_pill.py` rather than retyping them, so every format that
   imports the same module is pill-identical by construction.

   The pill is 114.59px tall (56.2px type at line-height normal + 2 x 18.8px),
   which at the unchanged seat CAP_Y=1318 puts it at 1260.7-1375.3 — bottom
   71.63% of frame height, inside LAW 12's 72%.  THE SEAT DOES NOT MOVE.

The 21/79 balance, the growing beat curve, the centred illustrations, the RAW 0%
full-bleed face with zero punches, the SFX schedule, the ghost rule, 25fps and
every approved content beat are inherited from round 5 untouched.

-------------------------------------------------------------------------------
INHERITED HEADER (fix round 5)
-------------------------------------------------------------------------------
ONE change, and only one: **every illustration is centred in the space above the
caption pill.**  Miguel, round 5: *centre the illustrations in the space above
the captions* — which both centres them for the viewer and gives them presence.

Nothing else moves.  The caption seat stays exactly where round 4 put it (pill
1258-1378, bottom 71.6% of frame height) because 72% is the platform-safety
limit and it cannot go lower.  The 21/79 face/illustration balance, the growing
beat curve, the SFX schedule, the RAW 0% full-bleed face, the ghost rule, LAW 11
fills, 25fps, the palette and every approved content beat are inherited.

-------------------------------------------------------------------------------
1. THE REGION, AND THE 74px THAT WERE NEVER THERE
-------------------------------------------------------------------------------
An illustration owns everything above the pill: **[0, 1258), centre 629**.

Every round up to 4 seated its scenes on `C.MID = 704`, the centre of the LAW 12
*content band* [192, 1214] — the region minus the top-10% platform strip and
minus 44px of clearance above the pill.  Those two subtractions are not
symmetric, so the band's centre sits 75px below the region's, and a picture
centred in the band is a picture pushed down toward the captions.

That is not a theory: `takeover_fix5_centroid.py` decoded every frame of
`out/takeover_fix4.mp4`, found each section's ground as its modal luma, called
everything more than 18 levels away from it ink, and measured the empty ground
above and below each of the seven compositions.

    unit              above   below     optical centre    off 629
    flash               568     429              698.5      +69.5
    toolwall            300     143              707.5      +78.5
    term card           588     421              712.5      +83.5
    ON DEMAND field     289     168              689.5      +60.5
    finite              402     245              707.5      +78.5
    portal              231     211              639.0      +10.0
    outro card          389     274              686.5      +57.5

Six of the seven carried roughly TWICE the empty ground above them as below.
That is the defect, stated in pixels.

-------------------------------------------------------------------------------
2. WHY THE SEAT IS DRIVEN BY THE OPTICAL CENTRE, NOT THE INK MASS
-------------------------------------------------------------------------------
Round 5 was asked to prove the fix with a measured vertical CENTROID, and the
instrument reports one — but it is not what the seats are derived from, because
the measurement itself shows the ink-mass centroid is the wrong ruler:

    outro card    ink spans 389-991 (centre 690)    ink mass at 812
    finite        ink spans 402-1013 (centre 708)   ink mass at 792

The outro's 122px gap is a single element: the solid INK @handle chip, the only
filled black shape on a cream card.  Seating by ink mass would have driven the
card 122px too high and left a 450px hole beneath it — trading Miguel's
complaint for its mirror image.  So the seat is driven by `optical_centre`, the
median-per-frame ink bounding-box midpoint, which is what equalises the
whitespace an eye actually reads.  Both numbers are reported before and after.

-------------------------------------------------------------------------------
3. THE SEATS ARE DERIVED, NEVER TYPED
-------------------------------------------------------------------------------
`ANCHORS` below is not a table of chosen numbers.  Each seat is

    seat = 704 (what fix4 used) - (that unit's measured offset from 629)

read at build time out of `_centroid_before_fix4.json`.  A translation moves a
composition's optical centre by exactly the translation, so one pass lands each
unit on 629; the round-5 check re-measures the finished MP4 to prove it rather
than assuming it.

`takeover_fix5_core.py` makes the seat a per-scene parameter (`mid`, plus
`mid_field` for the term takeover, which is ONE takeover but TWO pictures either
side of its internal hard cut, 249px of cream type and then an 800px dark
field — they cannot share a seat).  `C.MID` survives as the default, so fix4's
geometry still reproduces through the same functions.

-------------------------------------------------------------------------------
4. WHAT THE MOVE MUST NOT BREAK
-------------------------------------------------------------------------------
Moving a picture up is only safe while it stays out of the top 10% (y < 192),
where the phone's own status bar and the platform's chrome live.  The narrowest
clearance after the move is the portal's in-flight feed at y=199, 7px inside the
line, and the guard that proves it is the one already in `sc_portal` — it raises
rather than clipping.  The authored-geometry sweep in `audit()` re-checks every
sized atom in the page against [192, 1214], and the check script re-checks the
finished pixels.

-------------------------------------------------------------------------------
INHERITED HEADER (fix round 4)
-------------------------------------------------------------------------------
ONE change, and only one: the 55/45 takeover/face balance becomes ~79/21.

Miguel, round 4: *"more time for the illustrations than my face — maybe a 25/75
split"*, with two guards agreed in the brief: **the HOOK stays his face** (the
first beat opens on him — brand and human entry) and **ONE short face return
(~2s) lands before the final line** so the ending is a person.  Between those,
the illustrations own the video.

Everything else is inherited from fix round 3 unchanged: the RAW 0% full-bleed
face with zero punches, the LAW 12 caption seat (CAP_Y 1318, pill bottom 71.6%),
the tamed SFX palette at its pinned class gains, the fixed lemniscate, 25fps,
the palette, the scene interiors and every approved content beat.

-------------------------------------------------------------------------------
1. WHERE THE TIME WENT — the arithmetic, before the cut map
-------------------------------------------------------------------------------
fix3: face 24.28s / 54.04 = 44.9%, takeovers 29.76s = 55.1%, six face runs.
fix4 keeps ALL SIX approved scenes and deletes FOUR of the six face runs.

The two guards bound the answer exactly.  The term card debuts at 13.20 (its
approved seat: it must land on "What does that mean?" so the plate never carries
the words the pill is carrying — LAW 4), so the hook block is 0.00-13.20.  It
contains the format's two hook illustrations, the flash (1.64s) and the toolwall
(2.42s).  That leaves

    hook face   = 13.20 - 1.64 - 2.42 = 9.16s
    return face = 2.04s   ("~2s", on "which is just unbelievable")
    face total  = 11.20s = 20.7% of 54.04

**20.7% is the CEILING under the agreed guards, not a choice.**  Landing exactly
on 25.0% needs 13.51s of face, i.e. 2.3s more, and there are only three places
to find it: a third face beat mid-video (the brief forbids it — "between those,
the illustrations own the video"), a ~4s "short" return (it is specified as
~2s), or dropping the toolwall takeover so the hook face runs 3.14-13.20 in one
10.06s block (that lands on 25.2% — and deletes an approved scene, which round 4
explicitly forbids: "everything content-level is approved").  The brief's
direction is MORE illustration, so the ceiling is the right side to miss on.

-------------------------------------------------------------------------------
2. THE CUT MAP — fewer, longer, and the escalation is now the whole spine
-------------------------------------------------------------------------------
    face      0.00 - 1.52   1.52   HOOK opens on him
    FLASH     1.52 - 3.16   1.64   (unchanged)
    face      3.16 - 4.60   1.44
    TOOLWALL  4.60 - 7.00   2.40   (unchanged)
    face      7.00 - 13.20  6.20   the setup, ending on the term he is about to
                                   see on a plate
    TERM      13.20 - 20.00 6.80   was 3.94 — the ON DEMAND field now answers
                                   FOUR times at ~1.2s instead of three at 0.62
    FINITE    20.00 - 29.72 9.72   was 5.94 — the stack climbs for 2.6s onto
                                   "context is finite" and the picky DRAIN falls
                                   top-down for 4.4s onto "give access to"
    PORTAL    29.72 - 40.60 10.88  was 8.66 — opens ON "the people over at Nous
                                   Research" (fix3 opened 2.2s late), 7 waves
    GIVE      40.60 - 48.72 8.12   the stack-feed portal that used to be the
                                   outro's 3.84s prelude, standing on its own
    face     48.72 - 50.76  2.04   THE RETURN — "which is just unbelievable"
    OUTRO    50.76 - 54.04  3.28   the card, on the SAME frame as fix3 (50.76)

GROWING is intact and stronger: 1.64 -> 2.40 -> 6.80 -> 9.72 -> 10.88, then the
coda 8.12 -> 3.28.  Picture changes drop 13 -> 11 (Morgane's "limite toutes les
secondes"), and the longest face run drops 6.32 -> 6.20.

-------------------------------------------------------------------------------
3. LAW 16 — longer takeovers are not longer HOLDS
-------------------------------------------------------------------------------
Three scenes finished their motion in under 2s because every takeover used to be
short.  `takeover_fix4_core.py` makes their pacing a function of the span they
are given (see its header): the ON DEMAND answer count, the finite stack's climb
and the finite drain's stagger and order.  The portal's wave count is derived
here, from the same 0.98s/wave density fix3 shipped, and capped at 7 — at 8
waves the `wv * 23` rotation puts two feed seats 1.4px outside the LAW 12 safe
column, which the build guard rejects.

-------------------------------------------------------------------------------
4. SFX — one event per picture change, still
-------------------------------------------------------------------------------
Four of the six takeovers now hand over to ANOTHER takeover instead of to the
face, so a `reverse_air` release on those frames would double up with the next
takeover's seize whoosh on the same frame — two SFX, one event, which SFX LAW v2
forbids.  A release now fires only where the frame actually goes back to him.
The three `low_thump`s still mark the three longest takeovers' entrances, which
in this map are exactly the three takeover-to-takeover cuts.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "lib"))
sys.path.insert(0, str(HERE.parent.parent / "pipeline"))
import captions as CAP                                        # noqa: E402
import takeover_fix6_core as C                                # noqa: E402

VID = "takeover"
TITLE = "Hermes Agent — infinite tools (TAKEOVER / fix round 6)"

# --- CHASSIS PARAMETERS (promoted out of the lab, 2026-09-01) ----------------
# `HOME` is the lab: round-6 source material, READ ONLY.  Everything this
# chassis writes lands under `formats/takeover/`.
HOME = C.HOME
STAGE = C.STAGE                            # formats/takeover/stage
OUT_ROOT = C.OUT_ROOT                      # formats/takeover/build
OUT = OUT_ROOT

# ROUND 6 — the canonical pill, and the instrument that measures it.
P = C.P
MEASURER = P.PillMeasurer(HERE / "lib/_pillwidths.json")
SPLIT_LOG: list[dict] = []

FPS = 25                                   # GLOBAL LAW 6
W, H = C.W, C.H

# ---------------------------------------------------------------------------
# SFX LAW v2 — unchanged from fix round 1.  NEVER hand-set a gain (SFX.md 1).
# ---------------------------------------------------------------------------
SFX_DIR = C.SHARED / "sfx"
SFX_CLASS = {
    "soft_whoosh": "structure",
    "reverse_air": "structure",
    "low_thump": "structure",
    "tick": "detail",
    "pop": "detail",
}
CLASS_VOLUME = {"structure": "0.120", "detail": "0.077", "loop": "0.038"}

# ---------------------------------------------------------------------------
# FRAMING — GLOBAL LAW 7 as amended by Miguel's round-3 ruling.  ONE plate:
# the RAW 0% window, full-bleed, for every face second of the video.  No 5%,
# no 10%, no ladder, no punches — "punches deferred until the new lens".  The
# number is read from the standard, never retyped.
# ---------------------------------------------------------------------------
ZSTD = json.loads((C.SHARED / "zoom_standard.json").read_text())
ZLEVELS = {lv["level_pct"]: lv for lv in ZSTD["levels"]}

_L0 = ZLEVELS[0]
if _L0["ffmpeg_crop"] != "crop=1216:2160:1270:0":
    raise SystemExit(f"the 0% window moved: {_L0['ffmpeg_crop']}")
if not _L0["contains_head_union"] or _L0["frames_head_clipped"]:
    raise SystemExit("the 0% window clips the head union")

REST = "z00"
PLATES: dict[str, dict] = {REST: {
    "file": "face_z00.mp4", "pct": 0,
    "h": float(H), "top": 0.0,
    "crop": _L0["ffmpeg_crop"],
    "head_frac": _L0["head_frac_of_1920"],
    "face_frac": _L0["face_frac_of_1920"],
}}
# ROUND 3: exactly one level exists, so a "zoom" is unrepresentable.
assert len(PLATES) == 1 and PLATES[REST]["pct"] == 0


# ---------------------------------------------------------------------------
# frame arithmetic — ONE integer frame drives both the picture and its sound
# ---------------------------------------------------------------------------
def fr(t: float) -> int:
    return int(math.floor(t * FPS + 0.5))


def ft(f: int) -> float:
    return round(f / FPS, 2)


def fq(t: float) -> float:
    """Snap a time onto the 25fps grid."""
    return ft(fr(t))


# ---------------------------------------------------------------------------
# THE CUT MAP — ROUND 4.  Same six scenes, four fewer face runs, and the outro's
# stack-feed prelude promoted to a takeover of its own so the ~2s face return
# can land between it and the card.
#
# GROWING: 1.64 -> 2.40 -> 6.80 -> 9.72 -> 10.88, coda 8.12 -> 3.28.
# `waves` is DERIVED in build() from fix3's shipped 0.98s/wave density.
# ---------------------------------------------------------------------------
CUTS = [
    {"scene": "flash", "ground": C.INK, "t0": 1.50, "t1": 3.14,
     "seats": {"mid": "flash"}},
    {"scene": "toolwall", "ground": C.INK_2, "t0": 4.58, "t1": 7.00,
     "seats": {"mid": "toolwall"}},
    {"scene": "term", "ground": C.CREAM, "t0": 13.20, "t1": 20.00,
     "kw": {"split": 15.14},
     "seats": {"mid": "term_card", "mid_field": "ondemand_field"}},
    {"scene": "finite", "ground": C.CREAM, "t0": 20.00, "t1": 29.70,
     "kw": {"picky_at": 23.60},
     "seats": {"mid": "finite"}},
    # ONE portal, held open for 19s.  Round 4's first pass gave the give-up
    # beat its own takeover at 40.60 and MEASURED the result: the frame-to-frame
    # jump at that "cut" was 1.36 against 80-198 at every real cut, i.e. the
    # picture did not change — two portals back to back tear the same door down
    # and rebuild it, and the whoosh+thump scored a frame with no visual event
    # (SFX LAW v2).  The stack feed is now a SECOND PHASE of the same portal:
    # nothing rebuilds, the cut count drops again, and the door staying open
    # while first the world's tools and then his own MCP servers pass through
    # is a better reading of the claim than cutting between two doors.
    {"scene": "portal", "ground": C.INK_2, "t0": 29.70, "t1": 48.70,
     "kw": {"inf_at": 38.30, "stack_from": 40.58},
     "seats": {"mid": "portal"}},
    # ROUND 4: the outro section's ground is CREAM, not INK_2.  fix3's outro
    # opened on the INK_2 prelude; fix4's opens on the card, and `cut_on` lands
    # one frame after the clip boundary — measured, 50.76 read as bare ground
    # and 50.80 as the card, a one-frame dark flash between his face and the
    # cream.  Grounding the section in the card's own colour removes it.
    {"scene": "outro", "ground": C.CREAM, "t0": 50.74, "t1": None,
     "seats": {"mid": "outro_card"}},
]

# ---------------------------------------------------------------------------
# ROUND 5 — THE SEATS.  Derived, never typed.
#
# Every scene in fix4 was seated on C.MID, so a unit measured `off` pixels below
# the region's centre is fixed by seating it at `C.MID - off`.  A translation
# moves an optical centre by exactly the translation, so this lands each unit on
# REGION_MID in one pass — and the check script re-measures the finished MP4
# rather than taking that on faith.
# ---------------------------------------------------------------------------
BEFORE = HERE / "lib/_centroid_baseline.json"   # the fix4 measurement the
#                                                seats were derived from
SEAT_BASELINE = C.MID                      # what fix4 seated every scene on


def anchors() -> dict[str, dict]:
    if not BEFORE.exists():
        raise SystemExit(f"{VID}: no baseline measurement at {BEFORE} — run "
                         f"takeover_fix5_centroid.py on out/takeover_fix4.mp4")
    data = json.loads(BEFORE.read_text())
    if abs(data["region_mid"] - C.REGION_MID) > 1e-6:
        raise SystemExit(f"{VID}: the instrument measured against region mid "
                         f"{data['region_mid']}, the chassis says {C.REGION_MID}")
    out = {}
    for u in data["units"]:
        out[u["unit"]] = {
            "seat": round(SEAT_BASELINE - u["optical_offset"], 1),
            "was_optical": u["optical_centre"],
            "was_mass": u["mass_centroid"],
            "offset_applied": round(-u["optical_offset"], 1),
            "was_margin_above": u["margin_above"],
            "was_margin_below": u["margin_below"],
            "predicted_ink_top": round(u["ink_top_ever"] - u["optical_offset"], 1),
        }
    return out


ANCHORS = anchors()
# Every seat must keep its scene's highest ink out of the top 10%.  This is the
# arithmetic check on the PREDICTION; sc_portal's own guard and audit()'s
# geometry sweep check the authored result, and the check script checks pixels.
for _u, _a in ANCHORS.items():
    if _a["predicted_ink_top"] < C.TOP:
        raise SystemExit(f"{VID}: seating {_u} at {_a['seat']} would push ink to "
                         f"y={_a['predicted_ink_top']}, inside the top 10%")

# kwargs that are TIMES and must be quantised onto the frame grid.  A seat is a
# COORDINATE: quantising 634.5 as if it were a timestamp would silently reseat
# every scene onto the 25fps grid.
TIME_KW = {"split", "picky_at", "inf_at", "stack_from", "prelude_until"}

# fix3's approved portal: stream 32.42-38.30 carried 6 waves = 0.98s per wave.
# The cap is a LAW 12 fact, not taste: at 8 waves the `wv * 23` rotation lands
# two feed seats at x=160.6 and x+w=919.4, 1.4px outside the 162-918 column.
WAVE_PER = 0.98
WAVE_CAP = 7


def waves_for(stream_t0: float, stream_end: float) -> int:
    return max(3, min(WAVE_CAP, int(round((stream_end - stream_t0) / WAVE_PER))))

# ---------------------------------------------------------------------------
# THE FACE MODE MAP — ROUND 3: there isn't one.  Every face second is the RAW
# 0% window.  The list is kept (one entry) so the run/level bookkeeping and its
# guards stay live rather than being deleted along with the punches.
# ---------------------------------------------------------------------------
MODES = [(0.00, REST)]


# ---------------------------------------------------------------------------
# staging
# ---------------------------------------------------------------------------
FACE_PLATE_SHA = "6a8a9aaae534ff4dee52791fc6cd977998034006e55ac8562c6351327b0622c4"


def stage_assets() -> dict[str, str]:
    for rel in ["v", "music", "sfx", "logos"]:
        (STAGE / rel).mkdir(parents=True, exist_ok=True)
    for spec in PLATES.values():
        src = STAGE / "v" / spec["file"]
        if not src.exists():
            # ROUND 6 touches CAPTIONS ONLY, so the plate is not rebuilt: it
            # is carried over from the previous round's stage.  The digest is
            # asserted so "the face is inherited untouched" is a checked fact.
            prev = next((q for q in (HOME / "stage_fix6/v" / spec["file"],
                                     HOME / "stage_fix5/v" / spec["file"],
                                     HOME / "stage_fix4/v" / spec["file"])
                        if q.exists()), HOME / "stage_fix5/v" / spec["file"])
            if not prev.exists():
                raise SystemExit(f"missing face plate: {prev} "
                                 f"(run takeover_fix3_plates.py)")
            shutil.copy2(prev, src)
        digest = hashlib.sha256(src.read_bytes()).hexdigest()
        if digest != FACE_PLATE_SHA:
            raise SystemExit(f"the 0% face plate changed: {digest}")
    shutil.copy2(HOME / "media/audio.m4a", STAGE / "v/audio.m4a")
    shutil.copy2(C.FACTORY / "assets/music/bed_split_v2.mp3", STAGE / "music/bed.mp3")
    for name in SFX_CLASS:
        shutil.copy2(SFX_DIR / f"{name}.mp3", STAGE / "sfx" / f"{name}.mp3")
    media: dict[str, str] = {}
    for key, source in C.LOGO_FILES.items():
        if not source.exists():
            raise SystemExit(f"missing registry asset: {source}")
        shutil.copy2(source, STAGE / "logos" / f"{key}{source.suffix}")
        media[key] = f"assets/logos/{key}{source.suffix}"
    return media


def load_words() -> tuple[list[dict], float]:
    data = json.loads((C.SRC / "transcript_words.json").read_text())
    words = [w for w in data["words"] if w.get("type") == "word"]
    raw = min(words[-1]["end"] + C.TAIL_LEAD,
              min(C.probe(STAGE / "v" / p["file"]) for p in PLATES.values()),
              C.probe(STAGE / "v/audio.m4a"))
    return words, ft(int(math.floor(raw * FPS)))       # whole frames only


# ---------------------------------------------------------------------------
# the face — three crop levels, one visible at a time, switched by single-frame
# `set`s.  All three occupy the SAME full-bleed window, so nothing can expand.
# ---------------------------------------------------------------------------
def face_html(dur: float) -> str:
    parts = [f'  <div class="abs" id="ground" style="left:0;top:0;width:{W}px;'
             f'height:{H}px;background:{C.INK}"></div>']
    for i, (mode, spec) in enumerate(PLATES.items()):
        parts.append(
            f'  <div class="abs" id="fw-{mode}" style="left:0;top:{spec["top"]:.1f}px;'
            f'width:{W}px;height:{spec["h"]:.1f}px;overflow:hidden;opacity:0">'
            f'<video id="face-{mode}" src="assets/v/{spec["file"]}" data-start="0" '
            f'data-duration="{dur:.2f}" data-media-start="0" data-track-index="{1+i}" '
            f'muted playsinline style="position:absolute;left:0;top:0;width:{W}px;'
            f'height:{spec["h"]:.1f}px;object-fit:cover"></video></div>')
    return "\n".join(parts)


def face_tweens(cuts: list[dict], modes: list[tuple[float, str]]
                ) -> tuple[list[str], list[dict]]:
    events: list[tuple[float, str | None]] = [(t, m) for t, m in modes]
    for c in cuts:
        events.append((c["t0"], None))                 # the frame is seized
    events.sort(key=lambda e: (e[0], e[1] is not None))

    tw: list[str] = []
    for t, mode in events:
        for name in PLATES:
            tw.append(f'tl.set("#fw-{name}",{{opacity:{1 if name == mode else 0}}},'
                      f'{t:.2f});')
    segs = []
    for i, (t, mode) in enumerate(events):
        if mode is None:
            continue
        nxt = events[i + 1][0] if i + 1 < len(events) else None
        segs.append({"t": t, "mode": mode, "until": nxt})
    return tw, segs


# ---------------------------------------------------------------------------
# audio — AUDIO MIX LAW + SFX LAW v2 (inherited from fix round 1)
# ---------------------------------------------------------------------------
def ondemand_tick_times(t0_field: float, t1: float, n: int) -> list[float]:
    """DERIVED, not typed.  Mirrors `field_ondemand` exactly.  ROUND 4: `n` is
    no longer defaulted — it comes from `C.ondemand_lit`, which is the same
    function the core used to decide how many plates answer."""
    span = max(0.55, (t1 - t0_field - 0.25) / n)
    return [t0_field + 0.05 + k * span + 0.22 for k in range(n)]


def audio_block(dur: float, hits: list[tuple[float, str]]) -> tuple[str, list[str]]:
    els = [f'  <audio id="vo" src="assets/v/audio.m4a" data-start="0" '
           f'data-duration="{dur:.2f}" data-track-index="30" '
           f'data-volume="{C.VOICE_VOLUME}"></audio>']
    bed_len = C.probe(C.FACTORY / "assets/music/bed_split_v2.mp3")
    starts, t, i = [], 0.0, 0
    while t < dur - 0.1:
        d = min(bed_len, dur - t)
        starts.append((f"bg{i}", t))
        els.append(f'  <audio id="bg{i}" src="assets/music/bed.mp3" data-start="{t:.2f}" '
                   f'data-duration="{d:.2f}" data-track-index="{31+i}" '
                   f'data-volume="{C.BED_VOLUME}"></audio>')
        t += bed_len
        i += 1
    lens = {n: C.probe(SFX_DIR / f"{n}.mp3") for n in SFX_CLASS}
    for j, (t0, name) in enumerate(sorted(hits)):
        if t0 >= dur - 0.12:
            continue
        vol = CLASS_VOLUME[SFX_CLASS[name]]
        els.append(f'  <audio id="sfx{j}" src="assets/sfx/{name}.mp3" '
                   f'data-start="{t0:.2f}" data-duration="{min(lens[name], dur-t0):.2f}" '
                   f'data-track-index="{60+j}" data-volume="{vol}"></audio>')
    tw = [f'tl.to("#{starts[-1][0]}",{{volume:0,duration:1.45}},'
          f'{max(starts[-1][1], dur-1.5):.2f});']
    return "\n".join(els), tw


# ---------------------------------------------------------------------------
# build
# ---------------------------------------------------------------------------
def build(m: dict[str, str]) -> tuple[str, dict]:
    words, dur = load_words()
    bounds = C.word_boundaries(words)

    def on_word(t: float, what: str) -> None:
        if t >= dur - 0.05:
            return
        if min(abs(t - b) for b in bounds) > 1.0 / (2 * FPS) + 1e-6:
            raise SystemExit(f"{VID}: {what} at {t:.2f} is not a word boundary")

    # ---- quantise the cut map onto the frame grid, then re-validate ---------
    cuts: list[dict] = []
    prev_end = 0.0
    for i, c in enumerate(CUTS):
        t0 = fq(c["t0"])
        t1 = dur if c["t1"] is None else fq(c["t1"])
        kw = {k: (fq(v) if (k in TIME_KW and isinstance(v, float)) else v)
              for k, v in c.get("kw", {}).items()}
        # ROUND 5 — the seats, attached here so the cut map stays a cut map.
        for arg, unit in c.get("seats", {}).items():
            if unit not in ANCHORS:
                raise SystemExit(f"{VID}: no measured seat for unit {unit!r}")
            kw[arg] = ANCHORS[unit]["seat"]
        on_word(t0, f"takeover {i} entrance")
        on_word(t1, f"takeover {i} exit")
        if t0 < prev_end:
            raise SystemExit(f"{VID}: takeover {i} overlaps the previous one")
        if t1 - t0 < 1.2:
            raise SystemExit(f"{VID}: takeover {i} is {t1-t0:.2f}s — below the floor")
        prev_end = t1
        if c["scene"] == "portal":
            # DERIVED wave counts: fix3's shipped 0.98s/wave density, applied to
            # whatever stream window each phase actually has.  Phase 1 runs from
            # t0+0.50 to inf_at (or t1-0.55 with no lemniscate payoff); phase 2,
            # the stack, from `stack_from` to t1-0.55.
            stream_end = kw.get("inf_at") if kw.get("inf_at") else t1 - 0.55
            kw["waves"] = waves_for(t0 + 0.50, stream_end)
            sf = kw.pop("stack_from", None)
            if sf is not None:
                kw["stack"] = (sf, t1 - 0.55, waves_for(sf, t1 - 0.55))
        cuts.append({**c, "t0": t0, "t1": t1, "kw": kw})

    beats = [round(c["t1"] - c["t0"], 2) for c in cuts]
    if beats[:5] != sorted(beats[:5]):
        raise SystemExit(f"{VID}: the GROWING curve is broken: {beats}")
    # ROUND 4 — the balance is the deliverable, so it is ASSERTED, not reported.
    cover = sum(c["t1"] - c["t0"] for c in cuts)
    if cover / dur < 0.72:
        raise SystemExit(f"{VID}: takeovers hold {cover/dur:.1%} — round 4 wants ~75%+")

    # ---- face runs: v2's floor -------------------------------------------
    runs, prev = [], 0.0
    for c in cuts:
        if c["t0"] - prev > 0.05:
            runs.append((round(prev, 2), round(c["t0"], 2)))
        prev = c["t1"]
    if dur - prev > 0.05:
        runs.append((round(prev, 2), round(dur, 2)))
    for a, b in runs:
        if b - a > 7.0:
            raise SystemExit(f"{VID}: face run {a}-{b} is {b-a:.2f}s — over the 7s floor")

    # ---- the face level: ONE, declared at the head of every face run -------
    # ROUND 3 (Miguel): "full-face = the regular RAW 0% crop, punches deferred".
    # The level is not a decision any more, so it is DERIVED from the runs
    # instead of typed — a punch cannot be smuggled back in by editing a table.
    declared = {mode for _, mode in MODES}
    if declared != {REST}:
        raise SystemExit(f"{VID}: round 3 allows only the 0% level, got {declared}")
    modes = [(a, REST) for a, _ in runs]
    for t, mode in modes:
        on_word(t, f"face reveal -> {mode}")
        if not any(a - 0.001 <= t < b for a, b in runs):
            raise SystemExit(f"{VID}: face reveal at {t:.2f} is inside a takeover")
    if modes[0][0] != 0.0 or modes[0][1] != REST:
        raise SystemExit(f"{VID}: the video must open on the 0% standard")
    if len(modes) != len(runs):
        raise SystemExit(f"{VID}: {len(modes)} reveals for {len(runs)} face runs")

    face_tw, segs = face_tweens(cuts, modes)

    # ---- scenes ------------------------------------------------------------
    tw: list[str] = []
    secs: list[str] = []
    for i, c in enumerate(cuts):
        fn = C.SCENES[c["scene"]]
        inner, stw = fn(f"s{i}", c["t0"], c["t1"], m, **c["kw"])
        secs.append(C.section(f"s{i}", i, c["t0"], c["t1"], inner, c["ground"]))
        tw += stw

    # ---- SFX: one integer frame drives the picture and the sound -----------
    hits: list[tuple[float, str]] = []
    exits = set()
    seizes = {round(c["t0"], 2) for c in cuts}
    for c in cuts:
        hits.append((c["t0"], "soft_whoosh"))                 # SEIZE
        # ROUND 4: a RELEASE is the frame going back to HIM.  Four of the six
        # takeovers now hand over to another takeover, and that frame already
        # carries the next takeover's seize whoosh — a reverse_air there would
        # be a second SFX on one event, which SFX LAW v2 forbids.
        if c["t1"] < dur - 0.25 and round(c["t1"], 2) not in seizes:
            hits.append((c["t1"], "reverse_air"))             # RELEASE
            exits.add(round(c["t1"], 2))
        for key in ("split", "prelude_until"):                # internal hard cuts
            if c["kw"].get(key) is not None:
                hits.append((c["kw"][key], "soft_whoosh"))
    # low_thump.  fix2 spent it on crop cuts into the CEILING; round 3 has no
    # crop cuts, and an SFX with no visual event under it is exactly what SFX
    # LAW v2 forbids.  It is NOT deleted — the escalation has to stay audible —
    # it is repointed onto the escalation itself: the entrance of the three
    # LONGEST takeovers, layered under the seize whoosh already on that frame.
    # Same palette, same pinned class gain, one event per hit, 5 -> 3 hits.
    big = sorted(cuts, key=lambda c: (c["t1"] - c["t0"]), reverse=True)[:3]
    thumps = sorted(c["t0"] for c in big)
    if any(round(t, 2) in exits for t in thumps):
        raise SystemExit(f"{VID}: a thump landed on a release: {thumps}")
    hits += [(t, "low_thump") for t in thumps]
    # the ON DEMAND answers, derived from the core's own arithmetic.  ROUND 4:
    # the COUNT is derived too — the field is 4.96s long now, so it answers
    # four times, and the tick schedule follows the plates rather than a 3.
    term = next(c for c in cuts if c["scene"] == "term")
    lit = C.ondemand_lit(term["kw"]["split"] - 0.10, term["t1"])
    ticks = [fq(t) for t in ondemand_tick_times(term["kw"]["split"] - 0.10,
                                                term["t1"], len(lit))]
    hits += [(t, "tick") for t in ticks]
    # the infinity resolving inside the portal — one detail, one arrival
    portal = next(c for c in cuts if c["kw"].get("inf_at") is not None)
    hits.append((fq(portal["kw"]["inf_at"]), "pop"))

    hits = [(fq(t), n) for t, n in hits]
    for t, _ in hits:                                  # frame lock, hard assert
        if abs(t * FPS - round(t * FPS)) > 1e-6:
            raise SystemExit(f"{VID}: SFX at {t} is off the {FPS}fps grid")

    # ---- ROUND 6: ONE SIZE, AND A SPLITTER INSTEAD OF A SHRINK -------------
    # `build_captions` chunks on the conservative estimate (unchanged, so the
    # approved round-5 caption TEXT survives byte-for-byte); `split_phrases`
    # then measures every finished phrase as a real 56.2px Chromium pill and
    # splits at word boundaries anything that misses the 756px seat.  The log is
    # empty when the chunker was already sufficient — which is the claim, and it
    # is now a measured one rather than an assumed one.
    phrases = C.build_captions(words)
    phrases, split_log = C.split_phrases(phrases, MEASURER)
    SPLIT_LOG[:] = split_log
    audio, atw = audio_block(dur, hits)
    tw = face_tw + tw + atw

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width={W}, height={H}"/>
<title>{C.esc(TITLE)}</title>{C.GSAP}{C.FONTS}<style>{C.base_css()}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="{W}"
 data-height="{H}" data-duration="{dur:.2f}" data-fps="{FPS}">
{face_html(dur)}
{chr(10).join(secs)}
{C.caption_clips(phrases, dur)}
{audio}
</div><script>
window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});
const POP="back.out(2.05)";const SOFT="power3.out";const EXIT="power3.in";
{''.join(tw)}
window.__timelines["main"]=tl;
</script></body></html>"""

    report = audit(page, "\n".join(secs), phrases, cuts, runs, segs, hits, ticks, dur)
    return page, report


# ---------------------------------------------------------------------------
# lab guards
# ---------------------------------------------------------------------------
def guard_ghost_rule(page: str) -> dict:
    """GHOST RULE — zero visible ink at birth, on EVERY dash draw-on.

    Three things must hold:
      1. every element authored with `stroke-dasharray` also carries
         `stroke-opacity:0`, so its rest state paints nothing at all (a round
         linecap on a fully-offset dash paints a DOT — that is the defect);
      2. every `strokeDashoffset` tween has a matching `strokeOpacity` reveal on
         the same selector, so nothing is drawn while still invisible;
      3. no reveal lands ON its draw's start frame — at progress 0 the only ink
         a dash draw can paint is the cap.
    """
    authored = re.findall(r'<(?:path|circle) id="([^"]+)"[^>]*style="([^"]*)"', page)
    if not authored:
        raise SystemExit("GHOST RULE: no dash draw-on found — guard is not looking")
    for eid, style in authored:
        if "stroke-dasharray" in style and "stroke-opacity:0" not in style:
            raise SystemExit(f"GHOST RULE: #{eid} is born with visible ink")
    draws = {sel: float(t) for sel, t in re.findall(
        r'tl\.fromTo\("([^"]+)",\{strokeDashoffset:100\},\{strokeDashoffset:0,'
        r'[^}]*\},([\d.]+)\)', page)}
    reveals = {sel: float(t) for sel, t in re.findall(
        r'tl\.fromTo\("([^"]+)",\{strokeOpacity:0\},\{strokeOpacity:1,'
        r'[^}]*\},([\d.]+)\)', page)}
    if set(draws) != set(reveals):
        raise SystemExit(f"GHOST RULE: draw/reveal mismatch "
                         f"{sorted(set(draws) ^ set(reveals))}")
    for sel, t in draws.items():
        gap = reveals[sel] - t
        if not (0.0 < gap < 1.0 / FPS):
            raise SystemExit(f"GHOST RULE: {sel} reveal is {gap:+.3f}s from its "
                             f"draw — must land inside the first frame")
    # every authored glyph that is NEVER drawn must stay invisible forever
    never = [eid for eid, _ in authored if f'"#{eid}"' not in page]
    return {"draw_ons": len(authored), "drawn": len(draws),
            "never_drawn_and_invisible": len(never)}


def audit(page: str, secs: str, phrases: list[dict], cuts: list[dict],
          runs: list[tuple[float, float]], segs: list[dict],
          hits: list[tuple[float, str]], ticks: list[float], dur: float) -> dict:
    # AUDIO MIX LAW + SFX LAW v2 (class gains, never a hand-set number)
    if re.search(r'id="vo"[^>]*data-volume="1"', page) is None:
        raise SystemExit("voice track must be data-volume=1")
    for v in set(re.findall(r'id="bg\d+"[^>]*data-volume="([^"]+)"', page)):
        if v != C.BED_VOLUME:
            raise SystemExit(f"bed volume {v} violates the AUDIO MIX LAW")
    for src, vol in re.findall(r'id="sfx\d+" src="assets/sfx/([a-z_]+)\.mp3" '
                              r'data-start="[\d.]+" data-duration="[\d.]+" '
                              r'data-track-index="\d+" data-volume="([^"]+)"', page):
        want = CLASS_VOLUME[SFX_CLASS[src]]
        if vol != want:
            raise SystemExit(f"SFX LAW v2: {src} at {vol}, class constant is {want}")
    if len(re.findall(r'id="sfx\d+"', page)) != len([h for h in hits if h[0] < dur - 0.12]):
        raise SystemExit("SFX schedule lost an entry")
    if "swarm" in page or "tk_in" in page or "tk_out" in page:
        raise SystemExit("a retired SFX member is still referenced")

    # SYNC: every ON DEMAND tick must match the tween the core emitted
    term_i = next(i for i, c in enumerate(cuts) if c["scene"] == "term")
    term_c = cuts[term_i]
    lit = C.ondemand_lit(term_c["kw"]["split"] - 0.10, term_c["t1"])
    if len(lit) != len(ticks):
        raise SystemExit(f"{len(ticks)} ticks for {len(lit)} ON DEMAND answers")
    for k, idx in enumerate(lit):
        pat = (rf'tl\.to\("#s{term_i}f-t{idx}",\{{opacity:1,duration:0\.16,'
               rf'ease:"none"\}},([\d.]+)\)')
        found = re.search(pat, page)
        if not found:
            raise SystemExit(f"could not locate the ON DEMAND light tween for plate {idx}")
        visual = float(found.group(1))
        if abs(visual - ticks[k]) > 1.0 / FPS + 1e-6:
            raise SystemExit(f"tick {k} at {ticks[k]:.2f} is >1 frame from its "
                             f"visual event at {visual:.2f}")

    # GLOBAL LAW 7 / ROUND 2: a zoom is a CROP CUT.  Nothing may scale a face
    # plate, and no plate may be seated differently from the others — identical
    # geometry is what makes a cut a punch instead of an expansion.
    if re.search(r'"#(face|fw)-[a-z0-9]+"[^)]*scale', page):
        raise SystemExit("a face plate is being scaled — ROUND 2 forbids expansion")
    face_seats = re.findall(r'id="fw-[a-z0-9]+" style="left:0;top:([\d.]+)px;'
                            r'width:(\d+)px;height:([\d.]+)px', page)
    # ROUND 3: exactly ONE face window exists, so there is nothing to cut between.
    if len(face_seats) != 1:
        raise SystemExit(f"round 3 allows exactly one face plate, found "
                         f"{len(face_seats)}: {face_seats}")
    if face_seats[0] != ("0.0", str(W), f"{float(H):.1f}"):
        raise SystemExit(f"face window {face_seats[0]} is not the full-bleed 0% frame")
    if len(re.findall(r'id="face-[a-z0-9]+"', page)) != 1:
        raise SystemExit("more than one face video element is authored")
    if 'src="assets/v/face_z00.mp4"' not in page:
        raise SystemExit("the RAW 0% plate is not the face source")

    ghost = guard_ghost_rule(page)

    # GLOBAL LAW 11: rounded-bar fills are ONE continuous pill driven by width
    if re.search(r'#[a-z0-9]+-fill",\{scaleX', page):
        raise SystemExit("GLOBAL LAW 11: a meter fill is driven by scaleX")
    for pfx, (tw_, th_) in C.METERS.items():
        for w in re.findall(rf'"#{pfx}-fill",\{{width:"0px"\}},'
                            rf'\{{width:"([\d.]+)px"', page):
            if float(w) < th_ - 1e-6:
                raise SystemExit(f"GLOBAL LAW 11: {pfx} fill rests at {w}px, "
                                 f"thinner than its {th_}px track — a sliver")

    # LAW 4 — nothing on a takeover repeats what the pill is saying under it
    atoms = re.findall(r'>([A-Za-z@][A-Za-z0-9 .@\-]{2,40})</div>', secs)
    atoms += re.findall(r'>([A-Za-z@][A-Za-z0-9 .@\-]{2,40})</span>', secs)
    allw = [w for p in phrases for w in C.norm(p["text"])]
    spoken3 = {tuple(allw[i:i + 3]) for i in range(len(allw) - 2)}
    echoes = []
    for a in set(atoms):
        n = C.norm(a)
        if len(n) >= 3 and tuple(n[:3]) in spoken3:
            echoes.append(a)
        for p in phrases:
            if n and C.norm(p["text"]) == n:
                echoes.append(a)
    if echoes:
        raise SystemExit(f"caption echo on screen: {sorted(set(echoes))}")
    if len(allw) < 180:
        raise SystemExit(f"captions carry only {len(allw)} words")
    # ---- GLOBAL LAW 12 ----------------------------------------------------
    # (a) ONE caption seat for the whole video, and it is the safe one.
    cap_seats = set(re.findall(r'class="clip scap" style="top:([\d.]+)px"', page))
    if cap_seats != {f"{C.CAP_Y:.1f}"}:
        raise SystemExit(f"LAW 12: the caption moves between modes: {sorted(cap_seats)}")
    if C.CAP_Y + C.CAP_HALF > 0.72 * H:
        raise SystemExit(f"LAW 12: pill bottom {C.CAP_Y + C.CAP_HALF:.0f} is below "
                         f"{0.72 * H:.0f}")
    # (b) the pill never leaves the column the platform UI leaves alone.
    #     ROUND 6: judged on the MEASURED Chromium layout, not the estimate.
    #     The estimate is still reported next to it so the gap stays visible.
    MEASURER.want([p["text"] for p in phrases])
    MEASURER.resolve()
    for p in phrases:
        w = MEASURER.width(p["text"])
        if w > C.CAP_MAX_W:
            raise SystemExit(f"LAW 12: pill {w:.1f}px wide (max {C.CAP_MAX_W:.0f}) "
                             f"for {p['text']!r} — the splitter did not close it")
    widest = max(phrases, key=lambda q: MEASURER.width(q["text"]))
    # (c) nothing the takeovers draw may enter the pill's band, the top 10%, or
    #     the right column.  Measured on the finished MP4 by the check script;
    #     asserted here on the authored geometry of every sized, non-full-bleed
    #     element (full-frame grounds and masks are containers, not content).
    # id-anchored: only TOP-LEVEL positioned atoms.  A tile's logo <img> and a
    # plate_mark's <img> are positioned in their PARENT's coordinates, so a
    # naive left/top sweep reads them as elements at y=24 and fails the top-10%
    # test on geometry that is actually 300px down the frame.
    boxes = re.findall(r'id="[^"]+" style="left:(-?[\d.]+)px;top:(-?[\d.]+)px;'
                       r'width:([\d.]+)px;height:([\d.]+)px', secs)
    if len(boxes) < 150:
        raise SystemExit(f"LAW 12: geometry guard only saw {len(boxes)} boxes")
    bad = []
    for x, y, w, h in boxes:
        x, y, w, h = float(x), float(y), float(w), float(h)
        if w >= W:              # a ground, a full-frame mask, a centred type box
            continue
        if y < C.TOP - 0.6 or y + h > C.BOT + 0.6:
            bad.append(("v", x, y, w, h))
        if x < -0.6 or x + w > W + 0.6:
            continue            # a FEED tile parked off-frame, flying inward
        if x < C.SAFE_L - 0.6 or x + w > C.SAFE_R + 0.6:
            bad.append(("h", x, y, w, h))
    if bad:
        raise SystemExit(f"LAW 12: {len(bad)} elements outside the safe zones: "
                         f"{bad[:6]}")

    # ---- ROUND 5: THE SEATS ------------------------------------------------
    # (a) every scene that owns a picture must have been handed a measured seat.
    #     A scene falling back on C.MID is the exact defect this round fixes, so
    #     it fails the build rather than shipping quietly.
    seated = {(i, arg): c.get("seats", {}).get(arg)
              for i, c in enumerate(cuts) for arg in c.get("seats", {})}
    if len(seated) != 7:
        raise SystemExit(f"ROUND 5: {len(seated)} seats declared, the video has "
                         f"seven compositions")
    for c in cuts:
        for arg in c.get("seats", {}):
            if arg not in c["kw"]:
                raise SystemExit(f"ROUND 5: {c['scene']}.{arg} never reached the scene")
            if abs(c["kw"][arg] - C.MID) < 1e-9:
                raise SystemExit(f"ROUND 5: {c['scene']}.{arg} fell back to C.MID")
    # (b) a seat is a coordinate, so it must not have been snapped to the frame
    #     grid on its way through the quantiser.
    for c in cuts:
        for arg in c.get("seats", {}):
            v = c["kw"][arg]
            if abs(v * FPS - round(v * FPS)) < 1e-9 and abs(v - round(v)) > 1e-9:
                raise SystemExit(f"ROUND 5: seat {c['scene']}.{arg}={v} looks quantised")
    # (c) the caption seat is UNCHANGED from round 4 — round 5 moves pictures,
    #     never the pill, and the pill is already at the platform-safety limit.
    if C.CAP_Y != 1318.0 or C.CAP_HALF != 60.0:
        raise SystemExit(f"ROUND 5: the caption seat moved to {C.CAP_Y}+-{C.CAP_HALF}")
    # (d) NEW LAW (round 5): ONE caption font size for the whole video.
    cap_sizes = set(re.findall(r'class="scappill" style="font-size:([\d.]+)px"', page))
    if len(cap_sizes) != 1:
        raise SystemExit(f"ROUND 5: {len(cap_sizes)} caption font sizes: "
                         f"{sorted(cap_sizes)}")

    # ---- ROUND 6: THE CANONICAL CAPTION SPEC -------------------------------
    # (a) the one size is THE one size — the published factory's px(30).
    if float(next(iter(cap_sizes))) != P.CAP_FONT:
        raise SystemExit(f"ROUND 6: caption size is not {P.CAP_FONT}px")
    if C.cap_font("x") != P.CAP_FONT or C.cap_font("a" * 60) != P.CAP_FONT:
        raise SystemExit("ROUND 6: cap_font still varies with length")
    # (b) the pill geometry is the published one, byte for byte, in the CSS.
    css = C.base_css()
    for want in (f"font-size:{P.CAP_FONT}px",
                 f"padding:{P.CAP_PAD_Y}px {P.CAP_PAD_X}px",
                 f"border-radius:{P.CAP_RADIUS}px",
                 f"background:{P.CAP_BG}", f"color:{P.CAP_FG}",
                 f"font-family:{P.CAP_FAMILY}", f"font-weight:{P.CAP_WEIGHT}",
                 "white-space:nowrap", "transform:translateY(-50%)"):
        if want not in css:
            raise SystemExit(f"ROUND 6: the pill is not canonical — missing {want!r}")
    # (c) no inline style may re-declare pill geometry other than the size.
    inline = re.findall(r'class="scappill" style="([^"]*)"', page)
    if any(re.sub(r'font-size:[\d.]+px;?', "", s).strip() for s in inline):
        raise SystemExit("ROUND 6: a caption pill carries inline geometry")
    # (d) the splitter, not a shrink, is what closes an oversized phrase.
    for entry in SPLIT_LOG:
        for piece in entry["into"]:
            if MEASURER.width(piece) > C.CAP_MAX_W:
                raise SystemExit(f"ROUND 6: split beat still too wide: {piece!r}")
    if any(len(p["words"]) == 1 and MEASURER.width(p["text"]) > C.CAP_MAX_W
           for p in phrases):
        raise SystemExit("ROUND 6: a single word overflows the seat — it cannot "
                         "be split at a word boundary and must not be shrunk")

    cover = sum(c["t1"] - c["t0"] for c in cuts)
    by_mode: dict[str, float] = {}
    for s in segs:
        by_mode[s["mode"]] = round(
            by_mode.get(s["mode"], 0.0) + (s["until"] or dur) - s["t"], 2)
    face_total = sum(by_mode.values())
    if set(by_mode) != {REST}:
        raise SystemExit(f"ROUND 3: the face is not all 0%: {by_mode}")
    cut_times = sorted({round(t, 2) for t in
                        [c["t0"] for c in cuts] +
                        [c["t1"] for c in cuts if c["t1"] < dur - 0.05] +
                        [c["kw"][k] for c in cuts for k in
                         ("split", "prelude_until") if c["kw"].get(k)]})
    return {
        "video": VID, "fps": FPS, "duration": dur,
        "takeovers": len(cuts),
        "scenes": [c["scene"] + ("/stack" if c["kw"].get("feed") == "stack" else "")
                   for c in cuts],
        "beats": [round(c["t1"] - c["t0"], 2) for c in cuts],
        "takeover_seconds": round(cover, 2),
        "takeover_share": round(cover / dur, 3),
        # ROUND 4 — the deliverable number, both ways round.
        "balance": {
            "face_seconds": round(dur - cover, 2),
            "face_share": round((dur - cover) / dur, 3),
            "illustration_seconds": round(cover, 2),
            "illustration_share": round(cover / dur, 3),
            "fix3_face_share": 0.449,
            "face_runs_kept": len(runs),
            "fix3_face_runs": 6,
            "hook": [runs[0][0], runs[0][1]],
            "return": [runs[-1][0], runs[-1][1]],
        },
        "face_runs": [round(b - a, 2) for a, b in runs],
        "longest_face_run": round(max(b - a for a, b in runs), 2),
        "face": {
            "levels": {k: {"pct": p["pct"], "crop": p["crop"],
                           "head_frac": p["head_frac"], "face_frac": p["face_frac"]}
                       for k, p in PLATES.items()},
            "crop_cuts": 0,
            "punches": 0,
            "seconds_by_level": by_mode,
            "rest_share": 1.0,
        },
        "law12": {
            "cap_y": C.CAP_Y,
            "pill_top": C.CAP_Y - C.CAP_HALF,
            "pill_bottom": C.CAP_Y + C.CAP_HALF,
            "pill_bottom_pct": round((C.CAP_Y + C.CAP_HALF) / H, 4),
            "pill_centre_pct": round(C.CAP_Y / H, 4),
            "seats": sorted(cap_seats),
            "widest_pill_px": round(C.cap_w(widest["text"]), 1),
            "widest_pill_text": widest["text"],
            "content_band": [C.TOP, C.BOT],
            "safe_column": [C.SAFE_L, C.SAFE_R],
            "boxes_checked": len(boxes),
        },
        # ---- ROUND 6 — the deliverable numbers --------------------------
        "round6_caption_spec": {
            "font_px": P.CAP_FONT,
            "font_design_units": "px(30) at the factory's S=1.875",
            "padding_px": [P.CAP_PAD_Y, P.CAP_PAD_X],
            "radius_px": P.CAP_RADIUS,
            "background": P.CAP_BG,
            "colour": P.CAP_FG,
            "family": P.CAP_FAMILY,
            "weight": P.CAP_WEIGHT,
            "pill_height_px": round(MEASURER.height, 2) if MEASURER.height else None,
            "seat_top_px": C.CAP_Y,
            "seat_is_pill_centre": True,
            "pill_top_px": round(C.CAP_Y - (MEASURER.height or 0) / 2, 1),
            "pill_bottom_px": round(C.CAP_Y + (MEASURER.height or 0) / 2, 1),
            "pill_bottom_pct": round(
                (C.CAP_Y + (MEASURER.height or 0) / 2) / H, 4),
            "font_sizes_in_page": sorted(cap_sizes),
            "phrases": len(phrases),
            "phrases_split_by_the_splitter": len(SPLIT_LOG),
            "split_log": SPLIT_LOG,
            "widest_pill_measured_px": round(MEASURER.width(widest["text"]), 1),
            "widest_pill_estimate_px": round(C.cap_w(widest["text"]), 1),
            "widest_pill_text": widest["text"],
            "seat_budget_px": C.CAP_MAX_W,
            "measured_headroom_px": round(
                C.CAP_MAX_W - MEASURER.width(widest["text"]), 1),
        },
        # ROUND 5 — the deliverable, stated as the seats and where they came from
        "seats": {
            "region": [0.0, C.PILL_TOP],
            "region_mid": C.REGION_MID,
            "fix4_seat_for_every_scene": C.MID,
            "band_mid_minus_region_mid": round(C.MID - C.REGION_MID, 1),
            "baseline_measurement": BEFORE.name,
            "units": {u: {"seat": a["seat"],
                          "moved_up_px": round(-a["offset_applied"], 1),
                          "fix4_optical_centre": a["was_optical"],
                          "fix4_mass_centroid": a["was_mass"],
                          "fix4_margin_above": a["was_margin_above"],
                          "fix4_margin_below": a["was_margin_below"],
                          "predicted_ink_top": a["predicted_ink_top"]}
                      for u, a in ANCHORS.items()},
        },
        "pacing": {
            "cut_times": cut_times,
            "cuts": len(cut_times),
            "fix3_cuts": 13,
            "min_gap": round(min(b - a for a, b in zip(cut_times, cut_times[1:])), 2),
        },
        "ghost_rule": ghost,
        "captions": len(phrases),
        "sfx": {"count": len(hits),
                "by_name": {n: sum(1 for _, x in hits if x == n) for n in SFX_CLASS},
                "schedule": sorted([[t, n] for t, n in hits])},
    }


def write_project(page: str) -> Path:
    project = OUT_ROOT / VID
    project.mkdir(parents=True, exist_ok=True)
    dest = project / "assets"
    if dest.is_symlink() or dest.exists():
        dest.unlink() if dest.is_symlink() else shutil.rmtree(dest)
    dest.symlink_to(STAGE.resolve(), target_is_directory=True)
    (project / "index.html").write_text(page, encoding="utf-8")
    return project


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    CAP.add_handle_arg(ap)
    ap.add_argument("--out", default=None, help="project root (default: ./build)")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    C.HANDLE = CAP.handle(args.handle)     # the ONE parametrized constant
    global OUT_ROOT
    if args.out:
        OUT_ROOT = Path(args.out)

    media = stage_assets()
    page, report = build(media)
    project = write_project(page)
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / f"_report_{VID}.json").write_text(json.dumps(report, indent=2))
    print(f"project={project}  handle={C.HANDLE}")
    if not args.quiet:
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
