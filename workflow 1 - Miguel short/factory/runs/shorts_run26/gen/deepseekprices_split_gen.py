#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION — deepseekprices / COUNTER + METER.

    YouTube   classic split 50/50   projects/deepseekprices_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/deepseekprices_scene.py`
plus `plans/deepseekprices_scene_handoff.md` are the design agent's artefacts,
sealed by `review/artwork_pass_deepseekprices.json` (production v4,
`production.py seal`).  This file IMPORTS the module and SEATS it at the
handoff's own placement (k = 1.00, left 0, core top 192).  It never mutates a
byte of the module; the two border-flip emphases are DECLARED on the emitted
string (data-emphasis / target / check-at), exactly as the siblings do.

HD DELIVERY: authored AND encoded 1080x1920.  The face plate is
`face_bottom_hd.mp4` (1080x1058), so the seam is 1920 - 1057.5 = 862.5 and the
RENDERING pill top is 862.5 - 114.59/2 = 805.205 (the pill that renders, never
the frozen 108.2 seat constant).  The core's content band 86..568 lands at
canvas 278..760: 86 px under LAW 30's top-10 % line and 45.2 px over the pill.

TAKEOVER and FACESPLIT are not daily deliverables and this file cannot build one.
"""
from __future__ import annotations

import argparse
import html as ihtml
import json
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
import deepseekprices_scene as SC               # noqa: E402

RUN = Path(__file__).resolve().parents[1]
CUT = RUN / "cuts/deepseekprices"
PLAN = RUN / "plans/deepseekprices_plan.json"
ASSETS = Path.home() / "Documents/Workspace/assets"
LOGOS = ASSETS / "logos"
LIB_MUSIC = ASSETS / "audio/music/shorts-factory"
LIB_SFX = ASSETS / "audio/sfx/shorts-factory"

VID = "deepseekprices"
W, H = 1080.0, 1920.0
FPS = 25
DUR = SC.DUR                                     # 33.58, the cut master

SEAM = 862.5
CORE_TOP_SPLIT = SC.CANVAS_OFFSET                # 192.0, the handoff's number
CORE_K = 1.00
LEFT = (W - SC.CORE_W * CORE_K) / 2              # 0.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "DeepSeek raises prices and stays cheap"
LABEL_WINDOW = 1.0

# ------------------------------------------------------------------ marks
# MARK IDENTITY: the FILE is named, never "the logo" (handoff section 1).
STAGE_FILES = {k: f"logos/{v}" for k, v in SC.LOGO_FILES.items()}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}
CUTOUT_LANES = SC.CUTOUT_LOGO_LANES

# ------------------------------------------------------------------ geometry
C = SC.CUE
SLIDE_DONE = C["slide"] + 0.44                   # the tag's one displacement
BEST_DONE = C["best"] + 0.50                     # the DeepSeek column slides home
FOUR_DONE = C["four"] + 0.34                     # the counter has ridden up


def _lbl(b) -> tuple:
    x, y, w, h = b
    return (x, y, x + w, y + h)


def _col(cx: float) -> tuple:
    return (cx - SC.TILE / 2, SC.COL_TOP, cx + SC.TILE / 2,
            SC.TILE_TOP + SC.TILE)


def _shift(b, dx):
    return (b[0] + dx, b[1], b[2] + dx, b[3])


GX, GY, GW, GH = SC.GAUGE
CX = SC.COL_CX
RECTS: dict[str, tuple] = {
    "price-tag": (SC.TAG_LEFT, SC.TAG_TOP, SC.TAG_LEFT + SC.TAG_W,
                  SC.TAG_TOP + SC.TAG_H),
    "demand-gauge": (GX, GY, GX + GW, GY + GH),
    "key-term-v4flash": _lbl(SC.KEY_TERM_BOX),
    "price-chart": (SC.CHART_X0 - 8, SC.BASELINE_Y - 8, SC.CHART_X1 + 8,
                    SC.BASELINE_Y + 8),
    "col-deepseek": _col(CX["deepseek"]),
    "col-claude": _col(CX["claude"]),
    "col-openai": _col(CX["openai"]),
    "col-gemini": _col(CX["gemini"]),
    "label-price-per-token": _lbl(SC.PPT_BOX),
    "computer-badge": (SC.PC_LEFT, SC.PC_TOP, SC.PC_LEFT + SC.PC_W,
                       SC.PC_TOP + SC.PC_H),
    "label-ai-employee": _lbl(SC.EMP_BOX),
}


def _bar_h(t: float) -> float:
    if t < C["two"]:
        return SC.DS_UNIT
    if t < C["four"]:
        return 2 * SC.DS_UNIT
    return 4 * SC.DS_UNIT


def rect_at(name: str, t: float) -> tuple:
    """The seat at a HELD instant (never mid-tween)."""
    if name == "bar-deepseek":
        h = _bar_h(t)
        cx = CX["deepseek"]
        b = (cx - SC.BAR_W / 2, SC.BASELINE_Y - h, cx + SC.BAR_W / 2,
             SC.BASELINE_Y)
        return _shift(b, SC.DS_ALONE_DX) if t < BEST_DONE else b
    if name == "counter-ds":
        cx = CX["deepseek"]
        top = SC.BASELINE_Y - 2 * SC.DS_UNIT - SC.COUNTER_GAP - SC.COUNTER_H
        if t >= FOUR_DONE:
            top -= 2 * SC.DS_UNIT
        b = (cx - SC.COUNTER_W / 2, top, cx + SC.COUNTER_W / 2,
             top + SC.COUNTER_H)
        return _shift(b, SC.DS_ALONE_DX) if t < BEST_DONE else b
    b = RECTS[name]
    if name == "price-tag" and t < SLIDE_DONE:
        return _shift(b, SC.TAG_ALONE_DX)
    if name == "col-deepseek" and t < BEST_DONE:
        return _shift(b, SC.DS_ALONE_DX)
    return b


def canvas(box):
    """core px -> the canvas this page actually paints (top 192, k 1.00)."""
    return (CORE_K * box[0] + LEFT, CORE_TOP_SPLIT + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP_SPLIT + CORE_K * box[3])


LIFE_OF = {"bar-deepseek": "col-deepseek"}


def alive(name: str, t: float) -> bool:
    a, b = SC.LIFETIMES[LIFE_OF.get(name, name)]
    return a <= t and (b is None or t < b)


# --------------------------------------------------------------- label plan
# LAW 39 / LAW 50: every NAME below what it names; the counter rides ABOVE its
# bar (the plan's one "above", a value on a bar top, LAW 28).
LABEL_PLAN = {"key-term-v4flash": ("price-tag", "below", SC.KEY_TERM),
              "counter-ds": ("bar-deepseek", "above", "2X / 4X"),
              "label-price-per-token": ("price-chart", "below",
                                        "PRICE PER TOKEN"),
              "label-ai-employee": ("computer-badge", "below", "AI EMPLOYEE")}
LABEL_AT = {"key-term-v4flash": C["keyterm"],
            "counter-ds": C["two"] + 0.06,
            "label-price-per-token": C["ppt"],
            "label-ai-employee": C["employee"]}
SETTLED = {"key-term-v4flash": 11.0, "counter-ds": 20.5,
           "label-price-per-token": 20.5, "label-ai-employee": 29.2}
HOST_AT = {"price-tag": C["tag"], "bar-deepseek": C["col"],
           "price-chart": C["col"], "computer-badge": C["tower"]}
# typed states: what first appears, on which word (WORD-SYNC)
PRINTED_KEYS = {"key-term-v4flash": "V4 FLASH", "counter-2x": "2X",
                "counter-4x": "4X", "label-price-per-token": "PRICE PER TOKEN",
                "label-ai-employee": "AI EMPLOYEE"}
_A = C["eraseA"] + SC.ERASE_D
_B = C["eraseB"] + SC.ERASE_D
_O = SC.SHEET_UP + SC.SHEET_D + 0.02
PRINTED_LIFETIME = {"key-term-v4flash": (C["keyterm"], _A),
                    "counter-2x": (C["two"] + 0.06, C["four"] + 0.22),
                    "counter-4x": (C["four"] + 0.08, _B),
                    "label-price-per-token": (C["ppt"], _B),
                    "label-ai-employee": (C["employee"], _O)}

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.
CUE_WORDS = {
    "swing": (3, "victim"), "slide": (12, "increasing"),
    "needle": (13, "demand"), "keyterm": (21, "v4"),
    "arrow": (27, "increase"), "tagflip": (29, "prices"),
    "eraseA": (35, "now,"), "two": (43, "two"), "four": (45, "four"),
    "best": (50, "one"), "c1": (51, "of"), "c3": (53, "best"),
    "ppt": (62, "price"), "task": (66, "price"), "eraseB": (77, "buy"),
    "locally": (89, "locally"), "badge": (94, "ai"), "outro": (97, "follow"),
}
# AUTHORED instants: each inside its own word's 1.0 s LABEL_WINDOW
CUE_INSIDE = {"tag": (0, "deepseek"), "gauge": (12, "increasing"),
              "col": (35, "now,"), "c2": (52, "the"), "tower": (77, "buy"),
              "employee": (94, "ai")}


# ------------------------------------------------------------------ transcript
def words() -> list[dict]:
    d = json.loads((CUT / "transcript_tight.json").read_text())
    return [w for w in d["words"] if w.get("type") == "word"]


def clean_tokens(ws: list[dict]) -> tuple[list[dict], dict]:
    """LAW 6 / LAW 46 / LAW 47, all measured on the TIGHT transcript."""
    partial = [w["text"] for w in ws
               if w["text"].strip().endswith(("-", "...", "…"))]
    if partial:
        raise SystemExit(f"unexpected partial words in the take: {partial}")
    opening = "deepseek is a victim of their own success."
    head = " ".join(w["text"] for w in ws[:8]).lower()
    if head != opening:
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[8:]).lower()
    if "is a victim of" in later:
        raise SystemExit("LAW 46: the opening repeats inside the take")
    tail = DUR - float(ws[-1]["end"])
    cap = 0.20 + 1.0 / FPS
    if tail > 0.30:
        raise SystemExit(f"LAW 47: the master runs {tail:.3f}s past the last word")
    edl = json.loads((CUT / "edl.json").read_text())
    td = edl["take_detection"]
    rep = {"law47_tail_s": round(tail, 3), "law47_cap_s": round(cap, 3),
           "law47_verdict": ("PASS" if tail <= cap else "REPORTED")
           + f" — {tail:.3f}s past the last word against a {cap:.3f}s cap",
           "law46": "the scripted opening occurs ONCE inside the keeper take, "
                    "at word 0 / 0.10 s",
           "take_corroboration": {
               "mode": td.get("mode"),
               "keep_words": td.get("keep_words"),
               "raw_word_index": td.get("take_word_index"),
               "raw_start_s": td.get("take_start_s"),
               "words": td.get("take_words"), "of_raw_words": td.get("raw_words"),
               "dropped_words": td.get("dropped_words"),
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
    # LAW 45: each incoming chapter's first object starts INSIDE the erase
    for seam, first in ((C["eraseA"], C["col"]), (C["eraseB"], C["tower"])):
        if not (seam <= first <= seam + SC.ERASE_D):
            raise SystemExit(f"LAW 45: the chapter at {seam} opens bare")
    if C["employee"] + 0.28 >= C["outro"]:
        raise SystemExit("board ink still changing under the outro sheet")
    rep["_law43"] = {"board_mode": SC.BOARD_MODE,
                     "chapters": len(SC.BOARD_CHAPTERS),
                     "seams": list(SC.CHAPTER_SEAMS)}
    return rep


def assert_word_sync(ws: list[dict]) -> dict:
    """WORD-SYNC: every typed key first shows the value its word says."""
    pairs = {"key-term-v4flash": (21, "v4", C["keyterm"]),
             "counter-2x": (43, "two", C["two"] + 0.06),
             "counter-4x": (45, "four", C["four"] + 0.08),
             "label-price-per-token": (62, "price", C["ppt"]),
             "label-ai-employee": (94, "ai", C["employee"])}
    spoken = {"v4": "V4", "two": "2X", "four": "4X", "price": "PRICE",
              "ai": "AI"}
    rows = []
    for key, (idx, text, t) in pairs.items():
        w = ws[idx]
        if w["text"].strip().lower().rstrip(",.") != text:
            raise SystemExit(f"word-sync: {key} expects {text!r} at word {idx}")
        lo, hi = float(w["start"]), float(w["end"]) + LABEL_WINDOW
        if not (lo <= t <= hi):
            raise SystemExit(f"word-sync: {key} first shows at {t}, outside "
                             f"{lo:.3f}-{hi:.3f}")
        if not PRINTED_KEYS[key].startswith(spoken[text]):
            raise SystemExit(f"word-sync: {key} prints {PRINTED_KEYS[key]!r} on "
                             f"the word {text!r}")
        rows.append({"state": key, "first_visible_text": PRINTED_KEYS[key],
                     "at": round(t, 3), "word": w["text"],
                     "word_window": [round(lo, 3), round(hi, 3)]})
    # the 2X value is gone before the 4X value is readable: never both
    if PRINTED_LIFETIME["counter-2x"][1] > C["four"] + 0.22 + 1e-9:
        raise SystemExit("word-sync: 2X lingers under the spoken 'four'")
    if min(t for _i, _x, t in pairs.values()) != C["keyterm"]:
        raise SystemExit("LAW 9: V4 FLASH is not the first type on the board")
    return {"typed_states": rows, "disagreements": 0,
            "digits_that_tick": "2X -> 4X, swapped on 'four' (15.44), the only "
                                "changing value"}


def assert_law37(ws: list[dict]) -> dict:
    cues = PCUE.scan(ws)
    plan = json.loads(PLAN.read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / "prep/stages/deepseekprices.cues.json").read_text())
    if marker["keys"]["cue_count"] != len(cues):
        raise SystemExit("LAW 37: the prep marker disagrees with the re-run")
    if cues or declared:
        raise SystemExit("LAW 37: this scene builds no source card")
    return {"scan_cue_count": 0, "plan_declared_cards": 0,
            "prep_marker_cue_count": 0, "source_cards_in_the_page": 0}


# ------------------------------------------------------------------ laws
GUTTER_REFUSE = 16.0
# the plan's blocks, in DOM ids (the plan names objects, the module ids them)
PLAN_TO_DOM = {"price-tag": "price-tag", "key-term-v4flash": "key-term-v4flash",
               "baseline": "price-chart", "deepseek-column": "col-deepseek",
               "deepseek-bar": "bar-deepseek", "counter-4x": "counter-ds",
               "claude-column": "col-claude", "openai-column": "col-openai",
               "gemini-column": "col-gemini",
               "label-price-per-token": "label-price-per-token",
               "computer-badge": "computer-badge",
               "label-ai-employee": "label-ai-employee"}


def blocks() -> list[set]:
    plan = json.loads(PLAN.read_text())
    out = [set(b) for b in SC.DECLARED_BLOCKS]
    for b in plan["blocks"]:
        out.append({PLAN_TO_DOM[n] for n in b if n in PLAN_TO_DOM})
    # a column IS its tile + bar + counter standing on the baseline: the
    # plan's chart block names the column, the module's column block names the
    # bar, so the two are one block (transitive closure over shared members)
    merged = True
    while merged:
        merged = False
        for i in range(len(out)):
            for j in range(i + 1, len(out)):
                if out[i] & out[j] and "price-chart" in (out[i] | out[j]):
                    out[i] |= out.pop(j)
                    merged = True
                    break
            if merged:
                break
    return out


def assert_label_law() -> dict:
    bl = blocks()
    out: dict = {}
    for key, (host, side, text) in LABEL_PLAN.items():
        t0 = LABEL_AT[key]
        lt_key = SC.LIFETIMES[key][1]
        for tt in (t0 + 0.40, SLIDE_DONE + 0.1, 10.5, 15.2, FOUR_DONE + 0.1,
                   BEST_DONE + 0.1, 20.5, 23.5, 29.2):
            if tt < t0 + 0.40 or not alive(key, tt) or tt >= lt_key:
                continue
            kb, hb = rect_at(key, tt), rect_at(host, tt)
            if side == "below" and kb[1] < hb[3] - 0.01:
                raise SystemExit(f"LAW 39: {key} is not entirely below {host}")
            if side == "above" and kb[3] > hb[1] + 0.01:
                raise SystemExit(f"LAW 39: {key} is not entirely above {host} "
                                 f"at {tt}")
            kc, hc = (kb[0] + kb[2]) / 2, (hb[0] + hb[2]) / 2
            if abs(kc - hc) > 0.15 * (hb[2] - hb[0]) + 0.01:
                raise SystemExit(f"LAW 39: {key} is off {host}'s axis at {tt}")
        if not any({key, host} <= b for b in bl):
            raise SystemExit(f"LAW 41: {key} is not blocked with {host}")
        if t0 < HOST_AT[host] - 1e-9:
            raise SystemExit(f"LAW 39: {key} lands before its host")
        out[key] = {"host": host, "side": side, "text": text, "at": round(t0, 3),
                    "box_canvas_settled": [round(v, 1) for v in
                                           canvas(rect_at(key, SETTLED[key]))]}
    # LAW 50: the three NAMES share one size and one side
    names = ("label-price-per-token", "label-ai-employee")
    if any(LABEL_PLAN[n][1] != "below" for n in names + ("key-term-v4flash",)):
        raise SystemExit("LAW 50: a name is not below what it names")
    out["_law50"] = {"side": "below", "font_px": SC.KEY_FS,
                     "key_term_font_px": SC.KEY_TERM_FS}
    du = SC.KEY_TERM_FS * CORE_K / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} du")
    out["_key_term"] = {"text": SC.KEY_TERM, "font_px": SC.KEY_TERM_FS,
                        "design_units": round(du, 2), "first_type": True}
    return out


def assert_lifetime_law() -> dict:
    plan = json.loads(PLAN.read_text())
    outro = {n for n in SC.LIFETIMES if n.startswith("o-")}
    anchors = [n for n, (_a, b) in SC.LIFETIMES.items() if b is None]
    for n in anchors:
        if n not in SC.SCENE_ANCHORS and n not in outro:
            raise SystemExit(f"LAW 42: {n} never leaves and is not an anchor")
    shares = {}
    for n, (a, b) in SC.LIFETIMES.items():
        if b is None:
            continue
        shares[n] = round((b - a) / DUR, 3)
        if shares[n] > 0.40:
            raise SystemExit(f"LAW 42: {n} overstays the 40 % line")
    # CHAPTERS: nothing from one chapter survives the next seam
    for ch in SC.BOARD_CHAPTERS[:-1]:
        seam = ch["erase_at"]
        for n, (a, b) in SC.LIFETIMES.items():
            if a < seam and b is not None and b > seam + SC.ERASE_D + 1e-6:
                raise SystemExit(f"LAW 43: {n} survives the seam at {seam}")
    return {"board_mode": SC.BOARD_MODE, "outro_marks": sorted(outro),
            "longest_share": max(shares.items(), key=lambda kv: kv[1]),
            "plan_marks": sorted(m["mark"] for m in plan["lifetimes"])}


SPACING_TS = (2.5, 5.0, 8.0, 11.0, 13.5, 15.2, 16.4, 18.5, 20.5, 23.0, 26.0,
              29.2)


def assert_spacing_law() -> dict:
    """LAW 41 on the co-alive seats in CORE px, at HELD instants (the page
    itself is judged by geometry_audit --strict)."""
    bl = blocks()
    names = list(RECTS) + ["bar-deepseek", "counter-ds"]
    worst = (1e9, None)
    for t in SPACING_TS:
        live = [n for n in names if alive(n, t)]
        for i in range(len(live)):
            for j in range(i + 1, len(live)):
                a, b = live[i], live[j]
                if any({a, b} <= s for s in bl):
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
            "blocks": [sorted(b) for b in bl]}


# ------------------------------------------------------ LAW 38: emphasis
# Two border flips on DRAWN objects.  The emphasis IS the object's own outline;
# its target is the object's wrapper.  check_at is a HELD frame: the 0.38 s
# flip has completed and both are alive.
EMPH = {
    "tag": {"anchor": '<path id="tag-outline" class="tg"', "id": "tag-outline",
            "kind": "border", "target": "price-tag", "check_at": 10.40,
            "window": (C["tagflip"] + 0.38, C["eraseA"])},
    "bar": {"anchor": 'id="bar-deepseek"', "id": "bar-deepseek",
            "kind": "border", "target": "col-deepseek", "check_at": 22.00,
            "window": (C["task"] + 0.38, C["eraseB"])},
}


def assert_emphasis_law() -> dict:
    for name, e in EMPH.items():
        a, b = e["window"]
        if not (a <= e["check_at"] < b):
            raise SystemExit(f"LAW 38: the {name} flip is not complete and held "
                             f"at {e['check_at']}")
    return {"border_flips": [{"on": e["id"], "target": e["target"],
                              "check_at": e["check_at"],
                              "held": [round(v, 2) for v in e["window"]]}
                             for e in EMPH.values()],
            "rings_ellipses_circles": 0, "highlights": 0,
            "dom_elements_added": 0}


def declare_contracts(html: str) -> tuple[str, dict]:
    s = html
    for name, e in EMPH.items():
        if s.count(e["anchor"]) != 1:
            raise SystemExit(f"the module no longer emits ONE {e['anchor']!r}")
        s = s.replace(e["anchor"],
                      f'{e["anchor"]} data-emphasis="{e["kind"]}" '
                      f'data-emphasis-target="{e["target"]}" '
                      f'data-check-at="{e["check_at"]:.2f}"', 1)
    return s, {"emphases_stamped": len(EMPH), "connectors_stamped": 0}


def assert_cast_law() -> dict:
    rep = DF.assert_cast_resolves(list(SC.LOGO_FILES), dict(SC.LOGO_FILES),
                                  LOGOS, label="deepseekprices stage marks")
    return {"stage_marks": sorted(SC.LOGO_FILES),
            "resolved": {k: v["path"] for k, v in rep.items()},
            "media_sides_core_px": {k: v for k, v in SC.MEDIA_SIDES.items()},
            "cutout_lanes_not_ours": list(CUTOUT_LANES)}


def assert_draw_on(tweens: list[str], html: str) -> dict:
    """THE DRAW-ON DASH LAW: every class the scene reveals with a 100-unit dash
    resolves ONLY to elements that declare pathLength="100"."""
    sels = set()
    for t in tweens:
        if "strokeDasharray:100" in t:
            sels.update(re.findall(r'tl\.set\("([^"]+)"', t))
    checked = {}
    for sel in sels:
        cls = sel.split()[-1].lstrip(".")
        tags = re.findall(rf'<[a-z]+[^>]*class="{cls}"[^>]*>', html)
        if not tags or not all('pathLength="100"' in g for g in tags):
            raise SystemExit(f"DRAW-ON: {sel} reveals a path without "
                             'pathLength="100"')
        checked[sel] = len(tags)
    return {"dash_selectors": checked, "verdict": "every dash equals its "
            "path's declared length (100)"}


# ------------------------------------------------------------------ captions
def phrases(ws: list[dict]) -> list[list[dict]]:
    out, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w)
        end = w["text"].strip().rstrip('"').endswith((".", "!", "?"))
        gap = (ws[i + 1]["start"] - w["end"]) if i + 1 < len(ws) else 9.0
        # "four ... X": the unit belongs to its number, whatever the pause
        if i + 1 < len(ws) and ws[i + 1]["text"].strip(" ,.").upper() == "X":
            gap = 0.0
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
    forbidden = {t.lower() + suf for t in PRINTED_KEYS.values()
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
const SOFT = "power2.out";
const SWING = "power2.inOut";
const POP = "back.out(2.05)";
const none = "none";
const hidden = "hidden";
const tl = gsap.timeline({{paused:true}});
{"".join(tweens)}
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
        src = ASSETS / rel
        if not src.exists():
            raise SystemExit(f"registry key {key!r} does not resolve: {src}")
        shutil.copy2(src, dst / "assets/logos" / src.name)
        CC.MARK_INK[key] = CC.measure_mark(key, src)
        marks[key] = {"source": str(src), "url": LOGO_URL[key]}
    rec["marks"] = marks
    return rec


def media() -> dict:
    """The SIX rasters the scene paints (handoff section 1, MEDIA_SIDES)."""
    return {mkey: CC.mark_img(LOGO_URL[key], key, side)
            for mkey, (key, side) in SC.MEDIA_SIDES.items()}


def sfx_plan() -> list[tuple]:
    """EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22)."""
    return [("pop", C["tag"], SFX_STRUCTURE),         # the price tag lands
            ("whoosh", C["slide"], SFX_STRUCTURE),    # tag slides, gauge draws
            ("click", C["needle"], SFX_DETAIL),       # the needle swings high
            ("click", C["keyterm"], SFX_DETAIL),      # V4 FLASH is written
            ("click", C["arrow"], SFX_DETAIL),        # the up-arrow draws
            ("whoosh", C["eraseA"], SFX_STRUCTURE),   # chapter 2 opens
            ("pop", C["two"], SFX_DETAIL),            # bar 2X
            ("pop", C["four"], SFX_STRUCTURE),        # bar 4X
            ("whoosh", C["best"], SFX_STRUCTURE),     # slide + three columns
            ("click", C["ppt"], SFX_DETAIL),          # PRICE PER TOKEN
            ("whoosh", C["eraseB"], SFX_STRUCTURE),   # chapter 3, the tower
            ("click", C["locally"], SFX_DETAIL),      # the power button
            ("pop", C["badge"], SFX_STRUCTURE),       # the lanyard drops
            ("whoosh", C["outro"], SFX_STRUCTURE)]    # the rising sheet


def assert_sfx(sfx) -> dict:
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30:
        raise SystemExit(f"SFX flam: {worst}")
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "deliberately_silent": {
                "swing 0.72": "0.54 s after the tag pop; a sway is not an arrival",
                "gauge 3.24": "0.04 s after the slide whoosh; one gesture",
                "flips 9.70 / 21.28": "a colour flip is not an arrival",
                "c1-c3 17.06-17.52": "the 16.92 whoosh scores the three rises",
                "AI EMPLOYEE 28.72": "0.04 s after the badge pop"}}


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
    # the rail binds readable INK: JetBrains Mono advances 0.600 em
    typed = {"key-term-v4flash": (SC.KEY_TERM, SC.KEY_TERM_FS, SC.KEY_TERM_LS,
                                  11.0),
             "counter-ds": ("4X", SC.COUNTER_FS, 1.0, 20.5),
             "label-price-per-token": ("PRICE PER TOKEN", SC.KEY_FS, SC.KEY_LS,
                                       20.5),
             "label-ai-employee": ("AI EMPLOYEE", SC.KEY_FS, SC.KEY_LS, 29.2)}
    rights = {}
    for n, (text, fs, ls, t) in typed.items():
        b = canvas(rect_at(n, t))
        ink = len(text) * 0.6 * fs + (len(text) - 1) * ls
        rights[n] = round((b[0] + b[2]) / 2 + ink / 2, 1)
    type_right = max(rights.values())
    if type_right > CAP.LAW12_RAIL_X + 0.01:
        raise SystemExit(f"readable key ink reaches x={type_right:.1f}")
    names = list(RECTS) + ["bar-deepseek", "counter-ds"]
    boxes = [canvas(rect_at(n, t)) for n in names for t in SPACING_TS
             if alive(n, t)]
    ink_left = min(b[0] for b in boxes)
    ink_right = max(b[2] for b in boxes)
    if ink_left < 40 or W - ink_right < 40:
        raise SystemExit("the composition leaves the 40 px frame margin")
    return {"readable_type_right_x": rights, "ink_left_x": ink_left,
            "ink_right_x": ink_right, "law12_rail_x": CAP.LAW12_RAIL_X}


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
    cues = assert_cues(ws)
    wordsync = assert_word_sync(ws)
    law37 = assert_law37(ws)
    labels = assert_label_law()
    lifetimes = assert_lifetime_law()
    spacing = assert_spacing_law()
    emphasis = assert_emphasis_law()
    cast = assert_cast_law()
    SFX = sfx_plan()
    sfx_guard = assert_sfx(SFX)

    scene_html, tweens = SC.build(media(), outro_lockup(handle))
    drawon = assert_draw_on(tweens, scene_html)
    if "data-connect-to" in scene_html:
        raise SystemExit("LAW 40: the plan has no connectors")
    scene_html, declared = declare_contracts(scene_html)
    if scene_html.count("data-emphasis=") != scene_html.count("data-check-at"):
        raise SystemExit("an emphasis is missing its check instant")
    for shape in ("<circle", "<ellipse"):
        if shape in scene_html:
            raise SystemExit(f"LAW 38 rule 3: {shape} in the emitted scene")
    for key, (host, _s, _t) in LABEL_PLAN.items():
        if scene_html.count(f'data-label-for="{host}"') != 1:
            raise SystemExit(f"{key} does not declare its host {host}")

    m = CAP.PillMeasurer(RUN / "gen/_pillwidths_deepseekprices.json")
    beats, cap_rep = caption_beats(m, ws, clean_rep)
    CAP.assert_law12(SEAM, max(b["w"] for b in beats))
    band = guard_core_band(CORE_TOP_SPLIT, CORE_K, SEAM)
    rail = guard_rail()
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
    return {"staged": staged, "beats": beats, "seat": SEAM, "scale": CORE_K,
            "core": {"left": LEFT, "top": CORE_TOP_SPLIT}, "band": band,
            "rail": rail, "cues": cues, "word_sync": wordsync, "law37": law37,
            "law39": labels, "law42": lifetimes, "law41": spacing,
            "law38": emphasis, "declared": declared, "law2": cast,
            "law22": sfx_guard, "draw_on": drawon, "transcript": cap_rep,
            "phone_objects": objs, "render": {"w": 1080, "h": 1920, "zoom": 1}}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="split", choices=("split",))
    ap.parse_args()
    dst = RUN / "projects/deepseekprices_split"
    dst.mkdir(parents=True, exist_ok=True)
    rep = build_split(dst, "yt")
    rep["handle"] = CAP.handle("yt")
    rep["captions"] = {"n": len(rep["beats"]),
                       "widest_px": round(max(b["w"] for b in rep["beats"]), 1),
                       "texts": [b["text"] for b in rep["beats"]],
                       "min_aspect": round(min(b["w"] for b in rep["beats"])
                                           / CAP.CAP_PILL_HEIGHT, 2)}
    rep.pop("beats")
    report = {"video": VID, "lane": "counter+meter", "fps": FPS,
              "duration": DUR, "seam": SEAM, "formats": {"split": rep}}
    (RUN / "gen/_build_deepseekprices_split.json").write_text(
        json.dumps(report, indent=1, default=str))
    geom = {"video": VID, "fps": FPS, "duration": DUR,
            "shared": {"beat_edges": SC.BEAT_EDGES},
            "formats": {"split": {"phone_objects": rep["phone_objects"],
                                  "core": rep["core"], "scale": rep["scale"],
                                  "seat": rep["seat"]}}}
    (RUN / f"gen/_geom_{VID}_split.json").write_text(json.dumps(geom, indent=1))
    print(f"split: {dst}")
    print(json.dumps({"captions": rep["captions"], "band": rep["band"],
                      "rail": rep["rail"], "law41": rep["law41"]["tightest_pair"],
                      "law22": rep["law22"]["tightest_gap_s"],
                      "phone": rep["phone_objects"]}, indent=1))


if __name__ == "__main__":
    main()
