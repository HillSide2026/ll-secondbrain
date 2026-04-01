#!/usr/bin/env python3
"""
SharePoint MCP Server — LL Second Brain
========================================
Native MCP access for Claude Code, bounded to the approved repo-declared
SharePoint surface.

ACCESS POLICY (per ML1 directive):
  - No broader permissions than the approved runtime workflow declared in-repo.
  - Additional site/library access must be explicitly allowlisted here.
  - Treats MCP as a controlled replacement interface, not a general SharePoint gateway.

PERMITTED OPERATIONS:
  1. list_folder          — enumerate folder children (metadata only)
  2. get_item             — get metadata for a single item by path
  3. upload_draft         — write a file to Documentation/DRAFTS only
  4. find_latest_template — search allowlisted Documentation template zones
  5. diff_docs            — diff allowlisted Documentation template/WIP documents
  6. copy_template_to_wip — copy allowlisted Documentation templates to WIP
  7. review_site_page     — review one approved Clients SitePages page
  8. update_site_page_content — current Clients SitePages content-update helper
  9. provision_client_workspace — current Clients page/library provisioning helper
 10. manage_clients_site — governed broad site-management wrapper for /sites/Clients

HARDCODED ACCESS BOUNDARY:
  Drive: legalmatters  (Working Files drive, /sites/LegalMatters)
    - write_policy: PROHIBITED
    - allowed paths: LL Matters (Essential), LL Matters (Strategic),
                     LL Matters (Standard), LL Matters (Standard Cash Cows),
                     LL Matters (Parked), Clerk Work
    - EXCLUDED (root-confirmed but not in intake_paths): Data Management, Model File

  Drive: documentation  (Doc Pro Workspace, /sites/Documentation)
    - write_policy: PERMITTED — DRAFTS path only
    - metadata read path via drive alias: SB Execution/DRAFTS
    - allowlisted content-read zones: sharepoint_allowlist.json
    - allowlisted WIP write zones:    sharepoint_allowlist.json

  Site: Clients  (/sites/Clients) — MANAGED WORKSPACE
    - clients_documents             -> Documents library, approved prefixes only
    - clients_master_client_library -> Master Client Library, full library read
    - clients_yellowbricks_capital  -> Yellowbricks Capital library, full library read
    - clients_turtle_island         -> Turtle Island library, full library read
    - clients_our_sharepoint_test2  -> Our-SharePoint-Test2 library, full library read
    - clients_our_sharepoint_test   -> our-sharepoint test library, full library read
    - CURRENT RUNTIME SLICE: /sites/Clients/SitePages/*.aspx
      -> review existing page metadata, text web parts, and supported web part inventory
      -> update title, description, and existing text web part innerHtml only
      -> broader Clients SitePages structure and navigation authority exists in doctrine,
         but is not yet fully exposed by the current runtime tool set
    - CURRENT RUNTIME SLICE: client-workspace provisioning helper
      -> create one new client page
      -> create one new client document library
      -> assign existing principals to those created resources
      -> add one shared-home navigation link
      -> current helper only; broader Clients managed-workspace operations require
         additional runtime tools
    - CURRENT RUNTIME SLICE: broad /sites/Clients site-management wrapper
      -> page, library, folder, navigation, permission, and site operations
      -> scope hard-locked to /sites/Clients only
      -> selected destructive and permission-bearing operations require approval_token

Python 3.9 compatible. No external MCP SDK required.
Implements MCP JSON-RPC 2.0 stdio transport manually.
"""

from __future__ import annotations

import base64
import difflib
import hashlib
import json
import logging
import os
import re
import sys
import zipfile
from datetime import datetime, timezone
from io import BytesIO
from html import unescape as html_unescape
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import quote, urlparse
from uuid import uuid4
from xml.etree import ElementTree as ET

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
ALLOWLIST_PATH = _REPO_ROOT / "00_SYSTEM" / "security" / "sharepoint_allowlist.json"
TEMPLATE_REGISTRY_PATH = (
    _REPO_ROOT / "02_PLAYBOOKS" / "_ASSETS" / "execution" / "reference" / "TEMPLATE_REGISTRY.json"
)

# Drive registry — runtime boundary reconciled with sharepoint_sources.yaml
# and live Graph verification on 2026-03-27.
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
            "SB Execution/DRAFTS",
        ],
        "allowed_write_prefixes": [
            "SB Execution/DRAFTS",
        ],
    },
    "clients_documents": {
        "drive_id": "b!Z2HcxOh5RUCQGXT-pPqEiswlrvuCxxlNu8VyM91YlhpAlA4DeLb5Rqx9fqyQwozC",
        "site":     "levinellp.sharepoint.com/sites/Clients",
        "write_policy": "PROHIBITED",
        "allowed_read_prefixes": [
            "Playbooks",
            "Policies and Processes",
            "Templates",
            "Work in Progress",
        ],
        "allowed_write_prefixes": [],
    },
    "clients_master_client_library": {
        "drive_id": "b!Z2HcxOh5RUCQGXT-pPqEiswlrvuCxxlNu8VyM91YlhqMwNk18--jQoqKgAhm4Ore",
        "site":     "levinellp.sharepoint.com/sites/Clients",
        "write_policy": "PROHIBITED",
        "allowed_read_prefixes": ["*"],
        "allowed_write_prefixes": [],
    },
    "clients_yellowbricks_capital": {
        "drive_id": "b!Z2HcxOh5RUCQGXT-pPqEiswlrvuCxxlNu8VyM91YlhqmbvhP5L-TQpgLoINPwldI",
        "site":     "levinellp.sharepoint.com/sites/Clients",
        "write_policy": "PROHIBITED",
        "allowed_read_prefixes": ["*"],
        "allowed_write_prefixes": [],
    },
    "clients_turtle_island": {
        "drive_id": "b!Z2HcxOh5RUCQGXT-pPqEiswlrvuCxxlNu8VyM91Ylhof4o2iicPrTbmFr3v1Tfqn",
        "site":     "levinellp.sharepoint.com/sites/Clients",
        "write_policy": "PROHIBITED",
        "allowed_read_prefixes": ["*"],
        "allowed_write_prefixes": [],
    },
    "clients_our_sharepoint_test2": {
        "drive_id": "b!Z2HcxOh5RUCQGXT-pPqEiswlrvuCxxlNu8VyM91YlhqDSqbgOonXT461weas6yuX",
        "site":     "levinellp.sharepoint.com/sites/Clients",
        "write_policy": "PROHIBITED",
        "allowed_read_prefixes": ["*"],
        "allowed_write_prefixes": [],
    },
    "clients_our_sharepoint_test": {
        "drive_id": "b!Z2HcxOh5RUCQGXT-pPqEiswlrvuCxxlNu8VyM91YlhoUEjlfIvbmTYGm-_TsK9WQ",
        "site":     "levinellp.sharepoint.com/sites/Clients",
        "write_policy": "PROHIBITED",
        "allowed_read_prefixes": ["*"],
        "allowed_write_prefixes": [],
    },
}

_DOC_LIBRARY_PREFIXES = {
    "documentation": ["Doc Pro  In Tray"],
}

_ALLOWLIST_CACHE: Optional[dict] = None
_TEMPLATE_REGISTRY_CACHE: Optional[dict] = None
_TOKEN_CACHE: Dict[str, Any] = {}  # resource_base -> {"token": str, "expires_at": float}


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


class EscalationRequiredError(RuntimeError):
    """Raised when the request must escalate instead of executing."""


class ApprovalRequiredError(RuntimeError):
    """Raised when the request requires an approval token before execution."""


_CLIENTS_SITE_PATH = "/sites/Clients"
_MANAGE_CLIENTS_ALLOWED_WITHOUT_TOKEN = {
    "page.get",
    "page.list",
    "navigation.get",
    "permissions.get",
    "site.get_structure",
    "site.get_settings",
    "folder.create",
    "folder.rename",
    "folder.move",
    "page.create",
    "page.update",
    "library.create",
    "library.update",
    "navigation.upsert",
    "navigation.reorder",
}
_MANAGE_CLIENTS_REQUIRES_TOKEN = {
    "page.publish",
    "page.unpublish",
    "page.set_home",
    "page.delete",
    "library.delete",
    "folder.delete",
    "navigation.delete",
    "permissions.grant",
    "permissions.revoke",
    "permissions.break_inheritance",
    "permissions.restore_inheritance",
}
_MANAGE_CLIENTS_ALL_OPERATIONS = (
    _MANAGE_CLIENTS_ALLOWED_WITHOUT_TOKEN | _MANAGE_CLIENTS_REQUIRES_TOKEN
)


def _utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _new_operation_id(tool_name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", tool_name.lower()).strip("_")
    return f"{slug}_{uuid4().hex[:12]}"


def _target_ref(**kwargs: Any) -> dict:
    return {
        key: value
        for key, value in kwargs.items()
        if value not in (None, "", [], {})
    }


def _hash_input_record(record: dict) -> str:
    payload = json.dumps(record, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _summarize_arguments(arguments: dict) -> dict:
    summary: dict = {}
    for key, value in arguments.items():
        if key == "content" and isinstance(value, str):
            summary["content_length"] = len(value)
            continue
        if key == "text_webparts" and isinstance(value, list):
            summary["text_webparts"] = [
                {
                    "webpart_id": str(entry.get("webpart_id", "")).strip(),
                    "content_length": (
                        len(entry.get("inner_html"))
                        if isinstance(entry, dict) and isinstance(entry.get("inner_html"), str)
                        else None
                    ),
                }
                for entry in value
            ]
            continue
        if key in ("page_role_assignments", "library_role_assignments") and isinstance(value, list):
            summary[key] = [
                {
                    "principal_id": entry.get("principal_id"),
                    "principal_name": (
                        str(entry.get("principal_name", "")).strip()
                        if isinstance(entry, dict)
                        else ""
                    ),
                    "role": (
                        str(entry.get("role", "")).strip()
                        if isinstance(entry, dict)
                        else ""
                    ),
                }
                for entry in value
            ]
            continue
        if isinstance(value, str) and len(value) > 256:
            summary[key] = value[:253] + "..."
            continue
        summary[key] = value
    return summary


def _response_payload(
    *,
    status: str,
    operation_id: str,
    target_ref: dict,
    result_payload: dict,
    errors: Optional[List[dict]] = None,
    warnings: Optional[List[str]] = None,
) -> str:
    return json.dumps(
        {
            "status": status,
            "operation_id": operation_id,
            "target_ref": target_ref,
            "result_payload": result_payload,
            "errors": errors or [],
            "warnings": warnings or [],
            "executed_at": _utc_now_iso(),
        },
        indent=2,
    )


def _error_status_for_exception(exc: Exception) -> str:
    message = str(exc).lower()
    if isinstance(exc, FileNotFoundError):
        return "not_found"
    if isinstance(exc, ApprovalRequiredError):
        return "approval_required"
    if isinstance(exc, EscalationRequiredError):
        return "escalation_required"
    if isinstance(exc, PermissionError):
        return "scope_denied"
    if isinstance(exc, ValueError):
        return "validation_failed"
    if "graph api 404" in message:
        return "not_found"
    if "version conflict" in message:
        return "version_conflict"
    return "connector_error"


def _error_payload(tool_name: str, exc: Exception, arguments: Optional[dict] = None) -> str:
    operation_id = _new_operation_id(tool_name)
    status = _error_status_for_exception(exc)
    input_record = _summarize_arguments(arguments or {})
    _audit_log(
        operation_id=operation_id,
        tool_name=tool_name,
        actor_type="agent",
        actor_id=str((arguments or {}).get("actor_id", "")).strip() or "sharepoint-mcp",
        authorized_scope="error_path",
        target_object=_target_ref(tool_name=tool_name),
        action_type="tool_error",
        output_status=status,
        input_record=input_record or None,
        reason_code=str((arguments or {}).get("reason_code", "")).strip() or None,
        upstream_artifact_ref=str((arguments or {}).get("upstream_artifact_ref", "")).strip() or None,
        approval_reference=str((arguments or {}).get("approval_reference", "")).strip() or None,
        escalation_flag=(status == "escalation_required"),
    )
    return _response_payload(
        status=status,
        operation_id=operation_id,
        target_ref=_target_ref(tool_name=tool_name),
        result_payload={},
        errors=[{"message": str(exc)}],
    )


def _audit_log(
    *,
    operation_id: str,
    tool_name: str,
    actor_type: str,
    actor_id: str,
    authorized_scope: str,
    target_object: dict,
    action_type: str,
    output_status: str,
    input_record: Optional[dict] = None,
    version_before: Optional[str] = None,
    version_after: Optional[str] = None,
    reason_code: Optional[str] = None,
    upstream_artifact_ref: Optional[str] = None,
    approval_reference: Optional[str] = None,
    escalation_flag: bool = False,
) -> None:
    payload = {
        "operation_id": operation_id,
        "tool_name": tool_name,
        "timestamp": _utc_now_iso(),
        "actor_type": actor_type,
        "actor_id": actor_id,
        "authorized_scope": authorized_scope,
        "target_object": target_object,
        "action_type": action_type,
        "output_status": output_status,
        "version_before": version_before,
        "version_after": version_after,
        "reason_code": reason_code,
        "upstream_artifact_ref": upstream_artifact_ref,
        "approval_reference": approval_reference,
        "escalation_flag": escalation_flag,
    }
    if input_record is not None:
        payload["input_hash"] = _hash_input_record(input_record)
    log.info(
        "audit_event=%s",
        json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str),
    )


# =============================================================================
# Path Validation
# =============================================================================

def _normalize_path(path: str) -> str:
    """Strip leading/trailing slashes for consistent comparison."""
    return path.strip("/")


def _normalize_drive_path(drive_alias: str, path: str) -> str:
    """
    Normalize a drive-relative path.

    Some historical docs used the library label as a leading segment. Strip it so
    runtime calls remain rooted at the Graph drive root.
    """
    norm = _normalize_path(path)
    if not norm:
        return norm
    for prefix in _DOC_LIBRARY_PREFIXES.get(drive_alias, []):
        prefix_norm = _normalize_path(prefix)
        if norm == prefix_norm:
            return ""
        if norm.startswith(prefix_norm + "/"):
            return norm[len(prefix_norm) + 1 :]
    return norm


def _quote_graph_path(path: str) -> str:
    return quote(path, safe="/")


def _drive_root_url(drive_id: str, path: str = "", suffix: str = "") -> str:
    norm = _normalize_path(path)
    if not norm:
        return f"{GRAPH_BASE}/drives/{drive_id}/root{suffix}"
    return f"{GRAPH_BASE}/drives/{drive_id}/root:/{_quote_graph_path(norm)}{suffix}"


def _is_full_library_prefix(prefix: str) -> bool:
    return _normalize_path(prefix) == "*"


def _is_full_library_read(drive_alias: str) -> bool:
    return any(
        _is_full_library_prefix(prefix)
        for prefix in _DRIVES[drive_alias]["allowed_read_prefixes"]
    )


def _matches_allowed_prefix(norm: str, prefix: str) -> bool:
    prefix_norm = _normalize_path(prefix)
    if _is_full_library_prefix(prefix_norm):
        return True
    return norm == prefix_norm or norm.startswith(prefix_norm + "/")


def _is_allowed_read(drive_alias: str, path: str) -> bool:
    """Return True iff path is within an allowed read prefix for the drive."""
    norm = _normalize_drive_path(drive_alias, path)
    drive = _DRIVES[drive_alias]
    return any(
        _matches_allowed_prefix(norm, prefix)
        for prefix in drive["allowed_read_prefixes"]
    )


def _is_allowed_write(drive_alias: str, path: str) -> bool:
    """Return True iff path is within an allowed write prefix for the drive."""
    norm = _normalize_drive_path(drive_alias, path)
    drive = _DRIVES[drive_alias]
    if drive["write_policy"] == "PROHIBITED":
        return False
    return any(
        _matches_allowed_prefix(norm, prefix)
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

def _get_resource_token(resource_base: str) -> str:
    import time as _time_module

    # Return cached token if it has more than 60 seconds of validity remaining.
    cached = _TOKEN_CACHE.get(resource_base)
    if cached and _time_module.time() < cached["expires_at"] - 60:
        return cached["token"]

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
        scopes=[f"{resource_base.rstrip('/')}/.default"]
    )
    if "access_token" not in result:
        raise RuntimeError(f"Token acquisition failed: {result}")

    expires_in = int(result.get("expires_in", 3600))
    _TOKEN_CACHE[resource_base] = {
        "token": result["access_token"],
        "expires_at": _time_module.time() + expires_in,
    }
    return result["access_token"]


def _get_token() -> str:
    return _get_resource_token("https://graph.microsoft.com")


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


def _graph_get_optional(url: str, params: Optional[dict] = None) -> Optional[dict]:
    token = _get_token()
    r = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=60,
    )
    if r.status_code == 404:
        return None
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


def _graph_post(url: str, payload: dict) -> dict:
    token = _get_token()
    r = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=120,
    )
    if r.status_code >= 400:
        raise RuntimeError(f"Graph API POST {r.status_code}: {r.text[:500]}")
    if not r.text:
        return {}
    return r.json()


def _graph_post_no_body(url: str) -> None:
    token = _get_token()
    r = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=120,
    )
    if r.status_code >= 400:
        raise RuntimeError(f"Graph API POST {r.status_code}: {r.text[:500]}")


def _graph_patch(url: str, payload: dict) -> dict:
    token = _get_token()
    r = requests.patch(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=120,
    )
    if r.status_code >= 400:
        raise RuntimeError(f"Graph API PATCH {r.status_code}: {r.text[:500]}")
    if not r.text:
        return {}
    return r.json()


def _graph_delete(url: str, *, if_match: Optional[str] = None) -> None:
    token = _get_token()
    headers = {"Authorization": f"Bearer {token}"}
    if if_match:
        headers["If-Match"] = if_match
    r = requests.delete(
        url,
        headers=headers,
        timeout=120,
    )
    if r.status_code >= 400:
        raise RuntimeError(f"Graph API DELETE {r.status_code}: {r.text[:500]}")


def _graph_raw_get(url: str) -> requests.Response:
    token = _get_token()
    r = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=120,
        allow_redirects=True,
    )
    return r


def _get_sharepoint_site_token(site_base_url: str) -> str:
    parsed = urlparse(site_base_url)
    resource_base = f"{parsed.scheme}://{parsed.netloc}"
    return _get_resource_token(resource_base)


def _get_sharepoint_form_digest(site_base_url: str) -> str:
    token = _get_sharepoint_site_token(site_base_url)
    resp = requests.post(
        f"{site_base_url.rstrip('/')}/_api/contextinfo",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json;odata=verbose",
        },
        timeout=60,
    )
    if resp.status_code >= 400:
        raise RuntimeError(f"SharePoint REST {resp.status_code}: {resp.text[:500]}")
    payload = resp.json()
    return str(
        payload.get("d", {})
        .get("GetContextWebInformation", {})
        .get("FormDigestValue")
        or ""
    )


def _sharepoint_rest_request(
    site_base_url: str,
    endpoint: str,
    *,
    method: str = "GET",
    payload: Optional[dict] = None,
    x_http_method: Optional[str] = None,
) -> dict:
    method = method.upper()
    token = _get_sharepoint_site_token(site_base_url)
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json;odata=verbose",
    }
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json;odata=verbose"
        data = json.dumps(payload)
    request_method = method
    if method != "GET" or x_http_method:
        headers["X-RequestDigest"] = _get_sharepoint_form_digest(site_base_url)
    if x_http_method:
        request_method = "POST"
        headers["X-HTTP-Method"] = x_http_method

    resp = requests.request(
        request_method,
        f"{site_base_url.rstrip('/')}{endpoint}",
        headers=headers,
        data=data,
        timeout=120,
    )
    if resp.status_code >= 400:
        raise RuntimeError(f"SharePoint REST {resp.status_code}: {resp.text[:500]}")
    if not resp.text:
        return {}
    return resp.json()


def _sharepoint_rest_get_optional(site_base_url: str, endpoint: str) -> Optional[dict]:
    try:
        return _sharepoint_rest_request(site_base_url, endpoint, method="GET")
    except RuntimeError as exc:
        if "sharepoint rest 404" in str(exc).lower():
            return None
        raise


def _load_sharepoint_allowlist() -> dict:
    global _ALLOWLIST_CACHE
    if _ALLOWLIST_CACHE is None:
        _ALLOWLIST_CACHE = json.loads(ALLOWLIST_PATH.read_text(encoding="utf-8"))
    return _ALLOWLIST_CACHE


def _load_template_registry() -> dict:
    global _TEMPLATE_REGISTRY_CACHE
    if _TEMPLATE_REGISTRY_CACHE is None:
        _TEMPLATE_REGISTRY_CACHE = json.loads(
            TEMPLATE_REGISTRY_PATH.read_text(encoding="utf-8")
        )
    return _TEMPLATE_REGISTRY_CACHE


def _item_relative_path(item: dict) -> str:
    parent_path = item.get("parentReference", {}).get("path", "")
    _, _, tail = parent_path.partition("/root:")
    tail = _normalize_path(tail)
    name = str(item.get("name") or "")
    if not tail:
        return name
    if not name:
        return tail
    return f"{tail}/{name}"


def _item_matches_prefixes(item: dict, prefixes: List[str]) -> bool:
    rel_path = _normalize_path(_item_relative_path(item))
    return any(_matches_allowed_prefix(rel_path, _normalize_path(p)) for p in prefixes)


def _slim_item_with_path(item: dict) -> dict:
    result = _slim_item(item)
    result["path"] = _item_relative_path(item)
    return result


def _get_drive_item_by_id(drive_id: str, item_id: str) -> Optional[dict]:
    url = (
        f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}"
        "?$select=id,name,webUrl,lastModifiedDateTime,size,file,folder,parentReference"
    )
    return _graph_get_optional(url)


def _download_drive_item_bytes(drive_id: str, item_id: str) -> bytes:
    url = f"{GRAPH_BASE}/drives/{drive_id}/items/{item_id}/content"
    resp = _graph_raw_get(url)
    if resp.status_code >= 400:
        raise RuntimeError(f"Graph API GET {resp.status_code}: {resp.text[:500]}")
    return resp.content


def _template_read_zones() -> List[dict]:
    allowlist = _load_sharepoint_allowlist()
    return list(allowlist.get("template_read_zones", []))


def _wip_write_zones() -> List[dict]:
    allowlist = _load_sharepoint_allowlist()
    return list(allowlist.get("wip_write_zones", []))


def _documentation_site_id() -> str:
    allowlist = _load_sharepoint_allowlist()
    return str(
        allowlist.get("documentation_site_authority", {}).get("site_id") or ""
    )


def _clients_sitepages_surface() -> dict:
    allowlist = _load_sharepoint_allowlist()
    surface = dict(allowlist.get("clients_sitepages_surface", {}))
    if not surface:
        raise RuntimeError("Clients SitePages surface is not configured in sharepoint_allowlist.json.")
    return surface


def _clients_workspace_provisioning_surface() -> dict:
    allowlist = _load_sharepoint_allowlist()
    surface = dict(allowlist.get("clients_workspace_provisioning_surface", {}))
    if not surface:
        raise RuntimeError(
            "Clients workspace provisioning surface is not configured in sharepoint_allowlist.json."
        )
    return surface


def _clients_site_management_surface() -> dict:
    allowlist = _load_sharepoint_allowlist()
    surface = dict(allowlist.get("clients_site_management_surface", {}))
    if not surface:
        surface = {
            "site": allowlist.get("clients_site_authority", {}).get("site"),
            "site_id": allowlist.get("clients_site_authority", {}).get("site_id"),
            "page_root_path": _clients_sitepages_surface().get("page_root_path", "SitePages"),
            "allowed_page_glob": _clients_sitepages_surface().get("allowed_page_glob", "SitePages/*.aspx"),
            "site_pages_list_title": _clients_workspace_provisioning_surface().get(
                "site_pages_list_title", "Site Pages"
            ),
            "allowed_navigation_locations": _clients_workspace_provisioning_surface().get(
                "allowed_navigation_locations", ["TopNavigationBar", "QuickLaunch", "Footer"]
            ),
            "allowed_role_definitions": _clients_workspace_provisioning_surface().get(
                "allowed_role_definitions", ["Read", "Contribute", "Edit", "Full Control"]
            ),
        }
    return surface


def _clients_site_id() -> str:
    return str(_clients_site_management_surface().get("site_id") or "")


def _clients_site_base_url() -> str:
    site = str(_clients_site_management_surface().get("site") or "").strip()
    if not site:
        raise RuntimeError("Clients management surface is missing a configured site.")
    return site if site.startswith("http") else f"https://{site}"


def _require_managed_workspace_site(site_id: str) -> None:
    doc_site_id = _documentation_site_id()
    if not doc_site_id or site_id != doc_site_id:
        raise PermissionError(
            "Write operations are permitted only on the Documentation managed_workspace site."
        )


def _canonical_zone_path(prefix: str) -> str:
    return _normalize_drive_path("documentation", _normalize_path(prefix).lstrip("/"))


def _escape_odata_string(value: str) -> str:
    return value.replace("'", "''")


def _normalize_etag(value: Any) -> str:
    return str(value or "").strip().strip('"')


def _normalize_clients_page_path(page_path: str) -> str:
    surface = _clients_site_management_surface()
    root = _normalize_path(str(surface.get("page_root_path") or "SitePages"))
    norm = _normalize_path(page_path)

    if not norm:
        raise ValueError("'page_path' is required.")
    if "\\" in page_path or ".." in norm.split("/"):
        raise ValueError("'page_path' must not contain backslashes or '..'.")

    expected_pattern = rf"(?i)^{re.escape(root)}/[^/]+\.aspx$"
    if not re.match(expected_pattern, norm):
        raise PermissionError(
            f"Page path '{page_path}' is outside the approved Clients SitePages surface. "
            f"Expected '{root}/<page>.aspx'."
        )

    return f"{root}/{norm.split('/')[-1]}"


def _normalize_clients_site_path(site_path: str) -> str:
    if str(site_path or "").strip() != _CLIENTS_SITE_PATH:
        raise PermissionError(
            f"This tool is hard-limited to '{_CLIENTS_SITE_PATH}'."
        )
    return _CLIENTS_SITE_PATH


def _normalize_clients_site_relative_path(
    path: str,
    *,
    allow_empty: bool = False,
) -> str:
    raw = str(path or "").strip()
    if not raw:
        if allow_empty:
            return ""
        raise ValueError("'path' must not be empty.")

    parsed = urlparse(raw)
    if parsed.scheme or parsed.netloc:
        if parsed.netloc and parsed.netloc.lower() != "levinellp.sharepoint.com":
            raise PermissionError("Only the SharePoint host levinellp.sharepoint.com is permitted.")
        raw = parsed.path

    raw = raw.strip()
    if raw.startswith(_CLIENTS_SITE_PATH):
        raw = raw[len(_CLIENTS_SITE_PATH) :]
    elif raw.startswith(_CLIENTS_SITE_PATH.lstrip("/")):
        raw = raw[len(_CLIENTS_SITE_PATH.lstrip("/")) :]

    normalized = _normalize_path(raw)
    if not normalized and allow_empty:
        return ""
    if "\\" in str(path) or ".." in normalized.split("/"):
        raise PermissionError("'path' must not contain backslashes or '..'.")
    if not normalized:
        raise ValueError("'path' must not be empty.")
    return normalized


def _clients_server_relative_path(site_relative_path: str) -> str:
    norm = _normalize_clients_site_relative_path(site_relative_path, allow_empty=True)
    if not norm:
        return _CLIENTS_SITE_PATH
    return f"{_CLIENTS_SITE_PATH}/{norm}"


def _slugify_client_name(client_name: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", client_name).strip("-")
    if not slug:
        raise ValueError("'client_name' must include at least one alphanumeric character.")
    return slug


def _normalize_clients_page_name(page_name: str) -> str:
    name = page_name.strip()
    if not name:
        raise ValueError("'page_name' must not be empty.")
    if "/" in name or "\\" in name or ".." in name:
        raise ValueError("'page_name' must be a plain filename without path separators.")
    if not re.match(r"(?i)^[^/]+\.aspx$", name):
        raise ValueError("'page_name' must end with '.aspx'.")
    return name


def _normalize_clients_provisioning_page_path(page_name: str) -> str:
    root = _normalize_path(
        str(_clients_workspace_provisioning_surface().get("page_root_path") or "SitePages")
    )
    return f"{root}/{_normalize_clients_page_name(page_name)}"


def _validate_clients_library_name(library_name: str) -> str:
    name = library_name.strip()
    if not name:
        raise ValueError("'library_name' must not be empty.")
    surface = _clients_workspace_provisioning_surface()
    pattern = str(surface.get("allowed_library_name_regex") or "").strip()
    if pattern and not re.match(pattern, name):
        raise PermissionError(
            f"Library name '{library_name}' is outside the approved Clients provisioning pattern."
        )
    return name


def _validate_clients_managed_library_name(library_name: str) -> str:
    name = library_name.strip()
    if not name:
        raise ValueError("'library_name' must not be empty.")
    if "/" in name or "\\" in name or ".." in name:
        raise ValueError("'library_name' must not contain path separators or '..'.")
    return name


def _resolve_clients_site_page(page_path: str) -> dict:
    site_id = _clients_site_id()
    if not site_id:
        raise RuntimeError("Clients SitePages surface is missing a configured site_id.")

    norm_path = _normalize_clients_page_path(page_path)
    page_name = norm_path.rsplit("/", 1)[-1]
    url = f"{GRAPH_BASE}/sites/{site_id}/pages/microsoft.graph.sitePage"
    payload = _graph_get(
        url,
        params={"$filter": f"name eq '{_escape_odata_string(page_name)}'"},
    )
    pages = list(payload.get("value", []))
    if not pages:
        raise FileNotFoundError(
            f"Site page '{norm_path}' was not found in the approved Clients SitePages surface."
        )
    if len(pages) > 1:
        raise EscalationRequiredError(
            f"Multiple site pages matched '{page_name}'. Resolve ambiguity before execution."
        )

    page = pages[0]
    page_id = str(page.get("id") or "").strip()
    if not page_id:
        raise RuntimeError(f"Resolved site page '{norm_path}' is missing an id.")

    detail = _graph_get(
        f"{GRAPH_BASE}/sites/{site_id}/pages/{page_id}/microsoft.graph.sitePage"
    )
    return {
        "site_id": site_id,
        "page_id": page_id,
        "page_path": norm_path,
        "page": detail,
    }


def _list_site_page_webparts(site_id: str, page_id: str) -> List[dict]:
    payload = _graph_get(
        f"{GRAPH_BASE}/sites/{site_id}/pages/{page_id}/microsoft.graph.sitePage/webParts"
    )
    return list(payload.get("value", []))


def _get_site_page_webpart(site_id: str, page_id: str, webpart_id: str) -> dict:
    return _graph_get(
        f"{GRAPH_BASE}/sites/{site_id}/pages/{page_id}/microsoft.graph.sitePage/webParts/{webpart_id}"
    )


def _require_write_context(
    args: dict,
    *,
    require_approval_reference: bool = False,
) -> dict:
    context = {
        "run_id": str(args.get("run_id", "")).strip(),
        "workflow_ref": str(args.get("workflow_ref", "")).strip(),
        "runbook_ref": str(args.get("runbook_ref", "")).strip(),
        "capability_ref": str(args.get("capability_ref", "")).strip(),
        "artifact_version_ref": str(args.get("artifact_version_ref", "")).strip(),
        "provenance_label": str(args.get("provenance_label", "")).strip(),
        "reason_code": str(args.get("reason_code", "")).strip(),
        "upstream_artifact_ref": str(args.get("upstream_artifact_ref", "")).strip(),
        "actor_id": str(args.get("actor_id", "")).strip() or "sharepoint-mcp",
        "approval_reference": str(args.get("approval_reference", "")).strip(),
        "human_operator_id": str(args.get("human_operator_id", "")).strip(),
    }

    if not any(
        context[key] for key in ("workflow_ref", "runbook_ref", "capability_ref")
    ):
        raise ValueError(
            "One of 'workflow_ref', 'runbook_ref', or 'capability_ref' is required for write operations."
        )

    for field in (
        "run_id",
        "artifact_version_ref",
        "provenance_label",
        "reason_code",
        "upstream_artifact_ref",
    ):
        if not context[field]:
            raise ValueError(f"'{field}' is required for write operations.")

    if not re.match(r"(?i)^derived from ml2 v\S+", context["provenance_label"]):
        raise ValueError(
            "'provenance_label' must begin with 'Derived from ML2 v'."
        )

    if require_approval_reference and not context["approval_reference"]:
        raise EscalationRequiredError(
            "This action requires a valid 'approval_reference'."
        )

    return context


def _sp_d(payload: dict) -> Any:
    return payload.get("d", payload)


def _build_default_client_workspace_html(client_name: str, library_web_url: str) -> str:
    return (
        f"<h2><strong>Welcome to the {client_name} Workspace</strong></h2>"
        f"<p>This secure workspace is for documents, updates, and communication related to {client_name}.</p>"
        "<p><strong>Use this workspace to:</strong></p>"
        "<ul>"
        f"<li><a href=\"{library_web_url}\">View Documents</a></li>"
        "<li>Upload new files for review through the approved client library</li>"
        "<li>Review client-specific instructions and shared resources</li>"
        "<li>Contact Levine Law with your company name and matter details when support is needed</li>"
        "</ul>"
        "<p><strong>Important:</strong> Use the approved client library for sensitive documents and avoid duplicate copies in email or personal storage.</p>"
    )


def _build_text_canvas_layout(body_html: str) -> dict:
    return {
        "horizontalSections": [
            {
                "layout": "oneColumn",
                "id": "1",
                "emphasis": "none",
                "columns": [
                    {
                        "id": "1",
                        "width": 12,
                        "webparts": [
                            {
                                "@odata.type": "#microsoft.graph.textWebPart",
                                "id": str(uuid4()),
                                "innerHtml": body_html,
                            }
                        ],
                    }
                ],
            }
        ]
    }


def _clients_allowed_role_definitions() -> List[str]:
    return [
        str(name).strip()
        for name in _clients_site_management_surface().get("allowed_role_definitions", [])
        if str(name).strip()
    ]


def _resolve_sharepoint_role_definition_id(site_base_url: str, role_name: str) -> int:
    normalized = role_name.strip()
    if normalized not in _clients_allowed_role_definitions():
        raise PermissionError(
            f"Role '{role_name}' is outside the approved Clients provisioning role set."
        )
    payload = _sharepoint_rest_request(
        site_base_url,
        f"/_api/web/roledefinitions/getbyname('{_escape_odata_string(normalized)}')/id",
        method="GET",
    )
    role_id = _sp_d(payload).get("Id")
    if role_id is None:
        raise RuntimeError(f"Role definition '{role_name}' did not return an id.")
    return int(role_id)


def _resolve_sharepoint_principal(site_base_url: str, principal: dict) -> dict:
    principal_id = principal.get("principal_id")
    principal_name = str(principal.get("principal_name", "")).strip()

    if principal_id is not None and str(principal_id).strip():
        payload = _sharepoint_rest_request(
            site_base_url,
            f"/_api/web/siteusers/getbyid({int(principal_id)})?$select=Id,Title,LoginName,PrincipalType",
            method="GET",
        )
        data = _sp_d(payload)
        return {
            "id": int(data.get("Id")),
            "title": str(data.get("Title") or ""),
            "loginName": str(data.get("LoginName") or ""),
            "principalType": data.get("PrincipalType"),
        }

    if not principal_name:
        raise ValueError(
            "Each role-assignment entry requires either 'principal_id' or 'principal_name'."
        )

    site_group = _sharepoint_rest_get_optional(
        site_base_url,
        f"/_api/web/sitegroups/getbyname('{_escape_odata_string(principal_name)}')?$select=Id,Title,LoginName,PrincipalType",
    )
    if site_group:
        data = _sp_d(site_group)
        return {
            "id": int(data.get("Id")),
            "title": str(data.get("Title") or principal_name),
            "loginName": str(data.get("LoginName") or ""),
            "principalType": data.get("PrincipalType"),
        }

    payload = _sharepoint_rest_request(
        site_base_url,
        "/_api/web/siteusers"
        f"?$select=Id,Title,LoginName,PrincipalType"
        f"&$filter=Title eq '{_escape_odata_string(principal_name)}'",
        method="GET",
    )
    results = list(_sp_d(payload).get("results", []))
    if not results:
        raise FileNotFoundError(
            f"Principal '{principal_name}' was not found among SharePoint site groups or site users."
        )
    if len(results) > 1:
        raise EscalationRequiredError(
            f"Multiple SharePoint principals matched '{principal_name}'. Resolve the ambiguity before execution."
        )
    data = results[0]
    return {
        "id": int(data.get("Id")),
        "title": str(data.get("Title") or principal_name),
        "loginName": str(data.get("LoginName") or ""),
        "principalType": data.get("PrincipalType"),
    }


def _prepare_role_assignments(site_base_url: str, assignments: list, label: str) -> List[dict]:
    if not isinstance(assignments, list) or not assignments:
        raise ValueError(f"'{label}' must be a non-empty array.")

    prepared: List[dict] = []
    seen_principal_ids = set()
    for entry in assignments:
        if not isinstance(entry, dict):
            raise ValueError(f"Each '{label}' entry must be an object.")
        role_name = str(entry.get("role", "")).strip()
        if not role_name:
            raise ValueError(f"Each '{label}' entry requires 'role'.")
        principal_info = _resolve_sharepoint_principal(site_base_url, entry)
        if principal_info["id"] in seen_principal_ids:
            raise ValueError(
                f"Duplicate principal '{principal_info['title']}' in '{label}'."
            )
        seen_principal_ids.add(principal_info["id"])
        prepared.append(
            {
                "principal": principal_info,
                "role": role_name,
                "roledefid": _resolve_sharepoint_role_definition_id(site_base_url, role_name),
            }
        )
    return prepared


def _break_list_role_inheritance(site_base_url: str, list_title: str) -> None:
    _sharepoint_rest_request(
        site_base_url,
        f"/_api/web/lists/getbytitle('{_escape_odata_string(list_title)}')/breakroleinheritance(false)",
        method="POST",
    )


def _break_list_item_role_inheritance(site_base_url: str, list_title: str, item_id: int) -> None:
    _sharepoint_rest_request(
        site_base_url,
        f"/_api/web/lists/getbytitle('{_escape_odata_string(list_title)}')/items({item_id})/breakroleinheritance(false)",
        method="POST",
    )


def _add_list_role_assignment(site_base_url: str, list_title: str, principal_id: int, roledefid: int) -> None:
    _sharepoint_rest_request(
        site_base_url,
        f"/_api/web/lists/getbytitle('{_escape_odata_string(list_title)}')/roleassignments/addroleassignment(principalid={principal_id},roledefid={roledefid})",
        method="POST",
    )


def _add_list_item_role_assignment(
    site_base_url: str,
    list_title: str,
    item_id: int,
    principal_id: int,
    roledefid: int,
) -> None:
    _sharepoint_rest_request(
        site_base_url,
        f"/_api/web/lists/getbytitle('{_escape_odata_string(list_title)}')/items({item_id})/roleassignments/addroleassignment(principalid={principal_id},roledefid={roledefid})",
        method="POST",
    )


def _clients_site_page_list_title() -> str:
    return str(
        _clients_site_management_surface().get("site_pages_list_title") or "Site Pages"
    )


def _get_clients_page_list_item(page_name: str) -> dict:
    site_base_url = _clients_site_base_url()
    payload = _sharepoint_rest_request(
        site_base_url,
        f"/_api/web/lists/getbytitle('{_escape_odata_string(_clients_site_page_list_title())}')/items"
        f"?$select=Id,FileLeafRef,Title,HasUniqueRoleAssignments"
        f"&$filter=FileLeafRef eq '{_escape_odata_string(page_name)}'",
        method="GET",
    )
    results = list(_sp_d(payload).get("results", []))
    if not results:
        raise FileNotFoundError(f"Site Pages item '{page_name}' was not found.")
    if len(results) > 1:
        raise EscalationRequiredError(
            f"Multiple Site Pages items matched '{page_name}'. Resolve the ambiguity before execution."
        )
    return results[0]


def _get_clients_list_by_title_optional(list_title: str) -> Optional[dict]:
    return _sharepoint_rest_get_optional(
        _clients_site_base_url(),
        f"/_api/web/lists/getbytitle('{_escape_odata_string(list_title)}')"
        "?$select=Id,Title,HasUniqueRoleAssignments,RootFolder/ServerRelativeUrl,RootFolder/WelcomePage"
        "&$expand=RootFolder",
    )


def _create_clients_document_library(library_name: str, description: str) -> dict:
    return _graph_post(
        f"{GRAPH_BASE}/sites/{_clients_site_id()}/lists",
        {
            "displayName": library_name,
            "description": description,
            "list": {"template": "documentLibrary"},
        },
    )


def _create_clients_site_page(page_name: str, title: str, description: str, body_html: str) -> dict:
    return _graph_post(
        f"{GRAPH_BASE}/sites/{_clients_site_id()}/pages",
        {
            "@odata.type": "#microsoft.graph.sitePage",
            "name": page_name,
            "title": title,
            "description": description,
            "pageLayout": "article",
            "showComments": False,
            "showRecommendedPages": False,
            "canvasLayout": {
                "horizontalSections": [
                    {
                        "layout": "oneColumn",
                        "id": "1",
                        "emphasis": "none",
                        "columns": [
                            {
                                "id": "1",
                                "width": 12,
                                "webparts": [
                                    {
                                        "id": str(uuid4()),
                                        "innerHtml": body_html,
                                    }
                                ],
                            }
                        ],
                    }
                ]
            },
        },
    )


def _enable_clients_nav_audience_targeting(site_base_url: str) -> None:
    _sharepoint_rest_request(
        site_base_url,
        "/_api/web",
        method="POST",
        x_http_method="MERGE",
        payload={
            "__metadata": {"type": "SP.Web"},
            "NavAudienceTargetingEnabled": True,
        },
    )


def _find_navigation_node_by_title(site_base_url: str, title: str) -> Optional[dict]:
    location = "TopNavigationBar"
    payload = _sharepoint_rest_request(
        site_base_url,
        f"/_api/web/navigation/{location}?$select=Id,Title,Url,IsExternal",
        method="GET",
    )
    for node in _sp_d(payload).get("results", []):
        if str(node.get("Title") or "") == title:
            return node
    return None


def _navigation_location_endpoint(location: str) -> str:
    if location not in {
        str(value).strip()
        for value in _clients_site_management_surface().get("allowed_navigation_locations", [])
        if str(value).strip()
    }:
        raise PermissionError(
            f"Navigation location '{location}' is outside the approved Clients management surface."
        )
    return f"/_api/web/navigation/{location}"


def _get_navigation_node_by_id(site_base_url: str, node_id: int) -> dict:
    payload = _sharepoint_rest_request(
        site_base_url,
        f"/_api/web/navigation/getnodebyid({node_id})?$select=Id,Title,Url,IsExternal",
        method="GET",
    )
    return _sp_d(payload)


def _find_navigation_node_by_title_and_location(
    site_base_url: str,
    title: str,
    location: str,
) -> Optional[dict]:
    payload = _sharepoint_rest_request(
        site_base_url,
        f"{_navigation_location_endpoint(location)}?$select=Id,Title,Url,IsExternal",
        method="GET",
    )
    for node in _sp_d(payload).get("results", []):
        if str(node.get("Title") or "") == title:
            return node
    return None


def _create_navigation_node(site_base_url: str, title: str, url: str, location: str) -> dict:
    endpoint_base = _navigation_location_endpoint(location)
    attempts = [
        (
            f"{endpoint_base}/Add",
            {
                "parameters": {
                    "__metadata": {"type": "SP.NavigationNodeCreationInformation"},
                    "Title": title,
                    "Url": url,
                    "AsLastNode": True,
                    "IsExternal": False,
                }
            },
        ),
        (
            endpoint_base,
            {
                "__metadata": {"type": "SP.NavigationNode"},
                "Title": title,
                "Url": url,
                "IsExternal": False,
            },
        ),
    ]
    last_error: Optional[Exception] = None
    for endpoint, payload in attempts:
        try:
            response = _sharepoint_rest_request(
                site_base_url,
                endpoint,
                method="POST",
                payload=payload,
            )
            data = _sp_d(response)
            if data and data.get("Id") is not None:
                return data
            found = _find_navigation_node_by_title_and_location(site_base_url, title, location)
            if found:
                return found
        except Exception as exc:  # pragma: no cover - fallback path
            last_error = exc
    if last_error is not None:
        raise last_error
    raise RuntimeError("Navigation node creation did not return a result.")


def _create_top_navigation_node(site_base_url: str, title: str, url: str) -> dict:
    return _create_navigation_node(site_base_url, title, url, "TopNavigationBar")


def _set_navigation_node_audiences(site_base_url: str, node_id: int, audience_ids: List[str]) -> None:
    if not audience_ids:
        return
    _enable_clients_nav_audience_targeting(site_base_url)
    payloads = [
        {
            "__metadata": {"type": "SP.NavigationNode"},
            "AudienceIds": {"results": audience_ids},
        },
        {
            "__metadata": {"type": "SP.NavigationNode"},
            "AudienceIds": {
                "__metadata": {"type": "Collection(Edm.String)"},
                "results": audience_ids,
            },
        },
    ]
    last_error: Optional[Exception] = None
    for payload in payloads:
        try:
            _sharepoint_rest_request(
                site_base_url,
                f"/_api/web/navigation/getnodebyid({node_id})",
                method="POST",
                x_http_method="MERGE",
                payload=payload,
            )
            return
        except Exception as exc:  # pragma: no cover - fallback path
            last_error = exc
    if last_error is not None:
        raise last_error


def _update_navigation_node(
    site_base_url: str,
    node_id: int,
    *,
    title: str,
    url: str,
    is_external: bool = False,
) -> dict:
    _sharepoint_rest_request(
        site_base_url,
        f"/_api/web/navigation/getnodebyid({node_id})",
        method="POST",
        x_http_method="MERGE",
        payload={
            "__metadata": {"type": "SP.NavigationNode"},
            "Title": title,
            "Url": url,
            "IsExternal": bool(is_external),
        },
    )
    return _get_navigation_node_by_id(site_base_url, node_id)


def _delete_navigation_node(site_base_url: str, node_id: int) -> None:
    _sharepoint_rest_request(
        site_base_url,
        f"/_api/web/navigation/getnodebyid({node_id})",
        method="POST",
        x_http_method="DELETE",
    )


def _reset_list_role_inheritance(site_base_url: str, list_title: str) -> None:
    _sharepoint_rest_request(
        site_base_url,
        f"/_api/web/lists/getbytitle('{_escape_odata_string(list_title)}')/resetroleinheritance()",
        method="POST",
    )


def _reset_list_item_role_inheritance(site_base_url: str, list_title: str, item_id: int) -> None:
    _sharepoint_rest_request(
        site_base_url,
        f"/_api/web/lists/getbytitle('{_escape_odata_string(list_title)}')/items({item_id})/resetroleinheritance()",
        method="POST",
    )


def _update_clients_document_library(
    current_library_name: str,
    *,
    new_library_name: Optional[str] = None,
    description: Optional[str] = None,
) -> dict:
    payload = {"__metadata": {"type": "SP.List"}}
    if new_library_name is not None:
        payload["Title"] = new_library_name
    if description is not None:
        payload["Description"] = description
    _sharepoint_rest_request(
        _clients_site_base_url(),
        f"/_api/web/lists/getbytitle('{_escape_odata_string(current_library_name)}')",
        method="POST",
        x_http_method="MERGE",
        payload=payload,
    )
    return _get_clients_list_by_title_optional(new_library_name or current_library_name) or {}


def _create_clients_list(
    list_name: str,
    description: str,
    *,
    list_template: str,
) -> dict:
    return _graph_post(
        f"{GRAPH_BASE}/sites/{_clients_site_id()}/lists",
        {
            "displayName": list_name,
            "description": description,
            "list": {"template": list_template},
        },
    )


def _normalize_clients_navigation_location(location: str) -> str:
    raw = str(location or "").strip()
    mapping = {
        "quicklaunch": "QuickLaunch",
        "topnavigation": "TopNavigationBar",
        "topnavigationbar": "TopNavigationBar",
        "footer": "Footer",
    }
    normalized = mapping.get(re.sub(r"[^a-z]", "", raw.lower()), raw)
    return str(normalized).strip()


def _normalize_manage_clients_page_layout(layout: str) -> str:
    value = str(layout or "").strip()
    if value not in {"article", "home", "singleWebPartAppPage", "repostPage"}:
        raise ValueError(
            "'page_layout' must be one of 'article', 'home', 'singleWebPartAppPage', or 'repostPage'."
        )
    return value


def _page_path_from_name(page_name: str) -> str:
    root = str(_clients_site_management_surface().get("page_root_path") or "SitePages").strip() or "SitePages"
    return _normalize_clients_page_path(
        f"{_normalize_path(root)}/{_normalize_clients_page_name(page_name)}"
    )


def _resolve_clients_site_page_by_id(page_id: str) -> dict:
    site_id = _clients_site_id()
    detail = _graph_get(
        f"{GRAPH_BASE}/sites/{site_id}/pages/{page_id}/microsoft.graph.sitePage"
    )
    page_name = str(detail.get("name") or "").strip()
    if not page_name:
        raise RuntimeError(f"Resolved page id '{page_id}' did not return a name.")
    page_path = _page_path_from_name(page_name)
    return {
        "site_id": site_id,
        "page_id": str(detail.get("id") or page_id),
        "page_path": page_path,
        "page": detail,
    }


def _site_page_payload_to_canvas_layout(page_canvas: Optional[list]) -> dict:
    if page_canvas is None:
        return _build_text_canvas_layout("<p></p>")
    if not isinstance(page_canvas, list):
        raise ValueError("'page_canvas' must be an array when provided.")
    return {"horizontalSections": page_canvas}


def _clients_server_relative_page_path(page_path: str) -> str:
    return _clients_server_relative_path(_normalize_clients_page_path(page_path))


def _publish_clients_site_page(page_id: str) -> None:
    _graph_post_no_body(
        f"{GRAPH_BASE}/sites/{_clients_site_id()}/pages/{page_id}/microsoft.graph.sitePage/publish"
    )


def _unpublish_clients_site_page(page_path: str, comment: str) -> None:
    server_relative_path = _clients_server_relative_page_path(page_path)
    escaped_path = _escape_odata_string(server_relative_path)
    escaped_comment = _escape_odata_string(comment)
    _sharepoint_rest_request(
        _clients_site_base_url(),
        f"/_api/web/GetFileByServerRelativeUrl('{escaped_path}')/Unpublish(comment='{escaped_comment}')",
        method="POST",
    )


def _set_clients_home_page(page_path: str) -> None:
    norm_page_path = _normalize_clients_page_path(page_path)
    _sharepoint_rest_request(
        _clients_site_base_url(),
        "/_api/web/rootfolder",
        method="POST",
        x_http_method="MERGE",
        payload={
            "__metadata": {"type": "SP.Folder"},
            "WelcomePage": norm_page_path,
        },
    )


def _clients_drives() -> List[dict]:
    return _graph_paged_get(
        f"{GRAPH_BASE}/sites/{_clients_site_id()}/drives?$select=id,name,webUrl"
    )


def _get_clients_drive_by_name(library_name: str) -> dict:
    matches = [
        drive
        for drive in _clients_drives()
        if str(drive.get("name") or "").strip().lower() == library_name.strip().lower()
    ]
    if not matches:
        raise FileNotFoundError(f"Document library '{library_name}' was not found.")
    if len(matches) > 1:
        raise EscalationRequiredError(
            f"Multiple drives matched library '{library_name}'. Resolve ambiguity before execution."
        )
    return matches[0]


def _split_clients_library_path(path: str) -> tuple[str, str]:
    normalized = _normalize_clients_site_relative_path(path)
    parts = normalized.split("/", 1)
    library_name = parts[0].strip()
    if not library_name:
        raise ValueError("'path' must begin with a library name inside /sites/Clients.")
    relative_path = parts[1].strip() if len(parts) > 1 else ""
    return library_name, relative_path


def _resolve_clients_library(
    *,
    library_name: Optional[str] = None,
    list_id: Optional[str] = None,
) -> dict:
    if list_id:
        list_data = _graph_get(
            f"{GRAPH_BASE}/sites/{_clients_site_id()}/lists/{list_id}"
            "?$select=id,name,displayName,description,webUrl"
        )
        resolved_name = (
            str(list_data.get("displayName") or "").strip()
            or str(list_data.get("name") or "").strip()
        )
        rest_state = _get_clients_list_by_title_optional(resolved_name) or {}
        return {
            "list_id": str(list_data.get("id") or list_id),
            "library_name": resolved_name,
            "graph": list_data,
            "rest": _sp_d(rest_state) if rest_state else {},
        }

    normalized_name = _validate_clients_managed_library_name(str(library_name or "").strip())
    rest_state = _get_clients_list_by_title_optional(normalized_name)
    if not rest_state:
        raise FileNotFoundError(f"Document library '{normalized_name}' was not found.")
    data = _sp_d(rest_state)
    return {
        "list_id": str(data.get("Id") or ""),
        "library_name": str(data.get("Title") or normalized_name),
        "graph": {},
        "rest": data,
    }


def _resolve_clients_drive_item_by_path(path: str) -> dict:
    library_name, relative_path = _split_clients_library_path(path)
    if not relative_path:
        raise ValueError("Folder and file operations require a path below the library root.")
    drive = _get_clients_drive_by_name(library_name)
    drive_id = str(drive.get("id") or "")
    item = _graph_get_optional(
        (
            _drive_root_url(drive_id, relative_path)
            + "?$select=id,name,webUrl,eTag,lastModifiedDateTime,size,file,folder,parentReference,sharepointIds"
        )
    )
    if item is None:
        raise FileNotFoundError(f"Path '{path}' was not found.")
    sharepoint_ids = item.get("sharepointIds") or {}
    list_item_id = sharepoint_ids.get("listItemId")
    return {
        "library_name": library_name,
        "relative_path": relative_path,
        "drive": drive,
        "drive_id": drive_id,
        "item": item,
        "item_id": str(item.get("id") or ""),
        "list_item_id": int(list_item_id) if str(list_item_id or "").strip() else None,
    }


def _create_clients_folder(folder_path: str) -> dict:
    library_name, relative_path = _split_clients_library_path(folder_path)
    parent_path, _, folder_name = relative_path.rpartition("/")
    if not folder_name:
        raise ValueError("'folder_path' must end with a folder name.")
    drive = _get_clients_drive_by_name(library_name)
    drive_id = str(drive.get("id") or "")
    parent_url = (
        _drive_root_url(drive_id, parent_path, ":/children")
        if parent_path
        else _drive_root_url(drive_id, "", "/children")
    )
    return _graph_post(
        parent_url,
        {
            "name": folder_name,
            "folder": {},
            "@microsoft.graph.conflictBehavior": "fail",
        },
    )


def _move_or_rename_clients_folder(
    folder_path: str,
    *,
    destination_path: Optional[str] = None,
    new_name: Optional[str] = None,
) -> dict:
    resolved = _resolve_clients_drive_item_by_path(folder_path)
    item = resolved["item"]
    if "folder" not in item:
        raise ValueError(f"Path '{folder_path}' is not a folder.")

    payload: dict = {}
    if new_name is not None:
        normalized_name = str(new_name).strip()
        if not normalized_name or "/" in normalized_name or "\\" in normalized_name or ".." in normalized_name:
            raise ValueError("'new_name' must be a plain folder name without path separators.")
        payload["name"] = normalized_name

    if destination_path is not None:
        dest_library_name, dest_relative_path = _split_clients_library_path(destination_path)
        if dest_library_name.lower() != resolved["library_name"].lower():
            raise PermissionError(
                "folder.move currently supports moves only within the same Clients document library."
            )
        dest_parent = _graph_get_optional(
            (
                _drive_root_url(resolved["drive_id"], dest_relative_path)
                + "?$select=id,name,folder"
            )
        )
        if dest_parent is None:
            raise FileNotFoundError(
                f"Destination folder '{destination_path}' was not found."
            )
        if "folder" not in dest_parent:
            raise ValueError(f"Destination '{destination_path}' is not a folder.")
        payload["parentReference"] = {"id": str(dest_parent.get("id") or "")}

    if not payload:
        raise ValueError("No folder move or rename change was supplied.")

    return _graph_patch(
        f"{GRAPH_BASE}/drives/{resolved['drive_id']}/items/{resolved['item_id']}",
        payload,
    )


def _delete_clients_folder(folder_path: str) -> None:
    resolved = _resolve_clients_drive_item_by_path(folder_path)
    if "folder" not in resolved["item"]:
        raise ValueError(f"Path '{folder_path}' is not a folder.")
    _graph_delete(f"{GRAPH_BASE}/drives/{resolved['drive_id']}/items/{resolved['item_id']}")


def _navigation_children_endpoint(parent_id: int) -> str:
    return f"/_api/web/navigation/getnodebyid({parent_id})/Children"


def _list_navigation_nodes(site_base_url: str, location: str) -> List[dict]:
    payload = _sharepoint_rest_request(
        site_base_url,
        f"{_navigation_location_endpoint(location)}?$select=Id,Title,Url,IsExternal",
        method="GET",
    )
    return list(_sp_d(payload).get("results", []))


def _list_navigation_child_nodes(site_base_url: str, parent_id: int) -> List[dict]:
    payload = _sharepoint_rest_request(
        site_base_url,
        f"{_navigation_children_endpoint(parent_id)}?$select=Id,Title,Url,IsExternal",
        method="GET",
    )
    return list(_sp_d(payload).get("results", []))


def _create_navigation_child_node(
    site_base_url: str,
    parent_id: int,
    title: str,
    url: str,
    is_external: bool = False,
) -> dict:
    response = _sharepoint_rest_request(
        site_base_url,
        _navigation_children_endpoint(parent_id),
        method="POST",
        payload={
            "__metadata": {"type": "SP.NavigationNode"},
            "Title": title,
            "Url": url,
            "IsExternal": bool(is_external),
        },
    )
    data = _sp_d(response)
    if data and data.get("Id") is not None:
        return data
    for node in _list_navigation_child_nodes(site_base_url, parent_id):
        if str(node.get("Title") or "") == title:
            return node
    raise RuntimeError("Navigation child creation did not return a result.")


def _find_navigation_child_by_title(
    site_base_url: str,
    parent_id: int,
    title: str,
) -> Optional[dict]:
    for node in _list_navigation_child_nodes(site_base_url, parent_id):
        if str(node.get("Title") or "") == title:
            return node
    return None


def _move_navigation_node_to_first(site_base_url: str, node_id: int) -> None:
    _sharepoint_rest_request(
        site_base_url,
        f"/_api/web/navigation/getnodebyid({node_id})/moveToFirst()",
        method="POST",
    )


def _move_navigation_node_after(site_base_url: str, node_id: int, previous_node_id: int) -> None:
    _sharepoint_rest_request(
        site_base_url,
        f"/_api/web/navigation/getnodebyid({node_id})/moveAfter({previous_node_id})",
        method="POST",
    )


def _add_web_role_assignment(site_base_url: str, principal_id: int, roledefid: int) -> None:
    _sharepoint_rest_request(
        site_base_url,
        f"/_api/web/roleassignments/addroleassignment(principalid={principal_id},roledefid={roledefid})",
        method="POST",
    )


def _remove_web_role_assignment(site_base_url: str, principal_id: int) -> None:
    _sharepoint_rest_request(
        site_base_url,
        f"/_api/web/roleassignments/getbyprincipalid({principal_id})",
        method="POST",
        x_http_method="DELETE",
    )


def _remove_list_role_assignment(site_base_url: str, list_title: str, principal_id: int) -> None:
    _sharepoint_rest_request(
        site_base_url,
        f"/_api/web/lists/getbytitle('{_escape_odata_string(list_title)}')/roleassignments/getbyprincipalid({principal_id})",
        method="POST",
        x_http_method="DELETE",
    )


def _remove_list_item_role_assignment(
    site_base_url: str,
    list_title: str,
    item_id: int,
    principal_id: int,
) -> None:
    _sharepoint_rest_request(
        site_base_url,
        f"/_api/web/lists/getbytitle('{_escape_odata_string(list_title)}')/items({item_id})/roleassignments/getbyprincipalid({principal_id})",
        method="POST",
        x_http_method="DELETE",
    )


def _get_list_item_state(site_base_url: str, list_title: str, item_id: int) -> dict:
    payload = _sharepoint_rest_request(
        site_base_url,
        f"/_api/web/lists/getbytitle('{_escape_odata_string(list_title)}')/items({item_id})"
        "?$select=Id,HasUniqueRoleAssignments,FileLeafRef,Title",
        method="GET",
    )
    return _sp_d(payload)


def _format_role_assignments(payload: dict) -> List[dict]:
    results = []
    for entry in _sp_d(payload).get("results", []):
        member = entry.get("Member") or {}
        bindings = [
            {
                "id": binding.get("Id"),
                "name": binding.get("Name"),
            }
            for binding in (entry.get("RoleDefinitionBindings", {}) or {}).get("results", [])
        ]
        results.append(
            {
                "principal_id": member.get("Id"),
                "principal_title": member.get("Title"),
                "login_name": member.get("LoginName"),
                "principal_type": member.get("PrincipalType"),
                "roles": bindings,
            }
        )
    return results


def _get_site_role_assignments(site_base_url: str) -> List[dict]:
    payload = _sharepoint_rest_request(
        site_base_url,
        "/_api/web/roleassignments"
        "?$select=Member/Id,Member/Title,Member/LoginName,Member/PrincipalType,RoleDefinitionBindings/Id,RoleDefinitionBindings/Name"
        "&$expand=Member,RoleDefinitionBindings",
        method="GET",
    )
    return _format_role_assignments(payload)


def _get_list_role_assignments(site_base_url: str, list_title: str) -> List[dict]:
    payload = _sharepoint_rest_request(
        site_base_url,
        f"/_api/web/lists/getbytitle('{_escape_odata_string(list_title)}')/roleassignments"
        "?$select=Member/Id,Member/Title,Member/LoginName,Member/PrincipalType,RoleDefinitionBindings/Id,RoleDefinitionBindings/Name"
        "&$expand=Member,RoleDefinitionBindings",
        method="GET",
    )
    return _format_role_assignments(payload)


def _get_list_item_role_assignments(site_base_url: str, list_title: str, item_id: int) -> List[dict]:
    payload = _sharepoint_rest_request(
        site_base_url,
        f"/_api/web/lists/getbytitle('{_escape_odata_string(list_title)}')/items({item_id})/roleassignments"
        "?$select=Member/Id,Member/Title,Member/LoginName,Member/PrincipalType,RoleDefinitionBindings/Id,RoleDefinitionBindings/Name"
        "&$expand=Member,RoleDefinitionBindings",
        method="GET",
    )
    return _format_role_assignments(payload)


def _normalize_manage_clients_role(target: dict) -> str:
    role = str(target.get("role") or "").strip()
    if role == "custom":
        custom_role_name = str(target.get("custom_role_name") or "").strip()
        if not custom_role_name:
            raise ValueError("'custom_role_name' is required when role='custom'.")
        return custom_role_name
    mapping = {
        "read": "Read",
        "edit": "Edit",
        "contribute": "Contribute",
        "full_control": "Full Control",
    }
    if role not in mapping:
        raise ValueError(
            "'role' must be one of 'read', 'edit', 'contribute', 'full_control', or 'custom'."
        )
    return mapping[role]


def _resolve_manage_clients_principal(site_base_url: str, principal: dict) -> dict:
    if not isinstance(principal, dict):
        raise ValueError("'principal' must be an object.")
    principal_id = principal.get("id")
    display_name = str(principal.get("display_name", "")).strip()
    email = str(principal.get("email", "")).strip()

    translated: dict = {}
    if isinstance(principal_id, str) and principal_id.strip().isdigit():
        translated["principal_id"] = int(principal_id.strip())
    elif isinstance(principal_id, int):
        translated["principal_id"] = principal_id
    elif isinstance(principal_id, str) and principal_id.strip():
        translated["principal_name"] = principal_id.strip()

    if "principal_id" not in translated and "principal_name" not in translated:
        translated["principal_name"] = display_name or email

    return _resolve_sharepoint_principal(site_base_url, translated)


def _resolve_clients_permission_scope(resource_scope: dict) -> dict:
    if not isinstance(resource_scope, dict):
        raise ValueError("'resource_scope' must be an object.")
    kind = str(resource_scope.get("kind") or "").strip()
    if kind not in {"site", "page", "library", "folder", "file", "list_item"}:
        raise ValueError(
            "'resource_scope.kind' must be one of 'site', 'page', 'library', 'folder', 'file', or 'list_item'."
        )
    site_base_url = _clients_site_base_url()

    if kind == "site":
        return {
            "resource_type": "web",
            "kind": "site",
            "target_ref": _target_ref(site_path=_CLIENTS_SITE_PATH),
        }

    if kind == "page":
        page_id = str(resource_scope.get("id") or "").strip()
        page_path = str(resource_scope.get("path") or "").strip()
        resolved = (
            _resolve_clients_site_page_by_id(page_id)
            if page_id
            else _resolve_clients_site_page(page_path)
        )
        page_name = resolved["page_path"].rsplit("/", 1)[-1]
        page_item = _get_clients_page_list_item(page_name)
        return {
            "resource_type": "list_item",
            "kind": "page",
            "list_title": _clients_site_page_list_title(),
            "item_id": int(page_item.get("Id")),
            "page_path": resolved["page_path"],
            "page_id": resolved["page_id"],
            "has_unique_role_assignments": bool(page_item.get("HasUniqueRoleAssignments")),
            "target_ref": _target_ref(
                site_path=_CLIENTS_SITE_PATH,
                page_path=resolved["page_path"],
                page_id=resolved["page_id"],
                page_item_id=page_item.get("Id"),
            ),
        }

    if kind == "library":
        list_id = str(resource_scope.get("id") or "").strip()
        path = str(resource_scope.get("path") or "").strip()
        library_name = path.split("/", 1)[0].strip() if path else ""
        resolved = _resolve_clients_library(
            library_name=library_name or None,
            list_id=list_id or None,
        )
        rest_state = resolved.get("rest") or {}
        return {
            "resource_type": "list",
            "kind": "library",
            "list_title": resolved["library_name"],
            "list_id": resolved["list_id"],
            "has_unique_role_assignments": bool(rest_state.get("HasUniqueRoleAssignments")),
            "target_ref": _target_ref(
                site_path=_CLIENTS_SITE_PATH,
                library_name=resolved["library_name"],
                list_id=resolved["list_id"],
            ),
        }

    path = str(resource_scope.get("path") or "").strip()
    if not path:
        raise ValueError(f"'resource_scope.path' is required for kind='{kind}'.")
    resolved_item = _resolve_clients_drive_item_by_path(path)
    item = resolved_item["item"]
    if kind == "folder" and "folder" not in item:
        raise ValueError(f"Path '{path}' is not a folder.")
    if kind == "file" and "file" not in item:
        raise ValueError(f"Path '{path}' is not a file.")
    list_item_id = resolved_item.get("list_item_id")
    if not list_item_id:
        raise RuntimeError(f"Path '{path}' did not resolve to a SharePoint list item id.")
    item_state = _get_list_item_state(
        site_base_url,
        resolved_item["library_name"],
        int(list_item_id),
    )
    return {
        "resource_type": "list_item",
        "kind": kind,
        "list_title": resolved_item["library_name"],
        "item_id": int(list_item_id),
        "item_path": _normalize_clients_site_relative_path(path),
        "item_name": item.get("name"),
        "has_unique_role_assignments": bool(item_state.get("HasUniqueRoleAssignments")),
        "target_ref": _target_ref(
            site_path=_CLIENTS_SITE_PATH,
            library_name=resolved_item["library_name"],
            item_path=_normalize_clients_site_relative_path(path),
            item_id=resolved_item["item_id"],
            list_item_id=list_item_id,
        ),
    }


def _manage_clients_site_response(
    *,
    status: str,
    operation_id: str,
    site_path: str,
    operation: str,
    target_ref: Optional[dict] = None,
    changes_applied: Optional[List[dict]] = None,
    warnings: Optional[List[str]] = None,
    errors: Optional[List[str]] = None,
    approval_used: bool = False,
) -> str:
    return json.dumps(
        {
            "status": status,
            "operation_id": operation_id,
            "site_path": site_path,
            "operation": operation,
            "target_ref": target_ref or {},
            "changes_applied": changes_applied or [],
            "warnings": warnings or [],
            "errors": errors or [],
            "approval_used": approval_used,
            "executed_at": _utc_now_iso(),
        },
        indent=2,
    )


def _manage_clients_site_error_status(exc: Exception) -> str:
    message = str(exc).lower()
    if isinstance(exc, ApprovalRequiredError):
        return "approval_required"
    if isinstance(exc, FileNotFoundError):
        return "not_found"
    if isinstance(exc, PermissionError):
        return "scope_denied"
    if isinstance(exc, ValueError):
        return "validation_failed"
    if isinstance(exc, EscalationRequiredError):
        return "approval_required"
    if "version conflict" in message:
        return "version_conflict"
    if " 401" in message or " 403" in message or "access denied" in message:
        return "permission_denied"
    return "connector_error"


def _require_manage_clients_operation_approval(operation: str, options: dict) -> bool:
    if operation not in _MANAGE_CLIENTS_ALL_OPERATIONS:
        raise PermissionError(
            f"Operation '{operation}' is outside the approved manage_clients_site surface."
        )
    approval_token = str(options.get("approval_token", "")).strip()
    if operation in _MANAGE_CLIENTS_REQUIRES_TOKEN and not approval_token:
        raise ApprovalRequiredError(
            f"Operation '{operation}' requires 'options.approval_token'."
        )
    return bool(approval_token)


def _validate_clients_navigation_url(url: str, is_external: bool) -> str:
    value = str(url or "").strip()
    if not value:
        raise ValueError("'nav_node.url' must not be empty.")
    if is_external:
        return value

    parsed = urlparse(value)
    if parsed.scheme or parsed.netloc:
        if parsed.netloc.lower() != "levinellp.sharepoint.com":
            raise PermissionError("Navigation targets must remain inside levinellp.sharepoint.com.")
        if not parsed.path.startswith(_CLIENTS_SITE_PATH):
            raise PermissionError("Navigation targets must remain within /sites/Clients.")
        return parsed.path

    if value.startswith("/"):
        if not value.startswith(_CLIENTS_SITE_PATH):
            raise PermissionError("Navigation targets must remain within /sites/Clients.")
        return value

    return _clients_server_relative_path(value)


def _resolve_template_item(source_doc_id: str, template_library_id: Optional[str] = None) -> tuple[dict, dict]:
    zones = _template_read_zones()
    if template_library_id:
        zones = [z for z in zones if z.get("library_id") == template_library_id]
        if not zones:
            raise PermissionError(
                f"Library '{template_library_id}' is not an allowlisted template zone."
            )

    for zone in zones:
        library_id = zone.get("library_id")
        if not library_id:
            continue
        item = _get_drive_item_by_id(library_id, source_doc_id)
        if item and _item_matches_prefixes(item, zone.get("folder_prefixes", [])):
            return zone, item

    raise PermissionError(
        f"Template document '{source_doc_id}' was not found in an allowlisted template zone."
    )


def _resolve_diffable_item(item_id: str) -> tuple[dict, dict]:
    zones: List[dict] = []
    for zone in _template_read_zones():
        zones.append({**zone, "zone_type": "template"})
    for zone in _wip_write_zones():
        zones.append({**zone, "zone_type": "wip"})

    for zone in zones:
        library_id = zone.get("library_id")
        if not library_id:
            continue
        item = _get_drive_item_by_id(library_id, item_id)
        if item and _item_matches_prefixes(item, zone.get("folder_prefixes", [])):
            return zone, item

    raise PermissionError(
        f"Document '{item_id}' was not found in an allowlisted template or WIP zone."
    )


def _resolve_wip_zone(site_id: str, library_id: str, folder_path: str) -> dict:
    norm_path = _canonical_zone_path(folder_path)
    for zone in _wip_write_zones():
        if zone.get("site_id") != site_id or zone.get("library_id") != library_id:
            continue
        prefixes = [_canonical_zone_path(p) for p in zone.get("folder_prefixes", [])]
        if any(_matches_allowed_prefix(norm_path, prefix) for prefix in prefixes):
            return zone
    raise PermissionError(
        "Destination does not match an allowlisted SharePoint WIP write zone."
    )


def _parse_docx_text(content: bytes) -> str:
    try:
        with zipfile.ZipFile(BytesIO(content)) as zf:
            xml = zf.read("word/document.xml")
    except KeyError as exc:
        raise ValueError("DOCX is missing word/document.xml") from exc
    except zipfile.BadZipFile as exc:
        raise ValueError("DOCX file is invalid or corrupted") from exc

    root = ET.fromstring(xml)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs: List[str] = []
    for para in root.findall(".//w:p", ns):
        runs = [node.text or "" for node in para.findall(".//w:t", ns)]
        text = "".join(runs).strip()
        if text:
            paragraphs.append(text)
    return "\n".join(paragraphs).strip()


def _strip_markup(text: str) -> str:
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html_unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _extract_item_text(item: dict, content: bytes) -> str:
    mime = str(item.get("file", {}).get("mimeType") or "").lower()
    name = str(item.get("name") or "").lower()

    if name.endswith(".docx") or mime == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return _parse_docx_text(content)
    if name.endswith((".txt", ".md", ".csv", ".json", ".xml")) or mime.startswith("text/") or mime in {
        "application/json",
        "application/xml",
    }:
        return content.decode("utf-8", errors="replace")
    if name.endswith((".html", ".htm", ".aspx")) or mime in {"text/html", "application/xhtml+xml"}:
        return _strip_markup(content.decode("utf-8", errors="replace"))
    raise ValueError(
        f"Unsupported file type for text diff: {item.get('name')} ({mime or 'unknown mime'})"
    )


def _build_diff_summary(text_a: str, text_b: str, label_a: str, label_b: str) -> tuple[str, dict]:
    lines_a = text_a.splitlines()
    lines_b = text_b.splitlines()
    matcher = difflib.SequenceMatcher(a=lines_a, b=lines_b)
    counts = {"additions": 0, "deletions": 0, "edits": 0}
    hunks: List[str] = []

    for idx, (tag, i1, i2, j1, j2) in enumerate(matcher.get_opcodes(), start=1):
        if tag == "equal":
            continue
        if tag == "insert":
            counts["additions"] += j2 - j1
        elif tag == "delete":
            counts["deletions"] += i2 - i1
        elif tag == "replace":
            counts["edits"] += max(i2 - i1, j2 - j1)

        old_chunk = "\n".join(lines_a[i1:i2]) or "(none)"
        new_chunk = "\n".join(lines_b[j1:j2]) or "(none)"
        hunks.append(
            "\n".join(
                [
                    f"### Change {idx}",
                    f"- {label_a} lines: {i1 + 1}-{max(i1 + 1, i2)}",
                    f"- {label_b} lines: {j1 + 1}-{max(j1 + 1, j2)}",
                    "",
                    f"```text\n{old_chunk[:1200]}\n```",
                    "",
                    f"```text\n{new_chunk[:1200]}\n```",
                ]
            )
        )
        if len(hunks) >= 8:
            break

    summary_lines = [
        f"# Diff Summary: {label_a} vs {label_b}",
        "",
        f"- additions: {counts['additions']}",
        f"- deletions: {counts['deletions']}",
        f"- edits: {counts['edits']}",
    ]
    if hunks:
        summary_lines.append("")
        summary_lines.extend(hunks)
    else:
        summary_lines.extend(["", "No textual differences detected."])

    return "\n".join(summary_lines), counts


def _slim_site_page(page: dict, page_path: str) -> dict:
    return {
        "id": page.get("id"),
        "name": page.get("name"),
        "path": page_path,
        "title": page.get("title"),
        "description": page.get("description"),
        "pageLayout": page.get("pageLayout"),
        "promotionKind": page.get("promotionKind"),
        "publishingState": page.get("publishingState"),
        "eTag": page.get("eTag"),
        "createdDateTime": page.get("createdDateTime"),
        "lastModifiedDateTime": page.get("lastModifiedDateTime"),
        "webUrl": page.get("webUrl"),
        "showComments": page.get("showComments"),
        "showRecommendedPages": page.get("showRecommendedPages"),
    }


def _extract_html_links(html: str) -> List[str]:
    seen = set()
    links: List[str] = []
    for match in re.finditer(r"""href\s*=\s*["']([^"']+)["']""", html, flags=re.IGNORECASE):
        href = html_unescape(match.group(1).strip())
        if href and href not in seen:
            seen.add(href)
            links.append(href)
    return links


def _summarize_site_page_webparts(webparts: List[dict]) -> dict:
    text_webparts: List[dict] = []
    standard_webparts: List[dict] = []
    page_text_blocks: List[str] = []

    for position, webpart in enumerate(webparts, start=1):
        odata_type = str(webpart.get("@odata.type") or "").strip()
        webpart_id = str(webpart.get("id") or "").strip()
        if odata_type.lower().endswith("textwebpart"):
            inner_html = str(webpart.get("innerHtml") or "")
            plain_text = _strip_markup(inner_html)
            text_webparts.append(
                {
                    "id": webpart_id,
                    "position": position,
                    "innerHtml": inner_html,
                    "plainText": plain_text,
                    "links": _extract_html_links(inner_html),
                }
            )
            if plain_text:
                page_text_blocks.append(plain_text)
            continue

        standard_webparts.append(
            {
                "id": webpart_id,
                "position": position,
                "type": odata_type or "#microsoft.graph.standardWebPart",
                "webPartType": webpart.get("webPartType"),
            }
        )

    return {
        "text_webparts": text_webparts,
        "standard_webparts": standard_webparts,
        "page_text": "\n\n".join(page_text_blocks).strip(),
    }


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


def tool_refresh_drive_ids(args: dict) -> str:
    """
    Validate that each hardcoded drive ID in _DRIVES is accessible via Graph API.
    For each drive, calls GET /drives/{drive_id} and reports whether the drive is
    reachable. Mismatches (404, permission error, etc.) are surfaced as warnings.
    No writes are performed. Safe to call at any time.
    """
    import time as _time_module
    results = []
    warnings = []
    for alias, cfg in _DRIVES.items():
        drive_id = cfg["drive_id"]
        url = f"{GRAPH_BASE}/drives/{drive_id}"
        try:
            data = _graph_get_optional(url)
            if data is None:
                warnings.append(f"{alias}: drive_id NOT FOUND (404) — may need updating")
                results.append({"alias": alias, "drive_id": drive_id, "status": "not_found"})
            else:
                results.append({
                    "alias": alias,
                    "drive_id": drive_id,
                    "status": "ok",
                    "drive_name": data.get("name"),
                    "drive_type": data.get("driveType"),
                    "web_url": data.get("webUrl"),
                })
        except Exception as exc:
            warnings.append(f"{alias}: error — {exc}")
            results.append({"alias": alias, "drive_id": drive_id, "status": "error", "detail": str(exc)})

    return json.dumps({
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "total": len(results),
        "ok": sum(1 for r in results if r["status"] == "ok"),
        "not_found": sum(1 for r in results if r["status"] == "not_found"),
        "errors": sum(1 for r in results if r["status"] == "error"),
        "warnings": warnings,
        "drives": results,
    }, indent=2)


def tool_list_folder(args: dict) -> str:
    """
    List the children of a folder path within an approved drive.
    Returns item metadata only — no file content is read.
    """
    drive_alias = args.get("drive", "").lower()
    path        = args.get("path", "").strip()
    operation_id = _new_operation_id("list_folder")

    _require_valid_drive(drive_alias)

    if not path and not _is_full_library_read(drive_alias):
        raise ValueError("'path' is required and must not be empty.")

    if path and not _is_allowed_read(drive_alias, path):
        allowed = _DRIVES[drive_alias]["allowed_read_prefixes"]
        raise PermissionError(
            f"Path '{path}' is outside the approved read boundary for drive "
            f"'{drive_alias}'. Allowed prefixes: {allowed}"
        )

    drive_id = _DRIVES[drive_alias]["drive_id"]
    norm_path = _normalize_drive_path(drive_alias, path)

    log.info("list_folder drive=%s path=%s", drive_alias, norm_path)

    if norm_path:
        url = _drive_root_url(drive_id, norm_path, ":/children")
    else:
        url = _drive_root_url(drive_id, "", "/children")
    items = _graph_paged_get(url)
    result = [_slim_item(i) for i in items]
    target_ref = _target_ref(drive=drive_alias, path=norm_path or "/")
    _audit_log(
        operation_id=operation_id,
        tool_name="list_folder",
        actor_type="agent",
        actor_id="sharepoint-mcp",
        authorized_scope=f"drive={drive_alias}",
        target_object=target_ref,
        action_type="list_folder",
        output_status="success",
        input_record={"drive": drive_alias, "path": norm_path or ""},
    )
    return _response_payload(
        status="success",
        operation_id=operation_id,
        target_ref=target_ref,
        result_payload={"entries": result},
    )


def tool_get_item(args: dict) -> str:
    """
    Get metadata for a single item (file or folder) by path.
    No file content is returned.
    """
    drive_alias = args.get("drive", "").lower()
    path        = args.get("path", "").strip()
    operation_id = _new_operation_id("get_item")

    _require_valid_drive(drive_alias)

    if not path and not _is_full_library_read(drive_alias):
        raise ValueError("'path' is required and must not be empty.")

    if path and not _is_allowed_read(drive_alias, path):
        allowed = _DRIVES[drive_alias]["allowed_read_prefixes"]
        raise PermissionError(
            f"Path '{path}' is outside the approved read boundary for drive "
            f"'{drive_alias}'. Allowed prefixes: {allowed}"
        )

    drive_id = _DRIVES[drive_alias]["drive_id"]
    norm_path = _normalize_drive_path(drive_alias, path)

    log.info("get_item drive=%s path=%s", drive_alias, norm_path)

    if norm_path:
        url = _drive_root_url(drive_id, norm_path)
    else:
        url = _drive_root_url(drive_id)
    item = _graph_get(url)
    result = _slim_item(item)
    target_ref = _target_ref(drive=drive_alias, path=norm_path or "/")
    _audit_log(
        operation_id=operation_id,
        tool_name="get_item",
        actor_type="agent",
        actor_id="sharepoint-mcp",
        authorized_scope=f"drive={drive_alias}",
        target_object=target_ref,
        action_type="get_item",
        output_status="success",
        input_record={"drive": drive_alias, "path": norm_path or ""},
    )
    return _response_payload(
        status="success",
        operation_id=operation_id,
        target_ref=target_ref,
        result_payload={"item": result},
    )


def tool_review_site_page(args: dict) -> str:
    """
    Review an approved Clients SitePages page, including text web parts.
    """
    page_path = str(args.get("page_path", "")).strip()
    operation_id = _new_operation_id("review_site_page")

    resolved = _resolve_clients_site_page(page_path)
    site_id = resolved["site_id"]
    page_id = resolved["page_id"]
    norm_path = resolved["page_path"]
    page = resolved["page"]
    webparts = _list_site_page_webparts(site_id, page_id)
    webpart_summary = _summarize_site_page_webparts(webparts)
    warnings: List[str] = []
    if not webpart_summary["text_webparts"]:
        warnings.append("No text web parts were found on this page.")
    if webpart_summary["standard_webparts"]:
        warnings.append(
            "Standard web parts are reported as inventory only; this tool flattens text web parts, not standard web part internals."
        )

    target_ref = _target_ref(site_id=site_id, page_id=page_id, page_path=norm_path)
    _audit_log(
        operation_id=operation_id,
        tool_name="review_site_page",
        actor_type="agent",
        actor_id="sharepoint-mcp",
        authorized_scope=f"site_id={site_id} page_scope=SitePages/*.aspx",
        target_object=target_ref,
        action_type="review_site_page",
        output_status="success",
        input_record={"page_path": norm_path},
    )
    return _response_payload(
        status="success",
        operation_id=operation_id,
        target_ref=target_ref,
        result_payload={
            "page": _slim_site_page(page, norm_path),
            "page_text": webpart_summary["page_text"],
            "text_webparts": webpart_summary["text_webparts"],
            "standard_webparts": webpart_summary["standard_webparts"],
        },
        warnings=warnings,
    )


def tool_update_site_page_content(args: dict) -> str:
    """
    Apply the current runtime's bounded content-update helper to one Clients SitePages page.
    """
    page_path = str(args.get("page_path", "")).strip()
    expected_e_tag = str(args.get("expected_e_tag", "")).strip()
    title = args["title"] if "title" in args else None
    description = args["description"] if "description" in args else None
    text_webparts = args.get("text_webparts", [])
    operation_id = _new_operation_id("update_site_page_content")

    if not expected_e_tag:
        raise ValueError("'expected_e_tag' is required.")
    if title is not None and not isinstance(title, str):
        raise ValueError("'title' must be a string when provided.")
    if description is not None and not isinstance(description, str):
        raise ValueError("'description' must be a string when provided.")
    if text_webparts is None:
        text_webparts = []
    if not isinstance(text_webparts, list):
        raise ValueError("'text_webparts' must be an array when provided.")
    if title is None and description is None and not text_webparts:
        raise ValueError(
            "At least one of 'title', 'description', or 'text_webparts' must be provided."
        )

    write_context = _require_write_context(args)
    resolved = _resolve_clients_site_page(page_path)
    site_id = resolved["site_id"]
    page_id = resolved["page_id"]
    norm_path = resolved["page_path"]
    current_page = resolved["page"]
    current_e_tag = _normalize_etag(current_page.get("eTag"))
    if current_e_tag and current_e_tag != _normalize_etag(expected_e_tag):
        raise RuntimeError(
            f"Version conflict: expected eTag '{expected_e_tag}' but found '{current_page.get('eTag')}'."
        )

    updated_fields: List[str] = []
    updated_webparts: List[dict] = []
    seen_webpart_ids = set()

    if title is not None or description is not None:
        payload = {"@odata.type": "#microsoft.graph.sitePage"}
        if title is not None:
            payload["title"] = title
            updated_fields.append("title")
        if description is not None:
            payload["description"] = description
            updated_fields.append("description")
        _graph_patch(
            f"{GRAPH_BASE}/sites/{site_id}/pages/{page_id}/microsoft.graph.sitePage",
            payload,
        )

    for entry in text_webparts:
        if not isinstance(entry, dict):
            raise ValueError("Each 'text_webparts' entry must be an object.")
        webpart_id = str(entry.get("webpart_id", "")).strip()
        inner_html = entry.get("inner_html")
        if not webpart_id:
            raise ValueError("Each 'text_webparts' entry requires 'webpart_id'.")
        if webpart_id in seen_webpart_ids:
            raise ValueError(f"Duplicate webpart_id '{webpart_id}' in 'text_webparts'.")
        if not isinstance(inner_html, str):
            raise ValueError(
                f"'inner_html' is required and must be a string for webpart '{webpart_id}'."
            )
        seen_webpart_ids.add(webpart_id)

        current_webpart = _get_site_page_webpart(site_id, page_id, webpart_id)
        odata_type = str(current_webpart.get("@odata.type") or "").strip().lower()
        if not odata_type.endswith("textwebpart"):
            raise PermissionError(
                f"Web part '{webpart_id}' is not a text web part. Only existing text web parts may be updated by this tool."
            )

        _graph_patch(
            f"{GRAPH_BASE}/sites/{site_id}/pages/{page_id}/microsoft.graph.sitePage/webParts/{webpart_id}",
            {
                "@odata.type": "#microsoft.graph.textWebPart",
                "innerHtml": inner_html,
            },
        )
        updated_webparts.append(
            {
                "webpart_id": webpart_id,
                "content_length": len(inner_html),
            }
        )

    final_page = _graph_get(
        f"{GRAPH_BASE}/sites/{site_id}/pages/{page_id}/microsoft.graph.sitePage"
    )
    final_e_tag = str(final_page.get("eTag") or "")
    target_ref = _target_ref(site_id=site_id, page_id=page_id, page_path=norm_path)
    warnings = [
        "This runtime validates artifact provenance inputs but does not persist them as SharePoint page metadata."
    ]
    _audit_log(
        operation_id=operation_id,
        tool_name="update_site_page_content",
        actor_type="agent",
        actor_id=write_context["actor_id"],
        authorized_scope=f"site_id={site_id} page_scope=SitePages/*.aspx page_path={norm_path}",
        target_object=target_ref,
        action_type="update_site_page_content",
        output_status="success",
        input_record={
            "page_path": norm_path,
            "page_id": page_id,
            "expected_e_tag": expected_e_tag,
            "updated_fields": updated_fields,
            "text_webparts": [
                {
                    "webpart_id": item["webpart_id"],
                    "content_length": item["content_length"],
                }
                for item in updated_webparts
            ],
            "run_id": write_context["run_id"],
            "workflow_ref": write_context["workflow_ref"],
            "runbook_ref": write_context["runbook_ref"],
            "capability_ref": write_context["capability_ref"],
            "artifact_version_ref": write_context["artifact_version_ref"],
            "provenance_label": write_context["provenance_label"],
            "reason_code": write_context["reason_code"],
            "upstream_artifact_ref": write_context["upstream_artifact_ref"],
            "human_operator_id": write_context["human_operator_id"],
            "approval_reference": write_context["approval_reference"],
        },
        version_before=str(current_page.get("eTag") or ""),
        version_after=final_e_tag or None,
        reason_code=write_context["reason_code"],
        upstream_artifact_ref=write_context["upstream_artifact_ref"],
        approval_reference=write_context["approval_reference"] or None,
    )
    return _response_payload(
        status="success",
        operation_id=operation_id,
        target_ref=target_ref,
        result_payload={
            "page": _slim_site_page(final_page, norm_path),
            "updated_fields": updated_fields,
            "updated_webparts": updated_webparts,
            "previous_e_tag": str(current_page.get("eTag") or ""),
            "new_e_tag": final_e_tag,
            "artifact_version_ref": write_context["artifact_version_ref"],
            "provenance_label": write_context["provenance_label"],
            "run_id": write_context["run_id"],
        },
        warnings=warnings,
    )


def tool_provision_client_workspace(args: dict) -> str:
    """
    Provision one client workspace in /sites/Clients using the current helper batch.
    Creates one client page, one client library, explicit permissions on the
    created resources, and one shared-home navigation link.
    """
    operation_id = _new_operation_id("provision_client_workspace")
    client_name = str(args.get("client_name", "")).strip()
    page_name = str(args.get("page_name", "")).strip()
    page_title = str(args.get("page_title", "")).strip()
    page_description = str(args.get("page_description", "")).strip()
    page_body_html = args.get("page_body_html")
    library_name = str(args.get("library_name", "")).strip()
    home_link_title = str(args.get("home_link_title", "")).strip()
    home_link_location = str(args.get("home_link_location", "TopNavigationBar")).strip() or "TopNavigationBar"
    home_link_audience_ids = args.get("home_link_audience_ids", [])
    page_role_assignments = args.get("page_role_assignments", [])
    library_role_assignments = args.get("library_role_assignments", [])

    if not client_name:
        raise ValueError("'client_name' is required.")
    if page_body_html is not None and not isinstance(page_body_html, str):
        raise ValueError("'page_body_html' must be a string when provided.")
    if not isinstance(home_link_audience_ids, list):
        raise ValueError("'home_link_audience_ids' must be an array when provided.")

    for audience_id in home_link_audience_ids:
        if not isinstance(audience_id, str) or not re.match(
            r"(?i)^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            audience_id.strip(),
        ):
            raise ValueError(
                "Each 'home_link_audience_ids' entry must be a GUID string."
            )

    write_context = _require_write_context(args, require_approval_reference=False)
    surface = _clients_workspace_provisioning_surface()
    site_id = str(surface.get("site_id") or "")
    if not site_id or site_id != _clients_site_id():
        raise RuntimeError("Clients provisioning surface site_id does not match Clients site configuration.")
    site_base_url = _clients_site_base_url()
    allowed_nav_locations = [
        str(value).strip()
        for value in surface.get("allowed_navigation_locations", [])
        if str(value).strip()
    ]
    if home_link_location not in allowed_nav_locations:
        raise PermissionError(
            f"Navigation location '{home_link_location}' is outside the approved Clients provisioning surface."
        )

    slug = _slugify_client_name(client_name)
    page_name = _normalize_clients_page_name(page_name or f"{slug}.aspx")
    norm_page_path = _normalize_clients_provisioning_page_path(page_name)
    page_title = page_title or f"{client_name} Workspace"
    page_description = page_description or (
        f"Secure workspace for {client_name} documents, instructions, and contact with Levine Law."
    )
    library_name = _validate_clients_library_name(library_name or f"{slug}-Documents")
    home_link_title = home_link_title or page_title

    # Preflight on resource existence before any mutation.
    try:
        _resolve_clients_site_page(norm_page_path)
        raise ValueError(f"Site page '{norm_page_path}' already exists.")
    except FileNotFoundError:
        pass
    if _get_clients_list_by_title_optional(library_name):
        raise ValueError(f"Document library '{library_name}' already exists.")

    prepared_page_assignments = _prepare_role_assignments(
        site_base_url, page_role_assignments, "page_role_assignments"
    )
    prepared_library_assignments = _prepare_role_assignments(
        site_base_url, library_role_assignments, "library_role_assignments"
    )

    warnings: List[str] = []
    errors: List[dict] = []
    status = "success"
    library_result: dict = {}
    page_result: dict = {}
    nav_result: dict = {}
    permission_result = {"page": [], "library": []}

    try:
        created_library = _create_clients_document_library(
            library_name,
            f"Secure document library for {client_name}.",
        )
        library_state = _get_clients_list_by_title_optional(library_name)
        if not library_state:
            raise RuntimeError(
                f"Created document library '{library_name}' could not be reloaded."
            )
        library_data = _sp_d(library_state)
        server_relative_url = (
            library_data.get("RootFolder", {}) or {}
        ).get("ServerRelativeUrl") or ""
        library_web_url = (
            f"{site_base_url.rstrip('/')}{server_relative_url}"
            if server_relative_url.startswith("/")
            else str(created_library.get("webUrl") or "")
        )
        if not library_web_url:
            warnings.append(
                "Created library did not return a webUrl; page body link may be omitted."
            )
        library_result = {
            "id": created_library.get("id") or library_data.get("Id"),
            "displayName": created_library.get("displayName") or library_name,
            "webUrl": library_web_url,
            "serverRelativeUrl": server_relative_url,
        }

        page_body_html = (
            page_body_html
            if isinstance(page_body_html, str) and page_body_html.strip()
            else _build_default_client_workspace_html(client_name, library_web_url or "#")
        )
        created_page = _create_clients_site_page(
            page_name,
            page_title,
            page_description,
            page_body_html,
        )
        page_item = _get_clients_page_list_item(page_name)
        page_result = _slim_site_page(created_page, norm_page_path)
        page_result["listItemId"] = page_item.get("Id")

        _break_list_role_inheritance(site_base_url, library_name)
        for assignment in prepared_library_assignments:
            _add_list_role_assignment(
                site_base_url,
                library_name,
                assignment["principal"]["id"],
                assignment["roledefid"],
            )
            permission_result["library"].append(
                {
                    "principal_id": assignment["principal"]["id"],
                    "principal_title": assignment["principal"]["title"],
                    "role": assignment["role"],
                }
            )

        _break_list_item_role_inheritance(
            site_base_url,
            _clients_site_page_list_title(),
            int(page_item.get("Id")),
        )
        for assignment in prepared_page_assignments:
            _add_list_item_role_assignment(
                site_base_url,
                _clients_site_page_list_title(),
                int(page_item.get("Id")),
                assignment["principal"]["id"],
                assignment["roledefid"],
            )
            permission_result["page"].append(
                {
                    "principal_id": assignment["principal"]["id"],
                    "principal_title": assignment["principal"]["title"],
                    "role": assignment["role"],
                }
            )

        created_node = _create_top_navigation_node(
            site_base_url,
            home_link_title,
            str(created_page.get("webUrl") or ""),
        )
        nav_result = {
            "id": created_node.get("Id"),
            "title": created_node.get("Title") or home_link_title,
            "url": created_node.get("Url") or created_page.get("webUrl"),
            "location": home_link_location,
        }
        if home_link_audience_ids:
            try:
                _set_navigation_node_audiences(
                    site_base_url,
                    int(created_node.get("Id")),
                    [value.strip() for value in home_link_audience_ids],
                )
                nav_result["audience_ids"] = [value.strip() for value in home_link_audience_ids]
            except Exception as exc:
                status = "partial_success"
                warnings.append(
                    "Workspace page and library were created, but audience targeting could not be applied to the navigation link."
                )
                errors.append({"message": str(exc)})

    except Exception as exc:
        if library_result or page_result:
            status = "partial_success"
            warnings.append(
                "At least one Clients workspace resource was created before the batch stopped."
            )
            errors.append({"message": str(exc)})
        else:
            raise

    target_ref = _target_ref(
        site_id=site_id,
        client_name=client_name,
        page_path=norm_page_path,
        library_name=library_name,
    )
    input_record = {
        "client_name": client_name,
        "page_name": page_name,
        "page_title": page_title,
        "library_name": library_name,
        "page_role_assignments": [
            {
                "principal_id": item["principal"]["id"],
                "principal_title": item["principal"]["title"],
                "role": item["role"],
            }
            for item in prepared_page_assignments
        ],
        "library_role_assignments": [
            {
                "principal_id": item["principal"]["id"],
                "principal_title": item["principal"]["title"],
                "role": item["role"],
            }
            for item in prepared_library_assignments
        ],
        "home_link_title": home_link_title,
        "home_link_location": home_link_location,
        "home_link_audience_ids": [str(value).strip() for value in home_link_audience_ids],
        "run_id": write_context["run_id"],
        "workflow_ref": write_context["workflow_ref"],
        "runbook_ref": write_context["runbook_ref"],
        "capability_ref": write_context["capability_ref"],
        "artifact_version_ref": write_context["artifact_version_ref"],
        "provenance_label": write_context["provenance_label"],
        "reason_code": write_context["reason_code"],
        "upstream_artifact_ref": write_context["upstream_artifact_ref"],
        "human_operator_id": write_context["human_operator_id"],
        "approval_reference": write_context["approval_reference"],
    }
    _audit_log(
        operation_id=operation_id,
        tool_name="provision_client_workspace",
        actor_type="agent",
        actor_id=write_context["actor_id"],
        authorized_scope=(
            f"site_id={site_id} page_scope=SitePages/*.aspx "
            f"library_scope=*-Documents nav_scope={home_link_location}"
        ),
        target_object=target_ref,
        action_type="provision_client_workspace",
        output_status=status,
        input_record=input_record,
        reason_code=write_context["reason_code"],
        upstream_artifact_ref=write_context["upstream_artifact_ref"],
        approval_reference=write_context["approval_reference"] or None,
        escalation_flag=(status == "partial_success" and bool(errors)),
    )
    return _response_payload(
        status=status,
        operation_id=operation_id,
        target_ref=target_ref,
        result_payload={
            "client_name": client_name,
            "page": page_result,
            "library": library_result,
            "page_permissions": permission_result["page"],
            "library_permissions": permission_result["library"],
            "navigation_link": nav_result,
            "artifact_version_ref": write_context["artifact_version_ref"],
            "provenance_label": write_context["provenance_label"],
            "run_id": write_context["run_id"],
        },
        errors=errors,
        warnings=warnings,
    )


def tool_manage_clients_site(args: dict) -> str:
    """
    Execute governed site-management operations within /sites/Clients.
    """
    operation_id = _new_operation_id("manage_clients_site")
    operation = str(args.get("operation", "")).strip()
    site_path = str(args.get("site_path", "")).strip()
    raw_target = args.get("target", {})
    raw_options = args.get("options", {})
    approval_used = False
    warnings: List[str] = []
    changes_applied: List[dict] = []
    target_ref: dict = {}
    version_before: Optional[str] = None
    version_after: Optional[str] = None

    def _bool_option(options: dict, name: str, default: bool = False) -> bool:
        if name not in options:
            return default
        value = options.get(name)
        if not isinstance(value, bool):
            raise ValueError(f"'options.{name}' must be a boolean when provided.")
        return value

    try:
        normalized_site_path = _normalize_clients_site_path(site_path)
        if not operation:
            raise ValueError("'operation' is required.")
        if not isinstance(raw_target, dict):
            raise ValueError("'target' must be an object.")
        if raw_options is None:
            raw_options = {}
        if not isinstance(raw_options, dict):
            raise ValueError("'options' must be an object when provided.")

        target = dict(raw_target)
        options = dict(raw_options)
        dry_run = _bool_option(options, "dry_run", False)
        create_if_missing = _bool_option(options, "create_if_missing", False)
        overwrite = _bool_option(options, "overwrite", False)
        publish_after_update = _bool_option(options, "publish_after_update", False)
        expected_version = str(options.get("expected_version", "")).strip() or None
        reason = str(options.get("reason", "")).strip()
        approval_used = _require_manage_clients_operation_approval(operation, options)
        if options.get("require_approval_token") is True and not approval_used:
            raise ApprovalRequiredError(
                "'options.require_approval_token' was true but no 'options.approval_token' was supplied."
            )
        if publish_after_update and not approval_used:
            raise ApprovalRequiredError(
                "Publishing after page create/update requires 'options.approval_token'."
            )

        site_id = _clients_site_id()
        site_base_url = _clients_site_base_url()
        input_record = {
            "site_path": normalized_site_path,
            "operation": operation,
            "target": _summarize_arguments(target),
            "options": _summarize_arguments(options),
        }

        if operation == "page.list":
            pages = _graph_paged_get(
                f"{GRAPH_BASE}/sites/{site_id}/pages/microsoft.graph.sitePage"
            )
            page_layout = target.get("page_layout")
            if page_layout is not None:
                page_layout = _normalize_manage_clients_page_layout(page_layout)
            filtered_pages = []
            for page in pages:
                page_name = str(page.get("name") or "").strip()
                if not page_name:
                    continue
                page_path = _page_path_from_name(page_name)
                if page_layout and page.get("pageLayout") != page_layout:
                    continue
                filtered_pages.append(_slim_site_page(page, page_path))
            target_ref = _target_ref(site_path=normalized_site_path, page_layout=page_layout)
            changes_applied = filtered_pages

        elif operation == "page.get":
            page_name = str(target.get("page_name", "")).strip()
            if not page_name:
                raise ValueError("'target.page_name' is required for page.get.")
            resolved = _resolve_clients_site_page(_page_path_from_name(page_name))
            page = resolved["page"]
            webparts = _list_site_page_webparts(site_id, resolved["page_id"])
            webpart_summary = _summarize_site_page_webparts(webparts)
            target_ref = _target_ref(
                site_path=normalized_site_path,
                page_path=resolved["page_path"],
                page_id=resolved["page_id"],
            )
            if webpart_summary["standard_webparts"]:
                warnings.append(
                    "Standard web parts are returned as inventory only; their inner configuration remains connector-defined."
                )
            changes_applied = [
                {
                    "page": _slim_site_page(page, resolved["page_path"]),
                    "canvasLayout": page.get("canvasLayout"),
                    "titleArea": page.get("titleArea"),
                    "page_text": webpart_summary["page_text"],
                    "text_webparts": webpart_summary["text_webparts"],
                    "standard_webparts": webpart_summary["standard_webparts"],
                }
            ]

        elif operation == "page.create":
            page_name = str(target.get("page_name", "")).strip()
            if not page_name:
                raise ValueError("'target.page_name' is required for page.create.")
            page_path = _page_path_from_name(page_name)
            page_title = str(target.get("page_title", "")).strip()
            if not page_title:
                page_title = (
                    _normalize_clients_page_name(page_name)
                    .rsplit(".", 1)[0]
                    .replace("-", " ")
                    .replace("_", " ")
                    .strip()
                )
            page_layout = _normalize_manage_clients_page_layout(
                str(target.get("page_layout", "article"))
            )
            canvas_layout = _site_page_payload_to_canvas_layout(
                target.get("page_canvas") if "page_canvas" in target else None
            )
            payload = {
                "@odata.type": "#microsoft.graph.sitePage",
                "name": _normalize_clients_page_name(page_name),
                "title": page_title,
                "pageLayout": page_layout,
                "showComments": False,
                "showRecommendedPages": False,
                "canvasLayout": canvas_layout,
            }
            existing = None
            try:
                existing = _resolve_clients_site_page(page_path)
            except FileNotFoundError:
                existing = None
            if existing and not overwrite:
                raise ValueError(f"Site page '{page_path}' already exists.")
            if existing:
                current_page = existing["page"]
                version_before = str(current_page.get("eTag") or "") or None
                if expected_version:
                    current_e_tag = _normalize_etag(current_page.get("eTag"))
                    if current_e_tag and current_e_tag != _normalize_etag(expected_version):
                        raise RuntimeError(
                            f"Version conflict: expected eTag '{expected_version}' but found '{current_page.get('eTag')}'."
                        )
                target_ref = _target_ref(
                    site_path=normalized_site_path,
                    page_path=page_path,
                    page_id=existing["page_id"],
                )
                changes_applied = [
                    {
                        "operation": "page.update",
                        "page_path": page_path,
                        "page_title": page_title,
                        "page_layout": page_layout,
                        "publish_after_update": publish_after_update,
                    }
                ]
                warnings.append(
                    "page.create encountered an existing page and will update it because options.overwrite=true."
                )
                if not dry_run:
                    update_payload = dict(payload)
                    update_payload.pop("name", None)
                    _graph_patch(
                        f"{GRAPH_BASE}/sites/{site_id}/pages/{existing['page_id']}/microsoft.graph.sitePage",
                        update_payload,
                    )
                    if publish_after_update:
                        _publish_clients_site_page(existing["page_id"])
                    final_page = _graph_get(
                        f"{GRAPH_BASE}/sites/{site_id}/pages/{existing['page_id']}/microsoft.graph.sitePage"
                    )
                    version_after = str(final_page.get("eTag") or "") or None
                    changes_applied = [
                        {
                            "operation": "page.update",
                            "page": _slim_site_page(final_page, page_path),
                            "published": publish_after_update,
                        }
                    ]
            else:
                target_ref = _target_ref(site_path=normalized_site_path, page_path=page_path)
                changes_applied = [
                    {
                        "operation": "page.create",
                        "page_path": page_path,
                        "page_title": page_title,
                        "page_layout": page_layout,
                        "publish_after_update": publish_after_update,
                    }
                ]
                if not dry_run:
                    created = _graph_post(
                        f"{GRAPH_BASE}/sites/{site_id}/pages",
                        payload,
                    )
                    page_id = str(created.get("id") or "")
                    if publish_after_update and page_id:
                        _publish_clients_site_page(page_id)
                    final_page = (
                        _graph_get(
                            f"{GRAPH_BASE}/sites/{site_id}/pages/{page_id}/microsoft.graph.sitePage"
                        )
                        if page_id
                        else created
                    )
                    version_after = str(final_page.get("eTag") or "") or None
                    target_ref = _target_ref(
                        site_path=normalized_site_path,
                        page_path=page_path,
                        page_id=final_page.get("id"),
                    )
                    changes_applied = [
                        {
                            "operation": "page.create",
                            "page": _slim_site_page(final_page, page_path),
                            "published": publish_after_update,
                        }
                    ]

        elif operation == "page.update":
            page_name = str(target.get("page_name", "")).strip()
            if not page_name:
                raise ValueError("'target.page_name' is required for page.update.")
            page_path = _page_path_from_name(page_name)
            try:
                resolved = _resolve_clients_site_page(page_path)
            except FileNotFoundError:
                if not create_if_missing:
                    raise
                resolved = None

            if resolved is None:
                synthetic_args = {
                    "site_path": normalized_site_path,
                    "operation": "page.create",
                    "target": {
                        "page_name": page_name,
                        "page_title": target.get("page_title"),
                        "page_layout": target.get("page_layout", "article"),
                        "page_canvas": target.get("page_canvas"),
                    },
                    "options": {
                        "dry_run": dry_run,
                        "publish_after_update": publish_after_update,
                        "approval_token": options.get("approval_token"),
                        "reason": reason,
                    },
                }
                return tool_manage_clients_site(synthetic_args)

            current_page = resolved["page"]
            version_before = str(current_page.get("eTag") or "") or None
            if expected_version:
                current_e_tag = _normalize_etag(current_page.get("eTag"))
                if current_e_tag and current_e_tag != _normalize_etag(expected_version):
                    raise RuntimeError(
                        f"Version conflict: expected eTag '{expected_version}' but found '{current_page.get('eTag')}'."
                    )

            payload = {"@odata.type": "#microsoft.graph.sitePage"}
            changed_fields: List[str] = []
            if "page_title" in target:
                page_title = target.get("page_title")
                if page_title is not None and not isinstance(page_title, str):
                    raise ValueError("'target.page_title' must be a string when provided.")
                payload["title"] = page_title
                changed_fields.append("title")
            if "page_layout" in target:
                payload["pageLayout"] = _normalize_manage_clients_page_layout(target.get("page_layout"))
                changed_fields.append("pageLayout")
            if "page_canvas" in target:
                payload["canvasLayout"] = _site_page_payload_to_canvas_layout(target.get("page_canvas"))
                changed_fields.append("canvasLayout")
            if set(payload.keys()) == {"@odata.type"} and not publish_after_update:
                raise ValueError("No page fields were supplied for page.update.")

            target_ref = _target_ref(
                site_path=normalized_site_path,
                page_path=page_path,
                page_id=resolved["page_id"],
            )
            changes_applied = [
                {
                    "operation": "page.update",
                    "page_path": page_path,
                    "changed_fields": changed_fields,
                    "publish_after_update": publish_after_update,
                }
            ]
            if not dry_run:
                if set(payload.keys()) != {"@odata.type"}:
                    _graph_patch(
                        f"{GRAPH_BASE}/sites/{site_id}/pages/{resolved['page_id']}/microsoft.graph.sitePage",
                        payload,
                    )
                if publish_after_update:
                    _publish_clients_site_page(resolved["page_id"])
                final_page = _graph_get(
                    f"{GRAPH_BASE}/sites/{site_id}/pages/{resolved['page_id']}/microsoft.graph.sitePage"
                )
                version_after = str(final_page.get("eTag") or "") or None
                changes_applied = [
                    {
                        "operation": "page.update",
                        "page": _slim_site_page(final_page, page_path),
                        "changed_fields": changed_fields,
                        "published": publish_after_update,
                    }
                ]

        elif operation == "page.publish":
            page_name = str(target.get("page_name", "")).strip()
            if not page_name:
                raise ValueError("'target.page_name' is required for page.publish.")
            resolved = _resolve_clients_site_page(_page_path_from_name(page_name))
            current_page = resolved["page"]
            version_before = str(current_page.get("eTag") or "") or None
            if expected_version:
                current_e_tag = _normalize_etag(current_page.get("eTag"))
                if current_e_tag and current_e_tag != _normalize_etag(expected_version):
                    raise RuntimeError(
                        f"Version conflict: expected eTag '{expected_version}' but found '{current_page.get('eTag')}'."
                    )
            target_ref = _target_ref(
                site_path=normalized_site_path,
                page_path=resolved["page_path"],
                page_id=resolved["page_id"],
            )
            changes_applied = [
                {"operation": "page.publish", "page_path": resolved["page_path"]}
            ]
            if not dry_run:
                _publish_clients_site_page(resolved["page_id"])
                final_page = _graph_get(
                    f"{GRAPH_BASE}/sites/{site_id}/pages/{resolved['page_id']}/microsoft.graph.sitePage"
                )
                version_after = str(final_page.get("eTag") or "") or None
                changes_applied = [
                    {
                        "operation": "page.publish",
                        "page": _slim_site_page(final_page, resolved["page_path"]),
                    }
                ]

        elif operation == "page.unpublish":
            page_name = str(target.get("page_name", "")).strip()
            if not page_name:
                raise ValueError("'target.page_name' is required for page.unpublish.")
            resolved = _resolve_clients_site_page(_page_path_from_name(page_name))
            current_page = resolved["page"]
            version_before = str(current_page.get("eTag") or "") or None
            if expected_version:
                current_e_tag = _normalize_etag(current_page.get("eTag"))
                if current_e_tag and current_e_tag != _normalize_etag(expected_version):
                    raise RuntimeError(
                        f"Version conflict: expected eTag '{expected_version}' but found '{current_page.get('eTag')}'."
                    )
            target_ref = _target_ref(
                site_path=normalized_site_path,
                page_path=resolved["page_path"],
                page_id=resolved["page_id"],
            )
            changes_applied = [
                {"operation": "page.unpublish", "page_path": resolved["page_path"]}
            ]
            if not dry_run:
                _unpublish_clients_site_page(
                    resolved["page_path"],
                    reason or "manage_clients_site unpublish",
                )
                final_page = _graph_get(
                    f"{GRAPH_BASE}/sites/{site_id}/pages/{resolved['page_id']}/microsoft.graph.sitePage"
                )
                version_after = str(final_page.get("eTag") or "") or None
                changes_applied = [
                    {
                        "operation": "page.unpublish",
                        "page": _slim_site_page(final_page, resolved["page_path"]),
                    }
                ]

        elif operation == "page.delete":
            page_name = str(target.get("page_name", "")).strip()
            if not page_name:
                raise ValueError("'target.page_name' is required for page.delete.")
            resolved = _resolve_clients_site_page(_page_path_from_name(page_name))
            current_page = resolved["page"]
            version_before = str(current_page.get("eTag") or "") or None
            if expected_version:
                current_e_tag = _normalize_etag(current_page.get("eTag"))
                if current_e_tag and current_e_tag != _normalize_etag(expected_version):
                    raise RuntimeError(
                        f"Version conflict: expected eTag '{expected_version}' but found '{current_page.get('eTag')}'."
                    )
            target_ref = _target_ref(
                site_path=normalized_site_path,
                page_path=resolved["page_path"],
                page_id=resolved["page_id"],
            )
            changes_applied = [
                {
                    "operation": "page.delete",
                    "page_path": resolved["page_path"],
                    "previous_title": current_page.get("title"),
                }
            ]
            if not dry_run:
                _graph_delete(
                    f"{GRAPH_BASE}/sites/{site_id}/pages/{resolved['page_id']}/microsoft.graph.sitePage",
                    if_match=current_page.get("eTag"),
                )

        elif operation == "page.set_home":
            page_name = str(target.get("page_name", "")).strip()
            if not page_name:
                raise ValueError("'target.page_name' is required for page.set_home.")
            resolved = _resolve_clients_site_page(_page_path_from_name(page_name))
            target_ref = _target_ref(
                site_path=normalized_site_path,
                page_path=resolved["page_path"],
                page_id=resolved["page_id"],
            )
            changes_applied = [
                {
                    "operation": "page.set_home",
                    "welcome_page": resolved["page_path"],
                }
            ]
            if not dry_run:
                _set_clients_home_page(resolved["page_path"])

        elif operation == "library.create":
            library_name = _validate_clients_managed_library_name(
                str(target.get("library_name", "")).strip()
            )
            library_description = str(target.get("library_description", "") or "")
            library_template = str(target.get("library_template", "documentLibrary")).strip() or "documentLibrary"
            if library_template not in {"documentLibrary", "genericList"}:
                raise ValueError(
                    "'target.library_template' must be either 'documentLibrary' or 'genericList'."
                )
            existing = _get_clients_list_by_title_optional(library_name)
            if existing and not overwrite and not create_if_missing:
                raise ValueError(f"List '{library_name}' already exists.")
            target_ref = _target_ref(site_path=normalized_site_path, library_name=library_name)
            if existing:
                warnings.append(
                    "library.create encountered an existing list and will treat the request as satisfied."
                )
                changes_applied = [
                    {
                        "operation": "library.create",
                        "library_name": library_name,
                        "status": "already_exists",
                    }
                ]
            else:
                changes_applied = [
                    {
                        "operation": "library.create",
                        "library_name": library_name,
                        "library_template": library_template,
                    }
                ]
                if not dry_run:
                    created = _create_clients_list(
                        library_name,
                        library_description,
                        list_template=library_template,
                    )
                    resolved_library = _resolve_clients_library(library_name=library_name)
                    changes_applied = [
                        {
                            "operation": "library.create",
                            "library": {
                                "id": created.get("id") or resolved_library.get("list_id"),
                                "displayName": created.get("displayName") or library_name,
                                "description": library_description,
                                "serverRelativeUrl": (
                                    ((resolved_library.get("rest", {}) or {}).get("RootFolder", {}) or {}).get("ServerRelativeUrl")
                                ),
                                "webUrl": created.get("webUrl"),
                                "template": library_template,
                            },
                        }
                    ]

        elif operation == "library.update":
            library_name = _validate_clients_managed_library_name(
                str(target.get("library_name", "")).strip()
            )
            new_name = target.get("new_name")
            if new_name is not None:
                new_name = _validate_clients_managed_library_name(str(new_name).strip())
            library_description = target.get("library_description")
            if library_description is not None and not isinstance(library_description, str):
                raise ValueError("'target.library_description' must be a string when provided.")
            try:
                resolved_library = _resolve_clients_library(library_name=library_name)
            except FileNotFoundError:
                if not create_if_missing:
                    raise
                create_target = {
                    "library_name": new_name or library_name,
                    "library_description": library_description or "",
                    "library_template": target.get("library_template", "documentLibrary"),
                }
                return tool_manage_clients_site(
                    {
                        "site_path": normalized_site_path,
                        "operation": "library.create",
                        "target": create_target,
                        "options": {
                            "dry_run": dry_run,
                            "overwrite": overwrite,
                            "approval_token": options.get("approval_token"),
                            "reason": reason,
                        },
                    }
                )
            if new_name is None and library_description is None:
                raise ValueError(
                    "Provide at least one of 'target.new_name' or 'target.library_description' for library.update."
                )
            if new_name and new_name != library_name and _get_clients_list_by_title_optional(new_name):
                raise ValueError(f"List '{new_name}' already exists.")
            target_ref = _target_ref(
                site_path=normalized_site_path,
                library_name=new_name or library_name,
                list_id=resolved_library.get("list_id"),
            )
            changes_applied = [
                {
                    "operation": "library.update",
                    "library_name": library_name,
                    "new_name": new_name,
                    "description_changed": library_description is not None,
                }
            ]
            if not dry_run:
                updated = _update_clients_document_library(
                    library_name,
                    new_library_name=new_name,
                    description=library_description,
                )
                data = _sp_d(updated)
                changes_applied = [
                    {
                        "operation": "library.update",
                        "library": {
                            "id": data.get("Id"),
                            "displayName": data.get("Title") or (new_name or library_name),
                            "description": data.get("Description"),
                            "serverRelativeUrl": (
                                ((data.get("RootFolder", {}) or {}).get("ServerRelativeUrl"))
                            ),
                        },
                        "previous_name": library_name,
                    }
                ]

        elif operation == "library.delete":
            library_name = _validate_clients_managed_library_name(
                str(target.get("library_name", "")).strip()
            )
            resolved_library = _resolve_clients_library(library_name=library_name)
            target_ref = _target_ref(
                site_path=normalized_site_path,
                library_name=resolved_library["library_name"],
                list_id=resolved_library["list_id"],
            )
            changes_applied = [
                {
                    "operation": "library.delete",
                    "library_name": resolved_library["library_name"],
                    "list_id": resolved_library["list_id"],
                }
            ]
            if not dry_run:
                _graph_delete(
                    f"{GRAPH_BASE}/sites/{site_id}/lists/{resolved_library['list_id']}"
                )

        elif operation == "folder.create":
            folder_path = _normalize_clients_site_relative_path(
                str(target.get("folder_path", "")).strip()
            )
            target_ref = _target_ref(
                site_path=normalized_site_path,
                folder_path=folder_path,
            )
            existing = None
            try:
                existing = _resolve_clients_drive_item_by_path(folder_path)
            except FileNotFoundError:
                existing = None
            if existing is not None:
                if create_if_missing:
                    warnings.append(
                        f"Folder '{folder_path}' already exists; returning the existing folder because options.create_if_missing=true."
                    )
                    changes_applied = [
                        {
                            "operation": "folder.create",
                            "folder_path": folder_path,
                            "status": "already_exists",
                        }
                    ]
                else:
                    raise ValueError(f"Folder '{folder_path}' already exists.")
            else:
                changes_applied = [
                    {"operation": "folder.create", "folder_path": folder_path}
                ]
                if not dry_run:
                    created = _create_clients_folder(folder_path)
                    changes_applied = [
                        {
                            "operation": "folder.create",
                            "folder": {
                                "id": created.get("id"),
                                "name": created.get("name"),
                                "path": folder_path,
                                "webUrl": created.get("webUrl"),
                            },
                        }
                    ]

        elif operation == "folder.rename":
            folder_path = _normalize_clients_site_relative_path(
                str(target.get("folder_path", "")).strip()
            )
            new_name = str(target.get("new_name", "")).strip()
            if not new_name:
                raise ValueError("'target.new_name' is required for folder.rename.")
            current = _resolve_clients_drive_item_by_path(folder_path)
            if "folder" not in current["item"]:
                raise ValueError(f"Path '{folder_path}' is not a folder.")
            parent_path = folder_path.rsplit("/", 1)[0]
            renamed_path = f"{parent_path}/{new_name}"
            target_ref = _target_ref(site_path=normalized_site_path, folder_path=folder_path)
            changes_applied = [
                {
                    "operation": "folder.rename",
                    "from": folder_path,
                    "to": renamed_path,
                }
            ]
            if not dry_run:
                updated = _move_or_rename_clients_folder(folder_path, new_name=new_name)
                changes_applied = [
                    {
                        "operation": "folder.rename",
                        "folder": {
                            "id": updated.get("id"),
                            "name": updated.get("name"),
                            "path": renamed_path,
                            "webUrl": updated.get("webUrl"),
                        },
                    }
                ]

        elif operation == "folder.move":
            folder_path = _normalize_clients_site_relative_path(
                str(target.get("folder_path", "")).strip()
            )
            destination_path = _normalize_clients_site_relative_path(
                str(target.get("destination_path", "")).strip()
            )
            moved = _resolve_clients_drive_item_by_path(folder_path)
            if "folder" not in moved["item"]:
                raise ValueError(f"Path '{folder_path}' is not a folder.")
            final_name = str(target.get("new_name", "")).strip() or str(moved["item"].get("name") or "")
            final_path = f"{destination_path}/{final_name}"
            target_ref = _target_ref(site_path=normalized_site_path, folder_path=folder_path)
            changes_applied = [
                {
                    "operation": "folder.move",
                    "from": folder_path,
                    "to": final_path,
                }
            ]
            if not dry_run:
                updated = _move_or_rename_clients_folder(
                    folder_path,
                    destination_path=destination_path,
                    new_name=(str(target.get("new_name", "")).strip() or None),
                )
                changes_applied = [
                    {
                        "operation": "folder.move",
                        "folder": {
                            "id": updated.get("id"),
                            "name": updated.get("name"),
                            "path": final_path,
                            "webUrl": updated.get("webUrl"),
                        },
                    }
                ]

        elif operation == "folder.delete":
            folder_path = _normalize_clients_site_relative_path(
                str(target.get("folder_path", "")).strip()
            )
            _resolve_clients_drive_item_by_path(folder_path)
            target_ref = _target_ref(site_path=normalized_site_path, folder_path=folder_path)
            changes_applied = [
                {"operation": "folder.delete", "folder_path": folder_path}
            ]
            if not dry_run:
                _delete_clients_folder(folder_path)

        elif operation == "navigation.get":
            location_value = target.get("nav_location")
            allowed_locations = [
                _normalize_clients_navigation_location(value)
                for value in _clients_site_management_surface().get("allowed_navigation_locations", [])
            ]
            locations = (
                [_normalize_clients_navigation_location(location_value)]
                if location_value is not None
                else allowed_locations
            )
            changes_applied = []
            for location in locations:
                _navigation_location_endpoint(location)
                changes_applied.append(
                    {
                        "location": location,
                        "nodes": _list_navigation_nodes(site_base_url, location),
                    }
                )
            target_ref = _target_ref(
                site_path=normalized_site_path,
                nav_location=(locations[0] if len(locations) == 1 else None),
            )

        elif operation == "navigation.upsert":
            location = _normalize_clients_navigation_location(
                str(target.get("nav_location", "")).strip()
            )
            if not location:
                raise ValueError("'target.nav_location' is required for navigation.upsert.")
            _navigation_location_endpoint(location)
            nav_node = target.get("nav_node")
            if not isinstance(nav_node, dict):
                raise ValueError("'target.nav_node' must be an object for navigation.upsert.")
            node_id = nav_node.get("id")
            parent_id = nav_node.get("parent_id")
            if node_id is not None and str(node_id).strip() and not str(node_id).strip().isdigit():
                raise ValueError("'target.nav_node.id' must be a stringified integer when provided.")
            if parent_id is not None and str(parent_id).strip() and not str(parent_id).strip().isdigit():
                raise ValueError("'target.nav_node.parent_id' must be a stringified integer when provided.")
            title = str(nav_node.get("title", "")).strip()
            url = str(nav_node.get("url", "")).strip()
            is_external = nav_node.get("is_external", False)
            if not isinstance(is_external, bool):
                raise ValueError("'target.nav_node.is_external' must be a boolean when provided.")
            audience_ids = nav_node.get("audience_ids")
            if audience_ids is not None and not isinstance(audience_ids, list):
                raise ValueError("'target.nav_node.audience_ids' must be an array when provided.")

            existing = None
            if node_id is not None and str(node_id).strip():
                existing = _get_navigation_node_by_id(site_base_url, int(str(node_id).strip()))
                if not title:
                    title = str(existing.get("Title") or "").strip()
                if not url:
                    url = str(existing.get("Url") or "").strip()
                if not nav_node.get("is_external"):
                    is_external = bool(existing.get("IsExternal"))
            elif parent_id is not None and title:
                existing = _find_navigation_child_by_title(
                    site_base_url,
                    int(str(parent_id).strip()),
                    title,
                )
            elif title:
                existing = _find_navigation_node_by_title_and_location(
                    site_base_url,
                    title,
                    location,
                )

            if not title:
                raise ValueError("'target.nav_node.title' is required when the node is not already resolvable.")
            if not url:
                raise ValueError("'target.nav_node.url' is required when the node is not already resolvable.")
            normalized_url = _validate_clients_navigation_url(url, is_external)
            target_ref = _target_ref(
                site_path=normalized_site_path,
                nav_location=location,
                navigation_node_id=(existing.get("Id") if existing else None),
            )
            changes_applied = [
                {
                    "operation": "navigation.upsert",
                    "location": location,
                    "title": title,
                    "url": normalized_url,
                    "parent_id": (str(parent_id).strip() if parent_id is not None else None),
                }
            ]
            if not dry_run:
                if existing:
                    node = _update_navigation_node(
                        site_base_url,
                        int(existing.get("Id")),
                        title=title,
                        url=normalized_url,
                        is_external=is_external,
                    )
                elif parent_id is not None and str(parent_id).strip():
                    node = _create_navigation_child_node(
                        site_base_url,
                        int(str(parent_id).strip()),
                        title,
                        normalized_url,
                        is_external=is_external,
                    )
                else:
                    node = _create_navigation_node(
                        site_base_url,
                        title,
                        normalized_url,
                        location,
                    )
                if audience_ids is not None:
                    _set_navigation_node_audiences(
                        site_base_url,
                        int(node.get("Id")),
                        [str(value).strip() for value in audience_ids if str(value).strip()],
                    )
                final_node = _get_navigation_node_by_id(site_base_url, int(node.get("Id")))
                target_ref = _target_ref(
                    site_path=normalized_site_path,
                    nav_location=location,
                    navigation_node_id=final_node.get("Id"),
                )
                changes_applied = [
                    {
                        "operation": "navigation.upsert",
                        "navigation_node": {
                            "id": final_node.get("Id"),
                            "title": final_node.get("Title"),
                            "url": final_node.get("Url"),
                            "isExternal": final_node.get("IsExternal"),
                            "location": location,
                            "audience_ids": (
                                [str(value).strip() for value in audience_ids if str(value).strip()]
                                if audience_ids is not None
                                else None
                            ),
                        },
                    }
                ]

        elif operation == "navigation.reorder":
            location = _normalize_clients_navigation_location(
                str(target.get("nav_location", "")).strip()
            )
            if not location:
                raise ValueError("'target.nav_location' is required for navigation.reorder.")
            _navigation_location_endpoint(location)
            nav_order = target.get("nav_order")
            if not isinstance(nav_order, list) or not nav_order:
                raise ValueError("'target.nav_order' must be a non-empty array for navigation.reorder.")
            normalized_order = []
            for value in nav_order:
                value_str = str(value).strip()
                if not value_str.isdigit():
                    raise ValueError("Each 'target.nav_order' entry must be a navigation node id.")
                normalized_order.append(int(value_str))
            existing_nodes = _list_navigation_nodes(site_base_url, location)
            existing_ids = {int(node.get("Id")) for node in existing_nodes if node.get("Id") is not None}
            missing = [str(node_id) for node_id in normalized_order if node_id not in existing_ids]
            if missing:
                raise FileNotFoundError(
                    f"Navigation nodes not found in {location}: {', '.join(missing)}"
                )
            target_ref = _target_ref(site_path=normalized_site_path, nav_location=location)
            changes_applied = [
                {
                    "operation": "navigation.reorder",
                    "location": location,
                    "nav_order": [str(node_id) for node_id in normalized_order],
                }
            ]
            if not dry_run:
                _move_navigation_node_to_first(site_base_url, normalized_order[0])
                for previous_node_id, node_id in zip(normalized_order, normalized_order[1:]):
                    _move_navigation_node_after(site_base_url, node_id, previous_node_id)
                changes_applied = [
                    {
                        "operation": "navigation.reorder",
                        "location": location,
                        "nodes": _list_navigation_nodes(site_base_url, location),
                    }
                ]

        elif operation == "navigation.delete":
            location = _normalize_clients_navigation_location(
                str(target.get("nav_location", "")).strip()
            )
            if not location:
                raise ValueError("'target.nav_location' is required for navigation.delete.")
            _navigation_location_endpoint(location)
            nav_node = target.get("nav_node")
            if not isinstance(nav_node, dict):
                raise ValueError("'target.nav_node' must be an object for navigation.delete.")
            node_id = nav_node.get("id")
            title = str(nav_node.get("title", "")).strip()
            parent_id = nav_node.get("parent_id")
            if node_id is not None and str(node_id).strip() and not str(node_id).strip().isdigit():
                raise ValueError("'target.nav_node.id' must be a stringified integer when provided.")
            if parent_id is not None and str(parent_id).strip() and not str(parent_id).strip().isdigit():
                raise ValueError("'target.nav_node.parent_id' must be a stringified integer when provided.")
            if node_id is None and not title:
                raise ValueError("Provide either 'target.nav_node.id' or 'target.nav_node.title' for navigation.delete.")
            existing = None
            if node_id is not None and str(node_id).strip():
                existing = _get_navigation_node_by_id(site_base_url, int(str(node_id).strip()))
            elif parent_id is not None and str(parent_id).strip():
                existing = _find_navigation_child_by_title(
                    site_base_url,
                    int(str(parent_id).strip()),
                    title,
                )
            else:
                existing = _find_navigation_node_by_title_and_location(site_base_url, title, location)
            if not existing or existing.get("Id") is None:
                raise FileNotFoundError("The requested navigation node was not found.")
            target_ref = _target_ref(
                site_path=normalized_site_path,
                nav_location=location,
                navigation_node_id=existing.get("Id"),
            )
            changes_applied = [
                {
                    "operation": "navigation.delete",
                    "navigation_node": {
                        "id": existing.get("Id"),
                        "title": existing.get("Title"),
                        "url": existing.get("Url"),
                        "location": location,
                    },
                }
            ]
            if not dry_run:
                _delete_navigation_node(site_base_url, int(existing.get("Id")))

        elif operation == "permissions.get":
            resource_scope = _resolve_clients_permission_scope(target.get("resource_scope"))
            target_ref = resource_scope["target_ref"]
            if resource_scope["resource_type"] == "web":
                assignments = _get_site_role_assignments(site_base_url)
            elif resource_scope["resource_type"] == "list":
                assignments = _get_list_role_assignments(site_base_url, resource_scope["list_title"])
            else:
                assignments = _get_list_item_role_assignments(
                    site_base_url,
                    resource_scope["list_title"],
                    resource_scope["item_id"],
                )
            changes_applied = [
                {
                    "operation": "permissions.get",
                    "resource_kind": resource_scope["kind"],
                    "has_unique_role_assignments": resource_scope.get("has_unique_role_assignments"),
                    "assignments": assignments,
                }
            ]

        elif operation == "permissions.break_inheritance":
            resource_scope = _resolve_clients_permission_scope(target.get("resource_scope"))
            if resource_scope["resource_type"] == "web":
                raise ValueError("permissions.break_inheritance is not supported for site scope.")
            target_ref = resource_scope["target_ref"]
            if resource_scope.get("has_unique_role_assignments"):
                warnings.append("The target already has unique permissions; no inheritance break was needed.")
            changes_applied = [
                {
                    "operation": "permissions.break_inheritance",
                    "resource_kind": resource_scope["kind"],
                }
            ]
            if not dry_run and not resource_scope.get("has_unique_role_assignments"):
                if resource_scope["resource_type"] == "list":
                    _break_list_role_inheritance(site_base_url, resource_scope["list_title"])
                else:
                    _break_list_item_role_inheritance(
                        site_base_url,
                        resource_scope["list_title"],
                        resource_scope["item_id"],
                    )

        elif operation == "permissions.restore_inheritance":
            resource_scope = _resolve_clients_permission_scope(target.get("resource_scope"))
            if resource_scope["resource_type"] == "web":
                raise ValueError("permissions.restore_inheritance is not supported for site scope.")
            target_ref = resource_scope["target_ref"]
            if not resource_scope.get("has_unique_role_assignments"):
                warnings.append("The target already inherits permissions; no restore was needed.")
            changes_applied = [
                {
                    "operation": "permissions.restore_inheritance",
                    "resource_kind": resource_scope["kind"],
                }
            ]
            if not dry_run and resource_scope.get("has_unique_role_assignments"):
                if resource_scope["resource_type"] == "list":
                    _reset_list_role_inheritance(site_base_url, resource_scope["list_title"])
                else:
                    _reset_list_item_role_inheritance(
                        site_base_url,
                        resource_scope["list_title"],
                        resource_scope["item_id"],
                    )

        elif operation == "permissions.grant":
            resource_scope = _resolve_clients_permission_scope(target.get("resource_scope"))
            principal_info = _resolve_manage_clients_principal(site_base_url, target.get("principal"))
            role_name = _normalize_manage_clients_role(target)
            roledefid = _resolve_sharepoint_role_definition_id(site_base_url, role_name)
            target_ref = resource_scope["target_ref"]
            if resource_scope["resource_type"] != "web" and not resource_scope.get("has_unique_role_assignments"):
                raise ValueError(
                    "The target still inherits permissions. Call permissions.break_inheritance first."
                )
            changes_applied = [
                {
                    "operation": "permissions.grant",
                    "resource_kind": resource_scope["kind"],
                    "principal_id": principal_info["id"],
                    "principal_title": principal_info["title"],
                    "role": role_name,
                }
            ]
            if not dry_run:
                if resource_scope["resource_type"] == "web":
                    _add_web_role_assignment(site_base_url, principal_info["id"], roledefid)
                elif resource_scope["resource_type"] == "list":
                    _add_list_role_assignment(
                        site_base_url,
                        resource_scope["list_title"],
                        principal_info["id"],
                        roledefid,
                    )
                else:
                    _add_list_item_role_assignment(
                        site_base_url,
                        resource_scope["list_title"],
                        resource_scope["item_id"],
                        principal_info["id"],
                        roledefid,
                    )

        elif operation == "permissions.revoke":
            resource_scope = _resolve_clients_permission_scope(target.get("resource_scope"))
            principal_info = _resolve_manage_clients_principal(site_base_url, target.get("principal"))
            target_ref = resource_scope["target_ref"]
            if resource_scope["resource_type"] != "web" and not resource_scope.get("has_unique_role_assignments"):
                raise ValueError(
                    "The target still inherits permissions. Call permissions.break_inheritance first."
                )
            changes_applied = [
                {
                    "operation": "permissions.revoke",
                    "resource_kind": resource_scope["kind"],
                    "principal_id": principal_info["id"],
                    "principal_title": principal_info["title"],
                }
            ]
            if not dry_run:
                if resource_scope["resource_type"] == "web":
                    _remove_web_role_assignment(site_base_url, principal_info["id"])
                elif resource_scope["resource_type"] == "list":
                    _remove_list_role_assignment(
                        site_base_url,
                        resource_scope["list_title"],
                        principal_info["id"],
                    )
                else:
                    _remove_list_item_role_assignment(
                        site_base_url,
                        resource_scope["list_title"],
                        resource_scope["item_id"],
                        principal_info["id"],
                    )

        elif operation == "site.get_structure":
            pages = _graph_paged_get(
                f"{GRAPH_BASE}/sites/{site_id}/pages/microsoft.graph.sitePage"
            )
            lists = _graph_paged_get(
                f"{GRAPH_BASE}/sites/{site_id}/lists?$select=id,name,displayName,description,webUrl"
            )
            allowed_locations = [
                _normalize_clients_navigation_location(value)
                for value in _clients_site_management_surface().get("allowed_navigation_locations", [])
            ]
            navigation = {
                location: _list_navigation_nodes(site_base_url, location)
                for location in allowed_locations
            }
            target_ref = _target_ref(site_path=normalized_site_path)
            changes_applied = [
                {
                    "pages": [
                        _slim_site_page(page, _page_path_from_name(str(page.get("name") or "")))
                        for page in pages
                        if str(page.get("name") or "").strip()
                    ],
                    "lists": [
                        {
                            "id": item.get("id"),
                            "name": item.get("name"),
                            "displayName": item.get("displayName"),
                            "description": item.get("description"),
                            "webUrl": item.get("webUrl"),
                        }
                        for item in lists
                    ],
                    "navigation": navigation,
                }
            ]

        elif operation == "site.get_settings":
            web_settings = _sp_d(
                _sharepoint_rest_request(
                    site_base_url,
                    "/_api/web?$select=Id,Title,Url,Description,Language,WebTemplate,Configuration,NavAudienceTargetingEnabled",
                    method="GET",
                )
            )
            root_folder = _sp_d(
                _sharepoint_rest_request(
                    site_base_url,
                    "/_api/web/rootfolder?$select=WelcomePage,ServerRelativeUrl",
                    method="GET",
                )
            )
            target_ref = _target_ref(site_path=normalized_site_path)
            changes_applied = [
                {
                    "site": {
                        "id": web_settings.get("Id"),
                        "title": web_settings.get("Title"),
                        "url": web_settings.get("Url"),
                        "description": web_settings.get("Description"),
                        "language": web_settings.get("Language"),
                        "webTemplate": web_settings.get("WebTemplate"),
                        "configuration": web_settings.get("Configuration"),
                        "navAudienceTargetingEnabled": web_settings.get("NavAudienceTargetingEnabled"),
                        "welcomePage": root_folder.get("WelcomePage"),
                        "serverRelativeUrl": root_folder.get("ServerRelativeUrl"),
                    }
                }
            ]

        else:
            raise PermissionError(
                f"Operation '{operation}' is not admitted through manage_clients_site."
            )

        _audit_log(
            operation_id=operation_id,
            tool_name="manage_clients_site",
            actor_type="agent",
            actor_id="sharepoint-mcp",
            authorized_scope=f"site_id={site_id} site_scope={normalized_site_path} operation={operation}",
            target_object=target_ref,
            action_type=operation,
            output_status="success",
            input_record=input_record,
            version_before=version_before,
            version_after=version_after,
            reason_code=reason or None,
            approval_reference=(str(options.get("approval_token", "")).strip() or None),
            escalation_flag=False,
        )
        return _manage_clients_site_response(
            status="success",
            operation_id=operation_id,
            site_path=normalized_site_path,
            operation=operation,
            target_ref=target_ref,
            changes_applied=changes_applied,
            warnings=warnings,
            approval_used=approval_used,
        )
    except Exception as exc:
        status = _manage_clients_site_error_status(exc)
        error_target_ref = target_ref or _target_ref(
            site_path=(site_path or _CLIENTS_SITE_PATH),
            operation=operation,
        )
        _audit_log(
            operation_id=operation_id,
            tool_name="manage_clients_site",
            actor_type="agent",
            actor_id="sharepoint-mcp",
            authorized_scope=f"site_scope={site_path or _CLIENTS_SITE_PATH} operation={operation or 'UNKNOWN'} error_path",
            target_object=error_target_ref,
            action_type=operation or "manage_clients_site",
            output_status=status,
            input_record={
                "site_path": site_path,
                "operation": operation,
                "target": _summarize_arguments(raw_target if isinstance(raw_target, dict) else {}),
                "options": _summarize_arguments(raw_options if isinstance(raw_options, dict) else {}),
            },
            version_before=version_before,
            version_after=version_after,
            reason_code=(
                str(raw_options.get("reason", "")).strip()
                if isinstance(raw_options, dict)
                else None
            ),
            approval_reference=(
                str(raw_options.get("approval_token", "")).strip()
                if isinstance(raw_options, dict)
                else None
            ) or None,
            escalation_flag=(status == "approval_required"),
        )
        return _manage_clients_site_response(
            status=status,
            operation_id=operation_id,
            site_path=site_path or _CLIENTS_SITE_PATH,
            operation=operation or "",
            target_ref=error_target_ref,
            warnings=warnings,
            errors=[str(exc)],
            approval_used=approval_used,
        )


def tool_upload_draft(args: dict) -> str:
    """
    Upload a file to the Documentation DRAFTS folder.
    Target path is hardcoded to the allowlisted Documentation DRAFTS zone.
    Only the 'documentation' drive is permitted. No other paths are accessible.
    """
    filename    = args.get("filename", "").strip()
    content_str = args.get("content", "")
    encoding    = args.get("encoding", "utf-8")  # "utf-8" or "base64"
    operation_id = _new_operation_id("upload_draft")

    if not filename:
        raise ValueError("'filename' is required.")

    # Reject path traversal attempts
    if "/" in filename or "\\" in filename or ".." in filename:
        raise ValueError(
            "'filename' must be a plain filename with no path separators or '..'."
        )
    write_context = _require_write_context(args)

    drive_alias = "documentation"
    zones = _wip_write_zones()
    if not zones:
        raise RuntimeError("No SharePoint WIP write zones are configured.")
    zone = zones[0]
    drive_id = str(zone["library_id"])
    site_id = str(zone.get("site_id") or "")
    _require_managed_workspace_site(site_id)
    target_folder_id = str(zone.get("folder_id") or "")
    if not target_folder_id:
        raise RuntimeError("Configured WIP write zone is missing folder_id.")
    target_path = f"{_canonical_zone_path(zone['folder_prefixes'][0])}/{filename}"

    # Belt-and-suspenders: validate final path against write policy
    if not _is_allowed_write(drive_alias, target_path):
        raise PermissionError(
            f"Computed upload path '{target_path}' is outside the approved "
            f"write boundary. This should never happen — contact ML1."
        )

    if encoding == "base64":
        content_bytes = base64.b64decode(content_str)
    else:
        content_bytes = content_str.encode("utf-8")

    log.info("upload_draft filename=%s bytes=%d", filename, len(content_bytes))

    encoded_filename = quote(filename, safe="")
    url = f"{GRAPH_BASE}/drives/{drive_id}/items/{target_folder_id}:/{encoded_filename}:/content"
    result = _graph_put(url, content_bytes)
    item = _slim_item(result)
    target_ref = _target_ref(
        site_id=site_id,
        library_id=drive_id,
        path=target_path,
        filename=filename,
    )
    warnings = [
        "This runtime validates artifact provenance inputs but does not persist them as SharePoint metadata."
    ]
    _audit_log(
        operation_id=operation_id,
        tool_name="upload_draft",
        actor_type="agent",
        actor_id=write_context["actor_id"],
        authorized_scope=f"site_id={site_id} library_id={drive_id} path={_canonical_zone_path(zone['folder_prefixes'][0])}",
        target_object=target_ref,
        action_type="create_draft_document",
        output_status="success",
        input_record={
            "filename": filename,
            "encoding": encoding,
            "content_length": len(content_bytes),
            "run_id": write_context["run_id"],
            "workflow_ref": write_context["workflow_ref"],
            "runbook_ref": write_context["runbook_ref"],
            "capability_ref": write_context["capability_ref"],
            "artifact_version_ref": write_context["artifact_version_ref"],
            "provenance_label": write_context["provenance_label"],
            "reason_code": write_context["reason_code"],
            "upstream_artifact_ref": write_context["upstream_artifact_ref"],
            "human_operator_id": write_context["human_operator_id"],
        },
        version_after=str(item.get("id") or ""),
        reason_code=write_context["reason_code"],
        upstream_artifact_ref=write_context["upstream_artifact_ref"],
        approval_reference=write_context["approval_reference"] or None,
    )
    return _response_payload(
        status="success",
        operation_id=operation_id,
        target_ref=target_ref,
        result_payload={
            "item": item,
            "artifact_version_ref": write_context["artifact_version_ref"],
            "provenance_label": write_context["provenance_label"],
            "run_id": write_context["run_id"],
        },
        warnings=warnings,
    )


def tool_find_latest_template(args: dict) -> str:
    """
    Find the latest template in an allowlisted SharePoint template zone.
    """
    template_key = str(args.get("template_key", "")).strip()
    template_library_id = str(args.get("template_library_id", "")).strip() or None
    max_results = int(args.get("max_results", 10))
    operation_id = _new_operation_id("find_latest_template")

    if not template_key:
        raise ValueError("'template_key' is required.")
    if max_results < 1 or max_results > 20:
        raise ValueError("'max_results' must be between 1 and 20.")

    tokens = [token for token in re.split(r"[\s_\-]+", template_key.lower()) if token]
    templates: List[dict] = []

    for entry in _load_template_registry().get("templates", []):
        source_doc_id = str(entry.get("file_id") or "")
        if not source_doc_id:
            continue
        try:
            zone, item = _resolve_template_item(source_doc_id, template_library_id)
        except PermissionError:
            continue

        haystack = " ".join(
            [
                str(entry.get("canonical_name") or ""),
                str(entry.get("doc_type") or ""),
                str(item.get("name") or ""),
            ]
        ).lower()
        if not all(token in haystack for token in tokens):
            continue

        templates.append(
            {
                "doc_id": source_doc_id,
                "name": entry.get("canonical_name") or item.get("name"),
                "version": entry.get("version"),
                "last_modified_ts": item.get("lastModifiedDateTime"),
                "url": item.get("webUrl"),
                "template_library_id": zone.get("library_id"),
            }
        )

    templates.sort(key=lambda item: item.get("last_modified_ts") or "", reverse=True)
    log.info(
        "find_latest_template template_key=%s template_library_id=%s result_count=%d selected_doc_id=%s",
        template_key,
        template_library_id or "AUTO",
        len(templates[:max_results]),
        (templates[0]["doc_id"] if templates else "NONE"),
    )
    target_ref = _target_ref(
        template_key=template_key,
        template_library_id=template_library_id or "AUTO",
    )
    _audit_log(
        operation_id=operation_id,
        tool_name="find_latest_template",
        actor_type="agent",
        actor_id="sharepoint-mcp",
        authorized_scope="template_read_zones",
        target_object=target_ref,
        action_type="find_latest_template",
        output_status="success",
        input_record={
            "template_key": template_key,
            "template_library_id": template_library_id or "",
            "max_results": max_results,
        },
    )
    return _response_payload(
        status="success",
        operation_id=operation_id,
        target_ref=target_ref,
        result_payload={"templates": templates[:max_results]},
    )


def tool_diff_docs(args: dict) -> str:
    """
    Generate a read-only diff summary between two allowlisted SharePoint documents.
    """
    doc_a_id = str(args.get("doc_a_id", "")).strip()
    doc_b_id = str(args.get("doc_b_id", "")).strip()
    operation_id = _new_operation_id("diff_docs")

    if not doc_a_id or not doc_b_id:
        raise ValueError("'doc_a_id' and 'doc_b_id' are required.")

    zone_a, item_a = _resolve_diffable_item(doc_a_id)
    zone_b, item_b = _resolve_diffable_item(doc_b_id)
    if item_a.get("folder") or item_b.get("folder"):
        raise ValueError("diff_docs only supports files, not folders.")

    text_a = _extract_item_text(item_a, _download_drive_item_bytes(zone_a["library_id"], doc_a_id))
    text_b = _extract_item_text(item_b, _download_drive_item_bytes(zone_b["library_id"], doc_b_id))
    diff_summary_md, change_counts = _build_diff_summary(
        text_a,
        text_b,
        str(item_a.get("name") or doc_a_id),
        str(item_b.get("name") or doc_b_id),
    )
    log.info(
        "diff_docs doc_a_id=%s doc_b_id=%s size_a=%s size_b=%s method=text-diff-v1",
        doc_a_id,
        doc_b_id,
        item_a.get("size"),
        item_b.get("size"),
    )

    result = {
        "diff_summary_md": diff_summary_md,
        "change_counts": change_counts,
        "doc_a": _slim_item_with_path(item_a),
        "doc_b": _slim_item_with_path(item_b),
    }
    target_ref = _target_ref(doc_a_id=doc_a_id, doc_b_id=doc_b_id)
    _audit_log(
        operation_id=operation_id,
        tool_name="diff_docs",
        actor_type="agent",
        actor_id="sharepoint-mcp",
        authorized_scope="template_read_zones+wip_write_zones(read-only)",
        target_object=target_ref,
        action_type="diff_docs",
        output_status="success",
        input_record={"doc_a_id": doc_a_id, "doc_b_id": doc_b_id},
    )
    return _response_payload(
        status="success",
        operation_id=operation_id,
        target_ref=target_ref,
        result_payload=result,
    )


def tool_copy_template_to_wip(args: dict) -> str:
    """
    Copy a template document into an allowlisted SharePoint WIP destination.
    """
    source_doc_id = str(args.get("source_doc_id", "")).strip()
    dest_site_id = str(args.get("dest_site_id", "")).strip()
    dest_library_id = str(args.get("dest_library_id", "")).strip()
    dest_folder_path = str(args.get("dest_folder_path", "")).strip()
    new_name = str(args.get("new_name", "")).strip()
    overwrite = bool(args.get("overwrite", False))
    operation_id = _new_operation_id("copy_template_to_wip")

    if not source_doc_id:
        raise ValueError("'source_doc_id' is required.")
    if not dest_site_id or not dest_library_id or not dest_folder_path:
        raise ValueError(
            "'dest_site_id', 'dest_library_id', and 'dest_folder_path' are required."
        )
    if not new_name:
        raise ValueError("'new_name' is required.")
    if "/" in new_name or "\\" in new_name or ".." in new_name:
        raise ValueError("'new_name' must be a plain filename with no path separators or '..'.")
    write_context = _require_write_context(
        args,
        require_approval_reference=overwrite,
    )
    if overwrite:
        raise EscalationRequiredError(
            "overwrite=true is ML1-gated and not implemented by this MCP server; use an approved manual path referenced by 'approval_reference'."
        )

    zone, source_item = _resolve_template_item(source_doc_id)
    dest_zone = _resolve_wip_zone(dest_site_id, dest_library_id, dest_folder_path)
    _require_managed_workspace_site(dest_site_id)
    normalized_dest_folder = _canonical_zone_path(dest_folder_path)
    target_path = f"{normalized_dest_folder}/{new_name}"
    log.info(
        "copy_template_to_wip source_doc_id=%s dest_site_id=%s dest_library_id=%s dest_folder_path=%s allowlist_check=pass overwrite=%s",
        source_doc_id,
        dest_site_id,
        dest_library_id,
        normalized_dest_folder,
        overwrite,
    )

    existing = _graph_get_optional(_drive_root_url(dest_library_id, target_path))
    if existing is not None:
        raise PermissionError(
            f"Destination file '{target_path}' already exists. Overwrite is blocked by policy."
        )

    content = _download_drive_item_bytes(zone["library_id"], source_doc_id)
    content_type = (
        str(source_item.get("file", {}).get("mimeType") or "").strip()
        or "application/octet-stream"
    )
    upload_url = _drive_root_url(dest_library_id, target_path, ":/content")
    result = _graph_put(upload_url, content, content_type=content_type)
    payload = {
        "new_doc_id": result.get("id"),
        "new_url": result.get("webUrl"),
        "source_doc_id": source_doc_id,
        "dest_site_id": dest_zone.get("site_id"),
        "dest_library_id": dest_zone.get("library_id"),
        "dest_folder_path": normalized_dest_folder,
        "artifact_version_ref": write_context["artifact_version_ref"],
        "provenance_label": write_context["provenance_label"],
        "run_id": write_context["run_id"],
    }
    target_ref = _target_ref(
        source_doc_id=source_doc_id,
        dest_site_id=dest_zone.get("site_id"),
        dest_library_id=dest_zone.get("library_id"),
        dest_folder_path=normalized_dest_folder,
        new_name=new_name,
    )
    warnings = [
        "This runtime validates artifact provenance inputs but does not persist them as SharePoint metadata."
    ]
    _audit_log(
        operation_id=operation_id,
        tool_name="copy_template_to_wip",
        actor_type="agent",
        actor_id=write_context["actor_id"],
        authorized_scope=f"site_id={dest_zone.get('site_id')} library_id={dest_zone.get('library_id')} path={normalized_dest_folder}",
        target_object=target_ref,
        action_type="copy_template_to_wip",
        output_status="success",
        input_record={
            "source_doc_id": source_doc_id,
            "dest_site_id": dest_site_id,
            "dest_library_id": dest_library_id,
            "dest_folder_path": normalized_dest_folder,
            "new_name": new_name,
            "run_id": write_context["run_id"],
            "workflow_ref": write_context["workflow_ref"],
            "runbook_ref": write_context["runbook_ref"],
            "capability_ref": write_context["capability_ref"],
            "artifact_version_ref": write_context["artifact_version_ref"],
            "provenance_label": write_context["provenance_label"],
            "reason_code": write_context["reason_code"],
            "upstream_artifact_ref": write_context["upstream_artifact_ref"],
            "human_operator_id": write_context["human_operator_id"],
            "approval_reference": write_context["approval_reference"],
        },
        version_before=source_doc_id,
        version_after=str(result.get("id") or ""),
        reason_code=write_context["reason_code"],
        upstream_artifact_ref=write_context["upstream_artifact_ref"],
        approval_reference=write_context["approval_reference"] or None,
    )
    return _response_payload(
        status="success",
        operation_id=operation_id,
        target_ref=target_ref,
        result_payload=payload,
        warnings=warnings,
    )


# =============================================================================
# Tool Registry
# =============================================================================

_TOOLS = [
    {
        "name": "refresh_drive_ids",
        "description": (
            "Validate that each hardcoded drive ID in the server's drive registry is "
            "accessible via the Graph API. Calls GET /drives/{drive_id} for each entry "
            "and returns a report of ok / not_found / error status per drive. "
            "Mismatches indicate the drive ID is stale and needs updating. "
            "No writes performed — safe to call at any time."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "list_folder",
        "description": (
            "List the children (files and subfolders) of a folder path within an "
            "approved SharePoint drive. Returns item metadata only — no file content. "
            "Drives: 'legalmatters' (read-only), 'documentation' (DRAFTS path only), "
            "and 'clients_*' read-only aliases for the Clients site libraries. "
            "For full-library Clients aliases, an empty path targets the library root."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "drive": {
                    "type": "string",
                    "enum": sorted(_DRIVES),
                    "description": (
                        "Drive/library alias to query. Includes 'legalmatters', "
                        "'documentation', and the read-only 'clients_*' aliases "
                        "for the /sites/Clients libraries."
                    ),
                },
                "path": {
                    "type": "string",
                    "description": (
                        "Folder path relative to drive root. Must begin with an "
                        "approved intake prefix. Example: 'LL Matters (Essential)' "
                        "or 'LL Matters (Essential)/25-927-00003'. For full-library "
                        "Clients aliases, use an empty string to target the root."
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
            "Does NOT return file content. Same drive/path restrictions as list_folder. "
            "For full-library Clients aliases, an empty path returns the library root metadata."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "drive": {
                    "type": "string",
                    "enum": sorted(_DRIVES),
                    "description": "Drive/library alias to query (same as list_folder).",
                },
                "path": {
                    "type": "string",
                    "description": "Path to the item relative to drive root. Use an empty string for the root on full-library Clients aliases.",
                },
            },
            "required": ["drive", "path"],
        },
    },
    {
        "name": "review_site_page",
        "description": (
            "Review one existing SharePoint site page within the approved Clients "
            "SitePages helper surface. Returns page metadata, flattened text web "
            "part content, and supported web part inventory. Only existing "
            "`SitePages/*.aspx` pages in `/sites/Clients` are in scope."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "page_path": {
                    "type": "string",
                    "description": (
                        "Path to the page within the approved Clients SitePages surface. "
                        "Format: 'SitePages/<page>.aspx'. Example: 'SitePages/Home.aspx'."
                    ),
                },
            },
            "required": ["page_path"],
        },
    },
    {
        "name": "update_site_page_content",
        "description": (
            "Apply the current runtime's bounded content-update helper to one "
            "existing Clients SitePages page. Allowed mutations are limited to page "
            "title, page description, and existing text web part innerHtml. Broader "
            "Clients SitePages authority exists in doctrine but is not yet fully "
            "exposed through this specific tool."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "page_path": {
                    "type": "string",
                    "description": (
                        "Path to the target page within the approved Clients SitePages "
                        "surface. Format: 'SitePages/<page>.aspx'."
                    ),
                },
                "expected_e_tag": {
                    "type": "string",
                    "description": "Required current page eTag for version-safe update.",
                },
                "title": {
                    "type": "string",
                    "description": "Optional replacement page title.",
                },
                "description": {
                    "type": "string",
                    "description": "Optional replacement page description.",
                },
                "text_webparts": {
                    "type": "array",
                    "description": "Optional list of existing text web parts to update.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "webpart_id": {
                                "type": "string",
                                "description": "Identifier of an existing text web part on the page.",
                            },
                            "inner_html": {
                                "type": "string",
                                "description": "Replacement HTML for the existing text web part.",
                            },
                        },
                        "required": ["webpart_id", "inner_html"],
                    },
                },
                "run_id": {
                    "type": "string",
                    "description": "Required run identifier for write auditability.",
                },
                "workflow_ref": {
                    "type": "string",
                    "description": "Workflow reference. One of workflow_ref, runbook_ref, or capability_ref is required for writes.",
                },
                "runbook_ref": {
                    "type": "string",
                    "description": "Runbook reference. One of workflow_ref, runbook_ref, or capability_ref is required for writes.",
                },
                "capability_ref": {
                    "type": "string",
                    "description": "Capability reference. One of workflow_ref, runbook_ref, or capability_ref is required for writes.",
                },
                "artifact_version_ref": {
                    "type": "string",
                    "description": "Required artifact version reference for the page update.",
                },
                "provenance_label": {
                    "type": "string",
                    "description": "Required provenance label. Must begin with 'Derived from ML2 v'.",
                },
                "reason_code": {
                    "type": "string",
                    "description": "Required reason code for the write operation.",
                },
                "upstream_artifact_ref": {
                    "type": "string",
                    "description": "Required upstream artifact or prompt-chain reference.",
                },
                "approval_reference": {
                    "type": "string",
                    "description": "Optional ML1 approval reference for separately approved exception paths or change batches.",
                },
                "actor_id": {
                    "type": "string",
                    "description": "Optional initiating agent or operator identifier for audit logs.",
                },
                "human_operator_id": {
                    "type": "string",
                    "description": "Optional human operator identifier when the action is human-triggered.",
                },
            },
            "required": [
                "page_path",
                "expected_e_tag",
                "run_id",
                "artifact_version_ref",
                "provenance_label",
                "reason_code",
                "upstream_artifact_ref",
            ],
        },
    },
    {
        "name": "provision_client_workspace",
        "description": (
            "Execute one Clients provisioning helper batch. Creates one new "
            "client-specific SitePages page, one new `*-Documents` library, assigns "
            "existing principals to those created resources, and adds one shared-home "
            "navigation link."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "client_name": {
                    "type": "string",
                    "description": "Display name for the client workspace, such as 'ABC Corp'.",
                },
                "page_name": {
                    "type": "string",
                    "description": "Optional page filename. Format: '<client>.aspx'. Defaults to a slug derived from client_name.",
                },
                "page_title": {
                    "type": "string",
                    "description": "Optional page title. Defaults to '<client_name> Workspace'.",
                },
                "page_description": {
                    "type": "string",
                    "description": "Optional page description.",
                },
                "page_body_html": {
                    "type": "string",
                    "description": "Optional initial HTML body for the created client page. If omitted, the server generates a default workspace body.",
                },
                "library_name": {
                    "type": "string",
                    "description": "Optional document library name. Must match the approved `*-Documents` naming pattern.",
                },
                "page_role_assignments": {
                    "type": "array",
                    "description": "Required role assignments for the created page. Each entry must identify an existing principal and a role name.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "principal_id": {
                                "type": "integer",
                                "description": "Optional existing SharePoint principal id.",
                            },
                            "principal_name": {
                                "type": "string",
                                "description": "Optional existing SharePoint principal or site-group title.",
                            },
                            "role": {
                                "type": "string",
                                "description": "Required role name. Allowed values are defined by the Clients provisioning allowlist.",
                            },
                        },
                        "required": ["role"],
                    },
                },
                "library_role_assignments": {
                    "type": "array",
                    "description": "Required role assignments for the created library. Each entry must identify an existing principal and a role name.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "principal_id": {
                                "type": "integer",
                                "description": "Optional existing SharePoint principal id.",
                            },
                            "principal_name": {
                                "type": "string",
                                "description": "Optional existing SharePoint principal or site-group title.",
                            },
                            "role": {
                                "type": "string",
                                "description": "Required role name. Allowed values are defined by the Clients provisioning allowlist.",
                            },
                        },
                        "required": ["role"],
                    },
                },
                "home_link_title": {
                    "type": "string",
                    "description": "Optional shared-home navigation link title. Defaults to the page title.",
                },
                "home_link_location": {
                    "type": "string",
                    "description": "Optional navigation location. Currently only 'TopNavigationBar' is allowed.",
                },
                "home_link_audience_ids": {
                    "type": "array",
                    "description": "Optional Entra audience ids for the navigation link.",
                    "items": {"type": "string"},
                },
                "run_id": {
                    "type": "string",
                    "description": "Required run identifier for write auditability.",
                },
                "workflow_ref": {
                    "type": "string",
                    "description": "Workflow reference. One of workflow_ref, runbook_ref, or capability_ref is required for writes.",
                },
                "runbook_ref": {
                    "type": "string",
                    "description": "Runbook reference. One of workflow_ref, runbook_ref, or capability_ref is required for writes.",
                },
                "capability_ref": {
                    "type": "string",
                    "description": "Capability reference. One of workflow_ref, runbook_ref, or capability_ref is required for writes.",
                },
                "artifact_version_ref": {
                    "type": "string",
                    "description": "Required artifact version reference for the provisioning batch.",
                },
                "provenance_label": {
                    "type": "string",
                    "description": "Required provenance label. Must begin with 'Derived from ML2 v'.",
                },
                "reason_code": {
                    "type": "string",
                    "description": "Required reason code for the provisioning batch.",
                },
                "upstream_artifact_ref": {
                    "type": "string",
                    "description": "Required upstream artifact or prompt-chain reference.",
                },
                "approval_reference": {
                    "type": "string",
                    "description": "Optional approval reference when the batch is tied to a separate approval artifact.",
                },
                "actor_id": {
                    "type": "string",
                    "description": "Optional initiating agent or operator identifier for audit logs.",
                },
                "human_operator_id": {
                    "type": "string",
                    "description": "Optional human operator identifier when the action is human-triggered.",
                },
            },
            "required": [
                "client_name",
                "page_role_assignments",
                "library_role_assignments",
                "run_id",
                "artifact_version_ref",
                "provenance_label",
                "reason_code",
                "upstream_artifact_ref",
            ],
        },
    },
    {
        "name": "manage_clients_site",
        "description": (
            "Governed site-management wrapper for broad SharePoint operations "
            "within `/sites/Clients` only. Supports pages, libraries, folders, "
            "navigation, permissions, and site inspection under the approved "
            "control matrix. Some higher-risk operations require "
            "`options.approval_token`."
        ),
        "inputSchema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "site_path": {
                    "type": "string",
                    "const": "/sites/Clients",
                },
                "operation": {
                    "type": "string",
                    "enum": [
                        "page.create",
                        "page.update",
                        "page.publish",
                        "page.unpublish",
                        "page.delete",
                        "page.set_home",
                        "page.list",
                        "page.get",
                        "library.create",
                        "library.update",
                        "library.delete",
                        "folder.create",
                        "folder.move",
                        "folder.rename",
                        "folder.delete",
                        "navigation.get",
                        "navigation.upsert",
                        "navigation.reorder",
                        "navigation.delete",
                        "permissions.get",
                        "permissions.grant",
                        "permissions.revoke",
                        "permissions.break_inheritance",
                        "permissions.restore_inheritance",
                        "site.get_structure",
                        "site.get_settings",
                    ],
                },
                "target": {
                    "type": "object",
                    "description": "Operation target. Required keys depend on operation.",
                    "additionalProperties": False,
                    "properties": {
                        "page_name": {"type": "string"},
                        "page_title": {"type": "string"},
                        "page_layout": {
                            "type": "string",
                            "enum": ["article", "home", "singleWebPartAppPage", "repostPage"],
                        },
                        "page_canvas": {
                            "type": "array",
                            "description": "Structured page sections and web parts; not freeform HTML.",
                            "items": {
                                "type": "object",
                                "additionalProperties": True,
                            },
                        },
                        "library_name": {"type": "string"},
                        "library_description": {"type": "string"},
                        "library_template": {
                            "type": "string",
                            "enum": ["documentLibrary", "genericList"],
                        },
                        "folder_path": {"type": "string"},
                        "destination_path": {"type": "string"},
                        "new_name": {"type": "string"},
                        "nav_location": {
                            "type": "string",
                            "enum": ["quickLaunch", "topNavigation", "footer"],
                        },
                        "nav_node": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "id": {"type": "string"},
                                "title": {"type": "string"},
                                "url": {"type": "string"},
                                "parent_id": {"type": "string"},
                                "is_external": {"type": "boolean"},
                                "audience_ids": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                },
                            },
                        },
                        "nav_order": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "principal": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "type": {
                                    "type": "string",
                                    "enum": ["user", "group", "aad_group", "sharepoint_group"],
                                },
                                "id": {"type": "string"},
                                "email": {"type": "string"},
                                "display_name": {"type": "string"},
                            },
                        },
                        "role": {
                            "type": "string",
                            "enum": ["read", "edit", "contribute", "full_control", "custom"],
                        },
                        "custom_role_name": {"type": "string"},
                        "resource_scope": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "kind": {
                                    "type": "string",
                                    "enum": ["site", "page", "library", "folder", "file", "list_item"],
                                },
                                "path": {"type": "string"},
                                "id": {"type": "string"},
                            },
                            "required": ["kind"],
                        },
                    },
                },
                "options": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "dry_run": {"type": "boolean", "default": False},
                        "create_if_missing": {"type": "boolean", "default": False},
                        "overwrite": {"type": "boolean", "default": False},
                        "publish_after_update": {"type": "boolean", "default": False},
                        "require_approval_token": {"type": "boolean", "default": True},
                        "approval_token": {"type": "string"},
                        "expected_version": {"type": "string"},
                        "reason": {"type": "string"},
                    },
                },
            },
            "required": ["site_path", "operation", "target"],
        },
    },
    {
        "name": "upload_draft",
        "description": (
            "Upload a file to the Documentation site DRAFTS folder. "
            "Target is always the allowlisted Documentation WIP DRAFTS folder "
            "(`SB Execution/DRAFTS/{filename}` relative to the drive root). "
            "Only the filename is specified — the parent path is hardcoded and cannot "
            "be changed. Requires managed-workspace write context fields, provenance, "
            "and audit identifiers. No writes are permitted to any other path. "
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
                "run_id": {
                    "type": "string",
                    "description": "Required run identifier for write auditability.",
                },
                "workflow_ref": {
                    "type": "string",
                    "description": "Workflow reference. One of workflow_ref, runbook_ref, or capability_ref is required for writes.",
                },
                "runbook_ref": {
                    "type": "string",
                    "description": "Runbook reference. One of workflow_ref, runbook_ref, or capability_ref is required for writes.",
                },
                "capability_ref": {
                    "type": "string",
                    "description": "Capability reference. One of workflow_ref, runbook_ref, or capability_ref is required for writes.",
                },
                "artifact_version_ref": {
                    "type": "string",
                    "description": "Required artifact version reference for the generated draft.",
                },
                "provenance_label": {
                    "type": "string",
                    "description": "Required provenance label. Must begin with 'Derived from ML2 v'.",
                },
                "reason_code": {
                    "type": "string",
                    "description": "Required reason code for the write operation.",
                },
                "upstream_artifact_ref": {
                    "type": "string",
                    "description": "Required upstream artifact or prompt-chain reference.",
                },
                "actor_id": {
                    "type": "string",
                    "description": "Optional initiating agent or operator identifier for audit logs.",
                },
                "human_operator_id": {
                    "type": "string",
                    "description": "Optional human operator identifier when the action is human-triggered.",
                },
            },
            "required": [
                "filename",
                "content",
                "run_id",
                "artifact_version_ref",
                "provenance_label",
                "reason_code",
                "upstream_artifact_ref",
            ],
        },
    },
    {
        "name": "find_latest_template",
        "description": (
            "Find the latest template in an allowlisted SharePoint template zone. "
            "Searches the authoritative template registry plus live SharePoint metadata "
            "within configured template-read zones only."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "template_key": {
                    "type": "string",
                    "description": "Template search key, such as 'engagement agreement' or 'retainer'.",
                },
                "template_library_id": {
                    "type": "string",
                    "description": "Optional allowlisted template library ID to constrain the search.",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of matches to return. Default 10, maximum 20.",
                },
            },
            "required": ["template_key"],
        },
    },
    {
        "name": "diff_docs",
        "description": (
            "Generate a read-only textual diff summary between two allowlisted SharePoint "
            "documents. Reads file content only within the configured template and WIP zones."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "doc_a_id": {
                    "type": "string",
                    "description": "Drive item ID of the first allowlisted document.",
                },
                "doc_b_id": {
                    "type": "string",
                    "description": "Drive item ID of the second allowlisted document.",
                },
            },
            "required": ["doc_a_id", "doc_b_id"],
        },
    },
    {
        "name": "copy_template_to_wip",
        "description": (
            "Copy an allowlisted template document into an allowlisted SharePoint WIP "
            "destination for drafting. Overwrite is blocked by default and manual-approval "
            "paths are not exposed through this MCP server. Requires managed-workspace "
            "write context fields, provenance, and audit identifiers."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "source_doc_id": {
                    "type": "string",
                    "description": "Drive item ID of the source template document.",
                },
                "dest_site_id": {
                    "type": "string",
                    "description": "Destination SharePoint site ID. Must match an allowlisted WIP zone.",
                },
                "dest_library_id": {
                    "type": "string",
                    "description": "Destination document library ID. Must match an allowlisted WIP zone.",
                },
                "dest_folder_path": {
                    "type": "string",
                    "description": "Destination folder path relative to the destination drive root.",
                },
                "new_name": {
                    "type": "string",
                    "description": "Filename for the copied draft in the destination WIP folder.",
                },
                "overwrite": {
                    "type": "boolean",
                    "description": "Whether to overwrite an existing file. Default false; true is blocked by this server.",
                },
                "run_id": {
                    "type": "string",
                    "description": "Required run identifier for write auditability.",
                },
                "workflow_ref": {
                    "type": "string",
                    "description": "Workflow reference. One of workflow_ref, runbook_ref, or capability_ref is required for writes.",
                },
                "runbook_ref": {
                    "type": "string",
                    "description": "Runbook reference. One of workflow_ref, runbook_ref, or capability_ref is required for writes.",
                },
                "capability_ref": {
                    "type": "string",
                    "description": "Capability reference. One of workflow_ref, runbook_ref, or capability_ref is required for writes.",
                },
                "artifact_version_ref": {
                    "type": "string",
                    "description": "Required artifact version reference for the copied draft.",
                },
                "provenance_label": {
                    "type": "string",
                    "description": "Required provenance label. Must begin with 'Derived from ML2 v'.",
                },
                "reason_code": {
                    "type": "string",
                    "description": "Required reason code for the copy operation.",
                },
                "upstream_artifact_ref": {
                    "type": "string",
                    "description": "Required upstream artifact or prompt-chain reference.",
                },
                "approval_reference": {
                    "type": "string",
                    "description": "Required only for ML1-gated exception paths such as overwrite requests.",
                },
                "actor_id": {
                    "type": "string",
                    "description": "Optional initiating agent or operator identifier for audit logs.",
                },
                "human_operator_id": {
                    "type": "string",
                    "description": "Optional human operator identifier when the action is human-triggered.",
                },
            },
            "required": [
                "source_doc_id",
                "dest_site_id",
                "dest_library_id",
                "dest_folder_path",
                "new_name",
                "run_id",
                "artifact_version_ref",
                "provenance_label",
                "reason_code",
                "upstream_artifact_ref",
            ],
        },
    },
]

_TOOL_FN_MAP = {
    "refresh_drive_ids": tool_refresh_drive_ids,
    "list_folder":   tool_list_folder,
    "get_item":      tool_get_item,
    "review_site_page": tool_review_site_page,
    "update_site_page_content": tool_update_site_page_content,
    "provision_client_workspace": tool_provision_client_workspace,
    "manage_clients_site": tool_manage_clients_site,
    "upload_draft":  tool_upload_draft,
    "find_latest_template": tool_find_latest_template,
    "diff_docs": tool_diff_docs,
    "copy_template_to_wip": tool_copy_template_to_wip,
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
                    "version": "1.4.0",
                    "description": (
                        "Bounded SharePoint MCP — LL Second Brain. "
                        "Access limited to the approved repo-declared SharePoint boundary."
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
            except (EscalationRequiredError, PermissionError, ValueError) as exc:
                # Policy/validation errors — return as tool error (not JSON-RPC error)
                log.warning("tool error [%s]: %s", tool_name, exc)
                _ok(request_id, {
                    "content": [{"type": "text", "text": _error_payload(tool_name, exc, arguments)}],
                    "isError": True,
                })
            except Exception as exc:
                log.error("tool exception [%s]: %s", tool_name, exc, exc_info=True)
                _ok(request_id, {
                    "content": [{"type": "text", "text": _error_payload(tool_name, exc, arguments)}],
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
        "Drives: %s. Policy: read-only for legalmatters, Documentation DRAFTS-write, "
        "Clients managed-workspace authority with current SitePages helper slices, "
        "and a current Clients workspace-provisioning helper batch.",
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
