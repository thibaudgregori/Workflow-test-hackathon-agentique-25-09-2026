"""THE CANONICAL CAPTION MODULE — one pill spec, one size, one handle policy.

Promoted out of the format lab's round-6 closing captions round (approved by
Miguel 2026-09-01).  Every format chassis under `formats/` imports its caption
canon from HERE and never re-types a number.  The lab copies stay on disk as the
historical record; this file is the law they all now read.

-------------------------------------------------------------------------------
1. WHERE THE NUMBERS COME FROM
-------------------------------------------------------------------------------
The pill is not a new design.  It is the pill the PUBLISHED factory has been
shipping: 97.1% of 7,614 published caption pills are this exact object.

`pipeline/build_hyperframes_r2.py` authors the split format in a 576-wide design
space and scales by S = 1.875 into the native 1080x1920 canvas:

    .scap     { left:0; width:1080px; text-align:center; }
    .scappill { display:inline-block; transform:translateY(-50%);
                background:#C4573A; color:#fff; font-family:Nunito,sans-serif;
                font-weight:800; font-size:px(30)px; padding:px(10)px px(18)px;
                border-radius:px(12)px; white-space:nowrap; }

Read back off a published video (`references/builds/mcpupgrade_icon/projects/mcpupgrade_icon/`):

    font-size 56.2px   padding 18.8px 33.8px   border-radius 22.5px
    background #C4573A   color #fff   Nunito 800   nowrap   NO shadow

so "30px" and "56.2px" are the same size stated in the two design spaces.  A
format that authors natively in 1080 (every format-lab format does) writes 56.2.

-------------------------------------------------------------------------------
2. ONE SIZE.  THE SHRINK FORMULA IS DEAD.
-------------------------------------------------------------------------------
The published `cap_font()` returned `min(30, budget / (EM * len(text)))`, which
is why round 4 shipped EIGHT font sizes inside one video.  Round 6 keeps ONE
size and makes it canonical.  A phrase too wide for its seat is **SPLIT at a
word boundary** into more caption beats — the word timestamps in
`transcript_words.json` carry the split for free — and never squeezed, never
widened, never re-sized.

-------------------------------------------------------------------------------
3. MEASURED, NEVER ESTIMATED
-------------------------------------------------------------------------------
Every generator in the lab once carried `len(text) * 0.575 * font + padding`.
Measured against the 58 rendered pills of `takeover_fix5.mp4` that estimate runs
0.71-1.00 of the truth (mean 0.86): it is a BOUND, not a measurement, so it
cannot answer "did this pill actually fit".  At the canonical 56.2px it is wrong
in the direction that breaks builds — it calls "procedural disclosure." a
778.6px pill where Chromium paints 670.4px, demanding a Law-4-illegal split.

`PillMeasurer` lays the real `.scappill` box out in headless Chromium with the
real Nunito 800 webfont at the real size — the same engine HyperFrames renders
with.  Validation across all 58 pills of takeover fix5, predicted vs the TERRA
span decoded out of the finished MP4: delta -2.6 .. +1.3 px, mean -0.7 px.  The
model IS the renderer.

Two traps this module refuses to fall into, both learned the hard way:
  * a canvas `measureText` shortcut silently falls back to a system face without
    an explicit `document.fonts.load` and under-reports by ~70px — so the font
    load is PROVEN with `document.fonts.check` before a single number is kept;
  * past ~250,000px down the page Chromium's LayoutUnit grid coarsens enough
    that the SAME box reads 114.56 / 114.59 / 114.61 — three pill heights where
    there is only one — so spans are laid out in batches at integer positions.

-------------------------------------------------------------------------------
3b. NO BEAT IS A BARE FUNCTION WORD.  THE "in" / LINKEDIN DEFECT (run 9)
-------------------------------------------------------------------------------
`perplexityprojects_split` and `_cutout` shipped a caption beat whose whole text
was the single word **"in"** (from "store them *in* dedicated folders"), alive
22.36-22.52 s.  The pill is `white-space:nowrap` with fixed padding, so a
two-letter beat collapses the 264px pill into a **42px rounded square carrying a
bold lowercase "in" in white on a solid colour** — which is, stroke for stroke,
the LinkedIn badge.  The independent viewer test read it exactly that way and
held both renders: *"a stranger reads LinkedIn in a Perplexity video."*

ROOT CAUSE, stated precisely: **there is no brand-substitution code anywhere in
this factory.**  Nothing swapped a logo in.  The caption CHUNKER emitted a beat
containing only a function word, and the canonical pill's own geometry turned it
into a brand mark.  A defect of chunking, not of assets.

THE LAW, from run 9 on:
  * **A caption beat is never composed only of function words.**  Prepositions,
    articles, conjunctions, auxiliaries, pronouns and particles do not stand
    alone in a pill.  `merge_function_only_beats()` folds such a beat into a
    neighbour (forward first — a preposition binds to what follows it), and
    `assert_no_function_only_beat()` fails the build if one survives.
  * **A pill that renders SQUARE is refused**, whatever it says.  Measured in the
    render browser against the one canonical pill height of 114.59px: "in" is
    116.1px wide, an aspect of 1.01.  `PILL_MIN_ASPECT` = 1.45 sits in the
    measured gap between "you" (1.42) and "day." (1.53), so the boundary is read
    off the evidence rather than chosen.  The collapse to a badge is a SHAPE
    problem before it is a grammar problem.
  * **If a brand mark is ever substituted for a caption token**, `brand_token_ok()`
    is the gate: the token must be an EXACT registered brand name, at least 3
    characters, and must not appear in `FUNCTION_WORDS`.  "in", "it", "meta",
    "notion" as a common noun — all refused.  Today nothing calls it; it exists so
    that the next person who reaches for the idea inherits the rule instead of
    the defect.

Tested in `pipeline/test_captions_function_words.py` on the three canonical
strings: "store them in dedicated folders", "log in to Notion", "LinkedIn is
down".

-------------------------------------------------------------------------------
4. THE HANDLE IS A PARAMETER (Miguel, 2026-09-01)
-------------------------------------------------------------------------------
The outro chip is a parametrized constant.  The YouTube master renders
`@migueltorrezai`; the TikTok/Instagram variant renders `@migueltorrez.ai`.  One
parameter, deterministic re-render, ONLY the outro differs.  Default is YouTube.

-------------------------------------------------------------------------------
USAGE
-------------------------------------------------------------------------------
    import sys; sys.path.insert(0, str(FACTORY / "pipeline"))
    import captions as CAP

    CAP.CAP_FONT                     # 56.2 — THE ONLY SIZE
    CAP.pill_css()                   # the inline style string
    CAP.pill_rule()                  # the full `.scap` + `.scappill` stylesheet

    m = CAP.PillMeasurer(HOME / "_pillwidths.json")
    m.want(CAP.runs(tokens)); m.resolve()
    beats = CAP.split_to_fit(words, CAP.SEAT_MAX_W, m)

    CAP.handle()                     # "@migueltorrezai"   (default: YouTube)
    CAP.handle("tiktok_ig")          # "@migueltorrez.ai"
    CAP.add_handle_arg(parser)       # --handle {yt,tiktok_ig} on any chassis CLI
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

# =============================================================================
# 1. THE CANON.  Native 1080x1920 design space.  DO NOT parameterise these.
# =============================================================================
DESIGN_WIDTH = 576.0             # the published project's authoring space
NATIVE_WIDTH = 1080.0            # the canvas everything is delivered in
S = NATIVE_WIDTH / DESIGN_WIDTH  # 1.875 — the published scale

CAP_FONT = 56.2                  # px(30du) — THE ONLY SIZE.  Never derived.
CAP_FS = CAP_FONT                # alias: some chassis spell it CAP_FS
CAP_PAD_Y = 18.8                 # px(10du)   vertical padding
CAP_PAD_X = 33.8                 # px(18du)   horizontal padding
CAP_RADIUS = 22.5                # px(12du)   corner radius
CAP_BG = "#C4573A"               # TERRA
CAP_FG = "#fff"
CAP_FAMILY = "Nunito,sans-serif"
CAP_WEIGHT = 800
CAP_SHADOW = ""                  # explicitly none.  The published pill has none.

# MEASURED in the render browser (Chromium, Nunito 800, line-height `normal`),
# not modelled: 78.99px content box + 2 x 18.80 padding.  It is a CONSTANT — it
# does not vary with the phrase, only the width does.  Seats are derived from it.
CAP_PILL_HEIGHT = 114.59
CAP_H = CAP_PILL_HEIGHT          # alias
CAP_LINE_BOX_EM = 1.3699         # Nunito 800 line box, measured not modelled

# Frame + platform geometry the seats are cut against (GLOBAL LAW 12, round 3,
# as amended round 4: the COMPOSITION stays centred; only CAPTIONS and critical
# readable annotations avoid the right 15% column).
FRAME_W, FRAME_H = 1080.0, 1920.0
LAW12_BOTTOM = 0.72 * FRAME_H    # 1382.4 — the pill's BOTTOM edge may not pass
LAW12_RAIL_X = 918.0             # right 15% column: no caption ink beyond this
LAW12_TOP = 0.10 * FRAME_H       # 192 — top 10%, no meaningful content
SEAT_MAX_W = 2 * (LAW12_RAIL_X - FRAME_W / 2)   # 756.0 — widest legal pill
SEAT_INK_MAX = SEAT_MAX_W - 2 * CAP_PAD_X       # 688.4 — the ink budget

CANON = {
    "font_px": CAP_FONT, "pad_y": CAP_PAD_Y, "pad_x": CAP_PAD_X,
    "radius": CAP_RADIUS, "bg": CAP_BG, "fg": CAP_FG,
    "family": CAP_FAMILY, "weight": CAP_WEIGHT,
    "pill_height_px": CAP_PILL_HEIGHT, "line_box_em": CAP_LINE_BOX_EM,
    "shadow": "none", "sizes": "ONE — long phrases split, never shrunk",
}

FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@800'
    '&display=block" rel="stylesheet">'
)


def px(du: float) -> float:
    """Design units (576-wide space) -> native px.  px(30) == 56.25 ~ CAP_FONT."""
    return du * S


# =============================================================================
# 2. THE PILL, EMITTED
# =============================================================================
def pill_css(translate_y: bool = True) -> str:
    """The one and only pill declaration, as an inline `style` string.

    `translate_y` keeps the published `transform:translateY(-50%)` so a seat is
    stated as the pill's CENTRE.  Formats that seat by the top edge pass False.
    """
    tf = "transform:translateY(-50%);" if translate_y else ""
    return (f"display:inline-block;{tf}"
            f"background:{CAP_BG};color:{CAP_FG};font-family:{CAP_FAMILY};"
            f"font-weight:{CAP_WEIGHT};font-size:{CAP_FONT}px;"
            f"padding:{CAP_PAD_Y}px {CAP_PAD_X}px;"
            f"border-radius:{CAP_RADIUS}px;white-space:nowrap;")


def pill_rule(scap: str = ".scap", scappill: str = ".scappill",
              translate_y: bool = True) -> str:
    """The full stylesheet fragment: the centring row + the pill itself."""
    return (f"{scap} {{ position:absolute; left:0; width:{FRAME_W:.0f}px; "
            f"text-align:center; }}\n"
            f"{scappill} {{ {pill_css(translate_y)} }}")


def pill_height() -> float:
    """The canonical rendered pill height.  Seats derive from this, not guesses."""
    return CAP_PILL_HEIGHT


def seat_bounds(centre_y: float) -> tuple[float, float]:
    """(top, bottom) of a pill seated by its CENTRE at `centre_y`."""
    return (round(centre_y - CAP_PILL_HEIGHT / 2, 2),
            round(centre_y + CAP_PILL_HEIGHT / 2, 2))


def assert_law12(centre_y: float, widest_px: float | None = None) -> None:
    """Fail the build, loudly, when a seat or a pill breaks GLOBAL LAW 12."""
    top, bottom = seat_bounds(centre_y)
    if bottom > LAW12_BOTTOM:
        raise SystemExit(
            f"LAW 12: caption pill bottom {bottom:.1f}px "
            f"({bottom / FRAME_H:.1%}) is past the {LAW12_BOTTOM:.1f}px line")
    if top < LAW12_TOP:
        raise SystemExit(f"LAW 12: caption pill top {top:.1f}px is in the top 10%")
    if widest_px is not None:
        right = FRAME_W / 2 + widest_px / 2
        if right > LAW12_RAIL_X + 0.6:
            raise SystemExit(
                f"LAW 12: widest caption pill reaches x={right:.0f}, "
                f"{right - LAW12_RAIL_X:.0f}px into the right rail")


# =============================================================================
# 3. THE HANDLE — a parameter, not a constant (Miguel, 2026-09-01)
# =============================================================================
HANDLE_YT = "@migueltorrezai"          # the YouTube master
HANDLE_TIKTOK_IG = "@migueltorrez.ai"  # the TikTok / Instagram variant

HANDLES = {
    "yt": HANDLE_YT, "youtube": HANDLE_YT, "shorts": HANDLE_YT,
    "tiktok_ig": HANDLE_TIKTOK_IG, "tiktok": HANDLE_TIKTOK_IG,
    "ig": HANDLE_TIKTOK_IG, "instagram": HANDLE_TIKTOK_IG,
    "reels": HANDLE_TIKTOK_IG,
}
HANDLE_KEYS = ("yt", "tiktok_ig")      # the two the chassis CLIs expose
DEFAULT_HANDLE = "yt"


def handle(key: str | None = None) -> str:
    """Resolve a platform key to its @handle.  Default = the YouTube master.

    ONLY the outro differs between the two renders.  Nothing else in a video is
    allowed to branch on this parameter.
    """
    k = (key or DEFAULT_HANDLE).strip().lower()
    if k in HANDLES:
        return HANDLES[k]
    if k.startswith("@"):               # an explicit handle passes through
        return k
    raise SystemExit(f"unknown handle key {key!r} — one of {sorted(HANDLES)}")


def handle_slug(key: str | None = None) -> str:
    """`yt` / `tiktok_ig` — the stable suffix for a variant's output filename."""
    k = (key or DEFAULT_HANDLE).strip().lower()
    return "yt" if HANDLES.get(k, HANDLE_YT) == HANDLE_YT else "tiktok_ig"


def add_handle_arg(parser) -> None:
    """Give any chassis CLI the standard `--handle` flag."""
    parser.add_argument("--handle", default=DEFAULT_HANDLE, choices=HANDLE_KEYS,
                        help="outro @handle: yt=@migueltorrezai (default), "
                             "tiktok_ig=@migueltorrez.ai")


# --- the outro chip ----------------------------------------------------------
# Formats own their outro GEOMETRY (the ring, the rule, the tile row, the seat
# maths) because it is part of each format's picture.  What they share is the
# lockup: mono handle, terracotta rule above it, `daily AI` micro-line below.
# A chassis with a bespoke outro may use `handle()` alone and keep its own
# markup — it must never re-type the handle string.
OUTRO_MONO = "'JetBrains Mono',monospace"
OUTRO_DAILY = "daily AI"


def outro_chip_html(cy: float, key: str | None = None, *, elem_id: str = "o-handle",
                    size: float = 56.25, letter_spacing: float = 2.25,
                    color: str = "#141416", weight: int = 700,
                    width: float = FRAME_W, extra: str = "") -> str:
    """The standard centred @handle line, seated by its top edge at `cy`."""
    return (f'<div class="abs mono" id="{elem_id}" style="left:0;top:{cy}px;'
            f'width:{width:.0f}px;text-align:center;font-family:{OUTRO_MONO};'
            f'font-size:{size}px;line-height:{size * 1.36:.2f}px;'
            f'letter-spacing:{letter_spacing}px;font-weight:{weight};'
            f'color:{color};text-transform:none;{extra}">{handle(key)}</div>')


def outro_daily_html(cy: float, *, elem_id: str = "o-daily", size: float = 24.375,
                     letter_spacing: float = 8.25, color: str = CAP_BG,
                     weight: int = 500, width: float = FRAME_W,
                     extra: str = "") -> str:
    """The `daily AI` micro-line that sits under the handle in every outro."""
    return (f'<div class="abs mono" id="{elem_id}" style="left:0;top:{cy}px;'
            f'width:{width:.0f}px;text-align:center;font-family:{OUTRO_MONO};'
            f'font-size:{size}px;line-height:{size * 1.36:.2f}px;'
            f'letter-spacing:{letter_spacing}px;font-weight:{weight};'
            f'color:{color};text-transform:none;{extra}">{OUTRO_DAILY}</div>')


# =============================================================================
# 4. THE MEASURER — Chromium lays the real box out; nothing is estimated
# =============================================================================
_PAGE_HEAD = f"""<!doctype html><html><head><meta charset="utf-8">{FONT_LINK}
<style>* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ position:relative; width:4000px; }}
.scappill {{ {pill_css()} }}</style></head><body>"""

_READ = """() => Array.from(document.querySelectorAll('.scappill')).map(
  e => [e.dataset.i, e.getBoundingClientRect().width,
        e.getBoundingClientRect().height])"""

_BATCH = 250        # spans per layout pass — keeps every box above ~50,000px
_ROW = 200          # integer vertical pitch — sub-pixel flow offsets accumulate


class PillMeasurer:
    """Chromium-measured pill widths, cached on disk, deterministic offline.

        m = PillMeasurer(HOME / "_pillwidths.json")
        m.want(["some phrase", ...])   # queue
        m.resolve()                    # one headless batch, then cached
        m.width("some phrase")         # full pill width in px, padding included

    The cache is keyed by the exact string under a hash of the pill CSS, so a
    canon change invalidates it automatically instead of silently reusing widths
    measured against a different pill.
    """

    def __init__(self, cache: Path | str, css: str | None = None):
        self.cache = Path(cache)
        self.css = css or pill_css()
        self.css_key = hashlib.sha1(self.css.encode()).hexdigest()[:12]
        self.table: dict[str, float] = {}
        self.height: float | None = None
        self.measured_this_run = 0
        if self.cache.exists():
            blob = json.loads(self.cache.read_text())
            if blob.get("css_key") == self.css_key:
                self.table = {k: float(v) for k, v in blob["widths"].items()}
                self.height = blob.get("pill_height")
        self.pending: set[str] = set()

    # -- queue / resolve ---------------------------------------------------
    def want(self, texts) -> None:
        for t in texts:
            if t not in self.table:
                self.pending.add(t)

    def resolve(self) -> None:
        if not self.pending:
            return
        todo = sorted(self.pending)
        widths, height = _measure(todo, self.css)
        self.table.update(widths)
        self.height = height
        self.measured_this_run += len(todo)
        self.pending.clear()
        self._flush()

    def _flush(self) -> None:
        self.cache.parent.mkdir(parents=True, exist_ok=True)
        self.cache.write_text(json.dumps({
            "css_key": self.css_key, "css": self.css,
            "font_px": CAP_FONT, "pad": [CAP_PAD_Y, CAP_PAD_X],
            "radius": CAP_RADIUS, "pill_height": self.height,
            "widths": {k: round(v, 3) for k, v in sorted(self.table.items())},
        }, indent=1, ensure_ascii=False))

    # -- read --------------------------------------------------------------
    def width(self, text: str) -> float:
        if text not in self.table:
            self.want([text])
            self.resolve()
        return self.table[text]

    def fits(self, text: str, max_w: float) -> bool:
        return self.width(text) <= max_w

    def report(self) -> dict:
        return {"strings_measured": len(self.table),
                "measured_this_run": self.measured_this_run,
                "pill_height_px": self.height,
                "canonical_pill_height_px": CAP_PILL_HEIGHT,
                "widths_are": "measured in Chromium, not estimated",
                "estimator": "retired — the 0.575*len bound is dead"}


def _measure(texts: list[str], css: str) -> tuple[dict[str, float], float]:
    """One headless Chromium, batched integer-position layout, N strings.

    Raises rather than returns a fallback face's numbers, and raises rather than
    return more than one pill height: both failure modes silently shift seats.
    """
    import html as ihtml

    from playwright.sync_api import sync_playwright

    out: dict[str, float] = {}
    heights: set[float] = set()
    head = _PAGE_HEAD.replace(pill_css(), css) if css != pill_css() else _PAGE_HEAD
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": 1200, "height": 900})
        for b0 in range(0, len(texts), _BATCH):
            batch = texts[b0:b0 + _BATCH]
            spans = "".join(
                f'<span class="scappill" data-i="{i}" style="position:absolute;'
                f'left:0px;top:{i * _ROW}px">'
                f'{ihtml.escape(t, quote=False)}</span>'
                for i, t in enumerate(batch))
            pg.set_content(f"{head}{spans}</body></html>")
            pg.wait_for_function("document.fonts.ready.then(()=>true)", timeout=30000)
            pg.wait_for_timeout(120)
            if not pg.evaluate(
                    "() => { const e = document.querySelector('.scappill');"
                    " const s = getComputedStyle(e);"
                    " return document.fonts.check(s.fontWeight + ' '"
                    " + s.fontSize + ' Nunito'); }"):
                br.close()
                raise SystemExit(
                    "Nunito 800 did not load in the measuring browser — every "
                    "width would be a fallback face's.  Refusing to measure.")
            for i, w, h in pg.evaluate(_READ):
                out[batch[int(i)]] = round(float(w), 2)
                heights.add(round(float(h), 2))
        br.close()
    if len(heights) != 1:
        raise SystemExit(f"the canonical pill measured {sorted(heights)} px tall "
                         f"— there is exactly ONE pill height")
    h = heights.pop()
    if abs(h - CAP_PILL_HEIGHT) > 0.05:
        raise SystemExit(f"the pill renders {h}px tall, not the canonical "
                         f"{CAP_PILL_HEIGHT}px — seats derive from that height")
    return out, h


def runs(tokens: list[str]) -> list[str]:
    """Every contiguous word run of a phrase — the complete candidate set the
    splitter can ever ask about, so ONE browser batch covers a whole build."""
    return [" ".join(tokens[i:j])
            for i in range(len(tokens)) for j in range(i + 1, len(tokens) + 1)]


# =============================================================================
# 5. THE SPLITTER — the mechanism that replaces the dead shrink formula
# =============================================================================
def _join(ws) -> str:
    return " ".join(w["text"] if isinstance(w, dict) else str(w) for w in ws)


def split_to_fit(words: list, max_w: float, measurer: PillMeasurer,
                 join=_join) -> list[list]:
    """Greedy word-boundary split of one phrase into beats that each fit `max_w`
    as a RENDERED pill.  Never touches the type size.

    A single word wider than the seat cannot be split at a word boundary; it is
    returned as its own beat and the caller must FAIL THE BUILD rather than
    silently shrink it.
    """
    beats: list[list] = []
    cur: list = []
    for w in words:
        trial = cur + [w]
        if cur and measurer.width(join(trial)) > max_w:
            beats.append(cur)
            cur = [w]
        else:
            cur = trial
    if cur:
        beats.append(cur)
    return beats


def split_balanced(words: list, max_w: float, measurer: PillMeasurer,
                   forbidden: set[str] | None = None, join=_join) -> list[list]:
    """Split the WIDEST part repeatedly, choosing the most even word boundary —
    but LAW 4 outranks tidiness.

    Law 4: a caption never duplicates a string already painted on screen.
    `forbidden` holds the normalised on-screen strings; candidate boundaries are
    ranked by imbalance and the first one whose halves paint no on-screen string
    is taken (falling back to the most even split when every candidate collides).

    Used where a greedy left-to-right fill would strand a one-word tail — e.g.
    "called procedural disclosure." splits most evenly into "called procedural" +
    "disclosure.", and "disclosure." repeats the DISCLOSURE headline verbatim.
    """
    forbid = forbidden or set()
    parts: list[list] = [list(words)]
    while True:
        widest = max(parts, key=lambda r: measurer.width(join(r)))
        if measurer.width(join(widest)) <= max_w:
            break
        if len(widest) < 2:
            raise SystemExit(f"single word too wide for the caption band: "
                             f"{join(widest)!r} — the type size is NOT negotiable")
        order = sorted(range(1, len(widest)),
                       key=lambda k: abs(len(join(widest[:k])) - len(join(widest[k:]))))
        legal = [k for k in order
                 if all(join(half).lower() not in forbid
                        for half in (widest[:k], widest[k:]))]
        best = legal[0] if legal else order[0]
        at = parts.index(widest)
        parts[at:at + 1] = [widest[:best], widest[best:]]
    return parts


# =============================================================================
# 6. FUNCTION WORDS — no pill is ever a bare one (run 9, the "in"/LinkedIn defect)
# =============================================================================
# The list is deliberately CLOSED and English-only: it is a stopword list for a
# stopword problem, not a parts-of-speech tagger.  A word is in here only if it
# is a pure function word — it carries no argument on its own and a viewer
# reading it alone in a pill learns nothing.
# DELIBERATELY TIGHT.  A word earns a place here only when it carries no
# argument in ANY reading.  Directional and question words are OMITTED on
# purpose — "down" in "LinkedIn is down", "out" in "it rolled out", "how" in
# "how it works" are the whole point of their sentences, and merging them away
# would trade one defect for a worse one.
FUNCTION_WORDS = frozenset("""
a an the this that these those
i me my you your he him his she her it its we us our they them their
am is are was were be been being do does did have has had
can could shall should will would may might must
and or but nor so yet if because while
of to in on at for with from by into onto as than
not just also very too only even
""".split())

def _norm_token(tok: str) -> str:
    """Strip punctuation and case for stopword comparison.  Keeps letters and
    digits only, so "in," / "In" / "in." all normalise to "in"."""
    return "".join(ch for ch in tok.lower() if ch.isalnum())


def is_function_word(tok: str) -> bool:
    """True when this single token is a pure function word."""
    return _norm_token(tok) in FUNCTION_WORDS


def is_function_only(text: str) -> bool:
    """True when EVERY token of a beat is a function word.

    Reported, not refused, once a beat has two or more tokens: "you can" measures
    270.3px and reads as text.  The refusal below is the single-token case plus
    the measured shape test.
    """
    toks = [t for t in text.split() if _norm_token(t)]
    return bool(toks) and all(is_function_word(t) for t in toks)


# THE MEASURED SHAPE OF THE DEFECT.  Every candidate was laid out in the render
# browser at the canonical 56.2px / 33.8px padding, against the ONE canonical pill
# height of 114.59px:
#
#     "in"      116.1 px   aspect 1.01   <- the shipped defect: a SQUARE
#     "you"     163.1 px   aspect 1.42
#     "day."    174.8 px   aspect 1.53
#     "one."    179.6 px   aspect 1.57
#     "Now,"    202.7 px   aspect 1.77
#     "news"    206.9 px   aspect 1.81
#     "you can" 270.3 px   aspect 2.36
#
# (116.1px at 1080 wide is the clerk's measured "42px square" at 405x720 — the
# two numbers are the same object, which is how we know the model is the render.)
#
# The defect is not shortness.  It is SQUARENESS: a solid rounded square carrying
# two or three bold white glyphs is the universal shape of a brand badge, and a
# viewer reads it as one before reading it as a word.  So the law is stated on the
# pill's aspect ratio, where the evidence actually is, and 1.45 sits in the gap
# between "you" (1.42) and "day." (1.53) — the boundary is measured, not chosen.
#
# Note what this deliberately does NOT refuse: "day.", "one.", "Now," and "you
# can" are all narrow, and the published factory ships pills like them constantly.
# They read as text. Widening the law to cover them would trade one defect for a
# chunker that mangles every sentence ending.
PILL_MIN_ASPECT = 1.45
MIN_SOLO_CHARS = 4               # the fallback when no measured width is at hand


def is_badge_pill(width: float, height: float = CAP_PILL_HEIGHT) -> bool:
    """True when a rendered pill is square enough to read as a brand mark."""
    return width / height < PILL_MIN_ASPECT


def is_orphan_beat(text: str, width: float | None = None) -> bool:
    """A beat that must never reach the screen.

    Two independent refusals, either one sufficient:
      * ONE token that is a pure function word — it argues nothing on its own,
        whatever it measures ("in", "of", "you");
      * a pill that renders SQUARE (see `PILL_MIN_ASPECT`) — it reads as a badge,
        whatever it says.  With no measured width, a lone sub-4-character token
        stands in for the measurement.
    """
    toks = [t for t in text.split() if _norm_token(t)]
    if not toks:
        return False
    if len(toks) == 1 and is_function_word(toks[0]):
        return True
    if width is not None:
        return is_badge_pill(width)
    return len(toks) == 1 and len(_norm_token(toks[0])) < MIN_SOLO_CHARS


def brand_token_ok(token: str, registry) -> bool:
    """THE GATE for any future caption-token -> brand-mark substitution.

    Nothing in the factory substitutes brand marks into captions today.  When
    something does, it calls this and nothing else:

      * the token must resolve to an EXACT entry in `registry` (case-insensitive
        on the whole token, never a prefix, never a substring);
      * the token must be at least 3 characters after normalisation;
      * the token must NOT be a function word.

    "in" fails all three tests it is subject to.  "LinkedIn" passes.
    """
    t = _norm_token(token)
    if len(t) < 3 or t in FUNCTION_WORDS:
        return False
    return t in {_norm_token(k) for k in registry}


def merge_function_only_beats(beats: list, max_w: float, measurer,
                              join=_join) -> list:
    """Fold every orphan beat (see `is_orphan_beat`) into a neighbour.

    `beats` is a list of word-lists, as `split_to_fit` returns, and it should be
    the WHOLE video's beat stream — orphans are produced at phrase boundaries, so
    a merge applied inside one phrase at a time cannot see the neighbour it needs.

    Direction: FORWARD first — a preposition or an article binds to the words that
    follow it ("in dedicated folders") — falling back to backward when the forward
    merge would not fit the seat.  A beat neither neighbour can take is left
    alone, and `assert_no_function_only_beat` then fails the build rather than
    shipping the badge.
    """
    out = [list(b) for b in beats]
    i = 0
    guard = 0
    while i < len(out):
        guard += 1
        if guard > 10_000:                                  # pragma: no cover
            raise SystemExit("caption merge did not converge")
        txt = join(out[i])
        if not is_orphan_beat(txt, measurer.width(txt)):
            i += 1
            continue
        fwd = i + 1 < len(out) and measurer.width(join(out[i] + out[i + 1])) <= max_w
        bwd = i > 0 and measurer.width(join(out[i - 1] + out[i])) <= max_w
        if fwd:
            out[i + 1] = out[i] + out[i + 1]
            out.pop(i)
            continue
        if bwd:
            out[i - 1] = out[i - 1] + out[i]
            out.pop(i)
            i = max(0, i - 1)
            continue
        i += 1
    return out


merge_orphan_beats = merge_function_only_beats     # the name the law goes by


def assert_no_function_only_beat(texts) -> None:
    """Fail the build, loudly, on any beat that would paint a bare function word.

    `texts` may be plain strings or dicts carrying a "text" key.
    """
    bad = []
    for t in texts:
        if isinstance(t, dict):
            s, w = t["text"], t.get("w", t.get("pill_w_px"))
        else:
            s, w = str(t), None
        if is_orphan_beat(s, w):
            bad.append(f"{s!r}" + (f" ({w:.0f}px, aspect {w / CAP_PILL_HEIGHT:.2f})"
                                   if w else ""))
    if bad:
        raise SystemExit(
            "CAPTION LAW (run 9): a beat may never be a lone function word, nor "
            f"render as a pill squarer than {PILL_MIN_ASPECT} — it collapses into "
            "a brand badge (the \"in\" / LinkedIn defect). Offending beats:\n  "
            + "\n  ".join(bad))


__all__ = [
    "CAP_FONT", "CAP_FS", "CAP_PAD_X", "CAP_PAD_Y", "CAP_RADIUS", "CAP_BG",
    "CAP_FG", "CAP_FAMILY", "CAP_WEIGHT", "CAP_PILL_HEIGHT", "CAP_H",
    "CAP_LINE_BOX_EM", "CAP_SHADOW", "CANON", "FONT_LINK", "S", "px",
    "FRAME_W", "FRAME_H", "LAW12_BOTTOM", "LAW12_RAIL_X", "LAW12_TOP",
    "SEAT_MAX_W", "SEAT_INK_MAX", "pill_css", "pill_rule", "pill_height",
    "seat_bounds", "assert_law12",
    "HANDLE_YT", "HANDLE_TIKTOK_IG", "HANDLES", "HANDLE_KEYS", "DEFAULT_HANDLE",
    "handle", "handle_slug", "add_handle_arg", "outro_chip_html",
    "outro_daily_html", "OUTRO_MONO", "OUTRO_DAILY",
    "PillMeasurer", "runs", "split_to_fit", "split_balanced",
    "FUNCTION_WORDS", "MIN_SOLO_CHARS", "is_function_word", "is_function_only",
    "is_orphan_beat", "is_badge_pill", "PILL_MIN_ASPECT", "brand_token_ok",
    "merge_function_only_beats", "merge_orphan_beats",
    "assert_no_function_only_beat",
]
