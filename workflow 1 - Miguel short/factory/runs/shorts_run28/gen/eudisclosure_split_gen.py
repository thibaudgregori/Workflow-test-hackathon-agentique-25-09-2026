#!/usr/bin/env python3
"""ONE BUILD, ONE DOM COMPOSITION - eudisclosure / ICON CHOREOGRAPHY.

    YouTube   classic split 50/50   projects/eudisclosure_split   @migueltorrezai

THE LANE SCENE IS CONSUMED, NEVER RE-AUTHORED.  `gen/eudisclosure_scene.py` plus
`plans/eudisclosure_scene_handoff.md` are the design agent's artefacts, sealed by
`review/artwork_pass_eudisclosure.json` (production v4, `production.py seal`).
This file IMPORTS the module and SEATS it at the handoff's own placement
(k = 1.00, left 0, core top 192).  It never mutates a byte of the module and it
adds nothing to the emitted scene string: the scene has no connector, no label
and no emphasis to declare (handoff section 5).

HD DELIVERY: authored AND encoded 1080x1920.  The face plate is
`face_bottom_hd.mp4` (1080x1058), so the seam is 1920 - 1057.5 = 862.5 and the
RENDERING pill top is 862.5 - 114.59/2 = 805.205 (the pill that renders, never
the frozen 108.2 seat constant).  The core's content band 96..500 lands at
canvas 288..692: 96 px under LAW 30's top-10 % line and ~113 px over the pill.

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
sys.path.insert(0, str(Path(__file__).resolve().parent))
import captions as CAP                          # noqa: E402
import pointing_cues as PCUE                    # noqa: E402
import eudisclosure_scene as SC                 # noqa: E402

RUN = Path(__file__).resolve().parents[1]
CUT = RUN / "cuts/eudisclosure"
PLAN = RUN / "plans/eudisclosure_plan.json"
ASSETS = Path.home() / "Documents/Workspace/assets"
LIB_MUSIC = ASSETS / "audio/music/shorts-factory"
LIB_SFX = ASSETS / "audio/sfx/shorts-factory"

VID = "eudisclosure"
W, H = 1080.0, 1920.0
FPS = 25
DUR = SC.DUR                                     # 27.64, the cut master

SEAM = 862.5
CORE_TOP_SPLIT = SC.CANVAS_OFFSET                # 192.0, the handoff's number
CORE_K = 1.00
LEFT = (W - SC.CORE_W * CORE_K) / 2              # 0.0

SFX_STRUCTURE = 0.14
SFX_DETAIL = 0.09
BED = 0.065                                      # AUDIO MIX LAW

TITLE = "In Europe you must disclose AI"
LABEL_WINDOW = 1.0

# ------------------------------------------------------------------ printed keys
# Every word the top zone types.  DISCLOSE is the key term; the rest are stamp
# IMPRINTS, each a child of the object it is printed on (handoff section 5).
PRINTED_KEYS = {"key-disclose": SC.KEY_TERM, "imp-bub": "AI", "imp-page": "AI",
                "imp-pd-gen": "AI GENERATED", "imp-pd-mod": "AI MODIFIED",
                "imp-pd-real": "AI MODIFIED", "imp-shot": "AI MODIFIED"}
IMP_HOST = {"imp-bub": "bubble", "imp-page": "page", "imp-pd-gen": "pd-gen",
            "imp-pd-mod": "pd-mod", "imp-pd-real": "pd-real",
            "imp-shot": "shot"}
# the sheet covers the key term at SHEET_UP + SHEET_D + 0.02
KEY_TERM_GONE = SC.SHEET_UP + SC.SHEET_D + 0.02


def printed_lifetime(key: str) -> tuple:
    a, b = SC.LIFETIMES[key]
    return a, (b if b is not None else KEY_TERM_GONE)


# THE CUE TABLE, RE-READ OFF THE TIGHT TRANSCRIPT RATHER THAN TRUSTED.
CUE_WORDS = {
    "stars": (4, "europe,"), "keyterm": (9, "disclose"),
    "bubble": (17, "chatbot"), "slide_b": (19, "ai"),
    "stamp_b": (20, "generated"), "hit_bubble": (21, "content."),
    "hit_page": (22, "and"), "gen": (27, "ai"), "slide_c": (34, "because"),
    "stamp_c": (38, "say"), "mod": (41, "image"), "hit_gen": (43, "ai"),
    "hit_mod": (46, "ai"), "c_out": (48, "so"), "real": (53, "real"),
    "slide_d": (57, "real"), "color": (70, "color"),
    "light": (72, "lighting,"), "stamp_d": (73, "you"),
    "hit_photo": (77, "disclose"), "hit_shot": (78, "that."),
    "outro": (79, "now"),
}
# AUTHORED instants: each inside its own word's 1.0 s LABEL_WINDOW.  The
# handoff files "pole" under "in"; 0.44 is 0.06 s before "in" starts, so it is
# verified against "live" (0.32-0.44), whose window it sits in.
CUE_INSIDE = {"pole": (2, "live"), "field": (3, "in"), "flag_out": (15, "it's"),
              "page": (19, "ai"), "b_out": (25, "case"), "shot": (57, "real")}


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
    opening = "if you live in europe, now you have to disclose"
    head = " ".join(w["text"] for w in ws[:10]).lower()
    if head != opening:
        raise SystemExit(f"the take does not open on the scripted line: {head!r}")
    later = " ".join(w["text"] for w in ws[10:]).lower()
    if "live in europe" in later:
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
        if not (lo <= t <= hi):
            raise SystemExit(f"cue {name} at {t} is outside the window of "
                             f"{w['text']!r} ({lo:.3f}-{hi:.3f})")
        rep[name] = {"word": idx, "text": w["text"], "t": t,
                     "window": [round(lo, 3), round(hi, 3)]}
    missing = set(SC.CUE) - set(rep)
    if missing:
        raise SystemExit(f"cues the build never verified: {sorted(missing)}")
    if SC.BOARD_MODE != "chapters" or len(SC.BOARD_CHAPTERS) != 4:
        raise SystemExit("the scene is no longer the four chapters the plan "
                         "declared")
    edges = [c["erase_at"] for c in SC.BOARD_CHAPTERS]
    if edges != [SC.CUE["bubble"], SC.CUE["gen"], SC.CUE["c_out"],
                 SC.CUE["outro"]]:
        raise SystemExit(f"LAW 43: chapter erases {edges} are off their marks")
    # LAW 45: the board's key word DISCLOSE is fully drawn across every
    # handover (it lands 1.48 + 0.32 and is only covered by the outro sheet)
    kd0 = SC.CUE["keyterm"] + 0.32
    for e in edges[:-1]:
        if not (kd0 <= e and e + 0.30 < KEY_TERM_GONE):
            raise SystemExit(f"LAW 45: the handover at {e} lands on no idea")
    rep["_law43_45"] = {"board_mode": SC.BOARD_MODE, "chapters": 4,
                        "erase_at": edges,
                        "handover_idea": "DISCLOSE (the key word) is fully "
                                         "drawn across every chapter seam"}
    return rep


# every typed key and the spoken words it must agree with:
#   key: (printed, cue, (i0, i1) the words it lands on, spoken text)
WORD_SYNC = {
    "key-disclose": ("DISCLOSE", "keyterm", (9, 9), "disclose"),
    "imp-bub": ("AI", "hit_bubble", (19, 21), "ai generated content."),
    "imp-page": ("AI", "hit_page", (19, 21), "ai generated content."),
    "imp-pd-gen": ("AI GENERATED", "hit_gen", (43, 44), "ai generated"),
    "imp-pd-mod": ("AI MODIFIED", "hit_mod", (46, 47), "ai modified."),
    "imp-pd-real": ("AI MODIFIED", "hit_photo", (77, 78), "disclose that."),
    "imp-shot": ("AI MODIFIED", "hit_shot", (77, 78), "disclose that."),
}
# chapter D's imprint names what was said a beat earlier: "use AI to even do
# slight modifications ... you also have to disclose that"
CHAPTER_D_REFERENT = ((63, 68), "ai to even do slight modifications")


def assert_word_sync(ws: list[dict]) -> dict:
    """WORD-SYNC: every typed key first shows the value its words say, while
    or just after they are said.  No digits anywhere in this scene."""
    rows = []
    for key, (printed, cue, (i0, i1), spoken) in WORD_SYNC.items():
        if printed != PRINTED_KEYS[key]:
            raise SystemExit(f"word-sync: {key} prints {PRINTED_KEYS[key]!r}")
        got = " ".join(w["text"] for w in ws[i0:i1 + 1]).lower()
        if got != spoken:
            raise SystemExit(f"word-sync: {key} expects {spoken!r}, the take "
                             f"says {got!r}")
        t = SC.CUE[cue]
        lo = float(ws[i0]["start"]) - 0.011
        hi = float(ws[i1]["end"]) + LABEL_WINDOW
        if not (lo <= t <= hi):
            raise SystemExit(f"word-sync: {key} first shows at {t}, outside "
                             f"{lo:.3f}-{hi:.3f}")
        if printed_lifetime(key)[0] != t:
            raise SystemExit(f"word-sync: {key}'s lifetime does not start on "
                             "its press")
        rows.append({"state": key, "first_visible_text": printed,
                     "at": round(t, 2), "words": got,
                     "window": [round(lo, 3), round(hi, 3)]})
    (r0, r1), ref = CHAPTER_D_REFERENT
    got = " ".join(w["text"] for w in ws[r0:r1 + 1]).lower()
    if got != ref or float(ws[r1]["end"]) > SC.CUE["hit_photo"]:
        raise SystemExit("word-sync: chapter D's AI MODIFIED has no referent")
    if any(re.search(r"\d", v) for v in PRINTED_KEYS.values()):
        raise SystemExit("word-sync: a printed key carries a digit")
    if SC.CUE["keyterm"] != min(printed_lifetime(k)[0] for k in PRINTED_KEYS):
        raise SystemExit("LAW 9: DISCLOSE is not the first type on the board")
    return {"typed_states": rows, "disagreements": 0, "digits_that_tick": 0,
            "chapter_d_referent": {"words": got,
                                   "said": [ws[r0]["start"], ws[r1]["end"]]}}


def assert_law37(ws: list[dict]) -> dict:
    cues = PCUE.scan(ws)
    plan = json.loads(PLAN.read_text())
    declared = plan.get("pointing_cues") or []
    PCUE.assert_cues_covered(cues, declared)
    marker = json.loads((RUN / "prep/stages/eudisclosure.cues.json").read_text())
    if marker["keys"]["cue_count"] != len(cues):
        raise SystemExit("LAW 37: the prep marker disagrees with the re-run")
    if cues or declared:
        raise SystemExit("LAW 37: this scene builds no source card")
    return {"scan_cue_count": 0, "plan_declared_cards": 0,
            "source_cards_in_the_page": 0}


# ------------------------------------------------------------------ laws
def assert_label_law(scene_html: str) -> dict:
    """LAW 39 / 50: no free label.  Every imprint is a CHILD of its host, all
    imprints share one size and one rotation."""
    if "data-label-for" in scene_html:
        raise SystemExit("LAW 39: the scene emits a free label")
    out = {}
    for imp, host in IMP_HOST.items():
        m = re.search(rf'<div class="abs [^"]*" id="{host}"', scene_html)
        if not m:
            raise SystemExit(f"LAW 39: host #{host} missing")
        # the imprint sits inside the host's div before the next top-level host
        seg = scene_html[m.end():]
        nxt = min((seg.find(f'id="{h}"') for h in IMP_HOST.values()
                   if h != host and seg.find(f'id="{h}"') >= 0),
                  default=len(seg))
        if f'id="{imp}"' not in seg[:nxt]:
            raise SystemExit(f"LAW 39: #{imp} is not a child of #{host}")
        if not any(imp in b and host in b for b in SC.DECLARED_BLOCKS):
            raise SystemExit(f"LAW 41: {imp} is not blocked with {host}")
        w = SC.imp_w(PRINTED_KEYS[imp])
        host_w = SC.BUB_W if host == "bubble" else (
            SC.PG_W if host == "page" else SC.PD_W)
        margin = (host_w - w) / 2
        if margin < 15:
            raise SystemExit(f"LAW 41: {imp} leaves {margin:.1f}px in its host")
        out[imp] = {"host": host, "text": PRINTED_KEYS[imp],
                    "box_w": round(w, 1), "side_margin_px": round(margin, 1)}
    sizes = set(re.findall(r'class="abs mono imp"[^>]*font-size:(\d+)px',
                           scene_html))
    rots = set(re.findall(r'class="abs mono imp"[^>]*rotate\(([-\d.]+)deg',
                          scene_html))
    if len(sizes) != 1 or len(rots) != 1:
        raise SystemExit(f"LAW 50: imprints differ in size {sizes} / rotation "
                         f"{rots}")
    out["_law50"] = {"imprint_font_px": sizes.pop(), "rotation_deg": rots.pop()}
    du = SC.KEY_TERM_FS / CAP.S
    if du < 22.0:
        raise SystemExit(f"LAW 9: the key term is {du:.1f} du")
    out["_key_term"] = {"text": SC.KEY_TERM, "font_px": SC.KEY_TERM_FS,
                        "design_units": round(du, 2), "first_type": True}
    return out


COVERS = ("o-sheet",)


def assert_lifetime_law() -> dict:
    shares = {}
    for n, (a, b) in SC.LIFETIMES.items():
        if b is None:
            if n not in SC.SCENE_ANCHORS and n not in COVERS:
                raise SystemExit(f"LAW 42: {n} never leaves and is not an anchor")
            continue
        shares[n] = round((b - a) / DUR, 3)
        if shares[n] > 0.40:
            raise SystemExit(f"LAW 42: {n} is on screen {shares[n]:.0%}")
    return {"board_mode": SC.BOARD_MODE, "anchors": list(SC.SCENE_ANCHORS),
            "covers": list(COVERS), "longest_mark_share": max(shares.values()),
            "mark_shares": shares}


def assert_no_emphasis_no_connector(scene_html: str) -> dict:
    """LAW 38 / LAW 40: the scene declares neither (handoff section 5)."""
    for shape in ("<circle", "<ellipse", "data-emphasis", "data-connect-to"):
        if shape in scene_html:
            raise SystemExit(f"LAW 38/40: {shape} in the emitted scene")
    if SC.CONNECTORS:
        raise SystemExit("LAW 40: the module declares a connector")
    return {"connectors": 0, "emphasis_strokes": 0,
            "rings_ellipses_circles": 0}


def _tags_for(sel: str, html: str) -> list[str]:
    """'#id' -> the shape with that id; '#id .a' -> every shape inside the
    element id=... up to its </svg> whose class list holds every class."""
    parts = sel.split()
    if not parts[0].startswith("#"):
        raise SystemExit(f"unexpected dash selector {sel}")
    hid = parts[0][1:]
    if len(parts) == 1:
        return re.findall(rf'<(?:path|polyline|polygon|line|rect)\b[^>]*'
                          rf'id="{re.escape(hid)}"[^>]*>', html)
    if len(parts) != 2:
        raise SystemExit(f"unexpected dash selector {sel}")
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
            k0, k1 = printed_lifetime(key)
            if b["start"] < k1 and k0 < b["start"] + b["dur"]:
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
    # the scene's eases are string literals (handoff section 1)
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
SFX_FILES = ("pop", "click", "low_thump")


def stage(dst: Path, *, face: str) -> dict:
    v = dst / "assets/v"
    v.mkdir(parents=True, exist_ok=True)
    for sub in ("music", "sfx"):
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
    for s in SFX_FILES:
        src = LIB_SFX / f"{s}.mp3"
        if not src.exists():
            raise SystemExit(f"the {s} sfx does not resolve: {src}")
        shutil.copy2(src, dst / f"assets/sfx/{s}.mp3")
        rec["sfx_sources"][s] = str(src)
    shutil.copy2(CUT / face, v / face)
    rec["face"] = {"file": face, **probe_wh(CUT / face)}
    if SC.LOGO_FILES:
        raise SystemExit("the handoff says this scene paints no raster")
    rec["marks"] = {}
    return rec


def sfx_plan() -> list[tuple]:
    """EVERY SFX IS FRAME-LOCKED TO THE VISUAL EVENT IT SCORES (LAW 22)."""
    C = SC.CUE
    return [("pop", C["pole"], SFX_STRUCTURE),          # the flag draws
            ("click", C["keyterm"], SFX_DETAIL),        # DISCLOSE is typed
            ("pop", C["bubble"], SFX_STRUCTURE),        # the chat bubble
            ("pop", C["page"], SFX_DETAIL),             # the page draws
            ("low_thump", C["hit_bubble"], SFX_DETAIL),  # press: AI
            ("low_thump", C["hit_page"], SFX_DETAIL),    # press: AI
            ("pop", C["gen"], SFX_STRUCTURE),           # the AI Polaroid
            ("pop", C["stamp_c"], SFX_DETAIL),          # the stamp drops in
            ("pop", C["mod"], SFX_DETAIL),              # the second Polaroid
            ("low_thump", C["hit_gen"], SFX_DETAIL),     # press: AI GENERATED
            ("low_thump", C["hit_mod"], SFX_DETAIL),     # press: AI MODIFIED
            ("pop", C["real"], SFX_STRUCTURE),          # the real Polaroid
            ("pop", C["shot"], SFX_DETAIL),             # the screenshot drops
            ("click", C["color"], SFX_DETAIL),          # sun goes terracotta
            ("click", C["light"], SFX_DETAIL),          # the rays draw
            ("pop", C["stamp_d"], SFX_DETAIL),          # the stamp drops in
            ("low_thump", C["hit_photo"], SFX_DETAIL),   # press: AI MODIFIED
            ("low_thump", C["hit_shot"], SFX_DETAIL),    # press: AI MODIFIED
            ("pop", SC.CHIP_IN, SFX_DETAIL)]            # the outro stamp glyph


def assert_sfx(sfx) -> dict:
    ts = sorted(round(t, 3) for _n, t, _v in sfx)
    worst = min((round(b - a, 3), a, b) for a, b in zip(ts, ts[1:]))
    if worst[0] < 0.30:
        raise SystemExit(f"SFX flam: {worst}")
    return {"events": len(sfx), "tightest_gap_s": worst[0],
            "deliberately_silent": {
                "field 0.56 / stars 0.64": "inside the flag's pop; one arrival",
                "flag out 3.62": "an exit; the bubble pops 0.34 s later",
                "slide 4.98 / stamp drop 5.20": "0.10 / 0.12 s around the page "
                "pop; one sound scores the move",
                "chapter exits 6.80 / 13.98": "exits stay silent",
                "slides 9.74 / 16.18": "a slide is a move, not an arrival; "
                "16.18 is also 0.10 s before the screenshot pop",
                "sheet 23.32": "0.22 s after the last press; the glyph's pop "
                "at 23.82 scores the outro"}}


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
def canvas(box):
    """core px -> the canvas this page actually paints (top 192, k 1.00)."""
    return (CORE_K * box[0] + LEFT, CORE_TOP_SPLIT + CORE_K * box[1],
            CORE_K * box[2] + LEFT, CORE_TOP_SPLIT + CORE_K * box[3])


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
    """LAW 30: readable type stays left of the rail (x 918).  The rightmost
    readable type is an imprint on the right seat (x 672 + 135 = 807)."""
    rights = {}
    kt_ink = len(SC.KEY_TERM) * 0.6 * SC.KEY_TERM_FS + (len(SC.KEY_TERM) - 1) \
        * SC.KEY_TERM_LS
    rights["key-disclose"] = SC.AXIS + kt_ink / 2
    host_cx = {"imp-bub": SC.BUB_X1 + SC.BUB_W / 2,
               "imp-page": SC.PG_X + SC.PG_W / 2,
               "imp-pd-gen": SC.L_X + SC.PD_W / 2,
               "imp-pd-mod": SC.R_X + SC.PD_W / 2,
               "imp-pd-real": SC.L_X + SC.PD_W / 2,
               "imp-shot": SC.R_X + SC.PD_W / 2}
    for k, cx in host_cx.items():
        rights[k] = LEFT + cx + SC.imp_w(PRINTED_KEYS[k]) / 2
    type_right = max(rights.values())
    if type_right > CAP.LAW12_RAIL_X + 0.01:
        raise SystemExit(f"readable imprint box reaches x={type_right:.1f}")
    boxes = [canvas(o["core"]) for o in SC.BESPOKE + SC.UI_OBJECTS]
    ink_left = min(b[0] for b in boxes)
    ink_right = max(b[2] for b in boxes)
    if ink_left < 30 or W - ink_right < 30:
        raise SystemExit("the composition leaves the frame margin")
    if abs((ink_left + ink_right) / 2 - W / 2) > 0.5:
        raise SystemExit("LAW 30 amendment: the composition is not centred")
    return {"readable_type_right_x": round(type_right, 1),
            "per_key_right_x": {k: round(v, 1) for k, v in rights.items()},
            "ink_left_x": ink_left, "ink_right_x": ink_right,
            "law30_rail_x": CAP.LAW12_RAIL_X}


# THE KEY TERM'S BOX IS TRIMMED TO ITS INK, NOT MOVED (logged in
# plans/eudisclosure_split_notes.md).  The module sizes #key-disclose as its
# 58 px LINE box (core 96..154); the DISCLOSE ink, measured on this page in the
# render browser, spans core y 106..141 (canvas 298..333).  The line box's empty
# 13 px under the baseline put the declared box 11 px from the flag finial
# (core 165) and gate 1 refused the pair (cramp, floor 16).  Setting the box
# HEIGHT to 46 px (core 96..142) keeps top, width, line-height, font and
# centring, so not one pixel of ink moves; the declared box now ends 1 px under
# the ink and the measured gutter is the real one (core 142 -> 165 = 23 px).
# The module on disk is untouched; the cutout inherits the same line box.
KEY_TERM_INK_Y = (106.0, 141.0)                  # core px, measured 2026-09-23
KEY_TERM_BOX_H = 46.0


def key_term_box_css() -> str:
    top = SC.KEY_TERM_BOX[1]
    if not (top + KEY_TERM_BOX_H >= KEY_TERM_INK_Y[1] + 1.0
            and top <= KEY_TERM_INK_Y[0]):
        raise SystemExit("the trimmed key-term box would cut its own ink")
    gut = SC.FINIAL[1] - SC.FINIAL[2] - (top + KEY_TERM_BOX_H)
    if gut < 16.0:
        raise SystemExit(f"key term to finial gutter {gut:.1f}px")
    return f"#key-disclose {{ height:{KEY_TERM_BOX_H:.0f}px !important; }}"


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
    lifetimes = assert_lifetime_law()
    SFX = sfx_plan()
    sfx_guard = assert_sfx(SFX)

    scene_html, tweens = SC.build({}, outro_lockup(handle))
    drawon = assert_draw_on(tweens, scene_html)
    labels = assert_label_law(scene_html)
    law38_40 = assert_no_emphasis_no_connector(scene_html)

    m = CAP.PillMeasurer(RUN / "gen/_pillwidths_eudisclosure.json")
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
           f"overflow:hidden; background:{SC.CREAM}; }}\n"
           + key_term_box_css())
    (out / "index.html").write_text(head(TITLE, css) + "\n".join(body)
                                    + tail(tweens), encoding="utf-8")
    return {"staged": staged, "beats": beats, "seat": SEAM, "scale": CORE_K,
            "core": {"left": LEFT, "top": CORE_TOP_SPLIT}, "band": band,
            "rail": rail, "cues": cues, "word_sync": wordsync, "law37": law37,
            "law39_50": labels, "law42": lifetimes, "law38_40": law38_40,
            "law22": sfx_guard, "draw_on": drawon, "transcript": cap_rep,
            "phone_objects": objs, "render": {"w": 1080, "h": 1920, "zoom": 1}}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="split", choices=("split",))
    ap.parse_args()
    dst = RUN / "projects/eudisclosure_split"
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
    (RUN / "gen/_build_eudisclosure_split.json").write_text(
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
