"""ARTIFACT SPINE — shared core for the three lab variants.

THE FORMAT: one document is the whole video.  A mock Hermes Agent tool-registry
panel — real chrome, real registry marks, an always-present context meter — is
the only subject.  It advances (v1/v2 scroll, v3 zoom), and annotations land on
the line that is being spoken.  Miguel's face is in the SAME window rect as the
panel, so the frame never changes shape when the face bookends the piece.

Everything here is authored at 1080x1920 NATIVE (prototype resolution).  There
is no design-unit scale factor: 1 authored px == 1 rendered px.

What is shared: palette + type, the caption pill system (factory issue), the
audio block (AUDIO MIX LAW), the face window, the panel chrome, the seven region
builders, and the region state tweens (which are position-independent because
they address ids, not coordinates).  What each variant owns: the LAYOUT of the
regions (a vertical document vs a 2D board) and the CAMERA.
"""
from __future__ import annotations

import html as ihtml
import json
import math
import re
import subprocess
from pathlib import Path

WORKSPACE = Path.home() / "Documents/Workspace"
FACTORY = WORKSPACE / "projects/personal/content/shorts-factory"
SRC = FACTORY / "formats/_shared/hermesinfinite"  # frozen lab inputs, moved out of the format lab (archived) 2026-09-20 (MANIFEST.sha256 beside them)
ROOT = FACTORY / "formats/artifactspine/source"    # round-6 source material, READ ONLY
STAGE = ROOT / "stage"          # prebuilt plates; only ever symlinked, never written

# --- CHASSIS PARAMETERS (promoted out of the lab, 2026-09-01) ----------------
# The lab is history.  `OUT_ROOT` is where this chassis writes its projects; the
# caption canon comes from `pipeline/captions.py`, and the outro @handle is a
# parameter set by `chassis_gen.py --handle`.
import sys                                                     # noqa: E402
sys.path.insert(0, str(FACTORY / "pipeline"))
import captions as CAP                                         # noqa: E402

CHASSIS = Path(__file__).resolve().parent.parent
OUT_ROOT = CHASSIS / "build"    # where projects land.  Never the lab.
OUTRO_HANDLE = CAP.handle()     # the outro chip text

FPS = 30

# ---- frame geometry ----------------------------------------------------------
FW, FH = 1080.0, 1920.0
WIN_X, WIN_Y, WIN_W, WIN_H = 40.0, 84.0, 1000.0, 1516.0   # the ONE window rect
WIN_R = 28.0
CAP_Y = 1720.0                                             # caption pill centre

HEAD_H = 196.0                                             # panel header height
PAD = 32.0
VIEW_Y = WIN_Y + HEAD_H
VIEW_H = WIN_H - HEAD_H
DOC_W = WIN_W - 2 * PAD
DOC_TOP = 58.0        # keeps section 01's eyebrow clear of the top edge fade

# ---- palette (factory issue) -------------------------------------------------
CREAM = "#F6F1EA"
INK = "#141416"
INK_2 = "#242427"
MUTED = "#716B63"
MUTED_D = "#9A948B"
TERRA = "#C4573A"
TERRA_2 = "#E68569"
WHITE = "#FFFDF9"
PAPER = "#FBF6EF"          # row fill inside a white card
LINE = "#E4DCD1"           # hairline
LINE_2 = "#EFE8DE"         # meter track
DIM = "#F1EAE0"            # the not-loaded strip
DARK_LINE = "#3A3A3E"

BED_VOLUME = "0.065"
VOICE_VOLUME = "1"
SFX_VOLUME = "0.18"

FONTS = '<link href="assets/fonts/fonts.css" rel="stylesheet">'
GSAP = '<script src="assets/lib/gsap.min.js"></script>'

ADV_POPPINS = 0.64          # caps advance estimate, em — build-time width guards
ADV_MONO = 0.60


def esc(v: object) -> str:
    return ihtml.escape(str(v), quote=False)


def n(v: float) -> str:
    return f"{round(v, 2):g}"


def rgba(hex_color: str, alpha: float) -> str:
    v = hex_color.lstrip("#")
    return f"rgba({int(v[0:2],16)},{int(v[2:4],16)},{int(v[4:6],16)},{alpha})"


def rgb(hex_color: str) -> str:
    v = hex_color.lstrip("#")
    return f"rgb({int(v[0:2],16)},{int(v[2:4],16)},{int(v[4:6],16)})"


def norm(s: str) -> list[str]:
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()


def probe(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        check=True, capture_output=True, text=True).stdout.strip()
    return float(out)


def ink_w(text: str, fs: float, mono: bool = False, ls: float = 0.0) -> float:
    """Conservative rendered-ink estimate, used only for build-time guards."""
    adv = ADV_MONO if mono else ADV_POPPINS
    return len(text) * (adv * fs + ls)


# =============================================================================
# MARK INK — a row of marks is equalised by ink AREA, not by container box
# =============================================================================
MARK_INK: dict[str, dict[str, float]] = {}

LOGO_FILES = {
    "gdrive": "gdrive.svg", "github": "github.svg", "notion": "notion.png",
    "slack": "slack.png", "gmail": "gmail.png", "airtable": "airtable.svg",
    "figma": "figma.png", "elevenlabs": "elevenlabs.svg", "nous": "nous.png",
    "mcp": "mcp.svg",
}


def measure_marks() -> None:
    from io import BytesIO
    from PIL import Image
    for key, fname in LOGO_FILES.items():
        path = STAGE / "logos" / fname
        if not path.exists():
            raise SystemExit(f"missing staged mark: {path}")
        if path.suffix == ".svg":
            import cairosvg
            img = Image.open(BytesIO(cairosvg.svg2png(url=str(path), output_width=1024)))
        else:
            img = Image.open(path)
        img = img.convert("RGBA")
        bbox = img.getchannel("A").getbbox()
        if bbox is None:                       # fully opaque raster: the file IS the ink
            bbox = (0, 0, img.size[0], img.size[1])
        x0, y0, x1, y1 = bbox
        w, h = img.size
        MARK_INK[key] = {"img_w": float(w), "img_h": float(h),
                         "bbox_x": float(x0), "bbox_y": float(y0),
                         "bbox_w": float(x1 - x0), "bbox_h": float(y1 - y0),
                         "aspect": (x1 - x0) / (y1 - y0)}


def mark(eid: str, cx: float, cy: float, side: float, key: str, extra: str = "") -> str:
    """An <img> whose INK area is side*side, ink-centred on (cx, cy)."""
    m = MARK_INK[key]
    ink_wd = side * math.sqrt(m["aspect"])
    ink_ht = side / math.sqrt(m["aspect"])
    box_w = ink_wd * m["img_w"] / m["bbox_w"]
    box_h = box_w * m["img_h"] / m["img_w"]
    # ink centre inside the box, as a fraction of the box
    fx = (m["bbox_x"] + m["bbox_w"] / 2) / m["img_w"]
    fy = (m["bbox_y"] + m["bbox_h"] / 2) / m["img_h"]
    left = cx - box_w * fx
    top = cy - box_h * fy
    return (f'<img id="{eid}" src="assets/logos/{LOGO_FILES[key]}" alt="" class="abs" '
            f'style="left:{n(left)}px;top:{n(top)}px;width:{n(box_w)}px;height:{n(box_h)}px;'
            f'object-fit:contain;display:block;{extra}"/>')


# ---- atoms -------------------------------------------------------------------
def div(eid: str, x: float, y: float, w: float, h: float, style: str = "", cls: str = "abs",
        inner: str = "") -> str:
    return (f'<div class="{cls}" id="{eid}" style="left:{n(x)}px;top:{n(y)}px;'
            f'width:{n(w)}px;height:{n(h)}px;{style}">{inner}</div>')


def txt(eid: str, x: float, y: float, w: float, text: str, fs: float, *, color: str = INK,
        weight: int = 800, ls: float = 0.0, mono: bool = False, align: str = "left",
        upper: bool = True, lh: float = 1.30) -> str:
    cls = "abs mono" if mono else "abs disp"
    tt = "" if upper else "text-transform:none;"
    indent = f"text-indent:{n(ls)}px;" if (align == "center" and ls) else ""
    return (f'<div class="{cls}" id="{eid}" style="left:{n(x)}px;top:{n(y)}px;width:{n(w)}px;'
            f'height:{n(lh * fs)}px;line-height:{n(lh * fs)}px;font-size:{n(fs)}px;'
            f'text-align:{align};letter-spacing:{n(ls)}px;{indent}font-weight:{weight};'
            f'color:{color};{tt}white-space:nowrap;">{esc(text)}</div>')


def card(eid: str, x: float, y: float, w: float, h: float, inner: str, *, bg: str = WHITE,
         border: str = LINE, bw: float = 2.0, r: float = 22.0, shadow: str = "",
         extra: str = "") -> str:
    sh = f"box-shadow:{shadow};" if shadow else ""
    return (f'<div class="abs" id="{eid}" style="left:{n(x)}px;top:{n(y)}px;width:{n(w)}px;'
            f'height:{n(h)}px;background:{bg};border:{n(bw)}px solid {border};'
            f'border-radius:{n(r)}px;{sh}{extra}">{inner}</div>')


def bar(eid: str, x: float, y: float, w: float, h: float, *, track: str = LINE_2,
        r: float | None = None) -> str:
    rr = h / 2 if r is None else r
    return div(eid, x, y, w, h, f"background:{track};border-radius:{n(rr)}px;")


FILLS: dict[str, tuple[float, float, float]] = {}   # eid -> (track_w, h, radius)


def fill(eid: str, x: float, y: float, w: float, h: float, color: str = TERRA,
         r: float | None = None) -> str:
    """A meter fill that reaches by WIDTH, never by `scaleX`.

    GLOBAL LAW 3 (Miguel, 2026-08-30) — NO SQUARE-ENDED FILLS IN ROUNDED
    CONTAINERS.  The old build authored the fill at full track width and
    squeezed it with `scaleX`, which multiplies the HORIZONTAL corner radius by
    the same factor: at scaleX 0.62 a 12px radius renders as 7px, at 0.06 a 10px
    radius renders as 0.6px, i.e. a dead-straight chop sitting inside a pill.
    Shot on artifactspine_v1 — `hd-fill` at t=8/20/36/48 (and the t=48
    annotation ring lands ON that flat end) and `r4-fill` at t=21-22.

    `width` is outside the transform matrix, so `border-radius` paints a true
    cap at every value, and CSS's radius clamp keeps a sub-diameter fill a
    lozenge rather than a sliver.  The track geometry is recorded here so
    `fill_to` can resolve a fraction to real pixels."""
    rr = h / 2 if r is None else r
    FILLS[eid] = (w, h, rr)
    return div(eid, x, y, 0.0, h,
               f"background:{color};border-radius:{n(rr)}px;opacity:0;")


def ring(eid: str, x: float, y: float, w: float, h: float, *, color: str = TERRA,
         bw: float = 5.0, r: float = 18.0) -> str:
    """An annotation ring.  Drawn OVER content on purpose (lab annotation grammar)."""
    return div(eid, x, y, w, h,
               f"border:{n(bw)}px solid {color};border-radius:{n(r)}px;opacity:0;"
               f"box-shadow:0 0 0 {n(bw)}px {rgba(color,0.10)};", cls="abs anno")


def wash(eid: str, x: float, y: float, w: float, h: float, *, color: str = TERRA,
         alpha: float = 0.22, r: float = 10.0) -> str:
    return div(eid, x, y, w, h,
               f"background:{rgba(color,alpha)};border-radius:{n(r)}px;opacity:0;"
               f"transform-origin:left center;transform:scaleX(0.001);", cls="abs anno")


def strike(eid: str, x: float, y: float, w: float, h: float = 4.0, color: str = TERRA) -> str:
    return div(eid, x, y, w, h,
               f"background:{color};border-radius:{n(h/2)}px;transform-origin:left center;"
               f"transform:scaleX(0.001);opacity:0;", cls="abs anno")


def toggle(prefix: str, x: float, y: float, w: float, h: float) -> str:
    """A real switch: track + knob.  Off state authored; the flip is one tween."""
    knob = h - 12
    return (div(f"{prefix}-trk", x, y, w, h,
                f"background:{LINE_2};border:2px solid {LINE};border-radius:{n(h/2)}px;")
            + div(f"{prefix}-knb", x + 6, y + 6, knob, knob,
                  f"background:{MUTED_D};border-radius:{n(knob/2)}px;"))


def checkbox(prefix: str, x: float, y: float, s: float) -> str:
    tick = (f'<svg viewBox="0 0 24 24" width="100%" height="100%">'
            f'<path d="M5 12.5 L10 17.5 L19 7" fill="none" stroke="{WHITE}" stroke-width="3.2" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg>')
    return (div(f"{prefix}-bx", x, y, s, s,
                f"background:{TERRA};border:2.5px solid {TERRA};border-radius:{n(s*0.28)}px;")
            + div(f"{prefix}-tk", x + s * 0.16, y + s * 0.16, s * 0.68, s * 0.68,
                  "", inner=tick))


def hair(eid: str, x: float, y: float, w: float, color: str = LINE) -> str:
    return div(eid, x, y, w, 2.0, f"background:{color};")


# ---- animation helpers -------------------------------------------------------
def settle(sel: str, t: float, d: float = 0.44, s: float = 0.955) -> str:
    return (f'tl.set("{sel}",{{opacity:0}},0);'
            f'tl.fromTo("{sel}",{{opacity:0,scale:{s},transformOrigin:"50% 50%"}},'
            f'{{opacity:1,scale:1,duration:{d},ease:SOFT,immediateRender:false}},{t:.2f});')


def rise(sel: str, t: float, d: float = 0.40, dy: float = 22.0) -> str:
    return (f'tl.set("{sel}",{{opacity:0}},0);'
            f'tl.fromTo("{sel}",{{opacity:0,y:{n(dy)}}},{{opacity:1,y:0,duration:{d},'
            f'ease:SOFT,immediateRender:false}},{t:.2f});')


def rise_stagger(sels: list[str], t0: float, step: float, d: float = 0.38,
                 dy: float = 22.0) -> str:
    return "".join(rise(s, t0 + i * step, d, dy) for i, s in enumerate(sels))


def pop(sel: str, t: float, d: float = 0.36) -> str:
    return (f'tl.set("{sel}",{{opacity:0}},0);'
            f'tl.fromTo("{sel}",{{opacity:0,scale:0.72,transformOrigin:"50% 50%"}},'
            f'{{opacity:1,scale:1,duration:{d},ease:POP,immediateRender:false}},{t:.2f});')


def fade(sel: str, t: float, to: float = 1.0, d: float = 0.30) -> str:
    return f'tl.to("{sel}",{{opacity:{to},duration:{d},ease:SOFT}},{t:.2f});'


def setnow(sel: str, props: str, t: float) -> str:
    return f'tl.set("{sel}",{{{props}}},{t:.2f});'


def swap(sel_out: str, sel_in: str, t: float, d: float = 0.20) -> str:
    """A text STATE change.  GSAP's TextPlugin is not loaded and callback-driven
    text is not seek-safe, so every changing string is authored as stacked atoms
    and cross-faded — the rendered state is then a pure function of timeline
    progress, which is exactly what a deterministic renderer needs."""
    return (f'tl.to("{sel_out}",{{opacity:0,duration:{d},ease:EXIT}},{t:.2f});'
            f'tl.to("{sel_in}",{{opacity:1,duration:{d},ease:SOFT}},{t + d * 0.5:.2f});')


def scale_x(sel: str, t: float, to: float, d: float = 0.55, ease: str = "SOFT") -> str:
    return f'tl.to("{sel}",{{opacity:1,scaleX:{to},duration:{d},ease:{ease}}},{t:.2f});'


def fill_to(eid: str, t: float, frac: float, d: float = 0.55,
            ease: str = "SOFT", *, geom: tuple[float, float] | None = None) -> str:
    """GLOBAL LAW 3 — a meter reaches by `width`.  `frac` is the fraction of the
    track the reading claims, floored at one cap diameter so the resting shape
    is always a lozenge with two true semicircular ends, never a chopped bar.

    `geom` is (track_w, h) for callers whose tweens are emitted BEFORE the HTML
    that registers the fill (the header, in v1/v2)."""
    if geom is None:
        w, h, _r = FILLS[eid]
    else:
        w, h = geom
    return (f'tl.to("#{eid}",{{opacity:1,width:"{n(max(h, frac * w))}px",'
            f'duration:{d},ease:{ease}}},{t:.2f});')


HD_BAR_H, HD_BAR_R = 20.0, 10.0


def hd_geom(w: float) -> tuple[float, float]:
    """The header meter's track geometry — the ONE place `header_html` and
    `header_tweens` agree on it, so the tweens never depend on which of the two
    a variant happens to call first."""
    return w - 2 * PAD, HD_BAR_H


def anno_in(sel: str, t: float, d: float = 0.34) -> str:
    """A ring lands: it arrives slightly large and settles on its target."""
    return (f'tl.fromTo("{sel}",{{opacity:0,scale:1.16,transformOrigin:"50% 50%"}},'
            f'{{opacity:1,scale:1,duration:{d},ease:POP,immediateRender:false}},{t:.2f});')


def anno_out(sel: str, t: float, d: float = 0.26) -> str:
    return f'tl.to("{sel}",{{opacity:0,duration:{d},ease:EXIT}},{t:.2f});'


def wash_in(sel: str, t: float, d: float = 0.36) -> str:
    return (f'tl.set("{sel}",{{opacity:1}},{t:.2f});'
            f'tl.to("{sel}",{{scaleX:1,duration:{d},ease:SOFT}},{t:.2f});')


def count_to(eid: str, t: float, a: float, b: float, d: float, fmt: str = "int") -> str:
    """A numeric readout driven by one proxy object — no per-frame string math in
    the timeline, and it is seek-safe because GSAP re-evaluates from progress."""
    f = ("v=>v.toLocaleString('en-US')" if fmt == "int" else "v=>Math.round(v)+'%'")
    return (f'{{const o={{v:{a}}};const el=document.getElementById("{eid}");'
            f'const F={f};'
            f'tl.fromTo(o,{{v:{a}}},{{v:{b},duration:{d},ease:SOFT,immediateRender:false,'
            f'onUpdate:()=>{{el.textContent=F(o.v);}}}},{t:.2f});}}')


# ---- captions ----------------------------------------------------------------
FILLERS = {"uh", "um", "huh", "mm", "mhm", "erm", "ah", "eh"}


def clean_tokens(words: list[dict]) -> list[dict]:
    out: list[dict] = []
    for i, word in enumerate(words):
        text = word["text"].strip()
        if text.endswith("-"):
            continue
        if re.sub(r"[^a-z]", "", text.lower()) in FILLERS and len(text) <= 4:
            continue
        nxt = words[i + 1] if i + 1 < len(words) else None
        if (nxt and re.sub(r"[^a-z0-9]", "", text.lower())
                == re.sub(r"[^a-z0-9]", "", nxt["text"].lower())
                and nxt["start"] - word["end"] < 0.5):
            continue
        out.append(word)
    return out


def build_captions(words: list[dict]) -> list[dict]:
    phrases, cur = [], []
    words = clean_tokens(words)
    for i, word in enumerate(words):
        cur.append(word)
        nxt = words[i + 1] if i + 1 < len(words) else None
        punct = bool(re.search(r"[.,!?]$", word["text"]))
        gap = bool(nxt and nxt["start"] - word["end"] > 0.32)
        if len(cur) >= 4 or (punct and len(cur) >= 2) or gap or nxt is None:
            phrases.append({"t0": round(cur[0]["start"], 2),
                            "t1": round(word["end"] + 0.12, 2),
                            "text": " ".join(x["text"] for x in cur), "n": len(cur)})
            cur = []
    merged: list[dict] = []
    for p in phrases:
        if p["n"] == 1 and merged:
            merged[-1]["text"] += " " + p["text"]
            merged[-1]["t1"] = p["t1"]
            merged[-1]["n"] += 1
            continue
        merged.append(dict(p))
    for i in range(len(merged) - 1):
        merged[i]["t1"] = merged[i + 1]["t0"]
    return merged


def cap_font(text: str) -> float:
    return round(max(36.0, min(56.0, 907.0 / (0.575 * max(1, len(text))))), 1)


def caption_clips(phrases: list[dict], dur: float) -> str:
    clips = []
    for i, p in enumerate(phrases):
        t0, t1 = p["t0"], min(p["t1"], dur)
        if t1 - t0 < 0.08 or t0 >= dur:
            continue
        clips.append(
            f'  <div id="cap{i}" class="clip scap" style="top:{n(CAP_Y)}px" '
            f'data-start="{t0:.2f}" data-duration="{t1 - t0:.2f}" data-track-index="60">'
            f'<span class="scappill" style="font-size:{n(cap_font(p["text"]))}px">'
            f'{esc(p["text"])}</span></div>')
    return "\n".join(clips)


# ---- timing ------------------------------------------------------------------
ANCHORS = {
    "hookcut": "literally infinite tools",     # face -> artifact
    "youthink": "You think an",
    "loads": "loads every tool",
    "atonce": "all at once",
    "spoiler": "Well, spoiler",
    "dont": "they don't",
    "yousee": "You see, Hermes",
    "crack": "crack the code",
    "disclosure": "procedural disclosure",
    "whatmean": "What does that mean",
    "simple": "It's very simple",
    "means": "It means that",
    "seetools": "see the tools",
    "needsthem": "when it actually needs them",
    "consume": "Tools consume context",
    "finite": "context is finite",
    "finiteword": "finite",
    "bestway": "the best way to handle",
    "picky": "very picky",
    "access": "give access",
    "people": "And the people",
    "nous": "Nous Research",
    "lab": "the lab behind Hermes",
    "everneed": "all of the tools that we will ever need",
    "nolonger": "no longer have to",
    "worry": "worry about that",
    "ifyou": "If you have a Hermes agent",
    "servers": "all of the MCP servers",
    "andtools": "and all of the tools",
    "bloating": "without bloating your context",
    "unbelievable": "which is just unbelievable",
    "follow": "Follow for more",
    "daily": "every single day",
}


def load_timing() -> tuple[list[dict], float, dict[str, float]]:
    data = json.loads((SRC / "transcript_words.json").read_text())
    words = [w for w in data["words"] if w.get("type") == "word"]
    dur = round(min(probe(STAGE / "v/audio.m4a"), probe(STAGE / "v/face_full.mp4")), 3)

    def find(phrase: str) -> float:
        target = norm(phrase)
        for i in range(len(words)):
            raw = []
            for j in range(i, min(len(words), i + len(target) + 3)):
                raw.append(words[j]["text"])
                cand = norm(" ".join(raw))
                if cand == target:
                    return round(words[i]["start"], 2)
                if len(cand) > len(target):
                    break
        raise SystemExit(f"anchor not found: {phrase!r}")

    return words, dur, {k: find(v) for k, v in ANCHORS.items()}


# =============================================================================
# THE ARTIFACT — seven regions.  Each builder is position independent: it takes
# an origin and a width and returns (html, height).  ids are global so the state
# tweens below work for every variant.
# =============================================================================
SERVERS = [("gdrive", "Google Drive", 14), ("github", "GitHub", 31),
           ("notion", "Notion", 22), ("slack", "Slack", 18),
           ("gmail", "Gmail", 12), ("airtable", "Airtable", 9),
           ("figma", "Figma", 16), ("elevenlabs", "ElevenLabs", 7)]
assert sum(s[2] for s in SERVERS) == 129
SHOWN, HIDDEN_SERVERS, HIDDEN_TOOLS = 129, 3, 118
TOTAL_TOOLS = SHOWN + HIDDEN_TOOLS          # 247


def eyebrow(eid: str, x: float, y: float, w: float, text: str) -> str:
    return txt(eid, x, y, w, text, 22.0, color=TERRA, weight=700, ls=3.0, mono=True)


def region1(ox: float, oy: float, w: float) -> tuple[str, float]:
    """01 REGISTRY — the naive state: every server, every tool, one big number."""
    h: list[str] = [eyebrow("r1-eb", ox, oy, w, "01 · REGISTRY"),
                    txt("r1-title", ox, oy + 40, w, "TOOL REGISTRY", 56.0),
                    txt("r1-sub", ox, oy + 122, w, f"{TOTAL_TOOLS} tools · 11 servers connected",
                        26.0, color=MUTED, weight=600, upper=False),
                    # the strike takes its width from the measured ink of the
                    # claim it cancels, never from the column (Law 18 spirit)
                    strike("r1-strike", ox, oy + 138,
                           round(0.520 * 26.0 * len(f"{TOTAL_TOOLS} tools · 11 servers connected"), 1))]
    ry = oy + 180
    for i, (key, name, count) in enumerate(SERVERS):
        y = ry + i * 104
        chip_w, chip_h = 148.0, 42.0
        chip_x = ox + w - 24 - chip_w
        inner_row = ""
        h.append(card(f"r1-row{i}", ox, y, w, 92.0, inner_row, bg=PAPER, border="#EBE3D8",
                      bw=1.5, r=16.0))
        h.append(mark(f"r1-m{i}", ox + 54, y + 46, 40.0, key))
        h.append(txt(f"r1-n{i}", ox + 106, y + 46 - 18, 400.0, name, 27.0, mono=True,
                     weight=500, upper=False))
        h.append(txt(f"r1-c{i}", chip_x - 220, y + 46 - 14, 200.0, f"{count} tools", 21.0,
                     color=MUTED, weight=500, mono=True, align="right", upper=False))
        h.append(div(f"r1-chip{i}", chip_x, y + (92 - chip_h) / 2, chip_w, chip_h,
                     f"background:{LINE_2};border-radius:12px;"))
        cty = y + (92 - chip_h) / 2 + 10
        h.append(txt(f"r1-ct{i}a", chip_x, cty, chip_w, "READY", 19.0, color=MUTED,
                     weight=700, mono=True, ls=1.4, align="center"))
        h.append(txt(f"r1-ct{i}b", chip_x, cty, chip_w, "LOADED", 19.0, color=WHITE,
                     weight=700, mono=True, ls=1.4, align="center"))
        h.append(txt(f"r1-ct{i}c", chip_x, cty, chip_w, "—", 19.0, color=MUTED_D,
                     weight=700, mono=True, ls=1.4, align="center"))
    my = ry + len(SERVERS) * 104
    h.append(txt("r1-more", ox, my + 6, w,
                 f"+ {HIDDEN_SERVERS} more servers · {HIDDEN_TOOLS} tools", 24.0,
                 color=MUTED_D, weight=500, mono=True, upper=False))
    h.append(ring("r1-ring", ox - 10, ry - 10, w + 20, len(SERVERS) * 104 - 12 + 20))
    return "\n".join(h), (my + 6 + 32) - oy


def region2(ox: float, oy: float, w: float) -> tuple[str, float]:
    """02 DISCLOSURE — the key term as a real setting, and what it unfolds."""
    cy = oy + 44
    ch = 250.0
    tw_, th = 120.0, 62.0
    tx = ox + w - 32 - tw_
    h: list[str] = [
        eyebrow("r2-eb", ox, oy, w, "02 · DISCLOSURE"),
        card("r2-card", ox, cy, w, ch, "", bw=2.5, r=24.0),
        txt("r2-kicker", ox + 32, cy + 28, 420.0, "AGENT SETTING", 20.0, color=MUTED,
            weight=700, ls=2.2, mono=True),
        txt("r2-name", ox + 32, cy + 60, w - 220, "Procedural disclosure", 48.0, upper=False),
        txt("r2-desc", ox + 32, cy + 134, w - 220,
            "Tools are revealed to the model on demand", 24.0, color=MUTED, weight=500,
            upper=False),
        hair("r2-hair", ox + 32, cy + 186, w - 64),
        txt("r2-code", ox + 32, cy + 202, w - 64, "hermes.tools.disclosure = procedural",
            19.0, color=MUTED_D, weight=400, mono=True, upper=False),
        toggle("r2-tg", tx, cy + 52, tw_, th),
        txt("r2-statea", ox + 32, cy + 202, w - 64, "DISABLED", 20.0, color=MUTED_D,
            weight=700, ls=1.8, mono=True, align="right"),
        txt("r2-stateb", ox + 32, cy + 202, w - 64, "ENABLED", 20.0, color=TERRA,
            weight=700, ls=1.8, mono=True, align="right"),
        ring("r2-ring", ox - 10, cy - 10, w + 20, ch + 20, r=32.0),
    ]
    sy = cy + ch + 76
    h.append(txt("r2-steps-lb", ox, sy, w, "WHEN THE TOGGLE IS ON", 20.0, color=MUTED,
                 weight=700, ls=2.5, mono=True))
    steps = ["Tool schemas stay out of the prompt",
             "The model asks for a capability",
             "Only that tool's schema is injected"]
    by = sy + 42
    for i, s in enumerate(steps):
        y = by + i * 118
        h.append(card(f"r2-step{i}", ox, y, w, 104.0, "", bg=PAPER, border="#EBE3D8", bw=1.5,
                      r=18.0))
        h.append(div(f"r2-bg{i}", ox + 24, y + 30, 44.0, 44.0,
                     f"background:{TERRA};border-radius:22px;"))
        h.append(txt(f"r2-bn{i}", ox + 24, y + 30 + 8, 44.0, str(i + 1), 22.0, color=WHITE,
                     weight=800, align="center", mono=True))
        h.append(txt(f"r2-st{i}", ox + 92, y + 52 - 18, w - 120, s, 26.0, weight=600,
                     upper=False))
    ry = by + len(steps) * 118 + 12
    h.append(card("r2-res", ox, ry, w, 124.0, "", bg=CREAM, border="#E7DFD4", bw=2.0, r=18.0))
    h.append(txt("r2-res-lb", ox + 32, ry + 30, 460.0, "CONTEXT COST PER TURN", 20.0,
                 color=MUTED, weight=700, ls=2.0, mono=True))
    h.append(txt("r2-res-v", ox + 32, ry + 60, w - 64, "1,200 tokens", 44.0, color=TERRA,
                 align="right", mono=True, upper=False))
    return "\n".join(h), (ry + 124.0 + 24) - oy


def region3(ox: float, oy: float, w: float) -> tuple[str, float]:
    """03 THIS TURN — three tools lit, everything else a dim strip."""
    h: list[str] = [eyebrow("r3-eb", ox, oy, w, "03 · THIS TURN"),
                    txt("r3-title", ox, oy + 40, w, "LOADED THIS TURN", 54.0)]
    h.append(txt("r3-big", ox, oy + 118, 200.0, "3", 84.0, color=TERRA))
    h.append(txt("r3-of", ox + 62, oy + 152, 260.0, f"/ {TOTAL_TOOLS}", 38.0, color=MUTED,
                 weight=700, mono=True))
    h.append(txt("r3-tok", ox, oy + 152, w, "1,200 tokens", 28.0, color=INK, weight=700,
                 mono=True, align="right", upper=False))
    ry = oy + 240
    tools = ["fs.read_file", "github.create_pr", "notion.search_pages"]
    for i, t in enumerate(tools):
        y = ry + i * 114
        h.append(card(f"r3-row{i}", ox, y, w, 100.0, "", bw=2.0, border=TERRA, r=18.0))
        h.append(div(f"r3-bar{i}", ox + 2, y + 2, 10.0, 96.0,
                     f"background:{TERRA};border-radius:16px 0 0 16px;"))
        h.append(txt(f"r3-n{i}", ox + 44, y + 50 - 20, 560.0, t, 30.0, mono=True, weight=500,
                     upper=False))
        h.append(div(f"r3-chip{i}", ox + w - 24 - 152, y + 29, 152.0, 42.0,
                     f"background:{TERRA};border-radius:12px;"))
        h.append(txt(f"r3-ct{i}", ox + w - 24 - 152, y + 39, 152.0, "LOADED", 19.0,
                     color=WHITE, weight=700, ls=1.4, mono=True, align="center"))
    sy = ry + len(tools) * 114 + 14
    h.append(card("r3-strip", ox, sy, w, 210.0, "", bg=DIM, border="#DCD3C6", bw=2.0, r=18.0))
    h.append(txt("r3-s1", ox + 32, sy + 30, w - 64, f"{TOTAL_TOOLS - 3} tools · not loaded",
                 28.0, color=MUTED, weight=600, mono=True, upper=False))
    h.append(txt("r3-s2", ox + 32, sy + 78, w - 64, "0 tokens in context", 24.0,
                 color=MUTED_D, weight=500, mono=True, upper=False))
    tick_n, tick_w, tick_gap = 21, 26.0, 14.0
    span = tick_n * tick_w + (tick_n - 1) * tick_gap
    tx0 = ox + (w - span) / 2
    for r in range(2):
        for c in range(tick_n):
            h.append(div(f"r3-tk{r}{c}", tx0 + c * (tick_w + tick_gap), sy + 132 + r * 22,
                         tick_w, 10.0, f"background:#D6CCBE;border-radius:5px;"))
    h.append(ring("r3-ring", ox - 10, oy + 106, 470.0, 108.0, r=20.0))
    return "\n".join(h), (sy + 210.0 + 24) - oy


def region4(ox: float, oy: float, w: float) -> tuple[str, float]:
    """04 CONTEXT — the budget and its hard end-stop."""
    h: list[str] = [eyebrow("r4-eb", ox, oy, w, "04 · CONTEXT"),
                    txt("r4-title", ox, oy + 40, w, "CONTEXT BUDGET", 54.0)]
    cy = oy + 126
    ch = 340.0
    bx, by, bw_, bh = ox + 32, cy + 76, w - 64, 72.0
    h += [card("r4-card", ox, cy, w, ch, "", bw=2.0, r=24.0),
          txt("r4-lb", ox + 32, cy + 28, 520.0, "IF EVERY TOOL LOADS", 20.0, color=MUTED,
              weight=700,
              ls=2.2, mono=True),
          txt("r4-max", ox + 32, cy + 24, w - 64, "200,000 tokens", 24.0, weight=700,
              mono=True, align="right", upper=False),
          bar("r4-track", bx, by, bw_, bh, r=12.0),
          fill("r4-fill", bx, by, bw_, bh, TERRA, r=12.0),
          div("r4-stop", bx + bw_ - 5, by - 16, 8.0, bh + 32,
              f"background:{INK};border-radius:4px;opacity:0;"),
          txt("r4-f1", ox + 32, cy + 180, 460.0, "TOOL SCHEMAS", 20.0, color=TERRA,
              weight=700, ls=2.0, mono=True),
          txt("r4-f2", ox + 32, cy + 180, w - 64, "124,000", 20.0, color=TERRA, weight=700,
              mono=True, align="right", upper=False),
          txt("r4-hard", ox + 32, cy + 214, w - 64, "HARD LIMIT", 20.0, color=INK,
              weight=700, ls=2.0, mono=True, align="right"),
          hair("r4-hair", ox + 32, cy + 258, w - 64),
          txt("r4-note", ox + 32, cy + 280, w - 64,
              "every tool you connect eats the same budget", 24.0, color=MUTED,
              weight=500, upper=False),
          ring("r4-ring", bx - 14, by - 20, bw_ + 28, bh + 40, r=22.0)]
    sy = cy + ch + 66
    segs = [("SYSTEM", 0.12, "#CFC6B8"), ("TOOLS", 0.62, TERRA),
            ("FILES", 0.14, "#B9AF9F"), ("CHAT", 0.12, "#8F8577")]
    h.append(txt("r4-sl", ox, sy, w, "FULLY LOADED, IT LOOKS LIKE THIS", 20.0,
                 color=MUTED, weight=700, ls=2.5, mono=True))
    h.append(card("r4-card2", ox, sy + 40, w, 190.0, "", bw=2.0, r=22.0))
    stack_y = sy + 40 + 28
    inner_w = w - 56
    xacc = ox + 28
    for i, (name, frac, col) in enumerate(segs):
        sw = inner_w * frac
        r_left = "14px 0 0 14px" if i == 0 else "0"
        r_right = "0 14px 14px 0" if i == len(segs) - 1 else "0"
        radius = r_left if i == 0 else (r_right if i == len(segs) - 1 else "0")
        h.append(div(f"r4-sg{i}", xacc, stack_y, sw - (2 if i < len(segs) - 1 else 0), 76.0,
                     f"background:{col};border-radius:{radius};transform-origin:left center;"))
        xacc += sw
    ly = stack_y + 96
    lx = ox + 28
    for i, (name, frac, col) in enumerate(segs):
        h.append(div(f"r4-ld{i}", lx, ly + 8, 16.0, 16.0,
                     f"background:{col};border-radius:8px;"))
        h.append(txt(f"r4-ll{i}", lx + 26, ly, 210.0, name, 20.0, color=MUTED, weight=700,
                     ls=1.4, mono=True))
        lx += inner_w / len(segs)
    return "\n".join(h), (sy + 40 + 190 + 24) - oy


def region5(ox: float, oy: float, w: float) -> tuple[str, float]:
    """05 ACCESS — being picky, expressed as checkboxes that actually uncheck."""
    h: list[str] = [eyebrow("r5-eb", ox, oy, w, "05 · ACCESS"),
                    txt("r5-title", ox, oy + 40, w, "TOOL ACCESS", 54.0),
                    txt("r5-suba", ox, oy + 124, w, "6 servers · 6 granted", 24.0,
                        color=MUTED, weight=500, mono=True, upper=False),
                    txt("r5-subb", ox, oy + 124, w, "6 servers · 3 granted", 24.0,
                        color=TERRA, weight=700, mono=True, upper=False)]
    cw = (w - 24) / 2
    gy = oy + 176
    picks = SERVERS[:6]
    for i, (key, name, _c) in enumerate(picks):
        col, row = i % 2, i // 2
        x = ox + col * (cw + 24)
        y = gy + row * 130
        h.append(card(f"r5-c{i}", x, y, cw, 110.0, "", bg=PAPER, border="#EBE3D8", bw=1.5,
                      r=18.0))
        h.append(checkbox(f"r5-k{i}", x + 24, y + 33, 44.0))
        h.append(mark(f"r5-m{i}", x + 108, y + 55, 34.0, key))
        h.append(txt(f"r5-n{i}", x + 142, y + 55 - 18, cw - 160, name, 26.0, weight=600,
                     upper=False))
    ny = gy + 3 * 130 + 6
    h.append(card("r5-note", ox, ny, w, 110.0, "", bg=CREAM, border="#E7DFD4", bw=2.0,
                  r=18.0))
    h.append(txt("r5-nt", ox + 32, ny + 38, w - 64, "granted per task, not per session",
                 26.0, color=MUTED, weight=600, upper=False))
    # the claim is "the things you give access to" — that is the whole access
    # list, not one column of it (a column-shaped ring read as "these three")
    h.append(ring("r5-ring", ox - 10, gy - 10, w + 20, 3 * 130 - 20 + 20, r=24.0))
    return "\n".join(h), (ny + 110 + 24) - oy


def region6(ox: float, oy: float, w: float) -> tuple[str, float]:
    """06 NOUS RESEARCH — the peak beat.  Two numbers on one surface: the registry
    runs away to infinity while the context readout does not move."""
    cy = oy + 44
    ch = 620.0
    h: list[str] = [eyebrow("r6-eb", ox, oy, w, "06 · NOUS RESEARCH"),
                    card("r6-card", ox, cy, w, ch, "", bg=INK_2, border="#33333A", bw=2.0,
                         r=26.0),
                    mark("r6-mark", ox + 62, cy + 66, 56.0, "nous"),
                    txt("r6-lab", ox + 110, cy + 66 - 18, 520.0, "NOUS RESEARCH", 26.0,
                        color=CREAM, weight=700, ls=2.0, mono=True),
                    txt("r6-sub", ox + 32, cy + 66 - 14, w - 64, "the lab behind Hermes",
                        20.0, color=MUTED_D, weight=500, mono=True, align="right",
                        upper=False),
                    hair("r6-hair", ox + 32, cy + 124, w - 64, DARK_LINE),
                    txt("r6-l1", ox + 32, cy + 164, 460.0, "REGISTRY SIZE", 20.0,
                        color=MUTED_D, weight=700, ls=2.2, mono=True),
                    txt("r6-num", ox + 32, cy + 198, 560.0, str(TOTAL_TOOLS), 124.0,
                        color=CREAM),
                    txt("r6-inf", ox + 32, cy + 176, 560.0, "∞", 168.0, color=CREAM),
                    txt("r6-l2", ox + 32, cy + 164, w - 64, "CONTEXT USED", 20.0,
                        color=MUTED_D, weight=700, ls=2.2, mono=True, align="right"),
                    txt("r6-pct", ox + 32, cy + 214, w - 64, "6%", 96.0, color=TERRA_2,
                        align="right"),
                    bar("r6-bar", ox + 32, cy + 380, w - 64, 18.0, track="#34343A"),
                    # GLOBAL LAW 3 — authored at its REAL 6% width with a live
                    # 9px radius.  The old build authored it full-width and
                    # squashed it with scaleX(0.06), which crushed the radius to
                    # 0.5px: a flat orange brick in a pill track (shot on
                    # artifactspine_v1 t=35-38, the 06-NOUS RESEARCH card).
                    div("r6-fill", ox + 32, cy + 380,
                        max(18.0, 0.06 * (w - 64)), 18.0,
                        f"background:{TERRA_2};border-radius:9px;"),
                    txt("r6-note", ox + 32, cy + 418, w - 64,
                        "pinned · does not grow with the registry", 22.0, color=MUTED_D,
                        weight=500, mono=True, upper=False),
                    hair("r6-hair2", ox + 32, cy + 470, w - 64, DARK_LINE),
                    div("r6-flat", ox + 32, cy + 528, w - 64, 4.0,
                        f"background:{TERRA_2};border-radius:2px;transform-origin:left center;"
                        f"transform:scaleX(0.001);opacity:0;"),
                    txt("r6-flatlb", ox + 32, cy + 548, w - 64, "0 growth", 22.0,
                        color=TERRA_2, weight=700, ls=1.8, mono=True, align="right"),
                    ring("r6-ring", ox + w / 2, cy + 150, w / 2 - 12, 200.0, color=TERRA_2,
                         r=20.0),
                    ring("r6-ring2", ox + 24, cy + 30, 380.0, 72.0, color=TERRA_2, r=20.0)]
    return "\n".join(h), (cy + ch + 24) - oy


def region7(ox: float, oy: float, w: float) -> tuple[str, float]:
    """07 MCP SERVERS — give it everything, and watch the budget not care."""
    h: list[str] = [eyebrow("r7-eb", ox, oy, w, "07 · MCP SERVERS"),
                    txt("r7-title", ox, oy + 40, w, "CONNECT EVERYTHING", 54.0),
                    txt("r7-suba", ox, oy + 124, w, f"11 servers · {TOTAL_TOOLS} tools",
                        24.0, color=MUTED, weight=500, mono=True, upper=False),
                    txt("r7-subb", ox, oy + 124, w, "∞ servers · ∞ tools", 24.0,
                        color=TERRA, weight=700, mono=True, upper=False)]
    ry = oy + 178
    for i, (key, name, _c) in enumerate(SERVERS):
        y = ry + i * 92
        h.append(card(f"r7-row{i}", ox, y, w, 82.0, "", bg=PAPER, border="#EBE3D8", bw=1.5,
                      r=16.0))
        h.append(mark(f"r7-m{i}", ox + 46, y + 41, 34.0, key))
        h.append(txt(f"r7-n{i}", ox + 84, y + 41 - 17, 500.0, name, 26.0, weight=600,
                     upper=False))
        h.append(toggle(f"r7-tg{i}", ox + w - 24 - 76, y + 21, 76.0, 40.0))
    by = ry + len(SERVERS) * 92 + 14
    h += [card("r7-band", ox, by, w, 176.0, "", bg=INK_2, border="#33333A", bw=2.0, r=24.0),
          txt("r7-bl", ox + 32, by + 34, 520.0, "ALL SERVERS", 22.0, color=MUTED_D,
              weight=700, ls=2.2, mono=True),
          txt("r7-inf", ox + 32, by + 56, 300.0, "∞", 84.0, color=CREAM),
          txt("r7-br", ox + 32, by + 96, w - 64, "context unchanged", 24.0, color=TERRA_2,
              weight=700, mono=True, align="right", upper=False),
          ring("r7-ring", ox - 10, ry - 10, w + 20, len(SERVERS) * 92 - 10 + 20, r=22.0)]
    return "\n".join(h), (by + 176 + 24) - oy


REGIONS = [region1, region2, region3, region4, region5, region6, region7]


# =============================================================================
# STATE TWEENS — position independent, shared by all three variants.
# =============================================================================
def region_tweens(a: dict[str, float], arr: list[float], tw: list[str], *,
                  r2_res_t: float | None = None) -> None:
    """`arr[k]` is the moment the spine ARRIVES at region k+1.  Chrome (titles,
    card frames, tracks) is authored painted; the region's ITEMS paint on
    arrival, so no move ever lands on an inert surface and no section spoils
    itself while it is only peeking at the bottom of the window."""
    T = TERRA
    N = len(SERVERS)

    # --- R1: the registry loads, claims the whole window, then is negated -----
    r1_t = max(a["youthink"] + 0.06, arr[0] + 0.40)
    for suffix in ("row{}", "m{}", "n{}", "c{}", "chip{}", "ct{}a"):
        sels = [f"#r1-{suffix.format(i)}" for i in range(N)]
        tw.append(rise_stagger(sels, r1_t, 0.075, 0.34, 20.0))
    for i in range(N):
        tw.append(f'tl.set("#r1-ct{i}b",{{opacity:0}},0);')
        tw.append(f'tl.set("#r1-ct{i}c",{{opacity:0}},0);')
    tw.append(rise("#r1-more", r1_t + N * 0.075, 0.34, 20.0))
    # "loads every tool" — every chip flips to LOADED in a wave
    for i in range(N):
        t = a["loads"] + i * 0.05
        tw.append(f'tl.to("#r1-chip{i}",{{background:"{rgb(T)}",duration:0.22,ease:SOFT}},{t:.2f});')
        tw.append(swap(f"#r1-ct{i}a", f"#r1-ct{i}b", t + 0.04, 0.16))
    tw.append(anno_in("#r1-ring", a["atonce"] + 0.06))
    tw.append(anno_out("#r1-ring", a["spoiler"] + 0.24))
    # "they don't" — the claim is struck and every chip goes cold
    tw.append(f'tl.to("#r1-strike",{{opacity:1,scaleX:1,duration:0.34,ease:SOFT}},'
              f'{a["dont"]:.2f});')
    for i in range(N):
        t = a["dont"] + 0.10 + i * 0.035
        tw.append(f'tl.to("#r1-chip{i}",{{background:"{rgb(LINE_2)}",duration:0.20,ease:SOFT}},{t:.2f});')
        tw.append(swap(f"#r1-ct{i}b", f"#r1-ct{i}c", t, 0.14))

    # --- R2: the setting, and what turning it on unfolds ---------------------
    tw.append(anno_in("#r2-ring", a["crack"] + 0.05))
    tw.append(anno_out("#r2-ring", a["disclosure"] - 0.10))
    d = a["disclosure"] + 0.55                      # lands on the WORD "disclosure"
    tw.append(f'tl.to("#r2-tg-trk",{{background:"{rgb(T)}",borderColor:"{rgb(T)}",'
              f'duration:0.26,ease:SOFT}},{d:.2f});')
    tw.append(f'tl.to("#r2-tg-knb",{{x:58,background:"{rgb(WHITE)}",duration:0.30,'
              f'ease:POP}},{d:.2f});')
    tw.append(f'tl.to("#r2-card",{{borderColor:"{rgb(T)}",duration:0.30,ease:SOFT}},{d:.2f});')
    tw.append('tl.set("#r2-stateb",{opacity:0},0);')
    tw.append(swap("#r2-statea", "#r2-stateb", d + 0.10, 0.18))
    tw.append(rise_stagger([f"#r2-step{i}" for i in range(3)], d + 0.22, 0.13, 0.36, 24.0))
    tw.append(rise_stagger([f"#r2-bg{i}" for i in range(3)], d + 0.22, 0.13, 0.36, 24.0))
    tw.append(rise_stagger([f"#r2-bn{i}" for i in range(3)], d + 0.22, 0.13, 0.36, 24.0))
    tw.append(rise_stagger([f"#r2-st{i}" for i in range(3)], d + 0.22, 0.13, 0.36, 24.0))
    tw.append(rise("#r2-steps-lb", d + 0.18, 0.30, 18.0))
    rt = a["simple"] + 0.10 if r2_res_t is None else r2_res_t
    tw.append(rise("#r2-res", rt, 0.36, 22.0))
    tw.append(rise("#r2-res-lb", rt, 0.36, 22.0))
    tw.append(rise("#r2-res-v", rt + 0.06, 0.36, 22.0))

    # --- R3: three tools lit ------------------------------------------------
    tw.append(rise("#r3-strip", arr[2] + 0.10, 0.34, 20.0))
    tw.append(rise("#r3-s1", arr[2] + 0.16, 0.32, 16.0))
    tw.append(rise("#r3-s2", arr[2] + 0.22, 0.32, 16.0))
    for r in range(2):
        for c in range(21):
            tw.append(rise(f"#r3-tk{r}{c}", arr[2] + 0.30 + (r * 21 + c) * 0.012, 0.22, 8.0))
    for i in range(3):
        t = a["seetools"] + 0.05 + i * 0.30
        tw.append(pop(f"#r3-row{i}", t, 0.34))
        tw.append(pop(f"#r3-bar{i}", t, 0.34))
        tw.append(rise(f"#r3-n{i}", t + 0.04, 0.30, 14.0))
        tw.append(pop(f"#r3-chip{i}", t + 0.10, 0.30))
        tw.append(pop(f"#r3-ct{i}", t + 0.10, 0.30))
    tw.append(count_to("r3-big", a["seetools"] + 0.05, 0, 3, 0.95))
    tw.append(anno_in("#r3-ring", a["needsthem"] + 0.10))
    tw.append(anno_out("#r3-ring", a["consume"] - 0.35))

    # --- R4: the budget, and the wall at the end ----------------------------
    tw.append(rise("#r4-lb", arr[3] + 0.10, 0.32, 16.0))
    tw.append(rise("#r4-max", arr[3] + 0.16, 0.32, 16.0))
    tw.append(rise("#r4-note", arr[3] + 0.26, 0.32, 16.0))
    tw.append(fill_to("r4-fill", a["consume"] + 0.35, 0.62, 0.70))
    tw.append(rise("#r4-f1", a["consume"] + 0.55, 0.30, 14.0))
    tw.append(rise("#r4-f2", a["consume"] + 0.55, 0.30, 14.0))
    tw.append(f'tl.fromTo("#r4-stop",{{opacity:0,scaleY:0.2,transformOrigin:"50% 50%"}},'
              f'{{opacity:1,scaleY:1,duration:0.30,ease:POP,immediateRender:false}},'
              f'{a["finiteword"] + 0.06:.2f});')
    tw.append(rise("#r4-hard", a["finiteword"] + 0.14, 0.30, 12.0))
    tw.append(anno_in("#r4-ring", a["finiteword"] + 0.18))
    tw.append(anno_out("#r4-ring", a["bestway"] + 0.20))
    tw.append(rise("#r4-sl", a["consume"] + 0.70, 0.30, 16.0))
    for i in range(4):
        tw.append(rise(f"#r4-sg{i}", a["consume"] + 0.80 + i * 0.09, 0.30, 16.0))
        tw.append(rise(f"#r4-ld{i}", a["consume"] + 0.80 + i * 0.09, 0.30, 16.0))
        tw.append(rise(f"#r4-ll{i}", a["consume"] + 0.80 + i * 0.09, 0.30, 16.0))

    # --- R5: being picky — three boxes actually uncheck ----------------------
    for i in range(6):
        t = arr[4] + 0.10 + i * 0.075
        for suf in ("c", "k{}-bx", "k{}-tk", "m", "n"):
            sel = (f"#r5-{suf.format(i)}" if "{}" in suf else f"#r5-{suf}{i}")
            tw.append(rise(sel, t, 0.32, 20.0))
    tw.append(rise("#r5-note", arr[4] + 0.62, 0.32, 20.0))
    tw.append(rise("#r5-nt", arr[4] + 0.66, 0.32, 20.0))
    for j, i in enumerate([5, 3, 4]):               # Airtable, Slack, Gmail
        t = a["picky"] + 0.10 + j * 0.22
        tw.append(f'tl.to("#r5-k{i}-bx",{{background:"{rgb(WHITE)}",borderColor:"{rgb(MUTED_D)}",'
                  f'duration:0.24,ease:SOFT}},{t:.2f});')
        tw.append(f'tl.to("#r5-k{i}-tk",{{opacity:0,duration:0.18,ease:EXIT}},{t:.2f});')
        tw.append(f'tl.to("#r5-c{i}",{{opacity:0.42,duration:0.28,ease:SOFT}},{t + 0.04:.2f});')
        tw.append(f'tl.to("#r5-m{i}",{{opacity:0.32,duration:0.28,ease:SOFT}},{t + 0.04:.2f});')
        tw.append(f'tl.to("#r5-n{i}",{{opacity:0.38,duration:0.28,ease:SOFT}},{t + 0.04:.2f});')
    tw.append('tl.set("#r5-subb",{opacity:0},0);')
    tw.append(swap("#r5-suba", "#r5-subb", a["picky"] + 0.72, 0.20))
    tw.append(anno_in("#r5-ring", a["access"] + 0.05))
    tw.append(anno_out("#r5-ring", a["people"] + 0.20))

    # --- R6: the peak — registry runs to infinity, context does not move -----
    tw.append(settle("#r6-card", arr[5] + 0.02, 0.46, 0.965))
    # the card's own interior rules travel WITH it, else two hairlines float in
    # the gap where the card has not arrived yet
    tw.append(fade("#r6-hair", arr[5] + 0.20, 1.0, 0.28))
    tw.append(fade("#r6-hair2", arr[5] + 0.26, 1.0, 0.28))
    tw.append('tl.set("#r6-hair",{opacity:0},0);tl.set("#r6-hair2",{opacity:0},0);')
    tw.append(rise("#r6-mark", arr[5] + 0.16, 0.36, 20.0))
    tw.append(rise("#r6-lab", arr[5] + 0.16, 0.36, 20.0))
    tw.append(rise("#r6-sub", a["lab"] + 0.05, 0.34, 18.0))
    tw.append(anno_in("#r6-ring2", a["nous"] + 0.10))
    tw.append(anno_out("#r6-ring2", a["lab"] + 1.05))
    for k, sel in enumerate(("#r6-l1", "#r6-num", "#r6-l2", "#r6-pct")):
        tw.append(rise(sel, a["lab"] + 0.55 + k * 0.14, 0.36, 22.0))
    tw.append(rise("#r6-bar", a["lab"] + 1.35, 0.34, 18.0))
    tw.append(rise("#r6-fill", a["lab"] + 1.42, 0.34, 18.0))
    tw.append(rise("#r6-note", a["lab"] + 1.52, 0.34, 18.0))
    tw.append(count_to("r6-num", a["everneed"] + 0.10, TOTAL_TOOLS, 21400, 1.30))
    tw.append('tl.set("#r6-inf",{opacity:0},0);')
    tw.append(f'tl.to("#r6-num",{{opacity:0,duration:0.08,ease:EXIT}},'
              f'{a["everneed"] + 1.42:.2f});')
    tw.append(f'tl.fromTo("#r6-inf",{{opacity:0,scale:0.72,transformOrigin:"0% 50%"}},'
              f'{{opacity:1,scale:1,duration:0.44,ease:POP,immediateRender:false}},'
              f'{a["everneed"] + 1.50:.2f});')
    tw.append(f'tl.to("#r6-flat",{{opacity:1,scaleX:1,duration:0.70,ease:SOFT}},'
              f'{a["nolonger"] + 0.10:.2f});')
    tw.append(rise("#r6-flatlb", a["nolonger"] + 0.55, 0.30, 12.0))
    tw.append(anno_in("#r6-ring", a["nolonger"] + 0.15))
    tw.append(anno_out("#r6-ring", a["ifyou"] + 0.10))

    # --- R7: every server on, and the budget does not care -------------------
    for i in range(N):
        t = arr[6] + 0.10 + i * 0.075
        for suf in ("row", "m", "n", "tg{}-trk", "tg{}-knb"):
            sel = (f"#r7-{suf.format(i)}" if "{}" in suf else f"#r7-{suf}{i}")
            tw.append(rise(sel, t, 0.32, 20.0))
    tw.append(rise("#r7-band", arr[6] + 0.78, 0.34, 22.0))
    tw.append(rise("#r7-bl", arr[6] + 0.84, 0.34, 22.0))
    tw.append(anno_in("#r7-ring", arr[6] + 1.20))
    tw.append(anno_out("#r7-ring", a["bloating"] + 0.20))
    for i in range(len(SERVERS)):
        t = a["servers"] + 0.05 + i * 0.075
        tw.append(f'tl.to("#r7-tg{i}-trk",{{background:"{rgb(T)}",borderColor:"{rgb(T)}",'
                  f'duration:0.20,ease:SOFT}},{t:.2f});')
        tw.append(f'tl.to("#r7-tg{i}-knb",{{x:36,background:"{rgb(WHITE)}",duration:0.24,'
                  f'ease:POP}},{t:.2f});')
    tw.append('tl.set("#r7-subb",{opacity:0},0);')
    tw.append(swap("#r7-suba", "#r7-subb", a["andtools"] + 0.26, 0.20))
    tw.append(pop("#r7-inf", a["andtools"] + 0.30, 0.40))
    tw.append(rise("#r7-br", a["andtools"] + 0.46, 0.34, 16.0))


# =============================================================================
# PANEL CHROME + FACE WINDOW + CAPTIONS + AUDIO
# =============================================================================
def header_html(x: float, y: float, w: float) -> str:
    """The panel header.  Always on screen in v1/v2 (it is the panel's own
    chrome, outside the scrolling viewport), and the format's spine device: the
    context meter is introduced ALREADY FULL, never parked empty (Law 20)."""
    bx, bw_ = x + PAD, w - 2 * PAD
    h = [mark("hd-mark", x + PAD + 24, y + 52, 44.0, "nous"),
         txt("hd-name", x + PAD + 60, y + 52 - 21, 560.0, "HERMES AGENT", 32.0, weight=800),
         div("hd-chip", x + w - PAD - 214, y + 32, 214.0, 42.0,
             f"background:{LINE_2};border-radius:12px;"),
         txt("hd-chipt", x + w - PAD - 214, y + 42, 214.0, "tools.config", 20.0, color=MUTED,
             weight=700, mono=True, align="center", upper=False),
         hair("hd-hair", bx, y + 96, bw_),
         # state 0 — a real status line, not an empty vessel
         txt("hd-ready", bx, y + 128, bw_, "REGISTRY SYNCED · AGENT IDLE", 21.0,
             color=MUTED, weight=700, ls=2.0, mono=True),
         div("hd-dot", x + w - PAD - 16, y + 136, 14.0, 14.0,
             f"background:{TERRA};border-radius:7px;"),
         # state 1/2 — the meter, revealed already filling
         txt("hd-lb", bx, y + 118, 460.0, "CONTEXT WINDOW", 19.0, color=MUTED, weight=700,
             ls=2.2, mono=True),
         # the live number and its denominator are separate spans, so the counter
         # can never clobber the constant it is measured against
         (f'<div class="abs mono" id="hd-val" style="left:{n(bx)}px;top:{n(y + 114)}px;'
          f'width:{n(bw_)}px;height:27px;line-height:27px;font-size:21px;text-align:right;'
          f'font-weight:700;color:{INK};text-transform:none;white-space:nowrap">'
          f'<span id="hd-num">0</span><span style="color:{MUTED}"> / 200,000</span></div>'),
         bar("hd-track", bx, y + 150, bw_, HD_BAR_H, r=HD_BAR_R),
         fill("hd-fill", bx, y + 150, bw_, HD_BAR_H, TERRA, r=HD_BAR_R),
         # two tight annotations, each hugging exactly what is being claimed:
         # the READOUT for "all at once", the FILLED END of the bar for
         # "without bloating your context"
         ring("hd-ring", bx + bw_ - 336, y + 108, 348.0, 40.0, r=14.0),
         ring("hd-ring2", bx - 12, y + 146, 214.0, 36.0, r=14.0)]
    return "\n".join(h)


def header_tweens(a: dict[str, float], tw: list[str], *,
                  bloat_ring_t: float | None = None,
                  hd_w: float = WIN_W) -> None:
    """The meter is WITHHELD until the beat that fills it, then drained on the
    beat that refutes it, and it never moves again — that flat line is what the
    last annotation of the video lands on."""
    for sel in ("#hd-lb", "#hd-val", "#hd-track", "#hd-fill"):
        tw.append(f'tl.set("{sel}",{{opacity:0}},0);')
    t = a["loads"] + 0.28
    tw.append(f'tl.to("#hd-ready",{{opacity:0,duration:0.22,ease:EXIT}},{t:.2f});')
    tw.append(f'tl.to("#hd-dot",{{opacity:0,duration:0.22,ease:EXIT}},{t:.2f});')
    for sel in ("#hd-lb", "#hd-val", "#hd-track"):
        tw.append(f'tl.to("{sel}",{{opacity:1,duration:0.26,ease:SOFT}},{t + 0.18:.2f});')
    tw.append(fill_to("hd-fill", t + 0.20, 0.92, 0.62, geom=hd_geom(hd_w)))
    tw.append(count_to("hd-num", t + 0.20, 0, 184000, 0.62))
    tw.append(anno_in("#hd-ring", a["atonce"] + 0.10))
    tw.append(anno_out("#hd-ring", a["spoiler"] + 0.20))
    tw.append('tl.set("#hd-ring2",{opacity:0},0);')
    # refuted: the meter collapses to what procedural disclosure actually costs
    tw.append(fill_to("hd-fill", a["dont"] + 0.06, 0.06, 0.72, geom=hd_geom(hd_w)))
    tw.append(count_to("hd-num", a["dont"] + 0.06, 184000, 12000, 0.72))
    # the final annotation of the video comes home to this bar
    brt = a["bloating"] + 0.55 if bloat_ring_t is None else bloat_ring_t
    tw.append(anno_in("#hd-ring2", brt))
    tw.append(anno_out("#hd-ring2", a["unbelievable"] + 0.80))


def header_value_span() -> str:
    """`hd-val` carries a live number plus a static denominator; the counter only
    ever writes into the span, so the ' / 200,000' can never be clobbered."""
    return ('<span id="hd-num">0</span><span style="color:#716B63"> / 200,000</span>')


def face_html(dur: float) -> str:
    """ONE face element, in the SAME rect as the panel, always in sync with the
    voice because it spans the whole timeline and is only ever switched by
    opacity.  No data-media-start arithmetic can drift."""
    return (f'  <div class="clip" id="facewin" data-start="0" data-duration="{dur:.3f}" '
            f'data-track-index="50" style="left:{n(WIN_X)}px;top:{n(WIN_Y)}px;'
            f'width:{n(WIN_W)}px;height:{n(WIN_H)}px;border-radius:{n(WIN_R)}px;'
            f'overflow:hidden;background:#000;box-shadow:0 26px 64px rgba(20,20,22,0.16)">'
            f'<video id="face" src="assets/v/face_full.mp4" data-start="0" '
            f'data-duration="{dur:.3f}" data-media-start="0" muted playsinline '
            f'style="position:absolute;left:0;top:0;width:100%;height:100%;'
            f'object-fit:cover;object-position:center 38%"></video>'
            f'{outro_lockup()}</div>')


def outro_lockup() -> str:
    """LAW 10 + OUTRO ALIGNMENT — one centred column inside the same window."""
    bx, bw_ = 0.0, WIN_W
    by = WIN_H - 280.0
    return ("".join([
        f'<div class="abs" id="ol-band" style="left:0;top:{n(by)}px;width:{n(bw_)}px;'
        f'height:280px;background:{rgba(CREAM,0.96)};opacity:0"></div>',
        div("ol-rule", (WIN_W - 150) / 2, by + 56, 150.0, 6.0,
            f"background:{TERRA};border-radius:3px;transform-origin:center;"
            f"transform:scaleX(0.001);"),
        txt("ol-handle", bx, by + 98, bw_, OUTRO_HANDLE, 38.0, mono=True, ls=1.6,
            weight=700, align="center", upper=False),
        txt("ol-daily", bx, by + 172, bw_, "daily AI", 17.0, mono=True, ls=6.0, weight=500,
            color=TERRA, align="center", upper=False),
    ]))


def audio_block(dur: float, cues: list[tuple[float, str]]) -> tuple[str, list[str]]:
    """AUDIO MIX LAW: voice 1, bed 0.065, SFX 0.18."""
    els = [f'  <audio id="vo" src="assets/v/audio.m4a" data-start="0" '
           f'data-duration="{dur:.3f}" data-track-index="70" data-volume="{VOICE_VOLUME}">'
           f'</audio>']
    bed_len = probe(STAGE / "music/bed_split.mp3")
    starts, t, i = [], 0.0, 0
    while t < dur - 0.1:
        d = min(bed_len, dur - t)
        starts.append((f"bg{i}", t))
        els.append(f'  <audio id="bg{i}" src="assets/music/bed_split.mp3" '
                   f'data-start="{t:.2f}" data-duration="{d:.2f}" '
                   f'data-track-index="{71 + i}" data-volume="{BED_VOLUME}"></audio>')
        t += bed_len
        i += 1
    lens = {"as_scroll": 0.68, "as_ring": 0.60, "as_snap": 1.00, "as_toggle": 0.48}
    for j, (t0, name) in enumerate(cues):
        if t0 >= dur - 0.15 or t0 < 0:
            continue
        els.append(f'  <audio id="sfx{j}" src="assets/sfx/{name}.mp3" data-start="{t0:.2f}" '
                   f'data-duration="{min(lens[name], dur - t0):.2f}" '
                   f'data-track-index="{90 + j}" data-volume="{SFX_VOLUME}"></audio>')
    tw = [f'tl.to("#{starts[-1][0]}",{{volume:0,duration:1.45}},'
          f'{max(starts[-1][1], dur - 1.5):.2f});']
    return "\n".join(els), tw


def base_css() -> str:
    return f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden;
  font-family:Poppins,sans-serif; background:{CREAM}; }}
.clip {{ position:absolute; }} .abs {{ position:absolute; }}
.disp {{ font-family:Poppins,sans-serif; }}
.mono {{ font-family:'JetBrains Mono',monospace; text-transform:uppercase; }}
.scap {{ left:0; width:1080px; text-align:center; }}
#viewfade-t {{ position:absolute; left:0; top:0; width:100%; height:44px;
  background:linear-gradient(to bottom,{WHITE},rgba(255,253,249,0)); pointer-events:none; }}
#viewfade-b {{ position:absolute; left:0; bottom:0; width:100%; height:118px;
  background:linear-gradient(to top,{WHITE} 22%,rgba(255,253,249,0)); pointer-events:none; }}
.scappill {{ display:inline-block; transform:translateY(-50%); background:{TERRA};
  color:#fff; font-family:Nunito,sans-serif; font-weight:800; padding:19px 34px;
  border-radius:22px; white-space:nowrap; }}
"""


def page(title: str, body: str, tweens: list[str], dur: float) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=1080, height=1920"/>
<title>{esc(title)}</title>{GSAP}{FONTS}<style>{base_css()}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="1080"
 data-height="1920" data-duration="{dur:.3f}" data-fps="{FPS}">
{body}
</div><script>
window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});
const POP="back.out(2.05)";const SOFT="power3.out";const EXIT="power3.in";
const GLIDE="power3.inOut";
{''.join(tweens)}
window.__timelines["main"]=tl;
</script></body></html>"""


def bind_assets(project: Path) -> None:
    project.mkdir(parents=True, exist_ok=True)
    dest = project / "assets"
    if dest.is_symlink():
        dest.unlink()
    elif dest.exists() and not dest.is_dir():
        dest.unlink()
    if not dest.exists():
        dest.symlink_to(STAGE.resolve(), target_is_directory=True)
