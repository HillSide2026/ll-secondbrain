"""Google OAuth2 — Gmail + Drive + Docs.

Stage 2.9  Reads client-secret JSON created via Google Cloud Console.
First run opens a browser for consent; token is cached locally.
"""

from __future__ import annotations

import os
from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def _scopes() -> list[str]:
    raw = os.environ.get("GOOGLE_SCOPES", "").strip()
    scopes = raw.split()
    if not scopes:
        raise RuntimeError("GOOGLE_SCOPES is empty. Set it in .env.")
    return scopes


def get_creds() -> Credentials:
    client_json = os.environ.get("GOOGLE_OAUTH_CLIENT_JSON")
    token_path = os.environ.get("GOOGLE_TOKEN_PATH")
    if not client_json or not token_path:
        raise RuntimeError(
            "Missing GOOGLE_OAUTH_CLIENT_JSON or GOOGLE_TOKEN_PATH in env."
        )
    client_json_path = Path(client_json).expanduser()
    token_path_p = Path(token_path).expanduser()
    token_path_p.parent.mkdir(parents=True, exist_ok=True)

    scopes = _scopes()

    if token_path_p.exists():
        return Credentials.from_authorized_user_file(
            str(token_path_p), scopes=scopes
        )

    flow = InstalledAppFlow.from_client_secrets_file(
        str(client_json_path), scopes=scopes
    )
    creds = flow.run_local_server(port=0)
    token_path_p.write_text(creds.to_json(), encoding="utf-8")
    return creds


def get_drive():
    return build("drive", "v3", credentials=get_creds(), cache_discovery=False)


def get_docs():
    return build("docs", "v1", credentials=get_creds(), cache_discovery=False)
