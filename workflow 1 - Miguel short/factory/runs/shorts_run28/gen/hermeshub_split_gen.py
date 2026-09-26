#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION - hermeshub / ICON CHOREOGRAPHY.

    YouTube   classic split 50/50   projects/hermeshub_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/hermeshub_scene.py` plus
`plans/hermeshub_scene_handoff.md` are the design agent's artefacts, sealed by
`review/artwork_pass_hermeshub.json` (production v4, `production.py seal`).
This file IMPORTS the module and SEATS it at the handoff's own placement
(k = 1.00, left 0, core top 192).  It never mutates a byte of the module.

The only thing this page adds to the scene's emitted string is the measurement
contract (production visual_laws):
  * the three chapter-A links carry `data-anchor-side="top"`,
    `data-anchor-fraction="0.5"` and `data-check-at` (each ends on its app
    tile's top-centre, `anchor_points(app_tile, 1, "top")`);
  * the two border-flip hosts carry `data-emphasis="border"`, their target and
    a check instant: `#win-slack` (the window's own border, 17.84-18.90) and
    `#hub-toolbar` (the held flip, 18.96 to the outro).  The toolbar's first
    flip (11.26-11.90) is the same element's border and cannot carry a second
    declaration; its completion is asserted here in Python instead;
  * the toolbar's own parts (`#tb-slot`, `#tb-mark`, `#tb-led`) are declared
    `data-block="hub"`, the block their parent already carries (LAW 41: a
    container's contents), so the seated toolbar is one object on its window.
The geometry is untouched.

HD DELIVERY: authored AND encoded 1080x1920.  The face plate is
`face_bottom_hd.mp4` (1080x1058), so the seam is 1920 - 1057.5 = 862.5 and the
RENDERING pill top is 862.5 - 114.59/2 = 805.205 (the pill that renders, never
the frozen 108.2 seat constant).  The core's content band 70..570 lands at
canvas 262..762: 70 px under LAW 30's top-10 % line and ~43 px over the pill.

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
import hermeshub_scene as SC                    # noqa: E402

RUN = Path(__file__).resolve().parents[1]
CUT = RUN / "cuts/hermeshub"
PLAN = RUN / "plans/hermeshub_plan.json"
ASSETS = Path.home() / "Documents/Workspace/assets"
LOGOS = ASSETS / "logos"
LIB_MUSIC = ASSETS / "audio/music/shorts-factory"
LIB_SFX = ASSETS / "audio/sfx/shorts-factory"

VID = "hermeshub"
W, H = 1080.0, 1920.0
FPS = 25
DUR = SC.DUR                                     # 24.08, the cut master

SEAM = 862.5
CORE_TOP_SPLIT = SC.CANVAS_OFFSET                # 192.0, the handoff's number
CORE_K = 1.00
LEFT = (W - SC.CORE_W * CORE_K) / 2              # 0.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "Hermes Hub mode sits on any app"
LABEL_WINDOW = 1.0

# ------------------------------------------------------------------ marks
STAGE_FILES = {k: f"logos/{v}" for k, v in SC.LOGO_FILES.items()}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}
CUTOUT_LANES = SC.CUTOUT_LOGO_LANES


def _xywh(b) -> tuple:
    x, y, w, h = b
    return (x, y, x + w, y + h)


# Seats in CORE px (x0, y0, x1, y1), at the instant each label lands
TB_RECT = _xywh(SC.TB)                           # chapter B: 360,250 .. 720,354
RECTS: dict[str, tuple] = {
    "hub-toolbar": TB_RECT,
    "key-hub-mode": _xywh(SC.KEY_TERM_BOX),
    "lbl-always-on": _xywh(SC.LBL_ON_BOX),
}


def canvas(box):
    """core px -> the canvas this page actually paints (top 192, k 1.00)."""
    return (CORE_K * box[0] + LEFT, CORE_TOP_SPLIT + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP_SPLIT + CORE_K * box[3])


# --------------------------------------------------------------- label plan
# LAW 39 / LAW 9 (plan.labels): HUB MODE above the toolbar, ALWAYS ON below.
LABEL_PLAN = {"key-hub-mode": ("hub-toolbar", "above", SC.KEY_TERM),
              "lbl-always-on": ("hub-toolbar", "below", "ALWAYS ON")}
LABEL_AT = {"key-hub-mode": SC.CUE["keyterm"], "lbl-always-on": SC.CUE["lbl_on"]}
HOST_AT = {"hub-toolbar": SC.CUE["toolbar"]}
PRINTED_KEYS = {k: v[2] for k, v in LABEL_PLAN.items()}
PRINTED_LIFETIME = {k: SC.LIFETIMES[k] for k in LABEL_PLAN}

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.
CUE_WORDS = {
    "tile": (0, "hermes"), "rise": (6, "any"), "laptop": (7, "application"),
    "links": (10, "working"), "seamA": (20, "shipped"), "open": (21, "hub"),
    "boxout": (25, "allows"), "led": (30, "always-on"), "mark": (31, "hermes"),
    "flip1": (37, "toolbar"), "seamB": (38, "that"), "win": (40, "you"),
    "drag": (43, "drag"), "drop": (45, "drop"), "across": (47, "your"),
    "drop2": (49, "desktop,"), "seamC": (50, "and"), "context": (55, "context"),
    "flip2": (59, "application"), "flip3": (62, "sitting"),
    "outro": (66, "now,"),
}
# AUTHORED instants: each inside its own word's 1.0 s LABEL_WINDOW
CUE_INSIDE = {"apps": (7, "application"), "box": (20, "shipped"),
              "toolbar": (21, "hub"), "keyterm": (22, "mode."),
              "lbl_on": (30, "always-on"), "centre": (50, "and")}
# the two flips' returns, placed after their words by design
CUE_FREE = ("flip1back", "flip2back")


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
    opening = "hermes can now help you in any application"
    head = " ".join(w["text"] for w in ws[:8]).lower()
    if head != opening:
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[8:]).lower()
    if "can now help" in later:
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
           "law47_verdict": ("PASS" if tail <= cap + 1e-6 else "REPORTED")
           + f" - {tail:.3f}s past the last word against a {cap:.3f}s cap",
           "law46": "the scripted opening occurs ONCE inside the keeper take, "
                    "at word 0 / 0.10 s",
           "inner_stumble_kept": "'on on your computer' (2.62 / 2.90) - INNER "
                                 "STUMBLES STAY",
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
        if not (lo - 0.011 <= t <= hi):
            raise SystemExit(f"cue {name} at {t} is outside the window of "
                             f"{w['text']!r} ({lo:.3f}-{hi:.3f})")
        rep[name] = {"word": idx, "text": w["text"], "t": t,
                     "window": [round(lo, 3), round(hi, 3)]}
    missing = set(SC.CUE) - set(rep) - set(CUE_FREE)
    if missing:
        raise SystemExit(f"cues the build never verified: {sorted(missing)}")
    if SC.BOARD_MODE != "chapters" or len(SC.BOARD_CHAPTERS) != 4:
        raise SystemExit("the scene is no longer the four chapters the plan "
                         "declared")
    edges = [c["erase_at"] for c in SC.BOARD_CHAPTERS]
    if edges != [SC.CUE["seamA"], SC.CUE["seamB"], SC.CUE["seamC"],
                 SC.CUE["outro"]]:
        raise SystemExit(f"LAW 43: chapter erases {edges} are off their marks")
    # LAW 45: the next chapter lands on an object within 0.30 s of the erase
    # (5.34 -> the box 5.40; 11.98 and 15.86 carry the toolbar anchor across)
    if SC.CUE["box"] - SC.CUE["seamA"] > 0.30:
        raise SystemExit("LAW 45: empty board after the first seam")
    rep["_law43"] = {"board_mode": SC.BOARD_MODE, "chapters": 4,
                     "erase_at": edges,
                     "anchor_across_seams": list(SC.SCENE_ANCHORS)}
    return rep


# every typed key and the spoken words it must agree with
WORD_SYNC = {"key-hub-mode": ((21, 22), "hub mode.", "HUB MODE", "keyterm"),
             "lbl-always-on": ((30, 30), "always-on", "ALWAYS ON", "lbl_on")}


def assert_word_sync(ws: list[dict]) -> dict:
    """WORD-SYNC: every typed key first shows the value its words say, while
    or just after they are said.  No digit anywhere in this scene."""
    rows = []
    for key, ((i0, i1), spoken, printed, cue) in WORD_SYNC.items():
        got = " ".join(w["text"] for w in ws[i0:i1 + 1]).lower()
        if got != spoken:
            raise SystemExit(f"word-sync: {key} expects {spoken!r}, the take "
                             f"says {got!r}")
        t = SC.CUE[cue]
        last = ws[i1]
        lo, hi = float(last["start"]), float(last["end"]) + LABEL_WINDOW
        if not (lo - 0.01 <= t <= hi):
            raise SystemExit(f"word-sync: {key} first shows at {t}, outside "
                             f"{lo:.3f}-{hi:.3f}")
        rows.append({"state": key, "first_visible_text": printed,
                     "at": round(t, 2), "words": got,
                     "window": [round(lo, 3), round(hi, 3)]})
    if min(LABEL_AT.values()) != LABEL_AT["key-hub-mode"]:
        raise SystemExit("LAW 9: HUB MODE is not the first type on the board")
    return {"typed_states": rows, "disagreements": 0, "digits_that_tick": 0}


def assert_law37(ws: list[dict]) -> dict:
    cues = PCUE.scan(ws)
    plan = json.loads(PLAN.read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / "prep/stages/hermeshub.cues.json").read_text())
    if marker["keys"]["cue_count"] != len(cues):
        raise SystemExit("LAW 37: the prep marker disagrees with the re-run")
    if cues or declared:
        raise SystemExit("LAW 37: this scene builds no source card")
    return {"scan_cue_count": 0, "plan_declared_cards": 0,
            "source_cards_in_the_page": 0}


# ------------------------------------------------------------------ laws
def assert_label_law() -> dict:
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
        if LABEL_AT[key] < HOST_AT[host] - 1e-9:
            raise SystemExit(f"LAW 39: {key} lands before its host")
        gutter = (kb[1] - hb[3]) if side == "below" else (hb[1] - kb[3])
        out[key] = {"host": host, "side": side, "text": text,
                    "at": LABEL_AT[key], "gutter_core_px": round(gutter, 1),
                    "box_canvas": [round(v, 1) for v in canvas(kb)],
                    "declared": 'data-label-for="hub-toolbar"'}
    # LAW 28: the toolbar never moves while its names are on screen (the 5.90
    # rise completes at 6.40, under HUB MODE's entrance; the next move is 12.56)
    if not SC.CUE["win"] > SC.LIFETIMES["key-hub-mode"][1] - 1e-9:
        raise SystemExit("LAW 28: the toolbar moves while its names are shown")
    du = SC.KEY_TERM_FS / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} du")
    out["_key_term"] = {"text": SC.KEY_TERM, "font_px": SC.KEY_TERM_FS,
                        "design_units": round(du, 2), "first_type": True}
    return out


MARKS = ("hb-tile", "app-figma", "app-notion", "app-slack")
# the opaque cream sheet and the outro lockup pieces have no end by design
COVERS = ("o-sheet", "o-glyph", "o-rule", "o-slot")


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
    return {"board_mode": SC.BOARD_MODE, "anchors": list(SC.SCENE_ANCHORS),
            "covers": list(COVERS), "mark_shares": shares}


# LAW 38 rule 2: every emphasis is a DRAWN object's own border flip.
FLIP_D = 0.38
EMPH = {
    "win-slack": {"target": "win-slack", "flip": SC.CUE["flip2"],
                  "until": SC.CUE["flip2back"], "check_at": 18.50},
    "hub-toolbar": {"target": "hub-toolbar", "flip": SC.CUE["flip3"],
                    "until": SC.CUE["outro"], "check_at": 19.60},
}


def assert_emphasis_law() -> dict:
    flips = [("hub-toolbar", SC.CUE["flip1"], SC.CUE["flip1back"], None)]
    flips += [(k, e["flip"], e["until"], e["check_at"]) for k, e in EMPH.items()]
    for sel, a, b, chk in flips:
        if a + FLIP_D > b:
            raise SystemExit(f"LAW 38: the flip on #{sel} at {a} does not "
                             "complete")
        if chk is not None and not (a + FLIP_D <= chk < b):
            raise SystemExit(f"LAW 38: #{sel} is not checked at a held flip")
    return {"border_flips": [{"target": f"#{s}", "from": a, "until": b,
                              "check_at": c} for s, a, b, c in flips],
            "rings_ellipses_circles": 0, "highlights": 0,
            "dom_elements_added": 0,
            "note": "the 11.26 toolbar flip shares its element with the held "
                    "18.96 flip, which carries the one declaration"}


def assert_cast_law() -> dict:
    rep = DF.assert_cast_resolves(list(SC.LOGO_FILES), dict(SC.LOGO_FILES),
                                  LOGOS, label="hermeshub stage marks")
    return {"stage_marks": sorted(SC.LOGO_FILES),
            "resolved": {k: v["path"] for k, v in rep.items()},
            "mark_identity": "Hermes = nous-girl-line, never the H glyph",
            "cutout_lanes_not_ours": list(CUTOUT_LANES)}


def assert_draw_on(tweens: list[str], html: str) -> dict:
    """THE DRAW-ON DASH LAW: every selector revealed with a 100-unit dash
    resolves ONLY to shapes that declare pathLength="100"."""
    sels = set()
    for t in tweens:
        if "strokeDasharray:100" in t:
            for s in re.findall(r'tl\.set\("([^"]+)"', t):
                sels.update(p.strip() for p in s.split(","))
    checked = {}
    for sel in sorted(sels):
        parts = sel.split()
        hid, cls = parts[0][1:], parts[1].lstrip(".")
        m = re.search(rf'id="{re.escape(hid)}"(.*?)</svg>', html, re.S)
        tags = [g for g in re.findall(r'<(?:path|line|polyline|rect)\b[^>]*>',
                                      m.group(1) if m else "")
                if re.search(rf'class="[^"]*\b{re.escape(cls)}\b', g)]
        if not tags or not all('pathLength="100"' in g for g in tags):
            raise SystemExit(f"DRAW-ON: {sel} reveals a path without "
                             'pathLength="100"')
        checked[sel] = len(tags)
    return {"dash_selectors": checked, "verdict": "every dash equals its "
            "path's declared length (100)"}


CONN_CHECK_AT = 3.20        # all three drawn (2.70), chapter A held to 5.34


def declare_contracts(scene_html: str) -> tuple[str, dict]:
    s = scene_html
    if s.count("data-connect-to") != 3:
        raise SystemExit("LAW 40: expected exactly three connectors")
    lo, hi = SC.CUE["links"] + 0.12 + 0.28, SC.CUE["seamA"]
    if not (lo < CONN_CHECK_AT < hi):
        raise SystemExit("LAW 40: the check instant is not a completed state")
    conns = []
    for i, key in enumerate(SC.APP_KEYS):
        old = f'data-connect-to="app-{key}"'
        if s.count(old) != 1:
            raise SystemExit(f"cannot stamp the link into app-{key}")
        s = s.replace(old, f'{old} data-anchor-side="top" '
                           f'data-anchor-fraction="0.5" '
                           f'data-check-at="{CONN_CHECK_AT:.2f}"', 1)
        (sx, sy), (ex, ey) = SC.LINK_FROM[i], SC.LINK_TO[i]
        box = SC.app_box(i)
        if abs(ey - box[1]) > 1e-6 or abs(ex - (box[0] + box[2]) / 2) > 1e-6:
            raise SystemExit(f"LAW 40: link {key} does not end on the tile top")
        if abs(sy - SC.HT_BOX[3]) > 1e-6:
            raise SystemExit(f"LAW 40: link {key} does not start on the tile")
        conns.append({"id": f"link-{key}", "to": f"app-{key}", "side": "top",
                      "fraction": 0.5, "check_at": CONN_CHECK_AT,
                      "from_core": [round(sx, 2), sy], "to_core": [ex, ey]})
    stamped = []
    for eid, e in EMPH.items():
        key = f'id="{eid}"'
        if s.count(key) != 1:
            raise SystemExit(f"cannot stamp {eid}")
        s = s.replace(key, f'{key} data-emphasis="border" '
                           f'data-emphasis-target="{e["target"]}" '
                           f'data-check-at="{e["check_at"]:.2f}"', 1)
        stamped.append(eid)
    if (s.count("data-connect-to") + s.count("data-emphasis=")
            != s.count("data-check-at")):
        raise SystemExit("a connector or emphasis is missing its check instant")
    # LAW 41: the toolbar's own parts (its mark slot, the Nous mark, the status
    # light) are the toolbar's contents, so they belong to ITS block ("hub").
    # The audit does not inherit a block from an ancestor: undeclared, the slot
    # reads as a separate object 8.7 px above the window it is seated on.
    blocked = []
    for eid in TB_PARTS:
        key = f'id="{eid}"'
        if s.count(key) != 1:
            raise SystemExit(f"cannot declare {eid} inside the toolbar block")
        s = s.replace(key, f'{key} data-block="hub"', 1)
        blocked.append(eid)
    return s, {"connectors": conns, "emphases_stamped": stamped,
               "toolbar_parts_blocked_hub": blocked}


TB_PARTS = ("tb-slot", "tb-mark", "tb-led")


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
    norm = text.strip().upper().rstrip('.,!?"').lstrip('"').replace("-", " ")
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
    forbidden = set()
    for t in PRINTED_KEYS.values():
        for form in (t.lower(), t.lower().replace(" ", "-")):
            forbidden.update(form + suf for suf in ("", ".", ",", "!", "?"))
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
    # the scene's eases are string literals (handoff section 1); no constants
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
    """The FIVE rasters the scene paints (handoff section 1)."""
    return {
        "_hermes_img": CC.mark_img(LOGO_URL["nous-girl-line"], "nous-girl-line",
                                   SC.MARK_SIDE),
        "_hermes_tb_img": CC.mark_img(LOGO_URL["nous-girl-line"],
                                      "nous-girl-line", SC.TB_MARK_SIDE,
                                      eid="tb-mark", opacity=0),
        "_figma_img": CC.mark_img(LOGO_URL["figma"], "figma", SC.MARK_SIDE),
        "_notion_img": CC.mark_img(LOGO_URL["notion"], "notion", SC.MARK_SIDE),
        "_slack_img": CC.mark_img(LOGO_URL["slack"], "slack", SC.MARK_SIDE),
    }


def sfx_plan() -> list[tuple]:
    """EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22)."""
    C = SC.CUE
    return [("pop", C["tile"], SFX_STRUCTURE),       # the Hermes tile pops
            ("pop", C["laptop"], SFX_STRUCTURE),     # the laptop draws in
            ("click", C["links"], SFX_DETAIL),       # three lines into the apps
            ("pop", C["box"], SFX_STRUCTURE),        # the box, new chapter
            ("whoosh", C["toolbar"], SFX_DETAIL),    # toolbar rises out
            ("click", C["keyterm"] + 0.30, SFX_DETAIL),  # HUB MODE settles
            ("whoosh", C["boxout"], SFX_DETAIL),     # the empty box drops
            ("click", C["led"], SFX_DETAIL),         # status light on
            ("pop", C["mark"], SFX_DETAIL),          # Nous mark in the slot
            ("click", C["flip1"], SFX_DETAIL),       # toolbar border flip
            ("pop", C["win"], SFX_STRUCTURE),        # three windows
            ("whoosh", C["drag"], SFX_DETAIL),       # lift
            ("click", C["drop"] + 0.16, SFX_DETAIL),  # seated on Figma
            ("whoosh", C["across"], SFX_DETAIL),     # glide
            ("click", C["drop2"] + 0.16, SFX_DETAIL),  # seated on Slack
            ("whoosh", C["centre"], SFX_DETAIL),     # the block to the centre
            ("click", C["context"], SFX_DETAIL),     # rows drawn in
            ("click", C["flip2"], SFX_DETAIL),       # window border flip
            ("click", C["flip3"], SFX_DETAIL),       # toolbar border flip
            ("whoosh", C["outro"], SFX_STRUCTURE)]   # the rising sheet


def assert_sfx(sfx) -> dict:
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30:
        raise SystemExit(f"SFX flam: {worst}")
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "deliberately_silent": {
                "rise 1.34": "the tile's own move; the laptop pop 0.18 s later "
                             "scores the arrival",
                "apps 1.70-1.90": "inside the laptop pop's 0.36 s",
                "seam 5.34": "0.06 s before the box pop",
                "lid 5.86": "0.04 s before the toolbar whoosh",
                "labels leave 11.98 / Figma+Notion leave 15.86": "exits",
                "outro lockup 20.48": "rides the sheet's whoosh"}}


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
        fs, ls = ((SC.KEY_TERM_FS, 2.0) if n == "key-hub-mode"
                  else (SC.KEY_FS, SC.KEY_LS))
        ink = len(text) * 0.6 * fs + (len(text) - 1) * ls
        rights[n] = (b[0] + b[2]) / 2 + ink / 2
    type_right = max(rights.values())
    if type_right > CAP.LAW12_RAIL_X + 0.01:
        raise SystemExit(f"readable key ink reaches x={type_right:.1f}")
    boxes = [canvas(o["core"]) for o in SC.BESPOKE]
    boxes += [canvas((SC.WIN_X[0], SC.WIN_Y, SC.WIN_X[2] + SC.WIN_W,
                      SC.WIN_Y + SC.WIN_H))]
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
    scene_html, declared = declare_contracts(scene_html)
    for shape in ("<circle", "<ellipse"):
        if shape in scene_html:
            raise SystemExit(f"LAW 38 rule 3: {shape} in the emitted scene")
    if scene_html.count('data-label-for="hub-toolbar"') != 2:
        raise SystemExit("the toolbar does not carry its two declared labels")
    if 'id="tb-mark"' not in scene_html:
        raise SystemExit("the toolbar mark has no id: the 8.94 pop is dead")

    m = CAP.PillMeasurer(RUN / "gen/_pillwidths_hermeshub.json")
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
            "law40": declared, "law2": cast, "law22": sfx_guard,
            "draw_on": drawon, "transcript": cap_rep, "phone_objects": objs,
            "render": {"w": 1080, "h": 1920, "zoom": 1}}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="split", choices=("split",))
    ap.parse_args()
    dst = RUN / "projects/hermeshub_split"
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
    (RUN / "gen/_build_hermeshub_split.json").write_text(
        json.dumps(report, indent=1, default=str))
    geom = {"video": VID, "fps": FPS, "duration": DUR,
            "shared": {"beat_edges": SC.BEAT_EDGES},
            "formats": {"split": {"phone_objects": rep["phone_objects"],
                                  "core": rep["core"], "scale": rep["scale"],
                                  "seat": rep["seat"]}}}
    (RUN / f"gen/_geom_{VID}_split.json").write_text(json.dumps(geom, indent=1))
    print(f"split: {dst}")
    print(json.dumps({"captions": rep["captions"], "band": rep["band"],
                      "rail": rep["rail"], "transcript": {
                          k: rep["transcript"][k] for k in
                          ("law47_verdict", "function_word_merges",
                           "orphan_repartitions", "solo_word_merges")},
                      "law22": rep["law22"]["tightest_gap_s"],
                      "law40": rep["law40"], "draw_on": rep["draw_on"],
                      "phone": rep["phone_objects"]}, indent=1))


if __name__ == "__main__":
    main()
