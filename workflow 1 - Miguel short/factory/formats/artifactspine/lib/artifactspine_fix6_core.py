"""ARTIFACT SPINE — FIX ROUND 6.  THE CANONICAL CAPTION.

The closing captions round has exactly one job: this format's caption pill
becomes the SAME OBJECT as every other format's caption pill, and that object is
not a lab invention — it is the pill the factory has already published 7,614
times.  Everything else in these two videos is Miguel-approved and is not
touched: same window, same top seat centre, same schedule, same solver, same
SFX, same 25 fps.

--------------------------------------------------------------------------------
THE CANON, READ OUT OF THE PUBLISHED FACTORY (not chosen here)
--------------------------------------------------------------------------------
`references/builds/mcpupgrade_icon/projects/mcpupgrade_icon/index.html` is authored in a 576-wide
design space and painted into a 1080-wide root, i.e. every number in the file is
the design number x 1.875.  Its `.scappill` block and its 38 caption clips read:

    .scappill { display:inline-block; transform:translateY(-50%);
                background:#C4573A; color:#fff;
                font-family:Nunito,sans-serif; font-weight:800;
                padding:18.8px 33.8px; border-radius:22.5px;
                white-space:nowrap; }
    <span class="scappill" style="font-size:56.2px">…</span>   x38, ONE size

    56.2 / 1.875 = 29.97 -> 30 px      the design-space size
    18.8 / 1.875 = 10.03 -> 10 px      vertical padding
    33.8 / 1.875 = 18.03 -> 18 px      horizontal padding
    22.5 / 1.875 = 12.00 -> 12 px      corner radius

So in the 1080-wide space these two videos are authored in, the canonical pill
is **font-size 56.2 px, padding 18.8/33.8, radius 22.5, background #C4573A,
Nunito 800, white, nowrap**.  Round 5's lab pill was 41.0 px in a 19/34/22 box —
same family, wrong size and a third of a pixel off on every padding.  Round 6
replaces all six numbers with the published ones.

Pill height follows from the size and the font's own metrics, not from taste:
Nunito's hhea is ascent 1011 / descent -353 / lineGap 0 on a 1000 upem, so
`normal` line-height is 1.364 em and the box is

    56.2 * 1.364 + 2 * 18.8  =  76.66 + 37.60  =  114.3 px

against round 5's 92 px.  The pill grows 22 px; its CENTRE does not move.

--------------------------------------------------------------------------------
SPLIT, NEVER SHRINK
--------------------------------------------------------------------------------
The published `cap_font()` shrink-with-length formula is dead, and so is round
5's "solve one size from the widest caption" — both make the pill a function of
the phrase.  The canon is the other way round: the SIZE is fixed and the PHRASE
is cut to fit.  A caption whose ink exceeds the budget is split at word
boundaries into as few beats as possible, each beat timed from the word
timestamps it actually contains, so nothing is widened, squeezed or resized.

    ink budget   2 * (918 - 540) - 2 * 33.8  =  688.4 px      (LAW 12 rail)
    at 56.2 px   688.4 / 56.2               =  12.249 em      per caption

`918` is LAW 12's engagement-rail column.  At this format's TOP seat the rail
band (y 576..1824) is not even in play — the pill lives at y 231..345 — so the
budget is deliberately stricter than the law requires here, and it keeps this
format's beats inside the same width envelope as the published factory's
(published widest pill 808 px; ours cap at 756 px).

Splitting is a minimax partition, not a greedy fill: the words of an over-budget
phrase are cut into the fewest contiguous groups whose WIDEST group is as narrow
as possible, so a split reads as two balanced beats rather than a full line plus
an orphan.  Beat boundaries then take the real `start` of the first word of each
beat, so beat k ends exactly where beat k+1 begins and the caption track stays
gapless, exactly as it was before the split.

--------------------------------------------------------------------------------
WHAT ROUND 6 DOES NOT TOUCH
--------------------------------------------------------------------------------
The window (40,372 1000x1416, margins 40/40, scale exactly 1.000000, doc 936),
the top seat CENTRE (y 288), the schedule, the no-peek-ahead solver, the 30
state tweens, the pacing guard, the counter formatting, the Law 11 fills, the
ten SFX cues and 25 fps are round 5's, unchanged.  The pill is 22 px taller, so
its band becomes 12.03..17.98 % (round 5: 12.55..17.45 %) — still inside the
seat band, still 27 px clear of the artifact's top edge, so the pill still
overlaps ZERO document pixels at every frame of both cuts.
"""
from __future__ import annotations

import math
import re

import artifactspine_core as C
import artifactspine_fix3_core as L

FRAME_W, FRAME_H = 1080.0, 1920.0
SYM_TOL = 0.5

# ---- the window (round 5, unchanged) -----------------------------------------
WIN_X, WIN_W = 40.0, 1000.0
WIN_Y, WIN_H = 372.0, 1416.0

# ---- THE CANONICAL PILL (published factory, 1080-wide space) ------------------
# PROMOTED 2026-09-01: imported from `pipeline/captions.py`, the ONE place the
# canon lives, so this format cannot drift from the other five.
CAP_FS = C.CAP.CAP_FONT           # 56.2   30 px design-space x 1.875
CAP_PAD = C.CAP.CAP_PAD_X         # 33.8   18 px x 1.875   horizontal padding
CAP_VPAD = C.CAP.CAP_PAD_Y        # 18.8   10 px x 1.875   vertical padding
CAP_RADIUS = C.CAP.CAP_RADIUS     # 22.5   12 px x 1.875
CAP_BG = C.CAP.CAP_BG             # #C4573A
CAP_LINE = 1.364                  # Nunito hhea (1011 + 353 + 0) / 1000

CAP_Y = 288.0                     # the round-5 TOP seat centre — NOT moved
CAP_MAX_X = 918.0                 # LAW 12 rail column
CAP_INK_MAX = 2 * (CAP_MAX_X - 540.0) - 2 * CAP_PAD          # 688.4 px
CAP_MAX_EM = CAP_INK_MAX / CAP_FS                            # 12.249 em
RAIL_Y0 = 0.30 * FRAME_H          # 576
SEAT_LO, SEAT_HI = 0.115, 0.185
MIN_BEAT = 0.20                   # a split beat never flashes

FONT_WOFF2 = C.STAGE / "fonts" / "61025e3c21.woff2"          # Nunito 800, latin

_state: dict = {}


# =============================================================================
# THE FONT — advance widths straight out of the shipped file
# =============================================================================
def _metrics():
    if "cmap" not in _state:
        from fontTools.ttLib import TTFont
        f = TTFont(str(FONT_WOFF2))
        _state["upem"] = f["head"].unitsPerEm
        _state["cmap"] = f.getBestCmap()
        _state["hmtx"] = f["hmtx"]
    return _state["cmap"], _state["hmtx"], _state["upem"]


def em(s: str) -> float:
    """Sum of advances in em.  Kerning can only NARROW a line, so this is a safe
    upper bound on the rendered ink width."""
    cmap, hmtx, upem = _metrics()
    tot = 0
    for ch in s:
        g = cmap.get(ord(ch)) or cmap.get(ord("?"))
        tot += hmtx[g][0]
    return tot / upem


def ink(s: str) -> float:
    return em(s) * CAP_FS


def pill_w(s: str) -> float:
    return ink(s) + 2 * CAP_PAD


def pill_h() -> float:
    return round(CAP_FS * CAP_LINE + 2 * CAP_VPAD, 1)          # 114.3


def cap_font(_text: str) -> float:
    """THE canon: one size, every caption, every video, every format."""
    return CAP_FS


# =============================================================================
# SPLIT, NEVER SHRINK
# =============================================================================
def _minimax_partition(parts: list[str], k: int) -> list[list[str]]:
    """Cut `parts` into exactly k contiguous groups minimising the widest group.
    Exact DP — n is at most a dozen words, so there is no reason to approximate."""
    n = len(parts)
    seg = [[0.0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(i + 1, n + 1):
            seg[i][j] = em(" ".join(parts[i:j]))
    INF = float("inf")
    best = [[INF] * (k + 1) for _ in range(n + 1)]
    cut = [[0] * (k + 1) for _ in range(n + 1)]
    best[0][0] = 0.0
    for j in range(1, k + 1):
        for i in range(1, n + 1):
            for m in range(j - 1, i):
                if best[m][j - 1] == INF:
                    continue
                v = max(best[m][j - 1], seg[m][i])
                if v < best[i][j]:
                    best[i][j], cut[i][j] = v, m
    groups, i, j = [], n, k
    while j:
        m = cut[i][j]
        groups.append(parts[m:i])
        i, j = m, j - 1
    return list(reversed(groups))


def _retime(bounds: list[float], t0: float, t1: float) -> list[float]:
    """Push beat boundaries apart so no beat is shorter than MIN_BEAT, without
    moving the phrase's own start or end."""
    b = list(bounds)
    b[0], b[-1] = t0, t1
    for i in range(1, len(b) - 1):
        b[i] = max(b[i], b[i - 1] + MIN_BEAT)
    for i in range(len(b) - 2, 0, -1):
        b[i] = min(b[i], b[i + 1] - MIN_BEAT)
    for i in range(1, len(b) - 1):          # a phrase too short to hold k beats
        b[i] = max(b[i], b[i - 1] + 0.04)
    return b


def split_phrase(p: dict) -> list[dict]:
    """One caption in, one or more canonical-width captions out."""
    if em(p["text"]) <= CAP_MAX_EM:
        return [dict(p)]
    ws = p["ws"]
    toks = [w["text"] for w in ws]
    k = max(2, math.ceil(em(p["text"]) / CAP_MAX_EM))
    while k <= len(toks):
        groups = _minimax_partition(toks, k)
        if max(em(" ".join(g)) for g in groups) <= CAP_MAX_EM:
            break
        k += 1
    else:                                    # a single word wider than the budget
        groups = _minimax_partition(toks, len(toks))
    idx, starts = 0, []
    for g in groups:
        starts.append(ws[idx]["start"])
        idx += len(g)
    bounds = _retime(starts + [p["t1"]], p["t0"], p["t1"])
    out = []
    for i, g in enumerate(groups):
        out.append({"t0": round(bounds[i], 2), "t1": round(bounds[i + 1], 2),
                    "text": " ".join(g), "n": len(g), "split": len(groups)})
    _state.setdefault("splits", []).append((p["text"], [o["text"] for o in out]))
    return out


def build_captions(words: list[dict]) -> list[dict]:
    """`artifactspine_core.build_captions`, carrying the words of each phrase so
    a phrase can be cut at a real word boundary, then split to the canon."""
    phrases, cur = [], []
    words = C.clean_tokens(words)
    for i, word in enumerate(words):
        cur.append(word)
        nxt = words[i + 1] if i + 1 < len(words) else None
        punct = bool(re.search(r"[.,!?]$", word["text"]))
        gap = bool(nxt and nxt["start"] - word["end"] > 0.32)
        if len(cur) >= 4 or (punct and len(cur) >= 2) or gap or nxt is None:
            phrases.append({"t0": round(cur[0]["start"], 2),
                            "t1": round(word["end"] + 0.12, 2),
                            "text": " ".join(x["text"] for x in cur),
                            "n": len(cur), "ws": list(cur)})
            cur = []
    merged: list[dict] = []
    for p in phrases:
        if p["n"] == 1 and merged:
            merged[-1]["text"] += " " + p["text"]
            merged[-1]["t1"] = p["t1"]
            merged[-1]["n"] += 1
            merged[-1]["ws"] += p["ws"]
            continue
        merged.append(dict(p))
    for i in range(len(merged) - 1):
        merged[i]["t1"] = merged[i + 1]["t0"]

    _state["pre_split"] = len(merged)
    _state["splits"] = []
    out: list[dict] = []
    for p in merged:
        out.extend(split_phrase(p))
    _state["post_split"] = len(out)
    _state["caps"] = out
    return out


# =============================================================================
# THE CANONICAL CSS
# =============================================================================
CANON_CSS = (f"padding:{CAP_VPAD}px {CAP_PAD}px;", f"border-radius:{CAP_RADIUS}px;")
_base_css = C.base_css


def base_css() -> str:
    css = _base_css()
    css = css.replace("padding:19px 34px;", CANON_CSS[0])
    css = css.replace("border-radius:22px;", CANON_CSS[1])
    return css


# =============================================================================
# VERIFY THE EMITTED PAGE — the generator is not trusted
# =============================================================================
def verify_page(page: str) -> list[str]:
    bad = []
    block = re.search(r"\.scappill \{(.*?)\}", page, re.S)
    if not block:
        bad.append("no .scappill rule in the emitted page")
    else:
        b = " ".join(block.group(1).split())
        for want in (f"background:{CAP_BG}", "color:#fff",
                     "font-family:Nunito,sans-serif", "font-weight:800",
                     f"padding:{CAP_VPAD}px {CAP_PAD}px",
                     f"border-radius:{CAP_RADIUS}px", "white-space:nowrap",
                     "transform:translateY(-50%)"):
            if want not in b:
                bad.append(f".scappill missing canonical {want!r}  (got {b})")
    sizes = re.findall(r'class="scappill" style="font-size:([\d.]+)px"', page)
    if not sizes:
        bad.append("no caption pills in the emitted page")
    elif set(sizes) != {f"{CAP_FS}"}:
        bad.append(f"caption font sizes in the page: {sorted(set(sizes))} "
                   f"(want exactly {CAP_FS})")
    tops = {float(v) for v in
            re.findall(r'class="clip scap" style="top:([\d.]+)px"', page)}
    if tops != {CAP_Y}:
        bad.append(f"caption seat tops in the page: {sorted(tops)} (want {CAP_Y})")
    if bad:
        raise SystemExit("[canon/r6] emitted page failed:\n  " + "\n  ".join(bad))
    return [f"     CANON r6  emitted pills: {len(sizes)} clips, ONE font-size "
            f"{CAP_FS} px, ONE seat top {CAP_Y:.0f}, "
            f"padding {CAP_VPAD}/{CAP_PAD}, radius {CAP_RADIUS}, bg {CAP_BG} "
            f"— identical to the published factory pill"]


# =============================================================================
# LAW 12 — round-6 report
# =============================================================================
def pill_rect_max() -> tuple[float, float, float, float]:
    caps = _state["caps"]
    w = max(pill_w(c["text"]) for c in caps)
    h = pill_h()
    return (540.0 - w / 2, CAP_Y - h / 2, 540.0 + w / 2, CAP_Y + h / 2)


def law12_report(*, content_left: float, content_right: float,
                 content_top: float, content_bottom: float) -> list[str]:
    bad = []
    ml, mr = L.WIN_X, FRAME_W - (L.WIN_X + L.WIN_W)
    if abs(ml - mr) > SYM_TOL:
        bad.append(f"ASYMMETRIC: window margins left {ml:.1f} right {mr:.1f}")

    px0, py0, px1, py1 = pill_rect_max()
    if py0 < L.TOP_ZONE:
        bad.append(f"CAPTION SEAT: pill top {py0:.1f} < top-10% line {L.TOP_ZONE:.0f}")
    if not (SEAT_LO <= py0 / FRAME_H and py1 / FRAME_H <= SEAT_HI):
        bad.append(f"CAPTION SEAT: pill band {100 * py0 / FRAME_H:.1f}.."
                   f"{100 * py1 / FRAME_H:.1f} % outside "
                   f"{100 * SEAT_LO:.1f}..{100 * SEAT_HI:.1f} %")
    if py1 > RAIL_Y0:
        bad.append(f"CAPTION SEAT: pill bottom {py1:.1f} enters the rail band")
    if px1 > CAP_MAX_X:
        bad.append(f"CAPTION: widest pill reaches x={px1:.1f} (> {CAP_MAX_X:.0f})")
    if py1 > L.WIN_Y:
        bad.append(f"CAPTION OVERLAP: pill bottom {py1:.1f} is inside the "
                   f"presentation rect (top {L.WIN_Y:.1f})")
    caps = _state["caps"]
    over = [c["text"] for c in caps if pill_w(c["text"]) > 2 * (CAP_MAX_X - 540.0)]
    if over:
        bad.append(f"CAPTION: {len(over)} caption(s) still over budget: {over[:3]}")
    short = [c for c in caps if c["t1"] - c["t0"] < 0.08]
    if short:
        bad.append(f"CAPTION: {len(short)} beat(s) shorter than a rendered clip")
    if bad:
        raise SystemExit("[law12/r6] failed:\n  " + "\n  ".join(bad))

    gap = L.WIN_Y - py1
    ws = sorted((pill_w(c["text"]) for c in caps), reverse=True)
    ns = _state["pre_split"], _state["post_split"], len(_state["splits"])
    return [
        f"     LAW 12 r6  window margins  left {ml:.1f}  right {mr:.1f}  "
        f"(delta {abs(ml - mr):.2f} <= {SYM_TOL})  CENTRED",
        f"     LAW 12 r6  caption TOP SEAT  widest pill x {px0:.0f}..{px1:.0f} "
        f"(<= {CAP_MAX_X:.0f})  y {py0:.1f}..{py1:.1f} = "
        f"{100 * py0 / FRAME_H:.2f}..{100 * py1 / FRAME_H:.2f} % "
        f"(top-10% {L.TOP_ZONE:.0f}, rail band {RAIL_Y0:.0f})",
        f"     LAW 12 r6  pill-to-artifact gap {gap:.1f} px — ZERO overlap at "
        f"every frame, so no fresh content can ever sit under the pill",
        f"     CANON r6  ONE font size {CAP_FS} px, pill box {pill_h():.1f} px "
        f"for all {len(caps)} captions  (published factory pill, 30 px x 1.875)",
        f"     CANON r6  SPLIT not shrunk: {ns[0]} phrases -> {ns[1]} beats "
        f"({ns[2]} phrase(s) split at word boundaries)  widest pill "
        f"{ws[0]:.1f} px, next {ws[1]:.1f}/{ws[2]:.1f}  (budget "
        f"{CAP_INK_MAX + 2 * CAP_PAD:.1f})",
        f"     LAW 12 r6  artifact ink x {content_left:.0f}..{content_right:.0f}"
        f"   y {content_top:.0f}..{content_bottom:.0f}  — composition exempt from "
        f"the rail and the 72 % line (round-4 amendment)",
    ]


# =============================================================================
def apply(words: list[dict] | None = None) -> dict:
    """Repoint round 3's shared geometry at the round-5 window + top seat, and
    swap the caption object for the published canon."""
    caps = build_captions(words if words is not None else _words())
    before_pill = L.PILL_H

    L.WIN_X, L.WIN_Y, L.WIN_W, L.WIN_H = WIN_X, WIN_Y, WIN_W, WIN_H
    L.CAP_Y = CAP_Y
    L.PILL_H = pill_h()
    L.CAP_PAD = CAP_PAD
    L.cap_font = cap_font
    L.law12_report = law12_report
    C.build_captions = build_captions
    C.base_css = base_css

    C.measure_marks()
    g = L.Geom()
    if abs(g.s - 1.0) > 1e-9 or abs(g.doc_w - 936.0) > 1e-9:
        raise SystemExit(f"[r6] round-1 scale not restored: s={g.s:.6f} "
                         f"doc_w={g.doc_w:.2f}")

    print(f"     ROUND 6  CANONICAL PILL  font 56.2 px (was 41.0)  "
          f"padding {CAP_VPAD}/{CAP_PAD} (was 19/34)  radius {CAP_RADIUS} "
          f"(was 22)  bg {CAP_BG}")
    print(f"     ROUND 6  pill box {before_pill:.1f} -> {pill_h():.1f} px   "
          f"seat centre {CAP_Y:.0f} UNCHANGED   y "
          f"{CAP_Y - pill_h() / 2:.1f}..{CAP_Y + pill_h() / 2:.1f} = "
          f"{100 * (CAP_Y - pill_h() / 2) / FRAME_H:.2f}.."
          f"{100 * (CAP_Y + pill_h() / 2) / FRAME_H:.2f} %")
    print(f"     ROUND 6  captions {_state['pre_split']} -> {len(caps)} beats, "
          f"{len(_state['splits'])} phrase(s) SPLIT at word boundaries "
          f"(budget {CAP_MAX_EM:.3f} em = {CAP_INK_MAX:.1f} px of ink)")
    for src, parts in _state["splits"]:
        print(f"                {src!r}  ->  " + "  |  ".join(repr(p) for p in parts))
    return {"geom": g, "caps": caps}


def _words() -> list[dict]:
    import artifactspine_fix_core as X
    words, _dur, _a = X.load_timing()
    return words


def captions_of() -> list[dict]:
    return _state.get("caps") or build_captions(_words())
