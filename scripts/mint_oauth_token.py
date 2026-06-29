#!/usr/bin/env python3
"""One-time: mint a Google OAuth refresh token for the Drive uploader.

The MINE bot uploads Slack-submitted PDFs into a My-Drive inbox folder. A
service account can't own files there (no storage quota), so the uploader acts
as a *real user* via an OAuth refresh token. Run this once, as the Google
account that **owns the inbox folder**, to produce that token.

Prerequisites
-------------
1. In Google Cloud Console (any project, e.g. the existing one), create an
   OAuth 2.0 Client ID of type **Desktop app**. Note its client id + secret.
2. On the OAuth consent screen, add your Google account as a **test user**
   (and add the scope `.../auth/drive.file`). drive.file is non-sensitive, so
   the refresh token does not expire under "Testing".
3. `pip install google-auth-oauthlib`

Usage
-----
    GOOGLE_OAUTH_CLIENT_ID=xxx.apps.googleusercontent.com \
    GOOGLE_OAUTH_CLIENT_SECRET=yyy \
    python scripts/mint_oauth_token.py

A browser opens; sign in as the inbox-folder owner and approve. The script
prints the refresh token. Store the three values as GitHub Actions secrets on
mine-toread:
    GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET, GOOGLE_OAUTH_REFRESH_TOKEN
"""

import os
import sys

SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def main() -> int:
    cid = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    csec = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    if not cid or not csec:
        print("Set GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET first.",
              file=sys.stderr)
        return 2

    from google_auth_oauthlib.flow import InstalledAppFlow

    client_config = {
        "installed": {
            "client_id": cid,
            "client_secret": csec,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    }
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    # offline + consent forces a refresh_token to be returned.
    creds = flow.run_local_server(
        port=0, access_type="offline", prompt="consent"
    )
    if not creds.refresh_token:
        print("No refresh token returned — re-run; ensure prompt=consent.",
              file=sys.stderr)
        return 1
    print("\n=== Store this as the GOOGLE_OAUTH_REFRESH_TOKEN secret ===")
    print(creds.refresh_token)
    return 0


if __name__ == "__main__":
    sys.exit(main())
