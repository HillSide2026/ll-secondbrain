#!/usr/bin/env python3
"""
Google Slides OAuth Setup Script
=================================
Adds the Slides (presentations) scope to the existing Google OAuth token.
Overwrites 00_SYSTEM/local_secrets/google_token.json with a new token that
includes all previously-granted scopes plus:
  https://www.googleapis.com/auth/presentations

Run once, then restart Claude Code so the slides MCP server picks up the
updated token.

Usage:
    python scripts/google_slides_oauth_setup.py

Prerequisites:
    pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO_ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(_REPO_ROOT / ".env")
except ImportError:
    pass

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
except ImportError:
    print("Missing required packages. Install with:")
    print("  pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv")
    sys.exit(1)

# Full combined scope set — must include everything already granted plus presentations.
# Add presentations to the set without removing any existing scope.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.settings.basic",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/presentations",
]


def _resolve_client_path() -> Path:
    configured = os.getenv("GOOGLE_OAUTH_CLIENT_PATH", "").strip()
    if configured:
        p = Path(configured)
        return p if p.is_absolute() else _REPO_ROOT / configured
    return _REPO_ROOT / "00_SYSTEM" / "local_secrets" / "google_oauth_client.json"


def _resolve_token_path() -> Path:
    configured = os.getenv("GOOGLE_OAUTH_TOKEN_PATH", "").strip()
    if configured:
        p = Path(configured)
        return p if p.is_absolute() else _REPO_ROOT / configured
    return _REPO_ROOT / "00_SYSTEM" / "local_secrets" / "google_token.json"


def main() -> None:
    client_path = _resolve_client_path()
    token_path = _resolve_token_path()

    print("=" * 60)
    print("Google Slides OAuth Setup")
    print("=" * 60)
    print()
    print(f"Client secrets: {client_path}")
    print(f"Token output:   {token_path}")
    print()
    print("Scopes requested:")
    for scope in SCOPES:
        marker = " <-- NEW" if "presentations" in scope else ""
        print(f"  {scope}{marker}")
    print()

    if not client_path.exists():
        print(f"ERROR: Client secrets file not found: {client_path}")
        print("Set GOOGLE_OAUTH_CLIENT_PATH in .env or place google_oauth_client.json")
        print("at 00_SYSTEM/local_secrets/google_oauth_client.json")
        sys.exit(1)

    # Check if existing token already has the presentations scope — skip re-auth if so.
    if token_path.exists():
        try:
            existing = json.loads(token_path.read_text())
            existing_scopes = set(existing.get("scopes", []))
            if "https://www.googleapis.com/auth/presentations" in existing_scopes:
                print("Token already includes the presentations scope.")
                print("No re-authorization needed. The slides MCP server should work as-is.")
                print()
                print("If you are still getting auth errors, delete the token file and re-run:")
                print(f"  rm {token_path}")
                print(f"  python {Path(__file__).name}")
                return
        except Exception:
            pass  # Corrupted token — proceed with fresh auth

    print("Opening browser for authorization...")
    print("(If the browser does not open, check the terminal for a URL to visit manually.)")
    print()

    try:
        flow = InstalledAppFlow.from_client_secrets_file(str(client_path), SCOPES)
        # port=0 lets the OS pick any available port — avoids conflicts with Claude Code
        # or other processes already using 8080.
        creds = flow.run_local_server(
            port=0,
            prompt="consent",
            access_type="offline",
        )
    except Exception as exc:
        print(f"Local server flow failed: {exc}")
        sys.exit(1)

    if not getattr(creds, "refresh_token", None):
        print()
        print("WARNING: No refresh token received.")
        print("This can happen if you previously authorized this OAuth client and did not")
        print("revoke access before adding the new scope.")
        print()
        print("Fix: revoke app access at https://myaccount.google.com/permissions")
        print("then run this script again.")
        sys.exit(1)

    token_path.parent.mkdir(parents=True, exist_ok=True)
    token_path.write_text(creds.to_json())

    print()
    print("=" * 60)
    print("SUCCESS — token saved.")
    print("=" * 60)
    print()
    print(f"Token written to: {token_path}")
    print()

    # Quick smoke test against the Slides API.
    print("Smoke testing Slides API access...")
    try:
        from googleapiclient.discovery import build
        service = build("slides", "v1", credentials=creds)
        # Create and immediately delete a throwaway presentation to confirm write access.
        pres = service.presentations().create(body={"title": "_oauth_smoke_test"}).execute()
        pres_id = pres.get("presentationId", "")
        print(f"  Created test presentation: {pres_id}")
        # Clean up via Drive API if available.
        try:
            drive = build("drive", "v3", credentials=creds)
            drive.files().delete(fileId=pres_id).execute()
            print("  Deleted test presentation (cleanup OK).")
        except Exception:
            print(f"  Could not delete test presentation — delete manually if needed:")
            print(f"  https://docs.google.com/presentation/d/{pres_id}/edit")
        print()
        print("Slides API access confirmed.")
    except Exception as exc:
        print(f"  Smoke test failed: {exc}")
        print("  The token was saved but the Slides API may not be enabled in your GCP project.")
        print("  Enable it at: https://console.cloud.google.com/apis/library/slides.googleapis.com")

    print()
    print("Next step: restart Claude Code (or reload the MCP server) so the")
    print("slides MCP server picks up the updated token.")


if __name__ == "__main__":
    main()
