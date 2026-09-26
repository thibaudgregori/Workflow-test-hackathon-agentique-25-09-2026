#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION - stripekai / DIAGRAM BUILD.

    YouTube   classic split 50/50   projects/stripekai_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/stripekai_scene.py` plus
`plans/stripekai_scene_handoff.md` are the design agent's artefacts, sealed by
`review/artwork_pass_stripekai.json` (production v4, `production.py seal`).
This file IMPORTS the module and SEATS it at the handoff's own placement
(k = 1.00, left 0, core top 192).  It never mutates a byte of the module on disk.

FORMAT-SIDE STAMPS ON THE EMITTED STRING (the module on disk is untouched):
  * the one connector `#conn-built` gets `data-anchor-side`,
    `data-anchor-fraction` and `data-check-at` (LAW 40 contract);
  * an inkless virtual rectangle `#toolbox-2-body` is inserted INSIDE the
    returning toolbox's statically scaled authoring div (so it moves and scales
    with it): the body the emphasis boxes.  The toolbox as a whole cannot be the
    emphasis target: its terracotta screwdriver handle paints the very colour the
    outline flips to, and the flip is the BODY's outline, not the tools';
  * the ONE emphasis is declared on `#toolbox-2 .tbbody` (border flip).

HD DELIVERY: authored AND encoded 1080x1920.  The face plate is
`face_bottom_hd.mp4` (1080x1058), seam 862.5, RENDERING pill top
862.5 - 114.59/2 = 805.205.  The core's content band 76..538 lands at canvas
268..730: 76 px under LAW 30's top-10 % line and 75.2 px over the pill.

TAKEOVER and FACESPLIT are not daily deliverables and this file cannot build one.
"""
from __future__ import annotations

import argparse
import html as ihtml
import json
import math
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
import stripekai_scene as SC                    # noqa: E402

RUN = Path(__file__).resolve().parents[1]
CUT = RUN / "cuts/stripekai"
PLAN = RUN / "plans/stripekai_plan.json"
ASSETS = Path.home() / "Documents/Workspace/assets"
LOGOS = ASSETS / "logos"
LIB_MUSIC = ASSETS / "audio/music/shorts-factory"
LIB_SFX = ASSETS / "audio/sfx/shorts-factory"

VID = "stripekai"
W, H = 1080.0, 1920.0
FPS = 25
DUR = SC.DUR                                     # 35.82, the cut master

SEAM = 862.5
CORE_TOP_SPLIT = SC.CANVAS_OFFSET                # 192.0, the handoff's number
CORE_K = 1.00
LEFT = (W - SC.CORE_W * CORE_K) / 2              # 0.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "Stripe's Kai: one platform for 1,000 AI skills"
LABEL_WINDOW = 1.0

# ------------------------------------------------------------------ marks
# MARK IDENTITY: the FILE is named, never "the logo" (handoff section 1).
STAGE_FILES = dict(SC.LOGO_FILES)                # {"stripe": platforms/stripe-color.png}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}
CUTOUT_LANES = SC.CUTOUT_LOGO_LANES

# ------------------------------------------------------------------ geometry
C = SC.CUE
TB1_MOVED = C["seam1"] + 0.46                    # 10.56, the one displacement ends
PERSON_SEATED = C["seam2"] + 0.46                # 14.18, the person is in seat 0


def _lbl(b) -> tuple:
    x, y, w, h = b
    return (x, y, x + w, y + h)


def _cnt(cx: float, y: float, h: float) -> tuple:
    return (cx - SC.CSEAT / 2, y, cx + SC.CSEAT / 2, y + h)


SEAT0 = SC.fig_slots()[0]
PERSON_SEAT_BOX = (SEAT0[0], SEAT0[1], SEAT0[0] + SC.FIG_W, SEAT0[1] + SC.FIG_H)

RECTS: dict[str, tuple] = {
    "toolbox": SC.TB1_BOX,
    "key-kai": _lbl(SC.KEY_KAI_BOX),
    "cnt-skills-num": _cnt(SC.CNT_L_CX, SC.CNT_NUM_Y, SC.NUM_LH),
    "cnt-skills-unit": _cnt(SC.CNT_L_CX, SC.CNT_UNIT_Y, 40.0),
    "cnt-tools-num": _cnt(SC.CNT_R_CX, SC.CNT_NUM_Y, SC.NUM_LH),
    "cnt-tools-unit": _cnt(SC.CNT_R_CX, SC.CNT_UNIT_Y, 40.0),
    "person": SC.PERSON_BOX,
    "week-strip": SC.WEEK_BOX,
    "key-week": _lbl(SC.KEY_WEEK_BOX),
    "crowd": SC.CROWD_BOX,
    "key-83": _lbl(SC.KEY_83_BOX),
    "key-workforce": _lbl(SC.KEY_WORK_BOX),
    "buildings": SC.BLD_BOX,
    "key-orgs": _lbl(SC.KEY_ORGS_BOX),
    "toolbox-2": SC.TB2_BOX,
    "key-150": _lbl(SC.KEY_150_BOX),
}
# the instants at which a rect is IN TRANSIT and not a seat (skipped by the laws)
TRANSIT = {"toolbox": (C["seam1"], TB1_MOVED),
           "person": (C["seam2"], PERSON_SEATED)}


def in_transit(name: str, t: float) -> bool:
    w = TRANSIT.get(name)
    return bool(w) and w[0] <= t < w[1]


def rect_at(name: str, t: float) -> tuple:
    if name == "toolbox" and t >= TB1_MOVED - 1e-9:
        return SC.TB1_BOX1
    if name == "person" and t >= PERSON_SEATED - 1e-9:
        return PERSON_SEAT_BOX
    return RECTS[name]


def canvas(box):
    """core px -> the canvas this page actually paints (top 192, k 1.00)."""
    return (CORE_K * box[0] + LEFT, CORE_TOP_SPLIT + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP_SPLIT + CORE_K * box[3])


def alive(name: str, t: float) -> bool:
    a, b = SC.LIFETIMES[name]
    return a <= t and (b is None or t < b)


# --------------------------------------------------------------- label plan
# LAW 39 / LAW 50: (host, side, printed text, the instant it lands)
LABEL_PLAN = {
    "key-kai": ("toolbox", "below", SC.KEY_TERM, C["keyterm"]),
    "key-week": ("week-strip", "below", "1 WEEK", C["k_week"]),
    "key-83": ("crowd", "above", "83%", C["k_83"]),
    "key-workforce": ("crowd", "below", "OF THE WORKFORCE", C["k_work"]),
    "key-orgs": ("buildings", "below", "ORGANIZATIONS", C["k_orgs"]),
    "key-150": ("toolbox-2", "below", "150+ SKILLS", C["k_150"]),
}
# typed states: what first appears, on which word (WORD-SYNC).  `spoken` is the
# transcript's own wording of the value the key prints (normalised).
PRINTED_KEYS = {
    "key-kai": (SC.KEY_TERM, 16, ["kai"]),
    "cnt-skills-num": ("1,000", 24, ["1,000"]),
    "cnt-skills-unit": ("SKILLS", 25, ["skills"]),
    "cnt-tools-num": ("500", 27, ["500"]),
    "cnt-tools-unit": ("INTERNAL TOOLS", 28, ["internal", "tools"]),
    "key-week": ("1 WEEK", 37, ["a", "week"]),
    "key-83": ("83%", 46, ["83%"]),
    "key-workforce": ("OF THE WORKFORCE", 47, ["of", "the", "workforce"]),
    "key-orgs": ("ORGANIZATIONS", 72, ["organizations"]),
    "key-150": ("150+ SKILLS", 89, ["over", "150", "skills"]),
}
PRINTED_AT = {"key-kai": C["keyterm"], "cnt-skills-num": C["n_skills"],
              "cnt-skills-unit": C["u_skills"], "cnt-tools-num": C["n_tools"],
              "cnt-tools-unit": C["u_tools"], "key-week": C["k_week"],
              "key-83": C["k_83"], "key-workforce": C["k_work"],
              "key-orgs": C["k_orgs"], "key-150": C["k_150"]}

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.
CUE_WORDS = {
    "toolbox": (0, "stripe"), "tools": (2, "revealed"), "keyterm": (16, "kai"),
    "n_skills": (24, "1,000"), "u_skills": (25, "skills"), "n_tools": (27, "500"),
    "u_tools": (29, "tools"), "seam1": (30, "literally"), "person": (31, "one"),
    "built": (34, "built"), "k_week": (38, "week"), "seam2": (39, "and"),
    "k_83": (46, "83%"), "k_work": (49, "workforce"), "seam3": (60, "how"),
    "sparks": (68, "ai"), "k_orgs": (72, "organizations"), "seam4": (73, "they"),
    "overflow": (88, "loading"), "emph": (90, "150"), "k_150": (91, "skills"),
    "emphout": (93, "everyone"), "outro": (100, "now"),
}
# AUTHORED instants: each inside its own word's 1.0 s LABEL_WINDOW
CUE_INSIDE = {"plate": (0, "stripe"), "strip": (34, "built"),
              "fill": (35, "this"), "crowd": (39, "and"), "fill83": (46, "83%")}


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
    opening = "stripe just revealed their secrets on how"
    head = " ".join(_norm(w["text"]) for w in ws[:7])
    if head != opening:
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(_norm(w["text"]) for w in ws[7:])
    if "just revealed their secrets" in later:
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
           + f" - {tail:.3f}s past the last word against a {cap:.3f}s cap",
           "law46": "the scripted opening occurs ONCE inside the keeper take",
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
    if SC.BOARD_MODE != "chapters" or len(SC.BOARD_CHAPTERS) != 6:
        raise SystemExit("the scene is no longer the six chapters the plan "
                         "declared")
    if C["emphout"] + 0.30 >= C["outro"]:
        raise SystemExit("board ink still changing under the outro sheet")
    return rep


def assert_word_sync(ws: list[dict]) -> dict:
    """WORD-SYNC: every typed key first shows the value its words say - the key
    lands between the first word that carries it and LABEL_WINDOW after its
    last, and never before the value is spoken (LAW 24)."""
    rows = []
    for key, (text, idx, spoken) in PRINTED_KEYS.items():
        t = PRINTED_AT[key]
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
        raise SystemExit("LAW 9: KAI is not the first type")
    return {"typed_states": rows, "disagreements": 0, "digits_that_tick": 0,
            "note": "Numbers are printed whole (no tick-up), so no intermediate "
                    "value is ever on screen; 1 WEEK prints 'a week'."}


def assert_law37(ws: list[dict]) -> dict:
    cues = PCUE.scan(ws)
    plan = json.loads(PLAN.read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / "prep/stages/stripekai.cues.json").read_text())
    if marker["keys"]["cue_count"] != len(cues):
        raise SystemExit("LAW 37: the prep marker disagrees with the re-run")
    if cues or declared:
        raise SystemExit("LAW 37: this scene builds no source card")
    return {"scan_cue_count": 0, "plan_declared_cards": 0,
            "prep_marker_cue_count": 0, "source_cards_in_the_page": 0}


# ------------------------------------------------------------------ laws
GUTTER_REFUSE = 16.0
HELD = [3.0, 5.0, 8.0, 9.95, 11.2, 12.8, 13.5, 14.5, 16.0, 17.5, 20.0, 21.5,
        23.0, 23.8, 25.0, 28.2, 29.5, 31.0]


def assert_label_law() -> dict:
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    out: dict = {}
    for key, (host, side, text, t0) in LABEL_PLAN.items():
        checked = []
        for tt in [t0 + 0.30] + HELD:
            if tt < t0 or not alive(key, tt) or not alive(host, tt):
                continue
            if in_transit(host, tt):
                continue
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
    # LAW 50: the two toolbox keys sit the same way
    if LABEL_PLAN["key-kai"][1] != LABEL_PLAN["key-150"][1]:
        raise SystemExit("LAW 50: the two toolbox keys sit differently")
    du = SC.KEY_TERM_FS * CORE_K / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} du")
    out["_key_term"] = {"text": SC.KEY_TERM, "font_px": SC.KEY_TERM_FS,
                        "design_units": round(du, 2), "first_type": True}
    return out


def assert_lifetime_law() -> dict:
    for n, (a, b) in SC.LIFETIMES.items():
        if b is None:
            if n not in SC.SCENE_ANCHORS:
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
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    worst = (1e9, None)
    for t in HELD:
        live = [n for n in RECTS if alive(n, t) and not in_transit(n, t)]
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


# ------------------------------------------------------ LAW 40: the connector
CONN_CHECK_AT = 13.40          # drawn by 12.48, fades at 13.72; the toolbox is
#                                seated at TB1_BOX1 since 10.56


def assert_anchor_law() -> dict:
    tip = SC.CONN_TO
    x0, y0, x1, y1 = SC.TB1_BOX1
    frac = round((tip[1] - y0) / (y1 - y0), 12)
    anchor = (x0, y0 + frac * (y1 - y0))
    miss = math.hypot(tip[0] - anchor[0], tip[1] - anchor[1])
    if miss > 4.0:
        raise SystemExit(f"conn-built misses the toolbox's left edge by {miss}")
    a, b = SC.LIFETIMES["conn-built"]
    if not (a + 0.30 <= CONN_CHECK_AT < b) or CONN_CHECK_AT < TB1_MOVED:
        raise SystemExit("conn-built: check-at is not a held, seated instant")
    if not alive("toolbox", CONN_CHECK_AT):
        raise SystemExit("conn-built: its target is gone at the check")
    return {"conn-built": {"target": "toolbox", "side": "left",
                           "fraction": frac, "check_at": CONN_CHECK_AT,
                           "tip_core": list(tip),
                           "anchor_core": [round(v, 2) for v in anchor],
                           "miss_px": round(miss, 2),
                           "level_px": abs(SC.CONN_FROM[1] - SC.CONN_TO[1])}}


# ------------------------------------------------------ LAW 38: emphasis
EMPH = {"id": "emph-toolbox-2", "kind": "border", "target": "toolbox-2-body",
        "check_at": 29.50,
        "window": (C["emph"] + 0.34, C["emphout"])}
# the body rect in the returning toolbox's AUTHORING space, relative to its
# TB_VB_FULL view (the div inside #toolbox-2 at a static scale(0.9))
BODY_A = (10.0, 130.0, 350.0, 290.0)
BODY_LOCAL = (BODY_A[0] - SC.TB_VB_FULL[0], BODY_A[1] - SC.TB_VB_FULL[1],
              BODY_A[2] - SC.TB_VB_FULL[0], BODY_A[3] - SC.TB_VB_FULL[1])


def assert_emphasis_law() -> dict:
    a, b = EMPH["window"]
    if not (a <= EMPH["check_at"] < b):
        raise SystemExit(f"LAW 38: the flip is not complete and held at "
                         f"{EMPH['check_at']}")
    return {"flips": [{"on": "#toolbox-2 .tbbody", "kind": EMPH["kind"],
                       "target": EMPH["target"], "check_at": EMPH["check_at"],
                       "held": list(EMPH["window"])}],
            "rings_ellipses_circles": 0, "highlights": 0,
            "dom_elements_added": 1,
            "note": "the one added element is the inkless virtual body rect"}


def declare_contracts(html: str, anchors: dict) -> tuple[str, dict]:
    s = html
    # the emphasis: the returning toolbox's body outline, ONE rect in the page
    old = '<rect class="tbk2 tbbody"'
    if s.count(old) != 1:
        raise SystemExit("the module no longer emits ONE returning toolbox body")
    s = s.replace(old, f'<rect id="{EMPH["id"]}" class="tbk2 tbbody" '
                       f'data-emphasis="{EMPH["kind"]}" '
                       f'data-emphasis-target="{EMPH["target"]}" '
                       f'data-check-at="{EMPH["check_at"]:.2f}"', 1)
    # the virtual body rect, inside the scaled authoring div of #toolbox-2
    i = s.index('id="toolbox-2"')
    j = s.index("</svg>", i) + len("</svg>")
    x0, y0, x1, y1 = BODY_LOCAL
    s = (s[:j] + f'<div id="{EMPH["target"]}" class="abs" style="left:{x0:.0f}px;'
         f'top:{y0:.0f}px;width:{x1 - x0:.0f}px;height:{y1 - y0:.0f}px" '
         f'data-virtual-rect></div>' + s[j:])
    # the connector
    for cid, a in anchors.items():
        key = f'id="{cid}"'
        if s.count(key) != 1:
            raise SystemExit(f"cannot stamp {cid}")
        s = s.replace(key, f'{key} data-anchor-side="{a["side"]}" '
                           f'data-anchor-fraction="{a["fraction"]!r}" '
                           f'data-check-at="{a["check_at"]:.2f}"', 1)
    return s, {"connectors_stamped": len(anchors), "emphases_stamped": 1,
               "virtual_rects": [EMPH["target"]]}


def assert_cast_law() -> dict:
    rep = DF.assert_cast_resolves(list(STAGE_FILES), dict(STAGE_FILES),
                                  LOGOS, label="stripekai stage marks")
    return {"stage_marks": sorted(STAGE_FILES),
            "resolved": {k: v["path"] for k, v in rep.items()},
            "mark_side_authoring_px": SC.STRIPE_SIDE,
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
            k0, k1 = SC.LIFETIMES.get(key, (PRINTED_AT[key], DUR))
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
        CC.MARK_INK[key] = CC.measure_mark(key, src)
        marks[key] = {"source": str(src), "url": LOGO_URL[key]}
    rec["marks"] = marks
    return rec


def media() -> dict:
    """The ONE raster the scene paints (handoff section 1)."""
    return {"_stripe_img": CC.mark_img(LOGO_URL["stripe"], "stripe",
                                       SC.STRIPE_SIDE)}


def sfx_plan() -> list[tuple]:
    """EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22)."""
    return [("pop", C["toolbox"], SFX_STRUCTURE),    # the toolbox lands
            ("pop", C["tools"], SFX_DETAIL),         # the three tools rise
            ("click", C["keyterm"], SFX_DETAIL),     # KAI
            ("pop", C["n_skills"], SFX_DETAIL),      # 1,000
            ("click", C["u_skills"], SFX_DETAIL),    # SKILLS
            ("pop", C["n_tools"], SFX_DETAIL),       # 500
            ("click", C["u_tools"], SFX_DETAIL),     # INTERNAL TOOLS
            ("whoosh", C["seam1"], SFX_STRUCTURE),   # the toolbox slides right
            ("pop", C["person"], SFX_STRUCTURE),     # the builder
            ("click", C["built"], SFX_DETAIL),       # the line person -> toolbox
            ("click", C["k_week"], SFX_DETAIL),      # 1 WEEK
            ("whoosh", C["seam2"], SFX_STRUCTURE),   # the person walks into seat 0
            ("pop", C["k_83"], SFX_STRUCTURE),       # 83%
            ("click", C["k_work"], SFX_DETAIL),      # OF THE WORKFORCE
            ("whoosh", C["seam3"], SFX_STRUCTURE),   # the buildings
            ("pop", C["sparks"], SFX_DETAIL),        # the sparks
            ("click", C["k_orgs"], SFX_DETAIL),      # ORGANIZATIONS
            ("whoosh", C["seam4"], SFX_STRUCTURE),   # the toolbox returns
            ("pop", C["overflow"], SFX_STRUCTURE),   # the heap drops in
            ("click", C["emph"], SFX_STRUCTURE),     # the outline flips, strain
            ("click", C["k_150"], SFX_DETAIL),       # 150+ SKILLS
            ("whoosh", C["outro"], SFX_STRUCTURE)]   # the rising sheet


def assert_sfx(sfx) -> dict:
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30:
        raise SystemExit(f"SFX flam: {worst}")
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "deliberately_silent": {
                "plate 0.24": "0.14 s after the toolbox pop",
                "strip 12.30 / fill 12.46": "0.08 s after the line click",
                "crowd 13.80": "0.08 s after the seam whoosh",
                "fill83 15.40": "0.06 s after the 83% pop",
                "emphout 30.00": "a return to ink is not an arrival",
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
        raise SystemExit(f"core content starts at y={y0:.1f} - LAW 30")
    if y1 > pill_top - pill_clear:
        raise SystemExit(f"core content ends at y={y1:.1f}, within {pill_clear}"
                         f"px of the pill top {pill_top:.1f}")
    return {"content_top": y0, "content_bottom": y1,
            "pill_top_rendered": round(pill_top, 3),
            "clear_above_pill": round(pill_top - y1, 2),
            "clear_below_law30": round(y0 - 0.10 * H, 2)}


def guard_rail() -> dict:
    """LAW 30: readable annotations never past x 918 BETWEEN y 30 % and 95 %."""
    band_lo, band_hi = 0.30 * H, 0.95 * H
    rows, in_band = {}, []
    typed = {k: v[0] for k, v in PRINTED_KEYS.items()}
    for n, text in typed.items():
        b = canvas(RECTS[n])
        inb = b[3] > band_lo and b[1] < band_hi
        rows[n] = {"y": [round(b[1], 1), round(b[3], 1)], "in_rail_band": inb}
        if not inb:
            continue
        in_band.append(n)
        if n == "key-kai":
            fs, ls = SC.KEY_TERM_FS, SC.KEY_TERM_LS
        elif n.endswith("-num") or n == "key-83":
            fs, ls = SC.NUM_FS, SC.NUM_LS
        else:
            fs, ls = SC.KEY_FS, SC.KEY_LS
        ink = len(text) * 0.6 * fs + (len(text) - 1) * ls
        cx = (b[0] + b[2]) / 2
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
    rep["law40"] = assert_anchor_law()
    scene_html, rep["declared"] = declare_contracts(scene_html, rep["law40"])
    if scene_html.count("data-connect-to") != 1:
        raise SystemExit("the scene does not carry exactly one connector")
    if (scene_html.count("data-connect-to") + scene_html.count("data-emphasis=")
            != scene_html.count("data-check-at")):
        raise SystemExit("a connector or emphasis is missing its check instant")
    for shape in ("<circle", "<ellipse"):
        if shape in scene_html:
            raise SystemExit(f"LAW 38 rule 3: {shape} in the emitted scene")
    if not any("SWING" in t for t in tweens):
        raise SystemExit("the scene no longer uses SWING")

    m = CAP.PillMeasurer(RUN / "gen/_pillwidths_stripekai_split.json")
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
    dst = RUN / "projects/stripekai_split"
    dst.mkdir(parents=True, exist_ok=True)
    rep = build_split(dst, "yt")
    rep["handle"] = CAP.handle("yt")
    (RUN / "gen/_build_stripekai_split.json").write_text(
        json.dumps({"video": VID, "lane": "diagram build", "fps": FPS,
                    "duration": DUR, "seam": SEAM, "formats": {"split": rep}},
                   indent=1, default=str))
    print(f"split: {dst}")
    print(json.dumps({"captions": rep["captions"], "band": rep["band"],
                      "law41": rep["law41"]["tightest_pair"],
                      "law40": rep["law40"],
                      "law22": rep["law22"]["tightest_gap_s"],
                      "phone": rep["phone_objects"]}, indent=1, default=str))


if __name__ == "__main__":
    main()
