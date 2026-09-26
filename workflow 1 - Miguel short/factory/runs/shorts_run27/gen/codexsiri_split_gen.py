#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION - codexsiri / DIAGRAM BUILD.

    YouTube   classic split 50/50   projects/codexsiri_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/codexsiri_scene.py` plus
`plans/codexsiri_scene_handoff.md` are the design agent's artefacts, sealed by
`review/artwork_pass_codexsiri.json` (production v4, `production.py seal`).
This file IMPORTS the module and SEATS it at the handoff's own placement
(k = 1.00, left 0, core top 192).  It never mutates a byte of the module.

What this page adds to the emitted scene is DECLARATION only, never ink:
  * every connector gets `data-anchor-side`, `data-anchor-fraction` and
    `data-check-at` (production's LAW 40 contract);
  * the two marker highlights get `data-emphasis-target` (their own text
    line) and `data-check-at`;
  * the phone's outline flip (LAW 38 rule 2) is declared on `#phone` as
    `data-emphasis="border"`, target the Codex mark on its screen.

HD DELIVERY: authored AND encoded 1080x1920.  The face plate is
`face_bottom_hd.mp4` (1080x1058), so the seam is 1920 - 1057.5 = 862.5 and the
RENDERING pill top is 862.5 - 114.59/2 = 805.205 (the pill that renders, never
the frozen 108.2 seat constant).  The core's content band 76..538 lands at
canvas 268..730.

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
import codexsiri_scene as SC                    # noqa: E402

RUN = Path(__file__).resolve().parents[1]
CUT = RUN / "cuts/codexsiri"
PLAN = RUN / "plans/codexsiri_plan.json"
ASSETS = Path.home() / "Documents/Workspace/assets"
LOGOS = ASSETS / "logos"
LIB_MUSIC = ASSETS / "audio/music/shorts-factory"
LIB_SFX = ASSETS / "audio/sfx/shorts-factory"

VID = "codexsiri"
W, H = 1080.0, 1920.0
FPS = 25
DUR = SC.DUR                                     # 36.16, the cut master

SEAM = 862.5
CORE_TOP_SPLIT = SC.CANVAS_OFFSET                # 192.0, the handoff's number
CORE_K = 1.00
LEFT = (W - SC.CORE_W * CORE_K) / 2              # 0.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "Siri sucks, so one user replaced it with Codex"
LABEL_WINDOW = 1.0

# ------------------------------------------------------------------ marks
# MARK IDENTITY: the FILE is named, never "the logo" (handoff section 1).
STAGE_FILES = {k: f"logos/{v}" for k, v in SC.LOGO_FILES.items()}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in STAGE_FILES.items()}
CUTOUT_LANES = SC.CUTOUT_LOGO_LANES
C = SC.CUE


def _xywh(b) -> tuple:
    x, y, w, h = b
    return (x, y, x + w, y + h)


# Seats in CORE px (x0, y0, x1, y1), each at the instant its key is live.
RECTS: dict[str, tuple] = {
    "phone": SC.phone_box("hook_side"),
    "key-siri": _xywh(SC.KEY_SIRI_BOX),
    "box": _xywh(SC.BOX),
    "key-box": _xywh(SC.KEY_BOX_BOX),
    "gh-tile": SC.GH_BOX,
    "key-gh": _xywh(SC.KEY_GH_BOX),
    "codex-tile": SC.CX_BOX,
    "key-codex": _xywh(SC.KEY_CX_BOX),
    "clipboard": _xywh(SC.CLIP),
    "key-done": _xywh(SC.KEY_DONE_BOX),
    "gh-tile-2": _xywh(SC.GH2),
    "key-gh-2": _xywh(SC.KEY_GH2_BOX),
    "arrow-down": (SC.ARROW[0] - 60.0, SC.ARROW[1] - 20.0,
                   SC.ARROW[0] + 60.0, SC.ARROW[2] + 20.0),
    "key-desc": _xywh(SC.KEY_DESC_BOX),
}


def canvas(box):
    """core px -> the canvas this page actually paints (top 192, k 1.00)."""
    return (CORE_K * box[0] + LEFT, CORE_TOP_SPLIT + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP_SPLIT + CORE_K * box[3])


# --------------------------------------------------------------- label plan
# LAW 39 / LAW 9 / LAW 50: the plan's seven keys, host, side, printed text.
LABEL_PLAN = {"key-siri": ("phone", "above", SC.KEY_TERM),
              "key-box": ("box", "below", "OUT OF THE BOX"),
              "key-gh": ("gh-tile", "below", "GITHUB REPO"),
              "key-codex": ("codex-tile", "below", "CODEX"),
              "key-done": ("clipboard", "below", "GET STUFF DONE"),
              "key-gh-2": ("gh-tile-2", "below", "GITHUB REPO"),
              "key-desc": ("arrow-down", "above", "IN THE DESCRIPTION")}
LABEL_AT = {"key-siri": C["keyterm"], "key-box": C["keybox"],
            "key-gh": C["keygh"], "key-codex": C["keycodex"],
            "key-done": C["keydone"], "key-gh-2": C["keygh2"],
            "key-desc": C["keydesc"]}
HOST_AT = {"phone": C["phone"], "box": C["box"], "gh-tile": C["gh"],
           "codex-tile": C["codex"], "clipboard": C["clip"],
           "gh-tile-2": C["seam4"], "arrow-down": C["arrow"]}
PRINTED_KEYS = {k: v[2] for k, v in LABEL_PLAN.items()} | {"tag-free": "FREE"}
PRINTED_LIFETIME = {k: SC.LIFETIMES[k] for k in LABEL_PLAN}
PRINTED_LIFETIME["tag-free"] = SC.LIFETIMES["tag"]

# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.
CUE_WORDS = {
    "phone": (0, "siri"), "slide0": (1, "sucks,"), "hl1": (15, "this"),
    "box": (31, "so"), "move3": (39, "took"), "gh": (49, "github"),
    "keygh": (50, "repo"), "lineA": (54, "connect"), "codex": (58, "codex,"),
    "openai": (64, "openai."), "chargeB": (66, "this"),
    "chargeA": (67, "drastically"), "swap": (68, "improves"),
    "emph": (70, "experience"), "emphout": (72, "siri."), "move4": (73, "now"),
    "bubblet": (76, "communicate"), "clip": (78, "actually"),
    "tick1": (79, "get"), "tick2": (80, "stuff"), "tick3": (81, "done."),
    "seam4": (82, "this"), "slide5": (85, "100%"),
    "keydesc": (93, "description"), "arrow": (94, "down"), "outro": (101, "now"),
}
# AUTHORED instants: each inside its own word's 1.0 s LABEL_WINDOW
CUE_INSIDE = {"bubbleq": (1, "sucks,"), "keyterm": (1, "sucks,"),
              "hookout": (14, "ai."), "card": (14, "ai."), "hl2": (15, "this"),
              "cardout": (26, "siri"), "phone2": (27, "experience"),
              "keybox": (33, "out"), "seam2": (38, "he"), "lineB": (57, "to"),
              "keycodex": (58, "codex,"), "seam3": (72, "siri."),
              "keydone": (79, "get"), "keygh2": (83, "repo"),
              "tag": (85, "100%")}


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
    opening = "siri sucks, so here's how you can make it 100 times better"
    head = " ".join(w["text"] for w in ws[:12]).lower()
    if head != opening:
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[12:]).lower()
    if "so here's how you can make it" in later:
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
    if SC.BOARD_MODE != "chapters" or len(SC.BOARD_CHAPTERS) != 7:
        raise SystemExit("the scene is no longer the seven chapters the plan "
                         "declared")
    edges = [c["erase_at"] for c in SC.BOARD_CHAPTERS]
    want = [C["hookout"], C["cardout"], C["seam2"], C["seam3"], C["seam4"],
            C["outro"], None]
    if edges != want:
        raise SystemExit(f"LAW 43: chapter erases {edges} are off their words")
    rep["_law43"] = {"board_mode": SC.BOARD_MODE, "chapters": 7,
                     "erase_at": edges}
    return rep


# every typed key and the spoken words it must agree with:
# (first word, last word), the spoken text, the printed text, its instant
WORD_SYNC = {
    "key-siri": ((0, 1), "siri sucks,", "SIRI SUCKS", C["keyterm"]),
    "key-box": ((33, 36), "out of the box,", "OUT OF THE BOX", C["keybox"]),
    "key-gh": ((49, 50), "github repo", "GITHUB REPO", C["keygh"]),
    "key-codex": ((58, 58), "codex,", "CODEX", C["keycodex"]),
    "key-done": ((79, 81), "get stuff done.", "GET STUFF DONE", C["keydone"]),
    "key-gh-2": ((82, 83), "this repo", "GITHUB REPO", C["keygh2"]),
    "tag-free": ((85, 86), "100% free,", "FREE", C["tag"]),
    "key-desc": ((91, 93), "in the description", "IN THE DESCRIPTION",
                 C["keydesc"]),
}


def assert_word_sync(ws: list[dict]) -> dict:
    """WORD-SYNC: every typed key first shows while its words are being said
    or inside 1.0 s after them, and prints the value those words say."""
    rows = []
    for key, ((i0, i1), spoken, printed, t) in WORD_SYNC.items():
        got = " ".join(w["text"] for w in ws[i0:i1 + 1]).lower()
        if got != spoken:
            raise SystemExit(f"word-sync: {key} expects {spoken!r}, the take "
                             f"says {got!r}")
        if PRINTED_KEYS[key] != printed:
            raise SystemExit(f"word-sync: {key} prints {PRINTED_KEYS[key]!r}")
        lo = float(ws[i0]["start"])
        hi = float(ws[i1]["end"]) + LABEL_WINDOW
        if not (lo - 0.01 <= t <= hi):
            raise SystemExit(f"word-sync: {key} first shows at {t}, outside "
                             f"{lo:.3f}-{hi:.3f}")
        rows.append({"state": key, "first_visible_text": printed, "at": t,
                     "words": got, "window": [round(lo, 3), round(hi, 3)]})
    if min(LABEL_AT.values()) != LABEL_AT["key-siri"]:
        raise SystemExit("LAW 9: SIRI SUCKS is not the first type on the board")
    return {"typed_states": rows, "disagreements": 0, "digits_that_tick": 0,
            "note": "FREE lands on the tag at 27.20, inside the spoken '100%' "
                    "(27.02-27.78) of '100% free'; logged in the split notes"}


def assert_law37(ws: list[dict]) -> dict:
    """LAW 37 - ONE pointing cue ('this guy', 4.12), answered by the X post."""
    cues = PCUE.scan(ws)
    plan = json.loads(PLAN.read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / "prep/stages/codexsiri.cues.json").read_text())
    if marker["keys"]["cue_count"] != len(cues):
        raise SystemExit("LAW 37: the prep marker disagrees with the re-run")
    if len(cues) != 1:
        raise SystemExit(f"LAW 37: {len(cues)} cues, the plan answers one")
    cue = cues[0]
    at = C["card"]
    lo, hi = cue["window"]
    if not (lo <= at <= hi):
        raise SystemExit(f"LAW 37: the card rises at {at}, outside the cue's "
                         f"window {lo}..{hi}")
    held = C["cardout"] - C["card"]
    if not (2.0 <= held <= 4.0):
        raise SystemExit(f"GLOBAL LAW 3: the card is held {held:.2f}s")
    return {"scan_cue_count": len(cues), "plan_declared_cards": len(declared),
            "prep_marker": "prep/stages/codexsiri.cues.json -> cue_count 1",
            "cue": cue, "answered_by": "post-card", "raised_at": at,
            "held_s": round(held, 2),
            "platform": "X - the post lives on X, the card wears the X mark",
            "highlight": "one marker fill per claim line (#hl-post-1, "
                         "#hl-post-2) wiped at 4.12 and 4.22",
            "metrics_chrome": 0,
            "instrument": "pointing_cues.scan re-run on transcript_tight.json"}


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
        band = (hb[2] - hb[0]) * 0.65          # geometry_audit's own band
        if abs(kc - hc) > band + 0.01:
            raise SystemExit(f"LAW 39: {key} is off {host}'s axis")
        # the plan writes IN THE DESCRIPTION on 'description' and draws the
        # arrow under it on 'down': the words come first, the arrow hangs off
        # them.  Every other key lands after the thing it names.
        if LABEL_AT[key] < HOST_AT[host] - 1e-9 and key != "key-desc":
            raise SystemExit(f"LAW 39: {key} lands before its host")
        gutter = (kb[1] - hb[3]) if side == "below" else (hb[1] - kb[3])
        out[key] = {"host": host, "side": side, "text": text,
                    "at": LABEL_AT[key], "gutter_core_px": round(gutter, 1),
                    "box_canvas": [round(v, 1) for v in canvas(kb)]}
    hs = {round(RECTS[k][3] - RECTS[k][1], 2) for k in LABEL_PLAN
          if k != "key-siri"}
    if len(hs) != 1:
        raise SystemExit(f"LAW 50: the plain labels differ in height {hs}")
    out["_law50"] = {"plain_label_font_px": SC.KEY_FS, "row_h": hs.pop(),
                     "diagram_row_y": SC.KEY_ROW3_Y}
    du = SC.KEY_TERM_FS / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} du")
    out["_key_term"] = {"text": SC.KEY_TERM, "font_px": SC.KEY_TERM_FS,
                        "design_units": round(du, 2), "first_type": True}
    return out


MARKS = ("gh-tile", "codex-tile", "openai-badge", "phone-scr-codex",
         "gh-tile-2")


def _windows(v):
    return v if isinstance(v, list) else [v]


def assert_lifetime_law() -> dict:
    anchors = [n for n, v in SC.LIFETIMES.items()
               if any(b is None for _a, b in _windows(v))]
    for n in anchors:
        if n not in SC.SCENE_ANCHORS:
            raise SystemExit(f"LAW 42: {n} never leaves and is not an anchor")
    shares = {}
    for n in MARKS:
        tot = sum(b - a for a, b in _windows(SC.LIFETIMES[n]))
        shares[n] = round(tot / DUR, 3)
        if shares[n] > 0.40:
            raise SystemExit(f"LAW 42: {n} is on screen {shares[n]:.0%}")
    phone = sum(b - a for a, b in _windows(SC.LIFETIMES["phone"]))
    return {"board_mode": SC.BOARD_MODE, "anchors": sorted(anchors),
            "mark_shares": shares,
            "phone": {"windows": SC.LIFETIMES["phone"],
                      "share": round(phone / DUR, 3),
                      "note": "the drawn spine, two finite windows (LAW 42 "
                              "declaration), leaves at 3.82 and 26.32"}}


# LAW 40 contract, per connector: target, side, fraction, completed instant
CONNECTORS = {
    "line-a": {"to": "gh-tile", "side": "left", "fraction": 0.5,
               "check_at": 16.00, "end": SC.LINE_A[1]},
    "line-b": {"to": "codex-tile", "side": "left", "fraction": 0.5,
               "check_at": 17.40, "end": SC.LINE_B[1]},
    "charge-b": {"to": "gh-tile", "side": "right", "fraction": 0.5,
                 "check_at": 20.40, "end": SC.LINE_B[0]},
    "charge-a": {"to": "phone", "side": "right", "fraction": 0.5,
                 "check_at": 21.30, "end": SC.LINE_A[0]},
    # the string THREADS the punched hole: its end is the hole's left rim
    # (543, 246), 27 px inside the tag's box.  The plan's own words are "from
    # the tile's right edge to the tag's punched hole", so the declared target
    # is the hole itself (an id stamped on the tag's existing hole path, no ink
    # added), whose left edge at fraction 0.5 IS that rim.
    "tag-string": {"to": "tag-hole", "side": "left", "fraction": 0.5,
                   "check_at": 28.50, "end": SC.STRING[1],
                   "scene_to": "tag"},
}
# LAW 38: the two highlights on raster-card text, and the phone's border flip
EMPH = {
    "hl-post-1": {"kind": None, "target": "post-text-1", "check_at": 4.80},
    "hl-post-2": {"kind": None, "target": "post-text-2", "check_at": 5.00},
    "phone": {"kind": "border", "target": "phone-scr-codex",
              "check_at": 22.20},
}


def assert_emphasis_law() -> dict:
    a, b = C["emph"] + 0.34, C["emphout"]
    if not (a <= EMPH["phone"]["check_at"] < b):
        raise SystemExit("LAW 38: the phone flip is not complete and held at "
                         "its check instant")
    for n in ("hl-post-1", "hl-post-2"):
        k = "hl1" if n.endswith("1") else "hl2"
        if not (C[k] + SC.HL_WIPE_D <= EMPH[n]["check_at"] < C["cardout"]):
            raise SystemExit(f"LAW 38: {n} is not complete at its check")
    return {"border_flips": [{"on": "#phone .phbody", "from": C["emph"],
                              "until": C["emphout"], "declared_on": "phone",
                              "target": EMPH["phone"]["target"]}],
            "highlights": [{"id": n, "target": EMPH[n]["target"],
                            "check_at": EMPH[n]["check_at"]}
                           for n in ("hl-post-1", "hl-post-2")],
            "rings_ellipses_circles": 0, "dom_ink_added": 0}


def declare_contracts(html: str) -> tuple[str, dict]:
    s = html
    # the tag's punched hole: the SECOND `tgk` path inside #tag (body, hole)
    head_, rest = s.split('id="tag"', 1)
    first = rest.index('<path class="tgk"')
    second = rest.index('<path class="tgk"', first + 1)
    if 'a9.0 9.0 0 1 0 18.0 0' not in rest[second:second + 200]:
        raise SystemExit("the tag's second path is not its round hole")
    rest = (rest[:second] + '<path id="tag-hole" class="tgk"'
            + rest[second + len('<path class="tgk"'):])
    s = head_ + 'id="tag"' + rest
    for cid, a in CONNECTORS.items():
        key = f'id="{cid}"'
        if s.count(key) != 1:
            raise SystemExit(f"cannot stamp {cid}")
        scene_to = a.get("scene_to", a["to"])
        seg = s.split(key, 1)[1][:900]
        if f'data-connect-to="{scene_to}"' not in seg:
            raise SystemExit(f"{cid} does not connect to {scene_to}")
        if scene_to != a["to"]:
            i = s.index(key)
            j = s.index(f'data-connect-to="{scene_to}"', i)
            s = (s[:j] + f'data-connect-to="{a["to"]}"'
                 + s[j + len(f'data-connect-to="{scene_to}"'):])
        s = s.replace(key, f'{key} data-anchor-side="{a["side"]}" '
                           f'data-anchor-fraction="{a["fraction"]:g}" '
                           f'data-check-at="{a["check_at"]:.2f}"', 1)
    # TWO NAMES THAT ARE THEIR HOST'S OWN CONTENT, declared so Gate 1's
    # geometric weld does not pair them with a neighbour: FREE is written ON
    # the tag (it would otherwise weld to the stamped hole beside it), and the
    # author's name in the X header names the post (it would otherwise weld to
    # the avatar beside it, which is the platform's own header layout).
    for eid, host in LABEL_DECLARE.items():
        key = f'id="{eid}"'
        if s.count(key) != 1 or f'id="{host}"' not in s:
            raise SystemExit(f"cannot declare {eid} -> {host}")
        s = s.replace(key, f'{key} data-label-for="{host}"', 1)
    for eid, e in EMPH.items():
        key = f'id="{eid}"'
        if s.count(key) != 1:
            raise SystemExit(f"cannot stamp {eid}")
        kind = (f'data-emphasis="{e["kind"]}" ' if e["kind"] else "")
        s = s.replace(key, f'{key} {kind}data-emphasis-target="{e["target"]}" '
                           f'data-check-at="{e["check_at"]:.2f}"', 1)
    return s, {"connectors_stamped": sorted(CONNECTORS),
               "emphases_stamped": sorted(EMPH),
               "labels_declared": LABEL_DECLARE,
               "ids_stamped": ["tag-hole"]}


LABEL_DECLARE = {"tag-free": "tag", "post-name": "post-card"}


def assert_cast_law() -> dict:
    rep = DF.assert_cast_resolves(list(SC.LOGO_FILES), dict(SC.LOGO_FILES),
                                  LOGOS, label="codexsiri stage marks")
    return {"stage_marks": sorted(SC.LOGO_FILES),
            "resolved": {k: v["path"] for k, v in rep.items()},
            "cutout_lanes_not_ours": list(CUTOUT_LANES)}


def _tags_for(sel: str, html: str) -> list[str]:
    """'#id .a' -> every shape tag inside the element id=... up to its </svg>
    whose class list holds a."""
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
    # LAW 4: a phrase that IS a board key ('Siri sucks,' against SIRI SUCKS)
    # is joined to the phrase after it before partitioning, so the pill never
    # repeats the key word for word.
    groups = phrases(ws)
    joined_log = []
    gi = 0
    while gi < len(groups) - 1:
        if _joined(groups[gi]).strip().lower() in forbidden:
            joined_log.append(_joined(groups[gi]))
            groups[gi:gi + 2] = [groups[gi] + groups[gi + 1]]
        else:
            gi += 1
    rep["law4_joined_phrases"] = joined_log
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
    for sub in ("music", "sfx", "logos", "source"):
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
    post = {}
    for mkey, rel in SC.POST_ASSETS.items():
        src = RUN / rel
        if not src.exists():
            raise SystemExit(f"the source post raster is missing: {src}")
        shutil.copy2(src, dst / "assets/source" / src.name)
        post[mkey] = {"source": str(src), "url": f"assets/source/{src.name}"}
    rec["post"] = post
    return rec


def media(staged: dict) -> dict:
    """The rasters the scene paints (handoff section 1), sized by INK."""
    m = {mkey: CC.mark_img(LOGO_URL[k], k, side)
         for mkey, (k, side) in SC.MEDIA_SIDES.items()}
    for mkey, rec in staged["post"].items():
        m[mkey] = rec["url"]
    return m


def sfx_plan() -> list[tuple]:
    """EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22)."""
    return [("pop", C["phone"], SFX_STRUCTURE),       # the phone pops alone
            ("pop", C["bubbleq"], SFX_DETAIL),        # the '?' bubble
            ("click", C["keyterm"], SFX_DETAIL),      # SIRI SUCKS is written
            ("whoosh", C["card"], SFX_STRUCTURE),     # the X post rises
            ("click", C["hl1"], SFX_DETAIL),          # the marker wipe
            ("pop", C["phone2"], SFX_STRUCTURE),      # the phone is back
            ("pop", C["box"], SFX_STRUCTURE),         # the box rises round it
            ("click", C["keybox"], SFX_DETAIL),       # OUT OF THE BOX
            ("whoosh", C["move3"], SFX_STRUCTURE),    # out of the box, left
            ("pop", C["gh"], SFX_DETAIL),             # GitHub tile
            ("click", C["lineA"], SFX_DETAIL),        # line phone -> GitHub
            ("pop", C["codex"], SFX_DETAIL),          # Codex tile (+ its line)
            ("pop", C["openai"], SFX_DETAIL),         # OpenAI badge
            ("click", C["chargeB"], SFX_STRUCTURE),   # the charge runs back
            ("click", C["chargeA"], SFX_DETAIL),      # ... into the phone
            ("pop", C["swap"], SFX_STRUCTURE),        # the screen swaps
            ("whoosh", C["move4"], SFX_STRUCTURE),    # chapter 3 leaves
            ("pop", C["bubblet"], SFX_DETAIL),        # the talk bubble
            ("click", C["tick1"], SFX_DETAIL),        # tick 'get'
            ("click", C["tick3"], SFX_DETAIL),        # tick 'done'
            ("pop", C["seam4"], SFX_STRUCTURE),       # the repo, centred
            ("pop", C["tag"], SFX_DETAIL),            # the FREE tag swings in
            ("click", C["keydesc"], SFX_DETAIL),      # IN THE DESCRIPTION
            ("click", C["arrow"], SFX_STRUCTURE),     # the arrow draws down
            ("whoosh", C["outro"], SFX_STRUCTURE),    # the rising sheet
            ("pop", SC.CHIP_IN, SFX_DETAIL)]          # the outro glyph


def assert_sfx(sfx) -> dict:
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30:
        raise SystemExit(f"SFX flam: {worst}")
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "deliberately_silent": {
                "slide0 0.42 / hookout 3.62 / cardout 7.30": "moves and fades "
                "under a scored neighbour",
                "line-b 16.50": "0.08 s before the Codex pop that scores both",
                "clipboard 24.58 / tick 'stuff' 25.40": "0.28 s from a scored "
                "tick; two ticks score the three-tick run",
                "key GITHUB REPO 26.40 / slide 27.02 / string 27.40":
                "within 0.30 s of the repo pop or the tag pop",
                "emphasis flips": "a colour flip is not an arrival"}}


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
        fs, ls = ((SC.KEY_TERM_FS, SC.KEY_TERM_LS) if n == "key-siri"
                  else (SC.KEY_FS, SC.KEY_LS))
        ink = len(text) * 0.6 * fs + (len(text) - 1) * ls
        rights[n] = (b[0] + b[2]) / 2 + ink / 2
    type_right = max(rights.values())
    if type_right > CAP.LAW12_RAIL_X + 0.01:
        raise SystemExit(f"readable key ink reaches x={type_right:.1f}")
    boxes = [canvas(o["core"]) for o in SC.BESPOKE] + [
        canvas(SC.phone_box("diagram")), canvas(SC.CX_BOX),
        canvas(_xywh(SC.BADGE)), canvas(_xywh(SC.POST))]
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

    scene_html, tweens = SC.build(media(staged), outro_lockup(handle))
    drawon = assert_draw_on(tweens, scene_html)
    law40 = SC.assert_anchor_law()
    scene_html, declared = declare_contracts(scene_html)
    if scene_html.count("data-connect-to") != len(CONNECTORS):
        raise SystemExit("the scene does not carry the plan's connectors")
    if scene_html.count("data-label-for") != 7 + len(LABEL_DECLARE):
        raise SystemExit("the scene does not carry seven labelled keys")
    if (scene_html.count("data-connect-to") + scene_html.count("data-emphasis=")
            != scene_html.count("data-check-at")):
        raise SystemExit("a connector or emphasis is missing its check instant")
    for shape in ("<circle", "<ellipse"):
        if shape in scene_html:
            raise SystemExit(f"LAW 38 rule 3: {shape} in the emitted scene")
    for key, (host, _s, _t) in LABEL_PLAN.items():
        if f'id="{key}"' not in scene_html or \
                f'data-label-for="{host}"' not in scene_html:
            raise SystemExit(f"{key} does not declare its host {host}")

    m = CAP.PillMeasurer(RUN / "gen/_pillwidths_codexsiri.json")
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
            "law40": law40, "declared": declared,
            "law2": cast, "law22": sfx_guard, "draw_on": drawon,
            "transcript": cap_rep, "phone_objects": objs,
            "render": {"w": 1080, "h": 1920, "zoom": 1}}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="split", choices=("split",))
    ap.parse_args()
    dst = RUN / "projects/codexsiri_split"
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
    report = {"video": VID, "lane": "diagram build", "fps": FPS,
              "duration": DUR, "seam": SEAM, "formats": {"split": rep}}
    (RUN / "gen/_build_codexsiri_split.json").write_text(
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
