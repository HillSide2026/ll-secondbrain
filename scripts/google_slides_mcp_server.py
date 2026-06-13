#!/usr/bin/env python3
"""
Google Slides MCP Server — LL Second Brain
===========================================
Native MCP access for Google Slides, bounded to ML1-directed presentation work.

ACCESS POLICY:
  - Read tools (get_presentation, get_presentation_url) are unrestricted.
  - Write tools (create_presentation, add_slide, update_text, add_text_box)
    require approved_by, approval_artifact, and reason — same pattern as the
    Gmail MCP server.
  - No deletion of presentations. That is done manually via Google Drive.

PERMITTED OPERATIONS:
  1. create_presentation  — create a new Google Slides deck
  2. get_presentation     — read slide structure, placeholders, and notes
  3. add_slide            — append a slide with a named predefined layout
  4. update_text          — replace text in a named shape or placeholder
  5. add_text_box         — insert a new text box at given position/size
  6. get_presentation_url — return the edit and view URLs for a deck

CREDENTIALS:
  Reads GOOGLE_OAUTH_TOKEN_PATH from environment, falls back to
  00_SYSTEM/local_secrets/google_token.json. The token must include the
  https://www.googleapis.com/auth/presentations scope.

  Run scripts/google_slides_oauth_setup.py once to add that scope to the
  existing token.

Python 3.9 compatible. No external MCP SDK required.
Implements MCP JSON-RPC 2.0 stdio transport manually.
"""

from __future__ import annotations

import json
import logging
import os
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(_REPO_ROOT / ".env")
except ImportError:
    pass

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# =============================================================================
# Constants
# =============================================================================

SLIDES_SCOPE = "https://www.googleapis.com/auth/presentations"

PREDEFINED_LAYOUTS = {
    "BLANK",
    "CAPTION_ONLY",
    "TITLE",
    "TITLE_AND_BODY",
    "TITLE_AND_TWO_COLUMNS",
    "TITLE_ONLY",
    "SECTION_HEADER",
    "SECTION_TITLE_AND_DESCRIPTION",
    "ONE_COLUMN_TEXT",
    "MAIN_POINT",
    "BIG_NUMBER",
}

OPS_DIR = _REPO_ROOT / "06_RUNS" / "ops"
AUDIT_LOG = OPS_DIR / "slides_mcp_audit.ndjson"

# =============================================================================
# Logging
# =============================================================================

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)sZ [%(levelname)s] slides-mcp: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
log = logging.getLogger("slides_mcp")


# =============================================================================
# Auth
# =============================================================================

_SLIDES_SERVICE_CACHE: Optional[Any] = None
_SLIDES_CREDS_CACHE: Optional[Any] = None


def _get_token_path() -> Path:
    configured = os.getenv("GOOGLE_OAUTH_TOKEN_PATH", "").strip()
    if configured:
        p = Path(configured)
        return p if p.is_absolute() else _REPO_ROOT / configured
    return _REPO_ROOT / "00_SYSTEM" / "local_secrets" / "google_token.json"


def _get_slides_service() -> Any:
    global _SLIDES_SERVICE_CACHE, _SLIDES_CREDS_CACHE

    if _SLIDES_SERVICE_CACHE is not None and _SLIDES_CREDS_CACHE is not None:
        if not _SLIDES_CREDS_CACHE.expired:
            return _SLIDES_SERVICE_CACHE

    token_path = _get_token_path()
    if not token_path.exists():
        raise FileNotFoundError(
            f"Google OAuth token not found at {token_path}. "
            "Run scripts/google_slides_oauth_setup.py to generate a token with the "
            "presentations scope."
        )

    creds_data = json.loads(token_path.read_text())
    creds = Credentials.from_authorized_user_info(creds_data)

    if SLIDES_SCOPE not in (creds.scopes or set()):
        raise PermissionError(
            "The OAuth token does not include the presentations scope. "
            "Run scripts/google_slides_oauth_setup.py to re-authorize."
        )

    if creds.expired:
        if not creds.refresh_token:
            raise RuntimeError(
                "OAuth token is expired and has no refresh token. "
                "Run scripts/google_slides_oauth_setup.py to re-authorize."
            )
        try:
            creds.refresh(Request())
            token_path.write_text(creds.to_json())
        except Exception as exc:
            raise RuntimeError(
                "OAuth token refresh failed. Re-run scripts/google_slides_oauth_setup.py."
            ) from exc

    _SLIDES_CREDS_CACHE = creds
    _SLIDES_SERVICE_CACHE = build("slides", "v1", credentials=creds)
    return _SLIDES_SERVICE_CACHE


def _with_backoff(fn: Any, context: str = "") -> Any:
    for attempt in range(4):
        try:
            return fn()
        except HttpError as exc:
            if exc.resp.status in (429, 503) and attempt < 3:
                wait = 2 ** attempt
                log.warning("[backoff] %s attempt %d got HTTP %d, retrying in %ds",
                            context, attempt + 1, exc.resp.status, wait)
                time.sleep(wait)
            else:
                raise


# =============================================================================
# Audit
# =============================================================================

def _now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _append_audit(entry: Dict[str, Any]) -> None:
    OPS_DIR.mkdir(parents=True, exist_ok=True)
    with AUDIT_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


# =============================================================================
# Approval gate (same pattern as Gmail MCP server)
# =============================================================================

def _require_write_approval(args: Dict[str, Any], tool_name: str) -> Dict[str, str]:
    approved_by = str(args.get("approved_by", "")).strip()
    approval_artifact_text = str(args.get("approval_artifact", "")).strip()
    reason = str(args.get("reason", "")).strip()

    if not approved_by:
        raise PermissionError(f"{tool_name} requires 'approved_by'.")
    if not approval_artifact_text:
        raise PermissionError(f"{tool_name} requires 'approval_artifact'.")
    if not reason:
        raise PermissionError(f"{tool_name} requires 'reason'.")

    artifact_path = Path(approval_artifact_text)
    if not artifact_path.is_absolute():
        artifact_path = _REPO_ROOT / approval_artifact_text
    if not artifact_path.exists():
        raise PermissionError(f"approval_artifact not found: {artifact_path}")

    return {
        "approved_by": approved_by,
        "approval_artifact": str(artifact_path),
        "reason": reason,
    }


# =============================================================================
# Helpers
# =============================================================================

def _pt(value: float) -> Dict[str, Any]:
    return {"magnitude": float(value), "unit": "PT"}


def _presentation_url(presentation_id: str) -> str:
    return f"https://docs.google.com/presentation/d/{presentation_id}/edit"


def _presentation_view_url(presentation_id: str) -> str:
    return f"https://docs.google.com/presentation/d/{presentation_id}/pub"


def _slim_slide(slide: Dict[str, Any]) -> Dict[str, Any]:
    """Return a compact slide summary suitable for get_presentation output."""
    elements = []
    for el in slide.get("pageElements", []):
        obj_id = el.get("objectId", "")
        shape = el.get("shape", {})
        shape_type = shape.get("shapeType", "")
        placeholder = shape.get("placeholder", {})
        ph_type = placeholder.get("type", "")
        ph_index = placeholder.get("index")

        text_content = ""
        text_obj = shape.get("text", {})
        for te in text_obj.get("textElements", []):
            run = te.get("textRun", {})
            if run.get("content"):
                text_content += run["content"]

        entry: Dict[str, Any] = {
            "objectId": obj_id,
            "shapeType": shape_type,
        }
        if ph_type:
            entry["placeholderType"] = ph_type
        if ph_index is not None:
            entry["placeholderIndex"] = ph_index
        if text_content:
            entry["text"] = text_content.rstrip("\n")

        # Size and position for text boxes and shapes.
        size = el.get("size", {})
        transform = el.get("transform", {})
        if size or transform:
            entry["size"] = {
                "width_pt": size.get("width", {}).get("magnitude"),
                "height_pt": size.get("height", {}).get("magnitude"),
            }
            entry["position"] = {
                "x_pt": transform.get("translateX"),
                "y_pt": transform.get("translateY"),
            }

        elements.append(entry)

    notes_text = ""
    speaker_notes = slide.get("slideProperties", {}).get("notesPage", {})
    for el in speaker_notes.get("pageElements", []):
        shape = el.get("shape", {})
        ph = shape.get("placeholder", {})
        if ph.get("type") == "BODY":
            for te in shape.get("text", {}).get("textElements", []):
                run = te.get("textRun", {})
                if run.get("content"):
                    notes_text += run["content"]

    result: Dict[str, Any] = {
        "objectId": slide.get("objectId", ""),
        "elements": elements,
    }
    if notes_text.strip():
        result["speakerNotes"] = notes_text.rstrip("\n")
    return result


# =============================================================================
# Tool implementations
# =============================================================================

def tool_create_presentation(args: Dict[str, Any]) -> str:
    approval = _require_write_approval(args, "create_presentation")
    title = str(args.get("title", "")).strip()
    if not title:
        raise ValueError("'title' is required.")

    service = _get_slides_service()
    result = _with_backoff(
        lambda: service.presentations().create(body={"title": title}).execute(),
        "create_presentation",
    )
    pres_id = result.get("presentationId", "")
    output = {
        "presentationId": pres_id,
        "title": result.get("title", title),
        "url": _presentation_url(pres_id),
        "slide_count": len(result.get("slides", [])),
        "approved_by": approval["approved_by"],
        "approval_artifact": approval["approval_artifact"],
        "reason": approval["reason"],
    }
    _append_audit({"timestamp": _now_iso(), "tool": "create_presentation", **output})
    return json.dumps(output, indent=2)


def tool_get_presentation(args: Dict[str, Any]) -> str:
    presentation_id = str(args.get("presentation_id", "")).strip()
    if not presentation_id:
        raise ValueError("'presentation_id' is required.")

    service = _get_slides_service()
    result = _with_backoff(
        lambda: service.presentations().get(presentationId=presentation_id).execute(),
        f"get_presentation:{presentation_id}",
    )

    slides = [_slim_slide(s) for s in result.get("slides", [])]
    output = {
        "presentationId": presentation_id,
        "title": result.get("title", ""),
        "url": _presentation_url(presentation_id),
        "slide_count": len(slides),
        "slides": slides,
    }
    return json.dumps(output, indent=2)


def tool_add_slide(args: Dict[str, Any]) -> str:
    approval = _require_write_approval(args, "add_slide")
    presentation_id = str(args.get("presentation_id", "")).strip()
    if not presentation_id:
        raise ValueError("'presentation_id' is required.")

    layout = str(args.get("layout", "TITLE_AND_BODY")).strip().upper()
    if layout not in PREDEFINED_LAYOUTS:
        raise ValueError(
            f"'layout' must be one of: {sorted(PREDEFINED_LAYOUTS)}. Got '{layout}'."
        )

    insertion_index = args.get("insertion_index")
    request: Dict[str, Any] = {
        "createSlide": {
            "slideLayoutReference": {"predefinedLayout": layout},
        }
    }
    if insertion_index is not None:
        request["createSlide"]["insertionIndex"] = int(insertion_index)

    service = _get_slides_service()
    result = _with_backoff(
        lambda: service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={"requests": [request]},
        ).execute(),
        f"add_slide:{presentation_id}",
    )

    replies = result.get("replies", [{}])
    new_slide_id = replies[0].get("createSlide", {}).get("objectId", "") if replies else ""
    output = {
        "presentationId": presentation_id,
        "newSlideObjectId": new_slide_id,
        "layout": layout,
        "insertionIndex": insertion_index,
        "url": _presentation_url(presentation_id),
        "approved_by": approval["approved_by"],
        "approval_artifact": approval["approval_artifact"],
        "reason": approval["reason"],
    }
    _append_audit({"timestamp": _now_iso(), "tool": "add_slide", **output})
    return json.dumps(output, indent=2)


def tool_update_text(args: Dict[str, Any]) -> str:
    approval = _require_write_approval(args, "update_text")
    presentation_id = str(args.get("presentation_id", "")).strip()
    object_id = str(args.get("object_id", "")).strip()
    text = str(args.get("text", ""))

    if not presentation_id:
        raise ValueError("'presentation_id' is required.")
    if not object_id:
        raise ValueError("'object_id' is required (the shape or placeholder objectId from get_presentation).")

    requests = [
        {
            "deleteText": {
                "objectId": object_id,
                "textRange": {"type": "ALL"},
            }
        },
        {
            "insertText": {
                "objectId": object_id,
                "insertionIndex": 0,
                "text": text,
            }
        },
    ]

    service = _get_slides_service()
    _with_backoff(
        lambda: service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={"requests": requests},
        ).execute(),
        f"update_text:{presentation_id}:{object_id}",
    )

    output = {
        "presentationId": presentation_id,
        "objectId": object_id,
        "text_length": len(text),
        "url": _presentation_url(presentation_id),
        "approved_by": approval["approved_by"],
        "approval_artifact": approval["approval_artifact"],
        "reason": approval["reason"],
    }
    _append_audit({"timestamp": _now_iso(), "tool": "update_text", **output})
    return json.dumps(output, indent=2)


def tool_add_text_box(args: Dict[str, Any]) -> str:
    approval = _require_write_approval(args, "add_text_box")
    presentation_id = str(args.get("presentation_id", "")).strip()
    slide_id = str(args.get("slide_id", "")).strip()
    text = str(args.get("text", ""))

    if not presentation_id:
        raise ValueError("'presentation_id' is required.")
    if not slide_id:
        raise ValueError("'slide_id' is required (the slide objectId from get_presentation).")

    # Dimensions in points. Default to a reasonable 200x50pt box at origin.
    x_pt = float(args.get("x_pt", 100))
    y_pt = float(args.get("y_pt", 100))
    width_pt = float(args.get("width_pt", 400))
    height_pt = float(args.get("height_pt", 60))

    shape_id = f"textbox_{uuid.uuid4().hex[:12]}"

    requests = [
        {
            "createShape": {
                "objectId": shape_id,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {
                        "width": _pt(width_pt),
                        "height": _pt(height_pt),
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": x_pt,
                        "translateY": y_pt,
                        "unit": "PT",
                    },
                },
            }
        },
        {
            "insertText": {
                "objectId": shape_id,
                "insertionIndex": 0,
                "text": text,
            }
        },
    ]

    service = _get_slides_service()
    _with_backoff(
        lambda: service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={"requests": requests},
        ).execute(),
        f"add_text_box:{presentation_id}:{slide_id}",
    )

    output = {
        "presentationId": presentation_id,
        "slideObjectId": slide_id,
        "newShapeObjectId": shape_id,
        "text_length": len(text),
        "position": {"x_pt": x_pt, "y_pt": y_pt},
        "size": {"width_pt": width_pt, "height_pt": height_pt},
        "url": _presentation_url(presentation_id),
        "approved_by": approval["approved_by"],
        "approval_artifact": approval["approval_artifact"],
        "reason": approval["reason"],
    }
    _append_audit({"timestamp": _now_iso(), "tool": "add_text_box", **output})
    return json.dumps(output, indent=2)


def tool_get_presentation_url(args: Dict[str, Any]) -> str:
    presentation_id = str(args.get("presentation_id", "")).strip()
    if not presentation_id:
        raise ValueError("'presentation_id' is required.")
    output = {
        "presentationId": presentation_id,
        "edit_url": _presentation_url(presentation_id),
        "view_url": _presentation_view_url(presentation_id),
    }
    return json.dumps(output, indent=2)


# =============================================================================
# Tool registry
# =============================================================================

_APPROVAL_FIELDS = {
    "approved_by": {
        "type": "string",
        "description": "Approving human, typically ML1.",
    },
    "approval_artifact": {
        "type": "string",
        "description": "Repo-relative or absolute path to the approval artifact.",
    },
    "reason": {
        "type": "string",
        "description": "Short reason for this write operation.",
    },
}

_TOOLS: List[Dict[str, Any]] = [
    {
        "name": "create_presentation",
        "description": (
            "Create a new Google Slides presentation and return its ID and URL. "
            "Write tool — requires approved_by, approval_artifact, and reason."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title for the new presentation.",
                },
                **_APPROVAL_FIELDS,
            },
            "required": ["title", "approved_by", "approval_artifact", "reason"],
        },
    },
    {
        "name": "get_presentation",
        "description": (
            "Read a Google Slides presentation: slide IDs, placeholder objectIds, "
            "current text content, and speaker notes. Use this before calling "
            "update_text or add_text_box to discover the objectIds you need."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "presentation_id": {
                    "type": "string",
                    "description": "Google Slides presentation ID (from the URL or create_presentation).",
                },
            },
            "required": ["presentation_id"],
        },
    },
    {
        "name": "add_slide",
        "description": (
            "Append a slide to a presentation using a predefined layout. "
            "Returns the new slide's objectId. "
            "Write tool — requires approved_by, approval_artifact, and reason."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "presentation_id": {
                    "type": "string",
                    "description": "Google Slides presentation ID.",
                },
                "layout": {
                    "type": "string",
                    "enum": sorted(PREDEFINED_LAYOUTS),
                    "description": (
                        "Predefined slide layout. Default: TITLE_AND_BODY. "
                        "Common choices: BLANK, TITLE, TITLE_AND_BODY, TITLE_ONLY, SECTION_HEADER."
                    ),
                },
                "insertion_index": {
                    "type": "integer",
                    "description": (
                        "Zero-based position to insert the slide. "
                        "Omit to append at the end."
                    ),
                },
                **_APPROVAL_FIELDS,
            },
            "required": ["presentation_id", "approved_by", "approval_artifact", "reason"],
        },
    },
    {
        "name": "update_text",
        "description": (
            "Replace all text in a shape or placeholder identified by its objectId. "
            "Use get_presentation first to discover the objectId of the shape to update. "
            "Write tool — requires approved_by, approval_artifact, and reason."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "presentation_id": {
                    "type": "string",
                    "description": "Google Slides presentation ID.",
                },
                "object_id": {
                    "type": "string",
                    "description": (
                        "objectId of the shape or placeholder to update. "
                        "Obtain from get_presentation output."
                    ),
                },
                "text": {
                    "type": "string",
                    "description": "New text content. Replaces all existing text in the shape.",
                },
                **_APPROVAL_FIELDS,
            },
            "required": ["presentation_id", "object_id", "text", "approved_by", "approval_artifact", "reason"],
        },
    },
    {
        "name": "add_text_box",
        "description": (
            "Insert a new text box on a slide at a given position and size (in points). "
            "Returns the new shape's objectId. "
            "Write tool — requires approved_by, approval_artifact, and reason. "
            "Slide dimensions: standard Google Slides is 720 x 405 pt (widescreen)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "presentation_id": {
                    "type": "string",
                    "description": "Google Slides presentation ID.",
                },
                "slide_id": {
                    "type": "string",
                    "description": "objectId of the target slide (from get_presentation).",
                },
                "text": {
                    "type": "string",
                    "description": "Text to insert into the new text box.",
                },
                "x_pt": {
                    "type": "number",
                    "description": "Horizontal position of the top-left corner in points. Default: 100.",
                },
                "y_pt": {
                    "type": "number",
                    "description": "Vertical position of the top-left corner in points. Default: 100.",
                },
                "width_pt": {
                    "type": "number",
                    "description": "Width in points. Default: 400.",
                },
                "height_pt": {
                    "type": "number",
                    "description": "Height in points. Default: 60.",
                },
                **_APPROVAL_FIELDS,
            },
            "required": ["presentation_id", "slide_id", "text", "approved_by", "approval_artifact", "reason"],
        },
    },
    {
        "name": "get_presentation_url",
        "description": (
            "Return the edit URL and view/publish URL for a Google Slides presentation "
            "by ID. Read-only — no approval required."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "presentation_id": {
                    "type": "string",
                    "description": "Google Slides presentation ID.",
                },
            },
            "required": ["presentation_id"],
        },
    },
]

_TOOL_FN_MAP = {
    "create_presentation": tool_create_presentation,
    "get_presentation": tool_get_presentation,
    "add_slide": tool_add_slide,
    "update_text": tool_update_text,
    "add_text_box": tool_add_text_box,
    "get_presentation_url": tool_get_presentation_url,
}


# =============================================================================
# MCP JSON-RPC 2.0 stdio transport
# =============================================================================

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
                    "name": "slides-ll",
                    "version": "1.0.0",
                    "description": (
                        "Bounded Google Slides MCP — LL Second Brain. "
                        "Read-only tools unrestricted; write tools require ML1 approval."
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
            except (PermissionError, ValueError) as exc:
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
        "Google Slides MCP server starting. "
        "Read tools: unrestricted. Write tools: require ML1 approval."
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
