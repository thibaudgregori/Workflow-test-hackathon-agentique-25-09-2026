#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION - hermesdocs / ICON CHOREOGRAPHY.

    YouTube   classic split 50/50   projects/hermesdocs_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/hermesdocs_scene.py` plus
`plans/hermesdocs_scene_handoff.md` are the design agent's artefacts, sealed by
`review/artwork_pass_hermesdocs.json` (production v4, `production.py seal`).
This file IMPORTS the module and SEATS it at the handoff's own placement
(k = 1.00, left 0, core top 192).  It never mutates a byte of the module.

FORMAT-SIDE STAMPS ON THE EMITTED STRING (the module on disk is untouched):
  * the four connectors get `data-anchor-side`, `data-anchor-fraction` and
    `data-check-at` (production's LAW 40 contract), each checked after its
    line has drawn and before it leaves.  The two source arrows' heads are
    marked `data-connector-head` so the painted TIP is the measured end.
    Each connector is declared against a box that IS the painted outline it
    lands on: `fc` (a bordered div, its box includes the border) and two
    INKLESS virtual rects (the streamdeck precedent, run 27), `#safe-edge`
    (inside #safe, the body's outer stroke edge 380..700 x 160..460, so it
    rides the scene's own x tweens) and `#cloud-outer` (the cloud's measured
    getBBox grown by half its 8 px stroke).  The design agent's
    `data-connect-to="safe"` names the whole safe wrapper, whose CSS box is the
    420 px svg frame; an SVG shape's own box is its stroke CENTRE line, 4 px
    inside the painted edge where every end was landed.
  * the three border flips (LAW 38 rule 2, all on DRAWN objects) are declared
    `data-emphasis="border"` with their target and check instant.

HD DELIVERY: authored AND encoded 1080x1920.  The face plate is
`face_bottom_hd.mp4` (1080x1058), so the seam is 1920 - 1057.5 = 862.5 and the
RENDERING pill top is 862.5 - 114.59/2 = 805.205 (the pill that renders, never
the frozen 108.2 seat constant).  The core's content band 60..544 lands at
canvas 252..736: 60 px under LAW 30's top-10 % line and ~69 px over the pill.

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
import hermesdocs_scene as SC                   # noqa: E402

RUN = Path(__file__).resolve().parents[1]
CUT = RUN / "cuts/hermesdocs"
PLAN = RUN / "plans/hermesdocs_plan.json"
ASSETS = Path.home() / "Documents/Workspace/assets"
LOGOS = ASSETS / "logos"
LIB_MUSIC = ASSETS / "audio/music/shorts-factory"
LIB_SFX = ASSETS / "audio/sfx/shorts-factory"

VID = "hermesdocs"
W, H = 1080.0, 1920.0
FPS = 25
DUR = SC.DUR                                     # 28.28, the cut master

SEAM = 862.5
CORE_TOP_SPLIT = SC.CANVAS_OFFSET                # 192.0, the handoff's number
CORE_K = 1.00
LEFT = (W - SC.CORE_W * CORE_K) / 2              # 0.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "Hermes Agent reads your documents locally"
LABEL_WINDOW = 1.0

# ------------------------------------------------------------------ marks
STAGE_FILES = {k: f"logos/{v}" for k, v in SC.LOGO_FILES.items()}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}
CUTOUT_LANES = SC.CUTOUT_LOGO_LANES


def _xywh(b) -> tuple:
    x, y, w, h = b
    return (x, y, x + w, y + h)


def _tile(x, y) -> tuple:
    return (x, y, x + SC.TILE, y + SC.TILE)


def _src_key(i) -> tuple:
    y = SC.SRC_YS[i]
    return (SC.SRC_X + SC.TILE / 2 - 100, y + SC.TILE + 8,
            SC.SRC_X + SC.TILE / 2 + 100, y + SC.TILE + 8 + SC.KEY_LH)


# Seats in CORE px (x0, y0, x1, y1), each in its own un-shifted frame (the
# safe and its keys shift TOGETHER, the page and its keys slide TOGETHER).
RECTS: dict[str, tuple] = {
    "safe": SC.SAFE_BOX,
    "src-biz": _tile(SC.SRC_X, SC.SRC_YS[0]),
    "src-cli": _tile(SC.SRC_X, SC.SRC_YS[1]),
    "bigpage": SC.PAGE_BOX,
    "fc": _tile(*SC.FC_TILE),
    "key-local": _xywh(SC.KEY_TERM_BOX),
    "key-conf": _xywh(SC.SAFE_KEY_BOX),
    "key-zero": _xywh(SC.SAFE_KEY_BOX),
    "key-src-biz": _src_key(0),
    "key-src-cli": _src_key(1),
    "key-anydoc": _xywh(SC.ANYDOC_BOX),
    "key-os": _xywh(SC.OPENSRC_BOX),
    "key-fc": _xywh(SC.FC_KEY_BOX),
}


def canvas(box):
    """core px -> the canvas this page actually paints (top 192, k 1.00)."""
    return (CORE_K * box[0] + LEFT, CORE_TOP_SPLIT + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP_SPLIT + CORE_K * box[3])


# --------------------------------------------------------------- label plan
# LAW 39 / LAW 50: every name BELOW its host, centred on its axis.
C = SC.CUE
LABEL_PLAN = {
    "key-conf": ("safe", "below", "CONFIDENTIAL"),
    "key-zero": ("safe", "below", "ZERO RISK"),
    "key-src-biz": ("src-biz", "below", "BUSINESS"),
    "key-src-cli": ("src-cli", "below", "CLIENTS"),
    "key-anydoc": ("bigpage", "below", "ANYDOC"),
    "key-os": ("bigpage", "below", "OPEN SOURCE"),
    "key-fc": ("fc", "below", "FIRECRAWL"),
}
LABEL_AT = {"key-local": C["keyterm"], "key-conf": C["conf"],
            "key-zero": C["zero"] + 0.10,
            "key-src-biz": C["biz"] + 0.26, "key-src-cli": C["cli"] + 0.26,
            "key-anydoc": C["anydoc"], "key-os": C["open_src"],
            "key-fc": C["fc_key"]}
HOST_AT = {"safe": C["safe"], "src-biz": C["biz"] + 0.20,
           "src-cli": C["cli"], "bigpage": C["pdf"], "fc": C["fc"]}

# every TYPED string on the board, with its lifetime
PRINTED_KEYS = {k: v[2] for k, v in LABEL_PLAN.items()}
PRINTED_KEYS["key-local"] = SC.KEY_TERM
PRINTED_KEYS["pdf-tag"] = "PDF"
PRINTED_LIFETIME = {k: SC.LIFETIMES[k] for k in
                    ("key-local", "key-conf", "key-zero", "key-anydoc",
                     "key-os", "key-fc", "pdf-tag")}
PRINTED_LIFETIME["key-src-biz"] = SC.LIFETIMES["src-biz"]
PRINTED_LIFETIME["key-src-cli"] = SC.LIFETIMES["src-cli"]

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.
CUE_WORDS = {
    "safe": (0, "hermes"), "hermes": (1, "agent"), "lock": (7, "privacy."),
    "open": (8, "now"), "inside": (10, "read"), "page": (12, "documents"),
    "keyterm": (13, "locally,"), "conf": (23, "confidential"),
    "biz": (28, "business"), "cli": (31, "clients"), "srcout": (32, "and"),
    "hflip": (35, "hermes"), "close": (38, "now"), "zero": (41, "zero"),
    "cloud": (45, "data"), "line": (46, "actually"), "cross": (47, "leaking"),
    "c1out": (49, "they"), "anydoc": (54, "anydoc,"), "open_src": (58, "open"),
    "tag": (60, "pdf"), "scan": (61, "analyzer"), "slide": (62, "built"),
    "fc": (65, "team"), "fc_wire": (66, "over"), "fc_key": (68, "firecrawl."),
    "outro": (69, "now"),
}
# AUTHORED instants: each inside its own word's 1.0 s LABEL_WINDOW
CUE_INSIDE = {"door": (0, "hermes"), "hback": (35, "hermes"),
              "pdf": (49, "they")}


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
    opening = "hermes agent just dropped another banger for privacy."
    head = " ".join(w["text"] for w in ws[:8]).lower()
    if head != opening:
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[8:]).lower()
    if "just dropped another banger" in later:
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
    if SC.BOARD_MODE != "chapters" or len(SC.BOARD_CHAPTERS) != 2:
        raise SystemExit("the scene is no longer the chapters the plan declared")
    edges = [c["erase_at"] for c in SC.BOARD_CHAPTERS]
    if edges != [C["c1out"], C["outro"]]:
        raise SystemExit(f"LAW 43: chapter erases {edges} are off their words")
    rep["_law43"] = {"board_mode": SC.BOARD_MODE, "chapters": 2,
                     "erase_at": edges}
    return rep


# every typed key and the spoken words it must agree with:
# (first spoken word idx, last spoken word idx), spoken text, printed text
WORD_SYNC = {
    "key-local": ((13, 13), "locally,", "LOCALLY"),
    "key-conf": ((23, 23), "confidential", "CONFIDENTIAL"),
    "key-src-biz": ((28, 28), "business", "BUSINESS"),
    "key-src-cli": ((31, 31), "clients", "CLIENTS"),
    "key-zero": ((41, 42), "zero risk", "ZERO RISK"),
    "key-anydoc": ((54, 54), "anydoc,", "ANYDOC"),
    "key-os": ((58, 59), "open source", "OPEN SOURCE"),
    "key-fc": ((68, 68), "firecrawl.", "FIRECRAWL"),
}


def assert_word_sync(ws: list[dict]) -> dict:
    """WORD-SYNC: every typed key first shows the value its words say, while
    (or within 1.0 s after) they are said.  No digit ticks in this video."""
    rows = []
    for key, ((i0, i1), spoken, printed) in WORD_SYNC.items():
        got = " ".join(w["text"] for w in ws[i0:i1 + 1]).lower()
        if got != spoken:
            raise SystemExit(f"word-sync: {key} expects {spoken!r}, the take "
                             f"says {got!r}")
        if PRINTED_KEYS[key] != printed:
            raise SystemExit(f"word-sync: {key} prints {PRINTED_KEYS[key]!r}")
        t = LABEL_AT[key]
        lo = float(ws[i0]["start"])
        hi = float(ws[i1]["end"]) + LABEL_WINDOW
        if not (lo - 0.01 <= t <= hi):
            raise SystemExit(f"word-sync: {key} first shows at {t}, outside "
                             f"{lo:.3f}-{hi:.3f}")
        rows.append({"state": key, "first_visible_text": printed, "at": t,
                     "words": got, "window": [round(lo, 3), round(hi, 3)]})
    rows.append({"state": "pdf-tag", "first_visible_text": "PDF",
                 "at": C["pdf"] + 0.20,
                 "words": "They (16.88) - the page's own file-type tag; its "
                          "border flips on 'PDF' (20.44)",
                 "kind": "object chrome: part of the drawn PDF page"})
    if min(LABEL_AT.values()) != LABEL_AT["key-local"]:
        raise SystemExit("LAW 9: LOCALLY is not the first type on the board")
    return {"typed_states": rows, "disagreements": 0, "digits_that_tick": 0}


def assert_law37(ws: list[dict]) -> dict:
    cues = PCUE.scan(ws)
    plan = json.loads(PLAN.read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / "prep/stages/hermesdocs.cues.json").read_text())
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
        if kb[1] < hb[3] - 0.01:
            raise SystemExit(f"LAW 39: {key} is not entirely below {host}")
        kc, hc = (kb[0] + kb[2]) / 2, (hb[0] + hb[2]) / 2
        if abs(kc - hc) > 0.15 * (hb[2] - hb[0]) + 0.01:
            raise SystemExit(f"LAW 39: {key} is off {host}'s axis")
        if not any(key in b and host in b for b in blocks):
            raise SystemExit(f"LAW 41: {key} is not blocked with {host}")
        if LABEL_AT[key] < HOST_AT[host] - 1e-9:
            raise SystemExit(f"LAW 39: {key} lands before its host")
        out[key] = {"host": host, "side": side, "text": text,
                    "at": LABEL_AT[key],
                    "gutter_core_px": round(kb[1] - hb[3], 1),
                    "box_canvas": [round(v, 1) for v in canvas(kb)]}
    # LAW 50: one plain label size, sibling names share one row height
    if RECTS["key-anydoc"][3] - RECTS["key-anydoc"][1] != \
            RECTS["key-os"][3] - RECTS["key-os"][1]:
        raise SystemExit("LAW 50: ANYDOC / OPEN SOURCE rows differ")
    out["_law50"] = {"plain_label_font_px": SC.KEY_FS,
                     "row_px": SC.KEY_LH}
    du = SC.KEY_TERM_FS / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} du")
    out["_key_term"] = {"text": SC.KEY_TERM, "font_px": SC.KEY_TERM_FS,
                        "design_units": round(du, 2), "first_type": True}
    return out


def assert_lifetime_law() -> dict:
    """LAW 42 (chaptered build): every mark has a finite t_to or is a
    declared anchor."""
    anchors = [n for n, (_a, b) in SC.LIFETIMES.items() if b is None]
    for n in anchors:
        if n not in SC.SCENE_ANCHORS:
            raise SystemExit(f"LAW 42: {n} never leaves and is not an anchor")
    shares = {n: round((b - a) / DUR, 3)
              for n, (a, b) in SC.LIFETIMES.items() if b is not None}
    return {"board_mode": SC.BOARD_MODE, "anchors": sorted(anchors),
            "longest_marks": sorted(shares.items(), key=lambda kv: -kv[1])[:3],
            "every_non_anchor_finite": True}


# LAW 38 rule 2: every target is a DRAWN object -> each emphasis is the
# object's own border/outline flipping terracotta.  Nothing added to the DOM.
FLIP_D = 0.38
EMPH_HERMES_CHECK = round(C["hflip"] + FLIP_D + 0.12, 2)      # 12.36
EMPH_SAFE_CHECK = round(C["zero"] + FLIP_D + 0.12, 2)         # 14.62
EMPH_TAG_CHECK = round(C["tag"] + FLIP_D + 0.12, 2)           # 20.94
EMPHASES = [
    # (element id, target id, from, until, check)
    ("hermes", "hermes-mark", C["hflip"], C["hback"], EMPH_HERMES_CHECK),
    ("safe-body", "safe-door", C["zero"], SC.LIFETIMES["emph-safe"][1],
     EMPH_SAFE_CHECK),
    ("pdf-tag", "pg-edge", C["tag"], SC.LIFETIMES["pdf-tag"][1],
     EMPH_TAG_CHECK),
]


def assert_emphasis_law() -> dict:
    for eid, _t, a, b, chk in EMPHASES:
        if a + FLIP_D > b or not (a + FLIP_D <= chk < b):
            raise SystemExit(f"LAW 38: the flip on #{eid} does not complete "
                             "before it returns")
    return {"border_flips": [{"id": e, "target": t, "from": a, "until": b,
                              "check_at": c} for e, t, a, b, c in EMPHASES],
            "rings_ellipses_circles": 0, "highlights": 0,
            "dom_elements_added": 0}


def assert_cast_law() -> dict:
    rep = DF.assert_cast_resolves(list(SC.LOGO_FILES), dict(SC.LOGO_FILES),
                                  LOGOS, label="hermesdocs stage marks")
    if "automation/hermes-agent.png" in SC.LOGO_FILES.values():
        raise SystemExit("MARK IDENTITY: Hermes is the Nous girl, never the H")
    return {"stage_marks": sorted(SC.LOGO_FILES),
            "resolved": {k: v["path"] for k, v in rep.items()},
            "cutout_lanes_not_ours": list(CUTOUT_LANES)}


_DRAWN = r'<(?:path|polyline|polygon|line|rect)\b[^>]*>'


def _tags_for(sel: str, html: str) -> list[str]:
    parts = sel.split()
    if not parts[0].startswith("#") or len(parts) > 2:
        raise SystemExit(f"unexpected dash selector {sel}")
    hid = parts[0][1:]
    if len(parts) == 1:
        return [t for t in re.findall(_DRAWN, html)
                if re.search(rf'\bid="{re.escape(hid)}"', t)]
    want = [c for c in parts[1].split(".") if c]
    m = re.search(rf'id="{re.escape(hid)}"(.*?)</svg>', html, re.S)
    if not m:
        return []
    out = []
    for tag in re.findall(_DRAWN, m.group(1)):
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


# connector id -> (declared target in the module, measured target, side,
# fraction, check-at).  Fractions are computed from the target's own geometry
# box (an SVG shape's box excludes its stroke; a bordered div's includes it).
def _frac_y(y, box):
    return round((y - box[1]) / (box[3] - box[1]), 4)


# INKLESS VIRTUAL RECTS (the streamdeck precedent, run 27): the outline's
# OUTER edge, where the design agent landed every end (handoff section 5,
# "0.0 px gap at all eight ends").  An SVG shape's DOM box is its stroke
# CENTRE-line geometry, 4 px inside the painted edge of an 8 px outline.
SAFE_EDGE = SC.SAFE_BOX                                   # 380,160 .. 700,460
# the cloud's measured getBBox() (224.23, 231.75, 153.77 x 120.25) grown by
# half its 8 px stroke: its painted outer box.
CLOUD_GEOM = (224.23, 231.75, 378.0, 352.0)
_h = SC.CLOUD_STROKE / 2
CLOUD_EDGE = (CLOUD_GEOM[0] - _h, CLOUD_GEOM[1] - _h,
              CLOUD_GEOM[2] + _h, CLOUD_GEOM[3] + _h)
if abs(CLOUD_EDGE[2] - SC.LEAK[0][0]) > 0.01:
    raise SystemExit("the leak line no longer ends on the cloud's right bump")

CONNECTOR_DECL = {
    "arw-0": ("safe", "safe-edge", "left", _frac_y(SC.ARROW_DST[0][1], SAFE_EDGE),
              round(C["biz"] + 0.46 + 0.30 + 0.10, 2)),
    "arw-1": ("safe", "safe-edge", "left", _frac_y(SC.ARROW_DST[1][1], SAFE_EDGE),
              round(C["cli"] + 0.46 + 0.30 + 0.10, 2)),
    # the leak line is drawn FROM the safe and ENDS on the cloud's right bump
    "leak-l": ("safe", "cloud-outer", "right", _frac_y(SC.LEAK[0][1], CLOUD_EDGE),
               round(C["line"] + 0.40 + 0.12, 2)),
    "fc-l": ("fc", "fc", "left", 0.5, round(C["fc_wire"] + 0.34 + 0.12, 2)),
}


def assert_connectors(scene_html: str) -> dict:
    got = re.findall(r'id="((?:arw|leak|fc)-[^"]+)"[^>]*?data-connect-to="([^"]+)"',
                     scene_html)
    ids = {c["id"] for c in SC.CONNECTORS}
    if {g[0] for g in got} != ids or ids != set(CONNECTOR_DECL):
        raise SystemExit(f"LAW 40: connectors in the page {got} != {sorted(ids)}")
    life = {"arw-0": SC.LIFETIMES["arrows"], "arw-1": SC.LIFETIMES["arrows"],
            "leak-l": SC.LIFETIMES["leak"], "fc-l": SC.LIFETIMES["fcwire"]}
    for cid, tgt in got:
        if CONNECTOR_DECL[cid][0] != tgt:
            raise SystemExit(f"LAW 40: {cid} declares {tgt}")
        a0, a1 = life[cid]
        chk = CONNECTOR_DECL[cid][4]
        if not (a0 + 0.30 <= chk < a1 - EXIT_GUARD):
            raise SystemExit(f"LAW 40: {cid} is checked at {chk}, outside its "
                             f"drawn life {a0}-{a1}")
    return {"connectors": [{"id": c["id"], "from": c["from"], "to": c["to"],
                            "ends": c["ends"]} for c in SC.CONNECTORS]}


EXIT_GUARD = 0.0


def _insert_first_child(s: str, host: str, frag: str) -> str:
    m = re.search(rf'<div class="abs [^"]*" id="{re.escape(host)}"[^>]*>', s)
    if not m or s.count(f'id="{host}"') != 1:
        raise SystemExit(f"cannot find ONE #{host} for its virtual rect")
    return s[:m.end()] + frag + s[m.end():]


def declare_contracts(html: str) -> tuple[str, dict]:
    """Stamp LAW 40 / LAW 38 measurement declarations on the EMITTED html."""
    s = html
    rep: dict = {"connectors": {}, "emphases": []}
    # -- inkless virtual rects, inside the element they belong to (so they
    #    ride the scene's own x tweens and leave with their chapter)
    ox, oy = SC.SAFE_DIV[0], SC.SAFE_DIV[1]
    x0, y0, x1, y1 = SAFE_EDGE
    s = _insert_first_child(
        s, "safe", f'<div id="safe-edge" class="abs" style="left:{x0 - ox:.0f}px;'
        f'top:{y0 - oy:.0f}px;width:{x1 - x0:.0f}px;height:{y1 - y0:.0f}px" '
        f'data-virtual-rect></div>')
    x0, y0, x1, y1 = CLOUD_EDGE
    s = _insert_first_child(
        s, "cloud", f'<div id="cloud-outer" class="abs" style="left:{x0:.2f}px;'
        f'top:{y0:.2f}px;width:{x1 - x0:.2f}px;height:{y1 - y0:.2f}px" '
        f'data-virtual-rect></div>')
    rep["virtual_rects"] = {"safe-edge": SAFE_EDGE, "cloud-outer": CLOUD_EDGE}
    for cid, (tgt, meas, side, frac, chk) in CONNECTOR_DECL.items():
        key = f'data-connect-to="{tgt}"'
        fr = "" if frac is None else f'data-anchor-fraction="{frac:g}" '
        pat = re.compile(rf'(id="{re.escape(cid)}"[^>]*?){re.escape(key)}')
        s, n = pat.subn(rf'\1data-connect-to="{meas}" '
                        rf'data-anchor-side="{side}" {fr}'
                        rf'data-check-at="{chk:.2f}"', s)
        if n != 1:
            raise SystemExit(f"LAW 40: could not declare {cid} ({n} matches)")
        rep["connectors"][cid] = {"module_to": tgt, "to": meas, "side": side,
                                  "fraction": frac, "check_at": chk}
    # the two source arrows: the painted triangle TIP is the connector's end
    n_heads = 0
    for i in range(2):
        pat = re.compile(rf'(<g id="arw-{i}"[^>]*><path class="arw-l"[^>]*/>)'
                         r'<path d="M')
        s, n = pat.subn(r'\1<path data-connector-head="1" d="M', s)
        n_heads += n
    if n_heads != 2:
        raise SystemExit(f"could not mark the two arrowheads ({n_heads})")
    # emphases (LAW 38 rule 2): border / outline flips on drawn objects
    for eid, tgt, _a, _b, chk in EMPHASES:
        pat = re.compile(rf'id="{re.escape(eid)}"')
        s, n = pat.subn(f'id="{eid}" data-emphasis="border" '
                        f'data-emphasis-target="{tgt}" '
                        f'data-check-at="{chk:.2f}"', s, count=1)
        if n != 1:
            raise SystemExit(f"cannot stamp the emphasis on #{eid}")
        if f'id="{tgt}"' not in s:
            raise SystemExit(f"emphasis target #{tgt} is not in the page")
        rep["emphases"].append({"id": eid, "target": tgt, "kind": "border",
                                "check_at": chk})
    if s.count("data-check-at") != len(CONNECTOR_DECL) + len(EMPHASES):
        raise SystemExit("a declared mark lacks its data-check-at")
    return s, rep


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


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", text.lower().replace("-", " ")).strip()


def _is_board_key(text: str) -> str | None:
    norm = _norm(text)
    for key, t in PRINTED_KEYS.items():
        if norm == _norm(t):
            return key
    return None


SOLO_WORD_PENALTY = 250_000.0
NAME_PAIRS = (("hermes", "agent"), ("open", "source"), ("zero", "risk"))


def _splits_name(a: dict, b: dict) -> bool:
    """PROPER-NOUN SPELLING: a pill never ends on "Hermes" when the next pill
    opens on "Agent" (one product name), nor splits "open source" / "zero
    risk" (one phrase each)."""
    x = a["text"].strip().lower()
    y = re.sub(r"[^a-z]", "", b["text"].strip().lower())
    return any(x == p and y == q for p, q in NAME_PAIRS)


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
            if w > max_w or _norm(txt) in forbidden:
                continue
            if j < n and _splits_name(union[j - 1], union[j]):
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
    forbidden = {_norm(t) for t in PRINTED_KEYS.values()}
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
const none = "none";
const hidden = "hidden";
const POP="back.out(2.05)";const SOFT="power3.out";const SWING="power2.inOut";
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
    """The two rasters the scene paints (handoff section 1)."""
    return {
        "_hermes_img": CC.mark_img(LOGO_URL["nous-girl-line"], "nous-girl-line",
                                   SC.HERMES_MARK, eid="hermes-mark"),
        "_fc_img": CC.mark_img(LOGO_URL["firecrawl"], "firecrawl", SC.FC_MARK,
                               eid="fc-mark"),
    }


def sfx_plan() -> list[tuple]:
    """EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22)."""
    return [("pop", C["safe"], SFX_STRUCTURE),          # the safe, alone
            ("pop", C["hermes"], SFX_DETAIL),           # the Nous girl tile
            ("click", C["lock"], SFX_DETAIL),           # the dial locks
            ("whoosh", C["open"], SFX_DETAIL),          # the door swings open
            ("whoosh", C["inside"], SFX_DETAIL),        # Hermes moves inside
            ("pop", C["page"], SFX_DETAIL),             # the first page
            ("click", C["keyterm"], SFX_DETAIL),        # LOCALLY
            ("click", C["conf"], SFX_DETAIL),           # CONFIDENTIAL
            ("pop", C["biz"] + 0.20, SFX_STRUCTURE),    # the building tile
            ("pop", C["cli"], SFX_DETAIL),              # the client tile
            ("whoosh", C["srcout"], SFX_STRUCTURE),     # the sources leave
            ("whoosh", C["close"] + 0.16, SFX_DETAIL),  # the door swings shut
            ("click", C["close"] + 0.50, SFX_DETAIL),   # the dial turns back
            ("click", C["zero"] + 0.10, SFX_DETAIL),    # ZERO RISK
            ("whoosh", C["cloud"], SFX_STRUCTURE),      # slide + the cloud
            ("click", C["line"], SFX_DETAIL),           # the leak line
            ("pop", C["cross"], SFX_STRUCTURE),         # the X lands
            ("whoosh", C["c1out"], SFX_STRUCTURE),      # chapter 1 leaves
            ("click", C["anydoc"], SFX_DETAIL),         # ANYDOC
            ("click", C["open_src"], SFX_DETAIL),       # OPEN SOURCE
            ("whoosh", C["scan"], SFX_DETAIL),          # the scan sweep
            ("whoosh", C["slide"], SFX_DETAIL),         # the page slides
            ("pop", C["fc"], SFX_STRUCTURE),            # the Firecrawl tile
            ("click", C["fc_wire"], SFX_DETAIL),        # the page -> tile line
            ("click", C["fc_key"], SFX_DETAIL),         # FIRECRAWL
            ("whoosh", C["outro"], SFX_STRUCTURE)]      # the rising sheet


def assert_sfx(sfx) -> dict:
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30:
        raise SystemExit(f"SFX flam: {worst}")
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "deliberately_silent": {
                "door parts 0.36": "0.26 s after the safe's pop",
                "the slide 9.62": "the building pop 0.20 s later scores it",
                "arrows / pages 10.08-11.16": "each within 0.40 s of a tile pop",
                "the chapter-2 page 16.92": "0.04 s after the chapter whoosh",
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


# the x each typed key actually sits at when it is on screen (the scene's own
# LAW 19 displacements): the safe keys ride SHIFT1 / SHIFT2, the page keys
# start centred and slide by SLIDE.
KEY_SHIFTS = {"key-local": (0.0,), "key-conf": (0.0, SC.SHIFT1),
              "key-zero": (SC.SHIFT1, SC.SHIFT2),
              "key-src-biz": (0.0,), "key-src-cli": (0.0,),
              "key-anydoc": (0.0, SC.SLIDE), "key-os": (0.0, SC.SLIDE),
              "key-fc": (0.0,)}


def guard_rail() -> dict:
    # the rail binds readable INK: JetBrains Mono advances 0.600 em
    def ink(text, fs, ls):
        return len(text) * 0.6 * fs + (len(text) - 1) * ls
    rights, lefts = {}, {}
    for n, text in PRINTED_KEYS.items():
        if n == "pdf-tag":
            continue
        b = canvas(RECTS[n])
        fs, ls = ((SC.KEY_TERM_FS, SC.KEY_TERM_LS) if n == "key-local"
                  else (SC.KEY_FS, SC.KEY_LS))
        c = (b[0] + b[2]) / 2
        rights[n] = max(c + dx for dx in KEY_SHIFTS[n]) + ink(text, fs, ls) / 2
        lefts[n] = min(c + dx for dx in KEY_SHIFTS[n]) - ink(text, fs, ls) / 2
    type_right = max(rights.values())
    if type_right > CAP.LAW12_RAIL_X + 0.01:
        raise SystemExit(f"readable key ink reaches x={type_right:.1f}")
    # widest composed states (handoff section 2)
    ink_left = min(SC.SRC_X, CLOUD_EDGE[0])
    ink_right = SC.HINGES[0][0] + SC.HINGES[0][2] + SC.SHIFT2
    if ink_left < 30 or W - ink_right < 30 or min(lefts.values()) < 30:
        raise SystemExit("the composition leaves the frame margin")
    return {"readable_type_right_x": round(type_right, 1),
            "per_key_right_x": {k: round(v, 1) for k, v in rights.items()},
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
    conns = assert_connectors(scene_html)
    scene_html, conns["declared"] = declare_contracts(scene_html)
    for shape in ("<circle", "<ellipse"):
        if shape in scene_html:
            raise SystemExit(f"LAW 38 rule 3: {shape} in the emitted scene")

    m = CAP.PillMeasurer(RUN / "gen/_pillwidths_hermesdocs_split.json")
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
            "law40": conns, "law2": cast, "law22": sfx_guard,
            "draw_on": drawon, "transcript": cap_rep, "phone_objects": objs,
            "render": {"w": 1080, "h": 1920, "zoom": 1}}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="split", choices=("split",))
    ap.parse_args()
    dst = RUN / "projects/hermesdocs_split"
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
    (RUN / "gen/_build_hermesdocs_split.json").write_text(
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
                      "draw_on": rep["draw_on"],
                      "law40": rep["law40"]["declared"],
                      "phone": rep["phone_objects"]}, indent=1))


if __name__ == "__main__":
    main()
