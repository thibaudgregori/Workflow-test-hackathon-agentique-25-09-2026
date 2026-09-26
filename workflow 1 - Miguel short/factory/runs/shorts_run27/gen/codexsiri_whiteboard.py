#!/usr/bin/env python3
"""codexsiri — WHITEBOARD (Reels / Instagram), plan view, SIX CHAPTERS.

    "Siri sucks, so here's how you can make it 100 times better thanks to AI.
     This guy did exactly that. He was so frustrated with the Siri experience
     that was just so bad out of the box, that he took matter into his own hands
     and created this free GitHub repo that manages to connect his Siri to
     Codex, the coding assistant made by OpenAI. Now, this drastically improves
     his experience with Siri. Now he can communicate and actually get stuff
     done. This repo is 100% free, and it's also linked in the description down
     below if you ever need it. Now follow for more AI news ..."

It does NOT import the lane scene module (`gen/codexsiri_scene.py`): the board
redraws the plan's ARGUMENT in marker ink — the same phone, "?" bubble, box,
tiles, lines, terracotta re-trace with the screen swap, talk bubble, clipboard
with three ticks, the FREE tag and the arrow — and writes the same seven keys on
the same words.  Every drawn object is a `b.stroke()` marker path (the approved
run-24 look, `references/builds/whiteboard_marker_example/`); `b.shape()` is used
only for registry marks, the pasted X post card (a raster, LAW 37) and the one
cream occluder that lets the box's front panel hide the phone's lower third.

Chapters are the plan's own (`plan.boards.mode == "chapters"`), erases at 3.62,
7.30, 10.30, 23.30, 26.10; the opaque rising sheet at 31.86.

Run:  SHORTS_RUN=<run> python codexsiri_whiteboard.py
"""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
os.environ.setdefault("SHORTS_RUN", str(RUN))

F = RUN.parent.parent
sys.path.insert(0, str(F / "formats/whiteboard/lib"))
sys.path.insert(0, str(F / "pipeline"))

import captions as CAP                                              # noqa: E402
import whiteboard_build as WB                                       # noqa: E402
import whiteboard_fix6_core as core                                 # noqa: E402
from whiteboard_build import (                                      # noqa: E402
    AX, INK, LOGOS, MUTED, TERRA, anchor_points, highlight_lines, note_asset,
    rect_points,
)

VID = "codexsiri"
PLAN = json.loads((RUN / "plans/codexsiri_plan.json").read_text())
S = core.S                                    # 1.875 frame px per board unit
SRC = RUN / "assets/source_codexsiri"


def px_of(v: float) -> float:
    return round(v * S, 2)


def cb(v: float) -> float:
    return round(v / S, 3)


# --- THE MARKS (plan.cast) + the post card's three rasters ------------------
MARKS = {"siri": LOGOS / "ai-models/siri-color.png",
         "codex": LOGOS / "coding-tools/codex-color.png",
         "github": LOGOS / "coding-tools/github-mark.png",
         "openai": LOGOS / "ai-models/openai.png",
         "xlogo": LOGOS / "platforms/x-logo.svg",
         "avatar": SRC / "avatar_sharifshameem.jpg",
         "poster": SRC / "video_poster.jpg"}
INKED = ("siri", "codex", "github", "openai")


def _measure(path: Path) -> dict:
    """A MARK IS SIZED BY ITS INK, NOT BY ITS BOX (MARK IDENTITY)."""
    from PIL import Image
    im = Image.open(path).convert("RGBA")
    x0, y0, x1, y1 = im.getchannel("A").getbbox()
    w, h = im.size
    return {"img_w": float(w), "img_h": float(h),
            "bbox_w": float(x1 - x0), "bbox_h": float(y1 - y0),
            "off_x": float((x0 + x1) / 2 - w / 2),
            "off_y": float((y0 + y1) / 2 - h / 2),
            "aspect": (x1 - x0) / (y1 - y0)}


MARK_INK = {k: _measure(MARKS[k]) for k in INKED}


# =============================================================================
# CAPTIONS — §3b is the AUTHOR'S duty (merge over the whole beat stream)
# =============================================================================
_CORE_BUILD_CAPTIONS = core.build_captions
CAPTION_REPORT: dict = {}


class _PillW:
    def __init__(self) -> None:
        self._c: dict[str, float] = {}

    def width(self, text: str) -> float:
        if text not in self._c:
            self._c.update(core.pill_widths([text]))
        return self._c[text]


def _captions(words: list[dict]) -> list[dict]:
    phrases = _CORE_BUILD_CAPTIONS(words)
    m = _PillW()
    before = [p["text"] for p in phrases]
    merged = CAP.merge_function_only_beats([p["words"] for p in phrases],
                                           core.CAP_MAX_W_PX, m)
    out: list[dict] = []
    for g in merged:
        text = " ".join(x["text"] for x in g)
        out.append({"t0": round(float(g[0]["start"]), 2),
                    "t1": round(float(g[-1]["end"]) + 0.12, 2),
                    "text": text, "n": len(g), "words": list(g),
                    "split": 0, "pill_w_px": round(m.width(text), 1)})
    out.sort(key=lambda p: p["t0"])
    for k in range(len(out) - 1):
        out[k]["t1"] = out[k + 1]["t0"]
    CAPTION_REPORT.update({
        "beats_before_merge": len(before), "beats_after_merge": len(out),
        "merges": len(before) - len(out),
        "widest_pill_px": round(max(p["pill_w_px"] for p in out), 1),
        "budget_px": core.CAP_MAX_W_PX,
        "beats": [[p["t0"], p["t1"], p["text"]] for p in out],
        "law": "captions.py 3b: merge_function_only_beats over the WHOLE beat "
               "stream, then assert_no_function_only_beat inside build()",
    })
    return out


core.build_captions = _captions


# =============================================================================
# THE LAYOUT — board design units (576 x 460), 1 u = 1.875 frame px
# =============================================================================
L = dict(
    SW_OBJ=4.2,                    # 7.9 frame px — silhouettes
    SW_DET=2.8,                    # 5.25 frame px — interior ink / connectors
    SW_HAIR=1.6,                   # 3.0 frame px — hairlines
    TILE_R=cb(18.0),
    TILE_SIDE=cb(112.0),           # 59.73 u — the chart's tile
    MARK_INK_SIDE=cb(56.0),        # 0.50 of the tile
    SCREEN_MARK=38.0,              # 71 px — the brand mark on the phone screen
    FS_TERM=23.0,                  # 43.1 frame px >= KEY_TERM_MIN_FS 22
    FS_KEY=cb(28.0),               # 14.93 u
    FS_TAG=19.0,
)
BOARD_BOX = (40.0, 150.0, 536.0, 425.0)
TS = L["TILE_SIDE"]
PW, PH = 90.0, 150.0               # ONE phone, the same size everywhere (LAW 51)
PCY = 271.0                        # the phone's centre line, every chapter


def phone_box(x0: float, y0: float = PCY - PH / 2):
    return (x0, y0, x0 + PW, y0 + PH)


def cx_of(box) -> float:
    return (box[0] + box[2]) / 2


def cy_of(box) -> float:
    return (box[1] + box[3]) / 2


# ---- CHAPTER 0 — the phone, centred then one step left, the "?" bubble -------
PH0 = phone_box(192.0, 200.0)                  # after the slide
PH0_DX = AX - cx_of(PH0)                       # +51: authored centred first
BUB0 = (298.0, 212.0, 380.0, 272.0)
BUB0_BOX = (290.0, 212.0, 380.0, 288.0)        # body + tail
# ---- CHAPTER 1 — the X post card (frame px; board = /S) ----------------------
CARD_PX = (220.0, 281.25, 640.0, 448.0)        # x, y, w, h
CARD_U = (cb(CARD_PX[0]), cb(CARD_PX[1]), cb(CARD_PX[0] + CARD_PX[2]),
          cb(CARD_PX[1] + CARD_PX[3]))
POST_LINES = ("Siri sucks. So I made a way for Codex",
              "to act as my iPhone's voice assistant.",
              "Now Codex can read my screen, control",
              "apps, and take actions on my behalf –",
              "all in vanilla iOS 27.")
POST_TEXT_Y0, POST_LH, POST_FS = 91.0, 34.0, 24.0
# ---- CHAPTER 2 — the same phone, centred, standing in its open box -----------
PH2 = phone_box(AX - PW / 2)                   # 243..333
BOXF = (214.0, 282.0, 362.0, 370.0)            # the front panel
BOX_BOX = (190.0, 254.0, 386.0, 370.0)         # front + both flaps
# ---- CHAPTER 3 — phone | GitHub | Codex --------------------------------------
PH3 = phone_box(104.0)
TRAVEL3 = PH3[0] - PH2[0]                      # -139
GH_BOX = (AX - TS / 2, PCY - TS / 2, AX + TS / 2, PCY + TS / 2)
CX_BOX = (440.0 - TS / 2, PCY - TS / 2, 440.0 + TS / 2, PCY + TS / 2)
BADGE_C, BADGE_R = (CX_BOX[2], CX_BOX[1]), 10.5
BADGE_BOX = (BADGE_C[0] - BADGE_R, BADGE_C[1] - BADGE_R,
             BADGE_C[0] + BADGE_R, BADGE_C[1] + BADGE_R)
LINE_A = (PH3[2], PCY), tuple(anchor_points(GH_BOX, 1, "left")[0])
LINE_B = tuple(anchor_points(GH_BOX, 1, "right")[0]), \
    tuple(anchor_points(CX_BOX, 1, "left")[0])
KEY_ROW3 = 312.0                               # LAW 50: one baseline row
# ---- CHAPTER 4 — the Codex phone, the talk bubble, the clipboard -------------
PH4 = phone_box(136.0)
TRAVEL4 = PH4[0] - PH3[0]                      # +32
BUB4 = (244.0, 204.0, 322.0, 262.0)
BUB4_BOX = (236.0, 204.0, 322.0, 278.0)
CLIP = (340.0, 214.0, 420.0, 322.0)
CLIP_BOX = (340.0, 206.0, 420.0, 322.0)        # board + its clip
ROWS_Y = (244.0, 270.0, 296.0)
# ---- CHAPTER 5 — the repo tile, the FREE tag, the arrow ----------------------
GH2_C = (GH_BOX[0], 190.0, GH_BOX[2], 190.0 + TS)      # popped centred
GH2_DX = -74.7                                          # 140 frame px left
GH2 = (GH2_C[0] + GH2_DX, GH2_C[1], GH2_C[2] + GH2_DX, GH2_C[3])
TAG = (262.0, 196.0, 392.0, 244.0)
TAG_HOLE, TAG_HOLE_R = (276.0, 220.0), 4.0
STRING_END = (TAG_HOLE[0] - TAG_HOLE_R, TAG_HOLE[1])
STRING_FROM = tuple(anchor_points(GH2, 1, "right")[0])
ARROW = (AX, 330.0, AX, 378.0)
ARROW_BOX = (AX - 9.0, 330.0, AX + 9.0, 380.0)

# =============================================================================
# THE WRITTEN KEYS — the plan's own words, sides and instants
# =============================================================================
#  name -> (text, cx, box top, fs, write time, duration, colour, t_to)
KEYS = {
    "SIRI SUCKS":         ("SIRI SUCKS", AX, 158.0, L["FS_TERM"], 1.04, 0.36,
                           INK, 3.62),
    "OUT OF THE BOX":     ("OUT OF THE BOX", AX, 380.0, L["FS_KEY"], 9.20, 0.30,
                           INK, 10.30),
    "GITHUB REPO":        ("GITHUB REPO", AX, KEY_ROW3, L["FS_KEY"], 14.28,
                           0.30, INK, 23.30),
    "CODEX":              ("CODEX", cx_of(CX_BOX), KEY_ROW3, L["FS_KEY"], 16.86,
                           0.20, INK, 23.30),
    "GET STUFF DONE":     ("GET STUFF DONE", cx_of(CLIP), 332.0, L["FS_KEY"],
                           25.04, 0.30, INK, 26.10),
    # the SAME words a second time, on the second tile: the harness keys the
    # label law by rigid name, so this rigid carries a suffix; the page shows
    # "GITHUB REPO" (see plans/codexsiri_wb_notes.md).
    "GITHUB REPO (2)":    ("GITHUB REPO", cx_of(GH2), 258.0, L["FS_KEY"], 26.40,
                           0.28, INK, 31.86),
    "FREE":               ("FREE", 336.0, 204.0, L["FS_TAG"], 27.80, 0.22, INK,
                           31.86),
    "IN THE DESCRIPTION": ("IN THE DESCRIPTION", AX, 296.0, L["FS_KEY"], 29.48,
                           0.36, INK, 31.86),
}


def key_geom(name: str) -> dict:
    text, cx, top, fs, t, d, color, t_to = KEYS[name]
    w = core.text_w(text, fs)
    return {"text": text, "cx": cx, "fs": fs, "t": t, "d": d, "color": color,
            "t_to": t_to, "w": w, "baseline": top + 1.10 * fs,
            "box": (cx - w / 2, top, cx + w / 2, top + fs * 1.55)}


KEY_G = {k: key_geom(k) for k in KEYS}
KEY_TERM = "SIRI SUCKS"

LABEL_PLAN = {
    "sucks":       "SIRI SUCKS",          # THE KEY TERM — first, alone, ABOVE
    "out":         "OUT OF THE BOX",      # below the box
    "repo":        "GITHUB REPO",         # below the GitHub tile (LAW 50 row)
    "codex":       "CODEX",               # below the Codex tile, same row
    "get":         "GET STUFF DONE",      # below the clipboard
    "repo2":       "GITHUB REPO (2)",     # below the second tile, moves with it
    "description": "IN THE DESCRIPTION",  # above the arrow it names
}
COMPARISONS = ()

CONNECTORS = [
    {"to": "github", "end": LINE_A[1], "name": "line-phone-github"},
    {"to": "codex", "end": LINE_B[1], "name": "line-github-codex"},
    {"to": "phone3", "end": LINE_A[0], "name": "charge-a"},
    {"to": "tag", "end": STRING_END, "name": "tag-string"},
]

BLOCKS = (
    ("phone0", "phone0@axis", "bubble0", "mark:siri0", "type:SIRI SUCKS"),
    ("postcard",),
    ("phone2", "box", "mark:siri2", "type:OUT OF THE BOX"),
    ("github", "mark:github", "type:GITHUB REPO"),
    ("codex", "mark:codex", "openai", "mark:openai", "type:CODEX"),
    ("clipboard", "type:GET STUFF DONE"),
    ("github2", "mark:github2", "type:GITHUB REPO (2)",
     "tag", "type:FREE"),
    ("type:IN THE DESCRIPTION", "arrow"),
)
BOARD_ANCHORS = ()

# every cue is pinned to word INDEX **and** word TEXT.
ANCHORS = {
    "start":       (0, "siri"),         # 0.10  the phone
    "sucks":       (1, "sucks"),        # 0.42  the slide + the "?" bubble
    "this":        (15, "this"),        # 4.12  the pointing cue: highlight
    "experience":  (27, "experience"),  # 7.36  the phone is redrawn
    "sobad":       (31, "so"),          # 8.62  the box
    "out":         (33, "out"),         # 9.08  OUT OF THE BOX
    "took":        (39, "took"),        # 10.32 the phone travels left
    "github":      (49, "github"),      # 13.24 the GitHub tile
    "repo":        (50, "repo"),        # 13.60 GITHUB REPO
    "connect":     (54, "connect"),     # 15.00 line phone -> GitHub
    "codex":       (58, "codex"),       # 16.58 the Codex tile
    "openai":      (64, "openai."),     # 18.94 the maker badge
    "this2":       (66, "this"),        # 19.92 the charge, Codex -> GitHub
    "drastically": (67, "drastically"),  # 20.28 the charge, GitHub -> phone
    "improves":    (68, "improves"),    # 20.94 the screen changes hands
    "experience2": (70, "experience"),  # 21.62 the outline goes terracotta
    "siri3":       (72, "siri."),       # 22.76 and back
    "now2":        (73, "now"),         # 23.34 the phone slides to its talk seat
    "communicate": (76, "communicate"),  # 23.74 the talk bubble
    "get":         (79, "get"),         # 24.86 tick 1
    "stuff":       (80, "stuff"),       # 25.40 tick 2
    "done":        (81, "done."),       # 25.68 tick 3
    "this3":       (82, "this"),        # 26.10 the repo tile, inside the erase
    "repo2":       (83, "repo"),        # 26.34 GITHUB REPO again
    "pct":         (85, "100"),         # 27.02 the tile slides, the tag
    "free":        (86, "free"),        # 27.82 FREE
    "description": (93, "description"),  # 29.48 IN THE DESCRIPTION
    "down":        (94, "down"),        # 29.88 the arrow
    "outro":       (101, "now"),        # 31.86 THE OPAQUE RISING SHEET
    "daily":       (114, "day"),        # 34.70 the daily micro-line
}

# ---- the clock --------------------------------------------------------------
ERASE = 0.30
SEAMS = (3.62, 7.30, 10.30, 23.30, 26.10)
T_OUTRO = 31.86


# =============================================================================
# PRIMITIVES — every object is a marker path
# =============================================================================
def closed(pts):
    return list(pts) + [pts[0]]


def circle_pts(cx: float, cy: float, r: float, n: int = 20):
    return [(cx + r * math.cos(2 * math.pi * k / n + 0.3),
             cy + r * math.sin(2 * math.pi * k / n + 0.3)) for k in range(n + 2)]


def rp(box, r: float):
    return rect_points(box[0], box[1], box[2] - box[0], box[3] - box[1], r)


def draw_phone(b, box, t: float, tag: str, *, d: float = 0.30,
               pen: bool = True) -> str:
    """THE PHONE — body with rounded corners, the screen inset, the dynamic
    island and a side button on the LEFT edge (the right edge is where the line
    to GitHub lands).  Silhouette first; four strokes."""
    x0, y0, x1, y1 = box
    body = b.stroke(rp(box, 14.0), t, d * 0.62, width=L["SW_OBJ"],
                    wobble=0.22, seg=13.0, pen=pen, name=f"{tag}-body")
    scr = (x0 + 7.0, y0 + 9.0, x1 - 7.0, y1 - 9.0)
    b.stroke(rp(scr, 8.0), round(t + d * 0.64, 3), d * 0.22,
             width=L["SW_HAIR"], wobble=0.10, seg=12.0, pen=False,
             name=f"{tag}-screen")
    cx = (x0 + x1) / 2
    b.stroke([(cx - 9.0, y0 + 17.0), (cx + 9.0, y0 + 17.0)],
             round(t + d * 0.86, 3), d * 0.07, width=L["SW_DET"] + 1.4,
             wobble=0.04, seg=9.0, pen=False, name=f"{tag}-island")
    b.stroke([(x0 - 2.6, y0 + 40.0), (x0 - 2.6, y0 + 60.0)],
             round(t + d * 0.93, 3), d * 0.07, width=L["SW_DET"], wobble=0.03,
             seg=9.0, pen=False, name=f"{tag}-button")
    return body


def bubble(b, body, t: float, tag: str, *, d: float = 0.20) -> None:
    """A SPEECH BUBBLE with its tail pointing down-left at the phone."""
    x0, y0, x1, y1 = body
    b.stroke(rp(body, 10.0), t, d, width=L["SW_OBJ"] * 0.9, wobble=0.16,
             seg=12.0, pen=True, name=f"{tag}-body")
    b.stroke([(x0 + 10.0, y1 - 1.0), (x0 - 8.0, y1 + 16.0),
              (x0 + 24.0, y1 - 1.0)], round(t + d, 3), 0.06,
             width=L["SW_OBJ"] * 0.9, wobble=0.05, seg=9.0, pen=False,
             name=f"{tag}-tail")


def mark(b, media: dict, key: str, cx: float, cy: float, side: float, t: float,
         eid: str, *, tag: str = "", d: float = 0.26, s0: float = 0.60,
         t_to: float = 1e9):
    """A REGISTRY MARK, in COLOUR, SIZED BY ITS INK.  `mark:` names are
    DECORATIONS under LAW 39 and never host a label."""
    m = MARK_INK[key]
    ink_w = side * math.sqrt(m["aspect"])
    box_w = ink_w * m["img_w"] / m["bbox_w"]
    box_h = box_w * m["img_h"] / m["img_w"]
    dx = -m["off_x"] * box_w / m["img_w"]
    dy = -m["off_y"] * box_h / m["img_h"]
    x = cx - box_w / 2 + dx
    y = cy - box_h / 2 + dy
    b.shape(f'<image id="{eid}" href="{media[key]}" x="{b.u(x)}" y="{b.u(y)}" '
            f'width="{b.u(box_w)}" height="{b.u(box_h)}" opacity="0"/>')
    ink_h = ink_w / m["aspect"]
    box = (cx - ink_w / 2, cy - ink_h / 2, cx + ink_w / 2, cy + ink_h / 2)
    b.ink(box, f"mark:{tag or key}")
    b.pop(eid, t, d, s0)
    b.rigid("box", box, t, t_to, f"mark:{tag or key}")
    return box


def tile(b, media: dict, key: str, box, t: float, mark_t: float, name: str, *,
         t_to: float, register: bool = True) -> None:
    """THE CHART'S TILE, drawn by the marker: 112 frame px, radius 18, the
    detail stroke, the mark's INK at 0.50 of the tile."""
    b.stroke(rp(box, L["TILE_R"]), t, 0.26, width=L["SW_DET"], wobble=0.20,
             seg=12.0, pen=True, name=name)
    if register:
        b.rigid("box", box, round(t + 0.26, 3), t_to, name=name)
    mark(b, media, key, cx_of(box), cy_of(box), L["MARK_INK_SIDE"], mark_t,
         f"mk-{name}", tag=name if name != key else key, t_to=t_to)


def post_card_svg(media: dict) -> str:
    """THE SOURCE POST (LAW 37), pasted as a card in the chart: cream card,
    ink-alpha border, radius 18; avatar, name, handle, X mark; a hairline; the
    post's own five lines; a strip of the video it carried.  No metrics."""
    x, y, w, h = CARD_PX
    parts = [
        f'<rect x="1.5" y="1.5" width="{w - 3:g}" height="{h - 3:g}" rx="18" '
        f'fill="#FFFDF9" stroke="rgba(17,17,17,0.16)" stroke-width="3"/>',
        '<clipPath id="cp-avatar"><rect x="25" y="17" width="48" height="48" '
        'rx="12"/></clipPath>',
        f'<image href="{media["avatar"]}" x="25" y="17" width="48" height="48" '
        'preserveAspectRatio="xMidYMid slice" clip-path="url(#cp-avatar)"/>',
        '<text x="85" y="49" font-family="JetBrains Mono,monospace" '
        'font-weight="700" font-size="22" letter-spacing="1" fill="#141416">'
        'SHARIF SHAMEEM</text>',
        '<text x="299" y="48" font-family="JetBrains Mono,monospace" '
        'font-weight="500" font-size="19" letter-spacing="0.6" '
        'fill="rgba(20,20,22,0.55)">@SHARIFSHAMEEM</text>',
        f'<image href="{media["xlogo"]}" x="{w - 3 - 22 - 34:g}" y="27" '
        'width="28" height="28"/>',
        f'<rect x="25" y="77" width="{w - 6 - 44:g}" height="2" '
        'fill="rgba(20,20,22,0.15)"/>',
    ]
    for i, line in enumerate(POST_LINES):
        base = 3 + POST_TEXT_Y0 + i * POST_LH + 24.5
        parts.append(
            f'<text x="25" y="{base:g}" font-family="JetBrains Mono,monospace" '
            f'font-weight="400" font-size="{POST_FS:g}" fill="#141416" '
            f'xml:space="preserve">{core.esc(line)}</text>')
    sw_, sh, sy = w - 6 - 44, 150.0, 277.0
    img_h = sw_ * 1200.0 / 675.0
    off = 150.0 * sw_ / 675.0
    parts += [
        f'<clipPath id="cp-shot"><rect x="25" y="{sy:g}" width="{sw_:g}" '
        f'height="{sh:g}" rx="10"/></clipPath>',
        f'<image href="{media["poster"]}" x="25" y="{sy - off:.1f}" '
        f'width="{sw_:g}" height="{img_h:.1f}" clip-path="url(#cp-shot)" '
        'preserveAspectRatio="none"/>',
        f'<rect x="25" y="{sy:g}" width="{sw_:g}" height="{sh:g}" rx="10" '
        'fill="none" stroke="rgba(20,20,22,0.15)" stroke-width="2"/>',
    ]
    # the seat is an OUTER group so the rise tween (y 18 -> 0) on the inner
    # group never overwrites the translate.
    return (f'<g transform="translate({x:g},{y:g})"><g id="postcard" '
            f'style="opacity:0">' + "".join(parts) + "</g></g>")


def post_line_boxes() -> list[tuple[float, float, float, float]]:
    """The two claim lines' marker fills, in board units — the scene's own
    geometry (left pad - 6, 0.6 em advance x len + 12, line height - 2)."""
    x, y, _, _ = CARD_PX
    out = []
    for i in (0, 1):
        top = y + 3 + POST_TEXT_Y0 + i * POST_LH + 1
        wid = POST_FS * 0.6 * len(POST_LINES[i]) + 12
        out.append((cb(x + 19), cb(top), cb(x + 19 + wid),
                    cb(top + POST_LH - 2)))
    return out


# =============================================================================
# THE DRAWING — six chapters, five erases, then the sheet
# =============================================================================
def draw(b, a: dict, media: dict) -> list[str]:
    u = b.u
    txt: list[str] = []

    def key(name: str, pen: bool = True) -> str:
        """A written key: JetBrains Mono 700 UPPERCASE, the chart's key face."""
        g = KEY_G[name]
        eid = b.label(g["text"], g["cx"], g["baseline"], g["fs"], g["t"],
                      g["d"], color=g["color"], weight=700,
                      family="JetBrains Mono", register=False, pen=False)
        txt.append(name)
        b.rigid("type", g["box"], g["t"], g["t_to"], f"type:{name}")
        y = g["baseline"] - g["fs"] * 0.40
        if pen:
            b.strokes.append({"t": g["t"], "d": g["d"], "pts": b._pen_pts(
                [(u(g["cx"] - g["w"] / 2), u(y)),
                 (u(g["cx"] + g["w"] / 2), u(y))], g["t"])})
        b.bang(g["t"], "pop")
        return eid

    def travel(sel: str, t: float, d: float, x0: float, x1: float) -> None:
        b.tw.append(f'tl.fromTo("{sel}",{{x:{u(x0):.2f}}},{{x:{u(x1):.2f},'
                    f'duration:{d:.2f},ease:SWING,immediateRender:false}},'
                    f'{t:.2f});')

    def fade(sel: str, t: float, d: float = ERASE) -> None:
        b.swap(sel, t, "opacity:1", "opacity:0", d, ease="SOFT")

    # =====================================================================
    # CHAPTER 0 · 0.10-3.62 — SIRI, ON A PHONE, NOT UNDERSTANDING
    # =====================================================================
    s0, s1, s2, s3, s4 = SEAMS
    b.shape('<g id="ch0">')
    b.shape('<g id="ph0">')
    b.set0(f'tl.set("#ph0",{{x:{u(PH0_DX):.2f}}},0);')
    b.pen_shift, b.pen_shift_until = (u(PH0_DX), 0.0), a["sucks"]
    draw_phone(b, PH0, a["start"], "phone0", d=0.30)
    mark(b, media, "siri", cx_of(PH0), cy_of(PH0), L["SCREEN_MARK"], 0.28,
         "mk-siri0", tag="siri0", t_to=s0)
    b.pen_shift, b.pen_shift_until = (0.0, 0.0), -1.0
    b.shape("</g>")
    b.bang(a["start"], "soft_whoosh")
    ph0c = tuple(v + (PH0_DX if i % 2 == 0 else 0) for i, v in enumerate(PH0))
    b.rigid("box", ph0c, 0.40, round(a["sucks"] + 0.30, 2), name="phone0@axis")
    # 'sucks' — one step left, and Siri does not understand you.
    travel("#ph0", a["sucks"], 0.30, PH0_DX, 0.0)
    b.rigid("box", PH0, round(a["sucks"] + 0.30, 2), s0, name="phone0")
    bubble(b, BUB0, 0.60, "bubble0")
    qx, qy = cx_of(BUB0), cy_of(BUB0)
    b.stroke([(qx - 9.0, qy - 10.0), (qx - 6.0, qy - 18.0), (qx + 1.0, qy - 21.0),
              (qx + 8.0, qy - 17.0), (qx + 9.0, qy - 10.0), (qx + 4.0, qy - 4.0),
              (qx, qy + 1.0), (qx, qy + 8.0)], 0.80, 0.11,
             width=L["SW_OBJ"], wobble=0.05, seg=6.0, pen=True, name="q-hook")
    b.stroke([(qx, qy + 15.0), (qx + 0.4, qy + 17.0)], 0.91, 0.03,
             width=L["SW_OBJ"] + 0.8, wobble=0.02, seg=4.0, pen=False,
             name="q-dot")
    b.rigid("box", BUB0_BOX, 0.95, s0, name="bubble0")
    b.bang(0.60, "pop")
    key("SIRI SUCKS")
    b.shape("</g>")
    fade("#ch0", s0)
    b.bang(s0, "page_turn")

    # =====================================================================
    # CHAPTER 1 · 3.70-7.30 — THE SOURCE POST (LAW 37, cue 'this guy' 4.12)
    # =====================================================================
    b.shape('<g id="ch1">')
    b.shape(post_card_svg(media))
    b.set0('tl.set("#postcard",{opacity:0,y:18},0);')
    b.tw.append('tl.fromTo("#postcard",{opacity:0,y:18},{opacity:1,y:0,'
                'duration:0.36,ease:SOFT,immediateRender:false},3.70);')
    b.ink(CARD_U, "postcard")
    note_asset(b, "postcard")
    b.rigid("box", CARD_U, 3.70, s1, name="postcard")
    b.bang(3.70, "reverse_air")
    # LAW 38 rule 1 — text living in a raster: the marker fill, one per line,
    # wiped left to right on 'This' (4.12) and 4.22.
    highlight_lines(b, post_line_boxes(), a["this"], pad=False,
                    name="post-claim")
    for r in b.rigids[-2:]:
        r["t1"] = s1                          # they leave with the card
    b.bang(a["this"], "tick")
    b.shape("</g>")
    fade("#ch1", s1)
    b.bang(s1, "page_turn")

    # =====================================================================
    # CHAPTER 2 · 7.34-10.30 — STOCK SIRI, STILL IN ITS BOX
    # =====================================================================
    # LAW 45: the phone is redrawn centred INSIDE the erase (7.34-7.60).
    b.shape('<g id="ph2">')
    ph2_body = draw_phone(b, PH2, 7.34, "phone2", d=0.26)
    mark(b, media, "siri", cx_of(PH2), cy_of(PH2), L["SCREEN_MARK"], 7.50,
         "mk-siri2", tag="siri2", t_to=26.10)
    b.shape("</g>")
    b.rigid("box", PH2, 7.60, s2, name="phone2")
    b.bang(7.34, "soft_whoosh")

    b.shape('<g id="ch2">')
    # the box's front panel hides the phone's lower third: a cream occluder (the
    # board's own ground, not a visible fill) rises with the panel's outline.
    fx0, fy0, fx1, fy1 = BOXF
    b.shape(f'<rect id="box-occ" x="{u(fx0)}" y="{u(fy0)}" '
            f'width="{u(fx1 - fx0)}" height="{u(fy1 - fy0)}" '
            f'fill="{core.CREAM}"/>')
    org = f'svgOrigin:"{u(cx_of(BOXF))} {u(fy1)}"'
    b.set0(f'tl.set("#box-occ",{{scaleY:0,{org}}},0);')
    b.tw.append(f'tl.fromTo("#box-occ",{{scaleY:0,{org}}},{{scaleY:1,{org},'
                f'duration:0.20,ease:SOFT,immediateRender:false}},'
                f'{a["sobad"]:.2f});')
    b.stroke(rp(BOXF, 3.0), a["sobad"], 0.26, width=L["SW_OBJ"], wobble=0.22,
             seg=14.0, pen=True, name="box-front")
    b.stroke([(fx0, fy0), (190.0, 262.0), (224.0, 254.0), (PH2[0] - 2.0, fy0)],
             round(a["sobad"] + 0.26, 3), 0.10, width=L["SW_OBJ"] * 0.9,
             wobble=0.10, seg=10.0, pen=True, name="box-flap-l")
    b.stroke([(fx1, fy0), (386.0, 262.0), (352.0, 254.0), (PH2[2] + 2.0, fy0)],
             round(a["sobad"] + 0.36, 3), 0.10, width=L["SW_OBJ"] * 0.9,
             wobble=0.10, seg=10.0, pen=False, name="box-flap-r")
    # the shipping label on the front panel, low right: what makes it a box
    # that came in the post and not a crate.
    b.stroke(rp((316.0, 336.0, 348.0, 358.0), 2.0), round(a["sobad"] + 0.46, 3),
             0.08, width=L["SW_HAIR"], wobble=0.04, seg=8.0, pen=False,
             name="box-label")
    b.stroke([(322.0, 344.0), (342.0, 344.0)], round(a["sobad"] + 0.54, 3),
             0.04, width=L["SW_HAIR"], wobble=0.02, seg=8.0, pen=False,
             name="box-label-line")
    b.rigid("box", BOX_BOX, round(a["sobad"] + 0.46, 3), s2, name="box")
    b.bang(a["sobad"], "low_thump")
    key("OUT OF THE BOX")
    b.shape("</g>")
    # 'took' — the box is wiped while the phone lifts out to the left seat
    # (LAW 45 second method: the anchor object crosses the seam).
    fade("#ch2", s2)
    travel("#ph2", s2, 0.50, 0.0, TRAVEL3)
    b.bang(s2, "page_turn")

    # =====================================================================
    # CHAPTER 3 · 10.30-23.30 — phone — GitHub repo — Codex (by OpenAI)
    # =====================================================================
    b.rigid("box", PH3, round(s2 + 0.50, 2), s3, name="phone3")
    b.shape('<g id="ch3">')
    tile(b, media, "github", GH_BOX, a["github"], round(a["github"] + 0.12, 2),
         "github", t_to=s3)
    b.bang(a["github"], "pop")
    key("GITHUB REPO")
    b.stroke(list(LINE_A), a["connect"], 0.30, width=L["SW_DET"], wobble=0.05,
             seg=14.0, pen=True, name="line-phone-github")
    b.bang(a["connect"], "tick")
    b.stroke(list(LINE_B), 16.28, 0.28, width=L["SW_DET"], wobble=0.05,
             seg=14.0, pen=True, name="line-github-codex")
    tile(b, media, "codex", CX_BOX, a["codex"], round(a["codex"] + 0.12, 2),
         "codex", t_to=s3)
    b.bang(a["codex"], "pop")
    key("CODEX")
    # the maker, under the product: a small drawn badge on the tile's corner.
    b.stroke(closed(circle_pts(*BADGE_C, BADGE_R, 16)), a["openai"], 0.18,
             width=L["SW_HAIR"] + 0.4, wobble=0.10, seg=6.0, pen=True,
             name="openai")
    b.rigid("box", BADGE_BOX, round(a["openai"] + 0.18, 2), s3, name="openai")
    mark(b, media, "openai", *BADGE_C, 12.0, round(a["openai"] + 0.10, 2),
         "mk-openai", tag="openai", t_to=s3)
    b.bang(a["openai"], "tick")
    # THE PEAK — the marker re-traces both lines in terracotta, Codex back to
    # the phone, in two segments that never cross the GitHub mark.
    b.stroke([LINE_B[1], LINE_B[0]], a["this2"], 0.30, color=TERRA,
             width=L["SW_DET"] + 0.8, wobble=0.05, seg=14.0, pen=True,
             name="charge-b")
    b.stroke([LINE_A[1], LINE_A[0]], a["drastically"], 0.28, color=TERRA,
             width=L["SW_DET"] + 0.8, wobble=0.05, seg=14.0, pen=True,
             name="charge-a")
    b.bang(a["this2"], "reverse_air")
    b.shape("</g>")

    # the screen changes hands ('improves'): the Siri mark is scribbled out and
    # the Codex mark is stamped in its place; then the phone's own outline is
    # re-traced in terracotta on 'experience' and let go on 'Siri'.
    b.shape('<g id="phy">')
    sx, sy = cx_of(PH3), cy_of(PH3)
    scrib = [(sx - 15.0 + 30.0 * (k % 2), sy - 15.0 + 5.0 * k) for k in range(7)]
    sc_id = b.stroke(scrib, a["improves"], 0.16, width=L["SW_DET"],
                     wobble=0.05, seg=6.0, pen=True, name="scribble")
    fade(f"#mk-siri2,#{sc_id}", round(a["improves"] + 0.18, 2), 0.14)
    mark(b, media, "codex", sx, sy, L["SCREEN_MARK"],
         round(a["improves"] + 0.28, 2), "mk-codex-scr", tag="codex-scr",
         t_to=26.10)
    b.bang(a["improves"], "pop")
    rt = b.stroke(rp(PH3, 14.0), a["experience2"], 0.40, color=TERRA,
                  width=L["SW_OBJ"] + 0.4, wobble=0.22, seg=13.0, pen=True,
                  name="phone-emph")
    b.body[-1] = b.body[-1].replace(
        "<path ", f'<path data-emphasis="border" data-emphasis-target="{ph2_body}" '
        f'data-check-at="{a["experience2"] + 0.50:.2f}" ', 1)
    fade(f"#{rt}", a["siri3"], 0.24)
    b.bang(a["experience2"], "low_thump")
    b.shape("</g>")
    fade("#ch3", s3)
    travel("#ph2", s3, 0.30, TRAVEL3, TRAVEL3 + TRAVEL4)
    travel("#phy", s3, 0.30, 0.0, TRAVEL4)
    b.bang(s3, "page_turn")

    # =====================================================================
    # CHAPTER 4 · 23.30-26.10 — WHAT THE CODEX PHONE LETS HIM DO
    # =====================================================================
    b.rigid("box", PH4, round(s3 + 0.30, 2), s4, name="phone4")
    b.shape('<g id="ch4">')
    bubble(b, BUB4, a["communicate"], "bubble4", d=0.22)
    for i, (xa, xb) in enumerate(((256.0, 310.0), (256.0, 302.0),
                                  (256.0, 288.0))):
        yy = BUB4[1] + 16.0 + 13.0 * i
        b.stroke([(xa, yy), (xb, yy)], round(a["communicate"] + 0.30 + 0.07 * i,
                                             3), 0.06, width=L["SW_DET"],
                 wobble=0.04, seg=9.0, pen=(i == 0), name=f"talk-line-{i}")
    b.rigid("box", BUB4_BOX, round(a["communicate"] + 0.50, 2), s4,
            name="bubble4")
    b.bang(a["communicate"], "pop")
    tc = 24.46
    b.stroke(rp(CLIP, 6.0), tc, 0.22, width=L["SW_OBJ"], wobble=0.20,
             seg=13.0, pen=True, name="clipboard-body")
    b.stroke(rp((366.0, 206.0, 394.0, 222.0), 4.0), round(tc + 0.22, 3), 0.06,
             width=L["SW_DET"], wobble=0.05, seg=8.0, pen=False,
             name="clipboard-clip")
    for i, ry in enumerate(ROWS_Y):
        t_r = round(tc + 0.28 + 0.03 * i, 3)
        b.stroke(rp((352.0, ry - 6.0, 364.0, ry + 6.0), 2.0), t_r, 0.05,
                 width=L["SW_HAIR"] + 0.4, wobble=0.04, seg=6.0, pen=False,
                 name=f"row-box-{i}")
        b.stroke([(372.0, ry), (408.0 - 6.0 * i, ry)], t_r, 0.05,
                 width=L["SW_HAIR"] + 0.4, wobble=0.04, seg=9.0, pen=False,
                 name=f"row-line-{i}")
    b.rigid("box", CLIP_BOX, round(tc + 0.40, 2), s4, name="clipboard")
    b.bang(tc, "soft_whoosh")
    for i, w in enumerate(("get", "stuff", "done")):
        ry = ROWS_Y[i]
        b.stroke([(353.5, ry - 1.0), (358.0, ry + 4.0), (367.0, ry - 9.0)],
                 a[w], 0.14, color=TERRA, width=L["SW_DET"] + 0.4, wobble=0.03,
                 seg=5.0, pen=True, name=f"tick-{i}")
        b.bang(a[w], "tick")
    key("GET STUFF DONE")
    b.shape("</g>")
    fade("#ch4,#ph2,#phy", s4)
    b.bang(s4, "page_turn")

    # =====================================================================
    # CHAPTER 5 · 26.10-31.86 — THE REPO IS FREE, AND LINKED BELOW
    # =====================================================================
    # LAW 45: the repo tile is drawn centred INSIDE the erase (26.10-26.36).
    b.shape('<g id="ch5">')
    # tile + key are authored at the seat they hold after the 27.02 slide; the
    # group starts 140 frame px right (centred) and travels there as ONE block.
    b.shape('<g id="gh2g">')
    b.pen_shift, b.pen_shift_until = (u(-GH2_DX), 0.0), a["pct"]
    tile(b, media, "github", GH2, a["this3"], round(a["this3"] + 0.12, 2),
         "github2", t_to=31.86, register=False)
    # written by the clip wipe alone: the marker's underline would be judged at
    # the post-slide seat while it is drawn 74.7 u to the right of it.
    key("GITHUB REPO (2)", pen=False)
    b.pen_shift, b.pen_shift_until = (0.0, 0.0), -1.0
    b.shape("</g>")
    # registered at the seat it holds after the slide: nothing else is on this
    # board until the slide has landed, so there is no neighbour to judge.  The
    # "@axis" twin covers the tile's own drawing, centred (a placement).
    b.rigid("box", GH2_C, a["this3"], round(a["this3"] + 0.26, 2),
            name="github2@axis")
    b.rigid("box", GH2, round(a["this3"] + 0.26, 2), T_OUTRO, name="github2")
    b.bang(a["this3"], "pop")
    travel("#gh2g", a["pct"], 0.30, -GH2_DX, 0.0)
    b.set0(f'tl.set("#gh2g",{{x:{u(-GH2_DX):.2f}}},0);')
    # the price tag, drawn after the slide lands
    tx0, ty0, tx1, ty1 = TAG
    tag_pts = [(tx0, cy_of(TAG)), (tx0 + 18.0, ty0), (tx1, ty0), (tx1, ty1),
               (tx0 + 18.0, ty1), (tx0, cy_of(TAG))]
    b.stroke(tag_pts, 27.34, 0.30, width=L["SW_OBJ"], wobble=0.18, seg=12.0,
             pen=True, name="tag")
    b.stroke(closed(circle_pts(*TAG_HOLE, TAG_HOLE_R, 10)), 27.64, 0.05,
             width=L["SW_HAIR"] + 0.2, wobble=0.03, seg=4.0, pen=False,
             name="tag-hole")
    # the connector's target rectangle starts at the punched hole's rim, where
    # the string is tied (LAW 40: the end sits on the target's virtual box).
    b.rigid("box", (STRING_END[0], ty0, tx1, ty1), 27.64, T_OUTRO, name="tag")
    b.stroke([STRING_FROM, (257.0, 227.0), STRING_END], 27.66, 0.10,
             width=L["SW_HAIR"] + 0.4, wobble=0.04, seg=8.0, pen=False,
             name="tag-string")
    b.bang(27.34, "soft_whoosh")
    key("FREE")
    key("IN THE DESCRIPTION")
    ax_, ay0, _, ay1 = ARROW
    b.stroke([(ax_, ay0), (ax_, ay1)], a["down"], 0.22, color=TERRA,
             width=L["SW_DET"] + 0.8, wobble=0.04, seg=12.0, pen=True,
             name="arrow")
    b.stroke([(ax_ - 8.0, ay1 - 10.0), (ax_, ay1 + 1.0), (ax_ + 8.0, ay1 - 10.0)],
             round(a["down"] + 0.22, 3), 0.08, color=TERRA,
             width=L["SW_DET"] + 0.8, wobble=0.03, seg=6.0, pen=False,
             name="arrow-head")
    b.rigid("box", ARROW_BOX, round(a["down"] + 0.30, 2), T_OUTRO, name="arrow")
    b.bang(a["down"], "reverse_air")
    b.shape("</g>")
    # THE SIGN-OFF — the harness's opaque rising sheet.  No ink is authored at
    # or after 31.86: the last mark is the arrow head, done at 30.18.
    b.bang(T_OUTRO, "page_turn")
    return txt


# =============================================================================
# THE PHONE-SIZE BOXES — the plan's four bespoke objects at THIS board's seats
# =============================================================================
PHONE_AT = [
    (1.60, (184.0, 192.0, 392.0, 356.0), "phone with Siri"),
    (9.90, (184.0, 188.0, 392.0, 376.0), "phone in box"),
    (26.00, (334.0, 200.0, 426.0, 328.0), "clipboard with checkmarks"),
    (28.50, (256.0, 190.0, 398.0, 250.0), "free price tag"),
]


def norm_box(box) -> list[float]:
    return [round(px_of(box[0]) / 1080, 4), round(px_of(box[1]) / 1920, 4),
            round(px_of(box[2]) / 1080, 4), round(px_of(box[3]) / 1920, 4)]


def main() -> None:
    project, stats = WB.build(
        vid=VID,
        title="Siri replaced by Codex — whiteboard",
        handle_key="tiktok_ig",
        draw=draw, anchor_spec=ANCHORS,
        outro_key="outro", daily_key="daily",
        marks=MARKS, board_box=BOARD_BOX,
        label_plan=LABEL_PLAN, key_term=KEY_TERM, comparisons=COMPARISONS,
        blocks=BLOCKS, connectors=CONNECTORS, board_anchors=BOARD_ANCHORS)

    stats["captions_law3b"] = CAPTION_REPORT
    stats["seams"] = {"erase_at": list(SEAMS), "erase_s": ERASE,
                      "qc_seams": ",".join(f"{s:g}" for s in SEAMS),
                      "outro_wipe": T_OUTRO}
    stats["phone_test_objects"] = [
        {"name": n, "t": t, "bbox_board_u": list(bx), "bbox_norm": norm_box(bx)}
        for t, bx, n in PHONE_AT]
    stats["phone_at_args"] = [
        f"{t:g}:{','.join(str(v) for v in norm_box(bx))}:{n}"
        for t, bx, n in PHONE_AT]
    out = Path(__file__).resolve().parent / f"_wb_{VID}.json"
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items()
                      if k not in ("anchors", "captions_law3b")}, indent=1))
    print(f"-> {project}")


if __name__ == "__main__":
    main()
