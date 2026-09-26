# `pipeline/prerender` — catch the rejection before the render

Three tools. All three pass, or the project does not go to the render lane.

Every law they enforce is a property of the **page**, not of a pixel — so paying
for a Modal render, a `qc_pass` decode and a Gemini watcher call to discover a
16 px gutter, a lone `"in"` pill or an illegible bespoke object was always a
choice, never a necessity.

**Nothing here is re-implemented.** Each check is an existing module's own
function, called on the project directory. Where a law had no importable form,
the *browser* answers it — never a second copy of the rule.

---

## (a) `prerender_check.py <project>` — the page obeys the laws

| check | what runs | bar |
|---|---|---|
| `refs_resolve` | `modal_render.refs` — the packer's own reference list | every local `src`/`href` resolves |
| `assets_not_placeholder` | `cutout_depthfield._reads_as_placeholder` on every raster the page points at | nothing reads as a missing-image icon (run 9 shipped Exa's mark, which is stroke-for-stroke the broken-image glyph) |
| `page_audit` | duplicate ids, plus every `tl.set/to/fromTo` selector resolved **in the loaded page** | 0 duplicates, 0 dead targets |
| `caption_canon_page` | `captions.assert_no_function_only_beat` on the **measured** pills | pill height at the 114.59 canon ±3 design px, aspect ≥ `PILL_MIN_ASPECT` 1.45, no lone function word |
| `gate1_geometry_audit` | `pipeline/geometry_audit.py --step 0.25` | 0 errors, 0 warnings |
| `cutout_edge_fade_guard` | `cutout_core.guard_edge_fade(html)` | cutout only |
| `cutout_checks_24_25` | `cutout6_check.check_edge_fade` / `check_depth_field` | cutout only, empty fails list |

Exit **1** on any error. Measured on the staged `sparkchrome` projects,
**6.4-6.6 s per project**, all three formats.

### Two things that bit, written down so they do not bite again

**Gate 1 runs BEFORE the cutout checks, and its report stays in the project.**
`cutout6_check.check_edge_fade` reads `<project>/geometry_audit/report.json` by a
hard-coded path — that report is the *geometric* half of Law 8, the half a string
guard cannot see. Redirecting Gate 1's output would silently turn check 24 into a
fail. `--gate1-out` therefore takes a **copy**; it never moves the canonical file.

**`whiteboard_build.audit_page`'s dead-tween half is not usable on a DOM-lane
page.** Its membership test only understands `#id`, and every run-9 DOM page
tweens descendant selectors (`"b1-open .shead"`), so it reported **14 live
targets as dead** on `sparkchrome_cutout`. The same law asked of the browser —
`document.querySelectorAll(sel).length` — is exact, so that is what runs here.
The duplicate-id half is a pure string property and is unchanged.

### The one named waiver, and the measurement that earns it

`geometry_audit`'s older `SNAPSHOT_JS` lane measures raw
`getBoundingClientRect` against `FRAME_W = 1080`. A **split** page is authored
2160 wide with `zoom:2` (the newer `LAYOUT_JS` lane normalises by
`1080 / root.dataset.width`; the sample lane does not), so a pill that **is**
centred reports its centre at 1080 and the `offcenter` warning fires at exactly
`FRAME_W/2 = 540.0` px — on every split, including the two Miguel approved on
2026-09-02 (`sparkchrome_split`: 7 warnings, all of them this).

The waiver is pinned to that arithmetic and to nothing else: type `offcenter`,
page zoom > 1, measured offset 540 ± 1. A genuinely off-centre box does not land
on exactly half the frame width. Everything else in Gate 1 is still 0/0, and the
waived rows are listed in the report. **The instrument bug itself is not patched
here** — normalising that lane moves `EDGE_MARGIN`, `SEAM_MARGIN`,
`MIN_OVERLAP_PX` and `CENTER_TOL` on every split at once, which is a measured
change, not an overnight one. It is logged in `LEARNINGS.md`.

---

## (b) `phone_test_page.py <project>` — the Phone Test, with no video

Seeks the project's own GSAP timeline in headless Chrome exactly the way
`geometry_audit.py` does (same clip gate, same prime pass), screenshots the frame
at the composition's own encoded size, downscales to **405×720**, and crops each
declared object out **alone**.

The sheet, the judge's manifest and the **sealed answer key** are
`phone_crops.emit()` — the same function, imported, so the sealed-key discipline
has exactly one implementation in this factory.

Objects come from `--at`, `--plan` (`bespoke_objects`) or `--geom`
(`shared.phone_test_objects`). With none declared it emits **8 evenly spaced
whole frames** and marks the manifest `mode: "spaced-fallback"` — a legibility
sheet, *not* the Phone Test, and it says so.

### Parity, measured

`--parity <staged render.mp4>` cuts the same objects at the same timestamps
through `phone_crops`' own ffmpeg path and compares.

On `sparkchrome_split` against the staged 2026-09-02 render, six declared
objects:

```
every phone box identical: True
edge-mask IoU  min 0.969  mean 0.9824
```

Whole-frame fallback crops on `sparkchrome_cutout` come back at IoU 0.68-0.91,
because a browser `currentTime` seek lands on the **nearest decodable** frame
while the renderer lands on the exact one, and a whole frame is mostly the live
face band. **Judge a declared object, not a whole frame.**

Wall clock: **7.6 s** (split, 6 objects) and **8.7 s** (cutout, 8 fallback
frames), parity comparison included.

---

## (c) `draft_watch.py <project>` — buy the sense verdict early

A cheap Modal render, then `clerk_video_gemini.py` on it.

**There is no 540×960 render, and there is no resolution to drop either.**
`hyperframes render --resolution` takes presets only and requires an *integer
multiple* of the composition, so nothing below the composition's own size can be
asked for. And the daily **split page is already authored 2160×3840**
(`data-width="2160"`, `zoom:2`), so it renders at 2160×3840 with no
`--resolution` flag at all and `portrait-4k` on it is a 1× no-op; the cutout and
the whiteboard are authored 1080×1920.

**The entire saving is `-q draft`, and it is large.** Measured on the same
`sparkchrome_split`, 633 frames at 2160×3840: **80.1 s of render for $0.0061**,
against the high-quality 1080×1920 cutout's **100.2 s for $0.0146** — 2.4×
cheaper on a frame four times the size. The 540×960 artefact is one `ffmpeg`
scale off the draft (0.3-0.5 s) and exists for eyeballing.

**The watcher is fed the NATIVE draft, never the proxy.**
`clerk_video_gemini` re-encodes whatever it is given to 720×1280, so a 540-wide
input would be upscaled — a different input to the same model is a different
verdict, and this stage only earns its place if its verdict predicts the
post-render one.

```
exit 0   the draft rendered, no BLOCKING candidate
exit 2   blocking candidates — fix them, or waive each one IN WRITING
exit 1   the draft render or the watcher failed
```

It does **not** adjudicate. Gemini produces candidates; a clerk rules on them.
What this stage buys is seeing a candidate list while the page is still free to
change.

---

## The order, and it is the order

```
prerender_check  ->  phone_test_page  ->  draft_watch  ->  render_and_check
   (page laws)        (legibility)         (sense)          (the real render,
                                                             and its checks)
```

`pipeline/render/render_and_check.py` submits the real renders and starts **that
file's** `qc_pass` and **that file's** Gemini watcher the moment it lands, rather
than after the batch — and stages a render only once its own checks have passed.

The builder brief no longer carries a numbered list of check commands. The order
above is enforced by the workflow and by these two drivers, because a list is
something an agent can skip a line of and an exit code is not.
