"""deepresearch / DIAGRAM BUILD — run 4, STANDARD v1.1.

Forked from shorts_run3/gen3/deepresearch_gen.py (diagram lane only). Same proven
chassis: design space 576x1024 scaled by S=1.875 into 1080x1920, seam at design
y=460, terracotta caption pills riding the seam, face_bottom below the seam for the
whole duration, identical audio bed/sfx, event-only tweens, contiguous zones holding
0.15s under the incoming zone.

v1.1 (PILOT VERDICT, 2026-08-10) fixes applied here:
  BUILD ORDER   — every connector now draws AFTER both nodes it joins:
                  * producer stems fire on their own logo's landing (+0.30s), not
                    as one early cascade (4 of 7 stems used to precede their logo)
                  * the beat-2 DEEP RESEARCH hub lands before the arrow into it
                  * the convergence lines wait for the "your context" panel
                  * the beat-4 output nodes land before their arrows
  METERS COMPLETE — the four agent meters all fill to 100% (were 92/74/100/84%).
  ASSET HEALTH  — the broken 3-dot/2-line "connection" glyph is gone; the agent
                  mark is a plated sparkle (single clip-path, nothing to break).
  FILL THE SHAPE — check/cross marks are rounded squares in the card/node radius
                  family (no circles inside rounded boxes); the sparkle sits on a
                  plate in the same radius language as the logo tiles.
  OUTRO ALIGNMENT — the exit screen is one centred composition: FOLLOW on the
                  vertical axis, three equal nodes centred beneath it, arrows that
                  point at nodes that exist, then the serif line and the handle
                  chip on the same axis. (Run 3 put FOLLOW right-of-centre with a
                  left column and diagonal pointers — the "odd diagram" class.)
  SEAM IS SACRED — the run-3 outro wrapper's bottom edge sat exactly ON the seam
                  (an audit ERROR under v1.1); the outro atoms are now direct
                  children of the zone and the lowest ink clears the seam by 72
                  design px.
  ARROW TERMINATION — heads overlap the shaft end, so the drawn connector reaches
                  the box edge instead of stopping a head-length short of it.
  TRANSCRIPT IS TRUTH — every label tracks the spoken words ("your application",
                  not "your app").
  ATTRIBUTION   — @XFreeze appears only inside the tweet card, first screen, 2.95s.

Binding asset verdict (shorts_run3/plans/asset_verdicts_v3.json, deepresearch):
  image_1 = the @XFreeze x_card -> use, beat 1 ONLY, max 3s. Staged through PIL
  cropped to the header + the one claim paragraph: the metrics row (406 Likes /
  67 Reposts / 23.4K Views, source y>=600) never reaches the frame (law 3) and the
  crop keeps the type large enough to read on a phone (law 8).

Typography rule (Miguel's run-3 review): never mix typefaces inside one sentence —
accent by COLOUR only. Instrument Serif is reserved for standalone payoff lines.
"""
import html as ihtml
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from math import atan2, degrees, hypot
from pathlib import Path

from PIL import Image, ImageDraw

FACTORY = Path.home() / "Documents/Workspace/projects/personal/content/shorts-factory"
RUN1 = FACTORY / "shorts_run1"
R4 = FACTORY / "shorts_run4"
STAGE = R4 / "gen/_stage_deepresearch_diagram"
PROJ = R4 / "projects"
LOGOS = Path.home() / "Documents/Workspace/assets/logos"
VID = "deepresearch"
LANE = "diagram"
STEM = "2026-08-08_21-14-48"
CARD = RUN1 / "x_cards/card_XFreeze_2081597809862885661.png"

S = 1080 / 576
FPS = 30
SEAM = 460
ZONE_H = 460
FACE_H = 564
OVERLAP = 0.15


def px(v):
    return round(v * S, 1)


# ---------------------------------------------------------------- tokens
CREAM = "#F6F1EA"
DARK = "#101012"
INK = "#111111"
INK_S = "#6E6A62"
TERRA = "#C4573A"
TERRA_L = "#DD7259"
CAP_TERRA = "#C4573A"
ON_DARK = "#F3EEE6"
ON_DARK_S = "#9C978D"
TRACK_L = "rgba(17,17,17,0.10)"
TRACK_D = "rgba(255,255,255,0.13)"

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800'
    "&family=Nunito:wght@800"
    "&family=Instrument+Serif:ital@0;1"
    '&family=JetBrains+Mono:wght@400;500;700&display=block" rel="stylesheet">'
)
GSAP = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>'

# law 2: every producer he NAMES renders as its logo, never a text pill.
NAMED = ["openai", "claude", "gemini", "grok"]
MORE = ["perplexity", "deepseek", "copilot"]
ALL_LOGOS = NAMED + MORE
LOGO_SRC = {
    "openai": "ai-models/openai.png",
    "claude": "ai-models/claude-color.png",
    "gemini": "ai-models/gemini-color.png",
    "grok": "ai-models/grok.png",
    "perplexity": "ai-models/perplexity-color.png",
    "deepseek": "ai-models/deepseek.png",
    "copilot": "coding-tools/copilot-color.png",
}


def esc(s):
    return ihtml.escape(str(s), quote=False)


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(r.stdout.strip())


# ---------------------------------------------------------------- tweens (event-only)
def rise(sel, t, dy=20, d=0.42, e="SOFT"):
    return (f'tl.fromTo("{sel}",{{y:{px(dy)},opacity:0}},'
            f'{{y:0,opacity:1,duration:{d},ease:{e}}},{t:.2f});')


def slidex(sel, t, dx=-20, d=0.4):
    return (f'tl.fromTo("{sel}",{{x:{px(dx)},opacity:0}},'
            f'{{x:0,opacity:1,duration:{d},ease:SOFT}},{t:.2f});')


def fade(sel, t, d=0.4, to=1, frm=0):
    return f'tl.fromTo("{sel}",{{opacity:{frm}}},{{opacity:{to},duration:{d},ease:SOFT}},{t:.2f});'


def popo(sel, t, d=0.36, s=0.78):
    return (f'tl.fromTo("{sel}",{{scale:{s},opacity:0}},'
            f'{{scale:1,opacity:1,duration:{d},ease:POP}},{t:.2f});')


def slam(sel, t, d=0.34, s=1.18):
    return (f'tl.fromTo("{sel}",{{scale:{s},opacity:0}},'
            f'{{scale:1,opacity:1,duration:{d},ease:SLAM}},{t:.2f});')


def settle(sel, t, s0=0.965, d=0.5):
    """Frame-0 composition: already opaque, eases into place once, then holds."""
    return (f'tl.fromTo("{sel}",{{scale:{s0}}},{{scale:1,duration:{d},'
            f'ease:SOFT}},{t:.2f});')


def sweep(sel, t, d=0.45, to=1, frm=0):
    return f'tl.fromTo("{sel}",{{scaleX:{frm}}},{{scaleX:{to},duration:{d},ease:SOFT}},{t:.2f});'


def moveto(sel, t, x, y=0.0, d=0.6, x0=0.0, y0=0.0, s=None, s0=1.0):
    a = "x:%s,y:%s" % (px(x0), px(y0))
    b = "x:%s,y:%s" % (px(x), px(y))
    if s is not None:
        a += ",scale:%s" % s0
        b += ",scale:%s" % s
    return 'tl.fromTo("%s",{%s},{%s,duration:%s,ease:SOFT},%.2f);' % (sel, a, b, d, t)


def setopa(sel, t, v):
    return f'tl.set("{sel}",{{opacity:{v}}},{t:.2f});'


def hardkill(sel, t):
    return setopa(sel, t, 0)


def leave(sel, t, d=0.3):
    """Discrete exit: fade out, then a hard kill so nothing lingers on a clip boundary."""
    return [fade(sel, t, d, 0, 1), hardkill(sel, t + d)]


def retract(sel, t, d=0.3):
    """Exit for a drawn rule: fade, kill, then collapse scaleX so the element stops
    occupying geometry. An opacity-0 rule still measures 1:1 in the audit (and in any
    later layout maths) — the run-3 key-term underline read as a live 168px connector
    for 5s after it had visually left."""
    return leave(sel, t, d) + [f'tl.set("{sel}",{{scaleX:0}},{t + d:.2f});']


# ---------------------------------------------------------------- captions
STUTTER = {"uh", "um", "huh", "mm", "mmm", "hmm", "erm", "ah", "eh"}


def clean_words(words):
    """Law 6: stutters and partial words never reach the captions."""
    out = []
    for w in words:
        t = w["text"].strip()
        if not t or t.endswith("-"):
            continue
        if re.sub(r"[^a-z]", "", t.lower()) in STUTTER:
            continue
        out.append(w)
    return out


def build_captions(words):
    words = clean_words(words)
    phrases, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        endp = re.search(r"[.,!?]$", w["text"])
        gap = (i + 1 < len(words)) and (words[i + 1]["start"] - w["end"] > 0.32)
        if len(cur) >= 4 or (endp and len(cur) >= 2) or gap:
            phrases.append({"t0": round(cur[0]["start"], 2),
                            "t1": round(w["end"] + 0.12, 2),
                            "text": " ".join(x["text"] for x in cur)})
            cur = []
    if cur:
        phrases.append({"t0": round(cur[0]["start"], 2),
                        "t1": round(cur[-1]["end"] + 0.12, 2),
                        "text": " ".join(x["text"] for x in cur)})
    for i in range(len(phrases) - 1):
        phrases[i]["t1"] = round(phrases[i + 1]["t0"], 2)
    return phrases


CAP_MAX_W = 520.0
CAP_PAD = 36.0


def cap_font(text):
    est = 0.575 * max(1, len(text))
    return round(max(19.0, min(30.0, (CAP_MAX_W - CAP_PAD) / est)), 1)


def caption_clips(phrases, dur):
    out = []
    for i, c in enumerate(phrases):
        t0, t1 = c["t0"], min(c["t1"], dur)
        if t1 - t0 < 0.08 or t0 >= dur:
            continue
        out.append(
            f'  <div id="cap{i}" class="clip scap" style="top:{px(SEAM)}px" data-start="{t0}" '
            f'data-duration="{t1 - t0:.2f}" data-track-index="25">'
            f'<span class="scappill" style="font-size:{px(cap_font(c["text"]))}px">'
            f'{esc(c["text"])}</span></div>')
    return "\n".join(out)


# ---------------------------------------------------------------- audio
def audio_block(dur, beats, cta_start):
    els, idx = [], 0
    els.append(f'  <audio id="vo" src="assets/v/{VID}/audio.m4a" data-start="0" '
               f'data-duration="{dur:.2f}" data-track-index="30" data-volume="1"></audio>')
    bed_len = 52.0
    bed_ids, t, n = [], 0.0, 0
    while t < dur - 0.2:
        d = min(bed_len, dur - t)
        bid = f"bgm{n}"
        bed_ids.append((bid, t))
        els.append(f'  <audio id="{bid}" src="assets/music/bed_split.mp3" data-start="{t:.2f}" '
                   f'data-duration="{d:.2f}" data-track-index="31" data-volume="0.16"></audio>')
        t += bed_len
        n += 1
    sfx = []
    for b in beats:
        sfx.append((max(0.02, b[0]), "whoosh", 0.68, 0.2))
        sfx.append((b[0] + 0.35, "pop", 0.6, 0.28))
    sfx.append((cta_start, "whoosh", 0.68, 0.2))
    sfx.append((cta_start + 0.4, "boom", 0.88, 0.4))
    for t0, name, d, vol in sfx:
        if t0 >= dur - 0.1:
            continue
        els.append(f'  <audio id="sfx{idx}" src="assets/sfx/{name}.mp3" data-start="{t0:.2f}" '
                   f'data-duration="{min(d, dur - t0):.2f}" data-track-index="{32 + idx}" '
                   f'data-volume="{vol}"></audio>')
        idx += 1
    fade_at = max(bed_ids[-1][1] + 0.1, dur - 1.6)
    return "\n".join(els), [f'tl.to("#{bed_ids[-1][0]}",{{volume:0,duration:1.5}},{fade_at:.2f});']


# ---------------------------------------------------------------- shared CSS
def base_css():
    return f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden;
  font-family:Poppins,sans-serif; }}
.clip {{ position:absolute; }}
.abs {{ position:absolute; }}
.tz {{ left:0; top:0; width:1080px; height:{px(ZONE_H)}px; overflow:hidden; }}
.tz.cream {{ background:{CREAM}; }}
.tz.dark {{ background:{DARK}; }}
.serif {{ font-family:'Instrument Serif',serif; font-style:italic; line-height:1.0;
  color:{TERRA_L}; }}
.mono {{ font-family:'JetBrains Mono',monospace; letter-spacing:{px(2.0)}px;
  text-transform:uppercase; }}
.disp {{ font-family:Poppins,sans-serif; font-weight:800; letter-spacing:-0.02em;
  line-height:1.05; color:{INK}; overflow-wrap:break-word; }}
.disp.od {{ color:{ON_DARK}; }}
.shot {{ overflow:hidden; background:#FFFFFF;
  box-shadow:0 {px(14)}px {px(34)}px rgba(0,0,0,0.20); }}
.shot img {{ display:block; width:100%; height:100%; }}
.ltile {{ background:#FFFFFF; display:flex; align-items:center; justify-content:center;
  border:1px solid rgba(17,17,17,0.09);
  box-shadow:0 {px(4)}px {px(11)}px rgba(0,0,0,0.07); }}
.ltile.od {{ box-shadow:none; border:1px solid rgba(255,255,255,0.18); }}
.rule {{ display:block; transform-origin:left center; background:{TERRA}; }}
.node {{ border-radius:{px(13)}px; border:{px(2)}px solid rgba(17,17,17,0.20);
  background:#FFFFFF; display:flex; align-items:center; justify-content:center;
  text-align:center; font-family:'JetBrains Mono',monospace; color:{INK};
  text-transform:uppercase; }}
.node.hero {{ border-color:{TERRA_L}; }}
.node.od {{ background:#1C1C21; border-color:rgba(255,255,255,0.20); color:{ON_DARK}; }}
.node.od.hero {{ border-color:{TERRA_L}; }}
.node.dash {{ border-style:dashed; border-color:rgba(17,17,17,0.30); background:transparent; }}
.card {{ border-radius:{px(16)}px; border:{px(2)}px solid rgba(17,17,17,0.16);
  background:#FFFFFF; }}
.card.od {{ background:#1C1C21; border-color:rgba(255,255,255,0.16); }}
.ctchip {{ display:inline-block; background:rgba(16,16,18,0.62); color:{CREAM};
  font-family:'JetBrains Mono',monospace; border-radius:{px(999)}px;
  padding:{px(9)}px {px(22)}px; letter-spacing:{px(2)}px; white-space:nowrap; }}
.scap {{ left:0; width:1080px; text-align:center; }}
.scappill {{ display:inline-block; transform:translateY(-50%); background:{CAP_TERRA};
  color:#fff; font-family:Nunito,sans-serif; font-weight:800;
  padding:{px(10)}px {px(18)}px; border-radius:{px(12)}px; white-space:nowrap; }}
.mark {{ display:flex; align-items:center; justify-content:center;
  font-family:Poppins,sans-serif; font-weight:800; color:#fff; }}
"""


# ---------------------------------------------------------------- element helpers
def txt(tid, cls, text, left, top, w, fs, color=None, align="left", hide=True, extra=""):
    c = f"color:{color};" if color else ""
    o = "opacity:0;" if hide else ""
    return (f'<div id="{tid}" class="abs {cls}"{extra} style="left:{px(left)}px;'
            f'top:{px(top)}px;width:{px(w)}px;font-size:{px(fs)}px;text-align:{align};'
            f'{c}{o}">{esc(text)}</div>')


def shot(sid, key, left, top, w, media, rad=14, hide=True):
    src, (iw, ih) = media[key]
    h = round(w * ih / iw, 1)
    o = "opacity:0;" if hide else ""
    el = (f'<div id="{sid}" class="abs shot" style="left:{px(left)}px;top:{px(top)}px;'
          f'width:{px(w)}px;height:{px(h)}px;border-radius:{px(rad)}px;{o}">'
          f'<img src="{src}" alt=""/></div>')
    return el, h


def logo_tile(tid, x, y, size, key, dark=False, pad=0.20, hide=True):
    inner = size * (1 - 2 * pad)
    return (f'<div id="{tid}" class="abs ltile{" od" if dark else ""}" style="left:{px(x)}px;'
            f'top:{px(y)}px;width:{px(size)}px;height:{px(size)}px;'
            f'border-radius:{px(size * 0.26)}px;{"opacity:0;" if hide else ""}">'
            f'<img src="assets/img/logos/{key}.png" alt="" style="width:{px(inner)}px;'
            f'height:{px(inner)}px;object-fit:contain"/></div>')


def node_el(nid, x, y, w, h, label, fs=14, dark=False, hero=False, dash=False, ls=1.5,
            lh=1.25, extra_cls=""):
    cls = ("node" + (" od" if dark else "") + (" hero" if hero else "")
           + (" dash" if dash else "") + (f" {extra_cls}" if extra_cls else ""))
    col = f"color:{ON_DARK_S if dark else INK_S};" if dash else ""
    return (f'<div id="{nid}" class="abs {cls}" style="left:{px(x)}px;top:{px(y)}px;'
            f'width:{px(w)}px;height:{px(h)}px;font-size:{px(fs)}px;'
            f'letter-spacing:{px(ls)}px;line-height:{lh};{col}opacity:0">{esc(label)}</div>')


def panel_el(pid, x, y, w, h, dark=False):
    """A drawn panel that connectors may terminate on. Carries `node` so the audit
    counts it as a real box edge (a bare `.card` is not in the box set)."""
    return (f'<div id="{pid}" class="abs card node{" od" if dark else ""}" '
            f'style="left:{px(x)}px;top:{px(y)}px;width:{px(w)}px;height:{px(h)}px;'
            f'opacity:0"></div>')


def ring_el(rid, x, y, w, h, rad=12, color=TERRA_L, thick=3.0):
    return (f'<div id="{rid}" class="abs" style="left:{px(x)}px;top:{px(y)}px;'
            f'width:{px(w)}px;height:{px(h)}px;border-radius:{px(rad)}px;'
            f'border-style:solid;border-width:{px(thick)}px;border-color:{color};'
            f'opacity:0"></div>')


def arrow(aid, x, y, length, deg=0.0, thick=2.6, color=TERRA, head=11.0):
    """Law 7: the head's TIP lands exactly at the far end, i.e. AT the target box
    edge. v1.1: the shaft runs under the head (instead of stopping a full head-length
    short), so the drawn connector actually reaches the edge it claims."""
    shaft = max(3.0, length - head * 0.5)
    hh = head * 0.58
    return (f'<div class="abs" style="left:{px(x)}px;top:{px(y - thick / 2)}px;'
            f'width:{px(length)}px;height:{px(thick)}px;'
            f'transform:rotate({deg:.2f}deg);transform-origin:left center">'
            f'<div id="{aid}" class="rule" style="width:{px(shaft)}px;height:100%;'
            f'background:{color};transform:scaleX(0)"></div>'
            f'<div id="{aid}h" class="abs" style="left:{px(length - head)}px;'
            f'top:{px(thick / 2 - hh)}px;width:0;height:0;opacity:0;'
            f'border-left:{px(head)}px solid {color};'
            f'border-top:{px(hh)}px solid transparent;'
            f'border-bottom:{px(hh)}px solid transparent"></div></div>')


def arrow_to(aid, x0, y0, x1, y1, thick=2.6, color=TERRA, head=11.0):
    return arrow(aid, x0, y0, hypot(x1 - x0, y1 - y0),
                 degrees(atan2(y1 - y0, x1 - x0)), thick, color, head)


def arrow_in(aid, t, d=0.4):
    return [sweep(f"#{aid}", t, d), popo(f"#{aid}h", t + d * 0.8, 0.24, 0.3)]


def line_el(lid, x, y, length, deg=0.0, thick=2.2, color=TERRA):
    return (f'<div class="abs" style="left:{px(x)}px;top:{px(y - thick / 2)}px;'
            f'width:{px(length)}px;height:{px(thick)}px;'
            f'transform:rotate({deg:.2f}deg);transform-origin:left center">'
            f'<div id="{lid}" class="rule" style="width:100%;height:100%;'
            f'background:{color};transform:scaleX(0)"></div></div>')


def line_to(lid, x0, y0, x1, y1, thick=2.2, color=TERRA):
    return line_el(lid, x0, y0, hypot(x1 - x0, y1 - y0),
                   degrees(atan2(y1 - y0, x1 - x0)), thick, color)


def meter_el(mid, x, y, w, h, track=TRACK_L, fill=TERRA):
    return (f'<div id="{mid}w" class="abs" style="left:{px(x)}px;top:{px(y)}px;'
            f'width:{px(w)}px;height:{px(h)}px;background:{track};'
            f'border-radius:{px(h / 2)}px;overflow:hidden;opacity:0">'
            f'<div id="{mid}" class="rule" style="width:100%;height:100%;'
            f'background:{fill};border-radius:{px(h / 2)}px;transform:scaleX(0)"></div></div>')


def bar_el(bid, x, y, w, h, alpha=0.88):
    return (f'<div id="{bid}" class="abs" style="left:{px(x)}px;top:{px(y)}px;'
            f'width:{px(w)}px;height:{px(h)}px;border-radius:{px(h / 2)}px;'
            f'background:rgba(196,87,58,{alpha});opacity:0"></div>')


def mark_el(mid, x, y, size, glyph_char, color, rad_frac=0.30, fs_frac=0.56):
    """FILL THE SHAPE (v1.1): verdict marks are rounded squares in the same radius
    family as the cards/nodes they sit on — never circles inside rounded boxes."""
    return (f'<div id="{mid}" class="abs mark" style="left:{px(x)}px;top:{px(y)}px;'
            f'width:{px(size)}px;height:{px(size)}px;'
            f'border-radius:{px(size * rad_frac)}px;background:{color};opacity:0;'
            f'font-size:{px(size * fs_frac)}px">{glyph_char}</div>')


def check_el(cid, x, y, size=22, color=TERRA):
    return mark_el(cid, x, y, size, "&#10003;", color)


def x_el(xid, x, y, size=22, color=INK_S):
    return mark_el(xid, x, y, size, "&#10005;", color, fs_frac=0.50)


def strike_el(sid, x, y, w, thick=2.4, color=INK_S):
    return (f'<div class="abs" style="left:{px(x)}px;top:{px(y - thick / 2)}px;'
            f'width:{px(w)}px;height:{px(thick)}px">'
            f'<div id="{sid}" class="rule" style="width:100%;height:100%;'
            f'background:{color};transform:scaleX(0)"></div></div>')


def spark_tile(gid, x, y, size, dark=False, color=TERRA_L):
    """The agent mark. ASSET HEALTH (v1.1): the old 3-dot/2-line 'connection' glyph
    rendered broken, so the agent is now a sparkle cut from ONE clip-path, sitting on
    a plate in the same rounded-square language as the logo tiles."""
    inner = size * 0.54
    off = (size - inner) / 2
    plate = "#26262C" if dark else "#FFFFFF"
    edge = "rgba(255,255,255,0.18)" if dark else "rgba(17,17,17,0.09)"
    return (f'<div id="{gid}" class="abs" style="left:{px(x)}px;top:{px(y)}px;'
            f'width:{px(size)}px;height:{px(size)}px;'
            f'border-radius:{px(size * 0.26)}px;background:{plate};'
            f'border:1px solid {edge};opacity:0">'
            f'<div class="abs" style="left:{px(off)}px;top:{px(off)}px;'
            f'width:{px(inner)}px;height:{px(inner)}px;background:{color};'
            f'clip-path:polygon(50% 0%,61% 39%,100% 50%,61% 61%,50% 100%,'
            f'39% 61%,0% 50%,39% 39%)"></div></div>')


def zone(i, t0, t1, bg, inner, extra_dur=OVERLAP):
    return (f'  <section id="tz-b{i + 1}" class="clip tz {bg}" data-start="{t0:.2f}" '
            f'data-duration="{t1 - t0 + extra_dur:.2f}" data-track-index="{2 + i}">\n    '
            + "\n    ".join(inner) + "\n  </section>")


# ---------------------------------------------------------------- cue sheet
# every value is the exact start of the spoken word it fires on
CUE = {
    "trick": 2.30,          # "one simple trick"
    "cardout": 2.95,        # the card leaves -> 2.95s of screen time (verdict cap 3s)
    "before": 3.26,         # "Before you actually start"
    "task1": 4.54,          # "working on your task"
    "usai": 5.76,           # "actually use AI to do"
    "deep": 7.40,           # KEY TERM debut
    "workflow": 8.24,
    "dock": 9.30,           # the key term demotes into the flow
    "gpt": 9.98, "claude": 10.80, "gemini": 11.42, "grok": 11.94,
    "every": 12.42,         # "every major AI producer"
    "what": 14.56,
    "trigger": 16.46,
    "multiple": 18.20, "agents": 18.74,
    "research": 19.56, "task2": 20.34, "tackle": 21.42,
    "means": 22.14, "allinfo": 23.30, "context": 24.80,
    "remember": 25.48, "aiagent": 26.66,
    "twopara": 27.60, "briefs": 28.56, "intern": 29.44,
    "fullblown": 31.20, "employee": 32.68,
    "read": 34.32, "brought": 36.26,
    "thatway": 37.54, "say": 38.74, "good": 39.36, "notgood": 40.48,
    "produce": 42.16, "app": 42.84, "brief2": 43.70, "anything": 44.46,
    # outro (spoken): "Follow for more AI videos and tutorials each and every single day"
    "follow": 45.60, "aivideos": 46.48, "tutorials": 47.22, "everyday": 48.00,
}

# Beat 3 now holds its comparison until 34.26 instead of handing over at 33.30:
# the run-3 boundary opened a ~1.0s window where beat 4 was live but its first
# element (the research panel, cued on "read" at 34.32) had not landed yet, so the
# top zone rendered as a blank cream field — a dead frame the QC gate calls out.
BEATS = [(0.00, 14.56), (14.56, 25.48), (25.48, 34.26), (34.26, 45.60)]
CTA = 45.60

# tweet hit-box, measured off a printed coordinate grid over the cropped card (984x246):
# the claim paragraph runs y 143-235, x 32-932.
TWEET_CLAIM = (0.0325, 0.581, 0.915, 0.374)

AGENT_LABELS = ["AGENT 01", "AGENT 02", "AGENT 03", "AGENT 04"]
FINDINGS = ["ARCHITECTURE", "APPROACHES", "LIMITATIONS", "TRADE-OFFS", "EDGE CASES"]
GOOD_ROWS = [0, 2, 3]
BAD_ROWS = [1, 4]
# TRANSCRIPT IS TRUTH: he says "your application, your brief, anything that you
# really want" — the nodes carry his words, not an abbreviation of them.
OUTPUTS = ["YOUR APPLICATION", "YOUR BRIEF", "ANYTHING"]


def mono_w(text, fs, track=2.0):
    return round(len(text) * fs * 0.60 + max(0, len(text) - 1) * track, 1)


def hit(x, y, w, h, box, pad=0.012):
    fx, fy, fw, fh = box
    return (round(x + (fx - pad) * w, 1), round(y + (fy - pad) * h, 1),
            round((fw + 2 * pad) * w, 1), round((fh + 2 * pad) * h, 1))


# ---------------------------------------------------------------- shared blocks
def tweet_block(pfx, media, left, top, w):
    """Law 3: the card is the news for 2.95s, metrics cropped off, then it leaves.
    ATTRIBUTION: @XFreeze lives inside this card and nowhere else in the short."""
    el, h = shot(f"{pfx}c", "tweet", left, top, w, media, 16, hide=False)
    r = hit(left, top, w, h, TWEET_CLAIM)
    return [el, ring_el(f"{pfx}r", *r, 9)], h


def tweet_tw(pfx):
    return ([settle(f"#{pfx}c", 0.0), popo(f"#{pfx}r", CUE["trick"], 0.34, 0.9)]
            + leave(f"#{pfx}c", CUE["cardout"], 0.22)
            + leave(f"#{pfx}r", CUE["cardout"], 0.22))


def key_term(pfx, x=38, y=80, w=500, fs=52):
    """Law 9: the video's core term debuts CENTRE STAGE, large, at its first
    utterance, then docks into the waiting slot.

    v1.1 geometry: run 3 debuted the term ON TOP of the empty slot, so the dashed
    border ran straight through the display type. The debut now sits in clear air
    above the slot (33 design px of gap) and the dock is a single downward move."""
    return [txt(f"{pfx}t", "disp", "DEEP RESEARCH", x, y, w, fs, INK, "center",
                extra=" data-overlap-ok"),
            f'<div class="abs" style="left:{px(x + w / 2 - 84)}px;top:{px(y + fs * 1.15)}px;'
            f'width:{px(168)}px;height:{px(5)}px">'
            f'<div id="{pfx}u" class="rule" style="width:100%;height:100%;'
            f'background:{TERRA_L};transform:scaleX(0)"></div></div>']


def key_term_tw(pfx, dock):
    """Debut large, then ONE discrete move into the flow (never a drift)."""
    dx, dy, sc = dock
    return ([slam(f"#{pfx}t", CUE["deep"], 0.38, 1.20),
             sweep(f"#{pfx}u", CUE["workflow"], 0.5)]
            + retract(f"#{pfx}u", CUE["dock"], 0.24)
            + [moveto(f"#{pfx}t", CUE["dock"], dx, dy, 0.62, 0.0, 0.0, sc, 1.0)])


def logo_row(pfx, x, y, size, gap, keys):
    return [logo_tile(f"{pfx}{j}", x + j * (size + gap), y, size, k)
            for j, k in enumerate(keys)]


LOGO_AT = {"openai": CUE["gpt"], "claude": CUE["claude"], "gemini": CUE["gemini"],
           "grok": CUE["grok"], "perplexity": CUE["every"] + 0.14,
           "deepseek": CUE["every"] + 0.30, "copilot": CUE["every"] + 0.46}


def compare_cards(pfx, dark, y=104, cw=240, ch=232, gap=40, title_fs=30):
    """Beat 3 — law 7: same-theme paired cards are the SAME size and never touch.
    Same agent mark on both: only the brief differs."""
    x0 = (576 - (2 * cw + gap)) / 2
    x1 = x0 + cw + gap
    els = [txt(f"{pfx}h", "mono", "same agent", 48, 58, 480, 13,
               ON_DARK_S if dark else INK_S, "center")]
    for s, cx in (("a", x0), ("b", x1)):
        els.append(f'<div id="{pfx}{s}" class="abs card{" od" if dark else ""}" '
                   f'style="left:{px(cx)}px;top:{px(y)}px;width:{px(cw)}px;'
                   f'height:{px(ch)}px;opacity:0"></div>')
        els.append(spark_tile(f"{pfx}g{s}", cx + cw / 2 - 28, y + 18, 56, dark))
    for j in range(2):
        els.append(bar_el(f"{pfx}ba{j}", x0 + 26, y + 104 + j * 30, cw - 52, 16))
    for j in range(6):
        els.append(bar_el(f"{pfx}bb{j}", x1 + 26, y + 104 + j * 22, cw - 52, 13))
    els += [check_el(f"{pfx}k", x1 + cw - 44, y + 16, 26),
            txt(f"{pfx}ta", "disp od" if dark else "disp", "INTERN", x0, y + ch + 22, cw,
                title_fs, ON_DARK_S if dark else INK_S, "center"),
            txt(f"{pfx}tb", "disp od" if dark else "disp", "EMPLOYEE", x1, y + ch + 22, cw,
                title_fs, TERRA_L, "center")]
    return els


def compare_tw(pfx):
    # BUILD ORDER (v1.1): a container must not sit empty waiting for its contents —
    # run 3 held two blank cards for 1.2s before the agent mark arrived. Each card
    # now lands WITH its mark, and the "same agent" claim label lands on the words
    # "an AI agent".
    T = [popo(f"#{pfx}a", CUE["remember"], 0.44, 0.86),
         popo(f"#{pfx}ga", CUE["remember"] + 0.12, 0.36, 0.6),
         popo(f"#{pfx}b", CUE["remember"] + 0.14, 0.44, 0.86),
         popo(f"#{pfx}gb", CUE["remember"] + 0.26, 0.36, 0.6),
         fade(f"#{pfx}h", CUE["aiagent"], 0.35)]
    for j in range(2):
        T.append(rise(f"#{pfx}ba{j}", CUE["twopara"] + j * 0.18, 12, 0.34))
    T.append(slam(f"#{pfx}ta", CUE["intern"], 0.36, 1.16))
    for j in range(6):
        T.append(rise(f"#{pfx}bb{j}", CUE["fullblown"] + j * 0.11, 12, 0.32))
    T += [slam(f"#{pfx}tb", CUE["employee"], 0.36, 1.16),
          popo(f"#{pfx}k", CUE["employee"] + 0.22, 0.36, 0.4)]
    return T


REV_X, REV_Y, REV_W, REV_RH = 36.0, 118.0, 306.0, 44.0
REV_H = 18 + len(FINDINGS) * REV_RH + 10
OUT_X, OUT_YS, OUT_W, OUT_H = 372.0, (142.0, 218.0, 294.0), 172.0, 54.0


def review_block(pfx, dark):
    """Beat 4 — the research comes back, he keeps the good rows and kills the rest."""
    x, y, w, rh = REV_X, REV_Y, REV_W, REV_RH
    els = [panel_el(f"{pfx}p", x, y, w, REV_H, dark),
           txt(f"{pfx}h", "mono", "research", x + 18, y - 26, 150, 12,
               ON_DARK_S if dark else INK_S, "left"),
           txt(f"{pfx}v", "mono", "verdict", x + w - 158, y - 26, 150, 12,
               ON_DARK_S if dark else INK_S, "right")]
    for j, lab in enumerate(FINDINGS):
        ry = y + 18 + j * rh
        els.append(txt(f"{pfx}r{j}", "mono", lab, x + 22, ry + 12, w - 96, 13,
                       ON_DARK if dark else INK, "left"))
        els.append(strike_el(f"{pfx}s{j}", x + 18, ry + 19, mono_w(lab, 13) + 8,
                             2.4, ON_DARK_S if dark else INK_S))
        if j in GOOD_ROWS:
            els.append(check_el(f"{pfx}k{j}", x + w - 50, ry + 6, 24))
        else:
            els.append(x_el(f"{pfx}x{j}", x + w - 50, ry + 6, 24,
                            ON_DARK_S if dark else INK_S))
    for j, lab in enumerate(OUTPUTS):
        els.append(node_el(f"{pfx}o{j}", OUT_X, OUT_YS[j], OUT_W, OUT_H, lab, 12,
                           dark=dark, hero=(j == 0), ls=1.2))
        els.append(arrow_to(f"{pfx}a{j}", x + w + 6, y + REV_H / 2,
                            OUT_X, OUT_YS[j] + OUT_H / 2))
    return els


def review_tw(pfx):
    # BUILD ORDER (v1.1): run 3 held an empty white panel for 1.9s before the first
    # finding arrived — chrome before content. The findings now start filling it
    # 0.5s after it lands and the cascade is paced so the last row arrives exactly
    # on "brought", keeping the claim in sync.
    T = [popo(f"#{pfx}p", CUE["read"], 0.45, 0.9), fade(f"#{pfx}h", CUE["read"] + 0.24, 0.35)]
    for j in range(len(FINDINGS)):
        T.append(slidex(f"#{pfx}r{j}", CUE["read"] + 0.54 + j * 0.32, -14, 0.34))
    T.append(fade(f"#{pfx}v", CUE["thatway"], 0.35))
    for i, j in enumerate(GOOD_ROWS):
        T.append(popo(f"#{pfx}k{j}", CUE["good"] + i * 0.14, 0.34, 0.4))
    for i, j in enumerate(BAD_ROWS):
        T.append(popo(f"#{pfx}x{j}", CUE["notgood"] + i * 0.16, 0.34, 0.4))
        T.append(sweep(f"#{pfx}s{j}", CUE["notgood"] + 0.08 + i * 0.16, 0.34))
    # BUILD ORDER (v1.1): the node lands on the word, THEN its connector is drawn.
    ots = [CUE["app"], CUE["brief2"], CUE["anything"]]
    for j in range(3):
        T.append(popo(f"#{pfx}o{j}", ots[j], 0.4, 0.74))
        T += arrow_in(f"{pfx}a{j}", ots[j] + 0.20, 0.30)
    return T


# ================================================================= LANE: diagram
def lane_diagram(C):
    """Diagram build — one prompt fans into researchers and converges into one brief."""
    m = C["media"]
    Z, T = [], []

    # ---- beat 1 : the news, an empty slot before the task, then who this runs on
    t0, t1 = BEATS[0]
    size, gap = 50.0, 14.0
    gx = (576 - (7 * size + 6 * gap)) / 2                    # 71.0
    H = logo_row("p1", gx, 84, size, gap, ALL_LOGOS)
    for j in range(7):
        H.append(line_el(f"st1{j}", gx + size / 2 + j * (size + gap), 134, 18, 90.0))
    H += [line_el("bus1", gx + size / 2, 152, 6 * (size + gap)),
          line_el("bus1c", 288, 152, 16, 90.0),
          node_el("dash1", 168, 168, 240, 62, "", 15, dash=True),
          node_el("hero1", 168, 168, 240, 62, "", 15, hero=True),
          arrow("a1", 288, 230, 62, 90.0),
          node_el("task1", 178, 292, 220, 58, "YOUR TASK", 15)]
    H += key_term("k1", 38, 80, 500, 52)
    card, _ = tweet_block("t1", m, 53, 168, 470)
    H += card
    Z.append(zone(0, t0, t1, "cream", H))
    T += tweet_tw("t1")
    T += [popo("#task1", CUE["before"], 0.44, 0.82),
          popo("#dash1", CUE["task1"], 0.44, 0.84)]
    T += arrow_in("a1", CUE["usai"], 0.42)
    # debut centre 80+27.3 = 107.3 -> slot centre 199.0  => dy +91.7
    T += key_term_tw("k1", dock=(0.0, 91.7, 0.42))
    T += leave("#dash1", CUE["dock"] + 0.24, 0.26)
    T.append(fade("#hero1", CUE["dock"] + 0.3, 0.36))
    for j, k in enumerate(ALL_LOGOS):
        T.append(popo(f"#p1{j}", LOGO_AT[k], 0.36, 0.66))
    # BUILD ORDER (v1.1): the wiring is laid only once every node it joins exists —
    # all seven logos land first, then the rail, then each tap-in stem, then the drop
    # into the hero. Run 3 grew 4 of the 7 stems before their own logo; drawing them
    # on their logo instead just moved the dangle to the other end (a stem hanging
    # toward a rail that was not there yet), so the whole harness now goes last.
    T.append(sweep("#bus1", 13.02, 0.5))
    for j in range(7):
        T.append(sweep(f"#st1{j}", 13.56 + j * 0.05, 0.22))
    T.append(sweep("#bus1c", 14.06, 0.26))

    # ---- beat 2 : the fan-out and the convergence — the hero move of this lane
    t0, t1 = BEATS[1]
    aw, agap = 118.0, 14.0
    ax0 = (576 - (4 * aw + 3 * agap)) / 2                    # 31.0
    # The beat opens on the SHAPE it is about to fill: YOUR TASK plus the waiting
    # dashed silhouette of the hub, both painted on the section's very first frame
    # (pre-rolled, so the tween runs while the clip is still hidden). Run 4 round 1
    # held a lone 180x46 pill on empty cream for 1.9s here — the weakest frame in
    # the short. This is the lane's own slot->content language (beat 1 does the
    # same dash -> hero swap), not chrome standing before content.
    H = [node_el("d2t", 198, 56, 180, 46, "YOUR TASK", 14),
         node_el("d2ds", 168, 134, 240, 56, "", 15, dash=True),
         node_el("d2h", 168, 134, 240, 56, "DEEP RESEARCH", 15, hero=True),
         arrow("d2a", 288, 102, 32, 90.0)]
    for j in range(4):
        cx = ax0 + j * (aw + agap)
        H.append(node_el(f"d2n{j}", cx, 228, aw, 44, AGENT_LABELS[j], 12))
        H.append(arrow_to(f"d2f{j}", 288, 190, cx + aw / 2, 228))
        H.append(meter_el(f"d2m{j}", cx + 18, 282, aw - 36, 8))
        H.append(line_to(f"d2c{j}", cx + aw / 2, 296, 288, 314))
    # SEAM IS SACRED (v1.1): the whole convergence block sits 8 design units higher
    # than round 1, so the lowest ink in this beat is the panel bottom at design
    # y=402 (753.8px) — 51px clear of the caption pill's painted top edge (~805px),
    # instead of the 787.5px ring that used to sit 17px off it.
    H += [panel_el("d2b", 128, 314, 320, 88),
          txt("d2bl", "mono", "your context", 152, 322, 200, 11, INK_S, "left")]
    for j in range(4):
        H.append(bar_el(f"d2s{j}", 152, 342 + j * 14, 272 - (j % 2) * 46, 9))
    Z.append(zone(1, t0, t1, "cream", H))
    T.append(fade("#d2ds", t0 - 0.34, 0.30))
    T.append(popo("#d2t", CUE["what"], 0.44, 0.82))
    # BUILD ORDER: the hub node lands first, the arrow that joins it follows.
    T.append(popo("#d2h", CUE["trigger"], 0.44, 0.84))
    T += leave("#d2ds", CUE["trigger"] + 0.22, 0.24)
    T += arrow_in("d2a", CUE["trigger"] + 0.46, 0.32)
    for j in range(4):
        T.append(popo(f"#d2n{j}", CUE["multiple"] + j * 0.14, 0.34, 0.7))
        T += arrow_in(f"d2f{j}", CUE["agents"] + j * 0.12, 0.34)
        T.append(fade(f"#d2m{j}w", CUE["research"] + j * 0.10, 0.28))
        # METERS COMPLETE (v1.1): every fill bar reaches full.
        T.append(sweep(f"#d2m{j}", CUE["research"] + 0.16 + j * 0.10, 0.5, 1.0))
    T += [popo("#d2b", CUE["means"], 0.44, 0.9), fade("#d2bl", CUE["means"] + 0.3, 0.32)]
    # BUILD ORDER: the convergence lines are drawn only once the panel they land on exists.
    for j in range(4):
        T.append(sweep(f"#d2c{j}", CUE["means"] + 0.46 + j * 0.09, 0.34))
    for j in range(4):
        T.append(rise(f"#d2s{j}", CUE["allinfo"] + j * 0.13, 12, 0.32))
    # HIGHLIGHT DISCIPLINE (v1.1): round 1 put a terracotta ring around this panel,
    # but the four convergence connectors terminate on the panel's TOP edge, so the
    # ring's border was crossed by all four and read as broken (the meatwrapper
    # finding: never ring a node that connectors land on). The highlight is now the
    # panel's OWN border going terracotta on "your context" — same region, same
    # discrete event, nothing crosses it, and no ink moves toward the seam.
    # (colour written as rgb() so the id self-check does not read "#DD7259" as a selector)
    T.append(f'tl.fromTo("#d2b",{{borderColor:"rgba(17,17,17,0.16)"}},'
             f'{{borderColor:"rgb(221,114,89)",duration:0.38,ease:SOFT}},'
             f'{CUE["context"]:.2f});')

    # ---- beat 3 : two briefs, one agent, identical card size
    t0, t1 = BEATS[2]
    Z.append(zone(2, t0, t1, "dark", compare_cards("d3", True)))
    T += compare_tw("d3")

    # ---- beat 4 : read it, keep the good rows, feed what you build
    t0, _ = BEATS[3]
    Z.append(zone(3, t0, CTA, "cream", review_block("d4", False)))
    T += review_tw("d4")
    return Z, T


# ---------------------------------------------------------------- outro
def outro(t0, dur):
    """OUTRO ALIGNMENT (v1.1): ONE centred composition on the vertical axis —
    FOLLOW centred at the top, three equal nodes centred beneath it, arrows that
    point at nodes that are actually on screen, then the serif payoff and the
    handle chip on the same axis. Nothing floats off-axis, nothing reaches the
    seam (lowest ink clears it by 72 design px)."""
    H, T = [], []
    d = dur - t0

    hw, hh, hy = 268.0, 76.0, 76.0
    hx = (576 - hw) / 2                                      # 154.0
    H.append(node_el("ohn", hx, hy, hw, hh, "FOLLOW", 20, hero=True, ls=3.0))
    T.append(popo("#ohn", CUE["follow"] + 0.06, 0.5, 0.78))

    nw, nh, ngap, ny = 152.0, 52.0, 28.0, 216.0
    nx0 = (576 - (3 * nw + 2 * ngap)) / 2                    # 32.0
    labels = ["AI VIDEOS", "TUTORIALS", "EVERY DAY"]
    ats = [CUE["aivideos"], CUE["tutorials"], CUE["everyday"]]
    tails = [(hx + 54, hy + hh), (288.0, hy + hh), (hx + hw - 54, hy + hh)]
    for j, lab in enumerate(labels):
        cx = nx0 + j * (nw + ngap)
        H.append(node_el(f"on{j}", cx, ny, nw, nh, lab, 13))
        H.append(arrow_to(f"oa{j}", tails[j][0], tails[j][1], cx + nw / 2, ny, 2.4,
                          TERRA_L, 10.0))
        # BUILD ORDER: node first, then the connector that points at it.
        T.append(popo(f"#on{j}", ats[j], 0.4, 0.74))
        T += arrow_in(f"oa{j}", ats[j] + 0.22, 0.28)

    H += [txt("od", "serif", "one drop a day", 48, 296, 480, 32, TERRA_L, "center"),
          f'<div id="oe" class="abs" style="left:0;top:{px(350)}px;width:{px(576)}px;'
          f'text-align:center;opacity:0"><span class="ctchip" style="font-size:{px(16)}px">'
          f'Miguel Torrez AI</span></div>']
    T += [fade("#od", CUE["everyday"] + 0.62, 0.4), rise("#oe", CUE["everyday"] + 1.00, 12, 0.4)]

    zone_html = (f'  <section id="tz-outro" class="clip tz cream" data-start="{t0:.2f}" '
                 f'data-duration="{d:.2f}" data-track-index="6">\n    '
                 + "\n    ".join(H) + "\n  </section>")
    return zone_html, T


# ---------------------------------------------------------------- page
def build_html(C, phrases):
    dur = C["dur"]
    zones, tws = lane_diagram(C)
    outro_html, otw = outro(CTA, dur)
    zones = zones + [outro_html]
    tws += otw

    face = (f'  <video id="facebot" src="assets/v/{VID}/face_bottom.mp4" data-start="0" '
            f'data-duration="{dur:.2f}" data-media-start="0" data-track-index="1" muted '
            f'playsinline style="position:absolute;top:{px(SEAM)}px;left:0;width:1080px;'
            f'height:{px(FACE_H)}px;object-fit:cover"></video>')
    audio, atw = audio_block(dur, BEATS, CTA)
    tws += atw

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=1080, height=1920"/>
<title>{VID} — Diagram build (run 4)</title>
{GSAP}
{FONTS}
<style>
{base_css()}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920"
     data-duration="{dur:.2f}" data-fps="{FPS}">

{face}

{chr(10).join(zones)}

{caption_clips(phrases, dur)}

{audio}
</div>

<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
const POP = "back.out(2.2)";
const SOFT = "power3.out";
const SLAM = "power4.out";
{chr(10).join(tws)}
window.__timelines["main"] = tl;
</script>
</body>
</html>"""
    audit(html, tws)
    return html


def audit(html, tws):
    """Sibling learning: duplicate DOM ids silently retarget tweens. Fail the build
    loudly, and refuse to ship a tween pointing at an id that does not exist."""
    ids = re.findall(r'\sid="([^"]+)"', html)
    dupes = [k for k, v in Counter(ids).items() if v > 1]
    if dupes:
        raise SystemExit(f"[{LANE}] duplicate DOM ids: {sorted(dupes)}")
    known = set(ids)
    missing = sorted({s for s in re.findall(r'"#([A-Za-z0-9_\-]+)"', "\n".join(tws))
                      if s not in known})
    if missing:
        raise SystemExit(f"[{LANE}] tweens target unknown ids: {missing}")


# ---------------------------------------------------------------- staging
def round_corners(im, radius_at_1000=22):
    w, h = im.size
    r = int(round(radius_at_1000 * w / 1000.0))
    mask = Image.new("L", (w * 2, h * 2), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w * 2 - 1, h * 2 - 1], radius=r * 2, fill=255)
    mask = mask.resize((w, h), Image.LANCZOS)
    out = im.convert("RGBA")
    out.putalpha(mask)
    return out


def link(target: Path, dest: Path):
    if dest.is_symlink() or dest.exists():
        dest.unlink()
    dest.symlink_to(target.resolve())


def stage():
    """Local-only staging (no network): the run-1 x_card PNG, the workspace logo
    library, the factory audio bed/sfx, and symlinks to the run-1 cut."""
    for d in ["music", "sfx", "img/logos", "v"]:
        (STAGE / d).mkdir(parents=True, exist_ok=True)
    pub = FACTORY / "pipeline/assets"
    shutil.copy2(pub / "bed_split.mp3", STAGE / "music/bed_split.mp3")
    for s in ["pop", "whoosh", "boom", "ding"]:
        shutil.copy2(pub / f"{s}.mp3", STAGE / "sfx" / f"{s}.mp3")

    m = {}
    # law 3 + law 8: crop to the header and the one claim paragraph. The metrics row
    # (source y>=600) never reaches the frame, and the type stays phone-large.
    card = Image.open(CARD).convert("RGB")
    tw = round_corners(card.crop((8, 12, 992, 258)))
    tw.save(STAGE / "img/tweet.png")
    m["tweet"] = ("assets/img/tweet.png", tw.size)

    for key, rel in LOGO_SRC.items():
        Image.open(LOGOS / rel).convert("RGBA").save(STAGE / "img/logos" / f"{key}.png")

    vd = STAGE / "v" / VID
    vd.mkdir(exist_ok=True)
    cut = RUN1 / "cuts" / STEM
    for f in ["face_bottom.mp4", "audio.m4a"]:
        link(cut / f, vd / f)
    return m


def timings():
    cut = RUN1 / "cuts" / STEM
    words = [w for w in json.loads((cut / "transcript_tight.json").read_text())["words"]
             if w["type"] == "word"]
    dur = round(min(words[-1]["end"] + 0.6, probe(cut / "face_bottom.mp4"),
                    probe(cut / "audio.m4a")), 2)
    return words, dur


# ---------------------------------------------------------------- main
if __name__ == "__main__":
    media = stage()
    words, dur = timings()
    phrases = build_captions(words)
    C = {"media": media, "dur": dur}
    PROJ.mkdir(parents=True, exist_ok=True)
    d = PROJ / f"{VID}_{LANE}"
    d.mkdir(parents=True, exist_ok=True)
    a = d / "assets"
    if a.is_symlink():
        a.unlink()
    elif a.exists():
        shutil.rmtree(a)
    a.symlink_to(STAGE.resolve(), target_is_directory=True)
    (d / "index.html").write_text(build_html(C, phrases))
    print(f"BUILD DONE  {d}  dur={dur:.2f} cta={CTA:.2f} beats={BEATS} caps={len(phrases)}")
