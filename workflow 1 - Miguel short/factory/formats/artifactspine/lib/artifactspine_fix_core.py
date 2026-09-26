"""ARTIFACT SPINE — FIX ROUND 1 shared core.

Authority: `references/laws/REVIEW_2026-08-30.md` (five global laws + the artifact
spine verdict), `_shared/FRAMING.md`, `_shared/SFX.md`, `_shared/ROUNDFILL_AUDIT.md`.
Underneath: `STANDARD.md`'s 20 laws.

Miguel kept the format ("Super NICE representation") and asked for four things:

  1. PACING — "sometimes the animation goes too fast and people cannot see
     everything".  Hold each beat to comprehension, not just to the word timing.
  2. NO PEEK-AHEAD (Global Law 4) — the next section must not be visible at the
     bottom edge before its words (his example: 05 -> 06 Nous Research).
  3. The v2 face switch-ins ("extra nice") stay.
  4. v3's page-zoom is promoted to an official variant, with its two bugs fixed.

Plus the global laws: 25 fps (6), tamed frame-locked SFX (2), rounded fills (3),
no unmotivated moves (5), derived zoom caps (1).

WHAT THIS FILE CHANGES vs `artifactspine_core.py` (which it imports and reuses
for every geometry / atom / region builder):

* **FPS 30 -> 25** and a face plate that is native 25 (Global Law 6).  The old
  build ran `face_full.mp4`, which is 25 fps conformed to 30 by duplicating one
  frame in six; full-window it stutters.  `face_std_25.mp4` has the duplicates
  removed and is the derived MID plate.
* **THE PAINT MODEL IS INVERTED — this is the pacing fix.**  The old build
  painted a region's chrome and then popped every item in on arrival, so each
  landing was a cascade of 8-20 entrances competing with the voice.  Here the
  document is a DOCUMENT: static content is authored painted, and only genuine
  STATE CHANGES animate (a chip flips, a switch turns on, a box unchecks, a
  meter fills, a claim is struck).  Roughly 90 entrance tweens become ~30 state
  tweens.  Nothing is lost visually, because in the scroll variant a region is
  physically off-screen until the spine brings it in (see next point) and in the
  zoom variant a per-region veil lifts as the camera lands.
* **NO PEEK-AHEAD IS ENFORCED BY GEOMETRY** in the scroll variant: the gap after
  region k is solved so that region k+1's top edge sits at or below the viewport
  bottom while the spine rests on region k.  Measured on the old build, at rest
  on 05 you could read 404 px of the 06 NOUS RESEARCH card — exactly what Miguel
  flagged.  Now it is 0 px by construction, and the guard re-derives it.
* **SFX v2** — the tamed palette at its pinned class levels, every cue quantised
  to a 25 fps frame, and no hand-tuned lead/lag offsets (the old files carried
  leading silence; these are onset-trimmed).
* **COUNTER FORMATTING** — `count_to` rounded before formatting.  The old proxy
  ran `v.toLocaleString('en-US')` on a float, so the "LOADED THIS TURN" readout
  painted `2.844` across its own `/ 247` limit.  Shot on artifactspine_v3.mp4 at
  t=17.25.  This is Miguel's loader-overflow bug and it hit every counter in the
  piece (`hd-num`, `r3-big`, `r6-num`).
* **A PACING GUARD** (`audit`) that parses the emitted timeline and fails the
  build on: anything starting inside a spine move, less than STILL_MOVE seconds
  of stillness before a move, or a region visible before its arrival.

Round fills (Global Law 3) are inherited already-fixed from `artifactspine_core`
(`fill()` / `fill_to()` reach by width) — this file does not reintroduce scaleX
on any `-fill` element, and the guard asserts it.
"""
from __future__ import annotations

import re
from pathlib import Path

import artifactspine_core as C

# ---- Global Law 6: this build is authored and rendered at native 25 ----------
FPS = 25
FRAME = 1.0 / FPS
C.FPS = FPS                       # C.page() reads the module global at call time

# ---- Global Law 1: the derived face plate -----------------------------------
# FRAMING.md §5.  `face_std_25.mp4` is 1080x1350 (MID plate, face_frac 0.301 on
# a 1080x1920 canvas).  It is presented `object-fit:cover` inside the format's
# 1000x1516 window, which is a full-height crop scaled by 1516/1350 = 1.123 —
# INSIDE the 1.15 within-mode punch cap (rule 3), landing at face_frac 0.338 /
# head_frac 0.435.  For comparison the old `face_full.mp4` in the same window
# measured face_frac 0.396 / head_frac 0.510, i.e. right on the reference reel's
# full-face median.  This is a 15% reduction, derived rather than guessed, and
# it is why the plate had to change rather than the window (the window is the
# format's ONE WINDOW law).
FACE_PLATE = "face_std_25.mp4"

# ---- Global Law 2: SFX v2, the tamed palette --------------------------------
SFX_STRUCTURE = "0.120"      # soft_whoosh · reverse_air · low_thump
SFX_DETAIL = "0.077"         # tick · page_turn · pop
SFX_CLASS = {"soft_whoosh": SFX_STRUCTURE, "reverse_air": SFX_STRUCTURE,
             "low_thump": SFX_STRUCTURE, "tick": SFX_DETAIL,
             "page_turn": SFX_DETAIL, "pop": SFX_DETAIL}
SFX_LEN = {"soft_whoosh": 0.27, "reverse_air": 0.34, "low_thump": 0.42,
           "tick": 0.32, "page_turn": 0.79, "pop": 0.42}

# ---- pacing constants (the answer to "it goes too fast") --------------------
MOVE_D = 0.72          # a spine move.  Was 0.62; the travel is now uniform.
STILL_MOVE = 0.38      # required stillness before a spine move starts
STILL_CUT = 0.16       # required stillness before a face cut
RISE_D = 0.42          # was 0.34 — every entrance is ~25% longer
POP_D = 0.40           # was 0.34
ANNO_IN_D = 0.36
ANNO_OUT_D = 0.28
ANNO_MIN_HOLD = 0.80   # an annotation ring must be legible, not a blink


def q(t: float) -> float:
    """Quantise to a 25 fps frame boundary.  SFX.md sync rule: the EVENT'S FRAME
    IS THE AUTHORITY, so every scheduled time is a real frame time."""
    return round(round(t * FPS) / FPS, 4)


# =============================================================================
# PATCHES ONTO THE INHERITED CORE
# =============================================================================
def count_to(eid: str, t: float, a: float, b: float, d: float, fmt: str = "int") -> str:
    """MIGUEL'S LOADER-OVERFLOW BUG.

    `artifactspine_core.count_to` drove a float proxy straight into
    `v.toLocaleString('en-US')`, whose default `maximumFractionDigits` is 3.  A
    counter running 0 -> 3 therefore painted `2.844` — four glyphs at 84 px in a
    slot sized for one — straight across its own `/ 247` denominator.  Confirmed
    by decoding `out/artifactspine_v3.mp4` at t=17.25.  The same defect ran in
    `hd-num` (0 -> 184,000) and `r6-num` (247 -> 21,400); it was simply less
    obvious there because those readouts have room.

    Rounding happens BEFORE formatting, so the glyph count can never exceed the
    glyph count of the end value."""
    f = ("v=>Math.round(v).toLocaleString('en-US')" if fmt == "int"
         else "v=>Math.round(v)+'%'")
    return (f'{{const o={{v:{a}}};const el=document.getElementById("{eid}");'
            f'const F={f};'
            f'tl.fromTo(o,{{v:{a}}},{{v:{b},duration:{d},ease:SOFT,immediateRender:false,'
            f'onUpdate:()=>{{el.textContent=F(o.v);}}}},{t:.2f});}}')


C.count_to = count_to          # region_tweens/header_tweens resolve it globally


def face_html(dur: float) -> str:
    """ONE face element in the SAME rect as the panel (format law 1), now on the
    derived MID plate at native 25 fps."""
    return (f'  <div class="clip" id="facewin" data-start="0" data-duration="{dur:.3f}" '
            f'data-track-index="50" style="left:{C.n(C.WIN_X)}px;top:{C.n(C.WIN_Y)}px;'
            f'width:{C.n(C.WIN_W)}px;height:{C.n(C.WIN_H)}px;border-radius:{C.n(C.WIN_R)}px;'
            f'overflow:hidden;background:{C.INK};box-shadow:0 26px 64px rgba(20,20,22,0.16)">'
            f'<video id="face" src="assets/v/{FACE_PLATE}" data-start="0" '
            f'data-duration="{dur:.3f}" data-media-start="0" muted playsinline '
            f'style="position:absolute;left:0;top:0;width:100%;height:100%;'
            f'object-fit:cover;object-position:center center"></video>'
            f'{C.outro_lockup()}</div>')


def load_timing() -> tuple[list[dict], float, dict[str, float]]:
    """Same anchors, but the duration is pinned to the 25 fps plate and lands on
    an exact frame boundary (1354 frames / 25 = 54.160 s)."""
    import json
    data = json.loads((C.SRC / "transcript_words.json").read_text())
    words = [w for w in data["words"] if w.get("type") == "word"]
    dur = min(C.probe(C.STAGE / "v/audio.m4a"), C.probe(C.STAGE / "v" / FACE_PLATE))
    dur = round(int(dur * FPS) / FPS, 3)

    def find(phrase: str) -> float:
        target = C.norm(phrase)
        for i in range(len(words)):
            raw = []
            for j in range(i, min(len(words), i + len(target) + 3)):
                raw.append(words[j]["text"])
                cand = C.norm(" ".join(raw))
                if cand == target:
                    return round(words[i]["start"], 2)
                if len(cand) > len(target):
                    break
        raise SystemExit(f"anchor not found: {phrase!r}")

    return words, dur, {k: find(v) for k, v in C.ANCHORS.items()}


def audio_block(dur: float, cues: list[tuple[float, str]]) -> tuple[str, list[str]]:
    """AUDIO MIX LAW + SFX LAW v2.  Voice 1, bed 0.065, and effects on their
    PINNED CLASS CONSTANT (structure 0.120 / detail 0.077) — never a hand-set
    gain (SFX.md builder rule 1).  Every cue is already frame-quantised by the
    caller and the files are onset-trimmed, so `data-start` needs no lead/lag
    correction: the old `t - 0.04` offsets are gone because they now
    double-count."""
    els = [f'  <audio id="vo" src="assets/v/audio.m4a" data-start="0" '
           f'data-duration="{dur:.3f}" data-track-index="70" '
           f'data-volume="{C.VOICE_VOLUME}"></audio>']
    bed_len = C.probe(C.STAGE / "music/bed_split.mp3")
    starts, t, i = [], 0.0, 0
    while t < dur - 0.1:
        d = min(bed_len, dur - t)
        starts.append((f"bg{i}", t))
        els.append(f'  <audio id="bg{i}" src="assets/music/bed_split.mp3" '
                   f'data-start="{t:.2f}" data-duration="{d:.2f}" '
                   f'data-track-index="{71 + i}" data-volume="{C.BED_VOLUME}"></audio>')
        t += bed_len
        i += 1
    for j, (t0, name) in enumerate(sorted(cues)):
        if t0 >= dur - 0.15 or t0 < 0:
            continue
        if abs(t0 - q(t0)) > 1e-6:
            raise SystemExit(f"SFX cue {name}@{t0} is not on a 25fps frame")
        els.append(f'  <audio id="sfx{j}" src="assets/sfx/{name}.mp3" '
                   f'data-start="{t0:.2f}" '
                   f'data-duration="{min(SFX_LEN[name], dur - t0):.2f}" '
                   f'data-track-index="{90 + j}" data-volume="{SFX_CLASS[name]}"></audio>')
    tw = [f'tl.to("#{starts[-1][0]}",{{volume:0,duration:1.45}},'
          f'{max(starts[-1][1], dur - 1.5):.2f});']
    return "\n".join(els), tw


# =============================================================================
# THE DOCUMENT — regions, with GLOBAL LAW 4 solved as geometry
# =============================================================================
PEEK_MARGIN = 8.0        # extra px so a hairline cannot ride the bottom fade
GAP_MIN = 150.0          # the old flat gap; the solver never goes below it

# The steps card documents the setting; with the document painted rather than
# popped, "WHEN THE TOGGLE IS ON" would be on screen while the toggle is still
# DISABLED — a document that contradicts itself (format law 3).  Retitled.
STEPS_LABEL_OLD = "WHEN THE TOGGLE IS ON"
STEPS_LABEL_NEW = "HOW IT WORKS"


def layout_scroll() -> dict:
    """Lay the seven regions into one vertical document, CENTRE each one in the
    window, and SOLVE the gaps so that no unspoken section is ever visible.

    GLOBAL LAW 4, as geometry rather than as a schedule.

    Two decisions, and they interlock:

    **(1) A region rests CENTRED, not pinned at a fixed 60 px lead.**  The old
    build parked every section 60 px from the top, so a short section left up to
    430 px of dead white below it — which is precisely the space the next
    section used to leak into.  Centring gives
    `lead_k = (VIEW_H - h_k) / 2` = 135 / 197 / 245 / 267 / 307 / 316 / 96 px of
    air above and below, and the page reads composed instead of top-heavy.

    **(2) The gap is solved from the two leads it sits between.**  `#doc` sits at
    `doc_top` inside a `VIEW_H` viewport and is translated by `-stops[k]`, and
    `stops[k] = top_k + doc_top - lead_k`, so resting on region k the visible
    slice of the document is `[top_k - lead_k, top_k - lead_k + VIEW_H)`.  Two
    conditions have to hold at once:

        no peek ahead:  top_{k+1} >= top_k - lead_k + VIEW_H + PEEK_MARGIN
        no bleed back:  top_k + h_k <= top_{k+1} - lead_{k+1} - PEEK_MARGIN

    which together reduce to `gap_k >= max(lead_k, lead_{k+1}) + PEEK_MARGIN`.
    The bleed-back half is not academic: solving for the forward direction alone
    lets 54 px of region 01's footer sit above region 02 once 02 is centred,
    because 02 is shorter and therefore leads deeper.

    Measured on the old build (flat GAP=150, 60 px lead) the forward violation
    ran 52 px (01 -> 02), 176, 272, 316, **396 px (05 -> 06, the transition
    Miguel named)** and 414 px.  Solved gaps: 205 / 253 / 275 / 315 / 324 / 324.

    Because the largest gap (324) is a quarter of the viewport, no frame of a
    move is ever blank — at least 996 px of real document is always on screen."""
    heights, htmls = [], []
    y = 0.0
    for k, region in enumerate(C.REGIONS):
        html, h = region(0.0, 0.0, C.DOC_W)          # measure at origin
        heights.append(h)
    leads = [max(0.0, (C.VIEW_H - h) / 2) for h in heights]
    doc_top = leads[0]
    gaps = [max(GAP_MIN, max(leads[k], leads[k + 1]) + PEEK_MARGIN)
            for k in range(len(heights) - 1)]

    parts, tops, y = [], [], 0.0
    for k, region in enumerate(C.REGIONS):
        html, h = region(0.0, y, C.DOC_W)
        if k == 1:
            if STEPS_LABEL_OLD not in html:
                raise SystemExit("region2 steps label moved — retitle guard stale")
            html = html.replace(STEPS_LABEL_OLD, STEPS_LABEL_NEW)
        parts.append(html)
        tops.append(y)
        if k < len(C.REGIONS) - 1:
            y += h + gaps[k]
    stops = [t + doc_top - l for t, l in zip(tops, leads)]
    if abs(stops[0]) > 1e-6:
        raise SystemExit(f"region 01 must rest at scroll 0, got {stops[0]}")

    for k in range(1, len(stops)):
        if stops[k] <= stops[k - 1]:
            raise SystemExit(f"non-monotonic scroll stops: {stops}")
        peek = (tops[k - 1] - leads[k - 1] + C.VIEW_H) - tops[k]
        if peek > 0:
            raise SystemExit(f"PEEK-AHEAD: {peek:.0f}px of region {k + 1} visible "
                             f"while resting on region {k}")
        back = (tops[k - 1] + heights[k - 1]) - (tops[k] - leads[k])
        if back > 0:
            raise SystemExit(f"BLEED-BACK: {back:.0f}px of region {k} still visible "
                             f"while resting on region {k + 1}")
    return {"parts": parts, "tops": tops, "stops": stops, "heights": heights,
            "leads": leads, "gaps": gaps, "doc_top": doc_top,
            "doc_h": stops[-1] - doc_top + C.VIEW_H}


# =============================================================================
# THE SCHEDULE — state changes only.  One place, both variants.
# =============================================================================
def rise(sel: str, t: float, d: float = RISE_D, dy: float = 20.0) -> str:
    return C.rise(sel, q(t), d, dy)


def pop(sel: str, t: float, d: float = POP_D) -> str:
    return C.pop(sel, q(t), d)


def anno(tw: list[str], sel: str, t_in: float, t_out: float) -> None:
    """A ring lands and is HELD long enough to read.  The old build had rings up
    for as little as 0.4 s and sometimes two at once; here they are sequential
    and each holds at least ANNO_MIN_HOLD."""
    if t_out - t_in < ANNO_MIN_HOLD:
        raise SystemExit(f"annotation {sel} held {t_out - t_in:.2f}s "
                         f"(< {ANNO_MIN_HOLD}s) — not readable")
    tw.append(C.anno_in(sel, q(t_in), ANNO_IN_D))
    tw.append(C.anno_out(sel, q(t_out), ANNO_OUT_D))
    # hard kill after the exit: a cold render worker can seek past a fade-out
    # and restore stale visibility (the renderer's own lint calls this out).
    tw.append(f'tl.set("{sel}",{{opacity:0}},{q(t_out) + ANNO_OUT_D:.2f});')


def state_tweens(a: dict[str, float], arr: list[float], tw: list[str], *,
                 intro_rows: bool) -> None:
    """Every genuine state change in the artifact, and nothing else.

    THE PACING MODEL.  The old `region_tweens` painted a region's items on
    arrival: 8 rows + 8 marks + 8 names + 8 counts + 8 chips + 8 labels for
    region 01 alone, 42 individual ticks for region 03, 20 elements for 05, 40
    for 07.  Each landing was a wall of entrances, and Miguel could not take it
    in.  Here the document simply EXISTS — it is a document — and the timeline
    only ever shows things CHANGING.  Static content is authored painted and is
    revealed by the spine (scroll geometry) or by a per-region veil (zoom).

    `intro_rows` is the one exception: at the hook cut the panel replaces the
    face, so region 01's rows still cascade in.  That cascade IS the artifact
    arriving, and it has 1.2 s of clear air before "loads every tool"."""
    T = C.TERRA
    N = len(C.SERVERS)

    # ---- 01 REGISTRY --------------------------------------------------------
    if intro_rows:
        for suffix in ("row{}", "m{}", "n{}", "c{}", "chip{}", "ct{}a"):
            sels = [f"#r1-{suffix.format(i)}" for i in range(N)]
            tw.append("".join(rise(s, 3.00 + i * 0.085, 0.40, 18.0)
                              for i, s in enumerate(sels)))
        tw.append(rise("#r1-more", 3.72, 0.40, 18.0))
    for i in range(N):
        tw.append(f'tl.set("#r1-ct{i}b",{{opacity:0}},0);')
        tw.append(f'tl.set("#r1-ct{i}c",{{opacity:0}},0);')
    # "loads every tool" — every chip flips READY -> LOADED
    for i in range(N):
        t = q(a["loads"] + i * 0.07)
        tw.append(f'tl.to("#r1-chip{i}",{{background:"{C.rgb(T)}",duration:0.24,'
                  f'ease:SOFT}},{t:.2f});')
        tw.append(C.swap(f"#r1-ct{i}a", f"#r1-ct{i}b", t + 0.04, 0.18))
    anno(tw, "#r1-ring", a["loads"] + 0.02, a["atonce"] - 0.12)      # 4.18 -> 5.02
    # "they don't" — the claim is struck and every chip goes cold.
    # fromTo, not to: the element carries a CSS `transform:scaleX(0.001)` and a
    # bare `tl.to` on scaleX makes the renderer's lint (rightly) warn that GSAP
    # will clobber the whole CSS transform.  fromTo owns both ends.
    # opacity must be in BOTH ends: a cold render worker restores the authored
    # hidden state, so a fromTo that only reveals in its from-vars can encode
    # invisible even when a sequential preview looks right.
    tw.append(f'tl.fromTo("#r1-strike",{{opacity:1,scaleX:0.001,'
              f'transformOrigin:"left center"}},{{opacity:1,scaleX:1,duration:0.36,'
              f'ease:SOFT,immediateRender:false}},{q(a["dont"]):.2f});')
    tw.append(f'tl.set("#r1-strike",{{opacity:0}},0);')
    for i in range(N):
        t = q(a["dont"] + 0.06 + i * 0.045)
        tw.append(f'tl.to("#r1-chip{i}",{{background:"{C.rgb(C.LINE_2)}",duration:0.22,'
                  f'ease:SOFT}},{t:.2f});')
        tw.append(C.swap(f"#r1-ct{i}b", f"#r1-ct{i}c", t, 0.16))

    # ---- 02 DISCLOSURE ------------------------------------------------------
    anno(tw, "#r2-ring", a["crack"] + 0.04, a["disclosure"] - 0.28)   # 9.60 -> 11.60
    d = q(a["disclosure"] + 0.60)                                     # ON "disclosure"
    tw.append(f'tl.to("#r2-tg-trk",{{background:"{C.rgb(T)}",borderColor:"{C.rgb(T)}",'
              f'duration:0.28,ease:SOFT}},{d:.2f});')
    tw.append(f'tl.to("#r2-tg-knb",{{x:58,background:"{C.rgb(C.WHITE)}",duration:0.32,'
              f'ease:POP}},{d:.2f});')
    tw.append(f'tl.to("#r2-card",{{borderColor:"{C.rgb(T)}",duration:0.32,ease:SOFT}},'
              f'{d:.2f});')
    tw.append('tl.set("#r2-stateb",{opacity:0},0);')
    tw.append(C.swap("#r2-statea", "#r2-stateb", d + 0.10, 0.20))
    # the setting turning on is what produces the cost, so the result band is
    # part of the SAME beat rather than a separate entrance 1.7s later
    for sel in ("#r2-res", "#r2-res-lb", "#r2-res-v"):
        tw.append(rise(sel, d + 0.04, 0.40, 18.0))

    # ---- 03 THIS TURN -------------------------------------------------------
    tw.append('tl.set("#r3-big",{opacity:0},0);')
    for i in range(3):
        t = a["seetools"] + 0.04 + i * 0.34        # 0.30 -> 0.34, one row per beat
        tw.append(pop(f"#r3-row{i}", t))
        tw.append(pop(f"#r3-bar{i}", t))
        tw.append(rise(f"#r3-n{i}", t + 0.06, 0.34, 12.0))
        tw.append(pop(f"#r3-chip{i}", t + 0.12, 0.34))
        tw.append(pop(f"#r3-ct{i}", t + 0.12, 0.34))
    tw.append(f'tl.to("#r3-big",{{opacity:1,duration:0.22,ease:SOFT}},'
              f'{q(a["seetools"] + 0.04):.2f});')
    tw.append(count_to("r3-big", q(a["seetools"] + 0.04), 0, 3, 1.10))
    anno(tw, "#r3-ring", a["needsthem"] + 0.06, a["needsthem"] + 0.86)  # 18.50 -> 19.30

    # ---- 04 CONTEXT ---------------------------------------------------------
    for sel in ("#r4-f1", "#r4-f2", "#r4-hard"):
        tw.append(f'tl.set("{sel}",{{opacity:0}},0);')
    tw.append(C.fill_to("r4-fill", q(a["consume"] + 0.88), 0.62, 0.80))   # "context,"
    tw.append(rise("#r4-f1", a["consume"] + 1.10, 0.34, 12.0))
    tw.append(rise("#r4-f2", a["consume"] + 1.10, 0.34, 12.0))
    tw.append(f'tl.fromTo("#r4-stop",{{opacity:0,scaleY:0.2,transformOrigin:"50% 50%"}},'
              f'{{opacity:1,scaleY:1,duration:0.32,ease:POP,immediateRender:false}},'
              f'{q(a["finiteword"]):.2f});')                             # "finite."
    tw.append(rise("#r4-hard", a["finiteword"] + 0.08, 0.34, 12.0))
    anno(tw, "#r4-ring", a["finiteword"] + 0.12, a["finiteword"] + 1.50)  # 22.48 -> 23.86

    # ---- 05 ACCESS ----------------------------------------------------------
    for j, i in enumerate([5, 3, 4]):               # Airtable, Slack, Gmail
        t = q(a["picky"] + 0.06 + j * 0.28)         # 0.22 -> 0.28, one per beat
        tw.append(f'tl.to("#r5-k{i}-bx",{{background:"{C.rgb(C.WHITE)}",'
                  f'borderColor:"{C.rgb(C.MUTED_D)}",duration:0.26,ease:SOFT}},{t:.2f});')
        tw.append(f'tl.to("#r5-k{i}-tk",{{opacity:0,duration:0.20,ease:EXIT}},{t:.2f});')
        tw.append(f'tl.set("#r5-k{i}-tk",{{opacity:0}},{t + 0.20:.2f});')   # hard kill
        for suf, o in (("c", 0.42), ("m", 0.32), ("n", 0.38)):
            tw.append(f'tl.to("#r5-{suf}{i}",{{opacity:{o},duration:0.30,ease:SOFT}},'
                      f'{t + 0.04:.2f});')
    tw.append('tl.set("#r5-subb",{opacity:0},0);')
    tw.append(C.swap("#r5-suba", "#r5-subb", q(a["picky"] + 0.90), 0.22))
    anno(tw, "#r5-ring", a["access"] + 0.06, a["access"] + 1.20)          # 27.80 -> 28.94

    # ---- 06 NOUS RESEARCH — the peak beat -----------------------------------
    tw.append('tl.set("#r6-flatlb",{opacity:0},0);')
    anno(tw, "#r6-ring2", a["nous"] + 0.06, a["lab"] + 1.18)             # 30.84 -> 33.10
    tw.append(count_to("r6-num", q(a["everneed"] + 0.10), C.TOTAL_TOOLS, 21400, 1.30))
    tw.append('tl.set("#r6-inf",{opacity:0},0);')
    tw.append(f'tl.to("#r6-num",{{opacity:0,duration:0.08,ease:EXIT}},'
              f'{q(a["everneed"] + 1.50):.2f});')
    tw.append(f'tl.fromTo("#r6-inf",{{opacity:0,scale:0.72,transformOrigin:"0% 50%"}},'
              f'{{opacity:1,scale:1,duration:0.44,ease:POP,immediateRender:false}},'
              f'{q(a["everneed"] + 1.58):.2f});')                        # 37.22
    tw.append(f'tl.fromTo("#r6-flat",{{opacity:1,scaleX:0.001,'
              f'transformOrigin:"left center"}},{{opacity:1,scaleX:1,duration:0.66,'
              f'ease:SOFT,immediateRender:false}},{q(a["nolonger"] + 0.06):.2f});')  # 37.86
    tw.append('tl.set("#r6-flat",{opacity:0},0);')
    tw.append(rise("#r6-flatlb", a["nolonger"] + 0.56, 0.34, 12.0))      # 38.36
    # the 06 card carries NO ring: the video's homecoming annotation is the
    # header meter (hd-ring2), and two rings on the peak beat is exactly the
    # kind of stacking that made this format feel rushed.

    # ---- 07 MCP SERVERS -----------------------------------------------------
    for sel in ("#r7-inf", "#r7-br"):
        tw.append(f'tl.set("{sel}",{{opacity:0}},0);')
    # the ring lands on "a Hermes agent" and holds across the whole claim
    anno(tw, "#r7-ring", a["ifyou"] + 0.50, a["servers"] - 0.30)         # 41.08 -> 43.38
    for i in range(N):
        t = q(a["servers"] + 0.04 + i * 0.085)
        tw.append(f'tl.to("#r7-tg{i}-trk",{{background:"{C.rgb(T)}",'
                  f'borderColor:"{C.rgb(T)}",duration:0.22,ease:SOFT}},{t:.2f});')
        tw.append(f'tl.to("#r7-tg{i}-knb",{{x:36,background:"{C.rgb(C.WHITE)}",'
                  f'duration:0.26,ease:POP}},{t:.2f});')
    tw.append('tl.set("#r7-subb",{opacity:0},0);')
    tw.append(C.swap("#r7-suba", "#r7-subb", q(a["andtools"] + 0.08), 0.22))
    tw.append(pop("#r7-inf", a["andtools"] + 0.34, 0.44))
    tw.append(rise("#r7-br", a["andtools"] + 0.76, 0.36, 14.0))


def header_tweens(a: dict[str, float], tw: list[str], *, hd_w: float = C.WIN_W,
                  cut_in: float, ring2: tuple[float, float] | None = None) -> None:
    """The spine's one persistent instrument.  Withheld until "loads every tool"
    fills it, collapsed on "they don't", then it never moves again — and the
    video's last annotation comes home to it.

    Both rings are now sequential with a real hold; the old build fired `hd-ring`
    and `r1-ring` inside 40 ms of each other on "all at once"."""
    for sel in ("#hd-lb", "#hd-val", "#hd-track", "#hd-fill"):
        tw.append(f'tl.set("{sel}",{{opacity:0}},0);')
    for k, sel in enumerate(("#hd-mark", "#hd-name", "#hd-chip", "#hd-chipt", "#hd-hair",
                             "#hd-ready", "#hd-dot")):
        tw.append(rise(sel, cut_in + 0.04 + k * 0.05, 0.36, 14.0))
    t = q(a["loads"] + 0.28)
    tw.append(f'tl.to("#hd-ready",{{opacity:0,duration:0.22,ease:EXIT}},{t:.2f});')
    tw.append(f'tl.set("#hd-ready",{{opacity:0}},{t + 0.22:.2f});')
    tw.append(f'tl.to("#hd-dot",{{opacity:0,duration:0.22,ease:EXIT}},{t:.2f});')
    tw.append(f'tl.set("#hd-dot",{{opacity:0}},{t + 0.22:.2f});')
    for sel in ("#hd-lb", "#hd-val", "#hd-track"):
        tw.append(f'tl.to("{sel}",{{opacity:1,duration:0.28,ease:SOFT}},{t + 0.18:.2f});')
    tw.append(C.fill_to("hd-fill", t + 0.20, 0.92, 0.70, geom=C.hd_geom(hd_w)))
    tw.append(count_to("hd-num", t + 0.20, 0, 184000, 0.70))
    anno(tw, "#hd-ring", a["atonce"] + 0.16, a["spoiler"] + 0.46)        # 5.30 -> 6.30
    tw.append('tl.set("#hd-ring2",{opacity:0},0);')
    tw.append(C.fill_to("hd-fill", q(a["dont"] + 0.06), 0.06, 0.80,
                        geom=C.hd_geom(hd_w)))
    tw.append(count_to("hd-num", q(a["dont"] + 0.06), 184000, 12000, 0.80))
    r2i, r2o = ring2 or (a["bloating"] + 0.30, a["unbelievable"] + 1.20)
    anno(tw, "#hd-ring2", r2i, r2o)                                       # 47.20 -> 49.90


def outro_tweens(tw: list[str], cut_out: float, a: dict[str, float]) -> None:
    for sel in ("#ol-band", "#ol-rule", "#ol-handle", "#ol-daily"):
        tw.append(f'tl.set("{sel}",{{opacity:0}},0);')
    tw.append(C.fade("#ol-band", q(cut_out + 0.12), 1.0, 0.32))
    tw.append(f'tl.fromTo("#ol-rule",{{opacity:1,scaleX:0.001,'
              f'transformOrigin:"center center"}},{{opacity:1,scaleX:1,duration:0.42,'
              f'ease:SOFT,immediateRender:false}},{q(cut_out + 0.34):.2f});')
    tw.append(rise("#ol-handle", cut_out + 0.50, 0.44, 16.0))
    tw.append(C.fade("#ol-daily", q(a["daily"]), 1.0, 0.36))


# =============================================================================
# THE GUARD — the pacing and peek laws, re-derived from the emitted timeline
# =============================================================================
_TWEEN = re.compile(
    r'tl\.(set|to|fromTo)\("([^"]+)"\s*,\s*(.*?)\)\s*;', re.S)


def _events(tweens: list[str]) -> list[tuple[str, str, float, float]]:
    """(kind, selector, start, duration) for every emitted tween."""
    out: list[tuple[str, str, float, float]] = []
    src = "".join(tweens)
    for m in _TWEEN.finditer(src):
        kind, sel, rest = m.group(1), m.group(2), m.group(3)
        tail = re.findall(r",\s*(-?\d+(?:\.\d+)?)\s*$", rest)
        if not tail:
            continue
        t = float(tail[-1])
        d = 0.0
        if kind != "set":
            ds = re.findall(r"duration:\s*(\d+(?:\.\d+)?)", rest)
            d = float(ds[-1]) if ds else 0.0
        out.append((kind, sel, t, d))
    return out


def audit(tweens: list[str], moves: list[tuple[float, float]], *,
          cuts: list[float], label: str, still_exempt: tuple[float, ...] = ()) -> None:
    """Fail the build on a pacing or law violation.

    `moves` are (start, duration) of every spine move that is VISIBLE (a move
    hidden behind a face return is not one).  `cuts` are face cut times.

    `still_exempt` lists move start times excused from the stillness rule.  There
    is exactly one legitimate case: the zoom variant's opening move away from the
    establishing wide.  That shot's content IS the board assembling, and the move
    off it is what ends the assembly — demanding stillness first would mean
    either a dead wide or arriving at 01 after "loads every tool" has already
    been said.  The no-starts-DURING-the-move rule still applies to it."""
    ev = _events(tweens)
    bad: list[str] = []

    # Global Law 3 — no fill may reach by scaleX
    for kind, sel, _t, _d in ev:
        if sel.endswith("-fill") and kind != "set":
            src = "".join(tweens)
            if re.search(rf'tl\.\w+\("{re.escape(sel)}"[^;]*scaleX', src):
                bad.append(f"ROUNDFILL: {sel} animated with scaleX")

    for ms, md in moves:
        me = ms + md
        for kind, sel, t, d in ev:
            if kind == "set" or sel.startswith("#bg") or sel == "#board":
                continue
            if ms + 1e-6 < t < me - 1e-6:
                bad.append(f"PACING: {sel} starts at {t:.2f}, inside the move "
                           f"[{ms:.2f},{me:.2f}]")
        ends = [t + d for kind, sel, t, d in ev
                if kind != "set" and not sel.startswith("#bg") and sel != "#board"
                and t < ms - 1e-6]
        if ends and not any(abs(ms - e) < 1e-6 for e in still_exempt):
            still = ms - max(ends)
            if still < STILL_MOVE - 1e-6:
                bad.append(f"PACING: only {still:.2f}s of stillness before the "
                           f"move at {ms:.2f} (need {STILL_MOVE})")
    for ct in cuts:
        ends = [t + d for kind, sel, t, d in ev
                if kind != "set" and not sel.startswith("#bg") and sel != "#board"
                and t < ct - 1e-6 and t + d <= ct + 1e-6]
        starts = [t for kind, sel, t, d in ev
                  if kind != "set" and not sel.startswith("#bg") and sel != "#board"
                  and ct - STILL_CUT + 1e-6 < t < ct - 1e-6]
        if starts:
            bad.append(f"PACING: {len(starts)} tween(s) start inside "
                       f"{STILL_CUT}s before the face cut at {ct:.2f}")
    if bad:
        raise SystemExit(f"[{label}] guard failed:\n  " + "\n  ".join(bad))
    print(f"[{label}] guard OK — {len(ev)} timeline events, {len(moves)} visible "
          f"moves, {len(cuts)} face cuts")


def bind_assets(project: Path) -> None:
    C.bind_assets(project)
