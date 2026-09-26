#!/usr/bin/env python3
"""ONE BUILD, THREE COMPOSITIONS — perplexityprojects / Diagram Build.

    YouTube  classic split 50/50   projects/perplexityprojects_split      @migueltorrezai
    TikTok   cutout                projects/perplexityprojects_cutout     @migueltorrez.ai
    Reels    takeover              projects/perplexityprojects_takeover   @migueltorrez.ai

The lane scene lives in `perplexityprojects_scene.py` and is authored exactly
once; this file places it three times and supplies each format's own frame — the
split's seam and face band, the cutout's matte layer set and depth field, the
takeover's cut map. Captions come from `pipeline/captions.py` and are never
re-derived.

WHY THE THREE RENDERS ARE NOT ALL 4K. STANDARD's 4K default (Miguel, 2026-08-10)
is applied to the split and the takeover, both of which drive 2160-wide face
plates and re-rasterise their type crisply. The CUTOUT renders NATIVE 1080x1920,
because its face is not footage the browser scales freely: it is an encoded layer
set (`matte_*_v5_cut.webm` at 1188x990) and cutout law 6b plus `guard_plate_box`
require the painted box to BE that encoded size. At `zoom:2` the CSS box and the
device box stop being the same number, which is precisely the class of bug that
cost `grokprice` 13% of its plate's detail. Re-shipping a 2376x1980 layer set to
buy 4K for a TikTok upload that ingests at 1080x1920 is a second encode for no
delivered pixels, so the format ships at its native size and the FACE HF gate is
measured against the plate it was actually cut from.

GUARDS THIS BUILD ASSERTS BEFORE IT WILL WRITE ANYTHING
  * caption canon: one size 56.2, one measured pill height, widest pill inside
    the 756px seat, every seat inside Law 30's band
  * `guard_plate_box`: the cutout's layer box is WHOLE PIXELS, at WHOLE-PIXEL
    offsets, and equals the encoded size of BOTH staged layers
  * voice: the staged audio is re-probed and must be 48 kHz (never the analysis
    wav — that file is not even written by this run's cut)
  * takeover: every cut edge is a Scribe word boundary
"""
from __future__ import annotations

import argparse
import html as ihtml
import json
import shutil
import subprocess
import sys
from pathlib import Path

F = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(F / "pipeline"))
sys.path.insert(0, str(F / "formats/cutout/lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import captions as CAP                       # noqa: E402
import cutout_core as CC                     # noqa: E402
import cutout_depthfield as DF               # noqa: E402
import perplexityprojects_scene as SC        # noqa: E402

RUN = F / "shorts_run9"
CUT = RUN / "cuts/perplexityprojects"
SESSION = F / "pipeline/sam2/sessions/perplexityprojects"
LOGOS = Path.home() / "Documents/Workspace/assets/logos"
ENV = json.loads((RUN / "gen/_envelope_perplexityprojects.json").read_text())

VID = "perplexityprojects"
W, H = 1080.0, 1920.0
FPS = 25                                     # native capture, Global Law 6
DUR = 30.016

# ------------------------------------------------------------------ formats
SEAM = 862.5                                 # the published split's seam
TK_CAP_Y = 1318.0                            # takeover chassis
TK_PILL_TOP = 1258.0
TK_REGION_MID = 629.0
TK_LEAD = 0.18
CO_CAP_Y = ENV["seats"]["CAP_Y"]             # DERIVED from this session's matte
CO_ZY0, CO_ZY1 = ENV["seats"]["ZY0"], ENV["seats"]["ZY1"]


def plate_origin(box_w: float, box_h: float) -> tuple[float, float]:
    """THE ORIGIN IS THE PLATE'S, NOT AN ASSUMPTION OF SYMMETRY.

    A 1.2:1 plate is centred on the canvas and `(W - box_w)/2` is right for it.
    An OVER-WIDE plate — the standard LAW 44 remedy (`formats/cutout/CHASSIS.md`)
    — is deliberately asymmetric: the master crop is extended sideways so the
    plate is wider than the visible frame and the FRAME does the cutting, and
    its box sits at a more negative left offset than a centred one would.  Where
    `plate.json` records an over-wide box, that IS the box; a centred guess would
    put his face tens of pixels off where the plate actually paints it.

    The box WIDTH is still the ENCODED size of the staged layers and nothing
    else — the grokprice law (cutout v5.1), re-asserted by `guard_plate_box`.
    """
    ob = (json.loads((SESSION / "plate.json").read_text()).get("overwide")
          or {}).get("plate_box")
    if ob:
        if [float(ob["w"]), float(ob["h"])] != [float(box_w), float(box_h)]:
            raise SystemExit(
                f"plate.json's over-wide box is {ob['w']}x{ob['h']} but the "
                f"staged layers are {box_w}x{box_h} — the box must BE the "
                "encoded size.  Re-ship the matte at the plate's display size.")
        return float(ob["left"]), float(ob["top"])
    return float(round((W - box_w) / 2)), float(H - box_h)


# THE TAKEOVER CUT MAP — GROWING, RE-TIMED UNDER THE SWITCH LAW (v2).
# Every edge below is a word START in `transcript_tight.json`;
# `assert_word_boundaries` refuses to build otherwise, and
# `formats/takeover/lib/takeover_switch_law.py` refuses to ship otherwise.
#
#   face 0.00-1.92 | T1 1.92-5.48 | face -6.58 | T2 -21.40 | face -22.54
#   coda -30.016
#   takeovers 3.56 -> 14.82 s (GROWING) + coda 7.48 s,  face 4.16s = 13.9%
#   5 switches / 30.016s = 9.99/min  (DEFINITIVE 7.77/min, ceiling 10.10)
#
# WHY v1 WAS REJECTED (Miguel, 2026-09-01): *"the switches of the face are
# happening way too often, they should happen at transition moments ideally,
# right now you are cutting key visualizations."* v1 ran 7 switches = 13.99/min,
# 1.8x the DEFINITIVE, and three of its four face windows sat ON TOP of a build:
# the whole b0 payoff (the open box, the arrow, its head — 3.94-4.76) was drawn
# behind his face and the frame came back to a finished picture; the sheet swap
# (9.40-9.74) likewise; and 18.74 cut away ON THE FIRST FRAME of the `local
# files` branch, so the third arm of a three-arm diagram built entirely unseen.
#
# THE RULE THAT REPLACES "place the face windows by what they hide": a face
# window may only sit in a QUIET WINDOW of the scene — after a visualization has
# finished building AND held (>= 0.30s), before the next one starts. This lane's
# scene runs on ONE continuous timeline behind the cuts, so a face window does
# not merely skip a beat, it ERASES whatever was drawing underneath it. The two
# returns below are the two real argument seams that are also quiet:
#
#   5.48-6.58  "Perplexity Projects will allow you to"  — the b0 diagram landed
#              at 4.76 and holds until 6.28, and its fade-out (6.28-6.58) runs
#              out behind the face on purpose: a first pass returned at 6.46 and
#              the frame's first visible content was the old diagram at ~15%
#              opacity, a ghost. Returning on `turn` (6.58) instead lands the
#              cut on b1's first sheet stroke — the new idea, not the old one's
#              residue. Hiding an EXIT is legal; hiding a BUILD is not.
#   21.40-22.54 "You can now store them in"             — the three research
#              arms landed at 19.62, the laptop screen at 21.02; the dedicated-
#              folder fills do not start until 22.54.
#
# The hook window (0.00-1.92) is the format's own device (Law 20) and is exempt
# from the hidden-build rule: before the first takeover the scene has not been
# revealed, and 1.92 is where `#h-fold` starts drawing, so the cut arrives INTO
# the build rather than onto a finished picture.
TK_FACE = [(0.00, 1.92), (5.48, 6.58), (21.40, 22.54)]
TK_CUTS = [1.92, 5.48, 6.58, 21.40, 22.54]

SFX_STRUCTURE = 0.14     # see `sfx_levels()` — measured, not inherited
SFX_DETAIL = 0.09
BED = 0.065              # AUDIO MIX LAW


# ------------------------------------------------------------------ transcript
def words() -> list[dict]:
    d = json.loads((CUT / "transcript_tight.json").read_text())
    return [w for w in d["words"] if w.get("type") == "word"]


def clean_tokens(ws: list[dict]) -> list[dict]:
    """LAW 6: a partial word never reaches a caption. This take has none, and
    the build asserts that rather than assuming it."""
    bad = [w for w in ws if w["text"].strip().endswith(("-", "...", "…"))]
    if bad:
        raise SystemExit(f"partial words in the take: {[b['text'] for b in bad]}")
    return ws


def phrases(ws: list[dict]) -> list[list[dict]]:
    """Group into caption phrases at punctuation and at real pauses.

    The pause threshold is not a taste constant: 0.30s is above every
    intra-phrase gap in this take (max 0.24 inside a clause) and below every
    clause gap this take actually has, so it separates rather than guesses.
    """
    out, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w)
        end = w["text"].strip().endswith((".", ",", "!", "?"))
        gap = (ws[i + 1]["start"] - w["end"]) if i + 1 < len(ws) else 9.0
        if end or gap >= 0.30 or len(cur) >= 6:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def caption_beats(measurer) -> list[dict]:
    ws = clean_tokens(words())
    measurer.want(CAP.runs([w["text"] for w in ws]))
    measurer.resolve()
    # RUN 9, THE "in" / LinkedIn DEFECT.  `phrases()` flushed after "You can now
    # store them" and left the preposition "in" standing as its own beat; measured
    # in the render browser that pill is 116.1 px wide on a 114.59 px pill — a
    # SQUARE carrying a bold white lowercase "in", which is the LinkedIn badge.
    # Nothing substituted a logo; the chunker made one.
    #
    # The merge runs over the WHOLE beat stream, not inside one phrase at a time:
    # orphans are produced AT phrase boundaries, so the neighbour a beat needs is
    # in the next phrase by construction.  See pipeline/captions.py section 3b and
    # pipeline/test_captions_function_words.py.
    parts: list[list] = []
    for group in phrases(ws):
        parts.extend(CAP.split_to_fit(group, CAP.SEAT_MAX_W, measurer))
    parts = CAP.merge_orphan_beats(parts, CAP.SEAT_MAX_W, measurer)

    beats: list[dict] = []
    for part in parts:
        text = " ".join(w["text"] for w in part)
        beats.append({"text": text, "start": float(part[0]["start"]),
                      "end": float(part[-1]["end"]),
                      "w": measurer.width(text)})
    for i, b in enumerate(beats):                       # gapless
        nxt = beats[i + 1]["start"] if i + 1 < len(beats) else b["end"] + 0.26
        b["dur"] = round(max(0.24, min(nxt, DUR) - b["start"]), 3)
    CAP.assert_no_function_only_beat(beats)
    widest = max(b["w"] for b in beats)
    if widest > CAP.SEAT_MAX_W + 0.6:
        raise SystemExit(f"pill {widest:.1f}px exceeds the {CAP.SEAT_MAX_W} seat")
    return beats


def caption_html(beats, seat_y, *, breaks=()) -> str:
    """`breaks` are format switch times: a phrase may never be ALIVE across one,
    so it is split there (the facesplit finding, applied to the takeover's cuts).

    HALF A FRAME IS TRIMMED ONLY AT A BREAK. `data-start + data-duration` is a
    float sum, so a clip ending exactly ON a switch frame survives one frame into
    the next mode and lands the old seat's pill across the new one. But trimming
    EVERY clip — which is what the first pass did — opens a one-frame hole
    between every two captions, and at 25 fps that is a 40 ms flicker 34 times in
    a 30-second video. It was visible in the first split render (a sample at
    t=2.60 landed in the 0.02s hole between `...Perplexity Projects,` and `the
    evolution of...`). The track is GAPLESS everywhere and short by half a frame
    only where a cut actually happens.
    """
    half = 0.5 / FPS
    brk = set(round(t, 3) for t in breaks)
    out = []
    for b in beats:
        segs = [(b["start"], b["start"] + b["dur"])]
        for t in breaks:
            nxt = []
            for a, z in segs:
                if a < t < z:
                    nxt += [(a, t), (t, z)]
                else:
                    nxt.append((a, z))
            segs = nxt
        for a, z in segs:
            d = max(0.08, z - a - (half if round(z, 3) in brk else 0.0))
            out.append(
                f'<div class="clip scap" style="top:{seat_y}px" '
                f'data-start="{a:.2f}" data-duration="{d:.2f}" '
                f'data-track-index="25"><span class="scappill">'
                f'{ihtml.escape(b["text"], quote=False)}</span></div>')
    return "\n".join(out)


# ------------------------------------------------------------------ page shell
def head(title: str, w: int, h: int, zoom: int, extra_css: str) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width={int(W)}, height={int(H)}"/>
<title>{ihtml.escape(title)}</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Nunito:wght@800&family=JetBrains+Mono:wght@400;500;700&display=block" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:{int(W)}px; height:{int(H)}px; overflow:hidden;
  font-family:Poppins,sans-serif; zoom:{zoom}; }}
.clip {{ position:absolute; }} .abs {{ position:absolute; }}
.disp {{ font-family:Poppins,sans-serif; }}
.mono {{ font-family:'JetBrains Mono',monospace; text-transform:uppercase; }}
.core {{ transform-origin:0 0; }}
{CAP.pill_rule()}
{extra_css}
</style></head>
<body><div id="root" data-composition-id="main" data-start="0"
 data-width="{w}" data-height="{h}" data-duration="{DUR}" data-fps="{FPS}">
"""


def tail(tweens: list[str]) -> str:
    body = "".join(tweens)
    return f"""
</div>
<script>
window.__timelines = window.__timelines || {{}};
const SOFT = "power2.out";
const tl = gsap.timeline({{paused:true}});
{body}
window.__timelines["main"]=tl;
</script></body></html>
"""


def outro_lockup(handle_key: str) -> str:
    """The scene reserves `#o-slot`; every format seats THIS lockup inside it.

    The lockup is authored in CORE units, so each format's own `scale(k)` sizes
    it exactly as it sizes the rest of the scene — no format re-derives an outro
    type scale. The handle is the ONLY string that differs between the three
    renders (Miguel, 2026-09-01), and it is never re-typed: `captions.handle()`
    resolves it.
    """
    return (CAP.outro_chip_html(0.0, handle_key, size=56.25, width=SC.CORE_W)
            + CAP.outro_daily_html(86.0, size=24.375, width=SC.CORE_W))


# ------------------------------------------------------------------ staging
def stage(dst: Path, *, face: str | None, matte: bool) -> dict:
    v = dst / "assets/v"
    v.mkdir(parents=True, exist_ok=True)
    (dst / "assets/music").mkdir(parents=True, exist_ok=True)
    (dst / "assets/sfx").mkdir(parents=True, exist_ok=True)
    (dst / "assets/logos").mkdir(parents=True, exist_ok=True)
    rec: dict = {}

    # VOICE — the 48 kHz master, re-probed after staging (cutout law 6c: the
    # staged file is what mixes, so the staged file is what is measured).
    shutil.copy2(CUT / "audio.m4a", v / "voice.m4a")
    pr = probe_audio(v / "voice.m4a")
    if pr["sample_rate"] < 44100:
        raise SystemExit(f"staged voice is {pr['sample_rate']} Hz — the analysis "
                         "track can never be the mix (cutout law 6c)")
    rec["voice"] = {"source": str(CUT / "audio.m4a"), **pr}

    shutil.copy2(F / "assets/music/bed_split_v2.mp3", dst / "assets/music/bed.mp3")
    for s in ("whoosh", "pop", "click"):
        shutil.copy2(F / f"assets/sfx/{s}.mp3", dst / f"assets/sfx/{s}.mp3")
    if face:
        shutil.copy2(CUT / face, v / face)
        rec["face"] = {"file": face, **probe_wh(CUT / face)}
    if matte:
        # THE STAMP RECORDS THE FILE, NOT JUST ITS NAME (CHASSIS, known traps).
        # `ship.py --out` always writes the SAME filenames, so a re-track that
        # replaces a matte outright leaves `str(src)` identical.  The copy here
        # is unconditional, so a stale staged layer cannot happen — but the
        # per-layer `.src` stamp is still written, because
        # `cutout6_check.check_edge_clip` reads `splitlines()[0]` off it to find
        # the `_alpha.webm` sibling it has to sweep for LAW 44, and its second
        # line changes whenever the file does.
        for src, name in ((SESSION / f"matte_{VID}_v5_cut.webm", "matte.webm"),
                          (SESSION / f"matte_{VID}_v5_rim.webm", "matte_rim.webm")):
            if not src.exists():
                raise SystemExit(f"missing matte layer {src}")
            shutil.copy2(src, v / name)
            st = src.stat()
            (v / f"_{name}.src").write_text(f"{src}\n{st.st_size} {st.st_mtime_ns}")
        (v / "_matte_source.txt").write_text(str(SESSION))
        # THE DISPLAY PLATE IS NAMED BY ITS SIZE, and this session's size is the
        # OVER-WIDE one (1584x990, the LAW 44 remedy).  Derive it from the
        # ENCODED layer rather than typing 1188x990, or the FACE HF gate is
        # pointed at a plate that does not exist and reports nothing.
        cut_wh = probe_wh(v / "matte.webm")
        dp = SESSION / f"plate_display_{cut_wh['w']}x{cut_wh['h']}.mp4"
        if not dp.exists():
            raise SystemExit(f"no display plate at {dp} — ship.py --display "
                             f"{cut_wh['w']}x{cut_wh['h']} has not been run for "
                             "this matte, and FACE HF has nothing to compare to")
        rec["matte"] = {
            "cut": cut_wh,
            "rim": probe_wh(v / "matte_rim.webm"),
            "plate": str(dp),
        }
    # THE HARD ROSTER GUARD (run 9).  Existence was never the problem: `exa`
    # existed, decoded, and rasterised non-empty, and it still shipped a tile the
    # viewer test named as "a broken image".  `assert_cast_resolves` runs the
    # resolution AND the placeholder-shape test on every mark before a frame is
    # rendered.  See `formats/cutout/lib/cutout_depthfield.py`.
    DF.assert_cast_resolves(list(ALL_LOGO_FILES), ALL_LOGO_FILES, LOGOS,
                            label="perplexityprojects marks")
    for key, rel in ALL_LOGO_FILES.items():
        src = LOGOS / rel
        if not src.exists():
            raise SystemExit(f"missing registry mark: {src}  (add + register it)")
        shutil.copy2(src, dst / f"assets/logos/{Path(rel).name}")
        if matte:
            # `mark_img` sizes every mark by INK AREA and corrects its centroid,
            # which is why a row of them reads even.  That needs the mark
            # measured, so the cutout — the only format with a depth field —
            # registers all of them here.
            CC.MARK_INK[key] = CC.measure_mark(key, src)
    return rec


LOGO_FILES = {
    "perplexity": "ai-models/perplexity-color.png",
    "claude": "ai-models/claude-color.png",
    "chatgpt": "ai-models/chatgpt-color.svg",
    "gemini": "ai-models/gemini-color.png",
    "grok": "ai-models/grok.png",
    "deepseek": "ai-models/deepseek.svg",
    "kimi": "ai-models/kimi.png",
    "openai": "ai-models/openai.png",
}

# THE DEPTH FIELD'S CAST.  The geometry of the field is NOT this file's to invent
# any more — it comes from `formats/cutout/lib/cutout_depthfield.py`, frozen off
# the approved grokpublish render.  The only per-video choices are WHO is in the
# field and which mark the pop-behind card carries.
#
# LAW 29 / LAW 33: every tile is a REAL provider mark, repeated rather than left
# blank, never a generic glyph.  `perplexity` is deliberately ABSENT: it is the
# subject on the stage for the whole take, and a mark cannot be the subject and
# the wallpaper behind him in the same frame.  It crosses the band exactly once,
# on the pop-behind card, which is where a story mark is allowed to be.
#
# RUN 9, THE VIEWER TEST'S SYSTEMIC FINDING: the first cast was 22 marks wide and
# most of them were consumer apps — WhatsApp, Gmail, Drive, YouTube, GitHub,
# Telegram, Maps.  "For ~25 of the 30 seconds the largest, highest-contrast
# objects on screen are brands the narration never mentions ... it pays off
# exactly once, at 25.5 s."  At 0.5 s the hook frame was a dozen consumer icons
# with the subject reduced to a 40 px glyph, and at 7.5 s a crisp ChatGPT tile sat
# at his jaw while the sentence named Perplexity.
#
# THE CAST IS NOW TOPICAL AND NOTHING ELSE: nine AI providers / research surfaces,
# which is the exact comparison the script makes ("just like you can with any
# other AI provider").  The wall now argues the video instead of competing with
# it.  Three further changes carry the rest of that finding:
#   * `DEPTH_TEXTURE` recesses the whole field so it reads as texture, not content;
#   * `HOOK_CLEAR` holds the lanes off the first 1.3 s so the hook frame is the
#     Perplexity mark on cream;
#   * the pop-behind is re-keyed to the Perplexity that OPENS the product claim
#     at 6.82 s, which clears the host lane across 7.5 s.
DEPTH_FILES = {
    "claude": "ai-models/claude-color.png",
    "chatgpt": "ai-models/chatgpt-color.svg",
    "gemini": "ai-models/gemini-color.png",
    "grok": "ai-models/grok.png",
    "deepseek": "ai-models/deepseek.svg",
    "kimi": "ai-models/kimi.png",
    "openrouter": "platforms/openrouter-mark.svg",
    "firefox": "ai-models/firefox-color.png",
    "notion": "platforms/notion-color.png",
}

# THE MARKS THIS VIDEO IS NOT ALLOWED TO PUT ON THE WALL.  Kept as a named,
# asserted list rather than as an absence, because an absence is not a rule and
# the generic wall grew back once already.
DEPTH_BANNED = {"gmail", "gdrive", "youtube", "github", "whatsapp", "telegram",
                "slack", "gmaps", "n8n", "figma", "excalidraw", "airtable",
                "elevenlabs", "exa"}
if set(DEPTH_FILES) & DEPTH_BANNED:
    raise SystemExit(f"off-topic marks in the depth cast: "
                     f"{sorted(set(DEPTH_FILES) & DEPTH_BANNED)}")

ALL_LOGO_FILES = {**LOGO_FILES, **DEPTH_FILES}
LOGO_URL = {k: f"assets/logos/{Path(v).name}" for k, v in ALL_LOGO_FILES.items()}
DEPTH = list(DEPTH_FILES)

# THE POP-BEHIND.  A live app card crosses the mid lane at his shoulder, is
# occluded by him and re-emerges on the far side, carrying the mark he is
# naming.  `Perplexity` is spoken five times; the crossing is keyed on the one
# that OPENS the product claim ("turn Perplexity from a one-off research tool"),
# RUN 9 FIX: it was keyed on word 11 (4.90 s), so the crossing ENDED at 7.50 s and
# the host lane restored a ChatGPT tile at his jaw on the exact frame the sentence
# said "Perplexity".  It is now keyed on word 18 (6.82 s) — the Perplexity inside
# "turn Perplexity from a one-off research tool", the clause that opens the claim
# — so the card is mid-crossing at 7.50 s and the lane it hosts is CLEARED there.
# THE FIELD RECEDES.  The foundation's lane opacities (0.34 / 0.66 / 1.00) are
# frozen for the format and are NOT edited here — they are scaled for this video
# only, at the call site, so the sibling builds keep the foundation exactly.
DEPTH_TEXTURE = 0.70
HOOK_CLEAR = 1.30              # the lanes stay off until the hook has landed

POP_MARK = "perplexity"
POP_WORD_INDEX = 18
POP_LEAD, POP_SPAN = 0.10, 2.70


def seat_core(centre: float, k: float) -> float:
    """Seat the core so its CONTENT BAND is centred on `centre`.

    Centring the core BOX is the wrong sum and it is a Law 15 defect, not a
    rounding one: the box is 680 tall and the content occupies 40..534 of it, so
    the box's centre sits 53*k px below the content's. The takeover's first pass
    centred the box on `REGION_MID` and the diagram landed 70px high in the
    region it owns.
    """
    return round(centre - (SC.CONTENT_Y0 + SC.CONTENT_Y1) / 2 * k, 2)


def guard_core_band(fmt: str, top: float, k: float, cap_seat: float,
                    pill_clear: float = 24.0) -> dict:
    """The core is placed, not authored, so every placement is asserted.

    Two bounds, both from Law 30 as amended: nothing meaningful in the top 10%
    (y < 192), and nothing touching the caption pill (THE SEAM IS SACRED,
    promoted to an audit ERROR on 2026-08-10). The takeover hardens the second
    into its own 112px band, which its builder checks separately.
    """
    y0 = top + SC.CONTENT_Y0 * k
    y1 = top + SC.CONTENT_Y1 * k
    pill_top = cap_seat - CAP.CAP_PILL_HEIGHT / 2
    if y0 < 0.10 * H:
        raise SystemExit(f"{fmt}: core content starts at y={y0:.1f}, inside the "
                         f"top 10% ({0.10 * H:.0f}) — Law 30")
    if y1 > pill_top - pill_clear:
        raise SystemExit(f"{fmt}: core content ends at y={y1:.1f}, within "
                         f"{pill_clear}px of the pill top {pill_top:.1f} — the "
                         "seam is sacred")
    return {"content_top": round(y0, 1), "content_bottom": round(y1, 1),
            "law30_top_10pct": 0.10 * H, "pill_top": round(pill_top, 1),
            "clear_above_pill": round(pill_top - y1, 1)}


def probe_wh(p: Path) -> dict:
    o = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height", "-of", "json", str(p)],
        capture_output=True, text=True, check=True).stdout)["streams"][0]
    return {"w": int(o["width"]), "h": int(o["height"])}


def probe_audio(p: Path) -> dict:
    o = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
         "stream=sample_rate,channels", "-of", "json", str(p)],
        capture_output=True, text=True, check=True).stdout)["streams"][0]
    return {"sample_rate": int(o["sample_rate"]), "channels": int(o["channels"])}


def guard_plate_box(box: dict, staged: dict) -> None:
    """THE BOX IS THE PLATE'S ENCODED SIZE, NOT THE SCALE (cutout v5.1).

    Four checks, because each one alone forces a browser resample of his face.
    """
    for k in ("left", "top", "w", "h"):
        if abs(box[k] - round(box[k])) > 1e-9:
            raise SystemExit(f"plate box {k}={box[k]} is not a whole pixel — "
                             "Chromium will resample every frame of his face")
    for layer in ("cut", "rim"):
        enc = staged[layer]
        if (box["w"], box["h"]) != (enc["w"], enc["h"]):
            raise SystemExit(
                f"plate box {box['w']}x{box['h']} != encoded {layer} "
                f"{enc['w']}x{enc['h']} — set the box from the ENCODED size")


def sfx_levels() -> dict:
    """SFX LAW v2 specifies THREE level classes against a palette normalised to
    -19.0 dBFS. The factory's `assets/sfx/*.mp3` are NOT that palette — they are
    the un-normalised files the published corpus mixed at a flat 0.18 — so the
    lab's 0.120/0.077/0.038 constants would mean a different delivered level on
    these files. The gains here are the published 0.18 stepped DOWN toward the
    lab's structure/detail ratio, and each file's measured mean level is recorded
    so the next build can compare delivered loudness instead of gain constants.
    """
    out = {}
    for s in ("whoosh", "pop", "click"):
        r = subprocess.run(
            ["ffmpeg", "-v", "info", "-i", str(F / f"assets/sfx/{s}.mp3"),
             "-af", "volumedetect", "-f", "null", "-"],
            capture_output=True, text=True)
        mean = next((ln.split("mean_volume:")[1].strip()
                     for ln in r.stderr.splitlines() if "mean_volume:" in ln), "?")
        out[s] = {"mean_volume": mean}
    out["_gains"] = {"structure": SFX_STRUCTURE, "detail": SFX_DETAIL,
                     "published_corpus_flat": 0.18}
    return out


def audio_html(sfx: list[tuple[str, float, float]]) -> str:
    rows = [f'<audio id="vo" src="assets/v/voice.m4a" data-start="0" '
            f'data-duration="{DUR}" data-track-index="30" data-volume="1"></audio>',
            f'<audio id="bg0" src="assets/music/bed.mp3" data-start="0" '
            f'data-duration="{DUR}" data-track-index="31" '
            f'data-volume="{BED}"></audio>']
    for i, (name, at, vol) in enumerate(sfx):
        rows.append(f'<audio id="sfx{i}" src="assets/sfx/{name}.mp3" '
                    f'data-start="{at:.2f}" data-duration="0.62" '
                    f'data-track-index="{40 + i}" data-volume="{vol}"></audio>')
    return "\n".join(rows)


# ------------------------------------------------------------------ the three
def build_split(out: Path, handle: str) -> dict:
    staged = stage(out, face="face_bottom_4k.mp4", matte=False)
    scene_html, tweens = SC.build(LOGO_URL, outro_lockup(handle))
    k = 1.0
    left = (W - SC.CORE_W * k) / 2
    # SEATED ON LAW 30, NOT CENTRED IN THE ZONE. Centring the 680-tall core in
    # the 862.5 zone puts core y=0 at canvas 91.2, so the hook object's own
    # resting seat landed at canvas 117 — inside the top 10% the law reserves.
    # The core is seated so its declared content band starts exactly on the line.
    # The split's zone is tight (0..805 under the pill), so the core is seated
    # on the binding constraint rather than centred: content starts exactly on
    # Law 30's line and the band then sits 439 in a 0..805 region.
    top = round(0.10 * H - SC.CONTENT_Y0 * k, 2)
    m = CAP.PillMeasurer(RUN / "gen/_pillwidths.json")
    beats = caption_beats(m)
    CAP.assert_law12(SEAM, max(b["w"] for b in beats))
    band = guard_core_band("split", top, k, SEAM)

    body = [
        f'<video id="facebot" src="assets/v/face_bottom_4k.mp4" data-start="0" '
        f'data-duration="{DUR}" data-media-start="0" data-track-index="1" muted '
        f'playsinline style="position:absolute;top:{SEAM}px;left:0;width:{int(W)}px;'
        f'height:{H - SEAM}px;object-fit:cover"></video>',
        f'<section id="tz" class="clip tz" data-start="0" data-duration="{DUR}" '
        f'data-track-index="2">',
        f'<div class="abs core" id="core" style="left:{left}px;top:{top}px;'
        f'width:{SC.CORE_W}px;height:{SC.CORE_H}px;transform:scale({k})">',
        scene_html, "</div></section>",
        caption_html(beats, SEAM),
        audio_html(SPLIT_SFX),
    ]
    css = (f".tz {{ left:0; top:0; width:{int(W)}px; height:{SEAM}px; "
           f"overflow:hidden; background:{SC.CREAM}; }}")
    (out / "index.html").write_text(
        head("Perplexity Projects — the evolution of Spaces", 2160, 3840, 2, css)
        + "\n".join(body) + tail(tweens), encoding="utf-8")
    return {"staged": staged, "beats": beats, "seat": SEAM, "scale": k,
            "core": {"left": left, "top": top}, "band": band,
            "render": {"w": 2160, "h": 3840, "zoom": 2}}


SPLIT_SFX = [("whoosh", SC.CUE["projects0"], SFX_STRUCTURE),
             ("pop", SC.CUE["desk"], SFX_DETAIL),
             ("pop", SC.CUE["folders"], SFX_DETAIL),
             ("whoosh", SC.CUE["whether"], SFX_STRUCTURE),
             ("click", SC.CUE["dedicated"], SFX_DETAIL),
             ("whoosh", SC.CUE["anyother"], SFX_STRUCTURE)]


def build_cutout(out: Path, handle: str) -> dict:
    staged = stage(out, face=None, matte=True)
    box_w = float(staged["matte"]["cut"]["w"])
    box_h = float(staged["matte"]["cut"]["h"])
    box_left, box_top = plate_origin(box_w, box_h)
    box = {"w": box_w, "h": box_h, "left": box_left, "top": box_top}
    guard_plate_box(box, staged["matte"])

    scene_html, tweens = SC.build(LOGO_URL, outro_lockup(handle))
    k = round((CO_ZY1 - CO_ZY0) / SC.CORE_H, 4)
    left = (W - SC.CORE_W * k) / 2
    m = CAP.PillMeasurer(RUN / "gen/_pillwidths.json")
    beats = caption_beats(m)
    CAP.assert_law12(CO_CAP_Y, max(b["w"] for b in beats))
    core_top = seat_core((CO_ZY0 + CO_ZY1) / 2, k)
    band = guard_core_band("cutout", core_top, k, CO_CAP_Y)

    # THE DEPTH FIELD.  ROUND 1 OF THIS BUILD INVENTED ITS OWN AND MIGUEL
    # REJECTED IT ON SIGHT: 78/116/**168** px tiles at 0.52 x tile gaps, seated
    # at 1046/1214/1436 so the three rows sat 90 and 106 px apart instead of the
    # foundation's 26, in a 558 px band instead of 394, stepping ONCE for the
    # whole take and stepping the WRONG WAY.  "We used to have a beautiful
    # regular background ... you changed the perspective and you changed the
    # space."  Every one of those was a number, and the numbers now live in
    # `formats/cutout/lib/cutout_depthfield.py`, frozen off the approved
    # grokpublish render.  Only the cast and the pop-behind are chosen here.
    CC.BOXES.clear()
    bf = json.loads((RUN / f"gen/_df/bandframes_{VID}.json").read_text())
    cap_bottom = CO_CAP_Y + CAP.CAP_PILL_HEIGHT / 2
    y0, seat = DF.seat(bf, cap_bottom=cap_bottom, plate_top=box["top"],
                       plate_scale=round(box["h"] / 900.0, 4),
                       plate_left=box["left"])
    # THE FIELD RECEDES TO TEXTURE.  Scaled here, never in the foundation: the
    # foundation's 0.34 / 0.66 / 1.00 stay frozen for every other build.
    lane_defs = [(n, t, y, g, round(o * DEPTH_TEXTURE, 4), d)
                 for n, t, y, g, o, d in DF.lanes_at(y0)]
    ws = words()
    step_beats = DF.step_beats(ws, DUR, n=12, fps=FPS)
    lanes_html, lane_geom, n_tiles = DF.field(
        lane_defs, LOGO_URL, DEPTH, len(step_beats), rec=lambda *a, **k: None)
    tweens += DF.schedule(lane_defs, step_beats)
    # THE HOOK IS THE SUBJECT, NOT THE WALL.  The viewer test's first NO-SENSE on
    # this render was frame 0.50: "the picture's dominant mass is a dozen consumer
    # apps that are not the subject".  The lanes are held off the frame until the
    # Perplexity mark has landed and been read, then they arrive one lane at a
    # time.  The wrapper (`lw-`) is the same handle the pop-behind uses, and the
    # two windows do not overlap (hook 0..1.82, pop 6.72..9.42).
    tweens += [f'tl.set("#lw-{n}",{{opacity:0}},0);'
               for n, *_ in lane_defs]
    tweens += [f'tl.to("#lw-{n}",{{opacity:1,duration:0.52,ease:SOFT}},'
               f'{HOOK_CLEAR + i * 0.10:.2f});'
               for i, (n, *_) in enumerate(lane_defs)]

    pop_start = float(ws[POP_WORD_INDEX]["start"])
    if ws[POP_WORD_INDEX]["text"] != "Perplexity":
        raise SystemExit(f"the pop-behind is keyed on word {POP_WORD_INDEX}, which "
                         f"is {ws[POP_WORD_INDEX]['text']!r}, not 'Perplexity' — "
                         "the cut moved and the beat must be re-decided")
    pt0 = round(round((pop_start - POP_LEAD) * FPS) / FPS, 3)
    pt1 = round(round((pop_start - POP_LEAD + POP_SPAN) * FPS) / FPS, 3)
    pop_html, pop_tw, pop_rep = DF.pop_behind(
        "pop", lane_defs, LOGO_URL, POP_MARK, [(pt0, pt1)],
        rec=lambda *a, **k: None)
    tweens += pop_tw
    # THE CLAIM WINDOW OWNS THE FRAME.  `pop_behind` clears its own HOST lane
    # (mid) for the crossing, which is what put the Perplexity card at his
    # shoulder unobstructed.  It does not clear the NEAR lane — and the near lane
    # is the one at JAW height, which is where the viewer test found "a large
    # crisp green ChatGPT tile beside his jaw while the sentence names
    # Perplexity.  The picture names the wrong product."  For the length of the
    # claim, the only brand on screen is the one being claimed.
    tweens += [
        f'tl.to("#lw-near",{{opacity:0,duration:0.34,ease:SOFT}},{pt0 - 0.34:.2f});',
        f'tl.to("#lw-near",{{opacity:1,duration:0.40,ease:SOFT}},{pt1 + 0.10:.2f});',
    ]
    field = {"seat": seat, "lanes": lane_geom, "tiles": n_tiles,
             "step_beats": step_beats, "pop_behind": pop_rep,
             "foundation": "formats/cutout/lib/cutout_depthfield.py "
                           "(grokpublish, approved 2026-09-01)"}

    body = [
        f'<div class="abs ground" style="left:0;top:0;width:{int(W)}px;'
        f'height:{int(H)}px;background:{SC.CREAM}"></div>',
        f'<section id="tz-cut" class="clip" data-start="0" data-duration="{DUR}" '
        f'data-track-index="2" style="left:0;top:{CO_ZY0}px;width:{int(W)}px;'
        f'height:{CO_ZY1 - CO_ZY0}px;overflow:hidden">',
        f'<div class="abs core" id="core" style="left:{left:.1f}px;'
        f'top:{core_top - CO_ZY0:.2f}px;width:{SC.CORE_W}px;'
        f'height:{SC.CORE_H}px;transform:scale({k})">',
        scene_html, "</div></section>",
        # GLOBAL LAW 8 — the fade is on each LANE's own canvas-wide wrapper
        # now (`cutout_depthfield.field`), not on one outer box, because that is
        # where the foundation puts it and where the pop-behind needs it too.
        f'<div class="abs" id="lanes" data-overlap-ok data-bleed style="left:0;'
        f'top:0;width:{int(W)}px;height:{int(H)}px">'
        + lanes_html + pop_html + "</div>",
        f'<video id="matte-rim" src="assets/v/matte_rim.webm" data-start="0" '
        f'data-duration="{DUR}" data-media-start="0" data-track-index="59" muted '
        f'playsinline style="position:absolute;left:{int(box["left"])}px;'
        f'top:{int(box["top"])}px;width:{int(box["w"])}px;height:{int(box["h"])}px;'
        f'filter:drop-shadow(0 10px 26px rgba(0,0,0,.20))"></video>',
        f'<video id="matte" src="assets/v/matte.webm" data-start="0" '
        f'data-duration="{DUR}" data-media-start="0" data-track-index="60" muted '
        f'playsinline style="position:absolute;left:{int(box["left"])}px;'
        f'top:{int(box["top"])}px;width:{int(box["w"])}px;'
        f'height:{int(box["h"])}px"></video>',
        caption_html(beats, CO_CAP_Y),
        audio_html(SPLIT_SFX),
    ]
    page = (head("Perplexity Projects — the evolution of Spaces", 1080, 1920, 1, "")
            + "\n".join(body) + tail(tweens))
    # GLOBAL LAW 8, on the page this build is about to write to disk.  A guard is
    # only a guard if it is CALLED -- that is the whole lesson of run 9.
    edge_fade = CC.guard_edge_fade(page)
    (out / "index.html").write_text(page, encoding="utf-8")
    return {"staged": staged, "beats": beats, "seat": CO_CAP_Y, "scale": k,
            "edge_fade": edge_fade,
            "core": {"left": left, "top": core_top}, "plate": {"box": box},
            "band": band,
            "stage_zone": [CO_ZY0, CO_ZY1],
            "depth_field": field,
            "render": {"w": 1080, "h": 1920, "zoom": 1}}


def assert_word_boundaries(cuts: list[float]) -> list[dict]:
    ws = words()
    starts = {round(float(w["start"]), 2): w["text"] for w in ws}
    out = []
    for t in cuts:
        key = round(t, 2)
        if key not in starts:
            raise SystemExit(f"takeover cut at {t} is not a Scribe word boundary")
        out.append({"t": t, "word": starts[key]})
    return out


def takeover_runs() -> list[tuple[float, float]]:
    """The scene runs: the complement of TK_FACE inside [0, DUR)."""
    runs, cur = [], 0.0
    for a, z in TK_FACE:
        if a - cur > 1e-6:
            runs.append((round(cur, 3), round(a, 3)))
        cur = z
    if DUR - cur > 1e-6:
        runs.append((round(cur, 3), round(DUR, 3)))
    return runs


def switch_law_report(page: Path | None = None) -> dict:
    """THE TAKEOVER SWITCH LAW, measured off the page this build just wrote.

    Deterministic gate, not a review note: it re-parses the emitted HTML, finds
    every face<->scene boundary and every build window in the scene timeline,
    and refuses to ship a cut that takes the frame away from a visualization
    before it lands and holds, or that switches faster than the DEFINITIVE
    takeover's own rate. See `formats/takeover/lib/takeover_switch_law.py`.
    """
    sys.path.insert(0, str(F / "formats/takeover/lib"))
    import takeover_switch_law as LAW              # noqa: E402
    page = page or (RUN / "projects/perplexityprojects_takeover/index.html")
    rep = LAW.audit(page.read_text(encoding="utf-8"), DUR, "perplexityprojects")
    if not rep["ok"]:
        for d in rep["defects"]:
            print(f"  SWITCH-LAW DEFECT[{d['law']}] {d}")
        raise SystemExit("takeover switch law: the cut map cuts a "
                         "visualization or switches too often")
    return {k: rep[k] for k in
            ("switch_count", "switches_per_min", "definitive_per_min",
             "ceiling_per_min", "face_pct", "switches", "face_windows",
             "scene_windows")}


def build_takeover(out: Path, handle: str) -> dict:
    staged = stage(out, face="face_full_4k.mp4", matte=False)
    edges = assert_word_boundaries(TK_CUTS)
    scene_html, tweens = SC.build(LOGO_URL, outro_lockup(handle))
    k = 1.05
    left = (W - SC.CORE_W * k) / 2
    top = seat_core(TK_REGION_MID, k)
    m = CAP.PillMeasurer(RUN / "gen/_pillwidths.json")
    beats = caption_beats(m)
    CAP.assert_law12(TK_CAP_Y, max(b["w"] for b in beats))
    band = guard_core_band("takeover", top, k, TK_CAP_Y,
                           pill_clear=112.0)

    faces = []
    for i, (a, z) in enumerate(TK_FACE):
        faces.append(
            f'<video class="clip" id="face{i}" src="assets/v/face_full_4k.mp4" '
            f'data-start="{a:.2f}" data-duration="{z - a - 0.5 / FPS:.3f}" '
            f'data-media-start="{a:.2f}" data-track-index="{10 + i}" muted '
            f'playsinline style="left:0;top:0;width:{int(W)}px;height:{int(H)}px;'
            f'object-fit:cover"></video>')

    sfx = []
    for i, t in enumerate(TK_CUTS):
        entering = not any(abs(t - a) < 1e-6 for a, _ in TK_FACE)
        sfx.append(("whoosh" if entering else "pop", t,
                    SFX_STRUCTURE if entering else SFX_DETAIL))

    body = [
        f'<div class="abs ground" style="left:0;top:0;width:{int(W)}px;'
        f'height:{int(H)}px;background:{SC.CREAM}"></div>',
        f'<section id="tz" class="clip" data-start="0" data-duration="{DUR}" '
        f'data-track-index="2" style="left:0;top:0;width:{int(W)}px;'
        f'height:{int(H)}px;overflow:hidden">',
        f'<div class="abs core" id="core" style="left:{left:.1f}px;'
        f'top:{top:.1f}px;width:{SC.CORE_W}px;height:{SC.CORE_H}px;'
        f'transform:scale({k})">', scene_html, "</div></section>",
        "\n".join(faces),
        caption_html(beats, TK_CAP_Y, breaks=TK_CUTS),
        audio_html(sfx),
    ]
    (out / "index.html").write_text(
        head("Perplexity Projects — the evolution of Spaces", 2160, 3840, 2, "")
        + "\n".join(body) + tail(tweens), encoding="utf-8")
    switch_law_report(out / "index.html")          # refuses to ship a bad map
    face_s = sum(z - a for a, z in TK_FACE)
    return {"staged": staged, "beats": beats, "seat": TK_CAP_Y, "scale": k,
            "core": {"left": left, "top": top}, "cut_edges": edges,
            "band": band,
            "face_seconds": round(face_s, 3),
            "face_pct": round(face_s / DUR, 4),
            "takeover_lengths": [round(b - a, 2) for a, b in
                                 takeover_runs()],
            "switch_law": switch_law_report(out / "index.html"),
            "render": {"w": 2160, "h": 3840, "zoom": 2}}


# ------------------------------------------------------------------ main
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None,
                    choices=("split", "cutout", "takeover"))
    a = ap.parse_args()

    jobs = {
        "split": (RUN / "projects/perplexityprojects_split", "yt", build_split),
        "cutout": (RUN / "projects/perplexityprojects_cutout", "tiktok_ig",
                   build_cutout),
        "takeover": (RUN / "projects/perplexityprojects_takeover", "tiktok_ig",
                     build_takeover),
    }
    report = {"video": VID, "lane": "diagram", "fps": FPS, "duration": DUR,
              "sfx": sfx_levels(), "envelope": ENV["seats"], "formats": {}}
    for name, (dst, handle, fn) in jobs.items():
        if a.only and name != a.only:
            continue
        dst.mkdir(parents=True, exist_ok=True)
        rep = fn(dst, handle)
        rep["handle_key"] = handle
        rep["handle"] = CAP.handle(handle)
        rep["captions"] = {"n": len(rep["beats"]),
                           "widest_px": round(max(b["w"] for b in rep["beats"]), 1),
                           "font_px": CAP.CAP_FONT,
                           "pill_height_px": CAP.CAP_PILL_HEIGHT,
                           "sizes": 1}
        rep.pop("beats")
        report["formats"][name] = rep
        print(f"{name}: {dst}")
    (RUN / "gen/_build_perplexityprojects.json").write_text(
        json.dumps(report, indent=1))
    print(json.dumps({k: v for k, v in report.items() if k != "sfx"}, indent=1))


if __name__ == "__main__":
    main()
