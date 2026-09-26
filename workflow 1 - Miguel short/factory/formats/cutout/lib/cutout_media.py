"""THE VOICE SOURCE, and the treble check that proves it was used.

Imported by the cutout chassis and — because every backfill generator imports
`cutout_core` out of this same directory — by the whole backfill fleet.

=============================================================================
WHY THIS FILE EXISTS  (defect 2, Miguel, 2026-09-01)
=============================================================================

`publish_batch.py` copies the cut's `audio.wav` into every published package as
`source_audio.wav`.  That wav is the ANALYSIS track: 16 kHz mono, the rate
Scribe wants, and therefore a track with NOTHING above 8 kHz — a 16 kHz sample
rate has an 8 kHz Nyquist limit.  Ten of the thirteen cutout remakes mixed their
voice from it, so ten shorts shipped with the top octave of his voice amputated.

Measured on `deepresearch`, 8-16 kHz band power relative to full-band power
(`band_db` below):

    cut master  audio.m4a  48 kHz stereo      -30.6 dB
    published   original short                -31.2 dB      0.6 dB off master
    remake      cutout, mixed from the wav    -49.0 dB     18.4 dB off master

The fix has three parts and all three live here or next door:

1.  `resolve_voice` picks the FULL-QUALITY track and REFUSES a low-rate one,
    with the correct file named in the error.  A silent downgrade is how this
    happened; there is no fallback that quietly accepts 16 kHz.
2.  The analysis wav is renamed `analysis_16k_mono_DO_NOT_MIX.wav` in the
    package convention (`shorts_run*/publish/publish_batch.py`), so the old
    filename cannot be reached for by habit.  `resolve_voice` rejects BOTH names
    anyway — the rename is a guardrail, not the guard.
3.  `assert_treble_parity` is a build/QC gate: the 8-16 kHz band of the finished
    mix must sit within 6 dB of the voice master's own 8-16 kHz band.

WHY THE BAND IS MEASURED RELATIVE TO FULL BAND and not in dBFS: a mix is
normalised and a raw voice track is not, so absolute levels differ by the
mastering gain and say nothing.  The RATIO of treble to total is what an 8 kHz
brick wall destroys, and it is invariant to gain.  The window is 4096 samples,
Hann, hop 2048, averaged over the whole file.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import numpy as np

# The names a package may carry for the real voice, best first.  `audio.m4a` is
# what `cuts/<id>/` holds (AAC 48 kHz stereo, ~192 kbps); the two master videos
# carry the same 48 kHz track and are valid sources when the m4a was not copied.
VOICE_CANDIDATES = ("voice_master_48k.m4a", "voice_master.m4a", "audio.m4a",
                    "source_cut_master.mp4", "master.mp4", "face_full_hd.mp4")

# Names that are NEVER a mix source.  Both spellings are refused: the old one
# because it is the actual defect, the new one because it says so out loud.
ANALYSIS_NAMES = ("analysis_16k_mono_DO_NOT_MIX.wav", "source_audio.wav")

MIN_RATE = 44100        # below this, the top octave of speech is already gone
TREBLE_BAND = (8000.0, 16000.0)
TREBLE_TOL_DB = 6.0


# ------------------------------------------------------------------ probing
def probe_wh(path: Path) -> tuple[int, int]:
    """The ENCODED pixel dimensions of a video's first stream.

    The authority for the cutout layer's CSS box: a layer painted into anything
    other than its own encoded size is resampled every frame, which is exactly
    how `grokprice` lost 13 % of its face detail (`chassis_gen.guard_plate_box`).
    """
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height", "-of", "json", str(path)],
        capture_output=True, text=True, check=True).stdout
    st = (json.loads(out).get("streams") or [])
    if not st:
        raise SystemExit(f"{path} carries no video stream")
    return int(st[0]["width"]), int(st[0]["height"])


def audio_stream(path: Path) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
         "stream=codec_name,sample_rate,channels,bit_rate", "-of", "json",
         str(path)], capture_output=True, text=True, check=True).stdout
    st = json.loads(out).get("streams") or []
    if not st:
        raise SystemExit(f"{path} carries no audio stream")
    s = st[0]
    return dict(codec=s.get("codec_name"), rate=int(s.get("sample_rate", 0)),
                channels=int(s.get("channels", 0)),
                bit_rate=int(s["bit_rate"]) if s.get("bit_rate") else None)


def resolve_voice(src: Path) -> tuple[Path, dict]:
    """The full-quality voice for a package, or a SystemExit that names the fix.

    Deliberately not forgiving.  The whole defect was a pipeline that accepted
    whatever `source_audio.wav` happened to be, so this refuses every low-rate
    candidate instead of degrading to it.
    """
    for name in VOICE_CANDIDATES:
        p = src / name
        if not p.exists():
            continue
        st = audio_stream(p)
        if st["rate"] >= MIN_RATE:
            return p, st
        print(f"  skipping {name}: {st['rate']} Hz, below the {MIN_RATE} Hz "
              f"floor", flush=True)
    present = sorted(q.name for q in src.iterdir()) if src.is_dir() else []
    stale = [n for n in ANALYSIS_NAMES if (src / n).exists()]
    raise SystemExit(
        f"no full-quality voice in {src}.\n"
        f"  looked for: {', '.join(VOICE_CANDIDATES)}\n"
        f"  found:      {', '.join(present) or '(nothing)'}\n"
        + (f"  {stale[0]} is the 16 kHz mono ANALYSIS track and is never a mix "
           f"source — see cutout_media.py.\n" if stale else "")
        + "  Copy the cut's 48 kHz voice in as voice_master_48k.m4a:\n"
          "    cp <run>/cuts/<id>/audio.m4a <package>/src/voice_master_48k.m4a")


def stage_voice(src: Path, stage_dir: Path, bitrate: str = "192k") -> dict:
    """Transcode the resolved voice to `stage/v/voice.m4a`.

    THE STALE STAGED ASSET IS THE TRAP, AND IT BIT THIS EXACT FILE.  The first
    run of the fixed pipeline resolved the correct 48 kHz master and then kept
    the staged `voice.m4a` anyway, because the mtime rule the matte uses ("only
    re-copy when the staged file is OLDER") said the 16 kHz file already there
    was newer.  The chassis reported the right source in its record and shipped
    the wrong audio — the same class of silent failure as the defect itself.

    So staging is guarded three ways, in order of how load-bearing they are:

      1.  a STAMP of the source path, so any change of source forces a rebuild
          regardless of mtimes;
      2.  a RATE check on the staged file itself, not on the source;
      3.  a BAND check on the staged file against the source, which is the only
          one of the three that can catch a resample that kept the container's
          sample rate but threw the content away.

    Failing 2 or 3 rebuilds once and re-checks; failing twice is fatal.
    """
    voice = stage_dir / "v/voice.m4a"
    voice.parent.mkdir(parents=True, exist_ok=True)
    stamp = stage_dir / "v/_voice_source.txt"
    picked, st = resolve_voice(src)
    src_band = band_db(picked)

    def build():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(picked),
                        "-vn", "-c:a", "aac", "-b:a", bitrate, "-ar", "48000",
                        str(voice)], check=True)
        stamp.write_text(str(picked))

    if (not voice.exists()
            or not stamp.exists()
            or stamp.read_text().strip() != str(picked)
            or voice.stat().st_mtime < picked.stat().st_mtime):
        build()
    for attempt in (1, 2):
        got = audio_stream(voice)
        band = band_db(voice)
        if got["rate"] >= MIN_RATE and abs(band - src_band) <= TREBLE_TOL_DB:
            break
        if attempt == 2:
            raise SystemExit(
                f"the staged voice is still wrong after a rebuild: "
                f"{got['rate']} Hz, 8-16 kHz band {band} dB against the source's "
                f"{src_band} dB ({picked.name}).  Delete {voice} and re-run.")
        print(f"  staged voice is stale ({got['rate']} Hz, band {band} dB) — "
              f"rebuilding from {picked.name}", flush=True)
        build()
    return dict(source=str(picked), source_name=picked.name, **st,
                staged=str(voice), staged_rate=got["rate"],
                source_band_8_16k_db=src_band, staged_band_8_16k_db=band)


# ------------------------------------------------------------------- bands
def _pcm(path: Path, sr: int = 48000) -> np.ndarray:
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1",
         "-ar", str(sr), "-f", "f32le", "-"],
        capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def band_db(path: Path, lo: float = TREBLE_BAND[0], hi: float = TREBLE_BAND[1],
            sr: int = 48000, n: int = 4096) -> float:
    """Power in [lo, hi) as dB relative to the whole 20 Hz .. Nyquist band."""
    x = _pcm(path, sr)
    hop = n // 2
    if len(x) < n * 2:
        raise SystemExit(f"{path} is too short to measure")
    w = np.hanning(n)
    frames = np.stack([x[i:i + n] * w for i in range(0, len(x) - n, hop)])
    P = np.mean(np.abs(np.fft.rfft(frames, axis=1)) ** 2, axis=0)
    f = np.fft.rfftfreq(n, 1 / sr)
    full = P[(f >= 20) & (f < sr / 2)].sum()
    band = P[(f >= lo) & (f < hi)].sum()
    return round(float(10 * np.log10(max(band, 1e-30) / max(full, 1e-30))), 2)


def assert_treble_parity(mix: Path, voice_master: Path,
                         tol_db: float = TREBLE_TOL_DB) -> dict:
    """GATE: the finished mix must keep the voice master's 8-16 kHz band.

    A 16 kHz-sourced mix fails this by ~18 dB, which is not a subtle margin —
    the tolerance is 6 dB so that legitimate mixing (the music bed, the AAC
    encode, loudness normalisation) never trips it while an amputated top
    octave always does.
    """
    m = band_db(mix)
    v = band_db(voice_master)
    rec = dict(mix=str(mix), mix_8_16k_db=m, master=str(voice_master),
               master_8_16k_db=v, delta_db=round(m - v, 2), tol_db=tol_db,
               ok=abs(m - v) <= tol_db)
    if not rec["ok"]:
        raise SystemExit(
            f"TREBLE GATE FAILED: the mix's 8-16 kHz band is {m} dB against the "
            f"voice master's {v} dB ({rec['delta_db']:+} dB, tolerance "
            f"{tol_db}).\nThe mix was almost certainly built from the 16 kHz "
            f"mono analysis track (Nyquist 8 kHz).  See cutout_media.py.")
    return rec


# ----------------------------------------------------- the plate's own face HF
def plate_hf_reference(matte: Path) -> dict | None:
    """The face-HF of the plate the matte was cut from, cached beside it.

    The face-HF gate needs a reference that belongs to THIS video, not to some
    other short: "the render carries the detail its own plate carries".  The
    plate is not a chassis input, but `ship.py` records it, so the reference is
    read out of the matte's `*_ship.json` sibling.

    Cached in `<plate>.facehf.json` because the measurement costs a handful of
    ffmpeg seeks plus a mediapipe load, and the plate never changes once cut.
    Returns None when there is no ship record — the gate then reports instead of
    failing, which is the right behaviour for a matte that predates v5.
    """
    import cutout_facehf as FH
    ship = None
    for q in matte.parent.glob("*_ship.json"):
        try:
            rec = json.loads(q.read_text())
        except Exception:
            continue
        outs = rec.get("outputs") or {}
        if matte.name in {Path(v).name for v in outs.values()}:
            ship = rec
            break
    if ship is None:
        return None
    ref = ship.get("display_plate") or ship.get("plate")
    if not ref:
        return None
    pl = Path(ref)
    if not pl.is_absolute():
        pl = (matte.parent.parent.parent / ref)      # ship.py records session-relative
    if not pl.exists():
        return None
    cache = pl.with_suffix(pl.suffix + ".facehf.json")
    if cache.exists() and cache.stat().st_mtime >= pl.stat().st_mtime:
        return json.loads(cache.read_text())
    r = FH.face_hf(str(pl), k=FH.K_SKIN)
    out = dict(plate=str(pl), k=FH.K_SKIN, face_hf=r["face_hf"])
    cache.write_text(json.dumps(out, indent=1))
    return out
