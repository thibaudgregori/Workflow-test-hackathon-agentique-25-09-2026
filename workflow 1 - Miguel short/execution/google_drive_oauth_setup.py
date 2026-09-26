"""
Google Drive OAuth Setup Script
One-time authentication to get refresh token for Google Drive API.

Run this script once to authorize access. It will:
1. Open your browser for Google sign-in
2. Ask you to authorize Drive access
3. Save refresh token for future use (no re-auth needed)

Tool references:
- tools/google_drive.md (Google Drive API patterns)

Directive: directives/track_linkedin_metrics_notion.md
"""

import os
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# OAuth scopes needed for Google Drive
SCOPES = [
    'https://www.googleapis.com/auth/drive',  # Full Drive access
]

# File paths
WORKSPACE = Path(__file__).parent.parent
CREDENTIALS_FILE = WORKSPACE / 'secrets' / 'claude_code_oauth_credentials.json'  # Claude Code project OAuth
TOKEN_FILE = WORKSPACE / 'secrets' / 'google_drive_oauth_token.json'


def authenticate():
    """
    Run OAuth flow to get and save credentials.

    Returns:
        Credentials object for API calls
    """
    creds = None

    # Check if we already have a valid token
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    # If no valid credentials, run the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("Opening browser for authorization...")
            print("   Please sign in with your Google account (miguel@genial-agency.com).")
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

        print(f"Token saved to: {TOKEN_FILE}")

    return creds


def verify_access(creds):
    """
    Verify that we can access Google Drive API.
    """
    from googleapiclient.discovery import build

    print("\nVerifying API access...")

    # Test Google Drive API
    service = build('drive', 'v3', credentials=creds)

    # List files to verify access
    results = service.files().list(
        pageSize=5,
        fields="files(id, name, mimeType)"
    ).execute()

    files = results.get('files', [])

    if files:
        print(f"   Google Drive API: Connected, found {len(files)} files")
        print("\n   Sample files:")
        for f in files[:3]:
            print(f"   - {f['name']} ({f['mimeType'][:30]}...)")
    else:
        print("   Google Drive API: Connected, but no files found")

    # Check if LinkedIn Posts folder exists
    linkedin_folder_id = '1Z4NslnXFMemS-MXyhOQ75qpaQgoBWUE-'
    try:
        folder = service.files().get(
            fileId=linkedin_folder_id,
            fields='id, name'
        ).execute()
        print(f"\n   LinkedIn Posts folder: Found '{folder['name']}'")
    except Exception as e:
        print(f"\n   LinkedIn Posts folder: Not found or no access")

    return True


def main():
    print("=" * 60)
    print("GOOGLE DRIVE OAUTH SETUP")
    print("=" * 60)
    print()

    if not CREDENTIALS_FILE.exists():
        print(f"Credentials file not found: {CREDENTIALS_FILE}")
        print("   Please download OAuth credentials from Google Cloud Console")
        print("   (You can reuse the same credentials as YouTube)")
        return

    # Run authentication
    creds = authenticate()

    # Verify access
    if verify_access(creds):
        print("\n" + "=" * 60)
        print("SETUP COMPLETE")
        print("=" * 60)
        print("\nYou can now run the LinkedIn sync script.")
        print("The token will auto-refresh, no need to re-authenticate.")
    else:
        print("\nSetup incomplete. Please check the errors above.")


if __name__ == "__main__":
    main()
