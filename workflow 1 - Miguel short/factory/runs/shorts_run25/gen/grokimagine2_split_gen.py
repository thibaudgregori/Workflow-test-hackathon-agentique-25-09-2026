#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION - grokimagine2 / ICON CHOREOGRAPHY.

    YouTube   classic split 50/50   projects/grokimagine2_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/grokimagine2_scene.py` plus
`plans/grokimagine2_scene_handoff.md` are the design author's artefacts, sealed
by `review/artwork_pass_grokimagine2.json` (v4 seal, module + handoff hashes).
This file IMPORTS the module and SEATS it; it does not mutate a byte of the file
on disk.  Format-side contract stamps are made on the EMITTED string only.

TAKEOVER and FACESPLIT are not daily deliverables and this file cannot build one.

HD DELIVERY: authored AND encoded 1080x1920.  The face plate is
`face_bottom_hd.mp4` (1080x1058), so the seam is 1920 - 1057.5 = 862.5 and the
RENDERING pill top is 862.5 - 114.59/2 = 805.205.

THE TWO PLACEMENT DECISIONS THIS LANE OWNS
------------------------------------------
  k    = 0.95    NOT the handoff's 1.00, and that is LAW 30, not taste.  At k 1
                 the chapter-1 key VIDEOS (seat centre 885, ink ~835..934) puts
                 critical readable type past the 918 right rail between 30 % and
                 95 % of frame height.  At 0.95 about x 540 the key's ink ends at
                 540 + 394 x 0.95 = 914.3.  The composition stays centred and
                 symmetric (LAW 30 amendment); only readable type is railed.
  top  = 207.3   keeps the core's CONTENT BAND centred where the handoff seated
                 it (canvas 498): 498 - 306 x 0.95.
Logged in `plans/grokimagine2_split_notes.md`.

CONTRACT STAMPS (production v2), on the emitted string:
  * the four connectors get `data-anchor-side="top" data-anchor-fraction="0.5"
    data-check-at="12.40"` - the ends are SC.anchor_points(OUT_BOX, 1, "top").
  * the ONE emphasis (podium step 2's own outline flipping terracotta) is the
    `.pstep2` rect: it gets `id="emph-step2" data-emphasis="border"
    data-emphasis-target="podium" data-check-at="16.00" data-block="rank"`.
    A border flip adds no geometry; it is nested inside its target, so
    visual_laws excludes it from the target's own ink.
"""
from __future__ import annotations

import argparse
import html as ihtml
import json
import shutil
import subprocess
import sys
from pathlib import Path

F = Path(__file__).resolve().parents[3]           # the factory root
sys.path.insert(0, str(F / "pipeline"))
sys.path.insert(0, str(F / "pipeline/prep"))
sys.path.insert(0, str(F / "formats/cutout/lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import captions as CAP                          # noqa: E402
import cutout_core as CC                        # noqa: E402
import cutout_depthfield as DF                  # noqa: E402
import pointing_cues as PCUE                    # noqa: E402
import grokimagine2_scene as SC                 # noqa: E402

RUN = Path(__file__).resolve().parents[1]
CUT = RUN / "cuts/grokimagine2"
PLAN = RUN / "plans/grokimagine2_plan.json"
ASSETS = Path.home() / "Documents/Workspace/assets"
MUSIC = ASSETS / "audio/music/shorts-factory"
SFXLIB = ASSETS / "audio/sfx/shorts-factory"

VID = "grokimagine2"
W, H = 1080.0, 1920.0
FPS = 25
DUR = 32.32                                      # the cut master, prep's own

SEAM = 862.5
CORE_K = 0.95
BAND_CENTRE = SC.CANVAS_OFFSET + (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2   # 498.0
CORE_TOP_SPLIT = round(BAND_CENTRE - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2
                       * CORE_K, 2)                                    # 207.3
LEFT = round((W - SC.CORE_W * CORE_K) / 2, 2)                          # 27.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "Grok Imagine 2.0 makes mockups, infographics, images and videos"
LABEL_WINDOW = 1.0

STAGE_FILES = {k: f"logos/{v}" for k, v in SC.LOGO_FILES.items()}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}
CUTOUT_LANES = SC.CUTOUT_LOGO_LANES


# ------------------------------------------------------------------ geometry
def _rect(xywh) -> tuple:
    x, y, w, h = xywh
    return (x, y, x + w, y + h)


def _tile(xy) -> tuple:
    return (xy[0], xy[1], xy[0] + SC.TILE, xy[1] + SC.TILE)


# THE MOVING MARKS.  Three elements displace inside their lives (the palette at
# seam 1, the Grok tile at seam 3 and on "Magic", the picture on "Magic").
# Every judged box is a function of time; a transit window is not a held state.
TRANSIT = [(SC.CUE["seam1"], SC.CUE["seam1"] + 0.46),
           (SC.CUE["seam3"], SC.CUE["seam3"] + 0.46),
           (SC.CUE["wand_move"], SC.CUE["wand_move"] + 0.42)]


def rect_at(name: str, t: float) -> tuple:
    if name == "palette":
        return SC.PALETTE0_BOX if t < SC.CUE["seam1"] else SC.PALETTE1_BOX
    if name == "grok-tile":
        return _rect(SC.TILE_G0)
    if name == "grok-tile-2":
        if t < SC.CUE["seam3"]:
            return _rect(SC.TILE_P)
        if t < SC.CUE["wand_move"]:
            return _tile(SC.TILE_APP)
        return _tile(SC.TILE_APP_MOVED)
    if name == "picture":
        return SC.PICTURE_BOX if t < SC.CUE["wand_move"] else SC.PICTURE_BOX_MOVED
    if name == "selection":
        return _rect(SC.SEL)
    if name in SC.OUT_KEYS:
        return SC.OUT_BOX[name]
    if name.startswith("key-") and name[4:] in SC.OUT_KEYS:
        cx = SC.OUT_CX[SC.OUT_KEYS.index(name[4:])]
        return (cx - SC.OUT_KEY_SEAT / 2, SC.OUT_KEY_Y,
                cx + SC.OUT_KEY_SEAT / 2, SC.OUT_KEY_Y + SC.OUT_KEY_LH)
    fixed = {"key-grok-imagine": _rect(SC.KEY_TERM_BOX),
             "podium": SC.PODIUM_BOX,
             "key-best-video": _rect(SC.KEY_BEST_BOX),
             "wand": SC.WAND_BOX,
             "key-magic-wand": _rect(SC.KEY_WAND_BOX),
             "key-any-image": _rect(SC.KEY_IMAGE_BOX)}
    if name in fixed:
        return fixed[name]
    raise KeyError(name)


JUDGED = ["palette", "grok-tile", "key-grok-imagine", *SC.OUT_KEYS,
          *(f"key-{k}" for k in SC.OUT_KEYS), "podium", "key-best-video",
          "grok-tile-2", "picture", "wand", "key-magic-wand", "selection",
          "key-any-image"]
CONNECTORS = [f"conn-{k}" for k in SC.OUT_KEYS]


def canvas(box):
    return (CORE_K * box[0] + LEFT, CORE_TOP_SPLIT + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP_SPLIT + CORE_K * box[3])


def lifetime(name: str) -> tuple:
    return SC.LIFETIMES[name]


def alive(n: str, t: float) -> bool:
    t0, t1 = lifetime(n)
    return t0 <= t and (t1 is None or t < t1)


def in_transit(t: float) -> bool:
    return any(a <= t <= b + 0.02 for a, b in TRANSIT)


# --------------------------------------------------------------- label plan
LABEL_PLAN = {
    "key-grok-imagine": ("palette", "below", SC.KEY_TERM),
    "key-phone": ("phone", "below", "MOCKUPS"),
    "key-poster": ("poster", "below", "INFOGRAPHICS"),
    "key-polaroid": ("polaroid", "below", "IMAGES"),
    "key-clapper": ("clapper", "below", "VIDEOS"),
    "key-best-video": ("podium", "below", SC.KEY_BEST),
    "key-magic-wand": ("wand", "below", "MAGIC WAND"),
    "key-any-image": ("picture", "below", "ANY IMAGE"),
}
LABEL_AT = {k: lifetime(k)[0] for k in LABEL_PLAN}
HOST_AT = {h: lifetime(h)[0] for h, _s, _t in LABEL_PLAN.values()}
PRINTED_KEYS = {k: v[2] for k, v in LABEL_PLAN.items()}
PRINTED_LIFETIME = {k: lifetime(k) for k in PRINTED_KEYS}

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.
CUE_WORDS = {
    "keyterm": (3, "just", "start"),
    "tile": (9, "grok", "start"),
    "seam1": (15, "now,", "start"),
    "c_mock": (22, "ux/ui", "start"),
    "c_info": (24, "infographics,", "start"),
    "c_img": (25, "images,", "start"),
    "c_vid": (26, "videos,", "start"),
    "seam2": (32, "it's", "start"),
    "tile2": (37, "two", "start"),
    "seam3": (48, "if", "start"),
    "picture": (56, "application,", "start"),
    "wand_move": (62, "magic", "start"),
    "select": (68, "select", "start"),
    "replace": (80, "replace", "start"),
    "outro": (83, "now", "start"),
}
CUE_INSIDE = {
    "palette": (0, "grok"),
    "o_mock": (22, "ux/ui"), "k_mock": (23, "mockups,"),
    "o_info": (24, "infographics,"), "k_info": (24, "infographics,"),
    "o_img": (25, "images,"), "k_img": (25, "images,"),
    "o_vid": (26, "videos,"), "k_vid": (26, "videos,"),
    "emph": (37, "two"), "emphout": (46, "right"),
    "k_best": (43, "model"),
    "wand": (62, "magic"), "k_wand": (63, "wand,"),
    "k_image": (74, "image"),
}

# ------------------------------------------------ connector / emphasis contracts
CONN_CHECK_AT = 12.40          # all four drawn (11.40) and held until 13.00
EMPH_ID = "emph-step2"
EMPH_KIND = "border"
EMPH_TARGET = "podium"
EMPH_CHECK_AT = 16.00          # flipped by 14.90, released at 17.40


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
    head = " ".join(w["text"] for w in ws[:5]).lower()
    if not head.startswith("grok imagine 2.0 just released"):
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[5:]).lower()
    if "imagine 2.0 just released" in later:
        raise SystemExit("LAW 46: the opening repeats inside the take")
    tail = DUR - float(ws[-1]["end"])
    cap = 0.20 + 1.0 / FPS
    if tail > 0.30:
        raise SystemExit(f"LAW 47: the master runs {tail:.3f}s past the last word")
    edl = json.loads((CUT / "edl.json").read_text())
    td = edl["take_detection"]
    marker = td["cross_check_marker_rule"]
    gap = td["cross_check_transcript_gap_rule"]
    if marker["verdict"] not in ("equality", "bound"):
        raise SystemExit(f"marker cross-check is {marker['verdict']!r}")
    if marker["verdict"] == "bound" and marker["answer"] > td["take_word_index"]:
        raise SystemExit("the marker BOUND answers past the keeper take")
    if not td["corroboration"]["witnessed"]:
        raise SystemExit("the keeper take is uncorroborated")
    rep = {"law47_tail_s": round(tail, 3), "law47_cap_s": round(cap, 3),
           "law47_verdict": ("PASS" if tail <= cap else "REPORTED")
           + f" - {tail:.3f}s past the last word against a {cap:.3f}s cap",
           "take_corroboration": {
               "method": td["method"], "raw_word_index": td["take_word_index"],
               "raw_start_s": td["take_start_s"], "words": td["take_words"],
               "of_raw_words": td["raw_words"],
               "sign_offs_found": td["sign_offs_found"],
               "marker_rule": marker["verdict"],
               "marker_answer": marker["answer"],
               "markers_before_take": marker["markers_before_take"],
               "gap_rule": gap["verdict"],
               "gap_correct_thresholds": gap["correct_thresholds"],
               "corroboration": td["corroboration"]},
           "words": len(ws)}
    return list(ws), rep


def assert_cues(ws: list[dict]) -> dict:
    rep: dict = {}
    for name, (idx, text, edge) in CUE_WORDS.items():
        w = ws[idx]
        if w["text"].strip().lower() != text:
            raise SystemExit(f"cue {name}: word {idx} is {w['text']!r}, not {text!r}")
        got = round(float(w[edge]), 3)
        if abs(got - SC.CUE[name]) > 0.011:
            raise SystemExit(f"cue {name}: scene {SC.CUE[name]}, word {got}")
        rep[name] = {"word": idx, "text": w["text"], "t": SC.CUE[name]}
    for name, (idx, text) in CUE_INSIDE.items():
        w = ws[idx]
        if w["text"].strip().lower() != text:
            raise SystemExit(f"cue {name}: word {idx} is {w['text']!r}, not {text!r}")
        t = SC.CUE[name]
        lo, hi = float(w["start"]), float(w["end"]) + LABEL_WINDOW
        if not (lo <= t <= hi):
            raise SystemExit(f"cue {name} at {t} outside {w['text']!r} "
                             f"({lo:.3f}-{hi:.3f})")
        rep[name] = {"word": idx, "text": w["text"], "t": t,
                     "window": [round(lo, 3), round(hi, 3)]}
    missing = set(SC.CUE) - set(rep)
    if missing:
        raise SystemExit(f"cues the build never verified: {sorted(missing)}")

    # LAW 43 / LAW 45: every erase hands over.
    FADE = 0.22
    seams = []
    handover = {5.80: "palette (travels across the seam)",
                13.00: "podium (pops inside the erase)",
                17.86: "grok-tile-2 (travels across the seam)",
                28.24: "o-sheet (the opaque sheet IS the handover)"}
    for ch in SC.BOARD_CHAPTERS:
        t = ch["erase_at"]
        if t is None:
            continue
        end_word = max(float(w["end"]) for w in ws if float(w["end"]) <= t)
        if t < end_word - 1e-9:
            raise SystemExit(f"LAW 45: the seam at {t} cuts a spoken word")
        carried = [n for n in SC.LIFETIMES
                   if lifetime(n)[0] < t and (lifetime(n)[1] or DUR) > t + FADE]
        born = sorted(n for n in SC.LIFETIMES
                      if t <= lifetime(n)[0] <= t + FADE + 0.30)
        if not carried and not born:
            raise SystemExit(f"LAW 45: the seam at {t} hands over to nothing")
        seams.append({"erase_at": t, "last_word_ends": round(end_word, 3),
                      "carried_across": carried, "born_in_erase": born,
                      "handover": handover.get(round(t, 2))})
    last_board = max(lifetime(n)[0] for n in SC.LIFETIMES
                     if not n.startswith("o-")) + 0.30
    if last_board >= SC.CUE["outro"]:
        raise SystemExit("board ink still arriving at the outro anchor")
    rep["_law45"] = {"seams": seams,
                     "last_board_arrival_completes": round(last_board, 2),
                     "outro_at": SC.CUE["outro"]}
    return rep


def assert_word_sync(ws: list[dict]) -> dict:
    """Every typed key's FIRST visible state agrees with the word it lands on,
    and every word of it has been spoken (LAW 24)."""
    pairs = {"key-grok-imagine": (2, "2.0"), "key-phone": (23, "mockups,"),
             "key-poster": (24, "infographics,"), "key-polaroid": (25, "images,"),
             "key-clapper": (26, "videos,"), "key-best-video": (43, "model"),
             "key-magic-wand": (63, "wand,"), "key-any-image": (74, "image")}
    rows = []
    for key, (idx, text) in pairs.items():
        w = ws[idx]
        if w["text"].strip().lower() != text:
            raise SystemExit(f"word-sync: {key} expects {text!r} at {idx}")
        t = LABEL_AT[key]
        lo, hi = float(w["start"]), float(w["end"]) + LABEL_WINDOW
        if not (lo - 1e-3 <= t <= hi) and key != "key-grok-imagine":
            raise SystemExit(f"word-sync: {key} at {t} outside {text!r}")
        if key == "key-grok-imagine" and t < float(w["end"]):
            raise SystemExit("LAW 24: GROK IMAGINE 2.0 lands before '2.0' ends")
        rows.append({"state": key, "text": PRINTED_KEYS[key], "at": t,
                     "last_word_of_key": w["text"],
                     "word_window": [round(lo, 3), round(hi, 3)]})
    return {"states_checked": len(rows), "disagreements": 0, "states": rows,
            "digits_that_tick": 0,
            "note": "no counter ticks; the podium digits 1/2/3 are the shape's "
                    "own content and arrive with it at 13.00 on \"It's\", "
                    "before 'number two' (14.00) - they are a ranking object, "
                    "not a spoken value, and the tile lands on 2 on 'two'."}


def assert_law37(ws: list[dict]) -> dict:
    cues = PCUE.scan(ws)
    plan = json.loads(PLAN.read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / "prep/stages/grokimagine2.cues.json").read_text())
    if marker["keys"]["cue_count"] != len(cues):
        raise SystemExit("LAW 37: the prep marker disagrees with the re-run")
    if cues or declared:
        raise SystemExit("LAW 37: this take was planned with no cue")
    return {"scan_cue_count": 0, "plan_declared_cards": 0,
            "prep_marker_cue_count": 0, "source_post_cards": 0}


# ------------------------------------------------------------------ geometry
GUTTER_REFUSE = 16.0
GUTTER_AIM = 24.0


def assert_anchor_law() -> dict:
    """LAW 40 - each end re-derived from the TARGET's own built rect."""
    base = SC.assert_anchor_law()
    out = {}
    for k in SC.OUT_KEYS:
        x0, y0, x1, y1 = SC.OUT_BOX[k]
        end = SC.A_OUT[k]
        frac = (end[0] - x0) / (x1 - x0)
        if abs(end[1] - y0) > 0.01 or abs(frac - 0.5) > 1e-6:
            raise SystemExit(f"conn-{k}: end {end} is not the top-centre of {k}")
        c0, c1 = lifetime(f"conn-{k}")
        t0, t1 = lifetime(k)
        drawn = lifetime(f"conn-{k}")[0] + 0.30
        if not (drawn <= CONN_CHECK_AT < min(c1, t1)):
            raise SystemExit(f"conn-{k}: check-at is not a held instant")
        if not SC.conn_d(k).endswith(f"L{end[0]:.0f} {end[1]:.0f}"):
            raise SystemExit(f"conn-{k}: the path does not end on its anchor")
        out[f"conn-{k}"] = {"target": k, "side": "top", "fraction": 0.5,
                            "check_at": CONN_CHECK_AT,
                            "end_core": list(end),
                            "end_canvas": [round(v, 2) for v in
                                           canvas((*end, *end))[:2]],
                            "stroke_completes": round(drawn, 2)}
    return {"connectors": out, "arrowheads": 0, **{"module": base}}


def assert_emphasis_law() -> dict:
    t0, t1 = lifetime(EMPH_ID)
    if not (SC.CUE["emph"] + 0.34 <= EMPH_CHECK_AT < t1):
        raise SystemExit("LAW 38: the emphasis check instant is not held")
    return {"emphasis": {"id": EMPH_ID, "kind": EMPH_KIND, "target": EMPH_TARGET,
                         "fires": SC.CUE["emph"], "releases": SC.CUE["emphout"],
                         "check_at": EMPH_CHECK_AT, "ink": SC.TERRA_L,
                         "rest_ink": SC.INK},
            "rings_ellipses_circles": 0, "highlights": 0,
            "why": "rule 2: podium step 2 is DRAWN, so it takes boxing, and the "
                   "DOM lane's boxing is the step's OWN outline flipping to "
                   "terracotta. No raster text exists, so no highlight."}


def assert_label_law() -> dict:
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    out: dict = {}
    for key, (host, side, text) in LABEL_PLAN.items():
        t = LABEL_AT[key] + 0.5
        kb, hb = rect_at(key, t), rect_at(host, t)
        if side == "below" and kb[1] < hb[3] - 0.01:
            raise SystemExit(f"LAW 39: {key} is not entirely below {host}")
        kc, hc = (kb[0] + kb[2]) / 2, (hb[0] + hb[2]) / 2
        if abs(kc - hc) > 0.15 * (hb[2] - hb[0]):
            raise SystemExit(f"LAW 39: {key} is off {host}'s axis")
        if not any(key in b and host in b for b in blocks):
            raise SystemExit(f"LAW 41: {key} is not blocked with {host}")
        if LABEL_AT[key] < HOST_AT[host] - 1e-9:
            raise SystemExit(f"LAW 39: {key} lands before {host}")
        out[key] = {"host": host, "side": side, "text": text,
                    "centre_error_px": round(kc - hc, 3),
                    "gap_px": round(kb[1] - hb[3], 2), "at": LABEL_AT[key],
                    "key_box_canvas": [round(v, 1) for v in canvas(kb)]}
    first = min(LABEL_AT.values())
    if abs(first - SC.CUE["keyterm"]) > 1e-9:
        raise SystemExit("LAW 9: the key term is not the first type on screen")
    du = SC.KEY_TERM_FS * CORE_K / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} design units")
    out["_key_term"] = {"text": SC.KEY_TERM, "at": first,
                        "rendered_px": round(SC.KEY_TERM_FS * CORE_K, 2),
                        "design_units": round(du, 2),
                        "alone_until": sorted(LABEL_AT.values())[1]}
    out["_law50"] = {"siblings": [["key-phone", "key-poster", "key-polaroid",
                                   "key-clapper"],
                                  ["key-magic-wand", "key-any-image"]],
                     "note": "one size, one seat, one baseline per sibling set "
                             "(module constants OUT_KEY_* and SIB_KEY_*)."}
    return out


def assert_lifetime_law() -> dict:
    seams = {c["erase_at"] for c in SC.BOARD_CHAPTERS if c["erase_at"]}
    windowed = {"sun": "replaced on 'replace'",
                "emph-step2": "an emphasis lives only inside its beat"}
    for n, (t0, t1) in SC.LIFETIMES.items():
        if n.startswith("o-"):
            if t1 is not None:
                raise SystemExit(f"LAW 42: {n} is an outro anchor but dies")
            continue
        if t1 is None:
            raise SystemExit(f"LAW 42: {n} never leaves the board")
        if t1 not in seams and n not in windowed:
            raise SystemExit(f"LAW 42: {n} leaves at {t1}, not at a seam")
    shares = {n: round(((t1 or DUR) - t0) / DUR, 3)
              for n, (t0, t1) in SC.LIFETIMES.items() if not n.startswith("o-")}
    worst = max((v, k) for k, v in shares.items())
    return {"board_mode": SC.BOARD_MODE, "chapters": len(SC.BOARD_CHAPTERS),
            "anchors": list(SC.SCENE_ANCHORS), "windowed": windowed,
            "longest_lived_mark": {"mark": worst[1], "share": worst[0]},
            "note": "palette (39.8 %) and grok-tile-2 (42.9 %) carry finite t_to "
                    "at chapter seams - the plan's own declaration."}


def assert_spacing_law() -> dict:
    blocks = [set(b) for b in SC.DECLARED_BLOCKS]
    pairs, judged, worst, under = 0, 0, (1e9, None), []
    t = 0.0
    while t < SC.CUE["outro"]:
        if not in_transit(t):
            live = [n for n in JUDGED if alive(n, t)]
            for i in range(len(live)):
                for j in range(i + 1, len(live)):
                    a, b = live[i], live[j]
                    pairs += 1
                    if any({a, b} <= s for s in blocks):
                        continue
                    ax0, ay0, ax1, ay1 = rect_at(a, t)
                    bx0, by0, bx1, by1 = rect_at(b, t)
                    dx = max(bx0 - ax1, ax0 - bx1, 0.0)
                    dy = max(by0 - ay1, ay0 - by1, 0.0)
                    if dx <= 0.0 and dy <= 0.0:
                        raise SystemExit(f"LAW 41: {a} and {b} overlap at {t}")
                    g = (dx * dx + dy * dy) ** 0.5 * CORE_K
                    judged += 1
                    if g < worst[0]:
                        worst = (g, (a, b, round(t, 2)))
                    if g < GUTTER_AIM:
                        under.append([a, b, round(t, 2), round(g, 2)])
        t = round(t + 0.1, 2)
    if worst[0] < GUTTER_REFUSE:
        raise SystemExit(f"LAW 41: {worst[1]} is {worst[0]:.2f}px")
    return {"pairs_measured": pairs, "judged": judged,
            "tightest_page_px": round(worst[0], 2),
            "tightest_pair": list(worst[1]), "under_aim": under[:12],
            "under_aim_count": len(under),
            "blocks": [list(b) for b in SC.DECLARED_BLOCKS],
            "instrument": "0.1 s co-alive sweep over time-dependent rects, "
                          "transit windows skipped; geometry_audit --strict is "
                          "the independent DOM measurement"}


def assert_cast_law() -> dict:
    rep = DF.assert_cast_resolves(list(STAGE_FILES), STAGE_FILES, ASSETS,
                                  label="grokimagine2 stage marks")
    plan = json.loads(PLAN.read_text())
    if list(plan["cast"]) != list(STAGE_FILES):
        raise SystemExit(f"the plan's cast {plan['cast']} is not the scene's")
    if "grok" not in CC.MARK_INK:
        raise SystemExit("the stage mark was never measured")
    return {"stage_marks": list(STAGE_FILES), "resolve": rep,
            "ink_side_core_px": SC.MARK_SIDE, "tile_px": SC.TILE,
            "cutout_lanes_not_ours": list(CUTOUT_LANES)}


def assert_axis_law() -> dict:
    rows = []
    for i, (t0, t1) in enumerate(zip(SC.BEAT_EDGES, SC.BEAT_EDGES[1:])):
        t = t1 - 0.01
        while t > t0 and (in_transit(t) or not any(alive(n, t) for n in JUDGED)):
            t = round(t - 0.05, 2)
        boxes = [canvas(rect_at(n, t)) for n in JUDGED if alive(n, t)]
        if not boxes:
            rows.append({"beat": i, "empty": "outro beat"})
            continue
        left = min(b[0] for b in boxes)
        right = max(b[2] for b in boxes)
        if left < 40.0 or W - right < 40.0:
            raise SystemExit(f"beat {i} ink {left}..{right} inside the margin")
        rows.append({"beat": i, "at": t, "ink": [round(left, 1), round(right, 1)],
                     "offset_from_540": round((left + right) / 2 - 540, 2)})
    return {"beats": rows}


def assert_sfx(sfx) -> dict:
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30 - 1e-6:
        raise SystemExit(f"SFX flam: {worst}")
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "deliberately_silent": {
                "keys 2-4 of the fan / MAGIC WAND": "each lands 0.14-0.30 s "
                "after its own object's pop; one sound per gesture",
                "moves (5.80, 17.86, 21.00)": "a travel is not an arrival",
                "emph 14.56": "an outline flip adds nothing",
                "outro lockup": "rides the sheet's whoosh"}}


# ------------------------------------------------------------------ captions
def phrases(ws):
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


def _is_board_key(text: str):
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
    log, i = [], 0
    while i < len(parts):
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


def merge_board_key_beats(parts, max_w, measurer, forbidden):
    """LAW 4: a pill never repeats a board key while that key is on screen."""
    log, i = [], 0
    while i < len(parts):
        key = _is_board_key(_joined(parts[i]))
        if key is None:
            i += 1
            continue
        k0, k1 = PRINTED_LIFETIME[key]
        t0 = float(parts[i][0]["start"])
        t1 = float(parts[i + 1][0]["start"]) if i + 1 < len(parts) \
            else float(parts[i][-1]["end"])
        if not (t0 < (k1 or DUR) and k0 < t1):
            i += 1
            continue
        done = False
        for lo, hi in ((i - 1, i + 1), (i, i + 2)):
            if lo < 0 or hi > len(parts):
                continue
            u = [w for p in parts[lo:hi] for w in p]
            measurer.want([_joined(u)])
            measurer.resolve()
            if measurer.width(_joined(u)) <= max_w:
                log.append({"pill": _joined(parts[i]), "key": key,
                            "merged_to": _joined(u)})
                parts[lo:hi] = [u]
                i = lo
                done = True
                break
        if not done:
            # re-partition a window around it with the keys forbidden
            for lo, hi in ((i - 1, i + 2), (i - 1, i + 1), (i, i + 2)):
                lo, hi = max(0, lo), min(len(parts), hi)
                if hi - lo < 2:
                    continue
                got = _repartition([w for p in parts[lo:hi] for w in p],
                                   max_w, measurer, forbidden)
                if got is None:
                    continue
                log.append({"pill": _joined(parts[i]), "key": key,
                            "repartitioned_to": [_joined(p) for p in got]})
                parts[lo:hi] = got
                i = lo
                done = True
                break
        if not done:
            raise SystemExit(f"LAW 4: pill repeats live board key {key}")
    return parts, log


def merge_solo_word_beats(parts, max_w, measurer):
    log, i = [], 0
    while i < len(parts):
        if len(parts[i]) != 1:
            i += 1
            continue
        best = None
        for lo, hi in ((i - 1, i + 1), (i, i + 2)):
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
            best = (lo, hi, u)
            break
        if best is None:
            i += 1
            continue
        lo, hi, u = best
        log.append({"solo": _joined(parts[i]), "merged_to": _joined(u)})
        parts[lo:hi] = [u]
        i = max(0, lo)
    return parts, log


def caption_beats(measurer, ws, clean_rep):
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
    parts, key_log = merge_board_key_beats(parts, CAP.SEAT_MAX_W, measurer,
                                           forbidden)
    parts, solo_log = merge_solo_word_beats(parts, CAP.SEAT_MAX_W, measurer)
    beats = []
    for part in parts:
        text = _joined(part)
        beats.append({"text": text, "start": float(part[0]["start"]),
                      "end": float(part[-1]["end"]), "w": measurer.width(text)})
    for i, b in enumerate(beats):
        nxt = beats[i + 1]["start"] if i + 1 < len(beats) else b["end"] + 0.26
        b["dur"] = round(max(0.24, min(nxt, DUR) - b["start"]), 3)
    CAP.assert_no_function_only_beat(beats)
    if max(b["w"] for b in beats) > CAP.SEAT_MAX_W + 0.6:
        raise SystemExit("a pill exceeds the seat")
    for b in beats:
        key = _is_board_key(b["text"])
        if key:
            k0, k1 = PRINTED_LIFETIME[key]
            if b["start"] < (k1 or DUR) and k0 < b["start"] + b["dur"]:
                raise SystemExit(f"caption echo: {b['text']!r} vs {key}")
    clean_rep.update({"function_word_merges": merged,
                      "beats_before_merge": before,
                      "orphan_repartitions": orphan_log,
                      "board_key_echo_repairs": key_log,
                      "solo_word_merges": solo_log})
    return beats, clean_rep


def caption_html(beats, seat_y) -> str:
    ks = [round(b["start"] * FPS) for b in beats]
    last_k = round(min(beats[-1]["start"] + beats[-1]["dur"], DUR) * FPS)
    out = []
    for i, b in enumerate(beats):
        k0 = ks[i]
        k1 = ks[i + 1] if i + 1 < len(beats) else last_k
        if k1 <= k0 + 1:
            raise SystemExit(f"caption beat {i} ({b['text']!r}) under two frames")
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
const SOFT = "power2.out";
const SWING = "power2.inOut";
const POP = "back.out(2.05)";
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


def stage(dst: Path) -> dict:
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
    shutil.copy2(MUSIC / "bed_split_v2.mp3", dst / "assets/music/bed.mp3")
    for s in ("whoosh", "pop", "click"):
        shutil.copy2(SFXLIB / f"{s}.mp3", dst / f"assets/sfx/{s}.mp3")
    shutil.copy2(CUT / "face_bottom_hd.mp4", v / "face_bottom_hd.mp4")
    rec["face"] = {"file": "face_bottom_hd.mp4",
                   **probe_wh(CUT / "face_bottom_hd.mp4")}
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
    return {"_grok_img": CC.mark_img(LOGO_URL["grok"], "grok",
                                     SC.MARK_SIDE["grok"])}


def sfx_plan() -> list[tuple]:
    C = SC.CUE
    return [("pop", C["palette"], SFX_STRUCTURE),      # the palette
            ("click", C["keyterm"], SFX_DETAIL),       # GROK IMAGINE 2.0
            ("pop", C["tile"], SFX_STRUCTURE),         # the Grok tile
            ("pop", C["o_mock"], SFX_STRUCTURE),       # the phone
            ("click", C["k_mock"], SFX_DETAIL),        # MOCKUPS
            ("pop", C["o_info"], SFX_STRUCTURE),       # the poster
            ("pop", C["o_img"], SFX_STRUCTURE),        # the instant photo
            ("pop", C["o_vid"], SFX_STRUCTURE),        # the clapperboard
            ("pop", C["seam2"], SFX_STRUCTURE),        # the podium
            ("pop", C["tile2"], SFX_STRUCTURE),        # the tile on step 2
            ("click", C["k_best"], SFX_DETAIL),        # BEST VIDEO MODEL
            ("pop", C["picture"], SFX_STRUCTURE),      # the framed picture
            ("pop", C["wand"], SFX_STRUCTURE),         # the wand
            ("click", C["select"], SFX_DETAIL),        # the selection snaps
            ("click", C["k_image"], SFX_DETAIL),       # ANY IMAGE
            ("pop", C["replace"], SFX_STRUCTURE),      # sparkle: sun -> moon
            ("whoosh", C["outro"], SFX_STRUCTURE)]     # the rising sheet


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
def guard_core_band(top: float, k: float, cap_seat: float) -> dict:
    y0 = top + SC.CONTENT_Y0 * k
    y1 = top + SC.CONTENT_Y1 * k
    pill_top = cap_seat - CAP.CAP_PILL_HEIGHT / 2
    if y0 < 0.10 * H:
        raise SystemExit(f"core content starts at {y0:.1f}, inside the top 10%")
    if y1 > pill_top - 24.0:
        raise SystemExit(f"core content ends at {y1:.1f}, too near the pill")
    return {"content_top": round(y0, 2), "content_bottom": round(y1, 2),
            "pill_top_rendered": round(pill_top, 3),
            "clear_above_pill": round(pill_top - y1, 2),
            "clear_below_law30": round(y0 - 0.10 * H, 2)}


def guard_rail() -> dict:
    """LAW 30: readable type never past x 918.  Measured on the key INK: a
    JetBrains Mono glyph advances 0.600 em plus the letter-spacing."""
    worst = None
    for key, (_h, _s, text) in LABEL_PLAN.items():
        t = LABEL_AT[key] + 0.5
        x0, _y0, x1, _y1 = rect_at(key, t)
        fs = {"key-grok-imagine": SC.KEY_TERM_FS}.get(key)
        ls = SC.KEY_TERM_LS if fs else (SC.OUT_KEY_LS if key[4:] in SC.OUT_KEYS
                                         else SC.KEY_LS)
        fs = fs or (SC.OUT_KEY_FS if key[4:] in SC.OUT_KEYS else SC.KEY_FS)
        ink = len(text) * 0.6 * fs + (len(text) - 1) * ls
        cx = (x0 + x1) / 2
        right = LEFT + CORE_K * (cx + ink / 2 + ls / 2)
        if worst is None or right > worst[0]:
            worst = (right, key)
    if worst[0] > CAP.LAW12_RAIL_X:
        raise SystemExit(f"LAW 30: {worst[1]} ink reaches x={worst[0]:.1f}")
    return {"readable_type_right_x": round(worst[0], 1), "key": worst[1],
            "rail_x": CAP.LAW12_RAIL_X}


def phone_objects() -> list[dict]:
    out = []
    for o in SC.BESPOKE:
        box = o["core"]
        if o["name"] == "a framed picture":
            box = rect_at("picture", o["t"])
        x0, y0, x1, y1 = canvas(box)
        out.append({"name": o["name"], "t": o["t"],
                    "bbox": [round(x0 / W, 5), round(y0 / H, 5),
                             round(x1 / W, 5), round(y1 / H, 5)],
                    "canvas": [round(x0, 1), round(y0, 1), round(x1, 1),
                               round(y1, 1)]})
    return out


# ---------------------------------------------- the format-side contract stamps
def declare_contracts(html: str, anchors: dict) -> tuple[str, dict]:
    stamped = html
    for cid, a in anchors["connectors"].items():
        key = f'id="{cid}"'
        if stamped.count(key) != 1:
            raise SystemExit(f"cannot stamp {cid}")
        stamped = stamped.replace(
            key, f'{key} data-anchor-side="{a["side"]}" '
                 f'data-anchor-fraction="{a["fraction"]:g}" '
                 f'data-check-at="{a["check_at"]:.2f}"', 1)
    old = '<rect class="pdk pstep2"'
    if stamped.count(old) != 1:
        raise SystemExit("the module no longer emits the step-2 rect once")
    stamped = stamped.replace(
        old, f'<rect id="{EMPH_ID}" class="pdk pstep2" '
             f'data-emphasis="{EMPH_KIND}" data-emphasis-target="{EMPH_TARGET}" '
             f'data-check-at="{EMPH_CHECK_AT:.2f}" data-block="rank"', 1)
    return stamped, {"connectors_stamped": len(anchors["connectors"]),
                     "emphases_stamped": 1}


def build_split(out: Path, handle: str) -> dict:
    staged = stage(out)
    if (staged["face"]["w"], staged["face"]["h"]) != (1080, 1058):
        raise SystemExit(f"the face plate is {staged['face']}")
    ws, clean_rep = clean_tokens(words())
    rep = {"spacing": assert_spacing_law(), "anchors": assert_anchor_law(),
           "lifetimes": assert_lifetime_law(),
           "emphasis": assert_emphasis_law(), "labels": assert_label_law(),
           "cast": assert_cast_law(), "axis": assert_axis_law(),
           "cues": assert_cues(ws), "word_sync": assert_word_sync(ws),
           "law37": assert_law37(ws)}
    SFX = sfx_plan()
    rep["sfx"] = assert_sfx(SFX)

    scene_html, tweens = SC.build(media(), outro_lockup(handle))
    scene_html, declared = declare_contracts(scene_html, rep["anchors"])
    if scene_html.count("data-connect-to") != 4:
        raise SystemExit("the scene does not carry four connectors")
    if scene_html.count("data-label-for") != 8:
        raise SystemExit("the scene does not carry eight labelled keys")
    if (scene_html.count("data-connect-to") + scene_html.count("data-emphasis=")
            != scene_html.count("data-check-at")):
        raise SystemExit("a connector or emphasis is missing its check instant")
    for shape in ("<circle", "<ellipse"):
        if shape in scene_html:
            raise SystemExit(f"LAW 38 rule 3: {shape} in the scene")

    m = CAP.PillMeasurer(RUN / "gen/_pillwidths_grokimagine2.json")
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
        f'<div class="abs core" id="core" style="left:{LEFT}px;'
        f'top:{CORE_TOP_SPLIT}px;width:{SC.CORE_W}px;height:{SC.CORE_H}px;'
        f'transform:scale({CORE_K})">',
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
                "declared": declared, "phone_objects": objs,
                "transcript": cap_rep,
                "captions": {"n": len(beats),
                             "widest_px": round(max(b["w"] for b in beats), 1),
                             "texts": [b["text"] for b in beats]}})
    return rep


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="split", choices=("split",))
    ap.parse_args()
    dst = RUN / "projects/grokimagine2_split"
    dst.mkdir(parents=True, exist_ok=True)
    rep = build_split(dst, "yt")
    rep["handle"] = CAP.handle("yt")
    (RUN / "gen/_build_grokimagine2_split.json").write_text(
        json.dumps({"video": VID, "lane": "icon choreography", "fps": FPS,
                    "duration": DUR, "formats": {"split": rep}}, indent=1))
    print(f"split: {dst}")
    print(json.dumps({"captions": rep["captions"], "band": rep["band"],
                      "rail": rep["rail"],
                      "tightest": [rep["spacing"]["tightest_page_px"],
                                   rep["spacing"]["tightest_pair"]],
                      "sfx": rep["sfx"]["tightest_gap_s"],
                      "phone_objects": rep["phone_objects"]}, indent=1))


if __name__ == "__main__":
    main()
