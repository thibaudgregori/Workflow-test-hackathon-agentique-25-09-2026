"""Round 2 — generate 20 distinct static HyperFrames compositions.

10 faceless layouts (F01-F10) + 10 split layouts (S01-S10) per LAYOUTS_R2.md.

Authoring contract (~/.claude/skills/hyperframes-core):
  * clips are DIRECT children of the composition root (no wrapper stages)
  * never tween opacity/scale on a `.clip` for its exit — wrap scene content in an
    inner div, exit-tween the inner and hard-kill it with tl.set
  * <video>/<audio> live at the host root
  * animate only opacity / x / y / scale / rotation / color / backgroundColor
  * exactly one paused GSAP timeline on window.__timelines["main"]

Geometry is authored in the 576x1024 reference space of STYLE_SPEC.md and scaled
by S = 1.875 into the native 1080x1920 canvas at write time.

Connectors: there are NO hand-built logo tile rows anywhere (they caused label
collisions). Every connectors scene uses ui/connectors_panel.png (960x490) which
has the greeting, composer and the four logo tiles baked in with safe spacing.

Faceless safe area: no scene element may extend below y = 770 (design units) —
the caption pill occupies y 795-865.
"""
import json
import shutil
import sys
from pathlib import Path

FACTORY = Path.home() / "Documents/Workspace/projects/personal/content/shorts-factory"
HF_ROOT = FACTORY / "formats/split/source/hyperframes_r2"   # the July projects, frozen 2026-09-20
PUB = FACTORY / "formats/split/source/assets"   # July face plates and UI captures, frozen 2026-09-20; music/sfx come from the Workspace library
TL = json.loads((FACTORY / "pipeline/timeline.json").read_text())

S = 1080 / 576
DUR = TL["duration"]
BEATS = {b["id"]: b for b in TL["beats"]}


def px(v):
    return round(v * S, 1)


# ----------------------------------------------------------------------
# shared tokens
# ----------------------------------------------------------------------
CREAM = "#F0F3EE"
CREAM2 = "#F6F1EA"
DARK = "#101012"
DARK2 = "#17171B"
INK = "#111111"
GRAY = "#8C8C86"
TERRA = "#C66748"
TERRA_L = "#DD7259"
LIME = "#BEED4B"
YELLOW = "#F5A623"
YELLOW_SH = "#C97300"
CAP_TERRA = "#C4573A"

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800'
    "&family=Archivo+Black&family=Montserrat:ital,wght@1,900&family=Nunito:wght@800"
    "&family=Instrument+Serif:ital@0;1&family=Playfair+Display:ital,wght@1,800"
    '&family=Lora:wght@500;600&family=JetBrains+Mono:wght@400;500;700&display=block" rel="stylesheet">'
)
GSAP = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>'

# intrinsic aspect (h/w) of every staged UI capture — used so a screenshot is
# NEVER height-cropped: width is chosen, height always follows the aspect.
UI_ASPECT = {
    "memory_stack.png": 330 / 1600,
    "memory_toggle.png": 144 / 1600,
    "websearch_permission.png": 580 / 1552,
    "websearch_toggle.png": 254 / 1902,
    "projects_modal.png": 792 / 996,
    "thinking_card.png": 464 / 920,
    "connectors_directory.png": 1016 / 2188,
    "models_sheet.png": 502 / 409,
}
UI_FILES = sorted(UI_ASPECT)
UI_VIDS = ["memory", "websearch", "connectors"]  # uivid/<name>.mp4, 12s, 1280x720

FEATURES = [
    dict(key="memory", n=1, num="01", title="Memory", sub="Remembers you",
         word="Memory", ui="memory_stack.png", label="claude.ai · settings",
         app="Claude · Settings"),
    dict(key="websearch", n=2, num="02", title="Web Search", sub="Real-time + sources",
         word="Search", ui="websearch_permission.png", label="claude.ai · web search",
         app="Claude · Web search"),
    dict(key="projects", n=3, num="03", title="Projects", sub="Separate workspaces",
         word="Projects", ui="projects_modal.png", label="claude.ai · projects",
         app="Claude · Projects"),
    dict(key="thinking", n=4, num="04", title="Extended Thinking", sub="Reasons step by step",
         word="Thinking", ui="thinking_card.png", label="claude.ai · thinking",
         app="Claude · Thinking"),
    dict(key="connectors", n=5, num="05", title="Connectors", sub="Plugs into your tools",
         word="Connectors", ui="connectors_directory.png", label="claude.ai · connectors",
         app="Claude · Connectors"),
]
FEAT = {f["key"]: f for f in FEATURES}
FTRACK = {"memory": 3, "websearch": 4, "projects": 5, "thinking": 6, "connectors": 7}
# per-layout screenshot swaps (F06's rail reads as a settings panel, so it keeps
# the web-search settings toggle row instead of the permission card)
UI_OVERRIDE = {("F06", "websearch"): ("websearch_toggle.png", "claude.ai · data sources",
                                      "Claude · Data sources")}


def feat_for(lid, feat):
    ov = UI_OVERRIDE.get((lid, feat["key"]))
    if not ov:
        return feat
    f = dict(feat)
    f["ui"], f["label"], f["app"] = ov
    return f


def fit_ui(ui, max_w, max_h):
    """Largest (w, h) preserving intrinsic aspect that fits the box."""
    a = UI_ASPECT[ui]
    w = min(max_w, max_h / a)
    return round(w, 1), round(w * a, 1)


# ----------------------------------------------------------------------
# audio
# ----------------------------------------------------------------------
SFX_FACELESS = (
    [(0.02, "whoosh", 0.32), (1.55, "boom", 0.4)]
    + [(BEATS[b]["start"], "whoosh", 0.22) for b in
       ["memory", "websearch", "projects", "thinking", "connectors"]]
    + [(BEATS[b]["start"] + 0.1, "pop", 0.32) for b in
       ["memory", "websearch", "projects", "thinking", "connectors"]]
    + [(BEATS["thinking"]["start"] + 1.05, "ding", 0.25)]
    + [(BEATS["freeplan"]["start"] + 0.35, "boom", 0.38),
       (BEATS["freeplan"]["start"] + 1.0, "pop", 0.32),
       (BEATS["cta"]["start"], "whoosh", 0.24),
       (BEATS["cta"]["start"] + 0.28, "boom", 0.4)]
)

SFX_SPLIT = (
    [(0.05, "whoosh", 0.32), (1.9, "boom", 0.36), (5.85, "pop", 0.32), (6.6, "pop", 0.24),
     (6.75, "pop", 0.24), (6.9, "pop", 0.24), (13.9, "pop", 0.32), (20.75, "pop", 0.32),
     (27.95, "pop", 0.32), (30.4, "ding", 0.25), (32.7, "pop", 0.32), (35.2, "click", 0.24),
     (41.4, "pop", 0.32), (44.2, "pop", 0.32), (48.4, "boom", 0.42)]
)


def audio_block(bed, sfx, seed_ms):
    els = [
        f'  <audio id="voA" src="assets/audio_tight.m4a" data-start="0" '
        f'data-duration="{DUR}" data-track-index="20" data-volume="1"></audio>',
        f'  <audio id="bgm" src="assets/music/{bed}" data-start="0" '
        f'data-duration="{DUR}" data-track-index="21" data-volume="0.16"></audio>',
    ]
    for i, (t, name, vol) in enumerate(sfx):
        t2 = max(0.0, t + seed_ms / 1000)
        els.append(
            f'  <audio id="sfx{i}" src="assets/sfx/{name}.mp3" data-start="{t2:.2f}" '
            f'data-duration="1.2" data-track-index="{22 + i}" data-volume="{vol}"></audio>'
        )
    return "\n".join(els)


# ----------------------------------------------------------------------
# captions
# ----------------------------------------------------------------------
def caption_clips_faceless():
    out = []
    for i, c in enumerate(TL["captions_faceless"]):
        d = max(0.08, c["t1"] - c["t0"])
        out.append(
            f'  <div id="cap{i}" class="clip cap" data-start="{c["t0"]}" data-duration="{d:.2f}" '
            f'data-track-index="15"><span class="cappill">{c["text"]}</span></div>'
        )
    return "\n".join(out)


def caption_tweens_faceless():
    return "\n".join(
        f'tl.fromTo("#cap{i} .cappill",{{scale:0.9}},{{scale:1,duration:0.16,ease:"back.out(3)"}},{c["t0"]:.2f});'
        for i, c in enumerate(TL["captions_faceless"])
    )


SPLIT_MODES = [
    ("split", "intro", 0.0, 2.85), ("full", None, 2.85, 5.25),
    ("split", "memory", 5.25, 11.85), ("full", None, 11.85, 13.3),
    ("split", "websearch", 13.3, 18.4), ("full", None, 18.4, 20.15),
    ("split", "projects", 20.15, 25.1), ("full", None, 25.1, 27.35),
    ("split", "thinking", 27.35, 32.1), ("split", "connectors", 32.1, 40.5),
    ("split", "models", 40.5, 47.45), ("full", "cta", 47.45, DUR),
]
SP_TIMES = {"memory": (5.25, 11.85), "websearch": (13.3, 18.4), "projects": (20.15, 25.1),
            "thinking": (27.35, 32.1), "connectors": (32.1, 40.5)}


def split_cap_y(t, seam):
    for typ, scene, t0, t1 in SPLIT_MODES:
        if t0 <= t < t1:
            if typ == "split":
                return seam
            return 643 if scene == "cta" else 735
    return 735


def caption_clips_split(seam):
    out = []
    for i, c in enumerate(TL["captions_split"]):
        d = max(0.1, c["t1"] - c["t0"])
        y = split_cap_y((c["t0"] + c["t1"]) / 2, seam)
        out.append(
            f'  <div id="scap{i}" class="clip scap" style="top:{px(y)}px" data-start="{c["t0"]}" '
            f'data-duration="{d:.2f}" data-track-index="15">'
            f'<span class="scappill">{c["text"]}</span></div>'
        )
    return "\n".join(out)


# ----------------------------------------------------------------------
# tween helpers
# ----------------------------------------------------------------------
def pop(sel, t, d=0.35):
    return f'tl.fromTo("{sel}",{{scale:0}},{{scale:1,duration:{d},ease:POP}},{t:.2f});'


def popo(sel, t, d=0.3, s=0.75):
    return (f'tl.fromTo("{sel}",{{scale:{s},opacity:0}},'
            f'{{scale:1,opacity:1,duration:{d},ease:POP}},{t:.2f});')


def rise(sel, t, dy=26, d=0.38):
    return (f'tl.fromTo("{sel}",{{y:{px(dy)},opacity:0}},'
            f'{{y:0,opacity:1,duration:{d},ease:SOFT}},{t:.2f});')


def drop(sel, t, dy=22, d=0.32):
    return (f'tl.fromTo("{sel}",{{y:{px(-dy)},opacity:0}},'
            f'{{y:0,opacity:1,duration:{d},ease:SOFT}},{t:.2f});')


def slidex(sel, t, dx=-30, d=0.4):
    return (f'tl.fromTo("{sel}",{{x:{px(dx)},opacity:0}},'
            f'{{x:0,opacity:1,duration:{d},ease:SOFT}},{t:.2f});')


def fade(sel, t, d=0.4, to=1):
    return f'tl.fromTo("{sel}",{{opacity:0}},{{opacity:{to},duration:{d},ease:SOFT}},{t:.2f});'


def scene_exit(sid, t1):
    return [
        f'tl.to("#in-{sid}",{{scale:0.92,opacity:0,duration:0.25,ease:"power2.in"}},{t1:.2f});',
        f'tl.set("#in-{sid}",{{opacity:0}},{t1 + 0.28:.2f});',
    ]


def clipsec(sid, t0, t1, body, track):
    return (f'  <section id="sc-{sid}" class="clip scene" data-start="{t0}" '
            f'data-duration="{t1 - t0 + 0.3:.2f}" data-track-index="{track}">\n'
            f'    <div class="inner" id="in-{sid}">{body}</div>\n  </section>')


# ----------------------------------------------------------------------
# card primitives
# ----------------------------------------------------------------------
CHROME_H = 44
LABEL_H = 44


def uiimg(ui, w, h):
    return (f'<img class="uiimg" src="assets/ui/{ui}" alt="" '
            f'style="width:{px(w)}px;height:{px(h)}px"/>')


def _card(cid, head, ui, w, h, left, top, rot, head_h):
    tr = f"transform:rotate({rot}deg);" if rot else ""
    return (f'<div class="abs uicard" id="{cid}" style="left:{px(left)}px;top:{px(top)}px;'
            f'width:{px(w)}px;{tr}">{head}{uiimg(ui, w, h)}</div>'), head_h + h


def card_chrome(cid, ui, w, h, left, top, title, rot=0):
    head = (f'<div class="chromebar"><span class="dot r"></span><span class="dot y"></span>'
            f'<span class="dot g"></span><img class="mini" src="assets/logos/claude.png" alt=""/>'
            f'<span class="ctitle">{title}</span></div>')
    return _card(cid, head, ui, w, h, left, top, rot, CHROME_H)


def card_label(cid, ui, w, h, left, top, label, rot=0):
    return _card(cid, f'<div class="labelbar">{label}</div>', ui, w, h, left, top, rot, LABEL_H)


def card_plain(cid, ui, w, h, left, top, rot=0):
    return _card(cid, "", ui, w, h, left, top, rot, 0)


# ----------------------------------------------------------------------
# shared CSS
# ----------------------------------------------------------------------
def base_css():
    return f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ margin:0; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden;
  font-family:Poppins,sans-serif; }}
.clip {{ position:absolute; }}
.abs {{ position:absolute; }}
.center {{ left:0; width:1080px; text-align:center; }}
.scene {{ inset:0; }}
.inner {{ position:absolute; inset:0; transform-origin:50% 45%; }}
.bgfill {{ inset:0; }}
.uicard {{ background:#FFFFFF; border-radius:{px(14)}px; overflow:hidden;
  box-shadow:0 {px(14)}px {px(34)}px rgba(0,0,0,0.13); }}
.uiimg {{ display:block; }}
.chromebar {{ display:flex; align-items:center; gap:{px(8)}px; height:{px(CHROME_H)}px;
  padding:0 {px(16)}px; border-bottom:1px solid #EEECE6; }}
.dot {{ width:{px(9)}px; height:{px(9)}px; border-radius:50%; display:inline-block;
  flex:none; }}
.dot.r {{ background:#FF5F57; }} .dot.y {{ background:#FEBC2E; }} .dot.g {{ background:#28C840; }}
.mini {{ width:{px(16)}px; height:{px(16)}px; margin-left:{px(6)}px; }}
.ctitle {{ font-weight:600; font-size:{px(17)}px; color:#111; white-space:nowrap; }}
.labelbar {{ height:{px(LABEL_H)}px; display:flex; align-items:center;
  padding:0 {px(18)}px; font-family:'JetBrains Mono',monospace; font-size:{px(18)}px;
  color:#8B8A85; border-bottom:1px solid #F0EEE8; white-space:nowrap; }}
.free3d {{ font-family:Poppins,sans-serif; font-weight:800; text-transform:uppercase;
  color:{YELLOW}; letter-spacing:-0.03em; line-height:1;
  text-shadow:{px(4)}px {px(4)}px 0 {YELLOW_SH}; }}
.serifnum {{ font-family:'Instrument Serif',serif; font-style:italic; line-height:1;
  color:{TERRA_L}; }}
.monolbl {{ font-family:'JetBrains Mono',monospace; letter-spacing:{px(4)}px;
  text-transform:uppercase; }}
"""


# ======================================================================
# FACELESS
# ======================================================================
FL_THEME = {
    "F01": dict(bg=CREAM, ink=INK, sub=GRAY, badge=LIME, badgetxt="#111", align="center"),
    "F02": dict(bg=CREAM, ink=INK, sub=GRAY, badge=LIME, badgetxt="#111", align="top"),
    "F03": dict(bg=CREAM2, ink=INK, sub=GRAY, badge=LIME, badgetxt="#111", align="center"),
    "F04": dict(bg=CREAM, ink=INK, sub=GRAY, badge=LIME, badgetxt="#111", align="panel"),
    "F05": dict(bg=CREAM, ink=INK, sub=GRAY, badge=LIME, badgetxt="#111", align="center"),
    "F06": dict(bg=CREAM2, ink=INK, sub=GRAY, badge=TERRA, badgetxt="#fff", align="top"),
    "F07": dict(bg=DARK, ink="#F4EFE7", sub="#8E8B85", badge=TERRA_L, badgetxt="#fff",
                align="center"),
    "F08": dict(bg=CREAM, ink=INK, sub=GRAY, badge=LIME, badgetxt="#111", align="center"),
    "F09": dict(bg=CREAM2, ink=INK, sub=GRAY, badge=TERRA, badgetxt="#fff", align="center"),
    "F10": dict(bg=CREAM2, ink=INK, sub=GRAY, badge=TERRA, badgetxt="#fff", align="center"),
}
FL_HEAD = {"F01": "chrome", "F02": "label", "F03": "plain", "F04": "label",
           "F05": "chrome", "F06": "label", "F07": "chrome", "F08": "chrome",
           "F09": "label", "F10": "chrome"}

# per-layout max card width for each feature (design units). The connectors
# directory (ratio 0.66) and the web-search permission card (0.37) are tall, so
# their widths are pulled in wherever the slot is short.
FL_MAXW = {
    "F01": dict(memory=516, websearch=516, projects=404, thinking=476, connectors=476),
    "F02": dict(memory=512, websearch=512, projects=360, thinking=512, connectors=512),
    "F04": dict(memory=470, websearch=470, projects=404, thinking=470, connectors=470),
    "F05": dict(memory=500, websearch=500, projects=404, thinking=476, connectors=476),
    "F06": dict(memory=440, websearch=440, projects=400, thinking=440, connectors=440),
    "F07": dict(memory=516, websearch=516, projects=404, thinking=476, connectors=476),
    "F08": dict(memory=490, websearch=490, projects=404, thinking=490, connectors=490),
    "F09": dict(memory=500, websearch=500, projects=360, thinking=500, connectors=500),
    "F10": dict(memory=480, websearch=480, projects=404, thinking=480, connectors=480),
}


def fl_card(lid, cid, feat, w, h, left, top, rot=0):
    kind = FL_HEAD[lid]
    if kind == "chrome":
        return card_chrome(cid, feat["ui"], w, h, left, top, feat["app"], rot)
    if kind == "label":
        return card_label(cid, feat["ui"], w, h, left, top, feat["label"], rot)
    return card_plain(cid, feat["ui"], w, h, left, top, rot)


def fl_titles(k, feat, top, tsize=44, ssize=24, left=None, width=460, align="center"):
    if left is None:
        style = f"left:0;width:1080px;text-align:center;top:{px(top)}px"
    else:
        style = (f"left:{px(left)}px;width:{px(width)}px;text-align:{align};"
                 f"top:{px(top)}px")
    return (f'<div class="abs" id="{k}-tt" style="{style}">'
            f'<div class="fltitle" style="font-size:{px(tsize)}px">{feat["title"]}</div>'
            f'<div class="flsub" style="font-size:{px(ssize)}px">{feat["sub"]}</div></div>')


def fl_scene(lid, feat):
    """Return (html, tweens) for one faceless feature scene."""
    k = feat["key"]
    beat = BEATS[k]
    t0, t1 = beat["start"], beat["end"]
    idx = feat["n"] - 1
    rot = [-2, 2, -2, 2, -1.5][idx]
    cid = f"{k}-card"
    H, tw = [], []

    def badge(left, top, rotd=3):
        H.append(f'<div class="abs flbadge" id="{k}-badge" style="left:{px(left)}px;'
                 f'top:{px(top)}px;transform:rotate({rotd}deg)">#{feat["n"]}</div>')
        tw.append(pop(f"#{k}-badge", t0 + 0.22, 0.3))

    def titles(top, **kw):
        H.append(fl_titles(k, feat, top, **kw))
        tw.append(rise(f"#{k}-tt .fltitle", t0 + 0.33))
        tw.append(rise(f"#{k}-tt .flsub", t0 + 0.44))

    mw = FL_MAXW.get(lid, {}).get(k, 470)

    # ---------------- F01 Reference Pro / F07 Dark Mode ----------------
    if lid in ("F01", "F07"):
        sgn = 1 if lid == "F01" else -1
        w, h = fit_ui(feat["ui"], mw, 344)
        _, ch = fl_card(lid, cid, feat, w, h, 0, 0)
        top = 386 - ch / 2
        c, _ = fl_card(lid, cid, feat, w, h, (576 - w) / 2, top, rot * sgn)
        H.append(c)
        tw.append(pop(f"#{cid}", t0 + 0.1))
        badge((576 - w) / 2 - 18, top - 34, 3 * sgn)
        titles(600)

    # ---------------- F02 Headline Top ----------------
    elif lid == "F02":
        H.append(f'<div class="abs monolbl flkicker" id="{k}-kick" '
                 f'style="left:{px(56)}px;top:{px(122)}px;font-size:{px(17)}px">'
                 f'Feature {feat["num"]}</div>')
        H.append(f'<div class="abs serifnum" id="{k}-num" style="left:{px(52)}px;'
                 f'top:{px(150)}px;font-size:{px(118)}px">{feat["num"]}</div>')
        H.append(f'<div class="abs flbig" id="{k}-big" style="left:{px(56)}px;'
                 f'top:{px(288)}px;width:{px(470)}px">{feat["title"]}</div>')
        H.append(f'<div class="abs flsub" id="{k}-sb" style="left:{px(56)}px;top:{px(356)}px;'
                 f'width:{px(470)}px;font-size:{px(24)}px">{feat["sub"]}</div>')
        tw += [slidex(f"#{k}-kick", t0 + 0.08, -20, 0.3), slidex(f"#{k}-num", t0 + 0.14, -26),
               rise(f"#{k}-big", t0 + 0.34), rise(f"#{k}-sb", t0 + 0.5)]
        w, h = fit_ui(feat["ui"], mw, 302)
        _, ch = fl_card(lid, cid, feat, w, h, 0, 0)
        top = min(762 - ch, max(444, 606 - ch / 2))
        c, _ = fl_card(lid, cid, feat, w, h, (576 - w) / 2, top)
        H.append(c)
        tw.append(rise(f"#{cid}", t0 + 0.2, 46, 0.45))

    # ---------------- F03 Phone Frame ----------------
    elif lid == "F03":
        PL, PT, PW, PH = 98, 84, 380, 552
        SIW, SIH = PW - 28, PH - 28
        w, h = fit_ui(feat["ui"], SIW, SIH - 40)
        H.append(f'<div class="abs center flchip" id="{k}-chip" style="top:{px(22)}px">'
                 f'<span>#{feat["n"]} · {feat["title"]}</span></div>')
        H.append(
            f'<div class="abs phone" id="{k}-ph" style="left:{px(PL)}px;top:{px(PT)}px;'
            f'width:{px(PW)}px;height:{px(PH)}px">'
            f'<div class="phscreen" style="left:{px(14)}px;top:{px(14)}px;'
            f'width:{px(SIW)}px;height:{px(SIH)}px"><div class="phnotch"></div>'
            f'<div class="abs" style="left:{px((SIW - w) / 2)}px;top:{px((SIH - h) / 2)}px">'
            f'{uiimg(feat["ui"], w, h)}</div></div></div>')
        titles(660, tsize=42, ssize=23)
        tw += [drop(f"#{k}-chip", t0 + 0.08, 18, 0.3), popo(f"#{k}-ph", t0 + 0.14, 0.42, 0.86)]

    # ---------------- F04 Split Canvas ----------------
    elif lid == "F04":
        H.append(f'<div class="abs serifnum" id="{k}-num" style="left:{px(360)}px;'
                 f'width:{px(160)}px;text-align:right;top:{px(60)}px;font-size:{px(104)}px">'
                 f'{feat["num"]}</div>')
        H.append(f'<div class="abs fltitle onDark" id="{k}-t" style="left:{px(56)}px;'
                 f'width:{px(292)}px;top:{px(108)}px;font-size:{px(42)}px">{feat["title"]}</div>')
        H.append(f'<div class="abs flsub onDark" id="{k}-s" style="left:{px(56)}px;'
                 f'width:{px(292)}px;top:{px(232)}px;font-size:{px(23)}px">{feat["sub"]}</div>')
        tw += [drop(f"#{k}-num", t0 + 0.1, 18, 0.35), slidex(f"#{k}-t", t0 + 0.2, -24),
               slidex(f"#{k}-s", t0 + 0.32, -24)]
        w, h = fit_ui(feat["ui"], mw, 400)
        _, ch = fl_card(lid, cid, feat, w, h, 0, 0)
        top = max(320, min(762 - ch, 470 - ch / 2))
        c, _ = fl_card(lid, cid, feat, w, h, (576 - w) / 2, top)
        H.append(c)
        tw.append(popo(f"#{cid}", t0 + 0.22, 0.42, 0.8))

    # ---------------- F05 Big Number Ghost ----------------
    elif lid == "F05":
        H.append(f'<div class="abs center ghostnum" id="{k}-gn" style="top:{px(160)}px;'
                 f'font-size:{px(360)}px">{feat["num"]}</div>')
        tw.append(popo(f"#{k}-gn", t0 + 0.04, 0.5, 0.86))
        w, h = fit_ui(feat["ui"], mw, 380)
        _, ch = fl_card(lid, cid, feat, w, h, 0, 0)
        c, _ = fl_card(lid, cid, feat, w, h, (576 - w) / 2, 398 - ch / 2)
        H.append(c)
        tw.append(pop(f"#{cid}", t0 + 0.14))
        titles(640)

    # ---------------- F06 Sidebar Rail ----------------
    elif lid == "F06":
        dots = "".join(
            f'<div class="raildot{" on" if i == idx else ""}">'
            f'<span>{FEATURES[i]["num"]}</span></div>' for i in range(5))
        H.append(f'<div class="abs raillist" id="{k}-rail" style="top:{px(300)}px">{dots}</div>')
        H.append(f'<div class="abs fltitle" id="{k}-t" style="left:{px(104)}px;'
                 f'width:{px(440)}px;top:{px(118)}px;font-size:{px(42)}px">{feat["title"]}</div>')
        H.append(f'<div class="abs flsub" id="{k}-s" style="left:{px(104)}px;'
                 f'width:{px(440)}px;top:{px(186)}px;font-size:{px(24)}px">{feat["sub"]}</div>')
        tw += [fade(f"#{k}-rail", t0 + 0.05, 0.3), slidex(f"#{k}-t", t0 + 0.16, -26),
               slidex(f"#{k}-s", t0 + 0.28, -26)]
        w, h = fit_ui(feat["ui"], mw, 400)
        _, ch = fl_card(lid, cid, feat, w, h, 0, 0)
        top = max(266, min(760 - ch, 486 - ch / 2))
        c, _ = fl_card(lid, cid, feat, w, h, 104 + (440 - w) / 2, top)
        H.append(c)
        tw.append(rise(f"#{cid}", t0 + 0.34, 40, 0.45))

    # ---------------- F08 Spotlight Zoom ----------------
    elif lid == "F08":
        gw = 1000.0
        gh = round(gw * UI_ASPECT[feat["ui"]], 1)
        H.append(f'<div class="abs ghostwrap" id="{k}-gw" '
                 f'style="left:{px((576 - gw) / 2)}px;top:{px((1024 - gh) / 2)}px">'
                 f'{uiimg(feat["ui"], gw, gh)}</div>')
        H.append('<div class="abs bgfill scrim"></div>')
        H.append(f'<div class="abs center" id="{k}-chip2" style="top:{px(112)}px">'
                 f'<span class="flchip2">{feat["label"]}</span></div>')
        tw += [fade(f"#{k}-gw", t0 + 0.02, 0.5, to=0.14),
               drop(f"#{k}-chip2", t0 + 0.1, 16, 0.3)]
        w, h = fit_ui(feat["ui"], mw, 352)
        _, ch = fl_card(lid, cid, feat, w, h, 0, 0)
        c, _ = fl_card(lid, cid, feat, w, h, (576 - w) / 2, 416 - ch / 2)
        H.append(c)
        tw.append(popo(f"#{cid}", t0 + 0.2, 0.42, 0.7))
        titles(646)

    # ---------------- F09 Checklist Build ----------------
    elif lid == "F09":
        H.append(f'<div class="abs center flkicker2" id="{k}-kk" style="top:{px(108)}px">'
                 f'The free plan</div>')
        rows = "".join(
            f'<div class="ckrow{" on" if i <= idx else ""}" id="{k}-ck{i}">'
            f'<span class="ckbox">✓</span><span class="cktx">{FEATURES[i]["title"]}</span></div>'
            for i in range(5))
        H.append(f'<div class="abs cklist" id="{k}-list" style="left:{px(48)}px;'
                 f'top:{px(158)}px;width:{px(480)}px">{rows}</div>')
        tw += [fade(f"#{k}-kk", t0 + 0.05, 0.3), fade(f"#{k}-list", t0 + 0.08, 0.28),
               popo(f"#{k}-ck{idx}", t0 + 0.3, 0.32, 0.94)]
        w, h = fit_ui(feat["ui"], mw, 296)
        _, ch = fl_card(lid, cid, feat, w, h, 0, 0)
        top = min(758 - ch, max(460, 606 - ch / 2))
        c, _ = fl_card(lid, cid, feat, w, h, (576 - w) / 2, top)
        H.append(c)
        tw.append(rise(f"#{cid}", t0 + 0.42, 40, 0.45))

    # ---------------- F10 Editorial Serif ----------------
    else:
        H.append(f'<div class="abs monolbl flkicker" id="{k}-kick" style="left:{px(56)}px;'
                 f'top:{px(116)}px;font-size:{px(17)}px">Feature {feat["num"]}</div>')
        H.append(f'<div class="abs edword" id="{k}-w" style="left:{px(52)}px;top:{px(146)}px;'
                 f'width:{px(470)}px;font-size:{px(96)}px">{feat["word"]}</div>')
        H.append(f'<div class="abs edrule" id="{k}-r" style="left:{px(56)}px;top:{px(278)}px;'
                 f'width:{px(180)}px"></div>')
        H.append(f'<div class="abs flsub" id="{k}-s" style="left:{px(56)}px;top:{px(300)}px;'
                 f'width:{px(420)}px;font-size:{px(24)}px">{feat["sub"]}</div>')
        tw += [slidex(f"#{k}-kick", t0 + 0.06, -18, 0.3), rise(f"#{k}-w", t0 + 0.16, 28, 0.42),
               fade(f"#{k}-r", t0 + 0.34, 0.3), rise(f"#{k}-s", t0 + 0.42)]
        w, h = fit_ui(feat["ui"], mw, 386)
        _, ch = fl_card(lid, cid, feat, w, h, 0, 0)
        top = min(758 - ch, max(376, 574 - ch / 2))
        c, _ = fl_card(lid, cid, feat, w, h, 536 - w, top, 2.5)
        H.append(c)
        tw.append(rise(f"#{cid}", t0 + 0.3, 44, 0.48))

    tw += scene_exit(k, t1)
    return clipsec(k, t0, t1, "\n      ".join(H), FTRACK[k]), tw


def fl_hook_cta(lid):
    """Hook, free-plan and CTA — identical copy, arrangement varies by layout."""
    al = FL_THEME[lid]["align"]
    hk, fp, ct = BEATS["hook"], BEATS["freeplan"], BEATS["cta"]
    tw = []
    dk = lid in ("F04", "F07")

    if al == "top":
        hy = dict(logo=176, l1=286, l2=330, free=392, sub=524)
        fy = dict(l1=104, free=158, l2=272, card=364)
        cy = dict(l1=220, free=288, sub=422)
    elif al == "panel":
        hy = dict(logo=104, l1=196, l2=240, free=520, sub=660)
        fy = dict(l1=120, free=174, l2=288, card=400)
        cy = dict(l1=170, free=224, sub=356)
    else:
        hy = dict(logo=340, l1=444, l2=488, free=548, sub=676)
        fy = dict(l1=132, free=186, l2=300, card=396)
        cy = dict(l1=400, free=468, sub=602)

    # hook: on F04 the two lines sit inside the dark top panel, FREE in the cream half
    hl = " onDark" if dk else ""
    hs = " onDark" if lid == "F07" else ""
    hook = f"""
      <div class="abs center" id="hk-logo" style="top:{px(hy['logo'])}px">
        <img src="assets/logos/claude.png" alt="" style="width:{px(76)}px;height:{px(76)}px"/></div>
      <div class="abs center hkline{hl}" id="hk-l1" style="top:{px(hy['l1'])}px">Claude just gave away</div>
      <div class="abs center hkline{hl}" id="hk-l2" style="top:{px(hy['l2'])}px">almost <b>everything</b></div>
      <div class="abs center free3d" id="hk-free" style="top:{px(hy['free'])}px;font-size:{px(116)}px">FREE</div>
      <div class="abs center flsub{hs}" id="hk-sub" style="top:{px(hy['sub'])}px;font-size:{px(22)}px">without paying a single dollar</div>"""
    tw += [
        pop("#hk-logo", 0.05, 0.32),
        'tl.fromTo("#hk-logo img",{rotation:0},{rotation:234,duration:5.2,ease:"none"},0);',
        drop("#hk-l1", 0.55, 20, 0.25), drop("#hk-l2", 0.75, 20, 0.25),
        'tl.fromTo("#hk-free",{scale:0},{scale:1,duration:0.4,ease:"back.out(1.9)"},1.55);',
        fade("#hk-sub", 2.2, 0.35),
    ] + scene_exit("hook", hk["end"])

    fl = " onDark" if dk else ""
    # real "Select model" sheet (409x502) — never a mock picker
    MW = 250.0
    MH = round(MW * UI_ASPECT["models_sheet.png"], 1)
    fpl = f"""
      <div class="abs center hkline{fl}" id="fp-l1" style="top:{px(fy['l1'])}px">All on the</div>
      <div class="abs center free3d" id="fp-free" style="top:{px(fy['free'])}px;font-size:{px(96)}px">FREE</div>
      <div class="abs center hkline{fl}" id="fp-l2" style="top:{px(fy['l2'])}px">plan</div>
      <div class="abs uicard" id="fp-card" style="left:{px((576 - MW) / 2)}px;top:{px(fy['card'])}px;width:{px(MW)}px">
        {uiimg("models_sheet.png", MW, MH)}
      </div>"""
    tw += [
        fade("#fp-l1", fp["start"] + 0.05, 0.3),
        f'tl.fromTo("#fp-free",{{scale:0}},{{scale:1,duration:0.4,ease:"back.out(1.9)"}},{fp["start"] + 0.35:.2f});',
        fade("#fp-l2", fp["start"] + 0.62, 0.3),
        f'tl.fromTo("#fp-card",{{y:{px(80)},scale:0.66,opacity:0}},'
        f'{{y:0,scale:1,opacity:1,duration:0.42,ease:POP}},{fp["start"] + 1.0:.2f});',
    ] + scene_exit("fp", fp["end"])

    cl = " onDark" if dk else ""
    cta = f"""
      <div class="abs center hkline{cl}" id="cta-l1" style="top:{px(cy['l1'])}px;font-size:{px(36)}px">Comment</div>
      <div class="abs center ctafree" id="cta-free" style="top:{px(cy['free'])}px;font-size:{px(86)}px">&ldquo;FREE&rdquo;</div>
      <div class="abs center flsub{cl}" id="cta-sub" style="top:{px(cy['sub'])}px;font-size:{px(22)}px">and I&rsquo;ll send you the link</div>"""
    tw += [
        drop("#cta-l1", ct["start"] + 0.05, 18, 0.25),
        f'tl.fromTo("#cta-free",{{scale:0}},{{scale:1,duration:0.42,ease:"back.out(1.9)"}},{ct["start"] + 0.3:.2f});',
        fade("#cta-sub", ct["start"] + 0.75, 0.35),
    ]
    html = "\n".join([clipsec("hook", 0.0, hk["end"], hook, 2),
                      clipsec("fp", fp["start"], fp["end"], fpl, 8),
                      clipsec("cta", ct["start"], DUR - 0.3, cta, 9)])
    return html, tw


def fl_chrome(lid):
    """Persistent background / structural chrome as a track-0 clip."""
    th = FL_THEME[lid]
    body = f'<div class="abs bgfill" style="background:{th["bg"]}"></div>'
    if lid == "F04":
        body += (f'<div class="abs" style="left:0;top:0;width:1080px;height:{px(460)}px;'
                 f'background:{DARK2}"></div>')
    if lid == "F06":
        body += (f'<div class="abs" style="left:0;top:0;width:{px(72)}px;height:1920px;'
                 f'background:{DARK2}"></div>')
    if lid == "F10":
        body += (f'<div class="abs" style="left:{px(56)}px;top:{px(94)}px;width:{px(464)}px;'
                 f'height:{px(3)}px;background:rgba(198,103,72,0.30)"></div>')
    return (f'  <div id="chrome" class="clip" data-start="0" data-duration="{DUR}" '
            f'data-track-index="0" style="inset:0">{body}</div>')


def faceless_css(lid):
    th = FL_THEME[lid]
    return base_css() + f"""
.hkline {{ font-weight:600; font-size:{px(34)}px; color:{th['ink']}; }}
.hkline b {{ font-weight:800; }}
.hkline.onDark {{ color:#F6F1EA; }}
.fltitle {{ font-weight:700; color:{th['ink']}; line-height:1.18; }}
.fltitle.onDark {{ color:#F6F1EA; }}
.flsub {{ font-weight:500; color:{th['sub']}; margin-top:{px(4)}px; line-height:1.3; }}
.flsub.onDark {{ color:#A9A6A0; }}
.flbadge {{ background:{th['badge']}; color:{th['badgetxt']}; font-weight:800;
  font-size:{px(34)}px; padding:{px(6)}px {px(20)}px; border-radius:{px(12)}px;
  box-shadow:0 {px(4)}px {px(10)}px rgba(0,0,0,0.25); }}
.flkicker {{ font-weight:600; color:{TERRA}; }}
.flkicker2 {{ font-family:'JetBrains Mono',monospace; font-size:{px(20)}px;
  letter-spacing:{px(5)}px; text-transform:uppercase; color:{TERRA}; }}
.flbig {{ font-weight:800; font-size:{px(52)}px; color:{th['ink']}; line-height:1.05; }}
.modelcard {{ background:#FBFAF6; border-radius:{px(14)}px; overflow:hidden;
  box-shadow:0 {px(14)}px {px(34)}px rgba(0,0,0,0.13); }}
.mrow {{ display:flex; justify-content:space-between; align-items:center;
  padding:{px(14)}px {px(22)}px; }}
.mrow.sel {{ background:#ECEADD; }}
.mname {{ font-weight:700; font-size:{px(26)}px; color:#111; }}
.mrow.off .mname {{ color:#BBB9B2; }}
.mchk {{ width:{px(24)}px; height:{px(24)}px; border-radius:50%; background:#3FA452;
  color:#fff; font-size:{px(15)}px; font-weight:700; display:flex; align-items:center;
  justify-content:center; }}
.mfree {{ background:#4CD44C; color:#fff; font-weight:700; font-size:{px(17)}px;
  border-radius:{px(9)}px; padding:{px(4)}px {px(12)}px; }}
.ctafree {{ font-family:Montserrat,sans-serif; font-style:italic; font-weight:900;
  background:linear-gradient(135deg,#D45CC0 0%,#B6339D 55%,#9C2386 100%);
  -webkit-background-clip:text; background-clip:text; color:transparent; }}
.flchip span {{ display:inline-block; background:{th['badge']}; color:{th['badgetxt']};
  border-radius:{px(20)}px; padding:{px(8)}px {px(22)}px; font-weight:700;
  font-size:{px(22)}px; }}
/* F03 phone */
.phone {{ background:{DARK}; border-radius:{px(54)}px;
  box-shadow:0 {px(22)}px {px(48)}px rgba(0,0,0,0.24); }}
.phscreen {{ position:absolute; background:#FBFAF6; border-radius:{px(42)}px; overflow:hidden; }}
.phnotch {{ position:absolute; left:50%; top:{px(12)}px; width:{px(96)}px; height:{px(14)}px;
  border-radius:{px(9)}px; background:rgba(17,17,17,0.12); margin-left:{px(-48)}px; }}
/* F05 ghost number */
.ghostnum {{ font-family:'Instrument Serif',serif; font-style:italic; line-height:0.9;
  color:rgba(17,17,17,0.075); }}
/* F06 rail */
.raillist {{ left:0; width:{px(72)}px; display:flex; flex-direction:column;
  align-items:center; gap:{px(26)}px; }}
.raildot {{ width:{px(40)}px; height:{px(40)}px; border-radius:50%;
  background:rgba(255,255,255,0.10); display:flex; align-items:center;
  justify-content:center; font-family:'JetBrains Mono',monospace; font-size:{px(15)}px;
  color:#6E6C68; }}
.raildot.on {{ background:{TERRA}; color:#fff; }}
/* F08 spotlight */
.ghostwrap {{ opacity:0; }}
.scrim {{ background:{th['bg']}; opacity:0.60; }}
.flchip2 {{ display:inline-block; background:#fff; border-radius:{px(22)}px;
  padding:{px(9)}px {px(22)}px; font-family:'JetBrains Mono',monospace;
  font-size:{px(18)}px; color:#6E6C68; box-shadow:0 {px(8)}px {px(20)}px rgba(0,0,0,0.10); }}
/* F09 checklist */
.cklist {{ display:flex; flex-direction:column; gap:{px(6)}px; }}
.ckrow {{ display:flex; align-items:center; gap:{px(14)}px; padding:{px(9)}px {px(18)}px;
  border-radius:{px(12)}px; background:rgba(17,17,17,0.03); }}
.ckrow.on {{ background:#FFFFFF; box-shadow:0 {px(6)}px {px(16)}px rgba(0,0,0,0.07); }}
.ckbox {{ width:{px(28)}px; height:{px(28)}px; border-radius:{px(9)}px; background:#DDDCD6;
  color:#fff; font-weight:700; font-size:{px(17)}px; display:flex; align-items:center;
  justify-content:center; flex:none; }}
.ckrow.on .ckbox {{ background:{TERRA}; }}
.cktx {{ font-weight:600; font-size:{px(23)}px; color:#B4B2AB; }}
.ckrow.on .cktx {{ color:#111; }}
/* F10 editorial */
.edword {{ font-family:'Instrument Serif',serif; font-style:italic; color:{th['ink']};
  line-height:1; }}
.edrule {{ height:{px(4)}px; background:{TERRA}; }}
/* captions */
.cap {{ top:{px(795)}px; left:0; width:1080px; text-align:center; }}
.cappill {{ display:inline-block; background:#141716; color:#fff; font-weight:600;
  font-size:{px(30)}px; padding:{px(14)}px {px(26)}px; border-radius:{px(14)}px;
  border:1px solid rgba(255,255,255,0.10); }}
"""


def faceless_html(lid):
    scenes, tws = [], []
    for f in FEATURES:
        h, t = fl_scene(lid, feat_for(lid, f))
        scenes.append(h)
        tws += t
    hc_html, hc_tw = fl_hook_cta(lid)
    tws += hc_tw
    tws.append(f'tl.to("#bgm",{{volume:0,duration:1.5}},{DUR - 1.6:.2f});')
    seed = -10 + (int(lid[1:]) - 1) * 4
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=1080, height=1920"/>
<title>Abik Faceless R2 {lid}</title>
{GSAP}
{FONTS}
<style>
{faceless_css(lid)}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920"
     data-duration="{DUR}" data-fps="30">

{fl_chrome(lid)}

{hc_html}

{chr(10).join(scenes)}

{caption_clips_faceless()}

{audio_block("bed_faceless.mp3", SFX_FACELESS, seed)}
</div>

<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
const POP = "back.out(2.4)";
const SOFT = "power3.out";
{chr(10).join(tws)}
{caption_tweens_faceless()}
window.__timelines["main"] = tl;
</script>
</body>
</html>"""


# ======================================================================
# SPLIT
# ======================================================================
SP_THEME = {
    "S01": dict(seam=460, tone="alt"),
    "S02": dict(seam=564, tone="alt"),
    "S03": dict(seam=460, tone="dark"),
    "S04": dict(seam=460, tone="dark"),
    "S05": dict(seam=460, tone="cream"),
    "S06": dict(seam=460, tone="alt2"),
    "S07": dict(seam=460, tone="dark"),
    "S08": dict(seam=460, tone="cream"),
    "S09": dict(seam=460, tone="dark"),
    "S10": dict(seam=460, tone="alt2"),
}
ALT_BG = {"intro": "dark", "memory": "cream", "websearch": "dark", "projects": "cream",
          "thinking": "dark", "connectors": "dark", "models": "cream"}
ALT2_BG = {"intro": "dark", "memory": "cream", "websearch": "cream", "projects": "dark",
           "thinking": "dark", "connectors": "cream", "models": "cream"}


def sp_bg(lid, scene):
    tone = SP_THEME[lid]["tone"]
    if tone == "dark":
        return "dark"
    if tone == "cream":
        return "dark" if scene == "intro" else "cream"
    if tone == "alt2":
        return ALT2_BG[scene]
    return ALT_BG[scene]


def sp_zone(lid, sid, t0, t1, scene, body, track):
    seam = SP_THEME[lid]["seam"]
    top = seam if seam != 460 else 0
    return (f'  <section id="tz-{sid}" class="clip tz {sp_bg(lid, scene)}" '
            f'style="top:{px(top)}px;height:{px(460)}px" data-start="{t0}" '
            f'data-duration="{t1 - t0:.2f}" data-track-index="{track}">\n    {body}\n  </section>')


def sp_header(k, num, title, x, y, dark, nsize=64, tsize=34):
    return (f'<div class="abs shead" id="{k}-head" style="left:{px(x)}px;top:{px(y)}px">'
            f'<span class="serifnum" style="font-size:{px(nsize)}px">{num}</span>'
            f'<span class="stitle{" onDark" if dark else ""}" '
            f'style="font-size:{px(tsize)}px">{title}</span></div>')


SP_MAXW = {
    "S01": dict(memory=500, websearch=512, projects=296, thinking=500, connectors=500),
    "S02": dict(memory=512, websearch=520, projects=306, thinking=500, connectors=500),
    "S04": dict(memory=520, websearch=520, projects=316, thinking=520, connectors=520),
    "S06": dict(memory=500, websearch=512, projects=292, thinking=480, connectors=480),
    "S07": dict(memory=476, websearch=476, projects=276, thinking=476, connectors=476),
    "S10": dict(memory=520, websearch=520, projects=302, thinking=500, connectors=500),
}
# S04 uses its side-column poster variant for the tall projects modal
S04_SIDE = ("projects",)


def sp_scene(lid, feat):
    """Return (zone_html, tweens, root_extra) for one split feature scene.

    Coordinates are zone-local (0..460); the zone clip is offset by the seam.
    `root_extra` carries host-root elements (UI demo <video>s and their overlay
    clips) that cannot live inside the zone clip.
    """
    k = feat["key"]
    t0, t1 = SP_TIMES[k]
    dark = sp_bg(lid, k) == "dark"
    H, tw, root = [], [], []
    cid = f"{k}-card"
    mw = SP_MAXW.get(lid, {}).get(k, 460)

    # ---- S01 Reference Pro
    if lid == "S01":
        H.append(sp_header(k, feat["num"], feat["title"], 52, 62, dark))
        tw.append(rise(f"#{k}-head", t0 + 0.1, 30, 0.4))
        box_h = 240 if k == "memory" else 256
        w, h = fit_ui(feat["ui"], mw, box_h - LABEL_H)
        ch = LABEL_H + h
        c, _ = card_label(cid, feat["ui"], w, h, (576 - w) / 2,
                          150 if k == "memory" else 150 + (box_h - ch) / 2, feat["label"])
        H.append(c)
        tw.append(rise(f"#{cid}", t0 + 0.6, 50, 0.5))
        if k == "memory":
            H.append(f'<div class="abs pillrow" id="{k}-pills" style="top:{px(332)}px">'
                     f'<span class="spill" id="{k}-p0">preferences</span>'
                     f'<span class="spill" id="{k}-p1">projects</span>'
                     f'<span class="spill" id="{k}-p2">conversations</span></div>')
            for i in range(3):
                tw.append(popo(f"#{k}-p{i}", t0 + 1.35 + i * 0.15, 0.25, 0.8))

    # ---- S02 Inverted (content zone is the BOTTOM half; local coords 0..460)
    elif lid == "S02":
        H.append(sp_header(k, feat["num"], feat["title"], 52, 54, dark, nsize=58, tsize=32))
        tw.append(rise(f"#{k}-head", t0 + 0.1, 26, 0.4))
        w, h = fit_ui(feat["ui"], mw, 292 - LABEL_H)
        ch = LABEL_H + h
        c, _ = card_label(cid, feat["ui"], w, h, (576 - w) / 2, 138 + (292 - ch) / 2,
                          feat["label"])
        H.append(c)
        tw.append(rise(f"#{cid}", t0 + 0.6, 44, 0.5))

    # ---- S03 Full-bleed UI
    elif lid == "S03":
        w, h = fit_ui(feat["ui"], 576, 440)
        H.append(f'<div class="abs" id="{cid}" style="left:{px((576 - w) / 2)}px;'
                 f'top:{px((460 - h) / 2)}px">{uiimg(feat["ui"], w, h)}</div>')
        H.append('<div class="abs s3scrim"></div>')
        H.append(f'<div class="abs monolbl s3lbl" id="{k}-lbl" style="left:{px(46)}px;'
                 f'top:{px(38)}px;font-size:{px(16)}px">{feat["label"]}</div>')
        H.append(f'<div class="abs serifnum s3num" id="{k}-n" style="left:{px(46)}px;'
                 f'top:{px(292)}px;font-size:{px(50)}px">{feat["num"]}</div>')
        H.append(f'<div class="abs s3t" id="{k}-t" style="left:{px(46)}px;top:{px(348)}px;'
                 f'width:{px(484)}px;font-size:{px(38)}px">{feat["title"]}</div>')
        tw += [fade(f"#{cid}", t0 + 0.12, 0.45), fade(f"#{k}-lbl", t0 + 0.3, 0.35),
               rise(f"#{k}-n", t0 + 0.5, 22, 0.35), rise(f"#{k}-t", t0 + 0.62, 26, 0.4)]

    # ---- S04 Serif Poster
    elif lid == "S04":
        if k in S04_SIDE:  # tall assets -> side-column poster variant
            H.append(f'<div class="abs serifnum" id="{k}-n" style="left:{px(34)}px;'
                     f'top:{px(52)}px;font-size:{px(148)}px">{feat["num"]}</div>')
            # 26px keeps the longest single word ("Connectors") inside the
            # 172px column so it can never reach the card at x=220
            H.append(f'<div class="abs s4t" id="{k}-t" style="left:{px(36)}px;top:{px(224)}px;'
                     f'width:{px(172)}px;font-size:{px(26)}px">{feat["title"]}</div>')
            w, h = fit_ui(feat["ui"], mw, 372 - LABEL_H)
            c, _ = card_label(cid, feat["ui"], w, h, 220 + (316 - w) / 2, 40, feat["label"])
        else:
            H.append(f'<div class="abs serifnum" id="{k}-n" style="left:{px(34)}px;'
                     f'top:{px(20)}px;font-size:{px(158)}px">{feat["num"]}</div>')
            H.append(f'<div class="abs s4t" id="{k}-t" style="left:{px(252)}px;top:{px(56)}px;'
                     f'width:{px(290)}px;font-size:{px(34)}px">{feat["title"]}</div>')
            w, h = fit_ui(feat["ui"], mw, 212 - LABEL_H)
            ch = LABEL_H + h
            c, _ = card_label(cid, feat["ui"], w, h, (576 - w) / 2, 196 + (212 - ch) / 2,
                              feat["label"])
        H.append(c)
        tw += [drop(f"#{k}-n", t0 + 0.1, 24, 0.4), slidex(f"#{k}-t", t0 + 0.24, 26, 0.4),
               rise(f"#{cid}", t0 + 0.55, 40, 0.48)]

    # ---- S05 Phone in zone
    elif lid == "S05":
        # geometry chosen so the 6deg-rotated bounding box stays inside the zone
        # (corners: x 226..556, y 6..418 — clear of the edges and the caption pill)
        PW, PH, PL, PT = 290, 376, 246, 20
        SIW, SIH = PW - 24, PH - 24
        BAR, HOME = 34, 22
        w, h = fit_ui(feat["ui"], SIW, SIH - BAR - HOME - 16)
        H.append(f'<div class="abs sphone" id="{cid}" style="left:{px(PL)}px;top:{px(PT)}px;'
                 f'width:{px(PW)}px;height:{px(PH)}px;transform:rotate(6deg)">'
                 f'<div class="sphscreen" style="left:{px(12)}px;top:{px(12)}px;'
                 f'width:{px(SIW)}px;height:{px(SIH)}px">'
                 f'<div class="sphbar" style="height:{px(BAR)}px">{feat["label"]}</div>'
                 f'<div class="abs" style="left:{px((SIW - w) / 2)}px;'
                 f'top:{px(BAR + (SIH - BAR - HOME - h) / 2)}px">{uiimg(feat["ui"], w, h)}</div>'
                 f'<div class="sphhome"></div></div></div>')
        H.append(f'<div class="abs serifnum" id="{k}-n" style="left:{px(38)}px;top:{px(62)}px;'
                 f'font-size:{px(72)}px">{feat["num"]}</div>')
        H.append(f'<div class="abs s5t" id="{k}-t" style="left:{px(40)}px;top:{px(156)}px;'
                 f'width:{px(196)}px;font-size:{px(33)}px">{feat["title"]}</div>')
        H.append(f'<div class="abs s5s" id="{k}-s" style="left:{px(40)}px;top:{px(266)}px;'
                 f'width:{px(196)}px;font-size:{px(20)}px">{feat["sub"]}</div>')
        tw += [popo(f"#{cid}", t0 + 0.35, 0.45, 0.82), drop(f"#{k}-n", t0 + 0.1, 20, 0.35),
               slidex(f"#{k}-t", t0 + 0.22, -24), fade(f"#{k}-s", t0 + 0.42, 0.35)]

    # ---- S06 Progress steps
    elif lid == "S06":
        segs = "".join(
            f'<div class="stepseg{" on" if i <= feat["n"] - 1 else ""}">'
            f'<span>{FEATURES[i]["num"]}</span></div>' for i in range(5))
        H.append(f'<div class="abs steprow" id="{k}-steps" style="left:{px(48)}px;'
                 f'top:{px(40)}px;width:{px(480)}px">{segs}</div>')
        H.append(f'<div class="abs center s6t" id="{k}-t" style="top:{px(94)}px;'
                 f'font-size:{px(34)}px">{feat["title"]}</div>')
        tw += [fade(f"#{k}-steps", t0 + 0.06, 0.3), rise(f"#{k}-t", t0 + 0.2, 24, 0.38)]
        w, h = fit_ui(feat["ui"], mw, 246)
        c, _ = card_plain(cid, feat["ui"], w, h, (576 - w) / 2, 154 + (246 - h) / 2)
        H.append(c)
        tw.append(rise(f"#{cid}", t0 + 0.5, 40, 0.45))

    # ---- S07 Dark terminal
    elif lid == "S07":
        H.append(f'<div class="abs termbar" id="{k}-tb" style="left:0;top:{px(20)}px;'
                 f'width:1080px"><span class="dot r"></span><span class="dot y"></span>'
                 f'<span class="dot g"></span><span class="termttl">claude.ai</span></div>')
        H.append(f'<div class="abs termwin" id="{k}-win" style="left:{px(28)}px;top:{px(82)}px;'
                 f'width:{px(520)}px"><div class="termhead"><span class="tprompt">&gt;</span> '
                 f'{feat["title"].lower()}<span class="tcursor"></span></div></div>')
        w, h = fit_ui(feat["ui"], mw, 222)
        H.append(f'<div class="abs termimg" id="{cid}" style="left:{px(28 + (520 - w) / 2)}px;'
                 f'top:{px(150 + (222 - h) / 2)}px">{uiimg(feat["ui"], w, h)}</div>')
        H.append(f'<div class="abs monolbl s7num" id="{k}-n" style="left:{px(30)}px;'
                 f'top:{px(392)}px;font-size:{px(16)}px">step {feat["num"]} / 05</div>')
        tw += [fade(f"#{k}-tb", t0 + 0.05, 0.3), rise(f"#{k}-win", t0 + 0.16, 26, 0.4),
               rise(f"#{cid}", t0 + 0.55, 34, 0.45), fade(f"#{k}-n", t0 + 0.8, 0.3)]

    # ---- S08 Checklist
    elif lid == "S08":
        rows = "".join(
            f'<div class="s8row{" on" if i <= feat["n"] - 1 else ""}" id="{k}-r{i}">'
            f'<span class="s8box">✓</span><span class="s8tx">{FEATURES[i]["title"]}</span></div>'
            for i in range(5))
        H.append(f'<div class="abs monolbl s8lbl" id="{k}-lbl" style="left:{px(38)}px;'
                 f'top:{px(54)}px;font-size:{px(16)}px">the free plan</div>')
        H.append(f'<div class="abs s8list" id="{k}-list" style="left:{px(36)}px;'
                 f'top:{px(110)}px;width:{px(238)}px">{rows}</div>')
        w, h = fit_ui(feat["ui"], 248, 284)
        c, _ = card_plain(cid, feat["ui"], w, h, 292 + (248 - w) / 2, 110 + (284 - h) / 2)
        H.append(c)
        tw += [fade(f"#{k}-lbl", t0 + 0.05, 0.3), fade(f"#{k}-list", t0 + 0.1, 0.3),
               popo(f"#{k}-r{feat['n'] - 1}", t0 + 0.35, 0.3, 0.92),
               popo(f"#{cid}", t0 + 0.5, 0.4, 0.8)]

    # ---- S09 Video zone: real UI demo video fills the zone where one exists,
    #      ken-burns on the still screenshot otherwise.
    elif lid == "S09":
        seam = SP_THEME[lid]["seam"]
        ztop = seam if seam != 460 else 0
        if k in UI_VIDS:
            root.append(
                f'  <video id="uiv-{k}" src="assets/uivid/{k}.mp4" data-start="{t0}" '
                f'data-duration="{t1 - t0:.2f}" data-media-start="0" data-track-index="10" '
                f'muted playsinline style="position:absolute;top:{px(ztop)}px;left:0;'
                f'width:1080px;height:{px(460)}px;object-fit:cover"></video>')
        else:
            w, h = fit_ui(feat["ui"], 528, 336)
            H.append(f'<div class="abs" id="{cid}" style="left:{px((576 - w) / 2)}px;'
                     f'top:{px(196 - h / 2)}px">{uiimg(feat["ui"], w, h)}</div>')
            tw += [
                fade(f"#{cid}", t0 + 0.1, 0.5),
                f'tl.fromTo("#{cid}",{{scale:1,x:{px(-9)}}},{{scale:1.045,x:{px(9)},'
                f'duration:{t1 - t0 - 0.3:.2f},ease:"none"}},{t0 + 0.15:.2f});',
            ]
        # label + scrim ride above the video on their own root-level clip
        root.append(
            f'  <div id="ov-{k}" class="clip s9ov" data-start="{t0}" '
            f'data-duration="{t1 - t0:.2f}" data-track-index="11" '
            f'style="top:{px(ztop)}px;left:0;width:1080px;height:{px(460)}px">'
            f'<div class="abs s9scrim"></div>'
            f'<div class="abs center monolbl s9lbl" style="top:{px(390)}px;'
            f'font-size:{px(17)}px">{feat["num"]} — {feat["title"]}</div></div>')
        tw.append(fade(f"#ov-{k} .s9lbl", t0 + 0.4, 0.35))

    # ---- S10 Typographic
    else:
        H.append(f'<div class="abs s10num" id="{k}-n" style="left:{px(40)}px;top:{px(28)}px;'
                 f'font-size:{px(96)}px">{feat["num"]}</div>')
        H.append(f'<div class="abs s10w" id="{k}-w" style="left:{px(178)}px;top:{px(46)}px;'
                 f'width:{px(360)}px;font-size:{px(52)}px">{feat["word"]}</div>')
        w, h = fit_ui(feat["ui"], mw, 240)
        c, _ = card_plain(cid, feat["ui"], w, h, (576 - w) / 2, 158 + (240 - h) / 2)
        H.append(c)
        tw += [drop(f"#{k}-n", t0 + 0.08, 20, 0.35), slidex(f"#{k}-w", t0 + 0.2, 26, 0.4),
               rise(f"#{cid}", t0 + 0.5, 40, 0.45)]

    return sp_zone(lid, k, t0, t1, k, "\n    ".join(H), FTRACK[k]), tw, root


def sp_intro_models(lid):
    idark = sp_bg(lid, "intro") == "dark"
    mdark = sp_bg(lid, "models") == "dark"
    tw = []
    if lid in ("S02", "S04", "S10"):
        iy = dict(lbl=54, card=100, ev=338)
    elif lid in ("S06", "S08"):
        iy = dict(lbl=44, card=104, ev=342)
    else:
        iy = dict(lbl=56, card=90, ev=318)
    intro = (
        f'<div class="abs center monolbl introlbl" id="sx-lbl" style="top:{px(iy["lbl"])}px;'
        f'font-size:{px(16)}px">Claude · Free plan</div>'
        f'<div class="abs introcard" id="sx-card" style="left:{px(50)}px;top:{px(iy["card"])}px;'
        f'width:{px(476)}px;height:{px(196)}px">'
        f'<img src="assets/logos/claude.png" alt=""/><span>Claude</span></div>'
        f'<div class="abs center introev{"" if idark else " lt"}" id="sx-ev" '
        f'style="top:{px(iy["ev"])}px">EVERYTHING <span class="dollar">$0</span></div>'
    )
    tw += [fade("#sx-lbl", 0.15, 0.4),
           'tl.fromTo("#sx-card",{scale:0},{scale:1,duration:0.5,ease:"back.out(1.7)"},0.1);',
           'tl.fromTo("#sx-ev",{scale:0},{scale:1,duration:0.4,ease:"back.out(1.9)"},1.9);']

    if lid in ("S03", "S07", "S09"):
        my = dict(mark=112, pills=248, note=352)
    elif lid in ("S04", "S10"):
        my = dict(mark=98, pills=232, note=338)
    else:
        my = dict(mark=124, pills=254, note=356)
    models = (
        f'<div class="abs center mdmark{" onDark" if mdark else ""}" id="md-mark" '
        f'style="top:{px(my["mark"])}px">'
        f'<img src="assets/logos/claude.png" alt=""/><span>Claude</span></div>'
        f'<div class="abs pillrow" id="md-pills" style="top:{px(my["pills"])}px">'
        f'<span class="mdpill" id="md-p0">Sonnet <em>4.6</em></span>'
        f'<span class="mdpill orange" id="md-p1">Opus</span></div>'
        f'<div class="abs center mdnote{" onDark" if mdark else ""}" id="md-note" '
        f'style="top:{px(my["note"])}px">every model. zero dollars.</div>'
    )
    tw += [fade("#md-mark", 40.6, 0.4), pop("#md-p0", 41.4), pop("#md-p1", 44.2),
           fade("#md-note", 45.4, 0.4)]
    return (sp_zone(lid, "intro", 0.0, 2.85, "intro", intro, 2) + "\n"
            + sp_zone(lid, "models", 40.5, 47.45, "models", models, 8)), tw


def split_css(lid):
    return base_css() + f"""
#root {{ background:#000; }}
.tz {{ left:0; width:1080px; overflow:hidden; }}
.tz.dark {{ background:{DARK}; }}
.tz.cream {{ background:{CREAM2}; }}
.shead {{ display:flex; align-items:baseline; gap:{px(18)}px; }}
.stitle {{ font-weight:700; color:#1E1E1E; white-space:nowrap; }}
.stitle.onDark {{ color:#FFFFFF; }}
.pillrow {{ left:0; width:1080px; display:flex; justify-content:center; gap:{px(14)}px; }}
.spill {{ background:#fff; border-radius:{px(22)}px; padding:{px(10)}px {px(20)}px;
  font-family:'JetBrains Mono',monospace; font-size:{px(19)}px; color:#1E1E1E;
  box-shadow:0 {px(8)}px {px(20)}px rgba(0,0,0,0.16); }}
/* intro */
.introlbl {{ color:#8A8A8A; }}
.tz.cream .introlbl {{ color:#77746E; }}
.introcard {{ background:#F5F0E5; border-radius:{px(24)}px; display:flex; align-items:center;
  justify-content:center; gap:{px(12)}px; }}
.introcard img {{ width:{px(42)}px; height:{px(42)}px; }}
.introcard span {{ font-family:Lora,serif; font-weight:500; font-size:{px(52)}px; color:#171512; }}
.introev {{ font-family:'Playfair Display',serif; font-style:italic; font-weight:800;
  font-size:{px(46)}px; color:#fff; letter-spacing:0.02em; }}
.introev.lt {{ color:#1E1E1E; }}
.introev .dollar {{ color:{TERRA_L}; font-size:{px(54)}px; }}
/* models */
.mdmark {{ display:flex; align-items:center; justify-content:center; gap:{px(10)}px; }}
.mdmark img {{ width:{px(36)}px; height:{px(36)}px; }}
.mdmark span {{ font-family:Lora,serif; font-weight:500; font-size:{px(46)}px; color:#171512; }}
.mdmark.onDark span {{ color:#F4EFE7; }}
.mdpill {{ background:#fff; border-radius:{px(28)}px; padding:{px(14)}px {px(26)}px;
  font-weight:700; font-size:{px(26)}px; color:#1E1E1E;
  box-shadow:0 {px(10)}px {px(26)}px rgba(0,0,0,0.12); }}
.mdpill em {{ font-style:normal; color:{TERRA_L}; }}
.mdpill.orange {{ color:{TERRA_L}; }}
.mdnote {{ font-family:'JetBrains Mono',monospace; font-size:{px(19)}px; color:#87847E; }}
.mdnote.onDark {{ color:#8A8A8A; }}
/* S03 */
.s3scrim {{ left:0; top:{px(248)}px; width:1080px; height:{px(212)}px;
  background:linear-gradient(180deg, rgba(16,16,18,0) 0%, rgba(16,16,18,0.86) 58%,
  rgba(16,16,18,0.95) 100%); }}
.s3lbl {{ color:#B9B5AE; }}
.s3num {{ color:{TERRA_L}; }}
.s3t {{ font-weight:700; color:#fff; }}
/* S04 */
.s4t {{ font-weight:700; color:#F4EFE7; line-height:1.14; }}
.tz.cream .s4t {{ color:#1E1E1E; }}
/* S05 */
.sphone {{ background:{DARK}; border-radius:{px(38)}px;
  box-shadow:0 {px(18)}px {px(40)}px rgba(0,0,0,0.28); }}
.sphscreen {{ position:absolute; background:#FBFAF6; border-radius:{px(28)}px; overflow:hidden; }}
.sphbar {{ display:flex; align-items:center; justify-content:center;
  font-family:'JetBrains Mono',monospace; font-size:{px(14)}px; color:#96938D;
  border-bottom:1px solid #EDEAE2; }}
.sphhome {{ position:absolute; left:50%; bottom:{px(8)}px; width:{px(96)}px;
  height:{px(5)}px; border-radius:{px(3)}px; background:rgba(17,17,17,0.16);
  margin-left:{px(-48)}px; }}
.s5t {{ font-weight:700; color:#1E1E1E; line-height:1.15; }}
.s5s {{ font-weight:500; color:#7C7972; line-height:1.3; }}
/* S06 */
.steprow {{ display:flex; gap:{px(12)}px; }}
.stepseg {{ flex:1; height:{px(34)}px; border-radius:{px(10)}px; background:rgba(17,17,17,0.08);
  display:flex; align-items:center; justify-content:center;
  font-family:'JetBrains Mono',monospace; font-size:{px(15)}px; color:#8B8880; }}
.tz.dark .stepseg {{ background:rgba(255,255,255,0.10); }}
.stepseg.on {{ background:{TERRA}; color:#fff; }}
.s6t {{ font-weight:700; color:#1E1E1E; }}
.tz.dark .s6t {{ color:#F4EFE7; }}
/* S07 */
.termbar {{ display:flex; align-items:center; gap:{px(8)}px; padding:0 {px(28)}px;
  height:{px(40)}px; }}
.termttl {{ font-family:'JetBrains Mono',monospace; font-size:{px(18)}px; color:#9B978F;
  margin-left:{px(14)}px; }}
.termwin {{ background:{DARK2}; border:1px solid #2A2A31; border-radius:{px(14)}px;
  padding:{px(16)}px {px(20)}px {px(252)}px; }}
.termhead {{ font-family:'JetBrains Mono',monospace; font-size:{px(21)}px; color:#E8E6E1; }}
.tprompt {{ color:{TERRA_L}; }}
.tcursor {{ display:inline-block; width:{px(11)}px; height:{px(20)}px; background:{TERRA_L};
  margin-left:{px(8)}px; vertical-align:{px(-2)}px; }}
.termimg {{ border-radius:{px(8)}px; overflow:hidden; }}
.s7num {{ color:#7E7A73; }}
/* S08 */
.s8lbl {{ color:#8B8880; }}
.s8list {{ display:flex; flex-direction:column; gap:{px(5)}px; }}
.s8row {{ display:flex; align-items:center; gap:{px(10)}px; padding:{px(8)}px {px(12)}px;
  border-radius:{px(10)}px; background:rgba(17,17,17,0.035); }}
.s8row.on {{ background:#fff; box-shadow:0 {px(5)}px {px(14)}px rgba(0,0,0,0.07); }}
.s8box {{ width:{px(22)}px; height:{px(22)}px; border-radius:{px(7)}px; background:#DDDCD6;
  color:#fff; font-weight:700; font-size:{px(13)}px; display:flex; align-items:center;
  justify-content:center; flex:none; }}
.s8row.on .s8box {{ background:{TERRA}; }}
.s8tx {{ font-weight:600; font-size:{px(19)}px; color:#B4B2AB; white-space:nowrap; }}
.s8row.on .s8tx {{ color:#111; }}
/* S09 */
.s9ov {{ overflow:hidden; }}
.s9scrim {{ left:0; bottom:0; width:1080px; height:{px(150)}px;
  background:linear-gradient(180deg, rgba(16,16,18,0) 0%, rgba(16,16,18,0.72) 55%,
  rgba(16,16,18,0.90) 100%); }}
.s9lbl {{ color:#E6E2DA; }}
/* S10 */
.s10num {{ font-family:Poppins,sans-serif; font-weight:800; color:transparent;
  -webkit-text-stroke:{px(3)}px {TERRA_L}; line-height:1; }}
.s10w {{ font-weight:800; color:#1E1E1E; line-height:1.02; letter-spacing:-0.02em; }}
.tz.dark .s10w {{ color:#F4EFE7; }}
/* glitch */
#glitch {{ inset:0; }}
.gfree {{ top:{px(452)}px; left:0; width:1080px; text-align:center;
  font-family:'Archivo Black',sans-serif; font-size:{px(118)}px; letter-spacing:-0.01em;
  line-height:1; }}
.gr {{ color:rgba(255,40,40,0.8); margin-left:{px(-7)}px; }}
.gc {{ color:rgba(40,230,255,0.8); margin-left:{px(7)}px; }}
.gw {{ color:#fff; }}
.gflash {{ inset:0; background:#fff; }}
/* captions */
.scap {{ left:0; width:1080px; text-align:center; }}
.scappill {{ display:inline-block; transform:translateY(-50%); background:{CAP_TERRA};
  color:#fff; font-family:Nunito,sans-serif; font-weight:800; font-size:{px(30)}px;
  padding:{px(10)}px {px(18)}px; border-radius:{px(12)}px; white-space:nowrap; }}
"""


def split_html(lid):
    seam = SP_THEME[lid]["seam"]
    face_top = 0 if seam != 460 else px(460)
    face_els = []
    for i, (typ, scene, t0, t1) in enumerate(SPLIT_MODES):
        d = min(t1, DUR) - t0
        if d <= 0:
            continue
        if typ == "full":
            src = "assets/face_punch.mp4" if scene == "cta" else "assets/face_full.mp4"
            style = "top:0;left:0;width:1080px;height:1920px;object-fit:cover;"
        else:
            src = "assets/face_bottom.mp4"
            style = f"top:{face_top}px;left:0;width:1080px;height:{px(564)}px;object-fit:cover;"
        face_els.append(
            f'  <video id="face{i}" src="{src}" data-start="{t0}" data-duration="{d:.2f}" '
            f'data-media-start="{t0}" data-track-index="1" muted playsinline '
            f'style="position:absolute;{style}"></video>')

    zones, tws, overlays = [], [], []
    im_html, im_tw = sp_intro_models(lid)
    zones.append(im_html)
    tws += im_tw
    for f in FEATURES:
        h, t, root = sp_scene(lid, feat_for(lid, f))
        zones.append(h)
        tws += t
        overlays += root  # painted after the zones — DOM order is paint order

    glitch = """  <div id="glitch" class="clip" data-start="48.4" data-duration="0.95" data-track-index="12">
    <div class="abs gfree gr">FREE</div>
    <div class="abs gfree gc">FREE</div>
    <div class="abs gfree gw">FREE</div>
    <div class="abs gflash" id="gflash"></div>
  </div>"""
    tws += [
        'tl.fromTo("#gflash",{opacity:0.55},{opacity:0,duration:0.35,ease:"power2.out"},48.4);',
        'tl.fromTo("#glitch .gw",{opacity:1},{opacity:0.9,duration:0.06,repeat:14,yoyo:true,ease:"none"},48.4);',
        f'tl.to("#bgm",{{volume:0,duration:1.5}},{DUR - 1.6:.2f});',
    ]
    seed = -10 + (int(lid[1:]) - 1) * 4

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=1080, height=1920"/>
<title>Abik Split R2 {lid}</title>
{GSAP}
{FONTS}
<style>
{split_css(lid)}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920"
     data-duration="{DUR}" data-fps="30">

{chr(10).join(face_els)}

{chr(10).join(zones)}

{chr(10).join(overlays)}

{glitch}

{caption_clips_split(seam)}

{audio_block("bed_split.mp3", SFX_SPLIT, seed)}
</div>

<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
const POP = "back.out(2.4)";
const SOFT = "power3.out";
{chr(10).join(tws)}
window.__timelines["main"] = tl;
</script>
</body>
</html>"""


# ======================================================================
# staging + main
# ======================================================================
def stage_shared():
    a = HF_ROOT / "_assets"
    (a / "logos").mkdir(parents=True, exist_ok=True)
    (a / "sfx").mkdir(exist_ok=True)
    (a / "music").mkdir(exist_ok=True)
    (a / "ui").mkdir(exist_ok=True)
    for f in ["audio_tight.m4a", "face_bottom.mp4", "face_full.mp4", "face_punch.mp4"]:
        if not (a / f).exists():
            shutil.copy2(PUB / f, a / f)
    for f in ["claude.png", "google.svg", "microsoft.svg", "slack.png", "notion.png"]:
        shutil.copy2(PUB / "logos" / f, a / "logos" / f)
    for f in ["pop", "whoosh", "boom", "click", "ding"]:
        shutil.copy2(PUB / f"{f}.mp3", a / "sfx" / f"{f}.mp3")
    for f in ["bed_faceless.mp3", "bed_split.mp3"]:
        if not (a / "music" / f).exists():
            shutil.copy2(PUB / f, a / "music" / f)
    for f in UI_FILES:  # always re-copy: upstream captures get refreshed
        shutil.copy2(PUB / "ui" / f, a / "ui" / f)
    (a / "uivid").mkdir(exist_ok=True)
    for v in UI_VIDS:
        if not (a / "uivid" / f"{v}.mp4").exists():
            shutil.copy2(PUB / "uivid" / f"{v}.mp4", a / "uivid" / f"{v}.mp4")
    # deprecated capture must not linger in the staged pool
    (a / "ui" / "connectors_panel.png").unlink(missing_ok=True)
    return a


def link_assets(dest: Path, shared: Path):
    link = dest / "assets"
    if link.is_symlink():
        link.unlink()
    elif link.exists():
        shutil.rmtree(link)
    link.symlink_to(shared, target_is_directory=True)


FACELESS_IDS = [f"F{i:02d}" for i in range(1, 11)]
SPLIT_IDS = [f"S{i:02d}" for i in range(1, 11)]

if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    shared = stage_shared()
    for lid in FACELESS_IDS:
        if only and only not in (lid, "faceless"):
            continue
        d = HF_ROOT / f"faceless_{lid}"
        d.mkdir(parents=True, exist_ok=True)
        link_assets(d, shared)
        (d / "index.html").write_text(faceless_html(lid))
        print("wrote", d / "index.html")
    for lid in SPLIT_IDS:
        if only and only not in (lid, "split"):
            continue
        d = HF_ROOT / f"split_{lid}"
        d.mkdir(parents=True, exist_ok=True)
        link_assets(d, shared)
        (d / "index.html").write_text(split_html(lid))
        print("wrote", d / "index.html")
