#!/usr/bin/env python3
"""impossibletask — ONE build, THREE compositions (run 9, the daily pipeline).

    split    -> YouTube      classic 50/50, HANDLE_YT
    cutout   -> TikTok       matted silhouette + depth band, HANDLE_TIKTOK_IG
    takeover -> Reels        21/79 full-bleed alternation, HANDLE_TIKTOK_IG

The visual story lives ONCE, in `impossibletask_scene.py`, as a 1080x560 scene
block.  This file is three format SHELLS that place that block and add only the
chrome each format owns: the split's seam and face band, the cutout's matte
layers and depth lanes, the takeover's full-bleed cuts.  Nothing about the beats,
the atoms, the tweens or the SFX differs between the three — which is the whole
reason renders two and three are nearly free.

CAPTIONS come from `pipeline/captions.py` and are never re-derived: ONE size
(56.2 px), measured in the real render browser, long phrases SPLIT at word
boundaries, and one stable seat per format.

Run:  python impossibletask_gen.py
"""
from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

F = Path.home() / "Documents/Workspace/projects/personal/content/shorts-factory"
RUN = F / "shorts_run9"
sys.path.insert(0, str(F / "pipeline"))
sys.path.insert(0, str(F / "formats/cutout/lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import captions as CAP                                            # noqa: E402
import cutout_core as C                                           # noqa: E402
import cutout_depthfield as DF                                    # noqa: E402
import cutout_media as CM                                         # noqa: E402
import impossibletask_stage_v3 as S               # noqa: E402  (v2 -> v3: round 4)
from cutout_core import CREAM, INK, PAPER, TERRA, esc, rgba       # noqa: E402

VID = "impossibletask"
CUT = RUN / f"cuts/{VID}"
SESSION = F / "pipeline/sam2/sessions" / VID
LOGOS = Path.home() / "Documents/Workspace/assets/logos"
SFX_DIR = F / "format_lab/_shared/sfx"
BED = F / "assets/music/bed_split_v2.mp3"
GEN = Path(__file__).resolve().parent
ENVELOPE = GEN / f"envelope_{VID}.json"

W, H = 1080, 1920
FPS = 25                       # GLOBAL LAW 6 — and the raw is 25 fps NATIVE

# =============================================================================
# CLIP INTERVALS ARE HALF-OPEN AND FRAME-QUANTISED.  A FRAME BELONGS TO EXACTLY
# ONE CLIP.  (v4, 2026-09-02 — the fix for the fix.)
#
# THE HISTORY, because both halves of it matter.
#   v3 found real clip-boundary GHOSTING (one frame showing two beats at once)
#   and blamed an inclusive producer.  The producer is NOT inclusive: its
#   runtime is `p >= start && p < start + duration` (verified in
#   `packages/cli/dist/hyperframe-runtime.js`) — already half-open.  The ghost
#   was a FLOAT artefact, and so was v3's cure.  Shortening every clip by
#   CLIP_EPS = 0.02 put each clip's computed end EXACTLY on a frame time, where
#   double arithmetic decides the frame's fate by 1 ulp:
#
#       b6:  16.70 + (20.62 - 16.70 - 0.02) = 20.599999999999998
#       frame 515 is at 20.60, and 20.60 < 20.599999999999998 is FALSE
#       -> b6 gone, b7 (start 20.62) not yet arrived -> ONE BLANK FRAME
#
#   The Viewer Test decoded exactly that: a single fully blank cream frame at
#   20.60 s and again at 25.36 s, in BOTH the split and the cutout.  An eps that
#   lands on the grid does not avoid the boundary; it IS the boundary.
#
# THE CURE IS TO STOP DOING ARITHMETIC NEAR A FRAME TIME.  Every clip edge is
# snapped to a FRAME INDEX, and the clip's duration carries a HALF-FRAME of
# slack so its computed end sits in the middle of the gap between the last frame
# it owns and the first frame it does not:
#
#       start  = k0 / fps                       (k0 = round(t0 * fps))
#       dur    = (k1 - k0 - 0.5) / fps          (k1 = round(t1 * fps))
#       end    = (k1 - 0.5) / fps               -> 0.02 s clear of BOTH frames
#
# Frame k1 - 1 is 0.02 s inside the clip; frame k1 is 0.02 s outside it and is
# exactly the next clip's `data-start`.  No frame can be owned twice and none
# can be orphaned, and the margin is a trillion times any float error.
# `pipeline/clip_coverage_check.py` re-proves this on the emitted page and on
# every decoded frame of the finished render.
# =============================================================================
def frame_of(t: float, fps: int = FPS) -> int:
    """The frame index a wall-clock second belongs to, rounded half UP."""
    return math.floor(round(t * fps, 6) + 0.5)


def clip_start(t0: float) -> float:
    """A clip's `data-start`, snapped to the frame grid."""
    return round(frame_of(t0) / FPS, 3)


def clip_dur(t0: float, t1: float, *, last: bool = False) -> float:
    """On-screen duration for a clip that hands over to another at `t1`.

    The LAST clip of a track keeps every frame through `t1`: it hands over to
    nothing, so there is no boundary to keep clear of."""
    k0, k1 = frame_of(t0), frame_of(t1)
    if k1 <= k0:
        raise SystemExit(f"clip [{t0}, {t1}) is shorter than one frame")
    return round((k1 - k0 if last else k1 - k0 - 0.5) / FPS, 4)

# ---- the marks this build names.  LAW 35: the PRODUCT mark, never the parent --
MARKS = {
    "codex": LOGOS / "coding-tools/codex-color.png",     # not the OpenAI mark
    "x": LOGOS / "platforms/x-logo.svg",
}
# THE DEPTH FIELD'S CAST.  The geometry of the field is NOT a decision this file
# gets to make any more — it comes from `formats/cutout/lib/cutout_depthfield.py`,
# frozen off the approved grokpublish render.  The only per-video choice is WHO
# is in it (this list) and which mark the pop-behind card carries.
#
# LAW 29 / LAW 33: every tile is a REAL provider mark, repeated rather than left
# blank, and never a generic glyph.  The story's own marks — `codex` and `x` —
# are deliberately ABSENT: the depth band is the world he is standing in front
# of, and a mark cannot be the subject on the stage and the wallpaper behind him
# in the same frame.
DEPTH_FILES = {
    "gmail": LOGOS / "platforms/gmail-color.png",
    "gdrive": LOGOS / "platforms/google-drive.svg",
    "notion": LOGOS / "platforms/notion-color.png",
    "slack": LOGOS / "platforms/slack-color.png",
    "github": LOGOS / "coding-tools/github-mark.png",
    "airtable": LOGOS / "platforms/airtable-color.png",
    "telegram": LOGOS / "platforms/telegram.svg",
    "whatsapp": LOGOS / "platforms/whatsapp.svg",
    "gmaps": LOGOS / "platforms/google-maps-color.png",
    "exa": LOGOS / "platforms/exa-color.png",
    "claude": LOGOS / "ai-models/claude-color.png",
    "chatgpt": LOGOS / "ai-models/chatgpt-color.png",
    "figma": LOGOS / "design-tools/figma-color.png",
    "excalidraw": LOGOS / "design-tools/excalidraw-color.png",
    "apify": LOGOS / "platforms/apify-color.png",
    "elevenlabs": LOGOS / "platforms/elevenlabs-mark.svg",
    "openrouter": LOGOS / "platforms/openrouter-mark.svg",
    "youtube": LOGOS / "platforms/youtube-color.png",
    "perplexity": LOGOS / "ai-models/perplexity-color.png",
    "gemini": LOGOS / "ai-models/gemini-color.png",
    "n8n": LOGOS / "automation/n8n-icon.png",
    "make": LOGOS / "automation/make-color.png",
    "zapier": LOGOS / "automation/zapier-color.png",
}
DEPTH = list(DEPTH_FILES)

# THE POP-BEHIND.  A live app card crosses the mid lane at his shoulder, is
# occluded by him and re-emerges on the far side — on the beat where he NAMES
# the tool.  `Codex` is spoken exactly once, at 4.64 s.
POP_MARK = "codex"
POP_ON = ["Codex"]
POP_LEAD, POP_SPAN = 0.10, 2.70

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800'
    '&family=Nunito:wght@800&family=JetBrains+Mono:wght@400;500;700&display=block" '
    'rel="stylesheet">'
)
GSAP = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>'


# =============================================================================
# transcript + anchors
# =============================================================================
def load_words() -> list[dict]:
    data = json.loads((CUT / "transcript_tight.json").read_text())
    return [w for w in data["words"] if w.get("type") == "word"]


def anchor_fn(words: list[dict]):
    """`A("word")` -> that word's START, in cut-local seconds.  `"word#2"` takes
    the second occurrence.  Every anchor is an exact token from the tight
    transcript, so nothing in the scene is a hand-tuned time."""
    used: dict[str, int] = {}

    def A(key: str) -> float:
        text, sep, occ = key.partition("#")
        hits = [w for w in words if w["text"] == text]
        # AN AMBIGUOUS ANCHOR IS A BUILD FAILURE, NOT A DEFAULT.
        # The first draft silently took the FIRST match, and `A("way")` therefore
        # resolved to word 63 ("are WAY beyond", 18.68 s) instead of word 99
        # ("all the WAY to the end", 27.52 s) — putting the mission rail's second
        # step nine seconds before the sentence it belongs to, inside a beat that
        # is not even on screen.  It survived Gate 1 (geometry is time-blind) and
        # produced a value that looked like a GSAP ordering bug for an hour.  A
        # token that occurs more than once must now name WHICH one.
        if not sep and len(hits) > 1:
            raise SystemExit(
                f"anchor {text!r} is AMBIGUOUS: it occurs {len(hits)} times at "
                f"{[round(float(h['start']), 2) for h in hits]} — write "
                f"{text!r}#1 .. #{len(hits)} and say which word the beat means")
        n = int(occ) if occ else 1
        if len(hits) < n:
            raise SystemExit(
                f"anchor {key!r}: the tight transcript has {len(hits)} occurrence(s) "
                f"of {text!r}, not {n} — the cut moved and every beat keyed on it "
                "must be re-decided")
        used[key] = used.get(key, 0) + 1
        return round(float(hits[n - 1]["start"]), 2)

    A.used = used                                          # type: ignore[attr-defined]
    return A


# =============================================================================
# captions — pipeline/captions.py is the law, nothing here re-derives it
# =============================================================================
FILLERS = {"uh", "um", "erm", "eh"}


def clean_tokens(words: list[dict]) -> list[dict]:
    """LAW 6: stutters and false starts never reach a caption.  This take has
    none inside it (the cut asserts zero truncations), so this pass is a guard
    rather than a filter — it is kept because a silent behaviour change in Scribe
    is exactly the thing that would slip one through."""
    out = []
    for i, w in enumerate(words):
        t = w["text"].strip()
        if t.endswith("-"):
            continue
        if re.sub(r"[^a-z]", "", t.lower()) in FILLERS and len(t) <= 4:
            continue
        out.append(w)
    return out


def build_captions(words: list[dict]) -> tuple[list[dict], CAP.PillMeasurer]:
    """ONE SIZE, MEASURED, AND THE GROUPING IS FIT-AWARE.

    The first draft grouped on a word COUNT (4) and then handed any over-wide
    group to `split_balanced`.  That is the canon's mechanism used as a repair
    rather than as a last resort, and it produced pills like "AI impossible" —
    a balanced cut through the middle of a phrase, visible on the pre-render
    still sheet.  Here the group GROWS while the RENDERED pill still fits the
    seat, so the width bound shapes the phrase instead of breaking it:

        break when   adding the next word would exceed the 756 px seat
                  |  the word ends a clause (punctuation) and we have >= 2
                  |  the next word is more than 0.32 s away
                  |  the group has reached 5 words

    `split_balanced` stays as the guard for the case a single clause still does
    not fit, and the build asserts nothing ends up wider than the seat.
    """
    words = clean_tokens(words)
    m = CAP.PillMeasurer(GEN / f"_pillwidths_{VID}.json")
    m.want(CAP.runs([w["text"] for w in words][:0]))          # keep the cache key
    # measure every contiguous run of up to 6 words — the complete candidate set
    cands = [" ".join(w["text"] for w in words[i:j])
             for i in range(len(words))
             for j in range(i + 1, min(i + 7, len(words) + 1))]
    m.want(cands)
    m.resolve()

    groups: list[list[dict]] = []
    cur: list[dict] = []
    for i, w in enumerate(words):
        trial = cur + [w]
        if cur and m.width(" ".join(x["text"] for x in trial)) > CAP.SEAT_MAX_W:
            groups.append(cur)
            cur = [w]
        else:
            cur = trial
        nxt = words[i + 1] if i + 1 < len(words) else None
        punct = bool(re.search(r"[.,!?]$", w["text"]))
        gap = bool(nxt and nxt["start"] - w["end"] > 0.32)
        if cur and ((punct and len(cur) >= 2) or gap or len(cur) >= 5 or nxt is None):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    # a one- or two-word group is a stranded orphan: give it back to its
    # neighbour whenever the merged pill still fits the seat
    merged: list[list[dict]] = []
    for g in groups:
        if (len(g) <= 2 and merged
                and m.width(" ".join(x["text"] for x in merged[-1] + g)) <= CAP.SEAT_MAX_W):
            merged[-1] = merged[-1] + g
            continue
        merged.append(g)

    beats: list[dict] = []
    for g in merged:
        for part in CAP.split_balanced(g, CAP.SEAT_MAX_W, m,
                                       join=lambda ws: " ".join(w["text"] for w in ws)):
            beats.append({"t0": round(float(part[0]["start"]), 2),
                          "t1": round(float(part[-1]["end"]) + 0.12, 2),
                          "text": " ".join(w["text"] for w in part)})
    for i in range(len(beats) - 1):
        beats[i]["t1"] = beats[i + 1]["t0"]
    return beats, m


def caption_html(beats: list[dict], seat_y: float, dur: float) -> str:
    out = []
    for i, p in enumerate(beats):
        t0, t1 = p["t0"], min(p["t1"], dur)
        if t1 - t0 < 0.08 or t0 >= dur:
            continue
        last = i == len(beats) - 1
        out.append(
            f'  <div id="cap{i}" class="clip scap" style="top:{seat_y}px" '
            f'data-start="{clip_start(t0):.3f}" '
            f'data-duration="{clip_dur(t0, t1, last=last):.4f}" '
            f'data-track-index="25"><span class="scappill">{esc(p["text"])}'
            f'</span></div>')
    return "\n".join(out)


# =============================================================================
# audio — the AUDIO MIX LAW + SFX LAW v2 (the three level classes)
# =============================================================================
def probe_dur(p: Path) -> float:
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], check=True, capture_output=True,
        text=True).stdout.strip())


def audio_html(dur: float, sfx: list[tuple[str, float]]) -> tuple[str, list[str]]:
    els = [f'  <audio id="vo" src="assets/v/voice.m4a" data-start="0" '
           f'data-duration="{dur:.3f}" data-track-index="30" data-volume="1"></audio>']
    bed_len = probe_dur(BED)
    t, i, last = 0.0, 0, None
    while t < dur - 0.1:
        d = min(bed_len, dur - t)
        els.append(f'  <audio id="bg{i}" src="assets/music/bed_split.mp3" '
                   f'data-start="{t:.2f}" data-duration="{d:.2f}" '
                   f'data-track-index="{31 + i}" data-volume="0.065"></audio>')
        last = (f"bg{i}", t)
        t += bed_len
        i += 1
    for j, (name, t0) in enumerate(sorted(sfx, key=lambda s: s[1])):
        if t0 < 0 or t0 >= dur - 0.15:
            continue
        d = probe_dur(SFX_DIR / f"{name}.mp3")
        els.append(f'  <audio id="sfx{j}" src="assets/sfx/{name}.mp3" '
                   f'data-start="{t0:.2f}" data-duration="{min(d, dur - t0):.2f}" '
                   f'data-track-index="{60 + j}" '
                   f'data-volume="{S.SFX_CLASS[name]}"></audio>')
    tw = [f'tl.fromTo("#{last[0]}",{{volume:0.065}},{{volume:0,duration:1.45,'
          f'immediateRender:false}},{max(last[1], dur - 1.5):.2f});'] if last else []
    return "\n".join(els), tw


# =============================================================================
# staging
# =============================================================================
def stage(stage_dir: Path, *, need_face: str | None,
          need_matte: bool) -> tuple[dict, dict]:
    for rel in ("v", "logos", "music", "sfx"):
        (stage_dir / rel).mkdir(parents=True, exist_ok=True)
    # VOICE — cutout LAW 6c: the 48 kHz master, and the resolver REFUSES a
    # low-rate track by name.  The staged file is then re-probed, because a stale
    # staged asset once let a "fixed" build ship the defect it had just fixed.
    voice = CM.stage_voice(CUT, stage_dir)
    shutil.copy2(BED, stage_dir / "music/bed_split.mp3")
    for name in S.SFX_CLASS:
        src = SFX_DIR / f"{name}.mp3"
        if src.exists():
            shutil.copy2(src, stage_dir / "sfx" / f"{name}.mp3")
    if need_face:
        dst = stage_dir / "v" / Path(need_face).name
        if not dst.exists() or dst.stat().st_mtime < (CUT / need_face).stat().st_mtime:
            shutil.copy2(CUT / need_face, dst)
    if need_matte:
        for src_name, dst_name in (("matte_impossibletask_v5_cut.webm", "matte.webm"),
                                   ("matte_impossibletask_v5_rim.webm", "matte_rim.webm")):
            src = SESSION / src_name
            if not src.exists():
                raise SystemExit(f"missing matte layer {src}")
            dst = stage_dir / "v" / dst_name
            stamp = stage_dir / "v" / f"_{dst_name}.src"
            # THE STAMP RECORDS THE FILE, NOT JUST ITS NAME.  `ship.py --out`
            # always writes the SAME filenames, so a re-track that produces a
            # completely different matte leaves `str(src)` identical and the
            # staged copy was never refreshed.  That is not hypothetical: the
            # round-4 plate widening shipped on 2026-09-02 10:25 and the staged
            # `matte.webm` stayed at the 2026-09-01 20:42 LIFT matte, so the v8
            # and v9 renders composited the matte the widening had replaced
            # while check 26 swept the session file and reported the new one.
            # The stamp therefore carries the size and mtime as a SECOND LINE,
            # which changes whenever the file does.  Line 1 stays the bare path,
            # because `cutout6_check.check_edge_clip` reads `splitlines()[0]` to
            # find the alpha sibling to sweep.
            st = src.stat()
            tag = f"{src}\n{st.st_size} {st.st_mtime_ns}"
            if (not dst.exists() or not stamp.exists()
                    or stamp.read_text().strip() != tag):
                shutil.copy2(src, dst)
                stamp.write_text(tag)
    # THE SOURCE POST (v3).  LAW 14 ships the ACTUAL post as a raster, so it is
    # staged like media, not like a registry mark: `measure_mark` measures a
    # LOGO's ink and means nothing on a tweet card.
    (stage_dir / "source").mkdir(parents=True, exist_ok=True)
    card_src = RUN / json.loads((RUN / "plans/x_card_impossibletask.json")
                                .read_text())["file"]
    if not card_src.exists():
        raise SystemExit(f"the source card is missing: {card_src} — run "
                         "render_x_card_impossibletask.py")
    shutil.copy2(card_src, stage_dir / "source/card.png")

    media: dict[str, str] = {"postcard": "assets/source/card.png"}
    want = dict(MARKS)
    if need_matte:
        want.update(DEPTH_FILES)
    for key, src in want.items():
        if not src.exists():
            raise SystemExit(f"missing registry mark: {src}  (add + register it first)")
        shutil.copy2(src, stage_dir / "logos" / f"{key}{src.suffix}")
        media[key] = f"assets/logos/{key}{src.suffix}"
        C.MARK_INK[key] = C.measure_mark(key, src)
    return media, voice


def bind(project: Path, stage_dir: Path) -> None:
    project.mkdir(parents=True, exist_ok=True)
    dest = project / "assets"
    if dest.is_symlink() or dest.exists():
        dest.unlink() if dest.is_symlink() else shutil.rmtree(dest)
    dest.symlink_to(stage_dir.resolve(), target_is_directory=True)


# =============================================================================
# the scene, built once
# =============================================================================
def build_scene(A, media, handle: str):
    """Returns {beat_id: (html, tweens)} plus the whole build's SFX cue list."""
    scenes, sfx_all = {}, []
    for bid, _t0, _t1 in S.BEATS:
        fn = S.BEAT_FN[bid]
        # THE SCENE MODULE DECLARES ITS OWN SIGNATURES.  v1 hard-coded "b10 takes
        # the handle, b1 takes no media" here, which silently breaks the moment a
        # beat is split or renumbered — and the v2 rebuild splits two of them.
        if bid in getattr(S, "HANDLE_BEATS", {"b10"}):
            html, tw, sfx = fn(A, media, handle)
        elif bid in getattr(S, "NO_MEDIA", {"b1"}):
            html, tw, sfx = fn(A)
        else:
            html, tw, sfx = fn(A, media)
        scenes[bid] = (html, tw)
        sfx_all += sfx
    return scenes, sfx_all


def block(inner: str, top: float, scale: float = 1.0, eid: str = "blk") -> str:
    tf = f"transform:scale({scale});" if abs(scale - 1.0) > 1e-6 else ""
    return (f'<div class="abs" id="{eid}" style="left:0;top:{top}px;'
            f'width:{S.SCENE_W}px;height:{S.SCENE_H}px;{tf}">{inner}</div>')


def page(title: str, dur: float, body: str, tweens: list[str], css: str,
         *, width: int, height: int, zoom: int) -> str:
    z = f" zoom:{zoom};" if zoom != 1 else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width={W}, height={H}"/>
<title>{esc(title)}</title>{GSAP}{FONTS}<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden;{z}
  font-family:Poppins,sans-serif; background:{CREAM}; }}
.clip {{ position:absolute; }} .abs {{ position:absolute; }}
.disp {{ font-family:Poppins,sans-serif; }}
.mono {{ font-family:'JetBrains Mono',monospace; text-transform:uppercase; }}
{CAP.pill_rule()}
{css}
</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="{width}"
 data-height="{height}" data-duration="{dur:.3f}" data-fps="{FPS}">
{body}
</div><script>
window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});
const POP="back.out(2.05)";const SOFT="power3.out";const EXIT="power3.in";
{''.join(tweens)}
/* THE TIMELINE IS NOT PRIMED, AND THAT IS A DECISION.
   Priming (`tl.progress(1); tl.progress(0)`) is the documented cure for lazily
   recorded `to` start values — and it was tried here.  It fixed nothing visual
   and it BROKE THE AUDIO: the bed's fade-out is a `to` on the media element's
   `volume`, so priming recorded its start as the element's default 1.0 rather
   than the 0.065 the mix law sets, and rewinding then pinned the bed at full.
   Measured on that render: the 8-16 kHz band fell 5.6 dB against the voice
   master (-34.16 vs -28.55) and the encode's correlation with the cut collapsed
   from r=0.9937 to r=0.3615 — the music was drowning the voice.  The real cure
   is upstream: every property tween in `impossibletask_scene.py` is an explicit
   `fromTo`, including this one, so nothing depends on a recorded start and
   nothing has to be primed. */
window.__timelines["main"]=tl;
</script></body></html>"""


def audit_page(html: str) -> None:
    from collections import Counter
    ids = re.findall(r'\sid="([^"]+)"', html)
    dupes = sorted(k for k, v in Counter(ids).items() if v > 1)
    if dupes:
        raise SystemExit(f"duplicate ids: {dupes}")
    known = set(ids)
    script = html.split("<script>")[-1]
    missing = {sel.strip().lstrip("#")
               for m in re.finditer(r'tl\.(?:set|to|fromTo)\("([^"]+)"', script)
               for sel in m.group(1).split(",")
               if not sel.strip().startswith(".")
               and sel.strip().lstrip("#") not in known}
    if missing:
        raise SystemExit(f"tween targets that do not exist: {sorted(missing)}")


def caption_identity_guard(html: str, beats: list[dict]) -> int:
    """LAW 4: no on-screen text may repeat a caption pill verbatim."""
    def n(s):
        return " ".join(re.sub(r"[^a-z0-9 ]", " ", s.lower()).split())
    pills = {n(b["text"]) for b in beats}
    hits = 0
    for t in re.findall(r'>([^<>]{2,})</div>', html):
        if n(t) and n(t) in pills:
            raise SystemExit(f"double caption: on-screen {t!r} equals a pill verbatim")
        hits += 1
    return hits


# =============================================================================
# FORMAT 1 — CLASSIC SPLIT (YouTube)
# =============================================================================
SPLIT_SEAM = 862.5              # the published factory's own seam AND caption seat
SPLIT_FACE_H = 1057.5
SPLIT_BAND = (192.0, 779.0)     # LAW 30 top-10% line .. pill top minus clearance
SPLIT_BLK_Y = round(SPLIT_BAND[0] + (SPLIT_BAND[1] - SPLIT_BAND[0] - S.SCENE_H) / 2, 1)


def build_split(scenes, cap_beats, dur, sfx, handle_key: str) -> tuple[str, dict]:
    body = [f'  <video id="facebot" src="assets/v/face_bottom_4k.mp4" data-start="0" '
            f'data-duration="{dur:.3f}" data-media-start="0" data-track-index="1" '
            f'muted playsinline style="position:absolute;top:{SPLIT_SEAM}px;left:0;'
            f'width:{W}px;height:{SPLIT_FACE_H}px;object-fit:cover"></video>']
    tweens: list[str] = []
    for k, (bid, t0, t1) in enumerate(S.BEATS):
        end = dur if t1 is None else t1
        html, tw = scenes[bid]
        body.append(
            f'  <section id="tz-{bid}" class="clip tz" data-start="{clip_start(t0):.3f}" '
            f'data-duration="{clip_dur(t0, end, last=t1 is None):.4f}" '
            f'data-track-index="{2 + k}">'
            f'{block(html, SPLIT_BLK_Y, 1.0, eid=f"blk-{bid}")}</section>')
        tweens += tw
    body.append(caption_html(cap_beats, SPLIT_SEAM, dur))
    a_html, a_tw = audio_html(dur, sfx)
    body.append(a_html)
    tweens += a_tw
    css = (f".tz {{ left:0; top:0; width:{W}px; height:{SPLIT_SEAM}px; "
           f"overflow:hidden; background:{CREAM}; }}\n"
           f".scap {{ z-index:120; }}")
    html = page("Give your AI impossible tasks — Icon choreography", dur,
                "\n".join(body), tweens, css, width=2160, height=3840, zoom=2)
    report = {"format": "split", "seam_y": SPLIT_SEAM, "block_y": SPLIT_BLK_Y,
              "block_scale": 1.0, "caption_seat_centre": SPLIT_SEAM,
              "caption_seat_pct": round(SPLIT_SEAM / H * 100, 2),
              "face_src": "face_bottom_4k.mp4", "render": "2160x3840 @ zoom 2"}
    return html, report


# =============================================================================
# FORMAT 2 — CUTOUT (TikTok)
# =============================================================================
PLATE_W, PLATE_H = 1080.0, 900.0
CUT_MIN_CLEAR = 26.0
SEAT_EPS = 0.5
LANE_Y0, LANE_Y1 = 1120.0, 1560.0


def cutout_geometry() -> dict:
    """Everything below is DERIVED from the measured envelope and from the ENCODED
    size of the staged layers.  Nothing is typed."""
    env = json.loads(ENVELOPE.read_text())
    cut_w, cut_h = CM.probe_wh(SESSION / "matte_impossibletask_v5_cut.webm")
    rim_w, rim_h = CM.probe_wh(SESSION / "matte_impossibletask_v5_rim.webm")
    if (cut_w, cut_h) != (rim_w, rim_h):
        raise SystemExit(f"the two matte layers differ in size: "
                         f"{cut_w}x{cut_h} vs {rim_w}x{rim_h}")
    # THE BOX IS THE PLATE'S ENCODED SIZE, NOT THE SCALE (grokprice, 2026-09-01):
    # a fractional box at a sub-pixel offset makes the browser bilinear-resample
    # every frame of his face, and it cost that port 13 % of its plate's detail
    # with every geometry gate passing.
    scale = cut_h / PLATE_H
    # THE ORIGIN IS THE PLATE'S, NOT AN ASSUMPTION OF SYMMETRY.  This session
    # ships an OVER-WIDE plate — the standard LAW 44 remedy (CHASSIS.md): the
    # crop is extended on the LEFT ONLY so the plate is wider than the frame and
    # the FRAME does the cutting instead of the plate.  Its box is deliberately
    # asymmetric (1386x990 at left -252, right 1134), so `(W - cut_w)/2` would
    # place his face 99 px right of where the plate actually puts it.  The box
    # WIDTH is still the encoded size and nothing else — that is the grokprice
    # law and it is re-asserted below.
    ob = (json.loads((SESSION / "plate.json").read_text()).get("overwide")
          or {}).get("plate_box")
    if ob:
        if [float(ob["w"]), float(ob["h"])] != [float(cut_w), float(cut_h)]:
            raise SystemExit(
                f"plate.json's over-wide box is {ob['w']}x{ob['h']} but the "
                f"staged layers are {cut_w}x{cut_h} — the box must BE the "
                "encoded size.  Re-ship the matte at the plate's display size.")
        left = float(ob["left"])
    else:
        left = float(round((W - cut_w) / 2))
    top = float(H - cut_h)
    union_top = round(top + scale * float(env["union"]["y0"]), 1)
    cap_h = CAP.CAP_PILL_HEIGHT
    cap_y = round(union_top - CUT_MIN_CLEAR - cap_h / 2 - SEAT_EPS, 1)
    zy1 = round(cap_y - cap_h / 2 - CUT_MIN_CLEAR - SEAT_EPS, 1)
    zy0 = round(0.10 * H, 1)
    if zy1 - zy0 < S.SCENE_H:
        raise SystemExit(f"the stage zone {zy0}..{zy1} is {zy1 - zy0:.1f}px tall, "
                         f"under the scene block's {S.SCENE_H}px")
    return {"env": env, "box_w": float(cut_w), "box_h": float(cut_h),
            "plate_scale": round(scale, 4), "left": left, "top": top,
            "union_top": union_top, "cap_y": cap_y, "cap_h": cap_h,
            "zy0": zy0, "zy1": zy1,
            "blk_y": round(zy0 + (zy1 - zy0 - S.SCENE_H) / 2, 1)}


def guard_plate_box(g: dict) -> None:
    """The single assertion that catches the grokprice resample BEFORE the render
    rather than after it.  Four checks, because each one alone forces a resample."""
    for name, v in (("box_w", g["box_w"]), ("box_h", g["box_h"]),
                    ("left", g["left"]), ("top", g["top"])):
        if abs(v - round(v)) > 1e-9:
            raise SystemExit(f"plate box: {name}={v} is not a whole pixel — the "
                             "browser will resample his face for the whole take")
    if abs(g["box_h"] - PLATE_H * g["plate_scale"]) > 0.001:
        raise SystemExit("plate box: box_h != PLATE_H * PLATE_SCALE")


def depth_field(g: dict, media: dict, words: list[dict], dur: float):
    """THE BACKGROUND, AND IT IS NOT THIS FILE'S TO INVENT.

    Round 1 of this build wrote its own three lanes: 78/116/**168** px tiles at
    0.72 x tile gaps, the mid and near lanes OVERLAPPING by 2 px, and ONE step
    event for a 41-second take.  Every gate passed and Miguel rejected it on
    sight -- "we used to have a beautiful regular background ... you changed the
    perspective and you changed the space".  The geometry now comes from
    `formats/cutout/lib/cutout_depthfield.py`, frozen off the approved
    grokpublish render, and only the CAST and the pop-behind are chosen here.

    The band's Y is the one thing that still has to be solved per body, and it is
    solved the foundation's way: the rigid stack is slid down the legal band and
    scored on the 5th percentile of the PER-FRAME gutter, with the seat nearest
    the foundation's own offset from the caption pill winning.
    """
    bf = json.loads((GEN / f"_df/bandframes_{VID}.json").read_text())
    cap_bottom = g["cap_y"] + g["cap_h"] / 2
    y0, seat = DF.seat(bf, cap_bottom=cap_bottom, plate_top=g["top"],
                       plate_scale=g["plate_scale"], plate_left=g["left"])
    lanes = DF.lanes_at(y0)
    beats = DF.step_beats(words, dur, n=12, fps=FPS)
    lanes_html, geom, n_tiles = DF.field(lanes, media, DEPTH, len(beats))
    tw = DF.schedule(lanes, beats)

    starts = []
    for token in POP_ON:
        hits = [float(w["start"]) for w in words if w["text"] == token]
        if len(hits) != 1:
            raise SystemExit(f"the pop-behind is keyed on {token!r}, which occurs "
                             f"{len(hits)} times -- name WHICH one")
        starts.append(hits[0])
    crossings = [(round(round((s - POP_LEAD) * FPS) / FPS, 3),
                  round(round((s - POP_LEAD + POP_SPAN) * FPS) / FPS, 3))
                 for s in starts]
    pop_html, pop_tw, pop_rep = DF.pop_behind("pop", lanes, media, POP_MARK,
                                              crossings)
    return (lanes_html + pop_html, tw + pop_tw,
            {"seat": seat, "lanes": geom, "tiles": n_tiles,
             "step_beats": beats, "pop_behind": pop_rep,
             "foundation": "formats/cutout/lib/cutout_depthfield.py "
                           "(grokpublish, approved 2026-09-01)"})



def build_cutout(scenes, cap_beats, dur, sfx, media, A, handle_key: str, words):
    g = cutout_geometry()
    guard_plate_box(g)
    lanes_html, lanes_tw, field = depth_field(g, media, words, dur)

    shadow = f"filter:drop-shadow(0 10px 26px {rgba(INK, 0.30)});"
    geo = (f'left:{g["left"]:.0f}px;top:{g["top"]:.0f}px;width:{g["box_w"]:.0f}px;'
           f'height:{g["box_h"]:.0f}px;object-fit:fill;')
    body = [
        f'  <div class="abs" id="lanes" style="left:0;top:0;width:{W}px;'
        f'height:{H}px;z-index:20">{lanes_html}</div>',
        f'  <video id="cutout-rim" class="clip" src="assets/v/matte_rim.webm" '
        f'data-start="0" data-duration="{dur:.3f}" data-media-start="0" '
        f'data-track-index="0" muted playsinline style="{geo}{shadow}'
        f'z-index:59"></video>',
        f'  <video id="cutout" class="clip" src="assets/v/matte.webm" '
        f'data-start="0" data-duration="{dur:.3f}" data-media-start="0" '
        f'data-track-index="1" muted playsinline style="{geo}z-index:60"></video>',
    ]
    tweens = list(lanes_tw)
    for k, (bid, t0, t1) in enumerate(S.BEATS):
        end = dur if t1 is None else t1
        html, tw = scenes[bid]
        body.append(
            f'  <section id="sc-{bid}" class="clip stage" data-start="{clip_start(t0):.3f}" '
            f'data-duration="{clip_dur(t0, end, last=t1 is None):.4f}" '
            f'data-track-index="{2 + k}">'
            f'{block(html, g["blk_y"], 1.0, eid=f"blk-{bid}")}</section>')
        tweens += tw
    body.append(caption_html(cap_beats, g["cap_y"], dur))
    a_html, a_tw = audio_html(dur, sfx)
    body.append(a_html)
    tweens += a_tw
    css = (f".stage {{ left:0; top:0; width:{W}px; height:{H}px; "
           f"overflow:hidden; z-index:30; }}\n.scap {{ z-index:120; }}")
    html = page("Give your AI impossible tasks — Icon choreography (cutout)", dur,
                "\n".join(body), tweens, css, width=1080, height=1920, zoom=1)
    # GLOBAL LAW 8, on the page this build is about to write to disk.  The guard
    # is only a guard if it is CALLED — that is the whole lesson of this fix.
    edge_fade = C.guard_edge_fade(html)
    CAP.assert_law12(g["cap_y"])
    report = {"format": "cutout", "plate": {
        "box": [g["box_w"], g["box_h"]], "left": g["left"], "top": g["top"],
        "plate_scale": g["plate_scale"], "integral": True},
        "envelope": {"source": Path(g["env"]["source"]).name,
                     "frames_sampled": g["env"]["frames_sampled"],
                     "union_y0_plate": g["env"]["union"]["y0"],
                     "union_top_frame": g["union_top"]},
        "stage_zone": [g["zy0"], g["zy1"]], "block_y": g["blk_y"],
        "caption_seat_centre": g["cap_y"],
        "caption_seat_pct": round(g["cap_y"] / H * 100, 2),
        "caption_bottom_pct": round((g["cap_y"] + g["cap_h"] / 2) / H * 100, 2),
        "depth_field": field,
        "depth_lane_tiles": len(re.findall(r'id="ln-\w+\d+"', lanes_html)),
        "depth_lane_wrappers": len(re.findall(r'id="lw-\w+"', lanes_html)),
        "edge_fade": edge_fade,
        "render": "1080x1920 native"}
    return html, report


# =============================================================================
# FORMAT 3 — TAKEOVER (Reels)
# =============================================================================
TK_CAP_Y = 1318.0               # the format's single seat, bottom 71.63 %
TK_BAND = (192.0, 1235.0)
TK_SCALE = 1.08
TK_BLK_Y = round(TK_BAND[0] + (TK_BAND[1] - TK_BAND[0] - S.SCENE_H * TK_SCALE) / 2
                 - S.SCENE_H * (1 - TK_SCALE) / 2, 1)
TK_LEAD = 0.18                  # ALREADY MOVING ON ARRIVAL

# The cut map.  FACE beats replace scene beats entirely -- takeover shows exactly
# ONE thing at a time and a split never exists.  b6 is the beat the face takes:
# its content survives because b7 inherits the mini token and the column at the
# same seats, which is why the scene was authored that way.
# NEW LAW (2026-09-01): **the takeover switches ONLY at beat boundaries.**
# v1's map cut face -> scene at 0.92s, which sits INSIDE beat 1 — so the Reels
# viewer never saw the job card arrive, only the second half of a build already
# in progress.  Every entry below is now a whole scene beat, and the scene was
# re-cut (b0, b11) so the face could own one.
TK_MAP = [
    ("face", 0.00, 0.92),                                        # b0
    ("b1", 0.92, 2.72), ("b2", 2.72, 4.64), ("b3", 4.64, 8.54),
    ("b4", 8.54, 11.96), ("b5", 11.96, 16.70),
    ("face", 16.70, 20.62),                                      # b6
    ("b7", 20.62, 25.38),
    ("face", 25.38, 29.44),                                      # b8
    ("b9", 29.44, 37.92),
    ("face", 37.92, 39.36),                                      # b10
    ("b11", 39.36, None),
]
# The two dropped SCENE beats are safe to drop because b7 inherits both bars from
# b6 at their exact seats and b9 inherits the rail from b8 at 76 % — the cast
# carries forward across the cut instead of being re-staged.


def build_takeover(scenes, cap_beats, dur, sfx, handle_key: str):
    body, tweens, tk_sfx = [], [], list(sfx)
    face_s = 0.0
    for k, (what, t0, t1) in enumerate(TK_MAP):
        end = dur if t1 is None else t1
        if what == "face":
            face_s += end - t0
            body.append(
                f'  <video id="face{k}" class="clip" src="assets/v/face_full_4k.mp4" '
                f'data-start="{clip_start(t0):.3f}" '
                f'data-duration="{clip_dur(t0, end, last=t1 is None):.4f}" '
                f'data-media-start="{clip_start(t0):.3f}" data-track-index="{2 + k}" muted '
                f'playsinline style="left:0;top:0;width:{W}px;height:{H}px;'
                f'object-fit:cover;z-index:10"></video>')
            if t0 > 0:
                tk_sfx.append(("reverse_air", round(t0, 2)))
            continue
        html, tw = scenes[what]
        body.append(
            f'  <section id="tk-{what}" class="clip stage" data-start="{clip_start(t0):.3f}" '
            f'data-duration="{clip_dur(t0, end, last=t1 is None):.4f}" '
            f'data-track-index="{2 + k}">'
            f'{block(html, TK_BLK_Y, TK_SCALE, eid=f"blk-{what}")}</section>')
        tweens += tw
        tk_sfx.append(("soft_whoosh", round(t0, 2)))
    body.append(caption_html(cap_beats, TK_CAP_Y, dur))
    a_html, a_tw = audio_html(dur, tk_sfx)
    body.append(a_html)
    tweens += a_tw
    css = (f".stage {{ left:0; top:0; width:{W}px; height:{H}px; "
           f"overflow:hidden; background:{CREAM}; z-index:30; }}\n"
           f".scap {{ z-index:120; }}")
    html = page("Give your AI impossible tasks — Icon choreography (takeover)", dur,
                "\n".join(body), tweens, css, width=2160, height=3840, zoom=2)
    CAP.assert_law12(TK_CAP_Y)
    runs = [round(b - a, 2) for w, a, b in
            [(w, a, dur if b is None else b) for w, a, b in TK_MAP] if w == "face"]
    report = {"format": "takeover", "cut_map": [
        {"what": w, "in": a, "out": round(dur if b is None else b, 2),
         "len": round((dur if b is None else b) - a, 2)} for w, a, b in TK_MAP],
        "face_seconds": round(face_s, 2),
        "face_pct": round(face_s / dur * 100, 2),
        "longest_face_run_s": max(runs), "peak_beat_s": 8.48,
        "caption_seat_centre": TK_CAP_Y,
        "caption_bottom_pct": round((TK_CAP_Y + CAP.CAP_PILL_HEIGHT / 2) / H * 100, 2),
        "block_y": TK_BLK_Y, "block_scale": TK_SCALE,
        "face_src": "face_full_4k.mp4 (the raw 0 % window, zero punches)",
        "render": "2160x3840 @ zoom 2"}
    return html, report


# =============================================================================
# word-boundary guard — takeover LAW: cuts land on words
# =============================================================================
def assert_beat_boundaries(edges: list[float], dur: float) -> dict:
    """THE TAKEOVER SWITCHES ONLY AT BEAT BOUNDARIES (2026-09-01).

    A word start is not enough: v1's map was word-aligned AND still cut beat 1 in
    half.  The unit of a takeover cut is a whole scene beat."""
    beat_edges = {round(t0, 2) for _b, t0, _t1 in S.BEATS}
    beat_edges |= {round(t1, 2) for _b, _t0, t1 in S.BEATS if t1 is not None}
    bad = [e for e in edges if round(e, 2) not in beat_edges and abs(e - dur) > 0.01]
    if bad:
        raise SystemExit(
            f"takeover cuts that are not BEAT boundaries: {bad} — a takeover may "
            f"never switch mid-build.  Split the beat in the scene module first.")
    return {"beat_edges_checked": len(edges), "all_on_beat_edges": True}


def assert_word_boundaries(words: list[dict], edges: list[float], dur: float) -> dict:
    starts = {round(float(w["start"]), 2) for w in words}
    starts.add(0.0)
    bad = [e for e in edges if round(e, 2) not in starts and abs(e - dur) > 0.01]
    if bad:
        raise SystemExit(f"takeover cuts that are not on a word boundary: {bad}")
    return {"edges_checked": len(edges), "all_on_word_starts": True}


# =============================================================================
def main(only: set[str] | None = None) -> None:
    words = load_words()
    A = anchor_fn(words)
    dur = round(probe_dur(CUT / "master.mp4"), 3)
    tdur = round(float(words[-1]["end"]), 3)
    if dur < tdur:
        raise SystemExit(f"container {dur}s is shorter than the last word {tdur}s")

    cap_beats, measurer = build_captions(words)
    widest = max(measurer.width(b["text"]) for b in cap_beats)
    if widest > CAP.SEAT_MAX_W + 0.6:
        raise SystemExit(f"widest pill {widest:.1f}px exceeds the {CAP.SEAT_MAX_W}px seat")

    reports = {}
    projects = RUN / "projects"
    for key, fmt, handle_key in (("split", "split", "yt"),
                                 ("cutout", "cutout", "tiktok_ig"),
                                 ("takeover", "takeover", "tiktok_ig")):
        if only and key not in only:
            continue
        C.BOXES.clear()
        stage_dir = RUN / f"stage/{VID}_{key}"
        media, voice = stage(stage_dir,
                      need_face=("face_bottom_4k.mp4" if key == "split" else
                                 "face_full_4k.mp4" if key == "takeover" else None),
                      need_matte=(key == "cutout"))
        handle = CAP.handle(handle_key)
        scenes, sfx = build_scene(A, media, handle)
        if key == "split":
            html, rep = build_split(scenes, cap_beats, dur, sfx, handle_key)
        elif key == "cutout":
            html, rep = build_cutout(scenes, cap_beats, dur, sfx, media, A,
                                     handle_key, words)
        else:
            html, rep = build_takeover(scenes, cap_beats, dur, sfx, handle_key)
            rep["word_boundaries"] = assert_word_boundaries(
                words, [t for _w, t, _e in TK_MAP], dur)
            rep["beat_boundaries"] = assert_beat_boundaries(
                [t for _w, t, _e in TK_MAP], dur)
        audit_page(html)
        caption_identity_guard(html, cap_beats)
        if handle not in html:
            raise SystemExit(f"{key}: the outro handle {handle} is not in the page")
        other = CAP.HANDLE_YT if handle == CAP.HANDLE_TIKTOK_IG else CAP.HANDLE_TIKTOK_IG
        if other in html:
            raise SystemExit(f"{key}: the OTHER platform's handle {other} leaked in")
        proj = projects / f"{VID}_{key}"
        bind(proj, stage_dir)
        (proj / "index.html").write_text(html, encoding="utf-8")
        rep.update({
            "project": str(proj), "handle": handle, "handle_key": handle_key,
            "duration_s": dur, "fps": FPS,
            "html_bytes": len(html.encode()),
            "atoms": len(C.BOXES),
            "captions": len(cap_beats),
            "caption_font_px": CAP.CAP_FONT,
            "caption_pill_height_px": CAP.CAP_PILL_HEIGHT,
            "widest_pill_px": round(widest, 1),
            "caption_sizes_in_page": sorted(set(re.findall(
                r'\.scappill[^}]*font-size:([0-9.]+)px', html))),
            "voice": voice,
        })
        reports[key] = rep
        print(f"BUILT {key:9s} {rep['html_bytes']:>7d} bytes  "
              f"captions={len(cap_beats)}  handle={handle}")

    reports["shared"] = {
        "scene_module": S.__name__ + ".py",
        # v3 — S1..S4.  `build_scene` runs once per format, so the declarations
        # are deduplicated by (beat, name) before the audit; a scene that breaks
        # a spacing law never reaches this line, because `audit_spacing` raises.
        "spacing_audit": S.audit_spacing(),
        "source_card": json.loads((RUN / "plans/x_card_impossibletask.json")
                                  .read_text()),
        "scene_block": [S.SCENE_W, S.SCENE_H],
        "beats": len(S.BEATS),
        "anchors_used": sorted(A.used),           # type: ignore[attr-defined]
        "sfx_cues": len(sfx),
        "sfx_classes": {n: S.SFX_CLASS[n] for n in sorted({s[0] for s in sfx})},
        "transcript_words": len(words),
        "duration_s": dur, "transcript_end_s": tdur,
        "measurer": measurer.report(),
    }
    out = GEN / (f"_geom_{VID}.json" if not only
                 else f"_geom_{VID}_{'-'.join(sorted(only))}.json")
    out.write_text(json.dumps(reports, indent=1))
    print(f"-> {out}")


if __name__ == "__main__":
    # `--formats split takeover` renders a SUBSET.  It exists so a semantic
    # rebuild can re-render its own formats without stepping on a sibling
    # session that owns another one (run 9's cutout rebuild).
    argv = sys.argv[1:]
    sel: set[str] | None = None
    if "--formats" in argv:
        sel = set(argv[argv.index("--formats") + 1:])
        bad = sel - {"split", "cutout", "takeover"}
        if bad:
            raise SystemExit(f"unknown format(s): {sorted(bad)}")
    main(sel)
