#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION — openairesets / ICON CHOREOGRAPHY.

    YouTube   classic split 50/50   projects/openairesets_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/openairesets_scene.py`
plus `plans/openairesets_scene_handoff.md` are the design agent's artefacts,
sealed by `review/artwork_pass_openairesets.json` (production v4,
`production.py seal`).  This file IMPORTS the module and SEATS it at the
handoff's own placement (k = 1.00, left 0, core top 192).  It never mutates a
byte of the module on disk.

FORMAT-SIDE STAMPS ON THE EMITTED STRING (the module on disk is untouched):
  * the one connector (`#conn-sell`) gets `data-anchor-side="left"`,
    `data-anchor-fraction="0.5"` and `data-check-at` (production's LAW 40
    contract), checked after the arrow has drawn and the hourglass has stopped
    moving (before the flip);
  * the one emphasis (`#emph-hourglass`, a box) gets
    `data-emphasis-target="hourglass"` and `data-check-at` once it has popped.

TWO FORMAT-SIDE REPAIRS, BOTH ON THE EMITTED OUTPUT (logged in
`plans/openairesets_split_notes.md`):
  * LAW 24 (NO PEEK-AHEAD): ' / MONTH' lands on the START of 'month' (5.52)
    instead of 'per' (5.36);
  * the emphasis box is inked TERRA_L rgb(221,114,89) instead of TERRA: the
    hourglass's sand IS TERRA, and visual_laws refuses an emphasis painted in
    its target's own ink.  TERRA_L is the chart's emphasis-flip terracotta.

HD DELIVERY: authored AND encoded 1080x1920.  The face plate is
`face_bottom_hd.mp4` (1080x1058), so the seam is 1920 - 1057.5 = 862.5 and the
RENDERING pill top is 862.5 - 114.59/2 = 805.205.  The core's content band
72..564 lands at canvas 264..756: 72 px under LAW 30's top-10 % line and
49.2 px over the pill.

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
import openairesets_scene as SC                 # noqa: E402

RUN = Path(__file__).resolve().parents[1]
CUT = RUN / "cuts/openairesets"
PLAN = RUN / "plans/openairesets_plan.json"
ASSETS = Path.home() / "Documents/Workspace/assets"
LOGOS = ASSETS / "logos"
LIB_MUSIC = ASSETS / "audio/music/shorts-factory"
LIB_SFX = ASSETS / "audio/sfx/shorts-factory"

VID = "openairesets"
W, H = 1080.0, 1920.0
FPS = 25
DUR = SC.DUR                                     # 20.64, the cut master

SEAM = 862.5
CORE_TOP_SPLIT = SC.CANVAS_OFFSET                # 192.0, the handoff's number
CORE_K = 1.00
LEFT = (W - SC.CORE_W * CORE_K) / 2              # 0.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "OpenAI now sells usage resets"
LABEL_WINDOW = 1.0

# ------------------------------------------------------------------ marks
STAGE_FILES = {k: f"logos/{v}" for k, v in SC.LOGO_FILES.items()}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}
CUTOUT_LANES = SC.CUTOUT_LOGO_LANES

# ------------------------------------------------------------------ geometry
SHIFT_DONE = SC.CUE["shift"] + 0.36              # the slide's own duration
HOME_DONE = SC.CUE["home"] + 0.40


def _b(x, y, w, h) -> tuple:
    return (x, y, x + w, y + h)


# CORE px boxes at their held seats.
RECTS: dict[str, tuple] = {
    "hourglass": SC.HG_BOX,
    "openai-tile": SC.OPENAI_BOX,
    "price-tag": SC.TAG_INK,
    "key-term": _b(*SC.KEY_TERM_BOX),
    "key-200": _b(*SC.K200_BOX),
    "emph-hourglass": _b(*SC.EMPH_BOX),
    "hg-row": SC.ROW_BOX,
    "key-accounts": _b(*SC.KACC_BOX),
    "wall": SC.WALL_BOX,
    "key-building": _b(*SC.KBUILD_BOX),
}


def rect_at(name: str, t: float) -> tuple:
    b = RECTS[name]
    if name == "hourglass" and SHIFT_DONE - 1e-9 <= t < SC.CUE["home"]:
        return (b[0] + SC.HG_SHIFT_DX, b[1], b[2] + SC.HG_SHIFT_DX, b[3])
    return b


def canvas(box):
    """core px -> the canvas this page actually paints (top 192, k 1.00)."""
    return (CORE_K * box[0] + LEFT, CORE_TOP_SPLIT + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP_SPLIT + CORE_K * box[3])


# --------------------------------------------------------------- label plan
# LAW 39 / LAW 9 / LAW 50: RESETS ABOVE the hourglass (the key term); every
# object name BELOW what it names.
LABEL_PLAN = {"key-term": ("hourglass", "above", SC.KEY_TERM),
              "key-200": ("hourglass", "below", "$200 / MONTH"),
              "key-accounts": ("hg-row", "below", "4 ACCOUNTS"),
              "key-building": ("wall", "below", "KEEP BUILDING")}
LABEL_AT = {"key-term": SC.CUE["keyterm"], "key-200": SC.CUE["k200"],
            "key-accounts": SC.CUE["kacc"], "key-building": SC.CUE["kbuild"]}
HOST_AT = {"hourglass": SC.CUE["hg"], "hg-row": SC.CUE["hg2"],
           "wall": SC.CUE["c1"]}
PRINTED_KEYS = {k: v[2] for k, v in LABEL_PLAN.items()}
PRINTED_LIFETIME = {k: SC.LIFETIMES[k] for k in PRINTED_KEYS}

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.
CUE_WORDS = {
    "hg": (0, "openai"), "shift": (3, "selling"), "openai": (3, "selling"),
    "flip": (4, "resets"), "keyterm": (5, "for"),
    "ch0out": (8, "because"), "home": (9, "now"), "k200": (12, "$200"),
    "kmonth": (13, "per"), "drain1": (15, "subscription"), "drain2": (17, "no"),
    "emph": (18, "longer"), "k200out": (23, "which"), "shrink": (27, "to"),
    "hg2": (28, "four"), "hg3": (29, "different"), "hg4": (30, "accounts"),
    "allonce": (31, "all"), "c1": (40, "keep"), "c2": (41, "building"),
    "c3": (43, "things"), "outro": (47, "now"),
}
# AUTHORED instants, each inside its own word's window (start .. end + 1.0 s)
CUE_INSIDE = {"stream0": (0, "openai"), "drain0": (0, "openai"),
              "sell": (3, "selling"), "flipend": (4, "resets"),
              "kacc": (30, "accounts"), "kbuild": (41, "building"),
              "hand": (28, "four"), "tag": (6, "their")}
# drain0end = the end of 'started' (1.00); emphout = after 'users,' (8.80).
CUE_FREE = ("drain0end", "emphout")


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
    opening = "openai just started selling resets"
    head = " ".join(w["text"] for w in ws[:5]).lower()
    if head != opening:
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[5:]).lower()
    if "openai just started" in later:
        raise SystemExit("LAW 46: the opening repeats inside the take")
    tail = DUR - float(ws[-1]["end"])
    cap = 0.20 + 1.0 / FPS
    if tail > 0.30:
        raise SystemExit(f"LAW 47: the master runs {tail:.3f}s past the last word")
    edl = json.loads((CUT / "edl.json").read_text())
    td = edl["take_detection"]
    if td.get("corroboration") != "model-authored keep ranges":
        raise SystemExit(f"the keeper take is uncorroborated: {td.get('corroboration')}")
    rep = {"law47_tail_s": round(tail, 3), "law47_cap_s": round(cap, 3),
           "law47_verdict": ("PASS" if tail <= cap else "REPORTED")
           + f" — {tail:.3f}s past the last word against a {cap:.3f}s cap",
           "law46": "the scripted opening occurs ONCE inside the keeper take, "
                    "at word 0 / 0.10 s",
           "take_corroboration": {
               "mode": td.get("mode"), "keep_words": td.get("keep_words"),
               "take_word_index": td.get("take_word_index"),
               "take_start_s": td.get("take_start_s"),
               "dropped_words": td.get("dropped_words"),
               "raw_words": td.get("raw_words"),
               "corroboration": td.get("corroboration")},
           "words": len(ws)}
    return list(ws), rep


def _norm(s: str) -> str:
    return s.strip().lower().rstrip(",.")


def assert_cues(ws: list[dict]) -> dict:
    rep: dict = {}
    for name, (idx, text) in CUE_WORDS.items():
        w = ws[idx]
        if _norm(w["text"]) != text:
            raise SystemExit(f"cue {name}: word {idx} is {w['text']!r}, not "
                             f"{text!r} — the cut moved")
        got = round(float(w["start"]), 3)
        if abs(got - SC.CUE[name]) > 0.011:
            raise SystemExit(f"cue {name}: the scene fires at {SC.CUE[name]}, "
                             f"the word starts at {got}")
        rep[name] = {"word": idx, "text": w["text"], "t": SC.CUE[name]}
    for name, (idx, text) in CUE_INSIDE.items():
        w = ws[idx]
        if _norm(w["text"]) != text:
            raise SystemExit(f"cue {name}: word {idx} is {w['text']!r}")
        t = SC.CUE[name]
        lo, hi = float(w["start"]), float(w["end"]) + LABEL_WINDOW
        if not (lo <= t <= hi):
            raise SystemExit(f"cue {name} at {t} is outside the window of "
                             f"{w['text']!r} ({lo:.3f}-{hi:.3f})")
        rep[name] = {"word": idx, "text": w["text"], "t": t,
                     "window": [round(lo, 3), round(hi, 3)]}
    if abs(SC.CUE["drain0end"] - float(ws[2]["end"])) > 0.011:
        raise SystemExit("drain0end no longer lands on the end of 'started'")
    if not (float(ws[22]["end"]) <= SC.CUE["emphout"] < SC.CUE["k200out"]):
        raise SystemExit("the emphasis leaves before 'users,' ends")
    rep["drain0end"] = {"end_of": "started", "t": SC.CUE["drain0end"]}
    rep["emphout"] = {"after": "users,", "t": SC.CUE["emphout"]}
    missing = set(SC.CUE) - set(rep)
    if missing:
        raise SystemExit(f"cues the build never verified: {sorted(missing)}")
    if SC.BOARD_MODE != "chapters" or len(SC.BOARD_CHAPTERS) != 2:
        raise SystemExit("the scene is no longer the two chapters the plan "
                         "declared")
    if SC.CUE["c3"] + 0.36 >= SC.CUE["outro"]:
        raise SystemExit("board ink still changing under the outro sheet")
    rep["_law43"] = {"board_mode": SC.BOARD_MODE, "chapters": 2,
                     "erase_at": SC.BOARD_CHAPTERS[0]["erase_at"]}
    return rep


def assert_word_sync(ws: list[dict]) -> dict:
    """WORD-SYNC: every typed key first shows the value its word says."""
    rows = []
    checks = [  # (state, first visible text, at, word idx, word)
        ("key-term", "RESETS", SC.CUE["keyterm"], 4, "resets"),
        ("key-200 ($200)", "$200", SC.CUE["k200"], 12, "$200"),
        ("key-200 (/ MONTH)", "$200 / MONTH", KMONTH_AT, 14, "month"),
        ("key-accounts", "4 ACCOUNTS", SC.CUE["kacc"], 30, "accounts"),
        ("key-building", "KEEP BUILDING", SC.CUE["kbuild"], 41, "building"),
    ]
    for state, text, t, idx, word in checks:
        w = ws[idx]
        if _norm(w["text"]) != word:
            raise SystemExit(f"word-sync: {state} expects {word!r} at word {idx}")
        lo, hi = float(w["start"]), float(w["end"]) + LABEL_WINDOW
        if not (lo <= t <= hi):
            raise SystemExit(f"word-sync: {state} first shows at {t}, outside "
                             f"{lo:.3f}-{hi:.3f}")
        rows.append({"state": state, "first_visible_text": text, "at": t,
                     "word": w["text"], "word_window": [round(lo, 3), round(hi, 3)]})
    # the typed number is the spoken number, and the count is the spoken count
    if "$200" not in PRINTED_KEYS["key-200"] or ws[12]["text"] != "$200":
        raise SystemExit("word-sync: the typed price is not the spoken price")
    if not PRINTED_KEYS["key-accounts"].startswith("4 ") or _norm(ws[28]["text"]) != "four":
        raise SystemExit("word-sync: the typed count is not the spoken count")
    if min(LABEL_AT.values()) != LABEL_AT["key-term"]:
        raise SystemExit("LAW 9: RESETS is not the first type on the board")
    return {"typed_states": rows, "disagreements": 0, "digits_that_tick": 0}


def assert_law37(ws: list[dict]) -> dict:
    cues = PCUE.scan(ws)
    plan = json.loads(PLAN.read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / "prep/stages/openairesets.cues.json").read_text())
    if marker["keys"]["cue_count"] != len(cues):
        raise SystemExit("LAW 37: the prep marker disagrees with the re-run")
    if cues or declared:
        raise SystemExit("LAW 37: this scene builds no source card")
    return {"scan_cue_count": 0, "plan_declared_cards": 0,
            "source_cards_in_the_page": 0}


# ------------------------------------------------------------------ laws
GUTTER_REFUSE = 16.0


def _groups() -> list[set]:
    """LAW 41 blocks, transitively merged (the plan's and the module's)."""
    plan = json.loads(PLAN.read_text())
    alias = {"hg-row": "hg-row", "openai-tile": "openai-tile"}
    pairs = [tuple(b) for b in plan["blocks"]] + [tuple(b) for b in SC.DECLARED_BLOCKS]
    groups: list[set] = []
    for p in pairs:
        s = {alias.get(x, x) for x in p}
        hit = [g for g in groups if g & s]
        for g in hit:
            s |= g
            groups.remove(g)
        groups.append(s)
    return groups


def assert_label_law() -> dict:
    groups = _groups()
    out: dict = {}
    for key, (host, side, text) in LABEL_PLAN.items():
        t = LABEL_AT[key]
        kb, hb = rect_at(key, t + 0.5), rect_at(host, t + 0.5)
        if side == "below" and kb[1] < hb[3] - 0.01:
            raise SystemExit(f"LAW 39: {key} is not entirely below {host}")
        if side == "above" and kb[3] > hb[1] + 0.01:
            raise SystemExit(f"LAW 39: {key} is not entirely above {host}")
        kc, hc = (kb[0] + kb[2]) / 2, (hb[0] + hb[2]) / 2
        if abs(kc - hc) > 0.3:
            raise SystemExit(f"LAW 39: {key} is off {host}'s axis by {kc - hc:.2f}")
        if not any({key, host} <= g for g in groups):
            raise SystemExit(f"LAW 41: {key} is not blocked with {host}")
        if t < HOST_AT[host] - 1e-9:
            raise SystemExit(f"LAW 39: {key} lands before its host")
        out[key] = {"host": host, "side": side, "text": text, "at": t,
                    "box_canvas": [round(v, 1) for v in canvas(kb)]}
    # LAW 50: every object name BELOW, one size
    belows = [k for k, v in LABEL_PLAN.items() if v[1] == "below"]
    out["_law50"] = {"below": belows, "font_px": SC.KEY_FS,
                     "only_above": "key-term (the key term)"}
    du = SC.KEY_TERM_FS / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} du")
    out["_key_term"] = {"text": SC.KEY_TERM, "font_px": SC.KEY_TERM_FS,
                        "design_units": round(du, 2), "first_type": True}
    return out


def assert_lifetime_law() -> dict:
    plan = json.loads(PLAN.read_text())
    open_ended = [n for n, (_a, b) in SC.LIFETIMES.items() if b is None]
    grounds = {"o-sheet"}       # the opaque outro sheet is ground, not a mark
    for n in open_ended:
        if n not in SC.SCENE_ANCHORS and n not in grounds:
            raise SystemExit(f"LAW 42: {n} never leaves and is not an anchor")
    finite = {n: v for n, v in SC.LIFETIMES.items() if v[1] is not None}
    for n, (a, b) in finite.items():
        if b <= a:
            raise SystemExit(f"LAW 42: {n} has an empty window")
    plan_marks = {m["mark"] for m in plan["lifetimes"]}
    return {"board_mode": SC.BOARD_MODE, "anchors": sorted(SC.SCENE_ANCHORS),
            "ground": sorted(grounds), "finite": finite,
            "plan_marks": sorted(plan_marks)}


def assert_spacing_law() -> dict:
    """LAW 41 on the co-alive seats at the held instants."""
    groups = _groups()

    def alive(n, t):
        a, b = SC.LIFETIMES[n]
        if n == "hourglass" and t >= SC.CUE["shrink"]:
            return False                         # moving into the row seat
        return a <= t and (b is None or t < b)

    worst = (1e9, None)
    for t in (2.90, 3.20, 5.00, 5.60, 8.00, 12.70, 14.00, 15.40, 16.00):
        live = [n for n in RECTS if alive(n, t)]
        for i in range(len(live)):
            for j in range(i + 1, len(live)):
                a, b = live[i], live[j]
                if any({a, b} <= g for g in groups):
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
            "blocks": [sorted(g) for g in groups]}


EMPH_CHECK_AT = round(SC.CUE["emph"] + 0.34 + 0.22, 2)      # 7.60, popped
CONN_CHECK_AT = 2.60     # arrow drawn (1.62), flip done (2.12), before fade 3.30


def assert_emphasis_law() -> dict:
    """LAW 38 rule 2: the target is a DRAWN object, so the emphasis BOXES it."""
    a, b = SC.LIFETIMES["emph-hourglass"]
    if not (SC.CUE["emph"] + 0.34 <= EMPH_CHECK_AT < SC.CUE["emphout"]):
        raise SystemExit("LAW 38: the box is not complete before it leaves")
    if b > SC.BEAT_EDGES[2] + 0.30:
        raise SystemExit("LAW 38: the box outlives its beat")
    ex0, ey0, ex1, ey1 = RECTS["emph-hourglass"]
    hx0, hy0, hx1, hy1 = RECTS["hourglass"]
    air = min(hx0 - ex0, ex1 - hx1, hy0 - ey0, ey1 - hy1)
    if air - 5 / 2 < 4:
        raise SystemExit("LAW 38: the box has no clearance from the hourglass")
    return {"boxes": [{"on": "emph-hourglass", "kind": "box",
                       "target": "hourglass", "check_at": EMPH_CHECK_AT,
                       "held": [a, b], "air_core_px": air}],
            "rings_ellipses_circles": 0, "highlights": 0}


def assert_anchor_law() -> dict:
    """LAW 40: tile right-edge centre -> the hourglass's virtual rectangle
    left-edge centre at its displaced seat, level."""
    fx, fy = SC.A_SELL_FROM
    tx, ty = SC.A_SELL_TO
    hb = rect_at("hourglass", CONN_CHECK_AT)
    if abs(tx - hb[0]) > 0.01 or abs(ty - (hb[1] + hb[3]) / 2) > 0.01:
        raise SystemExit("LAW 40: the arrow does not land on the hourglass's "
                         "left-edge centre at the check instant")
    if abs(fy - ty) > 0.01:
        raise SystemExit("LAW 40: the arrow is not level")
    if not (SC.CUE["sell"] + 0.22 <= CONN_CHECK_AT < SC.CUE["ch0out"]):
        raise SystemExit("LAW 40: the check instant is not a completed state")
    return {"conn-sell": {"to": "hourglass", "side": "left", "fraction": 0.5,
                          "check_at": CONN_CHECK_AT,
                          "from_core": [fx, fy], "to_core": [tx, ty]}}


def assert_cast_law() -> dict:
    rep = DF.assert_cast_resolves(list(SC.LOGO_FILES), dict(SC.LOGO_FILES),
                                  LOGOS, label="openairesets stage marks")
    return {"stage_marks": sorted(SC.LOGO_FILES),
            "resolved": {k: v["path"] for k, v in rep.items()},
            "side_core_px": SC.MARK_SIDE,
            "cutout_lanes_not_ours": list(CUTOUT_LANES)}


def assert_draw_on(tweens: list[str], html: str) -> dict:
    """THE DRAW-ON DASH LAW: every dash-revealed selector resolves ONLY to
    elements that declare pathLength="100"."""
    sels = set()
    for t in tweens:
        if "strokeDasharray:100" in t:
            sels.update(re.findall(r'tl\.set\("([^"]+)"', t))
    checked = {}
    for sel in sels:
        if sel != "#conn-sell .cn":
            raise SystemExit(f"unexpected dash selector {sel}")
        m = re.search(r'id="conn-sell"(.*?)</svg>', html, re.S)
        tags = re.findall(r'<path[^>]*class="cn"[^>]*>', m.group(1)) if m else []
        if not tags or not all('pathLength="100"' in g for g in tags):
            raise SystemExit(f"DRAW-ON: {sel} reveals a path without "
                             'pathLength="100"')
        checked[sel] = len(tags)
    return {"dash_selectors": checked, "verdict": "every dash equals its "
            "path's declared length (100)"}


# LAW 24 (NO PEEK-AHEAD): the module shows ' / MONTH' on 'per' (5.36), 0.16 s
# before 'month' (5.52) is spoken.  The split moves it to the START of 'month',
# inside that word's own window.  Emitted tween only; the module is untouched.
KMONTH_AT = 5.52
KMONTH_OLD = ('tl.fromTo("#k200b",{opacity:0},{opacity:1,duration:0.26,'
              'ease:SOFT,immediateRender:false},5.36);')


def repair_tweens(tweens: list[str]) -> tuple[list[str], dict]:
    hits = [i for i, t in enumerate(tweens) if t == KMONTH_OLD]
    if len(hits) != 1:
        raise SystemExit("the module no longer emits the ' / MONTH' tween")
    out = list(tweens)
    out[hits[0]] = KMONTH_OLD.replace("},5.36);", f"}},{KMONTH_AT:.2f});")
    return out, {"k200b": {"from": 5.36, "to": KMONTH_AT,
                           "law": "LAW 24 no peek-ahead: MONTH waits for 'month'"}}


# THE EMPHASIS INK.  visual_laws refuses an emphasis painted in its target's
# own ink, and the hourglass's SAND is TERRA (#C4573A), the same ink as the
# module's box border.  The box is re-inked in TERRA_L, rgb(221,114,89): the
# terracotta family LAW 38 rule 2 names for emphasis flips (GRAPHIC CHART 2),
# so it is still the accent and no longer the sand.
EMPH_BORDER_OLD = f"border:5px solid {SC.TERRA};"
EMPH_BORDER_NEW = f"border:5px solid {SC.TERRA_L};"


def declare_contracts(html: str, anchors: dict) -> tuple[str, dict]:
    s = html
    key = 'id="emph-hourglass"'
    if s.count(key) != 1:
        raise SystemExit("the module no longer emits ONE emphasis box")
    i = s.index(key)
    j = s.index(">", i)
    tag = s[i:j]
    if EMPH_BORDER_OLD not in tag:
        raise SystemExit("the emphasis box no longer carries the TERRA border")
    s = s[:i] + tag.replace(EMPH_BORDER_OLD, EMPH_BORDER_NEW, 1) + s[j:]
    s = s.replace(key, f'{key} data-emphasis-target="hourglass" '
                       f'data-check-at="{EMPH_CHECK_AT:.2f}"', 1)
    for cid, a in anchors.items():
        key = f'id="{cid}"'
        if s.count(key) != 1:
            raise SystemExit(f"cannot stamp {cid}")
        s = s.replace(key, f'{key} data-anchor-side="{a["side"]}" '
                           f'data-anchor-fraction="{a["fraction"]!r}" '
                           f'data-check-at="{a["check_at"]:.2f}"', 1)
    return s, {"connectors_stamped": len(anchors), "emphases_stamped": 1,
               "emphasis_ink": f"{SC.TERRA} -> {SC.TERRA_L} (the sand is {SC.SAND})"}


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
const POP = "back.out(2.05)";
const SOFT = "power3.out";
const SWING = "power2.inOut";
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
    """The ONE raster the scene paints (handoff section 1)."""
    return {f"_{k}_img": CC.mark_img(LOGO_URL[k], k, SC.MARK_SIDE)
            for k in STAGE_FILES}


def sfx_plan() -> list[tuple]:
    """EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22)."""
    C = SC.CUE
    return [("pop", C["hg"], SFX_STRUCTURE),          # the hourglass arrives
            ("pop", C["openai"] + 0.06, SFX_DETAIL),  # the OpenAI tile
            ("whoosh", C["flip"], SFX_STRUCTURE),     # THE FLIP
            ("click", C["keyterm"], SFX_DETAIL),      # RESETS is written
            ("click", C["k200"], SFX_DETAIL),         # $200 is written
            ("pop", C["emph"], SFX_STRUCTURE),        # the box snaps on
            ("whoosh", C["shrink"], SFX_STRUCTURE),   # into the row seat
            ("pop", C["hg2"], SFX_DETAIL),            # the three pop in
            ("pop", C["hg3"], SFX_DETAIL),
            ("pop", C["hg4"], SFX_DETAIL),
            ("click", C["kacc"], SFX_DETAIL),         # 4 ACCOUNTS
            ("click", C["c1"], SFX_STRUCTURE),        # course 1
            ("click", C["c2"], SFX_STRUCTURE),        # course 2
            ("click", C["c3"], SFX_STRUCTURE),        # course 3
            ("whoosh", C["outro"], SFX_STRUCTURE)]    # the rising sheet


def assert_sfx(sfx) -> dict:
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30:
        raise SystemExit(f"SFX flam: {worst}")
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "deliberately_silent": {
                "tag 2.40": "0.22 s after the RESETS click",
                "arrow 1.40": "0.22 s after the tile pop",
                "drains": "sand falling is not an arrival",
                "KEEP BUILDING 14.60": "0.16 s before the third course"}}


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
    for n, (_h, _s, text) in LABEL_PLAN.items():
        b = canvas(rect_at(n, LABEL_AT[n] + 0.5))
        if n == "key-term":
            fs, ls = SC.KEY_TERM_FS, SC.KEY_TERM_LS
        else:
            fs, ls = SC.KEY_FS, SC.KEY_LS
        ink = len(text) * 0.6 * fs + (len(text) - 1) * ls
        rights[n] = (b[0] + b[2]) / 2 + ink / 2
    type_right = max(rights.values())
    if type_right > CAP.LAW12_RAIL_X + 0.01:
        raise SystemExit(f"readable key ink reaches x={type_right:.1f}")
    boxes = [canvas(rect_at(n, t)) for n in RECTS for t in (2.9, 12.7)]
    ink_left = min(b[0] for b in boxes)
    ink_right = max(b[2] for b in boxes)
    if ink_left < 40 or W - ink_right < 40:
        raise SystemExit("the composition leaves the 40 px frame margin")
    return {"readable_type_right_x": round(type_right, 1),
            "ink_left_x": ink_left, "ink_right_x": ink_right,
            "law30_rail_x": CAP.LAW12_RAIL_X}


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
           "law38": assert_emphasis_law(), "law2": assert_cast_law(),
           "law40": assert_anchor_law()}
    SFX = sfx_plan()
    rep["law22"] = assert_sfx(SFX)

    scene_html, tweens = SC.build(media(), outro_lockup(handle))
    tweens, rep["tween_repairs"] = repair_tweens(tweens)
    rep["draw_on"] = assert_draw_on(tweens, scene_html)
    scene_html, rep["declared"] = declare_contracts(scene_html, rep["law40"])
    if scene_html.count("data-connect-to") != 1:
        raise SystemExit("the scene does not carry its one connector")
    if (scene_html.count("data-connect-to") + scene_html.count("data-emphasis=")
            != scene_html.count("data-check-at")):
        raise SystemExit("a connector or emphasis is missing its check instant")
    for shape in ("<circle", "<ellipse"):
        if shape in scene_html:
            raise SystemExit(f"LAW 38 rule 3: {shape} in the emitted scene")
    for key, (host, _s, _t) in LABEL_PLAN.items():
        if f'id="{key}"' not in scene_html:
            raise SystemExit(f"{key} is missing from the scene")
    if not any("SWING" in t for t in tweens):
        raise SystemExit("the scene no longer uses SWING")

    m = CAP.PillMeasurer(RUN / "gen/_pillwidths_openairesets.json")
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
    rep.update({"staged": staged, "beats": beats, "seat": SEAM, "scale": CORE_K,
                "core": {"left": LEFT, "top": CORE_TOP_SPLIT}, "band": band,
                "rail": rail, "transcript": cap_rep, "phone_objects": objs,
                "render": {"w": 1080, "h": 1920, "zoom": 1}})
    return rep


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="split", choices=("split",))
    ap.parse_args()
    dst = RUN / "projects/openairesets_split"
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
    (RUN / "gen/_build_openairesets_split.json").write_text(
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
                      "phone": rep["phone_objects"]}, indent=1))


if __name__ == "__main__":
    main()
