#!/usr/bin/env python3
"""Build canonical YouTube packages for Shorts without uploading anything.

The manifest is a JSON object with a ``shorts`` array. Each row requires:
title, video_path, transcript_path, description, tags, and source_files. Rows
should also carry project_files (the factory EDIT files: generator, plan,
paperwork + clerk record, per-video chain scripts) which land under the
package's project/ subfolder so the short can be recreated from the package
alone (Miguel, 2026-08-13). Existing published videos may also provide
video_id, youtube_url, privacy_status, and published_at; those values are
recorded but never uploaded or changed here.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def find_workspace() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "AGENTS.md").exists() and (parent / "execution").exists():
            return parent
    return Path.home() / "Documents" / "Workspace"


WORKSPACE = find_workspace()
if str(WORKSPACE) not in sys.path:
    sys.path.insert(0, str(WORKSPACE))

from execution.standardize_youtube_transcripts import standardize_file  # noqa: E402

try:
    from execution.youtube_tag_style import validate_tag_casing  # noqa: E402
except ModuleNotFoundError:  # Standalone skill copy.
    from youtube_tag_style import validate_tag_casing  # noqa: E402

try:
    from execution.youtube_title_width import validate_youtube_title  # noqa: E402
except ModuleNotFoundError:  # Standalone skill copy.
    from youtube_title_width import validate_youtube_title  # noqa: E402


def resolve_path(value: str, manifest_dir: Path) -> Path:
    path = Path(value).expanduser()
    return path if path.is_absolute() else (manifest_dir / path).resolve()


def safe_title(value: str) -> str:
    cleaned = value.strip().replace("/", "-")
    if not cleaned or cleaned in {".", ".."}:
        raise ValueError(f"Invalid package title: {value!r}")
    return cleaned


def link_or_copy(source: Path, destination: Path) -> str:
    if not source.is_file():
        raise FileNotFoundError(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if destination.stat().st_size == source.stat().st_size:
            return "existing"
        raise FileExistsError(f"Refusing to replace different file: {destination}")
    try:
        os.link(source, destination)
        return "linked"
    except OSError:
        shutil.copy2(source, destination)
        return "copied"


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def extract_thumbnail(video_path: Path, output_path: Path) -> str:
    if output_path.exists() and output_path.stat().st_size > 0:
        return "existing"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-ss", "0.35", "-i", str(video_path), "-frames:v", "1",
        "-q:v", "2", str(output_path),
    ]
    subprocess.run(command, check=True)
    return "generated"


def validate_manifest(rows: list[dict[str, Any]]) -> None:
    titles = [str(row.get("title", "")).strip() for row in rows]
    ids = [str(row.get("video_id", "")).strip() for row in rows if row.get("video_id")]
    if len(titles) != len(set(titles)):
        raise ValueError("Manifest contains duplicate titles")
    if len(ids) != len(set(ids)):
        raise ValueError("Manifest contains duplicate video IDs")
    required = {"title", "video_path", "transcript_path", "description", "tags"}
    for index, row in enumerate(rows):
        missing = sorted(key for key in required if not row.get(key))
        if missing:
            raise ValueError(f"Manifest row {index} is missing: {', '.join(missing)}")
        try:
            validate_youtube_title(str(row["title"]).strip())
        except ValueError as exc:
            raise ValueError(f"Manifest row {index}: {exc}") from exc


def prepare_one(row: dict[str, Any], manifest_dir: Path, output_root: Path, write: bool) -> dict[str, Any]:
    title = str(row["title"]).strip()
    title_audit = validate_youtube_title(title)
    package_dir = output_root / safe_title(title)
    video_path = resolve_path(str(row["video_path"]), manifest_dir)
    transcript_path = resolve_path(str(row["transcript_path"]), manifest_dir)
    transcript = json.loads(transcript_path.read_text(encoding="utf-8"))
    tags = validate_tag_casing(row.get("tags", []))

    planned = {
        "title": title,
        "title_width_px": title_audit.width_px,
        "package_dir": str(package_dir),
        "video_id": row.get("video_id"),
        "video_path": str(video_path),
        "transcript_path": str(transcript_path),
        "source_count": len(row.get("source_files", [])),
        "write": write,
    }
    if not write:
        return planned

    package_dir.mkdir(parents=True, exist_ok=True)
    master_path = package_dir / f"{safe_title(title)}.mp4"
    link_or_copy(video_path, master_path)
    extract_thumbnail(master_path, package_dir / "thumbnail.jpg")

    write_text(package_dir / "youtube_description.md", str(row["description"]))
    write_text(package_dir / "youtube_timestamps.txt", f"00:00 {title}")
    write_text(package_dir / "youtube_tags.txt", "\n".join(tags))

    transcripts_dir = package_dir / "transcripts"
    write_json(transcripts_dir / "elevenlabs_scribe_raw.json", transcript)
    write_json(transcripts_dir / "transcript_full.json", transcript)
    write_json(
        transcripts_dir / "transcript_words.json",
        {
            "transcription_provider": "elevenlabs",
            "transcription_model": "scribe_v2",
            "language": transcript.get("language_code"),
            "duration": transcript.get("audio_duration_secs"),
            "words": transcript.get("words", []),
        },
    )
    standardize_file(transcripts_dir / "transcript_full.json", write=True)

    upload_metadata = {
        "title": title,
        "title_width_px": title_audit.width_px,
        "title_width_profile": title_audit.profile,
        "video_format": "Short",
        "type": "Standard",
        "website": False,
        "video_id": row.get("video_id"),
        "youtube_url": row.get("youtube_url") or (
            f"https://www.youtube.com/watch?v={row['video_id']}" if row.get("video_id") else None
        ),
        "privacy_status": row.get("privacy_status", "public"),
        "published_at": row.get("published_at"),
        "description": str(row["description"]),
        "tags": tags,
        "backfill_existing_video": bool(row.get("video_id")),
        "upload_performed": False,
    }
    write_json(package_dir / "upload_metadata.json", upload_metadata)

    production_dir = package_dir / "production"
    write_text(
        production_dir / "safety_scan.md",
        "# Safety scan\n\nHistorical package backfill for an already-published Short. "
        "No upload was performed by this package builder. The published factory render was retained.",
    )
    write_text(
        production_dir / "title_options.md",
        f"# Title decision\n\nPublished title retained: **{title}**",
    )

    for source_row in row.get("source_files", []):
        source = resolve_path(str(source_row["path"]), manifest_dir)
        relative = Path(str(source_row.get("destination") or source.name))
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"Unsafe source destination: {relative}")
        if relative.parts and relative.parts[0] == "source":
            relative = Path(*relative.parts[1:])
        link_or_copy(source, package_dir / "source" / relative)

    # Factory edit files (Miguel, 2026-08-13): the package must let a short be
    # RECREATED, not just re-edited — generator, plan, paperwork + clerk record,
    # and the per-video chain scripts ride along under project/. Small text
    # files only; media stays in source/.
    for project_row in row.get("project_files", []):
        source = resolve_path(str(project_row["path"]), manifest_dir)
        relative = Path(str(project_row.get("destination") or source.name))
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"Unsafe project destination: {relative}")
        if relative.parts and relative.parts[0] == "project":
            relative = Path(*relative.parts[1:])
        link_or_copy(source, package_dir / "project" / relative)

    planned["files"] = sum(1 for path in package_dir.rglob("*") if path.is_file())
    return planned


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, default=Path("~/Movies/Youtube/Short").expanduser())
    parser.add_argument("--write", action="store_true", help="Create packages; default is validation-only.")
    parser.add_argument("--summary-json", type=Path)
    args = parser.parse_args()

    manifest_path = args.manifest.expanduser().resolve()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows = data.get("shorts", [])
    validate_manifest(rows)
    results = [
        prepare_one(row, manifest_path.parent, args.output_root.expanduser().resolve(), args.write)
        for row in rows
    ]
    summary = {"manifest": str(manifest_path), "count": len(results), "write": args.write, "packages": results}
    if args.summary_json:
        write_json(args.summary_json.expanduser().resolve(), summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
