"""CUTOUT COMMENTARY — shared chassis for the format-lab prototype.

FORMAT: Miguel's matted silhouette (background removed from `face_full.mp4`)
stands IN FRONT of a full-bleed 1080x1920 explainer world.  News-commentator
staging: the scene is not beside him and not under him, it is BEHIND him.

Three variants share this file and differ only in `Stage` (how big he is, where
his silhouette sits) and in their own scene functions:
    v1 ANCHOR      k=0.52  bottom-third bust, the story plays above him
    v2 IMMERSED    k=0.88  large, scene elements travel BEHIND him (parallax)
    v3 INTERACTIVE k=0.62  mid, elements dock at his head / shoulder line

WHAT IS DERIVED, NEVER TYPED
----------------------------
The whole point of this format is that the scene has to stay legible around a
silhouette whose bounds MOVE.  `matte/envelope.json` (written by
`cutout_measure_matte.py`) carries the union silhouette in 48 horizontal bands,
sampled at 2 fps over the whole take.  `Stage.hits()` transforms those bands
into frame coordinates for a given scale and answers "does this box touch him
on ANY frame".  Every scene atom is recorded and swept:

  * a FRONT atom that hits the silhouette is a BUILD ERROR (his no-occlusion
    rule);
  * a BEHIND atom is allowed to be covered — that is the depth illusion, and
    it must be declared, so v2's parallax is explicit rather than accidental;
  * the caption pill is chrome, allowed over the TORSO, and asserted to clear
    the head band by CAP_HEAD_CLEAR px.

FACTORY LANGUAGE (STANDARD.md) reused unchanged: the cream/ink/terra palette,
the Nunito caption pill, Poppins display + JetBrains Mono kickers, the
`@migueltorrezai` outro chip, the audio mix law (voice 1 / bed 0.065 / sfx
0.18), no drawn faces, colour brand marks, underline = ink width.
"""
from __future__ import annotations
import sys as _asset_sys
from pathlib import Path as _AssetPath
_asset_sys.path.insert(0, str(next(p for p in _AssetPath(__file__).resolve().parents if (p / "execution/asset_library.py").is_file()) / "execution"))
from asset_library import resolve_source as library_asset, source_files as library_files


import html as ihtml
import json
import math
import re
import shutil
import subprocess
from pathlib import Path

WORKSPACE = Path.home() / "Documents/Workspace"
FACTORY = WORKSPACE / "projects/personal/content/shorts-factory"
LAB = FACTORY / "formats/cutout/source"      # round-6 source material, READ ONLY  # frozen lab inputs, moved out of the format lab (archived) 2026-09-20 (MANIFEST.sha256 beside them)
SRC = FACTORY / "formats/_shared/hermesinfinite"  # the cut + transcript, READ ONLY

# --- CHASSIS PARAMETERS (promoted out of the lab, 2026-09-01) ----------------
# The lab is history.  Projects land under `formats/cutout/`; the caption canon
# comes from `pipeline/captions.py`; the matte is a chassis INPUT (see
# `chassis_gen.py --matte` and `pipeline/sam2/`).
import sys                                                     # noqa: E402
sys.path.insert(0, str(FACTORY / "pipeline"))
import captions as CAP                                         # noqa: E402

CHASSIS = Path(__file__).resolve().parent.parent
OUT_ROOT = CHASSIS / "build"    # where projects land.  Never the lab.
OUTRO_HANDLE = CAP.handle()     # the outro chip text
LOGOS = WORKSPACE / "assets/logos"

FPS = 30
W, H = 1080, 1920
AX = 540.0                    # composition axis
MARGIN = 54.0                 # frame margin, nothing crosses it
COL_X, COL_W = 60.0, 960.0    # content column

# ---- palette (factory) ------------------------------------------------------
CREAM = "#F6F1EA"
INK = "#141416"
INK_2 = "#242427"
MUTED = "#716B63"
MUTED_D = "#9A948B"
TERRA = "#C4573A"
TERRA_2 = "#E68569"
WHITE = "#FFFDF9"
PAPER = "#FFFFFF"

# ---- type scale, px at 1080 native ------------------------------------------
DISP = 112.0
H1 = 76.0
H2 = 54.0
LBL = 27.0
MICRO = 21.0
HANDLE = 56.0
RULE_H = 11.0

# ---- audio mix law (Miguel, 2026-08-17) -------------------------------------
VOICE_VOLUME = "1"
BED_VOLUME = "0.065"
SFX_VOLUME = "0.18"

# ---- caption band -----------------------------------------------------------
CAP_Y = 1652.0                # pill vertical CENTRE
CAP_HEAD_CLEAR = 90.0         # px the pill must clear the silhouette head band

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800'
    '&family=Nunito:wght@800&family=JetBrains+Mono:wght@400;500;700&display=block" '
    'rel="stylesheet">'
)
GSAP = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>'

# uppercase advance estimates, em — build-time width guards only
ADV_POPPINS = 0.66
ADV_MONO = 0.62


# =============================================================================
# helpers
# =============================================================================
def esc(v: object) -> str:
    return ihtml.escape(str(v), quote=False)


def norm(s: str) -> list[str]:
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()


def rgb(hex_color: str) -> str:
    v = hex_color.lstrip("#")
    return f"rgb({int(v[0:2], 16)},{int(v[2:4], 16)},{int(v[4:6], 16)})"


def rgba(hex_color: str, alpha: float) -> str:
    v = hex_color.lstrip("#")
    return f"rgba({int(v[0:2], 16)},{int(v[2:4], 16)},{int(v[4:6], 16)},{alpha})"


def rad(w: float, h: float) -> float:
    return round(min(48.0, max(18.0, 0.17 * min(w, h))), 1)


def centered(w: float) -> float:
    return round(AX - w / 2, 1)


def fits(text: str, box_w: float, fs: float, ls: float = 0.0, mono: bool = False) -> bool:
    adv = ADV_MONO if mono else ADV_POPPINS
    return len(text) * (adv * fs + ls) <= box_w


def probe(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
         str(path)], check=True, capture_output=True, text=True).stdout.strip()
    return float(out)


# =============================================================================
# THE STAGE — where Miguel is, and therefore where the scene may not be
# =============================================================================
class Stage:
    """The cutout's placement plus the derived no-go map.

    The matte is `face_full.mp4` background-removed: a 1080x1920 close-up whose
    silhouette already touches the left/right frame edges below the shoulder
    line.  Scaling it by k about the FRAME BOTTOM keeps the shoulder crop
    reading as "cropped by the bottom of the frame" rather than as a floating
    sticker with a straight-cut hem.
    """

    def __init__(self, k: float, envelope: Path | None = None, dx: float = 0.0):
        """`dx` slides him off the frame axis.  Centring a presenter splits the
        free space into two channels too narrow to hold anything: measured at
        k=0.62, a centred Miguel leaves ~150px on each side at head height,
        which caps a docked plate at 125px — sticker-sized.  Sliding him 80px
        right collapses that into ONE 230px channel on his left, which is what
        a news over-the-shoulder graphic has always been."""
        self.k = k
        self.dx = dx
        self.box_w = round(W * k, 1)
        self.box_h = round(H * k, 1)
        self.left = round((W - self.box_w) / 2 + dx, 1)
        self.top = round(H - self.box_h, 1)
        env = json.loads((envelope or (LAB / "matte/envelope.json")).read_text())
        self.env = env
        self.bands = [b for b in env["bands"] if b["x0"] is not None]
        self.head_top = round(self.top + k * env["union"]["y0"], 1)
        self.head_bot = round(self.top + k * env["head"]["y1"], 1)
        self.head_x0 = round(self.left + k * env["head"]["x0"], 1)
        self.head_x1 = round(self.left + k * env["head"]["x1"], 1)

    # -- silhouette query ----------------------------------------------------
    def span(self, y: float) -> tuple[float, float] | None:
        """Frame-space x extent of the silhouette union at frame-space y."""
        ys = (y - self.top) / self.k
        for b in self.bands:
            if b["y0"] <= ys < b["y1"]:
                return (round(self.left + self.k * b["x0"], 1),
                        round(self.left + self.k * b["x1"], 1))
        return None

    def hits(self, x: float, y: float, w: float, h: float, pad: float = 22.0) -> bool:
        """Does this box touch the silhouette on ANY sampled frame?"""
        step = max(6.0, self.k * (H / 48) / 3)
        yy = y - pad
        while yy <= y + h + pad:
            s = self.span(yy)
            if s and not (x + w + pad <= s[0] or x - pad >= s[1]):
                return True
            yy += step
        return False

    def free_top(self) -> float:
        """Lowest y that is still fully clear of him across the full width."""
        return self.head_top

    def gutters(self, y: float, pad: float = 22.0) -> tuple[tuple[float, float], tuple[float, float]]:
        """(left, right) free x-ranges at frame-space y."""
        s = self.span(y)
        if s is None:
            return (0.0, float(W)), (0.0, float(W))
        return (0.0, round(s[0] - pad, 1)), (round(s[1] + pad, 1), float(W))

    def band_gutters(self, y0: float, y1: float, pad: float = 22.0):
        """Worst-case (narrowest) gutters over a y band — what a dock must fit."""
        lo_r, hi_l = W, 0.0
        yy = y0
        while yy <= y1:
            (_, lr), (rl, _) = self.gutters(yy, pad)
            lo_r = min(lo_r, lr)
            hi_l = max(hi_l, rl)
            yy += 8.0
        return (0.0, round(lo_r, 1)), (round(hi_l, 1), float(W))

    def video(self, dur: float, src: str = "assets/v/matte.webm",
              shadow: bool = True, z: int = 60, stroke: float = 4.0,
              stroke_color: str = WHITE) -> str:
        """ONE drop-shadow, and nothing else.

        MEASURED COST (this is the finding of the whole prototype): the die-cut
        sticker rim was first authored as a stack of eight zero-blur
        `drop-shadow()`s on the <video>.  Chromium re-runs that filter chain on
        every composited frame of a 1080x1920 video and the render went from
        ~4.5 min to a projected 3+ HOURS for the same 54s.  The rim is now BAKED
        into the matte by ffmpeg (`cutout_matte_stroked.webm`: alpha dilated 5x,
        filled cream, original overlaid), which costs one 60-second offline pass
        and zero per-frame work.  Never put a filter STACK on a full-frame video
        element in this framework."""
        sh = (f"filter:drop-shadow(0 {round(10 * self.k)}px {round(26 * self.k)}px "
              f"{rgba(INK, 0.30)});" if shadow else "")
        return (
            f'  <video id="cutout" class="clip" src="{src}" data-start="0" '
            f'data-duration="{dur:.3f}" data-media-start="0" data-track-index="1" '
            f'muted playsinline style="left:{self.left}px;top:{self.top}px;'
            f'width:{self.box_w}px;height:{self.box_h}px;object-fit:fill;{sh}z-index:{z}"></video>'
        )


# =============================================================================
# geometry recorder + occlusion guard
# =============================================================================
BOXES: list[dict] = []
EVENTS: list[float] = []


def rec(eid: str, x: float, y: float, w: float, h: float, *, behind: bool = False,
        chrome: bool = False) -> None:
    BOXES.append({"id": eid, "x": x, "y": y, "w": w, "h": h,
                  "behind": behind, "chrome": chrome})


def guard_stage(stage: Stage) -> dict:
    """FRONT atoms may not touch him; every atom stays inside the frame."""
    front_hits, off_frame = [], []
    for b in BOXES:
        if b["behind"] or b["chrome"]:
            # a parallax lane is WIDER than the frame on purpose — it is clipped
            # by #root's overflow and by him, which is the whole point
            continue
        if b["x"] < -20 or b["x"] + b["w"] > W + 20 or b["y"] < -20 or b["y"] + b["h"] > H + 20:
            off_frame.append(b["id"])
        if b["x"] < MARGIN - 0.6 or b["x"] + b["w"] > W - MARGIN + 0.6:
            off_frame.append(b["id"] + " (margin)")
        if stage.hits(b["x"], b["y"], b["w"], b["h"]):
            front_hits.append(b["id"])
    if front_hits:
        raise SystemExit(
            "OCCLUSION: front atoms overlap the silhouette envelope — "
            f"{sorted(set(front_hits))}")
    if off_frame:
        raise SystemExit(f"FRAME: atoms outside the safe frame — {sorted(set(off_frame))}")
    behind = [b["id"] for b in BOXES if b["behind"]]
    return {"atoms": len(BOXES), "behind": len(behind), "behind_ids": behind}


def guard_caption_band(stage: Stage, cap_h: float) -> None:
    top = CAP_Y - cap_h / 2
    if top < stage.head_bot + CAP_HEAD_CLEAR:
        raise SystemExit(
            f"caption band top {top:.0f} is within {CAP_HEAD_CLEAR}px of the head "
            f"band bottom {stage.head_bot:.0f} — the pill would crowd his face")


# =============================================================================
# atoms
# =============================================================================
def div(eid: str, x: float, y: float, w: float, h: float, style: str = "",
        cls: str = "abs", z: int | None = None, extra: str = "") -> str:
    zz = f"z-index:{z};" if z is not None else ""
    return (f'<div class="{cls}" id="{eid}"{extra} style="left:{x}px;top:{y}px;'
            f'width:{w}px;height:{h}px;{zz}{style}"></div>')


def txt(eid: str, y: float, text: str, fs: float, *, color: str = INK, weight: int = 800,
        ls: float = 0.0, mono: bool = False, x: float = COL_X, w: float = COL_W,
        align: str = "center", upper: bool = True, z: int | None = None,
        lh: float = 1.30) -> str:
    """A centred type atom.  `text-align:center` counts the TRAILING letter-space
    as advance but never paints it, so a tracked centred string sits ls/2 left of
    its own axis — `text-indent:ls` cancels it (factory finding)."""
    cls = "abs mono" if mono else "abs disp"
    tt = "" if upper else "text-transform:none;"
    indent = f"text-indent:{ls}px;" if (align == "center" and ls) else ""
    zz = f"z-index:{z};" if z is not None else ""
    return (f'<div class="{cls}" id="{eid}" style="left:{x}px;top:{y}px;width:{w}px;'
            f'height:{round(lh * fs, 1)}px;text-align:{align};font-size:{fs}px;'
            f'line-height:{round(lh * fs, 1)}px;letter-spacing:{ls}px;{indent}'
            f'font-weight:{weight};color:{color};{tt}{zz}">{esc(text)}</div>')


def txt_h(fs: float, lh: float = 1.30) -> float:
    return round(lh * fs, 1)


def svg(eid: str, x: float, y: float, w: float, h: float, body: str,
        vb: tuple[float, float] | None = None, z: int | None = None) -> str:
    """positioned atoms are DIVs; svg lives INSIDE (a bare positioned <svg>
    is not a string-classed element and breaks tooling)."""
    vw, vh = vb or (w, h)
    zz = f"z-index:{z};" if z is not None else ""
    return (f'<div class="abs" id="{eid}" style="left:{x}px;top:{y}px;'
            f'width:{w}px;height:{h}px;{zz}">'
            f'<svg viewBox="0 0 {vw} {vh}" width="100%" height="100%">{body}</svg></div>')


def rule(eid: str, y: float, w: float, color: str = TERRA, z: int | None = None) -> str:
    return div(eid, centered(w), y, w, RULE_H,
               f"background:{color};border-radius:{RULE_H / 2}px;transform-origin:center center;", z=z)


# ---- plates -----------------------------------------------------------------
MARK_INK: dict[str, dict[str, float]] = {}


def measure_mark(key: str, path: Path) -> dict[str, float]:
    from io import BytesIO
    from PIL import Image
    if path.suffix == ".svg":
        import cairosvg
        image = Image.open(BytesIO(cairosvg.svg2png(url=str(path), output_width=1024)))
    else:
        image = Image.open(path)
    image = image.convert("RGBA")
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise SystemExit(f"{key}: artwork rasterises empty")
    x0, y0, x1, y1 = bbox
    w, h = image.size
    return {"img_w": float(w), "img_h": float(h),
            "bbox_w": float(x1 - x0), "bbox_h": float(y1 - y0),
            "off_x": float((x0 + x1) / 2 - w / 2), "off_y": float((y0 + y1) / 2 - h / 2),
            "aspect": (x1 - x0) / (y1 - y0)}


def mark_img(src: str, key: str, side: float, *, eid: str | None = None,
             opacity: float | None = None, extra: str = "") -> str:
    """An <img> whose INK is `side` on a side BY AREA, centred in its parent.

    Marks in this cast span ink aspects 0.55 (nous girl) to 1.33 (Gmail); a
    square box with object-fit:contain would paint them at wildly different
    optical weights.  Sizing by ink area keeps a row of marks even.  The ink
    centroid offset is corrected too, so centring the box centres the INK.

    Put an animated mark directly in its plate with ``eid`` / ``opacity`` /
    ``extra``.  Do not wrap it in a fixed ``left`` / ``top`` slot: absolute
    offsets start at a bordered parent's padding edge, so a nominally centred
    slot moves by exactly the border width.  The percentage centre here is the
    bordered box's centre and remains the mark's centre while GSAP scales it.
    Calls without the optional attributes keep their legacy HTML byte-for-byte.
    """
    m = MARK_INK[key]
    ink_w = side * math.sqrt(m["aspect"])
    box_w = ink_w * m["img_w"] / m["bbox_w"]
    box_h = box_w * m["img_h"] / m["img_w"]
    dx = -m["off_x"] * box_w / m["img_w"]
    dy = -m["off_y"] * box_h / m["img_h"]
    attrs = ""
    if eid:
        attrs += f' id="{eid}"'
    if extra:
        attrs += " " + extra.strip()
    opacity_css = "" if opacity is None else f"opacity:{opacity:g};"
    return (f'<img{attrs} src="{src}" alt="" style="position:absolute;left:50%;top:50%;'
            f'width:{box_w:.2f}px;height:{box_h:.2f}px;object-fit:contain;display:block;'
            f'{opacity_css}transform:translate(-50%,-50%) '
            f'translate({dx:.2f}px,{dy:.2f}px)"/>')


def plate(eid: str, x: float, y: float, w: float, h: float, *, kids: str = "",
          fill: str = PAPER, border: str = None, bw: float = 3.0,
          z: int | None = None, style: str = "", cls: str = "abs node") -> str:
    b = border or rgba(INK, 0.14)
    zz = f"z-index:{z};" if z is not None else ""
    return (f'<div class="{cls}" id="{eid}" style="left:{x}px;top:{y}px;width:{w}px;'
            f'height:{h}px;background:{fill};border:{bw}px solid {b};'
            f'border-radius:{rad(w, h)}px;{zz}{style}">{kids}</div>')


def tool_plate(eid: str, x: float, y: float, size: float, src: str, key: str, *,
               ink: float = None, z: int | None = None, dim: bool = False) -> str:
    """A tool tile: the brand mark in ITS OWN colours (Law 12) on a white plate."""
    ink = ink or round(size * 0.52, 1)
    op = "opacity:1;" if not dim else "opacity:1;"
    return plate(eid, x, y, size, size, kids=mark_img(src, key, ink), z=z,
                 style=f"{op}display:block;")


def blank_plate(eid: str, x: float, y: float, size: float, z: int | None = None) -> str:
    """An anonymous tool tile — the shelf is bigger than the cast of real logos.
    Drawn as a plate with a small neutral glyph so it is never an EMPTY vessel."""
    g = size * 0.30
    kids = (f'<div style="position:absolute;left:50%;top:50%;width:{g:.1f}px;'
            f'height:{g:.1f}px;transform:translate(-50%,-50%);border-radius:{g * 0.28:.1f}px;'
            f'background:{rgba(INK, 0.16)}"></div>')
    return plate(eid, x, y, size, size, kids=kids, z=z)


# =============================================================================
# GLOBAL LAW 8 — EDGE FADE.  Shared, because it was NOT shared and that is
# exactly how run 9 shipped two hard-chopped depth bands.
# =============================================================================
# 46px = one third of a shelf tile (132), the largest fade that still leaves
# half a tile at full opacity.  The number lives here now; the cutout chassis
# re-exports it so the two can never drift.
EDGE_FADE = 46.0


def hmask(fade: float = EDGE_FADE, w: float = W) -> str:
    """A horizontal alpha fade at BOTH ends of a clipping container."""
    g = (f"linear-gradient(90deg,rgba(0,0,0,0) 0px,rgba(0,0,0,1) {fade}px,"
         f"rgba(0,0,0,1) {w - fade}px,rgba(0,0,0,0) {w}px)")
    return f"-webkit-mask-image:{g};mask-image:{g};"


def vmask(fade: float = EDGE_FADE) -> str:
    """A vertical alpha fade at both ends of a clipping container."""
    g = (f"linear-gradient(180deg,rgba(0,0,0,0) 0px,rgba(0,0,0,1) {fade}px,"
         f"rgba(0,0,0,1) calc(100% - {fade}px),rgba(0,0,0,0) 100%)")
    return f"-webkit-mask-image:{g};mask-image:{g};"


def lane_wrap(eid: str, y: float, h: float, cells: str, *,
              fade: float = EDGE_FADE, w: float = W, x: float = 0.0) -> str:
    """THE canonical depth-lane wrapper.  A lane strip is wider than the canvas
    by design, so its tiles are cut BY THE FRAME EDGE; the wrapper is exactly
    canvas width, carries the fade, and the tiles inside it are authored in the
    wrapper's own LOCAL coordinates (top 0) so the step tweens are unchanged.

    Depth lanes MUST come through here.  Tiles parented straight to a full-frame
    layer have no cut container to hang a mask on, the guard below has nothing
    to fail, and the band ships hard-chopped."""
    return (f'<div class="abs lanewrap" id="{eid}" style="left:{x}px;top:{y}px;'
            f'width:{w}px;height:{h}px;overflow:hidden;{hmask(fade, w)}">'
            f'{cells}</div>')


def guard_edge_fade(html: str, *, exempt: set[str] | frozenset[str] = frozenset(),
                    exempt_prefixes: tuple[str, ...] = ()) -> dict:
    """GLOBAL LAW 8, measured on the EMITTED HTML.

    Every clipping container must carry an alpha mask; a container with
    `overflow:hidden` and no mask is a hard chop and fails the build.

    Exempt by construction, each for a stated reason:
      root / the section clips  the frame itself and the per-beat clips — they
            cut nothing that the frame edge has not already cut
      lanes  the layer that HOLDS the faded lane wrappers
      meters a rounded meter's inner clip exists to hold the FILL inside the
            track's radius (Law 11); fading it would fade the pill's own cap.
            Detected structurally, by the `<id>-fill` child every meter emits,
            so a new meter never has to be added to a list.
    """
    meters = {m for m in re.findall(r'id="([^"]+)-fill"', html)}
    exempt = {"root", "lanes"} | set(exempt) | meters
    prefixes = ("tz-", "sc-") + tuple(exempt_prefixes)
    parts = html.split("overflow:hidden")
    unmasked = []
    for i, seg in enumerate(parts[:-1]):
        head = seg[-400:]
        tail = parts[i + 1][:400]
        if 'id="' not in head:            # a CSS rule, not an element
            continue
        eid = head.split('id="')[-1].split('"')[0]
        if eid in exempt or eid.startswith(prefixes):
            continue
        if "mask-image" not in tail and "mask-image" not in head:
            unmasked.append(eid)
    if unmasked:
        raise SystemExit(f"GLOBAL LAW 8: clipping containers with a hard edge — "
                         f"{sorted(set(unmasked))}")
    return {"masked_containers": html.count("mask-image:linear-gradient") // 2,
            "fade_px": EDGE_FADE, "meters_exempt": sorted(meters)}


# =============================================================================
# transcript / captions
# =============================================================================
FILLERS = {"uh", "um", "erm", "eh"}
GLUE = {("the", "code"), ("procedural", "disclosure"), ("nous", "research"),
        ("mcp", "servers"), ("hermes", "agent"), ("all", "at"), ("at", "once")}


def load_words() -> tuple[list[dict], float]:
    data = json.loads((SRC / "transcript_words.json").read_text())
    words = [w for w in data["words"] if w.get("type") == "word"]
    return words, float(data["duration"])


def clean_tokens(words: list[dict]) -> list[dict]:
    out: list[dict] = []
    for i, word in enumerate(words):
        text = word["text"].strip()
        if text.endswith("-"):
            continue
        if re.sub(r"[^a-z]", "", text.lower()) in FILLERS and len(text) <= 4:
            continue
        nxt = words[i + 1] if i + 1 < len(words) else None
        if (nxt and re.sub(r"[^a-z0-9]", "", text.lower())
                == re.sub(r"[^a-z0-9]", "", nxt["text"].lower())
                and nxt["start"] - word["end"] < 0.5):
            continue
        out.append(word)
    return out


def build_captions(words: list[dict]) -> list[dict]:
    phrases, cur = [], []
    words = clean_tokens(words)
    for i, word in enumerate(words):
        cur.append(word)
        nxt = words[i + 1] if i + 1 < len(words) else None
        pair = None
        if nxt:
            pair = (re.sub(r"[^a-z0-9]", "", word["text"].lower()),
                    re.sub(r"[^a-z0-9]", "", nxt["text"].lower()))
        punct = bool(re.search(r"[.,!?]$", word["text"]))
        gap = bool(nxt and nxt["start"] - word["end"] > 0.32)
        if pair in GLUE and len(cur) < 5:
            continue
        if len(cur) >= 4 or (punct and len(cur) >= 2) or gap or nxt is None:
            phrases.append({"t0": round(cur[0]["start"], 2),
                            "t1": round(word["end"] + 0.12, 2),
                            "text": " ".join(x["text"] for x in cur), "n": len(cur)})
            cur = []
    merged = []
    for p in phrases:
        if p["n"] == 1 and merged:
            merged[-1]["text"] += " " + p["text"]
            merged[-1]["t1"] = p["t1"]
            merged[-1]["n"] += 1
            continue
        merged.append(dict(p))
    for i in range(len(merged) - 1):
        merged[i]["t1"] = merged[i + 1]["t0"]
    return merged


def cap_font(text: str) -> float:
    return round(max(35.0, min(54.0, (COL_W - 70) / (0.575 * max(1, len(text))))), 1)


def cap_height() -> float:
    return round(1.30 * 54.0 + 2 * 19, 1)


def caption_clips(phrases: list[dict], dur: float) -> str:
    clips = []
    for i, p in enumerate(phrases):
        t0, t1 = p["t0"], min(p["t1"], dur)
        if t1 - t0 < 0.08 or t0 >= dur:
            continue
        clips.append(
            f'  <div id="cap{i}" class="clip scap" style="top:{CAP_Y}px" '
            f'data-start="{t0:.2f}" data-duration="{t1 - t0:.2f}" data-track-index="25">'
            f'<span class="scappill" style="font-size:{cap_font(p["text"])}px">'
            f'{esc(p["text"])}</span></div>')
    return "\n".join(clips)


def anchor_finder(words: list[dict]):
    def find(phrase: str) -> float:
        target = norm(phrase)
        for i in range(len(words)):
            raw = []
            for j in range(i, min(len(words), i + len(target) + 3)):
                raw.append(words[j]["text"])
                candidate = norm(" ".join(raw))
                if candidate == target:
                    return round(words[i]["start"], 2)
                if len(candidate) > len(target):
                    break
        raise SystemExit(f"anchor not found: {phrase!r}")
    return find


# =============================================================================
# tweens (shared vocabulary)
# =============================================================================
def pop(sel: str, t: float, d: float = 0.40, y: float = 26.0) -> str:
    return (f'tl.set("{sel}",{{opacity:0}},0);'
            f'tl.fromTo("{sel}",{{opacity:0,scale:0.88,y:{y}}},{{opacity:1,scale:1,y:0,'
            f'duration:{d:.2f},ease:POP,immediateRender:false}},{t:.2f});')


def settle(sel: str, t: float, d: float = 0.46, s: float = 0.93) -> str:
    return (f'tl.set("{sel}",{{opacity:0}},0);'
            f'tl.fromTo("{sel}",{{opacity:0,scale:{s}}},{{opacity:1,scale:1,'
            f'duration:{d:.2f},ease:SOFT,immediateRender:false}},{t:.2f});')


def fade(sel: str, t: float, d: float = 0.30, to: float = 1.0) -> str:
    return (f'tl.set("{sel}",{{opacity:0}},0);'
            f'tl.to("{sel}",{{opacity:{to},duration:{d:.2f},ease:SOFT}},{t:.2f});')


def fade_out(sel: str, t: float, d: float = 0.30, to: float = 0.0) -> str:
    return f'tl.to("{sel}",{{opacity:{to},duration:{d:.2f},ease:EXIT}},{t:.2f});'


def grow(sel: str, t: float, d: float = 0.40, origin: str = "left center") -> str:
    return (f'tl.set("{sel}",{{scaleX:0,transformOrigin:"{origin}"}},0);'
            f'tl.to("{sel}",{{scaleX:1,duration:{d:.2f},ease:SOFT}},{t:.2f});')


def slide_in(sel: str, t: float, dx: float, d: float = 0.44) -> str:
    return (f'tl.set("{sel}",{{opacity:0,x:{dx}}},0);'
            f'tl.to("{sel}",{{opacity:1,x:0,duration:{d:.2f},ease:SOFT}},{t:.2f});')


def hot(sel: str, t: float, color: str = TERRA, d: float = 0.24) -> str:
    return f'tl.to("{sel}",{{borderColor:"{rgb(color)}",duration:{d:.2f},ease:SOFT}},{t:.2f});'


def cool(sel: str, t: float, d: float = 0.28, alpha: float = 0.14) -> str:
    return f'tl.to("{sel}",{{borderColor:"{rgba(INK, alpha)}",duration:{d:.2f},ease:SOFT}},{t:.2f});'


def dim(sel: str, t: float, to: float = 0.30, d: float = 0.28) -> str:
    return f'tl.to("{sel}",{{opacity:{to},duration:{d:.2f},ease:SOFT}},{t:.2f});'


def tick(sel: str, t: float, s: float = 1.06, d: float = 0.30) -> str:
    return (f'tl.to("{sel}",{{scale:{s},duration:{d / 2:.2f},ease:"power2.out"}},{t:.2f});'
            f'tl.to("{sel}",{{scale:1,duration:{d / 2:.2f},ease:"power2.in"}},{t + d / 2:.2f});')


# =============================================================================
# audio
# =============================================================================
def audio_block(dur: float, sfx: list[tuple[str, float]]) -> tuple[str, list[str]]:
    """AUDIO MIX LAW: voice 1, bed 0.065, SFX 0.18 — constants, not parameters."""
    els = [f'  <audio id="vo" src="assets/v/voice.m4a" data-start="0" '
           f'data-duration="{dur:.3f}" data-track-index="30" data-volume="{VOICE_VOLUME}"></audio>']
    bed_len = probe(library_asset(Path.home() / "Documents/Workspace/assets/audio/music/shorts-factory/bed_split_v2.mp3"))
    starts, t, i = [], 0.0, 0
    while t < dur - 0.1:
        d = min(bed_len, dur - t)
        starts.append((f"bg{i}", t))
        els.append(f'  <audio id="bg{i}" src="assets/music/bed_split.mp3" '
                   f'data-start="{t:.2f}" data-duration="{d:.2f}" '
                   f'data-track-index="{31 + i}" data-volume="{BED_VOLUME}"></audio>')
        t += bed_len
        i += 1
    for j, (name, t0) in enumerate(sfx):
        if t0 >= dur - 0.15 or t0 < 0:
            continue
        d = probe(library_asset(LAB / f"sfx/{name}.mp3"))
        els.append(f'  <audio id="sfx{j}" src="assets/sfx/{name}.mp3" '
                   f'data-start="{t0:.2f}" data-duration="{min(d, dur - t0):.2f}" '
                   f'data-track-index="{40 + j}" data-volume="{SFX_VOLUME}"></audio>')
    tw = [f'tl.to("#{starts[-1][0]}",{{volume:0,duration:1.45}},'
          f'{max(starts[-1][1], dur - 1.5):.2f});']
    return "\n".join(els), tw


# =============================================================================
# staging + page
# =============================================================================
LOGO_FILES = {
    "nous": LOGOS / "ai-models/nous-girl-line.png",
    "mcp": LOGOS / "ai-models/mcp-mark.svg",
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
}
SFX_NAMES = ["step_in", "wall_slam", "plate_dock", "layer_pass", "meter_fill"]


def stage_assets(stage_dir: Path) -> dict[str, str]:
    for rel in ["v", "logos", "music", "sfx"]:
        (stage_dir / rel).mkdir(parents=True, exist_ok=True)
    # the FINAL matte: u2net alpha, contrast-sharpened + 2px eroded (halo), then
    # windowed by the measured chair cut (see cutout_chair_mask.py)
    matte = LAB / "matte/cutout_matte_stroked.webm"
    if not matte.exists():
        raise SystemExit(f"missing final matte: {matte}")
    dest = stage_dir / "v/matte.webm"
    if not dest.exists() or dest.stat().st_mtime < matte.stat().st_mtime:
        shutil.copy2(matte, dest)
    # DEFECT 2 (2026-09-01): this used to transcode `SRC/source_audio.wav`, the
    # 16 kHz MONO ANALYSIS track, straight into the mix — an 8 kHz Nyquist
    # ceiling, so the top octave of his voice was gone before the encoder saw
    # it.  `cutout_media.resolve_voice` picks the full-quality 48 kHz track and
    # refuses a low-rate one by name.
    import cutout_media as _CM
    _CM.stage_voice(SRC, stage_dir)
    shutil.copy2(library_asset(Path.home() / "Documents/Workspace/assets/audio/music/shorts-factory/bed_split_v2.mp3"), stage_dir / "music/bed_split.mp3")
    for name in SFX_NAMES:
        shutil.copy2(library_asset(LAB / f"sfx/{name}.mp3"), stage_dir / "sfx" / f"{name}.mp3")
    media: dict[str, str] = {}
    for key, source in LOGO_FILES.items():
        if not source.exists():
            raise SystemExit(f"missing registry asset: {source}")
        shutil.copy2(source, stage_dir / "logos" / f"{key}{source.suffix}")
        media[key] = f"assets/logos/{key}{source.suffix}"
        MARK_INK[key] = measure_mark(key, source)
    return media


def bind_assets(project: Path, stage_dir: Path) -> None:
    project.mkdir(parents=True, exist_ok=True)
    dest = project / "assets"
    if dest.is_symlink() or dest.exists():
        if dest.is_symlink():
            dest.unlink()
        elif dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()
    dest.symlink_to(stage_dir.resolve(), target_is_directory=True)


def base_css(ground: str = CREAM) -> str:
    return f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden;
  font-family:Poppins,sans-serif; background:{ground}; }}
.clip {{ position:absolute; }} .abs {{ position:absolute; }}
.disp {{ font-family:Poppins,sans-serif; }}
.mono {{ font-family:'JetBrains Mono',monospace; text-transform:uppercase; }}
.world {{ left:0; top:0; width:{W}px; height:{H}px; overflow:hidden; background:{ground}; }}
.scap {{ left:0; width:{W}px; text-align:center; z-index:120; }}
.scappill {{ display:inline-block; transform:translateY(-50%); background:{TERRA}; color:#fff;
  font-family:Nunito,sans-serif; font-weight:800; padding:19px 34px;
  border-radius:22px; white-space:nowrap;
  box-shadow:0 6px 22px {rgba(INK, 0.22)}; }}
"""


def page(title: str, dur: float, body: str, tweens: list[str], ground: str = CREAM) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width={W}, height={H}"/>
<title>{esc(title)}</title>{GSAP}{FONTS}<style>{base_css(ground)}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-width="{W}" data-height="{H}"
 data-duration="{dur:.3f}" data-fps="{FPS}">
{body}
</div><script>
window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});
const POP="back.out(2.05)";const SOFT="power3.out";const EXIT="power3.in";
{''.join(tweens)}
window.__timelines["main"]=tl;
</script></body></html>"""


def audit_page(html: str) -> None:
    """Every tween target must exist; no duplicate ids."""
    from collections import Counter
    ids = re.findall(r'\sid="([^"]+)"', html)
    dupes = sorted(k for k, v in Counter(ids).items() if v > 1)
    if dupes:
        raise SystemExit(f"duplicate ids: {dupes}")
    known = set(ids)
    script = html.split("<script>")[-1]
    missing = set()
    for match in re.finditer(r'tl\.(?:set|to|fromTo)\("([^"]+)"', script):
        for part in match.group(1).split(","):
            sel = part.strip().lstrip("#")
            if sel.startswith("."):
                continue
            if sel not in known:
                missing.add(sel)
    if missing:
        raise SystemExit(f"tween targets that do not exist: {sorted(missing)}")


def caption_identity_guard(html: str, phrases: list[dict]) -> None:
    """LAW 4: no on-screen text may repeat a caption pill verbatim."""
    texts = [t for t in re.findall(r'>([^<>]{2,})</div>', html) if norm(t)]
    pills = {" ".join(norm(p["text"])) for p in phrases}
    for t in texts:
        key = " ".join(norm(t))
        if key in pills:
            raise SystemExit(f"double caption: on-screen {t!r} equals a pill verbatim")
