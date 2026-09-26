#!/usr/bin/env bash
# Download the release media archives, verify them, and unpack them at the repo root.
# Needs: gh (logged in with access to this repo), shasum, tar.
set -euo pipefail
TAG="${1:-media-2026-09-26}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DL="$ROOT/.media-download"
mkdir -p "$DL"
cd "$DL"
gh release download "$TAG" --repo "$(cd "$ROOT" && gh repo view --json nameWithOwner -q .nameWithOwner)" --clobber
shasum -a 256 -c SHA256SUMS
for t in media-*.tar; do
  echo "unpacking $t"
  tar -xf "$t" -C "$ROOT"
done
echo "done. You can delete $DL to reclaim space."
