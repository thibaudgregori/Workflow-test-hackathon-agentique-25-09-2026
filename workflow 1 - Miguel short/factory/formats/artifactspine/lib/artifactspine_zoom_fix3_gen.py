"""ARTIFACT SPINE — FIX ROUND 3, the ZOOM variant.  `artifactspine_zoom_fix3.mp4`.

Round-2 built the uniform-card board (`CARD_W = 1000` for all eight cards, one
camera framing, 40 px margins at every stop, Law 11 pill fills).  Round 3 keeps
every one of those decisions and moves the whole thing into the Law 12 safe
window.

WHAT ROUND 3 CHANGES
--------------------
**1. THE CAPTION.**  1720 -> 1292, i.e. pill bottom 92 % -> 70.2 %, identical to
   the scroll variant.  Same pill, same y, on both cuts and in both modes
   (artifact and face) — Morgane's "not a fan of the captions drastically
   changing position" applies across a format, not just within a cut.

**2. THE FRAME IS THE SAFE WINDOW, NOT THE CANVAS.**  The camera stage was
   1080x1660 at the top of the canvas, so a 1000 px card painted x 40..1040 —
   240 px of every card, at every stop, sat under the platform's like / comment /
   share rail (x > 918, y 30-95 %).  The stage is now the same 872x1034.5 rect
   the face window uses:

       stage      x 40..912   y 176..1210.5      (was 0..1080 x 0..1660)
       card ink   x 84..869   y 216..1170        at EVERY card stop
       rail       x > 918                        empty for the whole video
       margins    43.5 px horizontal, >= 40 px vertical

**3. ONE SCALE FOR EVERY CARD STOP — the round-2 law, now exact.**  Round 2 fit
   each subject independently and capped at 1.0, so a 1216 px card and a 776 px
   card both painted 1000 px wide only because both were width-bound.  In the
   smaller frame the tallest card would have been height-bound and painted 9 px
   narrower than its neighbours — the exact defect Miguel flagged ("the Hermes
   Agent card is WIDER than the other cards"), re-introduced by the new rect.
   So the scale is solved ONCE for the whole board,

       S_UNI = min(FIT_W / CARD_W, FIT_H / max_card_h)

   and every card stop uses it.  All eight cards now paint at literally the same
   width in literally the same place, by construction rather than by luck.  Only
   the two establishing wides fit their own subject.

**4. THE GAP SOLVER LEARNED THE SCALE.**  Round 2's packing assumed scale 1
   (`STAGE_H/2 + CLEAR - h/2`).  At S_UNI the frame shows 1318 px of board, not
   1034, so the minimum gap is derived in BOARD units from the real visible
   window.  `_guard_margins` re-checks all ten stops on the emitted geometry.

KEPT: pacing, the veil that kills peek-ahead, the two face switch-ins and their
hidden column jumps, the two motivated non-arrival moves, the rounded counter
formatting, Law 11 fills, 25 fps, SFX v2.

Usage:  ~/Documents/Workspace/.venv/bin/python artifactspine_zoom_fix3_gen.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import artifactspine_core as C            # noqa: E402
import artifactspine_fix_core as X        # noqa: E402
import artifactspine_fix3_core as L       # noqa: E402

VAR = "zoom_fix3"

# ---- schedule (unchanged — round 1's pacing was approved) --------------------
CUT_IN = 2.84
CUT_OUT = 50.20
RETURNS = [(13.12, 15.12), (38.92, 40.56)]
ARRIVE = [3.32, 8.84, 14.20, 20.00, 24.56, 29.68, 39.28]
HIDDEN_MOVES = {2, 6}
CAM_D = 0.72
PUNCH_D = 0.90

# ---- the frame — LAW 12's safe window, shared with the face -----------------
STAGE_W, STAGE_H = L.WIN_W, L.WIN_H                # 872 x 1034.5
FRAME_CX, FRAME_CY = STAGE_W / 2, STAGE_H / 2
MARGIN = 40.0          # LAW: nothing is ever closer than this to the frame edge
CLEAR = 40.0           # LAW: a non-subject element is this far OUTSIDE the frame
FIT_W = STAGE_W - 2 * MARGIN      # 792
FIT_H = STAGE_H - 2 * MARGIN      # 954.5

# ---- the board ---------------------------------------------------------------
CARD_W = 1000.0        # THE law: one width, every card, header included
CARD_PAD = 44.0
TOP_CARD_H = 380.0
BOARD_PAD = 40.0       # board edge -> outermost element
BOARD_PAD_Y = 90.0
RAIL_X, RAIL_W, RAIL_H, RAIL_GAP = 40.0, 280.0, 104.0, 14.0
GUTTER = 120.0         # rail -> column A, and column -> column
BREATH = 40.0          # comfort on top of the solved minimum gap
COL_X = [RAIL_X + RAIL_W + GUTTER,
         RAIL_X + RAIL_W + GUTTER + CARD_W + GUTTER,
         RAIL_X + RAIL_W + GUTTER + 2 * (CARD_W + GUTTER)]
BOARD_W = COL_X[2] + CARD_W + BOARD_PAD

RAIL_LABELS = ["REGISTRY", "DISCLOSURE", "THIS TURN", "CONTEXT", "ACCESS",
               "NOUS", "SERVERS"]
# Reading order, top to bottom then left to right — "T" is the header card.
# The column breaks sit exactly where the face returns are, so both long
# diagonals happen behind Miguel's face and every VISIBLE move is a short
# vertical step.
COLUMNS: list[list] = [["T", 0, 1], [2, 3, 4, 5], [6]]


# =============================================================================
# LAW 11 — the context meter is a pill, and nothing floats at the end of a track
# =============================================================================
_STOP_RE = re.compile(r'<div class="abs" id="r4-stop".*?</div>', re.S)
_SEG_RE = re.compile(r'(id="r4-sg([012])"[^>]*?width:)(\d+(?:\.\d+)?)(px)')


def patch_region4(html: str) -> str:
    """Delete the detached end marker; close the stacked bar's 2 px seams."""
    out, n = _STOP_RE.subn("", html)
    if n != 1:
        raise SystemExit(f"r4-stop guard stale: matched {n} times")
    out, m = _SEG_RE.subn(lambda g: f"{g.group(1)}{C.n(float(g.group(3)) + 2)}{g.group(4)}",
                          out)
    if m != 3:
        raise SystemExit(f"r4 segment guard stale: matched {m} of 3")
    return out


def patch_r4_stop_tween(tw: list[str]) -> None:
    """The "finite." beat, without a floating tick: the vessel goes hard."""
    hits = [i for i, s in enumerate(tw) if '"#r4-stop"' in s]
    if len(hits) != 1:
        raise SystemExit(f"r4-stop tween guard stale: {len(hits)} hits")
    t = re.findall(r",(\d+\.\d+)\);\s*$", tw[hits[0]])
    if not t:
        raise SystemExit("could not read the r4-stop tween time")
    tw[hits[0]] = (f'tl.to("#r4-card",{{borderColor:"{C.rgb(C.INK)}",duration:0.32,'
                   f'ease:SOFT}},{float(t[0]):.2f});')


# =============================================================================
# THE CAMERA — one framing law, and now one SCALE for every card stop
# =============================================================================
def fit_scale(rect: tuple[float, float, float, float]) -> float:
    _rx, _ry, rw, rh = rect
    return min(FIT_W / rw, FIT_H / rh, 1.0)


def cam(rect: tuple[float, float, float, float], s: float) -> tuple[float, float, float]:
    rx, ry, rw, rh = rect
    return (round(s, 5), round(FRAME_CX - s * (rx + rw / 2), 1),
            round(FRAME_CY - s * (ry + rh / 2), 1))


def move(tw: list[str], t: float, rect, s: float, *, d: float = CAM_D):
    sc, x, y = cam(rect, s)
    tw.append(f'tl.to("#board",{{scale:{sc},x:{x},y:{y},duration:{d},ease:GLIDE}},'
              f'{X.q(t):.2f});')
    return sc, x, y


def _screen(rect, stop, s) -> tuple[float, float, float, float]:
    _s, ox, oy = cam(stop, s)
    rx, ry, rw, rh = rect
    return (s * rx + ox, s * ry + oy, s * (rx + rw) + ox, s * (ry + rh) + oy)


def _guard_margins(stops: list[tuple[str, tuple, float]],
                   elements: list[tuple[str, tuple]],
                   wide_stops: set[str]) -> list[str]:
    """MIGUEL'S LAW, EXECUTABLE, inside LAW 12's window.  At every camera stop,
    every element is either fully inside the frame with >= MARGIN of air, or
    fully outside it with >= CLEAR.  Nothing is ever allowed to sit ON the edge,
    and — new in round 3 — the frame itself is the safe rect, so "inside the
    frame" now means "outside the platform's UI"."""
    report, bad = [], []
    widths = []
    for sname, srect, s in stops:
        inside_all = sname in wide_stops
        for ename, erect in elements:
            x0, y0, x1, y1 = _screen(erect, srect, s)
            focus = inside_all or ename == sname
            if focus:
                m = min(x0, y0, STAGE_W - x1, STAGE_H - y1)
                if m < MARGIN - 0.51:
                    bad.append(f"{sname}: {ename} only {m:.1f}px from the frame "
                               f"edge (need {MARGIN:.0f})")
                if ename == sname and not inside_all:
                    widths.append(round(x1 - x0, 2))
            else:
                hits = (x1 > -CLEAR and x0 < STAGE_W + CLEAR
                        and y1 > -CLEAR and y0 < STAGE_H + CLEAR)
                if hits:
                    bad.append(f"{sname}: {ename} intersects the frame "
                               f"(x {x0:.0f}..{x1:.0f}, y {y0:.0f}..{y1:.0f})")
        report.append(f"     stop {sname:<8} scale={s:.4f}  "
                      f"subject={'ALL' if inside_all else sname}")
    if len(set(widths)) > 1:
        bad.append(f"CARD WIDTH LAW: subjects paint at {sorted(set(widths))} px")
    if bad:
        raise SystemExit("[zoom_fix3] MARGIN LAW failed:\n  " + "\n  ".join(bad))
    report.append(f"     every card stop paints its subject at {widths[0]:.1f} px "
                  f"wide — one width, {(STAGE_W - widths[0]) / 2:.1f} px of air each side")
    return report


# =============================================================================
def build() -> str:
    g = L.apply_geometry()
    words, dur, a = X.load_timing()
    inner_w = CARD_W - 2 * CARD_PAD

    # ---- measure every card at the ONE width --------------------------------
    heights: dict[int, float] = {}
    for k, region in enumerate(C.REGIONS):
        _html, h = region(0.0, 0.0, inner_w)
        heights[k] = h + 2 * CARD_PAD
    card_h = {"T": TOP_CARD_H, **heights}

    # ---- ONE SCALE for every card stop --------------------------------------
    s_uni = min(FIT_W / CARD_W, FIT_H / max(card_h.values()))
    vis_w, vis_h = STAGE_W / s_uni, STAGE_H / s_uni      # the frame, in board px
    clear_b = CLEAR / s_uni                              # CLEAR, in board px

    # ---- solve the gaps so a neighbour is never in shot ----------------------
    def min_gap(hi: float, hj: float) -> float:
        return (vis_h / 2 + clear_b) - min(hi, hj) / 2

    col_h, col_gaps = [], []
    for col in COLUMNS:
        gaps = [min_gap(card_h[col[i]], card_h[col[i + 1]]) + BREATH
                for i in range(len(col) - 1)]
        col_gaps.append(gaps)
        col_h.append(sum(card_h[c] for c in col) + sum(gaps))
    band_h = max(col_h)
    board_h = band_h + 2 * BOARD_PAD_Y

    need_pitch = (vis_w / 2 + clear_b) + CARD_W / 2
    if CARD_W + GUTTER < need_pitch:
        raise SystemExit(f"column pitch {CARD_W + GUTTER} < {need_pitch:.0f}")
    if COL_X[0] - (RAIL_X + RAIL_W) < (vis_w / 2 + clear_b) - CARD_W / 2:
        raise SystemExit("rail gutter too small")

    # ---- lay the board out ---------------------------------------------------
    rects: dict[object, tuple[float, float, float, float]] = {}
    for ci, col in enumerate(COLUMNS):
        y = BOARD_PAD_Y + ((band_h - col_h[ci]) / 2 if len(col) == 1 else 0.0)
        for i, key in enumerate(col):
            rects[key] = (COL_X[ci], y, CARD_W, card_h[key])
            if i < len(col) - 1:
                y += card_h[key] + col_gaps[ci][i]

    parts: list[str] = []
    for idx in range(len(C.REGIONS)):
        cx, cy, cw, ch = rects[idx]
        html, _h = C.REGIONS[idx](cx + CARD_PAD, cy + CARD_PAD, inner_w)
        if idx == 1:
            if X.STEPS_LABEL_OLD not in html:
                raise SystemExit("region2 steps label moved — retitle guard stale")
            html = html.replace(X.STEPS_LABEL_OLD, X.STEPS_LABEL_NEW)
        if idx == 3:
            html = patch_region4(html)
        parts.append(C.card(f"bc{idx}", cx, cy, cw, ch, "", r=30.0,
                            shadow="0 20px 52px rgba(20,20,22,0.10)"))
        parts.append(f'<div class="abs" id="rgw{idx}" style="left:0;top:0;width:100%;'
                     f'height:100%;opacity:0">{html}</div>')

    # ---- the header card — same width, and it holds the title too ------------
    tx, ty, _tw_, th = rects["T"]
    top = [C.card("topcard", tx, ty, CARD_W, th, "", r=30.0,
                  shadow="0 20px 52px rgba(20,20,22,0.10)"),
           C.txt("bt-title", tx + C.PAD, ty + 30, CARD_W - 2 * C.PAD, "TOOL REGISTRY",
                 62.0),
           C.txt("bt-sub", tx + C.PAD, ty + 112, CARD_W - 2 * C.PAD,
                 "one panel · seven sections", 28.0, color=C.MUTED, weight=600,
                 mono=True, upper=False),
           C.hair("bt-hair", tx + C.PAD, ty + 162, CARD_W - 2 * C.PAD),
           C.header_html(tx, ty + 180, CARD_W)]

    rail_total = 7 * RAIL_H + 6 * RAIL_GAP
    rail_y0 = BOARD_PAD_Y                       # same top line as the columns
    rail = []
    for i, label in enumerate(RAIL_LABELS):
        y = rail_y0 + i * (RAIL_H + RAIL_GAP)
        rail.append(C.card(f"rl{i}", RAIL_X, y, RAIL_W, RAIL_H, "", bg=C.PAPER,
                           border="#EBE3D8", bw=1.5, r=20.0))
        rail.append(C.div(f"rl{i}-b", RAIL_X + 2, y + 2, 8.0, RAIL_H - 4,
                          f"background:{C.TERRA};border-radius:18px 0 0 18px;opacity:0;"))
        rail.append(C.txt(f"rl{i}-n", RAIL_X + 30, y + RAIL_H / 2 - 16, 60.0,
                          f"0{i + 1}", 24.0, color=C.MUTED, weight=700, ls=1.4,
                          mono=True))
        rail.append(C.txt(f"rl{i}-t", RAIL_X + 86, y + RAIL_H / 2 - 16, RAIL_W - 112,
                          label, 24.0, color=C.MUTED, weight=700, ls=1.4, mono=True))
    board_inner = "\n".join(top + rail + parts)

    # ---- the ten stops, and the law ------------------------------------------
    wide = (0.0, 0.0, BOARD_W, board_h)
    s_wide = fit_scale(wide)
    stops: list[tuple[str, tuple, float]] = [("wide", wide, s_wide),
                                             ("T", rects["T"], s_uni)]
    stops += [(f"bc{k}", rects[k], s_uni) for k in range(7)]
    elements: list[tuple[str, tuple]] = [("T", rects["T"])]
    elements += [(f"bc{k}", rects[k]) for k in range(7)]
    elements.append(("rail", (RAIL_X, rail_y0, RAIL_W, rail_total)))
    stop_report = _guard_margins(stops, elements, wide_stops={"wide"})

    # ---- schedule ------------------------------------------------------------
    arrive = [X.q(t) for t in ARRIVE]
    for k in HIDDEN_MOVES:
        if not any(t0 <= arrive[k] and arrive[k] + CAM_D <= t1 for t0, t1 in RETURNS):
            raise SystemExit(f"move {k} at {arrive[k]} is not covered by a face return")
    punch_t = X.q(a["bloating"] - 0.34)          # on "without" — up to the meter
    final_t = X.q(a["unbelievable"] + 0.42)      # on "just unbelievable"

    tw: list[str] = []
    X.state_tweens(a, arrive, tw, intro_rows=False)
    patch_r4_stop_tween(tw)
    X.header_tweens(a, tw, hd_w=CARD_W, cut_in=CUT_IN,
                    ring2=(punch_t + PUNCH_D + 0.06, final_t - 0.72))

    s0, x0, y0 = cam(wide, s_wide)
    tw.append(f'tl.set("#board",{{scale:{s0},x:{x0},y:{y0},transformOrigin:"0px 0px"}},0);')
    tw.append(C.settle("#topcard", X.q(CUT_IN + 0.02), 0.34, 0.90))
    for i in range(len(RAIL_LABELS)):
        tw.append(X.rise(f"#rl{i}", CUT_IN + 0.02 + i * 0.020, 0.24, 22.0))
        tw.append(X.rise(f"#rl{i}-n", CUT_IN + 0.02 + i * 0.020, 0.24, 22.0))
        tw.append(f'tl.set("#rl{i}-t",{{opacity:0}},0);')
    for j in range(7):
        tw.append(C.settle(f"#bc{j}", X.q(CUT_IN + 0.04 + j * 0.026), 0.26, 0.90))
    tw.append(X.rise("#bt-title", CUT_IN + 0.02, 0.30, 22.0))
    tw.append(X.rise("#bt-sub", CUT_IN + 0.08, 0.30, 22.0))
    tw.append(X.rise("#bt-hair", CUT_IN + 0.08, 0.30, 22.0))

    for k, t in enumerate(arrive):
        move(tw, t, rects[k], s_uni)
        tw.append(f'tl.to("#rgw{k}",{{opacity:1,duration:0.32,ease:SOFT}},{t:.2f});')
        lit = X.q(t + CAM_D + 0.04)
        tw.append(C.fade(f"#rl{k}-b", lit, 1.0, 0.26))
        tw.append(f'tl.to("#rl{k}",{{background:"{C.rgb(C.WHITE)}",borderColor:'
                  f'"{C.rgb(C.TERRA)}",duration:0.28,ease:SOFT}},{lit:.2f});')
        for sel in (f"#rl{k}-n", f"#rl{k}-t"):
            tw.append(f'tl.to("{sel}",{{opacity:1,color:"{C.rgb(C.INK)}",duration:0.28,'
                      f'ease:SOFT}},{lit:.2f});')
        if k:
            tw.append(C.fade(f"#rl{k - 1}-b", lit, 0.0, 0.24))
            tw.append(f'tl.set("#rl{k - 1}-b",{{opacity:0}},{lit + 0.24:.2f});')
            tw.append(f'tl.to("#rl{k - 1}",{{background:"{C.rgb(C.PAPER)}",borderColor:'
                      f'"#EBE3D8",duration:0.26,ease:SOFT}},{lit:.2f});')
            for sel in (f"#rl{k - 1}-n", f"#rl{k - 1}-t"):
                tw.append(f'tl.to("{sel}",{{color:"{C.rgb(C.MUTED)}",duration:0.26,'
                          f'ease:SOFT}},{lit:.2f});')
    # the only two non-arrival moves, each with a spoken reason
    move(tw, punch_t, rects["T"], s_uni, d=PUNCH_D)
    move(tw, final_t, wide, s_wide, d=PUNCH_D)

    # ---- WHIP GUARD ---------------------------------------------------------
    travel: list[str] = []
    for k in range(1, len(arrive)):
        if k in HIDDEN_MOVES:
            continue
        (_s0, ax, ay), (_s1, bx, by) = cam(rects[k - 1], s_uni), cam(rects[k], s_uni)
        d = ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5
        travel.append(f"     move {k - 1}->{k}: {d:6.0f} px / {CAM_D}s")
        if d > 1600.0:
            raise SystemExit(f"WHIP: visible move {k - 1}->{k} travels {d:.0f}px "
                             f"in {CAM_D}s")

    for t0, t1 in [(0.0, X.q(CUT_IN))] + [(X.q(r[0]), X.q(r[1])) for r in RETURNS] \
            + [(X.q(CUT_OUT), dur)]:
        tw.append(f'tl.set("#stage",{{opacity:0}},{t0:.2f});')
        tw.append(f'tl.set("#facewin",{{opacity:1}},{t0:.2f});')
        if t1 < dur:
            tw.append(f'tl.set("#stage",{{opacity:1}},{t1:.2f});')
            tw.append(f'tl.set("#facewin",{{opacity:0}},{t1:.2f});')
    X.outro_tweens(tw, CUT_OUT, a)

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
        (punch_t, "low_thump"),
        (X.q(CUT_OUT), "reverse_air"),
    ]
    cues += [(arrive[k], "page_turn") for k in range(len(arrive))
             if k not in HIDDEN_MOVES]
    audio, atw = X.audio_block(dur, cues)
    tw += atw

    X.audit(tw,
            moves=[(arrive[k], CAM_D) for k in range(len(arrive))
                   if k not in HIDDEN_MOVES]
                  + [(punch_t, PUNCH_D), (final_t, PUNCH_D)],
            cuts=[X.q(CUT_IN)] + [X.q(t) for r in RETURNS for t in r] + [X.q(CUT_OUT)],
            label=VAR, still_exempt=(arrive[0],))

    # ---- LAW 12 — the artifact's ink, in FRAME pixels -------------------------
    ink_l = ink_t = 1e9
    ink_r = ink_b = -1e9
    for sname, srect, s in stops:
        for ename, erect in elements:
            x0, y0, x1, y1 = _screen(erect, srect, s)
            if x1 < -1 or x0 > STAGE_W + 1 or y1 < -1 or y0 > STAGE_H + 1:
                continue
            ink_l = min(ink_l, L.WIN_X + max(0.0, x0))
            ink_r = max(ink_r, L.WIN_X + min(STAGE_W, x1))
            ink_t = min(ink_t, L.WIN_Y + max(0.0, y0))
            ink_b = max(ink_b, L.WIN_Y + min(STAGE_H, y1))
    law = L.law12_report(content_left=ink_l, content_right=ink_r,
                         content_top=ink_t, content_bottom=ink_b)

    stage = (f'  <div class="clip" id="stage" data-start="0" data-duration="{dur:.3f}" '
             f'data-track-index="10" style="left:{C.n(L.WIN_X)}px;top:{C.n(L.WIN_Y)}px;'
             f'width:{C.n(STAGE_W)}px;height:{C.n(STAGE_H)}px;overflow:hidden;'
             f'border-radius:{C.n(C.WIN_R)}px">'
             f'<div class="abs" id="board" style="left:0;top:0;width:{C.n(BOARD_W)}px;'
             f'height:{C.n(board_h)}px">{board_inner}</div></div>')
    body = "\n".join([stage, X.face_html(dur),
                      C.caption_clips(C.build_captions(words), dur), audio])

    print(f"{VAR}: dur={dur:.3f} @ {X.FPS}fps  board={BOARD_W:.0f}x{board_h:.0f}")
    print("\n".join(g.report()))
    print("\n".join(law))
    print(f"     stage {L.WIN_X:.0f},{L.WIN_Y:.0f} {STAGE_W:.0f}x{STAGE_H:.1f}"
          f"   S_UNI={s_uni:.5f}  wide={s_wide:.5f}"
          f"   frame sees {vis_w:.0f}x{vis_h:.0f} of board")
    for ci, col in enumerate(COLUMNS):
        print(f"     col {ci}: " + " ".join(
            f"{('HEADER' if c == 'T' else f'0{c + 1}')}[{card_h[c]:.0f}]" for c in col)
            + "   gaps " + " ".join(f"{g_:.0f}" for g_ in col_gaps[ci]))
    print("\n".join(stop_report))
    print("\n".join(travel))
    return C.page("Hermes infinite tools — ARTIFACT SPINE ZOOM (fix round 3)",
                  body, tw, dur)


if __name__ == "__main__":
    project = C.OUT_ROOT / VAR
    X.bind_assets(project)
    (project / "index.html").write_text(build(), encoding="utf-8")
    print(f"project={project}")
