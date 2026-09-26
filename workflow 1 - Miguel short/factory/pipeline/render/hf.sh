#!/usr/bin/env bash
# hf.sh — the factory's ONLY laptop entry point to the HyperFrames CLI.
#
# WHY THIS FILE EXISTS (2026-09-03)
# ---------------------------------
# `npx hyperframes` resolves the npm `latest` tag on every call.  `latest` was
# 0.7.107 when the Modal image was built and is 0.8.26 today, so a laptop
# render placed through `npx` is a different renderer from one placed an
# afternoon earlier, and the first symptom is a parity or audio check failing
# for a reason that has nothing to do with the composition.
#
# The version that actually wrote every approved master in run 9 is the
# agent-tools checkout's built `dist`, which reports **0.7.71**.  That is the
# pin.  It is not a new version to prove — it is the one already on disk, the
# one Miguel approved renders from, and the one the guards are calibrated to.
#
# THE ONE THING 0.7.71 DOES THAT LATER BUILDS DO NOT.  Its mux passes
# `-avoid_negative_ts make_zero`, which discards the AAC sidecar's priming edit
# list.  HyperFrames' mixer places the voice 1024 samples early on its own
# timeline, so that undischarged priming is what puts the voice back onto the
# picture's timeline: `qc_pass`'s `audio_guards` measures 0 ms on a 0.7.71
# render and -20 ms on a 0.7.107 one, of the same project, on this same
# laptop.  The container reproduces the 0.7.71 delivered container explicitly
# (`modal_app._normalize_delivery_audio`).  This script asserts the result.
#
# USE
#   F=~/Documents/Workspace/projects/personal/content/shorts-factory
#   $F/pipeline/render/hf.sh render PROJECT -o OUT.mp4 -q high
#   $F/pipeline/render/hf.sh --version
#
# OVERRIDES (both are deliberate, both are loud)
#   HF_BIN=/path/to/hyperframes.mjs   run that binary instead of the checkout
#   HF_PIN=0.7.71                     the version this script insists on
#   HF_ALLOW_VERSION_DRIFT=1          downgrade the version assert to a warning
set -euo pipefail

HF_PIN="${HF_PIN:-0.7.71}"
CHECKOUT="$HOME/Documents/Workspace/projects/personal/infra/agent-tools/hyperframes/packages/cli/bin/hyperframes.mjs"

# The broken-IPv6 fault on this laptop (`reference_macbook_broken_ipv6`): node's
# registry/DNS path hangs where curl does not.  Harmless when it is not needed.
export NODE_OPTIONS="${NODE_OPTIONS:-} --dns-result-order=ipv4first"
export HYPERFRAMES_NO_TELEMETRY=1
export HYPERFRAMES_NO_UPDATE_CHECK=1

if [[ -n "${HF_BIN:-}" ]]; then
  RUN=(node "$HF_BIN")
elif [[ -f "$CHECKOUT" ]]; then
  RUN=(node "$CHECKOUT")
else
  # Last resort, and still pinned: never the bare `npx hyperframes`.
  RUN=(npx --yes "hyperframes@${HF_PIN}")
fi

GOT="$("${RUN[@]}" --version 2>/dev/null | tr -d '[:space:]')"
if [[ "$GOT" != "$HF_PIN" ]]; then
  MSG="hf.sh: resolved HyperFrames ${GOT:-<none>}, factory pin is ${HF_PIN} (${RUN[*]})"
  if [[ "${HF_ALLOW_VERSION_DRIFT:-0}" == "1" ]]; then
    echo "WARNING: $MSG" >&2
  else
    echo "ERROR: $MSG" >&2
    echo "  The agent-tools checkout's dist is the pin.  Rebuild it, set HF_BIN," >&2
    echo "  or set HF_ALLOW_VERSION_DRIFT=1 and re-prove qc_pass audio_guards." >&2
    exit 3
  fi
fi

"${RUN[@]}" "$@"
RC=$?

# THE DELIVERY ASSERT.  A render whose MP4 carries an AAC priming edit list is
# a render that will measure -20 ms on `audio_guards`.  Catch it here, at the
# moment it is written, rather than three checks later.
if [[ $RC -eq 0 && "${1:-}" == "render" ]]; then
  OUT=""
  PREV=""
  for a in "$@"; do
    if [[ "$PREV" == "-o" || "$PREV" == "--output" ]]; then OUT="$a"; fi
    PREV="$a"
  done
  if [[ -n "$OUT" && -f "$OUT" && "$OUT" == *.mp4 ]]; then
    PAD="$(ffprobe -v error -select_streams a:0 -show_entries stream=initial_padding \
             -of csv=p=0 "$OUT" 2>/dev/null | tr -d '[:space:]')"
    if [[ -n "$PAD" && "$PAD" != "0" ]]; then
      echo "ERROR: $OUT carries an AAC priming edit list (initial_padding=$PAD)." >&2
      echo "  qc_pass audio_guards will measure -20 ms on it.  The CLI that wrote" >&2
      echo "  it does not pass -avoid_negative_ts make_zero on the audio mux;" >&2
      echo "  see pipeline/render/README.md." >&2
      exit 4
    fi
  fi
fi

exit $RC
