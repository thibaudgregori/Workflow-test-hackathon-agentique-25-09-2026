#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION - streamdeck / ICON CHOREOGRAPHY.

    YouTube   classic split 50/50   projects/streamdeck_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/streamdeck_scene.py` plus
`plans/streamdeck_scene_handoff.md` are the design agent's artefacts, sealed by
`review/artwork_pass_streamdeck.json` (production v4, `production.py seal`).
This file IMPORTS the module and SEATS it at the handoff's own placement
(k = 1.00, left 0, core top 192).  It never mutates a byte of the module on disk.

FORMAT-SIDE STAMPS ON THE EMITTED STRING (the module on disk is untouched):
  * LAW 40 contract: the cable targets an inkless virtual rect `#deck1-body`
    (the keypad body's stroke centre line, where the handoff lands it) and the
    arrows target `#deck2-edge` (the body stroke's OUTER edge, where the heads'
    tips sit).  Both get `data-anchor-side`, `data-anchor-fraction` and
    `data-check-at`; the arrowheads carry the `ahead` class so the measured
    endpoint is the painted tip, not the shaft's end.
  * LAW 38 contract: the four border flips are declared on the flipped outline
    itself (`data-emphasis="border"`, target, check instant).  The big keycap's
    target is an inkless virtual rect `#bigkey-face`, because the cap carries a
    bulb whose INK base parts share the key base's ink.
  * LAW 30 (right rail, readable annotations): ONE CLICK, centred on the big key
    at x 845, puts its K ~7 px past x 918.  The big key AND its label move 8 px
    left TOGETHER (static left, no motion), so the weld (LAW 39) is exact and
    the ink ends inside the rail.  Logged in plans/streamdeck_split_notes.md.

HD DELIVERY: authored AND encoded 1080x1920.  The face plate is
`face_bottom_hd.mp4` (1080x1058), so the seam is 1920 - 1057.5 = 862.5 and the
RENDERING pill top is 862.5 - 114.59/2 = 805.205 (the pill that renders, never
the frozen 108.2 seat constant).  The core's content band 96..514 lands at
canvas 288..706: 96 px under LAW 30's top-10 % line and ~99 px over the pill.

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
import streamdeck_scene as SC                   # noqa: E402

RUN = Path(__file__).resolve().parents[1]
CUT = RUN / "cuts/streamdeck"
PLAN = RUN / "plans/streamdeck_plan.json"
ASSETS = Path.home() / "Documents/Workspace/assets"
LOGOS = ASSETS / "logos"
LIB_MUSIC = ASSETS / "audio/music/shorts-factory"
LIB_SFX = ASSETS / "audio/sfx/shorts-factory"

VID = "streamdeck"
W, H = 1080.0, 1920.0
FPS = 25
DUR = SC.DUR                                     # 30.48, the cut master

SEAM = 862.5
CORE_TOP_SPLIT = SC.CANVAS_OFFSET                # 192.0, the handoff's number
CORE_K = 1.00
LEFT = (W - SC.CORE_W * CORE_K) / 2              # 0.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "The best accessory for Claude is a Stream Deck"
LABEL_WINDOW = 1.0

# LAW 30 rail: the big key and ONE CLICK move left together (static)
RAIL_DX = -8.0

# ------------------------------------------------------------------ marks
STAGE_FILES = {k: f"logos/{v}" for k, v in SC.LOGO_FILES.items()}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}
CUTOUT_LANES = SC.CUTOUT_LOGO_LANES


def _xywh(b) -> tuple:
    x, y, w, h = b
    return (x, y, x + w, y + h)


def _dx(b, dx) -> tuple:
    return (b[0] + dx, b[1], b[2] + dx, b[3])


# Seats in CORE px (x0, y0, x1, y1), as PAINTED in this page
DECK1_BODY = (SC.DECK1[0] + SC.SHIFT_DX, SC.DECK1[1],
              SC.DECK1[0] + SC.SHIFT_DX + SC.DECK_W, SC.DECK1[1] + SC.DECK_H)
# the flashlight scene's painted extent: torch at its left seat, the beam's two
# edges (lower edge ends at y 452), the three devices
SCAN_PAINT = (SC.TORCH_L[0], SC.BEAM_TOP[1][1], SC.BEAM_TOP[1][0],
              SC.BEAM_BOT[1][1])
BIGKEY_BOX = _dx(_xywh(SC.BIGKEY), RAIL_DX)
RECTS: dict[str, tuple] = {
    "deck1": DECK1_BODY,
    "key-deck": _dx(_xywh(SC.KEY_TERM_BOX), SC.SHIFT_DX),
    "scan": SCAN_PAINT,
    "key-every": _xywh(SC.EVERY_BOX),
    "bigkey": BIGKEY_BOX,
    "key-oneclick": _dx(_xywh(SC.ONECLICK_BOX), RAIL_DX),
}


def canvas(box):
    """core px -> the canvas this page actually paints (top 192, k 1.00)."""
    return (CORE_K * box[0] + LEFT, CORE_TOP_SPLIT + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP_SPLIT + CORE_K * box[3])


# --------------------------------------------------------------- label plan
# LAW 39 / LAW 9 / LAW 50: three labels, all BELOW their hosts.
LABEL_PLAN = {"key-deck": ("deck1", "below", SC.KEY_TERM),
              "key-every": ("scan", "below", "EVERY DEVICE"),
              "key-oneclick": ("bigkey", "below", "ONE CLICK")}
LABEL_AT = {"key-deck": SC.CUE["key"], "key-every": SC.CUE["every"],
            "key-oneclick": SC.CUE["oneclick"]}
HOST_AT = {"deck1": SC.CUE["deck"], "scan": SC.CUE["torch"],
           "bigkey": SC.CUE["bigkey"]}
PRINTED_KEYS = {k: v[2] for k, v in LABEL_PLAN.items()}
PRINTED_LIFETIME = {k: SC.LIFETIMES[k] for k in PRINTED_KEYS}

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.
CUE_WORDS = {
    "deck": (0, "the"), "marks": (2, "accessory"), "shift": (12, "claude"),
    "cctile": (13, "code"), "cable": (16, "combination"), "torch": (21, "you"),
    "ccmark": (27, "claude"), "slide": (31, "look"), "bulb": (34, "every"),
    "fridge": (35, "single"), "tv": (36, "connected"), "every": (37, "device"),
    "lights": (44, "lights,"), "fridgeflip": (46, "fridge,"),
    "tvflip": (47, "anything"), "c2out": (49, "and"), "minis": (51, "map"),
    "arrows": (55, "actions"), "keys": (62, "directly"),
    "deckflip": (67, "buttons."), "c3out": (68, "because"),
    "typing": (74, "telling"), "bigkey": (79, "literally"),
    "press": (81, "clicking"), "outro": (84, "now"),
}
# AUTHORED instants: each inside its own word's 1.0 s LABEL_WINDOW
CUE_INSIDE = {"key": (7, "stream"), "c1out": (20, "deck,"),
              "beam": (32, "around"), "deck2": (49, "and"),
              "prompt": (68, "because"), "oneclick": (81, "clicking")}
# not instants of their own: the step between key marks, the flips' returns
CUE_FREE = ("marks_step", "fridgeback", "tvback")


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
    opening = "the best accessory for claude is the stream deck."
    head = " ".join(w["text"] for w in ws[:9]).lower()
    if head != opening:
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[9:]).lower()
    if "best accessory for claude" in later:
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
        if abs(got - SC.CUE[name]) > 0.011:
            raise SystemExit(f"cue {name}: the scene fires at {SC.CUE[name]}, "
                             f"the word starts at {got}")
        rep[name] = {"word": idx, "text": w["text"], "t": SC.CUE[name]}
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
    if SC.BOARD_MODE != "chapters" or len(SC.BOARD_CHAPTERS) != 4:
        raise SystemExit("the scene is no longer the four chapters the plan "
                         "declared")
    edges = [c["erase_at"] for c in SC.BOARD_CHAPTERS]
    if edges != [SC.CUE["c1out"], SC.CUE["c2out"], SC.CUE["c3out"],
                 SC.CUE["outro"]]:
        raise SystemExit(f"LAW 43: chapter erases {edges} are off their words")
    rep["_law43"] = {"board_mode": SC.BOARD_MODE, "chapters": 4,
                     "erase_at": edges}
    return rep


# every typed key and the spoken words it must agree with
WORD_SYNC = {"key-deck": ((7, 8), "stream deck.", "STREAM DECK"),
             "key-every": ((34, 37), "every single connected device",
                           "EVERY DEVICE"),
             "key-oneclick": ((81, 83), "clicking a button.", "ONE CLICK")}


def assert_word_sync(ws: list[dict]) -> dict:
    """WORD-SYNC: every typed key first shows while its words are said (never
    before the first of them, never later than 1.0 s after the last)."""
    rows = []
    for key, ((i0, i1), spoken, printed) in WORD_SYNC.items():
        got = " ".join(w["text"] for w in ws[i0:i1 + 1]).lower()
        if got != spoken:
            raise SystemExit(f"word-sync: {key} expects {spoken!r}, the take "
                             f"says {got!r}")
        if PRINTED_KEYS[key] != printed:
            raise SystemExit(f"word-sync: {key} prints {PRINTED_KEYS[key]!r}")
        t = LABEL_AT[key]
        lo, hi = float(ws[i0]["start"]), float(ws[i1]["end"]) + LABEL_WINDOW
        if not (lo - 0.01 <= t <= hi):
            raise SystemExit(f"word-sync: {key} first shows at {t}, outside "
                             f"{lo:.3f}-{hi:.3f}")
        rows.append({"state": key, "first_visible_text": printed, "at": t,
                     "words": got, "window": [round(lo, 3), round(hi, 3)]})
    if min(LABEL_AT.values()) != LABEL_AT["key-deck"]:
        raise SystemExit("LAW 9: STREAM DECK is not the first type on the board")
    return {"typed_states": rows, "disagreements": 0, "digits_that_tick": 0}


def assert_law37(ws: list[dict]) -> dict:
    cues = PCUE.scan(ws)
    plan = json.loads(PLAN.read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / "prep/stages/streamdeck.cues.json").read_text())
    if marker["keys"]["cue_count"] != len(cues):
        raise SystemExit("LAW 37: the prep marker disagrees with the re-run")
    if cues or declared:
        raise SystemExit("LAW 37: this scene builds no source card")
    return {"scan_cue_count": 0, "plan_declared_cards": 0,
            "source_cards_in_the_page": 0}


# ------------------------------------------------------------------ laws
def assert_label_law() -> dict:
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    block_of = {"deck1": "deck1", "scan": "beam", "bigkey": "bigkey"}
    out: dict = {}
    for key, (host, side, text) in LABEL_PLAN.items():
        kb, hb = RECTS[key], RECTS[host]
        if kb[1] < hb[3] - 0.01:
            raise SystemExit(f"LAW 39: {key} is not entirely below {host}")
        kc, hc = (kb[0] + kb[2]) / 2, (hb[0] + hb[2]) / 2
        if abs(kc - hc) > 0.15 * (hb[2] - hb[0]) + 0.01:
            raise SystemExit(f"LAW 39: {key} is off {host}'s axis")
        if not any(key in b and block_of[host] in b for b in blocks):
            raise SystemExit(f"LAW 41: {key} is not blocked with {host}")
        if LABEL_AT[key] < HOST_AT[host] - 1e-9:
            raise SystemExit(f"LAW 39: {key} lands before its host")
        out[key] = {"host": host, "side": side, "text": text,
                    "at": LABEL_AT[key],
                    "gutter_core_px": round(kb[1] - hb[3], 1),
                    "axis_off_px": round(kc - hc, 1),
                    "box_canvas": [round(v, 1) for v in canvas(kb)]}
    hs = {round(RECTS[k][3] - RECTS[k][1], 2) for k in ("key-every",
                                                         "key-oneclick")}
    if len(hs) != 1:
        raise SystemExit(f"LAW 50: the plain labels differ in height {hs}")
    out["_law50"] = {"plain_label_font_px": SC.KEY_FS, "row_h": hs.pop()}
    du = SC.KEY_TERM_FS / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} du")
    out["_key_term"] = {"text": SC.KEY_TERM, "font_px": SC.KEY_TERM_FS,
                        "design_units": round(du, 2), "first_type": True}
    return out


# the mark-bearing elements and their windows (LAW 42: < 40 % each)
MARK_WINDOWS = {
    "claude keys, chapter 1": (SC.CUE["marks"], SC.LIFETIMES["deck1"][1]),
    "claude-code tile": SC.LIFETIMES["tile-cc"],
    "claude-code on the flashlight": (SC.CUE["ccmark"],
                                      SC.LIFETIMES["torch"][1]),
    "claude keys, chapter 3": (SC.LIFETIMES["deck2"][0],
                               SC.LIFETIMES["deck2"][1]),
    "claude in the prompt header": SC.LIFETIMES["prompt"],
}


def assert_lifetime_law() -> dict:
    anchors = [n for n, (_a, b) in SC.LIFETIMES.items() if b is None]
    for n in anchors:
        if n not in SC.SCENE_ANCHORS:
            raise SystemExit(f"LAW 42: {n} never leaves and is not an anchor")
    shares = {}
    for n, (a, b) in MARK_WINDOWS.items():
        shares[n] = round((b - a) / DUR, 3)
        if shares[n] > 0.40:
            raise SystemExit(f"LAW 42: {n} is on screen {shares[n]:.0%}")
    for n, (a, b) in SC.LIFETIMES.items():
        if b is not None and (b - a) / DUR > 0.40:
            raise SystemExit(f"LAW 42: {n} lives {(b - a) / DUR:.0%}")
    return {"board_mode": SC.BOARD_MODE, "anchors": sorted(anchors),
            "mark_shares": shares}


# ------------------------------------------------------ LAW 38: emphasis
# (selector-in-emitted-html, new id, target id, check instant, window)
EMPH = [
    ('<path class="fro"', "emph-fridge", "fridge", 14.80,
     (SC.CUE["fridgeflip"] + 0.34, SC.CUE["fridgeback"])),
    ('<path class="tvvo"', "emph-tv", "tv", 15.50,
     (SC.CUE["tvflip"] + 0.34, SC.CUE["tvback"])),
    ('<path class="d2b"', "emph-deck2", "deck2", 21.60,
     (SC.CUE["deckflip"] + 0.34, SC.CUE["c3out"])),
    ('id="bigcap"', "bigcap", "bigkey-face", 26.40,
     (SC.CUE["press"] + 0.30, SC.CUE["outro"])),
]


def assert_emphasis_law() -> dict:
    rows = []
    for _old, eid, tgt, at, (a, b) in EMPH:
        if not (a <= at < b):
            raise SystemExit(f"LAW 38: {eid} is not complete and held at {at}")
        rows.append({"id": eid, "kind": "border", "target": tgt,
                     "check_at": at, "held": [round(a, 2), round(b, 2)]})
    return {"border_flips": rows, "rings_ellipses_circles": 0,
            "highlights": 0,
            "dom_elements_added": 1,
            "note": "the one added element is the inkless virtual rect "
                    "#bigkey-face (the keycap's face)"}


# ------------------------------------------------------ LAW 40: connectors
DECK2_EDGE = (SC.DECK2[0] - SC.DECK_SW / 2, SC.DECK2[1] - SC.DECK_SW / 2,
              SC.DECK2[0] + SC.DECK_W + SC.DECK_SW / 2,
              SC.DECK2[1] + SC.DECK_H + SC.DECK_SW / 2)
CABLE_CHECK_AT = 5.50          # drawn by 5.10, chapter leaves at 5.90
ARROWS_CHECK_AT = 20.90        # heads painted by ~18.32, chapter leaves 21.78


def assert_anchor_law() -> dict:
    out = {}
    # the cable: tile border -> keypad body stroke centre, left side, mid height
    x0, y0, x1, y1 = DECK1_BODY
    frac = (SC.CABLE_Y - y0) / (y1 - y0)
    miss = abs(SC.CABLE_X1 - x0) + abs(SC.CABLE_Y - (y0 + frac * (y1 - y0)))
    if miss > 0.5 or abs(frac - 0.5) > 1e-9:
        raise SystemExit(f"LAW 40: the cable misses the keypad body ({miss})")
    a, b = SC.LIFETIMES["cable"]
    if not (SC.CUE["cable"] + 0.40 <= CABLE_CHECK_AT < SC.CUE["c1out"]):
        raise SystemExit("cable: check-at is not a held instant")
    out["cable"] = {"target": "deck1-body", "side": "left", "fraction": 0.5,
                    "check_at": CABLE_CHECK_AT,
                    "end_core": [SC.CABLE_X1, SC.CABLE_Y], "miss_px": miss}
    # the arrows: three tips on the body's top stroke outer edge, level
    ex0, ey0, ex1, _ = DECK2_EDGE
    fr = []
    for ax, _ay in SC.ANCHORS:
        if abs(SC.ARROW_TIP_Y - ey0) > 0.01:
            raise SystemExit("LAW 40: an arrow tip is off the keypad's top edge")
        fr.append(round((ax - ex0) / (ex1 - ex0), 6))
    if abs(fr[0] + fr[2] - 1.0) > 1e-6 or abs(fr[1] - 0.5) > 1e-6:
        raise SystemExit(f"LAW 40: the arrows are not symmetric {fr}")
    if not (SC.CUE["arrows"] + 0.62 <= ARROWS_CHECK_AT < SC.CUE["c3out"]):
        raise SystemExit("arrows: check-at is not a held instant")
    out["arrows"] = {"target": "deck2-edge", "side": "top",
                     "fraction": fr[0], "fractions_all": fr,
                     "check_at": ARROWS_CHECK_AT,
                     "tips_core": [[round(ax, 1), SC.ARROW_TIP_Y]
                                   for ax, _ in SC.ANCHORS],
                     "level_px": 0.0}
    return out


def _insert_after_svg(s: str, host_id: str, snippet: str) -> str:
    i = s.index(f'id="{host_id}"')
    j = s.index("</svg>", i) + len("</svg>")
    return s[:j] + snippet + s[j:]


def declare_contracts(html: str, anchors: dict) -> tuple[str, dict]:
    s = html
    # -- LAW 30 rail: the big key and its label, 8 px left together
    for eid, box in (("bigkey", SC.BIGKEY), ("key-oneclick", SC.ONECLICK_BOX)):
        old = f'id="{eid}" style="left:{box[0]:.1f}px;'
        alt = f'id="{eid}" style="left:{box[0]:.0f}px;'
        new_x = box[0] + RAIL_DX
        if s.count(old) == 1:
            s = s.replace(old, f'id="{eid}" style="left:{new_x:.1f}px;', 1)
        elif s.count(alt) == 1:
            s = s.replace(alt, f'id="{eid}" style="left:{new_x:.0f}px;', 1)
        else:
            raise SystemExit(f"cannot seat {eid} on the rail")
    # -- virtual rects (inkless), inside the element they belong to
    m = SC.DECK_M
    s = _insert_after_svg(
        s, "deck1", f'<div id="deck1-body" class="abs" style="left:{m:.0f}px;'
        f'top:{m:.0f}px;width:{SC.DECK_W:.0f}px;height:{SC.DECK_H:.0f}px" '
        f'data-virtual-rect></div>')
    hw = SC.DECK_SW / 2
    s = _insert_after_svg(
        s, "deck2", f'<div id="deck2-edge" class="abs" style="left:{m - hw:.0f}px;'
        f'top:{m - hw:.0f}px;width:{SC.DECK_W + 2 * hw:.0f}px;'
        f'height:{SC.DECK_H + 2 * hw:.0f}px" data-virtual-rect></div>')
    cx, cy, cw, ch = SC.CAP
    old = '<div class="abs node" id="bigcap"'
    if s.count(old) != 1:
        raise SystemExit("the module no longer emits ONE big keycap")
    s = s.replace(old, f'<div id="bigkey-face" class="abs" style="left:{cx:.0f}px;'
                       f'top:{cy:.0f}px;width:{cw:.0f}px;height:{ch:.0f}px" '
                       f'data-virtual-rect></div>' + old, 1)
    # -- the connectors
    for cid, old_to, a in (("cable", 'data-connect-to="deck1"', anchors["cable"]),
                           ("arrows", 'data-connect-to="deck2"',
                            anchors["arrows"])):
        if s.count(old_to) != 1:
            raise SystemExit(f"cannot stamp {cid}")
        s = s.replace(old_to, f'data-connect-to="{a["target"]}" '
                              f'data-anchor-side="{a["side"]}" '
                              f'data-anchor-fraction="{a["fraction"]!r}" '
                              f'data-check-at="{a["check_at"]:.2f}"', 1)
    n_heads = s.count('<path class="ah" ')
    if n_heads != 3:
        raise SystemExit(f"expected three arrowheads, found {n_heads}")
    s = s.replace('<path class="ah" ', '<path class="ah ahead" ')
    # -- the emphases
    for old, eid, tgt, at, _w in EMPH:
        if s.count(old) != 1:
            raise SystemExit(f"cannot stamp emphasis {eid} ({old})")
        decl = (f'data-emphasis="border" data-emphasis-target="{tgt}" '
                f'data-check-at="{at:.2f}"')
        if old.startswith("id="):
            s = s.replace(old, f'{old} {decl}', 1)
        else:
            s = s.replace(old, old.replace("<path ", f'<path id="{eid}" {decl} ',
                                           1), 1)
    return s, {"connectors_stamped": 2, "emphases_stamped": len(EMPH),
               "virtual_rects": ["deck1-body", "deck2-edge", "bigkey-face"],
               "arrowheads_classed_ahead": 3,
               "rail_shift_px": {"bigkey": RAIL_DX, "key-oneclick": RAIL_DX}}


def assert_cast_law() -> dict:
    rep = DF.assert_cast_resolves(list(SC.LOGO_FILES), dict(SC.LOGO_FILES),
                                  LOGOS, label="streamdeck stage marks")
    return {"stage_marks": sorted(SC.LOGO_FILES),
            "resolved": {k: v["path"] for k, v in rep.items()},
            "cutout_lanes_not_ours": list(CUTOUT_LANES)}


def _tags_for(sel: str, html: str) -> list[str]:
    """'#id .a.b' -> every tag inside the element id=... up to its </svg>
    whose class list holds a and b."""
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
            sels.update(re.findall(r'tl\.set\("([^"]+)"', t))
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
    rep["proper_nouns"] = "as spoken: 'Claude Code', 'Stream Deck' (handoff 7)"
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
    """The FOUR rasters the scene paints (handoff section 1)."""
    return {
        "_claude_key_img": CC.mark_img(LOGO_URL["claude"], "claude",
                                       SC.MARK_SIDE["key"]),
        "_cc_tile_img": CC.mark_img(LOGO_URL["claude-code"], "claude-code",
                                    SC.MARK_SIDE["tile"]),
        "_cc_torch_img": CC.mark_img(LOGO_URL["claude-code"], "claude-code",
                                     SC.MARK_SIDE["torch"]),
        "_claude_prompt_img": CC.mark_img(LOGO_URL["claude"], "claude",
                                          SC.MARK_SIDE["prompt"]),
    }


def sfx_plan() -> list[tuple]:
    """EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22)."""
    C = SC.CUE
    return [("pop", C["deck"], SFX_STRUCTURE),       # the keypad draws
            ("pop", C["marks"], SFX_DETAIL),         # Claude marks on the keys
            ("click", C["key"], SFX_DETAIL),         # STREAM DECK is written
            ("whoosh", C["shift"], SFX_STRUCTURE),   # the keypad slides right
            ("pop", C["cctile"], SFX_DETAIL),        # the Claude Code tile lands
            ("click", C["cable"], SFX_DETAIL),       # the cable draws
            ("whoosh", C["c1out"], SFX_STRUCTURE),   # chapter 1 leaves
            ("pop", C["ccmark"], SFX_DETAIL),        # the mark on the handle
            ("whoosh", C["slide"], SFX_STRUCTURE),   # the flashlight slides
            ("click", C["beam"], SFX_DETAIL),        # the beam opens
            ("pop", C["bulb"], SFX_DETAIL),          # the bulb is found
            ("pop", C["fridge"], SFX_DETAIL),        # the fridge is found
            ("click", C["every"], SFX_DETAIL),       # EVERY DEVICE
            ("click", C["lights"], SFX_DETAIL),      # the bulb switches on
            ("whoosh", C["c2out"], SFX_STRUCTURE),   # chapter 2 leaves
            ("pop", C["minis"], SFX_DETAIL),         # the three devices pop
            ("click", C["arrows"], SFX_DETAIL),      # the arrows draw down
            ("pop", C["keys"], SFX_DETAIL),          # devices onto the keys
            ("whoosh", C["c3out"], SFX_STRUCTURE),   # chapter 3 leaves
            ("click", C["typing"], SFX_DETAIL),      # the prompt types
            ("pop", C["bigkey"] + 0.06, SFX_STRUCTURE),  # the big key lands
            ("click", C["press"], SFX_STRUCTURE),    # the key is pressed
            ("whoosh", C["outro"], SFX_STRUCTURE)]   # the rising sheet


def assert_sfx(sfx) -> dict:
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30:
        raise SystemExit(f"SFX flam: {worst}")
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "deliberately_silent": {
                "torch 6.08": "0.18 s after the chapter whoosh",
                "tv 10.52": "0.28 s after the fridge pop; one pop per arrival "
                            "would flam",
                "prompt 21.84": "0.06 s after the chapter whoosh",
                "ONE CLICK 25.80": "0.12 s after the press click",
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
        fs, ls = ((SC.KEY_TERM_FS, SC.KEY_TERM_LS) if n == "key-deck"
                  else (SC.KEY_FS, SC.KEY_LS))
        ink = len(text) * 0.6 * fs + (len(text) - 1) * ls
        rights[n] = round((b[0] + b[2]) / 2 + ink / 2, 1)
    type_right = max(rights.values())
    if type_right > CAP.LAW12_RAIL_X + 0.01:
        raise SystemExit(f"readable key ink reaches x={type_right:.1f}")
    boxes = [canvas(o["core"]) for o in SC.BESPOKE + SC.UI_OBJECTS]
    ink_left = min(b[0] for b in boxes)
    ink_right = max(b[2] for b in boxes)
    return {"readable_type_right_x": rights,
            "ink_left_x": ink_left, "ink_right_x": ink_right,
            "law30_rail_x": CAP.LAW12_RAIL_X}


PHONE_BOX = {  # the four bespoke objects as PAINTED in this page (core px)
    # held at 2.60, BEFORE the 3.30 slide: still centred on 540
    "Claude button keypad": SC.BESPOKE[0]["core"],
    "flashlight finding devices": (SC.BESPOKE[1]["core"][0],
                                   SC.BESPOKE[1]["core"][1], 1066.0,
                                   SC.BESPOKE[1]["core"][3]),
    "devices wired to keypad": SC.BESPOKE[2]["core"],
    "pressed light button": _dx(SC.BESPOKE[3]["core"], RAIL_DX),
}


def phone_objects() -> list[dict]:
    out = []
    for o in SC.BESPOKE:
        x0, y0, x1, y1 = canvas(PHONE_BOX[o["name"]])
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
           "law42": assert_lifetime_law(), "law38": assert_emphasis_law(),
           "law2": assert_cast_law()}
    SFX = sfx_plan()
    rep["law22"] = assert_sfx(SFX)

    scene_html, tweens = SC.build(media(), outro_lockup(handle))
    rep["draw_on"] = assert_draw_on(tweens, scene_html)
    rep["law40"] = assert_anchor_law()
    scene_html, rep["declared"] = declare_contracts(scene_html, rep["law40"])
    if scene_html.count("data-connect-to") != 2:
        raise SystemExit("the scene does not carry exactly two connectors")
    if (scene_html.count("data-connect-to") + scene_html.count("data-emphasis=")
            != scene_html.count("data-check-at")):
        raise SystemExit("a connector or emphasis is missing its check instant")
    for shape in ("<circle", "<ellipse"):
        if shape in scene_html:
            raise SystemExit(f"LAW 38 rule 3: {shape} in the emitted scene")
    for key, (host, _s, _t) in LABEL_PLAN.items():
        if scene_html.count(f'data-label-for="{host}"') != 1:
            raise SystemExit(f"{key} does not declare its host {host}")

    m = CAP.PillMeasurer(RUN / "gen/_pillwidths_streamdeck_split.json")
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
    rep.update({"staged": staged, "beats": beats, "seat": SEAM,
                "scale": CORE_K, "core": {"left": LEFT, "top": CORE_TOP_SPLIT},
                "band": band, "rail": rail, "transcript": cap_rep,
                "phone_objects": objs, "render": {"w": 1080, "h": 1920,
                                                  "zoom": 1}})
    return rep


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="split", choices=("split",))
    ap.parse_args()
    dst = RUN / "projects/streamdeck_split"
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
    (RUN / "gen/_build_streamdeck_split.json").write_text(
        json.dumps(report, indent=1, default=str))
    geom = {"video": VID, "fps": FPS, "duration": DUR,
            "shared": {"beat_edges": SC.BEAT_EDGES},
            "formats": {"split": {"phone_objects": rep["phone_objects"],
                                  "core": rep["core"], "scale": rep["scale"],
                                  "seat": rep["seat"]}}}
    (RUN / f"gen/_geom_{VID}_split.json").write_text(json.dumps(geom, indent=1))
    print(f"split: {dst}")
    print(json.dumps({"captions": rep["captions"], "band": rep["band"],
                      "rail": rep["rail"], "law40": rep["law40"],
                      "declared": rep["declared"],
                      "law22": rep["law22"]["tightest_gap_s"],
                      "phone": rep["phone_objects"]}, indent=1))


if __name__ == "__main__":
    main()
