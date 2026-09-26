#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION - grokfeatures / ICON CHOREOGRAPHY.

    YouTube   classic split 50/50   projects/grokfeatures_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/grokfeatures_scene.py` plus
`plans/grokfeatures_scene_handoff.md` are the design agent's artefacts, sealed by
`review/artwork_pass_grokfeatures.json` (production v4, `production.py seal`).
This file IMPORTS the module and SEATS it at the handoff's own placement
(k = 1.00, left 0, core top 192).  It never mutates a byte of the module.

The ONE thing it adds to the emitted scene string is the measurement contract
the geometry audit reads off the connector (`visual_laws.py`): the arrow's
`data-anchor-side`, `data-anchor-fraction` and `data-check-at`, and the
`data-connector-head` marker on its arrowhead so the measured endpoint is the
painted tip.  Each insertion is an exact, asserted single replacement of an
attribute list; no geometry, colour or timing changes.  (Logged in
`plans/grokfeatures_split_notes.md`.)

HD DELIVERY: authored AND encoded 1080x1920.  The face plate is
`face_bottom_hd.mp4` (1080x1058), so the seam is 1920 - 1057.5 = 862.5 and the
RENDERING pill top is 862.5 - 114.59/2 = 805.205 (the pill that renders, never
the frozen 108.2 seat constant).  The core's content band 88..534 lands at
canvas 280..726: 88 px under LAW 30's top-10 % line and ~79 px over the pill.

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
import pointing_cues as PCUE                    # noqa: E402
import cutout_core as CC                        # noqa: E402
from cutout_depthfield import assert_cast_resolves  # noqa: E402
import grokfeatures_scene as SC                 # noqa: E402

RUN = Path(__file__).resolve().parents[1]
CUT = RUN / "cuts/grokfeatures"
PLAN = RUN / "plans/grokfeatures_plan.json"
WS = Path.home() / "Documents/Workspace"
ASSETS = WS / "assets"
LOGOS = ASSETS / "logos"
LIB_MUSIC = ASSETS / "audio/music/shorts-factory"
LIB_SFX = ASSETS / "audio/sfx/shorts-factory"

VID = "grokfeatures"
W, H = 1080.0, 1920.0
FPS = 25
DUR = SC.DUR                                     # 34.77, the cut master

SEAM = 862.5
CORE_TOP_SPLIT = SC.CANVAS_OFFSET                # 192.0, the handoff's number
CORE_K = 1.00
LEFT = (W - SC.CORE_W * CORE_K) / 2              # 0.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "Grok is quietly a top AI contender"
LABEL_WINDOW = 1.0

# the connector is complete (line drawn 13.56 + 0.24, head 13.76 + 0.10) and the
# tile, page and label are all still up (they leave 14.70)
ARROW_CHECK_AT = 14.20

# ------------------------------------------------------------------ printed keys
PRINTED_KEYS = {"key-top3": "TOP 3", "key-models": "MODELS", "key-apps": "+ APPS",
                "key-24": "24 FEATURES", "key-gbuild": "GROK BUILD",
                "key-dash": "AGENT DASHBOARD", "key-modal": "MULTI-MODAL",
                "key-agent": "MULTI-AGENT", "key-deep": "DEEP RESEARCH"}
LABEL_FOR = {"key-top3": ("podium", "above"), "key-models": ("podium", "below"),
             "key-apps": ("podium", "below"), "key-24": ("cal", "below"),
             "key-gbuild": ("t-gbuild", "below"),
             "key-dash": ("ic-dash", "below"), "key-modal": ("ic-modal", "below"),
             "key-agent": ("ic-agent", "below"), "key-deep": ("ic-deep", "below")}
SINGLE_LINE_ROW = ("key-models", "key-apps", "key-24", "key-gbuild")
FEATURE_ROW = ("key-dash", "key-modal", "key-agent", "key-deep")

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.
CUE_WORDS = {
    "podium": (0, "a"), "grok": (8, "grok"), "models": (25, "model"),
    "apps": (30, "application"), "cal": (32, "in"), "ticks": (38, "shipped"),
    "key24": (40, "24"), "slide": (45, "grok"), "arrow": (46, "build"),
    "box": (48, "now,"), "dash": (55, "agent"), "modal": (57, "multi-modal"),
    "agent": (59, "multi-agent"), "deep": (61, "deep"), "boxflip": (66, "name"),
    "close": (69, "now,"), "spacex": (74, "spacex"), "drops": (77, "shipping"),
    "outro": (88, "now,"),
}
# AUTHORED instants: each inside its own word's 1.0 s LABEL_WINDOW.
CUE_INSIDE = {"chatgpt": (1, "lot"), "gemini": (1, "lot"), "hop": (10, "slowly"),
              "top3": (16, "three"), "grokflip": (16, "three"),
              "nums": (16, "three"), "grokback": (17, "contenders"),
              "c1out": (31, "side."), "gbuild": (45, "grok"),
              "keygb": (46, "build"), "c2out": (47, "application."),
              "boxback": (66, "name"), "c3out": (68, "few."),
              "topile": (75, "ai")}
NOT_INSTANTS = ("tick_step", "drop_step", "key_lag")


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
    opening = "a lot of people don't know this, but grok is"
    head = " ".join(w["text"] for w in ws[:10]).lower()
    if head != opening:
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[10:]).lower()
    if "a lot of people don't know" in later:
        raise SystemExit("LAW 46: the opening repeats inside the take")
    tail = DUR - float(ws[-1]["end"])
    cap = 0.20 + 1.0 / FPS
    if tail > 0.30:
        raise SystemExit(f"LAW 47: the master runs {tail:.3f}s past the last word")
    edl = json.loads((CUT / "edl.json").read_text())
    td = edl["take_detection"]
    if not td.get("keep_words"):
        raise SystemExit("the cut carries no model keep_words")
    rep = {"law47_tail_s": round(tail, 3), "law47_cap_s": round(cap, 3),
           "law47_verdict": ("PASS" if tail <= cap else "REPORTED")
           + f" - {tail:.3f}s past the last word against a {cap:.3f}s cap",
           "law46": "the scripted opening occurs ONCE inside the keeper take, "
                    "at word 0 / 0.10 s",
           "take_corroboration": {
               "mode": td.get("mode"), "keep_words": td.get("keep_words"),
               "take_word_index": td.get("take_word_index"),
               "take_start_s": td.get("take_start_s"),
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
                             f"{text!r} - the cut moved")
        got = round(float(w["start"]), 3)
        if not (got - 0.011 <= SC.CUE[name] <= float(w["end"])):
            raise SystemExit(f"cue {name}: the scene fires at {SC.CUE[name]}, "
                             f"the word spans {got}-{w['end']}")
        rep[name] = {"word": idx, "text": w["text"], "t": SC.CUE[name],
                     "word_start": got}
    for name, (idx, text) in CUE_INSIDE.items():
        w = ws[idx]
        if w["text"].strip().lower() != text:
            raise SystemExit(f"cue {name}: word {idx} is {w['text']!r}")
        t = SC.CUE[name]
        lo, hi = float(w["start"]), float(w["end"]) + LABEL_WINDOW
        if not (lo <= t <= hi):
            raise SystemExit(f"cue {name} at {t} is outside the window of "
                             f"{w['text']!r} ({lo:.3f}-{hi:.3f})")
        rep[name] = {"word": idx, "text": w["text"], "t": t,
                     "window": [round(lo, 3), round(hi, 3)]}
    missing = set(SC.CUE) - set(rep) - set(NOT_INSTANTS)
    if missing:
        raise SystemExit(f"cues the build never verified: {sorted(missing)}")
    if SC.BOARD_MODE != "chapters" or len(SC.BOARD_CHAPTERS) != 4:
        raise SystemExit("the scene is no longer the four chapters the plan "
                         "declared")
    edges = [c["erase_at"] for c in SC.BOARD_CHAPTERS]
    if edges != [SC.CUE["c1out"], SC.CUE["c2out"], SC.CUE["c3out"],
                 SC.CUE["outro"]]:
        raise SystemExit(f"LAW 43: chapter erases {edges} are off their marks")
    # LAW 45: each seam lands on an idea.  Seams 1 and 2: the next chapter's
    # object is complete within 0.30 s of its start (calendar 8.44 + 0.34,
    # box 14.84 + 0.30).  Seam 3: the box itself carries it (it never leaves).
    if SC.LIFETIMES["box"][0] > SC.CUE["c3out"] or \
            SC.LIFETIMES["box"][1] < SC.CUE["outro"]:
        raise SystemExit("LAW 45: the box no longer carries seam 3")
    rep["_law43_45"] = {"board_mode": SC.BOARD_MODE, "chapters": 4,
                        "erase_at": edges,
                        "handover_idea": {
                            "seam1": "the calendar page draws 8.44, complete "
                                     "by ~8.85",
                            "seam2": "the open box draws 14.84, complete by "
                                     "~15.15",
                            "seam3": "the box closes and carries the seam into "
                                     "the pile (never leaves)"}}
    return rep


# every typed key and the spoken words it must agree with:
#   key: (cue name, (i0, i1) the words it lands on, spoken text)
WORD_SYNC = {
    "key-top3": ("top3", (15, 16), "top three"),
    "key-models": ("models", (25, 25), "model"),
    "key-apps": ("apps", (30, 30), "application"),
    "key-24": ("key24", (40, 42), "24 major features"),
    "key-gbuild": ("keygb", (45, 46), "grok build"),
    "key-dash": ("dash", (55, 56), "agent dashboard,"),
    "key-modal": ("modal", (57, 57), "multi-modal"),
    "key-agent": ("agent", (59, 59), "multi-agent"),
    "key-deep": ("deep", (61, 62), "deep research"),
}


def key_first_visible(key: str) -> float:
    """The instant the key's own tween starts (the lifetime start)."""
    return SC.LIFETIMES[key][0]


def assert_word_sync(ws: list[dict]) -> dict:
    """WORD-SYNC: every typed key first shows the value its words say, while
    or just after they are said.  The one number (24) and the one digit (3)
    both land on the word that says them."""
    rows = []
    for key, (cue, (i0, i1), spoken) in WORD_SYNC.items():
        got = " ".join(w["text"] for w in ws[i0:i1 + 1]).lower()
        if got != spoken:
            raise SystemExit(f"word-sync: {key} expects {spoken!r}, the take "
                             f"says {got!r}")
        t = key_first_visible(key)
        lo = float(ws[i0]["start"]) - 0.011
        hi = float(ws[i1]["end"]) + LABEL_WINDOW
        if not (lo <= t <= hi):
            raise SystemExit(f"word-sync: {key} first shows at {t}, outside "
                             f"{lo:.3f}-{hi:.3f}")
        rows.append({"state": key, "first_visible_text": PRINTED_KEYS[key],
                     "at": round(t, 2), "words": got,
                     "window": [round(lo, 3), round(hi, 3)]})
    # "24" spoken 10.90-11.58: the ticks number 24 and the 24th completes at
    # 10.86 + 0.12, the label types at 10.92.  No counter ticks.
    ticks = sum(1 for d in range(1, SC.MONTH_DAYS + 1) if d not in SC.UNTICKED)
    last_tick_done = SC.CUE["ticks"] + (ticks - 1) * SC.CUE["tick_step"] + 0.12
    if ticks != 24 or not (ws[40]["start"] - 0.2 <= last_tick_done
                           <= ws[40]["end"]):
        raise SystemExit(f"word-sync: {ticks} ticks done at {last_tick_done}")
    if SC.KEY_TERM != "TOP 3" or SC.CUE["top3"] != min(
            key_first_visible(k) for k in PRINTED_KEYS):
        raise SystemExit("LAW 9: TOP 3 is not the first type on the board")
    return {"typed_states": rows, "disagreements": 0, "digits_that_tick": 0,
            "ticks": {"count": ticks, "last_done_at": round(last_tick_done, 3),
                      "word_24": [ws[40]["start"], ws[40]["end"]]},
            "numerals": {"1 2 3 on the steps": SC.CUE["nums"],
                         "after": "three (3.24-3.44)"}}


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
            "source_cards_in_the_page": 0}


# ------------------------------------------------------------------ laws
def _label_box(scene_html: str, key: str) -> tuple:
    m = re.search(rf'<div class="abs mono" id="{key}" style="([^"]*)"'
                  rf'([^>]*)>(.*?)</div>', scene_html)
    if not m:
        raise SystemExit(f"LAW 39: #{key} missing")
    st = dict(p.split(":", 1) for p in m.group(1).split(";") if ":" in p)
    px = {k: float(st[k].rstrip("px")) for k in ("left", "top", "width",
                                                 "height", "font-size")}
    return px, m.group(2), m.group(3)


def assert_label_law(scene_html: str) -> dict:
    """LAW 39 / 50: a name sits ABOVE (the key term) or BELOW its object, a
    sibling row shares one baseline and one size."""
    out = {}
    tops = {
        "podium": min(SC.T_CHATGPT[1], SC.T_GEMINI[1], SC.T_GROK[1]),
        "cal": SC.CAL_RING[2]}
    bottoms = {"podium": SC.FLOOR[2] + SC.FLOOR_SW / 2,
               "cal": SC.CAL[1] + SC.CAL[3] + SC.CAL_SW / 2,
               "t-gbuild": SC.T_GBUILD[1] + SC.TILE,
               **{f"ic-{k}": SC.ICON_Y + SC.ICON for k, _ in SC.FEATURES}}
    for key, (host, side) in LABEL_FOR.items():
        px, attrs, text = _label_box(scene_html, key)
        if f'data-label-for="{host}"' not in attrs:
            raise SystemExit(f"LAW 39: #{key} does not name {host}")
        shown = ihtml.unescape(text.replace("<br>", "")).upper()
        if shown.replace("-", "") != PRINTED_KEYS[key].replace(" ", "").replace(
                "-", "") and shown != PRINTED_KEYS[key]:
            if shown.replace(" ", "") != PRINTED_KEYS[key].replace(" ", ""):
                raise SystemExit(f"LAW 39: #{key} prints {shown!r}")
        if side == "above":
            gap = tops[host] - (px["top"] + px["height"])
        else:
            gap = px["top"] - bottoms[host]
        if gap < 16:
            raise SystemExit(f"LAW 39/41: #{key} sits {gap:.1f}px from {host}")
        if not any(key in b and (host in b or host == "podium" and "podium" in b)
                   for b in SC.DECLARED_BLOCKS):
            raise SystemExit(f"LAW 28/41: {key} is not blocked with {host}")
        out[key] = {"for": host, "place": side, "gap_px": round(gap, 1),
                    "font_px": px["font-size"], "top": px["top"]}
    for row in (SINGLE_LINE_ROW, FEATURE_ROW):
        tops_ = {out[k]["top"] for k in row}
        sizes = {out[k]["font_px"] for k in row}
        if len(tops_) != 1 or len(sizes) != 1:
            raise SystemExit(f"LAW 50: {row} differ in top {tops_} / size "
                             f"{sizes}")
    du = SC.KEY_TERM_FS / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} du")
    out["_law50"] = {"single_line_row_top": out[SINGLE_LINE_ROW[0]]["top"],
                     "feature_row_top": out[FEATURE_ROW[0]]["top"]}
    out["_key_term"] = {"text": SC.KEY_TERM, "font_px": SC.KEY_TERM_FS,
                        "design_units": round(du, 2), "first_type": True}
    return out


COVERS = ("o-sheet",)
# THE BOX CARRIES SEAM 3 (LAW 45's second remedy, plan lifetimes row 4): the
# open box of chapter 3 IS the first parcel of the pile in chapter 4.  It is the
# referent in both beats and leaves under the outro sheet.
CARRIERS = {"box": "open box (14.84-24.56) -> first parcel of the pile "
                   "(24.56-29.80), leaves under the sheet 30.28"}


def assert_lifetime_law() -> dict:
    shares = {}
    for n, (a, b) in SC.LIFETIMES.items():
        if b is None:
            if n not in SC.SCENE_ANCHORS and n not in COVERS:
                raise SystemExit(f"LAW 42: {n} never leaves and is not an anchor")
            continue
        shares[n] = round((b - a) / DUR, 3)
        if shares[n] > 0.40 and n not in CARRIERS:
            raise SystemExit(f"LAW 42: {n} is on screen {shares[n]:.0%}")
    return {"board_mode": SC.BOARD_MODE, "anchors": list(SC.SCENE_ANCHORS),
            "covers": list(COVERS), "carriers": CARRIERS,
            "longest_non_carrier_share": max(v for k, v in shares.items()
                                             if k not in CARRIERS),
            "mark_shares": shares}


def assert_emphasis_connector(scene_html: str) -> dict:
    """LAW 38 / LAW 40.  Two border flips of drawn objects, no ring; one
    connector whose ends sit on the page edge and the tile's left anchor."""
    for shape in ("<circle", "<ellipse", 'data-emphasis="ring"'):
        if shape in scene_html:
            raise SystemExit(f"LAW 38: {shape} in the emitted scene")
    if len(SC.CONNECTORS) != 1 or scene_html.count("data-connect-to=") != 1:
        raise SystemExit("LAW 40: the scene declares other than one connector")
    anchor = SC.assert_anchor_law()
    return {"connectors": 1, "arrow": anchor["arrow"],
            "emphasis": {"t-grok": "border flip to rgb(221,114,89) 3.30-4.84",
                         "#box .bxo": "outline flip 23.28-24.22"},
            "rings_ellipses_circles": 0}


def declare_connector(scene_html: str) -> tuple[str, dict]:
    """The measurement contract visual_laws.py reads (see module docstring).
    Exact single replacements; anything else is a refusal."""
    old_div = ('data-connect-to="t-gbuild" data-connect-from="cal" '
               'data-overlap-ok')
    new_div = (f'data-connect-to="t-gbuild" data-connect-from="cal" '
               f'data-anchor-side="left" data-anchor-fraction="0.5" '
               f'data-check-at="{ARROW_CHECK_AT}" data-overlap-ok')
    old_head = '<path class="ah" d='
    new_head = '<path class="ah" data-connector-head d='
    for old in (old_div, old_head):
        if scene_html.count(old) != 1:
            raise SystemExit(f"connector declaration: {old!r} found "
                             f"{scene_html.count(old)} times")
    out = scene_html.replace(old_div, new_div).replace(old_head, new_head)
    return out, {"arrow-cal": {"data-anchor-side": "left",
                               "data-anchor-fraction": 0.5,
                               "data-check-at": ARROW_CHECK_AT,
                               "head": "data-connector-head on path.ah"}}


def _tags_for(sel: str, html: str) -> list[str]:
    parts = sel.split()
    if not parts[0].startswith("#"):
        raise SystemExit(f"unexpected dash selector {sel}")
    hid = parts[0][1:]
    if len(parts) == 1:
        return re.findall(rf'<(?:path|polyline|polygon|line|rect)\b[^>]*'
                          rf'id="{re.escape(hid)}"[^>]*>', html)
    if len(parts) != 2:
        raise SystemExit(f"unexpected dash selector {sel}")
    want = [c for c in parts[1].split(".") if c]
    m = re.search(rf'id="{re.escape(hid)}"(.*?)</svg>', html, re.S)
    if not m:
        return []
    out = []
    for tag in re.findall(r'<(?:path|polyline|polygon|line|rect)\b[^>]*>',
                          m.group(1)):
        cm = re.search(r'class="([^"]*)"', tag)
        if cm and all(c in cm.group(1).split() for c in want):
            out.append(tag)
    return out


def assert_draw_on(tweens: list[str], html: str) -> dict:
    """THE DRAW-ON DASH LAW: every selector revealed with a 100-unit dash
    resolves ONLY to elements that declare pathLength="100"."""
    sels = set()
    for t in tweens:
        if "strokeDasharray:100" in t:
            for s in re.findall(r'tl\.set\("([^"]+)"', t):
                sels.update(p.strip() for p in s.split(","))
    checked = {}
    for sel in sorted(sels):
        tags = _tags_for(sel, html)
        if not tags or not all('pathLength="100"' in g for g in tags):
            raise SystemExit(f"DRAW-ON: {sel} reveals a path without "
                             'pathLength="100"')
        checked[sel] = len(tags)
    return {"dash_selectors": checked, "verdict": "every dash equals its "
            "path's declared length (100)"}


# ------------------------------------------------------------------ captions
# "features | to their Grok Build application." is one sentence across a
# 0.36 s breath: grouped apart, the DP can only strand "to their" (a two-word
# function-only beat) or split the product name.  Joined, it reads
# "24 major features to their" | "Grok Build application."
NO_PHRASE_BREAK_BEFORE = {12.70}


def phrases(ws: list[dict]) -> list[list[dict]]:
    out, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w)
        end = w["text"].strip().rstrip('"').endswith((".", "!", "?"))
        gap = (ws[i + 1]["start"] - w["end"]) if i + 1 < len(ws) else 9.0
        if i + 1 < len(ws) and round(float(ws[i + 1]["start"]), 2) in \
                NO_PHRASE_BREAK_BEFORE and not end:
            continue
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
# A PRODUCT NAME IS ONE READ: never break a pill between "Grok" and "Build"
# (words 45/46).  Keyed by word start time so it survives any regrouping.
NO_BREAK_AFTER = {13.06}


def _breaks_name(union, j) -> bool:
    return 0 < j < len(union) and round(float(union[j - 1]["start"]), 2) \
        in NO_BREAK_AFTER


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
            if _breaks_name(union, j):
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
            k0, k1 = SC.LIFETIMES[key]
            if b["start"] < k1 and k0 < b["start"] + b["dur"]:
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
.clip {{ position:absolute; }} .abs {{ position:absolute; box-sizing:border-box; }}
.mono {{ font-family:'JetBrains Mono',monospace; text-transform:uppercase; }}
.core {{ transform-origin:0 0; }}
{CAP.pill_rule()}
{extra_css}
</style></head>
<body><div id="root" data-composition-id="main" data-start="0"
 data-width="1080" data-height="1920" data-duration="{DUR}" data-fps="{FPS}">
"""


def tail(tweens: list[str]) -> str:
    # the scene's eases are string literals (handoff section 1)
    return f"""
</div>
<script>
window.__timelines = window.__timelines || {{}};
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
SFX_FILES = ("pop", "click", "low_thump")


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
    for s in SFX_FILES:
        src = LIB_SFX / f"{s}.mp3"
        if not src.exists():
            raise SystemExit(f"the {s} sfx does not resolve: {src}")
        shutil.copy2(src, dst / f"assets/sfx/{s}.mp3")
        rec["sfx_sources"][s] = str(src)
    shutil.copy2(CUT / face, v / face)
    rec["face"] = {"file": face, **probe_wh(CUT / face)}
    # MARK IDENTITY: the four registry files the handoff names, never guessed
    cast = assert_cast_resolves(list(SC.LOGO_FILES), dict(SC.LOGO_FILES), LOGOS,
                                label="grokfeatures stage marks")
    rec["marks"] = {}
    for key, rel in SC.LOGO_FILES.items():
        src = LOGOS / rel
        if not src.exists():
            raise SystemExit(f"missing registry mark: {src}")
        shutil.copy2(src, dst / f"assets/logos/{src.name}")
        CC.MARK_INK[key] = CC.measure_mark(key, src)
        rec["marks"][key] = {"path": str(src),
                             "aspect": round(CC.MARK_INK[key]["aspect"], 3),
                             "resolved": cast[key]["path"]}
    return rec


def scene_media() -> dict:
    return {mkey: CC.mark_img(f"assets/logos/{Path(SC.LOGO_FILES[k]).name}",
                              k, side)
            for mkey, (k, side) in SC.MEDIA_SIDES.items()}


def sfx_plan() -> list[tuple]:
    """EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22)."""
    C = SC.CUE
    return [("pop", C["podium"], SFX_STRUCTURE),       # the podium draws
            ("pop", C["chatgpt"], SFX_DETAIL),         # ChatGPT lands on 1
            ("pop", C["grok"], SFX_DETAIL),            # Grok lands on the floor
            ("low_thump", C["hop"] + 0.66, SFX_DETAIL),  # the hop lands on 3
            ("click", C["top3"], SFX_DETAIL),          # TOP 3 is typed
            ("pop", C["nums"] + 0.10, SFX_DETAIL),     # the step numerals
            ("click", C["models"], SFX_DETAIL),        # MODELS
            ("click", C["apps"] + 0.08, SFX_DETAIL),   # + APPS
            ("pop", C["cal"], SFX_STRUCTURE),          # the calendar draws
            ("click", C["ticks"], SFX_DETAIL),         # the ticks start
            ("click", C["key24"] + 0.36, SFX_DETAIL),  # 24 FEATURES settles
            ("pop", C["gbuild"], SFX_DETAIL),          # the Grok Build tile
            ("low_thump", C["arrow"] + 0.24, SFX_DETAIL),  # arrow tip lands
            ("pop", C["box"], SFX_STRUCTURE),          # the open box draws
            ("pop", C["dash"], SFX_DETAIL),            # icon rises
            ("pop", C["modal"], SFX_DETAIL),           # icon rises
            ("pop", C["agent"], SFX_DETAIL),           # icon rises
            ("pop", C["deep"], SFX_DETAIL),            # icon rises
            ("click", C["boxflip"], SFX_DETAIL),       # the box flips terracotta
            ("low_thump", C["close"] + 0.10, SFX_DETAIL),  # the lid closes
            ("pop", C["spacex"], SFX_DETAIL),          # the SpaceX plate
            ("pop", C["drops"], SFX_DETAIL),           # first parcel lands
            ("pop", C["drops"] + 4 * C["drop_step"], SFX_DETAIL),
            ("pop", C["drops"] + 8 * C["drop_step"], SFX_DETAIL),
            ("pop", SC.CHIP_IN, SFX_DETAIL)]           # the outro glyph


def assert_sfx(sfx) -> dict:
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30:
        raise SystemExit(f"SFX flam: {worst}")
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "deliberately_silent": {
                "gemini 0.62": "0.22 s after ChatGPT's pop; one arrival sound",
                "grok flip 3.30": "0.04 s after TOP 3's click",
                "tick run 9.96-10.98": "one click scores the run, not 24",
                "slide 13.06": "a slide is a move, not an arrival",
                "parcel drops": "one pop every fourth parcel (0.26 s steps "
                                "would flam)",
                "chapter exits / sheet 29.80": "exits stay silent; the glyph "
                                               "pop at 30.30 scores the outro"}}


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
def canvas(box):
    """core px -> the canvas this page actually paints (top 192, k 1.00)."""
    return (CORE_K * box[0] + LEFT, CORE_TOP_SPLIT + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP_SPLIT + CORE_K * box[3])


def guard_core_band(top: float, k: float, cap_seat: float,
                    pill_clear: float = 24.0) -> dict:
    y0 = top + SC.CONTENT_Y0 * k
    y1 = top + SC.CONTENT_Y1 * k
    pill_top = cap_seat - CAP.CAP_PILL_HEIGHT / 2
    if y0 < 0.10 * H:
        raise SystemExit(f"core content starts at y={y0:.1f} - LAW 30")
    if y1 > pill_top - pill_clear:
        raise SystemExit(f"core content ends at y={y1:.1f}, within {pill_clear}"
                         f"px of the pill top {pill_top:.1f}")
    return {"content_top": y0, "content_bottom": y1,
            "pill_top_rendered": round(pill_top, 3),
            "clear_above_pill": round(pill_top - y1, 2),
            "clear_below_law30": round(y0 - 0.10 * H, 2)}


def guard_rail(scene_html: str) -> dict:
    """LAW 30: readable type stays out of the right rail (x > 918 between
    30 % and 95 % of the height).  The rightmost labels (DEEP RESEARCH) sit
    at canvas y 428..480, above the 576 line; the amendment keeps the
    composition centred."""
    rail_y0, rail_y1 = 0.30 * H, 0.95 * H
    rows = {}
    for key in PRINTED_KEYS:
        px, _a, text = _label_box(scene_html, key)
        lines = ihtml.unescape(text).split("<br>")
        ls = SC.KEY_TERM_LS if key == "key-top3" else (
            SC.FKEY_LS if key in FEATURE_ROW else SC.KEY_LS)
        ink = max(len(s) * 0.6 * px["font-size"] + (len(s) - 1) * ls
                  for s in lines)
        cx = LEFT + px["left"] + px["width"] / 2
        dx = SC.MODELS_DX if key == "key-models" else (
            SC.CAL_DX if key == "key-24" else 0.0)
        right = max(cx + ink / 2, cx + dx + ink / 2)
        y0 = CORE_TOP_SPLIT + px["top"]
        y1 = y0 + px["height"]
        in_band = y1 > rail_y0 and y0 < rail_y1
        if in_band and right > CAP.LAW12_RAIL_X + 0.01:
            raise SystemExit(f"LAW 30: {key} reaches x={right:.1f} inside the "
                             "rail band")
        rows[key] = {"ink_right_x": round(right, 1), "y": [y0, y1],
                     "in_rail_band": in_band}
    boxes = [canvas(o["core"]) for o in SC.BESPOKE + SC.UI_OBJECTS]
    ink_left = min(b[0] for b in boxes)
    ink_right = max(b[2] for b in boxes)
    if ink_left < 30 or W - ink_right < 30:
        raise SystemExit("the composition leaves the frame margin")
    if abs((ink_left + ink_right) / 2 - W / 2) > 0.5:
        raise SystemExit("LAW 30 amendment: the composition is not centred")
    return {"labels": rows, "ink_left_x": ink_left, "ink_right_x": ink_right,
            "law30_rail_x": CAP.LAW12_RAIL_X,
            "rail_band_y": [rail_y0, rail_y1]}


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
    lifetimes = assert_lifetime_law()
    SFX = sfx_plan()
    sfx_guard = assert_sfx(SFX)

    scene_html, tweens = SC.build(scene_media(), outro_lockup(handle))
    drawon = assert_draw_on(tweens, scene_html)
    labels = assert_label_law(scene_html)
    law38_40 = assert_emphasis_connector(scene_html)
    scene_html, declared = declare_connector(scene_html)
    law38_40["declared"] = declared

    m = CAP.PillMeasurer(RUN / f"gen/_pillwidths_{VID}.json")
    beats, cap_rep = caption_beats(m, ws, clean_rep)
    CAP.assert_law12(SEAM, max(b["w"] for b in beats))
    band = guard_core_band(CORE_TOP_SPLIT, CORE_K, SEAM)
    rail = guard_rail(scene_html)
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
            "law39_50": labels, "law42": lifetimes, "law38_40": law38_40,
            "law22": sfx_guard, "draw_on": drawon, "transcript": cap_rep,
            "phone_objects": objs, "render": {"w": 1080, "h": 1920, "zoom": 1}}


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
                       "beats": [[b["text"], round(b["start"], 2)]
                                 for b in rep["beats"]],
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
                      "law22": rep["law22"]["tightest_gap_s"],
                      "law42": rep["law42"]["longest_non_carrier_share"],
                      "phone": rep["phone_objects"]}, indent=1))


if __name__ == "__main__":
    main()
