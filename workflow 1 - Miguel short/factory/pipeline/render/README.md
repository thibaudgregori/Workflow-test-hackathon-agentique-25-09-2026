# `pipeline/render` — the factory's cloud render lane

`shorts-factory-render` is a deployed Modal app that runs `hyperframes render`
in a container. `modal_render.py` is the laptop-side CLI: it packs a project,
fans however many you hand it out in parallel, writes the MP4s back, and prints
what each one cost.

```bash
PY=~/Documents/Workspace/.venv/bin/python
F=~/Documents/Workspace/projects/personal/content/shorts-factory

# one render at the delivered 1080x1920 (HD is the only delivery since 2026-09-03)
$PY $F/pipeline/render/modal_render.py <run>/projects/<id>_split \
    -o out/sparkchrome_split.mp4 -q high --resolution portrait-4k

# a whole day, all at once — this is the point of the lane
$PY $F/pipeline/render/modal_render.py <run>/projects/*_cutout \
    <run>/projects/*_whiteboard --out-dir out -q high

# prove a cloud render against a local one already on disk
$PY $F/pipeline/render/modal_render.py PROJ -o /tmp/cloud.mp4 --verify out/local.mp4

# re-measure the container sizing, or the packed upload, without rendering
$PY .../modal_render.py PROJ --bench
$PY .../modal_render.py PROJ --pack-only
```

Deploy after any edit to `modal_app.py`: `modal deploy modal_app.py` from this
directory. Registered in `projects/personal/infra/modal/CLAUDE.md`.

---

## The headline, because it is not the one you would guess

**Per render, the laptop is faster. The cloud's win is that thirty of them
finish in the time one does, and the machine stays free while they do.**

An M-series laptop renders these compositions on a hardware GPU with Chrome's
`drawElementImage` fast-capture path. A Modal CPU container has neither: it
rasterises through SwiftShader and captures by screenshot. On the 4K split that
costs a factor of four. Nothing in this lane closes that gap, and it does not
need to — a render you are not waiting for has no wall clock.

---

## Benchmark — the three sparkchrome projects, 2026-09-02

Same CLI (0.7.107), same flags, same day — **and note the local column here was
placed through `npx`, which is NOT how the factory renders locally.** The
factory's laptop lane is `hf.sh` → the agent-tools checkout, **0.7.71**, which
is what wrote the approved run-9 masters. The two builds are pixel-equivalent
(the parity table below holds) and disagree on exactly one delivered-container
field; see the `render_and_check` section. Local numbers are this laptop
(18 cores, 48 GB); Modal is 8 cores / 16 GiB. Local wall is the whole
`npx hyperframes render` invocation, Modal wall is dispatch → MP4 on disk
including the upload and the download, so the two are comparable end to end.

| render | size | upload | local wall | local renderer only | Modal renderer | Modal wall | Modal cost |
|---|---|---|---|---|---|---|---|
| `sparkchrome_split` | 2160×3840 | 47.2 MB | 133.1 s | 52.9 s | 220.5 s | 260.5 s | $0.0316 |
| `sparkchrome_cutout` | 1080×1920 | 31.0 MB | 114.4 s | 34.1 s | 98.6 s | 130.7 s | $0.0144 |
| `sparkchrome_whiteboard` | 1080×1920 | 16.9 MB | 112.1 s | 31.8 s | 44.1 s | 69.2 s | $0.0066 |
| **all three** | | **95.1 MB** | **359.5 s** sequential | 118.8 s | | **261 s** all at once | **$0.0526** |

**Read the two local columns.** `npx hyperframes` costs this machine a flat
**~80 s per invocation** before any rendering starts — 80.2 / 80.3 / 80.3 s
across the three renders, and a bare `npx hyperframes --version` measured
**79.9 s** twice in a row. That is the known broken-IPv6 fault on this laptop
(`reference_macbook_broken_ipv6`): node's registry fetch hangs where `curl` does
not. It is not a HyperFrames cost and it is not a Modal saving, so both columns
are given. **Installing the CLI globally is worth more to a local render than
this whole app is** — it would take a 10-video day from 60 minutes to 20, for
free, today.

> ### Call the CLI through `hf.sh`, and the reason is not speed
>
> **`npx hyperframes` resolves the npm `latest` tag on every call, and `latest`
> moved from 0.7.107 to 0.8.26 during the afternoon this app was built.** A
> local render placed through `npx` is a different renderer from one placed an
> afternoon earlier, and the first symptom is a check failing for a reason that
> has nothing to do with the cloud. That is not hypothetical — it is exactly
> the -20 ms below.
>
> ```bash
> $F/pipeline/render/hf.sh render PROJECT -o OUT.mp4 -q high   # pinned + asserted
> ```
>
> `hf.sh` resolves the `agent-tools/hyperframes` checkout — **0.7.71**, the
> build that wrote every approved master — asserts the version it got, and
> asserts the delivered MP4 afterwards. The 80-second `npx` tax measured below
> is gone (1.2-1.6 s today), so no global install was made; see the
> `render_and_check` section.
>
> To move the version, move it in both places at once: `HF_PIN` in `hf.sh` (and
> the checkout's `dist` it points at), `HF_VERSION` in `modal_app.py`, then
> re-run `--verify`, re-record the table above, **and** re-measure
> `qc_pass audio_guards` on a fresh render of an approved project.

Costs are computed, not billed-back: `billed_seconds × (8 cores × $0.0000131 +
16 GiB × $0.00000222)`, where billed seconds run from the container's own module
import to its last function exit plus the 2 s scaledown window, which is Modal's
published CPU/memory pricing and the same arithmetic `pipeline/sam2` prices its
GPU runs with. There is no per-render invoice line to read back; the dashboard
total is the check.

### Container sizing — measured, not chosen

Same project (`sparkchrome_split`), one render each:

| | renderer | capture stage | cost | cost × time |
|---|---|---|---|---|
| `render_c4` (4 cores / 8 GiB) | 338.6 s | 288.8 s | $0.0241 | 8.16 |
| `render_c8` (8 cores / 16 GiB) | 240.0 s | 195.4 s | $0.0353 | 8.47 |

Doubling the cores buys 1.41× the speed for 1.46× the money — near-linear, so
cost×time is a wash and speed is the tie-breaker. **8 cores ships.** Both
siblings stay deployed so the decision is re-measurable (`--bench`) on a heavier
composition or a later CLI rather than re-argued from memory. The capture stage
is 81 % of the render and scales at 1.48× per core doubling, so 16 cores would
buy less than it costs; that is why the ladder stops here.

---

## Day projections

10 videos/day is 30 renders (10 split + 10 cutout + 10 whiteboard). 30 videos is
90. Modal's wall clock is the slowest single render, because they all start at
once.

| | laptop, as it runs today | laptop, CLI installed globally | Modal | Modal cost |
|---|---|---|---|---|
| **10 videos (30 renders)** | 59.9 min, machine occupied | 19.8 min, machine occupied | **~4.4 min, machine free** | **$0.53** |
| **30 videos (90 renders)** | 3.0 h, machine occupied | 59.4 min, machine occupied | **~4.4 min, machine free** | **$1.58** |

The Modal column assumes the workspace grants as many concurrent containers as
there are renders. It served 3 at once without queueing. If the account is
capped at 10, a 30-render day becomes 3 waves (~13 min) and a 90-render day 9
waves (~39 min) — still ahead, and still on someone else's machine. Check the
cap before promising the 4-minute number for a full day.

**So, the two answers.** Time saved on a 10-video day: **about 55 minutes of
laptop time, and all of it is time the machine is unusable for anything else** —
though a third of that is the `npx` tax, which a global install fixes for free.
Cost: **about 50 cents a day, $16 a month at full quota.**

---

## Parity — what the cloud render is, exactly, against the laptop's

Every render: **same 2160×3840 / 1080×1920, same 633 frames, same 25 fps, same
25.320 s, byte size within 0.20 %.**

| | pixels >2 | pixels >8 | pixels >64 | glyph shift | edge-mask IoU | outline px |
|---|---|---|---|---|---|---|
| `sparkchrome_split` | 4.9 % | 0.15 % | 1 of 8.3 M | 0 px | 0.756 | within 3.5 % |
| `sparkchrome_cutout` | 9.3 % | 0.22 % | 3 of 2.1 M | 0 px | 0.833 | within 2.7 % |
| `sparkchrome_whiteboard` | 10.0 % | 0.16 % | 22 of 2.1 M | 0 px | 0.874 | within 2.0 % |
| **control: the laptop against ITSELF** (Chrome GPU + fast-capture vs Chrome software, same machine, same file) | 10.5 % | 0.23 % | 20 of 2.1 M | 0 px | — | — |

**Read the control row.** The laptop disagrees with itself by the same amount,
on the same composition, purely by switching Chrome's own rasterisation path.
The cloud render is inside the noise the laptop already produces.

### The font question, settled

Byte-hashing the font cache does not answer it and it is worth writing down why:
the compiler **subsets each family to the composition's own glyph coverage** and
names the file by content, so two caches built from two different compositions
hold different files for the same typeface *by construction*. The hashes can
only ever disagree. That is a broken instrument, not a strict one.

What separates "the same typeface" from "a fallback face" is **layout**. A
substituted face changes advance widths, so runs start and end on different
pixels and lines reflow. So the check (`glyph_parity` in `modal_render.py`)
takes the strong-edge mask of each frame — essentially the outlines — and
measures the shift needed to align them and the overlap once aligned.

On a type-only proof composition (three families, weights 400–800, 18 px to
120 px, accents, negative tracking, light-on-dark), rendered on both machines:

- **every text run occupies the same pixels.** Fifteen runs, left and right ink
  extents identical to 0 px on fourteen and 1 px on one, tops and bottoms
  identical, total ink within 0.09 %.
- **the residual is antialiasing weight, and it is largest at the smallest
  type** — +1.37 % ink at 18 px mono, +0.99 % at 24 px, +0.1 % at 90 px. That is
  CoreText against FreeType, a property of the two operating systems.
- **calibration:** swapping Poppins for Arial on the *same* machine drops the
  edge IoU to **0.32**. The cross-platform pair sits at **0.73–0.87**. The
  instrument fires on a real substitution and does not fire here.

`modal_render.py PROJ --fontprint` prints the container's baked font inventory
and toolchain versions when you want to see them directly.

### The bug this found, which was not fonts

The first cloud renders came back with the brand terracotta `#c1440e` at
**(202, 75, 9)** against the laptop's **(189, 66, 10)** — a 13-unit shift on
every frame of every render, with neutrals untouched. That signature is a colour
*matrix* mismatch, and the arithmetic named it exactly: encoding that RGB with
BT.601 and decoding it with BT.709 predicts (204.6, 76.9, 10.0). Debian
bookworm's **ffmpeg 5.1 converts the captured frames with the BT.601 matrix
while tagging the file BT.709.**

The fix is the third pin: a static ffmpeg from the same release line as the
laptop's (`FFMPEG_RELEASE = "n9.0"` against the laptop's 9.0.1), ahead of the
distro build on `PATH`. After it, the terracotta matches **exactly**, pixels >8
fell from 3.4 % to 0.16 %, and file sizes moved from −4 % to +0.2 % of the local
ones. It also made the container **35 % faster** — 5.1's encoder was the slower
part of the bill.

**The lesson for anyone extending this image: pin the toolchain to the laptop's,
all three of it.** Node, the HyperFrames CLI, and ffmpeg. Bump them together and
re-run `--verify`.

---

## How it is built, and why

- **Tarball in, MP4 out.** A shorts project is 15–47 MB of already-cut media.
  Modal moves arguments over 2 MiB through blob storage, so the tar *is* the
  upload and there is no second staging step to keep in sync. The volume
  (`shorts-factory-render`) keeps `/<session>/<name>.mp4` and `.log` afterwards,
  so a dropped download never means paying for the render twice.
- **The packer uploads only what the page references.** A project directory also
  carries `geometry_audit/` PNGs, `_matte.webm.src` provenance stubs and, for the
  whiteboard, a symlink to a staging folder of raw masters — 47 MB of directory
  for a 30 MB render. `modal_render.py` parses the composition's own `src=` /
  `href=`, resolves each through symlinks, and **fails** if any is missing. A
  silently-dropped asset is the one packing bug that yields a plausible-looking
  wrong video, so a broken reference is an error, never a warning.
- **The image is baked hard.** A cold HyperFrames container otherwise pays for
  the Chrome download, puppeteer's lazy first-run install, and a Google Fonts
  round trip per family. All three are paid once at build time by rendering a
  five-frame warm project that declares the factory's three families **in CSS
  rules** — an inline `style` attribute is not enough, and the first build of
  this image cached 11 font files instead of 31 because of it. The build now
  fails if any family is missing.
- **`unzip` is not optional.** `hyperframes browser ensure` downloads the Chrome
  headless shell as a zip and shells out to extract it. Without it the build
  pulls 115 MB and dies with "no zip archiver is available" — which is how the
  first build of this image failed.
- **`PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`.** Playwright is installed for exactly
  one thing, its `install-deps` package list, which is the canonical Chrome
  system-dependency list for Debian and beats hand-maintaining an apt list that
  breaks on a missing `libatk` six months later. Its own browser bundle is
  several hundred MB this image never opens; downloading it made the first
  build's npm step take **8 minutes instead of 18 seconds.**
- **Each slow stage is its own `run_commands`.** Modal keys its build cache on
  the whole call, so bundling them would mean a one-word edit to the warm
  project rebuilding the npm install from scratch.

## Alternatives that already exist, and why this is not one of them

HyperFrames ships three cloud paths of its own (`references/cloud.md`,
`lambda.md`, `cloudrun.md`):

- **`hyperframes cloud render`** — HeyGen-hosted, zero infrastructure, paid per
  credit. Needs a HeyGen sign-in (`hyperframes auth status` reports *not signed
  in* on this machine), bills 4K at 1.5×, and caps the direct upload at 200 MB.
  The genuine zero-effort option if Miguel ever wants credits instead of cents,
  and the projects fit the limit with room to spare.
- **`hyperframes lambda render` / `cloudrun render`** — bring-your-own AWS or
  GCP, with chunked distribution across invocations. Worth it only where that
  cloud ownership already exists; here it would mean standing up an account and
  a stack the factory has no other use for.

Modal is the build because the factory is already on it — `shorts-factory-sam2`
runs the matte lane on the same account, with the same cost arithmetic, the same
volume conventions and the same operator — so this is one more function in a
place that is already understood, not a fourth vendor.

---

## `render_and_check.py` — every check starts when ITS render lands (2026-09-03)

`modal_render.py` already fans renders out at once, and they come back at
different times: a 1080×1920 whiteboard in about a minute, a 2160×3840 split in
several. Until now the checks waited for the whole batch, so the fastest render
sat idle behind the slowest and every `qc_pass` and watcher call queued behind it.

`render_and_check.py` submits the renders and, **as each MP4 lands, starts that
file's own `qc_pass` and its own Gemini watcher in a thread**. It stages a render
only after that render's own checks have passed — which is where the check order
is actually enforced rather than merely written down.

It re-implements nothing: `modal_render`'s own `pack` / `one` / `price` are
imported and called, and `qc_pass.py` and `clerk_video_gemini.py` are invoked as
their own CLIs with their own flags. It schedules; it does not measure.

    render_and_check.py --spec jobs.json [--json report.json] [--stage]
                        [--no-qc] [--no-watch] [--function render] [--thinking medium]

    jobs.json = {"run": "<run>", "out_dir": "<run>/output",
                 "jobs": [{"project": "...", "vid": "...", "fmt": "split",
                           "quality": "high", "stage": "<staging path>",
                           "qc_args": ["--voice-master", "...", ...]}]}

Everything but `project` is optional: `vid`/`fmt` come from the `<id>_<fmt>`
project name, `quality` defaults to high, `geom` is found under `<run>/gen/`, and
`qc_args` is appended verbatim so a format's extra inputs stay the caller's
business. **Omit `resolution`** — every daily composition already renders at its
delivered size, 1080x1920 for every lane since 2026-09-03 (the pre-HD split page was
authored 2160x3840; the benchmark table below is from that era).

**Measured 2026-09-03**, two 1080×1920 `sparkchrome` renders submitted together:

```
[02:15:27] whiteboard  dispatched          [02:15:27] cutout  dispatched
[02:19:01] whiteboard  landed  213.8s  $0.0102  -> checks start NOW
[02:19:07] whiteboard  qc_pass done  5.8s
[02:21:26] cutout      landed  358.4s  $0.0146  -> checks start NOW
[02:21:31] cutout      qc_pass done  5.4s
batch wall 363.8s against 583.4s of the same work one render at a time
```

The whiteboard's checks were finished **2 min 19 s before the cutout landed**.

### The two things it exposed on its first run — both settled 2026-09-03

They turned out to be **one** thing, and it was not the container.

#### The -20 ms was the HyperFrames version, and the pin was matched to a version this laptop never ran

Both fresh Modal renders measured sync lag **-20 ms** (envelope r 0.9858 /
0.9843) where the staged, Miguel-approved 2026-09-02 files measured **0 ms**
(r 0.9977 / 0.9973). Treble and speech margin were fine on all four.

**-20 ms is 960 samples at 48 kHz — one AAC encoder priming interval (1024
samples = 21.33 ms) inside the guard's 10 ms envelope quantisation.** The exact
number is -1024 samples: a sample-accurate FFT cross-correlation of each mix
against `cuts/sparkchrome/audio.m4a` reads **0** for the laptop file and
**-1024** for the container's, on both the cutout and the whiteboard.

It is **one container field**, not one sample of media:

| | video `elst` | audio `elst` | `initial_padding` | audio frames |
|---|---|---|---|---|
| laptop `sparkchrome_cutout` | media time 0, dur 324096 | media time **0**, dur 1215488 | 0 | 1187 |
| Modal `sparkchrome_cutout` | media time 0, dur 324096 | media time **1024**, dur 1215360 | 1024 | 1188 |

Decode the container's file with `-ignore_editlist 1` and it reproduces the
laptop's PCM at lag 0 exactly. The video track is byte-for-byte the same shape.

**Where it comes from.** HyperFrames mixes the composition's audio to an AAC
sidecar and muxes it with `-c:a copy`. Up to and including **0.7.71** that mux
also passed `-avoid_negative_ts make_zero`, which discards the sidecar's
priming edit list. From **0.7.107** the flag is gone — upstream issue #3487:
`make_zero` can write an empty leading VIDEO edit that QuickTime and Safari
show as a black first frame — so the priming edit list survives and every
edit-list-honoring decoder now skips 1024 samples the older build played.

**And the pin was never the laptop's version.** `modal_app.py` said *"laptop:
npx hyperframes --version -> 0.7.107"*. The laptop does not render through
`npx`. It runs the `agent-tools/hyperframes` checkout, and that checkout's
built `dist` reports **0.7.71** (its `package.json` says 0.8.17 — the `dist` is
stale, and the `dist` is what runs). Every approved master in run 9 was
written by 0.7.71. Meanwhile `npx hyperframes` resolves the npm `latest` tag,
which is **0.8.26** today and drops `-avoid_negative_ts` as well.

**The proof it is the CLI and not the cloud:** a **local** render of
`sparkchrome_cutout` on this laptop with 0.7.107 out of the npx cache produces
`initial_padding=1024`, 1188 audio frames and **-21.33 ms** — the container's
file, made on the container's supposed adversary.

#### Which side is correct, and why the guard is not the thing to move

HyperFrames' mixer places the voice **1024 samples early on its own timeline**:
the file whose priming a decoder skips correlates against the cut's voice
master at -1024, the file whose priming is played correlates at 0. The
undischarged priming is what puts the voice back onto the picture's timeline —
so `audio_guards`' 0 ms law is the correct law, the approved masters satisfy
it, and a file that passes the guard is a file whose voice sits on its own
captions. Loosening the guard would ship a mix running 21 ms ahead of them.

#### The fix, on both sides

- **Container** — `modal_app._normalize_delivery_audio()` runs after every
  render, before the probe and before anything is persisted. If the delivered
  MP4 carries `initial_padding > 0` it is remuxed
  `-c copy -avoid_negative_ts make_zero -movflags +faststart`, which is
  literally the argument 0.7.71's own mux passes. **Stream copy: not one video
  or audio sample is re-encoded**, so the parity table above is untouched by
  construction. The run record carries `audio_elst` — `applied`, and the
  padding before and after — and the function raises if the remux leaves any.
- **Laptop** — `pipeline/render/hf.sh` is now the only entry point to the CLI.
  It resolves the checkout (`HF_BIN` overrides), **asserts** the resolved
  version equals `HF_PIN=0.7.71`, and after a `render` asserts the output MP4
  carries no priming edit list. No pipeline may call `npx hyperframes` again.

```bash
$F/pipeline/render/hf.sh render PROJECT -o OUT.mp4 -q high   # pinned, asserted
$F/pipeline/render/hf.sh --version                           # -> 0.7.71
```

**The image stays at `HF_VERSION = 0.7.107`** deliberately: the entire parity
section of this README — pixels, glyphs, colour, container sizing — was
measured against it, and the single place 0.7.71 and 0.7.107 disagree is now
handled explicitly in a stream copy where it can be read back and re-measured.
Moving the image pin means a rebuild **and** re-running `--verify`.

#### Proved, on a fresh render, 2026-09-03

`render_and_check.py --spec` on `(run 9) projects/chatgptchrome_cutout`,
1080×1920, 684 frames, quality high, against
`cuts/chatgptchrome/audio.m4a` — the SAME project whose pre-fix Modal render is
still on disk to compare against:

| `qc_pass audio_guards` | sync lag | envelope r | `initial_padding` | treble Δ | speech margin | verdict |
|---|---|---|---|---|---|---|
| Modal render **before** the fix | **-20 ms** | 0.9855 | 1024 | -0.23 dB | 22.12 dB | **FAIL** |
| Modal render **after** the fix | **0 ms** | **0.9969** | **0** | -0.22 dB | 21.54 dB | **PASS** |

Full `qc_pass` on the fresh render: `decoded_blank_frames`, `zero_ink_law`,
`clip_coverage_page`, `face_centring`, `pill_canon_rendered`,
`cutout_checks_24_25`, **`audio_guards`**, `contact_sheet` all PASS
(`double_exposure` REPORTED). The run record carries
`audio_elst = {"applied": true, "initial_padding_before": 1024,
"initial_padding_after": 0, "wall_s": 0.17}` — **0.17 s** on a 464.6 s batch,
$0.0185 for the whole render-and-check.

`audio_guards` now also reports `audio_initial_padding_samples`. It is not
judged — it is the pointer: **1024 there IS the -20 ms**, and it turns the next
occurrence of this from a bisect into a glance.

#### And the 80-second `npx` tax is gone

Measured 2026-09-03, cold shell: `npx hyperframes --version` **1.55 s**,
`NODE_OPTIONS=--dns-result-order=ipv4first npx hyperframes --version` **1.29 s**,
`npx --yes hyperframes@0.7.107 --version` **1.43 s**, `hf.sh --version`
**1.24 s** (and that is two CLI invocations — the assert and the pass-through).
The 79.9 s in the benchmark table above was the broken-IPv6 registry hang
(`reference_macbook_broken_ipv6`) and it is not reproducing tonight. **So no
global `npm i -g` was done**: it would buy nothing measurable, and `hf.sh`
already removes the reason it was wanted, which was never speed but the
`latest`-tag roulette. The day-projection table's "laptop, CLI installed
globally" column is the one to read.
