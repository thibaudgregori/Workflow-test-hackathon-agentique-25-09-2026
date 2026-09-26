# SFX LAW v2 — the tamed palette

Miguel, 2026-08-30, Global Law 2: *"Keep, but tame them."* The lab's first SFX
round was **unpleasant in character, louder than voice and bed, and slightly out
of sync**. This file is the replacement: seven sounds, three levels, one sync
rule. Everything below is measured, not chosen.

Files: `format_lab/_shared/sfx/*.mp3`
Audition mix: `format_lab/_shared/sfx_palette_demo.mp3` (real voice + bed + all
seven at their shipped levels — listen to this before changing anything)

---

## The instrument

Every dB in this file is on the factory's **pinned instrument** (STANDARD.md,
2026-08-18): frame RMS of a mono 16 kHz **s16le** decode (never `f32le`, which
reads +3.01 dB), **33 ms** frame. Any number quoted without that instrument is
not comparable to these.

Reference levels, measured on the actual `hermesinfinite` material:

| layer | at data-volume | p50 | p85 | p95 | peak |
|---|---|---|---|---|---|
| voice `v/audio.m4a` | 1 | -22.75 | **-16.00** | -13.69 | -8.83 |
| bed `bed_split_v2.mp3` | 0.065 | **-41.30** | **-34.40** | -32.71 | -29.98 |

**BED PRESENCE = its p85, -34.40 dBFS** — the level the music actually sits at
while it is playing material. (p50 is its floor between phrases, p95 its accent
ceiling.) Global Law 2 puts effects clearly under *that*, which is a stricter
line than merely under the voice.

---

## Why the old ones were wrong (the three defects, quantified)

**(a) Unpleasant.** Harshness is measurable: fraction of energy above 6 kHz.
The offenders were nearly pure hiss.

| old sound | hf6k | centroid |
|---|---|---|
| takeover `swarm` | 0.993 | 10 094 Hz |
| pureface `pf_tick` | 0.993 | 10 515 Hz |
| whiteboard `valve_click` | 0.984 | 9 504 Hz |
| artifactspine `as_ring` | 0.883 | 10 674 Hz |
| whiteboard `marker_squeak` (the hard NO) | 0.548 | 6 425 Hz |

**(b) Too loud.** At `data-volume="0.18"` the hottest lab one-shots peaked at
**-21.0 dBFS**, against a bed whose loudest single frame is **-29.98**. They ran
up to **9 dB above the music's absolute peak** and only ~5 dB under speech.

| old sound | peak @0.18 | vs bed presence |
|---|---|---|
| cutout `step_in` | -21.02 | **13.4 dB OVER** |
| facesplit `facesplit_cut` | -21.11 | 13.3 dB over |
| takeover `tk_out` | -21.78 | 12.6 dB over |
| takeover `tk_in` | -24.13 | 10.3 dB over |
| pureface `pf_rise` | -24.95 | 9.5 dB over |

For scale, the loudest SFX in the **approved, shipped** factory (`assets/sfx`,
runs 1-8) peaks at **-28.03** (`boom`). The lab was 7 dB hotter than anything
Miguel had ever signed off.

**(c) Out of sync — root-caused.** This was never a placement error. The old
files carry **leading silence before the transient**, so a builder scheduling
`data-start = event_time` heard the sound that much late no matter how carefully
the cut was placed:

| old sound | dead air before the transient |
|---|---|
| cutout `wall_slam` | **533 ms** (13 frames @25) |
| takeover `tk_out` | **492 ms** (12 frames) |
| whiteboard `marker_short` | 353 ms |
| cutout `layer_pass` | 352 ms |
| facesplit `facesplit_lift` | 295 ms |
| artifactspine `as_toggle` | 191 ms |

Every file in the new palette is **onset-trimmed: decoded sample 0 IS the
transient** (measured onset lag 3.0 ms, well inside one frame). `data-start` now
means what it says.

---

## The palette

Seven members, three level classes. Soft/tactile family: wood, cloth, paper,
felt — no metal, no hiss, no reverb tail.

| file | class | role | dur | centroid | hf6k | decay→-20 dB |
|---|---|---|---|---|---|---|
| `soft_whoosh.mp3` | structure | takeover IN / layout seize | 0.27 s | 803 Hz | 0.005 | 60 ms |
| `reverse_air.mp3` | structure | takeover OUT / release | 0.34 s | 2 734 Hz | 0.096 | 60 ms |
| `low_thump.mp3` | structure | punch-in / hard-cut landing | 0.42 s | 310 Hz | 0.000 | 55 ms |
| `tick.mp3` | detail | word emphasis / UI step | 0.32 s | 1 208 Hz | 0.004 | 15 ms |
| `page_turn.mp3` | detail | artifact section change | 0.79 s | 1 194 Hz | 0.001 | 45 ms |
| `pop.mp3` | detail | element arrival | 0.42 s | 689 Hz | 0.000 | 25 ms |
| `pen_loop.mp3` | loop | whiteboard pen (sustained) | 2.00 s | 2 747 Hz | 0.203 | — |

`soft_whoosh` + `reverse_air` are a deliberate matched **pair** (seize/release)
and are meant to read as siblings. The three percussive members are held at
least half an octave apart so they stay three sounds and not one — scored
independently they had collapsed onto 214 / 255 / 272 Hz.

---

## LEVELS — the pinned numbers

Every file is normalised to **one unity reference, -19.0 dBFS**, so a single
constant per class is exact for every member of that class. The reference is
derived, not chosen: the palette's worst crest factor is 16.33 dB, and -19.0
keeps every sample peak at or under -2 dBFS (an earlier pass at -12 dBFS hard-
clipped three files to 0.00 dBFS).

| class | `data-volume` | delivered peak | under bed presence | under voice |
|---|---|---|---|---|
| **structure** | **`0.120`** | **-37.40 dBFS** | **3.0 dB** | 21.4 dB |
| **detail** | **`0.077`** | **-41.30 dBFS** | **6.9 dB** | 25.3 dB |
| **loop** | **`0.038`** | **-47.30 dBFS** (sustained body) | **13.1 dB** | 31.5 dB |

Replaces the single old `SFX_VOLUME = "0.18"`.

**Read the constant and the file together.** The gain number dropped only
modestly (0.18 → 0.120), but because the files are now normalised the *delivered*
level dropped hard — `tk_in` went from -24.13 to -37.40 dBFS, a **13.3 dB** cut.
Never judge this mix by the constant alone; the source loudness of each file is
part of the math. That is the whole reason the palette is normalised.

**Why these three numbers**

- *structure* sits one clear step (3 dB) below bed presence. These carry the cut,
  so they are the loudest thing allowed — but they are under the music, which is
  what Miguel asked for and what the old ones violated.
- *detail* sits at the bed's own floor (-41.30). Frequent small events must not
  accumulate; at this level they read as texture, never as an announcement.
- *loop* is judged on its **sustained p85 body**, not its peak, because a loop is
  heard as its body. A continuous noise source masks speech far harder than a
  transient does, so it goes 6 dB below the bed floor. This is the answer to the
  marker squeak: same gesture, **12.5 dB quieter body** (-34.97 → -47.50) and
  **11.5 dB quieter peak** (-32.90 → -44.40), with the squeak filtered out of it.

**Not inaudible — proven by precedent.** The approved shipped factory SFX peak at
-28.0 (`boom`), -28.4 (`whoosh`), -40.7 (`pop`), -43.1 (`ding`), -43.9 (`click`).
Both new classes land *inside* that approved envelope: structure between `pop`
and `whoosh`, detail right on `pop`/`ding`. Miguel has shipped and approved
sounds at these levels for eight runs.

**Verified in a real mix**, not on isolated stems
(`_sfxpalette_work/mixproof.json`): voice + bed at 0.065 + all seven at their
class constants placed in speech pauses, where they are most exposed.

- Speech margin **21.11 dB → 21.06 dB** with all SFX added — a 0.05 dB cost,
  comfortably inside the approved run-7 corpus band of 15.85-23.70 dB.
- Lift over the bed alone: **0.13-2.43 dB**. The effect colours the moment; it
  never takes it over.

---

## SYNC RULE (Global Law 2, frame-lock)

> **An SFX's transient must land within ±1 frame — 40 ms at 25 fps — of the
> visual event it scores, and the EVENT'S FRAME IS THE AUTHORITY.**

The picture is never moved to fit the sound. If they disagree, the sound moves.

Mechanically, at 25 fps (Global Law 6 — face-led formats render at native 25):

1. Find the event's frame `f`. Its time is `t = f / 25`.
2. Schedule `data-start = t`. No hand-tuned lead or lag offsets — those were
   compensation for the leading silence, and the silence is gone.
3. The palette's own onset lag is 3.0 ms (`pen_loop` 20 ms), so the delivered
   transient lands **inside 1/13th of a frame**. The budget is spent on the
   visual, not the file.
4. `sfxpalette_verify.py` fails any file whose onset exceeds 40 ms.

Anything that was scheduled with a magic offset (`t0 - 0.06`, `t1 - 0.04` in
`takeover_core.py`) must have that offset **removed** when it moves to this
palette — the offsets now double-count.

For `pen_loop`, the transient rule does not apply: it is a sustained bed for the
writing gesture. Start it with the stroke and fade it out over ~120 ms when the
stroke stops.

---

## Rules for builders

1. **Never hand-set an SFX gain.** Use the class constant. Hand-setting a bed
   gain to 0.16 already put a builder in the ledger; the same applies here.
2. **Never drop an unnormalised mp3 into `_shared/sfx/`.** The constant would
   silently lie. Add it through `sfxpalette_pick.py` so it gets trimmed and
   normalised, then run the gate.
3. **Ration them.** These levels make effects safe, not free. Global Law 2 asks
   for taming, and an effect on every beat is untamed however quiet it is.
4. **Run the gate before shipping**:
   ```
   ~/Documents/Workspace/.venv/bin/python format_lab/_shared/sfxpalette_verify.py
   ```
   It re-derives every claim in this file from the files on disk — unity level,
   delivered level vs class target, clipping, onset lag vs the 40 ms budget,
   harshness ceiling, phone audibility. Exit 1 on any failure.

---

## Two findings worth keeping

**Taming and audibility are different jobs, and over-taming is its own defect.**
Chasing "soft, dark, no brightness" drove every *small* sound below 300 Hz,
where a phone speaker — the delivery device for shorts — reproduces nothing:
`low_thump` candidates measured 36-270 Hz with 0.000-0.028 of their energy in
the 300 Hz-8 kHz band. A sound can be perfectly tame and completely inaudible
where it actually plays. Selection therefore gates on a **phone-audibility floor
(≥0.35 of energy in 300 Hz-8 kHz)** alongside the harshness ceiling, and
`low_thump` needed harmonic generation from its low band (soft saturation,
harmonics kept above 300 Hz, mixed back at 4.0) to survive the speaker without
changing pitch.

**Harsh is fixable, so tame rather than reject.** Graphite on paper is inherently
broadband — all three pen candidates measured hf6k 0.76-0.84. Rather than
discard them, the lowest-strength low-pass that brings a sound under its ceiling
is searched for and applied (`pen_loop` 6 500 Hz, 0.838 → 0.203). Naturally soft
sounds are left completely untouched. That is literally "keep, but tame".

---

## Provenance

| step | script |
|---|---|
| measurement instrument | `_shared/sfxpalette_measure.py` |
| candidate generation (wave 1, 21 clips) | `_shared/sfxpalette_gen.py` |
| candidate generation (wave 2, 9 clips) | `_shared/sfxpalette_gen2.py` |
| pick / trim / tame / translate / normalise | `_shared/sfxpalette_pick.py` |
| real-mix proof | `_shared/sfxpalette_mixproof.py` |
| **gate** | `_shared/sfxpalette_verify.py` |
| raw candidates + JSON reports | `_shared/_sfxpalette_work/` |

Source: ElevenLabs `/v1/sound-generation`, 30 clips, spend approved by Miguel
for this fix round. API constraint measured here: `duration_seconds` must be
**≥ 0.5** (0.35 and 0.4 return `400 invalid_generation_settings`), so short
ticks and pops are generated at 0.5 s and trimmed to their real decay.
