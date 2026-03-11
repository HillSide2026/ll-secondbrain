#!/usr/bin/env python3
"""
SharePoint MCP Server — LL Second Brain
========================================
Native MCP access for Claude Code, bounded to the same access surface
as sharepoint_integration.py + the Documentation/DRAFTS write path.

ACCESS POLICY (per ML1 directive):
  - No broader permissions than the existing Python script workflow.
  - No additional sites, drives, folders, read capabilities, or write operations.
  - Treats MCP as a controlled replacement interface, not a broader gateway.

PERMITTED OPERATIONS:
  1. list_folder   — enumerate folder children (metadata only, no file content)
  2. get_item      — get metadata for a single item by path
  3. upload_draft  — write a file to Documentation/DRAFTS only

HARDCODED ACCESS BOUNDARY:
  Drive: legalmatters  (Working Files drive, /sites/LegalMatters)
    - write_policy: PROHIBITED
    - allowed paths: LL Matters (Essential), LL Matters (Strategic),
                     LL Matters (Standard), LL Matters (Standard Cash Cows),
                     LL Matters (Parked), Clerk Work
    - EXCLUDED (root-confirmed but not in intake_paths): Data Management, Model File

  Drive: documentation  (Doc Pro Workspace, /sites/Documentation)
    - write_policy: PERMITTED — DRAFTS path only
    - allowed read path:  Doc Pro  In Tray/SB Execution/DRAFTS
    - allowed write path: Doc Pro  In Tray/SB Execution/DRAFTS

Python 3.9 compatible. No external MCP SDK required.
Implements MCP JSON-RPC 2.0 stdio transport manually.
"""

from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# ── Load .env from repo root ───────────────────────────────────────────────────
_REPO_ROOT = Path(__file__).resolve().parents[1]

try:
    from dotenv import load_dotenv
    load_dotenv(_REPO_ROOT / ".env")
except ImportError:
    pass  # dotenv not available; rely on environment being pre-set

import msal        # pip install msal
import requests    # pip install requests


# =============================================================================
# ACCESS BOUNDARY (hardcoded — must not be widened without ML1 approval)
# =============================================================================

GRAPH_BASE = "https://graph.microsoft.com/v1.0"

# Drive registry — source of truth: sharepoint_sources.yaml verified 2026-03-06
_DRIVES: Dict[str, Dict[str, Any]] = {
    "legalmatters": {
        "drive_id": "b!h1ZUioTppUufgSXSnMchs-6DFblC5YNCsdfy7k-ghhOWiwXFZMfpQ76cRS11GoNU",
        "site":     "levinellp.sharepoint.com/sites/LegalMatters",
        "write_policy": "PROHIBITED",
        # Allowed root prefixes for read (intake_paths only).
        # Data Management and Model File are root-confirmed but excluded.
        "allowed_read_prefixes": [
            "LL Matters (Essential)",
            "LL Matters (Strategic)",
            "LL Matters (Standard)",
            "LL Matters (Standard Cash Cows)",
            "LL Matters (Parked)",
            "Clerk Work",
        ],
        "allowed_write_prefixes": [],  # No writes permitted on this drive
    },
    "documentation": {
        "drive_id": "b!aepYh7XvLkaJQFKWL0yhBXltDNo4pJRJpSPL-X-uZ-tNtZwBKQHoRYMyWJLL2q-P",
        "site":     "levinellp.sharepoint.com/sites/Documentation",
        "write_policy": "PERMITTED",
        # Read allowed only within DRAFTS (same as write scope)
        "allowed_read_prefixes": [
            "Doc Pro  In Tray/SB Execution/DRAFTS",
        ],
        "allowed_write_prefixes": [
            "Doc Pro  In Tray/SB Execution/DRAFTS",
        ],
    },
}


# =============================================================================
# Logging (stderr only — stdout is reserved for JSON-RPC)
# =============================================================================

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)sZ [%(levelname)s] sharepoint-mcp: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
log = logging.getLogger("sharepoint_mcp")


# =============================================================================
# Path Validation
# =============================================================================

def _normalize_path(path: str) -> str:
    """Strip leading/trailing slashes for consistent comparison."""
    return path.strip("/")


def _is_allowed_read(drive_alias: str, path: str) -> bool:
    """Return True iff path is within an allowed read prefix for the drive."""
    norm = _normalize_path(path)
    drive = _DRIVES[drive_alias]
    return any(
        norm == prefix or norm.startswith(prefix + "/")
        for prefix in drive["allowed_read_prefixes"]
    )


def _is_allowed_write(drive_alias: str, path: str) -> bool:
    """Return True iff path is within an allowed write prefix for the drive."""
    norm = _normalize_path(path)
    drive = _DRIVES[drive_alias]
    if drive["write_policy"] == "PROHIBITED":
        return False
    return any(
        norm == prefix or norm.startswith(prefix + "/")
        for prefix in drive["allowed_write_prefixes"]
    )


def _require_valid_drive(drive_alias: str) -> None:
    if drive_alias not in _DRIVES:
        raise ValueError(
            f"Unknown drive '{drive_alias}'. Valid drives: {list(_DRIVES)}"
        )


# =============================================================================
# Graph Client (matches sharepoint_integration.py exactly)
# =============================================================================

def _get_token() -> str:
    tenant    = os.environ.get("AZURE_TENANT_ID")
    client_id = os.environ.get("AZURE_CLIENT_ID")
    secret    = os.environ.get("AZURE_CLIENT_SECRET")
    missing = [k for k, v in {
        "AZURE_TENANT_ID": tenant,
        "AZURE_CLIENT_ID": client_id,
        "AZURE_CLIENT_SECRET": secret,
    }.items() if not v]
    if missing:
        raise RuntimeError(f"Missing environment variables: {missing}")

    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        authority=f"https://login.microsoftonline.com/{tenant}",
        client_credential=secret,
    )
    result = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )
    if "access_token" not in result:
        raise RuntimeError(f"Token acquisition failed: {result}")
    return result["access_token"]


def _graph_get(url: str, params: Optional[dict] = None) -> dict:
    token = _get_token()
    r = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=60,
    )
    if r.status_code >= 400:
        raise RuntimeError(f"Graph API {r.status_code}: {r.text[:500]}")
    return r.json()


def _graph_paged_get(url: str, params: Optional[dict] = None) -> List[dict]:
    """Paginate through all results (matches sharepoint_integration.py paged_get)."""
    items: List[dict] = []
    token = _get_token()
    while url:
        r = requests.get(
            url,
            headers={"Authorization": f"Bearer {token}"},
            params=params,
            timeout=60,
        )
        if r.status_code >= 400:
            raise RuntimeError(f"Graph API {r.status_code}: {r.text[:500]}")
        payload = r.json()
        items.extend(payload.get("value", []))
        url = payload.get("@odata.nextLink")
        params = None  # nextLink already has params embedded
    return items


def _graph_put(url: str, content: bytes, content_type: str = "application/octet-stream") -> dict:
    token = _get_token()
    r = requests.put(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": content_type,
        },
        data=content,
        timeout=120,
    )
    if r.status_code >= 400:
        raise RuntimeError(f"Graph API PUT {r.status_code}: {r.text[:500]}")
    return r.json()


# =============================================================================
# Tool Implementations
# =============================================================================

def _slim_item(item: dict) -> dict:
    """Return only the metadata fields exposed by the existing script."""
    result = {
        "id":               item.get("id"),
        "name":             item.get("name"),
        "lastModifiedDateTime": item.get("lastModifiedDateTime"),
        "size":             item.get("size"),
        "webUrl":           item.get("webUrl"),
    }
    if "folder" in item:
        result["type"] = "folder"
        result["childCount"] = item["folder"].get("childCount")
    elif "file" in item:
        result["type"] = "file"
        result["mimeType"] = item["file"].get("mimeType")
    else:
        result["type"] = "unknown"
    return result


def tool_list_folder(args: dict) -> str:
    """
    List the children of a folder path within an approved drive.
    Returns item metadata only — no file content is read.
    """
    drive_alias = args.get("drive", "").lower()
    path        = args.get("path", "").strip()

    _require_valid_drive(drive_alias)

    if not path:
        raise ValueError("'path' is required and must not be empty.")

    if not _is_allowed_read(drive_alias, path):
        allowed = _DRIVES[drive_alias]["allowed_read_prefixes"]
        raise PermissionError(
            f"Path '{path}' is outside the approved read boundary for drive "
            f"'{drive_alias}'. Allowed prefixes: {allowed}"
        )

    drive_id = _DRIVES[drive_alias]["drive_id"]
    norm_path = _normalize_path(path)

    log.info("list_folder drive=%s path=%s", drive_alias, norm_path)

    url = f"{GRAPH_BASE}/drives/{drive_id}/root:/{norm_path}:/children"
    items = _graph_paged_get(url)
    result = [_slim_item(i) for i in items]

    return json.dumps(result, indent=2)


def tool_get_item(args: dict) -> str:
    """
    Get metadata for a single item (file or folder) by path.
    No file content is returned.
    """
    drive_alias = args.get("drive", "").lower()
    path        = args.get("path", "").strip()

    _require_valid_drive(drive_alias)

    if not path:
        raise ValueError("'path' is required and must not be empty.")

    if not _is_allowed_read(drive_alias, path):
        allowed = _DRIVES[drive_alias]["allowed_read_prefixes"]
        raise PermissionError(
            f"Path '{path}' is outside the approved read boundary for drive "
            f"'{drive_alias}'. Allowed prefixes: {allowed}"
        )

    drive_id = _DRIVES[drive_alias]["drive_id"]
    norm_path = _normalize_path(path)

    log.info("get_item drive=%s path=%s", drive_alias, norm_path)

    url = f"{GRAPH_BASE}/drives/{drive_id}/root:/{norm_path}"
    item = _graph_get(url)
    return json.dumps(_slim_item(item), indent=2)


def tool_upload_draft(args: dict) -> str:
    """
    Upload a file to the Documentation DRAFTS folder.
    Target path is hardcoded: Doc Pro  In Tray/SB Execution/DRAFTS/{filename}
    Only the 'documentation' drive is permitted. No other paths are accessible.
    """
    filename    = args.get("filename", "").strip()
    content_str = args.get("content", "")
    encoding    = args.get("encoding", "utf-8")  # "utf-8" or "base64"

    if not filename:
        raise ValueError("'filename' is required.")

    # Reject path traversal attempts
    if "/" in filename or "\\" in filename or ".." in filename:
        raise ValueError(
            "'filename' must be a plain filename with no path separators or '..'."
        )

    _DRAFTS_PREFIX = "Doc Pro  In Tray/SB Execution/DRAFTS"
    drive_alias    = "documentation"
    drive_id       = _DRIVES[drive_alias]["drive_id"]
    target_path    = f"{_DRAFTS_PREFIX}/{filename}"

    # Belt-and-suspenders: validate final path against write policy
    if not _is_allowed_write(drive_alias, target_path):
        raise PermissionError(
            f"Computed upload path '{target_path}' is outside the approved "
            f"write boundary. This should never happen — contact ML1."
        )

    if encoding == "base64":
        import base64
        content_bytes = base64.b64decode(content_str)
    else:
        content_bytes = content_str.encode("utf-8")

    log.info("upload_draft filename=%s bytes=%d", filename, len(content_bytes))

    url = (
        f"{GRAPH_BASE}/drives/{drive_id}"
        f"/root:/{target_path}:/content"
    )
    result = _graph_put(url, content_bytes)
    return json.dumps(_slim_item(result), indent=2)


# =============================================================================
# Tool Registry
# =============================================================================

_TOOLS = [
    {
        "name": "list_folder",
        "description": (
            "List the children (files and subfolders) of a folder path within an "
            "approved SharePoint drive. Returns item metadata only — no file content. "
            "Drives: 'legalmatters' (read-only), 'documentation' (DRAFTS path only). "
            "Access is restricted to approved intake paths per ML1 policy."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "drive": {
                    "type": "string",
                    "enum": ["legalmatters", "documentation"],
                    "description": (
                        "Drive to query. 'legalmatters' = Working Files drive on "
                        "/sites/LegalMatters. 'documentation' = Doc Pro Workspace "
                        "on /sites/Documentation."
                    ),
                },
                "path": {
                    "type": "string",
                    "description": (
                        "Folder path relative to drive root. Must begin with an "
                        "approved intake prefix. Example: 'LL Matters (Essential)' "
                        "or 'LL Matters (Essential)/25-927-00003'."
                    ),
                },
            },
            "required": ["drive", "path"],
        },
    },
    {
        "name": "get_item",
        "description": (
            "Get metadata for a single file or folder by path within an approved "
            "SharePoint drive. Returns name, type, size, lastModifiedDateTime, webUrl. "
            "Does NOT return file content. Same drive/path restrictions as list_folder."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "drive": {
                    "type": "string",
                    "enum": ["legalmatters", "documentation"],
                    "description": "Drive to query (same as list_folder).",
                },
                "path": {
                    "type": "string",
                    "description": "Path to the item relative to drive root.",
                },
            },
            "required": ["drive", "path"],
        },
    },
    {
        "name": "upload_draft",
        "description": (
            "Upload a file to the Documentation site DRAFTS folder. "
            "Target is always: 'Doc Pro  In Tray/SB Execution/DRAFTS/{filename}'. "
            "Only the filename is specified — the parent path is hardcoded and cannot "
            "be changed. No writes are permitted to any other path. "
            "This is the only write operation this MCP server supports."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": (
                        "Plain filename (no path separators, no '..'). "
                        "Example: 'draft_agreement_2026-03-11.docx'"
                    ),
                },
                "content": {
                    "type": "string",
                    "description": (
                        "File content as a UTF-8 string (default) or base64-encoded "
                        "bytes. For binary files (e.g. .docx), use encoding='base64'."
                    ),
                },
                "encoding": {
                    "type": "string",
                    "enum": ["utf-8", "base64"],
                    "description": "Content encoding. Default: 'utf-8'.",
                },
            },
            "required": ["filename", "content"],
        },
    },
]

_TOOL_FN_MAP = {
    "list_folder":   tool_list_folder,
    "get_item":      tool_get_item,
    "upload_draft":  tool_upload_draft,
}


# =============================================================================
# JSON-RPC 2.0 stdio Transport (MCP wire format, Python 3.9 compatible)
# =============================================================================

def _write(msg: dict) -> None:
    """Write a JSON-RPC message to stdout (one JSON object per line)."""
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


def _handle(msg: dict) -> None:
    method     = msg.get("method", "")
    request_id = msg.get("id")  # None for notifications

    # Notifications (no id) — acknowledge silently
    if request_id is None:
        log.debug("notification: %s", method)
        return

    try:
        if method == "initialize":
            _ok(request_id, {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "sharepoint-ll",
                    "version": "1.0.0",
                    "description": (
                        "Bounded SharePoint MCP — LL Second Brain. "
                        "Access limited to sharepoint_integration.py boundary."
                    ),
                },
            })

        elif method == "tools/list":
            _ok(request_id, {"tools": _TOOLS})

        elif method == "tools/call":
            params    = msg.get("params", {})
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
            except (PermissionError, ValueError) as exc:
                # Policy/validation errors — return as tool error (not JSON-RPC error)
                log.warning("tool error [%s]: %s", tool_name, exc)
                _ok(request_id, {
                    "content": [{"type": "text", "text": f"ERROR: {exc}"}],
                    "isError": True,
                })
            except Exception as exc:
                log.error("tool exception [%s]: %s", tool_name, exc, exc_info=True)
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
    log.info(
        "SharePoint MCP server starting. "
        "Drives: %s. Policy: read-only for legalmatters, DRAFTS-write for documentation.",
        list(_DRIVES),
    )
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
