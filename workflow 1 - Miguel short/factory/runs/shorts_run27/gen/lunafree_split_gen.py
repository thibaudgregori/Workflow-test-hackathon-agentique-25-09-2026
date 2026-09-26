#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION - lunafree / ICON CHOREOGRAPHY.

    YouTube   classic split 50/50   projects/lunafree_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/lunafree_scene.py` plus
`plans/lunafree_scene_handoff.md` are the design agent's artefacts, sealed by
`review/artwork_pass_lunafree.json` (production v4, `production.py seal`).
This file IMPORTS the module and SEATS it at the handoff's own placement
(k = 1.00, left 0, core top 192).  It never mutates a byte of the module.

The one thing this page adds to the scene's emitted string is the connector's
measurement declaration (`data-anchor-side="left"` + `data-check-at`) on
`#conn-app`, which the module stamps with `data-connect-to` only; the geometry
is untouched (production visual_laws contract).

HD DELIVERY: authored AND encoded 1080x1920.  The face plate is
`face_bottom_hd.mp4` (1080x1058), so the seam is 1920 - 1057.5 = 862.5 and the
RENDERING pill top is 862.5 - 114.59/2 = 805.205 (the pill that renders, never
the frozen 108.2 seat constant).  The core's content band 64..506 lands at
canvas 256..698: 64 px under LAW 30's top-10 % line and ~107 px over the pill.

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
import lunafree_scene as SC                     # noqa: E402

RUN = Path(__file__).resolve().parents[1]
CUT = RUN / "cuts/lunafree"
PLAN = RUN / "plans/lunafree_plan.json"
ASSETS = Path.home() / "Documents/Workspace/assets"
LOGOS = ASSETS / "logos"
LIB_MUSIC = ASSETS / "audio/music/shorts-factory"
LIB_SFX = ASSETS / "audio/sfx/shorts-factory"

VID = "lunafree"
W, H = 1080.0, 1920.0
FPS = 25
DUR = SC.DUR                                     # 21.12, the cut master

SEAM = 862.5
CORE_TOP_SPLIT = SC.CANVAS_OFFSET                # 192.0, the handoff's number
CORE_K = 1.00
LEFT = (W - SC.CORE_W * CORE_K) / 2              # 0.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "GPT Luna is free in ChatGPT"
LABEL_WINDOW = 1.0
CONN_CHECK_AT = 5.40                             # arrow complete (5.02), tile held

# ------------------------------------------------------------------ marks
STAGE_FILES = {k: f"logos/{v}" for k, v in SC.LOGO_FILES.items()}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}
CUTOUT_LANES = SC.CUTOUT_LOGO_LANES


def _xywh(b) -> tuple:
    x, y, w, h = b
    return (x, y, x + w, y + h)


# Seats in CORE px (x0, y0, x1, y1), at the instant each label lands
RECTS: dict[str, tuple] = {
    "gift": SC.GIFT_BOX,
    "key-term": _xywh(SC.KEY_TERM_BOX),
    "key-users": _xywh(SC.KUSERS_BOX),
    "chatgpt-tile": SC.CHATGPT_BOX,
    "key-chatgpt": _xywh(SC.KCHAT_BOX),
    "amp": SC.AMP_BOX,
    "key-reason": _xywh(SC.KREASON_BOX),
    "piggy": SC.PIGGY_BOX,
    "key-budget": _xywh(SC.KBUDGET_BOX),
    "board": SC.BOARD_BOX,
    "key-arsenal": _xywh(SC.KARSENAL_BOX),
}


def canvas(box):
    """core px -> the canvas this page actually paints (top 192, k 1.00)."""
    return (CORE_K * box[0] + LEFT, CORE_TOP_SPLIT + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP_SPLIT + CORE_K * box[3])


# --------------------------------------------------------------- label plan
# LAW 39 / LAW 9 / LAW 50 (plan.labels): GPT LUNA above, the rest below.
LABEL_PLAN = {"key-term": ("gift", "above", SC.KEY_TERM),
              "key-users": ("gift", "below", SC.KEY_USERS),
              "key-chatgpt": ("chatgpt-tile", "below", "CHATGPT"),
              "key-reason": ("amp", "below", "REASONING"),
              "key-budget": ("piggy", "below", "BUDGET"),
              "key-arsenal": ("board", "below", "ARSENAL")}
LABEL_AT = {"key-term": SC.CUE["keyterm"], "key-users": SC.CUE["kfree"],
            "key-chatgpt": SC.CUE["kchat"], "key-reason": SC.CUE["kreason"],
            "key-budget": SC.CUE["kbudget"], "key-arsenal": SC.CUE["karsenal"]}
HOST_AT = {"gift": SC.CUE["gift"], "chatgpt-tile": SC.CUE["chatgpt"],
           "amp": SC.CUE["amp"], "piggy": SC.CUE["piggy"],
           "board": SC.CUE["board"]}
PRINTED_KEYS = {k: v[2] for k, v in LABEL_PLAN.items()}
PRINTED_KEYS["amp-max"] = "MAX"
PRINTED_LIFETIME = {k: SC.LIFETIMES[k] for k in LABEL_PLAN}
PRINTED_LIFETIME["amp-max"] = SC.LIFETIMES["amp"]

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.
CUE_WORDS = {
    "gift": (0, "gpt"), "keyterm": (2, "is"), "open": (5, "free"),
    "kfree": (7, "free"), "kgo": (9, "go"), "kusers": (10, "users"),
    "shift": (13, "chatgpt"), "amp": (15, "this"), "mighty": (20, "mighty"),
    "turn1": (23, "turn"), "kreason": (26, "reasoning"),
    "turn2": (26, "reasoning"), "turn3": (27, "all"), "turn4": (29, "way"),
    "max": (32, "max."), "piggy": (34, "if"), "coin": (38, "budget,"),
    "slide": (39, "this"), "tile": (41, "one"), "best": (44, "best"),
    "tools": (45, "tools"), "karsenal": (52, "arsenal."), "outro": (53, "now"),
}
# AUTHORED instants: each inside its own word's 1.0 s LABEL_WINDOW
CUE_INSIDE = {"rise": (5, "free"), "chatgpt": (13, "chatgpt"),
              "conn": (13, "chatgpt"), "kchat": (13, "chatgpt"),
              "kbudget": (38, "budget,"), "board": (39, "this")}
# chapter erases and the flip's return, placed after their words by design
CUE_FREE = ("ch0out", "ch1out", "bestout")


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
    opening = "gpt luna is now 100% free for free and go users"
    head = " ".join(w["text"] for w in ws[:11]).lower()
    if head != opening:
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[11:]).lower()
    if "gpt luna" in later or "100% free" in later:
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
                    "at word 0 / 0.12 s",
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
        # ON the word: at its start (10 ms) or inside its spoken span
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
    missing = set(SC.CUE) - set(rep) - set(CUE_FREE)
    if missing:
        raise SystemExit(f"cues the build never verified: {sorted(missing)}")
    if SC.BOARD_MODE != "chapters" or len(SC.BOARD_CHAPTERS) != 3:
        raise SystemExit("the scene is no longer the three chapters the plan "
                         "declared")
    edges = [c["erase_at"] for c in SC.BOARD_CHAPTERS]
    if edges != [SC.CUE["ch0out"], SC.CUE["ch1out"], SC.CUE["outro"]]:
        raise SystemExit(f"LAW 43: chapter erases {edges} are off their marks")
    # LAW 45: the next chapter's object lands within 0.30 s of the erase
    for e, nxt in ((SC.CUE["ch0out"], SC.CUE["amp"]),
                   (SC.CUE["ch1out"], SC.CUE["piggy"])):
        if nxt - e > 0.30:
            raise SystemExit(f"LAW 45: {nxt - e:.2f}s empty board after {e}")
    rep["_law43"] = {"board_mode": SC.BOARD_MODE, "chapters": 3,
                     "erase_at": edges}
    return rep


# every typed key and the spoken words it must agree with
WORD_SYNC = {"key-term": ((0, 1), "gpt luna", "GPT LUNA", "keyterm"),
             "ku-a FREE": ((7, 7), "free", "FREE", "kfree"),
             "ku-b + GO": ((8, 9), "and go", "+ GO", "kgo"),
             "ku-c USERS": ((10, 10), "users", "USERS", "kusers"),
             "key-chatgpt": ((13, 13), "chatgpt", "CHATGPT", "kchat"),
             "key-reason": ((26, 26), "reasoning", "REASONING", "kreason"),
             "amp-max": ((32, 32), "max.", "MAX", None),
             "key-budget": ((38, 38), "budget,", "BUDGET", "kbudget"),
             "key-arsenal": ((52, 52), "arsenal.", "ARSENAL", "karsenal")}


def assert_word_sync(ws: list[dict]) -> dict:
    """WORD-SYNC: every typed key first shows the value its words say, while
    or just after they are said.  No digit ticks anywhere in this scene."""
    rows = []
    for key, ((i0, i1), spoken, printed, cue) in WORD_SYNC.items():
        got = " ".join(w["text"] for w in ws[i0:i1 + 1]).lower()
        if got != spoken:
            raise SystemExit(f"word-sync: {key} expects {spoken!r}, the take "
                             f"says {got!r}")
        t = SC.CUE[cue] if cue else SC.CUE["max"] + 0.10
        last = ws[i1]
        lo, hi = float(last["start"]), float(last["end"]) + LABEL_WINDOW
        if not (lo - 0.01 <= t <= hi):
            raise SystemExit(f"word-sync: {key} first shows at {t}, outside "
                             f"{lo:.3f}-{hi:.3f}")
        rows.append({"state": key, "first_visible_text": printed,
                     "at": round(t, 2), "words": got,
                     "window": [round(lo, 3), round(hi, 3)]})
    if min(LABEL_AT.values()) != LABEL_AT["key-term"]:
        raise SystemExit("LAW 9: GPT LUNA is not the first type on the board")
    return {"typed_states": rows, "disagreements": 0, "digits_that_tick": 0,
            "note": "'100%' is spoken and never typed on the board"}


def assert_law37(ws: list[dict]) -> dict:
    cues = PCUE.scan(ws)
    plan = json.loads(PLAN.read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / "prep/stages/lunafree.cues.json").read_text())
    if marker["keys"]["cue_count"] != len(cues):
        raise SystemExit("LAW 37: the prep marker disagrees with the re-run")
    if cues or declared:
        raise SystemExit("LAW 37: this scene builds no source card")
    return {"scan_cue_count": 0, "plan_declared_cards": 0,
            "source_cards_in_the_page": 0}


# ------------------------------------------------------------------ laws
def assert_label_law() -> dict:
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    out: dict = {}
    for key, (host, side, text) in LABEL_PLAN.items():
        kb, hb = RECTS[key], RECTS[host]
        if side == "below" and kb[1] < hb[3] - 0.01:
            raise SystemExit(f"LAW 39: {key} is not entirely below {host}")
        if side == "above" and kb[3] > hb[1] + 0.01:
            raise SystemExit(f"LAW 39: {key} is not entirely above {host}")
        kc, hc = (kb[0] + kb[2]) / 2, (hb[0] + hb[2]) / 2
        if abs(kc - hc) > 0.15 * (hb[2] - hb[0]) + 0.01:
            raise SystemExit(f"LAW 39: {key} is off {host}'s axis")
        if not any(key in b and host in b for b in blocks):
            raise SystemExit(f"LAW 41: {key} is not blocked with {host}")
        if LABEL_AT[key] < HOST_AT[host] - 1e-9:
            raise SystemExit(f"LAW 39: {key} lands before its host")
        gutter = (kb[1] - hb[3]) if side == "below" else (hb[1] - kb[3])
        out[key] = {"host": host, "side": side, "text": text,
                    "at": LABEL_AT[key], "gutter_core_px": round(gutter, 1),
                    "box_canvas": [round(v, 1) for v in canvas(kb)]}
    # LAW 50: siblings share one baseline, plain labels one size
    if RECTS["key-users"][1] != RECTS["key-chatgpt"][1]:
        raise SystemExit("LAW 50: FREE + GO USERS and CHATGPT differ in baseline")
    if RECTS["key-budget"][1] != RECTS["key-arsenal"][1]:
        raise SystemExit("LAW 50: BUDGET and ARSENAL differ in baseline")
    hs = {round(RECTS[k][3] - RECTS[k][1], 2) for k in LABEL_PLAN
          if k != "key-term"}
    if len(hs) != 1:
        raise SystemExit(f"LAW 50: the plain labels differ in height {hs}")
    out["_law50"] = {"plain_label_font_px": SC.KEY_FS, "row_h": hs.pop(),
                     "baselines_core": {"chapter0": RECTS["key-users"][1],
                                        "chapter2": RECTS["key-budget"][1]}}
    du = SC.KEY_TERM_FS / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} du")
    out["_key_term"] = {"text": SC.KEY_TERM, "font_px": SC.KEY_TERM_FS,
                        "design_units": round(du, 2), "first_type": True}
    return out


MARKS = ("luna-tile", "chatgpt-tile", "luna-hung")
# the opaque cream sheet is the outro's cover, not a mark: it has no end by
# design and paints no ink (LIFETIMES carries it with None)
COVERS = ("o-sheet",)


def assert_lifetime_law() -> dict:
    anchors = [n for n, (_a, b) in SC.LIFETIMES.items() if b is None]
    for n in anchors:
        if n not in SC.SCENE_ANCHORS and n not in COVERS:
            raise SystemExit(f"LAW 42: {n} never leaves and is not an anchor")
    shares = {}
    for n in MARKS:
        a, b = SC.LIFETIMES[n]
        shares[n] = round((b - a) / DUR, 3)
        if shares[n] > 0.30:
            raise SystemExit(f"LAW 42: {n} is on screen {shares[n]:.0%}")
    return {"board_mode": SC.BOARD_MODE, "anchors": sorted(anchors),
            "covers": list(COVERS), "mark_shares": shares}


def assert_emphasis_law() -> dict:
    """LAW 38 rule 2: the target is a DRAWN plate, so the emphasis is its own
    border flip.  Nothing is added to the DOM."""
    a, b = SC.CUE["best"], SC.CUE["bestout"]
    if a + 0.38 > b:
        raise SystemExit("LAW 38: the flip on #luna-hung does not complete")
    return {"border_flips": [{"target": "#luna-hung", "from": a, "until": b}],
            "rings_ellipses_circles": 0, "highlights": 0,
            "dom_elements_added": 0}


def assert_cast_law() -> dict:
    rep = DF.assert_cast_resolves(list(SC.LOGO_FILES), dict(SC.LOGO_FILES),
                                  LOGOS, label="lunafree stage marks")
    return {"stage_marks": sorted(SC.LOGO_FILES),
            "resolved": {k: v["path"] for k, v in rep.items()},
            "cutout_lanes_not_ours": list(CUTOUT_LANES)}


def _tags_for(sel: str, html: str) -> list[str]:
    """'#id .a' -> every shape inside the element id=... up to its </svg>
    whose class list holds every named class."""
    parts = sel.split()
    if len(parts) != 2 or not parts[0].startswith("#"):
        raise SystemExit(f"unexpected dash selector {sel}")
    hid = parts[0][1:]
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


def declare_connector(scene_html: str) -> tuple[str, dict]:
    """Stamp the measurement contract on the ONE connector the module emits.
    The target anchor is the ChatGPT tile's LEFT border at mid height
    (SC.CONN_TO = anchor_points(CHATGPT_BOX, 1, 'left'), fraction 0.5)."""
    frac = (SC.CONN_TO[1] - SC.CHATGPT_BOX[1]) / (SC.CHATGPT_BOX[3]
                                                  - SC.CHATGPT_BOX[1])
    old = 'data-connect-to="chatgpt-tile" data-overlap-ok'
    if scene_html.count(old) != 1 or scene_html.count("data-connect-to") != 1:
        raise SystemExit("LAW 40: expected exactly one connector in the scene")
    new = (f'data-connect-to="chatgpt-tile" data-anchor-side="left" '
           f'data-anchor-fraction="{frac:.3f}" '
           f'data-check-at="{CONN_CHECK_AT:.2f}" data-overlap-ok')
    lo, hi = SC.LIFETIMES["conn-app"]
    if not (SC.CUE["conn"] + 0.22 < CONN_CHECK_AT < hi - 0.22):
        raise SystemExit("LAW 40: the check instant is not a completed state")
    return scene_html.replace(old, new), {
        "id": "conn-app", "to": "chatgpt-tile", "side": "left",
        "fraction": round(frac, 3), "check_at": CONN_CHECK_AT,
        "contact": SC.assert_connector_contact()}


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
    # the scene's tweens name three eases by identifier (handoff section 1)
    return f"""
</div>
<script>
window.__timelines = window.__timelines || {{}};
const none = "none";
const hidden = "hidden";
const POP = "back.out(2.05)";
const SOFT = "power3.out";
const SWING = "power2.inOut";
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
        src = ASSETS / rel
        if not src.exists():
            raise SystemExit(f"registry key {key!r} does not resolve: {src}")
        shutil.copy2(src, dst / "assets/logos" / src.name)
        CC.MARK_INK[key] = CC.measure_mark(key, src)
        marks[key] = {"source": str(src), "url": LOGO_URL[key]}
    rec["marks"] = marks
    return rec


def media() -> dict:
    """The THREE rasters the scene paints (handoff section 1)."""
    return {
        "_openai_img": CC.mark_img(LOGO_URL["openai"], "openai", SC.MARK_SIDE),
        "_chatgpt_img": CC.mark_img(LOGO_URL["chatgpt"], "chatgpt",
                                    SC.MARK_SIDE),
        "_openai_badge_img": CC.mark_img(LOGO_URL["openai"], "openai",
                                         SC.BADGE_MARK),
    }


def sfx_plan() -> list[tuple]:
    """EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22)."""
    C = SC.CUE
    return [("pop", C["gift"], SFX_STRUCTURE),       # the gift pops in
            ("click", C["keyterm"], SFX_DETAIL),     # GPT LUNA is written
            ("pop", C["open"], SFX_STRUCTURE),       # lid off, tile rises
            ("click", C["kfree"], SFX_DETAIL),       # FREE
            ("click", C["kusers"], SFX_DETAIL),      # USERS
            ("pop", C["chatgpt"], SFX_DETAIL),       # ChatGPT tile lands
            ("pop", C["amp"], SFX_STRUCTURE),        # the amp, new chapter
            ("whoosh", C["mighty"], SFX_DETAIL),     # the first waves
            ("click", C["turn1"], SFX_DETAIL),       # knob step
            ("click", C["kreason"], SFX_DETAIL),     # knob step + REASONING
            ("click", C["turn3"], SFX_DETAIL),       # knob step
            ("click", C["turn4"], SFX_DETAIL),       # knob step
            ("pop", C["max"] + 0.10, SFX_STRUCTURE),  # MAX, the waves blast
            ("pop", C["piggy"], SFX_STRUCTURE),      # the piggy, new chapter
            ("click", C["coin"], SFX_DETAIL),        # the coin drops in
            ("pop", C["board"], SFX_STRUCTURE),      # the pegboard arrives
            ("pop", C["tile"], SFX_DETAIL),          # the tile hangs
            ("click", C["best"], SFX_DETAIL),        # the border flips
            ("click", C["karsenal"], SFX_DETAIL),    # ARSENAL
            ("whoosh", C["outro"], SFX_STRUCTURE)]   # the rising sheet


def assert_sfx(sfx) -> dict:
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30:
        raise SystemExit(f"SFX flam: {worst}")
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "deliberately_silent": {
                "rise 2.40": "0.06 s after the lid pop; one pop scores both",
                "+ GO 3.60": "between FREE and USERS, 0.28 s from USERS",
                "shift 4.58 / arrow 4.80 / CHATGPT 4.96": "inside the ChatGPT "
                "pop's 0.30 s; one arrival scores the move",
                "chapter erases 5.84 / 11.96": "0.20 / 0.10 s before the next "
                "chapter's pop",
                "slide 13.14": "0.04 s before the board pop",
                "tools 14.42": "0.30 s after the flip click; the tools fade",
                "outro lockup 17.22": "rides the sheet's whoosh"}}


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
        raise SystemExit(f"core content starts at y={y0:.1f} - LAW 30")
    if y1 > pill_top - pill_clear:
        raise SystemExit(f"core content ends at y={y1:.1f}, within {pill_clear}"
                         f"px of the pill top {pill_top:.1f}")
    return {"content_top": y0, "content_bottom": y1,
            "pill_top_rendered": round(pill_top, 3),
            "clear_above_pill": round(pill_top - y1, 2),
            "clear_below_law30": round(y0 - 0.10 * H, 2)}


def guard_rail() -> dict:
    # the rail binds readable INK: JetBrains Mono advances 0.600 em
    rights = {}
    for n, (_h, _s, text) in LABEL_PLAN.items():
        b = canvas(RECTS[n])
        fs, ls = ((SC.KEY_TERM_FS, SC.KEY_TERM_LS) if n == "key-term"
                  else (SC.KEY_FS, SC.KEY_LS))
        ink = len(text) * 0.6 * fs + (len(text) - 1) * ls
        rights[n] = (b[0] + b[2]) / 2 + ink / 2
    type_right = max(rights.values())
    if type_right > CAP.LAW12_RAIL_X + 0.01:
        raise SystemExit(f"readable key ink reaches x={type_right:.1f}")
    boxes = [canvas(o["core"]) for o in SC.BESPOKE]
    boxes.append(canvas((SC.PIGGY_BOX[0] + SC.PIGGY_DX, SC.PIGGY_BOX[1],
                         SC.PIGGY_BOX[2] + SC.PIGGY_DX, SC.PIGGY_BOX[3])))
    ink_left = min(b[0] for b in boxes)
    ink_right = max(b[2] for b in boxes)
    if ink_left < 30 or W - ink_right < 30:
        raise SystemExit("the composition leaves the frame margin")
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
    cues = assert_cues(ws)
    wordsync = assert_word_sync(ws)
    law37 = assert_law37(ws)
    labels = assert_label_law()
    lifetimes = assert_lifetime_law()
    emphasis = assert_emphasis_law()
    cast = assert_cast_law()
    SFX = sfx_plan()
    sfx_guard = assert_sfx(SFX)

    scene_html, tweens = SC.build(media(), outro_lockup(handle))
    drawon = assert_draw_on(tweens, scene_html)
    scene_html, law40 = declare_connector(scene_html)
    for shape in ("<circle", "<ellipse"):
        if shape in scene_html:
            raise SystemExit(f"LAW 38 rule 3: {shape} in the emitted scene")
    for host, n in (("gift", 2), ("chatgpt-tile", 1), ("amp", 1),
                    ("piggy", 1), ("board", 1)):
        if scene_html.count(f'data-label-for="{host}"') != n:
            raise SystemExit(f"{host} does not carry its {n} declared label(s)")

    m = CAP.PillMeasurer(RUN / "gen/_pillwidths_lunafree.json")
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
            "law39": labels, "law42": lifetimes, "law38": emphasis,
            "law40": law40, "law2": cast, "law22": sfx_guard,
            "draw_on": drawon, "transcript": cap_rep, "phone_objects": objs,
            "render": {"w": 1080, "h": 1920, "zoom": 1}}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="split", choices=("split",))
    ap.parse_args()
    dst = RUN / "projects/lunafree_split"
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
    (RUN / "gen/_build_lunafree_split.json").write_text(
        json.dumps(report, indent=1, default=str))
    geom = {"video": VID, "fps": FPS, "duration": DUR,
            "shared": {"beat_edges": SC.BEAT_EDGES},
            "formats": {"split": {"phone_objects": rep["phone_objects"],
                                  "core": rep["core"], "scale": rep["scale"],
                                  "seat": rep["seat"]}}}
    (RUN / f"gen/_geom_{VID}_split.json").write_text(json.dumps(geom, indent=1))
    print(f"split: {dst}")
    print(json.dumps({"captions": rep["captions"], "band": rep["band"],
                      "rail": rep["rail"],
                      "law22": rep["law22"]["tightest_gap_s"],
                      "law40": rep["law40"],
                      "draw_on": rep["draw_on"],
                      "phone": rep["phone_objects"]}, indent=1))


if __name__ == "__main__":
    main()
