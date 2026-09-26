"""hermes / ICON CHOREOGRAPHY — run 5 (STANDARD v1.1 + the impeccable design pass).

Lineage: shorts_run3/gen3/hermes_gen.py -> shorts_run4/gen/hermes_icon_gen.py -> here.
The run-4 fork is the one that already carries every pilot-verdict fix (and two more
that only a painted-pixel seam measurement found), so run 5 forks THAT rather than
re-deriving them from run 3 and re-shipping known defects.
Same chassis: design space 576x1024 scaled by S=1.875 into 1080x1920, seam at design
y=460, terracotta caption pills riding the seam, face_bottom below the seam, identical
audio bed/sfx, event-only tweens (law 1: motion is an event, then the element HOLDS).

v1.1 FIXES APPLIED (Miguel's pilot verdict, 2026-08-10):
  1. TRANSCRIPT IS TRUTH — the key-term card reads "PROCEDURAL DISCLOSURE".
     Miguel says "procedural" at 11.88; run 3 printed "PROGRESSIVE" and that card
     is the defect, not the transcript. No agent re-litigates this.
  2. ASSET HEALTH — the n8n mark is the 3-dot/2-line "connection" glyph that renders
     broken at tile size (thin pink outlines, no mass). Replaced with Google Drive
     (solid, real MCP server). The OpenRouter asset was a BLACK ROUNDED SQUARE, i.e.
     a plate inside our white plate; replaced with the purple glyph cropped out of
     openrouter.svg so every tile is artwork-on-plate, never plate-on-plate.
  3. LAW 8 / upscaled — ladder.png (362x352 raster blown up to 465px, ~11px fine print,
     plus an orphan "1." ordinal from the source article) is GONE. Its content is now
     a coded 3-tier card stack: catalog size -> what the agent is given. Same facts,
     real type, no raster, no orphan ordinal, no attribution debt.
  4. FILL THE SHAPE — the free-floating circle check is gone; the "solved" mark is a
     rounded-square badge sharing the logo plates' corner ratio, seated in the
     centred active-tool stack.
  5. BUILD ORDER — every connector fires after both nodes it joins.
  6. OUTRO ALIGNMENT — one centred composition (logo row / node / payoff / handle chip
     all on x=288), no zero-ink wrapper, 150px of air above the seam.
  7. SEAM IS SACRED — the run-3 outro wrapper's bottom edge WAS the seam (an ERROR
     under v1.1). Elements are now placed directly in the section.
  8. HIGHLIGHT DISCIPLINE — the beat-1 ring lands on the Nous Research lockup when he
     says "crack the code" (run 3 ringed an arbitrary tool tile: semantic mismatch).
  9. Arrows: the shaft now spans the FULL length with the head overlaid on its last
     px, so both measured ends land exactly on the box edges they join (law 7), and
     the audit's floating-connector warnings go away honestly.
 10. SEAM IS SACRED measured on PAINTED pixels, not layout boxes: a compile-time seam
     budget (seam_guard) hard-fails any atom whose estimated ink bottom crosses design
     y 410, because the caption pill's painted top edge is y~429, not the 460 seam.

RUN 5 — impeccable pass (product register: this top zone is an instrument panel, so
design SERVES the read). STANDARD.md still wins every conflict: same cream/charcoal/
terracotta tokens, same Poppins/Instrument Serif/JetBrains Mono voice, same lane
language. What the pass changed, and why:
  A. beat 1 — the stats line stayed at full strength while the grid dimmed, so the
     loudest thing on screen at "crack the code" was not the ringed subject. It now
     dims WITH the grid it describes (hierarchy).
  B. beat 2 — the tier cards carried a 6px terracotta side-stripe whose opacity
     encoded "how much of the catalog the agent gets". A coloured side-stripe is a
     hard impeccable ban and the opacity ramp was data nobody can decode. Both gone;
     the numbers and the outcomes are the data.
  C. beat 2 — the row was a floating cluster (28px of padding on the left, 14 on the
     right). It is now a real four-column grid with symmetric 24px padding.
  D. beat 2 — "tools" was the one lowercase label in an all-uppercase mono system;
     and its arrow used TERRA, the ON-CREAM accent, on a dark card. Both aligned to
     the system's own rules (uppercase mono, TERRA_L for line work on dark).
  E. beat 3 — the odometer printed 34% / 88% / 12%. Those numbers are spoken NOWHERE
     in the transcript (run 4 filed this as still-open). Invented figures are claims;
     they are gone. The capsule is a gauge, and it reads without a numeral.
  F. beat 3 — the gauge now reaches FULL exactly on "context is finite" (METERS
     COMPLETE, and the honest reading of the sentence), then drops to lean on "give
     access". Three states, no numerals: fills, full, lean.
  G. beat 3 — the capsule was 196 tall and floated; it is 232 tall and shares the
     tool grid's bottom edge, so the two outer columns bottom-align on one line.
  H. beat 3 — a terracotta check badge floated under the ACTIVE label, attached to
     nothing. Deleted. "No longer have to worry" is now carried by the object that
     already means it: the dormant grid relights in two steps (0.24 -> 0.62 on "all
     of the tools", -> 1.00 on "no longer worry").
  I. beat 4 — the "6%" numeral is invented too, and it sat on a different baseline
     from its own label. Gone; the bar keeps the vocabulary beat 3 established.
  J. beat 4 — the Hermes card held the logo inside a white plate ON a white card, a
     nested container with a visible hairline box. The card IS the plate.
  K. beat 4 — the two stacked hero nodes were 64 and 78 tall. Same role, same size.

Binding asset verdicts (shorts_run3/plans/asset_verdicts_v3.json, hermes):
  input_file_0 = x_card  -> use, max 3.5s (metrics row CROPPED OFF: law 3)
  input_file_1 = photo:0 -> superseded: unreadable at short size, replaced by code
  input_file_2 = photo:1 -> REJECT (bench table) — never staged.
"""
import html as ihtml
import io
import json
import re
import shutil
import subprocess
from pathlib import Path

import cairosvg
import numpy as np
from PIL import Image, ImageDraw

FACTORY = Path.home() / "Documents/Workspace/projects/personal/content/shorts-factory"
RUN1 = FACTORY / "shorts_run1"
R5 = FACTORY / "shorts_run5"
STAGE = R5 / "gen/_stage_hermes_icon"
PROJ = R5 / "projects"
LOGOS = Path.home() / "Documents/Workspace/assets/logos"
VID = "hermes"
LANE = "icon"

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
TERRA = "#C66748"
TERRA_L = "#DD7259"
CAP_TERRA = "#C4573A"
ON_DARK = "#F3EEE6"
ON_DARK_S = "#9C978D"
CARD_D = "#1C1C21"
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

# 12 real MCP-server logos (law 2: a named tool renders as its logo, never a text pill).
# n8n dropped: its mark is the broken 3-dot/2-line connection glyph (ASSET HEALTH).
MCP = ["github", "slack", "notion", "figma", "apify", "exa",
       "gdrive", "make", "modal", "youtube", "openrouter", "gmaps"]
MCP_SRC = {
    "github": "coding-tools/github-mark.png",
    "slack": "platforms/slack-color.png",
    "notion": "platforms/notion-color.png",
    "figma": "design-tools/figma-color.png",
    "apify": "platforms/apify-color.png",
    "exa": "platforms/exa-color.png",
    "make": "automation/make-color.png",
    "modal": "automation/modal-color.png",
    "youtube": "platforms/youtube-color.png",
    "gmaps": "platforms/google-maps-color.png",
    "nous": "ai-models/nous-research.png",
}


def esc(s):
    return ihtml.escape(str(s), quote=False)


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(r.stdout.strip())


# ---------------------------------------------------------------- tweens (event-only)
def rise(sel, t, dy=22, d=0.42, e="SOFT"):
    return (f'tl.fromTo("{sel}",{{y:{px(dy)},opacity:0}},'
            f'{{y:0,opacity:1,duration:{d},ease:{e}}},{t:.2f});')


def slidex(sel, t, dx=-22, d=0.4):
    return (f'tl.fromTo("{sel}",{{x:{px(dx)},opacity:0}},'
            f'{{x:0,opacity:1,duration:{d},ease:SOFT}},{t:.2f});')


def fade(sel, t, d=0.4, to=1, frm=0):
    return f'tl.fromTo("{sel}",{{opacity:{frm}}},{{opacity:{to},duration:{d},ease:SOFT}},{t:.2f});'


def popo(sel, t, d=0.36, s=0.78):
    return (f'tl.fromTo("{sel}",{{scale:{s},opacity:0}},'
            f'{{scale:1,opacity:1,duration:{d},ease:POP}},{t:.2f});')


def slam(sel, t, d=0.34, s=1.20):
    return (f'tl.fromTo("{sel}",{{scale:{s},opacity:0}},'
            f'{{scale:1,opacity:1,duration:{d},ease:SLAM}},{t:.2f});')


def settle(sel, t, s0=0.965, d=0.5):
    """Frame-0 composition: already opaque, eases into place once, then holds."""
    return (f'tl.fromTo("{sel}",{{scale:{s0}}},{{scale:1,duration:{d},'
            f'ease:SOFT}},{t:.2f});')


def sweep(sel, t, d=0.45, to=1, frm=0):
    return f'tl.fromTo("{sel}",{{scaleX:{frm}}},{{scaleX:{to},duration:{d},ease:SOFT}},{t:.2f});'


def sweepy(sel, t, d=0.45, to=1, frm=0):
    return f'tl.fromTo("{sel}",{{scaleY:{frm}}},{{scaleY:{to},duration:{d},ease:SOFT}},{t:.2f});'


def setopa(sel, t, v):
    return f'tl.set("{sel}",{{opacity:{v}}},{t:.2f});'


def hardkill(sel, t):
    return setopa(sel, t, 0)


def leave(sel, t, d=0.3):
    """Discrete exit: fade out, then a hard kill so nothing lingers on a clip boundary."""
    return [fade(sel, t, d, 0, 1), hardkill(sel, t + d)]


# ---------------------------------------------------------------- captions
STUTTER = {"uh", "um", "huh", "mm", "mmm", "hmm", "erm", "ah", "eh"}


def clean_words(words):
    """Law 6: stutters and false starts never reach the captions."""
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
.serifup {{ font-family:'Instrument Serif',serif; line-height:1.0; }}
.mono {{ font-family:'JetBrains Mono',monospace; letter-spacing:{px(2.2)}px;
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
/* meter fills are NOT connectors: they carry their own class so the geometry audit
   stops scoring a partial fill's inner end as a floating connector end. */
.mfill {{ display:block; transform-origin:left center; background:{TERRA}; }}
.mfillY {{ display:block; transform-origin:bottom center; background:{TERRA}; }}
.ring {{ border-style:solid; }}
.node {{ border-radius:{px(14)}px; border:{px(2)}px solid rgba(17,17,17,0.20);
  background:#FFFFFF; display:flex; align-items:center; justify-content:center;
  text-align:center; font-family:'JetBrains Mono',monospace; color:{INK}; }}
.node.hero {{ border-color:{TERRA_L}; }}
.node.od {{ background:{CARD_D}; border-color:rgba(255,255,255,0.20); color:{ON_DARK}; }}
.node.od.hero {{ border-color:{TERRA_L}; }}
.tier {{ border-radius:{px(14)}px; border:{px(2)}px solid rgba(255,255,255,0.20);
  background:{CARD_D}; }}
.chip {{ display:inline-block; border-radius:{px(999)}px; background:rgba(198,103,72,0.13);
  color:{TERRA}; font-family:'JetBrains Mono',monospace; padding:{px(6)}px {px(15)}px;
  text-transform:uppercase; letter-spacing:{px(1.8)}px; white-space:nowrap; }}
.chip.od {{ background:rgba(221,114,89,0.22); color:{TERRA_L}; }}
.ctchip {{ display:inline-block; background:rgba(16,16,18,0.62); color:{CREAM};
  font-family:'JetBrains Mono',monospace; border-radius:{px(999)}px;
  padding:{px(9)}px {px(22)}px; letter-spacing:{px(2)}px; white-space:nowrap; }}
.scap {{ left:0; width:1080px; text-align:center; }}
.scappill {{ display:inline-block; transform:translateY(-50%); background:{CAP_TERRA};
  color:#fff; font-family:Nunito,sans-serif; font-weight:800;
  padding:{px(10)}px {px(18)}px; border-radius:{px(12)}px; white-space:nowrap; }}
"""


# ---------------------------------------------------------------- element helpers
def txt(tid, cls, text, left, top, w, fs, color=None, align="left", hide=True):
    c = f"color:{color};" if color else ""
    o = "opacity:0;" if hide else ""
    return (f'<div id="{tid}" class="abs {cls}" style="left:{px(left)}px;top:{px(top)}px;'
            f'width:{px(w)}px;font-size:{px(fs)}px;text-align:{align};{c}{o}">'
            f'{esc(text)}</div>')


def chip_el(cid, text, left, top, w, fs=14, align="left", dark=False):
    return (f'<div id="{cid}" class="abs" style="left:{px(left)}px;top:{px(top)}px;'
            f'width:{px(w)}px;text-align:{align};opacity:0">'
            f'<span class="chip{" od" if dark else ""}" style="font-size:{px(fs)}px">'
            f'{esc(text)}</span></div>')


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


def nous_mark(nid, x, y, size=42, fs=16, dark=False):
    """Nous Research lockup: the logo (never a text pill) plus its wordmark."""
    col = ON_DARK if dark else INK
    tw = fs * 10.6
    return (f'<div id="{nid}" class="abs" style="left:{px(x)}px;top:{px(y)}px;'
            f'width:{px(size + 12 + tw)}px;height:{px(size)}px;opacity:0">'
            f'<div class="abs ltile" style="left:0;top:0;width:{px(size)}px;'
            f'height:{px(size)}px;border-radius:{px(size * 0.24)}px">'
            f'<img src="assets/img/logos/nous.png" alt="" style="width:{px(size * 0.76)}px;'
            f'height:{px(size * 0.76)}px;object-fit:contain"/></div>'
            f'<div class="abs mono" style="left:{px(size + 12)}px;'
            f'top:{px((size - fs * 1.2) / 2)}px;width:{px(tw)}px;'
            f'font-size:{px(fs)}px;color:{col}">Nous Research</div></div>')


def nous_mark_w(size=42, fs=16):
    return size + 12 + fs * 10.6


def node_el(nid, x, y, w, h, label, fs=15, dark=False, hero=False, ls=1.6, hide=True):
    """`hide=False` renders the node already opaque so it can carry the FIRST painted
    frame of its zone (pair it with settle(), the frame-0 vocabulary the tweet card
    uses). Every other node stays hidden and is brought in by an event tween."""
    cls = "node" + (" od" if dark else "") + (" hero" if hero else "")
    return (f'<div id="{nid}" class="abs {cls}" style="left:{px(x)}px;top:{px(y)}px;'
            f'width:{px(w)}px;height:{px(h)}px;font-size:{px(fs)}px;'
            f'letter-spacing:{px(ls)}px;{"opacity:0" if hide else ""}">{esc(label)}</div>')


def ring_el(rid, x, y, w, h, rad=12, color=TERRA_L, thick=3.0):
    return (f'<div id="{rid}" class="abs ring" style="left:{px(x)}px;top:{px(y)}px;'
            f'width:{px(w)}px;height:{px(h)}px;border-radius:{px(rad)}px;'
            f'border-width:{px(thick)}px;border-color:{color};opacity:0"></div>')


def arrow(aid, x, y, length, deg=0.0, thick=3.0, color=TERRA, head=13.0):
    """Law 7: the arrow terminates AT the target box edge.

    The shaft spans the FULL length and the head triangle is overlaid on its last
    `head` px in the same colour (seamless). Run 3 appended the head past the shaft,
    so the measured connector end stopped 13px short of the box it pointed at and the
    geometry audit reported it as a floating connector on every arrow.
    """
    hh = head * 0.60
    return (f'<div class="abs" style="left:{px(x)}px;top:{px(y - thick / 2)}px;'
            f'width:{px(length)}px;height:{px(thick)}px;'
            f'transform:rotate({deg:.2f}deg);transform-origin:left center">'
            f'<div id="{aid}" class="rule" style="width:{px(length)}px;height:100%;'
            f'background:{color};transform:scaleX(0)"></div>'
            f'<div id="{aid}h" class="abs" style="left:{px(length - head)}px;'
            f'top:{px(thick / 2 - hh)}px;width:0;height:0;opacity:0;'
            f'border-left:{px(head)}px solid {color};'
            f'border-top:{px(hh)}px solid transparent;'
            f'border-bottom:{px(hh)}px solid transparent"></div></div>')


def arrow_in(aid, t, d=0.4):
    return [sweep(f"#{aid}", t, d), popo(f"#{aid}h", t + d * 0.8, 0.26, 0.3)]


def meter_el(mid, x, y, w, h, track=TRACK_L, fill=TERRA, rad=None):
    """FILL THE SHAPE: fill radius always equals track radius.

    `rad` exists because a pill radius (h/2) turns a small fill into a SLIDER KNOB —
    this lane's context bar lands at 6%, i.e. 13.7 design px on a 16px track, which at
    r8 is a circle. At r5 the same fill reads as a short bar and the fill still shares
    the track's corner geometry.
    """
    r = h / 2 if rad is None else rad
    return (f'<div id="{mid}w" class="abs" style="left:{px(x)}px;top:{px(y)}px;'
            f'width:{px(w)}px;height:{px(h)}px;background:{track};'
            f'border-radius:{px(r)}px;overflow:hidden;opacity:0">'
            f'<div id="{mid}" class="mfill" style="width:100%;height:100%;'
            f'background:{fill};border-radius:{px(r)}px;transform:scaleX(0)"></div></div>')


def capsule_el(cid, x, y, w, h, track=TRACK_D, fill=TERRA):
    """Vertical context meter that fills from the bottom.

    The fill uses `.mfillY`, not `.ruleY`: a half-full meter's inner end is not a
    connector end, and run 3 shipped a permanent `ctx3w end ... touches no box edge`
    warning because the audit could not tell the two apart.
    """
    return (f'<div id="{cid}w" class="abs" style="left:{px(x)}px;top:{px(y)}px;'
            f'width:{px(w)}px;height:{px(h)}px;background:{track};'
            f'border-radius:{px(18)}px;overflow:hidden;opacity:0">'
            f'<div id="{cid}" class="mfillY abs" style="left:0;bottom:0;width:100%;'
            f'height:100%;background:{fill};transform:scaleY(0)"></div></div>')


def bare_logo(lid, x, y, size, key, hide=True):
    """A logo with NO plate, for use on a surface that is already the plate.

    run 5 / impeccable: the beat-4 Hermes card is a white node; run 4 put the Nous
    mark inside a white `.ltile` on it, so the card carried a nested container with a
    visible hairline and its own shadow — a box inside a box for no gain.
    """
    return (f'<div id="{lid}" class="abs" style="left:{px(x)}px;top:{px(y)}px;'
            f'width:{px(size)}px;height:{px(size)}px;{"opacity:0;" if hide else ""}">'
            f'<img src="assets/img/logos/{key}.png" alt="" style="width:100%;height:100%;'
            f'object-fit:contain"/></div>')


def zone(i, t0, t1, bg, inner, extra_dur=OVERLAP):
    return (f'  <section id="tz-b{i + 1}" class="clip tz {bg}" data-start="{t0:.2f}" '
            f'data-duration="{t1 - t0 + extra_dur:.2f}" data-track-index="{2 + i}">\n    '
            + "\n    ".join(inner) + "\n  </section>")


# ---------------------------------------------------------------- cue sheet
# every cue is a spoken-word onset from shorts_run1/cuts/2026-08-08_20-59-13
CUE = {
    "infinite": 2.08, "cardout": 3.40, "grid": 3.58, "count": 4.62,
    "dont": 7.18, "hermes1": 8.56, "crack": 9.56,
    "disc": 11.88, "disc2": 12.48, "mean": 13.70, "demote": 15.20,
    "tiers": 15.50, "see": 16.72, "when": 18.44,
    "consume": 20.10, "ctxlab": 20.70, "grow": 21.50, "finite": 22.36,
    "handle": 24.20, "picky": 26.30, "give": 27.74, "nous": 30.78, "lab": 32.32,
    "alltools": 35.64, "nowor": 37.80,
    "hermes4": 40.72, "giveup": 43.06, "servers": 44.90,
    "tools4": 45.76, "without": 46.90, "unbel": 49.50,
}

BEATS = [(0.00, 11.80), (11.80, 20.00), (20.00, 40.58), (40.58, 50.74)]
CTA = 50.74

# the tiering facts, straight off the source infographic (law 11: positions are claims)
TIERS = [("24", "full listing"),
         ("830", "names only"),
         ("3,320", "server hint + search")]


def tweet_block(sid, media, left, top, w):
    """The tweet card plus the highlight ring that lands on the claim he is saying."""
    el, h = shot(sid, "tweet", left, top, w, media, 18, hide=False)
    rx = left + 0.030 * w
    ry = top + 0.418 * h
    return [el, ring_el(f"{sid}r", rx, ry, 0.940 * w, 0.272 * h, 10)], h


def tweet_tw(sid):
    return ([settle(f"#{sid}", 0.0), popo(f"#{sid}r", CUE["infinite"], 0.34, 0.9)]
            + leave(f"#{sid}", CUE["cardout"], 0.20)
            + leave(f"#{sid}r", CUE["cardout"], 0.20))


def key_term(prefix, dark, top=160, fs=56, cx=38, cw=500):
    """Law 9 + TRANSCRIPT IS TRUTH: the key term debuts centre stage, large, at its
    first utterance — and it prints exactly what Miguel says ("procedural")."""
    c1 = ON_DARK if dark else INK
    return [txt(f"{prefix}1", "disp od" if dark else "disp", "PROCEDURAL",
                cx, top, cw, fs, c1, "center"),
            txt(f"{prefix}2", "disp od" if dark else "disp", "DISCLOSURE",
                cx, top + fs * 1.18, cw, fs, TERRA_L if dark else TERRA, "center"),
            f'<div class="abs" style="left:{px(cx + cw / 2 - 50)}px;'
            f'top:{px(top + fs * 2.42)}px;width:{px(100)}px;height:{px(5)}px">'
            f'<div id="{prefix}u" class="rule" style="width:100%;height:100%;'
            f'background:{TERRA_L};transform:scaleX(0)"></div></div>']


def key_term_tw(prefix):
    return ([slam(f"#{prefix}1", CUE["disc"], 0.36, 1.18),
             slam(f"#{prefix}2", CUE["disc2"], 0.36, 1.18),
             sweep(f"#{prefix}u", CUE["mean"], 0.5)]
            + leave(f"#{prefix}1", CUE["demote"], 0.26)
            + leave(f"#{prefix}2", CUE["demote"], 0.26)
            + leave(f"#{prefix}u", CUE["demote"], 0.26))


def tier_card(cid, x, y, w, h, count, label):
    """One coded tier row: catalog size -> what the agent is actually given.

    Replaces run 3's ladder.png (a 362px raster blown up to 465px whose sub-lines
    rendered ~11px in frame — law 8 unreadable, plus an orphan "1." ordinal from the
    source article). Same facts, real type, no raster.

    run 5 / impeccable:
      * the 6px terracotta side-stripe is gone. A coloured side-stripe on a card is a
        hard ban, and here it was worse than decoration: its opacity encoded "share of
        the catalog the agent gets", which no viewer can read off an alpha value.
        The three counts and the three outcomes already ARE that data.
      * the row is a four-column grid with SYMMETRIC padding (24 both sides). Run 4
        padded 28 left / 14 right, so the whole cluster floated inside its own card.
      * "tools" was the only lowercase label in an all-uppercase mono system.
      * the arrow used TERRA (the on-cream accent) on a dark card; on dark, line work
        is TERRA_L. Filled masses stay TERRA — that is the system's own split.
    """
    pad = 24.0
    c_x, c_w = pad, 116.0                       # numerals, right-aligned to x=140
    u_x, u_w = 148.0, 52.0                      # unit label
    a_x, a_len, ah, hh = 208.0, 24.0, 13.0, 7.8  # shaft 208..232, head 232..245
    o_x = 256.0                                 # outcome, left-aligned
    o_w = w - pad - o_x                         # ...ending exactly `pad` from the edge
    return (
        f'<div id="{cid}" class="abs tier" style="left:{px(x)}px;top:{px(y)}px;'
        f'width:{px(w)}px;height:{px(h)}px;opacity:0">'
        f'<div class="abs" style="left:{px(c_x)}px;top:0;width:{px(c_w)}px;height:{px(h)}px;'
        f"display:flex;align-items:center;justify-content:flex-end;"
        f"font-family:'Instrument Serif',serif;font-size:{px(34)}px;color:{TERRA_L}\">"
        f'{esc(count)}</div>'
        f'<div class="abs" style="left:{px(u_x)}px;top:0;width:{px(u_w)}px;height:{px(h)}px;'
        f"display:flex;align-items:center;font-family:'JetBrains Mono',monospace;"
        f'font-size:{px(12)}px;letter-spacing:{px(1.2)}px;text-transform:uppercase;'
        f'color:{ON_DARK_S}">tools</div>'
        f'<div class="abs" style="left:{px(a_x)}px;top:{px(h / 2 - 1.5)}px;'
        f'width:{px(a_len)}px;height:{px(3)}px;background:{TERRA_L}"></div>'
        f'<div class="abs" style="left:{px(a_x + a_len)}px;top:{px(h / 2 - hh)}px;'
        f'width:0;height:0;border-left:{px(ah)}px solid {TERRA_L};'
        f'border-top:{px(hh)}px solid transparent;'
        f'border-bottom:{px(hh)}px solid transparent"></div>'
        f'<div class="abs" style="left:{px(o_x)}px;top:0;width:{px(o_w)}px;height:{px(h)}px;'
        f"display:flex;align-items:center;font-family:'JetBrains Mono',monospace;"
        f'font-size:{px(14)}px;letter-spacing:{px(1.5)}px;text-transform:uppercase;'
        f'color:{ON_DARK}">{esc(label)}</div>'
        f"</div>")


# ================================================================= LANE: icon
def lane_icon(C):
    """Icon choreography — real tool logos wake on demand, then collapse into one door."""
    m = C["media"]
    Z, T = [], []

    # ---- beat 1 : the tweet IS the news (3.6s), then the whole catalog appears
    t0, t1 = BEATS[0]
    H, _ = tweet_block("c1", m, 48, 130, 480)
    T += tweet_tw("c1")
    size, gap, cols = 66.0, 16.0, 4
    gw = cols * size + (cols - 1) * gap                 # 312
    gh = 3 * size + 2 * gap                             # 230
    # gy 74 -> 60: the beat's stack is grid + stats line + ringed lockup, and at 74 the
    # ring bottomed at design y 419 (785px) — 19px under the caption pill's painted top
    # edge (805px). Lifting the whole stack 14 design px buys the ring 46px of air
    # without changing a single gap inside the composition.
    gx, gy = (576 - gw) / 2, 60.0                       # 132 -> perfectly centred
    for j, k in enumerate(MCP):
        H.append(logo_tile(f"t1{j}", gx + (j % cols) * (size + gap),
                           gy + (j // cols) * (size + gap), size, k))
    nw1 = nous_mark_w(42, 15)
    nx1 = (576 - nw1) / 2
    H += [txt("i1c", "mono", "12 servers  ·  3,320 tools", 48, gy + gh + 20, 480, 15,
              INK_S, "center"),
          nous_mark("i1n", nx1, 352, 42, 15),
          ring_el("i1r", nx1 - 14, 341, nw1 + 28, 64, 22)]
    Z.append(zone(0, t0, t1, "cream", H))
    for j in range(12):
        T.append(popo(f"#t1{j}", CUE["grid"] + j * 0.045, 0.34, 0.62))
    T.append(fade("#i1c", CUE["count"], 0.4))
    for j in range(12):
        T.append(fade(f"#t1{j}", CUE["dont"], 0.4, 0.20, 1))
    # run 5 / impeccable: the stats line is a caption OF the grid, so it recedes WITH
    # the grid. Run 4 dimmed the twelve tiles to 0.20 and left this line at full
    # strength, which made it the loudest thing on screen at the exact moment the
    # ringed Nous lockup is the subject — hierarchy inverted on the beat's payoff.
    T.append(fade("#i1c", CUE["dont"], 0.4, 0.20, 1))
    # HIGHLIGHT DISCIPLINE: "they cracked the code" rings the lab that cracked it,
    # not an arbitrary tool tile (run 3 ringed tile #8 — semantic mismatch).
    T += [popo("#i1n", CUE["hermes1"], 0.45, 0.82),
          popo("#i1r", CUE["crack"], 0.42, 0.80)]

    # ---- beat 2 : key term centre stage, then the coded tiering panel
    t0, t1 = BEATS[1]
    H = key_term("k2", True, 160, 56)
    cx, cw, ch, cgap, cy0 = 44.0, 488.0, 84.0, 16.0, 88.0
    for j, (count, label) in enumerate(TIERS):
        H.append(tier_card(f"g2c{j}", cx, cy0 + j * (ch + cgap), cw, ch, count, label))
    H += [ring_el("g2a", cx - 4, cy0 - 4, cw + 8, ch + 8, 18),
          ring_el("g2b", cx - 4, cy0 + 2 * (ch + cgap) - 4, cw + 8, ch + 8, 18)]
    Z.append(zone(1, t0, t1, "dark", H))
    T += key_term_tw("k2")
    for j in range(3):
        T.append(rise(f"#g2c{j}", CUE["tiers"] + j * 0.14, 16, 0.38))
    T.append(popo("#g2a", CUE["see"], 0.34, 0.88))
    T += leave("#g2a", CUE["when"] - 0.14, 0.16)
    T.append(popo("#g2b", CUE["when"] + 0.06, 0.34, 0.88))

    # ---- beat 3 : exactly one tool awake at a time, the context capsule stays lean
    t0, t1 = BEATS[2]
    size, gap, cols = 56.0, 14.0, 3
    gx, gy = 34.0, 76.0
    gh = 4 * size + 3 * gap                             # 266 -> grid 76..342
    H = [logo_tile(f"t3{j}", gx + (j % cols) * (size + gap),
                   gy + (j // cols) * (size + gap), size, k, dark=True)
         for j, k in enumerate(MCP)]
    ax, ay, asz = 250.0, 157.0, 104.0                   # active tile, centred on the grid
    for bid, k in (("b30", "github"), ("b31", "notion"), ("b32", "modal")):
        H.append(logo_tile(bid, ax, ay, asz, k, dark=True, pad=0.10))
    ccx = 470.0                                         # one shared centre for the meter stack
    # run 5 / impeccable, two changes on this column:
    #  * the odometer printed 34% / 88% / 12%. Those numbers are spoken NOWHERE in the
    #    transcript — invented figures are claims, and run 4 filed them as still-open.
    #    Deleted. The gauge reads without a numeral, and the italic serif percentage
    #    had no alignment partner on that side of the frame anyway.
    #  * the capsule was 196 tall and ended at 306, floating between the grid (bottom
    #    342) and nothing. At 232 it ends at 342 too, so the two outer columns share a
    #    bottom edge and the beat reads as one instrument panel.
    H += [txt("i3n", "mono", "active", ax, ay + asz + 14, asz, 13, ON_DARK_S, "center"),
          # 84 -> 74: the highlight ring's top stroke lands at 98, so at 84 the label's
          # descender line cleared it by ~2 design px and the ring read as underlining
          # the word. HIGHLIGHT DISCIPLINE asks highlights to respect their neighbours;
          # 12 design px of air is the same gap the ring keeps on every other side.
          txt("i3c", "mono", "context", ccx - 76, 74, 152, 13, ON_DARK_S, "center"),
          capsule_el("ctx3", ccx - 34, 110, 68, 232),
          # FILL THE SHAPE on the highlight itself: a concentric ring 12px outside an
          # r18 capsule must carry r30, not r22. Run 4's ring cornered tighter than the
          # thing it was ringing.
          ring_el("i3r", ccx - 46, 98, 92, 256, 30),
          nous_mark("i3m", 34, 362, 40, 15, dark=True),
          chip_el("i3h", "Hermes", 256, 368, 120, 14, "left", dark=True)]
    Z.append(zone(2, t0, t1, "dark", H))
    for j in range(12):
        T.append(popo(f"#t3{j}", CUE["consume"] + j * 0.035, 0.3, 0.62))
        T.append(fade(f"#t3{j}", CUE["consume"] + j * 0.035 + 0.34, 0.2, 0.24, 1))
    # run 5 / impeccable + METERS COMPLETE: the gauge tells the sentence in three
    # states and no numerals. It fills on "tools consume context" (0.52), reaches FULL
    # exactly on "context is finite" — a finite container that has been consumed IS
    # full, and a bar that never completes is a bug — then drops to lean on "give
    # access", which is what being picky buys you.
    T += [popo("#b30", CUE["consume"] + 0.5, 0.4, 0.7),
          fade("#i3n", CUE["consume"] + 0.7, 0.35),
          fade("#i3c", CUE["ctxlab"], 0.35), fade("#ctx3w", CUE["ctxlab"] + 0.1, 0.35),
          sweepy("#ctx3", CUE["grow"], 0.5, 0.52),
          sweepy("#ctx3", CUE["finite"], 0.5, 1.0, 0.52),
          popo("#i3r", CUE["handle"], 0.42, 0.88)]
    # active-tool swaps CROSS-fade: the incoming tile starts before the outgoing one
    # dies, so the slot is never empty. Run 3 killed the old tile first and left a
    # 2-3 frame hole under a live "active" label (gate-2 catch, 26.5s and 35.6s).
    T += leave("#i3r", CUE["picky"] - 0.25, 0.2) + leave("#b30", CUE["picky"] + 0.04, 0.20)
    T += [popo("#b31", CUE["picky"], 0.4, 0.7),
          sweepy("#ctx3", CUE["give"], 0.55, 0.14, 1.0),
          popo("#i3m", CUE["nous"], 0.45, 0.82), popo("#i3h", CUE["lab"], 0.4, 0.7)]
    T += leave("#b31", CUE["alltools"] + 0.02, 0.20)
    T.append(popo("#b32", CUE["alltools"], 0.4, 0.7))
    # run 5 / impeccable: run 4 answered "we no longer have to worry" with a terracotta
    # check badge floating under the ACTIVE caption, attached to no object — the
    # weakest element in the short and the same free-floating-chrome family the pilot
    # verdict struck down. Deleted. The line is now carried by the object that already
    # means it: the dormant catalog relights in two readable steps, 0.24 -> 0.62 on
    # "all of the tools that we will ever need", -> 1.00 on "no longer have to worry".
    for j in range(12):
        T.append(fade(f"#t3{j}", CUE["alltools"] + 0.1 + j * 0.02, 0.3, 0.62, 0.24))
    for j in range(12):
        T.append(fade(f"#t3{j}", CUE["nowor"] + j * 0.018, 0.34, 1.0, 0.62))

    # ---- beat 4 : every server through one door into the agent
    t0, _ = BEATS[3]
    size, gap, cols = 56.0, 14.0, 3
    gx, gy = 34.0, 88.0
    gw = cols * size + (cols - 1) * gap                 # 196 -> grid 34..230
    nx, nw = 300.0, 228.0                               # right column 300..528
    row1_cy = gy + (size + gap) + size / 2              # 186 -> arrow rides row 2's centre
    H = [logo_tile(f"t4{j}", gx + (j % cols) * (size + gap),
                   gy + (j // cols) * (size + gap), size, k)
         for j, k in enumerate(MCP)]
    # run 5 / impeccable: the two hero nodes were 64 and 78 tall. They hold the same
    # rank in the same column, so they are the same size (NH). The Hermes card's logo
    # loses its white `.ltile` — a plate on a card that is already white, with its own
    # hairline border and shadow, i.e. a box inside a box.
    NH = 72.0
    n4a_y = row1_cy - NH / 2                            # 150 .. 222
    n4b_y = n4a_y + NH + 32                             # 254 .. 326
    H += [node_el("n4a", nx, n4a_y, nw, NH, "SEARCH & EXECUTE", 15, hero=True),
          # BUILD ORDER: both connectors are tweened in after the nodes they join.
          arrow("a4a", gx + gw, row1_cy, nx - (gx + gw), 0.0),
          arrow("a4b", nx + nw / 2, n4a_y + NH, 32, 90.0),
          f'<div id="n4b" class="abs node hero" style="left:{px(nx)}px;top:{px(n4b_y)}px;'
          f'width:{px(nw)}px;height:{px(NH)}px;opacity:0"></div>',
          bare_logo("n4l", nx + 18, n4b_y + (NH - 46) / 2, 46, "nous"),
          txt("n4t", "mono", "Hermes", nx + 78, n4b_y + (NH - 17 * 1.3) / 2, 124, 17,
              INK, "left"),
          # the "6%" numeral is invented too (nothing in the transcript states it) and
          # it sat 10px above its own label's baseline. Gone: the bar keeps the gauge
          # vocabulary beat 3 established, and 0.12 is the smallest fill that still
          # reads as a bar rather than a nub at this width.
          txt("i4c", "mono", "context", nx, 340, 96, 13, INK_S),
          meter_el("bf4", nx, 362, nw, 16, rad=5),
          # SEAM IS SACRED, measured not reasoned: at design y=396/fs 26 this line's
          # italic descender painted down to render row 793 while the caption pill's
          # painted top edge is 805 — a 12px gap, the tightest in the fleet and exactly
          # the "creative work touching captions" class. Re-seated under the tool grid
          # (centred on the grid's own axis, x=132) where it has 44px of air and reads
          # as the caption for the twelve servers it describes.
          txt("i4p", "serif", "one door, every tool", 20, 374, 224, 23, TERRA_L, "center")]
    Z.append(zone(3, t0, CTA, "cream", H))
    # BUILD ORDER: the Hermes card materialises WITH its logo and name. Run 3 staggered
    # them (+0.12 / +0.22) and shipped an empty bordered box on screen first — chrome
    # before content, which the pilot verdict bans (gate-2 catch at 40.7s).
    T += [popo("#n4b", CUE["hermes4"], 0.45, 0.8),
          popo("#n4l", CUE["hermes4"], 0.42, 0.62),
          slidex("#n4t", CUE["hermes4"], -14, 0.4)]
    # 41.90 -> 41.20: at 41.90 the beat held a single off-centre card on empty cream for
    # 1.2s (the weakest frame in the short). The cascade still finishes at 41.74, well
    # before "give up all of the MCP servers" (43.06) and long before the connector that
    # joins them (44.90), so BUILD ORDER is untouched — nodes first, wires after.
    for j in range(12):
        T.append(popo(f"#t4{j}", 41.20 + j * 0.045, 0.34, 0.62))
    T.append(popo("#n4a", CUE["giveup"] + 0.2, 0.42, 0.78))
    T += arrow_in("a4a", CUE["servers"], 0.42) + arrow_in("a4b", CUE["tools4"] + 0.2, 0.36)
    T += [fade("#i4c", CUE["without"], 0.35), fade("#bf4w", CUE["without"] + 0.1, 0.35),
          sweep("#bf4", CUE["without"] + 0.25, 0.5, 0.12),
          fade("#i4p", CUE["unbel"], 0.45)]
    return Z, T


# ---------------------------------------------------------------- outro
def outro(t0, dur):
    """v1.1 OUTRO ALIGNMENT: one deliberate centred composition on x=288 — logo row,
    hero node, payoff line, handle chip. No zero-ink wrapper (run 3's `ow` box had its
    bottom edge exactly ON the caption seam, which v1.1 promotes to an ERROR), and
    150px of clear air above the seam.

    run 5 / impeccable — the choreography, not the composition, was the defect:

      * DEAD FRAME. The cut to the outro canvas landed on nothing: the first tile only
        started at t0+0.12, so 50.74-50.82 of the delivered run-4/run-5 render is a
        charcoal frame with 0.0000% ink (measured on the render, not estimated). The
        run-3 gate pass filed this exact timestamp as "worth a hold-over"; it survived
        two runs because no gate scores an empty frame. The hero node now carries the
        zone's FIRST painted frame via the frame-0 vocabulary (`hide=False` + settle),
        the same pattern the tweet card uses at t=0.
      * BUILD ORDER (v1.1). Six decorative logo tiles arrived at 50.86-51.55 and the
        line that IS the outro, FOLLOW FOR DAILY AI, only landed at 51.40 — chrome
        before content, the law's own words. Content leads now; the row follows it.
      * CLAIM SYNC. t0 is the onset of the spoken word "Follow" (50.74), so the CTA is
        read and heard on the same frame instead of trailing the voice by 0.66s.
      * MOTION RESTRAINT. The build ran 1.90s of continuous element-by-element entrance
        under a 3.4s outro. Tightened to 1.70s, so the finished composition HOLDS STILL
        for 1.73s (law 1) instead of 1.53s. No tween was added; four were re-timed and
        one changed helper."""
    H, T = [], []
    d = dur - t0
    keys = ["github", "notion", "modal", "figma", "slack", "exa"]
    size, gap = 58.0, 14.0
    row_w = len(keys) * size + (len(keys) - 1) * gap    # 418
    rx = (576 - row_w) / 2                              # 79 -> centred
    for j, k in enumerate(keys):
        H.append(logo_tile(f"ot{j}", rx + j * (size + gap), 84, size, k, dark=True))
        T.append(popo(f"#ot{j}", t0 + 0.34 + j * 0.05, 0.30, 0.6))
    H += [node_el("ohn", (576 - 300) / 2, 186, 300, 66, "FOLLOW FOR DAILY AI", 15,
                  dark=True, hero=True, hide=False),
          txt("od", "serif", "one drop a day", 48, 276, 480, 32, TERRA_L, "center"),
          f'<div id="oe" class="abs" style="left:0;top:{px(336)}px;width:{px(576)}px;'
          f'text-align:center;opacity:0"><span class="ctchip" style="font-size:{px(16)}px;'
          f'background:rgba(246,241,234,0.16)">Miguel Torrez AI</span></div>']
    T += [settle("#ohn", t0, 0.965, 0.5), fade("#od", t0 + 0.98, 0.42),
          rise("#oe", t0 + 1.32, 14, 0.38)]
    zone_html = (f'  <section id="tz-outro" class="clip tz dark" data-start="{t0:.2f}" '
                 f'data-duration="{d:.2f}" data-track-index="6">\n    '
                 + "\n    ".join(H) + "\n  </section>")
    return zone_html, T


# ---------------------------------------------------------------- seam budget
# The caption pill rides the seam with translateY(-50%), so its PAINTED top edge is at
# design y ~429 (805px), not at the 460 seam line geometry_audit checks. A short can
# therefore audit 0-error while its ink visibly kisses the captions. This makes the
# budget a build failure instead of a frame-review discovery.
SEAM_INK_FLOOR = 410.0          # design px; 49 design px of air under the deepest ink
INK_OVER_FS = 1.30              # glyph box vs font-size for our display/serif faces


def seam_guard(zones_html):
    """Hard-fail if any positioned atom's estimated ink bottom crosses the floor.

    Sees `top:` + (`height:` | `font-size:`) on the same inline style. Elements that
    carry their font-size on an inner span (chips) are not covered — they sit high in
    every beat here, and the rendered check below is what proves the real number.
    """
    worst = (0.0, "")
    for st in re.findall(r'style="([^"]*)"', zones_html):
        mt = re.search(r'(?:^|;)top:(-?[0-9.]+)px', st)
        if not mt:
            continue
        top = float(mt.group(1)) / S
        mh = re.search(r'(?:^|;)height:([0-9.]+)px', st)
        mf = re.search(r'font-size:([0-9.]+)px', st)
        if mh:
            ink = top + float(mh.group(1)) / S
        elif mf:
            ink = top + INK_OVER_FS * float(mf.group(1)) / S
        else:
            continue
        if ink > worst[0]:
            worst = (ink, st[:88])
    if worst[0] > SEAM_INK_FLOOR:
        raise SystemExit(f"SEAM BUDGET FAIL: ink bottom design y={worst[0]:.1f} "
                         f"> {SEAM_INK_FLOOR}\n  {worst[1]}")
    return worst


# ---------------------------------------------------------------- page
def build_html(C, phrases):
    dur = C["dur"]
    zones, tws = lane_icon(C)
    outro_html, otw = outro(CTA, dur)
    zones = zones + [outro_html]
    tws += otw
    deepest = seam_guard("\n".join(zones))
    print(f"  seam budget OK: deepest ink design y={deepest[0]:.1f} "
          f"(floor {SEAM_INK_FLOOR})")

    face = (f'  <video id="facebot" src="assets/v/{VID}/face_bottom.mp4" data-start="0" '
            f'data-duration="{dur:.2f}" data-media-start="0" data-track-index="1" muted '
            f'playsinline style="position:absolute;top:{px(SEAM)}px;left:0;width:1080px;'
            f'height:{px(FACE_H)}px;object-fit:cover"></video>')
    audio, atw = audio_block(dur, BEATS, CTA)
    tws += atw

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=1080, height=1920"/>
<title>{VID} — Icon choreography</title>
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


# ---------------------------------------------------------------- staging
def round_corners(im, radius_at_1000=26):
    w, h = im.size
    r = int(round(radius_at_1000 * w / 1000.0))
    mask = Image.new("L", (w * 2, h * 2), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w * 2 - 1, h * 2 - 1], radius=r * 2, fill=255)
    mask = mask.resize((w, h), Image.LANCZOS)
    out = im.convert("RGBA")
    out.putalpha(mask)
    return out


def trim_frame(im, thresh=90, cover=0.85):
    """Strip a baked-in rectangular frame from a logo raster.

    run 5 / impeccable + FILL THE SHAPE: `ai-models/nous-research.png` ships the Nous
    girl inside a hard 4-5px BLACK SQUARE border. Dropped into our rounded white plate
    (beat 1 and beat 3) that is a sharp-cornered box inside a rounded box, which is
    the exact shape mismatch the pilot verdict named; on the white Hermes card in beat
    4 it draws a second, competing card outline. Peel the fully dark edge lines off
    (plus 1px of safety) and the mark takes the shape of whatever holds it.
    """
    g = np.array(im.convert("L"))
    dark = g < thresh
    t, b = 0, g.shape[0] - 1
    l, r = 0, g.shape[1] - 1
    while t < b and dark[t].mean() > cover:
        t += 1
    while b > t and dark[b].mean() > cover:
        b -= 1
    while l < r and dark[:, l].mean() > cover:
        l += 1
    while r > l and dark[:, r].mean() > cover:
        r -= 1
    if (t, l) == (0, 0) and (b, r) == (g.shape[0] - 1, g.shape[1] - 1):
        return im, 0
    pad = 1
    return im.crop((l + pad, t + pad, r + 1 - pad, b + 1 - pad)), t + pad


def square_pad(im, side):
    im = im.copy()
    im.thumbnail((side, side), Image.LANCZOS)
    out = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    out.paste(im, ((side - im.size[0]) // 2, (side - im.size[1]) // 2), im)
    return out


def svg_png(path, width):
    return Image.open(io.BytesIO(cairosvg.svg2png(url=str(path), output_width=width))).convert("RGBA")


def link(target: Path, dest: Path):
    if dest.is_symlink() or dest.exists():
        dest.unlink()
    dest.symlink_to(target.resolve())


def stage():
    for d in ["music", "sfx", "img/logos", "v"]:
        (STAGE / d).mkdir(parents=True, exist_ok=True)
    pub = FACTORY / "pipeline/assets"
    shutil.copy2(pub / "bed_split.mp3", STAGE / "music/bed_split.mp3")
    for s in ["pop", "whoosh", "boom", "ding"]:
        shutil.copy2(pub / f"{s}.mp3", STAGE / "sfx" / f"{s}.mp3")

    m = {}
    # law 3: the metrics row is cropped OFF. law 8: keep the header + the news paragraph.
    # 1000px source rendered at 900px in frame -> never upscaled.
    card = Image.open(RUN1 / "x_cards/card_Teknium_2081450522608107816.png").convert("RGB")
    tw = round_corners(card.crop((0, 0, 1000, 356)))
    tw.save(STAGE / "img/tweet.png")
    m["tweet"] = ("assets/img/tweet.png", tw.size)

    for key, rel in MCP_SRC.items():
        shutil.copy2(LOGOS / rel, STAGE / "img/logos" / f"{key}.png")

    # run 5 / impeccable: peel the baked-in black square frame off the Nous mark so it
    # inherits the shape of the plate or card that holds it (see trim_frame).
    nous, trimmed = trim_frame(Image.open(LOGOS / MCP_SRC["nous"]).convert("RGB"))
    nous.save(STAGE / "img/logos/nous.png")
    print(f"  nous mark: trimmed {trimmed}px of baked-in frame -> {nous.size}")

    # ASSET HEALTH replacements, both derived from local vector sources (no network):
    #  gdrive  -> replaces the broken 3-dot/2-line n8n connection glyph
    #  openrouter -> the purple glyph alone; the shipped PNG is a black rounded square
    #                (a plate inside our plate, and it vanishes into the dark canvas)
    square_pad(svg_png(LOGOS / "platforms/google-drive.svg", 512), 512).save(
        STAGE / "img/logos/gdrive.png")
    orl = svg_png(LOGOS / "platforms/openrouter.svg", 2400)
    a = np.array(orl)
    vis = a[..., 3] > 16
    purple = vis & (a[..., 2].astype(int) > 120) & (a[..., 0].astype(int) > 80) \
        & (a[..., 1].astype(int) < 120)
    ys, xs = np.where(purple)
    glyph = orl.crop((int(xs.min()) - 6, int(ys.min()) - 6,
                      int(xs.max()) + 7, int(ys.max()) + 7))
    square_pad(glyph, 512).save(STAGE / "img/logos/openrouter.png")

    vd = STAGE / "v" / VID
    vd.mkdir(exist_ok=True)
    cut = RUN1 / "cuts/2026-08-08_20-59-13"
    for f in ["face_bottom.mp4", "audio.m4a"]:
        link(cut / f, vd / f)
    return m


def timings():
    cut = RUN1 / "cuts/2026-08-08_20-59-13"
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
    print(f"BUILD DONE  {VID}_{LANE}  dur={dur:.2f} cta={CTA:.2f} caps={len(phrases)}")
