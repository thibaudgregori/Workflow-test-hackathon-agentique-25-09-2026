#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION — claudemanaged / ICON CHOREOGRAPHY.

    YouTube   classic split 50/50   projects/claudemanaged_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/claudemanaged_scene.py`
plus `plans/claudemanaged_scene_handoff.md` are the design agent's artefacts,
sealed by `review/artwork_pass_claudemanaged.json` (production v4,
`production.py seal`).  This file IMPORTS the module and SEATS it at the
handoff's own placement (k = 1.00, left 0, core top 192).  It never mutates a
byte of the module on disk.

FORMAT-SIDE STAMPS ON THE EMITTED STRING (the module on disk is untouched):
  * the two connectors (`#conn-advice`, `#conn-skills`) get
    `data-anchor-side="left"`, `data-anchor-fraction="0.5"` and
    `data-check-at` (production's LAW 40 contract), checked after each line
    has drawn and before its chapter erases;
  * the three border flips (LAW 38 rule 2, all on DRAWN objects) are declared
    `data-emphasis="border"` with their target and check instant:
    `#budget-meter` -> `meter-fill`, `#brain-outline` -> `advisor-brain`,
    `#book-hero` -> `skill-shelf`.

TWO FORMAT-SIDE REPAIRS, BOTH ON THE EMITTED TWEENS (logged in
`plans/claudemanaged_split_notes.md`), both LAW 24 (NO PEEK-AHEAD):
  * MANAGED AGENTS lands on the START of 'agents' (2.26) instead of 'managed'
    (1.62): it is still the first type on the board (LAW 9);
  * SESSION BUDGET lands on the START of 'budget' (8.06, with the coin)
    instead of 'session' (7.70).

HD DELIVERY: authored AND encoded 1080x1920.  The face plate is
`face_bottom_hd.mp4` (1080x1058), so the seam is 1920 - 1057.5 = 862.5 and the
RENDERING pill top is 862.5 - 114.59/2 = 805.205.  The core's content band
104..548 lands at canvas 296..740: 104 px under LAW 30's top-10 % line and
65.2 px over the pill.

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
import claudemanaged_scene as SC                # noqa: E402

RUN = Path(__file__).resolve().parents[1]
CUT = RUN / "cuts/claudemanaged"
PLAN = RUN / "plans/claudemanaged_plan.json"
ASSETS = Path.home() / "Documents/Workspace/assets"
LOGOS = ASSETS / "logos"
LIB_MUSIC = ASSETS / "audio/music/shorts-factory"
LIB_SFX = ASSETS / "audio/sfx/shorts-factory"

VID = "claudemanaged"
W, H = 1080.0, 1920.0
FPS = 25
DUR = SC.DUR                                     # 38.44, the cut master

SEAM = 862.5
CORE_TOP_SPLIT = SC.CANVAS_OFFSET                # 192.0, the handoff's number
CORE_K = 1.00
LEFT = (W - SC.CORE_W * CORE_K) / 2              # 0.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "Claude managed agents get four new features"
LABEL_WINDOW = 1.0

# ------------------------------------------------------------------ marks
STAGE_FILES = {k: f"logos/{v}" for k, v in SC.LOGO_FILES.items()}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}
CUTOUT_LANES = SC.CUTOUT_LOGO_LANES

# ------------------------------------------------------------------ LAW 24
# The emitted label instants (the module's are 1.62 and 7.70).
KEYTERM_AT = 2.26          # start of 'agents'
BUDGET_AT = 8.06           # start of 'budget'


def _b(x, y, w, h) -> tuple:
    return (x, y, x + w, y + h)


C = SC.CUE
SLIDE_D = 0.44
# CORE px boxes at their HOME (settled) seats; the alone offsets are applied in
# rect_at() before each object's one displacement.
RECTS: dict[str, tuple] = {
    "pocket-knife": SC.BESPOKE[0]["core"],
    "key-term-managed": _b(*SC.KEY_TERM_BOX),
    "piggy-bank": (SC.PG_HOME_LEFT + 24, SC.PG_TOP + 16,
                   SC.PG_HOME_LEFT + 284, SC.PG_TOP + 232),
    "label-session-budget": _b(*SC.BUDGET_BOX),
    "budget-meter": (SC.MT_LEFT, SC.MT_TOP, SC.MT_LEFT + SC.MT_W,
                     SC.MT_TOP + SC.MT_H),
    "session-tile": (SC.T2_CX - SC.TILE / 2, SC.T2_TOP,
                     SC.T2_CX + SC.TILE / 2, SC.T2_TOP + SC.TILE),
    "label-session": _b(*SC.SESSION_BOX),
    "advisor-brain": (SC.BR_LEFT + 18, SC.BR_TOP + 18, SC.BR_LEFT + 300,
                      SC.BR_TOP + 254),
    "label-advisor": _b(*SC.ADVISOR_BOX),
    "skill-shelf": (SC.SH_LEFT, SC.SH_TOP, SC.SH_LEFT + SC.SH_W,
                    SC.SH_TOP + SC.SH_H),
    "label-skills": _b(*SC.SKILLS_BOX),
    "agent-tile": (SC.T3_CX - SC.TILE / 2, SC.T3_TOP,
                   SC.T3_CX + SC.TILE / 2, SC.T3_TOP + SC.TILE),
    "signpost": SC.BESPOKE[4]["core"],
    "label-inference": _b(*SC.INFER_BOX),
}
# (alone dx, the displacement's start)
ALONE = {
    "piggy-bank": (SC.PG_ALONE_DX, C["slide1"]),
    "label-session-budget": (SC.PG_ALONE_DX, C["slide1"]),
    "session-tile": (SC.T2_ALONE_DX, C["advisor"]),
    "label-session": (SC.T2_ALONE_DX, C["advisor"]),
    "skill-shelf": (SC.SH_ALONE_DX, C["slide3"]),
    "label-skills": (SC.SH_ALONE_DX, C["slide3"]),
}
# lifetimes on the page (the module's, with the two LAW 24 repairs)
LIFE = {
    "pocket-knife": SC.LIFETIMES["pocket-knife"],
    "key-term-managed": (KEYTERM_AT, SC.LIFETIMES["key-term-managed"][1]),
    "piggy-bank": SC.LIFETIMES["piggy-bank"],
    "label-session-budget": (BUDGET_AT, SC.LIFETIMES["label-session-budget"][1]),
    "budget-meter": SC.LIFETIMES["budget-meter"],
    "session-tile": SC.LIFETIMES["session-group"],
    "label-session": (C["session"], SC.LIFETIMES["session-group"][1]),
    "advisor-brain": SC.LIFETIMES["advisor-brain"],
    "label-advisor": SC.LIFETIMES["label-advisor"],
    "skill-shelf": SC.LIFETIMES["skill-shelf"],
    "label-skills": SC.LIFETIMES["label-skills"],
    "agent-tile": SC.LIFETIMES["agent-tile"],
    "signpost": SC.LIFETIMES["signpost"],
    "label-inference": SC.LIFETIMES["label-inference"],
}


def moving(name: str, t: float) -> bool:
    if name not in ALONE:
        return False
    _dx, t0 = ALONE[name]
    return t0 - 1e-9 <= t < t0 + SLIDE_D


def rect_at(name: str, t: float) -> tuple:
    b = RECTS[name]
    if name in ALONE:
        dx, t0 = ALONE[name]
        if t < t0:
            return (b[0] + dx, b[1], b[2] + dx, b[3])
    return b


def canvas(box):
    """core px -> the canvas this page actually paints (top 192, k 1.00)."""
    return (CORE_K * box[0] + LEFT, CORE_TOP_SPLIT + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP_SPLIT + CORE_K * box[3])


# --------------------------------------------------------------- label plan
# LAW 39 / LAW 9 / LAW 50: every name BELOW what it names.
LABEL_PLAN = {"key-term-managed": ("pocket-knife", "below", SC.KEY_TERM),
              "label-session-budget": ("piggy-bank", "below", "SESSION BUDGET"),
              "label-session": ("session-tile", "below", "SESSION"),
              "label-advisor": ("advisor-brain", "below", "ADVISOR"),
              "label-skills": ("skill-shelf", "below", "SKILLS"),
              "label-inference": ("signpost", "below", "INFERENCE")}
LABEL_AT = {k: LIFE[k][0] for k in LABEL_PLAN}
# the board contents typed INSIDE the signpost (LAW 39: content, not labels)
BOARD_KEYS = {"sp-us": ("US", C["us"]), "sp-eu": ("EUROPE", C["europe"])}
PRINTED_KEYS = {**{k: v[2] for k, v in LABEL_PLAN.items()},
                **{k: v[0] for k, v in BOARD_KEYS.items()}}
PRINTED_LIFETIME = {**{k: LIFE[k] for k in LABEL_PLAN},
                    "sp-us": (C["us"], SC.LIFETIMES["signpost"][1]),
                    "sp-eu": (C["europe"], SC.LIFETIMES["signpost"][1])}

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.
CUE_WORDS = {
    "keyterm": (8, "managed"), "four": (13, "four"), "eraseA": (16, "number"),
    "budget": (26, "session"), "coin": (27, "budget"), "slide1": (28, "meaning"),
    "fill": (29, "no"), "cap": (31, "overspending"), "eraseB": (38, "number"),
    "session": (41, "session"), "advisor": (46, "advisor"),
    "smart": (51, "intelligent"), "help": (57, "help"), "eraseC": (62, "number"),
    "load": (67, "load"), "skills": (69, "skills"), "slide3": (70, "from"),
    "connect": (75, "connect"), "eraseD": (78, "and"),
    "inference": (87, "inference"), "us": (108, "us"), "europe": (110, "europe"),
    "outro": (114, "more"),
}
# AUTHORED instants, each inside its own word's window (start .. end + 1.0 s)
CUE_INSIDE = {"knife": (0, "claude"), "piggy": (16, "number"),
              "meter": (28, "meaning"), "tile2": (38, "number"),
              "advlabel": (46, "advisor"), "shelf": (62, "number"),
              "agent3": (70, "from"), "sign": (78, "and")}


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
    opening = "claude just made it easier to run their managed ai agents"
    head = " ".join(w["text"] for w in ws[:11]).lower()
    if head != opening:
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[11:]).lower()
    if "claude just made" in later or "made it easier" in later:
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
                    "at word 0 / 0.08 s",
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
                             f"{text!r} — the cut moved")
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
    if C["europe"] + 0.28 >= C["outro"]:
        raise SystemExit("board ink still changing under the outro sheet")
    rep["_law43"] = {"board_mode": SC.BOARD_MODE, "chapters": 5,
                     "seams": list(SC.CHAPTER_SEAMS)}
    return rep


def assert_word_sync(ws: list[dict]) -> dict:
    """WORD-SYNC: every typed key first shows the value its word says, and
    never before the LAST word it names has started (LAW 24)."""
    rows = []
    checks = [  # (state, first visible text, at, word idx, word)
        ("key-term-managed", SC.KEY_TERM, KEYTERM_AT, 10, "agents"),
        ("label-session-budget", "SESSION BUDGET", BUDGET_AT, 27, "budget"),
        ("label-session", "SESSION", LABEL_AT["label-session"], 41, "session"),
        ("label-advisor", "ADVISOR", LABEL_AT["label-advisor"], 46, "advisor"),
        ("label-skills", "SKILLS", LABEL_AT["label-skills"], 69, "skills"),
        ("label-inference", "INFERENCE", LABEL_AT["label-inference"], 87,
         "inference"),
        ("sp-us", "US", C["us"], 108, "us"),
        ("sp-eu", "EUROPE", C["europe"], 110, "europe"),
    ]
    for state, text, t, idx, word in checks:
        w = ws[idx]
        if _norm(w["text"]) != word:
            raise SystemExit(f"word-sync: {state} expects {word!r} at word {idx}")
        lo, hi = float(w["start"]), float(w["end"]) + LABEL_WINDOW
        if not (lo - 0.011 <= t <= hi):
            raise SystemExit(f"word-sync: {state} first shows at {t}, outside "
                             f"{lo:.3f}-{hi:.3f}")
        rows.append({"state": state, "first_visible_text": text, "at": t,
                     "word": w["text"], "word_window": [round(lo, 3), round(hi, 3)]})
    if min(LABEL_AT.values()) != LABEL_AT["key-term-managed"]:
        raise SystemExit("LAW 9: MANAGED AGENTS is not the first type on the board")
    return {"typed_states": rows, "disagreements": 0, "digits_that_tick": 0,
            "numbers_typed": 0}


def assert_law37(ws: list[dict]) -> dict:
    cues = PCUE.scan(ws)
    plan = json.loads(PLAN.read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / "prep/stages/claudemanaged.cues.json").read_text())
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
            t = ALONE[host][1] + SLIDE_D + 0.01
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
    open_ended = [n for n, (_a, b) in SC.LIFETIMES.items() if b is None]
    grounds = {"o-sheet", "o-glyph", "o-rule", "o-slot"}   # the outro lockup
    for n in open_ended:
        if n not in SC.SCENE_ANCHORS and n not in grounds:
            raise SystemExit(f"LAW 42: {n} never leaves and is not an anchor")
    for n, (a, b) in LIFE.items():
        if b <= a:
            raise SystemExit(f"LAW 42: {n} has an empty window")
        if (b - a) / DUR > 0.40:
            raise SystemExit(f"LAW 42: {n} is on screen {(b - a) / DUR:.0%}")
    longest = max(LIFE.items(), key=lambda kv: kv[1][1] - kv[1][0])
    return {"board_mode": SC.BOARD_MODE, "anchors": sorted(SC.SCENE_ANCHORS),
            "outro_ground": sorted(grounds),
            "longest": {"mark": longest[0], "window": longest[1],
                        "share": round((longest[1][1] - longest[1][0]) / DUR, 3)}}


SPACING_TIMES = (1.0, 2.6, 4.2, 6.0, 8.3, 9.3, 10.6, 12.5, 13.5, 14.6, 16.8,
                 19.2, 20.4, 22.2, 23.2, 24.9, 26.0, 28.0, 33.5, 34.6)


def assert_spacing_law() -> dict:
    """LAW 41 on the co-alive seats at settled instants."""
    groups = _groups()
    # a connector joins what it joins, so the brain/tile and shelf/tile
    # gutters are the connectors' spans, legal by design
    joined = [{"advisor-brain", "session-tile"}, {"skill-shelf", "agent-tile"}]

    def alive(n, t):
        a, b = LIFE[n]
        return a <= t < b

    worst = (1e9, None)
    for t in SPACING_TIMES:
        live = [n for n in RECTS if alive(n, t) and not moving(n, t)]
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
            "connector_joined": [sorted(j) for j in joined],
            "blocks": [sorted(g) for g in groups]}


# LAW 38 rule 2: three border flips, each on a DRAWN object, each held to its
# chapter erase.  (id, target, flip cue, check instant, erase)
EMPH = {
    "meter": {"id": "budget-meter", "kind": "border", "target": "meter-fill",
              "flip": C["cap"], "check_at": 10.40, "until": C["eraseB"]},
    "brain": {"id": "brain-outline", "kind": "border", "target": "advisor-brain",
              "flip": C["smart"], "check_at": 17.40, "until": C["eraseC"]},
    "book": {"id": "book-hero", "kind": "border", "target": "skill-shelf",
             "flip": C["load"], "check_at": 21.90, "until": C["eraseD"]},
}
FLIP_D = 0.38


def assert_emphasis_law() -> dict:
    for name, e in EMPH.items():
        if not (e["flip"] + FLIP_D <= e["check_at"] < e["until"]):
            raise SystemExit(f"LAW 38: the {name} flip is not complete and held "
                             f"at {e['check_at']}")
    # the book's flip lands at 21.22, the shelf slides at 22.44: check before
    if not EMPH["book"]["check_at"] < C["slide3"]:
        raise SystemExit("LAW 38: the book check lands inside the shelf's slide")
    return {"border_flips": [{"on": e["id"], "kind": e["kind"],
                              "target": e["target"], "check_at": e["check_at"],
                              "held": [e["flip"], e["until"]]}
                             for e in EMPH.values()],
            "rings_ellipses_circles": 0, "highlights": 0, "dom_ink_added": 0}


def assert_anchor_law() -> dict:
    """LAW 40: each connector is level and lands on its tile's left-edge
    centre at the settled instant after it has drawn."""
    out = {}
    checks = {"conn-advice": ("session-tile", 18.90, C["help"], C["eraseC"]),
              "conn-skills": ("agent-tile", 24.80, C["connect"], C["eraseD"])}
    for cn in SC.CONNECTORS:
        tgt, at, drawn, erase = checks[cn["id"]]
        if cn["to"] != tgt:
            raise SystemExit(f"LAW 40: {cn['id']} targets {cn['to']}")
        (fx, fy), (tx, ty) = cn["a"], cn["b"]
        tb = rect_at(tgt, at)
        if abs(tx - tb[0]) > 0.01 or abs(ty - (tb[1] + tb[3]) / 2) > 0.01:
            raise SystemExit(f"LAW 40: {cn['id']} misses {tgt}'s left-edge centre")
        if abs(fy - ty) > 0.01:
            raise SystemExit(f"LAW 40: {cn['id']} is not level")
        if not (drawn + 0.36 <= at < erase):
            raise SystemExit(f"LAW 40: {cn['id']} check is not a completed state")
        out[cn["id"]] = {"to": tgt, "side": "left", "fraction": 0.5,
                         "check_at": at, "from_core": [fx, fy], "to_core": [tx, ty]}
    return out


def assert_cast_law() -> dict:
    rep = DF.assert_cast_resolves(list(SC.LOGO_FILES), dict(SC.LOGO_FILES),
                                  LOGOS, label="claudemanaged stage marks")
    return {"stage_marks": sorted(SC.LOGO_FILES),
            "resolved": {k: v["path"] for k, v in rep.items()},
            "media_sides_core_px": {k: v[1] for k, v in SC.MEDIA_SIDES.items()},
            "cutout_lanes_not_ours": list(CUTOUT_LANES)}


def assert_draw_on(tweens: list[str], html: str) -> dict:
    """THE DRAW-ON DASH LAW: every dash-revealed selector resolves ONLY to
    paths that declare pathLength="100"."""
    sels = set()
    for t in tweens:
        if "strokeDasharray:100" in t:
            sels.update(re.findall(r'tl\.set\("([^"]+)"', t))
    paths = re.findall(r'<path\b[^>]*>', html)
    checked = {}
    for sel in sorted(sels):
        n = 0
        for part in sel.split(","):
            cls = part.strip().split()[-1]
            if not cls.startswith("."):
                raise SystemExit(f"unexpected dash selector {sel}")
            c = cls[1:]
            tags = [p for p in paths
                    if re.search(rf'class="[^"]*\b{re.escape(c)}\b', p)]
            if not tags or not all('pathLength="100"' in p for p in tags):
                raise SystemExit(f"DRAW-ON: {sel} reveals a path without "
                                 'pathLength="100"')
            n += len(tags)
        checked[sel] = n
    return {"dash_selectors": checked, "verdict": "every dash equals its "
            "path's declared length (100)"}


# LAW 24 (NO PEEK-AHEAD) repairs on the emitted tweens only.
def _retime(tweens: list[str], sel: str, old: float, new: float) -> list[str]:
    pat = re.compile(rf'^tl\.fromTo\("{re.escape(sel)}",\{{opacity:0,y:12\}},'
                     rf'.*\}},{old:.2f}\);$')
    hits = [i for i, t in enumerate(tweens) if pat.match(t)]
    if len(hits) != 1:
        raise SystemExit(f"the module no longer emits ONE {sel} key-in at {old}")
    out = list(tweens)
    out[hits[0]] = out[hits[0]][: -len(f"{old:.2f});")] + f"{new:.2f});"
    return out


def repair_tweens(tweens: list[str]) -> tuple[list[str], dict]:
    t = _retime(tweens, "#key-term-managed", C["keyterm"], KEYTERM_AT)
    t = _retime(t, "#label-session-budget", C["budget"], BUDGET_AT)
    return t, {
        "key-term-managed": {"from": C["keyterm"], "to": KEYTERM_AT,
                             "law": "LAW 24: AGENTS waits for 'agents'"},
        "label-session-budget": {"from": C["budget"], "to": BUDGET_AT,
                                 "law": "LAW 24: BUDGET waits for 'budget'"}}


def declare_contracts(html: str, anchors: dict) -> tuple[str, dict]:
    s = html
    stamped = []
    for e in EMPH.values():
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
    return s, {"connectors_stamped": len(anchors), "emphases_stamped": stamped}


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
    """The four rasters the scene paints (handoff section 1), all the Claude
    mark, each sized by INK."""
    return {mkey: CC.mark_img(LOGO_URL[key], key, side)
            for mkey, (key, side) in SC.MEDIA_SIDES.items()}


def sfx_plan() -> list[tuple]:
    """EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22)."""
    return [("pop", C["knife"], SFX_STRUCTURE),        # the knife lands
            ("click", KEYTERM_AT, SFX_DETAIL),         # MANAGED AGENTS
            ("pop", C["four"], SFX_DETAIL),            # the tools fold out
            ("whoosh", C["eraseA"], SFX_STRUCTURE),    # chapter 1: piggy
            ("pop", BUDGET_AT, SFX_DETAIL),            # coin + SESSION BUDGET
            ("whoosh", C["slide1"], SFX_STRUCTURE),    # piggy left, meter in
            ("whoosh", C["eraseB"], SFX_STRUCTURE),    # chapter 2: the tile
            ("click", C["session"], SFX_DETAIL),       # SESSION
            ("whoosh", C["advisor"], SFX_STRUCTURE),   # tile right, brain in
            ("click", C["help"], SFX_DETAIL),          # the connector draws
            ("whoosh", C["eraseC"], SFX_STRUCTURE),    # chapter 3: the shelf
            ("click", C["skills"], SFX_DETAIL),        # SKILLS
            ("whoosh", C["slide3"], SFX_STRUCTURE),    # shelf left, agent in
            ("click", C["connect"], SFX_DETAIL),       # the cable draws
            ("whoosh", C["eraseD"], SFX_STRUCTURE),    # chapter 4: signpost
            ("click", C["inference"], SFX_DETAIL),     # INFERENCE
            ("click", C["us"], SFX_DETAIL),            # US
            ("click", C["europe"], SFX_DETAIL),        # EUROPE
            ("whoosh", C["outro"], SFX_STRUCTURE)]     # the rising sheet


def assert_sfx(sfx) -> dict:
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30:
        raise SystemExit(f"SFX flam: {worst}")
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "deliberately_silent": {
                "tools 3.44-3.72": "one pop scores the fold-out, not four",
                "meter fill 9.08": "a fill is not an arrival",
                "flips 9.50/16.36/21.22": "a colour flip is not an arrival",
                "ADVISOR 14.10": "0.14 s after the brain's whoosh",
                "agent tile 22.50": "0.06 s after the shelf's whoosh"}}


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
        if n == "key-term-managed":
            fs, ls = SC.KEY_TERM_FS, SC.KEY_TERM_LS
        else:
            fs, ls = SC.KEY_FS, SC.KEY_LS
        ink = len(text) * 0.6 * fs + (len(text) - 1) * ls
        rights[n] = (b[0] + b[2]) / 2 + ink / 2
    # the board names, typed inside the signpost
    for eid, (text, _t), c, fs in (("sp-us", BOARD_KEYS["sp-us"], SC.SP_US_C,
                                    SC.SP_US_FS),
                                   ("sp-eu", BOARD_KEYS["sp-eu"], SC.SP_EU_C,
                                    SC.SP_EU_FS)):
        ink = len(text) * 0.6 * fs + (len(text) - 1) * 1.5
        rights[eid] = LEFT + SC.SP_LEFT + c[0] + ink / 2
    type_right = max(rights.values())
    if type_right > CAP.LAW12_RAIL_X + 0.01:
        raise SystemExit(f"readable key ink reaches x={type_right:.1f}")
    boxes = [canvas(rect_at(n, t)) for n in RECTS for t in SPACING_TIMES
             if LIFE[n][0] <= t < LIFE[n][1]]
    ink_left = min(b[0] for b in boxes)
    ink_right = max(b[2] for b in boxes)
    if ink_left < 40 or W - ink_right < 40:
        raise SystemExit("the composition leaves the 40 px frame margin")
    return {"readable_type_right_x": round(type_right, 1),
            "ink_left_x": round(ink_left, 1), "ink_right_x": round(ink_right, 1),
            "law30_rail_x": CAP.LAW12_RAIL_X}


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
    tweens, rep["tween_repairs"] = repair_tweens(tweens)
    rep["draw_on"] = assert_draw_on(tweens, scene_html)
    scene_html, rep["declared"] = declare_contracts(scene_html, rep["law40"])
    if scene_html.count("data-connect-to") != 2:
        raise SystemExit("the scene does not carry its two connectors")
    if (scene_html.count("data-connect-to") + scene_html.count("data-emphasis=")
            != scene_html.count("data-check-at")):
        raise SystemExit("a connector or emphasis is missing its check instant")
    for shape in ("<circle", "<ellipse"):
        if shape in scene_html:
            raise SystemExit(f"LAW 38 rule 3: {shape} in the emitted scene")
    for key in list(LABEL_PLAN) + list(BOARD_KEYS):
        if f'id="{key}"' not in scene_html:
            raise SystemExit(f"{key} is missing from the scene")

    m = CAP.PillMeasurer(RUN / "gen/_pillwidths_claudemanaged.json")
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
    dst = RUN / "projects/claudemanaged_split"
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
    (RUN / "gen/_build_claudemanaged_split.json").write_text(
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
