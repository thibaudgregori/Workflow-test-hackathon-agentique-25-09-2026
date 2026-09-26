"""
Upload a video to YouTube as private (draft) with title, description, and tags.

Uses resumable upload with exponential backoff retry logic.

Tool references:
- tools/youtube.md (YouTube API patterns, upload quota costs)

Usage:
    python execution/upload_youtube_video.py \
        --video "path/to/video.mp4" \
        --title "Video Title" \
        --description "path/to/description.md" \
        --tags "tag1,tag2,tag3" \
        --privacy private \
        --category-id 28
"""

import argparse
import json
import os
import random
import re
import sys
import time
from pathlib import Path

try:
    from execution.youtube_tag_style import validate_tag_casing
except ModuleNotFoundError:  # Standalone skill copy.
    from youtube_tag_style import validate_tag_casing

try:
    from execution.youtube_title_width import TitleAudit, validate_youtube_title
except ModuleNotFoundError:  # Standalone skill copy.
    from youtube_title_width import TitleAudit, validate_youtube_title

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

WORKSPACE = Path(os.environ.get('WORKSPACE_ROOT', '~/Documents/Workspace')).expanduser()
TOKEN_FILE = WORKSPACE / 'secrets' / 'youtube_oauth_token.json'

SCOPES = [
    'https://www.googleapis.com/auth/youtube',
]

# Retry config
MAX_RETRIES = 5
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# YouTube limits
MAX_DESCRIPTION_LENGTH = 5000
MAX_TITLE_LENGTH = 100
MAX_TITLE_WIDTH_PX = 600.0
UPLOAD_QUOTA_COST = 1600
DAILY_QUOTA = 10000


def load_credentials():
    """Load OAuth credentials from token file."""
    if not TOKEN_FILE.exists():
        print(f"ERROR: Token file not found: {TOKEN_FILE}")
        print("Run: python execution/youtube_oauth_setup.py")
        print("(You may need to delete the old token first to re-auth with upload scope)")
        sys.exit(1)

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_FILE, 'w') as f:
                f.write(creds.to_json())
        else:
            print("ERROR: Token is invalid. Re-run: python execution/youtube_oauth_setup.py")
            sys.exit(1)

    return creds


def read_description(desc_path: str) -> str:
    """Read description from .md file, strip markdown formatting, and validate limits."""
    path = Path(desc_path).expanduser()
    if not path.exists():
        print(f"ERROR: Description file not found: {desc_path}")
        sys.exit(1)

    text = path.read_text(encoding='utf-8')
    text = strip_markdown_formatting(text)
    validate_description_length(text, desc_path)

    return text


def strip_markdown_formatting(text: str) -> str:
    """Apply the same markdown cleanup used before sending the description to YouTube."""
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)  # headers
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # bold
    text = re.sub(r'\*(.+?)\*', r'\1', text)  # italic
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'\1: \2', text)  # links -> text: url
    return text


def validate_description_length(text: str, desc_path: str = ''):
    """Fail before upload if the final YouTube description exceeds the hard limit."""
    if len(text) > MAX_DESCRIPTION_LENGTH:
        over_by = len(text) - MAX_DESCRIPTION_LENGTH
        location = f" ({desc_path})" if desc_path else ""
        print(f"ERROR: Description{location} is {len(text)} characters after upload formatting.")
        print(f"YouTube's hard description limit is {MAX_DESCRIPTION_LENGTH}; this is {over_by} over.")
        print("Revise the description deliberately and re-run validation. The uploader never truncates descriptions silently.")
        print("Suggested cuts: hashtags, drop-comment prompt, chat highlights/resources, then lower-priority tool links or dense timestamps.")
        sys.exit(1)

    print(f"Description length OK: {len(text)} / {MAX_DESCRIPTION_LENGTH} characters")


def upload_video(youtube, video_path: str, title: str, description: str,
                 tags: list, privacy: str, category_id: str, publish_at: str = None):
    """Upload video with resumable upload and retry logic.

    publish_at: ISO-8601 UTC time (e.g. 2026-09-08T09:00:00Z). YouTube's native scheduling:
    the video is uploaded private with status.publishAt and YouTube itself makes it public at
    that time (privacy is forced to private, as the API requires).
    """
    # Defensive validation for callers that import this function directly.
    validate_youtube_title(
        title,
        max_width_px=MAX_TITLE_WIDTH_PX,
        max_characters=MAX_TITLE_LENGTH,
    )
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id,
        },
        'status': {
            'privacyStatus': 'private' if publish_at else privacy,
            'selfDeclaredMadeForKids': False,
        },
    }
    if publish_at:
        body['status']['publishAt'] = publish_at

    media = MediaFileUpload(
        video_path,
        mimetype='video/mp4',
        resumable=True,
        chunksize=10 * 1024 * 1024,  # 10MB chunks
    )

    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media,
    )

    response = None
    retry = 0

    print(f"Uploading: {video_path}")
    print(f"Title: {title}")
    print(f"Privacy: {privacy}")
    print()

    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                pct = int(status.progress() * 100)
                print(f"  Upload progress: {pct}%")
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES and retry < MAX_RETRIES:
                retry += 1
                wait = (2 ** retry) + random.random()
                print(f"  HTTP {e.resp.status} error. Retrying in {wait:.1f}s (attempt {retry}/{MAX_RETRIES})...")
                time.sleep(wait)
            elif e.resp.status == 403 and 'quotaExceeded' in str(e):
                print("ERROR: YouTube API daily quota exceeded (10,000 units).")
                print(f"Each upload costs {UPLOAD_QUOTA_COST} units. Max ~{DAILY_QUOTA // UPLOAD_QUOTA_COST} uploads/day.")
                sys.exit(1)
            else:
                raise

    video_id = response['id']
    video_url = f"https://youtu.be/{video_id}"
    studio_url = f"https://studio.youtube.com/video/{video_id}/edit"

    print()
    print(f"Upload complete!")
    print(f"  Video URL:  {video_url}")
    print(f"  Studio URL: {studio_url}")
    print(f"  Quota used: {UPLOAD_QUOTA_COST} / {DAILY_QUOTA} daily units")

    return {
        'video_id': video_id,
        'video_url': video_url,
        'studio_url': studio_url,
        'quota_used': UPLOAD_QUOTA_COST,
    }


def set_thumbnail(youtube, video_id: str, thumbnail_path: str):
    """Set a custom thumbnail for a video."""
    path = Path(thumbnail_path).expanduser()
    if not path.exists():
        print(f"WARNING: Thumbnail file not found: {thumbnail_path}. Skipping.")
        return False

    ext = path.suffix.lower()
    mime_map = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png'}
    mime_type = mime_map.get(ext, 'image/jpeg')

    media = MediaFileUpload(str(path), mimetype=mime_type)
    youtube.thumbnails().set(videoId=video_id, media_body=media).execute()
    print(f"  Thumbnail set: {thumbnail_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description='Upload video to YouTube as draft')
    parser.add_argument('--video', required=True, help='Path to video file')
    parser.add_argument('--title', required=True, help='Video title')
    parser.add_argument('--description', required=True, help='Path to description .md file')
    parser.add_argument('--tags', default='', help='Comma-separated tags')
    parser.add_argument('--privacy', default='private', choices=['private', 'unlisted', 'public'],
                        help='Privacy status (default: private)')
    parser.add_argument('--category-id', default='28', help='YouTube category ID (default: 28 = Science & Tech)')
    parser.add_argument('--thumbnail', default='', help='Path to thumbnail image file (optional)')
    parser.add_argument('--publish-at', default='', help='ISO-8601 UTC time for native YouTube scheduling (uploads private, YouTube publishes it then)')
    parser.add_argument('--validate-only', action='store_true',
                        help='Validate local files and description length, then exit without authenticating or uploading')
    args = parser.parse_args()

    # Validate video file
    video_path = Path(args.video).expanduser()
    if not video_path.exists():
        print(f"ERROR: Video file not found: {args.video}")
        sys.exit(1)

    # Load description
    description = read_description(args.description)

    # A title can fit the API's character limit and still truncate in search.
    try:
        title_audit: TitleAudit = validate_youtube_title(
            args.title,
            max_width_px=MAX_TITLE_WIDTH_PX,
            max_characters=MAX_TITLE_LENGTH,
        )
    except ValueError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)
    print(
        f"Title width OK: {title_audit.width_px:.1f} / "
        f"{title_audit.max_width_px:.0f}px ({title_audit.characters} characters)"
    )

    # Parse tags
    try:
        tags = validate_tag_casing(args.tags.split(',') if args.tags else [])
    except ValueError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    if args.validate_only:
        print("Validation complete. No upload performed.")
        print(
            f"Title: {title_audit.width_px:.1f} / {title_audit.max_width_px:.0f}px; "
            f"{title_audit.characters} / {title_audit.max_characters} characters"
        )
        print(f"Tags: {len(tags)}")
        return

    # Authenticate and upload
    creds = load_credentials()
    youtube = build('youtube', 'v3', credentials=creds)

    result = upload_video(
        youtube=youtube,
        video_path=str(video_path),
        title=args.title,
        description=description,
        tags=tags,
        privacy=args.privacy,
        category_id=args.category_id,
        publish_at=args.publish_at or None,
    )

    # Set thumbnail if provided
    if args.thumbnail:
        set_thumbnail(youtube, result['video_id'], args.thumbnail)

    # Output JSON for programmatic use
    print()
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
