"""THE SHARED LANE SCENE — Diagram Build, authored ONCE for three formats.

This is the "shared-scene economy" the daily distribution pipeline is built on:
one build emits three compositions, and the thing they share is THIS module. The
scene is authored in an intrinsic **1000 x 680 core** and each format places that
core in the region it owns, at the one scale that fits:

    classic split  top zone 0..862.5      scale 1.00   left 40   top 91.2
    cutout         stage zone 192..ZY1    scale 0.95   (derived from the envelope)
    takeover       full-bleed [0,1258)    scale 1.05   centred on REGION_MID 629

The core is a single absolutely-positioned wrapper with a STATIC
`transform: scale(k)` and `transform-origin: 0 0`. Static because Law 1 bans idle
motion and Law 21 bans animating the frame itself: the scale is a placement, not
a move, and it never changes during a video. `geometry_audit.py` measures live
client rects, so it sees the SCALED boxes — which is what actually ships.

WHY ONE CONTINUOUS TIMELINE. The takeover shows only some windows of this scene,
and the naive design is a separate scene per cutaway. It is not what the format
does: the world runs continuously behind the cuts, the face clips sit on top of
it, and a cutaway therefore samples a scene that has been developing all along.
That is what makes ARRIVE IN MOTION cheap — an interior tween that started
`LEAD` before the clip appeared is mid-gesture on the clip's first visible frame
without anything being authored twice.

THE STORY IS THE TRANSCRIPT'S, and every cue below is a word start read out of
`cuts/perplexityprojects/transcript_tight.json`, never a round number.
"""
from __future__ import annotations

# ---------------------------------------------------------------- palette
CREAM = "#F6F1EA"
CARD = "#FFFDF9"
INK = "#141416"
TERRA = "#C4573A"
MUTE = "rgba(20,20,22,.34)"
FAINT = "rgba(20,20,22,.20)"
HAIR = "rgba(20,20,22,.13)"

CORE_W, CORE_H = 1000.0, 680.0
# THE CONTENT BAND. Law 30 forbids meaningful content in the frame's top 10%
# (y < 192). The core is placed by each format, so the core cannot know its own
# canvas y — it declares the band it actually paints in and every format asserts
# that the band lands legally. CONTENT_Y0 is the smallest core y any atom
# occupies; CONTENT_Y1 the largest.
CONTENT_Y0, CONTENT_Y1 = 40.0, 534.0
SOFT = "SOFT"                      # the eases are declared in the page

# ---------------------------------------------------------------- cues
# every value is a word START from the tight transcript (index: word)
CUE = {
    "perplexity0": 0.20,   # w0  Perplexity
    "launched": 0.92,      # w2  launched
    "projects0": 1.92,     # w4  Projects,
    "evolution": 2.74,     # w6  evolution
    "spaces": 3.94,        # w9  Spaces.
    "arrow": 4.24,         # +0.30 after `Spaces.` starts: both nodes exist first
    "turn": 6.58,          # w17 turn
    "oneoff": 8.34,        # w21 one-off
    "tool": 9.20,          # w23 tool
    "desk": 10.54,         # w27 desk,
    "folders": 11.64,      # w30 folders
    "themes": 13.20,       # w38 themes
    "whether": 15.46,      # w45 whether
    "online": 16.22,       # w47 online
    "deep": 17.30,         # w49 deep
    "local": 18.74,        # w53 local
    "computer": 20.68,     # w61 computer.
    "store": 21.86,        # w65 store
    "dedicated": 22.54,    # w68 dedicated
    "anyother": 24.62,     # w75 any
    "outro": 25.88,        # w79 Now
    "daily": 28.18,        # w90 single
}

# beat windows, used by the formats for their own sectioning / cut maps
BEATS = [
    ("b0", 0.00, 6.52),
    ("b1", 6.52, 11.20),
    ("b2", 11.20, 15.42),
    ("b3", 15.42, 21.36),
    ("b4", 21.36, 25.86),
    ("ou", 25.86, 30.016),
]


# ---------------------------------------------------------------- helpers
def _s(d: dict) -> str:
    return "".join(f"{k}:{v};" for k, v in d.items())


def div(eid: str, cls: str, style: dict, inner: str = "", extra: str = "") -> str:
    return (f'<div class="abs {cls}" id="{eid}" style="{_s(style)}"{extra}>'
            f'{inner}</div>')


def box(eid, x, y, w, h, *, bg=CARD, radius=22.0, border=f"3.6px solid {HAIR}",
        cls="", inner="", extra="", shadow=True, opacity=None):
    st = {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
          "height": f"{h}px", "background": bg,
          "border-radius": f"{radius}px"}
    if border:
        st["border"] = border
    if shadow:
        st["box-shadow"] = "0 9px 32px rgba(0,0,0,.10)"
    if opacity is not None:
        st["opacity"] = opacity
    return div(eid, cls, st, inner, extra)


def label(eid, x, y, w, text, *, size=30.0, color=MUTE, weight=600, mono=True,
          ls=2.4, align="center", opacity=None):
    st = {"left": f"{x}px", "top": f"{y}px", "width": f"{w}px",
          "text-align": align, "font-size": f"{size}px",
          "line-height": f"{size * 1.34:.2f}px", "font-weight": weight,
          "color": color, "letter-spacing": f"{ls}px"}
    if opacity is not None:
        st["opacity"] = opacity
    return div(eid, "mono" if mono else "disp", st, text)


def folder_svg(w: float, h: float, *, mark: str = "", lines=(), fill=CARD,
               stroke=INK, sw=5.0, tab_frac=0.34):
    """A folder: a tab on the top-left, a body under it, ONE closed outline.

    The tab and the body are one path so the silhouette reads as a single object
    (LABEL + OBJECT = ONE BLOCK is about names; this is the same idea for the
    shape). `lines` are the ragged content rules — real ragged widths, never
    three identical wallpaper cards.
    """
    tw = w * tab_frac
    th = h * 0.155
    r = 12.0
    # ONE closed outline: the tab is the left part of the top edge, stepped down
    # to the body's own top edge. A folder read as two shapes reads as a bug.
    d = (f"M{r} 0 L{tw - r} 0 Q{tw} 0 {tw + 10} {th} "
         f"L{w - r} {th} A{r} {r} 0 0 1 {w} {th + r} L{w} {h - r} "
         f"A{r} {r} 0 0 1 {w - r} {h} L{r} {h} "
         f"A{r} {r} 0 0 1 0 {h - r} L0 {r} A{r} {r} 0 0 1 {r} 0 Z")
    body = (f'<path class="fbody" pathLength="100" d="{d}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>')
    rules = ""
    y = th + h * 0.30
    for i, frac in enumerate(lines):
        rules += (f'<rect class="frule r{i}" x="{w * 0.12:.1f}" y="{y:.1f}" '
                  f'width="{w * 0.76 * frac:.1f}" height="{h * 0.052:.1f}" '
                  f'rx="{h * 0.026:.1f}" fill="{FAINT}"/>')
        y += h * 0.125
    inner_mark = ""
    if mark:
        ms = min(w, h) * 0.34
        inner_mark = (f'<image class="fmark" href="{mark}" x="{(w - ms) / 2:.1f}" '
                      f'y="{th + (h - th - ms) / 2:.1f}" width="{ms:.1f}" '
                      f'height="{ms:.1f}" preserveAspectRatio="xMidYMid meet"/>')
    return (f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            f'{body}{rules}{inner_mark}</svg>')


def openbox_svg(w: float, h: float, *, sw=5.0, stroke=INK):
    """The SPACES glyph: a container with NO lid — three sides, open at the top."""
    r = 12.0
    d = (f"M0 0 L0 {h - r} A{r} {r} 0 0 0 {r} {h} L{w - r} {h} "
         f"A{r} {r} 0 0 0 {w} {h - r} L{w} 0")
    return (f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            f'<path class="obody" pathLength="100" d="{d}" fill="none" '
            f'stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" '
            f'stroke-linecap="round"/></svg>')


def sheet_svg(w: float, h: float, *, lines=(0.86, 0.62, 0.78, 0.44), sw=4.2):
    r = 10.0
    rules = ""
    y = h * 0.20
    for i, frac in enumerate(lines):
        rules += (f'<rect x="{w * 0.14:.1f}" y="{y:.1f}" '
                  f'width="{w * 0.72 * frac:.1f}" height="{h * 0.045:.1f}" '
                  f'rx="{h * 0.0225:.1f}" fill="{FAINT}"/>')
        y += h * 0.145
    return (f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            f'<rect class="sbody" x="{sw / 2}" y="{sw / 2}" '
            f'width="{w - sw}" height="{h - sw}" rx="{r}" fill="{CARD}" '
            f'stroke="{INK}" stroke-width="{sw}"/>{rules}</svg>')


def globe_svg(s: float, sw=5.0):
    c = s / 2
    r = s * 0.40
    return (f'<svg viewBox="0 0 {s} {s}" width="{s}" height="{s}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            f'<circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="{INK}" '
            f'stroke-width="{sw}"/>'
            f'<ellipse cx="{c}" cy="{c}" rx="{r * 0.42}" ry="{r}" fill="none" '
            f'stroke="{INK}" stroke-width="{sw * 0.7}"/>'
            f'<path d="M{c - r} {c} H{c + r}" stroke="{INK}" '
            f'stroke-width="{sw * 0.7}"/>'
            f'<path d="M{c - r * 0.86} {c - r * 0.45} H{c + r * 0.86}" '
            f'stroke="{INK}" stroke-width="{sw * 0.6}" opacity=".55"/>'
            f'<path d="M{c - r * 0.86} {c + r * 0.45} H{c + r * 0.86}" '
            f'stroke="{INK}" stroke-width="{sw * 0.6}" opacity=".55"/></svg>')


def depth_svg(s: float, sw=5.0):
    """DEEP research: three plates stacked downwards, the lowest terracotta."""
    out = []
    w = s * 0.78
    x = (s - w) / 2
    for i in range(3):
        y = s * 0.20 + i * s * 0.20
        col = TERRA if i == 2 else INK
        op = 1.0 if i == 2 else 0.42 + 0.2 * i
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" '
                   f'height="{s * 0.12:.1f}" rx="{s * 0.045:.1f}" fill="none" '
                   f'stroke="{col}" stroke-width="{sw}" opacity="{op:.2f}"/>')
    out.append(f'<path d="M{s / 2} {s * 0.14} V{s * 0.19}" stroke="{INK}" '
               f'stroke-width="{sw * 0.7}" opacity=".4"/>')
    return (f'<svg viewBox="0 0 {s} {s}" width="{s}" height="{s}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            + "".join(out) + "</svg>")


def laptop_svg(s: float, sw=5.0):
    w = s * 0.80
    x = (s - w) / 2
    top = s * 0.22
    hgt = s * 0.42
    return (f'<svg viewBox="0 0 {s} {s}" width="{s}" height="{s}" '
            f'style="position:absolute;left:0;top:0;overflow:visible">'
            f'<rect x="{x:.1f}" y="{top:.1f}" width="{w:.1f}" height="{hgt:.1f}" '
            f'rx="{s * 0.05:.1f}" fill="{CARD}" stroke="{INK}" '
            f'stroke-width="{sw}"/>'
            f'<rect x="{x + w * 0.16:.1f}" y="{top + hgt * 0.26:.1f}" '
            f'width="{w * 0.46:.1f}" height="{hgt * 0.10:.1f}" '
            f'rx="{hgt * 0.05:.1f}" fill="{FAINT}"/>'
            f'<rect class="lscreen" x="{x + w * 0.16:.1f}" y="{top + hgt * 0.52:.1f}" '
            f'width="{w * 0.32:.1f}" height="{hgt * 0.10:.1f}" '
            f'rx="{hgt * 0.05:.1f}" fill="{TERRA}" style="transform-origin:{x + w * 0.16:.1f}px {top + hgt * 0.57:.1f}px"/>'
            f'<rect x="{x - w * 0.10:.1f}" y="{top + hgt + s * 0.03:.1f}" '
            f'width="{w * 1.20:.1f}" height="{s * 0.075:.1f}" '
            f'rx="{s * 0.037:.1f}" fill="{INK}"/></svg>')


def stem(eid, x1, y1, x2, y2, *, sw=5.0, color=TERRA, head=True):
    """A connector as its own SVG, with stroke/2 of viewBox margin on every side.

    The hermesvoicemagic finding: a path traced on its own viewport boundary is
    CLIPPED to half its stroke and no gate can see it. So the box is inflated by
    the widest stroke it will carry, and the path is drawn in the inflated space.
    """
    pad = sw * 2 + 14
    x0, y0 = min(x1, x2) - pad, min(y1, y2) - pad
    w = abs(x2 - x1) + 2 * pad
    h = abs(y2 - y1) + 2 * pad
    ax, ay = x1 - x0, y1 - y0
    bx, by = x2 - x0, y2 - y0
    import math
    ang = math.atan2(by - ay, bx - ax)
    hl = 17.0
    hw = 10.0
    tipx, tipy = bx, by
    arrow = ""
    if head:
        # the shaft stops at the arrow's base so the head is the only thing that
        # reaches the target's edge -- arrows terminate AT a box edge (Law 7)
        bxs = bx - hl * math.cos(ang)
        bys = by - hl * math.sin(ang)
        p1 = (bxs - hw * math.sin(ang), bys + hw * math.cos(ang))
        p2 = (bxs + hw * math.sin(ang), bys - hw * math.cos(ang))
        arrow = (f'<path class="shead" d="M{tipx:.1f} {tipy:.1f} '
                 f'L{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f} Z" '
                 f'fill="{color}" opacity="0"/>')
        bx, by = bxs, bys
    return div(eid, "stemwrap", {"left": f"{x0}px", "top": f"{y0}px",
                                 "width": f"{w}px", "height": f"{h}px"},
               f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
               f'style="position:absolute;left:0;top:0;overflow:visible">'
               f'<path class="sline" pathLength="100" d="M{ax:.1f} {ay:.1f} '
               f'L{bx:.1f} {by:.1f}" fill="none" stroke="{color}" '
               f'stroke-width="{sw}" stroke-linecap="round" '
               f'stroke-opacity="0"/>{arrow}</svg>',
               extra=' data-overlap-ok')


# ---------------------------------------------------------------- the scene
def build(logo: dict, lockup: str = "") -> tuple[str, list[str]]:
    """Return (html, tweens) for the whole 30.016s scene in core coordinates."""
    H: list[str] = []
    T: list[str] = []

    def tw(js: str) -> None:
        T.append(js)

    def set0(sel: str, props: str) -> None:
        tw(f'tl.set("{sel}",{{{props}}},0);')

    def app(sel, at, dur, frm, to, ease=SOFT):
        tw(f'tl.fromTo("{sel}",{{{frm}}},{{{to},duration:{dur},ease:{ease},'
           f'immediateRender:false}},{at:.2f});')

    def to(sel, at, dur, props, ease=SOFT):
        tw(f'tl.to("{sel}",{{{props},duration:{dur},ease:{ease}}},{at:.2f});')

    def draw(sel, at, dur):
        """A dash draw-on that obeys THE GHOST RULE: it rests at stroke-opacity 0
        and reveals one frame (0.04s at 25fps) after the draw starts, because
        Skia paints a round linecap at progress 0 and an 'un-drawn' path is
        otherwise a visible dot."""
        set0(sel, "strokeDasharray:100,strokeDashoffset:100,strokeOpacity:0")
        tw(f'tl.set("{sel}",{{strokeOpacity:1}},{at + 0.04:.2f});')
        to(sel, at, dur, "strokeDashoffset:0")

    # ============================================================ b0 — HOOK
    # THE HOOK OBJECT (Law 20 / Law 13): the evolution, drawn. Not furniture.
    # RUN 9: at 118 the mark measured ~44 px on a 405x720 phone crop, and in the
    # cutout it lost the hook frame outright to a wall of 148 px app tiles ("the
    # one thing that is the subject is a 40 px glyph").  The hook mark is now 210
    # and shrinks to its old optical size on `launched`, when it stops being the
    # whole picture and becomes a node in one.
    MK = 210.0
    H.append(div("h-mark", "", {"left": f"{(CORE_W - MK) / 2:.1f}px",
                                "top": f"{(CORE_H - MK) / 2 - 60:.1f}px",
                                "width": f"{MK}px", "height": f"{MK}px",
                                "opacity": "0"},
                 f'<img src="{logo["perplexity"]}" alt="" '
                 f'style="width:100%;height:100%;object-fit:contain">'))
    # the folder: appears CENTRED (Law 19), then displaces right to make room
    FW, FH = 300.0, 230.0
    FX_C, FX_E, FY = (CORE_W - FW) / 2, 550.0, 208.0
    H.append(div("h-fold", "", {"left": f"{FX_C:.1f}px", "top": f"{FY}px",
                                "width": f"{FW}px", "height": f"{FH}px",
                                "opacity": "0"},
                 folder_svg(FW, FH, lines=(0.92, 0.58, 0.74))))
    # the OLD object: an open-sided box, smaller and quieter
    OW, OH = 210.0, 160.0
    OX, OY = 150.0, FY + (FH - OH) / 2
    H.append(div("h-open", "", {"left": f"{OX}px", "top": f"{OY:.1f}px",
                                "width": f"{OW}px", "height": f"{OH}px",
                                "opacity": "0"}, openbox_svg(OW, OH)))
    H.append(stem("h-arrow", OX + OW, FY + FH / 2, FX_E - 8, FY + FH / 2))
    H.append(label("h-lp", FX_C, 466.0, FW, "PROJECTS", size=54.0, color=INK,
                   weight=700, ls=4.0, opacity=0))
    H.append(label("h-ls", OX, 472.0, OW, "SPACES", size=30.0, color=MUTE,
                   ls=3.0, opacity=0))

    app("#h-mark", CUE["perplexity0"], 0.46, "opacity:0,scale:0.86",
        "opacity:1,scale:1")
    # y and scale together reproduce the APPROVED resting geometry exactly: the
    # mark's centre lands at core y=103 painting a 118 px box, i.e. the box the
    # split render has always come to rest in.  Only the first 0.72 s is bigger.
    to("#h-mark", CUE["launched"], 0.54, "y:-177.0,scale:0.5619")
    app("#h-fold", CUE["projects0"], 0.52, "opacity:0,scale:0.90",
        "opacity:1,scale:1")
    draw("#h-fold .fbody", CUE["projects0"] + 0.04, 0.62)
    set0("#h-fold .frule", "opacity:0")
    tw(f'tl.to("#h-fold .frule",{{opacity:1,duration:0.26,ease:{SOFT},'
       f'stagger:0.07}},{CUE["projects0"] + 0.60:.2f});')
    app("#h-lp", CUE["projects0"] + 0.34, 0.36, "opacity:0,y:14",
        "opacity:1,y:0")
    # `evolution` — the folder makes room for the thing it came from
    to("#h-fold", CUE["evolution"], 0.56, f"x:{FX_E - FX_C:.1f}")
    to("#h-lp", CUE["evolution"], 0.56, f"x:{FX_E - FX_C:.1f}")
    app("#h-open", CUE["spaces"], 0.40, "opacity:0,scale:0.92",
        "opacity:0.72,scale:1")
    draw("#h-open .obody", CUE["spaces"] + 0.04, 0.52)
    app("#h-ls", CUE["spaces"] + 0.30, 0.32, "opacity:0,y:12",
        "opacity:0.85,y:0")
    # the connector draws only AFTER both nodes exist (BUILD ORDER)
    draw("#h-arrow .sline", CUE["arrow"], 0.40)
    app("#h-arrow .shead", CUE["arrow"] + 0.34, 0.18, "opacity:0", "opacity:1")

    # RUN 9, THE UNLABELLED SHEET.  b0 used to clear at 6.28 and the one-off card
    # arrived at `turn` (6.58) with its ONE-OFF key 1.76 s behind it, so 6.7-8.3 s
    # was a blank unlabelled page alone in an empty field — two NO-SENSE frames in
    # the viewer test, on both the split and the cutout.
    #
    # THE LAW: a bespoke object and its printed key are ONE BLOCK and arrive on
    # the same beat, the beat the word is spoken.  So the hook diagram — which is
    # still exactly on topic while he says "Now, Perplexity Projects will allow
    # you to turn Perplexity from a" — HOLDS until the one-off card is ready, and
    # card and key land together on the word "one-off" at 8.34.
    #
    # ROUND 2 OF THE VIEWER TEST measured what was left: a 3-frame valley at
    # 8.24-8.32 s where the zone holds 0.000 % ink — b0's clear-out ended at
    # 8.34 and the one-off card's fade began at 8.34, so the two fades met at a
    # point instead of overlapping, and a crossfade that meets at a point is a
    # hole.  The card is NOT moved: it lands on the word "one-off" (8.34) and
    # that is the law.  b0's tail is lengthened instead, so the outgoing diagram
    # is still carrying ink while the incoming card takes over — ~7 frames of
    # genuine overlap, and the zone never empties.  The hold, the start and the
    # card are all untouched; only this fade's DURATION changed.
    b0_out = CUE["oneoff"] - 0.30
    for sel in ("#h-mark", "#h-fold", "#h-open", "#h-arrow", "#h-lp", "#h-ls"):
        to(sel, b0_out, 0.60, "opacity:0")

    # ============================================================ b1 — the desk
    SW_, SH_ = 152.0, 194.0
    DESK_Y = 470.0
    SEAT_Y = DESK_Y - SH_
    sheet_x = (232.0, 424.0, 616.0)
    H.append(div("b1-s0", "", {"left": f"{sheet_x[1]}px",
                               "top": f"{SEAT_Y - 96:.1f}px",
                               "width": f"{SW_}px", "height": f"{SH_}px",
                               "opacity": "0"},
                 sheet_svg(SW_, SH_, lines=(0.86, 0.62, 0.78, 0.44))))
    H.append(div("b1-s1", "", {"left": f"{sheet_x[1]}px",
                               "top": f"{SEAT_Y - 96:.1f}px",
                               "width": f"{SW_}px", "height": f"{SH_}px",
                               "opacity": "0"},
                 sheet_svg(SW_, SH_, lines=(0.72, 0.90, 0.55, 0.66))))
    H.append(label("b1-lo", sheet_x[1] - 60, SEAT_Y - 168, SW_ + 120, "ONE-OFF",
                   size=32.0, color=TERRA, ls=5.0, opacity=0))
    H.append(div("b1-desk", "", {"left": "108px", "top": f"{DESK_Y}px",
                                 "width": "784px", "height": "30px",
                                 "background": INK, "border-radius": "15px",
                                 "opacity": "0"}))
    H.append(div("b1-deskr", "", {"left": "108px", "top": f"{DESK_Y + 30}px",
                                  "width": "784px", "height": "12px",
                                  "background": "rgba(20,20,22,.28)",
                                  "border-radius": "0 0 8px 8px",
                                  "opacity": "0"}))
    H.append(label("b1-ld", 240.0, DESK_Y + 66, 520.0, "RESEARCH DESK",
                   size=40.0, color=INK, weight=700, ls=5.0, opacity=0))
    H.append(div("b1-a", "", {"left": f"{sheet_x[0]}px", "top": f"{SEAT_Y}px",
                              "width": f"{SW_}px", "height": f"{SH_}px",
                              "opacity": "0"},
                 sheet_svg(SW_, SH_, lines=(0.58, 0.84, 0.70))))
    H.append(div("b1-b", "", {"left": f"{sheet_x[2]}px", "top": f"{SEAT_Y}px",
                              "width": f"{SW_}px", "height": f"{SH_}px",
                              "opacity": "0"},
                 sheet_svg(SW_, SH_, lines=(0.90, 0.48, 0.66, 0.80))))

    set0("#b1-desk", "opacity:0,scaleX:0.16")
    set0("#b1-deskr", "opacity:0")
    app("#b1-s0", CUE["oneoff"], 0.42, "opacity:0,scale:0.88,y:26",
        "opacity:1,scale:1,y:0")
    app("#b1-lo", CUE["oneoff"] + 0.06, 0.32, "opacity:0,y:12", "opacity:1,y:0")
    # `tool` — the one-off IS the event: the sheet leaves, another takes its seat
    to("#b1-s0", CUE["tool"], 0.34, "opacity:0,x:-150,rotate:-7")
    app("#b1-s1", CUE["tool"] + 0.20, 0.34, "opacity:0,x:150,rotate:7",
        "opacity:1,x:0,rotate:0")
    # `desk` — the surface draws under it and the loose page becomes a place
    to("#b1-desk", CUE["desk"], 0.52, "opacity:1,scaleX:1")
    to("#b1-deskr", CUE["desk"] + 0.30, 0.26, "opacity:1")
    to("#b1-lo", CUE["desk"], 0.26, "opacity:0")
    to("#b1-s1", CUE["desk"] + 0.10, 0.46, "y:96")
    app("#b1-a", CUE["desk"] + 0.34, 0.40, "opacity:0,y:-40",
        "opacity:1,y:0")
    app("#b1-b", CUE["desk"] + 0.44, 0.40, "opacity:0,y:-40",
        "opacity:1,y:0")
    app("#b1-ld", CUE["desk"] + 0.36, 0.34, "opacity:0,y:14", "opacity:1,y:0")

    # ============================================================ b2 — folders
    GW, GH = 200.0, 150.0
    gx = (180.0, 400.0, 620.0)
    gy = DESK_Y - GH
    RAG = ((0.94, 0.55), (0.68, 0.88, 0.46), (0.82, 0.60))
    TAGW = (58.0, 40.0, 50.0)
    for i, x in enumerate(gx):
        H.append(div(f"b2-f{i}", "", {"left": f"{x}px", "top": f"{gy}px",
                                      "width": f"{GW}px", "height": f"{GH}px",
                                      "opacity": "0"},
                     folder_svg(GW, GH, lines=RAG[i], sw=4.4)))
        H.append(div(f"b2-t{i}", "", {"left": f"{x + 14}px",
                                      "top": f"{gy + 6}px",
                                      "width": f"{TAGW[i]}px", "height": "11px",
                                      "background": TERRA,
                                      "border-radius": "5.5px",
                                      "opacity": "0"}))
        app(f"#b2-f{i}", CUE["folders"] + 0.10 * i, 0.44,
            "opacity:0,y:52,scale:0.92", "opacity:1,y:0,scale:1")
        draw(f"#b2-f{i} .fbody", CUE["folders"] + 0.10 * i + 0.04, 0.50)
        set0(f"#b2-f{i} .frule", "opacity:0")
        tw(f'tl.to("#b2-f{i} .frule",{{opacity:1,duration:0.24,ease:{SOFT},'
           f'stagger:0.06}},{CUE["folders"] + 0.10 * i + 0.46:.2f});')
        app(f"#b2-t{i}", CUE["themes"] + 0.09 * i, 0.26,
            "opacity:0,scaleX:0.2", "opacity:1,scaleX:1")
    # the sheets tuck into the folders as they rise
    for sel in ("#b1-s1", "#b1-a", "#b1-b"):
        to(sel, CUE["folders"], 0.34, "opacity:0,scale:0.9")
    to("#b1-ld", CUE["folders"], 0.30, "opacity:0")

    # ======================================================= b3 — three intakes
    RW, RH = 260.0, 195.0
    RX, RY = (CORE_W - RW) / 2, DESK_Y - RH
    H.append(div("b3-r", "", {"left": f"{RX}px", "top": f"{RY}px",
                              "width": f"{RW}px", "height": f"{RH}px",
                              "opacity": "0"},
                 folder_svg(RW, RH, lines=(0.90, 0.62, 0.78), sw=5.0)))
    for i in range(4):
        H.append(div(f"b3-fill{i}", "", {
            "left": f"{RX + RW * 0.14:.1f}px",
            "top": f"{RY + RH * 0.50 + i * 22:.1f}px",
            "width": f"{RW * 0.72 * (0.9 - 0.12 * i):.1f}px", "height": "11px",
            "background": TERRA, "border-radius": "5.5px", "opacity": "0"}))

    NS = 142.0
    LBL_H = 38.0
    nodes = [
        ("on", 96.0, 60.0, globe_svg(NS), "ONLINE", CUE["online"],
         (96.0 + NS / 2 + 10, 60.0 + NS + LBL_H + 14), (RX, RY + 46)),
        ("dp", (CORE_W - NS) / 2, 40.0, depth_svg(NS), "DEEP", CUE["deep"],
         (CORE_W / 2, 40.0 + NS + LBL_H + 14), (CORE_W / 2, RY)),
        ("lo", CORE_W - 96.0 - NS, 60.0, laptop_svg(NS), "LOCAL", CUE["local"],
         (CORE_W - 96.0 - NS / 2 - 10, 60.0 + NS + LBL_H + 14),
         (RX + RW, RY + 46)),
    ]
    for key, nx, ny, glyph, name, cue, a, b in nodes:
        H.append(div(f"b3-n{key}", "", {"left": f"{nx:.1f}px", "top": f"{ny}px",
                                        "width": f"{NS}px", "height": f"{NS}px",
                                        "opacity": "0"}, glyph))
        H.append(label(f"b3-l{key}", nx - 40, ny + NS + 6, NS + 80, name,
                       size=28.0, color=MUTE, ls=4.0, opacity=0))
        H.append(stem(f"b3-s{key}", a[0], a[1], b[0], b[1]))
        app(f"#b3-n{key}", cue, 0.40, "opacity:0,scale:0.86,y:-22",
            "opacity:1,scale:1,y:0")
        app(f"#b3-l{key}", cue + 0.24, 0.28, "opacity:0,y:10", "opacity:1,y:0")
        # the stem draws AFTER its node exists — never before (BUILD ORDER)
        draw(f"#b3-s{key} .sline", cue + 0.44, 0.34)
        app(f"#b3-s{key} .shead", cue + 0.72, 0.16, "opacity:0", "opacity:1")

    app("#b3-r", CUE["whether"], 0.44, "opacity:0,scale:0.93",
        "opacity:1,scale:1")
    draw("#b3-r .fbody", CUE["whether"] + 0.04, 0.56)
    set0("#b3-r .frule", "opacity:0")
    tw(f'tl.to("#b3-r .frule",{{opacity:1,duration:0.24,ease:{SOFT},'
       f'stagger:0.07}},{CUE["whether"] + 0.52:.2f});')
    for i, x in enumerate(gx):
        to(f"#b2-f{i}", CUE["whether"], 0.34, "opacity:0")
        to(f"#b2-t{i}", CUE["whether"], 0.30, "opacity:0")
    # `computer` — the laptop's own screen answers, so the node is not inert:
    # its terracotta line extends. An event, then a hold (Law 1).
    set0("#b3-nlo .lscreen", "scaleX:0.34")
    to("#b3-nlo .lscreen", CUE["computer"], 0.34, "scaleX:1")

    # ============================================================ b4 — payoff
    for i in range(4):
        app(f"#b3-fill{i}", CUE["dedicated"] + 0.12 * i, 0.30,
            "opacity:0,scaleX:0.12", "opacity:1,scaleX:1")
    for key, *_ in nodes:
        to(f"#b3-s{key} .sline", CUE["dedicated"] + 0.34, 0.30,
           "strokeDashoffset:100")
        to(f"#b3-s{key} .shead", CUE["dedicated"] + 0.34, 0.20, "opacity:0")
        to(f"#b3-n{key}", CUE["dedicated"] + 0.46, 0.34, "opacity:0,scale:0.9")
        to(f"#b3-l{key}", CUE["dedicated"] + 0.46, 0.28, "opacity:0")

    PW, PH = 200.0, 150.0
    px_ = (120.0, 400.0, 680.0)
    py = DESK_Y - PH
    marks = (logo["claude"], logo["perplexity"], logo["chatgpt"])
    for i, x in enumerate(px_):
        if i == 1:
            continue
        H.append(div(f"b4-p{i}", "", {"left": f"{x}px", "top": f"{py}px",
                                      "width": f"{PW}px", "height": f"{PH}px",
                                      "opacity": "0"},
                     folder_svg(PW, PH, mark=marks[i], sw=4.4)))
    H.append(div("b4-mark", "", {"left": f"{px_[1] + (PW - 68) / 2:.1f}px",
                                 "top": f"{py + 46:.1f}px", "width": "68px",
                                 "height": "68px", "opacity": "0"},
                 f'<img src="{marks[1]}" alt="" '
                 f'style="width:100%;height:100%;object-fit:contain">'))
    # the receiver shrinks into the row's centre seat, then its siblings arrive
    # centre (500, 372.5) -> the row's centre seat (500, 395)
    to("#b3-r", CUE["anyother"], 0.52,
       f"x:0,y:{(py + PH / 2) - (RY + RH / 2):.1f},scale:{PW / RW:.4f}")
    for i in range(4):
        to(f"#b3-fill{i}", CUE["anyother"], 0.26, "opacity:0")
    to("#b3-r .frule", CUE["anyother"] + 0.30, 0.24, "opacity:0")
    app("#b4-mark", CUE["anyother"] + 0.40, 0.30, "opacity:0,scale:0.8",
        "opacity:1,scale:1")
    app("#b4-p0", CUE["anyother"] + 0.30, 0.46, "opacity:0,x:-90,scale:0.92",
        "opacity:1,x:0,scale:1")
    app("#b4-p2", CUE["anyother"] + 0.38, 0.46, "opacity:0,x:90,scale:0.92",
        "opacity:1,x:0,scale:1")
    for i in (0, 2):
        draw(f"#b4-p{i} .fbody", CUE["anyother"] + 0.30 + 0.08 * (i // 2), 0.44)

    # ============================================================ outro
    H.append(div("o-rule", "", {"left": f"{CORE_W / 2 - 92:.1f}px",
                                "top": "372px", "width": "184px",
                                "height": "7px", "background": TERRA,
                                "border-radius": "3.5px", "opacity": "0"}))
    H.append(div("o-slot", "", {"left": "0px", "top": "410px",
                                "width": f"{CORE_W}px", "height": "142px",
                                "opacity": "0"}, lockup))
    OU = CUE["outro"]
    # the shelf lifts into a small centred row: the outro is ONE composition
    # the shelf: three 120x90 folders centred at (380,187) (500,187) (620,187)
    SHELF_Y = 187.0
    to("#b3-r", OU, 0.60,
       f"x:0,y:{SHELF_Y - (RY + RH / 2):.1f},scale:{(PW * 0.60) / RW:.4f}")
    to("#b4-p0", OU, 0.60,
       f"x:{380.0 - (px_[0] + PW / 2):.1f},y:{SHELF_Y - (py + PH / 2):.1f},"
       f"scale:0.60")
    to("#b4-p2", OU, 0.60,
       f"x:{620.0 - (px_[2] + PW / 2):.1f},y:{SHELF_Y - (py + PH / 2):.1f},"
       f"scale:0.60")
    to("#b4-mark", OU, 0.60, f"x:0,y:{SHELF_Y - (py + 46 + 34):.1f},scale:0.60")
    to("#b1-desk", OU, 0.44, "opacity:0")
    to("#b1-deskr", OU, 0.44, "opacity:0")
    for sel in ("#b3-r", "#b4-p0", "#b4-p2", "#b4-mark"):
        to(sel, OU + 0.60, 0.40, "opacity:0.30")
    app("#o-rule", OU + 0.34, 0.42, "opacity:0,scaleX:0.3",
        "opacity:1,scaleX:1")
    app("#o-slot", OU + 0.44, 0.44, "opacity:0,y:16", "opacity:1,y:0")

    return "\n".join(H), T


# the outro lockup is placed by each FORMAT (it owns its own outro geometry and
# its own handle), but every format seats it inside `#o-slot` so the three
# renders differ in exactly one string.
OUTRO_SLOT_TOP = 410.0
