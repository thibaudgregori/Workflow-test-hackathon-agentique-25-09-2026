"""
YouTube OAuth Setup Script
One-time authentication to get refresh token for YouTube Analytics API.

Run this script once to authorize access. It will:
1. Open your browser for Google sign-in
2. Ask you to authorize the YouTube CMS app
3. Save refresh token for future use (no re-auth needed)

Tool references:
- tools/youtube.md (YouTube API patterns)
"""

import argparse
import os
import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# OAuth scopes needed for YouTube Analytics + Video Management
SCOPES = [
    'https://www.googleapis.com/auth/youtube',              # Full access (read + update metadata)
    'https://www.googleapis.com/auth/youtube.force-ssl',    # Required for commentThreads API
    'https://www.googleapis.com/auth/yt-analytics.readonly',
    'https://www.googleapis.com/auth/yt-analytics-monetary.readonly',  # Enables impressions + CTR metrics
]

# Credentials are canonical Workspace state, never skill payload.
WORKSPACE = Path(os.environ.get('WORKSPACE_ROOT', '~/Documents/Workspace')).expanduser()
CREDENTIALS_FILE = WORKSPACE / 'secrets' / 'youtube_oauth_credentials.json'
TOKEN_FILE = WORKSPACE / 'secrets' / 'youtube_oauth_token.json'


def authenticate(force_reauth=False):
    """
    Run OAuth flow to get and save credentials.

    Returns:
        Credentials object for API calls
    """
    creds = None

    # Check if we already have a valid token
    if TOKEN_FILE.exists() and not force_reauth:
        # Load the scopes recorded in the token itself. Passing SCOPES here can
        # make an under-scoped token appear correctly configured even though
        # Google will reject APIs that need the missing grants.
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))
        granted_scopes = set(creds.scopes or [])
        missing_scopes = sorted(set(SCOPES) - granted_scopes)
        if missing_scopes:
            print("🔐 Existing token is missing required scopes:")
            for scope in missing_scopes:
                print(f"   - {scope}")
            print("   Starting a fresh consent flow...")
            print()
            creds = None
    elif force_reauth:
        print("🔐 Forced re-authentication requested.")
        print()

    # If no valid credentials, run the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("🌐 Opening browser for authorization...")
            print("   Please sign in with your Google account that owns the YouTube channel.")
            print()

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE),
                SCOPES
            )

            # Run local server to handle OAuth callback
            creds = flow.run_local_server(
                port=8080,
                prompt='consent',
                access_type='offline'  # Get refresh token
            )

        # Save the credentials for future runs
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

        print(f"✅ Token saved to: {TOKEN_FILE}")

    return creds


def verify_access(creds):
    """
    Verify that we can access YouTube Analytics API.
    """
    from googleapiclient.discovery import build

    print("\n🔍 Verifying API access...")

    # Test YouTube Data API
    youtube = build('youtube', 'v3', credentials=creds)
    channels = youtube.channels().list(
        part='snippet,statistics',
        mine=True
    ).execute()

    if channels.get('items'):
        channel = channels['items'][0]
        print(f"   ✅ YouTube Data API: Connected to '{channel['snippet']['title']}'")
        channel_id = channel['id']
    else:
        print("   ❌ No channel found")
        return False

    # Test YouTube Analytics API
    analytics = build('youtubeAnalytics', 'v2', credentials=creds)

    # Query last 7 days of channel analytics
    response = analytics.reports().query(
        ids=f'channel=={channel_id}',
        startDate='2026-01-10',
        endDate='2026-01-17',
        metrics='views,estimatedMinutesWatched,averageViewDuration',
        dimensions='day'
    ).execute()

    if 'rows' in response:
        print(f"   ✅ YouTube Analytics API: Retrieved {len(response['rows'])} days of data")

        # Show sample
        print("\n   Sample data (last 7 days):")
        print("   Date       | Views | Watch Time (min) | Avg Duration (sec)")
        print("   " + "-" * 55)
        for row in response.get('rows', [])[-3:]:
            date, views, watch_min, avg_dur = row
            print(f"   {date} | {views:>5} | {watch_min:>16.1f} | {avg_dur:>18.1f}")
    else:
        print("   ⚠️  Analytics API connected but no data returned (may need time to populate)")

    return True


def main():
    parser = argparse.ArgumentParser(description="Authorize YouTube API access.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Run a fresh Google consent flow even when the current token is valid.",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("YOUTUBE OAUTH SETUP")
    print("=" * 60)
    print()

    if not CREDENTIALS_FILE.exists():
        print(f"❌ Credentials file not found: {CREDENTIALS_FILE}")
        print("   Please download OAuth credentials from Google Cloud Console")
        return

    # Run authentication
    creds = authenticate(force_reauth=args.force)

    # Verify access
    if verify_access(creds):
        print("\n" + "=" * 60)
        print("✅ SETUP COMPLETE")
        print("=" * 60)
        print("\nYou can now run the analytics sync script.")
        print("The token will auto-refresh, no need to re-authenticate.")
    else:
        print("\n❌ Setup incomplete. Please check the errors above.")


if __name__ == "__main__":
    main()
