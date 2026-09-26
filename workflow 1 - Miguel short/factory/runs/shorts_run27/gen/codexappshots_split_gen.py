#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION - codexappshots / ICON CHOREOGRAPHY.

    YouTube   classic split 50/50   projects/codexappshots_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/codexappshots_scene.py`
plus `plans/codexappshots_scene_handoff.md` are the design agent's artefacts,
sealed by `review/artwork_pass_codexappshots.json` (production v4,
`production.py seal`).  This file IMPORTS the module and SEATS it at the
handoff's own placement (k = 1.00, left 0, core top 192).  It never mutates a
byte of the module on disk.

FORMAT-SIDE STAMPS ON THE EMITTED STRING (the module on disk is untouched):
  * the one connector (`#c1-line`, already `data-connect-to="c1-codex"`) gets
    `data-anchor-side="left"`, `data-anchor-fraction="0.5"` and
    `data-check-at` (production's LAW 40 contract);
  * the three border flips (LAW 38 rule 2, all on DRAWN objects) are declared
    `data-emphasis="border"` with their target and check instant: each command
    keycap's own `.kcap` outline (-> `key-cmd-l` / `key-cmd-r`) and the laptop
    screen bezel `#c4-laptop-screen` (-> `c4-laptop`).

ONE FORMAT-SIDE REPAIR, LAW 30 (logged in `plans/codexappshots_split_notes.md`):
  * DESKTOP APP, centred under the Codex window at x 840, puts readable ink
    to x ~938 at canvas y 586-630, inside the right-rail column (x > 918,
    y 30-95 %).  The label is moved 22 px left (centre 818, ink right ~916),
    still inside LAW 39's +-15 % band under its 360 px window.

HD DELIVERY: authored AND encoded 1080x1920.  The face plate is
`face_bottom_hd.mp4` (1080x1058), so the seam is 1920 - 1057.5 = 862.5 and the
RENDERING pill top is 862.5 - 114.59/2 = 805.205.  The core's content band
108..520 lands at canvas 300..712: 108 px under LAW 30's top-10 % line and
93.2 px over the pill.

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
import codexappshots_scene as SC                # noqa: E402

RUN = Path(__file__).resolve().parents[1]
CUT = RUN / "cuts/codexappshots"
PLAN = RUN / "plans/codexappshots_plan.json"
ASSETS = Path.home() / "Documents/Workspace/assets"
LOGOS = ASSETS / "logos"
LIB_MUSIC = ASSETS / "audio/music/shorts-factory"
LIB_SFX = ASSETS / "audio/sfx/shorts-factory"

VID = "codexappshots"
W, H = 1080.0, 1920.0
FPS = 25
DUR = SC.DUR                                     # 34.12, the cut master

SEAM = 862.5
CORE_TOP_SPLIT = SC.CANVAS_OFFSET                # 192.0, the handoff's number
CORE_K = 1.00
LEFT = (W - SC.CORE_W * CORE_K) / 2              # 0.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "Codex Appshots: stop switching between apps"
LABEL_WINDOW = 1.0

# ------------------------------------------------------------------ marks
STAGE_FILES = {k: f"logos/{v}" for k, v in SC.LOGO_FILES.items()}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}
MEDIA_SIDES = {"_chatgpt_img": ("chatgpt", SC.MARK_SIDE),
               "_codex_img": ("codex", SC.MARK_SIDE),
               "_codex1_img": ("codex", SC.MARK_SIDE),
               "_codex4_img": ("codex", SC.MARK_SIDE),
               "_codex_title_img": ("codex", SC.TITLE_MARK_SIDE)}
CUTOUT_LANES = SC.CUTOUT_LOGO_LANES

# ------------------------------------------------------------------ LAW 30
APP_KEY_SHIFT = -22.0      # DESKTOP APP out of the right rail (see docstring)


def _b(x, y, w, h) -> tuple:
    return (x, y, x + w, y + h)


C = SC.CUE
TILE = SC.TILE
APP_BOX = (SC.APP_KEY_BOX[0] + APP_KEY_SHIFT, *SC.APP_KEY_BOX[1:])
# CORE px boxes at their SETTLED seats
RECTS: dict[str, tuple] = {
    "top-hat": SC.HAT_BOX,
    "hat-wand": (SC.WAND_DIV[0], SC.WAND_DIV[1], SC.WAND_DIV[0] + SC.WAND_DIV[2],
                 SC.WAND_DIV[1] + SC.WAND_DIV[3]),
    "tile-chatgpt": (SC.CHATGPT_TILE[0], SC.CHATGPT_TILE[1],
                     SC.CHATGPT_TILE[0] + TILE, SC.CHATGPT_TILE[1] + TILE),
    "tile-codex": (SC.CODEX_TILE[0], SC.CODEX_TILE[1],
                   SC.CODEX_TILE[0] + TILE, SC.CODEX_TILE[1] + TILE),
    "key-appshots": _b(*SC.KEY_TERM_BOX),
    "c1-laptop": (SC.LAPTOP1_X, SC.LAPTOP_Y, SC.LAPTOP1_X + SC.LAPTOP_W,
                  SC.LAPTOP_Y + SC.LAPTOP_H),
    "c1-codex": (SC.C1_TILE[0], SC.C1_TILE[1], SC.C1_TILE[0] + TILE,
                 SC.C1_TILE[1] + TILE),
    "trail": SC.TRAIL_BOX,
    "key-assistant": _b(*SC.ASSIST_KEY_BOX),
    "cmd-keys": SC.KEYROW_BOX,
    "key-keys": _b(*SC.KEYS_KEY_BOX),
    "c4-laptop": (SC.LAPTOP1_X, SC.LAPTOP_Y, SC.LAPTOP1_X + SC.LAPTOP_W,
                  SC.LAPTOP_Y + SC.LAPTOP_H),
    "polaroid": SC.BESPOKE[3]["core"],
    "key-shot": _b(*SC.SHOT_KEY_BOX),
    "c4-codex": (SC.C4_TILE[0], SC.C4_TILE[1], SC.C4_TILE[0] + TILE,
                 SC.C4_TILE[1] + TILE),
    "codex-window": SC.WINDOW_BOX,
    "key-app": _b(*APP_BOX),
    "piggy-bank": SC.PIG_BOX,
    "key-time": _b(*SC.TIME_KEY_BOX),
}
# (alone dx, the displacement's start, its duration): the chapter-4 laptop
# opens CENTRED and steps 300 px left on 'screenshot'
ALONE = {"c4-laptop": (-SC.LAPTOP2_DX, C["snap"] + 0.06, 0.40)}
LIFE = {n: SC.LIFETIMES[n] for n in RECTS}


def moving(name: str, t: float) -> bool:
    if name not in ALONE:
        return False
    _dx, t0, d = ALONE[name]
    return t0 - 1e-9 <= t < t0 + d


def rect_at(name: str, t: float) -> tuple:
    b = RECTS[name]
    if name in ALONE:
        dx, t0, _d = ALONE[name]
        if t < t0:
            return (b[0] + dx, b[1], b[2] + dx, b[3])
    return b


def canvas(box):
    """core px -> the canvas this page actually paints (top 192, k 1.00)."""
    return (CORE_K * box[0] + LEFT, CORE_TOP_SPLIT + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP_SPLIT + CORE_K * box[3])


# --------------------------------------------------------------- label plan
# LAW 39 / LAW 9 / LAW 50: every name BELOW what it names.
LABEL_PLAN = {"key-appshots": ("top-hat", "below", SC.KEY_TERM),
              "key-assistant": ("c1-codex", "below", "AI ASSISTANT"),
              "key-keys": ("cmd-keys", "below", "TWO COMMAND KEYS"),
              "key-shot": ("polaroid", "below", "SCREENSHOT"),
              "key-app": ("codex-window", "below", "DESKTOP APP"),
              "key-time": ("piggy-bank", "below", "MORE TIME")}
LABEL_AT = {k: SC.LIFETIMES[k][0] for k in LABEL_PLAN}
PRINTED_KEYS = {k: v[2] for k, v in LABEL_PLAN.items()}
PRINTED_LIFETIME = {k: SC.LIFETIMES[k] for k in LABEL_PLAN}

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.
CUE_WORDS = {
    "hat": (0, "here"), "wand": (3, "simple"), "trick": (4, "trick"),
    "chatgpt": (16, "chatgpt"), "codex": (19, "codex"), "c1out": (25, "you"),
    "walk1": (30, "switch"), "walk2": (32, "where"), "line": (37, "give"),
    "assistant": (46, "assistant"), "c2out": (47, "simply"),
    "two": (51, "two"), "press": (52, "command"), "keysback": (56, "keyboard"),
    "c3out": (57, "and"), "snap": (62, "screenshot"), "send": (72, "send"),
    "open": (78, "open"), "c4out": (84, "meaning"), "coin1": (90, "save"),
    "coin2": (92, "more"), "outro": (102, "now"),
}
# AUTHORED instants, each inside its own word's window (start .. end + 1.0 s)
CUE_INSIDE = {"sparkout": (14, "work"), "appshots": (23, "appshots"),
              "laptop1": (25, "you"), "codex1": (27, "longer"),
              "fpout": (35, "from"), "keys": (47, "simply"),
              "keylbl": (53, "keys"), "laptop2": (57, "and"),
              "photo": (62, "screenshot"), "shotlbl": (62, "screenshot"),
              "bezelback": (62, "screenshot"), "fly": (72, "send"),
              "applbl": (81, "application"), "piggy": (84, "meaning"),
              "timelbl": (93, "time")}


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
    opening = "here is one simple trick that is going to change"
    head = " ".join(w["text"] for w in ws[:10]).lower()
    if head != opening:
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[10:]).lower()
    if "one simple trick" in later or "here is one" in later:
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
           + f" - {tail:.3f}s past the last word against a {cap:.3f}s cap",
           "law46": "the scripted opening occurs ONCE inside the keeper take, "
                    "at word 0 / 0.10 s",
           "take_corroboration": {
               "mode": td.get("mode"), "keep_words": td.get("keep_words"),
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
                             f"{text!r} - the cut moved")
        got = round(float(w["start"]), 3)
        if abs(got - C[name]) > 0.011:
            raise SystemExit(f"cue {name}: the scene fires at {C[name]}, "
                             f"the word starts at {got}")
        rep[name] = {"word": idx, "text": w["text"], "t": C[name]}
    for name, (idx, text) in CUE_INSIDE.items():
        w = ws[idx]
        if _norm(w["text"]) != text:
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
    if SC.BOARD_MODE != "chapters" or len(SC.BOARD_CHAPTERS) != 5:
        raise SystemExit("the scene is no longer the five chapters the plan "
                         "declared")
    rep["_law43"] = {"board_mode": SC.BOARD_MODE, "chapters": 5,
                     "edges": list(SC.BEAT_EDGES)}
    return rep


def assert_word_sync(ws: list[dict]) -> dict:
    """WORD-SYNC: every typed key first shows the value its word says, and
    never before the LAST word it names has started (LAW 24)."""
    rows = []
    checks = [  # (state, first visible text, word idx, the last word it names)
        ("key-appshots", SC.KEY_TERM, 23, "appshots"),
        ("key-assistant", "AI ASSISTANT", 46, "assistant"),
        ("key-keys", "TWO COMMAND KEYS", 53, "keys"),
        ("key-shot", "SCREENSHOT", 62, "screenshot"),
        ("key-app", "DESKTOP APP", 81, "application"),
        ("key-time", "MORE TIME", 93, "time"),
    ]
    for state, text, idx, word in checks:
        t = LABEL_AT[state]
        w = ws[idx]
        if _norm(w["text"]) != word:
            raise SystemExit(f"word-sync: {state} expects {word!r} at word {idx}")
        lo, hi = float(w["start"]), float(w["end"]) + LABEL_WINDOW
        if not (lo - 0.011 <= t <= hi):
            raise SystemExit(f"word-sync: {state} first shows at {t}, outside "
                             f"{lo:.3f}-{hi:.3f}")
        rows.append({"state": state, "first_visible_text": text, "at": t,
                     "word": w["text"], "word_window": [round(lo, 3), round(hi, 3)]})
    if min(LABEL_AT.values()) != LABEL_AT["key-appshots"]:
        raise SystemExit("LAW 9: APPSHOTS is not the first type on the board")
    # 'TWO' is typed once, on 'keys', after 'two' was spoken (14.90)
    if not ws[51]["start"] <= LABEL_AT["key-keys"]:
        raise SystemExit("word-sync: TWO is typed before 'two'")
    return {"typed_states": rows, "disagreements": 0, "digits_that_tick": 0,
            "numbers_typed": 0, "count_words_typed": ["TWO (said 14.90, typed 15.72)"]}


def assert_law37(ws: list[dict]) -> dict:
    cues = PCUE.scan(ws)
    plan = json.loads(PLAN.read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / "prep/stages/codexappshots.cues.json").read_text())
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
    pairs = [tuple(b) for b in plan["blocks"]] + [tuple(b) for b in SC.DECLARED_BLOCKS]
    groups: list[set] = []
    for p in pairs:
        s = set(p)
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
        t = LABEL_AT[key] + 0.5
        if moving(host, t):
            t = ALONE[host][1] + ALONE[host][2] + 0.01
        kb, hb = rect_at(key, t), rect_at(host, t)
        if side == "below" and kb[1] < hb[3] - 0.01:
            raise SystemExit(f"LAW 39: {key} is not entirely below {host}")
        kc, hc = (kb[0] + kb[2]) / 2, (hb[0] + hb[2]) / 2
        if abs(kc - hc) > 0.15 * (hb[2] - hb[0]):
            raise SystemExit(f"LAW 39: {key} is off {host}'s axis by {kc - hc:.2f}")
        if not any({key, host} <= g for g in groups):
            raise SystemExit(f"LAW 41: {key} is not blocked with {host}")
        if LABEL_AT[key] < LIFE[host][0] - 1e-9:
            raise SystemExit(f"LAW 39: {key} lands before its host")
        out[key] = {"host": host, "side": side, "text": text, "at": LABEL_AT[key],
                    "axis_offset_px": round(kc - hc, 2),
                    "band_px": round(0.15 * (hb[2] - hb[0]), 1),
                    "box_canvas": [round(v, 1) for v in canvas(kb)]}
    out["_law50"] = {"below": list(LABEL_PLAN), "font_px": SC.KEY_FS,
                     "key_term_font_px": SC.KEY_TERM_FS}
    du = SC.KEY_TERM_FS / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} du")
    out["_key_term"] = {"text": SC.KEY_TERM, "font_px": SC.KEY_TERM_FS,
                        "design_units": round(du, 2), "first_type": True}
    return out


def assert_lifetime_law() -> dict:
    grounds = set(SC.SCENE_ANCHORS)
    for n, (a, b) in SC.LIFETIMES.items():
        if b is None:
            if n not in grounds:
                raise SystemExit(f"LAW 42: {n} never leaves and is not an anchor")
            continue
        if b <= a:
            raise SystemExit(f"LAW 42: {n} has an empty window")
        if (b - a) / DUR > 0.40:
            raise SystemExit(f"LAW 42: {n} is on screen {(b - a) / DUR:.0%}")
    finite = {n: v for n, v in SC.LIFETIMES.items() if v[1] is not None}
    longest = max(finite.items(), key=lambda kv: kv[1][1] - kv[1][0])
    return {"board_mode": SC.BOARD_MODE, "anchors": sorted(grounds),
            "longest": {"mark": longest[0], "window": longest[1],
                        "share": round((longest[1][1] - longest[1][0]) / DUR, 3)}}


SPACING_TIMES = (1.2, 2.5, 4.0, 5.6, 7.0, 7.9, 9.0, 10.1, 11.5, 13.2, 14.4,
                 16.0, 17.2, 18.2, 19.2, 20.4, 21.2, 22.6, 24.4, 25.6, 26.1,
                 27.6, 29.5)


def assert_spacing_law() -> dict:
    """LAW 41 on the co-alive seats at settled instants."""
    groups = _groups()

    def alive(n, t):
        a, b = LIFE[n]
        return a <= t < b

    worst = (1e9, None)
    pairs = 0
    for t in SPACING_TIMES:
        live = [n for n in RECTS if alive(n, t) and not moving(n, t)]
        for i in range(len(live)):
            for j in range(i + 1, len(live)):
                a, b = live[i], live[j]
                if any({a, b} <= g for g in groups):
                    continue
                pairs += 1
                ax0, ay0, ax1, ay1 = rect_at(a, t)
                bx0, by0, bx1, by1 = rect_at(b, t)
                dx = max(bx0 - ax1, ax0 - bx1, 0.0)
                dy = max(by0 - ay1, ay0 - by1, 0.0)
                g = (dx * dx + dy * dy) ** 0.5
                if dx <= 0 and dy <= 0:
                    raise SystemExit(f"LAW 41: {a} and {b} overlap at t={t}")
                if g < worst[0]:
                    worst = (g, (a, b, t))
    if worst[1] is not None and worst[0] < GUTTER_REFUSE:
        raise SystemExit(f"LAW 41: {worst[1]} is {worst[0]:.2f}px apart")
    return {"cross_block_pairs": pairs,
            "tightest_core_px": None if worst[1] is None else round(worst[0], 2),
            "tightest_pair": None if worst[1] is None else list(worst[1]),
            "refusal_line": GUTTER_REFUSE,
            "within_block_tightest_by_design": {
                "APPSHOTS to brim": 32, "tile bottoms to crown": 36,
                "label gutters": 28},
            "blocks": [sorted(g) for g in groups]}


# LAW 38 rule 2: three border flips, each on a DRAWN object, each held to its
# chapter step.  (stamp key, stamp attr, target, flip cue, flip dur, check, until)
EMPH = {
    "cmd-l": {"match": '<rect class="kl kcap"', "target": "key-cmd-l",
              "flip": C["two"], "d": 0.30, "check_at": 16.20,
              "until": C["keysback"]},
    "cmd-r": {"match": '<rect class="kr kcap"', "target": "key-cmd-r",
              "flip": C["two"], "d": 0.30, "check_at": 16.20,
              "until": C["keysback"]},
    "bezel": {"match": 'id="c4-laptop-screen"', "target": "c4-laptop",
              "flip": C["snap"], "d": 0.20, "check_at": 19.30,
              "until": C["bezelback"]},
}


def assert_emphasis_law() -> dict:
    for name, e in EMPH.items():
        if not (e["flip"] + e["d"] <= e["check_at"] < e["until"]):
            raise SystemExit(f"LAW 38: the {name} flip is not complete and held "
                             f"at {e['check_at']}")
    # the keys press 15.28-15.70; the laptop slides 18.50-18.90: check after
    if not EMPH["cmd-l"]["check_at"] > C["press"] + 0.42:
        raise SystemExit("LAW 38: the keycap check lands inside the press")
    if not EMPH["bezel"]["check_at"] > ALONE["c4-laptop"][1] + ALONE["c4-laptop"][2]:
        raise SystemExit("LAW 38: the bezel check lands inside the laptop's step")
    return {"border_flips": [{"on": e["match"], "kind": "border",
                              "target": e["target"], "check_at": e["check_at"],
                              "held": [e["flip"], e["until"]]}
                             for e in EMPH.values()],
            "rings_ellipses_circles": 0, "highlights": 0, "dom_ink_added": 0}


def assert_anchor_law() -> dict:
    """LAW 40: the one connector is level and lands on the Codex tile's
    left-edge centre at the settled instant after it has drawn."""
    tile = RECTS["c1-codex"]
    at = 11.40
    drawn = C["line"] + 0.50
    if not (drawn <= at < SC.LIFETIMES["c1-line"][1] - SC.EXIT_D):
        raise SystemExit("LAW 40: c1-line check is not a completed state")
    if abs(SC.LINE_X1 - tile[0]) > 0.01:
        raise SystemExit("LAW 40: c1-line misses the tile's left edge")
    if abs(SC.LINE_Y - (tile[1] + tile[3]) / 2) > 0.01:
        raise SystemExit("LAW 40: c1-line misses the tile's centre height")
    scr = SC.laptop_screen_box(SC.LAPTOP1_X)
    if abs(SC.LINE_X0 - scr[2]) > 0.01:
        raise SystemExit("LAW 40: c1-line does not start on the bezel's edge")
    return {"c1-line": {"to": "c1-codex", "side": "left", "fraction": 0.5,
                        "check_at": at, "from_core": [SC.LINE_X0, SC.LINE_Y],
                        "to_core": [SC.LINE_X1, SC.LINE_Y],
                        "ink": "round caps end on 370 and 784 (handoff: 0.0 px "
                               "gap / overshoot)"}}


def assert_cast_law() -> dict:
    rep = DF.assert_cast_resolves(list(SC.LOGO_FILES), dict(SC.LOGO_FILES),
                                  LOGOS, label="codexappshots stage marks")
    return {"stage_marks": sorted(SC.LOGO_FILES),
            "resolved": {k: v["path"] for k, v in rep.items()},
            "media_sides_core_px": {k: v[1] for k, v in MEDIA_SIDES.items()},
            "cutout_lanes_not_ours": list(CUTOUT_LANES)}


SHAPE_TAG = re.compile(r'<(?:path|rect|line|polyline|polygon)\b[^>]*>')


def assert_draw_on(tweens: list[str], html: str) -> dict:
    """THE DRAW-ON DASH LAW: every dash-revealed selector resolves ONLY to
    shapes that declare pathLength="100"."""
    sels = set()
    for t in tweens:
        if "strokeDasharray:100" in t:
            sels.update(re.findall(r'tl\.set\("([^"]+)"', t))
    shapes = SHAPE_TAG.findall(html)
    checked = {}
    for sel in sorted(sels):
        n = 0
        for part in sel.split(","):
            cls = part.strip().split()[-1]
            if not cls.startswith("."):
                raise SystemExit(f"unexpected dash selector {sel}")
            c = cls[1:]
            tags = [p for p in shapes
                    if re.search(rf'class="[^"]*\b{re.escape(c)}\b', p)]
            if not tags or not all('pathLength="100"' in p for p in tags):
                raise SystemExit(f"DRAW-ON: {sel} reveals a shape without "
                                 'pathLength="100"')
            n += len(tags)
        checked[sel] = n
    return {"dash_selectors": checked, "verdict": "every dash equals its "
            "shape's declared length (100)"}


def declare_contracts(html: str, anchors: dict) -> tuple[str, dict]:
    s = html
    stamped = []
    for name, e in EMPH.items():
        key = e["match"]
        if s.count(key) != 1:
            raise SystemExit(f"cannot stamp {name}: {s.count(key)} matches")
        s = s.replace(key, f'{key} data-emphasis="border" '
                           f'data-emphasis-target="{e["target"]}" '
                           f'data-check-at="{e["check_at"]:.2f}"', 1)
        stamped.append(name)
    for cid, a in anchors.items():
        key = f'id="{cid}"'
        if s.count(key) != 1:
            raise SystemExit(f"cannot stamp {cid}")
        s = s.replace(key, f'{key} data-anchor-side="{a["side"]}" '
                           f'data-anchor-fraction="{a["fraction"]:g}" '
                           f'data-check-at="{a["check_at"]:.2f}"', 1)
    # LAW 30: DESKTOP APP out of the right rail
    old = f'id="key-app" style="left:{SC.APP_KEY_BOX[0]:.0f}px;'
    if s.count(old) != 1:
        raise SystemExit("the module no longer emits DESKTOP APP where the "
                         "handoff says")
    s = s.replace(old, f'id="key-app" style="left:{APP_BOX[0]:.0f}px;', 1)
    return s, {"connectors_stamped": len(anchors), "emphases_stamped": stamped,
               "law30_moves": {"key-app": APP_KEY_SHIFT}}


# ------------------------------------------------------------------ captions
def phrases(ws: list[dict]) -> list[list[dict]]:
    out, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w)
        end = w["text"].strip().rstrip('"').endswith((".", "!", "?"))
        comma = w["text"].strip().endswith(",")
        gap = (ws[i + 1]["start"] - w["end"]) if i + 1 < len(ws) else 9.0
        if end or gap >= 0.295 or (comma and gap >= 0.25) or len(cur) >= 30:
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
# a pill never splits a product name or the instruction's noun phrase
NO_BREAK = {("chatgpt", "work"), ("two", "command"), ("command", "keys"),
            ("desktop", "application"), ("ai", "news")}


def _breakable(union, j) -> bool:
    if j <= 0 or j >= len(union):
        return True
    return (_norm(union[j - 1]["text"]), _norm(union[j]["text"])) not in NO_BREAK


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
            if not _breakable(union, j):
                continue
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
    # a phrase that IS a live board key (LAW 4) joins the phrase after it
    groups: list[list] = []
    for g in phrases(ws):
        if groups and _joined(groups[-1]).strip().lower() in forbidden:
            groups[-1] = groups[-1] + g
        else:
            groups.append(g)
    parts: list[list] = []
    for group in groups:
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
    """The five rasters the scene paints (handoff section 1), each sized by
    INK."""
    return {mkey: CC.mark_img(LOGO_URL[key], key, side)
            for mkey, (key, side) in MEDIA_SIDES.items()}


def sfx_plan() -> list[tuple]:
    """EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22)."""
    return [("pop", C["hat"], SFX_STRUCTURE),          # the hat lands
            ("click", C["trick"], SFX_DETAIL),         # the wand taps
            ("pop", C["chatgpt"], SFX_DETAIL),         # ChatGPT out of the hat
            ("pop", C["codex"], SFX_DETAIL),           # Codex out of the hat
            ("click", C["appshots"], SFX_DETAIL),      # APPSHOTS
            ("whoosh", C["c1out"], SFX_STRUCTURE),     # chapter 1 leaves
            ("pop", C["codex1"], SFX_DETAIL),          # the Codex tile lands
            ("click", C["walk1"], SFX_DETAIL),         # the walk out
            ("click", C["walk2"], SFX_DETAIL),         # the walk back
            ("click", C["line"], SFX_DETAIL),          # the line draws
            ("click", C["assistant"], SFX_DETAIL),     # AI ASSISTANT
            ("whoosh", C["c2out"], SFX_STRUCTURE),     # chapter 2 leaves
            ("click", C["press"], SFX_DETAIL),         # both keys press
            ("click", C["keylbl"], SFX_DETAIL),        # TWO COMMAND KEYS
            ("whoosh", C["c3out"], SFX_STRUCTURE),     # chapter 3 leaves
            ("click", C["snap"], SFX_DETAIL),          # the shutter
            ("click", C["shotlbl"], SFX_DETAIL),       # SCREENSHOT
            ("whoosh", C["fly"], SFX_STRUCTURE),       # the photo flies
            ("pop", C["fly"] + 0.52, SFX_DETAIL),      # absorbed, the tile bumps
            ("pop", C["open"] + 0.04, SFX_DETAIL),     # the app window opens
            ("click", C["applbl"], SFX_DETAIL),        # DESKTOP APP
            ("whoosh", C["c4out"], SFX_STRUCTURE),     # chapter 4 leaves
            ("pop", C["coin1"], SFX_DETAIL),           # clock coin 1
            ("pop", C["coin2"], SFX_DETAIL),           # clock coin 2
            ("click", C["timelbl"], SFX_DETAIL),       # MORE TIME
            ("whoosh", C["outro"], SFX_STRUCTURE)]     # the rising sheet


def assert_sfx(sfx) -> dict:
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30:
        raise SystemExit(f"SFX flam: {worst}")
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "deliberately_silent": {
                "sparkles 0.94": "the wand's tap already scores them",
                "flip 14.90 / bezel 18.44": "a colour flip is not an arrival",
                "polaroid out 18.70": "0.26 s after the shutter click",
                "Codex tile 21.34": "0.16 s before the fly's whoosh",
                "coin drops 26.16 / 26.98": "the coin's arrival is scored"}}


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
    """LAW 30: readable key ink stays out of the right 15 % column between
    y 30 % and 95 %.  JetBrains Mono advances 0.600 em."""
    rows = {}
    for n, (_h, _s, text) in LABEL_PLAN.items():
        b = canvas(rect_at(n, LABEL_AT[n] + 0.5))
        if n == "key-appshots":
            fs, ls = SC.KEY_TERM_FS, SC.KEY_TERM_LS
        else:
            fs, ls = SC.KEY_FS, SC.KEY_LS
        ink = len(text) * 0.6 * fs + (len(text) - 1) * ls
        right = (b[0] + b[2]) / 2 + ink / 2
        in_band = b[3] > 0.30 * H + 0.01 and b[1] < 0.95 * H
        rows[n] = {"ink_right_x": round(right, 1), "box_y": [b[1], b[3]],
                   "in_rail_band": in_band}
        if in_band and right > CAP.LAW12_RAIL_X + 0.01:
            raise SystemExit(f"LAW 30: {n} ink reaches x={right:.1f} inside the "
                             "right rail")
    boxes = [canvas(rect_at(n, t)) for n in RECTS for t in SPACING_TIMES
             if LIFE[n][0] <= t < LIFE[n][1]]
    ink_left = min(b[0] for b in boxes)
    ink_right = max(b[2] for b in boxes)
    if ink_left < 40 or W - ink_right < 40:
        raise SystemExit("the composition leaves the 40 px frame margin")
    return {"labels": rows, "ink_left_x": round(ink_left, 1),
            "ink_right_x": round(ink_right, 1),
            "law30_rail_x": CAP.LAW12_RAIL_X,
            "law30_band_y": [0.30 * H, 0.95 * H]}


def phone_objects() -> list[dict]:
    out = []
    for o in SC.BESPOKE:
        x0, y0, x1, y1 = canvas(o["core"])
        out.append({"name": o["name"], "t": o["t"],
                    "bbox": [round(x0 / W, 4), round(y0 / H, 4),
                             round(x1 / W, 4), round(y1 / H, 4)],
                    "canvas": [round(v, 1) for v in (x0, y0, x1, y1)]})
    plan = {o["name"]: o["bbox"] for o in json.loads(PLAN.read_text())["bespoke_objects"]}
    for o in out:
        pb = plan.get(o["name"])
        if pb is None or max(abs(a - b) for a, b in zip(pb, o["bbox"])) > 0.002:
            raise SystemExit(f"phone box for {o['name']} disagrees with the plan")
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
    for key in LABEL_PLAN:
        if f'id="{key}"' not in scene_html:
            raise SystemExit(f"{key} is missing from the scene")

    m = CAP.PillMeasurer(RUN / "gen/_pillwidths_codexappshots.json")
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
    dst = RUN / "projects/codexappshots_split"
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
    (RUN / "gen/_build_codexappshots_split.json").write_text(
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
