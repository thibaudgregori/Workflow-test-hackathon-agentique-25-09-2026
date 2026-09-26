# Abik Shorts Factory — Locked Style Spec

Reverse-engineered from `Good Faceless Abik.mp4` and `Good Split Abik.mp4` (frame forensics + pixel
sampling + Gemini 3.1 Pro motion analysis). Canvas: **576x1024 @ 30fps** (rendered at 1080x1920, same
proportions; all px values below are in 576x1024 reference units). Duration ≈ **50.9s**.

## Shared source
- Audio: `assets/audio_tight.m4a` — raw narration with every pause capped at 0.15s (55.2s → 50.9s),
  matching the references' jump-cut tightening. Word timestamps: `analysis/transcript_tight.json`.
- Face footage (split only): `assets/face_bottom.mp4` (576x564 zone crop), `assets/face_full.mp4`
  (9:16 full), `assets/face_punch.mp4` (tight CTA zoom).

## Narration beats (tightened timeline, seconds)
| # | Beat | Start | End |
|---|------|-------|-----|
| 0 | Hook "Claude just gave away…single dollar" | 0.00 | 5.20 |
| 1 | Memory | 5.28 | 11.50 |
| 2 | Web Search | 11.62 | 18.35 |
| 3 | Projects | 18.46 | 25.50 |
| 4 | Extended Thinking | 25.62 | 32.05 |
| 5 | Connectors | 32.14 | 39.50 |
| 6 | "All on the free plan" + models | 39.56 | 47.90 |
| 7 | CTA "Comment free" | 48.02 | 50.91 |

---

## FORMAT A — Faceless

**Background**: constant warm off-white `#F0F3EE`, full frame, every scene.

**Palette** (pixel-sampled):
- Ink black `#111111` (titles, hook text), gray `#8C8C86` (subtitles)
- Claude terracotta `#C66748` (starburst logo motif)
- FREE yellow: face gradient `#FFC93C → #F5A623`, extrusion side `#C97300`
- Lime badge `#BEED4B` fill, `#111` text, subtle dark shadow
- Caption pill `#141716`, white text
- Card white `#FFFFFF`, card header bar white w/ divider, chat-bubble beige `#ECEADD`
- Traffic lights `#FF5F57 #FEBC2E #28C840`, saved-green `#3FA452`, "free" badge green `#4CD44C`
- CTA magenta `#B6339D` gradient (lighter top-left `#D45CC0` → deep `#9C2386`) with soft magenta glow

**Typography**: Poppins (SemiBold 600 titles-hook / Bold 700 feature titles / Medium 500 subtitles);
FREE = Archivo Black, uppercase, ~120px cap height, 3D extrusion 10px down-right; CTA FREE =
Montserrat 900 Italic ~86px with fake quotes; captions Poppins 600 ~30px white.

**Scene structure** (element geometry):
- **Hook 0.0-5.2**: starburst (76px, center x, y≈390) spins in (scale 0→1 spring 300ms, then slow
  continuous rotation ~45°/s); "Claude just gave away" / "almost everything" (34px, two lines,
  "everything" bold 700) drop in (-20px y, fade, 200ms, staggered); FREE 3D slams in at ~1.55s
  (scale 0→1.2→1 overshoot 400ms + micro shake); "without paying a single dollar" (22px gray) fades
  in ~2.2s. All exit at 5.2s via blur-push (scale→0.92, blur 0→14px, opacity→0, 250ms).
- **Feature scenes 1-4** (Memory 5.28 / Web Search 11.62 / Projects 18.46 / Thinking 25.62): white
  mock-app card (420px wide, radius 16, rotation alternates -2°/+2°/-2°/+2°, y-center ≈ 470,
  shadow 0 15px 35px rgba(0,0,0,0.08)); header bar: traffic dots + terracotta mini-starburst +
  Poppins-SemiBold app title; body = per-scene mock UI (see content plans). Lime `#N` badge
  (86x52px, radius 12, rotation +3°, counter to card) pinned overlapping card's top-left corner,
  pops in +120ms after card. Below card: feature title (44px, 700) then gray subtitle (24px, 500),
  each sliding up +100ms apart. Card entrance: scale 0→1 spring w/ overshoot ~350ms.
- **Scene 5 Connectors 32.14**: no big card. Lime `#5` badge pops top-center (y≈330), title
  "Connectors" (44px) below it, then 2x2 grid (icon tiles 88x88 white rounded-22 cards w/ shadow,
  official Google "G", Microsoft, Slack, Notion logos, labels 20px) pop in staggered 80ms
  left-right top-bottom. Grid center y≈590.
- **Scene 6 Free plan 39.56**: "All on the" (34px) → FREE 3D yellow (repeat of hook asset ~92px) →
  "plan" (34px) stacked at y≈300-430; model-picker card (-3° rotation, 420px) springs from bottom
  at ~40.6s: rows "Sonnet 4.6" (selected, beige row + green check), "Opus" + green `free` pill,
  "Haiku" grayed. Caption pill continues.
- **CTA 48.02**: bare background; "Comment" (36px black 600) drops in; `"FREE"` magenta italic
  (86px, Montserrat 900 italic, quotes, gradient + glow) slams in with overshoot; "and I'll send
  you the link" (22px gray) fades below. No caption pill.

**Captions (faceless)**: ONE word at a time in a black pill (radius 14, padding 14x26, center
y≈820), Poppins 600 30px white, lowercase except proper nouns; pop 0.9→1.05→1 (~140ms) on every
word; pill width animates to fit. Active only during feature scenes 1-6 (not hook, not CTA).
Sourced from `transcript_tight.json` word timings.

**Transitions**: no cuts — blur-push: outgoing group scales to 0.92, blurs 14px, fades out 250ms;
incoming elements spring in. Background never changes.

## FORMAT B — Split

**Geometry**: top content zone y 0-460; bottom face zone y 460-1024 (`face_bottom.mp4` 576x564).
Full-screen face interludes (`face_full.mp4`) replace the whole frame between features. CTA uses
`face_punch.mp4` zoom.

**Timeline of modes** (tightened timeline):
split intro 0-2.85 → full 2.85-5.25 → split S1 Memory 5.25-11.85 → full 11.85-13.30 → split S2
Web Search 13.30-18.40 → full 18.40-20.15 → split S3 Projects 20.15-25.10 → full 25.10-27.35 →
split S4 Thinking 27.35-32.10 → split S5 Connectors 32.10-40.50 → split S6 Models 40.50-47.45 →
full CTA 47.45-50.91 (glitch FREE overlay at 48.40).

**Top-zone backgrounds** alternate: intro dark `#101012`; S1 cream `#F6F1EA`; S2 dark; S3 cream;
S4 dark; S5 dark; S6 cream full-height feel (uses cream `#F6F1EA`).

**Split scene anatomy**:
- Header: italic serif number `01`-`05` (Instrument Serif Italic, ~64px, terracotta `#DD7259`) +
  feature title (Poppins 700, 34px, ink `#1E1E1E` on cream / white on dark), top-left at ~(52, 72),
  slide-up 30px + fade 400ms cubic-out.
- Content card: real claude.ai UI screenshot in white rounded-12 card (width ~480px, x-centered,
  shadow), slides up 50px + fade 500ms, ~500ms after header. Micro-interactions where applicable
  (toggle flips ~800ms after card lands, cursor moves, tooltip).
- Optional pill row: white rounded pills (JetBrains Mono 19px, ink text, padding 10x18, shadow)
  pop in staggered 150ms (e.g. `preferences` `projects` `conversations` under S1 card).
- Mono micro-label: `claude.ai · settings` style inside card headers (JetBrains Mono 18px gray).
- **Intro**: mono tracked label `C L A U D E · F R E E P L A N` (JetBrains Mono 16px, gray
  `#8A8A8A`, letter-spacing 8px, y≈68); cream card (476x196, radius 24) center y≈188 with serif
  wordmark "✳Claude" (terracotta starburst 40px + Lora 500 46px ink); at ~1.9s "EVERYTHING $0"
  slams below (Playfair Display 800 Italic caps, white 44px, "$0" terracotta 52px).
- **S4 Thinking (dark)**: custom dark card `#17171B` radius 14 w/ subtle border: header
  "✳ Thinking…" (Instrument Serif Italic 26px cream); orange-dot bullets in JetBrains Mono 19px
  (`break the problem into steps`, `reason through each step`) typing in sequentially.
- **S5 Connectors (dark)**: real claude.ai home screenshot card (greeting + composer) with cursor
  hovering the tools menu; below card a row of 4 white icon tiles (64x64, radius 16: Google,
  Microsoft 365, Slack, Notion, JetBrains Mono 17px labels) popping in staggered.
- **S6 Models (cream)**: serif wordmark "✳Claude" centered y≈155; two white pills side-by-side
  y≈287: `Sonnet 4.6` (ink 700 + terracotta "4.6"), `Opus` (terracotta 700). Pop in sequentially.
- **CTA glitch**: at 48.40, white "FREE" (Archivo Black 120px, chromatic aberration: red copy
  -6px x, cyan copy +6px x, sliced) hard-cuts over `face_punch.mp4` with a white exposure flash
  (opacity 0.55 → 0 over 350ms), flickers ±10% opacity, exits ~49.3 hard cut.

**Captions (split)**: phrases of 2-4 words from the transcript, indigo pill `#575CB6` (radius 12,
padding 10x18), Nunito ExtraBold 800 ~30px white, sentence case WITH punctuation kept; pill
x-centered; y-center = 460 (straddling the seam) in split mode, y≈735 in full-face mode (CTA:
y≈643). Hard swaps, no animation. Always visible (every phrase covered).

**Transitions (split)**: hard cuts between split and full-face modes (0ms). Inside a scene,
elements animate in but never crossfade between scenes.

## Audio design (both formats)
- Music: lo-fi hip-hop instrumental bed, ducked well under VO (~-16dB). Faceless: upbeat ~115 BPM.
  Split: jazzy laid-back ~85-90 BPM. Start at 0, fade out over final 1.5s.
- SFX: soft pop (card/badge/pill entrances), low whoosh (hook/FREE slams, scene pushes), deep boom
  (3D FREE hits), digital click (toggle flips), success ding (checkmark in S4). Mixed ~-10dB.

## Factory variation axes (style stays LOCKED)
Variants v01-v10 per category differ ONLY in: mock-UI sample copy (chat texts, project names,
search result text), pill-row wording, icon grid order, card rotation signs (mirrored), which real
UI screenshot crop/scroll is used (split), and SFX seed offsets (±20ms). v01 = closest clone of the
reference. Hook text, feature titles, subtitles, captions, timings, colors, fonts never change.

## QC rubric (pass required per video)
1. Layout & colors match this spec (bg, pills, badges, seam at 460).
2. Captions legible, synced within ~150ms of speech, correct style per format.
3. All 8 beats present, correct order/timing ±0.3s; no overlap glitches, no clipped text.
4. Animations feel spring/pop (no linear drift), transitions per spec.
5. Audio: VO clear, music under VO, SFX on entrances; no silence gaps/doubled audio.
6. Faceless: no face anywhere. Split: face zone correct crop, no letterboxing.
