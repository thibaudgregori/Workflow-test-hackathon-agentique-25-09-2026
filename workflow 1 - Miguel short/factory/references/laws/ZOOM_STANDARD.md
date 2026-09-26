# ZOOM STANDARD — the 0% window and the zoom ladder

**Authority:** `format_lab/REVIEW_2026-08-30.md` **Global Law 7** (THE 0% ZOOM
STANDARD) and **Global Law 6** (25fps native). Underneath: `STANDARD.md`.
**Supersedes** `FRAMING.md` §5's `face_max_25` as the full-face reference — the
0% window is the same physical window, re-centred on a 64-frame union instead of
a 14-frame median. `face_wide_25` / `face_std_25` are unaffected and remain the
REST and MID plates.

Miguel, round 2: *"We have to come up with a sort of 'square' that we crop off
the main video that retains just my face as zoomed out as possible within all of
the frame that we're actually building out… determine that precise square where
I'm usually located. I call that a 0% zoom."*

---

## 1. THE 0% WINDOW

```
crop=1216:2160:1270:0      →  scale 1080:1920      (master 3840×2160)
```

| | |
|---|---|
| plate file | `_shared/face_zoom00_25.mp4` — 1080×1920, **25/1 CFR**, 1354 frames, 54.16 s |
| built by | `_shared/zoomstd_build.py` |
| scale factor | 0.88816 master px → canvas px |
| head on canvas | 1081 px = **56.3 %** of frame height |
| face (brow→chin) | **43.0 %** of frame height |
| head width | 65.9 % of frame width |

**Why 1216 × 2160 and nothing wider.** A 9:16 window cut from a 2160-tall master
can be at most `2160 × 9/16 = 1215` px wide. There is no wider full-bleed
vertical crop — the source physically cannot give one. 1215 is rounded up to
1216 to keep the width even for yuv420p; the resulting +0.08 % horizontal squeeze
is below perception. Height is the master's full 2160 at `y=0`, so nothing is
thrown away vertically either. **This window is the floor. "As zoomed out as
possible" is a solved constraint, not a preference.**

**Why x = 1270.** Free parameter. Set from the **union** of his head over the
whole master, not a median: 64 frames sampled evenly across all 54.17 s
(`zoomstd_measure.py` → `zoomstd_samples.json`), MediaPipe FaceLandmarker plus a
luminance silhouette scan for the black cap against the warm wall.

```
head left  min 1375      head right max 2382      union centre 1878.5
head width min 687  ·  median 809  ·  max 883      lateral sway 178 px
head top   min  216      chin max 1629            eye line median 873
```

`x = even(1878.5 − 1216/2) = 1270`. Round 1's median-derived x was 1266; the
union moves it 4 px right. Breathing margin at 0%: **105 px left / 104 px right /
216 px above the highest cap / 531 px below the lowest chin**, in master pixels,
against the *union* — i.e. across all 64 sampled frames his head never comes
within 100 px of a side edge.

**Verified on the render.** MediaPipe re-measured 7 frames of the finished
`face_zoom00_25.mp4`: face_frac median **0.425** (predicted 0.430), head_frac
median **0.550** (predicted 0.563) — inside round 1's ±0.020 tolerance, the gap
being cap-detection fallback on frames where the cap/wall edge is weak.
Container: 1080×1920, `r_frame_rate=25/1`, 1354 frames, 54.16 s.

**Relation to `face_max_25.mp4`.** Same width, x differs by 4 px. Renders that
already used `face_max_25` are not wrong and do not need redoing; new work uses
`face_zoom00_25.mp4` so every format shares one reference.

**Not a torso window.** His shoulder line spans ~2500 px of master. Nothing
9:16 and full-bleed can hold it (`FRAMING.md` §4). Shoulders-in framing is the
`face_wide_25` REST plate on a canvas the format owns, and that is unchanged.
The 0% window is the *full-face* reference only.

---

## 2. THE LEVEL TABLE

Level **N%** = a window of `(1 − N/100)` of the 0% window's dimensions,
re-centred so the eye line stays at the same fractional depth (0.4042 of the
window height). Composition is identical at every level — only tighter.

| level | master crop | scale k | head px | **head % of frame h** | face % of frame h | head cut on | side margin |
|---|---|---|---|---|---|---|---|
| **0 %** | `crop=1216:2160:1270:0` | 0.888 | 1081 | **56.3 %** | 43.0 % | 0/64 | 105 / 104 px |
| **5 %** | `crop=1154:2052:1300:44` | 0.936 | 1140 | **59.4 %** | 45.4 % | 0/64 | 75 / 72 px |
| **10 %** | `crop=1094:1944:1332:88` | 0.987 | 1202 | **62.6 %** | 47.8 % | 0/64 | 43 / 44 px |
| 15 % | `crop=1032:1836:1362:130` | 1.047 | 1274 | 66.4 % | 50.7 % | 0/64 | 13 / 12 px |
| 20 % | `crop=972:1728:1392:174` | 1.111 | 1353 | **70.5 %** | 53.8 % | **3/64** | **−17 / −18 px** |

Aspect error across the ladder: −0.07 % … +0.08 %. All windows sit inside the
master; all are even-dimensioned.

Machine-readable: `_shared/zoom_standard.json` (`levels[]`, each with `crop`,
`ffmpeg_crop`, `ffmpeg_vf_tail`, margins, clip count, re-centre band).

**Fallback windows inside the rendered 1080×1920 plate** — use only when the 4K
master is not at hand; cropping the already-scaled plate costs a second resample.

| level | window in `face_zoom00_25.mp4` |
|---|---|
| 0 % | `1080×1920 + 0 + 0` |
| 5 % | `1026×1824 + 26 + 40` |
| 10 % | `972×1728 + 56 + 78` |
| 15 % | `918×1632 + 82 + 116` |
| 20 % | `864×1536 + 108 + 154` |

---

## 3. THE CROP-CUT RULE

Round 2, verbatim: *"the footage EXPANDING (scale animation) looks off. Zooms
must be CROP CUTS within the 0% frame."*

1. **A zoom is a different crop window, cut to on a single frame.** Never a
   `scale`/`transform` animation of the footage, never a tween between two
   windows. At 25 fps even a 0.05 s tween renders an intermediate scale and
   reads as a smear.
2. **Cut from the 4K master** with `ffmpeg_vf_tail` (crop → scale 1080×1920).
   One resample, full detail. The plate-space windows in §2 are a fallback.
3. **The window is STATIC for the whole hold.** A window that follows his face
   frame by frame is a camera move and violates Global Law 5.
4. **Re-centring is per-cut, and bounded.** A window may be re-centred
   horizontally on his face position *at the cut*, then frozen. Travel from the
   0% centre is capped by the level's `recentre_band_px` — ±136 (5 %), ±106
   (10 %), ±75 (15 %), ±45 (20 %) — beyond which his widest measured head
   (883 px) no longer fits.
5. **Minimum hold after a punch: 0.4 s** (inherited, `guard_punch_holds`).
6. **Return is also a cut.** Coming back to 0 % is a cut, not a pull-out.
7. **Every level renders at native 25 fps** with the de-conform applied
   (Global Law 6, `FRAMING.md` §7). Judder is invisible at REST scale and
   obvious at full-face scale, which is exactly where this ladder lives.

---

## 4. RECOMMENDATION — default punch **5 %**, hard ceiling **10 %**

**Ship 5 % as the default punch. Cap every format at 10 %. Do not build 15 % or
20 % windows.** Three independent measurements land on the same answer.

**(a) The 0% window is already at the reference reel's ceiling.**
`FRAMING.md` §3 swept `references/ref2_instagram_split.mp4`, the reel Miguel
picked: its full-face mode runs face_frac 0.359 → **0.419 max**, median 0.393.
Our 0 % sits at **0.430** — 2.6 % *above* the most zoomed frame that reel ever
uses. We do not start with headroom; we start at its top. Every step up the
ladder spends borrowed room:

| level | face_frac | vs reference max (0.419) |
|---|---|---|
| 0 % | 0.430 | +2.6 % |
| 5 % | 0.454 | +8.2 % |
| 10 % | 0.478 | +14.2 % |
| 15 % | 0.507 | +21.0 % |
| 20 % | 0.538 | +28.5 % |

**(b) 15 % and 20 % re-enter the band Miguel already rejected.** Round 1
measured the rejected renders at head 66–72 % of frame height (`takeover_v1`
worst frame 72.3 %; `pureface_v3` p90 66.0 %, max 73.2 %). 15 % lands on
**66.4 %** and 20 % on **70.5 %** — the same pictures, rebuilt. Shipping them
would re-file the complaint.

**(c) 20 % physically clips him.** His head sways 178 px laterally. A static
20 % window centred on the union cuts the head on **3 of 64** sampled frames
(−17 px left, −18 px right of the union). Per-cut re-centring at 20 % has only
±45 px of band, less than a quarter of his sway, so a hold long enough to matter
will catch a clipped frame. 0–15 % clip nothing.

**Why 5 % and not 10 % as the default:** 5 % is a +5.5 % head growth — enough to
register as a beat change against a cut, small enough to stay inside the
"small zooms only" instruction, and it keeps 10 % in reserve as a genuine
top-of-video accent. 10 % (+11.2 % head) is the strongest punch that stays out
of the rejected band, so it is the ceiling, not the default.

**Grammar reminder:** size changes bigger than this ladder are **mode switches**
— cut to `face_std_25` or `face_wide_25` — not deeper crops. That is the
takeover grammar Miguel approved, and the 0 % window is where every full-face
beat in every format now starts.

---

## 5. Files

| file | what |
|---|---|
| `zoomstd_measure.py` | 64-frame union sweep → `zoomstd_samples.json` |
| `zoomstd_derive.py` | union → `zoom_standard.json` (0 % window + ladder + margins) |
| `zoomstd_build.py` | renders `face_zoom00_25.mp4` (25 fps native, de-conformed) |
| `zoomstd_sheet.py` | renders `zoom_ladder.png`, the contact sheet |
| `zoom_ladder.png` | **for Miguel** — 0/5/10/15/20 % on one master frame, labelled |
| `face_zoom00_25.mp4` | the 0 % plate, 1080×1920 @ 25/1, 1354 frames |

Staged for review: `~/Movies/Shorts Factory/Format Lab/Fixed2/zoomstd_face_zoom00_25.mp4`
and `…/zoomstd_zoom_ladder.png`.

**Generalising to future recordings** (any 4K 16:9 master): `0% crop_w =
master_h × 9/16`, full height, x centred on the union of the head across the
whole cut master. Level N is `(1 − N/100)` of that, eye line held at its 0 %
fractional depth.
