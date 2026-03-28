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

  Site: Clients  (/sites/Clients) — READ ONLY
    - clients_documents             -> Documents library, approved prefixes only
    - clients_master_client_library -> Master Client Library, full library read
    - clients_yellowbricks_capital  -> Yellowbricks Capital library, full library read
    - clients_turtle_island         -> Turtle Island library, full library read
    - clients_our_sharepoint_test2  -> Our-SharePoint-Test2 library, full library read
    - clients_our_sharepoint_test   -> our-sharepoint test library, full library read

Python 3.9 compatible. No external MCP SDK required.
Implements MCP JSON-RPC 2.0 stdio transport manually.
"""

from __future__ import annotations

import base64
import difflib
import json
import logging
import os
import re
import sys
import zipfile
from io import BytesIO
from html import unescape as html_unescape
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import quote
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


def _graph_raw_get(url: str) -> requests.Response:
    token = _get_token()
    r = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=120,
        allow_redirects=True,
    )
    return r


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


def _canonical_zone_path(prefix: str) -> str:
    return _normalize_drive_path("documentation", _normalize_path(prefix).lstrip("/"))


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

    return json.dumps(result, indent=2)


def tool_get_item(args: dict) -> str:
    """
    Get metadata for a single item (file or folder) by path.
    No file content is returned.
    """
    drive_alias = args.get("drive", "").lower()
    path        = args.get("path", "").strip()

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
    return json.dumps(_slim_item(item), indent=2)


def tool_upload_draft(args: dict) -> str:
    """
    Upload a file to the Documentation DRAFTS folder.
    Target path is hardcoded to the allowlisted Documentation DRAFTS zone.
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

    drive_alias = "documentation"
    zones = _wip_write_zones()
    if not zones:
        raise RuntimeError("No SharePoint WIP write zones are configured.")
    zone = zones[0]
    drive_id = str(zone["library_id"])
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
    return json.dumps(_slim_item(result), indent=2)


def tool_find_latest_template(args: dict) -> str:
    """
    Find the latest template in an allowlisted SharePoint template zone.
    """
    template_key = str(args.get("template_key", "")).strip()
    template_library_id = str(args.get("template_library_id", "")).strip() or None
    max_results = int(args.get("max_results", 10))

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
    return json.dumps({"templates": templates[:max_results]}, indent=2)


def tool_diff_docs(args: dict) -> str:
    """
    Generate a read-only diff summary between two allowlisted SharePoint documents.
    """
    doc_a_id = str(args.get("doc_a_id", "")).strip()
    doc_b_id = str(args.get("doc_b_id", "")).strip()

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
    return json.dumps(result, indent=2)


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
    if overwrite:
        raise PermissionError(
            "overwrite=true requires Manual approval and is not supported by this MCP server."
        )

    zone, source_item = _resolve_template_item(source_doc_id)
    dest_zone = _resolve_wip_zone(dest_site_id, dest_library_id, dest_folder_path)
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

    return json.dumps(
        {
            "new_doc_id": result.get("id"),
            "new_url": result.get("webUrl"),
            "source_doc_id": source_doc_id,
            "dest_site_id": dest_zone.get("site_id"),
            "dest_library_id": dest_zone.get("library_id"),
            "dest_folder_path": normalized_dest_folder,
        },
        indent=2,
    )


# =============================================================================
# Tool Registry
# =============================================================================

_TOOLS = [
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
        "name": "upload_draft",
        "description": (
            "Upload a file to the Documentation site DRAFTS folder. "
            "Target is always the allowlisted Documentation WIP DRAFTS folder "
            "(`SB Execution/DRAFTS/{filename}` relative to the drive root). "
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
            "paths are not exposed through this MCP server."
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
            },
            "required": [
                "source_doc_id",
                "dest_site_id",
                "dest_library_id",
                "dest_folder_path",
                "new_name",
            ],
        },
    },
]

_TOOL_FN_MAP = {
    "list_folder":   tool_list_folder,
    "get_item":      tool_get_item,
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
                    "version": "1.2.0",
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
        "Drives: %s. Policy: read-only for legalmatters and clients, DRAFTS-write for documentation.",
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
