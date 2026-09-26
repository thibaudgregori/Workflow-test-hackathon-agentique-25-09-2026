#!/usr/bin/env python3
"""WHITEBOARD harness — the CANONICAL per-video production harness (PLAN VIEW lane).

CANONICAL LOCATION (promoted 2026-09-02): `formats/whiteboard/lib/whiteboard_build.py`.
It was written inside `(run 9) gen/`; a run folder is not a home for a law, so
every daily run now imports it from here.  `formats/whiteboard/lib/whiteboard_build.py`
remains as a thin re-export shim so the run-9 generators keep working unchanged.
Every daily whiteboard (Reels) build MUST go through `build()` here — that is what
makes THE LABEL LAW, the rising-sheet outro and the caption canon unskippable.

The run folder is a parameter: set `SHORTS_RUN` in the environment (an absolute
path) to point the harness at a new run; unset, it resolves to the NEWEST
`shorts_run<N>` on disk (fixed 2026-09-03 — it used to be pinned to run 9).

Miguel, 2026-09-02: the Reels / Instagram delivery is now the WHITEBOARD format.
This module is the thin production harness that lets a per-video board reuse the
approved chassis (`formats/whiteboard/`) without forking it: the Board class, the
marker, the pen SFX rationing, the audio mix, the caption canon and the CSS all
come from `whiteboard_fix6_core`; only the DRAWING, the anchors and the media are
per video.

Variant: **plan view** (`--variant fix` in the chassis).  The camera never moves,
the whole board is in frame from frame 0, and the viewer watches the map fill in.
That is the variant Miguel named as the reference for this rebuild
(`~/Movies/Shorts Factory/Format Lab/whiteboard/planview - DEFINITIVE.mp4`), and
it is the variant the format was approved on ("SUUUUUPER nice!").

Everything the chassis asserts is asserted here too, on OUR board:
  * LAW 12 top band      — no ink above 102.4u, no marker body above it either
  * LAW 12 right rail    — nothing below y=307.2u may reach past x=489.6u
  * CAPTION BAND         — no ink below y=426.2u (the pill's reserved half)
  * caption canon        — pipeline/captions.py, ONE size, split at word bounds
  * anchors              — pinned to word INDEX and word TEXT; a re-transcription
                           fails the build instead of sliding the choreography
"""
from __future__ import annotations
import sys as _asset_sys
from pathlib import Path as _AssetPath
_asset_sys.path.insert(0, str(next(p for p in _AssetPath(__file__).resolve().parents if (p / "execution/asset_library.py").is_file()) / "execution"))
from asset_library import resolve_source as library_asset, source_files as library_files


import contextlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

F = Path.home() / "Documents/Workspace/projects/personal/content/shorts-factory"
# The run folder is a PARAMETER, not a constant baked into a shared library:
# `SHORTS_RUN=/abs/path/to/shorts_run<N>` moves the whole harness to the next run.
def _newest_run(root: Path) -> Path:
    """The run folder defaults to the NEWEST shorts_run<N>, never a frozen one.

    2026-09-03 (clerk, moleculezoom): the default was hard-pinned to
    run 9, so every run-10 invocation of the zero-ink scan died in
    `load_words` on a run-9 path that does not exist — and because the
    caller pipes through `tail`, the traceback surfaced with rc=0 and read as a
    pass. Worse than the crash is the silent case: had run 9 contained a video of
    the same id, the scan would have measured run 10's render against run 9's
    transcript and reported PASS. A run folder is a parameter, so it resolves to
    the highest-numbered run present; SHORTS_RUN still overrides it absolutely.
    """
    runs = sorted(
        (d for d in (root / "runs").glob("shorts_run*") if d.is_dir() and d.name[11:].isdigit()),
        key=lambda d: int(d.name[11:]),
    )
    if not runs:
        raise FileNotFoundError(f"no shorts_run<N> folder under {root}; set SHORTS_RUN")
    return runs[-1]


RUN = Path(os.environ.get("SHORTS_RUN") or _newest_run(F))
LOGOS = Path.home() / "Documents/Workspace/assets/logos"
SHARED_SFX = F / "formats/_shared/sfx"  # frozen lab inputs, moved out of the format lab (archived) 2026-09-20 (MANIFEST.sha256 beside them)
PEN_SRC = library_asset(F / "formats/whiteboard/source/sfx3/pen_soft3.mp3")
BED = library_asset(Path.home() / "Documents/Workspace/assets/audio/music/shorts-factory/bed_split_v2.mp3")

sys.path.insert(0, str(F / "pipeline"))
sys.path.insert(0, str(F / "formats/whiteboard/lib"))

import captions as CAP                                   # noqa: E402
import whiteboard_fix6_core as core                      # noqa: E402
from whiteboard_fix6_core import (                       # noqa: E402
    AX, CREAM, FPS, INK, INK_2, MUTED, SEAM, SW, SW_FAT, SW_THIN, TERRA,
    TERRA_2, WHITE, Board, esc, px, rect_points, text_w,
)

ZONE_H = core.ZONE_H              # 460 design units == 862.5 px
FACE_H = 564.0                    # 1057.5 px band under the seam
TOP_BAND_U = core.TOP_BAND_U      # 102.4
RAIL_X_U = core.RAIL_X_U          # 489.6
RAIL_Y_U = core.RAIL_Y_U          # 307.2
CAP_CLEAR_PX = core.CAP_CLEAR_PX  # 63.30
CAP_BAND_TOP_PX = px(SEAM) - CAP_CLEAR_PX          # 799.20
CAP_BAND_TOP_U = CAP_BAND_TOP_PX / core.S          # 426.24
PEN_REACH_U = 59.0 * core.PEN_SCALE                # 41.3

# =============================================================================
# THE WHITEBOARD LABEL LAW (run 9, from the independent viewer test)
# =============================================================================
# `perplexityprojects_whiteboard` scored 11 SENSE against 13 NO-SENSE — the worst
# render the factory has shipped — and every one of the structural defects was the
# same defect: **things were drawn and never named.**  SPACES was never drawn at
# all, so "the evolution of Perplexity Spaces" had no picture.  RESEARCH DESK, the
# video's key term, was never written.  ONLINE / DEEP / LOCAL were never written,
# so three unlabelled glyphs fed a folder and the middle one ("a stack of three
# overlapping squares") failed the Phone Test cold.
#
# The sibling split render, drawing the SAME argument, printed all seven keys and
# passed every one of those beats.  The difference was not the drawing.  It was
# the writing — and writing the word is a whiteboard's most native move.
#
# THE LAW, now enforced by `assert_label_law` at build time:
#   * every plan beat that names an object declares that object's KEY WORD, and
#     that word must be handwritten within `LABEL_WINDOW` of the word being
#     spoken.  Label and object are one block.
#   * a comparison the script SPEAKS (Spaces -> Projects) must be DRAWN as a
#     comparison: both terms on the board, and a connector between them.
#   * the key term (Law 9) is written first, alone, and large.
#   * the outro never overprints the diagram (`assert_outro_clear`), AND the
#     handover is CONTINUOUS: the zone's ink never reaches zero
#     (`assert_outro_clear` proves it on the authored geometry,
#     `assert_zone_never_blank` proves it again on the decoded render).
LABEL_WINDOW = 1.0             # seconds between a spoken word and its written key
KEY_TERM_MIN_FS = 22.0         # "large" is a number, not an opinion
OUTRO_WIPE = 0.56              # the wipe: a clean sheet rises over the board
OUTRO_RULE_TOP_U = 172.0       # the card's topmost ink, in board units
OUTRO_HANDLE_TOP_U = 196.0
OUTRO_DAILY_TOP_U = 248.0


def assert_label_law(b, a: dict[str, float], plan: dict, board_text: list[str],
                     *, key_term: str, comparisons=()) -> dict:
    """DETERMINISTIC. Reads the AUTHORED board, not a rendered frame.

    `plan` maps an anchor key -> the KEY WORD that beat writes.  Every entry must
    correspond to a `Board.label()` whose text matches and whose tween time is
    inside `LABEL_WINDOW` of the anchor.  `comparisons` are (left, right) pairs
    of key words that must BOTH be on the board.
    """
    # Board.label() registers a rigid of kind "type" named `type:<TEXT>`.
    written = {r["name"][5:]: float(r["t0"])
               for r in b.rigids if r["kind"] == "type"
               and r["name"].startswith("type:")}
    late, absent = [], []
    for anchor, word in plan.items():
        if anchor not in a:
            raise SystemExit(f"label law: beat {anchor!r} is not an anchor")
        if word not in written:
            absent.append(f"{anchor} @ {a[anchor]:.2f}s names {word!r} — never written")
            continue
        dt = written[word] - a[anchor]
        if abs(dt) > LABEL_WINDOW:
            late.append(f"{word!r} is written at {written[word]:.2f}s, "
                        f"{dt:+.2f}s from its word at {a[anchor]:.2f}s")
    if absent:
        raise SystemExit("WHITEBOARD LABEL LAW — a drawn object with no written "
                         "key:\n  " + "\n  ".join(absent))
    if late:
        raise SystemExit(f"WHITEBOARD LABEL LAW — a key written more than "
                         f"{LABEL_WINDOW}s from its word:\n  " + "\n  ".join(late))
    for left, right in comparisons:
        miss = [w for w in (left, right) if w not in written]
        if miss:
            raise SystemExit(f"WHITEBOARD LABEL LAW — the script speaks the "
                             f"comparison {left} -> {right} but {miss} is never "
                             f"drawn, so the comparison has no picture")
    if key_term not in written:
        raise SystemExit(f"WHITEBOARD LABEL LAW — the key term {key_term!r} is "
                         "not on the board (Law 9)")
    if written[key_term] > min(written.values()) + 1e-6:
        first = min(written, key=lambda k: written[k])
        raise SystemExit(f"WHITEBOARD LABEL LAW — the key term {key_term!r} is "
                         f"written at {written[key_term]:.2f}s but {first!r} "
                         f"beat it to the board at {written[first]:.2f}s. Law 9: "
                         "the key term is written FIRST, alone, large")
    fs = {r["name"][5:]: (r["y1"] - r["y0"]) / 1.55 for r in b.rigids
          if r["kind"] == "type" and r["name"].startswith("type:")}
    if fs.get(key_term, 0.0) < KEY_TERM_MIN_FS:
        raise SystemExit(f"WHITEBOARD LABEL LAW — the key term {key_term!r} is "
                         f"{fs.get(key_term, 0):.1f}u tall, under the "
                         f"{KEY_TERM_MIN_FS}u floor for 'large'")
    extra = sorted(set(board_text) - set(written))
    return {"window_s": LABEL_WINDOW, "key_term": key_term,
            "key_term_fs_u": round(fs[key_term], 1),
            "written": {k: round(v, 2) for k, v in sorted(written.items(),
                                                          key=lambda kv: kv[1])},
            "plan": plan, "comparisons": [list(c) for c in comparisons],
            "unplanned_text": extra, "verdict": "PASS"}


def assert_outro_clear(rep: dict, b, a: dict[str, float], outro_key: str) -> dict:
    """The outro region is DIAGRAM-FREE **and** the handover never goes blank.

    Two requirements that used to fight each other, now both proved on the
    AUTHORED geometry — no rendered frame required.

    1. NO OVERPRINT.  The card does not fade up over the board; it rides an
       OPAQUE, full-zone cream sheet that rises over the board.  A pixel of the
       diagram can no more show through it than through the page it is printed
       on, so `wipe_end <= card_start` (an ordering that only held because the
       board had to vanish first) is replaced by a coverage fact.
    2. NO DEAD SLOT.  Round 2 of the viewer test held this render for a 0.60 s
       totally empty visual zone (26.08-26.64 s, 15 frames at 0.000 % ink):
       the board's dissolve finished long before the card's fade began, and for
       ten of those frames nothing was entering and nothing was leaving.  With a
       rising sheet the two events are geometrically interlocked and the overlap
       is a pure inequality in TRAVEL, independent of the ease and of the
       duration: the card's first ink crosses into the zone at travel
       `card_ink_enters_px`, and the board's last ink is not covered until travel
       `board_covered_px`.  While `card_ink_enters_px < board_covered_px` there
       is no travel — and therefore no frame — at which the zone holds neither.
    """
    t0 = a[outro_key]
    late = sorted({r["name"] for r in b.rigids if float(r["t0"]) >= t0})
    if late:
        raise SystemExit(f"OUTRO — ink is authored at or after the outro starts "
                         f"({t0:.2f}s): {late}. Nothing may be drawn into the "
                         "region the handle card occupies")
    if not rep["sheet_opaque"]:
        raise SystemExit("OUTRO — the handle card's sheet is not opaque: the "
                         "diagram would read through it")
    if rep["sheet_covers_px"] + 1e-6 < px(ZONE_H):
        raise SystemExit(f"OUTRO — the sheet covers {rep['sheet_covers_px']:.1f} px "
                         f"of a {px(ZONE_H):.1f} px zone: the diagram would survive "
                         "beside the card")
    if rep["card_ink_enters_px"] >= rep["board_covered_px"]:
        raise SystemExit(
            f"OUTRO — a dead slot: the board's last ink is covered at travel "
            f"{rep['board_covered_px']:.1f} px but the card's first ink does not "
            f"enter until {rep['card_ink_enters_px']:.1f} px, so the zone is "
            "empty in between. The card must enter while the wipe is still "
            "finishing")
    return rep | {"outro_start": round(t0, 2), "verdict": "PASS"}


# =============================================================================
# ROUND-4 LAWS (Miguel, 2026-09-02) — the board's own instruments
# =============================================================================
# Everything below is ADDITIVE: no existing signature changed, no existing call
# site moved.  `build()` runs the new asserts with backward-compatible defaults,
# so a generator written before this section still builds; a generator that
# DECLARES (anchors=, connectors=, blocks=) gets the strict tier.
#
# The units are BOARD DESIGN UNITS (576 x 460).  One unit is `core.S` = 1.875
# frame design px, so a frame-space rule in px converts with `u_of_px()`.
# =============================================================================

def u_of_px(v: float) -> float:
    """Frame design px -> board design units."""
    return v / core.S


# --- LAW 38: THE HIGHLIGHT IS THE EMPHASIS FOR TEXT ON AN IMAGE --------------
# Miguel: "For text, do not circle or make a box, I want you to use the nice
# clean highlight that you used to use." and "circling of the clock looks off".
# AMENDED 2026-09-02: "do not use highlight for everything, it's just for when
# you need to highlight text on an image, for the rest you can use the boxing
# you were using before, which are perfectly fine."  So the marker is for words
# that are PIXELS — a post card, a screenshot, a document, a UI capture; a drawn
# object or board type takes `box_emphasis()` below.
# The primitive he means is the factory's MARKER FILL, first shipped in
# `references/builds/mathvoice_kinetic/mathvoice_kinetic_gen.py` and carried into run 7
# (`mathconjecture_kinetic_gen.py:601`): `.hl { background:rgba(198,103,72,0.32);
# border-radius:6px }`, wiped on left-to-right (`wipex`), ONE FILL PER LINE
# (never a union box, which scopes nothing), riding OVER the thing it scopes.
# It is re-homed here so the whiteboard has it natively.
HL_FILL = "rgba(198,103,72,0.32)"   # terracotta at 0.32 — the marker, not a box
HL_RADIUS_U = 3.2                   # 6 frame px
HL_PAD_X_U = 2.4                    # the swipe overruns the glyphs slightly
HL_PAD_Y_U = 1.2
HL_WIPE_D = 0.34                    # the run-6/7 swipe duration
HL_LINE_STAGGER = 0.10              # per extra line, as run 6 shipped it


def highlight(b, box, t: float, *, d: float = HL_WIPE_D, color: str = HL_FILL,
              name: str = "", pen: bool = True, pad: bool = True) -> str:
    """The emphasis for TEXT ON AN IMAGE. A translucent marker swipe over the
    words themselves (amended LAW 38).

    `box` is (x0, y0, x1, y1) in board units — normally a TEXT line's own bbox,
    one call per line.  The rect is authored at scaleX 0 and wiped open from its
    left edge, which is what a marker actually does.

    For a DRAWN object or board type, use `box_emphasis()` instead.  Never a
    ring, an ellipse or a circle — that shape is retired for every target.
    """
    x0, y0, x1, y1 = box
    if pad:
        x0, x1 = x0 - HL_PAD_X_U, x1 + HL_PAD_X_U
        y0, y1 = y0 - HL_PAD_Y_U, y1 + HL_PAD_Y_U
    eid = b.uid("hl")
    b.ink((x0, y0, x1, y1), f"hl:{name or eid}")
    b.shape(
        f'<rect id="{eid}" x="{b.u(x0)}" y="{b.u(y0)}" width="{b.u(x1 - x0)}" '
        f'height="{b.u(y1 - y0)}" rx="{b.u(HL_RADIUS_U)}" fill="{color}"/>')
    # The pivot is given to GSAP in SVG user space (`svgOrigin`), never as a CSS
    # `transform-box:fill-box` origin: GSAP bakes its own origin into the matrix
    # and writes transform-origin 0 0, which fill-box re-reads as the rect's own
    # corner, so every FRACTIONAL scale is displaced by scale x the rect's own
    # offset (dgxspark round 2: the half-full pool vanished; here the wipe's
    # left edge slid ~24 px during its first frames on viberesearch).
    org = f'svgOrigin:"{b.u(x0)} {b.u((y0 + y1) / 2)}"'
    b.set0(f'tl.set("#{eid}",{{scaleX:0,{org}}},0);')
    b.tw.append(
        f'tl.fromTo("#{eid}",{{scaleX:0,{org}}},{{scaleX:1,{org},duration:{d:.2f},'
        f'ease:SOFT,immediateRender:false}},{t:.2f});')
    # kind "hl" is registered so the camera can see it, and is exempt from the
    # spacing law by construction: a highlight is SUPPOSED to sit on its mark.
    b.rigid("hl", (x0, y0, x1, y1), t, name=f"hl:{name or eid}")
    if pen:
        cy = b.u((y0 + y1) / 2)
        b.strokes.append({"t": t, "d": d,
                          "pts": [(b.u(x0), cy), (b.u(x1), cy)]})
    return eid


def highlight_lines(b, boxes, t: float, **kw) -> list[str]:
    """One swipe PER LINE, staggered — never a union box over a paragraph."""
    return [highlight(b, bx, t + HL_LINE_STAGGER * i, **kw)
            for i, bx in enumerate(boxes)]


def highlight_label(b, text: str, cx: float, baseline: float, fs: float,
                    t: float, **kw) -> str:
    """The swipe sized to a `Board.label()` that is already on the board."""
    wid = text_w(text, fs)
    return highlight(b, (cx - wid / 2, baseline - fs * 1.10,
                         cx + wid / 2, baseline + fs * 0.20), t, name=text, **kw)


# --- LAW 38 (AMENDED 2026-09-02): BOXING IS THE EMPHASIS FOR DRAWN OBJECTS ---
# Miguel, after watching the fixed videos ("those look fantastic"):
#   "do not use highlight for everything, it's just for when you need to
#    highlight text on an image, for the rest you can use the boxing you were
#    using before, which are perfectly fine."
# So the law splits by TARGET, not by taste:
#   * text living inside a raster (a post card, a screenshot, a document, a UI
#     capture)              -> `highlight()` / `highlight_lines()`
#   * a DRAWN object, or board/scene TYPE
#                           -> `box_emphasis()` (this primitive)
#   * a ring / ellipse / circle -> retired everywhere. That was the actual
#     complaint (the circled clock), and it is the only shape still banned.
#
# The boxing primitive is the factory's OWN, shipped in runs 3-8 long before
# LAW 38 over-corrected it away:
#   * DOM lane   — the PANEL BORDER FLIP: `.node.hero { border-color: TERRA_L }`
#     driven by `tl.fromTo(sel, {borderColor:"rgba(17,17,17,0.16)"},
#     {borderColor:"rgb(221,114,89)", duration:0.38, ease:SOFT})`
#     (`references/builds/deepresearch_diagram/deepresearch_diagram_gen.py:317` + `:795`, where the
#     comment already records WHY it beat a ring: "never ring a node that
#     connectors land on").
#   * BOARD lane — the terracotta MARKER BOX popped around the thing it picks
#     out: `whiteboard_fix6_core.py:668` (`ring{i}` — misnamed, actually a rect:
#     `fill:none`, `stroke:TERRA`, `stroke-width:SW_THIN`, `rx:11`, popped in
#     over 0.34 s from scale 0.55, registered as kind `"box"`).
# `box_emphasis()` is that board-lane move, re-homed so a board never forks it.
BOX_COLOR = TERRA
BOX_W_U = SW_THIN                   # the hairline the chassis already draws with
BOX_RADIUS_U = 5.0                  # a BOX: a soft corner, never a pill or oval
BOX_PAD_U = 5.0                     # the run-6 inset (CELL + 10 => 5 a side)
BOX_POP_D = 0.34
BOX_POP_S0 = 0.55


def box_emphasis(b, box, t: float, *, d: float = BOX_POP_D,
                 color: str = BOX_COLOR, name: str = "", target: str = "",
                 pad: float = BOX_PAD_U, t_to: float = 1e9,
                 pen: bool = True) -> str:
    """THE emphasis for a DRAWN OBJECT or for board TYPE (amended LAW 38).

    A rectangular terracotta marker box popped around the thing it picks out.
    `box` is (x0, y0, x1, y1) in board units — the TARGET's own box; `pad` is
    added on every side so the box rides just outside its object's ink.

    Use `highlight()` instead when the words are part of a raster (a post card,
    a screenshot): a box on image text is refused by `assert_no_enclosure`.
    Never a ring, an ellipse or a circle — that shape is retired in every
    format, for every target.

    `target=` names the rigid this box is emphasising.  It is optional (the
    check falls back to containment) but it makes the paperwork readable and
    lets the check judge a target the box does not fully enclose.
    """
    x0, y0, x1, y1 = box
    x0, y0, x1, y1 = x0 - pad, y0 - pad, x1 + pad, y1 + pad
    eid = b.uid("bx")
    b.ink((x0, y0, x1, y1), f"box:{name or target or eid}")
    b.shape(
        f'<rect id="{eid}" x="{b.u(x0)}" y="{b.u(y0)}" width="{b.u(x1 - x0)}" '
        f'height="{b.u(y1 - y0)}" rx="{b.u(BOX_RADIUS_U)}" fill="none" '
        f'stroke="{color}" stroke-width="{b.u(BOX_W_U)}" opacity="0"/>')
    # The pen taps the box's TOP-LEFT CORNER, where a hand starts a rectangle,
    # never the box centre: the centre of a big box is the finished ink it is
    # framing (run 13, hermesdesktop 18.20-18.78 s: the pencil lay across the
    # VISUALS row for 0.58 s while the border box popped around the window).
    b.pop(eid, t, d, BOX_POP_S0,
          at=(x0 + BOX_RADIUS_U, y0) if pen else None)
    b.rigid("boxemph", (x0, y0, x1, y1), t, t_to,
            name=f"box:{name or target or eid}")
    if target:
        b.rigids[-1]["target"] = target
    return eid


def note_asset(b, *names: str) -> None:
    """Declare that these rigids are RASTERS — a post card, a screenshot, a
    document, a UI capture.  Their words are pixels, so their emphasis is
    `highlight()`, and `assert_no_enclosure` refuses a box drawn on them."""
    if not hasattr(b, "_assets"):
        b._assets = set()
    b._assets.update(names)


# a raster's name, when nobody declared one: the names this factory has actually
# used for a pasted screenshot (`postcard`, `x-card`, `shot`), never a DRAWN card
# ("job-card", "monitor-card") — which is why `note_asset()` exists.
ASSET_NAME_RE = re.compile(
    r"(?:^|[-_:])(?:postcard|post|tweet|screenshot|shot|capture|img|image|"
    r"raster|asset)(?:$|[-_:0-9])", re.I)


def _is_asset(b, r) -> bool:
    n = (r.get("name") or "")
    return (n in getattr(b, "_assets", set()) or
            _base_name(r) in getattr(b, "_assets", set()) or
            bool(ASSET_NAME_RE.search(n)))


# --- LAW 4: ARROWS INTO ONE TARGET LAND ON ALIGNED ANCHORS -------------------
def anchor_points(target: tuple[float, float, float, float], n: int,
                  side: str = "top", inset: float = 0.16):
    """The workaround Miguel asked for: connectors terminate on the target's
    VIRTUAL BOUNDING RECTANGLE, never on its irregular outline.

    Returns `n` points on one side of `target`, evenly spaced and SYMMETRIC
    about the target's axis, all at the same height (or, for a vertical side,
    the same x).  `inset` keeps the outermost anchors off the corners.
    """
    x0, y0, x1, y1 = target
    if side in ("top", "bottom"):
        y = y0 if side == "top" else y1
        lo, hi = x0 + (x1 - x0) * inset, x1 - (x1 - x0) * inset
        if n == 1:
            return [((x0 + x1) / 2, y)]
        return [(lo + (hi - lo) * i / (n - 1), y) for i in range(n)]
    x = x0 if side == "left" else x1
    lo, hi = y0 + (y1 - y0) * inset, y1 - (y1 - y0) * inset
    if n == 1:
        return [(x, (y0 + y1) / 2)]
    return [(x, lo + (hi - lo) * i / (n - 1)) for i in range(n)]


ANCHOR_Y_TOL_U = u_of_px(4.0)     # "same height" is 4 frame px, per Miguel
ANCHOR_SYM_TOL_U = u_of_px(4.0)


def assert_anchor_law(b, connectors) -> dict:
    """ROUND-4 LAW 4. `connectors` is a list of dicts:

        {"to": "<rigid name>", "end": (x, y), "name": "<connector id>"}

    Every connector into the SAME target must terminate at the same height
    (within `ANCHOR_Y_TOL_U`) or be mirror-symmetric about the target's centre
    axis.  Landing on the outline "at a different spot or height" is the defect.
    """
    if not connectors:
        return {"targets": 0, "verdict": "SKIP — no connectors declared"}
    by_name = {r["name"]: r for r in b.rigids if r.get("name")}
    groups: dict[str, list] = {}
    for c in connectors:
        groups.setdefault(c["to"], []).append(c)
    bad, rep = [], {}
    for tgt, cs in groups.items():
        if tgt not in by_name:
            raise SystemExit(f"ANCHOR LAW — connector target {tgt!r} is not a "
                             "registered rigid; a target must be a real object")
        r = by_name[tgt]
        cx = (r["x0"] + r["x1"]) / 2
        ys = [c["end"][1] for c in cs]
        xs = [c["end"][0] for c in cs]
        level = max(ys) - min(ys) <= ANCHOR_Y_TOL_U
        mirrored = (len(xs) % 2 == 0 and
                    all(abs((xs[i] + xs[-1 - i]) / 2 - cx) <= ANCHOR_SYM_TOL_U
                        for i in range(len(xs) // 2)) and level)
        on_rect = all(
            (abs(y - r["y0"]) <= 0.6 or abs(y - r["y1"]) <= 0.6 or
             abs(x - r["x0"]) <= 0.6 or abs(x - r["x1"]) <= 0.6)
            for x, y in ((c["end"][0], c["end"][1]) for c in cs))
        rep[tgt] = {"n": len(cs), "spread_u": round(max(ys) - min(ys), 2),
                    "level": level, "mirrored": mirrored, "on_rect": on_rect}
        if not on_rect:
            bad.append(f"{tgt}: an end does not sit on the target's virtual "
                       f"bounding rectangle")
        elif len(cs) > 1 and not (level or mirrored):
            bad.append(f"{tgt}: {len(cs)} connectors land at "
                       f"y={sorted(round(y, 1) for y in ys)} — spread "
                       f"{max(ys) - min(ys):.1f}u, over the "
                       f"{ANCHOR_Y_TOL_U:.1f}u tolerance, and not symmetric "
                       f"about x={cx:.1f}")
    if bad:
        raise SystemExit("ROUND-4 LAW 4 — arrows into a shared target must land "
                         "on ALIGNED anchors:\n  " + "\n  ".join(bad))
    return {"targets": len(groups), "detail": rep, "verdict": "PASS"}


# --- LAW 2 / LAW 38 (enforcement): NO RING. AND THE RIGHT TOOL PER TARGET -----
DECOR_PREFIXES = ("mark:", "logo:", "check:", "bullet:", "tick:", "hl:")


def assert_no_enclosure(b) -> dict:
    """ROUND-4 LAW 38 (amended 2026-09-02), enforced on the AUTHORED board.

    TWO REFUSALS and ONE ADVISORY — the split is by TARGET, not by shape:

      1. `kind == "ring"` — a ring, an ellipse or a circle drawn as emphasis.
         RETIRED EVERYWHERE, for every target.  This is the one Miguel actually
         complained about ("circling of the clock looks off").
      2. A `box_emphasis()` whose target is IMAGE TEXT — a raster: a post card,
         a screenshot, a document, a UI capture (declared with `note_asset()`,
         or named like one).  Words that are pixels get the marker HIGHLIGHT;
         a box around them is the wrong tool and reads as a cramped panel.
      3. ADVISORY (`wrong_tool`, never a refusal): a `highlight()` whose target
         is a DRAWN object or board TYPE with no raster under it.  Miguel's
         amendment prefers `box_emphasis()` there — but he approved boards that
         swipe a track bar and a written key, so this REPORTS and never gates.
         A law written from one instance already banned a tool he likes; it
         does not get to do that twice.

    A rectangular box around a DRAWN object is explicitly legal.  It still owes
    the spacing law (`assert_spacing_law` judges kind `"boxemph"` against every
    neighbour it does not contain: 16 u-px refusal, 24 aim).
    """
    rings = [r for r in b.rigids if r["kind"] == "ring"]
    bad = [f"{r['name'] or 'ring'} @ {r['t0']:.2f}s is a ring/ellipse emphasis "
           f"({r['x1'] - r['x0']:.0f}x{r['y1'] - r['y0']:.0f}u)" for r in rings]
    if bad:
        raise SystemExit(
            "ROUND-4 LAW 38 — a RING, an ELLIPSE or a CIRCLE is never emphasis, "
            "on any target:\n  " + "\n  ".join(bad) +
            "\n  Text on an image -> whiteboard_build.highlight(); a drawn "
            "object or board type -> whiteboard_build.box_emphasis().")

    wins = effective_windows(b)
    assets = [r for r in b.rigids if _is_asset(b, r)]
    boxes = [r for r in b.rigids if r["kind"] == "boxemph"]
    hls = [r for r in b.rigids if r["kind"] == "hl"]

    def _targets(e, pool):
        """What this emphasis is drawn ON: a declared target, else every rigid
        it holds or sits over while both are on the board."""
        named = e.get("target")
        if named:
            return [r for r in pool if _base_name(r) == named or
                    (r.get("name") or "") == named]
        out = []
        for r in pool:
            if r is e or not _win_overlap(wins[id(e)], wins[id(r)]):
                continue
            ox = min(e["x1"], r["x1"]) - max(e["x0"], r["x0"])
            oy = min(e["y1"], r["y1"]) - max(e["y0"], r["y0"])
            if _contains(e, r, 1.0) or (ox > 0.0 and oy > 0.0):
                out.append(r)
        return out

    boxed_raster = []
    for e in boxes:
        for r in _targets(e, assets):
            boxed_raster.append(
                f"{e['name']} @ {e['t0']:.2f}s boxes {r['name'] or r['kind']}, "
                f"which is a RASTER — its words are pixels")
    if boxed_raster:
        raise SystemExit(
            "ROUND-4 LAW 38 — a box is the emphasis for a DRAWN object; TEXT ON "
            "AN IMAGE gets the marker highlight:\n  " +
            "\n  ".join(sorted(set(boxed_raster))) +
            "\n  Replace with whiteboard_build.highlight() / highlight_lines() "
            "— one fill per line, over the words themselves.")

    wrong_tool = []
    for e in hls:
        tgt = _targets(e, [r for r in b.rigids
                           if r["kind"] not in ("hl", "boxemph")])
        if tgt and not any(_is_asset(b, r) for r in tgt):
            wrong_tool.append(
                f"{e['name']} @ {e['t0']:.2f}s swipes "
                f"{', '.join(sorted({r['name'] or r['kind'] for r in tgt}))} — "
                f"no raster under it; box_emphasis() is the amended default")
    return {"rings": 0, "boxes": len(boxes), "highlights": len(hls),
            "rasters": sorted({r["name"] for r in assets if r.get("name")}),
            "wrong_tool_advisory": sorted(set(wrong_tool)),
            "verdict": "PASS"}


# --- LAW 3: LABELS ABOVE OR BELOW, NEVER BESIDE ------------------------------
# --- THE CHAPTER CLAMP (ROUND-4 LAW 7's price) --------------------------------
# A chaptered board erases between idea groups, but a generator may still leave
# `t_to` at infinity on a mark it actually wipes.  Judging geometry across a
# seam then compares a chapter-1 key against a chapter-3 bar and invents
# violations that no viewer can see.  The chapter seams are read off the
# registry itself: an erase time shared by >= CHAPTER_MIN_SHARE rigids IS a
# seam, and an open-ended mark is clamped to the next seam after it is drawn.
# LAW 6 still judges the RAW window — the clamp is for geometry, never for
# lifetimes, or a board could hide a lingering mark behind a seam it never uses.
CHAPTER_MIN_SHARE = 3


def chapter_seams(b, min_share: int = CHAPTER_MIN_SHARE) -> list[float]:
    c = Counter(round(r["t1"], 2) for r in b.rigids if r["t1"] < 1e8)
    return sorted(t for t, n in c.items() if n >= min_share)


def effective_windows(b) -> dict[int, tuple[float, float]]:
    seams = chapter_seams(b)
    out: dict[int, tuple[float, float]] = {}
    for r in b.rigids:
        t1 = r["t1"]
        if t1 >= 1e8 and seams:
            nxt = [s for s in seams if s > r["t0"] + 1e-6]
            if nxt:
                t1 = nxt[0]
        out[id(r)] = (r["t0"], t1)
    return out


def _win_overlap(wa, wb, eps: float = 1e-6) -> bool:
    return wa[0] < wb[1] - eps and wb[0] < wa[1] - eps


def _base_name(r) -> str:
    """`type:IMPOSSIBLE@axis` and `type:IMPOSSIBLE` are ONE object in two
    placements (an entrance state), never two objects sharing a gutter."""
    n = (r.get("name") or "")
    return n.split("@", 1)[0]


def _area(r) -> float:
    return max(r["x1"] - r["x0"], 0.0) * max(r["y1"] - r["y0"], 0.0)


LABEL_WELD_U = 40.0        # how far a key may sit from the object it names
LABEL_AXIS_FRAC = 0.15     # Miguel's +/-15 % of the object's horizontal extent


def _boxes_overlap_t(a, b_, eps: float = 1e-6) -> bool:
    return a["t0"] < b_["t1"] - eps and b_["t0"] < a["t1"] - eps


def _rect_gap(a, b_) -> float:
    dx = max(b_["x0"] - a["x1"], a["x0"] - b_["x1"], 0.0)
    dy = max(b_["y0"] - a["y1"], a["y0"] - b_["y1"], 0.0)
    return math.hypot(dx, dy)


def _contains(a, b_, m: float = 0.0) -> bool:
    return (a["x0"] - m <= b_["x0"] and a["y0"] - m <= b_["y0"] and
            a["x1"] + m >= b_["x1"] and a["y1"] + m >= b_["y1"])


def _is_decor(r) -> bool:
    return (r["kind"] == "hl" or
            any((r.get("name") or "").startswith(p) for p in DECOR_PREFIXES))


def label_host(b, lab, wins=None):
    """The object a written key names: the nearest concurrent, non-decorative,
    non-type rigid inside `LABEL_WELD_U`.  A key CONTAINED by a shape is that
    shape's own content, not a label beside it."""
    wins = wins if wins is not None else effective_windows(b)
    cands = [r for r in b.rigids
             if r is not lab and r["kind"] not in ("type", "ring", "hl",
                                                   "boxemph")
             and not _is_decor(r)
             and _win_overlap(wins[id(r)], wins[id(lab)])]
    for r in cands:
        if _contains(r, lab, 1.0):
            return None                       # inside its container
    near = [(_rect_gap(r, lab), r) for r in cands]
    near = [(d, r) for d, r in near if d <= LABEL_WELD_U]
    if not near:
        return None
    near.sort(key=lambda p: p[0])
    return near[0][1]


def assert_label_side(b, plan: dict) -> dict:
    """ROUND-4 LAW 3 — "when we name things I would rather the text be at the
    top or bottom".  For every planned key that welds to an object, the key's
    centre must fall inside the object's horizontal extent (+/- 15 %) and the
    key must sit ABOVE or BELOW it.  Beside is an error."""
    wins = effective_windows(b)
    labs = {r["name"][5:]: r for r in b.rigids
            if r["kind"] == "type" and (r.get("name") or "").startswith("type:")}
    bad, rep = [], {}
    for word in plan.values():
        lab = labs.get(word)
        if lab is None:
            continue                          # assert_label_law owns absence
        host = label_host(b, lab, wins)
        if host is None:
            rep[word] = "unwelded"
            continue
        span = host["x1"] - host["x0"]
        hcx = (host["x0"] + host["x1"]) / 2
        lcx = (lab["x0"] + lab["x1"]) / 2
        off = abs(lcx - hcx)
        band = span * (0.5 + LABEL_AXIS_FRAC)
        above = lab["y1"] <= host["y0"] + 1.0
        below = lab["y0"] >= host["y1"] - 1.0
        rep[word] = {"host": host.get("name") or host["kind"],
                     "dx_u": round(lcx - hcx, 1), "band_u": round(band, 1),
                     "place": "above" if above else "below" if below else "beside"}
        if off > band or not (above or below):
            bad.append(f"{word!r} sits {rep[word]['place']} "
                       f"{host.get('name') or host['kind']!r}: centre off by "
                       f"{lcx - hcx:+.1f}u against a +/-{band:.1f}u band")
    if bad:
        raise SystemExit("ROUND-4 LAW 3 — a name goes ABOVE or BELOW the thing "
                         "it names, never beside it:\n  " + "\n  ".join(bad))
    return {"checked": len(rep), "detail": rep, "verdict": "PASS"}


# --- LAW 5: THE SPACING LAW / NO CRAMP ---------------------------------------
# Miguel's screenshot: IMPOSSIBLE TASK, the CODEX tile, the clock and the
# TEMP/PROGRESS panel jammed together, and the CODEX->panel arrow drawn straight
# through the word CODEX.
#
# CALIBRATION (measured, 2026-09-02, on the authored boards):
#   impossibletask_whiteboard  job-card | monitor-card        0.0 u   (touching)
#                              clock-ring | codex-tile        8.0 u
#                              clock | codex-tile            12.0 u
#   kimiram_whiteboard (APPROVED, must stay silent)
#                              kimi bricks | mark:deepseek   10.2 u  <- the floor
#                              type:KIMI K3 | mark:deepseek  12.0 u
# Miguel's stated rule is 24 frame px = 12.8 u.  At 12.8 u the APPROVED board
# reports three pairs, so 12.8 u cannot be the refusal line for this format:
# the gate is set at 8.5 u (15.9 px), the largest round value strictly under the
# approved floor, and 12.8 u is kept as the ADVISORY line the plan aims for.
GUTTER_ERR_U = 8.5                 # 15.9 frame px — refuses the build
GUTTER_AIM_U = u_of_px(24.0)       # 12.8 u — Miguel's number, reported not enforced


# --- INK EXTENTS — the clerk's instrument note (round 4, 2026-09-02) ----------
# THE FINDING.  The round-4 clerk measured the tightest board ink against the
# caption pill on DECODED PIXELS and got 29 px where this harness reported 2.5:
#
#   "2.5 px is a LINE-BOX number, not an ink number: the `PROJECTS` text
#    element's box carries descender leading below the glyphs, so its box bottom
#    lands ~2.5 px above the pill while the ink itself is 29 px clear...  If the
#    builder wants the gate to agree with the eye, the fix is to measure ink
#    extents rather than element boxes, not to move the type."
#
# `Board.label` registers the CSS LINE BOX: top = baseline - 1.10*fs, height =
# 1.55*fs, and a width from `text_w()` that pads fs*0.55 of side bearing.  None
# of that is ink.  The glyphs occupy cap height above the baseline and reach
# below it only when the string actually carries a descender.
#
# Poppins metrics (unitsPerEm 1000): capHeight 700, ascenders ~750, descender
# -210.  A round cap (O S G C Q) overshoots the cap line by ~1.5 %, so the top is
# taken at 0.72 em.  Measured against the clerk: PROJECTS at fs=22u, baseline
# 415u -> ink bottom 415u = 778.1 px; the clerk's lowest dark ink on that beat is
# y = 777.  One pixel, and that pixel is antialiasing.
#
# THIS CHANGES NO THRESHOLD AND NO VERDICT.  Every gate keeps its box-based
# number and its box-based pass/fail; the ink number is computed beside it so the
# instrument and the eye can be compared in one place.  Ink boxes are strictly
# SMALLER than line boxes, so an ink pass can never hide a box failure.
TYPE_CAP_EM = 0.72        # cap height + round-cap overshoot
TYPE_ASC_EM = 0.78        # b d f h k l t — taller than the cap line
TYPE_DESC_EM = 0.22       # g j p q y and the comma
TYPE_SIDE_EM = 0.275      # half of text_w()'s fs*0.55 side-bearing pad
_DESCENDER_CHARS = set("gjpqy,;$(){}[]/@")
_ASCENDER_CHARS = set("bdfhklt")


def type_ink_box(r: dict) -> dict:
    """The GLYPH-INK box of a rigid.  `type` rigids shrink from their line box to
    their drawn extent; every other kind is already ink and is returned as-is."""
    if r.get("kind") != "type":
        return r
    name = r.get("name") or ""
    text = name[5:] if name.startswith("type:") else ""
    fs = (r["y1"] - r["y0"]) / 1.55
    baseline = r["y0"] + 1.10 * fs
    top_em = TYPE_ASC_EM if any(c in _ASCENDER_CHARS for c in text) else TYPE_CAP_EM
    bot_em = TYPE_DESC_EM if any(c in _DESCENDER_CHARS for c in text) else 0.0
    side = TYPE_SIDE_EM * fs
    return dict(r, x0=r["x0"] + side, x1=r["x1"] - side,
                y0=baseline - top_em * fs, y1=baseline + bot_em * fs)


@contextlib.contextmanager
def ink_extents(b):
    """Swap every `type` rigid's LINE BOX for its GLYPH-INK box for the duration
    of the block, then put the line boxes back.  The registry is shared with the
    camera solver and the lifetime law, so the swap is always restored."""
    saved = [(r, r["x0"], r["y0"], r["x1"], r["y1"]) for r in b.rigids
             if r.get("kind") == "type"]
    for r, *_ in saved:
        r.update({k: v for k, v in type_ink_box(r).items()
                  if k in ("x0", "y0", "x1", "y1")})
    try:
        yield b
    finally:
        for r, x0, y0, x1, y1 in saved:
            r.update(x0=x0, y0=y0, x1=x1, y1=y1)


def board_ink_bottom_px(b, *, ink: bool = False) -> float:
    """The lowest drawn ink on the board, in frame px.  `ink=False` (default) is
    the line-box number every gate has always used; `ink=True` is the glyph-ink
    number the clerk measures on decoded pixels."""
    rigids = [type_ink_box(r) for r in b.rigids] if ink else b.rigids
    return max([r["y1"] * core.S for r in rigids]
               + [max(p[1] for p in s["pts"]) for s in b.strokes])


def assert_spacing_law(b, *, blocks=(), gutter_u: float = GUTTER_ERR_U,
                       ink: bool = False) -> dict:
    """ROUND-4 LAW 5. Pairwise gutter between concurrently visible objects.

    `blocks` is a sequence of name-tuples authored as ONE object (a stack of
    bricks, a lockup).  Members of a block are exempt from each other, never
    from the rest of the board.  Three blocks are formed automatically, because
    each is already a law:
      * a key welded to the object it names (GLOBAL LAW 9 / ROUND-4 LAW 3),
      * everything a single container holds (composition, not a gutter),
      * a run of printed type stacked on a shared column (a paragraph).

    `ink=True` measures the same pairs on GLYPH-INK extents instead of line boxes
    (see `type_ink_box`).  It is a REPORT ONLY — `build()` never gates on it, the
    threshold is untouched, and because ink boxes are strictly smaller than line
    boxes an ink run can only ever be looser than the box run it accompanies.
    """
    if ink:
        with ink_extents(b):
            rep = assert_spacing_law(b, blocks=blocks, gutter_u=gutter_u)
        return dict(rep, measured_on="glyph ink extents")
    wins = effective_windows(b)
    blk: dict[str, int] = {}
    for i, grp in enumerate(blocks):
        for n in grp:
            blk[n] = i
    judged = [r for r in b.rigids
              if r["kind"] not in ("ring", "hl") and not _is_decor(r)]
    weld: dict[int, str] = {}
    for lab in [r for r in judged if r["kind"] == "type"]:
        host = label_host(b, lab, wins)
        if host is not None:
            weld[id(lab)] = _base_name(host)
    # the smallest shape that fully holds a rigid is its container
    holder: dict[int, int] = {}
    for r in judged:
        best = None
        for c in judged:
            if c is r or c["kind"] == "type":
                continue
            if not _win_overlap(wins[id(c)], wins[id(r)]):
                continue
            if _contains(c, r, 1.0) and _area(c) > _area(r) + 1e-6:
                if best is None or _area(c) < _area(best):
                    best = c
        if best is not None:
            holder[id(r)] = id(best)

    def paragraph(a, c) -> bool:
        """Two printed lines on a shared column are ONE piece of type."""
        if a["kind"] != "type" or c["kind"] != "type":
            return False
        ox = min(a["x1"], c["x1"]) - max(a["x0"], c["x0"])
        lead = 1.2 * max(a["y1"] - a["y0"], c["y1"] - c["y0"])
        return ox > 0.0 and _rect_gap(a, c) <= lead

    def stacked(a, c) -> bool:
        """Identical shapes on a shared column, tighter than their own height:
        a STACK (memory bricks, rows of a ladder) is one object, not a gutter."""
        if a["kind"] == "type" or c["kind"] == "type":
            return False
        same = (abs(a["x0"] - c["x0"]) <= 1.0 and abs(a["x1"] - c["x1"]) <= 1.0 and
                abs((a["y1"] - a["y0"]) - (c["y1"] - c["y0"])) <= 1.0)
        h = min(a["y1"] - a["y0"], c["y1"] - c["y0"])
        return same and _rect_gap(a, c) <= 0.35 * h

    # A `box_emphasis()` is ONE BLOCK with the object it picks out and with
    # that object's written key: the box is drawn on purpose at BOX_PAD_U, and
    # a key welded to a boxed object is inside the same argument.  It is judged
    # against every OTHER neighbour, which is the crowding Miguel's law means.
    boxed: dict[int, set[str]] = {}
    for bx in (r for r in judged if r["kind"] == "boxemph"):
        held = {bx.get("target") or ""}
        for r in judged:
            if r is bx or not _win_overlap(wins[id(bx)], wins[id(r)]):
                continue
            if _contains(bx, r, 1.0):
                held.add(_base_name(r))
                held.add(weld.get(id(r)) or "")
        boxed[id(bx)] = {n for n in held if n}

    def same_block(a, c) -> bool:
        for bx, other in ((a, c), (c, a)):
            if bx["kind"] != "boxemph":
                continue
            held = boxed.get(id(bx), set())
            if _base_name(other) in held or (weld.get(id(other)) or "") in held:
                return True
        na, nc = a.get("name") or "", c.get("name") or ""
        if _base_name(a) and _base_name(a) == _base_name(c):
            return True                        # one object, two placements
        if na in blk and nc in blk and blk[na] == blk[nc]:
            return True
        if (weld.get(id(a)) == _base_name(c) and _base_name(c)) or \
           (weld.get(id(c)) == _base_name(a) and _base_name(a)):
            return True
        if id(a) in holder and holder[id(a)] == holder.get(id(c)):
            return True
        return paragraph(a, c) or stacked(a, c)

    tight, aim = [], []
    for i in range(len(judged)):
        for j in range(i + 1, len(judged)):
            a, c = judged[i], judged[j]
            if not _win_overlap(wins[id(a)], wins[id(c)]):
                continue
            if _contains(a, c) or _contains(c, a):
                continue                       # composition, not a gutter
            ox = min(a["x1"], c["x1"]) - max(a["x0"], c["x0"])
            oy = min(a["y1"], c["y1"]) - max(a["y0"], c["y0"])
            if ox > 0.0 and oy > 0.0:
                continue                       # real overlap: LAW 2 owns it
            if "@" in (a.get("name") or "") or "@" in (c.get("name") or ""):
                continue          # a placement twin is a TRANSITION, never judged
            if same_block(a, c):
                continue
            g = _rect_gap(a, c)
            line = (f"{a.get('name') or a['kind']} | {c.get('name') or c['kind']}"
                    f" = {g:.1f}u ({g * core.S:.1f} px)")
            if g < gutter_u:
                tight.append(line)
            elif g < GUTTER_AIM_U:
                aim.append(line)
    if tight:
        raise SystemExit(
            f"ROUND-4 LAW 5 — cramp: objects closer than {gutter_u:.1f}u "
            f"({gutter_u * core.S:.1f} px) with no block declared:\n  " +
            "\n  ".join(sorted(set(tight))) +
            "\n  Move them apart, or declare them one object via blocks=.")
    return {"gate_u": gutter_u, "gate_px": round(gutter_u * core.S, 1),
            "aim_u": round(GUTTER_AIM_U, 2), "aim_px": 24.0,
            "measured_on": "element line boxes",
            "under_aim": sorted(set(aim)), "objects": len(judged),
            "verdict": "PASS"}


def assert_no_text_crossing(b) -> dict:
    """ROUND-4 LAW 5, second half: a connector NEVER crosses a text bbox.

    Reads the authored pen paths (`Board.strokes`, frame px) against the type
    rigids, both clamped to their chapter.  A stroke whose own bounding box
    CONTAINS the text is that text's container (a card, a ring) and is judged
    by LAW 2, not here; a 2-point path is a label underline or a pen dab.
    """
    S = core.S
    wins = effective_windows(b)
    seams = chapter_seams(b)
    types = [r for r in b.rigids if r["kind"] == "type" and "@" not in (r.get("name") or "")]
    moving = [wins[id(r)] for r in b.rigids if "@" in (r.get("name") or "")]
    bad = []
    for s_ in b.strokes:
        pts = s_["pts"]
        if len(pts) < 2 or (len(set(map(tuple, pts))) == 1):
            continue              # a pen dab, not a path
        if any(w[0] - 1e-6 <= s_["t"] < w[1] for w in moving):
            continue              # drawn during an entrance/placement move
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        nxt = [x for x in seams if x > s_["t"] + 1e-6]
        sw = (s_["t"], nxt[0] if nxt else 1e9)
        sb = {"x0": min(xs) / S, "y0": min(ys) / S,
              "x1": max(xs) / S, "y1": max(ys) / S}
        for r in types:
            if _contains(sb, r, 2.0) or _contains(r, sb, 2.0):
                # the text's own container, or the pen writing THAT word
                continue
            if not _win_overlap(sw, wins[id(r)]):
                continue
            # THE CORE BAND.  An underline or a strike grazes the type's edge;
            # a CROSSING goes through the letters.  Only the core is protected.
            hh, ww = r["y1"] - r["y0"], r["x1"] - r["x0"]
            core_box = {"x0": r["x0"] + 0.04 * ww, "x1": r["x1"] - 0.04 * ww,
                        "y0": r["y0"] + 0.22 * hh, "y1": r["y1"] - 0.28 * hh}
            hit = None
            for k in range(len(pts) - 1):
                if _seg_hits_box(pts[k][0] / S, pts[k][1] / S,
                                 pts[k + 1][0] / S, pts[k + 1][1] / S, core_box):
                    hit = (pts[k][0] / S, pts[k][1] / S)
                    break
            if hit:
                bad.append(f"a stroke drawn at {s_['t']:.2f}s crosses "
                           f"{r['name']!r} at ({hit[0]:.0f},{hit[1]:.0f})u")
    if bad:
        raise SystemExit("ROUND-4 LAW 5 — a connector crossed printed type:\n  "
                         + "\n  ".join(sorted(set(bad))) +
                         "\n  Re-route the connector, or move the key: a name is "
                         "never something an arrow passes through.")
    return {"strokes": len(b.strokes), "types": len(types), "verdict": "PASS"}


def _seg_hits_box(x0, y0, x1, y1, r) -> bool:
    bx0, by0, bx1, by1 = r["x0"], r["y0"], r["x1"], r["y1"]
    if max(x0, x1) < bx0 or min(x0, x1) > bx1:
        return False
    if max(y0, y1) < by0 or min(y0, y1) > by1:
        return False
    if bx0 <= x0 <= bx1 and by0 <= y0 <= by1:
        return True
    if bx0 <= x1 <= bx1 and by0 <= y1 <= by1:
        return True
    dx, dy = x1 - x0, y1 - y0
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x0 - bx0), (dx, bx1 - x0), (-dy, y0 - by0), (dy, by1 - y0)):
        if abs(p) < 1e-12:
            if q < 0:
                return False
            continue
        t = q / p
        if p < 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
        if t0 > t1:
            return False
    return True


# --- LAW 6: A MARK LEAVES WHEN ITS BEAT IS DONE ------------------------------
# Miguel: "The perplexity logo stays and just bothers the entire flow."
ANCHOR_MAX_FRAC = 0.40             # visible longer than this without 'anchor' = error


def assert_lifetime_law(b, dur: float, *, anchors=(), single_board: bool = False,
                        max_frac: float = ANCHOR_MAX_FRAC) -> dict:
    """ROUND-4 LAW 6. Every drawn element declares a LIFETIME — a beat range, or
    the role `anchor`.

    A SINGLE-BOARD build (ROUND-4 LAW 7's exception: one idea that accumulates)
    is all-anchor by definition and is detected automatically — no rigid has a
    finite `t1`, so nothing was ever meant to leave.  A CHAPTERED build (any
    finite `t1` at all: the board erases) must give every mark either a finite
    `t1` or a place in `anchors`.
    """
    chaptered = bool(chapter_seams(b)) and not single_board
    keep = set(anchors)
    forever = [r for r in b.rigids
               if r["t1"] >= 1e8 and (dur - r["t0"]) > max_frac * dur
               and (r.get("name") or "") not in keep and not _is_decor(r)]
    rep = {"duration_s": round(dur, 2), "chaptered": chaptered,
           "max_frac": max_frac, "declared_anchors": sorted(keep),
           "lingering": [f"{r.get('name') or r['kind']} from {r['t0']:.2f}s "
                         f"({(dur - r['t0']) / dur:.0%} of the take)"
                         for r in forever]}
    if chaptered and forever:
        raise SystemExit(
            f"ROUND-4 LAW 6 — a mark stays past its beat.  This board ERASES "
            f"(it is chaptered), so every mark declares a lifetime: give it a "
            f"finite t_to in Board.rigid(), or name it in anchors=.\n  " +
            "\n  ".join(rep["lingering"]))
    rep["verdict"] = "PASS" if chaptered else "PASS (single board: all anchors)"
    return rep


# =============================================================================
# THE ZERO-INK LAW — proved on the decoded render, every frame, no sampling
# =============================================================================
def assert_zone_never_blank(mp4: Path, *, t_first_word: float,
                            zone_bottom: float = CAP_BAND_TOP_PX,
                            ink_floor: float = 1e-9) -> dict:
    """LAW: the visual zone's ink NEVER reaches zero, anywhere in the render.

    The visual zone is everything above the caption pill's reserved band, which
    is the region the viewer test measures — a caption pill is not a picture, so
    a frame carrying only a pill is a frame arguing nothing.

    Two exclusions, both of them the OPENING and nothing else:

      * frames before the first spoken word — there is no sentence yet for a
        picture to argue;
      * the composition's LEADING empty run, the contiguous stretch of cream from
        frame 0 while the first mark fades up.  A leading run can spill one frame
        past the first word (`perplexityprojects` starts speaking at 0.199 s and
        frame 5 lands at 0.200 s) and that frame is the tail of the opening, not
        a hole in the middle of an argument.  The instant ANY ink has appeared,
        the zone may never empty again — which is the whole law.

    Everything else must hold ink.  The whiteboard, the format this check was
    written for, satisfies the strict reading too: its leading run is two frames
    and it never touches zero afterwards.

    The scan is `clip_coverage_check.zone_ink_series` — the factory's existing
    per-frame ink instrument, reused rather than re-implemented so this check and
    the clip-coverage check can never disagree about what "ink" means.
    """
    sys.path.insert(0, str(F / "pipeline"))
    from clip_coverage_check import zone_ink_series             # noqa: E402

    fps, y1, w, frac = zone_ink_series(Path(mp4), zone_bottom)
    if not frac:
        raise SystemExit(f"{mp4} decoded to zero frames")
    lead = 0
    while lead < len(frac) and frac[lead] <= ink_floor:
        lead += 1
    k0 = max(lead, int(math.ceil(t_first_word * fps - 1e-9)))
    judged = frac[k0:]
    if not judged:
        raise SystemExit(f"{mp4} holds no ink at all after {t_first_word}s")
    blanks = [{"frame": k0 + i, "t": round((k0 + i) / fps, 4),
               "ink_frac": round(v, 8)}
              for i, v in enumerate(judged) if v <= ink_floor]
    rec = {"render": str(mp4), "frames": len(frac), "fps": round(fps, 3),
           "zone_bottom_design_px": zone_bottom,
           "zone_px": [w, y1], "first_word_s": round(t_first_word, 3),
           "leading_empty_frames": lead,
           "first_judged_frame": k0,
           "min_ink_frac_judged": round(min(judged), 8),
           "min_ink_frac_at_s": round((k0 + judged.index(min(judged))) / fps, 3),
           "blank_frames": blanks,
           "verdict": "PASS" if not blanks else "FAIL"}
    if blanks:
        span = f"{blanks[0]['t']:.2f}-{blanks[-1]['t']:.2f}s"
        raise SystemExit(
            f"ZERO-INK LAW — the visual zone holds no ink for "
            f"{len(blanks)} frame(s) ({span}) in {Path(mp4).name}. "
            "An empty visual zone is always NO-SENSE.")
    return rec


def probe(path: Path) -> float:
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)], check=True, capture_output=True,
        text=True).stdout.strip())


# =============================================================================
# transcript + anchors
# =============================================================================
def load_words(vid: str) -> list[dict]:
    data = json.loads((RUN / f"cuts/{vid}/transcript_tight.json").read_text())
    return [w for w in data["words"] if w.get("type") == "word"]


def anchors(words: list[dict], spec: dict[str, tuple[int, str]]) -> dict[str, float]:
    """Pin every cue to word INDEX **and** word TEXT (chassis rule)."""
    out: dict[str, float] = {}
    for key, (idx, want) in spec.items():
        got = re.sub(r"[^a-z0-9.]", "", words[idx]["text"].lower())
        if got != want:
            raise SystemExit(f"anchor {key}: word {idx} is {got!r}, expected {want!r}")
        out[key] = round(float(words[idx]["start"]), 2)
    return out


# =============================================================================
# staging — the chassis' own stage layout, per video
# =============================================================================
def stage(vid: str, stage_dir: Path, marks: dict[str, Path]) -> dict:
    cut = RUN / f"cuts/{vid}"
    for rel in ("v", "logos", "music", "sfx"):
        (stage_dir / rel).mkdir(parents=True, exist_ok=True)

    # VOICE — the 48 kHz cut master.  A 16 kHz analysis wav is never staged.
    voice = stage_dir / "v/audio.m4a"
    src_voice = cut / "audio.m4a"
    rate = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
         "stream=sample_rate", "-of", "csv=p=0", str(src_voice)],
        check=True, capture_output=True, text=True).stdout.strip()
    if int(rate) < 44100:
        raise SystemExit(f"{src_voice} is {rate} Hz — refusing an analysis-rate voice")
    if not voice.exists() or voice.stat().st_mtime < src_voice.stat().st_mtime:
        shutil.copy2(src_voice, voice)

    # FACE BAND — 1080x1058, the plate that sits under the seam.  Built once from
    # the cut's own bottom crop (cut at 1080x1058 since HD delivery, 2026-09-03;
    # the scale below is then a 1x no-op); never re-derived from the raw.
    band = stage_dir / "v/face_band.mp4"
    src_face = cut / "face_bottom_hd.mp4"
    if not src_face.exists() and (cut / "face_bottom_4k.mp4").exists():
        src_face = cut / "face_bottom_4k.mp4"   # pre-2026-09-03 cuts (runs 1-10)
    if not band.exists() or band.stat().st_mtime < src_face.stat().st_mtime:
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src_face),
             "-vf", "scale=1080:1058:flags=lanczos", "-r", "25",
             "-c:v", "libx264", "-preset", "medium", "-crf", "16",
             "-g", "25", "-keyint_min", "25", "-pix_fmt", "yuv420p",
             "-movflags", "+faststart", "-an", str(band)], check=True)

    shutil.copy2(BED, stage_dir / "music/bed_split.mp3")
    for name in core.PALETTE:
        shutil.copy2(library_asset(SHARED_SFX / f"{name}.mp3"), stage_dir / "sfx" / f"{name}.mp3")
    if not PEN_SRC.exists():
        raise SystemExit(f"{PEN_SRC} missing — the tamed pen is not on disk")
    shutil.copy2(PEN_SRC, stage_dir / "sfx" / core.PEN_FILE)

    media: dict[str, str] = {}
    for key, src in marks.items():
        if not src.exists():
            raise SystemExit(f"missing registry mark: {src}")
        shutil.copy2(src, stage_dir / "logos" / f"{key}{src.suffix}")
        media[key] = f"assets/logos/{key}{src.suffix}"
    return media


def bind(project: Path, stage_dir: Path) -> None:
    project.mkdir(parents=True, exist_ok=True)
    dest = project / "assets"
    if dest.is_symlink():
        dest.unlink()
    elif dest.exists():
        shutil.rmtree(dest)
    dest.symlink_to(stage_dir.resolve(), target_is_directory=True)


# =============================================================================
# outro — the chassis' themed outro, with the handle as the one parameter
# =============================================================================
def outro_block(t0: float, dur: float, handle: str, daily_t: float,
                board_ink_top_px: float) -> tuple[str, list[str], dict]:
    """THE OUTRO — A CLEAN SHEET RISES OVER THE BOARD (run 9, round 3).

    Round 1 shipped the card as a fade over a 94 %-opaque scrim, so the last
    3.4 s was a double exposure: "@migueltorrez.ai printed directly on top of the
    ghost diagram". Round 2 fixed that by ERASING first — board out, then card in
    — and bought the opposite defect at the same seam: **15 frames of a totally
    empty visual zone** (26.08-26.64 s, 0.000 % ink), across three spoken words.
    Fade-then-fade cannot win. Either the two overlap in TIME (a ghost) or they
    do not (a hole), and dialling the numbers only moves the failure.

    So this outro does not fade at all. An OPAQUE cream sheet, carrying the rule,
    the handle and `daily AI` already printed on it, rises from below the zone
    and covers the board — the most literal move a whiteboard has, a fresh sheet
    pulled up over the old one. Two facts fall out of the geometry and hold for
    every ease and every duration:

      * the sheet is opaque and full-zone, so no diagram pixel can read through
        or beside the card — round 1's defect is impossible, not merely avoided;
      * the sheet's edge covers the board's last ink only at travel
        `ZONE_H - board_ink_top`, and the card's own ink crosses into the zone at
        travel `card_ink_top`. `card_ink_top < ZONE_H - board_ink_top` makes the
        two windows OVERLAP, so at every instant of the wipe the zone holds the
        board, or the card, or (for most of it) both — round 2's defect is
        impossible too.

    The board itself never moves and never fades: its ink is at full strength
    right up to the pixel row the sheet's edge reaches, which is why the ink
    curve has no valley instead of merely a shallow one.

    `daily AI` is the one element that still fades, on its own word, on top of a
    sheet that is already carrying two other pieces of ink.
    """
    lift = px(ZONE_H)
    card_ink_top = px(OUTRO_RULE_TOP_U)
    board_covered = lift - board_ink_top_px
    html = (
        f'  <section id="outro" class="clip" style="left:0;top:0;width:1080px;'
        f'height:{px(ZONE_H)}px;overflow:hidden" data-start="{t0:.2f}" '
        f'data-duration="{dur - t0:.2f}" data-track-index="20">\n'
        # THE SHEET.  Opaque — a veil is not a sheet — and exactly zone-sized, so
        # `data-bleed` (it is the surface, its edges ARE the zone's edges).
        f'    <div id="osheet" data-bleed style="position:absolute;left:0;top:0;'
        f'width:1080px;height:{px(ZONE_H)}px;background:{CREAM}">\n'
        f'      <div id="o-rule" class="oc" style="top:{px(OUTRO_RULE_TOP_U)}px">'
        f'<span style="display:inline-block;width:{px(150)}px;height:{px(6)}px;'
        f'background:{TERRA};border-radius:{px(3)}px"></span></div>\n'
        f'      <div id="o-handle" class="oc" style="top:{px(OUTRO_HANDLE_TOP_U)}px;'
        f"font-family:'JetBrains Mono',monospace;font-weight:700;"
        f'font-size:{px(30)}px;letter-spacing:{px(1.2)}px;color:{INK};'
        f'line-height:{px(41)}px">{esc(handle)}</div>\n'
        f'      <div id="o-daily" class="oc" style="top:{px(OUTRO_DAILY_TOP_U)}px;'
        f"font-family:'JetBrains Mono',monospace;font-weight:500;"
        f'font-size:{px(13)}px;letter-spacing:{px(4.4)}px;color:{TERRA}">'
        f'daily AI</div>\n'
        f'    </div>\n  </section>'
    )
    tw = [
        f'tl.set("#osheet",{{y:{lift:.1f}}},0);tl.set("#o-daily",{{opacity:0}},0);',
        f'tl.fromTo("#osheet",{{y:{lift:.1f}}},{{y:0,duration:{OUTRO_WIPE:.2f},'
        f'ease:SWING,immediateRender:false}},{t0:.2f});',
        f'tl.fromTo("#o-daily",{{opacity:0}},{{opacity:1,duration:0.34,ease:SOFT,'
        f'immediateRender:false}},{max(daily_t, t0 + OUTRO_WIPE + 0.20):.2f});',
    ]
    return html, tw, {
        "move": "opaque sheet rises over the board",
        "wipe_start": round(t0, 2), "wipe_end": round(t0 + OUTRO_WIPE, 2),
        "travel_px": round(lift, 1),
        "sheet_opaque": True, "sheet_covers_px": round(lift, 1),
        "card_ink_enters_px": round(card_ink_top, 1),
        "board_covered_px": round(board_covered, 1),
        "overlap_px": round(board_covered - card_ink_top, 1),
        "board_moves": False, "board_fades": False,
    }


# =============================================================================
# page guards
# =============================================================================
def audit_page(html: str) -> None:
    ids = re.findall(r'\sid="([^"]+)"', html)
    dupes = sorted(k for k, v in Counter(ids).items() if v > 1)
    if dupes:
        raise SystemExit(f"duplicate ids: {dupes}")
    known = set(ids)
    script = html.split("<script>")[-1]
    missing = {sel.strip().lstrip("#")
               for m in re.finditer(r'tl\.(?:set|to|fromTo)\("([^"]+)"', script)
               for sel in m.group(1).split(",")
               if not sel.strip().startswith(".")
               and sel.strip().lstrip("#") not in known}
    if missing:
        raise SystemExit(f"tween targets that do not exist: {sorted(missing)}")


def caption_identity_guard(b, board_text: list[str], beats: list[dict]) -> dict:
    """LAW 4: no drawn word may repeat a caption pill **that is on screen with it**.

    Run 9 made the law's real shape visible.  The whiteboard's own chunker emits a
    pill reading exactly "research desk," — and RESEARCH DESK is the video's key
    term, the one word the viewer test held the render for NOT writing.  A
    time-blind guard makes those two requirements contradictory.

    They are not.  Law 4 exists so a viewer never reads the same string twice IN
    ONE FRAME.  A pill lives in a window; a board word lives from the stroke that
    writes it to the end of the take.  The test is therefore an OVERLAP test: a
    board word is illegal only if an identical pill is still alive when it is
    written.  Written after that pill has left, it is simply the board.

    This is stricter than it sounds — it still refuses every simultaneous double,
    which is every case the law was ever aimed at — and it is the only reading
    under which a key term the script speaks can also be written.
    """
    def n(s: str) -> str:
        return " ".join(re.sub(r"[^a-z0-9 ]", " ", s.lower()).split())

    # THE BOARD WORD'S LIFETIME IS ITS RIGID'S WINDOW, NOT "TO THE END OF THE
    # TAKE" (codexnondev, 2026-09-02).  The docstring above already states the
    # right law — "a board word is illegal only if an identical pill is still
    # alive when it is written" — but it modelled a board word as immortal,
    # which was true of the single board this guard was written for.  ROUND-4
    # LAW 43 made CHAPTERS the default, and a chaptered board ERASES: on the
    # first chaptered whiteboard to hit it, `CHATGPT WORK` is written at 17.30 s
    # and rubbed out at 21.42 s, and the guard refused the build over a pill at
    # 30.82-31.88 s that could not share a single frame with it.  The window is
    # already on the rigid (`t_to`, which LAW 42 makes mandatory on a chaptered
    # board), so the fix is to read it.  This can only ever ACCEPT builds the old
    # form accepted — a mark with no finite `t_to` still reads as immortal.
    written = {}
    for r in b.rigids:
        if r["kind"] == "type" and r["name"].startswith("type:"):
            key0 = n(r["name"][5:])
            t0, t1 = float(r["t0"]), float(r["t1"])
            if key0 in written:      # the same word written twice: union
                t0, t1 = min(t0, written[key0][0]), max(t1, written[key0][1])
            written[key0] = (t0, t1)
    clashes = []
    for beat in beats:
        key = n(beat["text"])
        if key not in written:
            continue
        w0, w1 = written[key]
        if w0 < float(beat["t1"]) - 1e-6 and float(beat["t0"]) < w1 - 1e-6:
            clashes.append(f"board text {beat['text']!r} is on the board "
                           f"{w0:.2f}-{w1:.2f}s while the identical pill is on "
                           f"screen ({beat['t0']:.2f}-{beat['t1']:.2f}s)")
    if clashes:
        raise SystemExit("LAW 4 — double caption:\n  " + "\n  ".join(clashes))
    near = {t: [round(written[n(t)][0], 2), round(written[n(t)][1], 2)]
            for t in board_text if n(t) in written
            and any(n(t) == n(x["text"]) for x in beats)}
    return {"law": "4 (overlap test)", "board_words_that_also_appear_as_a_pill": near}


# =============================================================================
# build
# =============================================================================
def build(*, vid: str, title: str, handle_key: str, draw, anchor_spec: dict,
          outro_key: str, daily_key: str, marks: dict[str, Path],
          board_box: tuple[float, float, float, float],
          label_plan: dict, key_term: str,
          comparisons=(),
          # ---- ROUND-4 LAWS (Miguel, 2026-09-02) -----------------------------
          # All optional, all additive.  A board that declares nothing is still
          # judged: the blocks the laws already imply (a key welded to its
          # object, a container's contents, a paragraph, a stack) are formed
          # automatically.  Declare only what the geometry cannot infer.
          blocks=(),          # LAW 5: name-tuples authored as ONE object
          connectors=(),      # LAW 4: [{"to": <rigid name>, "end": (x, y)}]
          board_anchors=(),   # LAW 6: rigid names that are allowed to persist
          ) -> tuple[Path, dict]:
    core.RNG.seed(20260902)
    handle = CAP.handle(handle_key)
    core.HANDLE = handle

    words = load_words(vid)
    a = anchors(words, anchor_spec)
    cut = RUN / f"cuts/{vid}"
    dur = round(probe(cut / "master.mp4"), 3)
    if float(words[-1]["end"]) > dur + 1e-3:
        raise SystemExit("the transcript runs past the container")

    stage_dir = RUN / f"stage/{vid}_whiteboard"
    project = RUN / f"projects/{vid}_whiteboard"
    media = stage(vid, stage_dir, marks)
    core.STAGE = stage_dir
    core.CAP_W_CACHE = Path(__file__).resolve().parent / "_capwidths_whiteboard.json"

    b = Board(1.0)
    board_text: list[str] = draw(b, a, media)

    # ---- LAW 12, statically, on the authored drawing -----------------------
    if b.ymin < TOP_BAND_U:
        raise SystemExit(f"LAW 12: ink at y={b.ymin:.1f}u is inside the top 10 % "
                         f"({TOP_BAND_U:.1f}u)")
    if b.railhits:
        raise SystemExit(f"LAW 12: right-rail intrusions: {b.railhits}")
    bb = board_box
    if abs((bb[0] + bb[2]) / 2 - AX) > 0.6:
        raise SystemExit("the board is off the composition axis")

    # ---- the marker, and the caption band ----------------------------------
    pen_art, pen_tw = core.pen_layer(b)
    pen_snd = core.pen_intervals(b.strokes, dur)
    tips = [min(p[1] for p in s["pts"]) / core.S for s in b.strokes]
    pen_top = min(tips + [board_box[1] + 2.0]) - PEN_REACH_U
    if pen_top < TOP_BAND_U:
        raise SystemExit(f"LAW 12: the marker reaches y={pen_top:.1f}u, inside the "
                         f"top 10 % ({TOP_BAND_U:.1f}u)")
    # THE GATE IS THE LINE-BOX NUMBER, unchanged.  The glyph-ink number beside it
    # is the clerk's instrument (see `board_ink_bottom_px`), reported only.
    ink_bottom_px = board_ink_bottom_px(b)
    ink_bottom_ink_px = board_ink_bottom_px(b, ink=True)
    if ink_bottom_px > CAP_BAND_TOP_PX:
        raise SystemExit(f"CAPTION BAND: ink reaches y={ink_bottom_px:.1f} px, "
                         f"inside the pill's band (top {CAP_BAND_TOP_PX:.1f} px)")

    # ---- captions, audio, outro --------------------------------------------
    phrases = core.build_captions(words)
    law4 = caption_identity_guard(b, board_text, phrases)
    # RUN 9 — the canon's function-word law.  The whiteboard's own chunker merges
    # single-word phrases and so never produced the "in" badge the split shipped,
    # but the law is asserted here too: it is the canon's, not the format's.
    CAP.assert_no_function_only_beat(phrases)
    audio, atw, astats = core.audio_block(dur, b.sfx, pen_snd)
    labels = assert_label_law(b, a, label_plan, board_text,
                              key_term=key_term, comparisons=comparisons)
    # ---- THE ROUND-4 LAWS, on the AUTHORED board ---------------------------
    # Order is the law's own: LAW 6 declares what is on screen when, and every
    # geometry law below reads those windows, so a lifetime error is reported
    # before a geometry error that only exists because a mark overstayed.
    round4 = {"law6_lifetimes": assert_lifetime_law(b, dur, anchors=board_anchors)}
    round4["law2_no_enclosure"] = assert_no_enclosure(b)
    round4["law3_label_side"] = assert_label_side(b, label_plan)
    round4["law5_spacing"] = assert_spacing_law(b, blocks=blocks)
    # The same pairs on glyph ink, reported beside the gate and never gating.
    try:
        round4["law5_spacing_ink"] = assert_spacing_law(b, blocks=blocks, ink=True)
    except SystemExit as e:                      # pragma: no cover — report only
        round4["law5_spacing_ink"] = {"measured_on": "glyph ink extents",
                                      "verdict": "REPORT", "note": str(e)}
    round4["law5_no_crossing"] = assert_no_text_crossing(b)
    round4["law4_anchors"] = assert_anchor_law(b, connectors)
    outro_html, otw, orep = outro_block(a[outro_key], dur, handle, a[daily_key],
                                        b.ymin * core.S)
    orep = assert_outro_clear(orep, b, a, outro_key)

    svg = (f'<svg id="svg" width="{px(b.w)}px" height="{px(b.h)}px" '
           f'viewBox="0 0 {px(b.w)} {px(b.h)}">'
           f'<defs>{"".join(b.defs)}</defs>{"".join(b.body)}{pen_art}</svg>')
    zone = (f'  <section id="tz" class="clip tz" data-start="0" '
            f'data-duration="{dur:.3f}" data-track-index="2">'
            # `data-bleed`: the camera surface IS the zone, so its bottom edge is
            # the seam by construction.  Without the opt-out Gate 1 reports one
            # `seam  cam touches the caption seam` — and it reports the SAME one
            # on the APPROVED chassis build (`formats/whiteboard/build/whiteboard`),
            # which is the negative control that proves it is a property of the
            # format's container, not of this drawing.
            f'<div id="cam" data-bleed style="width:{px(b.w)}px;'
            f'height:{px(b.h)}px">{svg}</div>'
            f'</section>')
    face = (f'  <video id="facebot" src="assets/v/face_band.mp4" data-start="0" '
            f'data-duration="{dur:.3f}" data-media-start="0" data-track-index="1" '
            f'muted playsinline style="position:absolute;top:{px(SEAM)}px;left:0;'
            f'width:1080px;height:{px(FACE_H)}px;object-fit:cover"></video>')
    # THE BOARD DOES NOT MOVE.  The outro is a sheet rising OVER it, so the
    # camera is a static placement for the whole take (Law 21).
    cam_tw = ['tl.set("#cam",{x:0,y:0,scale:1},0);']
    tweens = "".join(b.sets + cam_tw + b.tw + pen_tw + otw + atw)

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=1080, height=1920"/>
<title>{esc(title)}</title>{core.GSAP}{core.FONTS}
<style>{core.base_css()}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080"
 data-height="1920" data-duration="{dur:.3f}" data-fps="{FPS}">
{face}
{zone}
{outro_html}
{core.caption_clips(phrases, dur)}
{audio}
</div><script>
window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});
const POP="back.out(2.05)";const SOFT="power3.out";const SWING="power2.inOut";
const CAM="power2.inOut";
{tweens}
window.__timelines["main"]=tl;
</script></body></html>"""

    audit_page(page)
    if handle not in page:
        raise SystemExit("the outro handle is not in the page")
    other = CAP.HANDLE_YT if handle == CAP.HANDLE_TIKTOK_IG else CAP.HANDLE_TIKTOK_IG
    if other in page:
        raise SystemExit(f"the OTHER platform's handle {other} leaked in")

    bind(project, stage_dir)
    (project / "index.html").write_text(page, encoding="utf-8")

    stats = {
        "video": vid, "format": "whiteboard", "variant": "plan view (fix)",
        "project": str(project), "handle": handle, "handle_key": handle_key,
        "duration_s": dur, "fps": FPS,
        "render": "1080x1920 @ zoom 1",
        "board": f"{b.w:.0f}x{b.h:.0f} design units",
        "board_box": list(board_box),
        "strokes": len(b.strokes), "rigids": len(b.rigids),
        "board_text": board_text,
        "top_ink_u": round(b.ymin, 1), "top_band_u": round(TOP_BAND_U, 1),
        "pen_top_u": round(pen_top, 1),
        "ink_bottom_px": round(ink_bottom_px, 1),
        "cap_band_top_px": round(CAP_BAND_TOP_PX, 1),
        "cap_clearance_px": round(CAP_BAND_TOP_PX - ink_bottom_px, 1),
        # --- the same seam, measured on GLYPH INK (report only, no threshold) --
        "ink_bottom_ink_px": round(ink_bottom_ink_px, 1),
        "cap_clearance_ink_px": round(CAP_BAND_TOP_PX - ink_bottom_ink_px, 1),
        # the pill's real painted top edge — the surface the clerk measures
        # against; CAP_BAND_TOP_PX is the RESERVED band above it, 6.0 px higher.
        "seam_pill_top_px": round(px(SEAM) - CAP.CAP_PILL_HEIGHT / 2, 1),
        "cap_clearance_ink_to_pill_px": round(
            px(SEAM) - CAP.CAP_PILL_HEIGHT / 2 - ink_bottom_ink_px, 1),
        "seam_measures": "cap_clearance_px = line boxes vs the reserved band "
                         "(THE GATE); cap_clearance_ink_px = glyph ink vs the "
                         "same band; cap_clearance_ink_to_pill_px = glyph ink vs "
                         "the pill's painted top edge (the clerk's surface)",
        "rail_hits": b.railhits,
        "label_law": labels, "law4": law4, "round4": round4,
        "outro": orep,
        "captions": len(phrases),
        "cap_font_px": CAP.CAP_FONT,
        "cap_max_pill_w_px": round(max(p["pill_w_px"] for p in phrases), 1),
        "cap_w_budget_px": core.CAP_MAX_W_PX,
        "anchors": a,
        "html_bytes": len(page.encode()),
    } | astats
    return project, stats


# =============================================================================
# the verification lane — run AFTER the render, on the delivered file
# =============================================================================
def main() -> None:
    import argparse
    ap = argparse.ArgumentParser(description="prove the ZERO-INK LAW on a render")
    ap.add_argument("render", type=Path)
    ap.add_argument("--vid", required=True, help="cuts/<vid>/transcript_tight.json")
    ap.add_argument("--zone-bottom", type=float, default=CAP_BAND_TOP_PX)
    ap.add_argument("--json", type=Path, default=None)
    a = ap.parse_args()
    words = load_words(a.vid)
    rec = assert_zone_never_blank(a.render, t_first_word=float(words[0]["start"]),
                                 zone_bottom=a.zone_bottom)
    if a.json:
        a.json.write_text(json.dumps(rec, indent=1))
    print(json.dumps(rec, indent=1))


if __name__ == "__main__":
    main()
