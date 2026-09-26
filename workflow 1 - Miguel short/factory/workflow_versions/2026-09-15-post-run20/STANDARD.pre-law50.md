# Production procedure update — 2026-09-05

Read [PRODUCTION.md](PRODUCTION.md) for current execution. FIVE-word independent phone naming, sure confidence, no known-failure rendering, soft-alpha MatAnyone finishing and final-review-only delivery supersede older procedural wording below. Bespoke creation and all visual quality requirements remain.

# The Reel Standard — v1 (from Miguel's full 100-video review, 2026-08-09)

Every future reel follows these guidelines. This supersedes VARIANT_LANES.md as the design
contract; the QC rubric derives from the LAWS below.

## Lane verdicts (what survives)
| Lane | Verdict | Notes |
|---|---|---|
| V04 Icon Choreography | ⭐ FLAGSHIP | "So close" to target quality. Logos + clean diagrams + icon highlights (the fablevssol highlight-scramble = benchmark: "chef's kiss"). |
| V01 Kinetic Type | KEEP | Great for intros & theme-matched aesthetics (terminal look for CLI topics = "nailed it"). Trim text volume — never redundant with captions. |
| V02 Counter & Meter | KEEP (support) | Use where real numbers exist. Context-fill, price-drop bars, scorecards, counter upticks all approved. Not monotonous walls of meters. |
| V03 Diagram Build | KEEP (support) | Best moments approved (cage break, meatwrapper relay). Needs the geometry laws below. |
| V05 UI Pan & Highlight | SALVAGE the highlight, KILL the pan | Highlight on a STATIC asset synced to speech = "fantastic". Perpetual panning/drifting = banned. |
| V06 Steps & Checklist | KEEP (support) | Clean checkboxes fine; items must be MY words, tick in sync with speech; needs logos; no "header" feel. |
| V07 Split Comparison | ❌ DEAD (2026-08-09 chat) | Even with a fixed divider "it wouldn't make a difference" — retire. |
| V08 Quote Pull | ❌ DEAD | "Captions x2, no added value" — retire the lane. |
| V09 Timeline Rail | ❌ DEAD | Eats screen real estate, monotonous, double-rail bugs — retire. |
| V10 Shape & Pattern | ❌ DEAD | Pretty but adds no understanding — retire. |

## Production model (2026-08-09 chat)
- **Menu, not monolith:** the agent picks from the approved lanes and produces **3 variants per
  video, plus 1 bonus WHITEBOARD variant** (pilot 2026-08-09) — a reviewable volume. Creative
  freedom inside the menu; never 10-per-video floods.
- **WHITEBOARD mode (experimental bonus lane):** one continuous canvas for the whole short —
  elements accumulate, transform, and get annotated across beats (a diagram grows, icons persist
  and relocate, terms get circled/crossed out, arrows extend) instead of discrete scene swaps.
  Feels like watching one drawing being reasoned on. All LAWS apply (event-driven motion + holds,
  logos, no header, geometry); the canvas may pan/reflow ONLY as a discrete transition event when
  space runs out, never continuously.
- Approved menu: Icon Choreography (flagship) · Kinetic Type (theme-skinned intros/aesthetic) ·
  Counter & Meter (only where real numbers live) · Diagram Build · Steps & Checklist (sparingly).
  The speech-synced HIGHLIGHT is a move available inside any lane, always on static assets.
- **"Whiteboard" clarified:** it means NO static header chrome eating real estate — the full top
  zone belongs to the visuals. (Not accumulation/persistence across beats; discrete beat scenes
  are fine. Continuity experiments allowed occasionally.)
- **Stutters:** no aggressive re-cutting of the footage needed; but stutters/false starts NEVER
  appear in captions (drop partial words).
- **No image generation, ever** — all 2D is coded dynamic diagrams (SVG/CSS/GSAP).

## THE LAWS (violations = QC fail)
1. **NO idle motion. Ever.** No levitation/floating/perpetual drift/continuous zoom or pan.
   Motion = purposeful builds, transitions, ticks, highlights — then the element HOLDS STILL.
   ("Alive through events, not idle animation." Replaces the run-2 anti-static drift habit.)
2. **Logos are a must.** Any named tool/model (Claude Code, Grok Build, Codex, Nous Research…)
   renders as its logo, not a text pill. Model-focused shorts may keep the model logo throughout;
   multi-tool shorts show icons once for the visual grasp, then switch to concept diagrams.
3. **Tweet discipline.** The tweet appears only when it genuinely IS the news (source credibility),
   for 2–4s max, then leaves. Never open on a low-value tweet. NEVER show tweet metrics
   (likes/reposts/views). On-screen claims track what I SAY, never tweet copy. The asset judge
   must score the tweet's text AND visual value before allowing it.
4. **Captions live at the seam only.** No captions/top-text duplicating the spoken words anywhere
   else — no top captions, ever. A text-only top section is a failure: the top half is a
   WHITEBOARD for visuals (no "header" sections), because reading is what captions are for.
5. **Highlight system (the crown move).** Highlights land on the exact region matching the words
   being spoken, on a STATIC asset (no pan underneath). Semantic mismatch = QC fail.
6. **Stutter policy.** Stutters/false starts are cut aggressively from BOTH audio/video and
   captions (drop partial words entirely — never caption a stutter).
7. **Geometry laws.** Centered compositions; even spacing between lines; same-theme cards =
   same size; arrows terminate AT box edges (never on top of the target box); icons proportionate
   to their containers; nothing touches anything (pills vs cards, bars vs bars); no clipping or
   overflow ever (16,000-rows class bugs).
8. **Small-screen legibility.** Assets must read on a phone. Crop images to the crucial region;
   minimal info + a highlight beats a full screenshot. If an asset is unreadable at short-size
   (hermes bench image), don't use it.
9. **Key-term first.** The video's core term ("offices of slop") debuts CENTER STAGE large,
   then visualizations follow.
10. **Unique themed outros stay** — each video's outro matches its visual theme + handle chip.
    Channel identity: **Miguel Torrez AI**.
11. **Factual placement matters.** Diagram positions are claims (Codex ≠ open source even if the
    CLI is). Verify chart/diagram semantics like copy.
12. **Content accuracy of interactive/physical metaphors** — e.g., ripple sims must ripple
    plausibly (interference at walls), or simplify the visual.

## GRAPHIC CHART — the top zone's look (Miguel, 2026-09-06, after run 16: "EVERYTHING diverged on the top of the screen")

Every short in the catalogue shares ONE visual language above the face, and it is not up to an author. Run 16's three authors (a different agent lane, briefed to "invent fresh artwork") each invented a new one — Poppins everywhere, heavy filled shapes, a dark full-bleed world, one logo repeated fifty times — and every top zone went to the garbage. **The chart is the run-15 cutouts and splits** (`shorts_run15/gen/{geminitools,harnessrace,shieldstral}_scene.py`, their projects, and the 32 published shorts before them). Reproduce that look; a new visual language is a rejection before render.

1. **Ground: CREAM.** World `#F6F1EA`, cards `#FFFDF9`, mounts `#EFE7DC`. Never a dark or saturated full-bleed ground (the chassis' own law: cream only while the subject is dark).
2. **Ink: one near-black, one accent.** Ink `#141416`; terracotta `#C4573A` (light `rgb(221,114,89)`) for connectors, emphasis flips and the caption pill; muted ink `rgba(20,20,22,.34)`, hairlines `rgba(20,20,22,.15)`, line ink `rgba(20,20,22,.55)`, tile edges `rgba(17,17,17,.16)`. No navy, no teal, no purple, no green worlds.
3. **Type: JetBrains Mono for the story, uppercase.** The key term and every kicker/label in the top zone are JetBrains Mono, UPPERCASE, letter-spaced (key term ~48 px core / letter-spacing 2; labels small). Poppins is the chassis' display face for a word set the chassis itself types (a lockup, a count); it is never the label face. Nunito 800 is the caption pill only.
4. **Drawing: thin ink-line illustration.** Objects are SVG line drawings on cream/card fills with INK outlines (stroke 6-12 at core scale, round caps/joins), a plug, a stopwatch, a shield: silhouette first, few interior lines, no heavy filled blocks, no gradients, no shadows, no 3-D.
5. **Marks: real registry logos in tiles.** Tiles 112 px, 3 px ink-alpha border, radius 18, the mark's INK sized to 0.50 of the tile (`mark_img`); the product mark over the company mark; never a text pill, never a placeholder shape.
6. **Connectors and emphasis:** terracotta lines that terminate at box edges; emphasis is the panel border flip or the marker highlight; never rings.
7. **Cutout lanes:** the depth field carries a MIXED set of real topical marks (the ones the short names plus their obvious neighbours, `plan.cutout_logo_lanes`), never one mark repeated and never the story's own subject mark.
8. **Outro:** the chassis lockup (`captions.outro_chip_html` + `outro_daily_html`): terracotta rule, JetBrains Mono `@handle`, `daily AI` micro-line, on the video's own themed object. Not a Poppins chip.
9. **Before delivery, the orchestrator holds a contact sheet of full frames next to a run-15 frame.** Same ground, same type, same line weight, same tile grammar, or it does not ship.

---

## PILOT VERDICT — Miguel, 2026-08-10 (locks v1.1)

Watched via the 4-up comparisons. **Column order = enjoyment order on every
video, left best.** Global lane ranking:
1. **Icon Choreography** — flagship confirmed, wins everywhere it appears
2. **Kinetic Type**
3. **Counter & Meter** / **Diagram Build** (mid-field)
4. **Steps & Checklist** (low) and **Whiteboard LAST on all 10** — the bonus
   experiment did not win. As implemented it is out: textured/dotted canvas
   backgrounds are BANNED ("looks horrible", "shitty background"), no divider
   lines through logos, no stray handles floating on the canvas.

### New laws from the verdict (all recurring defect classes)

- **FILL THE SHAPE.** Inner elements must match their container's geometry: no
  circle checks inside rounded-square boxes, no rounded boxes inside sharp
  boxes, icons must fit their plate (grokprice conversations/loops/coding
  agents, reasoning, image gen). Miguel: "If you are going to fill gaps, the
  gaps have to make the shape!"
- **BUILD ORDER.** Connectors/stems appear AFTER the nodes they join, never
  before (hermes diagram grew stems before logos). Chrome never precedes
  content (checklist showed "then build" + empty checkboxes before anything
  began).
- **OUTRO ALIGNMENT.** The exit screen is a deliberate composition: if
  "Follow" is centered, everything else on screen must be part of that centered
  layout, and pointers must point at things that are actually there. Recurring
  on hermes, meatwrapper, slop, threed ("the diagram at the end is odd, as
  usual").
- **SEAM IS SACRED — promoted to audit ERROR.** Nothing touches the caption
  chip or the orange divider bar: "Creative work" touching captions, the X
  Premium+ card touching captions, AI icons touching the divider in outros
  (hackers, productivity), content cut by an orange bar (threed).
- **HIGHLIGHT DISCIPLINE.** Highlights inherit their target's transform (the
  test-cage highlight must tilt with the cage), respect collisions with
  neighboring elements (productivity $20-100/month), and never land on text too
  small to read (meatwrapper code text).
- **ATTRIBUTION.** The source handle (@composio, @xfreeze) belongs ONLY on the
  tweet card / first screen — never floating on later screens or canvases.
  Third-party demo footage (v0) gets light, discreet credit at point of use,
  and its placement must be considered, not dumped.
- **METERS COMPLETE.** A fill bar that never reaches full is a bug, not a
  style (grokprice counter timeline).
- **ASSET HEALTH.** The 3-dot/2-line "connection" glyph renders broken (hermes
  icon + whiteboard) — replace it; audit assets before use.

### Fact corrections (from this verdict)

- **TRANSCRIPT IS TRUTH (Miguel, 2026-08-10).** The spoken word is canon.
  Visuals NEVER "correct" the transcript — if a card disagrees with what Miguel
  said, the card is wrong, full stop. No agent theorizes about misspeaks or
  transcription errors: hermes says "procedural disclosure", so the cards
  showing "PROGRESSIVE DISCLOSURE" are the defect (icon/counter/whiteboard).
  The 2026-08-10 gate workers' "the card fixes a factual error" reasoning is
  exactly the move this law bans.
- **"ex xAI" is not a stutter** — xAI is now SpaceXAI, so "ex xAI" is a fact.
  Caption stutter-filtering must whitelist it (grokbuild).
- The grokbuild whiteboard evolution chart is "quite bland" — charts need the
  same design energy as the rest of the lane.

## RUN-6 REVIEW VERDICT — Miguel, 2026-08-12 (three new laws; no re-renders)

Review of the run-6 batch (agentreviews "very solid", grok46 "very clean").
The three shipped; these laws bind every build from now on.

- **COLOR MARKS (Law 12).** Brand marks ship in their ORIGINAL brand colors,
  never monochrome reductions — "always use the colored versions, they look so
  much nicer". This supersedes the run-6 monochrome-marks convention (the
  grok.png precedent, `deepseek-mark`, the black ElevenLabs "II") and retires
  "one accent per ground" as a reason to strip a logo's own palette. The
  accent-discipline rule still governs OUR OWN shapes (connectors, highlights,
  fills) — it just never applies to a brand's mark. Registry entries added as
  `*-mono`/`*-mark` monochrome variants stay for reference but are no longer
  the default pick.

- **UNIQUE VISUALIZATION (Law 13).** Icons and diagrams are the floor, not the
  ceiling. Every short should reach for at least one bespoke, animated,
  scene-level visualization tied to the story's central metaphor — the hermes
  tools video ("so unique and animated and visual") and the boat illustration
  are the named precedents; `shorts_run5/gen/hermes_icon_gen.py` is the
  canonical reference build, joined 2026-08-13 by
  `shorts_run6/gen/hermesjourney_icon_gen.py` (the journey constellation —
  "absolutely amazing… this is the level of quality I expect") and the
  builders BUILDER FIELD globe + perplexity balance scale ("FANTASTIC use of
  the scale"). "Very clean but generic" loses to "unique and
  catchy" every time. This is a design-ambition law, not a gate check: plan the
  bespoke scene at plan time, in the beat where the story peaks.

- **CENTERED COMPOSITION (Law 15; Miguel, 2026-08-13 review).** An element that
  mediates between two anchors (a wave between two plates, a connector between
  cards) sits CENTERED on the axis between those anchors — "try to avoid doing
  non-centered things like that." When a sequence swaps elements of different
  sizes, the optical center must hold: either normalize sizes so height and
  centering stay consistent, or fade each element in/out in place. Never let a
  beat drift visibly off-center relative to its own anchors (gptvoice: waves
  off-axis from the human/computer plates, the live-conversation lane, and the
  translation ending were all this class).

- **NO DEAD SLOTS (Law 16; Miguel, 2026-08-13 review).** Every drawn slot,
  lane, or track must activate within its beat. A paired element that never
  fills is "lost real estate for nothing" (gptvoice: the second speech-to-text
  lane drawn but never filled). Deliberate emptiness as storytelling does NOT
  survive review — if it stays inert, cut it or fill it. This sharpens FILL THE
  SHAPE: not just filled space, but every promise the layout makes gets kept.

- **REAL TWEET (Law 14).** When the source is an X post, show the ACTUAL tweet
  (screenshot media in a `shot()` card, highlight ring landing on the claim as
  Miguel says it — the `tweet_block()` treatment in
  `shorts_run5/gen/hermes_icon_gen.py`), never a coded re-creation of it. The
  provenance judging stays for accuracy (right post, legible at phone size, no
  misleading crop), but "asserts claims Miguel doesn't say" is handled by the
  highlight ring scoping what the eye reads — not by rejecting the real tweet
  and rebuilding it as a card. Coded cards remain for non-tweet sources that
  fail legibility.
  ANONYMOUS-ORIGINAL EXCEPTION (Miguel, 2026-08-13, grokimagine): the
  quote-tweet-to-original rule yields to credibility — if the quoted original's
  account is visually anonymous (blank avatar, empty or invisible display
  name), its card reads as a rendering bug on screen ("@blankspeaker"). Ship
  the credible quoting post (usually the handed URL) when its own text carries
  the claim. PROPER-NOUN SPELLING: names of real people/products on captions
  and plates follow the source payload's own spelling (the account name), not
  the transcriber's guess — Turturean not Terturian, Imagine not Imagen.

## 2026-08-13 EVENING REVIEW — two more laws

- **NO FACES (Law 17).** Coded human figures ship as SILHOUETTES or filled
  person glyphs only — never with rendered facial features. Eyes, mouths, and
  face detail on drawn avatars "look extremely weird" (Miguel, rejecting the
  heygen faces outright). Silhouette figures (grokimagine) and solid person
  glyphs (elevenagents, smallteams) are the approved treatments. If a story
  needs a face (lip-sync, expressions), represent it abstractly — never a
  drawn face. Real photographs of real people (Miguel's own face crop, avatars
  inside REAL tweet cards) are exempt: the law bans drawn faces, not real ones.
  ADDENDUM (Miguel, 2026-08-13 evening — heygen v2 ALSO rejected): never
  composite an object onto a silhouette's face region either. "Putting things
  in front of its mouth looks extremely weird." Silhouettes remain legal as
  passive figures (grokimagine), but when the STORY is about a face, mouth, or
  expression, drop the human figure entirely and tell it through objects — the
  video player, the transcript, the waveform. No human silhouettes in
  face-driven stories, full stop.

- **UNDERLINE = WORD SPAN (Law 18).** An underline extends AT MOST to the ink
  width of the words it underlines. Longer "looks like it's meant to be a
  divider when in reality it's an underline" (Miguel, on mathvoice and
  oneprompt). Underline primitives must take their width from the measured
  text span (ink_span of the underlined words), never from the lockup, column,
  or a hand-set constant. Dividers remain legal — but a divider sits between
  blocks, never directly under a phrase it could be misread as underlining.

## 2026-08-16 FABLE BATCH REVIEW — verdicts + Law 19

First Fable-built batch (run 7). harness_diagram: "fucking amazing, frankly
unbelievable… incredibly good animation. Bravo!" — joins the Law-13 named
references (`shorts_run7/gen/harness_diagram_gen.py`). mythos_icon: approved
clean ("super good, unbelievable"). mcphidden + billionusers: fix passes.

- **START CENTERED (Law 19; Miguel, 2026-08-16).** "I always want things to be
  centered when starting off." An element that opens a beat alone STARTS
  CENTERED on the composition axis — even when more items will join later.
  The choreography is: appear centered → MOVE to make room as the next item
  arrives (an animated displacement, part of the story) → later items may then
  appear in place without re-centering everything ("when you do the first
  displacement the rest of the things can actually just stay where they are").
  NEVER pre-position an opening element off-center in anticipation of items
  that have not appeared yet (mcphidden 28s: mock UI parked left waiting for
  an MCP plate on the right; 32s same class). This extends CENTERED
  COMPOSITION (Law 15) into time: Law 15 governs where things sit, Law 19
  governs how they arrive.

### Second-round verdicts (2026-08-16) — new canon

- **THE OCEAN is a Law-13 named reference** ("the lake with the water that
  expands and then barely even moves vertically is amazing"):
  `shorts_run7/gen/billionusers_counter_gen.py` b2. The transferable principle:
  when a story opposes two magnitudes, make them ONE substance seen at once —
  one body, no seams, no paired gauges. Joined the reference list alongside
  hermes, hermesjourney, Climb Collapses, BUILDER FIELD, the balance scale,
  and harness.

- **MOCK-UI ANATOMY (craft reference, not a law).** When a beat shows product
  UI, build REAL anatomy, not lorem chrome: colored registry marks + real
  product names + honest controls (headers, toggles, input-style fields),
  lockups sized off rendered ink. Reference: the mcphidden v2 connectors panel
  (Google Drive / GitHub / Notion rows) — "so much better than what you did
  before." Combine with the standing UI rule: flat, big, unrotated, no device
  frames.
  RULING (Miguel, 2026-08-16, overturns a builder judgment): docking sockets,
  ports, and any interior furniture live fully INSIDE their card with visible
  margin — never touching, straddling, or hanging off the card edge
  ("annoying"). Connector lines may cross the card border to reach an interior
  socket.
  VERIFICATION RULE: every annotation (ring, highlight, callout) is verified on
  a decoded frame from its ACTIVE window — a highlight that is only on screen
  for a beat escapes every static-state check (the mcphidden ADD-ring escape).

- **Junction polish note (harness, logged not law).** Where connector lines
  meet a box, connecting at/near the box corner lets the square corner edge
  peek through the joint. Prefer junctions landing on straight edge segments
  clear of the corner radius, or seat the joint so no corner shows. Miguel:
  tiny detail, no re-render required — but future builders should land stems
  mid-edge.

## 2026-08-19 REVIEW — Law 20 (the opening carries a state, never an empty vessel)

Run-8 round 2 verdict. mcpupgrade, hermesbuzz, airtable, buzzteams, geministt,
inkling, revolut, selfoptimize and the rest: approved, "very nice as usual".
ONE remark, on brainsdontmatter: *"I dislike the fact that the opening is very
'static' — we see two gauges not doing anything for like 5-10 seconds. This
doesn't match our always dynamic style. Rest is very nice, it's just the first
couple of seconds."*

- **THE HOOK IS A LAW-13 SURFACE (Law 20; Miguel, 2026-08-19).** Second remark,
  after a first fix pass missed: *"It sucks so bad. Why don't we have some
  unique visualization with a brain or something? This really looks so so bad
  at the beginning. no dynamism whatsoever."* The opening does not merely need
  a readable state — **it needs its own bespoke subject**, built to the same
  standard as the peak-beat visualization Law 13 demands. Chassis furniture
  (a gauge, a meter, a trough, a plate) is not a subject, however it is posed:
  filled, pegged, empty or animated, it is still furniture, and a hook made of
  furniture reads as nothing happening. Give the hook the video's IDEA as an
  object — brainsdontmatter's fix is a two-hemisphere brain that draws its
  folds on the opening line and then GROWS in word-synced steps while the
  performance meter answers each growth a beat late, that lag being the old
  rule the next scene tears apart.
  - Corollary (the vessel rule, which is necessary but NOT sufficient): never
    park an empty vessel in the opening — an unfilled gauge, empty trough,
    blank plate or empty outline says "nothing has started yet" exactly when
    the viewer decides whether to stay. Withhold it until the beat that fills
    it. **Satisfying this corollary alone is what failed review**: pass 1
    opened the fader pegged at its ceiling, which is a legitimate state and
    still got rejected, because the hook had no subject.
  - Applies to the OPENING ONLY. Mid-video an empty container is a legitimate
    beat (harness at 50s is one white outline on a dark ground filling the
    whole visual zone, and it is correct there).
  - Measured case: brainsdontmatter opened on an INTELLIGENCE gauge at rest and
    a PERFORMANCE bar at zero. The bar first paints at 1.2s and then measures
    EXACTLY 0.0 motion from 2s to 7s; the gauge is frozen 1s-5s. Between t=2 and
    t=5 the only moving thing on screen is the caption band.

- **DO NOT turn this into a motion threshold.** Three separate global metrics
  were tested against the whole approved corpus (n=23) and every one of them
  condemned work Miguel had already praised:
  | metric | brainsdontmatter | approved corpus | verdict |
  |---|---|---|---|
  | mean frame motion, first 5s | 14.3 (LOWEST of 24) | 18.0-43.2 | would fire, but see below |
  | visual-zone motion, first 10s | 2.84 | doers **1.84**, harness **1.98** | condemns two approved diagrams |
  | longest inert visual run | 3.8s | harness **4.2s**, gpttranscribe **5.2s** | condemns the Law-13 reference |
  Per-element parking fails too: harness's right-hand dashed slot sits unchanged
  **5.2s** — LONGER than the dead bar Miguel disliked. **Harness is objectively
  stiller than the video he rejected by every instrument tried.** Stillness is
  therefore NOT the defect and must never be gated. The defect is an opening
  that shows an empty vessel; judge it by what the frame CONTAINS, not by how
  much it moves.

## AUDIO MIX LAW (Miguel, 2026-08-17)

- Voice track `data-volume="1"`, bed `data-volume="0.065"` (was 0.13 — measured
  only ~12 dB under the voice because bed_split_v2 is mastered ~6 dB hotter
  than the recordings; 0.065 lands the standard 18+ dB speech margin). SFX stay
  at 0.18. Never judge a mix by the gain constant alone: source loudness is
  part of the math — measure the pause floor of the final mix.
- **Pinned instrument (2026-08-18).** The margin is speech minus pause floor =
  p85 minus p15 of frame RMS, on a mono 16 kHz **s16le** decode (never `f32le`,
  which reads +3.01 dB), at a **33 ms** frame. State the frame size next to any
  dB figure: the same file reads 18.03 at 10 ms, 16.88 at 33 ms, 14.33 at 100 ms.
- **Reference band, not a hard floor.** Measured on this instrument, the thirteen
  approved and published run-7 finals span **15.85 to 23.70 dB, median 18.29** —
  five sit under 18 and shipped with no remark. So "18+" is a target, and a
  verdict of VIOLATION requires the candidate to fall **below the approved
  corpus**, not merely below 18. Measure the corpus with the identical instrument
  before filing an audio finding; a metric that condemns shipped work is wrong
  about the metric. A batch landing at the bottom of the band is Miguel's call.

## Build gates (added 2026-08-09; Gemini QC unchanged as the final gate)

The inspection chain is now three gates. Gate 1 and Gate 2 are free (no API spend)
and run BEFORE Gemini; they exist to catch violations in seconds/for-free that
previously cost a render + Gemini round to discover. Gemini QC v3 stays exactly
as-is: the last word before a short ships.

**Gate 1 — geometry audit (pre-render, deterministic).** `pipeline/geometry_audit.py
<project_dir>` drives the real GSAP timeline in headless Chromium, samples every
0.5s, measures live bounding boxes, and enforces the geometry laws: clipped
elements, collisions (composition-aware: containment/concentric = OK; rings,
thin connector bars, letter-spacing box kisses exempt), same-class grid equality
+ alignment, frame margins, seam proximity, floating connector ends, centered-text
centering, ghosts (an atom that never reaches 1px size across the whole
timeline — e.g. a span authored right-to-left rendering at negative width — is
always an error), and glyph centring as an ERROR on both solo-glyph plates and
composed cards (near-miss rule: within 15% of an axis but off by >2px =
intended-centred-plus-bug; deliberate far-off-axis placements never judged).
Violations get annotated screenshots in `<project>/geometry_audit/`.
Exit 1 = errors = fix the generator BEFORE rendering. Warnings never block.
- Generators can opt out per element where a law legitimately does not apply:
  `data-overlap-ok` (intentional overlap), `data-bleed` (intentional edge bleed).
- WHITEBOARD lane: annotations (rings, highlight strokes, arrows drawn OVER
  content) and the outro-chip-over-dimmed-canvas overlay are the lane's
  aesthetic — those elements MUST carry `data-overlap-ok` or the audit flags
  them. Rotated strokes (X-strikes) and the taller-than-zone panning canvas are
  auto-exempted.
- Pilot baseline (2026-08-09): 33/40 run-3 projects audit 0-error; the 15 flags
  in the other 7 are mostly undeclared whiteboard annotations + one real escape
  (grokbuild whiteboard: cost-axis line strikes through the GROK BUILD label).
- GSAP gotcha the audit handles: it primes the timeline (progress 1 → 0) before
  sweeping, else fromTo immediateRender paints later tweens' from-values on
  elements whose entrance never ran (phantom visibles a forward render never shows).

**Gate 2 — native frame review (post-render, free, TOKEN-BURNER default).**
`pipeline/frame_review.py <mp4> --video-id <id>` — uncapped by Miguel's order
(2026-08-10): fixed 3fps sampling of the visual zone (top 50%, includes the
caption chip), 16x16-gray dedup collapses stillness, so EVERY distinct visual
state survives (~40-55 frames on a 50-70s short, ~330 tokens each). Scene
detection was dropped: it misses low-contrast cream-on-cream events; fixed-fps +
dedup cannot. Two things Brad's skill doesn't have, both in `manifest.md`:
- **Transcript fusion**: `--video-id` loads the Scribe word timings and prints
  the exact words spoken at each kept frame — claim-sync, highlight-match,
  key-term timing, and caption-echo checks read straight off the manifest.
- **Stillness map**: kept-frame gaps >=3s = confirmed stillness; any >6s run
  where dedup dropped nothing = IDLE-MOTION CANDIDATE, printed up top —
  corroborate with idle_motion_scan.py before reworking.
The building agent Reads the manifest + every frame and checks the static laws
before spending a Gemini call. Frames are intermediates: delete after review.

**Gate 2b — SIGNAL PARITY (post-render, free, added 2026-09-01).** Every gate above
this line measures where things ARE. Two defects Miguel caught in the 13 cutout
remakes were about what things are MADE OF, and all three gates passed both
defective builds. So the chain gains two measurements of the finished mp4 against
ITS OWN SOURCES — no reference to any other short, so the gate is portable:

- **FACE HF.** `formats/cutout/lib/cutout_facehf.py` — the std of a sigma-2.0
  high-pass over a crop **0.55x face height** (`K_SKIN`), centred on the nose, at
  native resolution. The finished short must sit within **12 %** of the plate it
  was cut from. Catches a face that was re-encoded, upscaled or otherwise put
  through a generation nobody priced: the defective `deepresearch` remake read
  5.65 against a 6.98 plate, 19 % of the face's detail smeared away.
  **The crop size is the whole instrument** — at 1.6x the crop is wider than his
  head and reads the cream die-cut edge instead of his skin (identical pixels:
  1.00x at k<=0.7, 1.39x at k=0.8). Quote k=0.55 for face noise, always.
- **TREBLE.** `formats/cutout/lib/cutout_media.py` — the 8-16 kHz band power
  relative to full band must sit within **6 dB** of the voice master's. Catches a
  mix built from the 16 kHz mono ANALYSIS wav, whose Nyquist ceiling is 8 kHz:
  ten of the thirteen remakes failed this by 18 dB. The build must RECORD which
  audio file it mixed (`_geom_*.json` -> `voice.source`) or the gate fails on the
  missing record alone.

Both run inside the cutout post-render check (`cutout6_check.py` checks 21 and
22). Any format that composites a face crop or mixes a voice owes the same two
numbers.

**Gate 3 — Gemini QC v3 (unchanged).** `shorts_run3/qc_v3.py` two-layer gate +
`idle_motion_scan.py` adjudication, per the section below. Final authority.

## QC v3 additions (each was a run-2 escape Miguel caught)
- idle-motion detector (inverse of run-2's static rule): flag continuous drift/zoom/pan on held elements
- double-caption detector (any top-zone text repeating seam captions / spoken words verbatim)
- divider/bar collision check in comparisons (moving elements never overlap content)
- highlight-semantics check: highlighted region must match the concurrently spoken concept
- arrow-termination + same-size-card + centering/spacing geometry pass
- tweet-metrics presence = automatic fail; tweet screen-time >4s = fail unless it is the news
- stutter words in captions = fail
- phone-legibility: minimum effective text size inside embedded assets

---

# FORMATS (integrated 2026-09-01)

The format lab is closed. Miguel approved all seven definitive videos on
2026-09-01 and the six surviving formats become first-class citizens of the
factory here. Origin for everything below: `format_lab/REVIEW_2026-08-30.md`
(six review rounds of verdicts) and the per-format `format_lab/<name>/NOTES.md`.
The chassis lives in `formats/<name>/`; that directory is authoritative for
constants and code, this section is authoritative for the rules.

## The format axis

A **FORMAT is the frame architecture** — where Miguel is, when, and what owns
the frame while he is not in it. A **LANE is the visual language** — Icon
Choreography, Kinetic Type, Counter & Meter, Diagram Build, Steps & Checklist.
They are ORTHOGONAL: a takeover can be built in the Icon lane, an artifact spine
carries Counter & Meter inside its document, a cutout world can be a Diagram
Build. Every LAW in this file applies to every format; the lane menu (top of
this document) is unchanged and still governs what the visuals look like.

**Format is assigned PER RECORDING AT INTAKE, from the transcript's shape** —
the same slot in the pipeline where the lane is chosen, and before any planning:

| the transcript is… | format |
|---|---|
| argument-first — a claim, then its support, visuals illustrating a line of reasoning | **classic split 50/50** (the existing factory) |
| persona/reaction-first — his read on a thing is the payload, the visual answers him | **facesplit** (he stays present) or **takeover** (the visual seizes the frame) |
| "look at this" evidence — a document, a panel, a settings screen, a registry, a page IS the subject | **artifact spine** |
| single-concept build — one idea assembled once, no scene changes | **whiteboard** |
| commentary-over-world — he narrates from inside the thing he is describing | **cutout** |

Between facesplit and takeover: facesplit when the visual and the face are both
live simultaneously for long stretches (comparisons, reactions to a UI);
takeover when the visuals want the WHOLE frame and the face is the frame
between them.

The seven definitive videos: `facesplit_fix6`, `takeover_fix6`,
`artifactspine_fix6` + `artifactspine_zoom_fix6`, `whiteboard_fix6` +
`whiteboard_zoom_fix6`, and the cutout chain `cutout_fix3c` → `_fix5` → `_fix6`.
**`pureface` is DEAD** (Miguel, round 2: *"I hate it. Throw this format to the
trash."*). It is not a format, it is not a variant, and it is not to be revived
under another name.

---

## 1. CLASSIC SPLIT 50/50 — the existing factory

The published format, 32 shorts and counting: the visual zone owns the top half,
Miguel's face the bottom half, the terracotta caption pill sits ON the seam at
y=960 and never moves. Everything in this document before this section was
written for it and still governs it. Its caption seat is what the caption canon
(Law 31) was reverse-engineered FROM, and it already complies with the caption
safe band (Law 30) at pill centre ~44%.

- **Variants:** none. It is one architecture; variety comes from the lane.
- **Chassis:** `formats/split/` — `pipeline/build_hyperframes_r2.py` remains the
  generator path, and the `.scappill` rule in it is the canonical pill's source
  of truth.
- **Format laws:** the seam is sacred (Law 4 + the 2026-08-10 audit-ERROR
  promotion); no top captions ever; the top zone is a whiteboard for visuals, not
  a header. **The lab audited this chassis and found the square-ended-fill defect
  living in it too** — Law 23 applies to the published factory retroactively.

## 2. FACESPLIT — dynamic 50/50 ↔ full-face

The split is not a commitment, it is a **switch**. The frame alternates between
the classic 50/50 and full-bleed face whenever what is relevant changes — twelve
switches in the definitive 54s cut — so the face gets the reaction beats at full
size and the visual gets the frame back the moment it has something to say.
Miguel, round 2: *"really fantastic work"*; round 4, on a build that had
re-proportioned the zones to solve a caption problem: *"no longer 50/50… not
good for us."*

- **Variants:** none surviving; the mode switch IS the variant axis.
- **Chassis:** `formats/facesplit/`.
- **Format laws:**
  - **THE SEAM IS EXACTLY 960, AND IT IS ASSERTED, NOT INTENDED.** 50/50 is the
    format. The generator asserts seam == 960 with zero spread across zone and
    band and refuses to build otherwise. Re-proportioning the zones to solve a
    caption, a margin or any other local problem is the WRONG TRADE — solve it
    inside the half you own.
  - **TWO SEATS, ONE PER MODE, SWAPPED AS A HARD CUT.** Split mode seats the pill
    on the seam (centre 960, 50.02% of frame height); face mode seats it on the
    chest (centre 1322.70, bottom 1380 = 71.88%, inside Law 30). The chunker
    forces a phrase break at every switch and blacks captions across the two
    animated moves, so no pill is ever alive while its seat changes. Both seats
    hold to 0.3px across the video. This is the ONE sanctioned exception to
    "caption position is stable" (Law 30) — two fixed seats, cut between, never a
    drift or a slide.
  - **THE PILL NEVER TOUCHES HIS FACE.** Split mode: pill bottom 334-416px above
    his brow on 129/129 probes. Face mode: 4-10px below the visible bottom of his
    lower lip at the video's two worst open-mouth poses, verified on a pixel
    ruler — because the face mesh is not reliable on this subject (landmark 152
    lands 62px into his neck, landmark 17 crosses his beard).
  - **TRIM EVERY CLIP BY HALF A FRAME.** `data-start + data-duration` is a float
    sum; a clip ending exactly ON a switch frame survives one frame into the next
    mode and lands the seam pill across his chin. Factory-wide, not facesplit-only:
    any format whose captions change on a switch frame has this exposure.

## 3. TAKEOVER — 21/79, growing cutaways

The frame belongs to exactly ONE thing at a time — Miguel full-bleed, or a
full-bleed visual — and **a split never exists**. When a visual earns it, it
seizes the entire frame for a beat while the voice carries, then hands it back.
The definitive cut runs **20.7% face / 79.3% illustration** (derived under the
guards, not chosen: the term card's approved 13.20 seat plus a ~2s return is
20.7%, and 25.0% is only reachable by deleting an approved scene). The hook is
his face; one short face return lands before the final line.

- **Variants:** the three lab cut maps (SPARSE / DENSE / GROWING) collapsed into
  one: **GROWING** is the format. Beat lengths escalate — 1.64 → 2.42 → 3.94 →
  5.94 → 8.66s — the first a flash you barely register, the last owning the video.
- **Chassis:** `formats/takeover/`.
- **Format laws:**
  - **THE FACE IS RAW 0%, ZERO PUNCHES.** Full-bleed `face_zoom00`, no punch-ins,
    no crops. Round 2 rejected the scale-animated "expansion" outright; round 3
    dropped punches entirely pending the new lens. Size changes are MODE
    SWITCHES (cut to a different plate), never deeper crops.
  - **ALREADY MOVING ON ARRIVAL.** Every takeover's interior tweens start
    `LEAD = 0.18s` BEFORE the clip is on screen, so its first visible frame is
    mid-gesture. Cutting to a static pose reads as a slide and instantly kills
    the device. (Law 20's spirit applied to every cutaway, not only the hook.)
  - **CUTS LAND ON WORDS.** Every entrance and exit sits on a Scribe word
    boundary, enforced at build time — the build fails on a non-boundary edge.
    No dissolves anywhere.
  - **THE BAND IS FIXED AND SACRED.** With no seam, the pill at its single seat
    (centre 1318, bottom 71.63%) is the only element surviving every cut; it is
    what makes the alternation legible instead of jarring. Nothing enters within
    112px of it, including elements in flight.
  - **SFX ARE THE GRAMMAR.** Entrance and exit take DIFFERENT sounds (seize vs
    release). A takeover without its signature reads as a rendering error.
  - **NO FACE RUN OVER ~7s** (longest in the definitive cut: 6.20s), and
    **THE PEAK NEEDS ≥6s** — a bespoke Law-13 object cannot be read in 3s of
    full-frame time.
  - **TAKEOVER SWITCH LAW (Miguel, 2026-09-01).** Round 3's watch item became a
    rejection on the first daily takeover: *"the switches of the face are
    happening way too often, they should happen at transition moments ideally,
    right now you are cutting key visualizations."* Now law, in three clauses:
    - **Switches only at beat transitions.** A face segment covers a claim or an
      aside where NOTHING is being drawn. A scene segment runs uninterrupted
      from a visualization's first build to its hold. The switch sits on the
      seam between two argument beats, never inside one.
    - **A visualization is never cut before it lands and holds.** A departure
      (scene → face) may not land inside a build window nor within
      `HOLD_MIN = 0.30s` of one finishing. Arrivals stay exempt — ALREADY MOVING
      ON ARRIVAL requires a mid-gesture first frame — but only up to
      `LEAD = 0.18s`; more than that and the face is covering a build the viewer
      never sees. Hiding an EXIT is legal; hiding a BUILD is not.
    - **Switch rate is bounded by the DEFINITIVE reference.**
      `takeover - DEFINITIVE.mp4` switches **7 times in 54.04s = 7.77/min**;
      the ceiling is **10.10/min** (7.77 x 1.30, so a 30s cut gets 5 switches).
      The rejected cut ran 13.99/min.

    **The check is deterministic, not a review note:**
    `formats/takeover/lib/takeover_switch_law.py <project>/index.html
    --duration <DUR> [--quiet-windows]`. It re-parses the emitted page —
    clips + every `tl.*` call — classifies each tween BUILD/EXIT/MOVE, derives
    face and scene windows and exits 1 with a named defect (`D` departure,
    `H` hidden build, `R` rate). `--quiet-windows` prints the legal switch
    moments so a cut map is PLACED, not guessed. It fires 10 build defects plus
    the rate ceiling on the rejected render and is silent on the DEFINITIVE. Lane generators call
    it from `build_takeover()` and refuse to write a page that breaks it.

    **It matters twice as much in a lane build.** The chassis lays scene clips
    over one continuous face plate, so a face window hides nothing. The lane
    builds invert that — ONE continuous scene timeline with face clips on top,
    which is what makes ARRIVE IN MOTION free — and there a face window ERASES
    whatever is drawing underneath it. That is how v1 lost the SPACES→PROJECTS
    arrow, the sheet swap, and the entire third arm of a three-arm diagram.
  - **WATCH ITEM (Morgane, round 3):** possibly too many angle changes. Round 4's
    rebalance answered it by extending scenes rather than adding cuts. Re-judge
    per video; do not overcorrect into stillness — the SWITCH LAW above is the
    measured version of this item.

## 4. ARTIFACT SPINE — one document is the whole video

A single mock artifact — a settings panel, a registry, a tool config, a document
with real chrome and real marks — is the only subject. The spine advances
through it and annotations land on the line being spoken. Miguel's face appears
only in the hook and the sign-off, and it occupies **exactly the same window
rect as the document**, so the frame never changes shape: the window's content
changes, not the composition. Miguel: *"Super NICE representation."*

- **Variants (both definitive, both approved):**
  - **SCROLL** — one continuous top-to-bottom journey through the document, six
    discrete word-synced moves, each ≤0.9s and each followed by a hold. Face
    switch-ins at two connective lines ("extra nice").
  - **PAGE-ZOOM** — the sections become cards on one large board and the camera
    moves between them, with motivated wides at the chapter seams.
- **Chassis:** `formats/artifactspine/`.
- **Format laws:**
  - **TOP CAPTION SEAT.** Alone among the formats, the pill sits in the UPPER
    zone (centre y=288, band 12.02-17.98%, fully below the top-10% line) —
    because a scroll shows already-CONSUMED content at the top of the frame, so
    that is the one place a pill cannot hide anything the viewer still needs.
  - **FULL-SIZE DOCUMENT.** The document fills the frame width minus the normal
    40px margins — window 1000×1416, doc 936px, transform scale asserted at
    exactly 1.000000. The round-3 viewport shrink is dead; it cost 21.5 points of
    frame area to white space. The generator refuses to build at any other scale.
  - **UNIFORM CARDS.** In the zoom variant every card is the same width (920px)
    with 40px of air each side, and no card touches a frame edge. A card wider
    than its siblings is a violation (round 2: the Hermes Agent card).
  - **ONE WINDOW.** The face and the artifact share one rect for the whole piece.
    A face-led format may change what is in the window; it may not change the
    window. Corollary: when the artifact is not confined to that rect, it is
    switched OFF with the face, or its chrome leaks around the face card.
  - **ADVANCE, THEN HOLD.** The spine never moves continuously. Every move is
    discrete, word-synced, ≤0.9s, then holds. Annotations land only on a held
    surface (Law 5 restated for a moving spine).
  - **CHROME PAINTED, CONTENT ON ARRIVAL** and **ONE PERSISTENT INSTRUMENT** —
    the artifact carries exactly one always-visible state device (the context
    meter), withheld until the beat that fills it, changed only on events, and
    the video's last annotation lands on it.
  - **THE ARTIFACT IS INTERNALLY CONSISTENT.** Every number, count and label on
    the document agrees with every other one; they are all on the same surface.
  - **PACE TO COMPREHENSION.** Round 1's remark: the animation sometimes goes too
    fast for the viewer to take everything in. Word timings are the floor, not
    the schedule.

## 5. WHITEBOARD — one drawing, gaining ink

The visual zone is ONE board for the whole video. No scenes, no swaps, no
transitions: every shape draws itself on with a marker stroke at the moment its
words are spoken, and nothing ever leaves. At the end the whole argument is one
readable diagram. Miguel, round 2: *"amazing!"* — this is the format the
2026-08-09 bonus lane was reaching for and missing.

- **Variants (both definitive, both approved):**
  - **PLAN VIEW** — the camera never moves; the whole board is on screen from the
    first stroke and fills with ink.
  - **CALM ZOOM LANE** — the camera follows the pen at working distance and pulls
    wide at chapter seams.
- **Chassis:** `formats/whiteboard/`.
- **Format laws:**
  - **THE BOARD IS BOILED DOWN.** Morgane, round 3: the diagram was too complex
    for a phone. Drawn elements went **59 → 39**, board text to four blocks, one
    technical name. **One idea per glyph** — two glyph groups saying the same
    thing means one of them goes. Every symbol must be self-evident to a normal
    viewer (the bowtie valve nobody could read became a BOOM GATE: an arm that
    lifts, which needs no teaching). Card captions sit INSIDE their card, low —
    a caption above a card puts the marker's body in the phone's top UI every
    time it writes it.
  - **THE PEN LEADS ITS STROKES.** The marker tip is AT the ink it is drawing,
    at the moment it is drawn, for every stroke including the first one (round 2's
    only bug: the pencil parked away from the Hermes box while the box drew).
    The pen is not a decoration that follows; it is the cause of the ink.
  - **WIDE ONLY AT CHAPTER SEAMS.** *A stop lasts until the narration moves to a
    different ELEMENT* — not until the drawing changes, not until a sentence
    ends. Round 4 calmed 15 stops / 14 moves to **8 stops / 7 moves, median hold
    6.60s**, and pulls wide at exactly the three approved chapter seams plus the
    final reveal. When the camera is already wide at a seam, the seam is honoured
    by STAYING — a wide-to-wide move is a move with no reason (Law 25). Every
    stop's centre IS its subject's centre, 8/8.
  - **RESERVED CLEARANCE BAND.** No drawn element enters the band above the
    caption seat (rows 799.20 → 862.5), and the band exempts nothing — a
    connector or a small mark under a pill is exactly as hidden as a card. Ink
    may cross the band only during a camera transit, never during a hold.
  - **PEN SFX ARE `loop` CLASS.** The marker squeak at shipped volume was a hard
    NO; it was root-caused and re-synthesised, not turned down (Law 22).
  - **THE LABEL LAW — every drawn object gets its word written beside it**
    (added 2026-09-02 after the run-9 Viewer Test held
    `perplexityprojects_whiteboard` at 11 SENSE / 13 NO-SENSE, the worst score
    recorded). *A whiteboard that draws without writing is using half the
    format.* Full statement and the measured evidence in
    `formats/whiteboard/CHASSIS.md` → **THE LABEL LAW**; enforced at build time
    by `assert_label_law` / `assert_outro_clear` in the shared harness
    `formats/whiteboard/lib/whiteboard_build.py` (every daily whiteboard builds
    through it; `shorts_run9/gen/whiteboard_build.py` is a re-export shim).
    - Every drawn object gets its **key word handwritten beside it at the beat
      that word is spoken** — label and object are ONE BLOCK, within 1.0 s.
      v1 drew a globe, a stack and a laptop and wrote none of ONLINE / DEEP /
      LOCAL; the sibling split render drew the same three and printed all three,
      and passed the beats the whiteboard failed.
    - **A comparison the script SPEAKS must be DRAWN as a comparison** — both
      terms on the board, in different shapes, with a connector. v1 never drew
      SPACES at all, so "the evolution of Perplexity Spaces" had no picture.
    - **The key term (Law 9) is written FIRST, alone, LARGE** — at least 22
      design units, and no other type reaches the board before it. v1 never wrote
      RESEARCH DESK, the video's central metaphor, anywhere.
    - **The outro never overprints the diagram.** The board EXITS — a wipe, which
      is a whiteboard's own erase — and the handle card starts only once the wipe
      has finished. A 0.94-opacity scrim is a veil, not an erase, and it cost the
      last 3.4 s of the short to a double exposure.
    - **A bespoke glyph passes the Phone Test cold, unlabelled, before its label
      is allowed to rescue it.** Three overlapping outlined squares are "stacked
      squares", not "deep research"; the replacement is a document with visible
      ruled page lines under a magnifier.
    - **An erase is a legal move again**, narrowly: to free a column, to retire a
      superseded key, and to leave the frame before the outro. It is authored as
      an opacity swap on the element's own id and it is never a default.

## 6. CUTOUT — commentary over a full-bleed world

Miguel's background-removed silhouette stands IN FRONT of a full-bleed
1080×1920 explainer world — no seam, no split, no face slot. The world is behind
him and it is the whole frame; tool tiles pass behind his shoulder and re-emerge
on the other side. Miguel, round 4: *"Looks amazing, bravo! I think we cracked
it… this is the standard!"* The format is DONE and is the reference build for
the back-catalogue ports (`format_lab/cutout_ports/`: airtable, buzzteams,
mcpupgrade, selfoptimize, vendorlock).

- **Variants:** one definitive architecture — anchored bust plus depth field.
  The IMMERSED depth treatment was absorbed into it; the INTERACTIVE dock-solving
  variant and Morgane's real-screen-recording-behind-him idea are logged as
  future variants, not shipping ones.
- **Chassis:** `formats/cutout/`.
- **Format laws:**
  - **THE MATTE IS SAM2, TRACKED, WITH A CREAM DIE-CUT RIM.** Not per-frame
    segmentation. Ships `_shared/matte_sam2_rim_v4.webm` — VP9 + alpha,
    1080×900, 25fps, 1354 frames, feather 0.6, **7px cream `#FFFDF9` rim** baked
    in offline. The rim is confirmed canon (round 2). Rimless twin
    `matte_sam2_v4.webm` exists for compositing experiments only.
  - **FRAME-0 WARM-UP (STANDING RULE, Miguel, 2026-08-31).** A frame-0 point
    prompt may never be a frame that ships. SAM2 re-segments a prompted frame
    from its prompt while every other frame is a memory-conditioned propagation,
    so frame 0 arrives 2.4× rougher than its own neighbours — on the one frame
    that decides whether anyone watches. Build chunk 0 as
    `[f0] + [f15…f1] + [f0, f1, f2…]`, prompt local index 0, **emit from local
    index 16**: the prompt lands on a throwaway copy and the real frame 0 arrives
    as a propagation with a 16-frame memory bank behind it. Pair it with a
    **MIRRORED** temporal-median pad (`[f1, f0, f1]`, not `[f0, f0, f1]`) — with
    replication, frame 0 was the only frame in the video the smoother never
    touched. Measured: frame-0 edge roughness 1.09/0.87px → 0.58/0.62px.
  - **NEVER OCCLUDE HIM.** No foreground element crosses his silhouette.
    Captions sit over the TORSO only and clear the head band. Every scene atom is
    either provably clear of the measured matte envelope on every frame, or
    explicitly declared `behind` — safe areas are DERIVED from the envelope,
    never typed. Chair, headrest and set furniture are excluded by a spatial
    region, not by hoping the model handles it.
  - **REAL LOGOS IN THE DEPTH FIELD.** The parallax lanes are the format's best
    moment (three lanes at 78/116/168px, opacity 0.34/0.66/1.0, stepping
    46/112/208px on one spoken beat) — and every tile in them carries a REAL
    provider mark, repeated if necessary. Gray placeholders and generic glyphs
    are banned twice over (Laws 29 and 33); a field of anonymous tiles reads as
    unfinished slots, not as unnamed tools.
  - **SHOULDERS VISIBLE, PLATE SCALE 1.10.** He is scaled about the plate's
    BOTTOM CENTRE (fixed point y=1920, so the base is welded to the frame edge
    and full-bleed survives) — head 28.7% of frame height. **1.1011 is the hard
    ceiling**: past it a whole tile stops fitting in the near lane's gutter and
    the depth cue reads as a sliver. Anything bigger requires re-authoring the
    lane, not moving a constant.
  - **NO FILTER STACKS ON THE CUTOUT.** Rims, glows and outlines are baked into
    the matte offline. One `drop-shadow` is the ceiling.
  - **CREAM ONLY WHILE THE SUBJECT IS DARK**, and **RECORD FOR THE FORMAT** — a
    half-body frame with headroom and nothing dark directly behind the shoulders.
    This is a set rule, not a build rule.

---

## THE MATTE — STANDING DECISION (Miguel, 2026-08-31)

Full derivation, measurements and alternatives: `format_lab/_shared/SAM2.md`
(companion: `_shared/MATTE.md` for the single-image bake-off).

**Production matte path: Modal A10G · fp32 · `sam2.1_hiera_base_plus` · chunk 350
/ overlap 8 · v3 post stack + cream rim. ~7 min and ~$0.17 per 54s video.**

- **MPS is dead** — 1.28× vs CPU and the machine is unusable while it runs
  (measured, killed at 44%). Matte work does not run locally.
- **`hiera_large` not adopted** — $0.24, 1.44× slower, statistically a wash on
  the deciding flicker instrument. Miguel, on the A/B: *"I don't really see a +
  to using the large one."*
- **bf16 is 3× faster ($0.058/video) but a measurably different contour** —
  reserved for a possible bulk back-catalogue job, and only after passing the
  full gate chain plus Miguel's eyes.

## OUTRO HANDLE — one parameter, two masters (Miguel, 2026-09-01)

The outro chip handle is a **parametrized constant**, not a hardcoded string.
One build, two deterministic renders, and the ONLY difference between them is
the outro:

| master | chip |
|---|---|
| YouTube | `@migueltorrezai` |
| TikTok / Instagram | `@migueltorrez.ai` |

Amends Law 10 (unique themed outros + handle chip): the chip's THEME is still
per-video, its HANDLE is per-platform. Re-rendering the variant must change
nothing else in the file — hold it to the containment standard (Law 31's
instrument): every differing pixel inside the chip's own rows.

---

## THE LAWS, CONTINUED — 21 to 36 (the format lab's global laws)

Sixteen new laws plus one amendment, distilled from six review rounds
(`format_lab/REVIEW_2026-08-30.md`, global laws 1-17 there). They apply to ALL
formats **including the published classic split**, and several of them describe
defects the lab found living in the existing chassis. Where a lab law sharpens
an existing law rather than adding one, the dedupe is stated inline.

21. **THE 0% ZOOM STANDARD** *(lab laws 1 + 7)*. Miguel, round 1: *"you zoom in
    way too much on my face… my entire torso and such can also be in the
    video."* The 0% window is the widest full-bleed 9:16 crop the 4K master can
    give — `crop=1216:2160:1270:0` → `scale=1080:1920`, head at 56.3% of frame
    height — and it is a solved constraint, not a preference (a 9:16 window cut
    from a 2160-tall master can be at most 1215px wide). Every zoom level is a
    percentage TIGHTER than it. **Default punch 5%, hard ceiling 10%.** Do not
    build 15% or 20%: they re-enter the head-66-72% band Miguel already rejected,
    and 20% clips his head on 3 of 64 sampled frames. **Punch-ins are HARD CROP
    CUTS** — a different crop window cut to on a single frame, from the 4K master,
    static for the whole hold — never a `scale`/`transform` animation of the
    footage, never a tween between windows, never a window that follows his face.
    Return is also a cut. Minimum hold after a punch 0.4s. Ladder, per-level
    re-centring bands and the generalisation to future recordings:
    `format_lab/_shared/ZOOM_STANDARD.md` + `zoom_standard.json`.
    *Extends Law 1 (no idle motion) to the camera itself.*

22. **SFX LAW v2** *(lab law 2)*. The lab's effects were unpleasant in character,
    too loud, and sometimes out of sync. All three are now specified.
    **Soft/tactile family only** — wood, cloth, paper — never sharp.
    **Every file normalised to one unity reference, −19.0 dBFS**, so a gain
    constant means the same thing for every sound. **Three level classes replace
    the single `SFX_VOLUME = 0.18`**: `structure` 0.120 (the cuts and seizes,
    one clear step under bed presence), `detail` 0.077 (ticks, pops, arrivals —
    they accumulate, so they read as texture, never as an announcement), `loop`
    0.038 (sustained bodies: the pen, the marker). **Every SFX is frame-locked to
    the visual event it scores.** Full palette, per-file measurements and the
    derivation: `format_lab/_shared/SFX.md`. Never judge an SFX by its gain
    constant alone — the delivered level is gain plus source loudness, same as
    the audio mix law.

23. **NO SQUARE-ENDED FILLS IN ROUNDED CONTAINERS; ROUNDED-BAR FILLS ARE ONE
    CONTINUOUS PILL** *(lab laws 3 + 11)*. Miguel: *"The straight bars at the end
    of rounded edge boxes is a big no no… UGLY AS FUCK… that's a big no even for
    the formats and variants that already exist."* Any fill, progress or
    highlight inside a rounded container is clipped to the container's radius and
    never terminates in a hard straight edge. A progress fill is ONE pill-shaped
    element with `min-width = track height` so it can never sliver, with no
    detached ticks or end markers; remaining progress is empty track and nothing
    else. **This is retroactive: audit the published chassis for it.**
    *Sharpens FILL THE SHAPE and METERS COMPLETE.*

24. **NO PEEK-AHEAD** *(lab law 4)*. Content that has not been spoken yet is not
    visible. The artifact spine's next section peeking at the bottom edge was the
    named case. Solve it as GEOMETRY (the region is not painted yet), not as a
    schedule that hopes the timing holds. A reveal AFTER the words is a reveal; a
    reveal before them is a spoiler.

25. **NO UNNECESSARY MOVES** *(lab law 5)*. A camera or scroll movement with no
    spoken reason does not happen. A move exists because the narration moved to a
    different OBJECT — not because the drawing changed, not because a sentence
    ended, not to add life. A wide-to-wide move is a move with no reason.
    *Extends Law 1 from element motion to camera motion; where Law 1 bans idle
    drift on a held element, Law 25 bans an unmotivated move of the frame itself.*

26. **FACE-LED FORMATS RENDER AT NATIVE 25 FPS** *(lab law 6)*. Root cause,
    measured: source face footage is 25fps conformed to 30 by duplicating 1 frame
    in 6 (**17% duplicates**). Invisible while the face is small — which is why
    the classic split never showed it — and a visible stutter at full-frame or
    zoomed scale. Face-led formats render 25fps native with the de-conform
    applied, until recordings are captured at 30 or 60. **Set rule: capture OBS
    at 30 or 60fps going forward.**

27. **EDGE FADE** *(lab law 8)*. Scope is narrow and confirmed: only for elements
    DELIBERATELY cut by the frame edge (a tile field that continues past the
    frame, a scrolling document's viewport edge). Those get a thin alpha fade
    instead of a hard clip line, because a hard slice reads as a rendering bug.
    Cards and UI never touch an edge at all — the margins rule is unchanged.
    *Sharpens Law 7's no-clipping clause: some clipping is intentional, and
    intentional clipping still has a required treatment.*

28. **LABEL + OBJECT = ONE BLOCK** *(lab law 9)*. A name moves with its object.
    Always, all formats, all videos. Named case: at ~33s in the cutout the "Nous
    Research" label stayed put while its Hermes card moved. If a label can be
    separated from its object by any animation, it is not attached — parent it.

29. **NO PLACEHOLDER TILES** *(lab law 10)*. Grid and tile fields always show
    real logos. **Repeat a mark rather than leave a gray blank.** A row of
    anonymous plates reads as unfinished slots, not as unnamed tools — the wall is
    only worth building if every plate is something the viewer could actually have
    connected.

30. **CAPTION SAFE BAND + PLATFORM UI SAFE ZONES** *(lab law 12, as amended in
    round 4)*. Measured against real S26 Ultra screenshots of TikTok, YouTube
    Shorts and IG Reels; binding constraint is TikTok's 75% line and the ~85%-width
    right rail.
    - The caption pill's BOTTOM edge sits at or above **72% of frame height**
      (y ≤ 1382 of 1920). Preferred centre band 40-65%.
    - **Caption position is STABLE across a video's modes** (Morgane: no drastic
      jumps). Facesplit's two fixed seats swapped as a hard cut are the sanctioned
      exception; a drifting or sliding seat is not.
    - No meaningful content in the bottom 28%, the right 15% column (x > 918)
      between y 30-95%, or the top 10%. The outro handle chip is exempt.
    - **AMENDMENT (Miguel, round 4 — this is the half that gets forgotten):** the
      right-rail clearance applies to CAPTIONS and critical readable annotations
      ONLY. **The COMPOSITION stays centred and symmetric.** Applying the rail
      clearance to the whole frame shoved the artifact spines to x=40 with 168px
      of dead space on the right — *"why are they not centered? they look so bad
      like this."* Content may sit under the translucent platform icons, exactly
      as every major channel's shorts do.
    - The published classic split already complies (pill centre ~44%).
    *This amends Law 4: captions live at ONE seat per video. In the split format
    that seat is the seam; a format without a seam still gets exactly one seat,
    and "no top captions ever" yields to the artifact spine's top seat, where the
    pill covers only already-consumed content.*

31. **ONE FONT SIZE, AND THE PILL IS COPIED, NOT DESIGNED** *(rounds 5-6)*. The
    caption specification is lifted verbatim from the published factory
    (`shorts_run8/projects/mcpupgrade_icon/index.html`, the rule behind 486 of
    507 published pills — 95.9%):

    ```css
    .scap     { left:0; width:1080px; text-align:center; }
    .scappill { display:inline-block; transform:translateY(-50%);
                background:#C4573A; color:#fff; font-family:Nunito,sans-serif;
                font-weight:800; padding:18.8px 33.8px; border-radius:22.5px;
                white-space:nowrap; }
    /* font-size:56.2px — ONE size, every pill, every video */
    ```

    In the 576-wide design space those are round numbers: 56.2 = px(30),
    33.8 = px(18), 18.8 = px(10), 22.5 = px(12) at S = 1.875. There is no
    `line-height` in the published rule, so Nunito's own `normal` (1.364em)
    applies and **the pill is 114.59px tall, constant for every phrase**. Every
    format reports that number, so cross-format uniformity is audited by one
    figure instead of by eye. `translateY(-50%)` means **the seat is the pill's
    CENTRE**, not its top — every bottom-of-pill number derives from that.
    - **THE SHRINK FORMULA IS DEAD.** `cap_font()`'s length-based sizing shipped
      five to eight distinct sizes per video. A phrase too wide for its seat is
      **SPLIT at a word boundary**, never shrunk and never squeezed. Take the
      fewest beats that all fit, and among those the partition whose widest beat
      is narrowest, so a split never strands an orphan. Each beat starts on the
      real `start` of its first word, so the track stays gapless.
    - **MEASURE THE WIDTH IN THE ENGINE THAT WILL RENDER IT.** The `0.575 * len`
      advance estimate is wrong by tens of pixels (it runs 0.71-1.00 of the truth,
      mean 0.86) and fails in the direction that forces splits a phrase did not
      need. Lay the real `.scappill` box out in headless Chromium with the real
      Nunito 800 webfont, **prove the font loaded** (`document.fonts.check()` — an
      empty pill never triggers the download and the whole corpus silently
      measures as Helvetica), and cache. Measure at integer page positions in
      small batches: past ~250,000px down a page Chromium returns three different
      heights for one box.
    - **Width budget:** the pill is symmetric about x=540 and the rail owns
      x > 918, so no pill exceeds `2 × (918 − 540) = 756px`. The published corpus
      does not honour this (widest 861.9px) because Law 30 postdates it; the
      definitive formats all do.
    - **A caption instrument needs a NEGATIVE CONTROL** — run it on the previous
      round's file, and if it cannot see that round's defect it is not evidence.
    - **Containment is not "nothing changed outside the region"; it is "nothing
      outside the region is CLUSTERED."** Two independent H.264 encodes of
      identical content already differ across ~22% of the frame — re-rendering an
      unchanged project is the control that proves it. Report the densest tile,
      not the bounding box, or diff a lossless pair.

32. **TILE CORNER CONSISTENCY** *(lab law 13)*. Every mark presented on a tile
    gets the same rounded-corner treatment. No pointed-corner odd-one-out (the
    Buzz logo in the buzzteams port). *Sharpens FILL THE SHAPE: consistency
    across siblings, not just fit within a parent.*

33. **NO GENERIC ICONS, EVER** *(lab law 14 — Law 29 hardened)*. Background and
    depth fields carry REAL provider logos — the AI tools we actually use and
    discuss — never generic placeholder glyphs. A generic glyph is a placeholder
    tile that has been dressed up. *Extends Law 2 (logos are a must) from named
    subjects to background furniture.*

34. **CHARTS: STANDARD FLAT-TOP BARS** *(lab law 15)*. Vertical bar charts use
    flat-top bars. No rounded or pill-topped bars, and **never a line traced
    across the bar tops** (selfoptimize ~27s: rounded rising bars plus a
    connecting line — *"ugly"*). RSI-style treatments remain fine.

35. **PRODUCT MARK OVER COMPANY MARK** *(lab law 16)*. When a specific product is
    discussed, use ITS logo, never the parent company's as a fallback — Claude
    Cowork gets the Cowork mark, not the Anthropic or Claude mark. Fetch and
    register missing product marks before building (per the standing
    add-missing-logos rule). *Extends Law 2 and Law 12 (colour marks).*

36. **MARK CONTAINMENT = QC CHECK** *(lab law 17)*. A logo stays inside its box.
    OpenCode escaping its tile at ~35s in the selfoptimize port is the named
    case. Visual containment is now an explicit item on every quality-check
    agent's list, not something noticed by eye. *Makes the 2026-08-16 interior-
    furniture ruling (sockets and ports live fully inside their card with visible
    margin) enforceable on marks too.*

### AMENDMENT TO LAW 20 — the hook is a Law-13 surface, in every format's own form

Law 20 stands unchanged in substance and is confirmed across all six formats: the
opening needs its own bespoke SUBJECT, not chassis furniture in a state. What the
lab adds is that **the subject is expressed in the format's grammar**, not as a
bolted-on prop:

- **classic split / facesplit** — the visual half opens on the video's idea as an
  object, exactly as Law 20 already requires.
- **takeover** — the hook is Miguel plus the format's OWN device: a sub-2s flash
  takeover, or a punch-in. The device is the subject. No gratuitous hook object.
- **artifact spine** — the artifact IS the subject, so the hook is the face plus
  the document's first region arriving; the persistent instrument is withheld
  until the beat that fills it (Law 20's vessel corollary, mechanised).
- **whiteboard** — the first stroke draws the video's central object, centred on
  the axis, alone (Law 19), and displaces to make room.
- **cutout** — Miguel plus the world building on his words. The world is the
  object; nothing is added in front of it.

The vessel corollary is unchanged and still necessary-but-not-sufficient: never
park an empty gauge, trough, plate or outline in the opening. And the 2026-08-19
finding stands — **stillness is not the defect and must never be gated.** Judge
what the opening frame CONTAINS.

### Cutout stage-zone ruling (Miguel, 2026-09-01)
The cutout IS a 50/50 at heart: his silhouette owns the bottom half (cap top
~44% of frame), the stage zone above is the visual surface — the boundary is
his outline (soft seam, crossings allowed) instead of a drawn seam. Therefore
**the classic LANES apply to the cutout's stage zone as-is** (icon, counter,
diagram, kinetic grammar all valid up top); the cutout adds only its own
devices: the depth band of real-logo tiles behind him, and behind-the-
silhouette crossings as payoff beats. A cutout counter video is a sibling of a
split counter video, not a different species. Freeform bespoke staging remains
allowed where a Law-13 idea demands it.

## DAILY TRIAL VERDICT — Miguel, 2026-09-01 (binding for EVERY video from here on)

Three rejections from the first `daily-shorts` run. Each is now a law with an
enforcing check; none is advisory.

1. **THE VIEWER TEST IS THE FIRST GATE, ON EVERY VIDEO.** "The visualization
   makes literally no sense. Were there even clerks in this loop?" A clerk that
   only measures instruments (fades, bands, ratios) is not a clerk. Every render
   is judged frame-by-frame as a first-time phone viewer: *What am I looking at?
   What is he saying? Does the picture argue the sentence?* Any NO-SENSE frame
   holds the video. Procedure: `pipeline/semantic_review.md`. Runs on ALL videos
   of a batch, never sampled.
2. **TAKEOVER SWITCH LAW (Miguel: *"the switches of the face are happening way
   too often, they should happen at transition moments ideally, right now you
   are cutting key visualizations"*).** Face<->scene switches happen ONLY at
   beat transitions. A visualization is never cut before it has landed and held
   (`HOLD_MIN = 0.30s`; arrivals keep `LEAD = 0.18s` of grace). Switch rate is
   bounded by the DEFINITIVE takeover: 7.77/min, ceiling 10.10/min.
   Check: `formats/takeover/lib/takeover_switch_law.py` — chassis law 11, full
   text in *3. TAKEOVER* above. Calibrated: 10 build defects plus the
   rate ceiling on the rejected `perplexityprojects_takeover` v1, silent on the
   DEFINITIVE. Lane
   generators call it inside `build_takeover()` and refuse to write on a
   defect.
3. **CUTOUT FOUNDATION LAW.** The approved cutout look is the grokpublish /
   hermesvoicemagic backfill family: that background, that lane spacing, that
   perspective, the pop-behind detail. Every cutout DERIVES from the chassis
   that encodes it; per-video freedom is the logo set and which logo pops when.
   Builders never write cutout backgrounds/lanes from scratch. Geometry is
   measured against the foundation constants in `lib/cutout6_check.py`.

Root cause shared by all three: builders rolled their own instead of deriving
from the approved chassis, and the sampled clerk measured pixels, not meaning.

---

## VISUAL QUALITY CHECKS (Miguel, 2026-09-02) — binding on every video

Two defects shipped through a chain that was green end to end.

* A **takeover where his face was not centred** in the full-face segments. Gate 1
  measures the authored DOM, Gate 2 is a self-read, Gate 3 is a rubric screener,
  the Viewer Test asks about meaning. Not one of them decodes the rendered pixels
  and asks *where the head actually is*.
* A **bespoke "moon" object, illegible and ugly at phone size**. Gate 3 never
  judges legibility at all, and the Viewer Test missed it because **the BUILDER
  ran the Viewer Test on its own work** and its own intent supplied the word
  "moon" for a shape nobody else could name.

Root cause of both: the factory had no instrument for *how it looks*, and its one
semantic gate was being self-administered. Five checks are now law. All five are
binding, all five run per video, and none of them has a warning tier unless it
says so.

### 1. THE PLATFORM MAPPING IS FIXED

| platform | format | handle |
|---|---|---|
| **YouTube** | classic **split**, builder picks the BEST lane for the transcript and justifies the pick | `@migueltorrezai` |
| **TikTok** | **cutout** (foundation depth field) | `@migueltorrez.ai` |
| **Instagram / Reels** | **WHITEBOARD**, always, every video | `@migueltorrez.ai` |

Miguel: *"we'll change if I see that it's not good."* Until he says otherwise,
Reels is whiteboard and there is no per-video format choice. The whiteboard is a
**bespoke build from the same beat plan** — it does not reuse the lane scene, it
reuses the argument. **TAKEOVER and FACESPLIT are no longer daily deliverables**;
they stay approved formats for lab work and for a video Miguel specifically asks
for. Staging dirs: `Daily/<date>/youtube/`, `/tiktok/`, `/reels/`.

### 2. SELF-REVIEW IS NOT A GATE — the independence rule

The Viewer Test is administered by a **fresh agent per video** that receives only
the **staged MP4s and the tight transcript**. It is forbidden from opening the
plan, the generator, the project HTML, the paperwork, or any builder return; if
it reads them the verdict is void. Builders no longer run the Viewer Test at all
and never report a Viewer Test verdict. They may of course look at their own
render and fix what they see — that is craft, not a gate.
Full text: `pipeline/semantic_review.md` -> THE INDEPENDENCE RULE.

### 3. THE PHONE TEST — object legibility at real size

For **every Law-13 bespoke object**: the frame is downscaled to **405x720**, the
object is cropped **alone with no context**, and a **fresh judge names it in three
words or fewer**. A different name, a hedge, an "I cannot tell", or an answer
needing more than three words is a **FAIL, and a fail is a REDESIGN**, not an
annotation. There is no "add a label to explain it" fix.
Builders PRODUCE the crops (they own the bounding boxes), clerks JUDGE them:
`pipeline/phone_crops.py <render> --out <run>/review --at "t:x0,y0,x1,y1:name"`.
Procedure: `pipeline/semantic_review.md` -> THE PHONE TEST.

### 4. FACE CENTRING — deterministic, ±4 % of frame width

In any **full-face segment** the detected face centre must sit within **4 % of the
frame width** of frame centre. Any sampled frame outside that band is a **FAIL**.
On the split's face band the same measurement runs at **warning level** (the split
plate is a fixed approved crop).

`pipeline/face_center_check.py <render.mp4> [--fmt takeover|facesplit --geom <_geom_<id>.json>] [--band]`
samples every 0.5 s, detects with MediaPipe BlazeFace (Haar fallback), validates
every hit (confidence >= 0.70 and >= 40 % skin-tone pixels, so a flat vector
graphic cannot be mistaken for a head), and exits 1 on a defect. Segments come
from `takeover.cut_map` / `facesplit.switches` when a geom is passed, otherwise
from a face-vs-scene layout detector on the frames themselves.

Calibration, 2026-09-02:

| render | worst dx | mean abs dx | verdict |
|---|---|---|---|
| rejected `impossibletask_takeover` (v1) | **-9.81 %** | 7.68 % | **FAIL** (13/13 face frames offend) |
| approved `perplexityprojects_takeover` v2 | -0.93 % | 0.56 % | PASS |
| reference `takeover - DEFINITIVE.mp4` | -2.87 % | 1.56 % | PASS |

The threshold sits in the middle of an empty gap, not on a boundary. It is a
guard in the builder brief and a law in the takeover and facesplit chassis.

### 5. GATE 3 DESCRIBES BEFORE IT JUDGES

`shorts_run3/qc_v3.py` now runs a **DESCRIBE pass first, by default**: Gemini
writes a one-line plain description of each sampled frame ("a sheet of paper
stamped IMPOSSIBLE TASK; the Codex logo below it") naming objects from the pixels,
plus the words spoken at that instant. Two mechanical findings fall out and both
are hard errors: `unidentifiable_object` (the description cannot name what an
object is) and `beat_mismatch` (the description does not match the transcript beat).
A rubric screener will answer "no violation" about a frame it never parsed; a
model that must first write what it saw has to look. `--no-describe` restores the
old two-pass behaviour; the output JSON is a superset, so existing readers are
unaffected.

### 6. THE CONTACT SHEET — mandatory build output

Every staged render ships a 12-frame 3x4 sheet at beat boundaries (+0.35 s),
<= 1800 px wide, at `<run>/review/sheet_<id>_<fmt>.png`, via
`pipeline/contact_sheet.py <render> --id <id> --fmt <fmt> --run <run> --geom <geom>`.
Three sheets per video. The daily run's final report lists every path. It is the
fastest possible read of a forty-second short, and it is the artefact that makes
an off-centre face or an unreadable object visible in one glance instead of one
playback.

### 7. A STILL FRAME CANNOT JUDGE A TRANSITION — flags are verified on the MOVING CLIP (Miguel, 2026-09-02)

Miguel read the 21 clerk flags of daily batch 2 and ruled **most of them false
positives**. The cause was structural, not sloppiness: the clerk samples a still
frame ~0.3 s after each visual boundary, which is **inside** the 1-2 s entry
animation. "Empty bubble", "no Opus mark yet", "the label lands late" were the
picture still arriving, and a still frame cannot tell a transition from a held
state. The ones he confirmed were the ones a frame CAN see — a cup jammed into
the phone, arcs overlapping the monitor, labels on different baselines — plus one
that only motion shows: a second Codex logo cut in half **while moving** ("it has
motion"). He also ruled the Claude Code mascot flag FALSE: people recognise it.

Four rules, binding on every video:

1. **Sample at boundary + 1.5 s**, not + 0.3 s. Entering elements have landed;
   you are judging the beat, not the animation. A beat shorter than 1.5 s is
   sampled at its midpoint and the row says so.
2. **Absence has a duration test.** An emptiness claim (empty zone, empty bubble,
   missing label) counts only if the emptiness **persists >= 1.5 s** of settled
   screen time. A LAW 2 "named tool with no mark" claim counts only if the mark is
   still absent **>= 2 s after the word**.
3. **Cramp / overlap / clipping is judged on a HELD frame, or declared a MOTION
   DEFECT** — an element crossing into, over or through another object or a border
   while moving. **Motion never excuses a collision**; it just has to be named as
   that class.
4. **EVERY candidate flag is verified on the moving clip before it may be written
   as a NO-SENSE row**: `pipeline/verify_flags_gemini.py <render> <id> --flags
   <flags.json>` cuts t-2.5 s .. t+3.5 s with audio and asks `gemini-3.5-flash-lite`
   for CONFIRMED / TRANSITION / REFUTED. **Only CONFIRMED counts.** TRANSITION and
   REFUTED go in the autopsy's separate **dismissed table** with the model's
   reason — logged, never deleted. The clerk's return carries both counts and the
   verification cost for that video (fractions of a cent).

This does not soften the gate: one CONFIRMED flag still holds the render, with no
warning tier. It stops the clerk holding a render on a frame of an animation.

**SUPERSEDED THE SAME DAY BY PROCEDURE v3 — THE ROLES ARE FLIPPED.** The
still-frame clerk was measured unstable (two runs on `codexvoice`, two different
lists; 4 of Miguel's 6 confirmed defects missed) while the moving-clip verifier
agreed with him 5/5, so **`pipeline/clerk_video_gemini.py` now WATCHES each staged
render end to end and PRODUCES the candidate list, and the Opus clerk only
ADJUDICATES it** (CONFIRMED / ACCEPTED-BEHAVIOUR / REFUTED) and runs the Phone
Test. Full procedure and the calibration numbers:
`pipeline/semantic_review.md` (v3) and
`shorts_run9/review/clerk_v3_calibration.md`.

---

## ROUND-2/3 LAWS (2026-09-02) — ten laws, ten instruments

Everything the run-9 rounds added, in one place, with the check that enforces it.
No line here is advisory and none has a warning tier unless it says so. The law
text lives in the sections above and in the format chassis; this is the index the
next daily run reads.

1. **The visual zone's ink NEVER reaches zero.** Only the opening is exempt —
   frames before the first spoken word, plus the composition's leading empty run.
   The instant any ink has appeared the zone may never empty again; an empty
   visual zone is always NO-SENSE.
   → `formats/whiteboard/lib/whiteboard_build.py: assert_zone_never_blank()`
   (CLI: `<render> --vid <id>`, built on `clip_coverage_check.zone_ink_series`).
2. **Clip intervals are half-open and FRAME-QUANTISED — one owner per frame.**
   `start = k0/fps`, `dur = (k1-k0-0.5)/fps`, `k = round(t*fps)`. Never a bare
   epsilon: an eps that lands on the frame grid does not avoid the boundary, it
   IS the boundary (one ulp of a double decided a 40 ms blank frame at 20.60 s).
   → `pipeline/clip_coverage_check.py` — holes=0, ghosts=0, 0 interior blanks,
   measured on the page AND on every decoded frame, neither of them sampled.
3. **An outro is an OPAQUE RISING SHEET, never a fade and never a scrim.** The
   board exits before the handle card starts; a 0.94-opacity veil cost a short
   its last 3.4 s to a double exposure.
   → `whiteboard_build.assert_outro_clear()` — no ink authored at or after the
   outro anchor, wipe complete before the card.
4. **A whiteboard WRITES every key word.** Every drawn object gets its key word
   handwritten beside it; a comparison the script speaks is drawn as a comparison
   (both terms, different shapes, a connector); the key term is written first,
   alone, and large (≥22 design units).
   → `whiteboard_build.assert_label_law()`, called from `build()`, which cannot
   run without `label_plan=` and `key_term=`.
5. **A caption beat is never a lone function word, and never a SQUARE pill.**
   Both refusals are independent: "in" argues nothing whatever it measures, and a
   pill at aspect 1.01 reads as the LinkedIn badge whatever it says.
   → `pipeline/captions.py` §3b — `merge_function_only_beats()` over the whole
   beat stream, then `assert_no_function_only_beat()`; `PILL_MIN_ASPECT = 1.45`,
   read off the measured gap between "you" (1.42) and "day." (1.53).
6. **The depth roster is TOPICAL, and no mark may read as a missing image.** The
   cast is the comparison the script actually makes — never a consumer-app wall,
   never a placeholder, never the story's own subject mark. A real logo that is a
   hollow single-colour box crossed by both its diagonals is refused as artwork,
   not as a missing file.
   → `cutout_depthfield.assert_cast_resolves()` before any frame renders, plus
   `cutout6_check.check_depth_field()` (check 25) on the emitted HTML.
7. **The protrusion gate is WINDOWED and it runs inside the shipper.** A sliding
   5 s window, hop 1 s; one qualifying window is a verdict. `ship.py` refuses to
   encode a matte from an alpha that fails it — a guard is only a guard if it is
   called, and `leak_check: clean` in a run record is not the same thing as a
   clean file.
   → `pipeline/sam2/protrusion.py` inside `pipeline/sam2/ship.py`; the fix is
   `bolsterfix.py` + a re-track, not `--allow-protrusion`.
8. **The face is CENTRED in every full-face segment, within ±4 % of frame width.**
   Warning level on the split's face band (a fixed approved crop). A near-constant
   dx across every sample means the plate window, not the animation.
   → `pipeline/face_center_check.py` — BlazeFace, every hit validated (confidence
   ≥ 0.70 and ≥ 40 % skin-tone pixels), exits 1 on a defect.
9. **A label arrives WITH its object, on the beat its word is spoken.** Object and
   printed key are ONE BLOCK. The cure is never to bring the label early — it
   would then precede its word — it is to HOLD the object until the key lands.
   → `assert_label_law()` on the whiteboard, Law 9 in every other format, and the
   Viewer Test on the frames.
10. **A flat-top bar has a real top — a masked top is not a top.** A bar that
    overruns its block and hides the overflow behind an alpha mask reads at phone
    size as a failed render; re-budget the heights so the peak lands inside the
    block.
    → Gate 1 geometry + the contact sheet; LAW 34's corollary.

---

## MARK IDENTITY (Miguel, 2026-09-02, batch-2 review) — LAW 2's missing half

LAW 2 says a named tool renders as its logo. It never said WHICH FILE, and a
registry that carries two files for one brand will hand you the wrong one. Two
rulings, both from the batch-2 review, both binding everywhere:

- **"Claude Code" is the OUTLINE-FREE MASCOT.** Registry key `claude-code`
  (`assets/logos/coding-tools/claudecode-color.png`), never the white-outlined
  sticker, which is now `claude-code-sticker`
  (`assets/logos/coding-tools/claude-code.png`). A sticker outline is a die-cut
  edge from a print sheet; on a cream board or a white tile it draws a halo
  around the mark that belongs to no brand. This is a FILE choice, not a design
  choice — the two live 20 characters apart in the same directory and the wrong
  one shipped in six run-9 projects.

- **"Claude Cowork" is the ORANGE mark**, `claude-cowork`, and it must READ AT
  PHONE SIZE. The cream original is `claude-cowork-pale` and is retired as a
  default: a cream bolt on the whiteboard's cream ground is invisible, which is
  what Miguel found. Anthropic publishes no orange Cowork asset (searched
  2026-09-02: the desktop app bundle, its `ion-dist` asset set, `app.asar`,
  Application Support, claude.com/product/cowork, the App Store), so the shipped
  file is the pale mark RECOLOURED to #D97757 along its own luminance ramp with
  the geometry and alpha untouched. It is DERIVED and the registry says so.

- **A MARK IS SIZED BY ITS INK, NOT BY ITS BOX.** Cowork's bolt covers 27.1 % of
  its bounding box where a solid app tile covers ~70 %, so an equal box gives it
  a third of the presence. Where marks sit in a row, scale each glyph so the row
  reads as equals at 405x720 — equal boxes are not equal marks.

Corollary for every future mark: when the registry holds more than one file for
a brand, the SCRIPT's word decides which one, and the pick is written into the
generator as a comment naming the registry key. "The logo" is not a spec.

---

## ROUND-4 LAWS (Miguel, 2026-09-02) — seven laws, seven instruments

Round 4 of the daily trial. Every line is Miguel's own verdict on the run-9
renders, and every law below carries the check that refuses a build without it.
No advisory tier: where a number is softer than the one Miguel said, the reason
is written down and the measurement that forced it is quoted.

The two lanes, because a law has to be checkable wherever the page comes from:

| lane | what it judges | where it lives |
|---|---|---|
| **DOM lane** | split / takeover / cutout / facesplit / artifact spine — pages composed of elements | `pipeline/geometry_audit.py` → `check_layout()` (Gate 1) |
| **BOARD lane** | whiteboard — one `<svg>` canvas whose ink is drawn progressively, so a DOM box is its FINAL shape at every instant and cannot be measured | `formats/whiteboard/lib/whiteboard_build.py`, on the AUTHORED board in board units, called from `build()` |

Gate 1 skips any clip containing `#cam > svg` and any element with a live
`stroke-dasharray` for exactly that reason. Neither lane is optional.

---

### LAW 37 — A POINTING CUE RAISES THE SOURCE POST

> *"When I say 'like this person, or guy on X' I usually point up, that means
> that the tweet related to that post should appear with the highlight."*

Miguel points at the ceiling when he cites someone. That gesture is on camera,
and it is the one moment the audience is told *this is not me talking, this is
something somebody posted*. If nothing is on screen there, the gesture points at
nothing.

The cue is a property of the SCRIPT, so it is found deterministically from the
tight transcript before anything is drawn: demonstrative or indefinite + person
or post ("this guy", "someone on X", "this post", "saw a post", "a guy who…").
At the cue word — inside ±1.0 s, one block, never after it — the SOURCE POST
card is on screen with the marker highlight on the line that carries the claim.
Still bound by **GLOBAL LAW 3**: 2-4 s, no metrics chrome, and only when the
post IS the news. A cue the post cannot answer is WAIVED IN WRITING in the plan,
never in silence.

**The check.** `pipeline/pointing_cues.py` — `scan(words)` lists every cue with
its word index, time and window; `assert_cues_covered(cues, plan_cards)` refuses
a plan that leaves one unanswered, or that raises a card with no highlighted
line (a post with nothing scoped argues nothing — GLOBAL LAW 5).
CLI: `pointing_cues.py --vid <id>`. The builder brief's PLAN step must list
every cue and the card it raises. Measured 2026-09-02: `impossibletask` has one
("like this guy", 2.72 s); `kimiram` and `perplexityprojects` have none.

---

### LAW 38 — EMPHASIS MATCHES ITS TARGET: HIGHLIGHT IMAGE TEXT, BOX A DRAWN OBJECT, NEVER RING ANYTHING

> *"For text, do not circle or make a box, I want you to use the nice clean
> highlight that you used to use."* — and, on the whiteboard, *"circling of the
> clock looks off"*.
>
> **AMENDED 2026-09-02**, after Miguel watched the fixed videos ("those look
> fantastic"): *"do not use highlight for everything, it's just for when you need
> to highlight text on an image, for the rest you can use the boxing you were
> using before, which are perfectly fine."*

The law reads off the TARGET, not off taste. Three rules, no exceptions:

1. **TEXT ON AN IMAGE → the marker HIGHLIGHT.** A source post, a screenshot, a
   document, a UI capture — anywhere the words the viewer is reading are part of
   a raster or an asset card. The primitive is the factory's own **marker fill**,
   first shipped in `shorts_run6/gen/mathvoice_kinetic_gen.py` and carried through
   run 7 (`mathconjecture_kinetic_gen.py:601`):

   ```css
   .hl { background: rgba(198,103,72,0.32); border-radius: 6px; }
   ```

   wiped open left-to-right (`wipex`, 0.34 s), **one fill per LINE** — never a
   union box over a paragraph, because a box that covers everything scopes
   nothing, which is the one job a highlight has. It rides over the thing it
   scopes (`data-overlap-ok`). On the board:
   `whiteboard_build.highlight()` / `highlight_lines()` / `highlight_label()`
   (`HL_FILL`, `HL_RADIUS_U = 3.2 u` = 6 px, `HL_WIPE_D = 0.34`,
   `HL_LINE_STAGGER = 0.10`), authored at `scaleX 0` and wiped open from its left
   edge, which is what a marker actually does.

2. **A DRAWN OBJECT or board/scene TYPE → BOXING, and boxing is fine.** This is
   the factory's own emphasis from runs 3-8 and it was never the complaint:
   * **DOM lane — the PANEL BORDER FLIP.** The object's OWN border goes
     terracotta: `.node.hero { border-color: TERRA_L }` driven by
     `tl.fromTo(sel, {borderColor:"rgba(17,17,17,0.16)"},
     {borderColor:"rgb(221,114,89)", duration:0.38, ease:SOFT})`
     (`shorts_run4/gen/deepresearch_diagram_gen.py:317` and `:795`, whose comment
     already records why it beat a ring: *"never ring a node that connectors land
     on"* — the ring's border was crossed by all four arrows and read as broken).
   * **BOARD lane — the terracotta MARKER BOX**, `fill:none`, `stroke:TERRA`,
     `stroke-width:SW_THIN`, a small `rx`, popped in over 0.34 s from scale 0.55.
     Shipped in `whiteboard_fix6_core.py:668` (the `ring{i}` rects — misnamed,
     they are rectangles) and now re-homed as
     **`whiteboard_build.box_emphasis(b, box, t, target=..., pad=BOX_PAD_U)`**,
     which registers kind `"boxemph"` so the checks can see it.
   A box is emphasis, so it obeys the spacing law like any other object: it never
   crowds a NEIGHBOUR (gutter ≥ 16 px / 8.5 u refusal, 24 px aim). It is welded
   to the object it picks out and to that object's written key — those are one
   block — and it is judged against everything else. It is never drawn on image
   text: that is the highlight's job.

3. **RINGS, ELLIPSES and CIRCLES are retired everywhere, on every target.** That
   shape is the actual complaint (the circled clock). There is no legal use.

**The check.**
* BOARD lane — `whiteboard_build.assert_no_enclosure()`: (a) a rigid of kind
  `ring` refuses the build; (b) a `box_emphasis()` whose target is a RASTER
  refuses the build (a raster is declared with `note_asset()`, or named like the
  captures this factory pastes — `postcard`, `post-card`, `shot`, `screenshot`,
  `tweet`, `capture`; a DRAWN `job-card` is not one, which is why the declaration
  exists); (c) a `highlight()` with no raster under it is reported as
  `wrong_tool_advisory` and **never gates** — Miguel approved a board that swipes
  a track bar and a written key, and this law has already over-banned one of his
  tools once.
* DOM lane — Gate 1 `enclose`: (a) ERROR on a ring/ellipse/circle used as
  emphasis (`<circle>`, `<ellipse>`, a `ring` class, or an outline whose radius is
  ≥ **50 %** of its short side — a pill, not a box) that contains another object
  with a margin ≤ 26 px; (b) ERROR on an emphasis box whose target is IMAGE TEXT
  (the target is or sits inside an `<img>`, a post card, a screenshot container,
  or anything carrying `data-asset`); (c) WARNING on a highlight over a drawn
  object or scene type. `data-container` opts out; **a rectangular box around a
  drawn object is no longer a finding at all**.
  An emphasis box is an outline drawn in the ACCENT (the terracotta family:
  `r > 120`, and `r` more than 1.35× both `g` and `b`) or declared with
  `data-emphasis="box"` — a NEUTRAL hairline is chrome, so a plain frame around
  a screenshot is never read as boxing its text.

Calibration (2026-09-02, after the amendment):

| page | verdict |
|---|---|
| the retired `impossibletask_whiteboard` rings (`clock-ring` 104×132 u @ 8.78 s, `system-ring` 188×130 u @ 10.56 s) | **REFUSED** — board lane, unchanged |
| a DOM ring around a drawn clock (synthetic) | **ERROR** `enclose` |
| a box over a post card's text (synthetic, and the same case declared on the board) | **ERROR** / **REFUSED** |
| a box around a drawn node, with its key inside (synthetic) | **PASS**, and `cramp` stays silent |
| a highlight over a drawn bar (synthetic) | **warning** only |
| a highlight over a post card (synthetic) | silent |
| a NEUTRAL hairline frame around a screenshot (synthetic) | silent — chrome, not emphasis |
| staged `impossibletask_whiteboard` | **PASS** — 6 highlights, raster `post-card` seen, 4 advisories |
| staged `kimiram_whiteboard`, `perplexityprojects_whiteboard` | **PASS**, nothing to report |
| staged `kimiram_split`, `impossibletask_split`, `kimiram_cutout`, `kimiram_facesplit`, `perplexityprojects_split` | **0 errors, no `enclose` finding** (the one warning is the pre-existing `offcenter scappill`) |

**Why the amendment exists.** The first draft of this law was written from ONE
rejected page and banned a whole primitive: it read "no circle, no ellipse, no
box" and retired the run-3-8 boxing along with the ring Miguel actually named.
Two of his complaints were about a ring around a clock and a box crushed against
text inside a cramped board — neither was an argument against boxing a drawn
object, which he then confirmed is "perfectly fine". A law inferred from a single
instance over-reaches; the fix is to make the law name its TARGET.

---

### LAW 39 — A NAME GOES ABOVE OR BELOW THE THING IT NAMES. NEVER BESIDE

> *"When we name things I would rather the text be at the top or bottom."*

Label and object are ONE BLOCK (GLOBAL LAW 9). This law fixes where that block
puts the writing: the label's centre falls inside the object's horizontal extent
**±15 %**, and the label sits entirely above or entirely below it. Side
placement is an error, not a taste.

Decorations do not host labels — a brand mark in a lockup, a bullet, a tick. A
rigid whose name starts `mark:`, `logo:`, `check:`, `bullet:`, `tick:` or `hl:`
is a decoration and is skipped as a host. A key CONTAINED by a shape is that
shape's own content, never a label beside it.

**The check.**
* BOARD lane — `whiteboard_build.assert_label_side(b, label_plan)`, welding each
  planned key to the nearest concurrent non-decorative object inside
  `LABEL_WELD_U = 40 u`.
* DOM lane — Gate 1 `sidelabel`: ERROR on a declared pair (`data-label-for`),
  WARNING on a geometric weld inside `LABEL_WELD_PX = 60`.

Calibration: fires on `impossibletask_whiteboard` (`THE JOB` sits beside
`agent`, centre off +62.0 u against a ±23.4 u band) and on
`impossibletask_split` (`b3-codexlbl` "CODEX" −342 px on a ±273 px band;
`b4-prnlbl`/`b5-prnlbl` "THE 3D PRINTER" +359 px). Silent on all three
references.

---

### LAW 40 — ARROWS INTO ONE TARGET LAND ON ALIGNED ANCHORS

> *"The arrows that point to the folder all point to a different spot or
> height… I would like some workaround."*

Here is the workaround, as a rule: **every connector into one target terminates
on a point of that target's VIRTUAL BOUNDING RECTANGLE — never on its irregular
outline** — and connectors sharing a target land at the SAME height (±4 px) or
mirror-symmetric about the target's centre axis.

`whiteboard_build.anchor_points(target_box, n, side="top"|"bottom"|"left"|"right",
inset=0.16)` returns those points: `n` of them, evenly spaced, symmetric about
the axis, held off the corners. Use it; do not hand-place ends.

**The check.**
* BOARD lane — `assert_anchor_law(b, connectors)` over the declared
  `connectors=[{"to": <rigid name>, "end": (x, y)}]`: the target must be a real
  registered rigid, every end must sit on its rectangle, and the group must be
  level or mirrored.
* DOM lane — Gate 1 `anchorline` over `data-connect-to` groups, `ANCHOR_Y_TOL_PX
  = 4`.

Calibration: both run-9 boards declare no connectors, so this reports SKIP on
them — it is the law for the geometry that produced Miguel's complaint and it
binds from the next build that draws two arrows into one thing.

---

### LAW 41 — THE SPACING LAW: NOTHING IS CRAMPED, AND NO LINE CROSSES A NAME

Miguel's screenshot: the IMPOSSIBLE TASK card, the CODEX tile, the clock and the
TEMP/PROGRESS panel jammed into one corner — and the arrow from CODEX to the
panel drawn straight **through the word CODEX**.

1. **Gutter.** Any two objects keep a gutter. The AIM is **24 design px**;
   the REFUSAL line is **16 design px** (8.5 board units), and the reason is
   measured, not preferred — see the calibration below.
2. **A connector never crosses printed type.** Judged on the type's CORE band
   (inset 22 % top / 28 % bottom / 4 % each side): an underline or a strike
   grazes an edge, a crossing goes through the letters.
3. **Nothing overlaps unless it was authored as one block.**

Four blocks form automatically, because each is already a law elsewhere: a key
welded to its object (LAW 39 / GLOBAL LAW 9); everything one container holds; a
run of printed lines on a shared column (a paragraph); identical shapes stacked
tighter than their own height (a stack of bricks, a ladder). A run of ≥3
identical shapes in one section is a SERIES — one object drawn in parts. Anything
else is declared: `blocks=(("a","b"),)` on the board, `data-block` in the DOM.

**CALIBRATION — why 16 px and not 24.** Measured 2026-09-02 at 0.5 s steps:

| page | tightest non-block gutter |
|---|---|
| `impossibletask_whiteboard` (rejected) | `job-card ⟷ monitor-card` **0.0 u** (touching) |
| `impossibletask_split` (rejected) | `b3-codexlbl ⟷ b3-panel` **2.0 px** |
| `perplexityprojects_cutout` (APPROVED) | **19.3 px** |
| `kimiram_whiteboard` (APPROVED) | **10.2 u = 19.1 px** |
| `kimiram_split` (APPROVED) | **25.0 px** |

At Miguel's 24 px, two boards he APPROVED report violations. A refusal line that
fires on approved work is not a law, it is noise, so the gate is the largest
round value strictly under the approved floor: **16 design px = 8.5 board
units**, the same number in both lanes. 24 px stays the number the PLAN aims for
and the clerk reads by eye.

**The check.**
* BOARD lane — `assert_spacing_law(b, blocks=…)` and `assert_no_text_crossing(b)`.
* DOM lane — Gate 1 `cramp` and `crossing`. A gutter of exactly 0 (edge contact)
  is NOT a cramp in the DOM lane: it is an assembled drawing or a connector
  landing, and real overlap belongs to `collision`.

Results: `impossibletask_whiteboard` → cramp `job-card | monitor-card = 0.0 u`
and crossing `a stroke drawn at 6.42 s crosses 'type:CODEX'` (Miguel's arrow,
exactly). `impossibletask_split` → 3 cramp errors including `b3-codexlbl |
b3-panel = 2.0 px`. All three approved references: **0 errors**.

---

### LAW 42 — A MARK LEAVES WHEN ITS BEAT IS DONE

> *"The perplexity logo stays and just bothers the entire flow."*

A mark is on screen while it is the referent. When its beat ends it EXITS —
unless it holds a declared **anchor** role: the spine of the argument the later
beats keep pointing back at. Every drawn element therefore declares a LIFETIME:
a finite beat range, or `anchor`.

A **single-board** build (LAW 43's exception — one idea that accumulates) is
all-anchor by definition and is detected automatically: no chapter seam exists,
so nothing was ever meant to leave. A **chaptered** build — one that erases —
must give every mark a finite `t_to` or a name in `board_anchors=`. Anything
visible for more than **40 %** of the runtime without that declaration is an
error.

**The check.** `whiteboard_build.assert_lifetime_law(b, dur, anchors=…)`, plus
the `Board.rigid(kind, box, t_from, t_to)` window it reads. Chapter seams are
read off the registry itself (an erase time shared by ≥3 rigids IS a seam), and
those seams also CLAMP open-ended marks for every geometry law above — without
the clamp a chapter-1 key gets compared against a chapter-3 bar and the audit
invents violations no viewer can see.

Calibration: fires on `impossibletask_whiteboard` — `11 PM` 95 %, `CODEX` 88 %,
`TEMP` 84 %, `PROGRESS` 83 %, `ASKED FOR` 59 %, `IT CAN DO` 56 %. Silent on
`kimiram_whiteboard` (single board: all anchors).

---

### LAW 43 — THE WHITEBOARD MAY USE SEVERAL BOARDS

> *"Not necessary to keep everything in a single screen unless it's a video that
> you think can work (like the hermes one)… if there's too many different ideas
> don't bother. Change the rules of the format."*

**The format law is inverted. CHAPTERS ARE THE DEFAULT; ONE BOARD IS THE
EXCEPTION.**

* **Chapters (default).** The board clears between idea groups. Each chapter is
  planned to FIT its ideas at legible scale — the Phone Test decides, not the
  author — and LAW 41's spacing is applied *per board*, on the whole legal
  surface, not on a corner of it.
* **One board (exception).** Only for a script with ONE idea that accumulates,
  where the finished frame is the argument (the Hermes journey, `kimiram`).
  Choosing it is a decision that goes in the plan with its reason.

Unchanged, and interlocking: the rising-sheet outro (LAW 3 of the ROUND-2/3
index), the label law, the pen without its squeak, no textured background, and
the ZERO-INK LAW at every chapter erase — an erase must hand over, never blank.
A chapter that clears to nothing is the same defect the outro dead-slot was.

**The check.** `formats/whiteboard/CHASSIS.md` carries the rewritten law;
`chapter_seams()` derives the seams; `assert_zone_never_blank()` proves the
handover on the decoded render; `assert_lifetime_law()` (LAW 42) proves every
chaptered mark declares when it leaves.

---

### LAW 44 — THE SILHOUETTE NEVER TOUCHES A SIDE EDGE ABOVE THE BUST

> the silhouette never touches a side edge above the bust; full-take sweep,
> never sampled

The cutout bust is welded to the bottom of the canvas and its shoulders spill
past both side edges on every frame — that is the format's full-bleed base, and
it is correct. A **limb** doing it is not. A hand reaching sideways past the
visible frame is sliced flat by the canvas edge, and because the cream keyline
is dilated from the same alpha, the keyline is cut too: the hand ends in a bare
vertical slice with no outline, which reads as an amputation.

Three staged cutouts shipped this with every gate green — `impossibletask` twice
(1.08 s and 0.16 s) and `kimiram` twice (0.80 s and 0.20 s). Three of those four
windows are **under 0.8 s**, i.e. under the 2.5 s stride a clerk spot-checks at,
so no amount of review diligence would have found them. **Sampling cannot clear
this class.** The sweep is ~40 s of CPU on a whole take and runs on every frame.

**A limb leaving frame is not the defect.** The evidence sheet
(`review/edgeclip_evidence_kimiram.png`) settles it: the control frames show the
cream keyline tracing his shoulder continuously into the frame edge, which is how
a body should exit. The defect frames show the hand ending in a hard vertical
slice with *no keyline along the cut*. What separates them is not where the
silhouette is — it is whether the silhouette is **complete**:

> the trim is flush against the **plate's own border**, so the rim (that same
> trim, dilated 7 px) is cut with it and the shape has no outline on the side it
> was cut. That outline-less block then enters the visible frame.

So **the gate is the plate's own left and right borders**, not the frame edge.
The frame edges are measured and reported, never gated.

The test is structural, not proportional. A "bottom 15 %" exclusion was tried
first and flags 100 % of frames in every take, because the shoulder occupies
16.8 % of the silhouette at the edge column. Instead, at each plate border column
the alpha's contiguous opaque runs are split into the **bust run** (the one
touching the bottom row — allowed to cross) and everything else. A frame fails
when an opaque run there is **detached** from the bust run, or when the bust run's
top climbs **more than 60 canvas px** above that take's own shoulder baseline.
60, not 30, because the plate border sits further out on the shoulder slope where
the same sway moves the contact row further: measured over whole takes, clean
plate-border columns max at 16 / 19 / 44 canvas px, against 255 and 408 for a cut
hand.

**The remedy is an OVER-WIDE PLATE, never a repaint and never a waiver.** On
kimiram no 1.2:1 window could satisfy the law at all — defect frames by
visible-left master column ran 117 / 120 / 76 / 20 / 26 / 24 across x 650-1000, a
measured optimum of 20 and never a zero, because the resting shoulder line falls
away steeply towards frame-left. So: **keep `k`, the head scale and the face
centre exactly as the foundation requires, and extend the master crop sideways so
the plate is wider than the visible frame and sits at a more negative left
offset.** Nothing on canvas moves — same visible window, same head parity, same
face centre, same frozen post parameters — and the frame does the cutting while
the plate never does. kimiram went from a 1188x990 box at (-54, 930) to 1485x990
at (-351, 930), with 78 canvas px between the plate border and the leftmost
silhouette of the whole take. The plate is then no longer 1.2:1 and no longer
centred, so the chassis reads the box origin from `plate.json` instead of
assuming symmetry.

**The check.** `pipeline/edge_clip_check.py` — full take, every frame, on the
shipped matte alpha with the plate box read from `_geom_*.json`. Wired as a
post-ship gate in `pipeline/sam2/ship.py` (a matte whose trim the plate cuts is
not shipped; `--allow-edge-clip "<reason>"` overrides in writing and records the
reason in the ship json) and as check 26 in `formats/cutout/lib/cutout6_check.py`.
Calibrated 2026-09-02: fires 2 windows on the shipped kimiram, 3 on the retired
impossibletask, silent on perplexityprojects.

**LAW 44a — AND IT NEVER TOUCHES THE PLATE'S TOP EDGE EITHER (2026-09-03).**
LAW 44 gates the plate's LEFT and RIGHT borders, and that omission shipped:
`supergrokplus_cutout` was plated with the crop's top edge BELOW his cap, so all
938 frames of the matte touched alpha row 0 and the delivered frame carried a
flat ~490 px slice across his head at canvas y 930 — with the caption pill seated
the canon clearance directly above it. The plate's top IS the frame's content
boundary on a bottom-planted cutout box; nothing is painted above it. The remedy
is on the PLATE, never on the seat: `pipeline/sam2/plate.py::window()` now slides
the bottom-planted crop UP until the crown has `HEADROOM_ON_CANVAS` (24 canvas
px) of clear plate above it — `k`, head parity and face centring untouched,
`visible_window_drift_master_px` 0.0 — `platelib.build_plate` refuses a plate
under the 8 px hard floor, a per-video envelope refuses to derive a seat from an
alpha whose crown is on row 0 for more than a quarter of frames, and
`cutout6_check.check_crown_clearance` (check 27) measures pill-bottom-to-crown on
the DELIVERED file every 0.5 s. Calibration and the full write-up are in
`LEARNINGS.md` under 2026-09-03 and in `formats/cutout/CHASSIS.md`.

`impossibletask` is the second take to need the remedy and the crop was extended
on the LEFT ONLY (box 1188x990 at -54 → 1386x990 at -252, plate 1260x900 from
master crop `2660x1900+270+260`), which leaves the right border where it already
was; over-wide is a plate change, never a canvas one, so extend only the side the
measurement asks for. Two things it moves downstream are written up in
`formats/cutout/CHASSIS.md`: plate space stops being 1080x900 for anything that
rescales a matte alpha, and the staged matte must be stamped by CONTENT — a
name-only stamp let two renders composite the matte a re-track had already
replaced, with every gate green on the file the gates read instead.

---

### LAW 45 — A CHAPTER HANDOVER MUST LAND ON AN IDEA

> Within **0.30 s of a chapter erase completing**, at least one complete,
> nameable object — or the board's key word — must be **fully drawn**. A bare
> stroke does not count.

An amendment to LAW 43, and the bill that came with it. Making chapters the
default gave the whiteboard four erases on a 41.6 s take, and the round-5 Viewer
Test found what was on the far side of them:

| seam | ink at seam+0.3 s | what the board held | words playing over it |
|---|---|---|---|
| ~5.2 s | 0.31 % | two unfinished box corners | *"build a full-blown"* |
| ~8.6 s | 1.8 % | one L-stroke and a bare arc | *"And before he even"* |
| **~16.85 s** | **0.30 %** | **one horizontal baseline** | *"the capacities of these"* |
| **~25.5 s** | **0.27 %** | **one short diagonal** | *"If you want to make sure your AI"* |

The two bold rows scored NO-SENSE. The worst put **0.9 s of the most
instructional sentence in the video over a single line.** Total exposure across
the four seams was ~2.7 s of a 41.6 s short.

**LAW 43's ZERO-INK clause was satisfied throughout** — minimum ink 0.27 %,
never 0, so every erase did hand over. Handing over to one stroke is not the
same as handing over to an idea, and **no ink-fraction threshold can tell those
apart**: a bare baseline is 6,960 px of ink and argues nothing, `THE JOB` is
1,612 px and argues everything. The discriminator has to be SHAPE.

**How to satisfy it.** Either start the incoming board's identifying object
*inside* the erase and draw it fast, or carry the outgoing board's anchor object
across the seam until the first new object completes. Both are legal; the first
is what `impossibletask_whiteboard` v3.2 does, with `SEAM_LAP = 0.04` and
`SEAM_DRAW = 0.28` against a 0.30 s erase. A chapter may also state its
**subject** rather than an object — writing `THE JOB` before drawing its track
is the native whiteboard order, the title then the thing.

**The check.** `formats/whiteboard/lib/seam_check.py` — for each seam it decodes
every frame of the window `[erase_completes, +1.6 s]` and reports **dead time**,
how long the board argued nothing. Per frame it thresholds the ink over the
board's legal surface, **removes the marker sprite by template match** (66x78 px
of solid fill sitting on the stroke it draws; without it a bare baseline plus
the pen merges into a 666x90 blob and passes every shape test), dilates, and
accepts a blob as one of two things:

* **OBJECT** — ink ≥ 2,600 px, box minor ≥ 46 px, major ≥ 118 px, and
  ink-weighted **σ_minor ≥ 18 px**. σ_minor is the whole check: a bounding box
  cannot separate a bar standing *on* a baseline (851x102, every box test
  passes) from the bar chart it will become, because the two touch and are one
  component at any dilation. Measured on the failing render: bare strokes
  **3.4-3.5 px**, the line-plus-half-popped-bar **13.8-14.2**, a finished
  90x40 u bar **21.7**, and every object the Viewer Test named — post card 38.4,
  Codex tile 43.8, bars 55.3, clock 60.6, monitor card 106.8-139.5.
* **WORD** — box height 26-80 px, width ≥ 80 px, ink ≥ 900 px, and ≥ 3 separate
  marks inside it. Type is thin by nature (`THE JOB` is σ 7.1) and the law
  admits the board's key word; the 3-mark rule is what stops one long stroke
  claiming to be one.

Landing is claimed only from the first of **3 consecutive** qualifying frames —
a single qualifying frame in an otherwise dead window is an artefact, not an
idea.

Calibrated 2026-09-02 on `impossibletask_whiteboard`: on the failing render it
reports dead 0.36 s at the 16.70 s seam and 0.68 s at 25.38 s, and FAILS at the
two frames the Viewer Test sampled (17.10 s, 25.70 s); on the fixed render all
five seams report **dead 0.00 s** and both probes PASS.

## STOPPING RULE (Miguel, 2026-09-02: "why have you been looping so much")

Clerks exist to catch what Miguel would REJECT, not to polish what he ACCEPTED.
- A render Miguel has approved ("looks good / fantastic") is DONE. Clerk notes on an
  approved render are LOGGED in the review file, never chased. The only further
  changes to an approved render are the ones Miguel asks for.
- A fix round is scoped to Miguel's findings on that render. Non-blocking observations
  a clerk adds (sub-second fade valleys, case of the outro handle, scale consistency
  between videos, advisory clearances) are recorded for the NEXT batch's brief, not
  re-rendered now.
- One clerk pass per fix round. If the clerk finds only new non-blocking notes, the
  render ships; if it finds a real regression of what Miguel asked for, one more fix.
- The batch is finished when every render is either Miguel-approved or has passed one
  clerk pass on the specific things Miguel asked to change. There is no round N+1
  because a clerk was thorough.
- **A clerk flag is not a defect until the moving clip says so (2026-09-02).** A
  still frame cannot judge a transition. Every candidate goes through
  `pipeline/verify_flags_gemini.py`; only CONFIRMED flags reopen a render,
  TRANSITION and REFUTED are logged in the dismissed table and chased by nobody.
  This is the loop-shortener the stopping rule was missing: most of batch 2's 21
  flags were animation frames, and re-rendering against them would have been pure
  looping.

## THE TWO EFFICIENCY LAWS (2026-09-03)

**The mechanical work happens ONCE, before the builders, and the checks happen
ONCE, in one decode.** `pipeline/prep/prep_batch.py` cuts, plates (over-wide by
default), prompts, tracks on Modal and ships the matte for the WHOLE batch in
parallel, and a builder consumes its prep package instead of redoing any of it;
`pipeline/qc/qc_pass.py` decodes a finished render once and runs every
frame-based check on that single stream. Neither re-implements a check: each
calls the existing module's own function with its decode primitive swapped for a
cache, so a number that comes out of these two is the number the individual CLI
prints, and a check that reports SKIPPED is never a pass.

## REJECTION MOVES BEFORE RENDER (2026-09-03)

**A render is the most expensive way to learn something the page already knew.**
Every law this factory can check is either a property of the PAGE — the DOM
boxes, the caption pills, the clipping containers, the asset files, the
legibility of a drawn object — or a property of MEANING, which needs motion but
does not need a *finished* render. Only the second kind ever justified paying for
one first, and even that one is cheap at draft quality.

So the order is fixed, and it is enforced by the workflow and by two drivers,
not by a list an agent can skip a line of.

```
prerender_check  ->  phone_test_page  ->  draft_watch  ->  render_and_check
   (page laws)        (legibility)         (sense)          (the real render,
                                                             and its checks)
```

### The three moves before a render — `pipeline/prerender/`

1. **`prerender_check.py <project>`** — Gate 1 with every round-4 class, plus the
   build-time laws measured **on the emitted page**: the caption canon and §3b on
   the MEASURED pills (`getBoundingClientRect` normalised by the page's own zoom,
   because `offsetHeight` rounds 114.59 to 115 and cannot see the law), duplicate
   ids and dead tween targets, every asset reference resolving, no mark reading
   as a missing-image icon, and — for a cutout — the edge-fade guard and checks
   24 + 25. **Non-zero exit means the project does not reach the render lane.**
   Measured: 6.4-6.6 s per project, all three formats.
2. **`phone_test_page.py <project>`** — the Phone Test with **no video render**:
   the timeline is seeked in headless Chrome, the frame is downscaled to 405×720,
   and each declared bespoke object is cropped out alone. The sheet, the judge's
   manifest and the SEALED key are `phone_crops.emit()` — the same function, so
   the sealed-key discipline has one implementation. **Parity proved** against the
   staged `sparkchrome_split`: every phone box identical, edge-mask IoU min 0.969
   / mean 0.982 across six objects. A project that declares no bespoke object gets
   8 spaced whole frames marked `spaced-fallback`, which is a legibility sheet and
   **not** a Phone Test — a video that drew an object and declared none has not
   been tested.
3. **`draft_watch.py <project>`** — a cheap Modal render plus the same Gemini
   watcher, so a SENSE problem surfaces while the page is still free to change.
   There is **no 540×960 render, and no resolution to drop**: `hyperframes
   --resolution` takes presets only and requires an integer multiple of the
   composition, and since HD DELIVERY (2026-09-03, below) every daily page is
   authored 1080×1920 with nothing beneath it. **The
   whole saving is `-q draft`**: measured on `sparkchrome_split` (a pre-HD
   2160×3840 page), 633 frames in **80.1 s for $0.0061**, against the high-quality 1080×1920
   cutout's 100.2 s for $0.0146 — 2.4× cheaper on a frame four times the size.
   The 540×960 artefact is one `ffmpeg` scale off the draft, for eyeballing. The watcher is fed the NATIVE draft, never the
   proxy — it re-encodes to 720×1280 itself, and a different input to the same
   model is a different verdict. Exit 2 = blocking candidates: fix them, or waive
   each one **in writing**. It is a stop, not a verdict; the clerk still rules.

### After the render — one driver, and the checks start per file

`pipeline/render/render_and_check.py` submits every render at once and starts
**that file's** `qc_pass` and **that file's** Gemini watcher the instant that file
lands, instead of after the batch — so the whiteboard's checks are finished while
the portrait-4k split is still rendering. It **stages a render only after that
render's own checks have passed**, which is where the ordering is actually
enforced rather than merely written down. It re-implements nothing: it imports
`modal_render`'s own `pack` / `one` / `price` and calls `qc_pass.py` and
`clerk_video_gemini.py` as their own CLIs.

### What this deletes from the builder brief

The twelve-item check list is **gone from the brief**. An author gets the law
pointers and the order; the commands live in the two drivers. A numbered list
inside a prompt is something an agent can skip a line of and still return
"followed"; an exit code is not.

Three laws still have no tool and are still the author's, and the brief says so
explicitly: the depth cast resolve (`cutout_depthfield.assert_cast_resolves` —
`prerender_check` catches a mark that reads as a broken-image glyph, but only the
author knows which keys the field asks for), `guard_plate_box`, and
`captions.merge_function_only_beats()` over the whole beat stream before
`assert_no_function_only_beat()` (`prerender_check` proves the result; it does
not do the merge).

### The design happens once, as an artifact — and two authors build from it

A single builder holding the plan in its own head produced three platform
renders that argued three slightly different things, because the plan was never
written down anywhere a second agent could read it. So the plan is now its own
step and its own file:

**`plans/<id>_plan.json` + `plans/<id>_plan.md`**, written by a PLAN AGENT that
designs and builds nothing: beats with word timestamps, the picture per beat, the
bespoke objects with their bboxes and their three-word names, the labels and
their above/below placement, the lifetimes and anchors, the connectors and
blocks, the pointing cues and the card that answers each one, highlight-vs-box
per emphasis target, the board mode and its chapters, the cast, and the lane with
its one-sentence reason.

Then **two authors run concurrently from that one plan**: the SCENE AUTHOR
(split + cutout from one shared scene) and the WHITEBOARD AUTHOR (through the
shared harness). **Neither re-plans.** A disagreement with the plan is written to
`plans/<id>_{scene,wb}_notes.md` and the plan is built anyway; the only exception
is a plan instruction a LAW forbids, and then the note names the law. Two authors
improvising fixes to one plan is exactly how three platforms end up arguing three
different things.

The clerk's forbidden list now names `<run>/plans/` explicitly. A plan that is a
real file is a plan a clerk can accidentally read, and a clerk that has read the
plan sees what was meant instead of what was drawn.

## VISUAL VERIFICATION MODEL (Miguel, 2026-09-03)

Every Gemini pass that WATCHES a render runs on `gemini-3.5-flash-lite`:
the clerk watcher (`pipeline/clerk_video_gemini.py`), the flag verifier
(`pipeline/verify_flags_gemini.py`), and Gate 3 describe (`shorts_run3/qc_v3.py`).
It replaced `gemini-3.8-flash` (watchers) and `gemini-3.6-flash` (Gate 3) at
roughly 2.5x lower token price. Env overrides: `GEMINI_CLERK_MODEL`,
`GEMINI_VERIFY_MODEL`, `GEMINI_GATE3_MODEL`. The v3 clerk calibration numbers in
`pipeline/semantic_review.md` were measured on 3.8-flash and are to be re-measured
on the first step-by-step run (recording 2026-09-02 20-34-49).

## HD DELIVERY (Miguel, 2026-09-03) — supersedes "4K is the default"

"No more 4K rendering, always HD." Every short, on every platform, is authored
AND encoded at **1080×1920**. The YouTube split is no exception: no `zoom:2`, no
`data-width="2160"`, no `portrait-4k`, no `--resolution` flag on any render job.
Page shell: `head(TITLE, 1080, 1920, 1, css)`; render dict `{"w": 1080, "h":
1920, "zoom": 1}`. The cut keeps mastering at 3840×2160 because the face crop
windows (LAW: 0 % = `crop=1216:2160`, bottom = `crop=2208:2160`) need those
pixels, but the plates it ships are delivery-sized: `face_bottom_hd.mp4`
1080×1058, `face_full_hd.mp4` 1080×1920. Anything named `*_4k.mp4` belongs to
runs 1-10. A page that arrives at the render lane 2160 wide is a rejection
before render, in the same class as a placeholder logo. Why: TikTok and Reels
play back at 1080p regardless, YouTube's 4K bitrate gain never survived the
phone, and the 4K split cost 2 to 3× the render time of the other two files
under Modal contention (run 10: 797 s vs 489 s uncontended, 4095 s vs 2833 s
contended).

## LAW 44 RULING (Miguel, 2026-09-03, run 12): a plate border gates only when it is ON SCREEN

"If my hand just goes slightly out of the border, it's okay." The edge-clip gate
measures the plate's own left and right borders; with an over-wide plate those
borders sit outside the phone's visible frame, so a hand cut there (and the 7 px
rim cut with it) is never seen: the frame does the cutting, which is the remedy
LAW 44 itself prescribes. From today `edge_clip_check.sweep` gates a plate side
only when its border lies inside the visible canvas or within 7 px of it; touches
at an off-screen border are reported, never refused. Headrest wings and any
furniture kept beside the head remain hard refusals (the protrusion gate is
unchanged). Run 12: astramath (1 frame, border 153 px off screen) and chatgptwork
(2 frames, 136 px off screen) were refused under the old reading and ship under
this one; hermeskanban's wing still refuses.

## DRAFT WATCH OFF BY DEFAULT (Miguel, 2026-09-03)

`pipeline/prerender/draft_watch.py` (a cheap Modal draft + the Gemini watcher before the real
render) is no longer part of the pre-render moves. Measured on run 10: six drafts, 5-18 min
each, about $1.30 of Gemini, one real catch (an empty frame) that qc_pass caught anyway, every
other flag a false positive or a written waiver. The pre-render moves are TWO: prerender_check
(the page laws, deterministic) and phone_test_page (the cold crops). The sense check stays where
it counts: Gate 3 inside qc_pass after the real render, and the clerk's watcher. draft_watch
remains available for a plan that names a specific sense risk worth seeing in motion first.

## RUN-12 REVIEW LAWS (Miguel, 2026-09-03 18:05) — "most of these are solid 9 out of 10"

**LAW 46 — A FALSE START IS NEVER A HOOK.** A scripted opening that repeats inside the
cut's first seconds is an abandoned attempt followed by a restart, and the take begins at
the LAST repeat. The cut stage verifies this on the TIGHT transcript (the raw Scribe pass
can merge the two attempts into one word run, as it did on astramath) and recuts once from
the restart (`cutlib.build_cut`, `FALSE_START_WINDOW_S` 6.0, prefix of 3 opening tokens). A
plan agent that sees a doubled opening in `transcript_tight.json` does not "use it as a
two-step hook"; it reports the cut as wrong. astramath shipped with "GPT Astra solved, GPT
Astra solved 10 serious" and Miguel: "that should have never happened."

**LAW 47 — THE TAIL IS 0.2 s.** The master ends 0.20 s after the last spoken word
(`TAIL_HOLD` 0.20, `TAIL_PAD` 0.25; was 0.35 / 0.45 and the masters ran 0.30-0.36 s past
the last word). Miguel: "be quite aggressive with the cut after the last word, ideally 0.2 s,
because here you slightly see me turning off recording." Run 12's nine unaffected files were
trimmed in place to last word + 0.20 s (stream copy; priors in `_tail_prior/`).

**LAW 48 — THE OUTLINE IS JUDGED AGAINST ITS SIBLINGS.** hermeskanban's cutout passed the
protrusion and edge gates and Miguel still saw "a bit of chair on my left side and some
flicker compared to the rest". A matte whose silhouette edge jitters frame to frame more than
the batch's clean mattes, or that keeps dark plate pixels beside the head, is refused even if
the windowed protrusion scan is clean. The repair record for this file
(`shorts_run12/review/repair_hermeskanban_outline.md`) names the measurement that becomes
the check.

**GATE-SCALING NOTE (hermeskanban scene author, run 12).** Gate 1 measures canvas px and the
cutout scales the shared core by ~0.95, so a 16 core-px gutter arrives as 15.2 canvas px and
is refused on the cutout while passing on the split. Author gutters at >= 24 core px.

**TOOL FIX.** `phone_test_page.py` now honours the precedence its docstring stated (`--at`
> `--plan` > `--geom`); it used to concatenate them, which cut crops of empty board.

**LAW 48, the measurement (from the hermeskanban repair, 2026-09-03):** the headrest is a
WEDGE, not a column, so a rectangular wing cut leaves the part of it right of the cut
column welded to the shoulder, and the silhouette's extreme column then runs perfectly
straight for ~130 rows. Two instruments prep must add to the post-heal gate: (1) refuse any
run of >= 40 consecutive rows whose extreme silhouette column is identical (a human edge is
never a straight column); (2) measure retained dark plate pixels (luma <= 60) in a 50-column
band just outside the cut column, and refuse a p95 above the batch's clean mattes. Repair
chain that worked: a second wingfix pass on the first pass's alpha with a taller, wider window
(x 510, rows 300-464) and --chunk 40 keyframes, then re-track. Edge jitter at the shoulder rows
fell from 15 px p95 to 3, matching the accepted costpertask matte. Known limit, unfixed: ~1 s
of bright wall (luma 150-180, cheek-coloured) welded to the face at 18.2-18.8 s; only a
second SAM2 object for the chair (README known-limit 4) removes it.

**LAW 46, amended (run 13, 2026-09-03 23:09).** A repeated opening PREFIX is a restart only
when the earlier hit does NOT match the full opening key and the keeper (the hit that does)
begins within one word of it. A rhetorical repeat inside one sentence is the keeper itself:
viberesearch's "You've heard about vibe coding, but have you heard about vibe researching"
tripped the first version and lost its cut. A restart with no measurable silence before it
takes head = max(abandoned word end + 0.06, restart − head_lead).

## RUN-13 CLERK FINDINGS (2026-09-04 02:00) — two things the watcher never saw

**LAW 47, hard cap.** The tail is `last word end + 0.20 s`, enforced as a CAP in `cutlib.build_cut`
(`TAIL_PAD = TAIL_HOLD = 0.20`; `detection["tail_cap"]` records when the silence search wanted
more). Run-13 masters came out at 0.24-0.32 s before the cap: the silence search finds the room
tone floor, which is always later than the word. Delivered files that pre-date the cap are trimmed
by remux (`-t last_word_end+0.20 -c copy`), priors kept in `_tail_prior/`.

**THE PEN TAPS A BOX AT ITS TOP-LEFT CORNER, NEVER ITS CENTRE.** `box_emphasis()` used to park
the pencil at the box's centre for the pop. The centre of a big box is the finished ink the box is
framing: on hermesdesktop the pencil lay across the VISUALS row for 0.58 s (18.20-18.78 s) while
the border box popped around the whole window, and the watcher scored the file 0 candidates. The
chassis now taps `(x0 + BOX_RADIUS_U, y0)`, where a hand starts a rectangle, which in this
factory's centred layouts is blank margin. The general rule: a pen tap on a POPPED shape belongs
on the shape's own stroke, never inside it.

**PICTURE NAMES THE SAME PLATFORM AS THE SENTENCE.** viberesearch says "this guy on X" while the
source card is a screenshot of a LinkedIn post (the X post by @wojkuli carried that screenshot as
its photo; the plan recorded the chain and waived the second attribution on purpose). The clerk
held all three renders as `picture_contradicts_sentence`. Ruling pending Miguel: (a) show the X
post card itself, (b) add a small "via @wojkuli on X" chip, or (c) accept because the words the
viewer reads are the news itself. Until ruled, a plan whose sentence names a platform must show a
card OF that platform, or say so in the plan's disagreements.

**Watcher recall this run:** 0 of 2 real defects found by `gemini-3.5-flash-lite` (both clerk
own-eyes finds), 1 false positive (an `empty_zone` on a deliberate blank tile). The clerk's own
decode pass is what catches things; the post-render watcher is a cheap first filter, not a gate.

## RUN-13 REVIEW CHANGES (Miguel, 2026-09-04)

Five changes he approved on the run-13 debrief, after approving 9 of 12 renders
("visuals are fucking crisp"). Four are shape changes to the daily workflow; the
fifth is a picture rule. Nothing above this section is edited by them.

### 1. THE CLERK DOES NOT RE-WATCH THE FILE — "remove the pure duplication in the second watch"

`render_and_check.py` runs the Gemini watcher on **every staged file the instant it
lands** and writes `<run>/review/cands_<id>_<fmt>.json`. The clerk then ran the
**same script on the same bytes** — same model, same 720×1280 encode, same media
resolution, same prompt — into `clerk_cands_<id>_<fmt>.json`, at **$0.10–0.15 per
video**. That is one opinion billed twice, not a second opinion.

**The clerk now READS `cands_<id>_<fmt>.json` and adjudicates it**, rows *and* beat
logs, plus whatever its own frame decode raises. Everything else about the clerk
stands: fresh agent, cold decode, `<run>/plans/` forbidden, CONFIRMED /
ACCEPTED-BEHAVIOUR / REFUTED with a measured number on every verdict, any CONFIRMED
row holds the render.

* **The clerk's own decode is not optional and it is the half that works.** Run-13
  recall: the watcher found **0 of 2** real defects, the clerk's own eyes found
  **both**, and the watcher raised 1 false positive. The watcher is a cheap filter
  over a file nobody has looked at yet.
* **A missing `cands` file is reported, never backfilled.** That render was watched
  by nothing; say so and rule on your own decode. Running the watcher to fill the
  hole is the duplication coming back through the side door.
* A fresh watch is legitimate on a render **no driver ever watched** (a hand-render,
  a repair staged outside `render_and_check`) — that is the first watch, not a
  second one.

Procedure text: `pipeline/semantic_review.md` **v3.1**.

### 2. THE PHONE TEST IS COLD, AND IT HAPPENS BEFORE THE RENDER — "run the phone test before, you are right"

`phone_test_page.py` already cut the four crops off the **page** before rendering
(2026-09-03) — but **only the builder looked at them**, and a builder cannot un-know
its own plan. That is exactly how the illegible moon shipped.

So the order gains one step, and it is the workflow that enforces it:

```
build  ->  prerender_check + phone_test_page  ->  COLD PHONE NAMER  ->  score vs the
           (build-green, no render)                (a fresh agent)      sealed key
                                                                            |
                                        PASS -> render_and_check -> staged  |
                                        FAIL -> redesign + re-cut, at most 2 rounds
                                                then render anyway and FLAG it
```

* **The namer gets ONLY the crop images.** Never the plan, the page, the project,
  the sheet, the manifest, the transcript or the sealed key. The author **copies**
  the crops to `<run>/review/cold/<md5(label)[:8]>/NN.png` first, keeping the index,
  so not even the file path names the video. `NN` is the key's object index.
* **Five words, not three.** The namer is judging a page screenshot to save a
  render, not ruling on a delivered file: a name that is the intended thing or an
  obvious synonym PASSES; a different thing, a hedge, or "cannot tell" FAILS. The
  clerk's post-render Phone Test stays at **three words** and stays binding.
* **SCORE THE IDEA, NOT THE NOUN (Miguel, 2026-09-06, run 16 plantsite).** The
  reader names what it sees in plain words; the author's score asks ONE question:
  would a stranger who said that get the picture the plan wants? "flower" for a
  browser window with a plant drawn in it is a PASS: flower and plant are the same
  visual idea, and the reader named the content of the container it saw. So are
  "document with bar chart" for a report, "browser window" for an app window,
  "laptop" for an open laptop. A FAIL is a DIFFERENT thing ("clipboard" for a
  report, "receipt" for a calendar), a hedge, or "cannot tell". Four readers
  said "flower" to the plant page and the author redesigned it three times and
  then stalled all three lanes: that was the score being literal, not the drawing
  being unreadable. Never fail an object for omitting its container word or for
  a sibling noun of the same thing.
* **OVER SEVERAL ROUNDS THE NOUN IS THE MEASUREMENT AND THE FLAG IS A SAMPLE
  (run 17, pcoverheat, 2026-09-08).** "a hedge or cannot tell FAILS" above is the
  ONE-SAMPLE rule and it still binds a single round. The moment you submit several
  independent rounds, `production.py::consensus` rules on the set, and the line it
  rules on is *how many readers reached the object*, not *how many felt sure*:
  * a SECOND reader naming a different thing fails it whatever the flags say;
  * at least half the reads must be `intended` or `synonym`;
  * and at least ONE reader must have been `sure` of a name that reached it, in
    five words or fewer — unanimity among readers who were all guessing is not a
    measurement, and a confidently WRONG reader is not evidence of legibility.

  What this cost: pcoverheat's download arrow — an arrow onto a bar — was named
  "download arrow" / "download arrow icon" / "download icon (arrow over line)" by
  **six of six** independent readers, zero different, and the old half-must-be-sure
  line refused it at `sure` 2 of 6. The identical drawing had SEALED at the artwork
  seat hours earlier on `sure` 3 of 6. Nothing about the ink changed between the two
  seats; the coin landed the other way four times, and the cutout lane returned
  `no staged path`. **Score the set, not the flag, and never redraw an object every
  reader already named.**
* **A READER THAT DECLINES THE PROMPT IS NOT A HEDGE.** pcoverheat's process list
  is a table headed PROCESSES with HOT / RAM / CPU columns; three readers answered
  `none — UI table, not object` and then named the panel anyway. That is the reader
  refusing "name the single everyday OBJECT" about a UI panel, which the graphic
  chart draws on purpose — the same class of error as ruling a jaw a headrest wing.
  Score the noun it gave. Its answer overran the five-word cap, so it can never be
  the `sure` read that carries the object, and it no longer refuses the whole round
  (it used to throw away every clean read of every other object in the same file).
* **A fail is a REDESIGN, not a label.** Bigger, simpler, or given the one feature
  that says what it is. Then `prerender_check` and `phone_test_page` run again, the
  crops are copied to a **fresh** cold folder, and a **different** namer looks — a
  namer that has already seen the object is not cold about it any more.
* **At most 2 redesign rounds.** Then the file renders anyway and the author writes
  `<run>/review/phone_flag_<id>_<fmt>.md` naming the objects, the intended names and
  the namer's answers. It ships with a KNOWN cold-read failure and the clerk is told
  so — after the clerk has written its own answers, never before.
* The economics: a failure caught here costs a rebuild. The same failure caught
  after the render costs a Modal render, a `qc_pass` decode, a watcher call and a
  clerk (run-13 `dgxspark` tank: **31 min and $0.18** for round 1 alone).

### 3. ONLY THE CUTOUT WAITS FOR THE SILHOUETTE — "we can make the split screen and whiteboard stop waiting for the cutout"

Prep's stages are not equally useful to the three formats. **The cut (~70 s) is
everything the plan, the split and the whiteboard need. The plate sweep, prompt0,
the track and the ship (~10 of prep's ~11 minutes) serve the CUTOUT alone.** Until
now every lane waited for the whole batch to close.

* **`prep_batch.py` stamps a per-recording, per-stage marker** the instant that
  stage lands: `<run>/prep/stages/<id>.<stage>.json` = `{id, stage, status, wall_s,
  at, keys{...}}`, written in `Stage.__exit__` (`mark_stage()`, 2026-09-04). The
  package json and `_batch.json` are unchanged and still authoritative — the marker
  is what you can read while the batch is still running. A marker that fails to
  write is swallowed: **a marker is never a gate.**
* **prep is LAUNCHED, not awaited.** A recording's chain starts at **its own** cut
  marker. A reporter reads `_batch.json` when the batch closes, in parallel with the
  waves.
* **Three lanes per recording, not two authors.** SPLIT (YouTube) and WHITEBOARD
  (Reels) start off the plan; CUTOUT (TikTok) starts when that recording's **ship**
  marker passes. The plan agent starts at the cut and does not wait for the cue
  stage either — it runs `pointing_cues.py` itself.
* **The shared scene survives as an artefact, because it is now shared across
  agents.** The split author writes `<run>/plans/<id>_scene_handoff.md` — the scene
  module's path, its entry points, its units, its asset keys, what to change to seat
  it in the stage zone. The cutout author reads it; if it is not on disk yet it
  builds from the plan and says so. **The plan is the contract; the file is the
  convenience.**
* The wing review moves with prompt0, so it belongs to the **cutout** author, not
  the plan agent.

### 4. AN OPEN DOUBT STOPS AND ASKS (the plan's two lists are not the same list)

`open_questions` are things an author can build around. **`open_doubts` are doubts
that change WHAT THE VIEWER SEES** — which card, which platform, which picture,
which claim. A plan carrying an `open_doubts` entry with
`changes_what_viewer_sees: true` **stops that recording**: the workflow logs it,
skips every builder for that video, and returns it as **"needs Miguel"** with the
question, the options and the plan's lean. One line, answered once, instead of a
guess discovered by three clerks.

Both directions are abuse: parking a real doubt in `open_questions` to keep the line
moving, and inventing a doubt you could have decided yourself.

### 5. THE CARD IS THE POST YOU SAW — and the cutout's logos are topical

**PLATFORM.** *Miguel: "all my info come from X, and that precise X post had a
LinkedIn post image."* When the sentence names a platform — "this guy on X",
"someone on LinkedIn" — the source card **shows that platform's post**: that frame,
that handle, and whatever the post carried inside. If the thing the viewer must READ
is a screenshot the post carried, **show the named platform's post first and then
zoom into the screenshot inside it.** Never show only the inner screenshot under a
sentence that names the wrapper — run 13 held all three `viberesearch` renders for
exactly that. A card the plan cannot build is an **open doubt** (change 4), not a
silent waiver. The plan records the platform per cue: `pointing_cues[].platform` is
the frame the card wears, `pointing_cues[].inner` is what it carried.

**THE PHONE TEST INFORMS, IT DOES NOT VETO (Miguel, 2026-09-08).** In three days this one gate
refused five lanes and caught zero defects that the rest of the chain would have missed. Its
arithmetic was calibrated as though a false PASS were catastrophic and a false FAIL free, when the
reverse is true: a false fail costs a whole video before a single frame exists, and a false pass has
three gates behind it (the clerk's own Phone Test on the delivered file, the watcher, and Miguel's
eyes). So the gate now blocks on exactly two findings, both of which mean the drawing is lying or
absent:

  * **IT MISLEADS** - two or more independent readers name a DIFFERENT object (kimiwork's app window,
    `Refrigerator` twice). That is the drawing.
  * **IT IS ILLEGIBLE** - fewer than half the readers reach the intended object at all.

Everything else PASSES and is ROUTED. A reader who names the intended thing and hedges has named the
intended thing; `hedged` is recorded on the object and the clerk must adjudicate it on the DELIVERED
render, where it moves, carries its label and lands on the word being spoken. That is the view the
viewer gets and the only one that can settle a hedge. Confidence orders the fix list; it never
creates a refusal. And the question must fit the object: only a `metaphor` object owes an answer to
"name the everyday object". A `ui` object is asked what software it looks like; `furniture`
(connectors, bars, arrows, brackets) has a role, not a name, and is never dispatched. A crop that
already has a verdict this run is refused by the dispatcher, not by a sentence in a brief.

**AN UNCERTAIN GATE RENDERS, IT DOES NOT HOLD.** A render is about two cents and produces something
Miguel can judge; a held lane is an hour and produces nothing. Run 18 ended 3 videos, 0 files, 0
things to look at. When the artwork gate is uncertain rather than certain-bad, the lane renders with
`review/artwork_flag_<id>.md` naming the object and what the readers said.

**A SCREEN IS NOT AN OBJECT (run 18, 2026-09-08).** Three of three videos in run 18 were held by
the same class of drawing: `hermesdoctor`'s terminal window ("no object; text label image"),
`saascut`'s app window ("credit card", then "browser window" unsure) and `grokstripe`'s automation
card ("no everyday object; logo card"). A rounded rectangle carrying rows of type reads as a picture
of text, not as a thing, however well it is drawn, and the Phone Test is right to refuse it. A
bespoke object owes a SILHOUETTE a stranger can name with the type removed. So: at PLAN time, do not
declare a window, card, panel or screen as a bespoke object. Either give it an unmistakable
real-world shape (a doctor's bag, a receipt, a door), or let it be UI, which is chrome the plan
declares as such and the Phone Test does not judge. This is a plan-level rule; an artwork author
cannot draw its way out of it.

**A FAILING DRAWING NEEDS A NEW DRAWING, NOT A SECOND OPINION (run 18, 2026-09-08).**
The three-round seal makes a PASS trustworthy; it says nothing about a MISS. Run 18's `saascut`
author ran three independent rounds on byte-identical crops and collected the same verdict three
times — app window read "credit card", unsure — while the drawing never changed, then spent three
more rounds confirming two alternates that already read. Six rounds, zero design changes. So: after
ANY cold round, split the set. What reads is SEALED and never re-read; what misses is REDRAWN, and
only the new crop goes to a fresh round. Alternates are the remedy after two failures on one object,
never a first move.

**GO CLOSER ON THE INNER READ (Miguel, run 17, 2026-09-08).** He approved the
`pcoverheat` split's card sequence by name — the X post, the highlight on the claim,
then the move to the line where the tool names the culprit — and asked for ONE thing:
*"maybe a bit more zoom would have been nice."* When the plan zooms from a source card
into the text the viewer must actually read, the target line ends at a scale where it
is comfortable on a phone, not merely legible: aim for the read line at **>= 42 design
px cap height** in the held frame, and let the card's chrome leave the frame if that is
what the scale costs. The wrapper still comes first; the zoom is what pays it off.

**LOGO LANES.** *Miguel, run-13 review: "it would be cool if the logos behind me in
cutout are relevant to the video."* The cutout's background logo lanes carry the
marks **this short names**, or their obvious neighbours in the same category —
`plan.cutout_logo_lanes`. A generic house set behind him is a rejection, on the same
principle as the topical cast: the wall is scenery, and scenery that argues nothing
is a dead zone with a logo in it.

## LAW 48, BUILT (2026-09-04) — the two instruments are a GATE now, and it caught reasoninglevel

Miguel, reviewing run 13: *"reasoning level cutout has a problem, the chair next to my head
(left side of the screen) is present as my outline. only this one will need redoing. we should
add a self-improving loop to that outline."*

`pipeline/sam2/outline.py`, wired as `ship.outline_gate` between the protrusion gate and the
encode, on the ALPHA, in both ship lanes. LAW 48's two instruments, with the numbers the whole
run-12/13 corpus gave them:

| instrument | approved corpus | rejected / repaired | ceiling |
|---|---|---|---|
| longest identical-column run (±1 px), p95 over frames | 33 - 50 rows | 59 - 132 rows | **60 rows** |
| share of frames carrying a >= 40-row run | 0.018 - 0.264 | 0.466 - 0.993 | **0.40** |
| retained plate-dark (luma <= 60), 50 columns inward from the edge, p95 as a share of the band | 0.14 - 0.62 | 0.99 - 1.00 | **0.78** |

**THE BAND IS THE LAW.** Both instruments run ONLY in the 180 rows ending at the shoulder
arrival (where silhouette width reaches 1.35x the head's) — jaw, neck, shoulder-top. Above it
is his black CAP, whose side is a genuinely straight edge for 40-107 rows on mattes he
approved; below it is his black T-SHIRT. Measured over the whole body neither instrument
separates a rejected matte from an approved one at all: the straight run reads p95 42-75
approved against 46-132 rejected, and the dark count reads 29,000-40,000 px on every matte in
the corpus because it is counting his own clothes. Windowed, nine of nine verdicts are correct.
The band is safe to derive because the plate solve freezes the geometry — crown row 13-28, head
width 323-334 px, shoulder arrival row 466-499, across nine tracked alphas.

**BOTH INSTRUMENTS ARE NEEDED.** hermeskanban v2, the file he rejected in run 12, is caught by
the straight-edge test alone (132 rows) and PASSES the dark test, because its surviving wedge
is a sliver. hermesdesktop v1 and dgxspark v1 are caught far more loudly by the dark test.
reasoninglevel v1 fails both.

**THE SELF-IMPROVING LOOP.** An outline refusal is `prep_batch`'s third repairable gate. It
runs `wingfix` on the refusing side with the window the gate MEASURED: the band's rows with the
top lifted 20 and **the bottom left exactly at the shoulder arrival** (there is no bottom
margin on purpose — wingfix cuts every pixel darker than its guard and his shirt is black), a
cut column taken from the deepest inward column of retained dark plate plus 10 px, and
`--chunk 40` so a corrective keyframe lands every <= 10 frames. Round 2 re-measures round 1's
alpha and cuts again, which is the two-window chain the hermeskanban repair had to be driven by
hand. The gate reproduces that human window independently: on hermeskanban's refused alpha it
measures cut column **509** over rows 279-499, against the **510** over rows 300-464 a human
read off `wingfix --measure` and shipped.

**FIRST LIVE RUN.** reasoninglevel refused in **1.7 s**, before any encode; one round; wingfix
`--wing-left 577 --rows-left 288,488 --chunk 40` (80 keyframes, median 14,159 px cut, max
removed luma 60 against a guard of 60, silhouette lost 2.2-3.1 %); re-track H100 128.5 s
**$0.1523**; re-ship 64 s; PASS. Left side: straight p95 87 -> **42** rows, at-line 99.4 % ->
**9.2 %**, dark p95 9,048 px (100 % of the band) -> **1,388 px (15 %)**. The left edge moved
off the frozen chair column onto his body (row 360: column 472 -> 540) and started moving like
a human edge (row 360 jitter p95 1 px -> 3 px, against costpertask's accepted 4 px).

**THE KNOWN LIMIT, AND IT IS MIGUEL'S OWN RULING.** The law says p95, so p95 refuses, and a
sub-second burst is invisible to it. hermesdesktop v2's right side maxes at **8,873 px (0.98 of
the band) on ONE frame at 1.4 s** — the chair splash at the start of that take Miguel saw and
told us not to redo. Every other approved matte's max is <= 5,671, so a max test at ~7,000
would catch it and pass everything else. It is NOT built, because it would refuse a file its
owner accepted. `dark_frac_max` is recorded in the `law48` block and never gated.

## LAW 49 — THE FIRST AND LAST FRAMES ARE THEIR OWN, NEVER A NEIGHBOUR'S (2026-09-04)

A BINARY MEDIAN WITH A DUPLICATED VOTE IS THAT VOTE. `ship.render`'s temporal median pads at
both ends, and the two padding modes duplicate DIFFERENT frames: `replicate`'s window at output
0 is `[f0, f0, f1]` and resolves to f0; **`mirror`'s is `[f1, f0, f1]` and resolves to f1.** So
from 2026-08-31, when mirror became the default, the opening frame of every matte carried
**frame ONE's silhouette over frame ZERO's picture**, and the tail frame carried the
second-to-last's. Measured on the alphas: dgxspark alpha_v2 frame 0 **7,195 px**, viberesearch
2,140, reasoninglevel 1,340, hermeskanban 705 — and on dgxspark those pixels are background
revealed inside a hand moving ~100 px in that frame, on a track SAM2 had got RIGHT. The
0.483-against-0.794 edge-curvature measurement that bought mirror its default was never
measuring a smoothed frame 0. It was measuring frame 1.

The fix is independent of `pad`: an end frame takes its own centre frame and skips the median
(what a replicate window resolves to anyway, for any window size), and `windows()` carries one
frame of lookahead so the LAST output frame can be named in a streaming pass. Only two frames
of a take change; both `workers` paths carry the flag so the md5 parity between workers 1 and
12 is unchanged. The ship json records `end_frame_check`: `revealed_px` (0 by construction,
recorded anyway) plus `median_would_add_px` / `median_would_lose_px`, the defect that used to
ship.

---

## THE CHAIR IS A SECOND OBJECT (Miguel, 2026-09-04)

Miguel, on the shipped `reasoninglevel` cutout: *"my left shoulder is chopped on a straight
vertical line, and at the end a piece of the headrest arm sits by my left ear."*  Then, after
seeing the fix: *"sure make it the main pass."*  This is that pass.

**THE LAW.  The cutout's cleaning pass tracks the chair as its own SAM2 object and subtracts it,
per frame, from him.  A rectangle is no longer the remedy; it is the fallback.**

For thirteen runs the matte had ONE positive prompt and no way to say *that black thing beside
the black cap is not him*, so every repair had to be a RECTANGLE (`wingfix`) carved out of a
wedge that slants a column per 3.3 rows.  A window wide enough at the bottom amputates the
shoulder; one that clears the cap leaves the arm by the ear.  Both symptoms, one cause.  SAM2 is
a MULTI-OBJECT video segmenter and the factory was using one object.

The standard pass, in order:

1. `prompt0` runs, then `chairprompt.chair_prompt` looks for a headrest wing beside the head on
   frame 0, **on both sides**.  The signal is a dark run with BRIGHT ON BOTH SIDES — wall,
   headrest, skin — because nothing else in the frame has that sandwich; the candidates are
   labelled as connected regions and the outermost region 80+ rows tall and under 150 px wide is
   the wing.  Out comes a box, four positive clicks down its spine and four negatives (his cap,
   his cheek at the interface, his shoulder inboard of the wing, his chest).  It lands in the
   prep record as `prompt0.chair_prompt` with a proof overlay in the session.
2. The track gets it as `exclude=`.  Left becomes object 2, right object 3, both prompted on the
   DISCARDED warm-lap copy of frame 0 (the STANDING RULE holds for every object), both
   propagated in the same loop, and the emitted alpha is `obj1 AND NOT (union of them)`.
3. Each exclusion mask is grown **2 px flat** so no fringe survives, then **8 px more into DARK
   PIXELS ONLY** (`luma < 60`, `wingfix`'s own guard) by geodesic dilation — a bright pixel stops
   the flood, so the extra reach can never eat skin.  The flood is FENCED to
   `crown + 180 .. shoulder arrival - 48`, derived per session from the frame-0 silhouette by
   `outline.py`'s band math, because the two black things that are HIS and touch the chair are
   his cap above and his t-shirt below.  Unfenced, 333 of the 375 px/frame a reach of 6 removes
   are his shirt.
4. **A miss is a legitimate answer.**  No wing found on a side means no exclusion object for that
   side, i.e. the old single-object pass, byte-identical.  `--no-chair-object` forces it, and
   `no_chair_object: true` on an intake row does it per recording.
5. **`wingfix` IS STILL THERE, AS THE FALLBACK.**  If LAW 48 still refuses after the two-object
   track, the auto-repair runs exactly as before — and its re-track keeps the chair object.

What it bought, measured on `reasoninglevel` (chair residue `x 440..570 / y 190..450`, and the
LAW 48 gate):

| | residue median / p95 / max | frames > 1,000 px | LAW 48 left p95 / at-line | rounds |
|---|---|---|---|---|
| v1, rejected by Miguel | 12,339 / 15,764 / 16,895 | 383/383 | 87 / 99.4 % REFUSED | — |
| v2, the `wingfix` repair | 723 / 1,964 / 3,383 | 81/383 | 42 / 9.2 % | 1 repair, 2 tracks |
| **the standard pass** | **487 / 925 / 1,051** | **5/383** | **37.8 / 4.6 %** | **0, round 0** |

Edge jitter on the rows the wingfix amputated collapses — row 480 from 15.58 px mean / p95 75 /
28.1 % of frames moving >= 5 px to 0.78 / p95 1 / 0.9 %, row 460 from 4.98 / 27.0 / 14.5 % to
0.98 / 2.0 / 0.7 %, both then BETTER than `costpertask`, the matte Miguel accepted.  Cap rows and
the whole right side are unchanged to the pixel.  And it is CHEAPER than the repair it replaces:
two objects track at 117 ms/frame against 157.6 for the one-object wingfix re-track, $0.116
against $0.152, one GPU run instead of two.

**The remainder is his cap, and it stays.**  About 16 px/frame of dark survive at the ear-top on
`reasoninglevel` because a bright sliver of wall separates the chair from his cap there and the
flood correctly stops.  Pushing the reach to 16 px does clear it and takes a 383 px bite out of
his cap at 1 s.  8 px is the last value that takes the strip and leaves the cap.

## COST LEDGER (Miguel, 2026-09-04)

**"By the end of the video I want to know modal cost per video plus per total
run as well as gemini costs. Every paid service I want to quantify."**

Every paid call in this factory now books itself into `<run>/costs.jsonl` at the
moment its price is measured, and `pipeline/cost_report.py` adds them up into
`<run>/review/COSTS.md` + `costs.json`. Nothing is re-priced: each row's `usd`
is the number the code that made the call already computed — `sam2/track.py`'s
`cost()`, `render/modal_render.py`'s `price()`, each Gemini watcher's own token
arithmetic, `qc_v3`'s own arithmetic. The ONE price the ledger owns is ElevenLabs
Scribe, because the API returns a duration and no cost.

**A cost that has to be re-added by hand is a cost that gets reported wrong.**
Run 13's table was assembled out of six artefact families and came out at ~$2.7;
the artefacts say **$4.33** (backfilled, `shorts_run13/costs.jsonl`). The missing
money was not exotic: renders and watchers whose `.priorN` fix rounds nobody
re-added ($0.23), a re-track that happened after the bench note was written
($0.15), Scribe passes that no script had ever priced ($0.08), and the chair
job's eleven GPU containers ($1.16). Run 12 backfills to **$3.27**.

### The row, and why a re-run cannot double count

`record(run, service, stage, usd, video=, fmt=, units=, note=, ref=)` appends one
JSON line. `service` is `modal | gemini | elevenlabs | other`; `stage` is
`scribe | sweep | track | ship | draft | render | watch | gate3 | verify |
clerk_watch`. The **key** is `service|stage|video|fmt|ref`, and a record whose key
exists REPLACES that line. For that to work the `ref` must name ONE PAID CALL,
not one file, so every call site writes

    <path relative to the run>@<the call's own measured identity>

— the Modal container's `t_import_epoch` or `container` id, the render's epoch for
the watcher that watched it, the audio duration for a Scribe pass. A second fix
round is a second container, hence a second row; re-reading a report is the same
container, hence a replacement. Run resolution: the explicit `run`, then
`$SHORTS_RUN`, then walking up from the `ref`.

### Where each call books itself

| call | file:function |
|---|---|
| BiRefNet master sweep | `prep_batch.ledger_sweep` (from the package), `birefnet_master_sweep.main` (hand-run) |
| SAM2 track | `prep_batch.collect_tracks`, `prep_batch.repair_round`, `sam2/track.py:main` (hand-run, `--run`) |
| matte ship | `prep_batch.collect_remote_ship`, `sam2/track.py:main` |
| ElevenLabs Scribe | `prep_batch.prep_front` (cut stage), `prep/cutlib.tight_transcript` (hand-run) |
| Modal render | `render/render_and_check.one_job` |
| post-render watcher | `clerk_video_gemini.main` (books itself — same call whether a driver or a hand-run made it) |
| clerk re-watch | `clerk_video_gemini.main`, stage `clerk_watch` from the `clerk_` out name |
| flag verification | `verify_flags_gemini.main` |
| Gate 3 | `qc/qc_pass.py` main, parsed off `qc_v3`'s own stdout and stored as `gate3_cost_usd` |
| intake Scribe | the prep-launcher brief in `.claude/workflows/daily-shorts.js` (one `costs.py add` line per recording) |

`render_and_check --stage` runs the report after its last render, so the number
exists **by the end of the video** without anyone asking, and the daily workflow
returns the run total. `costs_backfill.py --run <run>` reconstructs a pre-ledger
run from its artefacts. A ledger failure can never fail a stage: every call site
uses `costs.safe_record`, which swallows and prints.

### The one unmeasured price

ElevenLabs Scribe is booked as an **estimate** at `$0.40` per audio-hour
(`costs.SCRIBE_USD_PER_AUDIO_HOUR`, override `$SCRIBE_USD_PER_AUDIO_HOUR`), and
every row it writes says so in its note. It is ~2 % of a run, and it is the only
number in `COSTS.md` that is not measured. Replace the rate with the live plan's
own figure when someone reads it off the ElevenLabs usage page.

---

## INNER STUMBLES STAY (Miguel, 2026-09-04)

**THE LAW.  A discard marker AFTER the keeper opening is a MID-SENTENCE STUMBLE and it stays in
the video.  Only a marker BEFORE the keeper is a false start.**

`game33c`/run 14 is the case.  Its markers sit at w2, w62, w85 and w124; the keeper opening is
w86.  Reading `markers[-1]` the marker rule answered w125 and the cut REFUSED —
*"a discard marker sits inside the chosen take"* — on a take that is perfectly good:

    [86] You can now create your own 3D game for only 33 cents ...
    [120] Now, of course, for [124] thrir-- [125] 33 cents, you're not getting ...

"for thrir-- 33 cents" is him fumbling the word and immediately saying it right.  That is how he
talks, it is inside the keeper, and cutting the take because of it is the bug.

**The old reading did not just refuse a good take; it threw away its own corroboration.**  The
marker rule's claim has only ever been about the last false start, so it must read the last marker
BEFORE the keeper — w85, which answers w86.  That is EQUALITY with the content rule, the strongest
witness the family has.  So the same change that keeps the stumble also makes the cut
self-corroborating: `game33c` no longer needs `allow_uncorroborated` at all.

Every inner stumble is RECORDED, not silently kept: `cuts/<id>/edl.json` carries an
`inner_markers` list with each one's word index, text, start, end and a nine-word context window,
and the cut prints them.  A clerk or Miguel can find every take that carries one and decide
whether it should have been re-filmed — the decision is theirs, not the cut's.

---

## SELF-HEAL FROM THE GATE'S OWN WINDOW (2026-09-04)

Miguel: *"every time you encounter bugs like this fix them; the idea is to have a self-healing
loop."*

**THE LAW.  When a gate refuses on a side that has no exclusion object, the repair loop tries a
CHAIR OBJECT derived from the gate's own refusal window BEFORE it reaches for a rectangle.  And it
is allowed to answer "this is not my kind of problem".**

Both gates already hand back the window they are complaining about — `outline` reports the band
rows and a `wing_column`, `protrusion` reports the wing's own columns — so a refusal is a SEED for
an exclusion prompt, not a mystery.  `chairprompt.from_refusal()` turns that window into a box,
four positive clicks down its dark spine and the four standard negatives;
`prep_batch.chair_from_gate()` merges it into the session's `chair_prompt.json` and the re-track
picks it up.  A chair-object fix reuses the previous round's prompts, because it changes
`exclude=`, not the frame-0 mask.

Proven on run 14 the day it was built: `trycrm` and `game33c` both refused the protrusion gate on
the RIGHT — the side the detector is blind to, because his hair touches the wing — both had a real
wedge there, and both derived a prompt from the gate's numbers and passed after ONE round with no
cut and no human.

**THE GUARD IS THE LAW, NOT THE FEATURE.**  The window is used verbatim and the region is never
grown into its connected component: at those rows every dark thing is connected, and growing it
ran through his beard, neck and shirt (`grokbuild` 291 px, `trycrm` 349).  A window wider than
150 px is called **"not a wing"** and NO prompt is produced, because a false chair object carves
his face.  A rejection is a finding, and it names the remedy: a reasoned `--allow-outline`, never
another cut.

---

## OPEN CALIBRATION QUESTION — LAW 48's straight run and a LEAN (2026-09-04)

**`grokbuild` (run 14) refused LAW 48 on the right at straight p95 61 against the 60-row ceiling,
and the straight run is HIS OWN JAW-TO-SHOULDER LINE, not furniture.**

The evidence, all measured: the refusal window is cut column 494 with the silhouette edge at 768,
a 275 px "wedge"; on frame 0 the dark inside the mask there is his beard, lips, jaw and neck, with
the chair correctly EXCLUDED just outside the edge, and cut column 494 sits in his chin.  He is
leaning, so his jaw runs into his shoulder almost vertically for 61-79 rows.  Only `straight_p95`
fails — at-line 29.3 % against a 40 % ceiling and dark 59.3 % against 78 % are both well inside.
The two `wingfix` rounds that ran before it was caught punched **7,719 and 8,174 px per frame of
holes in his dark neck** while moving the right edge 0-10 px, so the carved tracks are damaged and
the uncarved one is the correct matte; it shipped under `--allow-outline` with that measurement as
its reason.

`straight_p95_max = 60` was calibrated on nine alphas of Miguel sitting UPRIGHT.  **Whether it
should widen, or gain a lean-aware term, is Miguel's decision — it was NOT changed to make one
video pass.**

## GATE 3 IS ADVISORY (2026-09-05, from Miguel's self-healing rule)

Gemini describe-mode inside `qc_pass` no longer fails a render on its own. Four files in two
days were blocked by claims that measured false on the pixels: hermeskanban's "unidentifiable
icon" (unchanged, Miguel-approved art), moleculezoom's "card held > 4 s" (2.32 s), dgxspark's
"pen at full size" on an empty frame, and grokbuild's caption mismatch "at 30.0 s" in a 27.9 s
video. Its `describe_errors` stay on the qc record under `verdicts.gate3_gemini_describe =
REPORTED` plus an `advisory` note, and the independent clerk adjudicates every one against the
frames, as it already does for the watcher. Nothing else in the 13 checks changed.

## THE RUN NEVER QUITS (2026-09-05)

Run 14 did not fail on craft. It failed twice on **giving up**, and both failures are now
structurally impossible in `.claude/workflows/daily-shorts.js` (the Workspace one, not $HOME).

**1. A NON-OK MARKER IS NOT A VERDICT.** The ship gate read `trycrm.ship.json` status `"error"` —
a crash on the LAST LINE of `track.py`, *after* a successful paid track with every artifact on
disk — and `grokbuild.ship.json` `"REFUSED"`, reported STOP, and the cutout lane ended for good.
Twenty minutes later a repair agent fixed both mattes and rewrote both markers to `"ok"`, and
nothing was watching. `game33c` lost its plan AND all three lanes the same way, on a cut refusal
that was a rule bug. So the cut gate and the ship gate now treat `error` and `REFUSED` as **not
final**: they keep watching for the marker to be REWRITTEN (prep's own auto-repair re-stamps it in
place on every round), they accept a `<run>/prep/stages/<id>.<stage>.override.json` written by a
repair agent, and they poll three times with a wait between. **Only `SKIPPED_NEEDS_KEY`,
`not_a_short`, and a marker still non-ok at timeout are final.**

**2. A LANE THAT ENDS NON-OK GETS ONE REPAIR ROUND, NOT AN OBITUARY.** When a gate or a lane is
still non-ok, the workflow spawns a REPAIR agent (opus) modelled on the prep-fix work of
2026-09-04: root-cause on the artefacts, fix at the source in the pipeline with a regression check,
re-run **only that recording's failed stages** through a one-row intake plus `--skip`, and rewrite
the marker (a prep re-stamp, or a signed override). Then the gate and the lane run again. **One
repair round per recording per run**; after that the recording is `needs_miguel` and the run
carries on around it. Every non-ok lane is listed in the run's result under `needs_repair` with the
marker error verbatim.

**3. THE USAGE CAP IS A WAIT, NOT AN END.** Two runs in a row died with `staged 2/9` when agents
started coming back as API 429 "session limit · resets HH:MM", and both were resumed by hand hours
later. Every `agent()` call now goes through one wrapper. A null return is probed (see 4); a cap —
detected by the error text, or by the probe itself being unable to run — is logged as
`USAGE CAP at <label>; waiting` and the SAME call is retried after a sleeper agent (`sleep 570` in
Bash, ~10 min a tick, 6 ticks in the first hour and up to 6 h in total). **A cap never spends a
retry and never ends a lane.** Any other failure is retried twice, then recorded in
`agent_failures` and the run continues.

**4. EVERY BRIEF LEAVES A TRACE, SO A RESUME IS FREE.** `agent()` returns *null* on a terminal API
error — no reason, no distinction between an agent that was killed and one that finished and lost
its return. So every brief in the workflow now ends with two sentinels: **FIRST ACTION** write
`<run>/review/agent_started_<label>.txt`, **LAST ACTION** write `<run>/review/agent_done_<label>.json`
(copied to `state_<label>.json`) with exactly the return. And every brief **reads its own done file
first**: if it exists, the agent returns it verbatim and does no work. That single rule buys three
things — a probe can tell "died" from "finished", a retry of a finished agent is free, and
`Workflow({scriptPath, resumeFromRunId})` after a cap continues from where it died **with no hand
reconciliation**.

**5. THE CLERK JUDGES WHAT STAGED.** A lane that failed no longer costs a video its audit: the
clerk runs on whatever is on disk and says how many renders it judged. The run's result carries,
per recording, the staged formats, the missing formats **with their reason**, and the clerk verdict.

**6. DELIVER IS A PHASE, AND IT CANNOT FAIL THE RUN.** `costs:report` (Bash-only, low effort) and
the Drive push run at the end under `Deliver`. The push goes only to recordings whose clerk returned
PASS (`push_run_to_drive.py --ids …`); a HOLD stays out of Miguel's Drive folder.

**HOW IT IS PROVEN.** `pipeline/workflow_dryrun.mjs` loads the real workflow file with stubbed
`agent()/pipeline()/parallel()/log()/phase()` and drives five scenarios: a marker that goes
error → ok on the 3rd poll, an agent returning null twice then a value, a usage-cap error text, a
resume where the done-files exist, and a marker that stays non-ok until a repair agent fixes it.
Run it after ANY edit to `daily-shorts.js`: `node pipeline/workflow_dryrun.mjs`.
## AUDIT FIXES A1/A4/A5 + FLICKER (2026-09-05)

**A1, anatomy is a veto.** `chairprompt.from_refusal()` now distinguishes an over-wide body window as `outcome: "verified anatomy"`, and `prep_batch` treats every `verdict: "not a wing"` as a hard stop before `wingfix` in both protrusion and outline branches. A verified-anatomy outline refusal may ship the unchanged alpha under a recorded `--allow-outline` only when straight-run p95 is the sole refusing instrument and both at-line persistence and retained-dark remain inside their ceilings. A protrusion refusal, a mixed refusal, a missing ceiling, or any second failing instrument becomes `needs_miguel`. The grokbuild replay uses its real 275 px window and asserts zero carve calls, zero re-track cost, unchanged tag `v1`, and the measured reason: p95 61 against 60, at-line 29.3% inside 45%, dark 59.4% inside 78%.

**A4, the straight-run scan now considers every start.** The old greedy jump returned 36 rows for `[100] + [101] x 35 + [102] x 35` at tolerance 1 even though the legal suffix is 70 rows. `_longest_flat()` now uses a monotonic sliding window and returns `(70, 1)`. The corrected counter raised clean-corpus persistence, so the persistence ceiling was re-calibrated from 40% to 45%; 40% would falsely reject the approved hermeskanban v4 at 41.43%. The nine-alpha run-12/13 corpus was measured before and after: costpertask v1, dgxspark v2, hermesdesktop v2, hermeskanban v4 and viberesearch v1 stayed `clean`; reasoninglevel v1, hermeskanban v2, hermesdesktop v1 and dgxspark v1 stayed `outline`; verdict flips: **zero**. The retained-dark numbers did not change.

**A5, missing evidence cannot become clean.** `outline.scan()` now records alpha and plate frame counts, refuses mismatched spatial or temporal stacks, and returns `unmeasurable` when either side has zero valid LAW 48 measurements. `ship.py` turns that into the non-repairable `outline_measurement` refusal before encode, and even `--allow-outline` cannot waive it. The audit's two reproductions now both fail closed: four empty alpha frames and four alpha frames paired with zero plate frames.

**game33c flicker, fixed at the mask and at the post stack.** The saved evidence rules out disappearance and the seam: obj2 never fell below 11,320 px, obj3 never fell below 5,632 px, and the only chunk seam is frame 350 at 14 s. The local transition is raw obj3 drift: frame 128 to 129, 5.12 to 5.16 s, grew 14,675 to 17,630 px, added 2,955 px over `[1024,193,1130,465]`, and 2,981 of those pixels were dark; 646 dark pixels were still opaque immediately before the jump and became zero immediately after it. Flat plus luma grew by 2,949 px while the luma-only contribution fell 684 to 586, so hard-luma connectivity was not the cause. The pre-fix right-chair support measured median 345.5 dark pixels per frame from 4.0 to 5.0 s, range 5 to 617.

The deployed tracker now derives each chair object's stable support from pixels it owns on at least 20% of a chunk, carries that support across chunks, fences it to rows 184..428, and applies it only through the dark gate with 10 luma levels of measured q=2-JPEG-to-MP4 codec headroom. Its exclusion diagnostic is now the effective union, not raw logits. The first guarded ship exposed one more source bug: generic `fill_holes` resurrected 125 dark chair pixels at frame 100 and median/polish grew them. `ship.py` now accepts the aligned effective exclusion guard and re-applies it after fill-holes, temporal median, polish and display-size resampling; local prep and Modal `ship_remote` pass it automatically. One H100 v3 call tracked 691 frames for **$0.3185**; no second GPU call ran. The final aligned guard reads exactly **0 opaque chair pixels on all 691 shipped matte frames**. A deliberately wider conservative support reads frame 0 = 0, median 1, p95 43.5, max 80 over the whole take, and median 8.5 / max 30 from 4.0 to 5.0 s, versus 345.5 / 617 before.

Final matte gates all passed: protrusion clean; outline left p95 43.0 / at-line 13.7% / dark 23.9%, right 42.1 / 8.6% / 55.2%, against 60 / 45% / 78%; edge clip clean. The cutout-only page passed prerender with 0 geometry errors and 0 warnings, then `render_and_check` passed qc with no failed check and the watcher returned 0 candidates. The untrimmed render is preserved at `tiktok/_tail_prior/game33c_cutout.flickerfix.mp4`; the rejected prior is at `tiktok/_held_prior/game33c_cutout.flicker.mp4`; the staged delivery is `~/Movies/Shorts Factory/Daily/2026-09-04/tiktok/game33c_cutout.mp4`, trimmed with `-t 27.620` to the 25 fps container duration 27.640 s. Evidence: `shorts_run14/review/flicker_game33c_series.json` and `shorts_run14/review/flicker_game33c_sheet.png`. Regression coverage lives in `pipeline/prep/test_regressions_2026_09_04.py`.

## NO REPAIR MAY REMOVE SKIN (2026-09-05)

The flicker fix above is real and it is kept: the chair back is gone from `game33c` on all 691 frames by both the fixer's instrument and the clerk's independent decode. The same carve then ate his beard, jaw and hairline on the same side. Measured on the delivered file with the clerk's own instrument (enclosed cream inside the body, foreground threshold 200, crop x480-1080 y1000-1620 at 1080x1920): **enclosed holes max 938 px, p95 190, 11 frames over 300 px, sustained 8.48-8.88 s**, against **46 px** on the render it replaced; open serration inside the eroded body 1,265 px. At 405x720 it read as a torn white gash down the side of his face, and **every existing gate was green on those frames** — protrusion clean, LAW 48 clean, edge clip clean, gate 3 `describe_errors` empty, watcher 0 candidates.

**The law. A repair may bite into the silhouette from OUTSIDE. It may never remove pixels the presenter owns from INSIDE, and it may never remove skin.** Concretely, three rules, all enforced in code and none of them a note:

1. **A carried exclusion mask is a BRIDGE, never a claim.** A temporally stabilised chair support may only be applied where the CURRENT frame's own flat+luma chair mask is within `EXCL_TEMPORAL_REACH` (20 px) of it, and where that mask is empty on a frame it may not be applied at all. Darkness alone is not evidence: a beard, a hairline and a black cap are dark, which is exactly how a support built from "pixels the chair owned on 20% of the chunk" came to own his face when he leaned into that column. 20 px is measured, not chosen — the legitimate bridge the anti-flicker support exists for (obj3's dropped lower wing, 3.8-5.4 s) sits p95 7.7 px / max 19.6 px from the current chair evidence, while the support that ate his face sits 20-107 px away (p95 50.9 in the 8.32-9.36 s window). Sweeping it: at 20 px the chair reading is median 6 px against 5 with no clip and 194 before the fix, while the serration falls from max 914 / p95 234 to max 20 / p95 4.
2. **An exclusion may never leave a pocket ENCLOSED by the presenter.** Anything the subtraction leaves fully enclosed by the body is his by construction and is handed straight back — in the tracker, before the diagnostic union is written, and again in the ship post stack before the polish and after the nearest-neighbour resample.
3. **The ship gate REFUSES with the numbers.** `ship.py` measures, per frame, the enclosed holes the exclusion guard is responsible for (a hole is charged to the guard only when the guard touches it; a hole nowhere near it is a tracker artefact on a different budget) and the presenter pixels the guard removes whose plate luma is >= 110. Ceilings: **50 px** of guard-attributable holes and **60 px** of bright loss, per frame. Over either is `ShipRefused(gate="presenter_loss")`, never a silent ship. `--allow-presenter-loss` takes a written reason and is recorded; the correct remedy is always at the source — narrow the carve and re-track, or ship the uncarved alpha and remove the furniture by plate geometry the way LAW 44 removes a cut hand.

**A session tracked under an older rule does not need a new GPU call.** `pipeline/sam2/support_refit.py` re-applies the deployed rule to the saved diagnostics — the old effective exclusion, the same file from a track without temporal support (the current-frame flat+luma mask), and that track's alpha as the only place the wrongly-removed presenter pixels still exist — and writes both the repaired alpha and its corrected guard. It imports the rule from `modal_app.py` rather than restating it, so the two can never drift.

**game33c, the result.** `alpha_v4.mkv` from the one paid H100 v3 track, zero additional GPU spend. Delivered enclosed holes **max 52 px on 2 of 691 frames** against 938 before and 46 on the prior render, 0 frames over 300; every residual speck sits at the same canvas coordinates in the prior render and is attributed to the guard **0 px on all 691 frames** by the ship gate's own instrument. Serration inside the body 20 px (was 1,265). Bright loss 0. The 90,877 pixels handed back are **92.9 % skin-toned**, mean BGR (25, 38, 82), against (21, 27, 48) for what both mattes agree is not him. Gates: protrusion clean, LAW 48 clean (left p95 43.0 / at-line 13.7 % / dark 23.9 %; right 42.1 / 8.6 % / 55.2 %), edge clip CLEAN, presenter loss clean. Evidence: `shorts_run14/review/facehole_game33c_series.json`, `shorts_run14/review/facehole_game33c_sheet.png`. Regression: `pipeline/prep/test_regressions_2026_09_04.py`.

## AN OVERLAP EXEMPTION IS NOT A LICENCE TO DRAW OVER INK (2026-09-05, run 15)

geminitools shipped with a decorative "charge" stroke authored to run across the plug's body and
through the Gemini spark, in all three formats, and no gate saw it: the DOM stroke carried
`data-overlap-ok` (which a connector must carry) and the whiteboard stroke was pen ink, not a
rigid, so both were exempt by construction. Rule: any authored path that is not a connector must
keep a 4 px ink-to-ink gutter from every mark, name and object; generators assert it
(`assert_charge_clearance` pattern) and refuse the build. `data-overlap-ok` exempts an element
from the geometry audit's overlap count, never from crossing a mark.

## DRAWN GEOMETRY IS ASSERTED AGAINST THE PLAN (2026-09-05, run 15)

harnessrace's split builder derived its own chip die (121x89, centred) instead of the plan's
`canvas_rects["chip4-die"]` (176x124, mounted high), which put the LLM wordmark under the closing
tick; the cutout and whiteboard built the plan's rect and were fine. Rule: when a plan declares a
`canvas_rects` entry for an element, the generator builds that rect and asserts it (position and
size within 2 px) in its paperwork; a deliberate deviation is logged with a reason, never silent.

## WHEN A COLD READ FAILS TWICE, CHANGE THE METAPHOR (2026-09-05, run 15)

shieldstral's "shapes fitting into slots" failed eight cold readers across seven drawings
(toolbar, punched cards, box of shapes, geometric shapes); a key entering a padlock passed on
its first read, on all three formats. Rule: after two failed cold reads on the same object, stop
refining the drawing. Build two candidates (the best refinement and a different metaphor that
carries the same meaning), cut both crops, run one cold namer per candidate, and render only the
one that reads. A metaphor whose identity lives in something invisible at phone scale (a hole,
"through", a fit) loses to one whose identity is its silhouette (a key, a lock, a ladder).

## THE COLD READER IS AN INSTRUMENT, AND AN UNREAD SHARED SCENE IS NOT A PASS (2026-09-06, run 16)

plantsite lost all three lanes to one missing verb. The ARTWORK author had no agent-spawn tool in
its toolset, so it ran **zero** of the three cold reads it owed, said so in its own return
(`cold_reads_run: 0`, `cold_reads_outstanding: 3`, `blocking_before_render: true`) and returned
**verdict PASS** anyway; nothing checked it. Three lanes then built on the unread shared module.
The WHITEBOARD author, build-green with strict geometry 0/0 and prerender PASS, hit the same
missing verb, could not dispatch its namer, and returned with nothing staged. The SPLIT and CUTOUT
authors, with the same gap, improvised `claude -p` per crop and got real reads back: four
independent readers named the shared peak object **"flower"**, never "a website about plants".
Then all three lanes said, correctly, *that drawing is in the shared module and is not mine to
change* — and a shared artefact with no live owner deadlocked the recording. Three rules:

1. **Dispatch with the instrument.** `pipeline/cold_read.py dispatch --crop <abs> ... --out
   <evidence.json> --tag round1 --cold-root <run>/review/cold` blind-copies each crop under a
   random token and launches one independent `claude -p` per crop from `/tmp` on **absolute
   paths**, on session capacity, with no plan, topic, manifest or key. It needs no agent-spawn
   verb. It exits non-zero on a dispatch failure, because a reader that answers "file not found"
   is not a read — that cost run 16 two scored rows before the split author caught it. **"My
   toolset has no Agent tool" is never a reason to stall a lane or to hand on unread artwork.**
2. **The shared scene is sealed where it is drawn.** `production.py artwork-pass --run --vid
   --module --handoff --evidence --scoring` binds the module and handoff to a cold read of every
   bespoke object; `artwork-check` refuses a missing or stale one. An artwork verdict of PASS
   requires that record and `cold_reads_run` equal to the object count. No format lane may redraw
   the shared module, so it is proven at the artwork stage or the recording holds there.
3. **On a repair round the shared module has an owner.** The lane that takes
   `<run>/gen/.<vid>_scene.lock` atomically (`O_CREAT|O_EXCL`) owns it for that round: seat the
   plan's sanctioned replacement or, after two failed candidates, a fresh metaphor per the rule
   above, re-read it cold, re-run `artwork-pass`, and republish module and handoff with a note.
   A lane that does not hold the lock polls it (bounded) and rebuilds from the republished module
   rather than forking its own copy. Whiteboard draws its own composition and never takes it.
   **"Not mine to change" is not a terminal reason on a repair round.**

Regression: `pipeline/prep/test_regressions_2026_09_04.py` ("run 16 plantsite" block) and
`pipeline/test_production.py`.

## THE COLD READER IS A STOCHASTIC INSTRUMENT, AND ONE DRAW OF IT IS NOT A MEASUREMENT (2026-09-06, run 16, kimiwork)

kimiwork sealed its shared module on ONE `sure` read per object and lost split and cutout anyway.
Measured on BYTE-IDENTICAL crops, same sha256, five independent dispatches: the presentation
screen came back sure / sure / unsure / unsure / sure, and the receipt came back "document with
download arrow" `unsure` on the very crop the artwork seal had just read "receipt", `sure`. Nothing
about those two drawings changed between reads. Gating a binary on one draw of that instrument does
both halves of the damage at once: it fails good objects at random in every later lane, and it
seals a marginal one on a lucky draw. kimiwork's app window sealed 1/1 `sure`, then two independent
readers called it **"Refrigerator"** off one identical crop, and by then the only agent allowed to
redraw it had gone home. Both lanes returned "not mine to change" and the gate could only say
**"no staged path"**. Three rules:

1. **A shared scene seals on `production.SEAL_ROUNDS` (3) independent rounds, never one.**
   `--evidence` now takes several reader files, comma separated; `artwork-pass` refuses a single
   sample by name. Three dispatches at the seal cost minutes. A seal that fails downstream costs
   the recording.
2. **Rule on the set, not on the sample.** A scoring row may carry `reads: [{name, confidence,
   match: intended|synonym|different}]`, one judgement per dispatched read. Whether a noun is a
   synonym stays the author's call; the arithmetic is the code's: a SECOND reader naming a
   different object fails the object however many rounds are run (that is the drawing), one
   different name in four or more reads is instrument noise and is recorded rather than fatal, and
   at least half the reads must be `sure`. A row with no per-read judgement keeps the old
   single-sample rule exactly. **Re-reading a drawing until it passes is not the remedy; neither is
   failing it because one reader blinked.**
3. **The repair-round lock is a real file now.** `production.py scene-lock --run <run> --vid <vid>
   --holder <lane>` takes `<run>/gen/.<vid>_scene.lock` with `O_CREAT|O_EXCL`, is reentrant for its
   holder, refuses another lane by name, and releases with `--release`. The lock had been law since
   this morning and had **no implementation anywhere**, which is why two kimiwork lanes each read
   CLAIMS.md, said "not mine to change" and stopped. `artwork-check` now answers a changed module by
   naming the owner and the next move instead of dead-ending on "evidence changed". A rule that
   names an instrument has to ship the instrument.

Regression: `pipeline/test_production.py` (`test_one_lucky_read_cannot_seal_a_shared_scene`,
`test_consensus_fails_the_misread_window_and_clears_the_instrument_noise`,
`test_repair_round_gives_the_shared_scene_an_owner`), asserted on kimiwork's measured reads.

**A DRAW-ON MEASURES ITSELF (Miguel, 2026-09-08).** The dash used to reveal a
stroked path must equal that path's own length. A literal `strokeDasharray:100`
is a 100-unit dash and a 100-unit GAP, repeating, so any path longer than 100
user units ships with holes in it: it shipped a warning triangle with an open
apex and a stethoscope whose tubes stopped short of the Y junction. Where a path
declares `pathLength`, THAT is the unit the dash is measured in and the declared
value wins; `getTotalLength()` returns the geometric length there and using it
sets a dash about twice the path, which pops the drawing on instead of drawing
it. One expression is correct in both worlds and every `draw()` helper uses it:

    strokeDasharray:(i,t)=>t.getAttribute("pathLength")||t.getTotalLength()+1

Neither failure is visible to the Phone Test or to the clerk. Both look at the
drawing at rest, after the animation has finished, so a broken draw-on reaches
the viewer with every gate green. It is caught by reading the helper, not by
sampling a frame.

**A TRIANGLE IS NOT A BOX (Miguel, 2026-09-08).** A mark set inside a tapering
outline is centred on the outline's INTERIOR AREA CENTROID, not on its bounding
box and not on a fixed clearance from one edge. In an apex-up triangle that
centroid sits two thirds of the way down from the apex; a bar-and-dot placed by
its clearance above the base leaves the whole taper empty and reads as sinking,
which is exactly what shipped in `hermesdoctor`'s warning triangle (mark rows
111 to 206 of a 244 px glyph, 37 px of triangle left below it). Horizontal
centring is not the test: that glyph was centred to within half a pixel and
still read wrong.
