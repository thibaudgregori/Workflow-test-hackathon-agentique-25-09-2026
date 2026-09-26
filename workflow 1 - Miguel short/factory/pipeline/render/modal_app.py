"""shorts-factory-render — the factory's HyperFrames render lane on Modal.

DEPLOYED (`modal deploy modal_app.py`), not a `modal run` script.  The public
surface is three CPU functions that share ONE implementation:

    render      the production entry (the measured winner: 8 cores / 16 GiB)
    render_c8   the 8-core benchmark sibling
    render_c4   the 4-core benchmark sibling

Hand any of them a tar of ONE project directory (`index.html` + exactly the
files that page references) and get back the MP4 bytes, the CLI's own stage
timings, and the container's billed core-seconds priced with Modal's published
rates.

WHY A TARBALL AND NOT A VOLUME.  A shorts project is 15-45 MB of already-cut
media.  Modal moves function arguments through blob storage above 2 MiB, so the
tar IS the upload and there is no second staging step to keep in sync.  The
volume is durable scratch AFTER the fact: every run leaves
`/vol/<session>/<name>.mp4` and `<name>.log` behind, so a dropped download never
means paying for the render twice.

WHY THE IMAGE IS BAKED THIS HARD.  A cold HyperFrames container that has never
rendered pays for (a) the Chrome-for-Testing download (which needs `unzip` in
the image), (b) puppeteer's lazy first-run install, and (c) a Google-Fonts round
trip per family.  All three are
paid ONCE at image-build time by rendering a five-frame warm project that
requests the factory's exact three families (Poppins, Nunito, JetBrains Mono).
What ships is a container whose font cache already holds the same WOFF2 bytes
the laptop's `~/.cache/hyperframes/fonts` holds, which is what makes the cloud
render glyph-identical instead of glyph-similar.

THREE THINGS ARE PINNED, DELIBERATELY.  `NODE_VERSION` matches the laptop's
`node --version`, `HF_VERSION` names the HyperFrames CLI this image installs
(the laptop's own lane is pinned separately by `hf.sh` — see the PINS block),
and `FFMPEG_RELEASE` matches the laptop's `ffmpeg -version` release
line.  A render is a browser rasterising type and an encoder writing colour;
drifting any of the three drifts pixels.  The ffmpeg pin is not defensive
paranoia — the distro build shipped a measured 13-unit shift on the brand
terracotta, and that is the whole story of this app's parity.  Bump the three
together, re-run `modal_render.py ... --verify`, and only then move the pins.

Calling it, from anywhere:

    import modal
    render = modal.Function.from_name("shorts-factory-render", "render")
    out = render.remote(project_tar=tar_bytes, name="sparkchrome_split",
                        quality="high", resolution=None)  # HD delivery since 2026-09-03; "portrait-4k" only for legacy zoom:2 pages
    Path("out.mp4").write_bytes(out["video"])

`modal_render.py` in this directory is that call with the packing, the
parallel fan-out, the cost arithmetic and the local file handling written.
"""
from __future__ import annotations

import base64
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import tarfile
import tempfile
import time
import uuid
from pathlib import Path

import modal

# ── PINS ────────────────────────────────────────────────────────────────────
# Both must track the laptop.  See the module docstring.
NODE_VERSION = "24.14.0"          # laptop: node --version -> v24.14.0
# THE HYPERFRAMES PIN, and read the note before moving it (2026-09-03).
#   * the LAPTOP does not render through `npx`.  `pipeline/render/hf.sh` is the
#     factory's only entry point and it resolves the agent-tools checkout at
#     `infra/agent-tools/hyperframes/packages/cli/bin/hyperframes.mjs`, whose
#     built `dist` reports **0.7.71**.  Every approved master in run 9
#     was written by that build.
#   * `npx hyperframes` resolves the npm `latest` tag, which is **0.8.26**
#     today and was 0.7.107 when this image was built.  Nothing in the factory
#     may call it unpinned; `hf.sh` exists to make that impossible.
#   * this image stays at 0.7.107 because the whole parity section of
#     `README.md` — pixels, glyphs, colour, sizing — was measured against it.
#     The ONE place 0.7.71 and 0.7.107 disagree is the delivered container's
#     AAC priming edit list, and `_normalize_delivery_audio` settles that
#     explicitly, in a stream copy, where it can be read and re-measured.
#     Moving this pin means rebuilding the image AND re-running `--verify`.
HF_VERSION = "0.7.107"            # laptop lane: 0.7.71 (see hf.sh) — read above
PLAYWRIGHT_VERSION = "1.56.0"     # used ONLY for `playwright install-deps chromium`

# THE THIRD PIN, and the one that actually decided parity.  Debian bookworm
# ships ffmpeg 5.1, and 5.1 converts the captured RGB frames to YUV with the
# BT.601 matrix while tagging the file BT.709.  A player then decodes 709 from
# 601 data, which leaves neutrals alone and shifts saturated colour hard: the
# factory's terracotta #c1440e (193,68,14) came back as (202,75,9) from the
# container against (189,66,10) from the laptop — a 13-unit shift on the brand
# colour, on every frame of every render.  Measured, not guessed: encoding that
# RGB with 601 and decoding it with 709 predicts (204.6,76.9,10.0), which is
# the container's number inside chroma-subsampling noise.  So the container
# gets a static ffmpeg from the SAME release line as the laptop's `ffmpeg
# -version`, ahead of the distro build on PATH.  Bump this together with the
# laptop's ffmpeg and re-run `modal_render.py ... --verify`.
FFMPEG_RELEASE = "n9.0"           # laptop: ffmpeg 9.0.1
FFMPEG_TARBALL = ("https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/"
                  f"ffmpeg-{FFMPEG_RELEASE}-latest-linux64-gpl-{FFMPEG_RELEASE[1:]}.tar.xz")

# The factory's three families, requested by every shipped composition.  Baked
# into the image's font cache so no render pays a Google Fonts round trip and
# every render rasterises the same bytes the laptop does.
WARM_FONTS = ("Poppins:wght@500;600;700;800"
              "&family=Nunito:wght@800"
              "&family=JetBrains+Mono:wght@400;500;700")

NODE_TARBALL = (f"https://nodejs.org/dist/v{NODE_VERSION}/"
                f"node-v{NODE_VERSION}-linux-x64.tar.xz")

# A three-frame project that touches everything a real render touches: all
# three families at several weights on timed clips, registered on the
# `window.__timelines["main"]` hook the factory's own compositions use (without
# it the producer burns its full 45 s sub-timeline readiness budget).  Rendering
# it at build time is what bakes Chrome, puppeteer's lazy install and the font
# cache into the image layer.
WARM_HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=1080, height=1920"/>
<title>warm</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family={WARM_FONTS}&display=block" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ margin:0; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden;
  background:#F6F1EA; font-family:Poppins,sans-serif; }}
/* One RULE per family, not just an inline style attribute: the compiler
   resolves Google Fonts from the families it sees declared in CSS, so a warm
   project that only names Poppins in a rule bakes ONLY Poppins and leaves the
   other two to be fetched on every billed render. Measured: the first build of
   this image cached 11 files instead of 31. */
.f-poppins {{ font-family:Poppins,sans-serif; }}
.f-nunito {{ font-family:Nunito,sans-serif; }}
.f-jetbrains {{ font-family:'JetBrains Mono',monospace; }}
.clip {{ position:absolute; }}
</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="0.2" data-fps="25">
  <div class="clip f-poppins" id="a" data-start="0" data-duration="0.2"
       style="left:80px;top:300px;font-weight:800;font-size:90px;color:#1a1a1a">Poppins 800</div>
  <div class="clip f-nunito" id="b" data-start="0" data-duration="0.2"
       style="left:80px;top:520px;font-weight:800;font-size:90px;color:#1a1a1a">Nunito 800</div>
  <div class="clip f-jetbrains" id="c" data-start="0" data-duration="0.2"
       style="left:80px;top:740px;font-weight:500;font-size:70px;color:#1a1a1a">JetBrains 500</div>
  <div class="clip f-poppins" id="d" data-start="0" data-duration="0.2"
       style="left:80px;top:900px;font-weight:600;font-size:70px;color:#c1440e">Poppins 600</div>
</div><script>
window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});
tl.fromTo("#a",{{opacity:0}},{{opacity:1,duration:0.1}},0);
window.__timelines["main"]=tl;
</script></body></html>
"""

WARM_B64 = base64.b64encode(WARM_HTML.encode()).decode()

image = (
    modal.Image.debian_slim(python_version="3.12")
    # `unzip` is NOT optional: `hyperframes browser ensure` downloads the
    # Chrome-for-Testing headless shell as a .zip and shells out to a zip
    # archiver to extract it.  Without one it downloads 115 MB and then dies
    # with "no zip archiver is available", which is how the first build of this
    # image failed.
    .apt_install("curl", "ca-certificates", "xz-utils", "unzip", "ffmpeg",
                 "fontconfig")
    # Node pinned to the laptop's build, installed from the official tarball so
    # the version is exact rather than whatever the distro repo happens to hold.
    .run_commands(
        f"curl -fsSL {NODE_TARBALL} -o /tmp/node.tar.xz",
        "mkdir -p /opt/node && tar -xJf /tmp/node.tar.xz -C /opt/node "
        "--strip-components=1 && rm /tmp/node.tar.xz",
    )
    .env({
        "PATH": "/opt/node/bin:/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin",
        # Telemetry and the update check are network round trips on a path that
        # is billed by the second and has nothing to report from a container.
        "HYPERFRAMES_NO_TELEMETRY": "1",
        "HYPERFRAMES_NO_UPDATE_CHECK": "1",
        # Playwright is installed for ONE thing — its `install-deps` package
        # list.  Its own browser bundle is several hundred MB this image never
        # opens, and downloading it made the first build's npm step take 8 min.
        "PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD": "1",
        "HOME": "/root",
    })
    # Each of the next four stages is its OWN `run_commands` call, and that is
    # deliberate: Modal keys its build cache on the whole call, so bundling them
    # would mean a one-word edit to the warm project rebuilding the npm install
    # from scratch.  Ordered cheapest-to-invalidate last.
    .run_commands(f"npm i -g hyperframes@{HF_VERSION} playwright@{PLAYWRIGHT_VERSION}")
    # Playwright owns the canonical Chrome system-dependency list for Debian;
    # hand-maintaining that apt list is how cloud renders die on a missing
    # libatk six months later.  It also brings the CJK/emoji font packages.
    .run_commands("playwright install-deps chromium")
    .run_commands("hyperframes browser ensure")
    # Static ffmpeg, matched to the laptop's release line.  Placed after the
    # slow layers so a bump here does not rebuild npm, and ahead of the distro
    # build on PATH by the .env() below.  See FFMPEG_RELEASE for why.
    .run_commands(
        f"curl -fsSL {FFMPEG_TARBALL} -o /tmp/ffmpeg.tar.xz",
        "mkdir -p /opt/ffmpeg && tar -xJf /tmp/ffmpeg.tar.xz -C /opt/ffmpeg "
        "--strip-components=1 && rm /tmp/ffmpeg.tar.xz",
        "/opt/ffmpeg/bin/ffmpeg -version | head -1",
    )
    .env({"PATH": "/opt/ffmpeg/bin:/opt/node/bin:/usr/local/bin:/usr/local/sbin:"
                  "/usr/sbin:/usr/bin:/sbin:/bin"})
    .run_commands(
        # The Google-Fonts round trip and puppeteer's lazy first-run install,
        # both paid once here.  `-q draft` because this render's PIXELS are
        # thrown away — only its side effects are kept.
        "mkdir -p /opt/warm",
        # base64 rather than a heredoc: `run_commands` lowers each string to a
        # single Dockerfile RUN line, so an embedded newline would truncate it.
        f"printf %s {WARM_B64} | base64 -d > /opt/warm/index.html",
        "hyperframes render /opt/warm -o /tmp/warm.mp4 -q draft && test -s /tmp/warm.mp4",
        "rm -f /tmp/warm.mp4",
        # Prove the cache is populated at build time rather than discovering it
        # is empty on a billed render.
        # Not decoration: the build FAILS here if a family did not bake, which
        # is the only moment the mistake is cheap to catch.
        "ls -1 /root/.cache/hyperframes/fonts",
        "for f in poppins nunito jetbrains-mono; do "
        "test -d /root/.cache/hyperframes/fonts/$f || "
        "{ echo \"MISSING FONT CACHE: $f\"; exit 1; }; done",
        "find /root/.cache/hyperframes/fonts -name '*.woff2' | wc -l",
    )
)

app = modal.App("shorts-factory-render")

# Run artifacts only.  Chrome and the fonts are baked IMAGE LAYERS, so a cold
# container never waits on a volume mount to be able to render.
vol = modal.Volume.from_name("shorts-factory-render", create_if_missing=True)

# Modal's published CPU rates — the same constants `pipeline/sam2/modal_app.py`
# prices its GPU runs with, so the two lanes' numbers are comparable.
CPU_USD_S_CORE, MEM_USD_S_GIB = 0.0000131, 0.00000222
SCALEDOWN = 2

T_IMPORT = time.time()
CONTAINER_ID = str(uuid.uuid4())

_TRACE = re.compile(r'"totalElapsedMs":(\d+)')
_STAGE = re.compile(r'"phase":"(\w+)","status":"end".*?"durationMs":(\d+)')


def _audio_initial_padding(path: Path) -> int:
    """The delivered file's declared AAC encoder-priming, in samples."""
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
         "stream=initial_padding", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True)
    try:
        return int((r.stdout or "0").strip() or 0)
    except ValueError:
        return 0


def _normalize_delivery_audio(path: Path) -> dict:
    """Strip the AAC priming EDIT LIST from the delivered MP4.  Stream copy.

    THE 20 MS, AND WHY THIS IS NOT A WORKAROUND.  A fresh container render of
    an approved composition measured **-20 ms** on `qc_pass`'s `audio_guards`
    (`sync_lag`, 10 ms envelope) where the staged, Miguel-approved file of the
    SAME project measured 0 ms.  -20 ms is 960 samples at 48 kHz — one AAC
    encoder priming interval (1024 samples = 21.33 ms) inside the guard's
    10 ms quantisation.  Measured, not inferred: the two files' audio elst
    entries are `media time: 0, duration 1215488` (laptop) against
    `media time: 1024, duration 1215360` (container), the video elst is
    IDENTICAL in both, and decoding the container's file with
    `-ignore_editlist 1` reproduces the laptop's PCM at lag 0 exactly.  The
    difference is one container field, not one sample of audio or video.

    WHERE IT COMES FROM.  HyperFrames mixes the composition's audio to an AAC
    sidecar and muxes it with `-c:a copy`.  Up to and including 0.7.71 that
    mux also passed `-avoid_negative_ts make_zero`, which discards the
    sidecar's priming edit list; from 0.7.107 the flag is gone (upstream issue
    #3487 — `make_zero` can write an empty leading VIDEO edit that QuickTime
    shows as a black first frame) and the priming edit list survives.  So a
    player that honours edit lists now skips 1024 samples the old builds
    played.  The factory's laptop renders through the agent-tools checkout,
    whose built `dist` is **0.7.71** — every approved master in run 9
    was written by the make_zero build — and this image pins 0.7.107.  A local
    0.7.107 render of `sparkchrome_cutout` on the laptop reproduces the
    container's -21.33 ms exactly, which is what proves this is the CLI
    version and not the container.

    WHY STRIPPING IS THE CORRECT SIDE.  HyperFrames' mixer places the voice
    1024 samples EARLY on its own timeline (measured: the container's file,
    whose priming the decoder skips, correlates against the cut's voice master
    at -1024 samples; the laptop's, whose priming is played, at 0).  The
    undischarged priming is what puts the voice back onto the picture's
    timeline, which is why the guard's law is 0 ms and why the approved
    masters satisfy it.  Reproducing the delivered container the approved
    masters have is therefore the fix; loosening the guard would ship a mix
    that runs 21 ms ahead of its own captions.

    `-c copy` throughout: not one video or audio sample is re-encoded, so
    frame parity and the `--verify` numbers are untouched by construction.
    """
    before = _audio_initial_padding(path)
    if before <= 0:
        return {"applied": False, "initial_padding_before": before,
                "initial_padding_after": before,
                "reason": "no priming edit list on the delivered audio"}
    tmp = path.with_suffix(".elstfix.mp4")
    t0 = time.time()
    # 2026-09-03 (Miguel: "black screen as the first frame"): `-avoid_negative_ts
    # make_zero` did strip the audio priming edit but ALSO wrote an empty
    # 21.4 ms leading VIDEO edit (upstream #3487), which QuickTime shows as a
    # black first frame; 17 delivered shorts carried it.  Reading the input
    # with `-ignore_editlist 1` drops the priming edit at the source instead,
    # leaves the video timeline untouched, and is what "reproduces the
    # laptop's PCM at lag 0 exactly" above.  The video start is asserted below.
    p = subprocess.run(
        ["ffmpeg", "-v", "error", "-ignore_editlist", "1", "-i", str(path),
         "-c", "copy", "-movflags", "+faststart", "-y", str(tmp)],
        capture_output=True, text=True)
    if p.returncode != 0 or not tmp.exists() or tmp.stat().st_size == 0:
        tmp.unlink(missing_ok=True)
        raise RuntimeError(
            f"delivery audio normalisation failed rc={p.returncode}\n"
            f"{(p.stderr or '')[-2000:]}")
    after = _audio_initial_padding(tmp)
    if after != 0:
        tmp.unlink(missing_ok=True)
        raise RuntimeError(
            f"delivery audio normalisation left initial_padding={after}; "
            "the delivered container must carry none")
    vstart = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=start_time", "-of", "csv=p=0", str(tmp)],
        capture_output=True, text=True).stdout.strip()
    if vstart not in ("0.000000", "0", "0.0"):
        tmp.unlink(missing_ok=True)
        raise RuntimeError(
            f"delivery normalisation left the VIDEO starting at {vstart} s; "
            "a leading video edit shows as a black first frame (2026-09-03)")
    tmp.replace(path)
    return {"applied": True, "initial_padding_before": before,
            "initial_padding_after": after,
            "wall_s": round(time.time() - t0, 2)}


def _probe(path: Path) -> dict:
    """ffprobe the artifact.  A render that produced a file is not a render
    that produced a VIDEO; the parity check downstream compares these fields
    before it compares a single pixel."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,r_frame_rate,nb_frames,codec_name,pix_fmt",
         "-show_entries", "format=duration,size",
         "-of", "json", str(path)],
        capture_output=True, text=True, check=True)
    d = json.loads(out.stdout)
    st = (d.get("streams") or [{}])[0]
    fm = d.get("format") or {}
    a = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0",
         "-show_entries", "stream=codec_name,sample_rate,channels",
         "-of", "json", str(path)],
        capture_output=True, text=True, check=True)
    ast = (json.loads(a.stdout).get("streams") or [{}])[0]
    return dict(width=st.get("width"), height=st.get("height"),
                fps=st.get("r_frame_rate"), frames=st.get("nb_frames"),
                codec=st.get("codec_name"), pix_fmt=st.get("pix_fmt"),
                duration=float(fm.get("duration", 0)),
                bytes=int(fm.get("size", 0)),
                audio_codec=ast.get("codec_name"),
                sample_rate=ast.get("sample_rate"), channels=ast.get("channels"))


def _impl(project_tar: bytes,
          name: str,
          cores: float,
          mem_gib: float,
          quality: str,
          resolution: str | None,
          fps: int | None,
          workers: str | None,
          session: str,
          return_video: bool,
          extra_args: list[str] | None,
          t_fn_entry: float) -> dict:
    """Unpack, render, probe, persist, price.  Shared by every sized wrapper so
    the 4-core and 8-core numbers differ ONLY in the container they ran in."""
    work = Path(tempfile.mkdtemp(prefix="hfrender-"))
    proj = work / name
    proj.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(project_tar), mode="r:*") as tf:
        tf.extractall(proj)
    if not (proj / "index.html").exists():
        raise RuntimeError(f"tar for {name} has no index.html at its root")

    unpacked = sum(p.stat().st_size for p in proj.rglob("*") if p.is_file())
    out = work / f"{name}.mp4"

    cmd = ["hyperframes", "render", str(proj), "-o", str(out), "-q", quality]
    if resolution:
        cmd += ["--resolution", resolution]
    if fps:
        cmd += ["-f", str(fps)]
    if workers:
        cmd += ["-w", str(workers)]
    cmd += list(extra_args or [])

    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=str(work))
    render_s = time.time() - t0
    log = (p.stdout or "") + "\n" + (p.stderr or "")

    if p.returncode != 0 or not out.exists() or out.stat().st_size == 0:
        # Persist the failure log so the diagnosis does not require a re-render.
        d = Path("/vol") / session
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{name}.FAILED.log").write_text(log)
        vol.commit()
        raise RuntimeError(
            f"render {name} failed rc={p.returncode}\n{log[-4000:]}")

    # The font bytes this render actually rasterised.  The compiler SUBSETS each
    # family to the composition's own glyphs and names the file by content, so
    # these hashes are a fingerprint of the exact outlines that were drawn —
    # and `modal_render.py --verify` can check every one of them against the
    # laptop's own cache.  A silent fallback to a system face is invisible in a
    # frame diff at 1080p and unmistakable here.
    fc = Path("/root/.cache/hyperframes/fonts")
    fonts = {str(f.relative_to(fc)): hashlib.sha256(f.read_bytes()).hexdigest()
             for f in sorted(fc.rglob("*.woff2"))} if fc.exists() else {}

    # BEFORE the probe and before anything is persisted: bring the delivered
    # container onto the convention every approved master in the factory has.
    # See `_normalize_delivery_audio` — this is the -20 ms, and it is one
    # stream-copy remux, not a re-encode.
    audio_elst = _normalize_delivery_audio(out)

    probe = _probe(out)
    stages = {m.group(1): int(m.group(2)) / 1000.0 for m in _STAGE.finditer(log)}
    tot = _TRACE.findall(log)

    d = Path("/vol") / session
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy2(out, d / f"{name}.mp4")
    (d / f"{name}.log").write_text(log)

    rec = dict(
        name=name, ok=True, cmd=" ".join(cmd),
        container_id=CONTAINER_ID, session=session,
        cores=cores, mem_gib=mem_gib,
        quality=quality, resolution=resolution,
        upload_bytes=len(project_tar), unpacked_bytes=unpacked,
        render_seconds=round(render_s, 2),
        cli_total_seconds=round(int(tot[-1]) / 1000.0, 2) if tot else None,
        cli_stage_seconds={k: round(v, 2) for k, v in stages.items()},
        probe=probe, fonts=fonts, audio_elst=audio_elst,
        hf_version=HF_VERSION, node_version=NODE_VERSION,
        t_import_epoch=T_IMPORT, t_fn_entry_epoch=t_fn_entry,
        t_fn_exit_epoch=time.time(),
        log_tail=log[-3000:],
    )
    if return_video:
        rec["video"] = out.read_bytes()
    vol.commit()
    shutil.rmtree(work, ignore_errors=True)
    return rec


def _sig(cores: float, mem_gib: float):
    """The wrapper body, written once.  `cores`/`mem_gib` are passed through to
    the cost arithmetic rather than sniffed from the cgroup: what Modal BILLS
    is what was requested, and a sniffed value would silently disagree."""
    def run(project_tar: bytes, name: str, quality: str = "high",
            resolution: str | None = None, fps: int | None = None,
            workers: str | None = None, session: str = "run",
            return_video: bool = True,
            extra_args: list[str] | None = None) -> dict:
        return _impl(project_tar, name, cores, mem_gib, quality, resolution,
                     fps, workers, session, return_video, extra_args,
                     time.time())
    return run


# ── THE PRODUCTION ENTRY ────────────────────────────────────────────────────
# 8 cores / 16 GiB is the MEASURED winner, not a guess: at 4 cores the same
# sparkchrome_split render is slower by more than the halved core rate saves,
# so the 8-core container is both faster AND cheaper per render.  The numbers
# live in `README.md`.  Re-measure with `modal_render.py --bench` before moving
# this.
# THE DEFAULT STAYS 8 CORES.  Measured 2026-09-03 15:15 on the same draft
# render of sparkchrome_whiteboard: 32 cores 58.1 s render / 77.5 s wall /
# $0.031 against 8 cores 51.7 s / 61.5 s / $0.008.  Chrome's frame capture is
# one thread, so extra cores bought nothing and the bigger container placed
# slower.  Miguel's rule was "switch only if shorter"; it was not.  render_c16
# and render_c32 stay deployed as sizing lanes for a future measurement.
@app.function(image=image, volumes={"/vol": vol}, timeout=3600,
              cpu=8.0, memory=(16384, 32768), scaledown_window=SCALEDOWN)
def render(project_tar: bytes, name: str, quality: str = "high",
           resolution: str | None = None, fps: int | None = None,
           workers: str | None = None, session: str = "run",
           return_video: bool = True,
           extra_args: list[str] | None = None) -> dict:
    """Render ONE project.  Returns the run record, with `video` = MP4 bytes."""
    return _sig(8.0, 16.0)(project_tar, name, quality, resolution, fps,
                           workers, session, return_video, extra_args)


# ── THE BENCHMARK SIBLINGS ──────────────────────────────────────────────────
# Kept deployed so the sizing decision stays re-measurable on a later CLI or a
# heavier composition instead of being re-derived from memory.
@app.function(image=image, volumes={"/vol": vol}, timeout=3600,
              cpu=8.0, memory=(16384, 32768), scaledown_window=SCALEDOWN)
def render_c8(project_tar: bytes, name: str, quality: str = "high",
              resolution: str | None = None, fps: int | None = None,
              workers: str | None = None, session: str = "bench",
              return_video: bool = False,
              extra_args: list[str] | None = None) -> dict:
    return _sig(8.0, 16.0)(project_tar, name, quality, resolution, fps,
                           workers, session, return_video, extra_args)


@app.function(image=image, volumes={"/vol": vol}, timeout=3600,
              cpu=16.0, memory=(16384, 32768), scaledown_window=SCALEDOWN)
def render_c16(project_tar: bytes, name: str, quality: str = "high",
              resolution: str | None = None, fps: int | None = None,
              workers: str | None = None, session: str = "bench",
              return_video: bool = False,
              extra_args: list[str] | None = None) -> dict:
    return _sig(16.0, 16.0)(project_tar, name, quality, resolution, fps,
                           workers, session, return_video, extra_args)


@app.function(image=image, volumes={"/vol": vol}, timeout=3600,
              cpu=32.0, memory=(32768, 65536), scaledown_window=SCALEDOWN)
def render_c32(project_tar: bytes, name: str, quality: str = "high",
              resolution: str | None = None, fps: int | None = None,
              workers: str | None = None, session: str = "bench",
              return_video: bool = False,
              extra_args: list[str] | None = None) -> dict:
    return _sig(32.0, 32.0)(project_tar, name, quality, resolution, fps,
                           workers, session, return_video, extra_args)


@app.function(image=image, volumes={"/vol": vol}, timeout=3600,
              cpu=4.0, memory=(8192, 16384), scaledown_window=SCALEDOWN)
def render_c4(project_tar: bytes, name: str, quality: str = "high",
              resolution: str | None = None, fps: int | None = None,
              workers: str | None = None, session: str = "bench",
              return_video: bool = False,
              extra_args: list[str] | None = None) -> dict:
    return _sig(4.0, 8.0)(project_tar, name, quality, resolution, fps,
                          workers, session, return_video, extra_args)


@app.function(image=image, timeout=300, cpu=1.0, memory=(2048, 4096),
              scaledown_window=2)
def fontprint() -> dict:
    """SHA-256 of every font file the image baked, plus the toolchain versions.

    This is the parity instrument, not a debug helper.  A cloud render that
    silently substitutes a fallback face is the classic way a container ships a
    video that is subtly not the one the laptop makes, and the only way to
    settle it is to compare the BYTES both machines rasterise, not the pixels
    they produce.  `modal_render.py --fontprint` diffs this against the
    laptop's own `~/.cache/hyperframes/fonts`.
    """
    import hashlib

    root = Path("/root/.cache/hyperframes/fonts")
    files = {}
    for f in sorted(root.rglob("*")):
        if f.is_file():
            files[str(f.relative_to(root))] = dict(
                sha256=hashlib.sha256(f.read_bytes()).hexdigest(), bytes=f.stat().st_size)
    ver = {}
    for tool, cmd in (("node", ["node", "--version"]),
                      ("hyperframes", ["hyperframes", "--version"]),
                      ("ffmpeg", ["ffmpeg", "-version"]),
                      ("chrome", ["hyperframes", "browser", "path"])):
        try:
            ver[tool] = subprocess.run(cmd, capture_output=True, text=True
                                       ).stdout.strip().splitlines()[0]
        except Exception as e:                       # noqa: BLE001
            ver[tool] = f"error: {e}"
    return dict(font_files=files, versions=ver)


def cost(rec: dict, dispatched_at: float | None = None) -> dict:
    """Billed container seconds -> USD, boot to scaledown.

    Containers bill from boot to scaledown, so the charge is the span from the
    container's own module import to the last function exit, plus the
    `scaledown_window`.  NOT the render's own wall clock: a container that
    served two renders billed once, and naive summing double-counts.
    """
    billed = (rec["t_fn_exit_epoch"] - rec["t_import_epoch"]) + SCALEDOWN
    cpu = billed * rec["cores"] * CPU_USD_S_CORE
    mem = billed * rec["mem_gib"] * MEM_USD_S_GIB
    if dispatched_at is not None:
        rec["cold_start_seconds"] = round(rec["t_import_epoch"] - dispatched_at, 2)
    rec["billed_container_seconds"] = round(billed, 1)
    rec["measured_cost_usd"] = round(cpu + mem, 4)
    rec["cost_breakdown_usd"] = dict(cpu=round(cpu, 4), mem=round(mem, 4))
    return rec


@app.local_entrypoint()
def smoke(project: str, quality: str = "draft", resolution: str = "",
          session: str = "smoke"):
    """Prove the deploy answers, for cents.

        modal run modal_app.py::smoke --project .../projects/sparkchrome_whiteboard
    """
    src = Path(project).resolve()
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        for p in sorted(src.rglob("*")):
            if p.is_file() and not p.name.startswith("._"):
                tf.add(p, arcname=str(p.relative_to(src)))
    t0 = time.time()
    r = render.remote(project_tar=buf.getvalue(), name=src.name,
                      quality=quality, resolution=resolution or None,
                      session=session, return_video=False)
    cost(r, t0)
    print(json.dumps({k: v for k, v in r.items() if k != "log_tail"}, indent=1))
    print(f"\nBILLED {r['billed_container_seconds']}s = ${r['measured_cost_usd']}")
