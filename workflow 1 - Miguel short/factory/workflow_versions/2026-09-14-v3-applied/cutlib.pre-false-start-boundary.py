#!/usr/bin/env python3
"""THE CUT, AS A LIBRARY — take detection + the 4K cut master + the tight
transcript, extracted generically from the `build_cut_*.py` family.

WHAT THIS IS.  Ten run-9 `build_cut_<id>.py` scripts are ninety percent the same
program.  The ten percent that differs is (a) the opening key and the sign-off
key, (b) hand-verified `EXPECTED_*` constants, and (c) a docstring recording
what that particular raw taught the ledger.  This module is the ninety percent,
written once, with the ten percent as ARGUMENTS.

THE LEDGER RULES IT CARRIES, verbatim in behaviour:

  PRIMARY — CONTENT.  A take OPENS on a scripted key and is COMPLETE only when
  it reaches the spoken sign-off.  The LAST complete opening wins.  Nothing else
  is decisive; the two cross-checks below are WITNESSES, not deciders.

  CROSS-CHECK 1 — THE MARKER RULE.  A discard marker is a spoken "no." or a
  truncated word (trailing `-`, `...`, `…`).  The rule answers `markers[-1] + 1`.
  On some raws that is an EQUALITY (lunacheaper: 26 markers, last w902, answer
  w903 = the content answer).  On others it is a LOWER BOUND, because several
  abandonments carry no partial word at all (sparkchrome: 14 markers against 20
  restarts).  On others it ABSTAINS entirely (deepseekflash: zero markers).  All
  three are legal; a marker INSIDE the chosen take is not, and closure refuses it.

  CROSS-CHECK 2 — THE TRANSCRIPT-GAP SWEEP.  The last inter-word gap >= T, swept
  at ten thresholds.  A rule that is correct on a BAND of thresholds is evidence;
  a rule correct at exactly one point is not, which is why every threshold is
  recorded with the answer it gives and how many words early it is.

  CROSS-CHECK 2b — THE ENVELOPE.  The end of the last >= 0.30 s run of
  sub-threshold 10 ms RMS windows before the winner's first word.  This is the
  INSTRUMENT that puts the head inside a measured silence rather than at a padded
  constant, and the head is ASSERTED to land inside that run.

  CLOSURE.  No discard marker and no further scripted opening may survive inside
  the chosen take, and the take must actually contain the sign-off.

TWO BUGS OF THE FAMILY DELIBERATELY NOT FORKED
----------------------------------------------
1. THE 16 kHz ANALYSIS WAV.  `build_cut_lunacheaper.py` still writes
   `analysis_16k_mono_DO_NOT_MIX.wav` beside the master.  It is never a legal mix
   source (Gate 2b TREBLE: ten run-9 remakes mixed from a 16 kHz analysis track
   and lost their top octave by 18.4 dB), and the daily brief says "NEVER any 16k
   analysis wav".  `build_cut_sparkchrome.py` had already dropped it.  This module
   writes 48 kHz stereo ONLY and records `analysis_wav_written: false`.  Scribe
   still needs 16 kHz mono, so one is extracted to a TEMPORARY directory for the
   upload and deleted; it never lands beside the master where a build could reach
   for it.
2. HAND-TYPED FACE WINDOWS.  `build_cut_sparkchrome.py` hard-codes `FACE_CX`,
   `FULL_X0` and `BOTTOM_X0` as constants measured in a previous session.  A crop
   window belongs to one day, one chair and one distance to the lens.  Windows
   here are always MEASURED on THIS master (`plate.measure_framing`), the way
   `build_cut_lunacheaper.py` does it, and the measurement rows ship in the edl.

NO LLM ANYWHERE.  Scribe is an ASR API, not a model making a judgement.
"""
from __future__ import annotations

import array
import functools
import json
import math
import os
import platform
import re
import subprocess
import sys
import tempfile
import wave
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

WORKSPACE = Path.home() / "Documents" / "Workspace"
F = WORKSPACE / "projects/personal/content/shorts-factory"
VOCAB = WORKSPACE / "execution" / "transcription_vocabulary.json"
VIDEO_USE_HELPERS = WORKSPACE / "projects/personal/infra/agent-tools/video-use/helpers"

# ---- the family's frozen constants ----------------------------------------
SILENCE_NOISE = "-35dB"
SILENCE_MIN = 0.4
SILENCE_KEEP = 0.16

# TAIL (Miguel, 2026-09-03: "be quite aggressive with the cut after the last
# word, ideally 0.2 s, because you slightly see me turning off recording").
# Was 0.45 / 0.35: run 12's masters ran 0.32 s past the last word.
TAIL_PAD = 0.20
TAIL_HOLD = 0.20
# The tail is measured from the LAST WORD's Scribe end, not from where the
# silence detector first hears silence (which is 0.05-0.15 s later, after the
# voice decays): run 13 masters ran 0.24-0.32 s past the last word with the
# silence-anchored rule.  The hard cap below is last word end + TAIL_HOLD.
# FALSE START (Miguel, 2026-09-03, astramath): a scripted opening that repeats
# inside the cut's first seconds is a restart, and the take begins at the LAST
# repeat.  The raw Scribe pass can merge the two attempts into one (it heard
# 'GPT Astra ... solved' where the take said 'GPT Astra solved, GPT Astra
# solved'), so this is verified on the TIGHT transcript after the cut and the
# cut is redone once from the restart.  Never a 'two-step hook'.
FALSE_START_WINDOW_S = 6.0
FALSE_START_PREFIX = 3        # tokens of the opening key that identify an attempt
# LEAD-IN (geo, run 19, 2026-09-13): the content rule picks the LAST scripted
# opening, and that word is not always where the delivered SENTENCE begins.  On
# geo the take is "this is why | AI SEO, also known as GEO, is brutally hard":
# the keeper opening ("AI" w26 @37.38) sits 0.141 s after "why" inside ONE
# breath, so there is no >= SILENCE_RUN_MIN silence anywhere before it and the
# head refused the whole cut.  The head belongs at the start of the UTTERANCE
# that carries the keeper — the maximal run of words joined by transcript gaps
# below SILENCE_RUN_MIN — which on geo is "this" w23 @36.779 with a MEASURED
# 0.48 s silence run (36.169-36.649) in front of it.  The walk-back may never
# cross an earlier scripted opening or a discard marker (those words belong to
# an abandoned attempt) and is bounded in words and seconds.
LEADIN_WORDS_MAX = 8
LEADIN_S_MAX = 3.0
EOF_GUARD = 0.02
HEAD_LEAD = 0.10
HEAD_FALLBACK = 0.22

ENV_WIN = 0.010          # 10 ms RMS windows
ENV_FLOOR = 0.012        # normalised RMS treated as voiced
SUSTAIN_S = 0.15         # a real onset HOLDS above the floor this long
SILENCE_RUN_MIN = 0.30
MAX_LEAD_IN = 0.35

FPS = 25
MASTER_W, MASTER_H = 3840, 2160
FULL_W = 1216            # the widest 9:16 window a 2160-tall master can give (1215), even
BOTTOM_W = 2208          # the split's bottom-half torso window
# HD DELIVERY (Miguel, 2026-09-03: "no more 4k rendering, always HD").  The cut
# master stays 3840x2160 (the crop windows need the pixels) but the face plates
# the pages consume are cut at DELIVERY size: full 1080x1920, bottom 1080x1058.
FULL_PLATE = (1080, 1920)
BOTTOM_PLATE = (1080, 1058)

DEFAULT_GAP_SWEEP = (0.8, 0.9, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0, 8.0)

# ---- the intermediate encoder ----------------------------------------------
# The cut master and the two face plates are INTERMEDIATES: later stages decode
# them, nothing ever delivers them.  On macOS they are encoded by Apple's
# hardware H.264 encoder at a constant quality ABOVE the x264 files they
# replace (2026-09-03: q:v 85 measures 34 Mbit/s on the 4K master against
# libx264 crf 17's 25.9, 12.4 against 8.0 on face_full_hd, and SSIM 0.997
# against the x264 file), which is 5-10x faster wall clock for the same
# pixels.  Where videotoolbox is not there — Linux, a build without it — the
# libx264 settings below are used unchanged, so the fallback is the old file.
VT_ENCODER = "h264_videotoolbox"
VT_QUALITY = "85"                 # 1-100, constant quality; see the note above
X264_MASTER = ("-c:v", "libx264", "-preset", "fast", "-crf", "17")
X264_PLATE = ("-c:v", "libx264", "-preset", "fast", "-crf", "18")


@functools.lru_cache(maxsize=1)
def videotoolbox_available() -> bool:
    """Probed once per process: macOS AND an ffmpeg that lists the encoder."""
    if platform.system() != "Darwin":
        return False
    try:
        out = subprocess.run(["ffmpeg", "-hide_banner", "-v", "error",
                              "-encoders"], capture_output=True, text=True,
                             check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return False
    return VT_ENCODER in out


def intermediate_video_args(x264: tuple[str, ...], *, gop: int | None = None
                            ) -> list[str]:
    """Encoder flags for an intermediate, hardware first, libx264 as fallback.

    `gop` is the keyframe cadence the face plates assert.  videotoolbox takes
    `-g` and honours it exactly (verified: a plate cut at `-g 25` reports a
    keyframe every 25 frames); `-keyint_min` / `-sc_threshold` are libx264
    options and are only spelled on the libx264 path.
    """
    if videotoolbox_available():
        args = ["-c:v", VT_ENCODER, "-q:v", VT_QUALITY, "-pix_fmt", "yuv420p"]
        if gop:
            args += ["-g", str(gop)]
        return args
    args = list(x264)
    if gop:
        args += ["-g", str(gop), "-keyint_min", str(gop), "-sc_threshold", "0"]
    return args


# =============================================================================
# shell
# =============================================================================
def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def probe(path: Path, entries: str, stream: str | None = None) -> str:
    cmd = ["ffprobe", "-v", "error"]
    if stream:
        cmd += ["-select_streams", stream]
    cmd += ["-show_entries", entries, "-of", "csv=p=0", str(path)]
    return subprocess.run(cmd, check=True, capture_output=True,
                          text=True).stdout.strip()


def probe_duration(path: Path) -> float:
    return float(probe(path, "format=duration"))


# =============================================================================
# A.  THE WORD STREAM
# =============================================================================
def norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def is_truncated(text: str) -> bool:
    s = text.strip()
    return s.endswith("-") or s.endswith("...") or s.endswith("…")


def is_spoken_no(text: str) -> bool:
    return re.fullmatch(r"no[.,!?]", text.strip().lower()) is not None


def is_discard_marker(text: str) -> bool:
    return is_spoken_no(text) or is_truncated(text)


def load_words(transcript: Path) -> list[dict]:
    data = json.loads(Path(transcript).read_text(encoding="utf-8"))
    return [w for w in data["words"] if w.get("type") == "word"]


def _alts(token) -> tuple[str, ...]:
    if isinstance(token, (list, tuple)):
        return tuple(norm(str(t)) for t in token)
    return (norm(str(token)),)


def phrase_indexes(words: list[dict], key) -> list[int]:
    """Every index where `key` matches, token for token.

    A key token may be a string or a tuple of alternatives.  Matching is on the
    normalised word (letters and digits only), which is why `isn't` and `isnt`
    are the same token and why punctuation never has to be spelled.
    """
    key = tuple(_alts(t) for t in (key if isinstance(key, (list, tuple)) else (key,)))
    n = len(key)
    if n == 0:
        return []
    return [i for i in range(len(words) - n + 1)
            if all(norm(words[i + k]["text"]) in key[k] for k in range(n))]


def opening_indexes(words: list[dict], key, *, truncation_arm: bool = True) -> list[int]:
    """Scripted openings, with the TRUNCATION ARM on the key's last token.

    An abort that dies inside the key's final word (`Bigger isn-`) is still an
    attempt, and the ranking has to see it or the winner is chosen against an
    under-counted field.  `build_cut_lunacheaper.py` spells that arm by hand as
    `OPENING_NEXT = ("isnt", "isn")`; here it is derived — the last token also
    matches a TRUNCATED word whose normalised text is a non-empty prefix of it.

    Both counts are reported by `detect_take`, so a builder can always see
    whether the arm changed the field or was merely harmless.
    """
    key = tuple(_alts(t) for t in (key if isinstance(key, (list, tuple)) else (key,)))
    n = len(key)
    if n == 0:
        return []
    out = []
    for i in range(len(words) - n + 1):
        ok = True
        for k in range(n):
            w = words[i + k]
            got = norm(w["text"])
            if got in key[k]:
                continue
            if (truncation_arm and k == n - 1 and is_truncated(w["text"])
                    and got and any(a.startswith(got) for a in key[k])):
                continue
            ok = False
            break
        if ok:
            out.append(i)
    return out


def opening_indexes_multi(words: list[dict], keys, *, truncation_arm: bool = True
                          ) -> list[int]:
    """The union of several scripted-opening FAMILIES, de-duplicated and sorted.

    Some raws do not have one script attempted N times; they have two or three
    phrasings of the same opening (`build_cut_minimaxh3.py`'s `OPENING_KEYS`).
    A family list is the honest key there — a single over-short key that happens
    to span them all fires mid-sentence too, and the ranking is then done against
    a field that contains things that were never attempts.
    """
    out: set[int] = set()
    for k in keys:
        out |= set(opening_indexes(words, k, truncation_arm=truncation_arm))
    return sorted(out)


def sign_off_indexes(words: list[dict], key) -> list[int]:
    return phrase_indexes(words, key)


def discard_markers(words: list[dict]) -> list[int]:
    return [i for i, w in enumerate(words) if is_discard_marker(w.get("text", ""))]


def gap_indexes(words: list[dict], threshold: float) -> list[int]:
    return [i for i in range(1, len(words))
            if words[i]["start"] - words[i - 1]["end"] >= threshold]


# =============================================================================
# B.  THE ENVELOPE — cross-check 2b, and the head
# =============================================================================
def envelope(raw: Path, start: float, end: float, scratch: Path
             ) -> tuple[list[float], list[float]]:
    scratch.mkdir(parents=True, exist_ok=True)
    tmp = scratch / "_probe.wav"
    subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
         "-i", str(raw), "-vn", "-ac", "1", "-ar", "16000",
         "-acodec", "pcm_s16le", str(tmp), "-y"], check=True)
    with wave.open(str(tmp), "rb") as handle:
        rate = handle.getframerate()
        frames = handle.readframes(handle.getnframes())
    tmp.unlink()
    samples = array.array("h")
    samples.frombytes(frames)
    step = int(rate * ENV_WIN)
    times, values = [], []
    for i in range(0, len(samples) - step, step):
        chunk = samples[i:i + step]
        rms = math.sqrt(sum(float(v) * v for v in chunk) / len(chunk)) / 32768.0
        times.append(start + i / rate)
        values.append(rms)
    return times, values


def silence_runs(times, values, thresh) -> list[tuple[float, float]]:
    runs, start = [], None
    for t, v in zip(times, values):
        if v < thresh:
            if start is None:
                start = t
        elif start is not None:
            runs.append((start, t))
            start = None
    if start is not None:
        runs.append((start, times[-1] + ENV_WIN))
    return runs


def utterance_lead_in(words: list[dict], first: int, *, openings=(),
                      markers=(), gap_min: float = SILENCE_RUN_MIN,
                      words_max: int = LEADIN_WORDS_MAX,
                      seconds_max: float = LEADIN_S_MAX) -> dict | None:
    """Where the SENTENCE carrying the keeper opening actually begins.

    The keeper is the last scripted opening; it can sit mid-breath behind a
    lead-in the speaker really said ("this is why | AI SEO ...", geo/run 19).
    Walk back over word boundaries whose transcript gap is BELOW `gap_min` and
    stop at the first boundary that could hold a silence run.  Two floors keep
    an abandoned attempt out of the take: the walk may not reach or pass an
    EARLIER scripted opening, nor a discard marker, because those words are the
    abandonment itself.  Returns None when the keeper already starts its own
    utterance (nothing to do) or when a floor blocks the walk.
    """
    if first <= 0:
        return None
    floor = max([int(i) + 1 for i in openings if int(i) < first]
                + [int(i) + 1 for i in markers if int(i) < first] + [0])
    j = first
    while (j - 1 >= floor
           and first - (j - 1) <= words_max
           and float(words[first]["start"]) - float(words[j - 1]["start"]) <= seconds_max
           and float(words[j]["start"]) - float(words[j - 1]["end"]) < gap_min):
        j -= 1
    if j == first:
        return None
    return {
        "keeper_index": int(first),
        "keeper_start_s": round(float(words[first]["start"]), 3),
        "lead_in_index": int(j),
        "lead_in_start_s": round(float(words[j]["start"]), 3),
        "lead_in_prev_end_s": round(float(words[j - 1]["end"]), 3),
        "lead_in_words": [str(w.get("text", "")) for w in words[j:first]],
        "boundary_gap_s": round(float(words[j]["start"])
                                - float(words[j - 1]["end"]), 3),
        "floor_index": int(floor),
        "rule": (f"the keeper opening sits inside one breath; the take starts "
                 f"at the head of its utterance — the maximal run of words "
                 f"joined by transcript gaps < {gap_min}s, never crossing an "
                 f"earlier opening or a discard marker, at most {words_max} "
                 f"words / {seconds_max}s back"),
    }


def measured_head(raw: Path, prev_end: float, scribe_start: float,
                  scratch: Path, head_lead: float = HEAD_LEAD,
                  scribe_end: float | None = None) -> dict:
    """THE HEAD, MEASURED — behaviour identical to build_cut_lunacheaper.py.

    The onset is chosen by the END of the last >= SILENCE_RUN_MIN run of
    sub-threshold windows (silence DURATION, not amplitude), cross-checked by
    SUSTAIN — the first window that holds above the threshold for SUSTAIN_S.
    The sustain onset may lead the run's end by at most MAX_LEAD_IN; beyond that
    the run ended on a non-speech transient and SUSTAIN wins.  The head is then
    ASSERTED to sit inside the measured silence run — never at a padded constant.
    """
    lo = max(0.0, prev_end - 0.30)
    hi = scribe_start + 0.60
    times, values = envelope(raw, lo, hi, scratch)
    peak = max(values) if values else 0.0
    thresh = max(ENV_FLOOR, peak * 0.06)
    win = max(1, int(round(SUSTAIN_S / ENV_WIN)))

    runs = [r for r in silence_runs(times, values, thresh)
            if r[1] - r[0] >= SILENCE_RUN_MIN and r[1] <= scribe_start + 0.15
            and r[1] > prev_end - 0.05]
    scribe_drift = 0.0
    if not runs and scribe_end is not None and scribe_end > scribe_start + 0.5:
        # SCRIBE START INSIDE MEASURED SILENCE (plantsite, run 16, 2026-09-06;
        # rule tightened after the 2026-09-06 prep audit): the transcript's first
        # word spans a pause (33.14 -> 36.20 s over ~3 s of digital silence) and
        # the real onset is later.  The AUDIO decides, under three conditions:
        # (1) a >= SILENCE_RUN_MIN silence run must CONTAIN scribe_start, so a
        #     Scribe start already inside speech is never moved;
        # (2) the onset is the FIRST sustained speech after that run, and it
        #     must lie inside the first word's own Scribe span (+0.15 s), so no
        #     genuine first speech can be skipped for a later pause;
        # (3) all-silent audio still refuses.
        hi2 = scribe_end + 0.60
        times2, values2 = envelope(raw, lo, hi2, scratch)
        peak2 = max(values2) if values2 else 0.0
        thresh2 = max(ENV_FLOOR, peak2 * 0.06)
        containing = [r for r in silence_runs(times2, values2, thresh2)
                      if r[1] - r[0] >= SILENCE_RUN_MIN and r[0] <= scribe_start <= r[1]]
        if containing:
            r0, r1 = containing[0]
            win2 = max(1, int(round(SUSTAIN_S / ENV_WIN)))
            # the FIRST SUSTAINED onset after the containing run; isolated
            # above-threshold windows shorter than SUSTAIN_S (a click, a breath,
            # plantsite's 20 ms transient at 35.78 s) are walked through, they
            # are not speech and never move the head
            onset2 = next((times2[i] for i in range(len(values2) - win2)
                           if times2[i] >= r1 - ENV_WIN
                           and all(v >= thresh2 for v in values2[i:i + win2])), None)
            if onset2 is not None and onset2 <= scribe_end + 0.15:
                times, values, thresh, peak = times2, values2, thresh2, peak2
                runs = [(r0, onset2)]        # the silence runs up to the sustained onset
                scribe_drift = round(onset2 - scribe_start, 3)
    if not runs:
        raise RuntimeError(
            "no silence run >= SILENCE_RUN_MIN before the take's first word")
    run_start, run_end = runs[-1]

    # SUSTAIN looks only AFTER the last silence run begins.  Before 2026-09-03
    # it was allowed to start 50 ms before the previous word's Scribe end, and
    # on astramath (run 11) that let the voiced tail of an abandoned "that's w-"
    # (Scribe end 97.84, real end 98.00) count as the take's onset: 97.79
    # against a Scribe start of 100.72, so cross-check 2b refused the cut.  A
    # >= SILENCE_RUN_MIN run ending within 0.15 s of the take's first word
    # cannot contain the onset, so nothing before it can be the onset either.
    sustain_onset = None
    for i in range(len(values) - win):
        if all(v >= thresh for v in values[i:i + win]) and times[i] >= run_start:
            sustain_onset = times[i]
            break
    if sustain_onset is None:
        sustain_onset = scribe_start
    lead_in = round(sustain_onset - run_end, 3)
    if 0.0 <= lead_in <= MAX_LEAD_IN:
        onset, rule = run_end, "silence-run end"
    else:
        onset, rule = sustain_onset, ("sustain (the silence run ended on a "
                                      "non-speech transient)")

    voiced = [t for t, v in zip(times, values) if v >= thresh]
    prev_voiced_end = max([t for t in voiced if t <= prev_end + 0.25], default=lo)
    floor = min(values) if values else 0.0

    head = onset - head_lead
    if not (run_start + 0.05 <= head <= onset):
        head = max(run_start + 0.05, onset - HEAD_FALLBACK)
    if not (run_start <= head <= run_end):
        raise RuntimeError(
            f"head {head:.3f} does not sit inside the measured silence run "
            f"[{run_start:.3f}, {run_end:.3f}]")
    return {
        "onset_rule": rule,
        "primary_rule": (f"END of the last >= {SILENCE_RUN_MIN}s run of "
                         f"sub-threshold 10ms windows (silence DURATION, not "
                         f"amplitude)"),
        "cross_check_rule": (f"SUSTAIN: first 10ms window holding >= threshold "
                             f"for {SUSTAIN_S}s; speech may lead it by at most "
                             f"{MAX_LEAD_IN}s"),
        "measured_onset_s": round(onset, 3),
        "sustain_onset_s": round(sustain_onset, 3),
        "sustain_lead_in_s": lead_in,
        "silence_run_s": [round(run_start, 3), round(run_end, 3)],
        "silence_run_duration_s": round(run_end - run_start, 3),
        "scribe_start_s": round(scribe_start, 3),
        "scribe_vs_onset_s": round(scribe_start - onset, 3),
        "scribe_start_inside_silence_drift_s": scribe_drift,
        "prev_utterance_audible_end_s": round(prev_voiced_end, 3),
        "silence_before_take_s": round(onset - prev_voiced_end, 3),
        "envelope_threshold": round(thresh, 5),
        "envelope_peak": round(peak, 5),
        "envelope_floor": round(floor, 6),
        "head_s": round(head, 3),
        "head_lead_s": head_lead,
        "head_inside_silence_run": True,
        "head_pad_vs_onset_s": round(onset - head, 3),
        "head_pad_vs_scribe_s": round(scribe_start - head, 3),
    }


# =============================================================================
# C.  TAKE DETECTION
# =============================================================================
def detect_take(words: list[dict], *, opening_key=None, sign_off_key,
                opening_families=None, gap_sweep=DEFAULT_GAP_SWEEP,
                expected: dict | None = None,
                allow_uncorroborated: bool = False) -> dict:
    """The ledger's three rules, run together, with the content rule deciding.

    `expected` is optional and NOTHING is hard-coded: every key present in it is
    asserted, so a builder who has hand-verified a number can pin it and a
    re-transcription that moves it fails loudly instead of silently re-cutting.
    Recognised keys: raw_words, take_index, take_start, take_words, markers,
    last_marker, openings, sign_offs, gap_correct_at.
    """
    expected = dict(expected or {})
    rec: dict = {}

    def want(key, got, label):
        if key in expected and expected[key] != got:
            raise RuntimeError(f"{label} moved: {got!r} vs expected "
                               f"{expected[key]!r}")

    want("raw_words", len(words), "raw word count")

    sign_offs = sign_off_indexes(words, sign_off_key)
    want("sign_offs", len(sign_offs), "sign-off count")
    if not sign_offs:
        raise RuntimeError(
            f"the sign-off key {sign_off_key!r} never fires in this raw — the "
            "content rule has no completion test and cannot decide a take")
    end_index = sign_offs[-1]

    if (opening_key is None) == (opening_families is None):
        raise RuntimeError("pass exactly one of opening_key / opening_families")
    families = list(opening_families) if opening_families else [opening_key]
    openings = opening_indexes_multi(words, families)
    openings_no_arm = opening_indexes_multi(words, families, truncation_arm=False)
    want("openings", len(openings), "opening count")
    candidates = [i for i in openings if i < end_index]
    if not candidates:
        raise RuntimeError("no scripted opening before the sign-off")
    first = candidates[-1]

    # --- CROSS-CHECK 1: the marker rule ------------------------------------
    markers = discard_markers(words)
    spoken_nos = [i for i in markers if is_spoken_no(words[i].get("text", ""))]
    want("markers", len(markers), "marker count")
    if markers:
        want("last_marker", markers[-1], "last marker")
    # ── INNER STUMBLES STAY (Miguel, 2026-09-04) ─────────────────────────
    # A discard marker AFTER the keeper opening is a MID-SENTENCE STUMBLE, not
    # a false start, and it stays in the video.  Only a marker BEFORE the keeper
    # is a false start.  So the marker rule's claim is about the LAST MARKER
    # BEFORE THE KEEPER — that is the only thing it was ever able to witness —
    # and an inner stumble can no longer make it "DISAGREE" with the content
    # rule.  game33c/run 14 is the case: markers at w2, w62, w85, w124, keeper
    # at w86.  Reading markers[-1] = w124 the rule answered w125 and the cut
    # REFUSED; reading the last marker before the keeper, w85, it answers w86 —
    # EQUALITY with the content rule, i.e. the strongest witness there is.  The
    # old reading did not just refuse a good take, it threw away its own
    # corroboration.
    markers_before = [i for i in markers if i < first]
    markers_inside = [i for i in markers if first <= i <= end_index]
    marker_answer = (markers_before[-1] + 1) if markers_before else None
    if marker_answer is None:
        marker_verdict = "abstains"
    elif marker_answer == first:
        marker_verdict = "equality"
    elif marker_answer < first:
        marker_verdict = "bound"
    else:
        # UNREACHABLE BY CONSTRUCTION: markers_before are all < first, so
        # marker_answer <= first.  Kept so a future edit that widens the set
        # trips the branch instead of silently shipping a false start.
        marker_verdict = "DISAGREES"

    # --- CROSS-CHECK 2: the transcript-gap sweep ---------------------------
    sweep, correct_at = {}, []
    for threshold in gap_sweep:
        alt = gap_indexes(words, threshold)
        answer = alt[-1] if alt else None
        ok = answer == first
        if ok:
            correct_at.append(threshold)
        sweep[f">={threshold}"] = {
            "n_gaps": len(alt), "answers": answer, "is_correct": ok,
            "words_early": (first - answer) if answer is not None else None,
        }
    if "gap_correct_at" in expected and tuple(correct_at) != tuple(expected["gap_correct_at"]):
        raise RuntimeError(f"the gap rule is now correct at {correct_at}, not "
                           f"the recorded {list(expected['gap_correct_at'])}")
    gap_verdict = ("band" if len(correct_at) >= 2
                   else "point" if len(correct_at) == 1 else "DISAGREES")
    boundary_gap = round(words[first]["start"] - words[first - 1]["end"], 3) \
        if first > 0 else None

    # --- the corroboration verdict -----------------------------------------
    corroborated = marker_verdict in ("equality", "bound") or gap_verdict in ("band", "point")
    if marker_verdict == "DISAGREES":
        raise RuntimeError(
            f"the marker rule answers w{marker_answer}, AFTER the content "
            f"rule's w{first} — and `markers_before` is supposed to make that "
            "impossible.  Something widened the marker set; do not ship this.")
    if not corroborated and not allow_uncorroborated:
        raise RuntimeError(
            "NO INDEPENDENT WITNESS: the marker rule abstains and the gap rule "
            f"is correct at no threshold in {list(gap_sweep)}.  The family has "
            "never cut a take on the content rule alone; pin the numbers by "
            "hand and pass allow_uncorroborated=True with a written reason.")

    take_start = float(words[first]["start"])
    want("take_index", first, "take index")
    if "take_start" in expected and abs(take_start - expected["take_start"]) > 0.01:
        raise RuntimeError(f"take start moved: expected {expected['take_start']} "
                           f"got {take_start}")
    want("take_words", len(words) - first, "take length")

    # --- CLOSURE ------------------------------------------------------------
    # An inner discard marker is a STUMBLE AND IT STAYS (see the note above).
    # It is recorded, not refused, so a clerk or Miguel can find every one of
    # them in `edl.json -> inner_markers` and decide later whether a take with
    # one in it should have been re-filmed.
    inner_markers = [
        {"index": int(i), "text": words[i].get("text", ""),
         "start": round(float(words[i]["start"]), 3),
         "end": round(float(words[i]["end"]), 3),
         "context": " ".join(w.get("text", "")
                             for w in words[max(first, i - 4):i + 5])}
        for i in markers_inside]
    if inner_markers:
        print(f"  INNER STUMBLES KEPT ({len(inner_markers)}): "
              + "; ".join(f"w{m['index']} {m['text']!r} @{m['start']}"
                          for m in inner_markers), flush=True)
    if [i for i in openings if i > first]:
        raise RuntimeError("another scripted opening survives inside the chosen take")
    if not [i for i in sign_offs if i >= first]:
        raise RuntimeError("chosen take does not reach the sign-off")

    in_take_gaps = [round(words[i]["start"] - words[i - 1]["end"], 3)
                    for i in range(first + 1, len(words))]
    rec.update({
        "method": ("last scripted opening that reaches the spoken sign-off; "
                   "the content rule decides, the marker rule and the gap "
                   "sweep witness"),
        "opening_families": [list(k) if isinstance(k, (list, tuple)) else [k]
                             for k in families],
        "sign_off_key": list(sign_off_key) if isinstance(sign_off_key, (list, tuple)) else [sign_off_key],
        "openings_found": openings,
        "openings_without_truncation_arm": len(openings_no_arm),
        "truncation_arm_added": len(openings) - len(openings_no_arm),
        "sign_offs_found": len(sign_offs),
        "inner_markers": inner_markers,
        "markers_before_keeper": [int(i) for i in markers_before],
        "take_word_index": first,
        "take_words": len(words) - first,
        "raw_words": len(words),
        "take_start_s": round(take_start, 3),
        "take_text": " ".join(w["text"].strip() for w in words[first:]),
        "cross_check_marker_rule": {
            "verdict": marker_verdict,
            "answer": marker_answer,
            "markers_total": len(markers),
            "markers_before_take": len(markers_before),
            "restarts_before_take": len([i for i in openings if i <= first]),
            "under_count": (len([i for i in openings if i <= first])
                            - len(markers_before)),
            "test": "^no[.,!?]$ OR a trailing hyphen/ellipsis",
            "morphology": {"punctuated_spoken_no": len(spoken_nos),
                           "truncations": len(markers) - len(spoken_nos),
                           "total": len(markers)},
            "note": ("EQUALITY is the strongest form; BOUND is legal and "
                     "expected when abandonments carry no partial word; "
                     "ABSTAINS is legal on a raw with no markers at all."),
        },
        "cross_check_transcript_gap_rule": {
            "verdict": gap_verdict,
            "correct_thresholds": list(correct_at),
            "sweep": sweep,
            "boundary_gap_s": boundary_gap,
            "note": ("a rule correct on a BAND of thresholds is evidence; a "
                     "single correct point is not, which is why all "
                     f"{len(gap_sweep)} are recorded with the answer each gives"),
        },
        "corroboration": {
            "marker": marker_verdict, "gap": gap_verdict,
            "witnessed": bool(corroborated),
            "allow_uncorroborated": bool(allow_uncorroborated),
        },
        "closure_is_asserted": (
            f"no discard marker and no further scripted opening survives inside "
            f"w{first}..w{len(words) - 1}, and the take reaches the sign-off at "
            f"w{[i for i in sign_offs if i >= first][0]}"),
        "stutters_inside_take": 0,
        "largest_in_take_gap_s": max(in_take_gaps) if in_take_gaps else None,
        "expected_pins_asserted": sorted(expected),
    })
    return rec


# =============================================================================
# D.  THE CUT MASTER
# =============================================================================
def detect_silences(raw: Path, start: float, end: float) -> list[tuple[float, float]]:
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
         "-i", str(raw), "-af",
         f"silencedetect=noise={SILENCE_NOISE}:d={SILENCE_MIN}",
         "-vn", "-f", "null", "-"], capture_output=True, text=True, check=False)
    silences, current = [], None
    for line in result.stderr.splitlines():
        m0 = re.search(r"silence_start:\s*([0-9.]+)", line)
        if m0:
            current = float(m0.group(1))
            continue
        m1 = re.search(r"silence_end:\s*([0-9.]+)", line)
        if m1 and current is not None:
            se = float(m1.group(1))
            if se - current >= SILENCE_MIN:
                silences.append((current, se))
            current = None
    return silences


def keep_segments(duration: float, silences) -> list[tuple[float, float]]:
    segments, cursor, half = [], 0.0, SILENCE_KEEP / 2
    for start, end in silences:
        segments.append((cursor, min(duration, start + half)))
        cursor = max(0.0, end - half)
    segments.append((cursor, duration))
    return [(a, b) for a, b in segments if b - a > 0.05]


def measure_face(master: Path) -> dict:
    """MEASURED ON THIS MASTER, never inherited (build_cut_lunacheaper's rule)."""
    sys.path.insert(0, str(F / "pipeline/sam2"))
    import plate as PL  # noqa: E402
    dur = probe_duration(master)
    times = [round(dur * f, 2) for f in
             (0.05, 0.12, 0.20, 0.28, 0.36, 0.45, 0.54, 0.63, 0.72, 0.82, 0.92)]
    rows = PL.measure_framing(str(master), times, MASTER_W, MASTER_H)
    if not rows:
        raise RuntimeError("the face landmarker resolved no frame on this master")
    cx = sorted(r["face_cx_px"] for r in rows)
    hh = sorted(r["head_h_px"] for r in rows)
    tops = sorted(r["head_top_px"] for r in rows if r["head_top_px"] is not None)
    mid = len(cx) // 2
    return {
        "probes": times, "n_probes": len(rows),
        "face_cx_px": round(cx[mid], 1),
        "face_cx_min_max": [cx[0], cx[-1]],
        "head_h_median_px": round(hh[len(hh) // 2], 1),
        "cap_top_min_px": tops[0] if tops else None,
        "rows": rows,
    }


def face_plate(master: Path, out: Path, name: str, width: int, x0: int,
               out_size: tuple[int, int], face_cx: float) -> dict:
    out_w, out_h = out_size
    vf = f"crop={width}:{MASTER_H}:{x0}:0,scale={out_w}:{out_h}:flags=lanczos"
    run(["ffmpeg", "-v", "error", "-i", str(master), "-vf", vf, "-an",
         *intermediate_video_args(X264_PLATE, gop=FPS),
         "-movflags", "+faststart", str(out / name), "-y"])
    # `,`-STRIP, 2026-09-03.  ffprobe's csv row for a frame that carries an
    # empty `side_data_list` is `1,` — a trailing comma, not a second field.
    # h264_videotoolbox attaches that side data to EVERY keyframe (libx264 only
    # to frame 0), so the bare `v == "1"` test used to find NO keyframes at all
    # on a videotoolbox plate, `gaps` came out empty and the sparse-plate
    # assertion passed VACUOUSLY.  Stripping the comma makes the assertion real
    # on both encoders; on libx264 it also stops frame 0 being missed.
    flags = [row.split(",")[0] for row in subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "frame=key_frame", "-read_intervals", "%+30", "-of", "csv=p=0",
         str(out / name)], capture_output=True, text=True, check=True).stdout.split()]
    idx = [i for i, v in enumerate(flags) if v == "1"]
    gaps = [b - a for a, b in zip(idx, idx[1:])]
    if gaps and max(gaps) > 25:
        raise RuntimeError(f"{name}: keyframe gap {max(gaps)} frames > 25 "
                           "(sparse plate)")
    return {"vf": vf, "x0": x0, "width": width, "out_size": [out_w, out_h],
            "window_centre_px": x0 + width / 2,
            "offset_from_face_px": round(abs(x0 + width / 2 - face_cx), 1),
            "keyframes_in_first_30s": len(idx),
            "max_gap_frames": max(gaps) if gaps else None}


# =============================================================================
# E.  THE TIGHT TRANSCRIPT
# =============================================================================

def apply_corrections(payload: dict, vocab_path: Path = VOCAB) -> int:
    """SPELLING CORRECTIONS (Miguel, 2026-09-05: "grok always has a K, not a q").
    Scribe keeps writing "Groq" for Grok even with the keyterm hint, and the
    caption pills print whatever the transcript says.  The vocabulary carries an
    explicit `corrections` map (spoken -> written); every word is rewritten in
    place, multi-word keys match across adjacent words, punctuation is kept.
    Returns the number of words changed and records them under
    payload["corrections_applied"] so a clerk can see what was rewritten."""
    try:
        corr = (json.loads(Path(vocab_path).read_text()) or {}).get("corrections") or {}
    except Exception:                                            # noqa: BLE001
        return 0
    if not corr:
        return 0
    words = [w for w in payload.get("words", []) if w.get("type") == "word"]
    changed = []
    def core(t: str):
        m = re.match(r"^(\W*)(.*?)(\W*)$", t, re.S)
        return m.group(1), m.group(2), m.group(3)
    keys = sorted(corr, key=lambda k: -len(k.split()))
    i = 0
    while i < len(words):
        hit = False
        for k in keys:
            parts = k.split(); n = len(parts)
            if i + n <= len(words) and all(core(words[i + j]["text"])[1] == parts[j] for j in range(n)):
                reps = corr[k].split()
                if len(reps) == n:
                    for j in range(n):
                        pre, _, post = core(words[i + j]["text"])
                        old = words[i + j]["text"]; words[i + j]["text"] = pre + reps[j] + post
                        changed.append({"i": i + j, "from": old, "to": words[i + j]["text"], "start": words[i + j].get("start")})
                    i += n; hit = True; break
        if not hit:
            i += 1
    if changed:
        payload["corrections_applied"] = changed
    return len(changed)

def tight_transcript(audio_m4a: Path, out_json: Path,
                     keyterms: list[str] | None = None) -> dict:
    """Scribe v2 on the CUT audio.

    The 16 kHz mono wav Scribe wants is written to a TEMPORARY directory and
    deleted; it never lands beside the master, where a build could mix from it.
    """
    sys.path.insert(0, str(VIDEO_USE_HELPERS))
    from dotenv import load_dotenv
    import transcribe as vu  # noqa: E402
    load_dotenv(WORKSPACE / ".env")
    key = os.environ.get("ELEVENLABS_API_KEY") or vu.load_api_key()
    terms = list(vu.load_keyterms(VOCAB)) + list(keyterms or [])
    seen, deduped = set(), []
    for t in terms:
        if t and t not in seen:
            seen.add(t)
            deduped.append(t)
    with tempfile.TemporaryDirectory() as td:
        wav = Path(td) / "scribe_16k_mono.wav"
        vu.extract_audio(audio_m4a, wav)
        payload = vu.call_scribe(wav, key, language="en", num_speakers=1,
                                 keyterms=deduped[:1000])
    n_corr = apply_corrections(payload)
    if n_corr:
        print(f"[corrections] {n_corr} word(s) rewritten from the vocabulary map: "
              + ", ".join(f"{c['from']}->{c['to']}" for c in payload["corrections_applied"][:6]))
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                        encoding="utf-8")
    words = [w for w in payload.get("words", []) if w.get("type") == "word"]
    # ── THE COST LEDGER (2026-09-04) ────────────────────────────────────────
    # Scribe is the one paid call in this pipeline that returns NO cost and no
    # character count, so it was invisible in every run total.  A HAND-RUN cut
    # books it here off $SHORTS_RUN; inside prep_batch the cut stage books it
    # with the SAME ref, so the two can only replace each other.
    if os.environ.get("SHORTS_RUN"):
        try:
            sys.path.insert(0, str(F / "pipeline"))
            import costs as COSTS                                # noqa: E402
            _secs = payload.get("audio_duration_secs")
            _run = COSTS.resolve_run(os.environ["SHORTS_RUN"], out_json)
            COSTS.safe_record(
                _run, "elevenlabs", "scribe", COSTS.scribe_usd(_secs),
                video=out_json.parent.name, units=f"{_secs} s audio",
                note=f"Scribe v2 on the cut audio, {COSTS.SCRIBE_RATE_SOURCE}",
                ref=COSTS.call_ref(_run, out_json, _secs))
        except Exception as exc:                                 # noqa: BLE001
            print(f"[costs] scribe not recorded ({type(exc).__name__}: {exc})",
                  file=sys.stderr)
    return {"file": str(out_json), "words": len(words),
            "keyterms_sent": len(deduped[:1000]),
            "first_word_s": round(float(words[0]["start"]), 3) if words else None,
            "audio_duration_secs": payload.get("audio_duration_secs")}


# =============================================================================
# F.  THE WHOLE CUT
# =============================================================================
def build_cut(*, vid: str, raw: Path, raw_transcript: Path, out_dir: Path,
              sign_off_key, opening_key=None, opening_families=None,
              expected: dict | None = None,
              keyterms: list[str] | None = None,
              gap_sweep=DEFAULT_GAP_SWEEP,
              allow_uncorroborated: bool = False,
              head_lead: float = HEAD_LEAD,
              transcribe: bool = True,
              _force_take_start: tuple[float, float] | None = None,
              _false_start_round: int = 0) -> dict:
    """cuts/<id>/ — the 4K cut master, two HD face plates (delivery size), 48 kHz audio,
    the edl and the tight transcript.  Nothing here is inherited from another
    session and nothing here writes a 16 kHz analysis wav."""
    raw, out_dir = Path(raw), Path(out_dir)
    if not raw.exists():
        raise FileNotFoundError(raw)
    out_dir.mkdir(parents=True, exist_ok=True)

    words = load_words(raw_transcript)
    detection = detect_take(words, opening_key=opening_key,
                            opening_families=opening_families,
                            sign_off_key=sign_off_key, gap_sweep=gap_sweep,
                            expected=expected,
                            allow_uncorroborated=allow_uncorroborated)
    first = detection["take_word_index"]
    take_start = float(words[first]["start"])
    prev_end = float(words[first - 1]["end"]) if first else 0.0
    if _force_take_start is not None:
        # a FALSE START was found on the tight transcript of the first cut: the
        # take restarts here, and the abandoned attempt ends at prev_end.  The
        # raw Scribe pass may not have a word at this instant at all (it merged
        # the two attempts), so the raw words are not consulted for the start.
        take_start, prev_end = _force_take_start
        detection["false_start_recut"] = {
            "round": _false_start_round,
            "restart_source_s": round(take_start, 3),
            "abandoned_attempt_ends_source_s": round(prev_end, 3),
            "rule": (f"a scripted opening repeated within the first "
                     f"{FALSE_START_WINDOW_S} s of the cut; the take begins at "
                     "the LAST repeat (Miguel, 2026-09-03)")}
    try:
        head = measured_head(raw, prev_end=prev_end,
                             scribe_start=take_start, scratch=out_dir,
                             head_lead=head_lead,
                             scribe_end=(float(words[first]["end"]) if _force_take_start is None else None))
    except RuntimeError as exc:
        if "no silence run" not in str(exc):
            raise
        if _force_take_start is None:
            # THE KEEPER SAT MID-BREATH (geo, run 19, 2026-09-13).  There is no
            # silence before the keeper opening because the speaker ran into it
            # from a lead-in in the same breath.  Start the take at the head of
            # that utterance instead and measure the head there; if THAT
            # boundary has no measured silence either, the refusal stands.
            lead = utterance_lead_in(
                words, first, openings=detection.get("openings_found") or (),
                markers=discard_markers(words))
            if lead is None:
                raise
            take_start, prev_end = lead["lead_in_start_s"], lead["lead_in_prev_end_s"]
            head = measured_head(raw, prev_end=prev_end,
                                 scribe_start=take_start, scratch=out_dir,
                                 head_lead=head_lead,
                                 scribe_end=float(words[lead["lead_in_index"]]["end"]))
            lead["measured_onset_s"] = head["measured_onset_s"]
            lead["silence_run_s"] = head.get("silence_run_s")
            detection["lead_in_walk_back"] = lead
            print(f"  LEAD-IN WALK-BACK: the take starts at w{lead['lead_in_index']} "
                  f"{' '.join(lead['lead_in_words'])!r} @{lead['lead_in_start_s']}, "
                  f"{lead['boundary_gap_s']}s after the previous word, not at the "
                  f"keeper w{first} @{lead['keeper_start_s']}", flush=True)
        else:
            # an immediate restart may have no measurable silence before it; the
            # head then sits just after the abandoned word and before the restart
            head = {
                "measured_onset_s": round(take_start, 3),
                "head_s": round(max(prev_end + 0.06, take_start - head_lead), 3),
                "onset_rule": "restart with no silence run: head = max(prev_end + 0.06, restart - head_lead)",
                "silence_run_duration_s": 0.0}
    env_equality = abs(head["measured_onset_s"] - take_start)
    if _force_take_start is not None:
        # A RESTART has no clean silence before it: the abandoned attempt ends
        # a few hundred ms earlier and a breath or click often sits in the gap,
        # so the envelope's onset and the tight-Scribe start disagree by more
        # than the 0.20 s gate (astramath: 0.30 s).  The head is placed so it
        # never includes the abandoned word (>= prev_end + 0.06) and never
        # clips the restart (<= its Scribe start - head_lead); inside that band
        # the envelope onset wins.  Drift up to 0.5 s is recorded, not fatal.
        if env_equality > 0.50:
            raise RuntimeError(
                f"false-start recut: envelope onset {head['measured_onset_s']} "
                f"vs restart {take_start} disagree by {env_equality:.2f} s")
        lo, hi = prev_end + 0.06, take_start - head_lead
        head["head_s"] = round(min(max(head["measured_onset_s"], lo), hi), 3) if lo <= hi else round(hi, 3)
        head["restart_head_rule"] = (f"head clamped to [{lo:.3f}, {hi:.3f}] "
                                     f"(abandoned word end + 0.06, restart - head_lead)")
    elif env_equality > 0.20 and not head.get("scribe_start_inside_silence_drift_s"):
        raise RuntimeError(
            f"cross-check 2b drifted: envelope onset {head['measured_onset_s']} "
            f"vs Scribe start {take_start}")
    elif head.get("scribe_start_inside_silence_drift_s"):
        detection["scribe_start_inside_silence"] = {
            "scribe_start_s": round(take_start, 3), "measured_onset_s": head["measured_onset_s"],
            "drift_s": head["scribe_start_inside_silence_drift_s"],
            "rule": "Scribe placed the first word inside measured silence; the audio onset wins, head before it"}
    detection["head_measurement"] = head
    detection["cross_check_envelope_gap_rule"] = (
        f"the end of the last >= {SILENCE_RUN_MIN}s silence run in a 10ms-window "
        f"RMS envelope is {head['measured_onset_s']}s, which is "
        f"{round(env_equality, 3)}s from the winner's Scribe start ({take_start}s). "
        f"The run itself is {head['silence_run_duration_s']}s long.")

    raw_duration = probe_duration(raw)
    start = head["head_s"]
    end = min(raw_duration - EOF_GUARD, float(words[-1]["end"]) + TAIL_PAD)
    duration = end - start

    silences = detect_silences(raw, start, end)
    if silences and silences[-1][1] >= duration - 0.12:
        tail_start = silences[-1][0]
        detection["trailing_silence_tail"] = {
            "rule": "trailing silence ends the take: cut at voice_end + TAIL_HOLD",
            "voice_end_source_s": round(start + tail_start, 3),
            "tail_hold_s": TAIL_HOLD}
        duration = min(duration, tail_start + TAIL_HOLD)
        end = start + duration
        silences = silences[:-1]
    # LAW 47 hard cap: never more than TAIL_HOLD after the last spoken word
    last_word_end = float(words[-1]["end"])
    if end > last_word_end + TAIL_HOLD:
        detection["tail_cap"] = {"rule": "LAW 47: end = last word end + TAIL_HOLD",
                                 "was_end_s": round(end, 3),
                                 "end_s": round(last_word_end + TAIL_HOLD, 3)}
        end = last_word_end + TAIL_HOLD
        duration = end - start
        silences = [s_ for s_ in silences if s_[0] < duration]
    segments = keep_segments(duration, silences)

    filters, concat_inputs = [], []
    for i, (a, b) in enumerate(segments):
        s0, s1 = start + a, start + b
        filters.append(
            f"[0:v]trim=start={s0:.3f}:end={s1:.3f},setpts=PTS-STARTPTS[v{i}];"
            f"[0:a]atrim=start={s0:.3f}:end={s1:.3f},asetpts=PTS-STARTPTS[a{i}]")
        concat_inputs.append(f"[v{i}][a{i}]")
    graph = ";".join(filters) + ";" + "".join(concat_inputs)
    graph += f"concat=n={len(segments)}:v=1:a=1[v][a]"

    master = out_dir / "master.mp4"
    run(["ffmpeg", "-v", "error", "-i", str(raw), "-filter_complex", graph,
         "-map", "[v]", "-map", "[a]", "-r", str(FPS),
         *intermediate_video_args(X264_MASTER),
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
         str(master), "-y"])

    # THE FACE MEASUREMENT STAYS AHEAD OF THE PLATES.  face_cx decides both
    # crop windows, so it cannot be measured beside them.
    fm = measure_face(master)
    face_cx = fm["face_cx_px"]
    full_x0 = max(0, min(MASTER_W - FULL_W,
                         int(round(face_cx - FULL_W / 2)) & ~1))
    bottom_x0 = max(0, min(MASTER_W - BOTTOM_W,
                           int(round(face_cx - BOTTOM_W / 2)) & ~1))

    # THE POST-MASTER CHORES RUN TOGETHER.  Both plates read the finished
    # master and nothing else; the 48 kHz audio reads the finished master and
    # the tight transcript reads that audio, so the audio and Scribe are ONE
    # task and the three tasks are independent.  They are subprocess- and
    # network-bound, which is why threads are enough.
    def _audio_then_transcript():
        # 48 kHz stereo ONLY.  No 16 kHz analysis wav beside the master.
        run(["ffmpeg", "-v", "error", "-i", str(master), "-vn",
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
             str(out_dir / "audio.m4a"), "-y"])
        if not transcribe:
            return None
        return tight_transcript(out_dir / "audio.m4a",
                                out_dir / "transcript_tight.json", keyterms)

    with ThreadPoolExecutor(max_workers=3) as pool:
        f_bottom = pool.submit(face_plate, master, out_dir,
                               "face_bottom_hd.mp4", BOTTOM_W, bottom_x0,
                               BOTTOM_PLATE, face_cx)
        f_full = pool.submit(face_plate, master, out_dir, "face_full_hd.mp4",
                             FULL_W, full_x0, FULL_PLATE, face_cx)
        f_audio = pool.submit(_audio_then_transcript)
        faces = {"face_bottom_hd.mp4": f_bottom.result(),
                 "face_full_hd.mp4": f_full.result()}
        tight = f_audio.result()

    cut_dur = probe_duration(master)
    edl = {
        "vid": vid,
        "source": str(raw),
        "source_take_start": round(start, 3),
        "source_take_end": round(end, 3),
        "source_take_duration": round(duration, 3),
        "cut_master_duration": round(cut_dur, 3),
        "cut_fps": FPS,
        "cut_audio": probe(master, "stream=sample_rate,channels", "a:0").replace("\n", " "),
        "face_measurement": {**{k: v for k, v in fm.items() if k != "rows"},
                             "windows": faces,
                             "note": ("windows are MEASURED on THIS cut master, "
                                      "never inherited")},
        "face_probe_rows": fm["rows"],
        "take_detection": detection,
        "silence_noise": SILENCE_NOISE,
        "silence_min": SILENCE_MIN,
        "silence_keep": SILENCE_KEEP,
        "micro_cuts_source": [],
        "detected_silences": [{"start": round(a, 3), "end": round(b, 3)}
                              for a, b in silences],
        "keep_segments": [
            {"tight_start": round(sum(y - x for x, y in segments[:i]), 3),
             "source_start": round(start + a, 3), "source_end": round(start + b, 3)}
            for i, (a, b) in enumerate(segments)],
        "edl_keep_segments_duration_s": round(sum(b - a for a, b in segments), 3),
        "audio_sync_offset_ms": 0,
        "audio_written": ["audio.m4a (48 kHz stereo)"],
        "analysis_wav_written": False,
        "mix_source": "audio.m4a (48 kHz stereo) — there is no 16 kHz file here",
        "raw_duration": round(raw_duration, 3),
    }
    if transcribe:
        edl["tight_transcript"] = tight
        # FALSE-START VERIFICATION on the tight transcript (the one that heard
        # every word of the cut).  If the scripted opening occurs more than once
        # inside FALSE_START_WINDOW_S, the earlier occurrences are abandoned
        # attempts and the cut is redone from the last one.  One round.
        families = list(opening_families) if opening_families else [opening_key]
        twords = load_words(Path(tight["file"]))
        # match on the family's first FALSE_START_PREFIX tokens, not the whole
        # key: an abandoned attempt is by definition shorter than the key
        # ("GPT Astra solved," then the restart), so the full key only ever
        # finds the keeper.  The truncation arm on the prefix's last token
        # still catches an attempt that dies inside that word.
        prefixes = [tuple(k)[:FALSE_START_PREFIX] if isinstance(k, (list, tuple))
                    else (k,) for k in families]
        # A RESTART, not a rhetorical repeat (viberesearch, run 13: "You've
        # heard about vibe coding, but have you heard about vibe researching"
        # repeats the prefix INSIDE one sentence and is the keeper itself).
        # The keeper is the prefix hit that ALSO matches the full opening key;
        # an abandoned attempt is a prefix hit BEFORE the keeper that does not,
        # with at most one word between its prefix and the keeper's start.
        full_hits = set(opening_indexes_multi(twords, families))
        pref_hits = [i for i in opening_indexes_multi(twords, prefixes)
                     if float(twords[i]["start"]) < FALSE_START_WINDOW_S]
        keepers = [i for i in pref_hits if i in full_hits]
        keeper = keepers[0] if keepers else None
        abandoned = [i for i in pref_hits
                     if keeper is not None and i < keeper and i not in full_hits
                     and keeper - (i + FALSE_START_PREFIX) <= 1]
        reps = abandoned + ([keeper] if keeper is not None and abandoned else [])
        if len(reps) >= 2 and _false_start_round == 0:
            def to_source(t_tight: float) -> float:
                cum = 0.0
                for a, b in segments:
                    if t_tight < cum + (b - a) + 1e-6:
                        return start + a + (t_tight - cum)
                    cum += b - a
                return start + segments[-1][1]
            last = reps[-1]
            restart_src = to_source(float(twords[last]["start"]))
            aband_end_src = to_source(float(twords[last - 1]["end"]))
            edl["false_start_found"] = {
                "repeats_in_window": len(reps),
                "tight_starts_s": [round(float(twords[i]["start"]), 2) for i in reps],
                "restart_source_s": round(restart_src, 3),
                "abandoned_attempt_ends_source_s": round(aband_end_src, 3),
                "action": "recut from the last repeat"}
            return build_cut(vid=vid, raw=raw, raw_transcript=raw_transcript,
                             out_dir=out_dir, sign_off_key=sign_off_key,
                             opening_key=opening_key,
                             opening_families=opening_families,
                             expected=expected, keyterms=keyterms,
                             gap_sweep=gap_sweep,
                             allow_uncorroborated=allow_uncorroborated,
                             head_lead=head_lead, transcribe=transcribe,
                             _force_take_start=(restart_src, aband_end_src),
                             _false_start_round=1)
        elif len(reps) >= 2:
            raise RuntimeError(
                f"FALSE START still present after the recut: opening repeats at "
                f"tight {[round(float(twords[i]['start']), 2) for i in reps]} s")
    (out_dir / "edl.json").write_text(json.dumps(edl, indent=2), encoding="utf-8")
    return edl


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--vid", required=True)
    ap.add_argument("--raw", required=True, type=Path)
    ap.add_argument("--raw-transcript", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--opening", required=True,
                    help="comma-separated key tokens; use a|b for alternatives")
    ap.add_argument("--sign-off", required=True, help="same shape")
    ap.add_argument("--keyterms", default="")
    ap.add_argument("--no-transcribe", action="store_true")
    a = ap.parse_args()
    key = lambda s: tuple(tuple(t.split("|")) for t in s.split(","))  # noqa: E731
    print(json.dumps(build_cut(
        vid=a.vid, raw=a.raw, raw_transcript=a.raw_transcript, out_dir=a.out,
        opening_key=key(a.opening), sign_off_key=key(a.sign_off),
        keyterms=[t for t in a.keyterms.split(",") if t],
        transcribe=not a.no_transcribe,
    ), indent=1)[:4000])
