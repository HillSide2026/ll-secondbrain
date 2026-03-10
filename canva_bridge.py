#!/usr/bin/env python3
"""
Minimal Canva OAuth bridge (Authorization Code + PKCE).

Routes:
  GET /
  GET /oauth/start
  GET /oauth/callback
  GET /design/:id
"""

import base64
import hashlib
import html
import json
import os
import secrets
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Dict, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, quote, urlencode, urlparse, unquote
from urllib.request import Request, urlopen


AUTH_URL = "https://www.canva.com/api/oauth/authorize"
TOKEN_URL = "https://api.canva.com/rest/v1/oauth/token"
DESIGNS_URL = "https://api.canva.com/rest/v1/designs"

DEFAULT_REDIRECT_URI = "http://127.0.0.1:3000/oauth/callback"
DEFAULT_SCOPES = "design:content:read design:content:write design:meta:read"


def load_env_file(env_path: Path) -> None:
    """Load simple KEY=VALUE entries from .env into os.environ if missing."""
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if ((value.startswith('"') and value.endswith('"'))
                or (value.startswith("'") and value.endswith("'"))):
            value = value[1:-1]
        if key and key not in os.environ:
            os.environ[key] = value


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def create_pkce_pair() -> Tuple[str, str]:
    code_verifier = b64url(os.urandom(64))
    code_challenge = b64url(hashlib.sha256(code_verifier.encode("ascii")).digest())
    return code_verifier, code_challenge


def save_json(path: Path, payload: Dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def load_json(path: Path) -> Optional[Dict]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def remove_file(path: Path) -> None:
    try:
        path.unlink()
    except FileNotFoundError:
        return


def request_json(method: str, url: str, headers: Optional[Dict] = None,
                 form_data: Optional[Dict] = None, json_data: Optional[Dict] = None,
                 timeout: int = 30) -> Tuple[int, Dict]:
    hdrs = dict(headers or {})
    body = None

    if form_data is not None:
        body = urlencode(form_data).encode("utf-8")
        hdrs.setdefault("Content-Type", "application/x-www-form-urlencoded")
    elif json_data is not None:
        body = json.dumps(json_data).encode("utf-8")
        hdrs.setdefault("Content-Type", "application/json")

    req = Request(url, data=body, headers=hdrs, method=method.upper())
    try:
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            parsed = json.loads(raw) if raw else {}
            return resp.status, parsed
    except HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            parsed = {"error": "http_error", "message": raw}
        return exc.code, parsed
    except URLError as exc:
        return 0, {"error": "network_error", "message": str(exc)}


def extract_design_id(payload: Dict) -> Optional[str]:
    candidate = payload
    if isinstance(candidate, dict) and "data" in candidate:
        candidate = candidate["data"]
    if isinstance(candidate, dict) and "design" in candidate:
        candidate = candidate["design"]
    if isinstance(candidate, list):
        candidate = candidate[0] if candidate else {}
    if not isinstance(candidate, dict):
        return None
    return candidate.get("id") or candidate.get("design_id") or candidate.get("gid")


def extract_urls(payload: Dict) -> Tuple[Optional[str], Optional[str]]:
    candidate = payload
    if isinstance(candidate, dict) and "data" in candidate:
        candidate = candidate["data"]
    if isinstance(candidate, dict) and "design" in candidate:
        candidate = candidate["design"]
    if isinstance(candidate, list):
        candidate = candidate[0] if candidate else {}
    if not isinstance(candidate, dict):
        return None, None

    edit_url = candidate.get("edit_url")
    view_url = candidate.get("view_url")
    if isinstance(candidate.get("urls"), dict):
        urls = candidate["urls"]
        edit_url = edit_url or urls.get("edit_url") or urls.get("edit")
        view_url = view_url or urls.get("view_url") or urls.get("view") or urls.get("web")
    return edit_url, view_url


def json_pretty(payload: Dict) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False)


ROOT = Path(__file__).resolve().parent
load_env_file(ROOT / ".env")

CANVA_CLIENT_ID = os.getenv("CANVA_CLIENT_ID", "").strip()
CANVA_CLIENT_SECRET = os.getenv("CANVA_CLIENT_SECRET", "").strip()
CANVA_REDIRECT_URI = os.getenv("CANVA_REDIRECT_URI", DEFAULT_REDIRECT_URI).strip()
CANVA_SCOPES = os.getenv("CANVA_SCOPES", DEFAULT_SCOPES).strip() or DEFAULT_SCOPES
SESSION_SECRET = os.getenv("SESSION_SECRET", "")
PORT = int(os.getenv("PORT", "3000"))
CANVA_TOKEN_FILE = Path(os.getenv("CANVA_TOKEN_FILE", "./tokens.json"))
CANVA_STATE_FILE = Path(os.getenv("CANVA_STATE_FILE", "./oauth_state.json"))

REDIRECT_PARSED = urlparse(CANVA_REDIRECT_URI)
HOST = REDIRECT_PARSED.hostname or "127.0.0.1"


class CanvaBridgeHandler(BaseHTTPRequestHandler):
    server_version = "CanvaBridge/0.2"

    def log_message(self, fmt, *args):
        return

    def _send_json(self, code: int, payload: Dict):
        body = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, code: int, title: str, body_html: str):
        doc = f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>{html.escape(title)}</title>
    <style>
      body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 24px; }}
      pre {{ background: #f6f8fa; padding: 12px; overflow-x: auto; }}
      a {{ color: #0969da; }}
    </style>
  </head>
  <body>
    <h1>{html.escape(title)}</h1>
    {body_html}
  </body>
</html>"""
        raw = doc.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _redirect(self, location: str):
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

    def _render_error_html(self, title: str, status: int, payload: Dict):
        escaped = html.escape(json_pretty(payload))
        body = (
            f"<p>Status: <strong>{status}</strong></p>"
            f"<pre>{escaped}</pre>"
        )
        self._send_html(502, title, body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/":
            self.handle_root()
            return

        if path == "/oauth/start":
            self.handle_oauth_start()
            return

        if path == "/oauth/callback":
            self.handle_oauth_callback(parsed.query)
            return

        if path.startswith("/design/") and len(path) > len("/design/"):
            design_id = unquote(path[len("/design/"):])
            self.handle_design_route(design_id)
            return

        self._send_json(404, {"error": "not_found", "path": path})

    def handle_root(self):
        body = (
            "<p>Canva OAuth bridge is running.</p>"
            "<p><a href=\"/oauth/start\">Start Canva OAuth</a></p>"
            "<p>Route format for design metadata: <code>/design/:id</code></p>"
        )
        self._send_html(200, "Canva Bridge", body)

    def handle_oauth_start(self):
        if not CANVA_CLIENT_ID or not CANVA_CLIENT_SECRET:
            self._send_json(500, {
                "error": "missing_config",
                "message": "CANVA_CLIENT_ID and CANVA_CLIENT_SECRET are required."
            })
            print("[FAIL] Missing Canva credentials in environment.")
            return

        code_verifier, code_challenge = create_pkce_pair()
        state = secrets.token_urlsafe(32)

        oauth_state_payload = {
            "state": state,
            "code_verifier": code_verifier,
            "created_at": int(time.time()),
            "session_secret_present": bool(SESSION_SECRET),
        }
        save_json(CANVA_STATE_FILE, oauth_state_payload)

        query = urlencode({
            "response_type": "code",
            "client_id": CANVA_CLIENT_ID,
            "redirect_uri": CANVA_REDIRECT_URI,
            "scope": CANVA_SCOPES,
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        })
        auth_redirect = f"{AUTH_URL}?{query}"
        print("[OK] /oauth/start generated PKCE + state and wrote oauth_state.json")
        self._redirect(auth_redirect)

    def handle_oauth_callback(self, query_string: str):
        params = parse_qs(query_string)
        code = (params.get("code") or [None])[0]
        state = (params.get("state") or [None])[0]
        oauth_error = (params.get("error") or [None])[0]

        if oauth_error:
            payload = {
                "error": "oauth_error",
                "message": oauth_error,
                "details": (params.get("error_description") or [""])[0],
            }
            self._render_error_html("Canva OAuth Failed", 400, payload)
            print(f"[FAIL] OAuth error returned by Canva: {oauth_error}")
            return

        if not code or not state:
            payload = {"error": "missing_code_or_state"}
            self._render_error_html("Canva OAuth Failed", 400, payload)
            print("[FAIL] Callback missing code or state.")
            return

        local_state = load_json(CANVA_STATE_FILE)
        if not local_state:
            payload = {"error": "missing_local_state"}
            self._render_error_html("Canva OAuth Failed", 400, payload)
            print("[FAIL] oauth_state.json missing or invalid.")
            return

        if state != local_state.get("state"):
            payload = {"error": "state_mismatch"}
            self._render_error_html("Canva OAuth Failed", 400, payload)
            print("[FAIL] State mismatch in OAuth callback.")
            return

        client_pair = f"{CANVA_CLIENT_ID}:{CANVA_CLIENT_SECRET}".encode("utf-8")
        basic_auth = base64.b64encode(client_pair).decode("ascii")
        token_headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {basic_auth}",
        }
        token_form = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": CANVA_REDIRECT_URI,
            "code_verifier": local_state.get("code_verifier", ""),
            "client_id": CANVA_CLIENT_ID,
        }
        token_status, token_payload = request_json(
            "POST", TOKEN_URL, headers=token_headers, form_data=token_form
        )

        if token_status != 200:
            print("[FAIL] Token exchange failed.")
            print(json_pretty(token_payload))
            self._render_error_html("Canva Token Exchange Failed", token_status, token_payload)
            return

        access_token = token_payload.get("access_token")
        refresh_token = token_payload.get("refresh_token")
        expires_in = int(token_payload.get("expires_in", 0) or 0)
        expires_at = int(time.time()) + expires_in if expires_in > 0 else None
        returned_scope = token_payload.get("scope") or CANVA_SCOPES

        token_record = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": expires_in,
            "expires_at": expires_at,
            "scope": returned_scope,
            "saved_at": int(time.time()),
        }
        save_json(CANVA_TOKEN_FILE, token_record)
        remove_file(CANVA_STATE_FILE)

        if not access_token:
            payload = {"error": "missing_access_token", "token_response": token_payload}
            self._render_error_html("Canva Token Exchange Failed", 502, payload)
            print("[FAIL] Token payload missing access_token.")
            return

        if expires_at and int(time.time()) >= expires_at:
            payload = {"error": "expired_token_after_exchange", "token_response": token_payload}
            self._render_error_html("Canva Token Exchange Failed", 401, payload)
            print("[FAIL] Access token already expired.")
            return

        api_headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }

        create_body = {
            "title": "Phase 1 Test Design",
            "design_type": {
                "type": "preset",
                "name": "presentation",
            },
        }
        create_headers = dict(api_headers)
        create_headers["Content-Type"] = "application/json"
        create_status, create_payload = request_json(
            "POST",
            DESIGNS_URL,
            headers=create_headers,
            json_data=create_body,
        )

        if create_status not in (200, 201):
            print("[FAIL] Canva design creation failed.")
            print(json_pretty(create_payload))
            self._render_error_html("Canva Design Creation Failed", create_status, create_payload)
            return

        design_id = extract_design_id(create_payload if isinstance(create_payload, dict) else {})
        if not design_id:
            payload = {
                "error": "missing_design_id",
                "create_response": create_payload,
            }
            self._render_error_html("Canva Design Creation Failed", 502, payload)
            print("[FAIL] Canva create response missing design ID.")
            return

        metadata_status, metadata_payload = request_json(
            "GET",
            f"{DESIGNS_URL}/{quote(design_id, safe='')}",
            headers=api_headers,
        )
        if metadata_status not in (200, 201):
            print("[FAIL] Canva design metadata fetch failed.")
            print(json_pretty(metadata_payload))
            self._render_error_html("Canva Design Metadata Fetch Failed", metadata_status, metadata_payload)
            return

        edit_url, view_url = extract_urls(metadata_payload)
        metadata_json = html.escape(json_pretty(metadata_payload))
        edit_link = (
            f'<a href="{html.escape(edit_url)}" target="_blank">{html.escape(edit_url)}</a>'
            if edit_url else "not available"
        )
        view_link = (
            f'<a href="{html.escape(view_url)}" target="_blank">{html.escape(view_url)}</a>'
            if view_url else "not available"
        )

        body = (
            "<p><strong>Design created</strong></p>"
            f"<p>Design ID: <code>{html.escape(design_id)}</code></p>"
            f"<p>Edit URL: {edit_link}</p>"
            f"<p>View URL: {view_link}</p>"
            f"<h2>Metadata JSON</h2><pre>{metadata_json}</pre>"
        )
        self._send_html(200, "Design created", body)

        print("[OK] Design created.")
        print(f"Design ID: {design_id}")
        print(f"Edit URL: {edit_url or 'not available'}")
        print(f"View URL: {view_url or 'not available'}")

    def handle_design_route(self, design_id: str):
        token_data = load_json(CANVA_TOKEN_FILE)
        if not token_data:
            payload = {"error": "missing_token_file", "token_file": str(CANVA_TOKEN_FILE)}
            self._render_error_html("Canva Design Lookup Failed", 401, payload)
            return

        access_token = token_data.get("access_token")
        expires_at = token_data.get("expires_at")
        if not access_token:
            payload = {"error": "missing_access_token", "token_file": str(CANVA_TOKEN_FILE)}
            self._render_error_html("Canva Design Lookup Failed", 401, payload)
            return

        if isinstance(expires_at, int) and time.time() >= expires_at:
            payload = {
                "error": "expired_token",
                "expires_at": expires_at,
                "now": int(time.time()),
            }
            self._render_error_html("Canva Design Lookup Failed", 401, payload)
            return

        headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
        status, payload = request_json(
            "GET",
            f"{DESIGNS_URL}/{quote(design_id, safe='')}",
            headers=headers,
        )
        if status not in (200, 201):
            self._render_error_html("Canva Design Lookup Failed", status, payload)
            return

        edit_url, view_url = extract_urls(payload)
        edit_link = (
            f'<a href="{html.escape(edit_url)}" target="_blank">{html.escape(edit_url)}</a>'
            if edit_url else "not available"
        )
        view_link = (
            f'<a href="{html.escape(view_url)}" target="_blank">{html.escape(view_url)}</a>'
            if view_url else "not available"
        )
        body = (
            f"<p>Design ID: <code>{html.escape(design_id)}</code></p>"
            f"<p>Edit URL: {edit_link}</p>"
            f"<p>View URL: {view_link}</p>"
            f"<h2>Metadata JSON</h2><pre>{html.escape(json_pretty(payload))}</pre>"
        )
        self._send_html(200, f"Design {design_id}", body)


def main():
    if not CANVA_CLIENT_ID or not CANVA_CLIENT_SECRET:
        print("[WARN] CANVA_CLIENT_ID or CANVA_CLIENT_SECRET is missing. Set them in .env.")

    print("Starting Canva bridge...")
    print(f"Redirect URI: {CANVA_REDIRECT_URI}")
    print(f"Scopes: {CANVA_SCOPES}")
    print(f"Listening on: http://{HOST}:{PORT}")
    print("Routes:")
    print("  GET /")
    print("  GET /oauth/start")
    print("  GET /oauth/callback")
    print("  GET /design/:id")

    server = HTTPServer((HOST, PORT), CanvaBridgeHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Canva bridge.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
