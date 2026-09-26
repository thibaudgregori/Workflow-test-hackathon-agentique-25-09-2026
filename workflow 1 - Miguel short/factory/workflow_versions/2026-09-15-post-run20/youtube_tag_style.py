#!/usr/bin/env python3
"""Canonical YouTube tag casing shared by upload and backfill workflows."""

from __future__ import annotations

import re
from collections.abc import Iterable


LOWERCASE_JOINERS = {
    "a", "an", "and", "at", "for", "from", "in", "of", "on", "or",
    "the", "to", "vs", "with",
}

EXACT_TOKENS = {
    value.casefold(): value
    for value in (
        "3D", "AI", "API", "APIs", "CLI", "DOE", "GPT", "GPTs", "KPIs",
        "LLM", "LLMs", "MCP", "MCPs", "OpenAI", "RAG", "UI", "xAI", "YC",
        "ChatGPT", "MakerSchool", "TheirStack", "YouTube", "n8n",
    )
}


# A NUMBER CARRIES ITS UNIT'S OWN CASE, NOT TITLE CASE (2026-09-15).
# The generic rule below upper-cases the first letter of a token, which turned
# the tag "1080p AI Video" into "1080P AI Video" and blocked two finished Shorts
# at the publish gate. A resolution, a frame rate or a parameter count is written
# one way in the world and Title Case does not apply to it: 1080p, 4K, 60fps, 7B.
UNIT_SUFFIXES = {
    "p": "p", "i": "i", "k": "K", "fps": "fps", "hz": "Hz", "khz": "kHz",
    "x": "x", "b": "B", "kb": "KB", "mb": "MB", "gb": "GB", "tb": "TB",
    "ms": "ms", "bit": "bit",
}
_NUMBER_UNIT = re.compile(r"^(\d+(?:\.\d+)?)([A-Za-z]+)$")


def _number_unit(token: str) -> str | None:
    """Return the conventional form of a number+unit token, else None."""
    match = _NUMBER_UNIT.match(token)
    if not match:
        return None
    number, unit = match.groups()
    canonical = UNIT_SUFFIXES.get(unit.casefold())
    return f"{number}{canonical}" if canonical else None


def _canonicalize_token(token: str, *, first: bool) -> str:
    if not token:
        return token

    exact = EXACT_TOKENS.get(token.casefold())
    if exact:
        return exact

    unit = _number_unit(token)
    if unit:
        return unit

    if not first and token.casefold() in LOWERCASE_JOINERS:
        return token.casefold()

    if "-" in token:
        parts = token.split("-")
        return "-".join(
            _canonicalize_token(part, first=first and index == 0)
            for index, part in enumerate(parts)
        )

    # Preserve deliberate mixed-case brands (WordPress, iPhone) and acronyms.
    if token.isupper() or any(char.isupper() for char in token[1:]):
        return token

    match = re.match(r"^([^A-Za-z]*)([A-Za-z])(.*)$", token)
    if not match:
        return token
    prefix, initial, remainder = match.groups()
    return f"{prefix}{initial.upper()}{remainder.lower()}"


def canonicalize_tag(tag: str) -> str:
    """Return a tag in the channel's Title Case / exact-acronym style."""
    words = str(tag).strip().split()
    return " ".join(
        _canonicalize_token(word, first=index == 0)
        for index, word in enumerate(words)
    )


def validate_tag_casing(tags: Iterable[str]) -> list[str]:
    """Raise with actionable corrections when tag casing is not canonical."""
    cleaned = [str(tag).strip() for tag in tags if str(tag).strip()]
    corrections = [
        f"{tag!r} -> {canonicalize_tag(tag)!r}"
        for tag in cleaned
        if tag != canonicalize_tag(tag)
    ]
    if corrections:
        raise ValueError(
            "YouTube tags must use Title Case with exact acronyms/brands "
            "(including AI and 3D). Fix: " + "; ".join(corrections)
        )
    return cleaned
