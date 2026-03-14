#!/usr/bin/env python3
"""
Review Promotions / Social / Forums inbox threads per PRO-018,
while routing matter-related threads back through PRO-014.

This workflow is proposal-first:
- Matter-associated threads may receive add-only matter/state labels when
  execution is explicitly requested under PRO-014.
- Non-matter category threads are reported as soft-junk cleanup candidates
  under PRO-018.

Constraints:
- No label creation
- No label removal
- No archive/delete
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
GMAIL_GOVERNANCE_DIR = REPO_ROOT / "gmail_governance"

import sys

if str(GMAIL_GOVERNANCE_DIR) not in sys.path:
    sys.path.insert(0, str(GMAIL_GOVERNANCE_DIR))

from batch_classifier import (  # type: ignore
    classify_thread,
    get_matter_signal_confidence,
    get_soft_junk_gmail_categories,
    resolve_thread_matter,
    supports_auto_matter_routing,
)
from matter_enforcement import (  # type: ignore
    MATTER_LEAF_PATTERN,
    MATTER_TIER_PREFIXES,
    get_matter_labels,
)
from state_enforcement import CANONICAL_LABELS, get_gmail_service  # type: ignore


DEFAULT_QUERY = "in:inbox (category:promotions OR category:social OR category:forums)"
REPORT_DIR = REPO_ROOT / "06_RUNS" / "ops"
DEFAULT_METADATA_BATCH_SIZE = 100
DEFAULT_PROGRESS_EVERY = 500
DEFAULT_BATCH_PAUSE_SECONDS = 0.2
DEFAULT_RETRY_LIMIT = 4


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def get_header(headers: Iterable[Dict[str, Any]], name: str) -> str:
    for header in headers:
        if str(header.get("name", "")).lower() == name.lower():
            return str(header.get("value", ""))
    return ""


def list_thread_ids(service: Any, query: str, max_threads: Optional[int]) -> List[str]:
    thread_ids: List[str] = []
    page_token: Optional[str] = None

    while True:
        kwargs: Dict[str, Any] = {"userId": "me", "q": query, "maxResults": 500}
        if page_token:
            kwargs["pageToken"] = page_token

        response = service.users().threads().list(**kwargs).execute()
        thread_ids.extend(str(item["id"]) for item in response.get("threads", []) if item.get("id"))
        if max_threads and len(thread_ids) >= max_threads:
            return thread_ids[:max_threads]

        page_token = response.get("nextPageToken")
        if not page_token:
            return thread_ids


def build_label_maps(service: Any) -> Dict[str, Dict[str, str]]:
    labels = service.users().labels().list(userId="me").execute().get("labels", [])
    name_to_id = {str(label["name"]): str(label["id"]) for label in labels if label.get("name")}
    id_to_name = {str(label["id"]): str(label["name"]) for label in labels if label.get("id")}
    return {"name_to_id": name_to_id, "id_to_name": id_to_name}


def is_retryable_fetch_error(error_text: str) -> bool:
    lowered = error_text.lower()
    return (
        "429" in lowered
        or "ratelimitexceeded" in lowered
        or "too many concurrent requests for user" in lowered
    )


def fetch_thread_metadata_batch(
    service: Any,
    thread_ids: List[str],
    retry_limit: int,
) -> Dict[str, Dict[str, Any]]:
    threads_by_id: Dict[str, Dict[str, Any]] = {}
    final_errors: Dict[str, str] = {}
    pending_ids = list(thread_ids)
    attempts = 0

    while pending_ids and attempts < retry_limit:
        errors_by_id: Dict[str, str] = {}
        batch = service.new_batch_http_request()

        def callback(request_id: str, response: Optional[Dict[str, Any]], exception: Optional[BaseException]) -> None:
            if exception is not None:
                errors_by_id[request_id] = str(exception)
                return
            if response is not None:
                threads_by_id[request_id] = response

        for thread_id in pending_ids:
            request = service.users().threads().get(
                userId="me",
                id=thread_id,
                format="metadata",
                metadataHeaders=["Subject", "From"],
            )
            batch.add(request, request_id=thread_id, callback=callback)

        batch.execute()

        retry_ids: List[str] = []
        for thread_id, error_text in errors_by_id.items():
            if is_retryable_fetch_error(error_text):
                retry_ids.append(thread_id)
            else:
                final_errors[thread_id] = error_text

        pending_ids = retry_ids
        attempts += 1
        if pending_ids:
            time.sleep(min(2 ** attempts, 8))

    for thread_id in pending_ids:
        final_errors[thread_id] = "rate_limit_retry_exhausted"

    for thread_id, error_text in final_errors.items():
        threads_by_id[thread_id] = {
            "id": thread_id,
            "messages": [],
            "_fetch_error": error_text,
        }

    return threads_by_id


def extract_existing_state_labels(label_names: List[str]) -> List[str]:
    return sorted(label for label in label_names if label in CANONICAL_LABELS)


def extract_existing_matter_labels(label_names: List[str]) -> List[str]:
    matter_labels: List[str] = []
    for label_name in label_names:
        if not any(label_name.startswith(prefix) for prefix in MATTER_TIER_PREFIXES):
            continue
        leaf = label_name.split("/")[-1] if "/" in label_name else label_name
        if MATTER_LEAF_PATTERN.match(leaf):
            matter_labels.append(label_name)
    return sorted(matter_labels)


def prepare_add_only_actions(
    record: Dict[str, Any],
    name_to_id: Dict[str, str],
) -> Dict[str, Any]:
    state_actions: List[str] = []
    matter_actions: List[str] = []
    add_label_names: List[str] = []
    add_label_ids: List[str] = []

    proposed_matter_label = record.get("proposed_matter_label")
    proposed_state_label = record.get("proposed_state_label")
    existing_matter_labels = record.get("existing_matter_labels", [])
    existing_state_labels = record.get("existing_state_labels", [])
    auto_route_matter = record.get("auto_route_matter_association", False)

    if auto_route_matter and proposed_matter_label:
        if len(existing_matter_labels) > 1:
            matter_actions.append("blocked_multiple_matter_labels")
        elif existing_matter_labels == [proposed_matter_label]:
            matter_actions.append("already_present")
        elif existing_matter_labels:
            matter_actions.append("blocked_existing_matter_label")
        elif proposed_matter_label not in name_to_id:
            matter_actions.append("missing_gmail_matter_label")
        else:
            matter_actions.append("ready_add")
            add_label_names.append(proposed_matter_label)
            add_label_ids.append(name_to_id[proposed_matter_label])
    else:
        matter_actions.append("not_applicable")

    if auto_route_matter and proposed_state_label:
        if len(existing_state_labels) > 1:
            state_actions.append("blocked_multiple_state_labels")
        elif existing_state_labels == [proposed_state_label]:
            state_actions.append("already_present")
        elif existing_state_labels:
            state_actions.append("blocked_existing_state_label")
        elif proposed_state_label not in name_to_id:
            state_actions.append("missing_gmail_state_label")
        else:
            state_actions.append("ready_add")
            add_label_names.append(proposed_state_label)
            add_label_ids.append(name_to_id[proposed_state_label])
    else:
        state_actions.append("not_applicable")

    return {
        "matter_actions": matter_actions,
        "state_actions": state_actions,
        "add_label_names": add_label_names,
        "add_label_ids": add_label_ids,
    }


def classify_thread_record(
    thread_id: str,
    thread: Dict[str, Any],
    label_maps: Dict[str, Dict[str, str]],
    matter_labels: Dict[str, List[Dict[str, str]]],
) -> Dict[str, Any]:
    label_id_to_name = label_maps["id_to_name"]
    fetch_error = thread.get("_fetch_error")
    if fetch_error:
        return {
            "thread_id": thread_id,
            "status": "fetch_error",
            "error": fetch_error,
        }

    messages = thread.get("messages", [])
    if not messages:
        return {
            "thread_id": thread_id,
            "status": "empty_thread",
        }

    first_message = messages[0]
    last_message = messages[-1]
    first_headers = first_message.get("payload", {}).get("headers", [])
    last_headers = last_message.get("payload", {}).get("headers", [])

    subject = get_header(first_headers, "Subject") or "(No Subject)"
    sender = get_header(first_headers, "From") or "(Unknown)"
    last_sender = get_header(last_headers, "From") or ""
    snippet = str(first_message.get("snippet", ""))

    thread_label_ids = set()
    for message in messages:
        thread_label_ids.update(message.get("labelIds", []))

    current_labels = sorted(
        label_id_to_name.get(label_id, label_id)
        for label_id in thread_label_ids
    )
    existing_state_labels = extract_existing_state_labels(current_labels)
    existing_matter_labels = extract_existing_matter_labels(current_labels)
    soft_junk_categories = get_soft_junk_gmail_categories(current_labels)

    matter_resolution = resolve_thread_matter(
        subject,
        sender,
        snippet,
        current_labels,
        matter_labels,
    )
    matter_signal = matter_resolution.get("signal")
    matter_confidence = get_matter_signal_confidence(matter_signal)
    auto_route_matter_association = (
        matter_resolution.get("status") == "matched"
        and supports_auto_matter_routing(matter_signal)
    )
    review_required_matter_candidate = (
        matter_resolution.get("status") == "matched"
        and not auto_route_matter_association
    )
    proposed_state_label = None
    if auto_route_matter_association:
        proposed_state_label = classify_thread(
            subject,
            sender,
            snippet,
            current_labels,
            last_sender=last_sender,
            message_count=len(messages),
            has_matter_association=True,
        )

    record = {
        "thread_id": thread_id,
        "subject": subject,
        "sender": sender,
        "last_sender": last_sender,
        "message_count": len(messages),
        "snippet": snippet[:200],
        "current_labels": current_labels,
        "existing_state_labels": existing_state_labels,
        "existing_matter_labels": existing_matter_labels,
        "soft_junk_gmail_categories": soft_junk_categories,
        "soft_junk_cleanup_candidate": bool(soft_junk_categories) and matter_resolution.get("status") == "none_found",
        "review_required_matter_candidate": review_required_matter_candidate,
        "auto_route_matter_association": auto_route_matter_association,
        "matter_resolution_status": matter_resolution.get("status"),
        "matter_resolution_signal": matter_resolution.get("signal"),
        "matter_resolution_confidence": matter_confidence,
        "extracted_matter_number": matter_resolution.get("matter_number"),
        "proposed_matter_label": matter_resolution.get("proposed_label"),
        "proposed_state_label": proposed_state_label,
        "ambiguous_matches": matter_resolution.get("ambiguous_matches", []),
    }

    record.update(prepare_add_only_actions(record, label_maps["name_to_id"]))
    return record


def execute_add_only_labels(
    service: Any,
    records: List[Dict[str, Any]],
    approval_artifact: str,
    approved_by: str,
    reason: str,
) -> Dict[str, Any]:
    executed: List[Dict[str, Any]] = []

    for record in records:
        add_label_ids = record.get("add_label_ids", [])
        if not add_label_ids:
            continue

        service.users().threads().modify(
            userId="me",
            id=record["thread_id"],
            body={"addLabelIds": add_label_ids, "removeLabelIds": []},
        ).execute()

        executed.append({
            "thread_id": record["thread_id"],
            "added_labels": record.get("add_label_names", []),
            "approved_by": approved_by,
            "approval_artifact": approval_artifact,
            "reason": reason,
        })

    return {
        "executed_count": len(executed),
        "executed_threads": executed,
    }


def build_summary(records: List[Dict[str, Any]]) -> Dict[str, int]:
    return {
        "threads_scanned": len(records),
        "fetch_errors": sum(1 for record in records if record.get("status") == "fetch_error"),
        "matter_matched": sum(1 for record in records if record.get("matter_resolution_status") == "matched"),
        "matter_ambiguous": sum(1 for record in records if record.get("matter_resolution_status") == "ambiguous"),
        "matter_review_required": sum(1 for record in records if record.get("review_required_matter_candidate")),
        "soft_junk_cleanup_candidates": sum(1 for record in records if record.get("soft_junk_cleanup_candidate")),
        "ready_matter_label_adds": sum(1 for record in records if "ready_add" in record.get("matter_actions", [])),
        "ready_state_label_adds": sum(1 for record in records if "ready_add" in record.get("state_actions", [])),
        "blocked_matter_conflicts": sum(
            1 for record in records
            if any(action.startswith("blocked_") for action in record.get("matter_actions", []))
        ),
        "blocked_state_conflicts": sum(
            1 for record in records
            if any(action.startswith("blocked_") for action in record.get("state_actions", []))
        ),
    }


def build_markdown_report(
    run_id: str,
    query: str,
    summary: Dict[str, int],
    records: List[Dict[str, Any]],
    execution: Optional[Dict[str, Any]],
) -> str:
    lines = [
        f"# Soft Junk Review {run_id}",
        "",
        f"- Query: `{query}`",
        f"- Threads scanned: `{summary['threads_scanned']}`",
        f"- Fetch errors: `{summary['fetch_errors']}`",
        f"- Matter matched: `{summary['matter_matched']}`",
        f"- Matter ambiguous: `{summary['matter_ambiguous']}`",
        f"- Matter review required: `{summary['matter_review_required']}`",
        f"- Soft-junk cleanup candidates: `{summary['soft_junk_cleanup_candidates']}`",
        f"- Ready matter-label adds: `{summary['ready_matter_label_adds']}`",
        f"- Ready state-label adds: `{summary['ready_state_label_adds']}`",
        "",
        "## Matter-associated threads",
        "",
    ]

    matched_records = [record for record in records if record.get("matter_resolution_status") == "matched"]
    if not matched_records:
        lines.append("- None")
    else:
        for record in matched_records:
            lines.append(
                "- `{thread_id}` | `{matter}` | matter_actions={matter_actions} | state_actions={state_actions} | subject={subject}".format(
                    thread_id=record["thread_id"],
                    matter=record.get("extracted_matter_number") or record.get("proposed_matter_label") or "matched",
                    matter_actions=",".join(record.get("matter_actions", [])),
                    state_actions=",".join(record.get("state_actions", [])),
                    subject=record.get("subject", "(No Subject)"),
                )
            )

    lines.extend([
        "",
        "## Matter review required",
        "",
    ])

    review_records = [record for record in records if record.get("review_required_matter_candidate")]
    if not review_records:
        lines.append("- None")
    else:
        for record in review_records:
            lines.append(
                "- `{thread_id}` | signal={signal} | confidence={confidence} | subject={subject}".format(
                    thread_id=record["thread_id"],
                    signal=record.get("matter_resolution_signal"),
                    confidence=record.get("matter_resolution_confidence"),
                    subject=record.get("subject", "(No Subject)"),
                )
            )

    lines.extend([
        "",
        "## Soft-junk cleanup candidates",
        "",
    ])

    candidate_records = [record for record in records if record.get("soft_junk_cleanup_candidate")]
    if not candidate_records:
        lines.append("- None")
    else:
        for record in candidate_records:
            lines.append(
                "- `{thread_id}` | categories={categories} | signal={signal} | subject={subject}".format(
                    thread_id=record["thread_id"],
                    categories=",".join(record.get("soft_junk_gmail_categories", [])),
                    signal=record.get("matter_resolution_signal"),
                    subject=record.get("subject", "(No Subject)"),
                )
            )

    if execution:
        lines.extend([
            "",
            "## Add-only label execution",
            "",
            f"- Executed threads: `{execution.get('executed_count', 0)}`",
        ])

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Review category-labeled inbox threads per PRO-018 and route matter threads per PRO-014.")
    parser.add_argument("--query", default=DEFAULT_QUERY, help="Gmail query to scan.")
    parser.add_argument("--max-threads", type=int, default=None, help="Optional cap on scanned threads.")
    parser.add_argument(
        "--metadata-batch-size",
        type=int,
        default=DEFAULT_METADATA_BATCH_SIZE,
        help=f"Threads to fetch per Gmail batch request. Default: {DEFAULT_METADATA_BATCH_SIZE}.",
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=DEFAULT_PROGRESS_EVERY,
        help=f"Emit a progress line every N processed threads. Default: {DEFAULT_PROGRESS_EVERY}.",
    )
    parser.add_argument(
        "--batch-pause-seconds",
        type=float,
        default=DEFAULT_BATCH_PAUSE_SECONDS,
        help=f"Pause between Gmail metadata batches. Default: {DEFAULT_BATCH_PAUSE_SECONDS}.",
    )
    parser.add_argument(
        "--retry-limit",
        type=int,
        default=DEFAULT_RETRY_LIMIT,
        help=f"Retry attempts for rate-limited Gmail metadata fetches. Default: {DEFAULT_RETRY_LIMIT}.",
    )
    parser.add_argument("--execute-labels", action="store_true", help="Apply add-only matter/state labels for matched matter threads.")
    parser.add_argument("--approval-artifact", default="", help="Approval artifact path required for --execute-labels.")
    parser.add_argument("--approved-by", default="", help="Approver name required for --execute-labels.")
    parser.add_argument("--reason", default="", help="Reason required for --execute-labels.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.execute_labels and (not args.approval_artifact or not args.approved_by or not args.reason):
        raise SystemExit("--execute-labels requires --approval-artifact, --approved-by, and --reason.")
    if args.execute_labels:
        approval_path = Path(args.approval_artifact)
        if not approval_path.is_absolute():
            approval_path = REPO_ROOT / approval_path
        if not approval_path.exists():
            raise SystemExit(f"Approval artifact not found: {approval_path}")

    service = get_gmail_service()
    label_maps = build_label_maps(service)
    matter_labels = get_matter_labels(service)
    thread_ids = list_thread_ids(service, args.query, args.max_threads)
    total_threads = len(thread_ids)
    records: List[Dict[str, Any]] = []
    metadata_batch_size = max(1, min(args.metadata_batch_size, 100))
    progress_every = max(1, args.progress_every)
    batch_pause_seconds = max(0.0, args.batch_pause_seconds)
    retry_limit = max(1, args.retry_limit)

    for start in range(0, total_threads, metadata_batch_size):
        chunk = thread_ids[start:start + metadata_batch_size]
        threads_by_id = fetch_thread_metadata_batch(service, chunk, retry_limit)
        for thread_id in chunk:
            thread = threads_by_id.get(thread_id, {"id": thread_id, "messages": [], "_fetch_error": "missing_batch_response"})
            records.append(classify_thread_record(thread_id, thread, label_maps, matter_labels))

        processed = min(start + len(chunk), total_threads)
        if processed == total_threads or processed % progress_every == 0:
            print(
                f"[soft_junk_review] processed {processed}/{total_threads} threads",
                file=sys.stderr,
                flush=True,
            )
        if processed < total_threads and batch_pause_seconds:
            time.sleep(batch_pause_seconds)

    summary = build_summary(records)
    execution: Optional[Dict[str, Any]] = None

    if args.execute_labels:
        execution = execute_add_only_labels(
            service,
            records,
            args.approval_artifact,
            args.approved_by,
            args.reason,
        )

    run_id = now_stamp()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = REPORT_DIR / f"soft_junk_review_{run_id}.json"
    md_path = REPORT_DIR / f"soft_junk_review_{run_id}.md"

    report = {
        "run_id": run_id,
        "query": args.query,
        "summary": summary,
        "execution": execution,
        "threads": records,
    }
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    md_path.write_text(
        build_markdown_report(run_id, args.query, summary, records, execution),
        encoding="utf-8",
    )

    print(json.dumps({
        "run_id": run_id,
        "query": args.query,
        "summary": summary,
        "execution": execution,
        "json_report": str(json_path),
        "markdown_report": str(md_path),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
