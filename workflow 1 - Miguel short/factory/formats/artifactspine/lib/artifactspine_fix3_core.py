"""ARTIFACT SPINE — FIX ROUND 3 shared geometry.  GLOBAL LAW 12.

Authority: `references/laws/REVIEW_2026-08-30.md` ROUND 3 — Morgane's review, Miguel's
rulings, and THE CALCULATION (S26 Ultra screenshots of TikTok / YouTube Shorts /
IG Reels).

    12. CAPTION SAFE BAND + UI SAFE ZONES.  Caption pill BOTTOM edge at or above
        72 % of frame height (y <= 1382 at 1920).  Caption position STABLE across
        a video's modes.  No meaningful content in the bottom 28 %, the right
        15 % column (x > 918) between y 30-95 %, or the top 10 %.  The outro
        @handle chip is exempt.

Both round-2 artifact-spine cuts failed it: `artifactspine_fix` (APPROVED on
content) sat at 87-92 %, `artifactspine_zoom_fix2` at ~92 %.  Measured on
`Fixed/artifactspine_fix.mp4`: the terracotta pill runs y 1663 -> 1776, i.e.
**bottom 92.5 %** — under TikTok's creator block (75 %) and under Reels'
description (92 %).  Morgane is right; it is unreadable on all three platforms.

WHAT ROUND 3 CHANGES, AND ONLY THIS
-----------------------------------
**One safe window, shared by both variants and by every mode.**

    caption pill centre      y = 1292      (pill 115 px tall -> bottom 1349.5)
    caption pill bottom      70.3 % of frame height          (law: <= 72 %)
    the ONE WINDOW rect      x 40..912   y 192..1210.5
    right-most artifact px   x = 889 (scroll) / 869 (zoom)   (law: <= 918)
    top-most artifact px     y = 215 (scroll) / 232 (zoom)   (law: >= 192)
    bottom-most artifact px  y = 1208 (scroll) / 1170 (zoom) (law: <= 1382)

The window had to lose 128 px of width (the right 15 % is the platform
engagement rail) and 482 px of height (the caption has to live above it), so the
artifact is presented through a SCALE rather than redesigned: the document, the
panel header and the whole seven-region composition are authored at exactly the
geometry Miguel approved and painted through one `transform: scale()`.

That is the point.  Pacing, the no-peek-ahead solver, the two face switch-ins,
the SFX cues, the counter formatting, the round-fill law — every approved
decision survives byte-for-byte, because the composition is unchanged and only
its presentation rect moved.

**The face gets WIDER, for free.**  `face_std_25` in the old 1000x1516 window
was `object-fit:cover` scaled 1.123x -> head_frac 0.435.  The same plate in the
new 872x1018 window scales 0.807x -> **head_frac 0.313**.  Miguel's round-1
Global Law 1 ("you zoom in way too much") and his round-3 ruling (full-face is
the RAW 0 % crop, no punches, no virtual set) are both satisfied without
touching the asset: we are now 45 % wider than the 0 % ceiling, not tighter.
Verified frame-by-frame — cap top clears the window by ~80 px, chin by ~239 px,
shoulders are in shot for the first time in this format.
"""
from __future__ import annotations

import artifactspine_core as C
import artifactspine_fix_core as X       # noqa: F401  (re-exported for the gens)

# ---- LAW 12, as numbers ------------------------------------------------------
FRAME_W, FRAME_H = 1080.0, 1920.0
TOP_ZONE = 0.10 * FRAME_H               # 192   — nothing meaningful above this
BOTTOM_ZONE = 0.72 * FRAME_H            # 1382.4 — nothing meaningful below this
RAIL_X = 0.85 * FRAME_W                 # 918   — the engagement rail column
RAIL_Y0, RAIL_Y1 = 0.30 * FRAME_H, 0.95 * FRAME_H

# The pill is 112-114 px tall across the whole caption set (measured on the
# rendered round-2 file at t=12 and t=20; `cap_font` caps at 56 px and the
# `.scappill` box is font-size * 1.357 + 2 * 19 px of padding).  115 is that
# maximum with a pixel of safety, and every number below is derived from it.
PILL_H = 115.0
CAP_Y = 1292.0                          # pill centre -> bottom 1349.5 (70.3 %)
CAP_GAP = 24.0                          # air between the window and the pill

WIN_X = 40.0
WIN_Y = 192.0                           # the window EDGE is the 10 % line
WIN_W = 872.0                           # right edge 912 < 918
WIN_H = (CAP_Y - PILL_H / 2 - CAP_GAP) - WIN_Y          # 1034.5

LEAD_MIN = 46.0     # virtual px of air above/below the TALLEST region at rest

# ---- LAW 12, the caption's WIDTH ---------------------------------------------
# The pill is centred on x=540, so the rail column also caps how wide it may get.
# Round 2's `cap_font` sized to 907 px of ink (pill up to 975 px, x 52..1028) and
# 15 of the 52 captions crossed x=918 — i.e. the tail of every long line sat
# under the like / comment / share icons on all three platforms.
#
# The ink constant is CALIBRATED ON RENDERED PIXELS, not guessed.  Measured
# pills give ink/(len*fs) = 0.437 ("and context is finite.") .. 0.556 ("Hermes
# Agent managed to" — wide caps, no descenders).  A first pass at 0.530 shipped
# one pill to x=931 and was caught by the 52-frame sweep; 0.600 is the measured
# worst case plus 8 %, and every one of the 52 captions then lands inside 918.
CAP_MAX_X = 918.0
CAP_PAD = 34.0                                   # .scappill horizontal padding
CAP_INK_MAX = 2 * (CAP_MAX_X - 540.0) - 2 * CAP_PAD      # 688 px of ink
CAP_ADV = 0.600                                  # ink per (char * font-size)
CAP_FS_MIN, CAP_FS_MAX = 32.0, 56.0


def cap_font(text: str) -> float:
    n = max(1, len(text))
    return round(max(CAP_FS_MIN, min(CAP_FS_MAX, CAP_INK_MAX / (CAP_ADV * n))), 1)


class Geom:
    """The solved presentation of an unchanged composition."""

    def __init__(self) -> None:
        heights = [C.REGIONS[k](0.0, 0.0, C.DOC_W)[1] for k in range(len(C.REGIONS))]
        self.heights = heights
        self.virt_view_h = max(heights) + 2 * LEAD_MIN       # 1220.0
        self.vh = C.HEAD_H + self.virt_view_h                # 1416.0
        self.s = WIN_H / self.vh                             # 0.7306
        self.vw = WIN_W / self.s                             # 1193.6
        self.doc_w = self.vw - 2 * C.PAD

    def report(self) -> list[str]:
        return [
            f"     LAW 12  window {WIN_X:.0f},{WIN_Y:.0f} {WIN_W:.0f}x{WIN_H:.1f}"
            f"  -> right {WIN_X + WIN_W:.0f} (<{RAIL_X:.0f})"
            f"  bottom {WIN_Y + WIN_H:.1f} (<{BOTTOM_ZONE:.0f})",
            f"     LAW 12  caption pill centre {CAP_Y:.0f}  bottom "
            f"{CAP_Y + PILL_H / 2:.1f} = {100 * (CAP_Y + PILL_H / 2) / FRAME_H:.1f} % "
            f"(law <= 72.0 %)",
            f"     scale   s={self.s:.5f}  virtual panel {self.vw:.1f}x{self.vh:.1f}"
            f"  viewport {self.virt_view_h:.0f}  doc_w {self.doc_w:.1f}",
        ]


def apply_geometry() -> Geom:
    """Repoint the inherited core at the safe window.  Every builder reads these
    module globals at CALL time, so the seven regions, the header, the face
    window, the outro lockup and the caption clips all move together."""
    C.measure_marks()
    g = Geom()
    C.WIN_X, C.WIN_Y, C.WIN_W, C.WIN_H = WIN_X, WIN_Y, WIN_W, WIN_H
    C.VIEW_Y = WIN_Y + C.HEAD_H
    C.VIEW_H = g.virt_view_h            # the VIRTUAL viewport the doc is laid in
    C.DOC_W = g.doc_w                   # the VIRTUAL document width
    C.CAP_Y = CAP_Y
    C.cap_font = cap_font               # LAW 12: the pill stays out of the rail
    return g


def panel_html(dur: float, g: Geom, parts: list[str], doc_top: float,
               doc_h: float) -> str:
    """The ONE WINDOW, with the approved composition painted through one scale.

    `#pscale` is the only new element in the whole build.  Everything inside it
    is authored in the coordinates Miguel approved; GSAP tweens on its children
    are in those same coordinates, so no tween, no fill geometry and no ring
    rect needed a single number changed."""
    return (
        f'  <div class="clip" id="panel" data-start="0" data-duration="{dur:.3f}" '
        f'data-track-index="10" style="left:{C.n(WIN_X)}px;top:{C.n(WIN_Y)}px;'
        f'width:{C.n(WIN_W)}px;height:{C.n(WIN_H)}px;background:{C.WHITE};'
        f'border:2px solid {C.LINE};border-radius:{C.n(C.WIN_R)}px;overflow:hidden;'
        f'box-shadow:0 26px 64px rgba(20,20,22,0.13)">\n'
        f'  <div class="abs" id="pscale" style="left:0;top:0;width:{C.n(g.vw)}px;'
        f'height:{C.n(g.vh)}px;transform:scale({g.s:.6f});transform-origin:0 0">\n'
        + C.header_html(0.0, 0.0, g.vw) + "\n"
        + f'  <div class="abs" id="viewport" style="left:0;top:{C.n(C.HEAD_H)}px;'
          f'width:{C.n(g.vw)}px;height:{C.n(g.virt_view_h)}px;overflow:hidden">'
        + f'<div class="abs" id="doc" style="left:{C.n(C.PAD)}px;top:{C.n(doc_top)}px;'
          f'width:{C.n(g.doc_w)}px;height:{C.n(doc_h)}px">'
        + "\n".join(parts)
        + '</div><div id="viewfade-t"></div><div id="viewfade-b"></div>'
        + "</div>\n  </div>\n  </div>"
    )


def law12_report(*, content_left: float, content_right: float,
                 content_top: float, content_bottom: float) -> list[str]:
    """Fail the build if any artifact ink lands in a platform UI zone."""
    bad = []
    if content_right > RAIL_X:
        bad.append(f"RIGHT RAIL: content reaches x={content_right:.0f} (> {RAIL_X:.0f})")
    if content_bottom > BOTTOM_ZONE:
        bad.append(f"BOTTOM 28%: content reaches y={content_bottom:.0f} "
                   f"(> {BOTTOM_ZONE:.0f})")
    if content_top < TOP_ZONE:
        bad.append(f"TOP 10%: content reaches y={content_top:.0f} (< {TOP_ZONE:.0f})")
    if CAP_Y + PILL_H / 2 > BOTTOM_ZONE:
        bad.append(f"CAPTION: pill bottom {CAP_Y + PILL_H / 2:.0f} > {BOTTOM_ZONE:.0f}")
    if bad:
        raise SystemExit("[law12] failed:\n  " + "\n  ".join(bad))
    return [f"     LAW 12  artifact ink x {content_left:.0f}..{content_right:.0f} "
            f"(rail {RAIL_X:.0f})   y {content_top:.0f}..{content_bottom:.0f} "
            f"(top {TOP_ZONE:.0f}, bottom {BOTTOM_ZONE:.0f})  OK"]
