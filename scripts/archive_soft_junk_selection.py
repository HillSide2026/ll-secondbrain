#!/usr/bin/env python3
"""
Archive an approved subset of PRO-018 soft-junk cleanup candidates.

Selection is limited to:
- threads marked soft_junk_cleanup_candidate in a review report
- approved sender strings (normalized exact match)
- approved thread ids

Archive action:
- remove INBOX only
- no delete / trash
- no label creation
- no label removal other than INBOX
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
GMAIL_GOVERNANCE_DIR = REPO_ROOT / "gmail_governance"
if str(GMAIL_GOVERNANCE_DIR) not in sys.path:
    sys.path.insert(0, str(GMAIL_GOVERNANCE_DIR))

from state_enforcement import get_gmail_service  # type: ignore


OPS_DIR = REPO_ROOT / "06_RUNS" / "ops"
AUDIT_LOG = OPS_DIR / "soft_junk_cleanup_audit.ndjson"


def normalize_sender(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip())


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def append_audit(entry: Dict[str, Any]) -> None:
    OPS_DIR.mkdir(parents=True, exist_ok=True)
    with AUDIT_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Archive an approved subset of PRO-018 soft-junk cleanup candidates.")
    parser.add_argument("--report", required=True, help="Path to soft_junk_review report JSON.")
    parser.add_argument("--approval-artifact", required=True, help="Approval artifact path.")
    parser.add_argument("--selection-file", default="", help="Optional JSON file with approved_senders and approved_thread_ids.")
    parser.add_argument("--approved-by", required=True, help="Approving human.")
    parser.add_argument("--reason", required=True, help="Reason for archive execution.")
    parser.add_argument("--approved-sender", action="append", default=[], help="Approved sender string. Repeatable.")
    parser.add_argument("--approved-thread-id", action="append", default=[], help="Approved thread id. Repeatable.")
    parser.add_argument("--execute", action="store_true", help="Perform Gmail archive writes. Default: dry-run.")
    return parser.parse_args()


def load_report(path_text: str) -> Dict[str, Any]:
    path = Path(path_text)
    if not path.is_absolute():
        path = REPO_ROOT / path
    if not path.exists():
        raise SystemExit(f"Report not found: {path}")
    return json.loads(path.read_text())


def resolve_approval_artifact(path_text: str) -> Path:
    path = Path(path_text)
    if not path.is_absolute():
        path = REPO_ROOT / path
    if not path.exists():
        raise SystemExit(f"Approval artifact not found: {path}")
    return path


def resolve_optional_path(path_text: str) -> Path:
    path = Path(path_text)
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path


def load_selection_file(path_text: str) -> Dict[str, Any]:
    path = resolve_optional_path(path_text)
    if not path.exists():
        raise SystemExit(f"Selection file not found: {path}")
    return json.loads(path.read_text())


def select_threads(
    report: Dict[str, Any],
    approved_senders: Set[str],
    approved_thread_ids: Set[str],
) -> List[Dict[str, Any]]:
    selected: List[Dict[str, Any]] = []
    seen_ids: Set[str] = set()

    for thread in report.get("threads", []):
        if not thread.get("soft_junk_cleanup_candidate"):
            continue

        thread_id = str(thread.get("thread_id", "")).strip()
        sender = normalize_sender(str(thread.get("sender", "")))

        if thread_id in approved_thread_ids or sender in approved_senders:
            if thread_id and thread_id not in seen_ids:
                selected.append(thread)
                seen_ids.add(thread_id)

    return selected


def archive_selected_threads(
    selected_threads: Iterable[Dict[str, Any]],
    approved_by: str,
    approval_artifact: str,
    reason: str,
    execute: bool,
) -> Dict[str, Any]:
    service = get_gmail_service()
    results: List[Dict[str, Any]] = []

    for thread in selected_threads:
        thread_id = str(thread["thread_id"])
        gmail_thread = service.users().threads().get(userId="me", id=thread_id, format="metadata").execute()
        label_ids = set()
        for message in gmail_thread.get("messages", []):
            label_ids.update(message.get("labelIds", []))

        archived_already = "INBOX" not in label_ids
        if execute and not archived_already:
            service.users().threads().modify(
                userId="me",
                id=thread_id,
                body={"removeLabelIds": ["INBOX"], "addLabelIds": []},
            ).execute()

        result = {
            "thread_id": thread_id,
            "sender": thread.get("sender"),
            "subject": thread.get("subject"),
            "archived": execute and not archived_already,
            "already_archived": archived_already,
        }
        results.append(result)
        append_audit({
            "timestamp": now_iso(),
            "tool": "archive_soft_junk_selection",
            "approved_by": approved_by,
            "approval_artifact": approval_artifact,
            "reason": reason,
            **result,
        })

    return {
        "selected_count": len(results),
        "archived_count": sum(1 for result in results if result["archived"]),
        "already_archived_count": sum(1 for result in results if result["already_archived"]),
        "results": results,
    }


def main() -> int:
    args = parse_args()
    report = load_report(args.report)
    approval_artifact = resolve_approval_artifact(args.approval_artifact)

    approved_sender_values = list(args.approved_sender)
    approved_thread_id_values = list(args.approved_thread_id)
    if args.selection_file:
        selection = load_selection_file(args.selection_file)
        approved_sender_values.extend(selection.get("approved_senders", []))
        approved_thread_id_values.extend(selection.get("approved_thread_ids", []))

    approved_senders = {normalize_sender(sender) for sender in approved_sender_values if normalize_sender(sender)}
    approved_thread_ids = {str(thread_id).strip() for thread_id in approved_thread_id_values if str(thread_id).strip()}
    selected_threads = select_threads(report, approved_senders, approved_thread_ids)

    OPS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")
    summary_path = OPS_DIR / f"soft_junk_selection_execution_{timestamp}.json"

    summary: Dict[str, Any] = {
        "run_id": timestamp,
        "source_report": args.report,
        "approved_by": args.approved_by,
        "approval_artifact": str(approval_artifact),
        "reason": args.reason,
        "execute": args.execute,
        "approved_sender_count": len(approved_senders),
        "approved_thread_id_count": len(approved_thread_ids),
        "selected_count": len(selected_threads),
        "selected_threads": [
            {
                "thread_id": thread["thread_id"],
                "sender": thread.get("sender"),
                "subject": thread.get("subject"),
            }
            for thread in selected_threads
        ],
    }

    if args.execute:
        execution = archive_selected_threads(
            selected_threads,
            approved_by=args.approved_by,
            approval_artifact=str(approval_artifact),
            reason=args.reason,
            execute=True,
        )
        summary["execution"] = execution

    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({
        "summary_path": str(summary_path),
        "selected_count": len(selected_threads),
        "execute": args.execute,
        "execution": summary.get("execution"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
