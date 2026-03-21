#!/usr/bin/env python3
"""
Canva MCP Server — LL Second Brain
==================================
Persistent stdio MCP server for governed Canva access.

This replaces the old one-shot OAuth proof bridge with tool-callable endpoints
that Claude can invoke during a session once OAuth credentials exist.

PERMITTED OPERATIONS:
  1. auth_status  — inspect OAuth/token readiness
  2. start_oauth  — start one-time OAuth bootstrap and return the Canva auth URL
  3. list_designs — list Canva designs using the REST API
  4. get_design   — fetch one design by id
  5. create_design — create a draft design from a minimal preset payload or
                     caller-supplied JSON body

Python 3.9 compatible. No external MCP SDK required.
Implements MCP JSON-RPC 2.0 stdio transport manually.
"""

from __future__ import annotations

import base64
import hashlib
import html
import json
import logging
import os
import secrets
import sys
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, quote, urlencode, urlparse
from urllib.request import Request, urlopen


AUTH_URL = "https://www.canva.com/api/oauth/authorize"
TOKEN_URL = "https://api.canva.com/rest/v1/oauth/token"
DESIGNS_URL = "https://api.canva.com/rest/v1/designs"

DEFAULT_REDIRECT_URI = "http://127.0.0.1:3000/oauth/callback"
DEFAULT_SCOPES = "design:content:read design:content:write design:meta:read"
TOKEN_REFRESH_SKEW_SECONDS = 60


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


def save_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def load_json(path: Path) -> Optional[Dict[str, Any]]:
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


def request_json(
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    form_data: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
) -> Tuple[int, Dict[str, Any]]:
    hdrs = dict(headers or {})
    body = None

    if form_data is not None:
        form_payload = {key: value for key, value in form_data.items() if value is not None}
        body = urlencode(form_payload).encode("utf-8")
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


def extract_design_id(payload: Dict[str, Any]) -> Optional[str]:
    candidate: Any = payload
    if isinstance(candidate, dict) and "data" in candidate:
        candidate = candidate["data"]
    if isinstance(candidate, dict) and "design" in candidate:
        candidate = candidate["design"]
    if isinstance(candidate, list):
        candidate = candidate[0] if candidate else {}
    if not isinstance(candidate, dict):
        return None
    return candidate.get("id") or candidate.get("design_id") or candidate.get("gid")


def extract_urls(payload: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    candidate: Any = payload
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


def json_pretty(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False)


def build_url(base: str, params: Optional[Dict[str, Any]] = None) -> str:
    if not params:
        return base
    filtered = {key: value for key, value in params.items() if value not in (None, "", [])}
    if not filtered:
        return base
    return f"{base}?{urlencode(filtered)}"


ROOT = Path(__file__).resolve().parent
load_env_file(ROOT / ".env")


def _resolve_env_path(env_key: str, default_relative: str) -> Path:
    configured = os.getenv(env_key, "").strip() or default_relative
    path = Path(configured)
    if not path.is_absolute():
        path = ROOT / path
    return path


CANVA_CLIENT_ID = os.getenv("CANVA_CLIENT_ID", "").strip()
CANVA_CLIENT_SECRET = os.getenv("CANVA_CLIENT_SECRET", "").strip()
CANVA_REDIRECT_URI = os.getenv("CANVA_REDIRECT_URI", DEFAULT_REDIRECT_URI).strip()
CANVA_SCOPES = os.getenv("CANVA_SCOPES", DEFAULT_SCOPES).strip() or DEFAULT_SCOPES
CANVA_TOKEN_FILE = _resolve_env_path("CANVA_TOKEN_FILE", "./tokens.json")
CANVA_STATE_FILE = _resolve_env_path("CANVA_STATE_FILE", "./oauth_state.json")

OPS_DIR = ROOT / "06_RUNS" / "ops"
AUDIT_LOG = OPS_DIR / "canva_mcp_audit.ndjson"

REDIRECT_PARSED = urlparse(CANVA_REDIRECT_URI)
CALLBACK_HOST = REDIRECT_PARSED.hostname or "127.0.0.1"
CALLBACK_PORT = REDIRECT_PARSED.port or 3000
CALLBACK_PATH = REDIRECT_PARSED.path or "/oauth/callback"


logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)sZ [%(levelname)s] canva-mcp: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
log = logging.getLogger("canva_mcp")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _append_audit(entry: Dict[str, Any]) -> None:
    OPS_DIR.mkdir(parents=True, exist_ok=True)
    with AUDIT_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _audit_tool(tool_name: str, ok: bool, details: Optional[Dict[str, Any]] = None) -> None:
    payload = {
        "ts": _now_iso(),
        "tool": tool_name,
        "ok": ok,
    }
    if details:
        payload["details"] = details
    _append_audit(payload)


def _require_canva_config() -> None:
    missing = []
    if not CANVA_CLIENT_ID:
        missing.append("CANVA_CLIENT_ID")
    if not CANVA_CLIENT_SECRET:
        missing.append("CANVA_CLIENT_SECRET")
    if missing:
        raise RuntimeError(f"Missing Canva config: {', '.join(missing)}")


def _basic_auth_headers() -> Dict[str, str]:
    _require_canva_config()
    client_pair = f"{CANVA_CLIENT_ID}:{CANVA_CLIENT_SECRET}".encode("utf-8")
    basic_auth = base64.b64encode(client_pair).decode("ascii")
    return {
        "Accept": "application/json",
        "Authorization": f"Basic {basic_auth}",
    }


def _persist_token_payload(token_payload: Dict[str, Any], previous: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    expires_in = int(token_payload.get("expires_in", 0) or 0)
    refresh_token = token_payload.get("refresh_token") or (previous or {}).get("refresh_token")
    record = {
        "access_token": token_payload.get("access_token"),
        "refresh_token": refresh_token,
        "expires_in": expires_in,
        "expires_at": int(time.time()) + expires_in if expires_in > 0 else None,
        "scope": token_payload.get("scope") or (previous or {}).get("scope") or CANVA_SCOPES,
        "saved_at": int(time.time()),
        "token_type": token_payload.get("token_type"),
    }
    save_json(CANVA_TOKEN_FILE, record)
    return record


def _load_token_record() -> Optional[Dict[str, Any]]:
    return load_json(CANVA_TOKEN_FILE)


def _exchange_authorization_code(code: str, code_verifier: str) -> Dict[str, Any]:
    status, payload = request_json(
        "POST",
        TOKEN_URL,
        headers=_basic_auth_headers(),
        form_data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": CANVA_REDIRECT_URI,
            "code_verifier": code_verifier,
            "client_id": CANVA_CLIENT_ID,
        },
    )
    if status != 200:
        raise RuntimeError(f"Canva token exchange failed ({status}): {json_pretty(payload)}")
    if not payload.get("access_token"):
        raise RuntimeError("Canva token exchange succeeded but access_token was missing.")
    return _persist_token_payload(payload)


def _refresh_access_token(refresh_token: str) -> Dict[str, Any]:
    if not refresh_token:
        raise RuntimeError("No Canva refresh_token is available.")
    status, payload = request_json(
        "POST",
        TOKEN_URL,
        headers=_basic_auth_headers(),
        form_data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": CANVA_CLIENT_ID,
        },
    )
    if status != 200:
        raise RuntimeError(f"Canva token refresh failed ({status}): {json_pretty(payload)}")
    if not payload.get("access_token"):
        raise RuntimeError("Canva token refresh succeeded but access_token was missing.")
    previous = _load_token_record()
    return _persist_token_payload(payload, previous=previous)


def _ensure_access_token() -> str:
    token_record = _load_token_record()
    if not token_record:
        raise RuntimeError(
            f"No Canva token file found at {CANVA_TOKEN_FILE}. Call start_oauth first."
        )

    access_token = token_record.get("access_token")
    refresh_token = token_record.get("refresh_token")
    expires_at = token_record.get("expires_at")
    now = int(time.time())

    if not access_token:
        if refresh_token:
            token_record = _refresh_access_token(refresh_token)
            access_token = token_record.get("access_token")
        else:
            raise RuntimeError("Canva token record is missing access_token and refresh_token.")

    if isinstance(expires_at, int) and now >= (expires_at - TOKEN_REFRESH_SKEW_SECONDS):
        if not refresh_token:
            raise RuntimeError(
                "Canva access token is expired or near expiry and no refresh_token is available. "
                "Call start_oauth to re-authorize."
            )
        token_record = _refresh_access_token(refresh_token)
        access_token = token_record.get("access_token")

    if not access_token:
        raise RuntimeError("Unable to obtain a valid Canva access token.")

    return access_token


class _ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True


def _html_doc(title: str, body_html: str) -> bytes:
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
    return doc.encode("utf-8")


class _OAuthManager:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._server: Optional[_ReusableHTTPServer] = None
        self._thread: Optional[threading.Thread] = None
        self._last_status: Dict[str, Any] = {"state": "idle"}

    def _ensure_server(self) -> None:
        with self._lock:
            if self._thread and self._thread.is_alive():
                return
            try:
                self._server = _ReusableHTTPServer((CALLBACK_HOST, CALLBACK_PORT), CanvaOAuthCallbackHandler)
            except OSError as exc:
                raise RuntimeError(
                    f"Unable to start Canva OAuth callback server on {CALLBACK_HOST}:{CALLBACK_PORT}: {exc}"
                ) from exc
            self._thread = threading.Thread(
                target=self._server.serve_forever,
                daemon=True,
                name="canva-oauth-callback",
            )
            self._thread.start()
            log.info("Canva OAuth callback server listening on %s:%s%s", CALLBACK_HOST, CALLBACK_PORT, CALLBACK_PATH)

    def start(self, force_reauth: bool = False) -> Dict[str, Any]:
        _require_canva_config()
        if force_reauth:
            remove_file(CANVA_TOKEN_FILE)

        code_verifier, code_challenge = create_pkce_pair()
        state = secrets.token_urlsafe(32)
        oauth_state_payload = {
            "state": state,
            "code_verifier": code_verifier,
            "created_at": int(time.time()),
            "redirect_uri": CANVA_REDIRECT_URI,
            "scope": CANVA_SCOPES,
        }
        save_json(CANVA_STATE_FILE, oauth_state_payload)
        self._ensure_server()

        auth_url = build_url(
            AUTH_URL,
            {
                "response_type": "code",
                "client_id": CANVA_CLIENT_ID,
                "redirect_uri": CANVA_REDIRECT_URI,
                "scope": CANVA_SCOPES,
                "state": state,
                "code_challenge": code_challenge,
                "code_challenge_method": "S256",
            },
        )

        self._last_status = {
            "state": "awaiting_user_authorization",
            "started_at": _now_iso(),
            "authorization_url": auth_url,
            "callback_url": CANVA_REDIRECT_URI,
            "callback_server_running": self.is_server_running(),
        }
        return {
            "authorization_url": auth_url,
            "callback_url": CANVA_REDIRECT_URI,
            "callback_server_running": self.is_server_running(),
            "next_step": (
                "Open the authorization_url in a browser, complete Canva consent, "
                "then call auth_status until authenticated becomes true."
            ),
        }

    def complete(self, query_string: str) -> Tuple[int, str, str]:
        params = parse_qs(query_string)
        code = (params.get("code") or [None])[0]
        state = (params.get("state") or [None])[0]
        oauth_error = (params.get("error") or [None])[0]

        if oauth_error:
            message = (params.get("error_description") or [""])[0]
            self._last_status = {
                "state": "oauth_error",
                "error": oauth_error,
                "message": message,
                "updated_at": _now_iso(),
            }
            _audit_tool("oauth_callback", False, {"error": oauth_error, "message": message})
            body = (
                f"<p>OAuth error: <strong>{html.escape(oauth_error)}</strong></p>"
                f"<pre>{html.escape(message)}</pre>"
            )
            return 400, "Canva OAuth Failed", body

        if not code or not state:
            self._last_status = {
                "state": "oauth_error",
                "error": "missing_code_or_state",
                "updated_at": _now_iso(),
            }
            _audit_tool("oauth_callback", False, {"error": "missing_code_or_state"})
            return 400, "Canva OAuth Failed", "<p>Missing code or state.</p>"

        local_state = load_json(CANVA_STATE_FILE)
        if not local_state:
            self._last_status = {
                "state": "oauth_error",
                "error": "missing_local_state",
                "updated_at": _now_iso(),
            }
            _audit_tool("oauth_callback", False, {"error": "missing_local_state"})
            return 400, "Canva OAuth Failed", "<p>Local OAuth state file is missing or invalid.</p>"

        if state != local_state.get("state"):
            self._last_status = {
                "state": "oauth_error",
                "error": "state_mismatch",
                "updated_at": _now_iso(),
            }
            _audit_tool("oauth_callback", False, {"error": "state_mismatch"})
            return 400, "Canva OAuth Failed", "<p>State mismatch.</p>"

        try:
            token_record = _exchange_authorization_code(code, str(local_state.get("code_verifier", "")))
            remove_file(CANVA_STATE_FILE)
        except Exception as exc:
            self._last_status = {
                "state": "oauth_error",
                "error": str(exc),
                "updated_at": _now_iso(),
            }
            _audit_tool("oauth_callback", False, {"error": str(exc)})
            return 500, "Canva OAuth Failed", f"<pre>{html.escape(str(exc))}</pre>"

        self._last_status = {
            "state": "authenticated",
            "updated_at": _now_iso(),
            "expires_at": token_record.get("expires_at"),
            "scope": token_record.get("scope"),
        }
        _audit_tool("oauth_callback", True, {"expires_at": token_record.get("expires_at")})
        body = (
            "<p><strong>Canva OAuth completed successfully.</strong></p>"
            "<p>You can return to Claude and call Canva MCP tools now.</p>"
        )
        return 200, "Canva OAuth Complete", body

    def status(self) -> Dict[str, Any]:
        token_record = _load_token_record()
        state_record = load_json(CANVA_STATE_FILE)
        now = int(time.time())
        expires_at = token_record.get("expires_at") if token_record else None
        authenticated = bool(token_record and token_record.get("access_token"))
        expired = bool(isinstance(expires_at, int) and now >= expires_at) if token_record else False
        return {
            "configured": bool(CANVA_CLIENT_ID and CANVA_CLIENT_SECRET),
            "token_file": str(CANVA_TOKEN_FILE),
            "token_file_exists": CANVA_TOKEN_FILE.exists(),
            "state_file": str(CANVA_STATE_FILE),
            "pending_oauth": bool(state_record),
            "authenticated": authenticated and not expired,
            "expired": expired,
            "expires_at": expires_at,
            "scope": token_record.get("scope") if token_record else None,
            "callback_server_running": self.is_server_running(),
            "last_status": self._last_status,
        }

    def is_server_running(self) -> bool:
        return bool(self._thread and self._thread.is_alive())


_OAUTH_MANAGER = _OAuthManager()


class CanvaOAuthCallbackHandler(BaseHTTPRequestHandler):
    server_version = "CanvaMCPCallback/1.0"

    def log_message(self, fmt: str, *args: Any) -> None:
        return

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != CALLBACK_PATH:
            body = _html_doc("Not Found", "<p>Unknown path.</p>")
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        status, title, body_html = _OAUTH_MANAGER.complete(parsed.query)
        body = _html_doc(title, body_html)
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def _canva_headers(access_token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }


def tool_auth_status(args: Dict[str, Any]) -> str:
    del args
    payload = _OAUTH_MANAGER.status()
    _audit_tool("auth_status", True, {"authenticated": payload.get("authenticated")})
    return json_pretty(payload)


def tool_start_oauth(args: Dict[str, Any]) -> str:
    force_reauth = bool(args.get("force_reauth", False))
    payload = _OAUTH_MANAGER.start(force_reauth=force_reauth)
    _audit_tool("start_oauth", True, {"force_reauth": force_reauth})
    return json_pretty(payload)


def tool_list_designs(args: Dict[str, Any]) -> str:
    access_token = _ensure_access_token()
    params: Dict[str, Any] = {}
    if "page_size" in args and args.get("page_size") is not None:
        params["page_size"] = int(args["page_size"])
    if args.get("continuation"):
        params["continuation"] = str(args["continuation"])

    status, payload = request_json(
        "GET",
        build_url(DESIGNS_URL, params),
        headers=_canva_headers(access_token),
    )
    if status not in (200, 201):
        raise RuntimeError(f"Canva list_designs failed ({status}): {json_pretty(payload)}")

    _audit_tool("list_designs", True, {"status": status})
    return json_pretty(payload)


def tool_get_design(args: Dict[str, Any]) -> str:
    design_id = str(args.get("design_id", "")).strip()
    if not design_id:
        raise ValueError("get_design requires 'design_id'.")

    access_token = _ensure_access_token()
    status, payload = request_json(
        "GET",
        f"{DESIGNS_URL}/{quote(design_id, safe='')}",
        headers=_canva_headers(access_token),
    )
    if status not in (200, 201):
        raise RuntimeError(f"Canva get_design failed ({status}): {json_pretty(payload)}")

    edit_url, view_url = extract_urls(payload)
    result = {
        "design_id": design_id,
        "edit_url": edit_url,
        "view_url": view_url,
        "response": payload,
    }
    _audit_tool("get_design", True, {"design_id": design_id})
    return json_pretty(result)


def tool_create_design(args: Dict[str, Any]) -> str:
    access_token = _ensure_access_token()
    raw_payload = args.get("payload")

    if raw_payload is not None:
        if not isinstance(raw_payload, dict):
            raise ValueError("create_design 'payload' must be an object when provided.")
        create_body = raw_payload
    else:
        title = str(args.get("title", "")).strip() or "SB Draft Design"
        design_type_name = str(args.get("design_type_name", "")).strip() or "presentation"
        create_body = {
            "title": title,
            "design_type": {
                "type": "preset",
                "name": design_type_name,
            },
        }

    headers = _canva_headers(access_token)
    headers["Content-Type"] = "application/json"
    status, payload = request_json(
        "POST",
        DESIGNS_URL,
        headers=headers,
        json_data=create_body,
    )
    if status not in (200, 201):
        raise RuntimeError(f"Canva create_design failed ({status}): {json_pretty(payload)}")

    design_id = extract_design_id(payload)
    edit_url, view_url = extract_urls(payload)
    result: Dict[str, Any] = {
        "design_id": design_id,
        "edit_url": edit_url,
        "view_url": view_url,
        "create_response": payload,
    }

    if design_id and bool(args.get("fetch_metadata", True)):
        metadata_status, metadata_payload = request_json(
            "GET",
            f"{DESIGNS_URL}/{quote(design_id, safe='')}",
            headers=_canva_headers(access_token),
        )
        result["metadata_status"] = metadata_status
        result["metadata_response"] = metadata_payload
        if metadata_status in (200, 201):
            meta_edit_url, meta_view_url = extract_urls(metadata_payload)
            result["edit_url"] = meta_edit_url or result["edit_url"]
            result["view_url"] = meta_view_url or result["view_url"]

    _audit_tool("create_design", True, {"design_id": design_id})
    return json_pretty(result)


_TOOLS = [
    {
        "name": "auth_status",
        "description": (
            "Inspect Canva OAuth readiness, token presence, expiry, and callback "
            "server status."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "start_oauth",
        "description": (
            "Start the one-time Canva OAuth bootstrap. Returns an authorization URL "
            "to open in a browser while the MCP server listens for the callback."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "force_reauth": {
                    "type": "boolean",
                    "description": "When true, clear the current token file before starting a new OAuth flow.",
                },
            },
        },
    },
    {
        "name": "list_designs",
        "description": "List Canva designs using the current OAuth token.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "page_size": {
                    "type": "integer",
                    "description": "Optional page size forwarded to the Canva designs API.",
                },
                "continuation": {
                    "type": "string",
                    "description": "Optional continuation cursor forwarded to the Canva designs API.",
                },
            },
        },
    },
    {
        "name": "get_design",
        "description": "Fetch one Canva design by id and return metadata plus edit/view URLs when available.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "design_id": {
                    "type": "string",
                    "description": "Canva design id.",
                },
            },
            "required": ["design_id"],
        },
    },
    {
        "name": "create_design",
        "description": (
            "Create a Canva draft design. Either provide a full payload object or "
            "use the minimal title + design_type_name preset form."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Design title when using the minimal preset payload.",
                },
                "design_type_name": {
                    "type": "string",
                    "description": "Canva preset design type name, e.g. 'presentation'.",
                },
                "payload": {
                    "type": "object",
                    "description": "Optional raw Canva create-design JSON payload to send directly.",
                },
                "fetch_metadata": {
                    "type": "boolean",
                    "description": "When true, fetch design metadata after creation if an id is returned.",
                },
            },
        },
    },
]

_TOOL_FN_MAP = {
    "auth_status": tool_auth_status,
    "start_oauth": tool_start_oauth,
    "list_designs": tool_list_designs,
    "get_design": tool_get_design,
    "create_design": tool_create_design,
}


def _write(msg: Dict[str, Any]) -> None:
    line = json.dumps(msg, separators=(",", ":"))
    sys.stdout.write(line + "\n")
    sys.stdout.flush()


def _ok(request_id: Any, result: Any) -> None:
    _write({"jsonrpc": "2.0", "id": request_id, "result": result})


def _err(request_id: Any, code: int, message: str) -> None:
    _write({
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": code, "message": message},
    })


def _handle(msg: Dict[str, Any]) -> None:
    method = msg.get("method", "")
    request_id = msg.get("id")

    if request_id is None:
        log.debug("notification: %s", method)
        return

    try:
        if method == "initialize":
            _ok(request_id, {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "canva-ll",
                    "version": "1.0.0",
                    "description": (
                        "Canva MCP — LL Second Brain. Draft-design access with "
                        "one-time OAuth bootstrap and governed runtime calls."
                    ),
                },
            })
        elif method == "tools/list":
            _ok(request_id, {"tools": _TOOLS})
        elif method == "tools/call":
            params = msg.get("params", {})
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})

            if tool_name not in _TOOL_FN_MAP:
                _err(request_id, -32601, f"Unknown tool: '{tool_name}'")
                return

            log.info("tools/call name=%s", tool_name)
            try:
                text = _TOOL_FN_MAP[tool_name](arguments)
                _ok(request_id, {
                    "content": [{"type": "text", "text": text}],
                    "isError": False,
                })
            except (PermissionError, ValueError, RuntimeError) as exc:
                log.warning("tool error [%s]: %s", tool_name, exc)
                _audit_tool(tool_name, False, {"error": str(exc)})
                _ok(request_id, {
                    "content": [{"type": "text", "text": f"ERROR: {exc}"}],
                    "isError": True,
                })
            except Exception as exc:
                log.error("tool exception [%s]: %s", tool_name, exc, exc_info=True)
                _audit_tool(tool_name, False, {"error": str(exc)})
                _ok(request_id, {
                    "content": [{"type": "text", "text": f"ERROR: {exc}"}],
                    "isError": True,
                })
        else:
            _err(request_id, -32601, f"Method not found: '{method}'")
    except Exception as exc:
        log.error("handler exception: %s", exc, exc_info=True)
        _err(request_id, -32603, f"Internal error: {exc}")


def main() -> None:
    log.info("Canva MCP server starting. OAuth callback: %s", CANVA_REDIRECT_URI)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError as exc:
            log.error("JSON parse error: %s | input: %.200s", exc, line)
            _write({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {exc}"},
            })
            continue
        _handle(msg)


if __name__ == "__main__":
    main()
