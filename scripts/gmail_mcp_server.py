#!/usr/bin/env python3
"""
Gmail MCP Server — LL Second Brain
==================================
Native MCP access for Gmail, bounded to the same governed access surface as the
repo's Gmail scripts.

ACCESS POLICY (per ML1 directive):
  - Proposal-first for interactive mailbox work.
  - Controlled writes are permitted only for explicit label application tools.
  - Write tools require approved_by, approval_artifact, and reason.
  - No broader permissions than the existing Gmail script workflows.

PERMITTED OPERATIONS:
  1. list_messages            — list message stubs using Gmail query semantics
  2. get_message              — fetch one message by id
  3. list_threads             — list thread stubs using Gmail query semantics
  4. get_thread               — fetch one thread by id
  5. list_labels              — list mailbox labels
  6. apply_state_label        — apply one canonical state label to a thread
  7. apply_matter_label       — apply one canonical matter label to a thread
  8. apply_matter_label_query — apply one canonical matter label to all threads
                                 matching a Gmail query

Python 3.9 compatible. No external MCP SDK required.
Implements MCP JSON-RPC 2.0 stdio transport manually.
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
_GMAIL_GOVERNANCE_DIR = _REPO_ROOT / "gmail_governance"
if str(_GMAIL_GOVERNANCE_DIR) not in sys.path:
    sys.path.insert(0, str(_GMAIL_GOVERNANCE_DIR))

try:
    from dotenv import load_dotenv

    load_dotenv(_REPO_ROOT / ".env")
except ImportError:
    pass

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


CANONICAL_STATE_LABELS = {
    "00_Triage",
    "10_Action_Matthew",
    "20_Action_Team",
    "30_Waiting_External",
    "40_Replied_Awaiting_Response",
    "50_Calendar",
    "60_Filing",
    "70_Filed",
    "80_Junk (Pending Review)",
    "90_Archive",
}

MATTER_TIER_PREFIXES = {"LL/1./1.1/", "LL/1./1.2/", "LL/1./1.3/", "LL/1./1.4/"}
MATTER_LEAF_PATTERN = re.compile(r"^(\d{2,3}-\d{2,5}(?:-\d{5})?)\b")
VALID_MESSAGE_FORMATS = {"minimal", "metadata", "full", "raw"}

OPS_DIR = _REPO_ROOT / "06_RUNS" / "ops"
AUDIT_LOG = OPS_DIR / "gmail_mcp_audit.ndjson"
LOG_DIR = _REPO_ROOT / "06_RUNS" / "logs"
CLEANUP_LOG = LOG_DIR / "inbox_cleanup.log"

BATCH_SIZE = 1000

TRASH_QUERIES = [
    "in:inbox from:support@systemsandteams.com",
    "in:inbox from:news@bizbuysell.com",
    "in:inbox from:(noreply@medium.com OR newsletters@medium.com OR hello@medium.com)",
    "in:inbox from:david.a@plantationsinternational.com",
    "in:inbox from:notifications@account.brilliant.org",
    "in:inbox from:bettiegram@backofficebetties.com",
    "in:inbox from:email@e.lucid.co",
    "in:inbox from:noreply@skool.com",
    "in:inbox from:iwoszapar@user.luma-mail.com",
    "in:inbox from:support@epicnetwork.com",
    "in:inbox from:info@vivaglobal.us",
    "in:inbox from:communications@riskintelligence.lseg.com",
    "in:inbox from:communications@bnaibrith.ca",
    "in:inbox from:sales@infowisesolutions.com",
    "in:inbox from:team@weargustin.com",
    "in:inbox from:Windows365@mails.microsoft.com",
    "in:inbox from:teamzoom@zoom.us",
    "in:inbox from:customer-success-advisor@zoom.us",
    "in:inbox from:noreply@youtube.com",
    "in:inbox from:no-reply@mail.instagram.com",
    "in:inbox from:TDSurvey@feedback-td.com",
    "in:inbox from:notification@promo.bitget.com",
    "in:inbox from:talent@eq.tm.intuit.com",
    "in:inbox from:newsletters@audible.com",
    "in:inbox from:vaclav@vibetoexit.com",
]

ARCHIVE_QUERIES = [
    "in:inbox from:(messaging@promo.lexisnexis.ca OR experts@lawpay.info)",
    "in:inbox from:(info@ontario-commercial.com OR support@ontario-commercial.com)",
    "in:inbox from:marketing@getappara.ai",
    "in:inbox from:bruna@legalboards.com",
    "in:inbox from:inquiries-portagemaadvisory.ca@shared1.ccsend.com",
    "in:inbox from:dbaskin@baskinwealth.com",
    "in:inbox from:jprekaski@fbc.ca",
    "in:inbox from:(notifications-noreply@linkedin.com OR linkedin@e.linkedin.com OR messages-noreply@linkedin.com OR jobs-listings@linkedin.com)",
    "in:inbox from:hello@bighand.com",
    "in:inbox from:Jacob@updates.creme.digital",
    "in:inbox from:MyClaw@aisecret.us",
]

# Category sweep — archives pre-2026 inbox threads with soft-junk category labels.
# Date cutoff is fixed by ML1 directive. Do not remove.
CATEGORY_SWEEP_QUERY = (
    "in:inbox before:2026/1/1 "
    "(category:promotions OR category:social OR category:updates OR category:forums)"
)

_FROM_ANGLE_RE = re.compile(r"<([^>]+@[^>]+)>")
_EMAIL_RE = re.compile(r"[\w.+\-]+@[\w.\-]+")


logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)sZ [%(levelname)s] gmail-mcp: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
log = logging.getLogger("gmail_mcp")

cleanup_logger = logging.getLogger("gmail_inbox_cleanup")
cleanup_logger.setLevel(logging.INFO)
if not cleanup_logger.handlers:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    cleanup_handler = logging.FileHandler(CLEANUP_LOG)
    cleanup_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    cleanup_logger.addHandler(cleanup_handler)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _append_audit(entry: Dict[str, Any]) -> None:
    OPS_DIR.mkdir(parents=True, exist_ok=True)
    with AUDIT_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _resolve_approval_artifact(path_text: str) -> Path:
    artifact_path = Path(path_text)
    if not artifact_path.is_absolute():
        artifact_path = _REPO_ROOT / artifact_path
    return artifact_path


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

    artifact_path = _resolve_approval_artifact(approval_artifact_text)
    if not artifact_path.exists():
        raise PermissionError(f"approval_artifact not found: {artifact_path}")

    return {
        "approved_by": approved_by,
        "approval_artifact": str(artifact_path),
        "reason": reason,
    }


def _require_cleanup_authorization(args: Dict[str, Any], tool_name: str) -> Dict[str, str]:
    approved_by = str(args.get("approved_by", "")).strip()
    reason = str(args.get("reason", "")).strip()
    if not approved_by:
        raise PermissionError(f"{tool_name} requires 'approved_by'.")
    if not reason:
        raise PermissionError(f"{tool_name} requires 'reason'.")
    return {
        "approved_by": approved_by,
        "reason": reason,
    }


def _get_token_path() -> Path:
    configured = os.getenv("GOOGLE_OAUTH_TOKEN_PATH", "").strip()
    if configured:
        token_path = Path(configured)
        if not token_path.is_absolute():
            token_path = _REPO_ROOT / configured
        return token_path
    return _REPO_ROOT / "00_SYSTEM" / "local_secrets" / "google_token.json"


def _get_gmail_service() -> Any:
    token_path = _get_token_path()
    if not token_path.exists():
        raise FileNotFoundError(
            f"Gmail OAuth token not found at {token_path}. "
            "Set GOOGLE_OAUTH_TOKEN_PATH or run the Gmail OAuth setup."
        )

    creds_data = json.loads(token_path.read_text())
    creds = Credentials.from_authorized_user_info(creds_data)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build("gmail", "v1", credentials=creds)


def _list_all_labels(service: Any) -> List[Dict[str, Any]]:
    return service.users().labels().list(userId="me").execute().get("labels", [])


def _label_name_to_id(labels: List[Dict[str, Any]]) -> Dict[str, str]:
    return {str(label.get("name", "")): str(label.get("id", "")) for label in labels if label.get("name")}


def _label_id_to_name(labels: List[Dict[str, Any]]) -> Dict[str, str]:
    return {str(label.get("id", "")): str(label.get("name", "")) for label in labels if label.get("id")}


def _get_thread(service: Any, thread_id: str) -> Dict[str, Any]:
    return service.users().threads().get(userId="me", id=thread_id).execute()


def _collect_thread_label_ids(thread: Dict[str, Any]) -> List[str]:
    label_ids = set()
    for message in thread.get("messages", []):
        label_ids.update(message.get("labelIds", []))
    return sorted(label_ids)


def _find_existing_matter_label_ids(thread_label_ids: List[str], label_id_to_name: Dict[str, str]) -> List[str]:
    matter_label_ids: List[str] = []
    for label_id in thread_label_ids:
        label_name = label_id_to_name.get(label_id, "")
        if not any(label_name.startswith(prefix) for prefix in MATTER_TIER_PREFIXES):
            continue
        leaf = label_name.split("/")[-1] if "/" in label_name else label_name
        if MATTER_LEAF_PATTERN.match(leaf):
            matter_label_ids.append(label_id)
    return matter_label_ids


def _resolve_matter_label_id(
    labels: List[Dict[str, Any]],
    matter_label_name: str = "",
    matter_number: str = "",
) -> Dict[str, Any]:
    name_to_id = _label_name_to_id(labels)

    if matter_label_name:
        if matter_label_name not in name_to_id:
            raise ValueError(f"Matter label not found: {matter_label_name}")
        return {
            "matter_label_name": matter_label_name,
            "matter_label_id": name_to_id[matter_label_name],
            "resolution": "explicit_label_name",
        }

    if not matter_number:
        raise ValueError("Either 'matter_label_name' or 'matter_number' is required.")

    candidates: List[Dict[str, str]] = []
    for label in labels:
        label_name = str(label.get("name", ""))
        if not any(label_name.startswith(prefix) for prefix in MATTER_TIER_PREFIXES):
            continue
        leaf = label_name.split("/")[-1] if "/" in label_name else label_name
        match = MATTER_LEAF_PATTERN.match(leaf)
        if match and match.group(1) == matter_number:
            candidates.append({
                "matter_label_name": label_name,
                "matter_label_id": str(label.get("id", "")),
            })

    if not candidates:
        raise ValueError(f"No matter label found for matter_number '{matter_number}'.")
    if len(candidates) > 1:
        candidate_names = sorted(item["matter_label_name"] for item in candidates)
        raise ValueError(
            "Ambiguous matter_number '{}'; matching labels: {}".format(
                matter_number,
                candidate_names,
            )
        )

    resolved = candidates[0]
    resolved["resolution"] = "matter_number_lookup"
    return resolved


def _apply_thread_modify(
    service: Any,
    thread_id: str,
    add_label_ids: List[str],
    remove_label_ids: List[str],
) -> Dict[str, Any]:
    return service.users().threads().modify(
        userId="me",
        id=thread_id,
        body={
            "addLabelIds": add_label_ids,
            "removeLabelIds": remove_label_ids,
        },
    ).execute()


def _collect_message_ids_by_query(service: Any, query: str) -> List[str]:
    message_ids: List[str] = []
    page_token: Optional[str] = None

    while True:
        kwargs: Dict[str, Any] = {"userId": "me", "q": query, "maxResults": 500}
        if page_token:
            kwargs["pageToken"] = page_token

        response = service.users().messages().list(**kwargs).execute()
        message_ids.extend(str(item["id"]) for item in response.get("messages", []) if item.get("id"))
        page_token = response.get("nextPageToken")
        if not page_token:
            break

    return message_ids


def _collect_thread_ids_by_query(service: Any, query: str) -> List[str]:
    thread_ids: List[str] = []
    page_token: Optional[str] = None

    while True:
        kwargs: Dict[str, Any] = {"userId": "me", "q": query, "maxResults": 500}
        if page_token:
            kwargs["pageToken"] = page_token

        response = service.users().threads().list(**kwargs).execute()
        thread_ids.extend(str(item["id"]) for item in response.get("threads", []) if item.get("id"))
        page_token = response.get("nextPageToken")
        if not page_token:
            break

    return thread_ids


def _batch_modify_messages(
    service: Any,
    message_ids: List[str],
    add_label_ids: List[str],
    remove_label_ids: List[str],
) -> None:
    if not message_ids:
        return

    for start in range(0, len(message_ids), BATCH_SIZE):
        chunk = message_ids[start:start + BATCH_SIZE]
        service.users().messages().batchModify(
            userId="me",
            body={
                "ids": chunk,
                "addLabelIds": add_label_ids,
                "removeLabelIds": remove_label_ids,
            },
        ).execute()


def _cleanup_query_sets(scope: str) -> List[Dict[str, Any]]:
    if scope not in {"trash", "archive", "all"}:
        raise ValueError("'scope' must be one of ['trash', 'archive', 'all'].")

    query_sets: List[Dict[str, Any]] = []
    if scope in {"trash", "all"}:
        query_sets.append({
            "class": "trash",
            "queries": TRASH_QUERIES,
            "add_label_ids": ["TRASH"],
            "remove_label_ids": ["INBOX"],
        })
    if scope in {"archive", "all"}:
        query_sets.append({
            "class": "archive",
            "queries": ARCHIVE_QUERIES,
            "add_label_ids": [],
            "remove_label_ids": ["INBOX"],
        })
    return query_sets


def _preview_cleanup(scope: str) -> Dict[str, Any]:
    service = _get_gmail_service()
    preview: Dict[str, Any] = {
        "scope": scope,
        "trash_total": 0,
        "archive_total": 0,
        "queries": [],
    }

    for query_set in _cleanup_query_sets(scope):
        cleanup_class = query_set["class"]
        for query in query_set["queries"]:
            ids = _collect_message_ids_by_query(service, query)
            count = len(ids)
            preview["queries"].append({
                "class": cleanup_class,
                "query": query,
                "count": count,
            })
            if cleanup_class == "trash":
                preview["trash_total"] += count
            else:
                preview["archive_total"] += count

    preview["total"] = preview["trash_total"] + preview["archive_total"]
    return preview


def _log_cleanup_event(message: str) -> None:
    cleanup_logger.info(message)


def _extract_from_email(header_val: str) -> str:
    m = _FROM_ANGLE_RE.search(header_val)
    if m:
        return m.group(1).lower().strip()
    m2 = _EMAIL_RE.search(header_val)
    if m2:
        return m2.group(0).lower().strip()
    return ""


def _get_thread_from_email(thread: Dict[str, Any]) -> str:
    messages = thread.get("messages", [])
    if not messages:
        return ""
    headers = messages[0].get("payload", {}).get("headers", [])
    for h in headers:
        if h.get("name", "").lower() == "from":
            return _extract_from_email(h.get("value", ""))
    return ""


def _existing_sender_emails() -> set:
    emails: set = set()
    for q in TRASH_QUERIES + ARCHIVE_QUERIES:
        emails.update(m.lower() for m in _EMAIL_RE.findall(q))
    return emails


def _update_pro018_archive_senders(new_senders: List[str]) -> None:
    pro018_path = (
        _REPO_ROOT / "01_DOCTRINE" / "05_PROTOCOLS"
        / "PRO-018_Inbox_Soft_Junk_Cleanup_Protocol.md"
    )
    content = pro018_path.read_text(encoding="utf-8")
    new_lines = "\n".join(f"- `{s}`" for s in new_senders)
    marker = "\n\n---\n\n## 5."
    idx = content.find(marker)
    if idx != -1:
        content = content[:idx] + "\n" + new_lines + content[idx:]
        pro018_path.write_text(content, encoding="utf-8")


def _update_script_archive_queries(new_senders: List[str]) -> None:
    script_path = Path(__file__).resolve()
    content = script_path.read_text(encoding="utf-8")
    new_entries = "\n".join(f'    "in:inbox from:{s}",' for s in new_senders)
    pattern = re.compile(r"(^ARCHIVE_QUERIES\s*=\s*\[)(.*?)(\n\])", re.MULTILINE | re.DOTALL)

    def replacer(m: re.Match) -> str:  # type: ignore[type-arg]
        return m.group(1) + m.group(2) + "\n" + new_entries + m.group(3)

    new_content, count = pattern.subn(replacer, content)
    if count == 1:
        script_path.write_text(new_content, encoding="utf-8")


def tool_list_messages(args: Dict[str, Any]) -> str:
    service = _get_gmail_service()
    max_results = int(args.get("max_results", 10))
    query = args.get("query")
    label_ids = args.get("label_ids")

    if max_results < 1 or max_results > 500:
        raise ValueError("'max_results' must be between 1 and 500.")
    if label_ids is not None and not isinstance(label_ids, list):
        raise ValueError("'label_ids' must be a list when provided.")

    kwargs: Dict[str, Any] = {"userId": "me", "maxResults": max_results}
    if query:
        kwargs["q"] = str(query).strip()
    if label_ids:
        kwargs["labelIds"] = [str(item) for item in label_ids]
    messages = service.users().messages().list(**kwargs).execute().get("messages", [])
    return json.dumps(messages, indent=2)


def tool_get_message(args: Dict[str, Any]) -> str:
    service = _get_gmail_service()
    message_id = str(args.get("message_id", "")).strip()
    format_name = str(args.get("format", "metadata")).strip()

    if not message_id:
        raise ValueError("'message_id' is required.")
    if format_name not in VALID_MESSAGE_FORMATS:
        raise ValueError(f"'format' must be one of {sorted(VALID_MESSAGE_FORMATS)}.")

    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format=format_name,
    ).execute()
    return json.dumps(message, indent=2)


def tool_list_threads(args: Dict[str, Any]) -> str:
    service = _get_gmail_service()
    max_results = int(args.get("max_results", 10))
    query = str(args.get("query", "")).strip()

    if max_results < 1 or max_results > 500:
        raise ValueError("'max_results' must be between 1 and 500.")

    kwargs: Dict[str, Any] = {"userId": "me", "maxResults": max_results}
    if query:
        kwargs["q"] = query
    threads = service.users().threads().list(**kwargs).execute().get("threads", [])
    return json.dumps(threads, indent=2)


def tool_get_thread(args: Dict[str, Any]) -> str:
    service = _get_gmail_service()
    thread_id = str(args.get("thread_id", "")).strip()

    if not thread_id:
        raise ValueError("'thread_id' is required.")

    thread = _get_thread(service, thread_id)
    return json.dumps(thread, indent=2)


def tool_list_labels(args: Dict[str, Any]) -> str:
    service = _get_gmail_service()
    prefix = str(args.get("prefix", "")).strip()
    labels = service.users().labels().list(userId="me").execute().get("labels", [])
    if prefix:
        labels = [label for label in labels if str(label.get("name", "")).startswith(prefix)]
    return json.dumps(labels, indent=2)


def tool_preview_inbox_cleanup(args: Dict[str, Any]) -> str:
    scope = str(args.get("scope", "all")).strip().lower() or "all"
    preview = _preview_cleanup(scope)
    return json.dumps(preview, indent=2)


def tool_preview_garbage_candidates(args: Dict[str, Any]) -> str:
    batch_size = int(args.get("batch_size", 50))
    if batch_size < 1 or batch_size > 500:
        raise ValueError("'batch_size' must be between 1 and 500.")

    import batch_classifier as governance_batch_classifier

    batch = governance_batch_classifier.generate_batch(batch_size)
    candidate_labels = {"80_Junk (Pending Review)", "90_Archive"}
    candidates = [
        thread
        for thread in batch.get("threads", [])
        if thread.get("proposed_label") in candidate_labels
    ]
    result = {
        "batch_id": batch.get("batch_id"),
        "batch_size": batch.get("batch_size", 0),
        "candidate_count": len(candidates),
        "junk_count": sum(1 for item in candidates if item.get("proposed_label") == "80_Junk (Pending Review)"),
        "archive_count": sum(1 for item in candidates if item.get("proposed_label") == "90_Archive"),
        "candidates": candidates,
    }
    return json.dumps(result, indent=2)


def tool_execute_inbox_cleanup(args: Dict[str, Any]) -> str:
    scope = str(args.get("scope", "all")).strip().lower() or "all"
    authorization = _require_cleanup_authorization(args, "execute_inbox_cleanup")
    preview = _preview_cleanup(scope)

    service = _get_gmail_service()
    run_ts = _now_iso()
    _log_cleanup_event(
        "=== inbox_cleanup START | {} | mode=MCP_EXECUTE | scope={} | approved_by={} | reason={} ===".format(
            run_ts,
            scope,
            authorization["approved_by"],
            authorization["reason"],
        )
    )

    executed_queries: List[Dict[str, Any]] = []
    for query_set in _cleanup_query_sets(scope):
        cleanup_class = query_set["class"]
        add_label_ids = query_set["add_label_ids"]
        remove_label_ids = query_set["remove_label_ids"]
        for query in query_set["queries"]:
            ids = _collect_message_ids_by_query(service, query)
            if ids:
                _batch_modify_messages(service, ids, add_label_ids, remove_label_ids)
            _log_cleanup_event(
                "query={!r} | class={} | count={} | add={} | remove={}".format(
                    query,
                    cleanup_class,
                    len(ids),
                    add_label_ids,
                    remove_label_ids,
                )
            )
            executed_queries.append({
                "class": cleanup_class,
                "query": query,
                "count": len(ids),
            })

    result = {
        "executed_at": run_ts,
        "scope": scope,
        "trash_total": preview["trash_total"],
        "archive_total": preview["archive_total"],
        "total": preview["total"],
        "approved_by": authorization["approved_by"],
        "reason": authorization["reason"],
        "queries": executed_queries,
    }
    _log_cleanup_event(
        "=== inbox_cleanup COMPLETE | trashed={} | archived={} | mode=MCP_EXECUTE ===".format(
            result["trash_total"],
            result["archive_total"],
        )
    )
    _append_audit({
        "timestamp": run_ts,
        "tool": "execute_inbox_cleanup",
        **result,
    })
    return json.dumps(result, indent=2)


def tool_execute_category_sweep(args: Dict[str, Any]) -> str:
    authorization = _require_cleanup_authorization(args, "execute_category_sweep")
    max_threads = int(args.get("max_threads", 500))
    if max_threads < 1 or max_threads > 2000:
        raise ValueError("max_threads must be between 1 and 2000.")

    service = _get_gmail_service()
    labels = _list_all_labels(service)
    label_id_to_name = _label_id_to_name(labels)

    thread_ids = _collect_thread_ids_by_query(service, CATEGORY_SWEEP_QUERY)
    if len(thread_ids) > max_threads:
        thread_ids = thread_ids[:max_threads]

    existing = _existing_sender_emails()
    seen_senders: set = set()
    new_sender_emails: List[str] = []
    archived_ids: List[str] = []
    archived_message_ids: List[str] = []
    skipped_matter = 0
    errors: List[str] = []

    for thread_id in thread_ids:
        try:
            thread = service.users().threads().get(
                userId="me",
                id=thread_id,
                format="metadata",
                metadataHeaders=["From"],
            ).execute()
        except Exception as exc:
            errors.append(f"{thread_id}: {exc}")
            continue

        thread_label_ids = _collect_thread_label_ids(thread)
        if _find_existing_matter_label_ids(thread_label_ids, label_id_to_name):
            skipped_matter += 1
            continue

        archived_ids.append(thread_id)
        for msg in thread.get("messages", []):
            if msg.get("id"):
                archived_message_ids.append(msg["id"])

        from_email = _get_thread_from_email(thread)
        if from_email and from_email not in existing and from_email not in seen_senders:
            seen_senders.add(from_email)
            new_sender_emails.append(from_email)

    if archived_message_ids:
        _batch_modify_messages(service, archived_message_ids, [], ["INBOX"])

    if new_sender_emails:
        _update_pro018_archive_senders(new_sender_emails)
        _update_script_archive_queries(new_sender_emails)

    run_ts = _now_iso()
    result = {
        "executed_at": run_ts,
        "query": CATEGORY_SWEEP_QUERY,
        "threads_inspected": len(thread_ids),
        "archived": len(archived_ids),
        "skipped_matter": skipped_matter,
        "new_senders_added": len(new_sender_emails),
        "new_senders": new_sender_emails,
        "errors": len(errors),
        "approved_by": authorization["approved_by"],
        "reason": authorization["reason"],
    }
    _log_cleanup_event(
        f"execute_category_sweep | archived={result['archived']} | "
        f"new_senders={result['new_senders_added']} | approved_by={authorization['approved_by']}"
    )
    _append_audit({"timestamp": run_ts, "tool": "execute_category_sweep", **result})
    return json.dumps(result, ensure_ascii=False, indent=2)


def tool_resolve_confirmed_junk_threads(args: Dict[str, Any]) -> str:
    approval = _require_write_approval(args, "resolve_confirmed_junk_threads")
    thread_ids = args.get("thread_ids", [])
    if not isinstance(thread_ids, list) or not thread_ids:
        raise ValueError("'thread_ids' must be a non-empty list.")

    clean_thread_ids = [str(thread_id).strip() for thread_id in thread_ids if str(thread_id).strip()]
    if not clean_thread_ids:
        raise ValueError("'thread_ids' must contain at least one non-empty thread id.")

    service = _get_gmail_service()
    labels = _list_all_labels(service)
    name_to_id = _label_name_to_id(labels)

    if "90_Archive" not in name_to_id:
        raise ValueError("State label does not exist in Gmail: 90_Archive")

    target_label_id = name_to_id["90_Archive"]
    results: List[Dict[str, Any]] = []

    for thread_id in clean_thread_ids:
        thread = _get_thread(service, thread_id)
        thread_label_ids = _collect_thread_label_ids(thread)
        current_state_labels = [
            label_name
            for label_name in CANONICAL_STATE_LABELS
            if name_to_id.get(label_name) in thread_label_ids
        ]
        remove_label_ids = {
            name_to_id[label_name]
            for label_name in current_state_labels
            if label_name in name_to_id
        }
        if "INBOX" in thread_label_ids:
            remove_label_ids.add("INBOX")

        no_change = (
            len(current_state_labels) == 1
            and current_state_labels[0] == "90_Archive"
            and "INBOX" not in thread_label_ids
        )

        if not no_change:
            _apply_thread_modify(
                service,
                thread_id,
                [target_label_id],
                sorted(remove_label_ids),
            )

        result = {
            "thread_id": thread_id,
            "prior_state_labels": current_state_labels,
            "new_state_label": "90_Archive",
            "archived": True,
            "no_change": no_change,
        }
        results.append(result)
        _append_audit({
            "timestamp": _now_iso(),
            "tool": "resolve_confirmed_junk_threads",
            "approved_by": approval["approved_by"],
            "approval_artifact": approval["approval_artifact"],
            "reason": approval["reason"],
            **result,
        })

    summary = {
        "thread_count": len(results),
        "approved_by": approval["approved_by"],
        "approval_artifact": approval["approval_artifact"],
        "reason": approval["reason"],
        "results": results,
    }
    return json.dumps(summary, indent=2)


def tool_apply_state_label(args: Dict[str, Any]) -> str:
    approval = _require_write_approval(args, "apply_state_label")
    thread_id = str(args.get("thread_id", "")).strip()
    state_label = str(args.get("state_label", "")).strip()

    if not thread_id:
        raise ValueError("'thread_id' is required.")
    if state_label not in CANONICAL_STATE_LABELS:
        raise ValueError(f"'state_label' must be one of {sorted(CANONICAL_STATE_LABELS)}.")

    service = _get_gmail_service()
    labels = _list_all_labels(service)
    name_to_id = _label_name_to_id(labels)

    if state_label not in name_to_id:
        raise ValueError(f"State label does not exist in Gmail: {state_label}")

    thread = _get_thread(service, thread_id)
    thread_label_ids = _collect_thread_label_ids(thread)

    current_state_labels = [
        label_name
        for label_name in CANONICAL_STATE_LABELS
        if name_to_id.get(label_name) in thread_label_ids
    ]
    remove_label_ids = [
        name_to_id[label_name]
        for label_name in current_state_labels
        if label_name in name_to_id
    ]
    target_label_id = name_to_id[state_label]

    no_change = len(current_state_labels) == 1 and current_state_labels[0] == state_label
    if not no_change:
        _apply_thread_modify(service, thread_id, [target_label_id], remove_label_ids)

    result = {
        "thread_id": thread_id,
        "prior_state_labels": current_state_labels,
        "new_state_label": state_label,
        "no_change": no_change,
        "approved_by": approval["approved_by"],
        "approval_artifact": approval["approval_artifact"],
        "reason": approval["reason"],
    }
    _append_audit({
        "timestamp": _now_iso(),
        "tool": "apply_state_label",
        **result,
    })
    return json.dumps(result, indent=2)


def tool_apply_matter_label(args: Dict[str, Any]) -> str:
    approval = _require_write_approval(args, "apply_matter_label")
    thread_id = str(args.get("thread_id", "")).strip()
    matter_label_name = str(args.get("matter_label_name", "")).strip()
    matter_number = str(args.get("matter_number", "")).strip()

    if not thread_id:
        raise ValueError("'thread_id' is required.")
    if bool(matter_label_name) == bool(matter_number):
        raise ValueError("Provide exactly one of 'matter_label_name' or 'matter_number'.")

    service = _get_gmail_service()
    labels = _list_all_labels(service)
    label_id_to_name = _label_id_to_name(labels)
    resolved = _resolve_matter_label_id(
        labels,
        matter_label_name=matter_label_name,
        matter_number=matter_number,
    )

    thread = _get_thread(service, thread_id)
    thread_label_ids = _collect_thread_label_ids(thread)
    current_matter_label_ids = _find_existing_matter_label_ids(thread_label_ids, label_id_to_name)
    current_matter_labels = [label_id_to_name[label_id] for label_id in current_matter_label_ids if label_id in label_id_to_name]

    target_label_id = resolved["matter_label_id"]
    target_label_name = resolved["matter_label_name"]

    no_change = len(current_matter_label_ids) == 1 and current_matter_label_ids[0] == target_label_id
    if not no_change:
        _apply_thread_modify(service, thread_id, [target_label_id], current_matter_label_ids)

    result = {
        "thread_id": thread_id,
        "prior_matter_labels": current_matter_labels,
        "new_matter_label": target_label_name,
        "resolution": resolved["resolution"],
        "no_change": no_change,
        "approved_by": approval["approved_by"],
        "approval_artifact": approval["approval_artifact"],
        "reason": approval["reason"],
    }
    _append_audit({
        "timestamp": _now_iso(),
        "tool": "apply_matter_label",
        **result,
    })
    return json.dumps(result, indent=2)


def tool_apply_matter_label_query(args: Dict[str, Any]) -> str:
    approval = _require_write_approval(args, "apply_matter_label_query")
    query = str(args.get("query", "")).strip()
    matter_label_name = str(args.get("matter_label_name", "")).strip()
    matter_number = str(args.get("matter_number", "")).strip()

    if not query:
        raise ValueError("'query' is required.")
    if bool(matter_label_name) == bool(matter_number):
        raise ValueError("Provide exactly one of 'matter_label_name' or 'matter_number'.")

    service = _get_gmail_service()
    labels = _list_all_labels(service)
    label_id_to_name = _label_id_to_name(labels)
    resolved = _resolve_matter_label_id(
        labels,
        matter_label_name=matter_label_name,
        matter_number=matter_number,
    )

    thread_ids = _collect_thread_ids_by_query(service, query)
    target_label_id = resolved["matter_label_id"]
    target_label_name = resolved["matter_label_name"]
    results: List[Dict[str, Any]] = []

    for thread_id in thread_ids:
        thread = _get_thread(service, thread_id)
        thread_label_ids = _collect_thread_label_ids(thread)
        current_matter_label_ids = _find_existing_matter_label_ids(thread_label_ids, label_id_to_name)
        current_matter_labels = [
            label_id_to_name[label_id]
            for label_id in current_matter_label_ids
            if label_id in label_id_to_name
        ]

        no_change = len(current_matter_label_ids) == 1 and current_matter_label_ids[0] == target_label_id
        if not no_change:
            _apply_thread_modify(service, thread_id, [target_label_id], current_matter_label_ids)

        result = {
            "thread_id": thread_id,
            "prior_matter_labels": current_matter_labels,
            "new_matter_label": target_label_name,
            "resolution": resolved["resolution"],
            "no_change": no_change,
        }
        results.append(result)
        _append_audit({
            "timestamp": _now_iso(),
            "tool": "apply_matter_label_query",
            "query": query,
            "approved_by": approval["approved_by"],
            "approval_artifact": approval["approval_artifact"],
            "reason": approval["reason"],
            **result,
        })

    summary = {
        "query": query,
        "thread_count": len(results),
        "changed_count": sum(1 for item in results if not item["no_change"]),
        "no_change_count": sum(1 for item in results if item["no_change"]),
        "new_matter_label": target_label_name,
        "resolution": resolved["resolution"],
        "approved_by": approval["approved_by"],
        "approval_artifact": approval["approval_artifact"],
        "reason": approval["reason"],
        "thread_ids": [item["thread_id"] for item in results],
    }
    return json.dumps(summary, indent=2)


_TOOLS = [
    {
        "name": "list_messages",
        "description": (
            "List Gmail message stubs using standard Gmail query syntax. "
            "Read-only tool for proposal and triage workflows."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of messages to return. Range: 1-500. Default: 10.",
                },
                "query": {
                    "type": "string",
                    "description": "Optional Gmail search query, such as 'in:inbox newer_than:2d'.",
                },
                "label_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional Gmail label ids used to filter the result set.",
                },
            },
        },
    },
    {
        "name": "get_message",
        "description": "Fetch one Gmail message by id. Supports minimal, metadata, full, or raw format.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "message_id": {
                    "type": "string",
                    "description": "Gmail message id.",
                },
                "format": {
                    "type": "string",
                    "enum": ["minimal", "metadata", "full", "raw"],
                    "description": "Response format. Default: metadata.",
                },
            },
            "required": ["message_id"],
        },
    },
    {
        "name": "list_threads",
        "description": "List Gmail thread stubs using standard Gmail query syntax.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of threads to return. Range: 1-500. Default: 10.",
                },
                "query": {
                    "type": "string",
                    "description": "Optional Gmail search query, such as 'label:INBOX'.",
                },
            },
        },
    },
    {
        "name": "get_thread",
        "description": "Fetch one Gmail thread by id, including its messages and current label ids.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "thread_id": {
                    "type": "string",
                    "description": "Gmail thread id.",
                },
            },
            "required": ["thread_id"],
        },
    },
    {
        "name": "list_labels",
        "description": "List Gmail labels. Optional prefix filter helps narrow to canonical matter or state labels.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prefix": {
                    "type": "string",
                    "description": "Optional label-name prefix filter, such as 'LL/' or '00_'.",
                },
            },
        },
    },
    {
        "name": "preview_inbox_cleanup",
        "description": (
            "Preview confirmed inbox garbage cleanup using the governed sender lists from "
            "PRO-018. Returns counts only. No Gmail writes."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "scope": {
                    "type": "string",
                    "enum": ["trash", "archive", "all"],
                    "description": "Cleanup scope to preview. Default: all.",
                },
            },
        },
    },
    {
        "name": "execute_inbox_cleanup",
        "description": (
            "Execute confirmed inbox garbage cleanup using the governed sender lists from "
            "PRO-018. This is an ML1-directed bulk cleanup path. "
            "Requires approved_by and reason. Logs to 06_RUNS/logs/inbox_cleanup.log."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "scope": {
                    "type": "string",
                    "enum": ["trash", "archive", "all"],
                    "description": "Cleanup scope to execute. Default: all.",
                },
                "approved_by": {
                    "type": "string",
                    "description": "Approving human, typically ML1.",
                },
                "reason": {
                    "type": "string",
                    "description": "Short reason for the ML1-directed bulk cleanup.",
                },
            },
            "required": ["approved_by", "reason"],
        },
    },
    {
        "name": "execute_category_sweep",
        "description": (
            "Archive all inbox threads older than 2026-01-01 that carry a Gmail soft-junk "
            "category label (PROMOTIONS, SOCIAL, UPDATES, or FORUMS) and have no matter label. "
            "Extracts sender addresses from archived threads and appends new senders to the "
            "PRO-018 archive-class list so future execute_inbox_cleanup runs will cover them. "
            "ML1-directed. Requires approved_by and reason. "
            "Date cutoff (before:2026/1/1) is fixed by ML1 directive."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "approved_by": {
                    "type": "string",
                    "description": "Approving human, typically ML1.",
                },
                "reason": {
                    "type": "string",
                    "description": "Short reason for the category sweep.",
                },
                "max_threads": {
                    "type": "integer",
                    "description": "Maximum threads to process per run. Range: 1-2000. Default: 500.",
                },
            },
            "required": ["approved_by", "reason"],
        },
    },
    {
        "name": "preview_garbage_candidates",
        "description": (
            "Run the PRO-014 state-and-matter classifier in proposal mode and return current "
            "threads that would be marked as 80_Junk (Pending Review) or 90_Archive. "
            "This does not include PRO-018 soft-junk cleanup candidates."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "batch_size": {
                    "type": "integer",
                    "description": "Number of fresh inbox threads to inspect. Range: 1-500. Default: 50.",
                },
            },
        },
    },
    {
        "name": "resolve_confirmed_junk_threads",
        "description": (
            "Resolve specific ML1-confirmed junk threads by promoting them to 90_Archive "
            "and removing INBOX. Requires approved_by, approval_artifact, and reason."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "thread_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of Gmail thread ids to resolve as confirmed junk.",
                },
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
                    "description": "Short reason for the confirmed-junk resolution.",
                },
            },
            "required": ["thread_ids", "approved_by", "approval_artifact", "reason"],
        },
    },
    {
        "name": "apply_state_label",
        "description": (
            "Apply one canonical state label to a Gmail thread with exclusivity enforcement. "
            "Controlled write tool. Requires approved_by, approval_artifact, and reason."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "thread_id": {
                    "type": "string",
                    "description": "Gmail thread id.",
                },
                "state_label": {
                    "type": "string",
                    "enum": sorted(CANONICAL_STATE_LABELS),
                    "description": "Canonical state label to apply.",
                },
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
                    "description": "Short reason for the controlled label write.",
                },
            },
            "required": ["thread_id", "state_label", "approved_by", "approval_artifact", "reason"],
        },
    },
    {
        "name": "apply_matter_label",
        "description": (
            "Apply one canonical matter label to a Gmail thread with exclusivity enforcement. "
            "Provide exactly one of matter_label_name or matter_number. Controlled write tool. "
            "Requires approved_by, approval_artifact, and reason."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "thread_id": {
                    "type": "string",
                    "description": "Gmail thread id.",
                },
                "matter_label_name": {
                    "type": "string",
                    "description": "Exact Gmail label path to apply, such as 'LL/1./1.1/25-927-00003 -- Stream Ventures Limited'.",
                },
                "matter_number": {
                    "type": "string",
                    "description": "Matter number used to resolve the canonical matter label when unique.",
                },
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
                    "description": "Short reason for the controlled label write.",
                },
            },
            "required": ["thread_id", "approved_by", "approval_artifact", "reason"],
        },
    },
    {
        "name": "apply_matter_label_query",
        "description": (
            "Apply one canonical matter label to every Gmail thread matching a query, "
            "with exclusivity enforcement per thread. Provide exactly one of "
            "matter_label_name or matter_number. Controlled write tool. Requires "
            "approved_by, approval_artifact, and reason."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Gmail query selecting the target thread set, such as 'in:inbox from:aspireinfusions.com'.",
                },
                "matter_label_name": {
                    "type": "string",
                    "description": "Exact Gmail label path to apply.",
                },
                "matter_number": {
                    "type": "string",
                    "description": "Matter number used to resolve the canonical matter label when unique.",
                },
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
                    "description": "Short reason for the controlled bulk label write.",
                },
            },
            "required": ["query", "approved_by", "approval_artifact", "reason"],
        },
    },
]

_TOOL_FN_MAP = {
    "list_messages": tool_list_messages,
    "get_message": tool_get_message,
    "list_threads": tool_list_threads,
    "get_thread": tool_get_thread,
    "list_labels": tool_list_labels,
    "preview_inbox_cleanup": tool_preview_inbox_cleanup,
    "preview_garbage_candidates": tool_preview_garbage_candidates,
    "execute_inbox_cleanup": tool_execute_inbox_cleanup,
    "execute_category_sweep": tool_execute_category_sweep,
    "resolve_confirmed_junk_threads": tool_resolve_confirmed_junk_threads,
    "apply_state_label": tool_apply_state_label,
    "apply_matter_label": tool_apply_matter_label,
    "apply_matter_label_query": tool_apply_matter_label_query,
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
                    "name": "gmail-ll",
                    "version": "1.0.0",
                    "description": (
                        "Bounded Gmail MCP — LL Second Brain. "
                        "Proposal-first with controlled label writes."
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
        "Gmail MCP server starting. Policy: proposal-first with controlled state/matter label writes."
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
