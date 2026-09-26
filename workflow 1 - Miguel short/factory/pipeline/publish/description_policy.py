"""Read-only preflight for the author-written Shorts description strategy.

No model, credentials, network, publication or automatic content classification.
Meaning and completeness are reviewed by the author under VOICE.md.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

VERSION = "2026-09-08"
PLATFORMS = ("youtube", "tiktok", "instagram")


def validate_captions(caps, package, platforms=PLATFORMS):
    """Return reviewable measurements; reject missing/stale source evidence."""
    strategy = caps.get("description_strategy")
    if not isinstance(strategy, dict) or strategy.get("version") != VERSION:
        raise ValueError("Review and regenerate captions under pipeline/publish/VOICE.md; "
                         "description_strategy version 2026-09-08 is required.")
    kind = strategy.get("content_type")
    length = strategy.get("description_length")
    if kind not in {"news", "tutorial", "explainer"}:
        raise ValueError("content_type must be news, tutorial or explainer")
    if length not in {"concise", "detailed"} or (kind != "tutorial" and length != "concise"):
        raise ValueError("Only tutorials use detailed descriptions; news/explainers use concise")
    for key in ("reason", "resource_review", "transcript_path", "transcript_sha256"):
        if not isinstance(strategy.get(key), str) or not strategy[key].strip():
            raise ValueError(f"description_strategy.{key} is required")
    source = Path(strategy["transcript_path"]).expanduser()
    if not source.is_absolute():
        source = Path(package) / source
    raw = source.read_bytes()
    if hashlib.sha256(raw).hexdigest() != strategy["transcript_sha256"]:
        raise ValueError("Transcript changed or wrong source hash; reread the exact final transcript")
    transcript = json.loads(raw).get("text")
    if not isinstance(transcript, str) or not transcript.strip():
        raise ValueError("Source must contain the full transcript in its text field")
    evidence = strategy.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        raise ValueError("At least one verbatim transcript excerpt is required")
    normalized = " ".join(transcript.split())
    for quote in evidence:
        if not isinstance(quote, str) or not quote.strip() or " ".join(quote.split()) not in normalized:
            raise ValueError("Strategy evidence is not present in the bound transcript")

    measurements = {}
    for platform in platforms:
        if platform not in PLATFORMS:
            raise ValueError(f"Unknown platform: {platform}")
        row = caps.get(platform)
        field = "description" if platform == "youtube" else "caption"
        content = row.get(field) if isinstance(row, dict) else None
        if not isinstance(content, str) or not content.strip():
            raise ValueError(f"{platform}.{field} must be nonempty plain text")
        if "—" in content:
            raise ValueError(f"{platform}: rewrite the em dash in Miguel's voice")
        if platform == "youtube":
            if len(content) > 5000:
                raise ValueError("YouTube description exceeds 5,000 characters; never truncate")
            # A fragment within a source URL, such as /en#book, is not a hashtag.
            hashtags = re.findall(r"(?<!\S)#[\w]+", content)
            if len(hashtags) > 3:
                raise ValueError("YouTube descriptions allow at most three topical hashtags")
        measurements[platform] = {"characters": len(content), "words": len(content.split())}
    return {"policy_version": VERSION, "content_type": kind, "description_length": length,
            "reason": strategy["reason"], "transcript_path": str(source.resolve()),
            "measurements": measurements, "semantic_review": "author responsibility under VOICE.md"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--platforms", default=",".join(PLATFORMS))
    args = parser.parse_args()
    package = args.package.expanduser().resolve()
    try:
        caps = json.loads((package / "Publishing/captions.json").read_text())
        result = validate_captions(caps, package, args.platforms.split(","))
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Description preflight: {exc}\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
