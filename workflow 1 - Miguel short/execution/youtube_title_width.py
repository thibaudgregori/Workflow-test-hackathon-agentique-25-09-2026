#!/usr/bin/env python3
"""Measure YouTube title display width using Nick's demonstrated checker profile.

The profile is calibrated to the example shown in Nick's audit:
"How to Go Viral on LinkedIn in 2025 Using Claude and Antigravity" = 624 px.
Titles pass only when they are at most 600 display pixels and at most the
YouTube API's 100-character hard limit.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path

from PIL import ImageFont


PROFILE_NAME = "nick-cmt-v1"
DEFAULT_MAX_WIDTH_PX = 600.0
DEFAULT_MAX_CHARACTERS = 100
BASE_FONT_SIZE = 28
REFERENCE_TITLE = "How to Go Viral on LinkedIn in 2025 Using Claude and Antigravity"
REFERENCE_WIDTH_PX = 624.0

FONT_CANDIDATES = (
    Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
    Path("/Library/Fonts/Arial.ttf"),
    Path("/usr/share/fonts/truetype/msttcorefonts/Arial.ttf"),
    Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
)


@dataclass(frozen=True)
class TitleAudit:
    """Deterministic title-width and character-limit result."""

    title: str
    width_px: float
    max_width_px: float
    characters: int
    max_characters: int
    passes_width: bool
    passes_characters: bool
    ok: bool
    profile: str
    font_path: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def resolve_font_path(font_path: str | Path | None = None) -> Path:
    """Resolve an Arial-compatible local font without downloading anything."""
    requested = font_path or os.environ.get("YOUTUBE_TITLE_FONT")
    if requested:
        path = Path(requested).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"Title font not found: {path}")
        return path

    for candidate in FONT_CANDIDATES:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        "No Arial-compatible font found. Set YOUTUBE_TITLE_FONT to a local .ttf file."
    )


@lru_cache(maxsize=8)
def _load_font(font_path: str) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(font_path, BASE_FONT_SIZE)


def _raw_width(title: str, font_path: Path) -> float:
    return float(_load_font(str(font_path)).getlength(title))


def measure_title_width(title: str, font_path: str | Path | None = None) -> float:
    """Return Nick-checker-compatible display pixels for one title.

    Pillow measures the Arial glyphs. A fixed profile calibration reproduces
    the 624 px result visible in Nick's audit while retaining the relative
    width of narrow and wide characters. This is deliberately not a character
    count proxy.
    """
    resolved = resolve_font_path(font_path)
    reference_raw = _raw_width(REFERENCE_TITLE, resolved)
    if reference_raw <= 0:
        raise RuntimeError(f"Font produced an invalid reference width: {resolved}")
    scale = REFERENCE_WIDTH_PX / reference_raw
    return round(_raw_width(title, resolved) * scale, 1)


def audit_youtube_title(
    title: str,
    *,
    max_width_px: float = DEFAULT_MAX_WIDTH_PX,
    max_characters: int = DEFAULT_MAX_CHARACTERS,
    font_path: str | Path | None = None,
) -> TitleAudit:
    """Audit a title without raising for ordinary validation failures."""
    cleaned = str(title).strip()
    resolved = resolve_font_path(font_path)
    width_px = measure_title_width(cleaned, resolved)
    characters = len(cleaned)
    passes_width = bool(cleaned) and width_px <= max_width_px
    passes_characters = bool(cleaned) and characters <= max_characters
    return TitleAudit(
        title=cleaned,
        width_px=width_px,
        max_width_px=float(max_width_px),
        characters=characters,
        max_characters=int(max_characters),
        passes_width=passes_width,
        passes_characters=passes_characters,
        ok=passes_width and passes_characters,
        profile=PROFILE_NAME,
        font_path=str(resolved),
    )


def validate_youtube_title(
    title: str,
    *,
    max_width_px: float = DEFAULT_MAX_WIDTH_PX,
    max_characters: int = DEFAULT_MAX_CHARACTERS,
    font_path: str | Path | None = None,
) -> TitleAudit:
    """Return the audit or raise an actionable ValueError."""
    audit = audit_youtube_title(
        title,
        max_width_px=max_width_px,
        max_characters=max_characters,
        font_path=font_path,
    )
    failures: list[str] = []
    if not audit.title:
        failures.append("title is empty")
    elif not audit.passes_width:
        failures.append(
            f"display width is {audit.width_px:.1f}px / {audit.max_width_px:.1f}px "
            f"({audit.width_px - audit.max_width_px:.1f}px over)"
        )
    if audit.title and not audit.passes_characters:
        failures.append(
            f"character count is {audit.characters} / {audit.max_characters} "
            f"({audit.characters - audit.max_characters} over)"
        )
    if failures:
        raise ValueError(
            "YouTube title failed preflight: "
            + "; ".join(failures)
            + ". Shorten or rewrite it; never rely on YouTube truncation."
        )
    return audit


def _collect_titles(args: argparse.Namespace) -> list[str]:
    titles = list(args.titles)
    if args.file:
        titles.extend(
            line.strip()
            for line in args.file.expanduser().read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    if not titles and not sys.stdin.isatty():
        titles.extend(line.strip() for line in sys.stdin if line.strip())
    return titles


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit YouTube titles against Nick's 600-pixel display-width rule."
    )
    parser.add_argument("titles", nargs="*", help="One or more quoted title candidates")
    parser.add_argument("--file", type=Path, help="Text file with one title per line")
    parser.add_argument("--font", type=Path, help="Override the local Arial-compatible .ttf")
    parser.add_argument("--max-pixels", type=float, default=DEFAULT_MAX_WIDTH_PX)
    parser.add_argument("--max-characters", type=int, default=DEFAULT_MAX_CHARACTERS)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    titles = _collect_titles(args)
    if not titles:
        parser.error("provide at least one title, --file, or newline-delimited stdin")

    audits = [
        audit_youtube_title(
            title,
            max_width_px=args.max_pixels,
            max_characters=args.max_characters,
            font_path=args.font,
        )
        for title in titles
    ]
    if args.json:
        print(json.dumps({"profile": PROFILE_NAME, "titles": [row.to_dict() for row in audits]}, indent=2))
    else:
        for row in audits:
            status = "PASS" if row.ok else "FAIL"
            print(
                f"{status}  {row.width_px:.1f}/{row.max_width_px:.0f}px  "
                f"{row.characters}/{row.max_characters} chars  {row.title}"
            )
    raise SystemExit(0 if all(row.ok for row in audits) else 1)


if __name__ == "__main__":
    main()
