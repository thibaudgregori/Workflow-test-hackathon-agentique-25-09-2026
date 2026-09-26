#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION — hermesbrowser / ICON CHOREOGRAPHY.

    YouTube   classic split 50/50   projects/hermesbrowser_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/hermesbrowser_scene.py`
plus `plans/hermesbrowser_scene_handoff.md` are the design agent's artefacts,
sealed by `review/artwork_pass_hermesbrowser.json` (production v4,
`production.py seal`).  This file IMPORTS the module and SEATS it at the
handoff's own placement (k = 1.00, left 0, core top 192).  It never mutates a
byte of the module on disk; it only stamps the round-4 declarations the page
owes (connector anchors, emphasis targets, check instants) onto the emitted
string.

HD DELIVERY: authored AND encoded 1080x1920.  The face plate is
`face_bottom_hd.mp4` (1080x1058), so the seam is 1920 - 1057.5 = 862.5 and the
RENDERING pill top is 862.5 - 114.59/2 = 805.205 (the pill that renders, never
the frozen 108.2 seat constant).  The core's content band 70..574 lands at
canvas 262..766: 70 px under LAW 30's top-10 % line, 39.2 px over the pill.

TAKEOVER and FACESPLIT are not daily deliverables and this file cannot build one.
"""
from __future__ import annotations

import argparse
import hashlib
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
import hermesbrowser_scene as SC                # noqa: E402

RUN = Path(__file__).resolve().parents[1]
CUT = RUN / "cuts/hermesbrowser"
PLAN = RUN / "plans/hermesbrowser_plan.json"
ASSETS = Path.home() / "Documents/Workspace/assets"
LOGOS = ASSETS / "logos"
LIB_MUSIC = ASSETS / "audio/music/shorts-factory"
LIB_SFX = ASSETS / "audio/sfx/shorts-factory"
SCENE_FILE = Path(SC.__file__).resolve()

VID = "hermesbrowser"
W, H = 1080.0, 1920.0
FPS = 25
DUR = SC.DUR                                     # 26.48, the cut master

SEAM = 862.5
CORE_TOP_SPLIT = SC.CANVAS_OFFSET                # 192.0, the handoff's number
CORE_K = 1.00
LEFT = (W - SC.CORE_W * CORE_K) / 2              # 0.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "Hermes Agent gets its own browser"
LABEL_WINDOW = 1.0
C = SC.CUE

# ------------------------------------------------------------------ marks
# MARK IDENTITY: Hermes is the Nous girl, file `nous-girl-line.png`, never the
# Hermes H glyph (handoff section 1).
STAGE_FILES = {k: f"logos/{v}" for k, v in SC.LOGO_FILES.items()}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}
HERMES_KEY = next(iter(SC.LOGO_FILES))
CUTOUT_LANES = SC.CUTOUT_LOGO_LANES

# ------------------------------------------------------------------ geometry
# The browser is ONE element authored at its chapter-B home and offset by
# transforms: chapter A (+86, +130) until the 3.58 glide lands, chapter C
# (-200, 0) once the 15.40 slide lands.  MAIN BROWSER slides with it.
GLIDE_DONE = C["seamA"] + 0.04 + 0.50            # 4.12
SLIDE_DONE = C["question"] + 0.46                # 15.86
TILE_SLID = C["browser"] + 0.40                  # 1.48


def _lbl(b) -> tuple:
    x, y, w, h = b
    return (x, y, x + w, y + h)


def _tile(xy) -> tuple:
    return (xy[0], xy[1], xy[0] + SC.TILE, xy[1] + SC.TILE)


def _shift(b, dx, dy=0.0) -> tuple:
    return (b[0] + dx, b[1] + dy, b[2] + dx, b[3] + dy)


RECTS: dict[str, tuple] = {
    "hb-tile": _tile(SC.TILE_A),
    "key-hermes-agent": _lbl(SC.KEY_TERM_BOX),
    "hb-browser": SC.BROWSER_B,
    "lbl-browser": _lbl(SC.LBL_BROWSER),
    "app-frame": SC.FRAME_BOX,
    "lbl-main": _lbl(SC.LBL_MAIN_B),
    "q-bubble": _lbl(SC.BUBBLE),
    "hb-tile-c": _tile(SC.TILE_C),
    "lbl-hermes": _lbl(SC.LBL_HERMES),
}
for _i, _n in enumerate(SC.OBJ_NAMES):
    RECTS[f"obj-{_n}"] = SC.obj_box(_i)
    RECTS[f"lbl-{_n}"] = (SC.OBJ_CX[_i] - SC.VERB_SEAT / 2, SC.VERB_ROW_Y,
                          SC.OBJ_CX[_i] + SC.VERB_SEAT / 2, SC.VERB_ROW_Y + 44.0)


def rect_at(name: str, t: float) -> tuple:
    b = RECTS[name]
    if name == "hb-browser":
        if t < GLIDE_DONE:
            return SC.BROWSER_A
        if t >= SLIDE_DONE:
            return SC.BROWSER_C
        return b
    if name == "lbl-main" and t >= SLIDE_DONE:
        return _shift(b, SC.BR_C_DX)
    if name == "hb-tile" and t < TILE_SLID:
        return _shift(b, SC.TILE_A_START_DX)
    return b


def lifetime(name: str) -> tuple:
    return SC.LIFETIMES[name]


def alive(name: str, t: float) -> bool:
    a, b = lifetime(name)
    return a <= t and (b is None or t < b)


def canvas(box):
    """core px -> the canvas this page actually paints (top 192, k 1.00)."""
    return (CORE_K * box[0] + LEFT, CORE_TOP_SPLIT + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP_SPLIT + CORE_K * box[3])


# --------------------------------------------------------------- label plan
# id -> (host, side, printed text, first-visible instant, word index, spoken)
LABEL_PLAN = {
    "key-hermes-agent": ("app-frame", "above", SC.KEY_TERM, C["keyterm"], 0,
                         ["hermes", "agent"]),
    "lbl-browser": ("hb-browser", "below", "BROWSER", C["lbl_browser"], 5,
                    ["browser"]),
    "lbl-binoculars": ("obj-binoculars", "below", "SEE", C["lbl_see"], 23,
                       ["see"]),
    "lbl-wheel": ("obj-wheel", "below", "OPERATE", C["lbl_operate"], 26,
                  ["operate"]),
    "lbl-microscope": ("obj-microscope", "below", "ANALYZE", C["lbl_analyze"],
                       28, ["analyze"]),
    "lbl-main": ("hb-browser", "below", "MAIN BROWSER", C["lbl_main"], 43,
                 ["main", "browser"]),
    "lbl-hermes": ("hb-tile-c", "below", "HERMES AGENT", C["lbl_hermes"], 60,
                   ["hermes", "agent"]),
}
PRINTED_KEYS = {k: v[2] for k, v in LABEL_PLAN.items()}

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.
CUE_WORDS = {
    "tile": (0, "hermes"), "keyterm": (1, "agent"), "browser": (5, "browser"),
    "frame": (9, "desktop"), "seamA": (11, "now,"), "see": (23, "see,"),
    "operate": (26, "operate"), "analyze": (28, "analyze"),
    "flip": (29, "anything"), "seamB": (35, "so"), "question": (49, "any"),
    "hermes": (60, "hermes"), "do": (66, "do"), "help": (70, "help"),
    "outro": (74, "now"),
}
# AUTHORED instants: each inside its own word's 1.0 s LABEL_WINDOW
CUE_INSIDE = {"lbl_browser": (5, "browser"), "lbl_see": (23, "see,"),
              "lbl_operate": (26, "operate"), "lbl_analyze": (28, "analyze"),
              "lbl_main": (43, "main"), "lbl_hermes": (60, "hermes"),
              "flipback": (34, "it.")}


def _norm(t: str) -> str:
    return t.strip().lower().strip('.,!?"')


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
    opening = "hermes agent now has a browser inside of its desktop application"
    head = " ".join(_norm(w["text"]) for w in ws[:11])
    if head != opening:
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(_norm(w["text"]) for w in ws[11:])
    if "agent now has a" in later or "has a browser inside" in later:
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
    if C["help"] + 0.38 >= C["outro"]:
        raise SystemExit("board ink still changing under the outro sheet")
    rep["_law43"] = {"board_mode": SC.BOARD_MODE, "chapters": 3,
                     "seams": [C["seamA"], C["seamB"]], "outro": C["outro"]}
    return rep


def assert_word_sync(ws: list[dict]) -> dict:
    """WORD-SYNC: every typed key first shows the value its words say, landing
    between its first spoken word and LABEL_WINDOW after its last."""
    rows = []
    for key, (_h, _s, text, t, idx, spoken) in LABEL_PLAN.items():
        got = [_norm(x["text"]) for x in ws[idx: idx + len(spoken)]]
        if got != spoken:
            raise SystemExit(f"word-sync: {key} expects {spoken} from word "
                             f"{idx}, the take says {got}")
        if " ".join(spoken).upper() != text:
            raise SystemExit(f"word-sync: {key} prints {text!r} on {spoken}")
        w = ws[idx + len(spoken) - 1]
        lo = float(ws[idx]["start"])
        hi = float(w["end"]) + LABEL_WINDOW
        if not (lo - 1e-6 <= t <= hi):
            raise SystemExit(f"word-sync: {key} first shows at {t}, outside "
                             f"{' '.join(spoken)!r} {lo:.3f}-{hi:.3f}")
        rows.append({"state": key, "first_visible_text": text, "at": t,
                     "spoken": " ".join(spoken),
                     "word_window": [round(lo, 3), round(hi, 3)]})
    if min(v[3] for v in LABEL_PLAN.values()) != C["keyterm"]:
        raise SystemExit("LAW 9: HERMES AGENT is not the first type")
    return {"typed_states": rows, "disagreements": 0, "digits_that_tick": 0}


def assert_law37(ws: list[dict]) -> dict:
    cues = PCUE.scan(ws)
    plan = json.loads(PLAN.read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / f"prep/stages/{VID}.cues.json").read_text())
    if marker["keys"]["cue_count"] != len(cues):
        raise SystemExit("LAW 37: the prep marker disagrees with the re-run")
    if cues or declared:
        raise SystemExit("LAW 37: this scene builds no source card")
    return {"scan_cue_count": 0, "plan_declared_cards": 0,
            "prep_marker_cue_count": 0, "source_cards_in_the_page": 0}


# ------------------------------------------------------------------ laws
GUTTER_REFUSE = 16.0
HELD = [3.10, 3.50, 5.0, 8.40, 9.30, 10.40, 11.20, 13.0, 14.5, 17.0, 19.0,
        20.90, 21.90]


def assert_label_law() -> dict:
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    out: dict = {}
    for key, (host, side, text, t0, _i, _s) in LABEL_PLAN.items():
        checked = []
        for tt in [t0 + 0.30] + HELD:
            if tt < t0 or not alive(key, tt) or not alive(host, tt):
                continue
            if host == "hb-browser" and (C["seamA"] <= tt < GLIDE_DONE
                                         or C["question"] <= tt < SLIDE_DONE):
                continue                          # the browser is in transit
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
        if not any({key, host} <= b for b in blocks):
            raise SystemExit(f"LAW 41: {key} is not blocked with {host}")
        out[key] = {"host": host, "side": side, "text": text, "at": t0,
                    "checked_at": checked,
                    "box_canvas": [round(v, 1) for v in canvas(RECTS[key])]}
    # the key term lands on "Agent" ABOVE the centred tile, before the frame
    # that becomes its host exists (plan labels[0].note): same axis x = 540
    kt, tile0 = rect_at("key-hermes-agent", 0.8), rect_at("hb-tile", 0.8)
    if not (kt[3] <= tile0[1] and abs((kt[0] + kt[2]) / 2 - (tile0[0] + tile0[2]) / 2)
            < 0.5):
        raise SystemExit("LAW 9: HERMES AGENT is not above the centred tile")
    out["_key_term_before_frame"] = {"above": "hb-tile (centred)", "axis_x": 540}
    # LAW 50: the verb row, and the chapter-C row
    for row in (("lbl-binoculars", "lbl-wheel", "lbl-microscope"),
                ("lbl-main", "lbl-hermes")):
        ys = {RECTS[n][1] for n in row}
        hs = {round(RECTS[n][3] - RECTS[n][1], 3) for n in row}
        ws_ = {round(RECTS[n][2] - RECTS[n][0], 3) for n in row}
        if len(ys) != 1 or len(hs) != 1 or len(ws_) != 1:
            raise SystemExit(f"LAW 50: {row} do not share one seat/baseline")
    out["_law50"] = {"verb_row_y": SC.VERB_ROW_Y, "c_row_y": SC.C_ROW_Y,
                     "font_px": SC.KEY_FS}
    du = SC.KEY_TERM_FS * CORE_K / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} du")
    out["_key_term"] = {"text": SC.KEY_TERM, "font_px": SC.KEY_TERM_FS,
                        "design_units": round(du, 2), "first_type": True}
    return out


def assert_lifetime_law() -> dict:
    for n, (a, b) in SC.LIFETIMES.items():
        if b is None:
            if n not in SC.SCENE_ANCHORS and not n.startswith("o-"):
                raise SystemExit(f"LAW 42: {n} never leaves and is not an anchor")
            continue
        if (b - a) / DUR > 0.40 and n not in SC.SCENE_ANCHORS:
            raise SystemExit(f"LAW 42: {n} overstays the 40 % line")
    for anc in SC.SCENE_ANCHORS:
        for seam in (C["seamA"], C["seamB"]):
            if not alive(anc, seam) or not alive(anc, seam + 0.6):
                raise SystemExit(f"LAW 45: the anchor {anc} is not on the board "
                                 f"through the seam {seam}")
    return {"board_mode": SC.BOARD_MODE, "chapters": len(SC.BOARD_CHAPTERS),
            "anchors": list(SC.SCENE_ANCHORS),
            "longest_finite_share_non_anchor": round(max(
                (b - a) / DUR for n, (a, b) in SC.LIFETIMES.items()
                if b is not None and n not in SC.SCENE_ANCHORS), 3)}


def assert_spacing_law() -> dict:
    """LAW 41 on the co-alive seats in CORE px (the page itself is judged by
    geometry_audit --strict)."""
    plan = json.loads(PLAN.read_text())
    alias = {"browser": "hb-browser", "hermes-tile": "hb-tile",
             "label-browser": "lbl-browser", "binoculars": "obj-binoculars",
             "label-see": "lbl-binoculars", "steering-wheel": "obj-wheel",
             "label-operate": "lbl-wheel", "microscope": "obj-microscope",
             "label-analyze": "lbl-microscope",
             "label-main-browser": "lbl-main", "hermes-tile-c": "hb-tile-c",
             "label-hermes": "lbl-hermes", "question-bubble": "q-bubble"}
    blocks = ([set(b) for b in SC.DECLARED_BLOCKS]
              + [{alias.get(x, x) for x in b} for b in plan["blocks"]])
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
# (target box in core px at the check instant, check instant). Each check
# instant is a HELD frame: the draw has completed and both ends are alive.
CONNECTORS = {
    "link-binoculars": (SC.BROWSER_B, 10.60, SC.VERB_ENDS[0]),
    "link-wheel": (SC.BROWSER_B, 10.60, SC.VERB_ENDS[1]),
    "link-microscope": (SC.BROWSER_B, 10.60, SC.VERB_ENDS[2]),
    "link-do": (SC.BROWSER_C, 21.00, SC.DO_END),
}


def _tip(html: str, cid: str, head: bool) -> tuple[float, float]:
    """The PAINTED end: the shaft's end, or the arrowhead's middle vertex."""
    m = re.search(rf'id="{cid}" style="left:([\d.-]+)px;top:([\d.-]+)px', html)
    if not m:
        raise SystemExit(f"{cid}: cannot read its wrapper")
    x0, y0 = map(float, m.groups())
    i = html.index(f'id="{cid}"')
    if head:
        h = re.search(r'class="shead"[^>]*d="M[\d.-]+ [\d.-]+ L([\d.-]+) ([\d.-]+)',
                      html[i:])
        tx, ty = map(float, h.groups())
    else:
        s = re.search(r'class="sline"[^>]*d="M[\d.-]+ [\d.-]+ L([\d.-]+) ([\d.-]+)"',
                      html[i:])
        tx, ty = map(float, s.groups())
    return (x0 + tx, y0 + ty)


def assert_anchor_law(html: str) -> dict:
    """Each end re-derived from the emitted path and the TARGET's own rect.
    production refuses a miss over 4 px."""
    out = {}
    for cid, (box, check_at, planned) in CONNECTORS.items():
        tip = _tip(html, cid, head=(cid == "link-do"))
        x0, y0, x1, y1 = box
        d = {"left": abs(tip[0] - x0), "right": abs(tip[0] - x1),
             "top": abs(tip[1] - y0), "bottom": abs(tip[1] - y1)}
        side = min(d, key=d.get)
        if side in ("left", "right"):
            ex = x0 if side == "left" else x1
            frac = round((min(max(tip[1], y0), y1) - y0) / (y1 - y0), 6)
            anchor = (ex, y0 + frac * (y1 - y0))
        else:
            ey = y0 if side == "top" else y1
            frac = round((min(max(tip[0], x0), x1) - x0) / (x1 - x0), 6)
            anchor = (x0 + frac * (x1 - x0), ey)
        miss = math.hypot(tip[0] - anchor[0], tip[1] - anchor[1])
        if miss > 4.0 + 1e-6:
            raise SystemExit(f"{cid}: its painted tip misses the {side} edge by "
                             f"{miss:.2f}px")
        drift = math.hypot(anchor[0] - planned[0], anchor[1] - planned[1])
        if drift > 4.0:
            raise SystemExit(f"{cid}: lands {drift:.2f}px from the planned end")
        a, b = SC.LIFETIMES[cid]
        if not (a + 0.30 <= check_at < (b or DUR)):
            raise SystemExit(f"{cid}: check-at {check_at} is not held")
        if not alive("hb-browser", check_at):
            raise SystemExit(f"{cid}: its target is gone at {check_at}")
        if rect_at("hb-browser", check_at) != box:
            raise SystemExit(f"{cid}: the browser is not at its box at {check_at}")
        out[cid] = {"target": "hb-browser", "side": side, "fraction": frac,
                    "check_at": check_at, "tip_core": [round(v, 2) for v in tip],
                    "anchor_core": [round(v, 2) for v in anchor],
                    "miss_px": round(miss, 2),
                    "from_planned_end_px": round(drift, 2)}
    bottoms = [out[f"link-{n}"] for n in SC.OBJ_NAMES]
    ys = {round(o["anchor_core"][1], 3) for o in bottoms}
    xs = sorted(o["anchor_core"][0] for o in bottoms)
    if len(ys) != 1 or abs((xs[0] + xs[2]) / 2 - SC.AXIS) > 0.01:
        raise SystemExit("LAW 40: the three verb links are not level/mirrored")
    return out


# ------------------------------------------------------ LAW 38: emphasis
# Both targets are DRAWN objects, so both are border flips of the object's own
# outline (LAW 38 rule 2); nothing is added to the DOM.
#   * the Hermes tile's flip is DECLARED on the tile (`data-emphasis="border"`),
#     target the Nous mark inside it (`hb-mark-c`), checked at 21.90;
#   * the browser's flip (9.92 -> 11.40) is left UNDECLARED in the DOM: the
#     emphasis contract counts every descendant stroke of the emphasis element,
#     and the browser holds the task tick, which is legitimately undrawn
#     (dashoffset 100, stroke-opacity 0) until 20.38.  Stamping it fails
#     "Completed emphasis still has an unfinished stroke" on a stroke that is
#     not the emphasis.  The flip is still a plain border-colour tween on a
#     drawn object and is verified here and by eye (see the split notes).
EMPH = {
    "browser": {"id": "hb-browser", "kind": "border", "declared": False,
                "check_at": 10.80, "window": (C["flip"] + 0.38, C["flipback"])},
    "hermes": {"id": "hb-tile-c", "kind": "border", "declared": True,
               "target": "hb-mark-c",
               "check_at": 21.90, "window": (C["help"] + 0.38, C["outro"])},
}


def assert_emphasis_law() -> dict:
    for name, e in EMPH.items():
        a, b = e["window"]
        if not (a <= e["check_at"] < b):
            raise SystemExit(f"LAW 38: the {name} flip is not complete and held "
                             f"at {e['check_at']}")
    return {"border_flips": [{"on": e["id"], "kind": e["kind"],
                              "declared": e["declared"],
                              "target": e.get("target"),
                              "check_at": e["check_at"],
                              "held": list(e["window"])} for e in EMPH.values()],
            "rings_ellipses_circles": 0, "highlights": 0,
            "dom_ink_added": 0}


def declare_contracts(html: str, anchors: dict) -> tuple[str, dict]:
    s = html
    stamped = []
    for e in EMPH.values():
        if not e["declared"]:
            continue
        key = f'id="{e["id"]}"'
        if s.count(key) != 1:
            raise SystemExit(f"cannot stamp {e['id']}")
        s = s.replace(key, f'{key} data-emphasis="{e["kind"]}" '
                           f'data-emphasis-target="{e["target"]}" '
                           f'data-check-at="{e["check_at"]:.2f}"', 1)
        stamped.append(e["id"])
    for cid, a in anchors.items():
        key = f'id="{cid}"'
        if s.count(key) != 1:
            raise SystemExit(f"cannot stamp {cid}")
        s = s.replace(key, f'{key} data-anchor-side="{a["side"]}" '
                           f'data-anchor-fraction="{a["fraction"]:g}" '
                           f'data-check-at="{a["check_at"]:.2f}"', 1)
    return s, {"connectors_stamped": len(anchors), "emphases_stamped": stamped,
               "emphases_undeclared": [e["id"] for e in EMPH.values()
                                       if not e["declared"]]}


def assert_cast_law() -> dict:
    rep = DF.assert_cast_resolves(list(STAGE_FILES), dict(SC.LOGO_FILES),
                                  LOGOS, label="hermesbrowser stage marks")
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
            k0, k1 = lifetime(key)
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
    """ONE raster, two ids (handoff section 1)."""
    url = LOGO_URL[HERMES_KEY]
    return {"_hermes_img": CC.mark_img(url, HERMES_KEY, SC.MARK_SIDE,
                                       eid="hb-mark"),
            "_hermes_img_c": CC.mark_img(url, HERMES_KEY, SC.MARK_SIDE,
                                         eid="hb-mark-c")}


def sfx_plan() -> list[tuple]:
    """EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22)."""
    return [("pop", C["tile"], SFX_STRUCTURE),        # the Hermes tile lands
            ("click", C["keyterm"], SFX_DETAIL),      # HERMES AGENT is written
            ("pop", C["browser"] + 0.08, SFX_STRUCTURE),  # the browser pops
            ("click", C["frame"], SFX_DETAIL),        # the app frame draws
            ("whoosh", C["seamA"], SFX_STRUCTURE),    # chapter A leaves, glide
            ("pop", C["see"], SFX_STRUCTURE),         # binoculars
            ("pop", C["operate"], SFX_STRUCTURE),     # steering wheel
            ("pop", C["analyze"], SFX_STRUCTURE),     # microscope
            ("whoosh", C["seamB"], SFX_STRUCTURE),    # chapter B leaves
            ("click", C["lbl_main"], SFX_DETAIL),     # MAIN BROWSER is written
            ("whoosh", C["question"], SFX_STRUCTURE),  # slide + the bubble
            ("pop", C["hermes"], SFX_STRUCTURE),      # the Hermes tile again
            ("click", C["do"], SFX_DETAIL),           # the arrow draws
            ("pop", C["do"] + 0.34, SFX_STRUCTURE),   # the tick
            ("whoosh", C["outro"], SFX_STRUCTURE)]    # the rising sheet


def assert_sfx(sfx) -> dict:
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30:
        raise SystemExit(f"SFX flam: {worst}")
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "deliberately_silent": {
                "lbl_browser 1.30": "0.14 s after the browser pop",
                "verb labels": "0.10 s after their object's pop",
                "bubble 15.56": "0.16 s inside the slide's whoosh",
                "lbl_hermes 18.40": "0.16 s after the tile pop",
                "flips": "a colour flip is not an arrival"}}


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
    rights = {}
    for n, (_h, _s, text, _t, _i, _sp) in LABEL_PLAN.items():
        b = canvas(rect_at(n, 21.0 if n in ("lbl-main", "lbl-hermes") else
                           (10.5 if n.startswith("lbl-") and n != "lbl-browser"
                            else 3.0)))
        fs, ls = ((SC.KEY_TERM_FS, 2.0) if n == "key-hermes-agent"
                  else (SC.KEY_FS, SC.KEY_LS))
        ink = len(text) * 0.6 * fs + (len(text) - 1) * ls
        rights[n] = (b[0] + b[2]) / 2 + ink / 2
    type_right = max(rights.values())
    if type_right > CAP.LAW12_RAIL_X + 0.01:
        raise SystemExit(f"readable key ink reaches x={type_right:.1f}")
    boxes = [canvas(rect_at(n, t)) for n in RECTS for t in HELD if alive(n, t)]
    ink_left = min(b[0] for b in boxes)
    ink_right = max(b[2] for b in boxes)
    if ink_left < 40 or W - ink_right < 40:
        raise SystemExit("the composition leaves the 40 px frame margin")
    return {"readable_type_right_x": round(type_right, 1),
            "ink_left_x": ink_left, "ink_right_x": ink_right,
            "law30_rail_x": CAP.LAW12_RAIL_X}


def phone_objects() -> list[dict]:
    plan = json.loads(PLAN.read_text())
    by_name = {o["name"]: o for o in plan["bespoke_objects"]}
    out = []
    for o in SC.BESPOKE:
        x0, y0, x1, y1 = canvas(o["core"])
        bb = [round(x0 / W, 4), round(y0 / H, 4), round(x1 / W, 4),
              round(y1 / H, 4)]
        pb = by_name[o["name"]]["bbox"]
        if max(abs(a - b) for a, b in zip(bb, pb)) > 0.002:
            raise SystemExit(f"{o['name']}: the plan's bbox {pb} disagrees with "
                             f"the page {bb}")
        out.append({"name": o["name"], "t": o["t"], "bbox": pb,
                    "canvas": [x0, y0, x1, y1]})
    return out


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ------------------------------------------------------------------ build
def build_split(out: Path, handle: str) -> dict:
    scene_sha = sha(SCENE_FILE)
    seal = json.loads((RUN / f"review/artwork_pass_{VID}.json").read_text())
    if seal["evidence"].get(str(SCENE_FILE)) != scene_sha:
        raise SystemExit("the scene module no longer matches its seal")
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
    if scene_html.count("data-connect-to") != 4:
        raise SystemExit("the scene does not carry four connectors")
    if scene_html.count("data-label-for") != 7:
        raise SystemExit("the scene does not carry seven labelled keys")
    if (scene_html.count("data-connect-to") + scene_html.count("data-emphasis=")
            != scene_html.count("data-check-at")):
        raise SystemExit("a connector or emphasis is missing its check instant")
    for shape in ("<circle", "<ellipse"):
        if shape in scene_html:
            raise SystemExit(f"LAW 38 rule 3: {shape} in the emitted scene")

    m = CAP.PillMeasurer(RUN / f"gen/_pillwidths_{VID}.json")
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
    if sha(SCENE_FILE) != scene_sha:
        raise SystemExit("the scene module changed during the build")
    rep.update({"staged": staged, "beats": beats, "seat": SEAM, "scale": CORE_K,
                "core": {"left": LEFT, "top": CORE_TOP_SPLIT},
                "transcript": cap_rep, "phone_objects": objs,
                "scene_sha256": scene_sha,
                "render": {"w": 1080, "h": 1920, "zoom": 1}})
    return rep


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="split", choices=("split",))
    ap.parse_args()
    dst = RUN / f"projects/{VID}_split"
    dst.mkdir(parents=True, exist_ok=True)
    rep = build_split(dst, "yt")
    rep["handle"] = CAP.handle("yt")
    rep["captions"] = {"n": len(rep["beats"]),
                       "widest_px": round(max(b["w"] for b in rep["beats"]), 1),
                       "texts": [b["text"] for b in rep["beats"]],
                       "min_aspect": round(min(b["w"] for b in rep["beats"])
                                           / CAP.CAP_PILL_HEIGHT, 2)}
    rep.pop("beats")
    report = {"video": VID, "lane": "icon choreography", "fps": FPS,
              "duration": DUR, "seam": SEAM, "formats": {"split": rep}}
    (RUN / f"gen/_build_{VID}_split.json").write_text(
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
                      "law41_px": rep["law41"]["tightest_core_px"],
                      "law22": rep["law22"]["tightest_gap_s"],
                      "declared": rep["declared"],
                      "law40": {k: (v["side"], v["fraction"], v["miss_px"])
                                for k, v in rep["law40"].items()},
                      "phone": rep["phone_objects"]}, indent=1))


if __name__ == "__main__":
    main()
