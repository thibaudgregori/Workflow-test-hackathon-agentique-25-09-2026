"""ARTIFACT SPINE — FIX ROUND 3, the scroll variant.  `artifactspine_fix3.mp4`.

Round-2 verdict on `Fixed/artifactspine_fix.mp4`: **APPROVED** ("nice!").
Round-3 measurement on the same file: the caption pill runs y 1663..1776, i.e.
**bottom at 92.5 % of frame height** — buried under TikTok's creator block,
Shorts' title row and Reels' description.  Morgane flagged it; the S26 Ultra
screenshots confirmed it; Global Law 12 now forbids it.

THIS BUILD CHANGES EXACTLY ONE THING: WHERE THE PIECE IS PAINTED.

    caption pill centre   1720 -> 1292        bottom 92.5 % -> 70.3 %
    the ONE WINDOW        40,84 1000x1516  -> 40,176 872x1034.5
    artifact ink          x .. 1008, y 116..1600  ->  x .. 898, y 201..1208

The document itself is untouched.  Its seven regions, their heights, the centred
rest positions, the solved no-peek-ahead gaps, the 30 state tweens, the two face
switch-ins at 13.12 and 38.92, both hidden moves, all ten SFX cues and every
pacing guard are byte-for-byte the approved build — they are simply authored at
the approved geometry inside `#pscale` and painted through a single
`transform: scale(0.7306)`.  Nothing was redesigned to fit; the presentation
rect moved and the composition came with it.

Consequences worth naming:

* **The face got wider, not tighter.**  `face_std_25` cover-fitted the old
  1000x1516 window at 1.123x (head_frac 0.435).  The same plate in 872x1034.5
  fits at 0.807x -> **head_frac 0.313**, with the cap clearing the top by ~80 px
  and shoulders in frame.  That is Global Law 1 and Miguel's round-3 "no zooms,
  full-face is the RAW 0 % crop" ruling honoured by geometry rather than by a
  new asset.
* **Travel got shorter.**  The uniform 1328 px spine move becomes ~970 px on
  screen (1328 virtual x 0.7306), so the one thing Miguel said still went a
  little fast is now slower in screen pixels at the identical timing.
* **The right 15 % is empty.**  The old panel reached x=1008 and put the READY /
  LOADED chips of all eight registry rows directly under the like / comment /
  share rail.  Artifact ink now stops at x=898.

Usage:  ~/Documents/Workspace/.venv/bin/python artifactspine_fix3_gen.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import artifactspine_core as C            # noqa: E402
import artifactspine_fix_core as X        # noqa: E402
import artifactspine_fix3_core as L       # noqa: E402

VAR = "fix3"

# ---- the schedule — APPROVED, untouched --------------------------------------
CUT_IN = 2.84            # pause 2.80-3.14, after "literally infinite tools."
CUT_OUT = 50.20          # pause 50.10-50.74, after "unbelievable."
RETURNS = [(13.12, 15.12), (38.92, 40.56)]
ARRIVE = [CUT_IN, 8.84, 14.30, 20.00, 24.56, 29.70, 39.30]
HIDDEN_MOVES = {2, 6}


def build() -> str:
    g = L.apply_geometry()
    words, dur, a = X.load_timing()
    lay = X.layout_scroll()
    parts, tops, stops = lay["parts"], lay["tops"], lay["stops"]
    heights, doc_top, doc_h = lay["heights"], lay["doc_top"], lay["doc_h"]

    arrive = [X.q(t) for t in ARRIVE]
    for k in range(1, len(arrive)):
        if arrive[k] <= arrive[k - 1] + 0.8:
            raise SystemExit(f"scroll moves too close: {arrive}")
    for k in HIDDEN_MOVES:
        t0, t1 = next((r for r in RETURNS
                       if r[0] <= arrive[k] and arrive[k] + X.MOVE_D <= r[1]), (0, 0))
        if not t1:
            raise SystemExit(f"move {k} at {arrive[k]} is not covered by a face return")

    tw: list[str] = []
    X.state_tweens(a, arrive, tw, intro_rows=True)
    X.header_tweens(a, tw, hd_w=g.vw, cut_in=CUT_IN)

    # THE SPINE: discrete, word-synced, then still.  Virtual px; `#pscale` turns
    # each one into ~970 screen px.
    tw.append('tl.set("#doc",{y:0},0);')
    for k in range(1, len(stops)):
        tw.append(f'tl.to("#doc",{{y:{-stops[k]:.1f},duration:{X.MOVE_D},ease:GLIDE}},'
                  f'{arrive[k]:.2f});')

    # the face window — one element, opacity-switched, never out of sync
    tw.append(f'tl.set("#facewin",{{opacity:0}},{X.q(CUT_IN):.2f});')
    for t0, t1 in RETURNS:
        tw.append(f'tl.set("#facewin",{{opacity:1}},{X.q(t0):.2f});')
        tw.append(f'tl.set("#facewin",{{opacity:0}},{X.q(t1):.2f});')
    tw.append(f'tl.set("#facewin",{{opacity:1}},{X.q(CUT_OUT):.2f});')
    X.outro_tweens(tw, CUT_OUT, a)

    # ---- SFX v2 — rationed, class-pinned, frame-locked (approved set) --------
    cues: list[tuple[float, str]] = [
        (X.q(CUT_IN), "soft_whoosh"),
        (X.q(a["dont"]), "low_thump"),
        (X.q(a["disclosure"] + 0.60), "tick"),
        (X.q(RETURNS[0][0]), "reverse_air"),
        (X.q(RETURNS[0][1]), "soft_whoosh"),
        (X.q(a["finiteword"]), "low_thump"),
        (X.q(a["everneed"] + 1.58), "pop"),
        (X.q(RETURNS[1][0]), "reverse_air"),
        (X.q(RETURNS[1][1]), "soft_whoosh"),
        (X.q(CUT_OUT), "reverse_air"),
    ]
    cues += [(arrive[k], "page_turn") for k in range(1, len(arrive))
             if k not in HIDDEN_MOVES]
    audio, atw = X.audio_block(dur, cues)
    tw += atw

    X.audit(tw,
            moves=[(arrive[k], X.MOVE_D) for k in range(1, len(arrive))
                   if k not in HIDDEN_MOVES],
            cuts=[X.q(CUT_IN)] + [X.q(t) for r in RETURNS for t in r] + [X.q(CUT_OUT)],
            label=VAR)

    # ---- LAW 12 — the artifact's ink, in FRAME pixels ------------------------
    # `#pscale` sits inside the panel's 2 px border, so frame_x = WIN_X + 2 + s*vx.
    def fx(vx: float) -> float:
        return L.WIN_X + 2.0 + g.s * vx

    def fy(vy: float) -> float:
        return L.WIN_Y + 2.0 + g.s * vy

    ink_l = fx(C.PAD - 10.0)                       # the r*-ring gutter
    ink_r = fx(C.PAD + g.doc_w + 10.0)
    ink_t = fy(32.0)                               # hd-chip, the topmost element
    ink_b = min(fy(g.vh), L.WIN_Y + L.WIN_H - 2.0)  # the viewport's clipped floor
    law = L.law12_report(content_left=ink_l, content_right=ink_r,
                         content_top=ink_t, content_bottom=ink_b)

    body = "\n".join([L.panel_html(dur, g, parts, doc_top, doc_h),
                      X.face_html(dur),
                      C.caption_clips(C.build_captions(words), dur), audio])
    page = C.page("Hermes infinite tools — ARTIFACT SPINE (fix round 3)", body, tw, dur)

    print(f"{VAR}: dur={dur:.3f} @ {X.FPS}fps  doc_h={doc_h:.0f}"
          f"  virt_view={g.virt_view_h:.0f}  doc_top={doc_top:.0f}")
    print("\n".join(g.report()))
    print("\n".join(law))
    print(f"     heights   {[round(h) for h in heights]}")
    print(f"     leads     {[round(v) for v in lay['leads']]}")
    print(f"     gaps      {[round(v) for v in lay['gaps']]}")
    print(f"     travel    virtual "
          f"{[round(stops[k] - stops[k - 1]) for k in range(1, 7)]}")
    print(f"               screen  "
          f"{[round((stops[k] - stops[k - 1]) * g.s) for k in range(1, 7)]}")
    print(f"     arrivals  {arrive}  hidden={sorted(HIDDEN_MOVES)}")
    for k in range(6):
        print(f"     peek 0{k + 1}->0{k + 2}: "
              f"{max(0.0, (tops[k] - lay['leads'][k] + g.virt_view_h) - tops[k + 1]):.0f}px  "
              f"bleed-back: "
              f"{max(0.0, (tops[k] + heights[k]) - (tops[k + 1] - lay['leads'][k + 1])):.0f}px")
    return page


if __name__ == "__main__":
    project = C.OUT_ROOT / VAR
    X.bind_assets(project)
    (project / "index.html").write_text(build(), encoding="utf-8")
    print(f"project={project}")
