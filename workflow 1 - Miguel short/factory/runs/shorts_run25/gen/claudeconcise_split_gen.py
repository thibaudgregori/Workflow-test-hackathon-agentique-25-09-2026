#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION — claudeconcise / DIAGRAM BUILD.

    YouTube   classic split 50/50   projects/claudeconcise_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/claudeconcise_scene.py`
plus `plans/claudeconcise_scene_handoff.md` are the design agent's artefacts,
sealed by `review/artwork_pass_claudeconcise.json` (production v4,
`production.py seal`).  This file IMPORTS the module and SEATS it at the
handoff's own placement (k = 1.00, left 0, core top 192).  It never mutates a
byte of the module on disk.

FORMAT-SIDE STAMPS ON THE EMITTED STRING (the module on disk is untouched):
  * every connector gets `data-anchor-side`, `data-anchor-fraction` and
    `data-check-at` (production's LAW 40 contract);
  * inkless virtual rectangles are inserted INSIDE their holders so they move
    with them: `#scroll-a-paper` (the long scroll's PAPER, the plan's landing
    rect for mascot -> scroll), `#scroll-b-note` (the paper that survives the
    snip: the short note), `#dial-knob` (the knob the ridge belongs to).  The two
    scroll arrows are retargeted onto them;
  * the two emphases are declared: the dial's grip ridge (fill flip, target the
    knob) and the short note's paper edge (border flip, target the short note);
  * the ANTHROPIC wordmark raster carries `id="mark-anthropic"` (the plan's own
    block name).

HD DELIVERY: authored AND encoded 1080x1920.  The face plate is
`face_bottom_hd.mp4` (1080x1058), seam 862.5, RENDERING pill top
862.5 - 114.59/2 = 805.205.  The core's content band 10..574 lands at canvas
202..766: 10 px under LAW 30's top-10 % line and 39.2 px over the pill.

TAKEOVER and FACESPLIT are not daily deliverables and this file cannot build one.
"""
from __future__ import annotations

import argparse
import html as ihtml
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

F = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(F / "pipeline"))
sys.path.insert(0, str(F / "pipeline/prep"))
sys.path.insert(0, str(F / "formats/cutout/lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import captions as CAP                          # noqa: E402
import cutout_core as CC                        # noqa: E402
import cutout_depthfield as DF                  # noqa: E402
import pointing_cues as PCUE                    # noqa: E402
import claudeconcise_scene as SC                # noqa: E402

RUN = Path(__file__).resolve().parents[1]
CUT = RUN / "cuts/claudeconcise"
PLAN = RUN / "plans/claudeconcise_plan.json"
ASSETS = Path.home() / "Documents/Workspace/assets"
LOGOS = ASSETS / "logos"
LIB_MUSIC = ASSETS / "audio/music/shorts-factory"
LIB_SFX = ASSETS / "audio/sfx/shorts-factory"

VID = "claudeconcise"
W, H = 1080.0, 1920.0
FPS = 25
DUR = SC.DUR                                     # 41.774, the cut master

SEAM = 862.5
CORE_TOP_SPLIT = SC.CANVAS_OFFSET                # 192.0, the handoff's number
CORE_K = 1.00
LEFT = (W - SC.CORE_W * CORE_K) / 2              # 0.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "Claude Code's Concise output style: short answers in plain English"
LABEL_WINDOW = 1.0

# ------------------------------------------------------------------ marks
# MARK IDENTITY: the FILE is named, never "the logo" (handoff section 1).
STAGE_FILES = {"claude-code": SC.LOGO_FILES["claude-code"],
               "anthropic-wordmark": SC.ANTH_FILE}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}
CUTOUT_LANES = SC.CUTOUT_LOGO_LANES

# ------------------------------------------------------------------ geometry
C = SC.CUE
SHIFT_DONE = C["shift"] + 0.42                   # 20.50
SMALL_DONE = C["ch2"] + 0.36                     # 30.14


def _lbl(b) -> tuple:
    x, y, w, h = b
    return (x, y, x + w, y + h)


def _shift(b, dx):
    return (b[0] + dx, b[1], b[2] + dx, b[3])


DIAL_SMALL_BOX = (SC.DIAL_SMALL_XY[0], SC.DIAL_SMALL_XY[1],
                  SC.DIAL_SMALL_XY[0] + SC.DIAL_W * SC.DIAL_SMALL_K,
                  SC.DIAL_SMALL_XY[1] + SC.DIAL_H * SC.DIAL_SMALL_K)
# scroll-local virtual rectangles (the paper, and the paper after the snip)
PAPER_LOCAL = (SC.PAPER_BOX[0] - SC.SCROLL_X, SC.PAPER_BOX[1] - SC.SCROLL_Y,
               SC.PAPER_BOX[2] - SC.SCROLL_X, SC.PAPER_BOX[3] - SC.SCROLL_Y)
NOTE_LOCAL = (PAPER_LOCAL[0], PAPER_LOCAL[1], PAPER_LOCAL[2], SC.CUT_LOCAL)
SHORT_NOTE_BOX = (SC.PAPER_BOX[0], SC.PAPER_BOX[1], SC.PAPER_BOX[2], SC.CUT_Y)

RECTS: dict[str, tuple] = {
    "mascot-a": SC.MASCOT_A_BOX,
    "bubble": SC.box_of(SC.BUBBLE),
    "key-term": _lbl(SC.KEY_TERM_BOX),
    "note-a": SC.NOTE_BOX,
    "lbl-simple": _lbl(SC.LBL_SIMPLE),
    "scroll-a": SC.SCROLL_BOX,
    "lbl-pages": _lbl(SC.LBL_PAGES),
    "anth-card": SC.ANTH_BOX,
    "dial": SC.DIAL_BOX,
    "lbl-styles": _lbl(SC.LBL_STYLES),
    "mascot-b": SC.MASCOT_B_BOX,
    "lbl-concise": _lbl(SC.LBL_CONCISE),
    "mascot-c": SC.MASCOT_C_BOX,
    "scroll-b": SC.SCROLL_BOX,
    "short-note": SHORT_NOTE_BOX,
    "scissors": SC.box_of(SC.SCISSORS),
    "lbl-short": _lbl(SC.LBL_SHORT),
    "lbl-under": _lbl(SC.LBL_UNDER),
}


def rect_at(name: str, t: float) -> tuple:
    b = RECTS[name]
    if name in ("dial", "lbl-styles") and SHIFT_DONE - 1e-9 <= t < C["ch2"]:
        return _shift(b, SC.SHIFT_DX)
    if name == "dial" and t >= SMALL_DONE - 1e-9:
        return DIAL_SMALL_BOX
    if name == "scroll-b" and t >= C["drop"] + 0.50:
        return (SC.SCROLL_BOX[0], SC.SCROLL_BOX[1], SC.SCROLL_BOX[2], SC.CUT_Y)
    return b


def canvas(box):
    """core px -> the canvas this page actually paints (top 192, k 1.00)."""
    return (CORE_K * box[0] + LEFT, CORE_TOP_SPLIT + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP_SPLIT + CORE_K * box[3])


def lifetime(name: str) -> tuple:
    if name == "short-note":
        return SC.LIFETIMES["scroll-b"]
    return SC.LIFETIMES[name]


def alive(name: str, t: float) -> bool:
    a, b = lifetime(name)
    return a <= t and (b is None or t < b)


# --------------------------------------------------------------- label plan
# LAW 39 / LAW 50: (host, side, printed text, the instant it lands)
LABEL_PLAN = {
    "key-term": ("mascot-a", "below", SC.KEY_TERM, C["keyterm"]),
    "lbl-simple": ("note-a", "above", "SIMPLE", C["simple"]),
    "lbl-pages": ("scroll-a", "above", "2-3 PAGES", C["pages"]),
    "lbl-styles": ("dial", "below", "OUTPUT STYLES", C["styles"]),
    "lbl-concise": ("dial", "above", "CONCISE", SMALL_DONE),
    "lbl-short": ("scroll-b", "above", "SHORT", C["snip"]),
    "lbl-under": ("short-note", "below", "UNDERSTOOD", C["under"]),
}
# typed states: what first appears, on which word (WORD-SYNC).  `spoken` is the
# transcript's own wording of the value the key prints.
PRINTED_KEYS = {
    "key-term": (SC.KEY_TERM, 1, ["no", "longer", "speaks", "english"]),
    "lbl-simple": ("SIMPLE", 37, ["simple"]),
    "lbl-pages": ("2-3 PAGES", 43, ["two", "to", "three", "pages"]),
    "lbl-styles": ("OUTPUT STYLES", 67, ["output", "styles"]),
    "dial-word": ("CONCISE", 93, ["concise"]),
    "lbl-concise": ("CONCISE", 108, ["concise"]),
    "lbl-short": ("SHORT", 121, ["short"]),
    "lbl-under": ("UNDERSTOOD", 128, ["understand"]),
}
PRINTED_AT = {"key-term": C["keyterm"], "lbl-simple": C["simple"],
              "lbl-pages": C["pages"], "lbl-styles": C["styles"],
              "dial-word": C["concise"], "lbl-concise": C["lblconcise"],
              "lbl-short": C["snip"], "lbl-under": C["under"]}
PRINTED_LIFETIME = {"key-term": SC.LIFETIMES["key-term"],
                    "lbl-simple": SC.LIFETIMES["lbl-simple"],
                    "lbl-pages": SC.LIFETIMES["lbl-pages"],
                    "lbl-styles": SC.LIFETIMES["lbl-styles"],
                    "dial-word": (C["concise"], SC.SHEET_UP + SC.SHEET_D),
                    "lbl-concise": SC.LIFETIMES["lbl-concise"],
                    "lbl-short": SC.LIFETIMES["lbl-short"],
                    "lbl-under": SC.LIFETIMES["lbl-under"]}

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.
CUE_WORDS = {
    "mascot": (0, "claude"), "bubble": (1, "no"), "jargon": (3, "speaks"),
    "hookout": (27, "notice"), "note": (31, "ask"), "conn_na": (33, "for"),
    "simple": (37, "simple,"), "conn_ms": (41, "give"), "scroll": (42, "you"),
    "pages": (46, "pages"), "ch1": (52, "now,"), "anth": (53, "anthropic"),
    "dial": (58, "feature"), "conn_ad": (59, "that"), "styles": (67, "output"),
    "anthout": (69, "output"), "shift": (76, "ai"), "conn_dm": (77, "how"),
    "concise": (93, "concise."), "turn": (108, "concise,"),
    "ch2": (109, "now"), "mascot_c": (111, "ai"), "conn_dc": (112, "agent"),
    "conn_cs": (114, "always"), "scroll_b": (115, "reply"),
    "scissors": (119, "a"), "snip": (121, "short"), "scissout": (125, "helping"),
    "under": (128, "understand"), "outro": (132, "now,"),
}
# AUTHORED instants: each inside its own word's 1.0 s LABEL_WINDOW
CUE_INSIDE = {"keyterm": (4, "english,"), "mascot_b": (76, "ai"),
              "lblconcise": (108, "concise,"), "drop": (121, "short")}


# ------------------------------------------------------------------ transcript
def words() -> list[dict]:
    d = json.loads((CUT / "transcript_tight.json").read_text())
    return [w for w in d["words"] if w.get("type") == "word"]


def _norm(t: str) -> str:
    return t.strip().lower().strip('.,!?"')


def clean_tokens(ws: list[dict]) -> tuple[list[dict], dict]:
    """LAW 6 / LAW 46 / LAW 47, all measured on the TIGHT transcript."""
    partial = [w["text"] for w in ws
               if w["text"].strip().endswith(("-", "...", "…"))]
    if partial:
        raise SystemExit(f"unexpected partial words in the take: {partial}")
    opening = "claude no longer speaks english, and"
    head = " ".join(w["text"] for w in ws[:6]).lower()
    if head != opening:
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[6:]).lower()
    if "no longer speaks" in later:
        raise SystemExit("LAW 46: the opening repeats inside the take")
    sign = " ".join(_norm(w["text"]) for w in ws[-6:])
    if sign != "catch you in the next one":
        raise SystemExit(f"the take does not end on the sign-off: {sign!r}")
    tail = DUR - float(ws[-1]["end"])
    cap = 0.20 + 1.0 / FPS
    if tail > 0.30:
        raise SystemExit(f"LAW 47: the master runs {tail:.3f}s past the last word")
    edl = json.loads((CUT / "edl.json").read_text())
    td = edl["take_detection"]
    marker = td["cross_check_marker_rule"]
    gap = td["cross_check_transcript_gap_rule"]
    rep = {"law47_tail_s": round(tail, 3), "law47_cap_s": round(cap, 3),
           "law47_verdict": ("PASS" if tail <= cap else "REPORTED")
           + f" — {tail:.3f}s past the last word against a {cap:.3f}s cap",
           "law46": "the scripted opening occurs ONCE inside the keeper take",
           "take_corroboration": {
               "method": td["method"],
               "raw_word_index": td["take_word_index"],
               "raw_start_s": td["take_start_s"],
               "words": td["take_words"], "of_raw_words": td["raw_words"],
               "openings_found": td.get("openings_found"),
               "marker_rule": marker["verdict"],
               "marker_answer": marker["answer"],
               "markers_before_take": marker["markers_before_take"],
               "gap_rule": gap["verdict"],
               "corroboration": td.get("corroboration")},
           "words": len(ws)}
    return list(ws), rep


def assert_cues(ws: list[dict]) -> dict:
    rep: dict = {}
    for name, (idx, text) in CUE_WORDS.items():
        w = ws[idx]
        if w["text"].strip().lower() != text:
            raise SystemExit(f"cue {name}: word {idx} is {w['text']!r}, not "
                             f"{text!r} — the cut moved")
        got = round(float(w["start"]), 3)
        if abs(got - C[name]) > 0.011:
            raise SystemExit(f"cue {name}: the scene fires at {C[name]}, "
                             f"the word starts at {got}")
        rep[name] = {"word": idx, "text": w["text"], "t": C[name]}
    for name, (idx, text) in CUE_INSIDE.items():
        w = ws[idx]
        if w["text"].strip().lower() != text:
            raise SystemExit(f"cue {name}: word {idx} is {w['text']!r}")
        t = C[name]
        lo, hi = float(w["start"]), float(w["end"]) + LABEL_WINDOW
        if not (lo <= t <= hi):
            raise SystemExit(f"cue {name} at {t} is outside the window of "
                             f"{w['text']!r} ({lo:.3f}-{hi:.3f})")
        rep[name] = {"word": idx, "text": w["text"], "t": t,
                     "window": [round(lo, 3), round(hi, 3)]}
    missing = set(C) - set(rep)
    if missing:
        raise SystemExit(f"cues the build never verified: {sorted(missing)}")
    if SC.BOARD_MODE != "chapters" or len(SC.BOARD_CHAPTERS) != 3:
        raise SystemExit("the scene is no longer the three chapters the plan "
                         "declared")
    if C["under"] + 0.38 >= C["outro"]:
        raise SystemExit("board ink still changing under the outro sheet")
    return rep


def assert_word_sync(ws: list[dict]) -> dict:
    """WORD-SYNC: every typed key first shows the value its words say — the
    key's spoken words are all heard by the time it lands (+ LABEL_WINDOW) and
    the key lands on (or within LABEL_WINDOW after) the word that carries it."""
    rows = []
    for key, (text, idx, spoken) in PRINTED_KEYS.items():
        t = PRINTED_AT[key]
        # the spoken phrase starts at word idx; the key lands between its first
        # word and LABEL_WINDOW after its last
        got = [_norm(x["text"]) for x in ws[idx: idx + len(spoken)]]
        if got != spoken:
            raise SystemExit(f"word-sync: {key} expects {spoken} from word "
                             f"{idx}, the take says {got}")
        w = ws[idx + len(spoken) - 1]
        lo = float(ws[idx]["start"])
        hi = float(w["end"]) + LABEL_WINDOW
        if not (lo - 1e-6 <= t <= hi):
            raise SystemExit(f"word-sync: {key} first shows at {t}, outside "
                             f"{' '.join(spoken)!r} {lo:.3f}-{hi:.3f}")
        rows.append({"state": key, "first_visible_text": text, "at": t,
                     "word": w["text"], "spoken": " ".join(spoken),
                     "word_window": [round(lo, 3), round(hi, 3)]})
    if min(PRINTED_AT.values()) != C["keyterm"]:
        raise SystemExit("LAW 9: NO LONGER ENGLISH is not the first type")
    return {"typed_states": rows, "disagreements": 0, "digits_that_tick": 0,
            "note": "2-3 PAGES lands on 'pages' after 'two to three' is heard; "
                    "UNDERSTOOD prints the past participle of 'understand'."}


def assert_law37(ws: list[dict]) -> dict:
    cues = PCUE.scan(ws)
    plan = json.loads(PLAN.read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / "prep/stages/claudeconcise.cues.json").read_text())
    if marker["keys"]["cue_count"] != len(cues):
        raise SystemExit("LAW 37: the prep marker disagrees with the re-run")
    if cues or declared:
        raise SystemExit("LAW 37: this scene builds no source card")
    return {"scan_cue_count": 0, "plan_declared_cards": 0,
            "prep_marker_cue_count": 0, "source_cards_in_the_page": 0}


# ------------------------------------------------------------------ laws
GUTTER_REFUSE = 16.0
HELD = [2.6, 5.0, 8.5, 10.0, 12.95, 14.5, 16.5, 19.0, 21.2, 24.0, 27.0,
        29.70, 30.9, 32.55, 33.0, 34.4, 36.6, 37.5]


def assert_label_law() -> dict:
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    out: dict = {}
    for key, (host, side, text, t0) in LABEL_PLAN.items():
        checked = []
        for tt in [t0 + 0.30] + HELD:
            if tt < t0 or not alive(key, tt) or not alive(host, tt):
                continue
            if host == "dial" and SMALL_DONE > tt >= C["ch2"]:
                continue                          # the dial is in transit
            kb, hb = rect_at(key, tt), rect_at(host, tt)
            if side == "below" and kb[1] < hb[3] - 0.01:
                raise SystemExit(f"LAW 39: {key} is not entirely below {host} "
                                 f"at {tt}")
            if side == "above" and kb[3] > hb[1] + 0.01:
                raise SystemExit(f"LAW 39: {key} is not entirely above {host} "
                                 f"at {tt}")
            kc, hc = (kb[0] + kb[2]) / 2, (hb[0] + hb[2]) / 2
            if abs(kc - hc) > 0.15 * (hb[2] - hb[0]) + 0.01:
                raise SystemExit(f"LAW 39: {key} is off {host}'s axis at {tt}")
            checked.append(round(tt, 2))
        if not checked:
            raise SystemExit(f"LAW 39: {key} was never checked")
        blk_host = "scroll-b" if host == "short-note" else host
        if not any({key, blk_host} <= b for b in blocks):
            raise SystemExit(f"LAW 41: {key} is not blocked with {blk_host}")
        out[key] = {"host": host, "side": side, "text": text, "at": t0,
                    "checked_at": checked,
                    "box_canvas": [round(v, 1) for v in canvas(RECTS[key])]}
    du = SC.KEY_TERM_FS * CORE_K / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} du")
    out["_key_term"] = {"text": SC.KEY_TERM, "font_px": SC.KEY_TERM_FS,
                        "design_units": round(du, 2), "first_type": True}
    return out


def assert_lifetime_law() -> dict:
    for n, (a, b) in SC.LIFETIMES.items():
        if b is None:
            if n not in SC.SCENE_ANCHORS and not n.startswith("emph-"):
                raise SystemExit(f"LAW 42: {n} never leaves and is not an anchor")
            continue
        if (b - a) / DUR > 0.40:
            raise SystemExit(f"LAW 42: {n} overstays the 40 % line")
    return {"board_mode": SC.BOARD_MODE, "chapters": len(SC.BOARD_CHAPTERS),
            "anchors": list(SC.SCENE_ANCHORS),
            "longest_finite_share": round(max(
                (b - a) / DUR for a, b in SC.LIFETIMES.values()
                if b is not None), 3)}


def assert_spacing_law() -> dict:
    """LAW 41 on the co-alive seats in CORE px (the page itself is judged by
    geometry_audit --strict)."""
    plan = json.loads(PLAN.read_text())
    blocks = ([set(b) for b in SC.DECLARED_BLOCKS]
              + [set(b) for b in plan["blocks"]]
              + [{"short-note", n} for n in ("scroll-b", "scissors", "lbl-short",
                                             "lbl-under")])
    worst = (1e9, None)
    for t in HELD:
        live = [n for n in RECTS if alive(n, t)]
        for i in range(len(live)):
            for j in range(i + 1, len(live)):
                a, b = live[i], live[j]
                if any({a, b} <= s for s in blocks):
                    continue
                ax0, ay0, ax1, ay1 = rect_at(a, t)
                bx0, by0, bx1, by1 = rect_at(b, t)
                dx = max(bx0 - ax1, ax0 - bx1, 0.0)
                dy = max(by0 - ay1, ay0 - by1, 0.0)
                g = (dx * dx + dy * dy) ** 0.5
                if dx <= 0 and dy <= 0:
                    raise SystemExit(f"LAW 41: {a} and {b} overlap at t={t}")
                if g < worst[0]:
                    worst = (g, (a, b, t))
    if worst[0] < GUTTER_REFUSE:
        raise SystemExit(f"LAW 41: {worst[1]} is {worst[0]:.2f}px apart")
    return {"tightest_core_px": round(worst[0], 2),
            "tightest_pair": list(worst[1]), "refusal_line": GUTTER_REFUSE,
            "blocks": [list(b) for b in SC.DECLARED_BLOCKS]}


# ------------------------------------------------------ LAW 40: connectors
# (target id, target box in core px at the check instant, check instant). The
# check instant is a HELD frame: the draw has completed and both ends are alive.
CONNECTORS = {
    "conn-na": ("mascot-a", SC.MASCOT_A_BOX, 8.50),
    "conn-ms": ("scroll-a-paper", SC.PAPER_BOX, 12.95),
    "conn-ad": ("dial", SC.DIAL_BOX, 16.50),
    "conn-dm": ("mascot-b", SC.MASCOT_B_BOX, 24.00),
    "conn-dc": ("mascot-c", SC.MASCOT_C_BOX, 31.00),
    "conn-cs": ("scroll-b-note", SHORT_NOTE_BOX, 32.55),
}
PLANNED = {"conn-na": SC.A_NA, "conn-ms": SC.A_MS, "conn-ad": SC.A_AD,
           "conn-dm": SC.A_DM, "conn-dc": SC.A_DC, "conn-cs": SC.A_CS}
TARGET_LIFE = {"scroll-a-paper": "scroll-a", "scroll-b-note": "scroll-b"}


def _tip(html: str, cid: str) -> tuple[float, float]:
    m = re.search(rf'id="{cid}" style="left:([\d.-]+)px;top:([\d.-]+)px.*?'
                  r'<path class="cn" d="M([\d.-]+) ([\d.-]+) L([\d.-]+) ([\d.-]+)"',
                  html, re.S)
    if not m:
        raise SystemExit(f"{cid}: cannot read its shaft")
    x0, y0, _a, _b, tx, ty = map(float, m.groups())
    return (x0 + tx, y0 + ty)


def assert_anchor_law(html: str) -> dict:
    """Each end re-derived from the emitted path and the TARGET's own rect.
    The declared anchor is the point on the target's edge where the painted
    shaft lands; production refuses a miss over 4 px."""
    out = {}
    for cid, (tgt, box, check_at) in CONNECTORS.items():
        tip = _tip(html, cid)
        x0, y0, x1, y1 = box
        d = {"left": abs(tip[0] - x0), "right": abs(tip[0] - x1),
             "top": abs(tip[1] - y0), "bottom": abs(tip[1] - y1)}
        side = min(d, key=d.get)
        if side in ("left", "right"):
            ex = x0 if side == "left" else x1
            frac = round((min(max(tip[1], y0), y1) - y0) / (y1 - y0), 12)
            anchor = (ex, y0 + frac * (y1 - y0))
        else:
            ey = y0 if side == "top" else y1
            frac = round((min(max(tip[0], x0), x1) - x0) / (x1 - x0), 12)
            anchor = (x0 + frac * (x1 - x0), ey)
        miss = math.hypot(tip[0] - anchor[0], tip[1] - anchor[1])
        if miss > 4.0 + 1e-6:
            raise SystemExit(f"{cid}: its painted tip misses the {side} edge of "
                             f"{tgt} by {miss:.2f}px")
        planned = PLANNED[cid][1]
        drift = math.hypot(anchor[0] - planned[0], anchor[1] - planned[1])
        if drift > 4.0:
            raise SystemExit(f"{cid}: lands {drift:.2f}px from the planned end")
        a, b = SC.LIFETIMES[cid]
        if not (a + 0.30 <= check_at < (b or DUR)):
            raise SystemExit(f"{cid}: check-at {check_at} is not held")
        if not alive(TARGET_LIFE.get(tgt, tgt), check_at):
            raise SystemExit(f"{cid}: its target is gone at {check_at}")
        out[cid] = {"target": tgt, "side": side, "fraction": frac,
                    "check_at": check_at, "tip_core": [round(v, 2) for v in tip],
                    "anchor_core": [round(v, 2) for v in anchor],
                    "miss_px": round(miss, 2),
                    "from_planned_end_px": round(drift, 2)}
    return out


# ------------------------------------------------------ LAW 38: emphasis
EMPH = {
    "ridge": {"id": "dial-ridge", "kind": "fill", "target": "dial-knob",
              "check_at": 29.70,
              "window": (C["turn"] + 0.30 + 0.38, C["ch2"])},
    "edge": {"id": "scroll-b-edge", "kind": "border", "target": "scroll-b-note",
             "check_at": 37.00,
             "window": (C["under"] + 0.38, C["outro"])},
}


def assert_emphasis_law() -> dict:
    for name, e in EMPH.items():
        a, b = e["window"]
        if not (a <= e["check_at"] < b):
            raise SystemExit(f"LAW 38: the {name} flip is not complete and held "
                             f"at {e['check_at']}")
    return {"flips": [{"on": e["id"], "kind": e["kind"], "target": e["target"],
                       "check_at": e["check_at"], "held": list(e["window"])}
                      for e in EMPH.values()],
            "rings_ellipses_circles": 0, "highlights": 0,
            "dom_elements_added": 0}


def _insert_virtual(s: str, holder: str, vid: str, box) -> str:
    x0, y0, x1, y1 = box
    i = s.index(f'id="{holder}"')
    j = s.index("</svg></div>", i) + len("</svg>")
    return (s[:j] + f'<div id="{vid}" class="abs" style="left:{x0:.0f}px;'
            f'top:{y0:.0f}px;width:{x1 - x0:.0f}px;height:{y1 - y0:.0f}px" '
            f'data-virtual-rect></div>' + s[j:])


def declare_contracts(html: str, anchors: dict) -> tuple[str, dict]:
    s = html
    # the ridge: ONE rect in the page
    old = '<rect class="ridge"'
    if s.count(old) != 1:
        raise SystemExit("the module no longer emits ONE dial ridge")
    e = EMPH["ridge"]
    s = s.replace(old, f'<rect id="{e["id"]}" class="ridge" '
                       f'data-emphasis="{e["kind"]}" '
                       f'data-emphasis-target="{e["target"]}" '
                       f'data-check-at="{e["check_at"]:.2f}"', 1)
    # the short note's paper edge: the first `.frm` INSIDE #scroll-b
    e = EMPH["edge"]
    i = s.index('id="scroll-b"')
    j = s.index('<path class="frm"', i)
    new = (f'<path id="{e["id"]}" class="frm" data-emphasis="{e["kind"]}" '
           f'data-emphasis-target="{e["target"]}" '
           f'data-check-at="{e["check_at"]:.2f}"')
    s = s[:j] + new + s[j + len('<path class="frm"'):]
    # connectors
    for cid, a in anchors.items():
        key = f'id="{cid}"'
        if s.count(key) != 1:
            raise SystemExit(f"cannot stamp {cid}")
        s = s.replace(key, f'{key} data-anchor-side="{a["side"]}" '
                           f'data-anchor-fraction="{a["fraction"]!r}" '
                           f'data-check-at="{a["check_at"]:.2f}"', 1)
    # the virtual rectangles, inside their holders so they move with them
    s = _insert_virtual(s, "scroll-a", "scroll-a-paper", PAPER_LOCAL)
    s = _insert_virtual(s, "scroll-b", "scroll-b-note", NOTE_LOCAL)
    s = _insert_virtual(s, "dial", "dial-knob", SC.KNOB_LOCAL)
    retarget = {}
    for cid, (old_t, new_t) in {"conn-ms": ("scroll-a", "scroll-a-paper"),
                                "conn-cs": ("scroll-b", "scroll-b-note")}.items():
        i = s.index(f'id="{cid}"')
        k = s.index(f'data-connect-to="{old_t}"', i)
        s = (s[:k] + f'data-connect-to="{new_t}"'
             + s[k + len(f'data-connect-to="{old_t}"'):])
        retarget[cid] = f"{old_t} -> {new_t}"
    return s, {"connectors_stamped": len(anchors), "emphases_stamped": 2,
               "retargeted": retarget,
               "virtual_rects": ["scroll-a-paper", "scroll-b-note", "dial-knob"]}


def assert_cast_law() -> dict:
    rep = DF.assert_cast_resolves(list(STAGE_FILES), dict(STAGE_FILES),
                                  LOGOS, label="claudeconcise stage marks")
    return {"stage_marks": sorted(STAGE_FILES),
            "resolved": {k: v["path"] for k, v in rep.items()},
            "mark_side_core_px": SC.MARK_SIDE,
            "cutout_lanes_not_ours": list(CUTOUT_LANES)}


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
    norm = text.strip().upper().rstrip('.,!?"').strip()
    for key, (t, _i, _s) in PRINTED_KEYS.items():
        if norm == t.upper():
            return key
    return None


SOLO_WORD_PENALTY = 250_000.0


def _repartition(union, max_w, measurer, forbidden):
    n = len(union)
    texts = {(i, j): _joined(union[i:j]) for i in range(n)
             for j in range(i + 1, n + 1)}
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
            if w > max_w or txt.strip().lower() in forbidden:
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


def repair_orphan_beats(parts, max_w, measurer, forbidden):
    log, i, guard = [], 0, 0
    while i < len(parts):
        guard += 1
        if guard > 5000:
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
            got = _repartition([w for p in parts[lo:hi] for w in p], max_w,
                               measurer, forbidden)
            if got is not None:
                fixed = (lo, hi, got)
                break
        if fixed is None:
            raise SystemExit(f"SS3b: the orphan beat {txt!r} has no repartition")
        lo, hi, got = fixed
        log.append({"orphan": txt, "repartitioned_to": [_joined(p) for p in got]})
        parts[lo:hi] = got
        i = lo
    return parts, log


def merge_solo_word_beats(parts, max_w, measurer):
    log, i = [], 0
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
            if _is_board_key(txt) is not None:
                continue
            best = (direction, lo, hi, u)
            break
        if best is None:
            i += 1
            continue
        direction, lo, hi, u = best
        log.append({"solo": _joined(parts[i]), "direction": direction,
                    "merged_to": _joined(u)})
        parts[lo:hi] = [u]
        i = max(0, lo)
    return parts, log


def caption_beats(measurer, ws, rep) -> tuple[list[dict], dict]:
    measurer.want(CAP.runs([w["text"] for w in ws]))
    measurer.resolve()
    forbidden = {t.lower() + suf for (t, _i, _s) in PRINTED_KEYS.values()
                 for suf in ("", ".", ",", "!", "?")}
    parts: list[list] = []
    for group in phrases(ws):
        got = _repartition(group, CAP.SEAT_MAX_W, measurer, forbidden)
        if got is None:
            got = CAP.split_balanced(group, CAP.SEAT_MAX_W, measurer,
                                     forbidden=forbidden)
        parts.extend(got)
    before = len(parts)
    # SS3b over the WHOLE beat stream
    parts = CAP.merge_function_only_beats(parts, CAP.SEAT_MAX_W, measurer)
    merged = before - len(parts)
    parts, orphan_log = repair_orphan_beats(parts, CAP.SEAT_MAX_W, measurer,
                                            forbidden)
    parts, solo_log = merge_solo_word_beats(parts, CAP.SEAT_MAX_W, measurer)
    beats: list[dict] = []
    for part in parts:
        text = _joined(part)
        measurer.want([text])
        measurer.resolve()
        beats.append({"text": text, "start": float(part[0]["start"]),
                      "end": float(part[-1]["end"]), "w": measurer.width(text)})
    for i, b in enumerate(beats):
        nxt = beats[i + 1]["start"] if i + 1 < len(beats) else b["end"] + 0.26
        b["dur"] = round(max(0.24, min(nxt, DUR) - b["start"]), 3)
    CAP.assert_no_function_only_beat(beats)
    widest = max(b["w"] for b in beats)
    if widest > CAP.SEAT_MAX_W + 0.6:
        raise SystemExit(f"pill {widest:.1f}px exceeds the seat")
    for b in beats:
        key = _is_board_key(b["text"])
        if key is not None:
            k0, k1 = PRINTED_LIFETIME[key]
            if b["start"] < (k1 or DUR) and k0 < b["start"] + b["dur"]:
                raise SystemExit(f"LAW 4: the pill {b['text']!r} echoes the "
                                 f"live board key {key}")
    rep["function_word_merges"] = merged
    rep["beats_before_merge"] = before
    rep["orphan_repartitions"] = orphan_log
    rep["solo_word_merges"] = solo_log
    rep["board_keys_forbidden_at_split"] = sorted(forbidden)
    return beats, rep


def caption_html(beats, seat_y) -> str:
    """FRAME-QUANTISED, half-open, ONE OWNER PER FRAME."""
    ks = [round(b["start"] * FPS) for b in beats]
    last_k = round(min(beats[-1]["start"] + beats[-1]["dur"], DUR) * FPS)
    out = []
    for i, b in enumerate(beats):
        k0 = ks[i]
        k1 = ks[i + 1] if i + 1 < len(beats) else last_k
        if k1 <= k0 + 1:
            raise SystemExit(f"caption beat {i} ({b['text']!r}) is under two "
                             "frames long")
        out.append(
            f'<div id="cap{i}" class="clip scap" style="top:{seat_y}px" '
            f'data-start="{k0 / FPS:.3f}" '
            f'data-duration="{(k1 - k0 - 0.5) / FPS:.4f}" '
            f'data-track-index="25"><span class="scappill">'
            f'{ihtml.escape(b["text"], quote=False)}</span></div>')
    return "\n".join(out)


# ------------------------------------------------------------------ page shell
def head(title: str, extra_css: str) -> str:
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
  font-family:Poppins,sans-serif; zoom:1; }}
.clip {{ position:absolute; }} .abs {{ position:absolute; }}
.mono {{ font-family:'JetBrains Mono',monospace; text-transform:uppercase; }}
.core {{ transform-origin:0 0; }}
{CAP.pill_rule()}
{extra_css}
</style></head>
<body><div id="root" data-composition-id="main" data-start="0"
 data-width="1080" data-height="1920" data-duration="{DUR}" data-fps="{FPS}">
"""


def tail(tweens: list[str]) -> str:
    return f"""
</div>
<script>
window.__timelines = window.__timelines || {{}};
const SOFT = "power3.out";
const SWING = "power2.inOut";
const POP = "back.out(2.05)";
const tl = gsap.timeline({{paused:true}});
{chr(10).join(tweens)}
window.__timelines["main"]=tl;
</script></body></html>
"""


def outro_lockup(handle_key: str) -> str:
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
    bed = LIB_MUSIC / "bed_split_v2.mp3"
    if not bed.exists():
        raise SystemExit(f"the split bed does not resolve: {bed}")
    shutil.copy2(bed, dst / "assets/music/bed.mp3")
    rec["bed"] = str(bed)
    rec["sfx_sources"] = {}
    for s in ("whoosh", "pop", "click"):
        src = LIB_SFX / f"{s}.mp3"
        if not src.exists():
            raise SystemExit(f"the {s} sfx does not resolve: {src}")
        shutil.copy2(src, dst / f"assets/sfx/{s}.mp3")
        rec["sfx_sources"][s] = str(src)
    shutil.copy2(CUT / face, v / face)
    rec["face"] = {"file": face, **probe_wh(CUT / face)}
    marks = {}
    for key, rel in STAGE_FILES.items():
        src = LOGOS / rel
        if not src.exists():
            raise SystemExit(f"registry key {key!r} does not resolve: {src}")
        shutil.copy2(src, dst / "assets/logos" / src.name)
        if key == "claude-code":
            CC.MARK_INK[key] = CC.measure_mark(key, src)
        marks[key] = {"source": str(src), "url": LOGO_URL[key]}
    rec["marks"] = marks
    return rec


def media() -> dict:
    """The TWO rasters the scene paints (handoff section 1)."""
    w, h = SC.ANTH_MARK
    return {
        "_claudecode_img": CC.mark_img(LOGO_URL["claude-code"], "claude-code",
                                       SC.MARK_SIDE),
        "_anthropic_img": (
            f'<img id="mark-anthropic" src="{LOGO_URL["anthropic-wordmark"]}" '
            f'alt="" style="position:absolute;left:50%;top:50%;width:{w:.0f}px;'
            f'height:{h:.1f}px;transform:translate(-50%,-50%);display:block"/>'),
    }


def sfx_plan() -> list[tuple]:
    """EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22)."""
    return [("pop", C["mascot"], SFX_STRUCTURE),     # Claude Code lands
            ("click", C["jargon"], SFX_DETAIL),      # the gibberish scribbles in
            ("click", C["keyterm"], SFX_DETAIL),     # NO LONGER ENGLISH
            ("pop", C["note"], SFX_STRUCTURE),       # the simple note
            ("click", C["simple"], SFX_DETAIL),      # SIMPLE
            ("click", C["conn_ms"], SFX_DETAIL),     # arrow out to the scroll
            ("click", C["pages"], SFX_DETAIL),       # 2-3 PAGES
            ("pop", C["anth"], SFX_STRUCTURE),       # the ANTHROPIC card
            ("pop", C["dial"], SFX_STRUCTURE),       # the dial
            ("click", C["styles"], SFX_DETAIL),      # OUTPUT STYLES
            ("whoosh", C["shift"], SFX_STRUCTURE),   # dial slides left
            ("click", C["conn_dm"], SFX_DETAIL),     # arrow dial -> Claude Code
            ("click", C["concise"], SFX_DETAIL),     # CONCISE on the dial
            ("whoosh", C["turn"], SFX_STRUCTURE),    # the knob turns
            ("whoosh", C["ch2"], SFX_STRUCTURE),     # the chapter changes
            ("pop", C["mascot_c"], SFX_DETAIL),      # Claude Code, centre
            ("click", C["conn_dc"], SFX_DETAIL),     # arrow dial -> Claude Code
            ("click", C["conn_cs"], SFX_DETAIL),     # arrow out to the scroll
            ("pop", C["scissors"], SFX_DETAIL),      # scissors arrive
            ("click", C["snip"], SFX_STRUCTURE),     # the snip, SHORT
            ("click", C["under"], SFX_DETAIL),       # UNDERSTOOD
            ("whoosh", C["outro"], SFX_STRUCTURE)]   # the rising sheet


def assert_sfx(sfx) -> dict:
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30:
        raise SystemExit(f"SFX flam: {worst}")
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "deliberately_silent": {
                "bubble 0.34": "0.22 s after the tile pop",
                "conn_na 7.72": "one pop scores the note and its arrow",
                "scroll 10.04": "0.20 s after the arrow click",
                "conn_ad 15.20": "0.30 s after the dial pop",
                "mascot_b 20.16": "0.08 s after the shift whoosh",
                "scroll_b 31.48": "0.28 s after the arrow click",
                "fades/exits": "a fade-out is not an arrival"}}


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
def guard_core_band(top: float, k: float, cap_seat: float,
                    pill_clear: float = 24.0) -> dict:
    y0 = top + SC.CONTENT_Y0 * k
    y1 = top + SC.CONTENT_Y1 * k
    pill_top = cap_seat - CAP.CAP_PILL_HEIGHT / 2
    if y0 < 0.10 * H:
        raise SystemExit(f"core content starts at y={y0:.1f} — LAW 30")
    if y1 > pill_top - pill_clear:
        raise SystemExit(f"core content ends at y={y1:.1f}, within {pill_clear}"
                         f"px of the pill top {pill_top:.1f}")
    return {"content_top": y0, "content_bottom": y1,
            "pill_top_rendered": round(pill_top, 3),
            "clear_above_pill": round(pill_top - y1, 2),
            "clear_below_law30": round(y0 - 0.10 * H, 2)}


def guard_rail() -> dict:
    """LAW 30: readable annotations never past x 918 BETWEEN y 30 % and 95 %
    (the round-4 amendment: the composition itself stays centred).  Every key
    in this scene sits above y 30 %, so the rail band holds no readable type."""
    band_lo, band_hi = 0.30 * H, 0.95 * H
    rows, in_band = {}, []
    for n in LABEL_PLAN:
        b = canvas(RECTS[n])
        rows[n] = {"y": [round(b[1], 1), round(b[3], 1)],
                   "in_rail_band": b[3] > band_lo and b[1] < band_hi}
        if rows[n]["in_rail_band"]:
            in_band.append(n)
    for n in in_band:
        _h, _s, text, _t = LABEL_PLAN[n]
        fs, ls = ((SC.KEY_TERM_FS, SC.KEY_TERM_LS) if n == "key-term"
                  else (SC.KEY_FS, SC.KEY_LS))
        ink = len(text) * 0.6 * fs + (len(text) - 1) * ls
        cx = (canvas(RECTS[n])[0] + canvas(RECTS[n])[2]) / 2
        if cx + ink / 2 > CAP.LAW12_RAIL_X + 0.01:
            raise SystemExit(f"LAW 30: {n} ink reaches the right rail")
    return {"rail_band_y": [band_lo, band_hi], "keys": rows,
            "keys_in_rail_band": in_band, "law30_rail_x": CAP.LAW12_RAIL_X}


def phone_objects() -> list[dict]:
    out = []
    for o in SC.BESPOKE:
        x0, y0, x1, y1 = canvas(o["core"])
        out.append({"name": o["name"], "t": o["t"],
                    "bbox": [round(x0 / W, 4), round(y0 / H, 4),
                             round(x1 / W, 4), round(y1 / H, 4)],
                    "canvas": [x0, y0, x1, y1]})
    return out


# ------------------------------------------------------------------ build
def build_split(out: Path, handle: str) -> dict:
    staged = stage(out, face="face_bottom_hd.mp4")
    if (staged["face"]["w"], staged["face"]["h"]) != (1080, 1058):
        raise SystemExit(f"the face plate is {staged['face']}")
    ws, clean_rep = clean_tokens(words())
    rep = {"cues": assert_cues(ws), "word_sync": assert_word_sync(ws),
           "law37": assert_law37(ws), "law39": assert_label_law(),
           "law42": assert_lifetime_law(), "law41": assert_spacing_law(),
           "law38": assert_emphasis_law(), "law2": assert_cast_law()}
    SFX = sfx_plan()
    rep["law22"] = assert_sfx(SFX)

    scene_html, tweens = SC.build(media(), outro_lockup(handle))
    rep["law40"] = assert_anchor_law(scene_html)
    scene_html, rep["declared"] = declare_contracts(scene_html, rep["law40"])
    if scene_html.count("data-connect-to") != 6:
        raise SystemExit("the scene does not carry six connectors")
    if (scene_html.count("data-connect-to") + scene_html.count("data-emphasis=")
            != scene_html.count("data-check-at")):
        raise SystemExit("a connector or emphasis is missing its check instant")
    for shape in ("<circle", "<ellipse"):
        if shape in scene_html:
            raise SystemExit(f"LAW 38 rule 3: {shape} in the emitted scene")
    if 'id="mark-anthropic"' not in scene_html:
        raise SystemExit("the ANTHROPIC wordmark lost its block id")
    if not any("SWING" in t for t in tweens):
        raise SystemExit("the scene no longer uses SWING")

    m = CAP.PillMeasurer(RUN / "gen/_pillwidths_claudeconcise.json")
    beats, cap_rep = caption_beats(m, ws, clean_rep)
    CAP.assert_law12(SEAM, max(b["w"] for b in beats))
    rep["band"] = guard_core_band(CORE_TOP_SPLIT, CORE_K, SEAM)
    rep["rail"] = guard_rail()
    objs = phone_objects()

    body = [
        f'<video id="facebot" src="assets/v/face_bottom_hd.mp4" data-start="0" '
        f'data-duration="{DUR}" data-media-start="0" data-track-index="1" muted '
        f'playsinline style="position:absolute;top:{SEAM}px;left:0;width:{int(W)}px;'
        f'height:{H - SEAM}px;object-fit:cover"></video>',
        f'<section id="tz" class="clip tz" data-start="0" data-duration="{DUR}" '
        f'data-track-index="2">',
        f'<div class="abs core" id="core" style="left:{LEFT}px;top:{CORE_TOP_SPLIT}px;'
        f'width:{SC.CORE_W:.0f}px;height:{SC.CORE_H:.0f}px;transform:scale({CORE_K})">',
        scene_html, "</div></section>",
        caption_html(beats, SEAM),
        audio_html(SFX),
    ]
    css = (f".tz {{ left:0; top:0; width:{int(W)}px; height:{SEAM}px; "
           f"overflow:hidden; background:{SC.CREAM}; }}")
    (out / "index.html").write_text(head(TITLE, css) + "\n".join(body)
                                    + tail(tweens), encoding="utf-8")
    rep.update({"staged": staged, "seat": SEAM, "scale": CORE_K,
                "core": {"left": LEFT, "top": CORE_TOP_SPLIT},
                "phone_objects": objs, "transcript": cap_rep,
                "captions": {"n": len(beats),
                             "widest_px": round(max(b["w"] for b in beats), 1),
                             "texts": [b["text"] for b in beats],
                             "starts": [b["start"] for b in beats]},
                "render": {"w": 1080, "h": 1920, "zoom": 1}})
    return rep


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="split", choices=("split",))
    ap.parse_args()
    dst = RUN / "projects/claudeconcise_split"
    dst.mkdir(parents=True, exist_ok=True)
    rep = build_split(dst, "yt")
    rep["handle"] = CAP.handle("yt")
    (RUN / "gen/_build_claudeconcise_split.json").write_text(
        json.dumps({"video": VID, "lane": "diagram build", "fps": FPS,
                    "duration": DUR, "seam": SEAM, "formats": {"split": rep}},
                   indent=1, default=str))
    print(f"split: {dst}")
    print(json.dumps({"captions": rep["captions"], "band": rep["band"],
                      "law41": rep["law41"]["tightest_pair"],
                      "law40": {k: [v["side"], v["fraction"], v["miss_px"]]
                                for k, v in rep["law40"].items()},
                      "law22": rep["law22"]["tightest_gap_s"],
                      "phone": rep["phone_objects"]}, indent=1, default=str))


if __name__ == "__main__":
    main()
