# ROUNDFILL AUDIT — Global Law 3, retroactive sweep

> **GLOBAL LAW 3 (Miguel, 2026-08-30).** *"The straight bars at the end of
> rounded edge boxes is a big no no... UGLY AS FUCK... across multiple
> generations... that's a big no even for the formats and variants that already
> exist."*
> Any fill / progress / highlight inside a rounded-corner container must be
> clipped to the container's radius — never terminate in a hard straight edge.

Task id `roundaudit`. Swept: all six lab formats (`format_lab/*/*_gen.py`,
`*_lib.py`, `*_core.py`, `*_common.py`) **and** the production chassis
(`shorts_run7/gen/*_gen.py`, `shorts_run8/gen/*_gen.py`).

**Every site below was confirmed by decoding a frame from the actual render at a
moment the fill is partial.** No site was filed, and no fix was applied, on
static reading alone. Evidence lives in
`format_lab/_shared/roundfill_evidence/`.

**Result: 5 confirmed sites in the lab, all 5 fixed. 2 confirmed sites in
published production videos, untouched (listed for Miguel's call). 3 lab meters
confirmed already CLEAN and left alone.**

---

## 1. The two defect classes

**Class A — scaled rounded fill.** The fill carries the right `border-radius`,
but it is driven with `scaleX` / `scaleY`. A transform multiplies the *horizontal*
corner radius by the same factor as the width: at `scaleX(0.62)` a 12px radius
paints as 7.4px, at `scaleX(0.06)` a 10px radius paints as **0.6px** — a
dead-straight chop. The bar looks fine at 90% and disgraceful at 6%, which is
exactly why it survived several generations of review.

**Class B — square-edged fill in a rounded, `overflow:hidden` container.**
`overflow:hidden` only protects the **container's** corners. The fill's own
leading edge is a hard vertical chop sitting in the middle of a pill. This one is
wrong at *every* value, and it was even documented as if it were the fix
(`takeover_core.meter`'s old docstring claimed the square edge was deliberate).

**Class C (transient, NOT filed).** Rules, hairlines, stems and washes that wipe
`scaleX 0 → 1` and **complete**. Their leading edge is straight for ~0.3s during
the wipe, but they come to rest at full width with intact corners. Standard wipe
grammar; no resting defect was seen in any render. Listed in §6 as a watch list.

---

## 2. Canonical fix patterns

### R1 — HTML horizontal meter (Class A **and** Class B)

The rule: **a fill never has its own fill-axis scaled.** Animate `width`, which
lives outside the transform matrix, so `border-radius` paints a true
semicircular cap at every value. CSS's own radius clamp keeps a sub-diameter
fill a lozenge rather than a sliver, so even a 0% reading can never go straight.

```python
# AUTHOR — fill carries the track's radius and starts at zero width
f'<div class="abs" id="{p}-track" style="left:{x}px;top:{y}px;'
f'width:{w}px;height:{h}px;border-radius:{h/2}px;background:{track};'
f'overflow:hidden">'                                  # belt-and-braces
f'<div id="{p}-fill" style="position:absolute;left:0;top:0;width:0px;'
f'height:{h}px;border-radius:{h/2}px;background:{fill}"></div></div>'

# REACH — one property, floored at one cap diameter
def fill_to(p, t, frac, d, ease):
    return (f'tl.fromTo("#{p}-fill",{{width:"0px"}},'
            f'{{width:"{max(h, frac * w):.1f}px",duration:{d},ease:{ease},'
            f'immediateRender:false}},{t:.2f});')
```

Notes that cost time to learn:
* the px value **must be quoted** — `{width:157.5px}` is a JS syntax error;
  emit `{width:"157.5px"}`;
* `max(h, frac*w)` is the floor, not a nicety: it keeps the lozenge honest at
  tiny readings instead of letting CSS squash it to a circle-ish blob;
* geometry is recorded at author time (`METERS` / `FILLS` dicts) so the tween can
  resolve a fraction to real pixels. Where the tweens are emitted **before** the
  HTML (artifactspine's header, in v1/v2), pass geometry explicitly —
  `fill_to(..., geom=hd_geom(w))`.

### R2 — HTML vertical meter

Identical, animating `height` with the element pinned `bottom:0`. (Already the
shipped shape in `cutout_v3_gen.vmeter` — see §4.)

### R3 — SVG rect fill

Do **not** reach for a `clipPath`. In SVG a `userSpaceOnUse` clip-path lives in
the element's own coordinate system, so GSAP's transform scales the clip along
with the rect and the rounding it was supposed to guarantee evaporates. Animate
the `width` **attribute** and leave `rx` constant:

```python
b.shape(f'<rect id="mt-fill" x="{u(X)}" y="{u(Y)}" width="0" '
        f'height="{u(H)}" rx="{u(H/2)}" fill="{C}" opacity="0"/>')
b.set0('tl.set("#mt-fill",{attr:{width:0}},0);')
b.swap("#mt-fill", t, "attr:{width:0}", f"attr:{{width:{u(max(H, frac*W))}}}", d)
```

AttrPlugin ships in the GSAP core bundle these compositions already load, and
`Board.label` was already wiping its clip rect this way — the fix is idiomatic,
not novel.

### R4 — the translate alternative (already in production, and correct)

`shorts_run7/gen/cursordeal_counter_gen.py:962-967` reveals a full-width fill that
carries the track's radius by tweening `x` inside a matching rounded clip. Both
visible ends stay rounded. Valid wherever the fill is 100% wide and the reading
is expressed as how much of it has slid out of view.

---

## 3. CONFIRMED SITES — lab (all fixed)

| # | Format | File · line (pre-fix) | Element | Class | Render · frame |
|---|--------|----------------------|---------|-------|----------------|
| 1 | takeover | `takeover/takeover_core.py:209-222` `meter()` | `#{p}-fill` | B | `takeover/out/takeover_v1.mp4` **t=17.5, 18.0, 18.5, 19.0, 19.5**; also `takeover_v3.mp4` t=38, 50 |
| 2 | artifactspine | `artifactspine/artifactspine_core.py:198-205` `fill()` → `hd-fill` (:952) | `#hd-fill` | A | `artifactspine/out/artifactspine_v1.mp4` **t=8, 20, 36, 48** |
| 3 | artifactspine | same `fill()` → `r4-fill` (:607) | `#r4-fill` | A | `artifactspine_v1.mp4` **t=21.0, 21.5, 22.0** |
| 4 | artifactspine | `artifactspine_core.py:706-708` inline `div("r6-fill", …)` | `#r6-fill` | A | `artifactspine_v1.mp4` **t=35, 36, 37, 38** |
| 5 | facesplit | `facesplit/facesplit_lib.py:505-508` | `#cd-fill` | A | `facesplit/out/facesplit_v1.mp4` **t=40, 46** (clean-ish at t=22 where frac≈0.9 — the defect is a function of the reading) |
| 6 | whiteboard | `whiteboard/whiteboard_core.py:542-549` `mt-fill` + `cp-meter` | `#mt-fill` | A (SVG) | `whiteboard/out/whiteboard_v1.mp4` **t=28, 34, 46** |

Six element sites across five generator files — counted as **5 confirmed code
sites** because #2 and #3 are the same defective `fill()` primitive reached by
two callers, and one fix repairs both.

### What each looked like

* **takeover** — a pill-shaped rail, an orange brick, and a razor-flat right
  edge floating in the middle of it. The purest possible statement of the law.
  `roundfill_evidence/takeover_v1_meter_t17.5-19.5.png`
* **artifactspine `hd-fill`** — the header meter is on screen for essentially the
  whole video, and at t=48 the video's *final annotation ring* lands directly on
  the flat end. `artifactspine_v1_hd-fill_t8-48.png`
* **artifactspine `r6-fill`** — inside the 06 NOUS RESEARCH card Miguel called
  "the peak beat". Dark pill track with visibly rounded ends, orange stub with
  two square ones. `artifactspine_v1_r6-fill_t35-38.png`
* **artifactspine `r4-fill`** — CONTEXT BUDGET, a 72px bar at 62%: rounded left
  corners (crushed to 7px), dead-straight right end.
  `artifactspine_v1_r4-fill_t21-22.png`
* **facesplit `cd-fill`** — CONTEXT USED at the 0.205 resting reading: a 6px pill
  cap rendered as 1.2px. `facesplit_v1_cd-fill_t22-46.png`
* **whiteboard `mt-fill`** — mildest of the six (hand-drawn container hides a
  lot) but the same failure: rx=6 crushed to ~1.5du inside a hand-drawn rounded
  box. `whiteboard_v1_mt-fill_t22-46.png`

### Fixes applied (post-fix line numbers)

| Format | Change |
|--------|--------|
| takeover | `takeover_core.py:209` `METERS` registry; `:212` `meter()` now authors a `width:0` fill carrying `border-radius:h/2`; `:329` new `fill_to()` reaching by width. Call sites `:593` (1.0), `:655` (0.07), `:809` (0.08) moved off `grow_x`. |
| artifactspine | `artifactspine_core.py:198` `FILLS` registry; `:201` `fill()` authors width 0 with a live radius, no transform; `:312` new `fill_to()`; `:331` `hd_geom()`/`HD_BAR_H`/`HD_BAR_R` so `header_html` and `header_tweens` share one geometry regardless of call order; `:753` `r6-fill` authored at its real 6% width. Call sites `:881`, `:1021`, `:1027`. `header_tweens` gained `hd_w=` (v3 passes `TOP_CARD_W`). |
| facesplit | `facesplit_lib.py:512` `cd-fill` authored at width 0 with the pill radius, no `transform-origin`; `:539` new `cd_fill_to()`; six call sites `:560, :614, :615, :618, :630, :647, :657`. |
| whiteboard | `whiteboard_core.py:542-579` — `cp-meter` clipPath **deleted** (it scaled with its own element and did nothing), rect authored `width="0" rx="H/2"`, three `b.swap` calls moved to `attr:{width:…}`. |

### Verification of the fixes

1. **Generators re-run clean.** artifactspine v1/v2/v3 `build()`, whiteboard
   v1/v2/v3 `build()`, takeover v1/v2/v3 `C.build()`, facesplit `stage_html()` +
   `cd_fill_to()` — all execute and emit the expected markup/tweens. Every
   meter still has exactly one fill tween per variant; no `scaleX` remains on
   any `-fill` element.
2. **Live browser proof.** `roundfill_evidence/FIX_PROOF_before_after.png` —
   headless Chromium at 2× with the same GSAP 3.14.2 build the compositions
   load, rendering old vs new markup side by side for all three patterns (R1
   Class A, R1 Class B, R3 SVG). Old: flat bricks. New: true round caps.
3. Renders themselves are the rebuild agents' job; the generators are clean for
   them to inherit.

---

## 4. CONFIRMED CLEAN — no defect seen, nothing changed

| Format | File · line | Why it passes |
|--------|-------------|---------------|
| cutout v1 | `cutout/cutout_v1_gen.py:144` `meter()` | Fill carries its own radius **and** sits in a rounded `overflow:hidden` wrapper. Frames t=28/46/50 show a clearly rounded cap. `CLEAN_cutout_v1_meter_t28-50.png` |
| cutout v2 | `cutout/cutout_v2_gen.py:77` `hmeter()` | Same construction as v1. |
| cutout v3 | `cutout/cutout_v3_gen.py:106` `vmeter()` | Vertical twin; frames t=28/46 show a rounded top cap. `CLEAN_cutout_v3_vmeter_t28-46.png` |
| pureface | — | Surveyed v1 across t=10…50: face plus caption pills only. No fill inside any rounded container exists in this format. |

Cutout is the reference implementation and is *why* the law is cheap to obey —
it was already doing most of it. Its meters survive only because the bar is tall
(h=54, radius 23), so even a squashed cap still reads round; the R1 pattern is
strictly safer and should be adopted there too if cutout is ever regenerated for
another reason. **Not changed now — no defect was seen, and the law is
"no fix without a seen defect."**

---

## 5. PUBLISHED-VIDEO EXPOSURE — list only, NOT touched

Per instruction, `shorts_run7/` and `shorts_run8/` were **audited only**. No
production file was modified. Nothing here is fixed without Miguel's say-so.

### Confirmed carrying the defect

| Video | Run | Generator · line | Element | Class | Frame |
|-------|-----|------------------|---------|-------|-------|
| `mcpupgrade_icon.mp4` | run8 | `shorts_run8/gen/mcpupgrade_icon_gen.py:530-537` (`bore()`), driven by `current_rise` `:634` | `#b3-cur` | **B** | t=21.5, 22.0, 22.5, 23.0 — a hard-edged orange strip in a pill-shaped bore, top and bottom clipped to flat chords. Rests at `scaleX(CUR_THIN=0.26)` from "plug" to "energy" (~2s) before `current_widen` takes it to 1.0. `PUBLISHED_mcpupgrade_b3-cur_t21.5-23.png` |

### Mild — same code pattern, defect visible only under magnification

| Video | Run | Generator · line | Element | Class | Frame |
|-------|-----|------------------|---------|-------|-------|
| `hermesbuzz_kinetic.mp4` | run8 | `shorts_run8/gen/hermesbuzz_kinetic_gen.py:694` (`.tfill`), stepped by `growx` `:403` / `:1406` | `#…-fl` | A | t=24, 25 — the fill *does* keep a small elliptical cap (radius 5du crushed to ~1.5du). Squashed, not straight. Would probably survive review; the underlying pattern is the same one that fails badly at smaller radii. `PUBLISHED_hermesbuzz_tfill_t24-25.png` |

### Audited and cleared

* **All other run7/run8 `scaleX`/`scaleY` fills complete to 1.0** — a wipe with a
  transient straight leading edge, resting full and rounded. Machine sweep over
  all 26 production generators found no other element that comes to REST at a
  partial scale inside a rounded container. Cleared: `appsdistrib`,
  `billionusers`, `chatgptphone`, `deepseekbox`, `doers`, `harness`,
  `hermesvoice`, `livetranslation`, `mathconjecture`, `mcphidden`, `mythos`,
  `gpttranscribe`, `airtable`, `brainsdontmatter`, `buzzteams`, `geministt`,
  `hermessubagents`, `hermesvoicemagic`, `inkling`, `revolut`, `selfoptimize`,
  `skillssh`, `vendorlock`.
* **`cursordeal_counter.mp4`** (`cursordeal_counter_gen.py:962-967`) — clean by
  construction, and the source of fix pattern R4.

**Exposure summary: 1 published video confirmed carrying a visible straight-ended
fill (`mcpupgrade_icon`), 1 carrying the same pattern in a mild form
(`hermesbuzz_kinetic`), 24 clear.**

---

## 6. Watch list — transient, deliberately NOT filed

These wipe `scaleX 0 → 1` and come to rest at full width with intact corners, so
no resting defect exists and none was seen in any render. They do show a straight
leading edge for the ~0.3s of the wipe. Recorded here so a future round does not
have to re-derive that they were considered:

* `artifactspine_core.py` — `wash()` (`:231`), `strike()` (`:238`), `r4-stop` (`:650`/`:884`).
* `takeover_core.py` — the `-rule` and `-ceil` bars (`:619`, `:737`, `:871`).
* `whiteboard_core.py` — `#o-rule` (`:771`).
* `facesplit_lib.py:273` — the generic `wipe` helper.
* production: every `grow_x`/`wipex`/`grow` 0→1 in run7/run8.

If Miguel extends the law to cover wipe-transients, the fix is the same R1
pattern (tween `width` instead of `scaleX`) and every one of these is a
mechanical conversion.

---

## 7. Standing rule for future generators

> A fill, meter, progress bar, loading bar or highlight sweep inside a rounded
> container **reaches by `width` (or `height`, or `x`) — never by `scaleX` /
> `scaleY`** — and carries the container's own radius. `overflow:hidden` on the
> track is required but is never sufficient on its own, because it does not
> touch the fill's leading edge. In SVG, animate the `width` attribute with a
> constant `rx`; never rely on a `userSpaceOnUse` `clipPath`, which is scaled by
> the very transform it is meant to police.
