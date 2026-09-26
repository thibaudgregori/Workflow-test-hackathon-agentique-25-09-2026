#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION — falagent / ICON CHOREOGRAPHY.

    YouTube   classic split 50/50   projects/falagent_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/falagent_scene.py` plus
`plans/falagent_scene_handoff.md` are the design agent's artefacts, sealed by
`review/artwork_pass_falagent.json` (production v4, `production.py seal`).
This file IMPORTS the module and SEATS it at the handoff's own placement
(k = 1.00, left 0, core top 192).  It never mutates a byte of the module.

FORMAT-SIDE STAMPS ON THE EMITTED STRING (the module on disk is untouched):
  * the five connectors get `data-anchor-side`, `data-anchor-fraction` and
    `data-check-at` (production's LAW 40 contract), each checked after its
    line has drawn and before its chapter erases;
  * the two border flips (LAW 38 rule 2, both on DRAWN objects) are declared
    `data-emphasis="border"` with their target and check instant: `#model-1`
    (the chosen tile's own border) -> its mark, and the three film-strip frame
    outlines -> the strip's body.

HD DELIVERY: authored AND encoded 1080x1920.  The face plate is
`face_bottom_hd.mp4` (1080x1058), so the seam is 1920 - 1057.5 = 862.5 and the
RENDERING pill top is 862.5 - 114.59/2 = 805.205 (the pill that renders, never
the frozen 108.2 seat constant).  The core's content band 86..494 lands at
canvas 278..686: 86 px under LAW 30's top-10 % line and ~119 px over the pill.

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
import falagent_scene as SC                     # noqa: E402

RUN = Path(__file__).resolve().parents[1]
CUT = RUN / "cuts/falagent"
PLAN = RUN / "plans/falagent_plan.json"
ASSETS = Path.home() / "Documents/Workspace/assets"
LOGOS = ASSETS / "logos"
LIB_MUSIC = ASSETS / "audio/music/shorts-factory"
LIB_SFX = ASSETS / "audio/sfx/shorts-factory"

VID = "falagent"
W, H = 1080.0, 1920.0
FPS = 25
DUR = SC.DUR                                     # 33.24, the cut master

SEAM = 862.5
CORE_TOP_SPLIT = SC.CANVAS_OFFSET                # 192.0, the handoff's number
CORE_K = 1.00
LEFT = (W - SC.CORE_W * CORE_K) / 2              # 0.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "fal.ai released its own agent: fal agent"
LABEL_WINDOW = 1.0

# ------------------------------------------------------------------ marks
STAGE_FILES = {k: f"logos/{v}" for k, v in SC.LOGO_FILES.items()}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}
CUTOUT_LANES = SC.CUTOUT_LOGO_LANES


def _xywh(b) -> tuple:
    x, y, w, h = b
    return (x, y, x + w, y + h)


# Seats in CORE px (x0, y0, x1, y1)
RECTS: dict[str, tuple] = {
    "fal-tile": SC.FAL0_BOX, "clapper": SC.CLAP_BOX, "easel": SC.EASEL_BOX,
    "model-row": SC.ROW_BOX, "dartboard": SC.DB_BOX, "strip": SC.ST_BOX,
    "fal-tile-2": SC.FAL2_BOX, "window": SC.WIN_BOX,
    "key-falagent": _xywh(SC.KEY_FAL_BOX),
    "key-videos": _xywh(SC.KEY_VIDEOS_BOX),
    "key-images": _xywh(SC.KEY_IMAGES_BOX),
    "key-model": _xywh(SC.KEY_MODEL_BOX),
    "key-prompt": _xywh(SC.KEY_PROMPT_BOX),
    "key-consistent": _xywh(SC.KEY_CONS_BOX),
    "key-tuned": _xywh(SC.KEY_TUNED_BOX),
    "key-anygen": _xywh(SC.KEY_ANYGEN_BOX),
}


def canvas(box):
    """core px -> the canvas this page actually paints (top 192, k 1.00)."""
    return (CORE_K * box[0] + LEFT, CORE_TOP_SPLIT + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP_SPLIT + CORE_K * box[3])


# --------------------------------------------------------------- label plan
# LAW 39 / LAW 50: every key BELOW its host, centred on its axis.
LABEL_PLAN = {
    "key-falagent": ("fal-tile", "below", SC.KEY_TERM),
    "key-videos": ("clapper", "below", "VIDEOS"),
    "key-images": ("easel", "below", "IMAGES"),
    "key-model": ("model-row", "below", "THE MODEL"),
    "key-prompt": ("dartboard", "below", "THE PROMPT"),
    "key-consistent": ("strip", "below", "CONSISTENT"),
    "key-tuned": ("fal-tile-2", "below", "FINE-TUNED"),
    "key-anygen": ("window", "below", "ANY GENERATION"),
}
C = SC.CUE
LABEL_AT = {"key-falagent": C["keyterm"], "key-videos": C["k_videos"],
            "key-images": C["k_images"], "key-model": C["k_model"],
            "key-prompt": C["k_prompt"], "key-consistent": C["k_consist"],
            "key-tuned": C["k_tuned"], "key-anygen": C["k_anygen"]}
HOST_AT = {"fal-tile": C["fal"], "clapper": C["clap"], "easel": C["easel"],
           "model-row": C["seam2"], "dartboard": C["seam3"],
           "strip": C["seam4"], "fal-tile-2": C["seam5"],
           "window": C["seam6"]}

# every TYPED string on the board, with its lifetime
PRINTED_KEYS = {k: v[2] for k, v in LABEL_PLAN.items()}
PRINTED_KEYS["url"] = "fal.ai"
PRINTED_LIFETIME = {k: SC.LIFETIMES[k] for k in LABEL_PLAN}
PRINTED_LIFETIME["url"] = SC.LIFETIMES["url"]

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.
CUE_WORDS = {
    "palette": (0, "creative"), "spark": (4, "ai"), "slide": (9, "best"),
    "fal": (11, "fal.ai"), "friend": (12, "just"), "keyterm": (15, "agent."),
    "seam1": (19, "creative"), "clap": (25, "videos"),
    "easel": (27, "images,"), "seam2": (33, "choosing"), "pick": (34, "the"),
    "k_model": (35, "model."), "pickout": (36, "it's"),
    "seam3": (37, "getting"), "k_prompt": (39, "prompt"),
    "seam4": (45, "all"), "cats": (48, "generations"),
    "k_consist": (50, "consistent"), "emph": (51, "across"),
    "seam5": (54, "fal"), "k_tuned": (58, "fine-tuned"), "both": (60, "do"),
    "links": (61, "exactly"), "seam6": (72, "inside"), "url": (76, "website"),
    "help": (80, "help"), "gen_links": (81, "you"),
    "k_anygen": (84, "generation"), "outro": (89, "now"),
}
# AUTHORED instants: each inside its own word's 1.0 s LABEL_WINDOW
CUE_INSIDE = {"k_videos": (25, "videos"), "snap": (25, "videos"),
              "k_images": (27, "images,")}
# the dart is authored to LAND (13.70 + 0.18) inside 'right' (13.76-13.94)
DART_LAND = C["dart"] + 0.18
DART_WORD = (40, "right")


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
    opening = "creative people working with ai now have a new best friend."
    head = " ".join(w["text"] for w in ws[:11]).lower()
    if head != opening:
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[11:]).lower()
    if "creative people working" in later:
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
           + f" — {tail:.3f}s past the last word against a {cap:.3f}s cap",
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
    idx, text = DART_WORD
    w = ws[idx]
    if w["text"].strip().lower() != text or not (
            float(w["start"]) <= DART_LAND <= float(w["end"])):
        raise SystemExit(f"the dart lands at {DART_LAND:.2f}, not inside "
                         f"{w['text']!r}")
    rep["dart"] = {"word": idx, "text": w["text"], "starts": C["dart"],
                   "lands": round(DART_LAND, 2),
                   "word_span": [w["start"], w["end"]]}
    missing = set(C) - set(rep)
    if missing:
        raise SystemExit(f"cues the build never verified: {sorted(missing)}")
    if SC.BOARD_MODE != "chapters" or len(SC.BOARD_CHAPTERS) != 8:
        raise SystemExit("the scene is no longer the chapters the plan declared")
    edges = [c["erase_at"] for c in SC.BOARD_CHAPTERS[:-1]]
    want = [C["seam1"], C["seam2"], C["seam3"], C["seam4"], C["seam5"],
            C["seam6"], C["outro"]]
    if edges != want:
        raise SystemExit(f"LAW 43: chapter erases {edges} are off their words")
    rep["_law43"] = {"board_mode": SC.BOARD_MODE, "chapters": 8,
                     "erase_at": edges}
    return rep


# every typed key and the spoken words it must agree with:
# (first spoken word idx, last spoken word idx), spoken text, printed text
WORD_SYNC = {
    "key-falagent": ((14, 15), "fal agent.", "FAL AGENT"),
    "key-videos": ((25, 25), "videos", "VIDEOS"),
    "key-images": ((27, 27), "images,", "IMAGES"),
    "key-model": ((34, 35), "the model.", "THE MODEL"),
    "key-prompt": ((38, 39), "the prompt", "THE PROMPT"),
    "key-consistent": ((50, 50), "consistent", "CONSISTENT"),
    "key-tuned": ((58, 58), "fine-tuned", "FINE-TUNED"),
    "key-anygen": ((83, 84), "any generation", "ANY GENERATION"),
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
    rows.append({"state": "url", "first_visible_text": "fal.ai",
                 "at": C["url"], "words": "their own website (25.14)",
                 "kind": "UI chrome: the address bar of fal's own website"})
    if min(LABEL_AT.values()) != LABEL_AT["key-falagent"] or \
            C["url"] < LABEL_AT["key-falagent"]:
        raise SystemExit("LAW 9: FAL AGENT is not the first type on the board")
    return {"typed_states": rows, "disagreements": 0, "digits_that_tick": 0}


def assert_law37(ws: list[dict]) -> dict:
    cues = PCUE.scan(ws)
    plan = json.loads(PLAN.read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / "prep/stages/falagent.cues.json").read_text())
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
            # the chapter-5 plate and its key are one declared block
            raise SystemExit(f"LAW 41: {key} is not blocked with {host}")
        if LABEL_AT[key] < HOST_AT[host] - 1e-9:
            raise SystemExit(f"LAW 39: {key} lands before its host")
        out[key] = {"host": host, "side": side, "text": text,
                    "at": LABEL_AT[key],
                    "gutter_core_px": round(kb[1] - hb[3], 1),
                    "box_canvas": [round(v, 1) for v in canvas(kb)]}
    # LAW 50: the two sibling labels share one baseline and one size
    if RECTS["key-videos"][1] != RECTS["key-images"][1] or \
            RECTS["key-videos"][3] != RECTS["key-images"][3]:
        raise SystemExit("LAW 50: VIDEOS / IMAGES do not share one row")
    out["_law50"] = {"plain_label_font_px": SC.KEY_FS,
                     "videos_images_same_row": True}
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


# LAW 38 rule 2: both targets are DRAWN objects -> each emphasis is the
# object's own border/outline flipping terracotta.  Nothing added to the DOM.
EMPH_MODEL_CHECK = round(C["pick"] + 0.30 + 0.12, 2)          # 12.44
EMPH_STRIP_CHECK = round(C["emph"] + 0.30 + 0.12, 2)          # 17.46


def assert_emphasis_law() -> dict:
    flips = [("#model-1", C["pick"], C["pickout"], EMPH_MODEL_CHECK),
             ("#strip .stfr", C["emph"], C["seam5"] - 0.20, EMPH_STRIP_CHECK)]
    for tgt, a, b, chk in flips:
        if a + 0.30 > b or not (a + 0.30 <= chk < b):
            raise SystemExit(f"LAW 38: the flip on {tgt} does not complete "
                             "before it returns")
    return {"border_flips": [{"target": t, "from": a, "until": b,
                              "check_at": c} for t, a, b, c in flips],
            "rings_ellipses_circles": 0, "highlights": 0,
            "dom_elements_added": 0}


def assert_cast_law() -> dict:
    rep = DF.assert_cast_resolves(list(SC.LOGO_FILES), dict(SC.LOGO_FILES),
                                  LOGOS, label="falagent stage marks")
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


# connector id -> (target, side, fraction, check-at): after the draw, before
# its chapter erases.
CONNECTOR_DECL = {
    "conn-friend": ("fal-tile", "left", 0.5, 5.60),
    "conn-prompt": ("dartboard-2", "top", 0.5, 23.00),
    "conn-consist": ("strip-2", "top", 0.5, 23.00),
    "conn-out-a": ("out-image", "left", 0.5, 28.60),
    "conn-out-b": ("out-video", "left", 0.5, 28.60),
}


def assert_connectors(scene_html: str) -> dict:
    got = re.findall(r'id="(conn-[^"]+)"[^>]*?data-connect-to="([^"]+)"',
                     scene_html)
    if {g[0] for g in got} != set(SC.CONNECTORS) or \
            {g[0] for g in got} != set(CONNECTOR_DECL):
        raise SystemExit(f"LAW 40: connectors in the page {got} != "
                         f"{sorted(SC.CONNECTORS)}")
    for cid, tgt in got:
        if SC.CONNECTORS[cid]["to"] != tgt or CONNECTOR_DECL[cid][0] != tgt:
            raise SystemExit(f"LAW 40: {cid} declares {tgt}")
        a0, a1 = SC.LIFETIMES[cid]
        chk = CONNECTOR_DECL[cid][3]
        if not (a0 + 0.40 <= chk < a1):
            raise SystemExit(f"LAW 40: {cid} is checked at {chk}, outside its "
                             f"drawn life {a0}-{a1}")
    targets = [t for _c, t in got]
    if len(targets) != len(set(targets)):
        raise SystemExit("LAW 40: a target receives two lines")
    return {"connectors": [{"id": c, "to": t,
                            "ends": SC.CONNECTORS[c]["ends"]} for c, t in got]}


def declare_contracts(html: str) -> tuple[str, dict]:
    """Stamp LAW 40 / LAW 38 measurement declarations on the EMITTED html."""
    s = html
    rep: dict = {"connectors": {}, "emphases": []}
    for cid, (tgt, side, frac, chk) in CONNECTOR_DECL.items():
        key = f'data-connect-to="{tgt}"'
        pat = re.compile(rf'(id="{re.escape(cid)}"[^>]*?){re.escape(key)}')
        s, n = pat.subn(rf'\1{key} data-anchor-side="{side}" '
                        rf'data-anchor-fraction="{frac:g}" '
                        rf'data-check-at="{chk:.2f}"', s)
        if n != 1:
            raise SystemExit(f"LAW 40: could not declare {cid} ({n} matches)")
        rep["connectors"][cid] = {"to": tgt, "side": side, "fraction": frac,
                                  "check_at": chk}
    # emphasis 1: the chosen tile's own border -> its mark (the tile's img)
    m = re.search(r'(<div class="abs node" id="model-1"[^>]*>)(<img\b)', s)
    if not m:
        raise SystemExit("cannot find #model-1 and its mark")
    s = (s[:m.start()]
         + m.group(1).replace('id="model-1"',
                              'id="model-1" data-emphasis="border" '
                              'data-emphasis-target="model-1-mark" '
                              f'data-check-at="{EMPH_MODEL_CHECK:.2f}"')
         + '<img id="model-1-mark"' + s[m.end():])
    rep["emphases"].append({"id": "model-1", "target": "model-1-mark",
                            "kind": "border", "check_at": EMPH_MODEL_CHECK})
    # emphasis 2: the strip's three frame outlines -> the strip's body
    body_pat = re.compile(r'<rect class="stk stbody"')
    s, n = body_pat.subn('<rect id="strip-body" class="stk stbody"', s)
    if n != 1:
        raise SystemExit(f"cannot stamp the strip body ({n})")
    i = 0

    def fr(mm):
        nonlocal i
        out = (f'<rect id="strip-frame-{i}" data-emphasis="border" '
               f'data-emphasis-target="strip-body" '
               f'data-check-at="{EMPH_STRIP_CHECK:.2f}" class="stk stfr"')
        i += 1
        return out
    s, n = re.subn(r'<rect class="stk stfr"', fr, s)
    if n != 3:
        raise SystemExit(f"expected three strip frames, found {n}")
    rep["emphases"] += [{"id": f"strip-frame-{k}", "target": "strip-body",
                         "kind": "border", "check_at": EMPH_STRIP_CHECK}
                        for k in range(3)]
    if s.count("data-check-at") != len(CONNECTOR_DECL) + 4:
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


def _splits_name(a: dict, b: dict) -> bool:
    """PROPER-NOUN SPELLING: a pill never ends on "fal" when the next pill
    opens on "agent" (the product is one name, "fal agent")."""
    return (a["text"].strip().lower() == "fal"
            and b["text"].strip().lower().startswith("agent"))


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
    """The five rasters the scene paints (handoff section 1)."""
    return {f"_{key}_img": CC.mark_img(LOGO_URL[key], key, SC.MEDIA_SIDES[key])
            for key in SC.LOGO_FILES}


def sfx_plan() -> list[tuple]:
    """EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22)."""
    return [("pop", C["palette"], SFX_STRUCTURE),     # the palette, alone
            ("pop", C["spark"], SFX_DETAIL),          # the AI spark
            ("whoosh", C["slide"], SFX_DETAIL),       # palette makes room
            ("pop", C["fal"], SFX_STRUCTURE),         # the fal plate
            ("click", C["friend"], SFX_DETAIL),       # the friendship line
            ("click", C["keyterm"], SFX_DETAIL),      # FAL AGENT
            ("whoosh", C["seam1"], SFX_STRUCTURE),    # chapter 0 leaves
            ("pop", C["clap"], SFX_DETAIL),           # the clapperboard
            ("click", C["snap"] + 0.10, SFX_DETAIL),  # the stick SHUTS (8.90)
            ("pop", C["easel"], SFX_DETAIL),          # the easel
            ("whoosh", C["seam2"], SFX_STRUCTURE),    # the model row
            ("click", C["k_model"], SFX_DETAIL),      # THE MODEL
            ("whoosh", C["seam3"], SFX_STRUCTURE),    # the dartboard
            ("click", C["k_prompt"], SFX_DETAIL),     # THE PROMPT
            ("pop", DART_LAND, SFX_STRUCTURE),        # the dart lands
            ("whoosh", C["seam4"], SFX_STRUCTURE),    # the film strip
            ("pop", C["cats"], SFX_DETAIL),           # the first cat
            ("click", C["k_consist"], SFX_DETAIL),    # CONSISTENT
            ("whoosh", C["seam5"], SFX_STRUCTURE),    # the plate returns
            ("click", C["k_tuned"], SFX_DETAIL),      # FINE-TUNED
            ("pop", C["both"], SFX_DETAIL),           # dartboard + strip
            ("click", C["links"], SFX_DETAIL),        # the two lines
            ("whoosh", C["seam6"], SFX_STRUCTURE),    # the window closes round
            ("click", C["url"], SFX_DETAIL),          # fal.ai in the bar
            ("pop", C["help"], SFX_DETAIL),           # the two outputs
            ("click", C["k_anygen"], SFX_DETAIL),     # ANY GENERATION
            ("whoosh", C["outro"], SFX_STRUCTURE)]    # the rising sheet


def assert_sfx(sfx) -> dict:
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30:
        raise SystemExit(f"SFX flam: {worst}")
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "deliberately_silent": {
                "VIDEOS 8.62 / IMAGES 9.46": "0.06 s after their object's pop",
                "the pick 12.02": "a colour flip is not an arrival; THE MODEL "
                                  "clicks 0.10 s later",
                "cats 2 and 3": "one pop scores the three-cat cascade",
                "strip-2 20.12": "0.08 s after the dartboard-2 pop",
                "output lines 27.06": "0.26 s after the outputs' pop",
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
    # the rail binds readable INK: JetBrains Mono advances 0.600 em
    def ink(text, fs, ls):
        return len(text) * 0.6 * fs + (len(text) - 1) * ls
    rights = {}
    for n, (_h, _s, text) in LABEL_PLAN.items():
        b = canvas(RECTS[n])
        fs, ls = ((SC.KEY_TERM_FS, SC.KEY_TERM_LS) if n == "key-falagent"
                  else (SC.KEY_FS, SC.KEY_LS))
        rights[n] = (b[0] + b[2]) / 2 + ink(text, fs, ls) / 2
    type_right = max(rights.values())
    if type_right > CAP.LAW12_RAIL_X + 0.01:
        raise SystemExit(f"readable key ink reaches x={type_right:.1f}")
    boxes = [canvas(o["core"]) for o in SC.BESPOKE]
    boxes += [canvas(SC.WIN_BOX), canvas(SC.ROW_BOX), canvas(SC.FAL0_BOX)]
    ink_left = min(b[0] for b in boxes)
    ink_right = max(b[2] for b in boxes)
    if ink_left < 30 or W - ink_right < 30:
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

    m = CAP.PillMeasurer(RUN / "gen/_pillwidths_falagent.json")
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
    dst = RUN / "projects/falagent_split"
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
    (RUN / "gen/_build_falagent_split.json").write_text(
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
                      "phone": rep["phone_objects"]}, indent=1))


if __name__ == "__main__":
    main()
