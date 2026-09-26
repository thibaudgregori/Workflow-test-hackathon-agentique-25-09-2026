"""FACESPLIT — FIX ROUND 6.  THE CLOSING CAPTIONS ROUND.  Two changes, nothing
else: the CANONICAL caption pill, and the TWO-SEAT caption system.

  A. THE CANONICAL PILL.  The caption is no longer this format's to design.  It
     is the published factory pill — 56.2px (= 30 design units) Nunito 800,
     18.8/33.8 padding, 22.5 radius, #C4573A — lifted verbatim from
     references/builds/mcpupgrade_icon/projects/mcpupgrade_icon/index.html, the rule behind 97.1% of
     the 7,614 published caption pills.  It renders 114.59px tall, measured in
     the render browser on every build.  Round 5's derived 41.62px is gone; so
     is the published cap_font() shrink formula.  A phrase that will not fit the
     756px width budget is SPLIT at a word boundary into two caption beats
     (5 of them here) — never shrunk, never squeezed, never widened.

  B. TWO SEATS, ONE PER MODE, SWAPPED AS A HARD CUT (Miguel, confirmed).
       SPLIT  the pill sits ON THE SEAM, centred on y=960, exactly as the 32
              published shorts sit theirs on their own seam.  902.7..1017.3.
       FACE   the round-5 below-lip seat, still pinned by its BOTTOM at 1380px
              (71.88%, Law 12).  1265.4..1380.
     The chunker already forced a phrase break at every mode switch and blacked
     captions out across the two animated moves, so no pill is ever alive while
     its seat changes: the swap is a cut on the switch frame, verified on
     decoded frames at all twelve switches.

EVERYTHING ELSE IS ROUND 5, UNTOUCHED: the 50/50 seam at exactly 960, the
thirteen-segment mode map, all twelve switch times, the compress/expand beats,
the zone layout, the SFX set, the Law-11 meter, the 25fps grid.

--- round 4/5's documentation, kept verbatim below ---

FACESPLIT — FIX ROUND 4.  Dynamic switching, thirteen segments, EXACTLY 50/50.

Miguel, 2026-08-30: *"DYNAMIC switching between full-face and 50/50, back and
forth, whenever what's relevant changes — NOT one committed transition."*

THE MODE MAP — face when the moment is him talking to you, split when a visual
is earning the zone, face again the instant it stops earning it:

  #   t          mode    span   what is on screen / why
  --  ---------  ------  -----  ---------------------------------------------
  1   0.00       FACE    3.08   "Hermes Agent can now have literally infinite
                                tools."  The hook is the man making the claim.
  2   3.08 cut   SPLIT   2.68   "You think an AI agent loads every tool all at
                                once?"  THE CRAM: every tool slams into the
                                context window and the meter pegs at 100%.
                                That picture IS the question.
  3   5.76 cut   FACE    5.68   "Well, spoiler, they don't. You see, Hermes
                                Agent managed to crack the code. They
                                introduced something that's called-"  The
                                punchline, the aside and the setup are all his
                                face; the wrong picture is deleted on the cut.
  4   11.44 COMPRESS ->  10.84  the frame closes into its band and lands
      11.88      SPLIT          exactly on "procedural": the key term debuts
                                centre stage (Law 9), then PROCEDURAL
                                DISCLOSURE is staged physically — one tool in,
                                that one out, the next one in — then "tools
                                consume context" fills the window and "finite"
                                puts the ceiling on the meter.
  5   22.72 cut  FACE    2.76   "That means that the best way to handle your
                                context is by-"  Advice, delivered by a person.
  6   25.48 cut  SPLIT   4.12   "-being VERY PICKY..."  the ring, the cull, the
                                single survivor sliding to the centre.
  7   29.60 cut  FACE    1.12   "And the people over at-"  a 1.1s seize.
  8   30.72 cut  SPLIT   3.64   lands on "Nous": the mark, the lab, the chip.
  9   34.36 cut  FACE    1.24   "-so we can literally get-"  a 1.2s seize.
  10  35.60 cut  SPLIT   4.92   lands on "ALL of the tools": the shelf runs off
                                both frame edges = infinite, and the meter does
                                not move.
  11  40.52 cut  FACE    3.12   "If you have a Hermes agent, you can now
                                literally just give up-"  second person, direct.
  12  43.64 cut  SPLIT   6.56   "-ALL of the MCP servers..."  the lockup names
                                the shelf, the meter ticks 2% on "bloating" and
                                stops, the light wave crosses every tile.
  13  50.20 EXPAND ->    3.52   the band lets go and he takes the whole frame
      50.64      FACE           back for the sign-off (v3's finding, kept).

FIX ROUND 5 — the mode map above is UNCHANGED for the FIFTH round running,
every switch time to the frame, every content beat preserved.  Round 5 is pure
geometry, and it is TWO numbers plus one law:

  A. THE BAND'S INTERNAL FRAMING.  Miguel: *"solve the collisions by REFRAMING
     THE FACE, not by moving the pill... so the pill zone lands on his CHEST."*
     The seam does NOT move (still asserted at 960 on exact arithmetic); the
     band's magnification does: k = 5/9 -> 4/7, its measured maximum, which
     walks his whole face 25px further DOWN the band and takes the pill's bottom
     edge OFF the brow line and onto the cap (median clearance -4.7px -> +16.8px,
     measured over all 1625 master frames).  The CHEST seat itself is proved
     unreachable in facesplit_fix5_cam.py: his chest sits at 86-100% of frame
     height in any band-filling framing and Law 12 caps the caption at 72%.

  B. ONE CAPTION FONT SIZE FOR THE WHOLE VIDEO.  Round 4 shipped EIGHT (56.25 /
     54.38 / 51.94 / 49.69 / 45.94 / 44.25 / 39.75 / 37.31 px) because its
     `cap_font` scaled with phrase length.  Round 5 derives ONE — 24.1du =
     45.19px — from the FACE-mode collision: the pill is short enough (96px) for
     its TOP to sit below his highest chin (1276px), so the pill reads as
     sitting on his neck, never on his chin or mouth.  Phrases break earlier so
     they still fit one line; no word is re-worded, dropped, or re-timed.

ROUND 4's change, kept verbatim:

  1. THE SPLIT IS EXACTLY 50/50 AGAIN.  Miguel: *"no longer 50/50... not good
     for us."*  Visual zone y 0..960, face band y 960..1920, asserted at import
     on exact arithmetic.  Round 3 had traded the halves away (1318/785) to buy
     a caption seat; round 4 keeps the seat and moves the SPLIT MAGNIFICATION
     instead — s = 5/8 exactly, plate 1728x1920, transform-origin 864 x 2560,
     band content 1200px tall with 240px bleeding off the frame bottom so his
     features walk down past the pill.  See facesplit_fix4_cam.py.

  Consequences, all mechanical: the visual zone is 512du instead of 702.9du, so
  each ink block is re-centred in the zone's LEGAL band ([192px, 915px]) rather
  than in the zone; and the caption seat does NOT move — bottom 1380px, centre
  69.0-69.6%, ONE seat, both modes, whole video, asserted on the emitted HTML.

ZOOM: none.  Zero punch-ins, zero creep.  Both modes render at their derived
scale forever; the punch energy is the switch itself (2.444x head height, as a
hard cut).
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE / "lib"))
sys.path.insert(0, str(_HERE.parent.parent / "pipeline"))

import captions as CAP                     # noqa: E402
import facesplit_fix6_lib as L             # noqa: E402

VID = "facesplit_fix6"


# =============================================================================
# SEGMENT 2 — THE CRAM (the wrong picture, 3.08 - 5.76)
# =============================================================================
def cram_section(t0: float, t1: float, a: dict[str, float], tw: list[str],
                 sfx: list[tuple[float, str]]) -> str:
    """"You think an AI agent loads every tool all at once?"

    The video's central object — the CONTEXT WINDOW — is introduced here doing
    the WRONG thing, so that the same object doing the right thing later is an
    answer rather than an assertion.  It enters alone and centred (Law 19), it
    is filled within 1.4s (Law 20's corollary: never park an empty vessel), and
    it is deleted by the hard cut on "Well, spoiler, they don't."
    """
    p = "cw"
    tiles = "".join(
        L.plate(f"{p}s{i}", L.CORE_X[i], L.SHELF_Y, L.TILE, key, ink=L.TILE * 0.58)
        for i, key in enumerate(L.CORE))
    inside = "".join(
        L.plate(f"{p}t{i}", L.SLOTS[i][0], L.SLOTS[i][1], L.TILE, L.CORE[i],
                ink=L.TILE * 0.58) for i in range(6))
    kids = (L.txt(f"{p}-head", L.CARD_HEAD_Y - L.CARD_Y, "CONTEXT WINDOW", L.MICRO,
                  mono=True, ls=3.0, color=L.MUTED, weight=500, x=0.0,
                  w=L.CARD_W - 2 * L.PLATE_BORDER)
            + L.meter(p))
    body = (L.txt(f"{p}-lbl", L.SHELF_LBL_Y, "AVAILABLE TOOLS", 13.0, mono=True, ls=4.4,
                  color=L.MUTED, weight=500)
            + tiles
            + L.card(p, L.CARD_X, L.CARD_Y, L.CARD_W, L.CARD_H, kids)
            + inside)

    # the card lands ON the cut frame, so the seize and the subject are one event
    tw.append(L.settle(f"#{p}", t0, 0.38, 0.90))
    tw.append(f'tl.set("#{p}-fill",{{width:0}},0);')
    # the shelf arrives on "loads"
    for i in range(len(L.CORE)):
        tw.append(f'tl.set("#{p}s{i}",{{opacity:0}},0);'
                  f'tl.fromTo("#{p}s{i}",{{opacity:0,scale:0.7}},{{opacity:1,scale:1,'
                  f'duration:0.32,ease:POP,immediateRender:false}},'
                  f'{a["loads"] + 0.05 * i:.2f});')
    tw.append(L.fade(f"#{p}-lbl", a["loads"], 0.28))
    sfx.append((L.fq(a["loads"]), "tick"))
    # ...and on "every tool ALL AT ONCE" every single one of them piles in
    for i in range(6):
        sx, sy = L.SLOTS[i]
        tw.append(L.fly(f"#{p}t{i}", a["every"] + 0.13 * i,
                        L.CORE_X[i] - sx, L.SHELF_Y - sy, 0.40))
        tw.append(f'tl.to("#{p}s{i}",{{opacity:0.26,duration:0.24,ease:SOFT}},'
                  f'{a["every"] + 0.13 * i:.2f});')
    tw.append(L.fill_to(p, a["every"], 0.34, 0.40))
    tw.append(L.fill_to(p, a["all0"], 1.0, 0.40, ease='"power2.inOut"'))
    return L.section("cram", 4, t0, t1,
                     L.zone_wrap("cramwrap", L.dy_for(L.STAGE_EXTENT), body))


# =============================================================================
# SEGMENT 4a — THE KEY TERM (11.88 - 15.08)
# =============================================================================
def term_section(t0: float, t1: float, a: dict[str, float], tw: list[str]) -> str:
    """LAW 9 — the video's core term debuts CENTRE STAGE, one line per spoken
    word, the payoff word in the accent colour.  It is what the compress lands
    on, so the move has something to have been for."""
    body = (L.txt("tm1", 150.0, "PROCEDURAL", 58.0, color=L.INK)
            + L.txt("tm2", 226.0, "DISCLOSURE", 58.0, color=L.TERRA))
    for sel, t in (("#tm1", a["procedural"]), ("#tm2", a["disclosure"])):
        tw.append(f'tl.set("{sel}",{{opacity:0}},0);'
                  f'tl.fromTo("{sel}",{{opacity:0,y:{L.px(14)},scale:0.94}},'
                  f'{{opacity:1,y:0,scale:1,duration:0.38,ease:POP,immediateRender:false}},'
                  f'{t:.2f});')
    tw.append(L.tick("#tm2", a["whatmean"], 1.05, 0.34))
    tw.append(L.out("#tm1", t1 - 0.38, 0.30, -L.px(16)))
    tw.append(L.out("#tm2", t1 - 0.34, 0.30, -L.px(16)))
    return L.section("term", 5, t0, t1,
                     L.zone_wrap("termwrap", L.dy_for(L.TERM_EXTENT), body))


# =============================================================================
# SEGMENTS 4b/6/10/12 — THE STAGE (one persistent object, 15.08 - 50.20)
# =============================================================================
def stage_html() -> str:
    tiles = "".join(
        L.plate(f"sh{i}", L.EXT_X[i], L.SHELF_Y, L.TILE, key, ink=L.TILE * 0.58)
        for i, key in enumerate(L.SHELF))
    inside = "".join(
        L.plate(f"it{i}", L.SLOTS[i][0], L.SLOTS[i][1], L.TILE, L.CORE[i], ink=L.TILE * 0.58,
                kids=(f'<div class="abs" id="it{i}-ring" '
                      f'style="left:{L.px(-L.RING_GAP - L.PLATE_BORDER)}px;'
                      f'top:{L.px(-L.RING_GAP - L.PLATE_BORDER)}px;'
                      f'width:{L.px(L.TILE + 2 * L.RING_GAP)}px;'
                      f'height:{L.px(L.TILE + 2 * L.RING_GAP)}px;'
                      f'border:{L.px(3.0)}px solid {L.TERRA};'
                      f'border-radius:{L.px(L.rad(L.TILE, L.TILE) + L.RING_GAP)}px"></div>'
                      if i == 1 else ""))
        for i in range(6))
    inside += L.plate("hero0", L.SOLO[0], L.SOLO[1], L.TILE, L.CORE[L.HERO_A],
                      ink=L.TILE * 0.58)
    inside += L.plate("hero1", L.SOLO[0], L.SOLO[1], L.TILE, L.CORE[L.HERO_B],
                      ink=L.TILE * 0.58)
    kids = (L.txt("cd-head", L.CARD_HEAD_Y - L.CARD_Y, "CONTEXT WINDOW", L.MICRO,
                  mono=True, ls=3.0, color=L.MUTED, weight=500, x=0.0,
                  w=L.CARD_W - 2 * L.PLATE_BORDER)
            + L.meter("cd"))
    body = (L.txt("st-lbl", L.SHELF_LBL_Y, "AVAILABLE TOOLS", 13.0, mono=True, ls=4.4,
                  color=L.MUTED, weight=500)
            + f'<div class="abs" id="shelf" data-bleed style="left:0;top:0;'
              f'width:{L.px(576)}px;height:{L.px(120)}px">{tiles}</div>'
            + f'<div class="abs" id="mcplock" style="left:{L.px(L.centered(190.0))}px;'
              f'top:{L.px(L.MCP_LOCK_Y)}px;width:{L.px(190.0)}px;height:{L.px(L.MCP_MARK)}px">'
            + L.mark_img("mcplock-g", 20.0, L.MCP_MARK / 2, L.MCP_MARK * 0.86, "mcp")
            + L.txt("mcplock-t", (L.MCP_MARK - 16 * 1.36) / 2, "MCP SERVERS", 16.0,
                    mono=True, ls=3.0, color=L.INK, weight=700, x=44.0, w=146.0,
                    align="left")
            + "</div>"
            + L.card("cd", L.CARD_X, L.CARD_Y, L.CARD_W, L.CARD_H, kids)
            + inside)
    return L.zone_wrap("stagewrap", L.dy_for(L.STAGE_EXTENT), body)


def stage_tweens(a: dict[str, float], t_in: float, t_out: float,
                 sfx: list[tuple[float, str]], light_at: float) -> list[str]:
    tw: list[str] = []

    tw.append(L.settle("#cd", t_in + 0.06, 0.52, 0.90))
    tw.append(L.fade("#st-lbl", t_in + 0.30, 0.30))
    tw.append('tl.set("#cd-fill",{width:0},0);')
    tw.append('tl.set("#it1-ring",{opacity:0},0);')
    tw.append('tl.set("#mcplock",{opacity:0},0);')

    # the shelf arrives on "the AGENT will actually see the tools"
    for i in range(len(L.SHELF)):
        base = f'tl.set("#sh{i}",{{opacity:0}},0);'
        if i < len(L.CORE):
            tw.append(base + f'tl.fromTo("#sh{i}",{{opacity:0,scale:0.7,'
                             f'x:{L.px(L.CORE_X[i] - L.EXT_X[i])}}},'
                             f'{{opacity:1,scale:1,x:{L.px(L.CORE_X[i] - L.EXT_X[i])},'
                             f'duration:0.34,ease:POP,immediateRender:false}},'
                             f'{a["agentw"] + 0.05 * i:.2f});')
        else:
            # NO PEEK-AHEAD (Global Law 4): the extra seven do not exist on
            # screen until "ALL of the tools we will ever need".
            tw.append(base)

    def load(i, t, sel=None, seat=None, shelf_i=None):
        si = i if shelf_i is None else shelf_i
        sx, sy = seat or L.SLOTS[i]
        tw.append(L.fly(sel or f"#it{i}", t, L.CORE_X[si] - sx, L.SHELF_Y - sy))
        tw.append(f'tl.to("#sh{si}",{{opacity:0.26,duration:0.26,ease:SOFT}},{t:.2f});')

    def unload(i, t, sel=None, seat=None, shelf_i=None, d=0.38):
        si = i if shelf_i is None else shelf_i
        sx, sy = seat or L.SLOTS[i]
        tw.append(L.unfly(sel or f"#it{i}", t, L.CORE_X[si] - sx, L.SHELF_Y - sy, d))
        tw.append(f'tl.to("#sh{si}",{{opacity:1,duration:0.26,ease:SOFT}},{t + 0.10:.2f});')

    # PROCEDURAL DISCLOSURE made physical: one tool in, that one out, the next
    # one in — the agent only ever holds the tool it needs, at the card's centre.
    load(L.HERO_A, a["tools1"], sel="#hero0", seat=L.SOLO, shelf_i=L.HERO_A)
    sfx.append((L.fq(a["tools1"]), "tick"))
    unload(L.HERO_A, a["when"], sel="#hero0", seat=L.SOLO, shelf_i=L.HERO_A)
    load(L.HERO_B, a["needs2"], sel="#hero1", seat=L.SOLO, shelf_i=L.HERO_B)
    unload(L.HERO_B, a["consume0"] + 0.06, sel="#hero1", seat=L.SOLO,
           shelf_i=L.HERO_B, d=0.30)

    # TOOLS CONSUME CONTEXT — the window fills, the meter rises...
    for slot in range(6):
        load(slot, a["consume"] + 0.09 * slot)
    sfx.append((L.fq(a["consume"]), "tick"))
    tw.append(L.fill_to("cd", a["consume"], 0.30, 0.50))
    tw.append(L.fill_to("cd", a["consume"] + 0.55, 0.72, 0.62))
    # ...and COMPLETES on "finite", where the ceiling appears.  A meter that
    # never reaches full is a bug, not a style.
    tw.append(L.fill_to("cd", a["ctx2"] + 0.10, 1.0, 0.62, ease='"power2.inOut"'))
    # LAW 11: the ceiling is the fill ARRIVING at 100%, not a detached end tick.
    # The beat is carried by the card itself taking the hit.
    tw.append(L.tick("#cd", a["finite"], 1.02, 0.34))
    sfx.append((L.fq(a["finite"]), "pop"))

    # BE PICKY — one survivor, and it moves to the centre of the card
    tw.append(L.fade("#it1-ring", a["very"], 0.26))
    tw.append(L.tick("#it1", a["picky"], 1.08, 0.30))
    for j, i in enumerate([0, 2, 3, 4, 5]):
        unload(i, a["give"] + 0.09 * j)
    tw.append(f'tl.to("#it1",{{x:{L.px(L.SOLO[0] - L.SLOTS[1][0])},'
              f'y:{L.px(L.SOLO[1] - L.SLOTS[1][1])},duration:0.62,ease:SOFT}},'
              f'{a["give"] + 0.30:.2f});')
    tw.append(L.fill_to("cd", a["give"] + 0.20, 0.18, 0.85, ease='"power2.inOut"'))

    # THE INFINITE SHELF — it runs off both edges, the meter does not move
    for i in range(len(L.SHELF)):
        if i < len(L.CORE):
            tw.append(f'tl.to("#sh{i}",{{x:0,duration:0.66,ease:SOFT}},'
                      f'{a["all1"] + 0.02 * i:.2f});')
        else:
            tw.append(f'tl.fromTo("#sh{i}",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,'
                      f'duration:0.34,ease:POP,immediateRender:false}},'
                      f'{a["all1"] + 0.12 + 0.055 * (i - len(L.CORE)):.2f});')
    # LAW 11 again: no hold tick.  "No longer" is the fill DROPPING and staying.
    tw.append(L.fill_to("cd", a["nolonger"], 0.205, 0.45))

    # ...and they are MCP SERVERS
    tw.append(f'tl.fromTo("#mcplock",{{opacity:0,y:{L.px(-10)}}},{{opacity:1,y:0,'
              f'duration:0.40,ease:SOFT,immediateRender:false}},{a["mcp"]:.2f});')
    sfx.append((L.fq(a["mcp"]), "tick"))
    tw.append(L.tick("#sh6", a["mcp"] + 0.16, 1.12, 0.32))

    # WITHOUT BLOATING YOUR CONTEXT — the meter ticks 2% and stops
    tw.append(L.fill_to("cd", a["bloating"], 0.225, 0.50))

    # the light wave: every tile the shelf holds, left to right
    for i in range(len(L.SHELF)):
        tw.append(L.tick(f"#sh{i}", light_at + 0.035 * i, 1.10, 0.26))
    tw.append(L.tick("#it1", light_at + 0.20, 1.10, 0.30))

    # The stage retires on the last word of the argument ("...unbelievable"), a
    # clear 0.44s before the expand starts, so the growing frame never sweeps
    # over a live card — and so the card is never deleted by an unmount pop.
    tw.append(f'tl.to("#stagewrap",{{opacity:0,duration:0.36,ease:EXIT}},{t_out - 0.44:.2f});')
    return tw


# =============================================================================
# SEGMENT 8 — THE MAKERS (30.72 - 34.36)
# =============================================================================
def makers_section(t0: float, t1: float, a: dict[str, float], tw: list[str]) -> str:
    mk, mky = 140.0, 86.0
    body = (L.plate("mk", L.centered(mk), mky, mk, "nous", ink=mk * 0.74)
            + L.txt("mk-lab", mky + mk + 26.0, "NOUS RESEARCH", 30.0, color=L.INK, ls=1.0)
            + f'<div class="abs" id="mk-chip" style="left:{L.px(L.centered(200.0))}px;'
              f'top:{L.px(mky + mk + 84.0)}px;width:{L.px(200.0)}px;height:{L.px(46.0)}px;'
              f'background:{L.TERRA};border-radius:{L.px(14.0)}px">'
            + L.txt("mk-chip-t", (46.0 - 20 * 1.36) / 2, "HERMES", 20.0, mono=True, ls=3.0,
                    color="#FFFFFF", weight=700, x=0.0, w=200.0)
            + "</div>")
    tw.append(L.settle("#mk", a["nous"], 0.48, 0.88))
    tw.append(f'tl.set("#mk-lab",{{opacity:0}},0);'
              f'tl.fromTo("#mk-lab",{{opacity:0,y:{L.px(12)}}},{{opacity:1,y:0,'
              f'duration:0.40,ease:SOFT,immediateRender:false}},{a["lab"]:.2f});')
    tw.append(f'tl.set("#mk-chip",{{opacity:0}},0);'
              f'tl.fromTo("#mk-chip",{{opacity:0,scale:0.8}},{{opacity:1,scale:1,'
              f'duration:0.38,ease:POP,immediateRender:false}},{a["hermes1"]:.2f});')
    return L.section("makers", 6, t0, t1,
                     L.zone_wrap("makerswrap", L.dy_for(L.MAKERS_EXTENT), body))


# =============================================================================
# SEGMENT 13 — THE SIGN-OFF, ON HIS FACE (50.64 - end)
# =============================================================================
def face_outro(t0: float, dur: float, a: dict[str, float], tw: list[str]) -> str:
    """v3's finding, kept: the CTA is a person asking, at his own size.

    The face is full bleed, so the sign-off lockup sits ON the footage
    and gets round 1's scrim back — his t-shirt is black and INK type on black is
    not type.  Law 12 exempts the outro @handle chip from the bottom-28 % rule
    ("nothing actionable there"), and it is the ONLY thing in this build that
    uses the exemption: the caption pill still ends at 1380 through the sign-off.

    Air: the pill's bottom edge is 1380 and the handle's box starts at 1716, so
    the lockup keeps the 100 px of air the format's law asks for (336 px here),
    and the last baseline clears the frame bottom by ~103 px."""
    hy, dy = 1716.0, 1784.0
    body = (f'<div class="abs" id="fo-scrim" style="left:0;top:{1920 - 460:.0f}px;'
            f'width:1080px;height:460px;background:linear-gradient(to bottom,'
            f'rgba(0,0,0,0),rgba(0,0,0,.72))"></div>'
            + f'<div class="abs mono" id="fo-handle" style="left:0;top:{hy}px;width:1080px;'
              f'text-align:center;font-size:{L.px(L.HANDLE)}px;'
              f'line-height:{L.px(L.HANDLE * 1.36)}px;letter-spacing:{L.px(1.2)}px;'
              f'font-weight:700;color:#FFFFFF;text-transform:none">{L.OUTRO_HANDLE}</div>'
            + f'<div class="abs mono" id="fo-daily" style="left:0;top:{dy}px;width:1080px;'
              f'text-align:center;font-size:{L.px(13.0)}px;'
              f'line-height:{L.px(13 * 1.36)}px;letter-spacing:{L.px(4.4)}px;'
              f'font-weight:500;color:{L.TERRA_2};text-transform:none">daily AI</div>')
    tw.append(L.fade("#fo-scrim", t0, 0.45))
    tw.append(L.settle("#fo-handle", a["follow"] + 0.10, 0.44, 0.93))
    tw.append(L.fade("#fo-daily", a["tutorials"], 0.34))
    return (f'  <section id="faceoutro" class="clip" data-start="{t0:.2f}" '
            f'data-duration="{dur - t0:.2f}" data-track-index="20" '
            f'style="left:0;top:0;width:1080px;height:1920px">\n{body}\n  </section>')


# =============================================================================
def main() -> None:
    L.stage_assets()
    ws = L.words()
    a = L.anchors(ws)
    dur = L.duration()

    tw: list[str] = []
    sfx: list[tuple[float, str]] = []
    M = L.Modes()

    # ---- the mode map ------------------------------------------------------
    T_CRAM = M.cut(3.08, "split")                     # "You think an AI agent..."
    T_BACK1 = M.cut(5.76, "face")                     # "Well, spoiler, they don't."
    T_TERM = M.compress(11.44)                        # lands ON "procedural" 11.88
    T_ADVICE = M.cut(22.72, "face")                   # "That means the best way..."
    T_PICKY = M.cut(25.48, "split")                   # "...being VERY PICKY"
    T_AND = M.cut(29.60, "face")                      # "And the people over at-"
    T_NOUS = M.cut(30.72, "split")                    # lands on "Nous"
    T_SO = M.cut(34.36, "face")                       # "-so we can literally get-"
    T_ALL = M.cut(35.60, "split")                     # lands on "ALL of the tools"
    T_IFYOU = M.cut(40.52, "face")                    # "If you have a Hermes agent"
    T_MCP = M.cut(43.64, "split")                     # "-ALL of the MCP servers"
    T_SIGNOFF = M.expand(50.20)                       # lands 50.64, before "Follow"
    tw += M.tw

    # ---- the zone ----------------------------------------------------------
    t_stage_in, t_stage_out = 15.08, 50.20
    sections = [
        cram_section(T_CRAM, T_BACK1, a, tw, sfx),
        term_section(T_TERM, t_stage_in, a, tw),
        L.section("stage", 7, t_stage_in, t_stage_out, stage_html()),
        makers_section(T_NOUS, T_SO, a, tw),
    ]
    tw += stage_tweens(a, t_stage_in, t_stage_out, sfx, light_at=48.20)

    # The stage is ONE persistent object across four split segments, so its
    # state survives every face excursion.  Visibility is toggled on the exact
    # switch frames; nothing in it animates while it is hidden.
    for t in (T_ADVICE, T_AND, T_IFYOU):
        tw.append(f'tl.set("#stagewrap",{{opacity:0}},{t - 0.02:.2f});')
    for t in (T_PICKY, T_ALL, T_MCP):
        tw.append(f'tl.set("#stagewrap",{{opacity:1}},{t - 0.02:.2f});')

    # ---- SFX (SFX LAW v2 — tamed palette, class constants, frame-locked) ----
    # Seizes get a structure member, releases get its matched sibling, and four
    # of the face flashes are deliberately SILENT: Global Law 2 asks for taming,
    # and an effect on every switch is untamed however quiet it is.
    sfx += [
        (T_CRAM, "low_thump"),        # the first descent
        (T_BACK1, "reverse_air"),     # the release back to his face
        (11.44, "soft_whoosh"),       # THE COMPRESS
        (T_PICKY, "low_thump"),
        (T_NOUS, "low_thump"),
        (T_ALL, "soft_whoosh"),       # the shelf seizes the zone
        (50.20, "reverse_air"),       # THE EXPAND
    ]

    # ---- the sign-off, over the face ---------------------------------------
    top_sections = [face_outro(T_SIGNOFF, dur, a, tw)]

    caps = L.caption_clips(L.build_captions(ws, M.breaks, M.blackouts), dur,
                           M.timeline)
    page = L.compose("Hermes infinite tools — facesplit (fix round 6, canonical pill, two seats)",
                     dur, sections, caps, tw, sfx, top_sections)
    L.write(L.OUT_ROOT / "facesplit", page)

    face = sum(b - a_ for a_, b in M.spans("face", dur))
    split = sum(b - a_ for a_, b in M.spans("split", dur))
    print(f"{VID}: dur={dur:.3f} fps={L.FPS} switches={len(M.log) - 1} "
          f"face={face:.2f}s split={split:.2f}s sfx={len(sfx)} zooms=0")
    for t, kind, mode in M.log:
        print(f"   {t:6.2f}  {kind:<9} -> {mode}")


if __name__ == "__main__":
    import argparse
    _ap = argparse.ArgumentParser(description=__doc__)
    CAP.add_handle_arg(_ap)
    _ap.add_argument("--out", default=None, help="project root (default: ./build)")
    _args = _ap.parse_args()
    L.OUTRO_HANDLE = CAP.handle(_args.handle)   # the ONE parametrized constant
    if _args.out:
        L.OUT_ROOT = Path(_args.out)
    main()
    print(f"handle={L.OUTRO_HANDLE}")
