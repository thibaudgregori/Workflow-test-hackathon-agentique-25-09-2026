"""mathvoice — KINETIC TYPE lane, run 6 (STANDARD v1.1 + the 2026-08-13 laws).

Lineage: shorts_run5/gen/slop_kinetic_gen.py (Miguel's pilot winner in this lane)
-> shorts_run6/gen/langchain_kinetic_gen.py -> slowfrontier_kinetic_gen.py ->
stolenapp_kinetic_gen.py -> this file.  The measured layout system (`stack` /
`left_for` / `lockup_gap` / `ink_span`, the probed CAP/RANGE tables, the FIXED
`cap_mid`, the 4-step spacing scale), the tween vocabulary, the caption builder
and every build guard are carried over byte-for-byte where they applied —
including `guard_caption_identity` and `guard_shifts`.

WHAT THIS SHORT IS

A mathematician solved an OPEN mathematics problem by talking to ChatGPT Voice.
The winning take walks one argument: he did it with his voice -> here is the post
-> nobody had solved it until now -> the tool was ChatGPT Voice -> so the frontier
to getting work done has dropped, for everyone -> if the hardest problem falls,
so does the rest -> and "the rest" is our busy work, our businesses, our daily
life -> soon most of it is a conversation.

THE BRIEF IS PRUNED BY THE TAKE (elevenagents' rule, stolenapp's second sighting).
The dispatch offers a coffee-cup timescale for the bespoke scene.  Miguel really
does say it — "you can literally just grab a cup of coffee, have a discussion with
ChatGPT" — in dead takes at 353.8-380.2 and 404.1-425.0 of the raw, neither of
which reaches the sign-off.  The LAST COMPLETE take says "the frontier to getting
the work done has actually dropped again significantly", so the bespoke scene is
built on THAT, and no cup appears anywhere.

RUN-6 CONTRACT (agentreviews / erdos / grokpublish / langchain / slowfrontier /
stolenapp / gptvoice):
  * 4K is the deliverable — the design space stays 1080x1920 and the 4K project
    adds `zoom:2` to #root with data-width/height 2160x3840; the face is the
    NATIVE 4K crop (cuts/mathvoice/face_bottom_4k.mp4).
  * The bed is `assets/music/bed_split_v2.mp3` (staged as bed_split.mp3).
  * The outro chip signs `@migueltorrezai`, lowercase.
  * Gate 1 runs on the 1080 DESIGN copy, never on projects_4k.
  * NO `vector-effect="non-scaling-stroke"` anywhere (grokpublish v3).

THE 2026-08-13 LAWS, AS BUILT
  * LAW 12 COLOR MARKS — ChatGPT ships as the official COLOURED app icon, bare at
    the node rect (a coloured tile inside our white plate is plate-on-plate).
  * LAW 13 UNIQUE VISUALIZATION — `THE CLIMB COLLAPSES`, one continuous scene
    across b5+b6 (13.78-21.32), sitting exactly on the story's peak.  Six columns
    whose heights ARE the climb collapse by scaleY about their own base, in two
    stages because he says "dropped AGAIN significantly", and the ground inverts
    on the word "dropped" so the section cut IS the drop.
  * LAW 14 REAL TWEET — the actual @DavidTurturean post (the handed URL is
    @gdb QUOTING it: the erdos trap, third sighting), with two per-LINE marker
    fills landing on the claim as Miguel says it.
  * LAW 15 CENTERED COMPOSITION — every held state of the scene is centred on the
    zone axis by construction, and each stage's dy is asserted against measured
    ink extents rather than eyeballed.  Both intermediate collapse states are
    centred because a linear blend of two centred configurations is centred.
  * LAW 16 NO DEAD SLOTS — all six column slots activate in b5; all six token
    slots fill in b6, one per spoken word across "for / each / and / every /
    single", each on the exact centre of the column whose summit it is.

Layout maths uses REAL measured glyph widths (headless Chromium, same webfonts as
the render), cached to gen/_measure_mathvoice_kinetic.json.
"""
import hashlib
import html as ihtml
import json
import math
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

WORKSPACE = Path.home() / "Documents/Workspace"
FACTORY = WORKSPACE / "projects/personal/content/shorts-factory"
RUN = FACTORY / "shorts_run6"
PUB = FACTORY / "pipeline/assets"
LOGOS = WORKSPACE / "assets/logos"
GEN = RUN / "gen"
CUT = RUN / "cuts/mathvoice"
STAGE = RUN / "stage"
PROJECTS = RUN / "projects"
PROJECTS_4K = RUN / "projects_4k"

POST_ID = "2081955446404112493"       # the handed URL (@gdb) -- a QUOTE
NEWS_POST_ID = "2081780318881677693"  # the QUOTED post (@DavidTurturean) -- the news
SOURCE_JSON = RUN / "plans" / f"source_{POST_ID}.json"
CARD_JSON = RUN / "plans/x_card_mathvoice.json"
CARD_PNG = RUN / "assets/source/mathvoice_card_DavidTurturean.png"
MARK_CHATGPT = LOGOS / "ai-models/chatgpt-color.png"

VID = "mathvoice"
LANE = "kinetic"
NAME = f"{VID}_{LANE}"

S = 1080 / 576
FPS = 30
SEAM = 460
ZONE_H = 460
FACE_H = 564
OVERLAP = 0.15

SAFE_BOTTOM = 410.0
SAFE_TOP = 24.0
SAFE_LEFT = 24.0
SAFE_RIGHT = 552.0

# ---------------------------------------------------------------- layout system
AXIS = 214.0
TIGHT = 16.0
STEP = 30.0
GAP = 46.0
BREAK = 64.0
RULE_H = 7.0

# bump when the measurement PAYLOAD changes shape, so a stale cache can never be
# read as a fresh one (ink + left-side-bearing joined the width on 2026-08-13)
MEASURE_V = "ink-v1"

CAP = {
    "pop": (0.149, 0.880),
    "ser": (0.048, 1.019),
    "mono": (0.453, 1.200),
    "kick": (0.272, 1.029),
}
RANGE = {"pop": (-0.19, 1.21), "ser": (-0.20, 1.10), "mono": (0.00, 1.33),
         "kick": (0.00, 1.31)}


def px(v):
    return round(v * S, 1)


# ---------------------------------------------------------------- tokens
CREAM = "#F6F1EA"
DARK = "#101012"
INK = "#141416"
MUTE = "#6E6A63"
MUTE_D = "#A6A29A"
TERRA = "#C66748"
TERRA_L = "#DD7259"
CAP_TERRA = "#C4573A"
SURFACE = "#FFFCF8"
HL = "rgba(198,103,72,0.32)"      # the marker pen, on the white card
HL_R = 6.0

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800'
    "&family=Nunito:wght@800"
    "&family=Instrument+Serif:ital@0;1"
    '&family=JetBrains+Mono:wght@400;500;700&display=block" rel="stylesheet">'
)
GSAP = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>'

MARK = 84.0            # design units, the bare ChatGPT tile (laws 2 + 12)
CARD_W = 520.0

# law 3 — a metric word anywhere in the VISUAL ZONE is a build failure.
METRIC_WORDS = ("like", "likes", "repost", "reposts", "retweet", "retweets", "view",
                "views", "reply", "replies", "bookmark", "bookmarks", "impression",
                "impressions", "quote", "quotes", "follower", "followers")

# law 4 exemption — ONE class, the video's KEY TERM, which law 9 REQUIRES on
# screen and centre stage.  Set as two display lines that assemble as he names
# them, so neither line's word set can equal the caption pill's.
NAME_LINES = ["CHATGPT", "VOICE"]
KEY_TERM = "CHATGPT VOICE"

# ================================================================ the bespoke
# scene's geometry, all of it derived, none of it typed twice.
COL_N = 6
COL_W = 72.0
COL_GAP = 6.0
COL_PITCH = COL_W + COL_GAP
FLAT_H = 22.0                       # the collapsed floor: a bar you can see
RISE = 40.0                         # one step of the climb
TOK = 34.0                          # the token that sits on a summit
COL_L = round((576.0 - (COL_N * COL_PITCH - COL_GAP)) / 2.0, 1)
# The flat stage closes the gaps: each column widens about its own centre to the
# pitch plus 1.5 design units of overlap.  1.5 is the largest overlap that stays
# under the geometry audit's 3.0-PHYSICAL-px collision floor (1.5 x 1.875 = 2.81px)
# and the smallest that reliably kills the antialiasing hairline at a join.
COL_MERGE_OVER = 1.5
COL_SX_FLAT = round((COL_PITCH + COL_MERGE_OVER) / COL_W, 5)


def col_h(i):
    return FLAT_H + RISE * i


def col_x(i):
    return round(COL_L + i * COL_PITCH, 1)


def col_cx(i):
    return round(col_x(i) + COL_W / 2.0, 1)


# every column's bottom, placed so the FULL scene (summit token top .. base) is
# centred on the zone axis
SCENE_H = col_h(COL_N - 1) + TOK
BASE = round(AXIS + SCENE_H / 2.0, 1)
TOK_FLAT_TOP = round(BASE - FLAT_H - TOK, 1)     # a token seated on the flat bar


def stage_dy(hmax):
    """The dy that centres a scene state whose tallest column is `hmax`."""
    return round(AXIS - (BASE - (hmax + TOK) / 2.0), 1)


def esc(s):
    return ihtml.escape(str(s), quote=False)


def norm(s):
    return "".join(c if (c.isalnum() or c == " ") else " " for c in s.lower()).split()


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(r.stdout.strip())


# ---------------------------------------------------------------- ink geometry
def ink_span(kind, top, fs):
    if kind == "ser":
        return (top - 0.165 * fs, top + 1.085 * fs)
    if kind == "mono":
        return (top + 0.10 * fs, top + 1.42 * fs)
    return (top + 0.07 * fs, top + 1.41 * fs)


def cap_h(kind, fs):
    a, b = CAP[kind]
    return round((b - a) * fs, 2)


def cap_mid(kind, top, fs):
    """NB: `top` is the ELEMENT top, not the cap top that `stack()` returns."""
    a, b = CAP[kind]
    return top + (a + b) / 2.0 * fs


def top_for_cap(kind, cap_top, fs):
    return round(cap_top - CAP[kind][0] * fs, 1)


def und_gap(fs):
    return round(max(12.0, 0.13 * fs), 1)


def _bleed(spec):
    kind, v = spec
    if kind == "box":
        return 0.0, 0.0, v
    rt, rb = RANGE[kind]
    ct, cb = CAP[kind]
    return (ct - rt) * v, (rb - cb) * v, (rb - rt) * v


def lockup_gap(up, dn, want):
    _, bu, hu = _bleed(up)
    ad, _, hd = _bleed(dn)
    tol = 0.16 * min(hu, hd) if (up[0] != "box" and dn[0] != "box") else 0.0
    return round(max(want, bu + ad - tol), 1)


def stack(rows, axis=AXIS):
    """Vertical stack, centred as a BLOCK on the zone's optical axis."""
    total = sum(h for h, _ in rows) + sum(g for _, g in rows[1:])
    y = axis - total / 2.0
    tops = []
    for i, (h, g) in enumerate(rows):
        if i:
            y += g
        tops.append(round(y, 1))
        y += h
    return tops


def left_for(width):
    return round((576.0 - width) / 2.0, 1)


# ---------------------------------------------------------------- tweens
def _ir(ir):
    return "" if ir else ",immediateRender:false"


def fade(sel, t, d=0.34, to=1.0, ir=True):
    return (f'tl.fromTo("{sel}",{{opacity:0}},'
            f'{{opacity:{to},duration:{d},ease:SOFT{_ir(ir)}}},{t:.2f});')


def slam(sel, t, d=0.28, s=1.18, ir=True):
    return (f'tl.fromTo("{sel}",{{scale:{s},opacity:0}},'
            f'{{scale:1,opacity:1,duration:{d},ease:POP{_ir(ir)}}},{t:.2f});')


def popo(sel, t, d=0.32, s=0.78, ir=True):
    return (f'tl.fromTo("{sel}",{{scale:{s},opacity:0}},'
            f'{{scale:1,opacity:1,duration:{d},ease:POP{_ir(ir)}}},{t:.2f});')


def settle(sel, t=0.0, d=0.46, s=0.968, ir=True):
    """Frame-0 safe section opener: already opaque, only settles into place."""
    return (f'tl.fromTo("{sel}",{{scale:{s}}},'
            f'{{scale:1,duration:{d},ease:SOFT{_ir(ir)}}},{t:.2f});')


def wipex(sel, t, d=0.42, frm=0.0, ir=True):
    return (f'tl.fromTo("{sel}",{{scaleX:{frm}}},'
            f'{{scaleX:1,duration:{d},ease:SOFT{_ir(ir)}}},{t:.2f});')


def wipey(sel, t, d=0.40, frm=0.0, ir=True):
    """A column growing out of the base (transform-origin is 50% 100%)."""
    return (f'tl.fromTo("{sel}",{{scaleY:{frm}}},'
            f'{{scaleY:1,duration:{d},ease:SOFT{_ir(ir)}}},{t:.2f});')


def morph(sel, t, frm, to, d=0.46, ir=True):
    """ONE discrete state change of a column: its height, its width and its seat.

    scaleY and y ease identically, so a token glued to the column's top can track
    it with a plain y tween: `BASE + y(t) - h*scaleY(t)` is a linear combination
    of two identically-eased interpolations, hence itself one.

    scaleX is what turns SIX BARS into ONE FLOOR at the flat stage: each column
    widens about its own centre by exactly the gap (plus 1.5 units, so no
    antialiasing hairline survives at the joins), which is why the payoff line can
    say "SAME STARTING LINE" and be describing what is actually on screen.
    """
    sy0, sx0, y0 = frm
    sy1, sx1, y1 = to
    return (f'tl.fromTo("{sel}",{{scaleY:{sy0},scaleX:{sx0},y:{px(y0)}}},'
            f'{{scaleY:{sy1},scaleX:{sx1},y:{px(y1)},duration:{d},'
            f'ease:SOFT{_ir(ir)}}},{t:.2f});')


def sety(sels, y):
    return f'tl.set("{",".join(sels)}",{{y:{px(y)}}},0);'


STEP_LEAD = 0.20
STEP_DUR = 0.36


def stepy(sels, cue, y0, y1, lead=STEP_LEAD, d=STEP_DUR):
    """ONE discrete step as the incoming line lands: the block re-centres itself."""
    return (f'tl.fromTo("{",".join(sels)}",{{y:{px(y0)}}},{{y:{px(y1)},'
            f'duration:{d},ease:SOFT,immediateRender:false}},{cue - lead:.2f});')


# ---------------------------------------------------------------- captions
FILLERS = {"uh", "um", "huh", "mm", "mhm", "erm", "ah", "eh"}
STUTTER_OK = {"ex"}

# ---- proper-noun spelling adjudication (STANDARD law 14, 2026-08-13) ----------
# Scribe heard the mathematician's surname as "Terturian".  The man's own X
# account spells it "Turturean" (plans/x_card_mathvoice.json -> author.name
# "David Turturean", username "DavidTurturean"), and that spelling is already on
# screen inside the real tweet card.  STANDARD law 14 PROPER-NOUN SPELLING: names
# of real people follow the SOURCE PAYLOAD's own spelling, not the transcriber's
# guess.  Leaving both spellings in one short is the actual defect - the card
# says Turturean while the caption under it said Terturian.
#
# This is a DISPLAY adjudication and nothing else, exactly like slowfrontier's
# Soul/Sol: the transcript on disk is untouched, `timings()` still resolves every
# SUBS anchor (including "david terturian solved") against the transcriber's
# tokens, so every section cut lands on the identical frame.  Both spellings are
# 9 characters, so `cap_font` returns the same size and the pill geometry does
# not move either.
CAPTION_SPELLING = {"Terturian": "Turturean"}


def respell(words):
    """Return a DISPLAY copy of the words with proper nouns spelled the way the
    source payload spells them.  Asserted, never assumed: a declared fix that
    never fires fails the build (a silent no-op would ship the wrong name), and
    the timing fields are copied straight through."""
    hits = {k: 0 for k in CAPTION_SPELLING}
    out = []
    for w in words:
        t = w["text"]
        for wrong, right in CAPTION_SPELLING.items():
            if wrong in t:
                t = t.replace(wrong, right)
                hits[wrong] += 1
        d = dict(w)
        d["text"] = t
        out.append(d)
    dead = sorted(k for k, n in hits.items() if n == 0)
    if dead:
        sys.exit(f"LAW 14 PROPER-NOUN SPELLING: declared respell never fired: {dead}")
    return out


def clean_words(words):
    """STANDARD law 6 — stutters and fillers never reach the captions.  The third
    form (grok46) is an immediate repetition of a COMPLETE word."""
    out = []
    for i, w in enumerate(words):
        t = w["text"].strip()
        base = t.strip(".,!?").lower()
        if not t:
            continue
        if base in STUTTER_OK:
            out.append(w)
            continue
        if t.endswith("-") or base in FILLERS:
            continue
        nxt = words[i + 1] if i + 1 < len(words) else None
        if (nxt and nxt["text"].strip(".,!?").lower() == base
                and nxt["start"] - w["end"] < 0.5):
            continue
        out.append(w)
    return out


def build_captions(words):
    words = respell(clean_words(words))
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
def audio_block(dur, cuts, cta, bed_len):
    els, idx = [], 0
    els.append(f'  <audio id="vo" src="assets/v/audio.m4a" data-start="0" '
               f'data-duration="{dur:.2f}" data-track-index="30" data-volume="1"></audio>')
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
    for c in cuts:
        sfx.append((max(0.02, c), "whoosh", 0.68, 0.2))
        sfx.append((c + 0.32, "pop", 0.6, 0.28))
    sfx.append((cta, "whoosh", 0.68, 0.2))
    sfx.append((cta + 0.4, "boom", 0.88, 0.4))
    for t0, name, d, vol in sorted(sfx):
        if t0 >= dur - 0.1:
            continue
        els.append(f'  <audio id="sfx{idx}" src="assets/sfx/{name}.mp3" data-start="{t0:.2f}" '
                   f'data-duration="{min(d, dur - t0):.2f}" data-track-index="{32 + idx}" '
                   f'data-volume="{vol}"></audio>')
        idx += 1
    fade_at = max(bed_ids[-1][1] + 0.1, dur - 1.6)
    return "\n".join(els), [f'tl.to("#{bed_ids[-1][0]}",{{volume:0,duration:1.5}},{fade_at:.2f});']


# ---------------------------------------------------------------- CSS
def base_css(is_4k):
    zoom = " zoom:2;" if is_4k else ""
    return f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden;{zoom}
  font-family:Poppins,sans-serif; }}
.clip {{ position:absolute; }}
.abs {{ position:absolute; }}
.tz {{ left:0; top:0; width:1080px; height:{px(ZONE_H)}px; overflow:hidden; }}
.tz.cream {{ background:{CREAM}; }}
.tz.dark {{ background:{DARK}; }}
.ol {{ transform-origin:0% 50%; }}
/* type */
.pop8 {{ font-weight:800; color:{INK}; letter-spacing:-0.02em; line-height:1.04;
  white-space:nowrap; }}
.pop8.d {{ color:{CREAM}; }}
.mono {{ font-family:'JetBrains Mono',monospace; white-space:nowrap; color:{MUTE};
  letter-spacing:0.04em; }}
.mono.d {{ color:{MUTE_D}; }}
.mut {{ color:{MUTE}; }}
.mut.d {{ color:{MUTE_D}; }}
.tr {{ color:{TERRA}; }}
.tr.d {{ color:{TERRA_L}; }}
/* surfaces */
.strike {{ background:{TERRA}; }}
.strike.d {{ background:{TERRA_L}; }}
.chip {{ display:inline-block; font-family:'JetBrains Mono',monospace; font-weight:700;
  border-radius:{px(18)}px; padding:{px(8)}px {px(18)}px; letter-spacing:{px(1.6)}px;
  text-transform:uppercase; white-space:nowrap;
  background:rgba(246,241,234,0.13); color:{CREAM}; }}
/* THE CLIMB — a column grows out of, and collapses onto, its own base */
.col {{ transform-origin:50% 100%; background:{INK}; }}
.col.d {{ background:{CREAM}; }}
.tok {{ background:{TERRA}; }}
.tok.d {{ background:{TERRA_L}; }}
/* the REAL tweet (law 14) and its marker pen (law 5) */
.shot {{ display:block; object-fit:contain;
  filter:drop-shadow(0 {px(12)}px {px(30)}px rgba(0,0,0,0.35)); }}
.hl {{ background:{HL}; border-radius:{px(HL_R)}px; }}
/* captions */
.scap {{ left:0; width:1080px; text-align:center; }}
.scappill {{ display:inline-block; transform:translateY(-50%); background:{CAP_TERRA};
  color:#fff; font-family:Nunito,sans-serif; font-weight:800;
  padding:{px(10)}px {px(18)}px; border-radius:{px(12)}px; white-space:nowrap; }}
"""


# ---------------------------------------------------------------- scene builder
class Z:
    """One section under construction (design space: 576 x 460 top zone)."""

    def __init__(self, sid, t0, t1, dark, track):
        self.sid = sid
        self.t0, self.t1 = t0, t1
        self.dark = dark
        self.track = track
        self.h, self.tw, self.boxes, self.shifts = [], [], [], []
        self.texts = []
        self.unders = []      # LAW 18 claims: (rule, target atom, text, left, w)

    @property
    def d(self):
        return " d" if self.dark else ""

    def eid(self, n):
        return f"{self.sid}-{n}"

    def add(self, s):
        self.h.append(s)

    def t(self, *s):
        for x in s:
            if isinstance(x, list):
                self.tw += x
            elif x:
                self.tw.append(x)

    # -- guards ---------------------------------------------------------
    def shifted(self, label, dy, names):
        got = {b[0]: b for b in self.boxes}
        for n in names:
            _, left, right, top, bottom = got[n]
            assert bottom + dy <= SAFE_BOTTOM, \
                f"{self.sid}/{n} @ {label}: shifted ink bottom {bottom + dy:.1f}"
            assert top + dy >= SAFE_TOP, \
                f"{self.sid}/{n} @ {label}: shifted ink top {top + dy:.1f}"
        self.shifts.append((label, dy, tuple(names)))

    def moved(self, label, top, bottom, centre=None):
        """A state this section reaches by tween rather than by parking: assert the
        measured extents AND, when it is a scene state, its optical centre."""
        assert top >= SAFE_TOP, f"{self.sid} @ {label}: ink top {top:.1f} < {SAFE_TOP}"
        assert bottom <= SAFE_BOTTOM, \
            f"{self.sid} @ {label}: ink bottom {bottom:.1f} > {SAFE_BOTTOM}"
        if centre is not None:
            got = (top + bottom) / 2.0
            assert abs(got - centre) < 0.05, \
                f"LAW 15 {self.sid} @ {label}: state centre {got:.2f} != {centre:.2f}"
        self.shifts.append((label, 0.0, ("[moved] "
                                         f"{top:.1f}..{bottom:.1f}",)))

    def _check(self, name, left, right, top, bottom):
        self.boxes.append((name, left, right, top, bottom))
        assert bottom <= SAFE_BOTTOM, f"{self.sid}/{name}: ink bottom {bottom:.1f} > {SAFE_BOTTOM}"
        assert top >= SAFE_TOP, f"{self.sid}/{name}: ink top {top:.1f} < {SAFE_TOP}"
        assert left >= SAFE_LEFT, f"{self.sid}/{name}: left {left:.1f} < {SAFE_LEFT}"
        assert right <= SAFE_RIGHT, f"{self.sid}/{name}: right {right:.1f} > {SAFE_RIGHT}"

    # -- primitives -----------------------------------------------------
    def txt(self, name, text, left, top, fs, w, cls="pop8", kind="pop", color=None,
            attrs="", cue=None, html=None):
        it, ib = ink_span(kind, top, fs)
        self._check(name, left, left + w, it, ib)
        self.texts.append((name, text, self.t0 if cue is None else cue, self.t1))
        col = f"color:{color};" if color else ""
        a = (" " + attrs) if attrs else ""
        body = html if html else esc(text)
        self.add(f'<div class="abs {cls}{self.d}" id="{self.eid(name)}"{a} '
                 f'style="left:{px(left)}px;top:{px(top)}px;font-size:{px(fs)}px;{col}">'
                 f'{body}</div>')
        return f"#{self.eid(name)}"

    def ctxt(self, name, text, top, fs, w, cls="pop8", kind="pop", color=None, attrs="",
             html=False, cue=None):
        """Centred text in a full-frame-width box (exempt from margin/offcenter by
        construction: the box IS the frame, so its centre cannot drift)."""
        it, ib = ink_span(kind, top, fs)
        self._check(name, (576 - w) / 2, (576 + w) / 2, it, ib)
        self.texts.append((name, text, self.t0 if cue is None else cue, self.t1))
        col = f"color:{color};" if color else ""
        a = (" " + attrs) if attrs else ""
        body = text if html else esc(text)
        self.add(f'<div class="abs {cls}{self.d}" id="{self.eid(name)}"{a} '
                 f'style="left:0;top:{px(top)}px;width:{px(576)}px;text-align:center;'
                 f'font-size:{px(fs)}px;{col}">{body}</div>')
        return f"#{self.eid(name)}"

    def rect(self, name, left, top, w, h, cls, extra="", attrs="", check=True):
        if check:
            self._check(name, left, left + w, top, top + h)
        a = (" " + attrs) if attrs else ""
        self.add(f'<div class="abs {cls}" id="{self.eid(name)}"{a} '
                 f'style="left:{px(left)}px;top:{px(top)}px;width:{px(w)}px;'
                 f'height:{px(h)}px;{extra}"></div>')
        return f"#{self.eid(name)}"

    def raw(self, s):
        self.add(s)

    def mark(self, name, left, top, size, src):
        """LAW 12 — a brand tile ships BARE: the artwork IS the mark, so a white
        plate under it would be plate-on-plate (gptvoice's ChatGPT rule)."""
        self._check(name, left, left + size, top, top + size)
        self.add(f'<img class="abs" id="{self.eid(name)}" src="{src}" alt="" '
                 f'style="left:{px(left)}px;top:{px(top)}px;width:{px(size)}px;'
                 f'height:{px(size)}px;object-fit:contain"/>')
        return f"#{self.eid(name)}"

    def shot(self, name, left, top, w, h, src, attrs=""):
        self._check(name, left, left + w, top, top + h)
        a = (" " + attrs) if attrs else ""
        self.add(f'<img class="abs shot" id="{self.eid(name)}" src="{src}" alt=""{a} '
                 f'style="left:{px(left)}px;top:{px(top)}px;width:{px(w)}px;'
                 f'height:{px(h)}px"/>')
        return f"#{self.eid(name)}"

    def strike(self, name, left, top, w, h=RULE_H, attrs=""):
        return self.rect(name, left, top, w, h, cls=f"strike{self.d} ol",
                         extra=f"border-radius:{px(h / 2.0)}px", attrs=attrs)

    def underline(self, name, M, target, text, top, fs, kind="pop", attrs=""):
        """LAW 18 — a rule under a phrase spans THAT PHRASE'S INK, and no more.

        Miguel, 2026-08-13: "the line goes beyond the actual size of the words
        that you're underlining ... it looks like it's meant to be a divider when
        in reality it's an underline."  So the width cannot come from the lockup,
        from the widest line of it, or from a constant: it comes from the measured
        ink of the one line sitting above this rule.

        `ctxt` centres the line's ADVANCE box in the 576-wide frame, and the first
        ink starts one left-side-bearing inside that box, so the rule's left edge
        is (576 - adv)/2 + lsb and its width is the ink.  That lands the rule on
        the letters rather than on the paper around them.
        """
        adv, ink, lsb = M.w(text, fs, kind), M.ink(text, fs, kind), M.lsb(text, fs, kind)
        left = round((576.0 - adv) / 2.0 + lsb, 1)
        w = round(ink, 1)
        self.unders.append((name, target, text, left, w))
        return self.strike(name, left, top, w, attrs=attrs)

    def column(self, name, i, attrs=""):
        h = col_h(i)
        return self.rect(name, col_x(i), BASE - h, COL_W, h, cls=f"col{self.d}",
                         attrs=attrs)

    def token(self, name, i, top):
        return self.rect(name, col_cx(i) - TOK / 2.0, top, TOK, TOK,
                         cls=f"tok{self.d}",
                         extra=f"border-radius:{px(round(TOK * 0.28, 1))}px")

    def cchip(self, name, text, top, fs, w):
        h = fs * 1.34 + 16.0
        self._check(name, (576 - w) / 2, (576 + w) / 2, top, top + h)
        self.add(f'<div class="abs" id="{self.eid(name)}" style="left:0;top:{px(top)}px;'
                 f'width:{px(576)}px;text-align:center">'
                 f'<span class="chip" style="font-size:{px(fs)}px;text-transform:none">'
                 f'{esc(text)}</span></div>')
        return f"#{self.eid(name)}"

    def section(self, extra_dur=OVERLAP):
        inner = "\n        ".join(self.h)
        return (f'  <section id="tz-{self.sid}" class="clip tz '
                f'{"dark" if self.dark else "cream"}" data-start="{self.t0:.2f}" '
                f'data-duration="{self.t1 - self.t0 + extra_dur:.2f}" '
                f'data-track-index="{self.track}">\n        {inner}\n  </section>')


# ---------------------------------------------------------------- measurement
M100_POP = ["ONLY HIS VOICE", "AN OPEN PROBLEM", "NOBODY HAD SOLVED IT", "UNTIL NOW",
            "CHATGPT", "VOICE", "SAME", "STARTING LINE", "IF THE HARDEST",
            "PROBLEM FALLS", "BUSY WORK", "BUSINESSES",
            "DAILY LIFE", "SOON MOST OF IT", "IS A CONVERSATION", "FOLLOW",
            "FOR DAILY AI"]
# `.chip` uses PIXEL letter-spacing, so it must be probed at the size it ships at.
MFIX = [("handle", "chip", 16.0, "@migueltorrezai", False)]


def measure():
    """Three numbers per string, all measured, none estimated.

    `w`   the ADVANCE box — what `ctxt` centres in the frame.
    `ink` the painted extent — what LAW 18 says an underline may span.
    `lsb` how far inside the advance box the first ink starts.

    The advance box is NOT the ink: side bearings put 4-18 physical px of empty
    paper inside each end of a display line at these sizes, so a rule cut to the
    advance box already overhangs the letters it underlines.
    """
    specs = ([(f"pop::{t}", "pop8", 100, t, False) for t in M100_POP]
             + [(k, c, fs, t, raw) for k, c, fs, t, raw in MFIX])
    sig = hashlib.sha1(json.dumps([specs, MEASURE_V], ensure_ascii=False)
                       .encode()).hexdigest()[:12]
    cache = GEN / f"_measure_{NAME}.json"
    if cache.exists():
        blob = json.loads(cache.read_text())
        if blob.get("sig") == sig:
            return blob
    from playwright.sync_api import sync_playwright

    items = "".join(
        f'<span id="m{i}" class="{c}" style="font-size:{px(fs)}px'
        f'{";text-transform:none" if c == "chip" else ""}">'
        f'{t if raw else esc(t)}</span>'
        for i, (k, c, fs, t, raw) in enumerate(specs))
    page = (f'<!doctype html><html><head><meta charset="utf-8"/>{FONTS}'
            f'<style>{base_css(False)}'
            f'#probe{{position:absolute;left:0;top:0}}'
            f'#probe span{{display:inline-block;margin:0 80px 80px 0}}</style></head>'
            f'<body><div id="root"><div id="probe">{items}</div>'
            f'<canvas id="mcv" width="8" height="8"></canvas></div></body></html>')
    tmp = GEN / f"_measure_{NAME}.html"
    tmp.write_text(page, encoding="utf-8")
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto(tmp.as_uri())
        pg.evaluate("Promise.race([document.fonts.ready,"
                    " new Promise(r => setTimeout(r, 9000))])")
        pg.wait_for_timeout(300)
        ok = pg.evaluate("() => document.fonts.check('800 100px Poppins')"
                         " && document.fonts.check('500 40px Poppins')"
                         " && document.fonts.check('700 100px \"JetBrains Mono\"')")
        if not ok:
            br.close()
            sys.exit("MEASURE FAILED: webfonts did not load; layout would not match render")
        rows = pg.evaluate("""(n) => Array.from({length:n}, (_, i) => {
          const el = document.getElementById('m' + i);
          const cs = getComputedStyle(el);
          const plain = el.className === 'pop8';   // no padding, no text-transform
          const adv = el.getBoundingClientRect().width;
          if (!plain) return {adv, plain};
          const ctx = document.getElementById('mcv').getContext('2d');
          ctx.font = cs.fontStyle + ' ' + cs.fontWeight + ' ' + cs.fontSize
                   + ' ' + cs.fontFamily;
          ctx.letterSpacing = cs.letterSpacing === 'normal' ? '0px' : cs.letterSpacing;
          ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
          const m = ctx.measureText(el.textContent);
          return {adv, plain, cadv: m.width,
                  ink: m.actualBoundingBoxRight + m.actualBoundingBoxLeft,
                  lsb: -m.actualBoundingBoxLeft};
        })""", len(specs))
        br.close()
    # ink is measured on the CANVAS and the layout is laid out by the DOM, so the
    # two have to be setting the same typeset — assert their advance widths agree
    # before trusting an ink extent.  (Chip strings are padded and uppercased by
    # CSS, so canvas cannot see what the DOM draws; they get no ink and LAW 18
    # never asks them for one.)
    ink_rows = [(k, r) for (k, *_), r in zip(specs, rows) if r["plain"]]
    for k, r in ink_rows:
        if abs(r["cadv"] - r["adv"]) > 1.0:
            sys.exit(f"MEASURE FAILED: canvas advance {r['cadv']:.2f} != DOM advance "
                     f"{r['adv']:.2f} for {k}; the ink extents are not this typeset's")
    out = {"sig": sig,
           "w": {k: round(r["adv"] / S, 2) for (k, *_), r in zip(specs, rows)},
           "ink": {k: round(r["ink"] / S, 2) for k, r in ink_rows},
           "lsb": {k: round(r["lsb"] / S, 2) for k, r in ink_rows}}
    cache.write_text(json.dumps(out, indent=1))
    tmp.unlink()
    return out


class Mx:
    def __init__(self, blob):
        self.raw = blob["w"]
        self.raw_ink = blob["ink"]
        self.raw_lsb = blob["lsb"]

    def w(self, text, fs, kind="pop"):
        return round(self.raw[f"{kind}::{text}"] * fs / 100.0, 2)

    def ink(self, text, fs, kind="pop"):
        """The PAINTED width of the string — LAW 18's ruler."""
        return round(self.raw_ink[f"{kind}::{text}"] * fs / 100.0, 2)

    def lsb(self, text, fs, kind="pop"):
        """Empty paper between the advance box's left edge and the first ink."""
        return round(self.raw_lsb[f"{kind}::{text}"] * fs / 100.0, 2)

    def fit(self, text, fs_max, avail, kind="pop"):
        w100 = self.raw[f"{kind}::{text}"]
        return math.floor(min(fs_max, (avail - 1.0) * 100.0 / w100) * 10.0) / 10.0

    def fit_all(self, texts, fs_max, avail, kind="pop"):
        """One size for a set of lines that must read as ONE object."""
        return min(self.fit(t, fs_max, avail, kind) for t in texts)

    def fx(self, key):
        return self.raw[key]


# ================================================================ the lane
def sec1(C, M):
    """0.00-4.68 cream — the hook, in the order he says it.

    He names the instrument first ("using only AI and his voice") and the target
    last ("an open mathematics problem"), so the lockup builds in that order and
    the rule arrives between them, on the word "voice".
    """
    s = C["s"]
    z = Z("b1", 0.00, 4.679, False, 2)

    hf = M.fit_all(["ONLY HIS VOICE", "AN OPEN PROBLEM"], 92.0, 512.0)
    aw, bw = M.w("ONLY HIS VOICE", hf), M.w("AN OPEN PROBLEM", hf)
    y_a, y_u, y_b = stack([
        (cap_h("pop", hf), 0.0),
        (RULE_H, und_gap(hf)),
        (cap_h("pop", hf), lockup_gap(("box", RULE_H), ("pop", hf), GAP)),
    ])
    a = z.ctxt("hero", "ONLY HIS VOICE", top_for_cap("pop", y_a, hf), hf, aw)
    # LAW 18: this rule underlines ONLY HIS VOICE, so it is that line's ink wide.
    # It used to take max(aw, bw) — the width of AN OPEN PROBLEM, the line BELOW
    # it — and overhung the words above by 303 physical px at 4K.
    u = z.underline("u", M, "hero", "ONLY HIS VOICE", y_u, hf)
    b = z.ctxt("hero2", "AN OPEN PROBLEM", top_for_cap("pop", y_b, hf), hf, bw,
               color=TERRA, cue=s["solve"])
    # BUILD ORDER: the rule follows the line it belongs to, never precedes it.
    z.t(settle(a, z.t0, 0.46),
        wipex(u, s["voice1"], 0.42),
        slam(b, s["solve"], 0.34, 1.22))
    d1 = round(AXIS - (y_a + cap_h("pop", hf) / 2.0), 1)
    d2 = round(AXIS - (y_a + (y_u + RULE_H)) / 2.0, 1)
    z.t(sety([a], d1), stepy([a], s["voice1"], d1, d2),
        sety([u], d2), stepy([a, u], s["solve"], d2, 0.0))
    z.shifted("hero alone", d1, ["hero"])
    z.shifted("+ rule", d2, ["hero", "u"])
    return z


def sec2(C, M):
    """4.68-8.34 dark — LAW 14: the REAL post, alone, with the marker pen.

    The handed URL is @gdb quoting this; the card is the QUOTED author's, which
    `guard_provenance` asserts rather than remembers.  The claim wraps across two
    lines, so the highlight is two per-LINE fills — a union box would cover the
    whole tweet and scope nothing, which is the one job law 5 gives a highlight.
    """
    m = C["media"]
    z = Z("b2", 4.679, 8.340, True, 3)
    ch = m["card_h"]
    cl, ct = left_for(CARD_W), round(AXIS - ch / 2.0, 1)
    card = z.shot("card", cl, ct, CARD_W, ch, m["card"], attrs="data-source-quote")
    z.t(settle(card, z.t0, 0.46, 0.972))
    for i, r in enumerate(C["card_rects"]):
        sel = z.rect(f"hl{i}", round(cl + r["x"] * CARD_W, 1), round(ct + r["y"] * ch, 1),
                     round(r["w"] * CARD_W, 1), round(r["h"] * ch, 1),
                     cls="hl ol", attrs="data-overlap-ok")
        z.t(wipex(sel, C["s"]["solved"] + 0.10 * i, 0.34))
    return z


def sec3(C, M):
    """8.34-10.76 cream — an OPEN problem is one nobody has closed."""
    s = C["s"]
    z = Z("b3", 8.340, 10.760, False, 4)

    kf = M.fit("NOBODY HAD SOLVED IT", 46.0, 470.0)
    hf = M.fit("UNTIL NOW", 112.0, 512.0)
    kw, hw = M.w("NOBODY HAD SOLVED IT", kf), M.w("UNTIL NOW", hf)
    y_k, y_u, y_h = stack([
        (cap_h("pop", kf), 0.0),
        (RULE_H, und_gap(kf)),
        (cap_h("pop", hf), lockup_gap(("box", RULE_H), ("pop", hf), GAP)),
    ])
    k = z.ctxt("w1", "NOBODY HAD SOLVED IT", top_for_cap("pop", y_k, kf), kf, kw)
    # LAW 18: already the right LINE, but `kw` is the advance box — 5 physical px
    # at 4K wider than the letters.  The ink is the ruler.
    u = z.underline("u", M, "w1", "NOBODY HAD SOLVED IT", y_u, kf)
    h = z.ctxt("hero", "UNTIL NOW", top_for_cap("pop", y_h, hf), hf, hw, color=TERRA,
               cue=s["untilnow"])
    z.t(settle(k, z.t0, 0.44),
        wipex(u, s["rule3"], 0.42),
        slam(h, s["untilnow"], 0.34, 1.22))
    d1 = round(AXIS - (y_k + (y_u + RULE_H)) / 2.0, 1)
    z.t(sety([k, u], d1), stepy([k, u], s["untilnow"], d1, 0.0))
    z.shifted("headline + rule", d1, ["w1", "u"])
    return z


def sec4(C, M):
    """10.76-13.78 dark — LAW 9: the key term, centre stage, on its own words.

    LAW 2 + LAW 12: ChatGPT is the one named product in this narration, so it is
    its official COLOURED app icon, and the tile ships BARE — a coloured square
    inside our white plate is plate-on-plate.  The two display lines land on the
    two times he says the name, so the term assembles as he speaks it; that also
    keeps either line's word set from equalling the caption pill's.
    """
    s, m = C["s"], C["media"]
    # b4 runs to "frontier" rather than to "This": cut at 13.779 the key term's
    # second line lands at 13.52 and the section ends 0.26s later, i.e. law 9's
    # centre-stage term would exist for eight frames.  Held to 14.619 it reads for
    # 1.10s, and the scene that follows loses nothing: its own opening state is a
    # flat ground with no claim in it.
    z = Z("b4", 10.760, 14.619, True, 5)

    # HEIGHT binds here, not width (stolenapp: "under a plate, HEIGHT binds the
    # hero").  With an 84-unit mark above them, two display lines at 100 put the
    # second line's ink 17 units past the 410 seam floor; 82 is the largest size
    # whose ink clears it, and it still ships the key term at 154 physical px.
    nf = M.fit_all(["CHATGPT", "VOICE"], 82.0, 500.0)
    n1w, n2w = M.w("CHATGPT", nf), M.w("VOICE", nf)
    y_m, y_n1, y_n2 = stack([
        (MARK, 0.0),
        (cap_h("pop", nf), lockup_gap(("box", MARK), ("pop", nf), STEP)),
        (cap_h("pop", nf), lockup_gap(("pop", nf), ("pop", nf), TIGHT)),
    ])
    mk = z.mark("mk", left_for(MARK), y_m, MARK, m["chatgpt"])
    n1 = z.ctxt("n1", "CHATGPT", top_for_cap("pop", y_n1, nf), nf, n1w, attrs="data-name",
                cue=s["gpt1"])
    n2 = z.ctxt("n2", "VOICE", top_for_cap("pop", y_n2, nf), nf, n2w, color=TERRA_L,
                attrs="data-name", cue=s["gpt2"])
    z.t(settle(mk, z.t0, 0.46),
        slam(n1, s["gpt1"], 0.32, 1.16),
        slam(n2, s["gpt2"], 0.32, 1.16))
    d1 = round(AXIS - (y_m + MARK / 2.0), 1)
    d2 = round(AXIS - (y_m + (y_n1 + cap_h("pop", nf))) / 2.0, 1)
    z.t(sety([mk], d1), stepy([mk], s["gpt1"], d1, d2),
        sety([n1], d2), stepy([mk, n1], s["gpt2"], d2, 0.0))
    z.shifted("mark alone", d1, ["mk"])
    z.shifted("+ CHATGPT", d2, ["mk", "n1"])
    return z


def sec5(C, M):
    """13.78-17.68 cream — LAW 13, part 1: THE CLIMB.

    Six columns whose heights ARE the climb (22 + 40i design units), all bottoms
    on one base, pitch 78 with a 6-unit gap so nothing ever touches.

    LAW 15, THE HORIZONTAL HALF.  The first cut of this beat drew the columns one
    at a time, left to right, and every partial state sat in the LEFT half of the
    frame with the right half empty — the "not centred for some reason" class
    Miguel caught on smallteams, in the axis this lane usually gets for free
    because its atoms are full-width centred text.  A run of boxes has no such
    luck.  The fix is not a horizontal park: it is to DRAW EVERY SLOT FROM THE
    FIRST FRAME.  All six start at the floor height (a row of equal slabs, 3.6%
    top-zone ink, no thin frame either) and RISE into the climb on their cues, so
    the composition is horizontally centred at every instant by construction and
    LAW 16 is satisfied before the beat even starts.

    It also makes the scene a palindrome: the ground rises into a climb here, and
    the climb falls back to ground in b6, with the same six elements.

    Vertically the block still re-centres at every arrival (the lane's own
    parked-offset grammar), which is what makes LAW 15 true at every held instant
    rather than only at the end.
    """
    s = C["s"]
    z = Z("b5", 14.619, 17.680, False, 6)

    cols = [z.column(f"c{i}", i) for i in range(COL_N)]
    tok = z.token("tk", COL_N - 1, BASE - col_h(COL_N - 1) - TOK)

    # column 0 IS the floor height, so it is complete at frame 0 and only settles.
    z.t(settle(cols[0], z.t0, 0.46))
    groups = [([1, 2], s["getting"]), ([3, 4], s["work"]), ([5], s["done"])]
    for idxs, cue in groups:
        for j, i in enumerate(idxs):
            z.t(wipey(cols[i], cue + 0.08 * j, 0.46,
                      frm=round(FLAT_H / col_h(i), 5)))

    # the dy that centres a state whose tallest column is `hmax`, with no token yet
    hmaxes = [FLAT_H] + [col_h(max(idxs)) for idxs, _ in groups]
    d = [round(AXIS - (BASE - h / 2.0), 1) for h in hmaxes]
    cues = [cue for _, cue in groups] + [s["hasdrop"]]
    z.t(sety(cols, d[0]))
    for k in range(len(groups)):
        z.t(stepy(cols, cues[k], d[k], d[k + 1]))
    z.t(sety([tok], d[3]))
    z.t(popo(tok, s["hasdrop"], 0.34, 0.72))
    z.t(stepy(cols + [tok], s["hasdrop"], d[3], 0.0))

    for k, h in enumerate(hmaxes):
        z.moved(f"tallest {h:g} centred", BASE - h + d[k], BASE + d[k], AXIS)
        assert BASE - h + d[k] >= SAFE_TOP and BASE + d[k] <= SAFE_BOTTOM, \
            f"b5 stage {k} leaves the safe band"
    z.moved("full climb", BASE - col_h(COL_N - 1) - TOK, BASE, AXIS)
    # the summit token enters glued to column 5's top and rides home with it
    assert abs((BASE - col_h(COL_N - 1) - TOK + d[3])
               - (BASE - col_h(COL_N - 1) + d[3] - TOK)) < 1e-9
    return z


def sec6(C, M):
    """17.68-21.32 dark — LAW 13, part 2: THE DROP.

    The ground inverts ON the word "dropped", so the section cut IS the drop.  The
    columns then collapse by `scaleY` about their own base, in TWO stages because
    he says "dropped AGAIN significantly": half first (heights 18/38/58/78/98/118,
    a staircase of half the rise), then flat (all 18).

    Both intermediate states are centred, and not by luck: the group carries a dy
    per stage, and a linear blend of two centred configurations is centred, so the
    motion between stages is centred at every frame too.

    LAW 16: the five remaining token slots fill, one per spoken word across
    "for / each / and / every / single", left to right, each on the exact centre of
    the column whose summit it is.
    """
    s = C["s"]
    # b6 runs to "can" rather than to "If": the payoff lockup lands at 21.02 and a
    # 21.319 cut would show the finished composition for 0.30s — the climax of the
    # whole bespoke scene, gone before it registers.  Held to 22.239 it reads for
    # 1.22s.
    z = Z("b6", 17.680, 22.239, True, 7)

    # TWO display lines, not one: `SAME STARTING LINE` on a single line fits the
    # 516-unit band at about 46 design units and leaves the payoff composition
    # occupying 136 of the zone's 460 — a small object in a frame the climb has
    # just vacated. Broken in two it carries 64, and the block fills the space the
    # collapse opened up, which is what the beat is FOR.
    hf = M.fit_all(["SAME", "STARTING LINE"], 78.0, 516.0)
    h1w, h2w = M.w("SAME", hf), M.w("STARTING LINE", hf)
    y_h1, y_h2, y_floor = stack([
        (cap_h("pop", hf), 0.0),
        (cap_h("pop", hf), lockup_gap(("pop", hf), ("pop", hf), TIGHT)),
        (TOK + FLAT_H, lockup_gap(("pop", hf), ("box", TOK + FLAT_H), BREAK)),
    ])
    bar_top = round(y_floor + TOK, 1)

    h_full = [col_h(i) for i in range(COL_N)]
    h_half = [round((col_h(i) + FLAT_H) / 2.0, 2) for i in range(COL_N)]
    dy0 = 0.0
    dy1 = stage_dy(max(h_half))
    dy2 = stage_dy(FLAT_H)
    dy3 = round(bar_top - (BASE - FLAT_H), 1)

    cols = [z.column(f"c{i}", i) for i in range(COL_N)]
    toks = [z.token(f"t{i}", i, TOK_FLAT_TOP) for i in range(COL_N)]

    for i in range(COL_N):
        s1 = round(h_half[i] / h_full[i], 5)
        s2 = round(FLAT_H / h_full[i], 5)
        z.t(morph(cols[i], z.t0, (1.0, 1.0, dy0), (s1, 1.0, dy1), 0.46),
            morph(cols[i], s["flat"], (s1, 1.0, dy1), (s2, COL_SX_FLAT, dy2),
                  0.46, ir=False))
    # the merged floor: assert the extents the audit never sees, because they are
    # reached by transform rather than authored
    merged_l = round(col_cx(0) - COL_W * COL_SX_FLAT / 2.0, 2)
    merged_r = round(col_cx(COL_N - 1) + COL_W * COL_SX_FLAT / 2.0, 2)
    assert merged_l >= SAFE_LEFT and merged_r <= SAFE_RIGHT, \
        f"merged floor {merged_l}..{merged_r} leaves the safe band"
    assert abs((merged_l + merged_r) / 2.0 - 288.0) < 0.05, \
        f"LAW 15: merged floor centre {(merged_l + merged_r) / 2.0} != 288"
    over = COL_W * COL_SX_FLAT - COL_PITCH
    assert abs(over - COL_MERGE_OVER) < 0.01, f"merge overlap drifted: {over}"
    assert over * S < 3.0, \
        "merge overlap would trip the geometry audit's collision floor"
    z.t(stepy(cols, s["hero6"], dy2, dy3))

    # the summit token is glued to column 5's top; it is authored on the FLAT seat
    # like its five siblings and parked up to the summit, so from the flat stage on
    # all six share one y and one final step.
    summit = toks[COL_N - 1]
    y_s0 = round(BASE - col_h(COL_N - 1) - TOK - TOK_FLAT_TOP, 1)
    y_s1 = round((BASE + dy1 - max(h_half)) - TOK - TOK_FLAT_TOP, 1)
    z.t(sety([summit], y_s0),
        f'tl.fromTo("{summit}",{{y:{px(y_s0)}}},{{y:{px(y_s1)},duration:0.46,'
        f'ease:SOFT,immediateRender:false}},{z.t0:.2f});',
        f'tl.fromTo("{summit}",{{y:{px(y_s1)}}},{{y:{px(dy2)},duration:0.46,'
        f'ease:SOFT,immediateRender:false}},{s["flat"]:.2f});')

    others = [toks[i] for i in range(COL_N - 1)]
    z.t(sety(others, dy2))
    for i, cue in enumerate(C["tokcues"]):
        z.t(popo(others[i], cue, 0.30, 0.62))
    z.t(stepy(toks, s["hero6"], dy2, dy3))

    hero1 = z.ctxt("hero", "SAME", top_for_cap("pop", y_h1, hf), hf, h1w,
                   color=TERRA_L, cue=s["hero6"])
    hero2 = z.ctxt("hero2", "STARTING LINE", top_for_cap("pop", y_h2, hf), hf, h2w,
                   color=TERRA_L, cue=s["hero6"])
    z.t(slam(hero1, s["hero6"], 0.34, 1.20),
        slam(hero2, s["hero6"] + 0.10, 0.34, 1.20))

    z.moved("stage 0 — the climb, inherited", BASE - col_h(5) - TOK, BASE, AXIS)
    z.moved("stage 1 — half", BASE + dy1 - max(h_half) - TOK, BASE + dy1, AXIS)
    z.moved("stage 2 — flat", BASE + dy2 - FLAT_H - TOK, BASE + dy2, AXIS)
    z.moved("stage 3 — seated under the line", TOK_FLAT_TOP + dy3, BASE + dy3)
    assert abs((TOK_FLAT_TOP + dy3) - y_floor) < 0.05, \
        f"floor unit does not land on its stack seat: {TOK_FLAT_TOP + dy3} vs {y_floor}"
    assert ink_span("pop", top_for_cap("pop", y_h2, hf), hf)[1] < y_floor, \
        "the hero lockup's ink overlaps the token row"
    return z


def sec7(C, M):
    """22.24-25.86 cream — if the hardest one falls, so does the rest.

    The "so does the rest" line is NOT typeset here: it landed at 25.62 against a
    25.859 cut, i.e. it held for seven frames.  The next section IS the rest —
    busy work, businesses, daily life — so the argument is completed by the cut
    rather than by a fourth atom nobody has time to read.
    """
    s = C["s"]
    z = Z("b7", 22.239, 25.859, False, 8)

    hf = M.fit_all(["IF THE HARDEST", "PROBLEM FALLS"], 92.0, 512.0)
    aw, bw = M.w("IF THE HARDEST", hf), M.w("PROBLEM FALLS", hf)
    y_a, y_b, y_u = stack([
        (cap_h("pop", hf), 0.0),
        (cap_h("pop", hf), lockup_gap(("pop", hf), ("pop", hf), TIGHT)),
        (RULE_H, und_gap(hf)),
    ])
    a = z.ctxt("hero", "IF THE HARDEST", top_for_cap("pop", y_a, hf), hf, aw)
    b = z.ctxt("hero2", "PROBLEM FALLS", top_for_cap("pop", y_b, hf), hf, bw, color=TERRA,
               cue=s["falls"])
    # LAW 18: the rule sits under PROBLEM FALLS, so that is the line it measures.
    # max(aw, bw) happened to pick the same line here only because PROBLEM FALLS
    # is the wider of the two — an accident, not a rule.
    u = z.underline("u", M, "hero2", "PROBLEM FALLS", y_u, hf)
    z.t(settle(a, z.t0, 0.44),
        slam(b, s["falls"], 0.34, 1.18),
        wipex(u, s["way"], 0.42))
    d1 = round(AXIS - (y_a + cap_h("pop", hf) / 2.0), 1)
    z.t(sety([a], d1), stepy([a], s["falls"], d1, 0.0))
    z.shifted("first line alone", d1, ["hero"])
    return z


def sec8(C, M):
    """25.86-29.40 dark — the rest, named: three centred lines, one size.

    Centred rather than rail-aligned: these three are peers with no order claim
    (stolenapp numbered its rows because Miguel said "and most importantly"; he
    says nothing of the kind here), so a shared optical centre is the honest
    treatment and it keeps LAW 15 trivially true.
    """
    s = C["s"]
    z = Z("b8", 25.859, 29.840, True, 9)

    rf = M.fit_all(["BUSY WORK", "BUSINESSES", "DAILY LIFE"], 62.0, 470.0)
    rows = ["BUSY WORK", "BUSINESSES", "DAILY LIFE"]
    ws = [M.w(t, rf) for t in rows]
    ch = cap_h("pop", rf)
    tops = stack([(ch, 0.0)] + [(ch, lockup_gap(("pop", rf), ("pop", rf), STEP))
                                for _ in rows[1:]])
    cues = [z.t0, s["biz"], s["daily"]]
    sels = [z.ctxt(f"r{i}", t, top_for_cap("pop", tops[i], rf), rf, ws[i],
                   color=(TERRA_L if i == 2 else None), cue=cues[i])
            for i, t in enumerate(rows)]
    z.t(settle(sels[0], z.t0, 0.44),
        slam(sels[1], s["biz"], 0.32, 1.16),
        slam(sels[2], s["daily"], 0.32, 1.16))
    d1 = round(AXIS - (tops[0] + ch / 2.0), 1)
    d2 = round(AXIS - (tops[0] + (tops[1] + ch)) / 2.0, 1)
    z.t(sety([sels[0]], d1), stepy([sels[0]], s["biz"], d1, d2),
        sety([sels[1]], d2), stepy(sels[:2], s["daily"], d2, 0.0))
    z.shifted("row 1 alone", d1, ["r0"])
    z.shifted("rows 1-2", d2, ["r0", "r1"])
    return z


def sec9(C, M):
    """29.40-33.42 cream — the thesis."""
    s = C["s"]
    z = Z("b9", 29.840, 33.419, False, 10)

    hf = M.fit_all(["SOON MOST OF IT", "IS A CONVERSATION"], 86.0, 512.0)
    aw, bw = M.w("SOON MOST OF IT", hf), M.w("IS A CONVERSATION", hf)
    y_a, y_u, y_b = stack([
        (cap_h("pop", hf), 0.0),
        (RULE_H, und_gap(hf)),
        (cap_h("pop", hf), lockup_gap(("box", RULE_H), ("pop", hf), GAP)),
    ])
    a = z.ctxt("hero", "SOON MOST OF IT", top_for_cap("pop", y_a, hf), hf, aw)
    # LAW 18: b1's defect, second sighting — the rule took IS A CONVERSATION's
    # width while sitting under SOON MOST OF IT, overhanging by 274px at 4K.
    u = z.underline("u", M, "hero", "SOON MOST OF IT", y_u, hf)
    b = z.ctxt("hero2", "IS A CONVERSATION", top_for_cap("pop", y_b, hf), hf, bw,
               color=TERRA, cue=s["talking"])
    z.t(settle(a, z.t0, 0.44),
        wipex(u, s["rule9"], 0.42),
        slam(b, s["talking"], 0.34, 1.22))
    d1 = round(AXIS - (y_a + cap_h("pop", hf) / 2.0), 1)
    d2 = round(AXIS - (y_a + (y_u + RULE_H)) / 2.0, 1)
    z.t(sety([a], d1), stepy([a], s["rule9"], d1, d2),
        sety([u], d2), stepy([a, u], s["talking"], d2, 0.0))
    z.shifted("hero alone", d1, ["hero"])
    z.shifted("+ rule", d2, ["hero", "u"])
    return z


def outro(C, M):
    """33.42-end dark — ONE deliberate centred composition (OUTRO ALIGNMENT)."""
    s, t0, t1 = C["s"], C["outro_t0"], C["dur"]
    z = Z("out", t0, t1, True, 11)
    hf, df, cf = 76.0, 56.0, 16.0
    dw = M.w("FOR DAILY AI", df)
    chh = cf * 1.34 + 16.0
    y_a, y_b, y_u, y_c = stack([
        (cap_h("pop", hf), 0.0),
        (cap_h("pop", df), lockup_gap(("pop", hf), ("pop", df), STEP)),
        (RULE_H, und_gap(df)),
        (chh, GAP),
    ])
    a = z.ctxt("w1", "FOLLOW", top_for_cap("pop", y_a, hf), hf, M.w("FOLLOW", hf))
    b = z.ctxt("w2", "FOR DAILY AI", top_for_cap("pop", y_b, df), df, dw, color=TERRA_L,
               cue=s["news"])
    # LAW 18: the right line already, now the right ruler (ink, not advance box).
    u = z.underline("u", M, "w2", "FOR DAILY AI", y_u, df)
    c = z.cchip("hc", "@migueltorrezai", y_c, cf, M.fx("handle"))
    z.t(settle(a, t0, 0.44),
        slam(b, s["news"], 0.32, 1.18),
        wipex(u, s["news"] + 0.52, 0.42),
        popo(c, s["day"], 0.34, 0.82))
    return z


# ---------------------------------------------------------------- build guards
def guard_ids(html):
    ids = re.findall(r'\sid="([^"]+)"', html)
    dup = [k for k, v in Counter(ids).items() if v > 1]
    if dup:
        sys.exit(f"DUPLICATE DOM IDS: {dup}")
    return set(ids)


def guard_tweens(html, ids, zones):
    sels = set()
    for raw in re.findall(r'tl\.(?:to|fromTo|set)\("([^"]+)"', html):
        for part in raw.split(","):
            part = part.strip()
            if part.startswith("#"):
                sels.add(part[1:])
    missing = sorted(s for s in sels if s not in ids)
    if missing:
        sys.exit(f"TWEEN SELECTORS WITH NO ELEMENT: {missing}")
    untweened = []
    for z in zones:
        for el in z.h:
            m = re.search(r'\sid="([^"]+)"', el)
            if m and m.group(1) not in sels:
                untweened.append(m.group(1))
    if untweened:
        sys.exit(f"SECTION CHILDREN WITH NO TWEEN: {untweened}")
    return len(ids), len(sels)


def guard_shifts(html, zones):
    """Every atom inside a step group must enter on scale, opacity or x."""
    shifted = set()
    for z in zones:
        for _, _, names in z.shifts:
            shifted |= {z.eid(n) for n in names if not n.startswith("[moved]")}
    bad = []
    for sel, frm in re.findall(r'tl\.fromTo\("([^"]+)",\{([^}]*)\}', html):
        parts = [p.strip() for p in sel.split(",")]
        if len(parts) > 1:
            continue
        if ("opacity:0" in frm and re.search(r"(?:^|,)\s*y:", frm)
                and parts[0][1:] in shifted):
            bad.append(parts[0])
    if bad:
        sys.exit(f"Y-ENTRANCE INSIDE A STEP GROUP (cancels the parked offset): {bad}")


def guard_tweens_per_property(html):
    """One element, ONE tween per property (langchain)."""
    scale_owner = Counter()
    for sel, rest in re.findall(r'tl\.(?:to|fromTo)\("([^"]+)",(.+?)\);', html):
        if "scale:" not in rest or "scaleX:" in rest.replace("scale:", ""):
            continue
        for part in sel.split(","):
            part = part.strip()
            if part.startswith("#"):
                scale_owner[part] += 1
    return {k: v for k, v in scale_owner.items() if v > 1}


def guard_echo(zones, words):
    """Law 4 — no top-zone text transcribing the spoken line. Bar: 3 consecutive
    spoken words verbatim.  Two attribute-declared exemptions: `data-source-quote`
    (the REAL tweet quotes the POST) and `data-name` (the KEY TERM's display
    lines, which law 9 requires on screen)."""
    toks = norm(" ".join(w["text"] for w in words))
    tri = {" ".join(toks[i:i + 3]) for i in range(len(toks) - 2)}
    hits, names = [], []
    for z in zones:
        for el in z.h:
            if "data-source-quote" in el:
                continue
            body = re.sub(r"<[^>]+>", " ", el).strip()
            if "data-name" in el:
                names.append(ihtml.unescape(body))
                continue
            zt = norm(body)
            for i in range(len(zt) - 2):
                g = " ".join(zt[i:i + 3])
                if g in tri:
                    hits.append((z.sid, g))
    if hits:
        sys.exit(f"CAPTION ECHO (3 consecutive spoken words on screen): {hits}")
    bad = [n for n in names if n not in NAME_LINES]
    if bad:
        sys.exit(f"LAW 4: `data-name` on strings that are not declared proper nouns: {bad}")
    if sorted(names) != sorted(NAME_LINES):
        sys.exit(f"LAW 4: declared key-term lines not all rendered: "
                 f"got {sorted(names)} want {sorted(NAME_LINES)}")
    if " ".join(names[:2]) != KEY_TERM:
        sys.exit(f"LAW 9: the key term's display lines do not recompose to {KEY_TERM!r}: "
                 f"{names[:2]}")
    return len(names)


def guard_caption_identity(zones, phrases):
    """Law 4, the half no trigram guard can see (langchain -> slowfrontier)."""
    hits = []
    for c in phrases:
        ct = set(norm(c["text"]))
        if not ct:
            continue
        for z in zones:
            for name, text, cue, end in z.texts:
                if cue >= c["t1"] or end <= c["t0"]:
                    continue
                st = set(norm(text))
                if st and st == ct:
                    hits.append((round(c["t0"], 2), c["text"], f"{z.sid}/{name}", text))
    if hits:
        sys.exit("LAW 4: caption pill is token-identical to an on-screen atom "
                 f"(captions x2): {hits}")
    return len(phrases)


def guard_provenance(html, zones, src, card):
    """Laws 3 + 14, as a build failure rather than a promise (erdos -> stolenapp).

    (a) the handed URL is a QUOTE, so the shipped card must be the QUOTED post's:
        the rendered card's text must be a byte-identical PREFIX of the news
        post's fetched text, and must NOT be the quoting post's text;
    (b) the card must be attributed to the NEWS author;
    (c) the highlighted claim must be a prefix of that same fetched text;
    (d) no engagement metric word may be RENDERED IN THE VISUAL ZONE (captions are
        verbatim speech and are exempt by law 4's own logic, so the check is
        scoped to the section markup).
    """
    quoted = next((t for t in src.get("referenced_tweets", [])
                   if t.get("id") == NEWS_POST_ID), None)
    if not quoted:
        sys.exit(f"PROVENANCE: the fetched post does not reference the news post {NEWS_POST_ID}")
    if (src.get("referenced_tweets_raw") or [{}])[0].get("type") != "quoted":
        sys.exit("PROVENANCE: referenced_tweets_raw is not a QUOTE relationship")
    if not quoted["text"].startswith(card["card_text"]):
        sys.exit("PROVENANCE: the shipped card text is not a prefix of the QUOTED (news) post")
    if card["card_text"] in src["text"]:
        sys.exit("PROVENANCE: the card is carrying the QUOTING post, not the news")
    if card["author"]["username"] != quoted["author"]["username"]:
        sys.exit(f"PROVENANCE: card attributed to {card['author']['username']!r}, "
                 f"not to the news author {quoted['author']['username']!r}")
    if not quoted["text"].startswith(card["claim"]):
        sys.exit("PROVENANCE: the highlighted claim is not a prefix of the news post")
    if card.get("metrics_rendered") or card.get("badge_rendered"):
        sys.exit("LAW 3: the card renders metrics or an unearned badge")
    if f'src="{CARD_PNG.name}"' in html:
        sys.exit("the card is referenced by bare filename rather than its staged path")
    zone_markup = "\n".join(el for z in zones for el in z.h)
    visible = norm(re.sub(r"<[^>]+>", " ", zone_markup))
    bad = sorted({w for w in visible if w in METRIC_WORDS})
    if bad:
        sys.exit(f"LAW 3: engagement-metric words in the visual zone: {bad}")
    return card["card_text"]


def guard_no_scaling_stroke(html):
    if "non-scaling-stroke" in html:
        sys.exit("BANNED: vector-effect=non-scaling-stroke in a zoomed factory project")


def guard_underlines(html, zones):
    """LAW 18 — every rule that sits under a phrase spans that phrase, no wider.

    Two assertions, neither of them arithmetic re-derivation:

    1. NO HAND-SET RULES.  Every `.strike` element in the page must have been
       built by `Z.underline()`, which can only get its width from a measured
       string.  A `z.strike(...)` with a literal or a lockup width never reaches
       the render.
    2. THE RULE UNDERLINES WHAT IT CLAIMS.  Each rule declares its target atom;
       this finds the atom whose ink bottom is nearest above the rule and asserts
       it IS that target.  That is exactly the defect Miguel caught: b1 and b9
       measured the line BELOW the rule, so the rule overhung the words above it
       by 303 and 274 physical px at 4K.

    Dividers stay legal — but a divider that sits directly under a phrase would
    fail (1), which is the point: it would read as an underline.
    """
    drawn = set(re.findall(r'class="abs strike[^"]*" id="([^"]+)"', html))
    declared, checked = set(), []
    for z in zones:
        for name, target, text, left, w in z.unders:
            declared.add(z.eid(name))
            # "directly above" is read off ink TOPS, not bottoms: these lines are
            # all-caps, so a rule set one cap-gap under the cap bottom still sits
            # inside the font's descender band and no atom's ink bottom clears it.
            rule_top = next(b[3] for b in z.boxes if b[0] == name)
            above = [b for b in z.boxes if b[0] != name and b[3] < rule_top]
            if not above:
                sys.exit(f"LAW 18: {z.eid(name)} underlines nothing")
            nearest = max(above, key=lambda b: b[3])
            if nearest[0] != target:
                sys.exit(f"LAW 18: {z.eid(name)} claims to underline '{target}' but the "
                         f"atom above it is '{nearest[0]}'")
            # Sized and seated on the line above.  Bounded against that line's
            # ADVANCE box with a 1-unit slack rather than against its ink, because
            # the ink legitimately overshoots the advance box by a fraction of a
            # unit at the right end (letter-spacing is negative), and because a
            # check against the ink would only restate the arithmetic that set the
            # width.  The slack is 1 design unit; the defect it exists to catch
            # measured 79 and 72.
            adv_w = nearest[2] - nearest[1]
            if w > adv_w + 1.0:
                sys.exit(f"LAW 18: {z.eid(name)} is {w:.1f} wide over a {adv_w:.1f} "
                         f"'{target}' — a rule wider than the words above it")
            off = (left + w / 2.0) - (nearest[1] + adv_w / 2.0)
            if abs(off) > 3.0:
                sys.exit(f"LAW 18: {z.eid(name)} sits {off:+.1f} off the centre of "
                         f"'{target}' — an underline rides its own words")
            checked.append((z.eid(name), text, w))
    stray = sorted(drawn - declared)
    if stray:
        sys.exit(f"LAW 18: rule(s) built outside Z.underline(), width unverifiable: {stray}")
    return checked


def guard_scene_slots(zones):
    """LAW 16 — every drawn slot activates.  Each of the six column slots has an
    entrance in b5, and each of the six token slots has one in b6."""
    by_id = {z.sid: z for z in zones}
    b5, b6 = by_id["b5"], by_id["b6"]
    tw5 = " ".join(b5.tw)
    for i in range(COL_N):
        if f"#{b5.eid(f'c{i}')}" not in tw5:
            sys.exit(f"LAW 16: column slot {i} is drawn but never activates in b5")
    tw6 = " ".join(b6.tw)
    for i in range(COL_N):
        if f'tl.fromTo("#{b6.eid(f"t{i}")}"' not in tw6:
            sys.exit(f"LAW 16: token slot {i} is drawn but never fills in b6")
    return COL_N


# ---------------------------------------------------------------- page
def build_html(C, M, is_4k):
    dur = C["dur"]
    zones = [sec1(C, M), sec2(C, M), sec3(C, M), sec4(C, M), sec5(C, M),
             sec6(C, M), sec7(C, M), sec8(C, M), sec9(C, M), outro(C, M)]
    n_names = guard_echo(zones, C["words"])
    guard_caption_identity(zones, C["phrases"])
    guard_scene_slots(zones)
    tws = []
    for z in zones:
        tws += z.tw
    sections = [z.section(0.0 if z.sid == "out" else OVERLAP) for z in zones]

    face = (f'  <video id="facebot" src="assets/v/face_bottom_4k.mp4" data-start="0" '
            f'data-duration="{dur:.2f}" data-media-start="0" data-track-index="1" muted '
            f'playsinline style="position:absolute;top:{px(SEAM)}px;left:0;width:1080px;'
            f'height:{px(FACE_H)}px;object-fit:cover"></video>')
    cuts = [z.t0 for z in zones[1:-1]]
    audio, atw = audio_block(dur, cuts, C["outro_t0"], C["bed_len"])
    tws += atw
    dims = ('data-width="2160" data-height="3840"' if is_4k
            else 'data-width="1080" data-height="1920"')

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=1080, height=1920"/>
<title>mathvoice — Kinetic type (run 6{", 4K" if is_4k else ""})</title>
{GSAP}
{FONTS}
<style>
{base_css(is_4k)}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" {dims}
     data-duration="{dur:.2f}" data-fps="{FPS}">

{face}

{chr(10).join(sections)}

{caption_clips(C["phrases"], dur)}

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
    ids = guard_ids(html)
    n_ids, n_sels = guard_tweens(html, ids, zones)
    guard_shifts(html, zones)
    guard_no_scaling_stroke(html)
    guard_provenance(html, zones, C["src"], C["card"])
    rules = guard_underlines(html, zones)
    doubled = guard_tweens_per_property(html)
    if doubled:
        sys.exit(f"TWO SCALE TWEENS ON ONE ELEMENT (langchain's grow-then-shrink): "
                 f"{sorted(doubled)}")
    return html, zones, n_ids, n_sels, n_names, rules


# ---------------------------------------------------------------- timing
CTA_ANCHOR = "follow for more ai"
SUBS = {
    "voice1": "voice this mathematician",
    "solve": "solve an open",
    # TIMING TOKEN, not display copy: this is matched against the transcript's
    # own tokens, so it keeps Scribe's "terturian".  The caption GLYPHS are
    # respelled to "Turturean" by CAPTION_SPELLING above; touching this string
    # would move the b2 section cut.
    "david": "david terturian solved",
    "solved": "solved one of",
    "extremely": "extremely complex mathematical",
    "rule3": "complex mathematical",
    "untilnow": "mathematical problems using",
    "using2": "using the new",
    "gpt1": "chatgpt chatgpt voice",
    "gpt2": "voice this means",
    "thismeans": "this means that the",
    "frontier": "frontier to getting",
    "getting": "getting the work",
    "work": "work done has",
    "done": "done has actually",
    "hasdrop": "has actually dropped",
    "dropped": "dropped again significantly",
    "flat": "significantly for each",
    "tok0": "for each and",
    "tok1": "each and every single one",
    "tok2": "and every single one",
    "tok3": "every single one of",
    "tok4": "single one of us",
    "hero6": "one of us if",
    "iff": "if a mathematician",
    "falls": "solve a very",
    "cansolve": "can solve a",
    "way": "this way that",
    "rest": "means that most",
    "most": "most busy work",
    "biz": "businesses and our",
    "daily": "daily life is",
    "veryclose": "very close to",
    "rule9": "solvable by literally",
    "talking": "talking with a",
    "now": "now follow for",
    "news": "news and videos",
    "day": "day catch you",
}

# Section cuts are asserted against the cues they claim to sit on.
SECTION_CUES = {"b2": "david", "b3": "extremely", "b4": "using2", "b5": "frontier",
                "b6": "dropped", "b7": "cansolve", "b8": "most", "b9": "veryclose"}


def timings():
    words = [w for w in json.loads((CUT / "transcript_tight.json").read_text())["words"]
             if w["type"] == "word"]
    dur = round(min(words[-1]["end"] + 0.6, probe(CUT / "face_bottom_4k.mp4"),
                    probe(CUT / "audio.m4a")), 2)

    toks, tstart = [], []
    for w in words:
        for tk in norm(w["text"]):
            toks.append(tk)
            tstart.append(w["start"])

    def find(phrase):
        q = norm(phrase)
        n = len(q)
        hits = [i for i in range(len(toks) - n + 1) if toks[i:i + n] == q]
        if not hits:
            raise SystemExit(f"anchor not found: {phrase!r}")
        if len(hits) > 1:
            raise SystemExit(f"anchor is AMBIGUOUS ({len(hits)} hits): {phrase!r}")
        return round(tstart[hits[0]], 2)

    sub = {k: find(v) for k, v in SUBS.items()}
    cta = find(CTA_ANCHOR)
    assert cta < dur
    return words, cta, dur, sub


# ---------------------------------------------------------------- staging
def link(target: Path, dest: Path):
    if dest.is_symlink() or dest.exists():
        dest.unlink()
    dest.symlink_to(target.resolve())


def stage():
    host = STAGE / NAME
    for d in ["img", "music", "sfx", "v", "logos"]:
        (host / d).mkdir(parents=True, exist_ok=True)
    # THE BED IS bed_split_v2 (2026-08-10): the original has a vocal intro Miguel
    # rejected. It is staged under the historical filename the markup expects.
    shutil.copy2(FACTORY / "assets/music/bed_split_v2.mp3", host / "music/bed_split.mp3")
    for s in ["pop", "whoosh", "boom"]:
        shutil.copy2(PUB / f"{s}.mp3", host / "sfx" / f"{s}.mp3")
    shutil.copy2(MARK_CHATGPT, host / "logos/chatgpt-color.png")
    shutil.copy2(CARD_PNG, host / "img" / CARD_PNG.name)
    for f in ["face_bottom_4k.mp4", "audio.m4a"]:
        link(CUT / f, host / "v" / f)

    from PIL import Image
    marks = {"chatgpt": "assets/logos/chatgpt-color.png",
             "card": f"assets/img/{CARD_PNG.name}"}
    with Image.open(MARK_CHATGPT) as im:
        marks["chatgpt_px"] = im.size[0]
    with Image.open(CARD_PNG) as im:
        marks["card_px"] = im.size[0]
        marks["card_h"] = round(CARD_W * im.size[1] / im.size[0], 2)
    return marks, host


def assert_no_upscale(media, is_4k):
    """Law 8 — no raster may be rendered above its intrinsic width.  The physical
    width includes the design scale AND the 4K root zoom (agentreviews)."""
    z = 2 if is_4k else 1
    out = {}
    for key, design_w in [("chatgpt", MARK), ("card", CARD_W)]:
        src_w = media[f"{key}_px"]
        physical = design_w * S * z
        ratio = physical / src_w
        assert ratio <= 1.0, (
            f"LAW 8: {key} upscaled {ratio:.3f}x ({physical:.1f}px from {src_w}px)")
        out[key] = {"ratio": round(ratio, 4), "physical_px": round(physical, 1),
                    "intrinsic_px": src_w}
    return out


# ---------------------------------------------------------------- main
if __name__ == "__main__":
    GEN.mkdir(parents=True, exist_ok=True)
    src = json.loads(SOURCE_JSON.read_text())
    card = json.loads(CARD_JSON.read_text())
    media, host = stage()
    words, cta, dur, sub = timings()
    M = Mx(measure())
    C = {"media": media, "dur": dur, "s": sub, "words": words,
         "src": src, "card": card,
         "card_rects": card["claim_line_rect_fractions"],
         "tokcues": [sub[f"tok{i}"] for i in range(COL_N - 1)],
         "outro_t0": sub["now"], "cta": cta,
         "bed_len": probe(FACTORY / "assets/music/bed_split_v2.mp3"),
         "phrases": build_captions(words)}

    ratios = None
    for root, is_4k in [(PROJECTS, False), (PROJECTS_4K, True)]:
        proj = root / NAME
        proj.mkdir(parents=True, exist_ok=True)
        link(host, proj / "assets")
        html, zones, n_ids, n_sels, n_names, rules = build_html(C, M, is_4k)
        (proj / "index.html").write_text(html, encoding="utf-8")
        if is_4k:
            ratios = assert_no_upscale(media, True)

    by_id = {z.sid: z for z in zones}
    for sid, cue in SECTION_CUES.items():
        assert abs(by_id[sid].t0 - sub[cue]) < 0.005, \
            f"section {sid} cuts at {by_id[sid].t0} but its cue {cue} is {sub[cue]}"
    assert abs(by_id["out"].t0 - sub["now"]) < 0.005

    print(f"dur={dur:.2f} outro={sub['now']:.2f} cta={cta:.2f} caps={len(C['phrases'])} "
          f"ids={n_ids} tweens={n_sels} names={n_names} bed={C['bed_len']:.2f}s")
    print(f"card {CARD_W:.0f}x{media['card_h']:.1f} design units "
          f"({media['card_px']}px source), tweet on screen "
          f"{by_id['b2'].t1 - by_id['b2'].t0:.3f}s authored")
    print(f"scene: {COL_N} columns pitch {COL_PITCH:.0f} span {col_x(0):.0f}.."
          f"{col_x(COL_N - 1) + COL_W:.0f} centre {(col_x(0) + col_x(COL_N - 1) + COL_W) / 2:.1f} "
          f"base {BASE:.1f} heights {[col_h(i) for i in range(COL_N)]}")
    for k, v in ratios.items():
        print(f"law8 {k:9s} {v['physical_px']}px from {v['intrinsic_px']}px = {v['ratio']}x")
    for eid, text, w in rules:
        print(f"law18 {eid:7s} rule {w * S * 2:7.1f}px @4K = ink of '{text}'")
    for z in zones:
        lo = min(b[3] for b in z.boxes)
        hi = max(b[4] for b in z.boxes)
        print(f"  {z.sid:4s} {z.t0:6.2f}-{z.t1:6.2f} {'dark ' if z.dark else 'cream'} "
              f"atoms={len(z.h):2d} ink y {lo:6.1f}..{hi:6.1f}")
        for label, dy, names in z.shifts:
            if names and names[0].startswith("[moved]"):
                print(f"       state {label:34s} {names[0][8:]}")
            else:
                print(f"       step  {label:34s} +{dy:6.1f} -> 0  ({', '.join(names)})")
    print(f"BUILD DONE -> {PROJECTS_4K / NAME / 'index.html'}")
