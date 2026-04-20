#!/usr/bin/env python3
"""
Backlog Cleanup Agent v0.1
==========================
Approved workflow for clearing email backlog via deterministic rules + minimal AI.

Authority:  ML1 approval 2026-04-16
Policy:     Backlog Cleanup Policy v0.1
Skill:      agents/backlog-cleanup-agent/skill.md

Separation constraint: this script ONLY archives. It does NOT classify or label.
It must not be merged with the inbox triage agent.

Allowed:    archive (remove INBOX label)
Forbidden:  delete, spam, unsubscribe, label mutation (except processed_cleanup tag)

Usage:
  # Phase 1 — dry run (no mutations)
  python3 scripts/backlog_cleanup_agent.py --dry-run --max-threads 200

  # Phase 2 — live (newsletters/receipts/notifications only, capped)
  python3 scripts/backlog_cleanup_agent.py --max-threads 500 --phase 2
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import time
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "gmail_governance"))

from state_enforcement import get_gmail_service  # type: ignore

# ── Constants ──────────────────────────────────────────────────────────────────

AGENT_VERSION = "backlog-cleanup-v0.2"
APPROVAL_BY = "ML1"
APPROVAL_DATE = "2026-04-16"
SKILL_DOC = REPO_ROOT / "agents" / "backlog-cleanup-agent" / "skill.md"

AUDIT_DIR = REPO_ROOT / "06_RUNS" / "ops" / "backlog_cleanup"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

# Backlog window default (days). Open decision — ML1 to confirm.
DEFAULT_BACKLOG_DAYS = 60

# Sender patterns that trigger deterministic archive
ARCHIVE_SENDER_PATTERNS = [
    r"no-reply@",
    r"noreply@",
    r"notifications?@",
    r"updates@",
    r"newsletter@",
    r"donotreply@",
    r"do-not-reply@",
    r"mailer@",
    r"bounce@",
    r"automated@",
    r"automailer@",
]
_ARCHIVE_SENDER_RE = re.compile("|".join(ARCHIVE_SENDER_PATTERNS), re.IGNORECASE)

# Gmail system category label IDs that indicate bulk/promo content
ARCHIVE_CATEGORY_LABELS = {
    "CATEGORY_PROMOTIONS",
    "CATEGORY_UPDATES",
    "CATEGORY_FORUMS",
    "CATEGORY_SOCIAL",
}

# Scope filter: categories to query in inbox
SCOPE_QUERY_CATEGORIES = (
    "category:promotions OR category:updates OR category:forums OR category:social"
)

# Phase 2 restriction: only archive these categories (more conservative)
PHASE2_ARCHIVE_CATEGORIES = {
    "CATEGORY_PROMOTIONS",
    "CATEGORY_UPDATES",
}

# Protected label prefixes — threads with these are skipped
MATTER_LABEL_PREFIX = "LL/"
MANUAL_LABEL_SKIP_PREFIXES = ("LL/",)  # any matter label = skip

# Canonical state labels applied by the triage agent — if any present, skip
CANONICAL_STATE_LABELS = {
    "00_Triage", "10_Action_Matthew", "20_Action_Team", "30_Waiting_External",
    "40_Replied_Awaiting_Response", "50_Calendar", "60_Filing",
    "70_Filed", "80_Junk_to_Review", "90_Archive",
}

# Sender domains that are system-generated but matter-related — never archive
PROTECTED_SENDER_DOMAINS = {
    "clio.com", "adobesign.com", "docusign.com", "dropbox.com",
    "bcregistries.gov.bc.ca", "corporateonline.gov.bc.ca",
    "ontario.ca", "courts.gc.ca", "osb-bsf.gc.ca", "fintrac-canafe.gc.ca",
    "lsbc.ca", "lso.ca",
}

# Clio matter ID pattern in subject — protect if present
_MATTER_ID_RE = re.compile(r"\b\d{2}-\d{3,5}-\d{5}\b")

# ── Helpers ────────────────────────────────────────────────────────────────────


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def get_header(headers: List[Dict[str, Any]], name: str) -> str:
    for h in headers:
        if h.get("name", "").lower() == name.lower():
            return h.get("value", "")
    return ""


def has_bulk_headers(headers: List[Dict[str, Any]]) -> bool:
    """Detect bulk/automated send headers."""
    list_id = get_header(headers, "List-ID")
    precedence = get_header(headers, "Precedence")
    list_unsubscribe = get_header(headers, "List-Unsubscribe")
    return bool(list_id or list_unsubscribe or precedence.lower() in ("bulk", "list", "junk"))


def has_unsubscribe_in_body(snippet: str) -> bool:
    return bool(re.search(r"unsubscribe", snippet, re.IGNORECASE))


def is_protected(
    thread_labels: List[str],
    is_starred: bool,
    has_recent_reply: bool,
    sender: str,
    subject: str,
) -> Tuple[bool, str]:
    """Return (protected, reason)."""
    if is_starred:
        return True, "starred"
    if has_recent_reply:
        return True, "ml1_replied"
    for label in thread_labels:
        if label.startswith(MATTER_LABEL_PREFIX):
            return True, f"matter_label:{label}"
    # Triage agent has classified this thread — leave it alone
    for label in thread_labels:
        if label in CANONICAL_STATE_LABELS:
            return True, f"triage_label:{label}"
    # Matter number in subject
    if _MATTER_ID_RE.search(subject):
        return True, "matter_id_in_subject"
    # Protected sender domain
    sender_lower = sender.lower()
    for domain in PROTECTED_SENDER_DOMAINS:
        if domain in sender_lower:
            return True, f"protected_domain:{domain}"
    return False, ""


def deterministic_archive_check(
    sender: str,
    thread_labels: List[str],
    headers: List[Dict[str, Any]],
    snippet: str,
    phase: int,
) -> Tuple[bool, str]:
    """Return (should_archive, reason). No AI involved."""

    # Sender pattern match
    if _ARCHIVE_SENDER_RE.search(sender):
        return True, f"sender_pattern:{sender}"

    # Category label
    category_labels = set(thread_labels) & ARCHIVE_CATEGORY_LABELS
    if phase == 2:
        category_labels = category_labels & PHASE2_ARCHIVE_CATEGORIES
    if category_labels:
        return True, f"category:{','.join(sorted(category_labels))}"

    # Bulk headers
    if has_bulk_headers(headers):
        return True, "bulk_headers"

    # Unsubscribe in snippet
    if has_unsubscribe_in_body(snippet):
        return True, "unsubscribe_link"

    return False, ""


def archive_thread(service: Any, thread_id: str, dry_run: bool) -> bool:
    """Remove INBOX label from thread. Returns True on success."""
    if dry_run:
        return True
    try:
        service.users().threads().modify(
            userId="me",
            id=thread_id,
            body={"removeLabelIds": ["INBOX"]},
        ).execute()
        return True
    except Exception as exc:
        logging.warning(f"archive_thread failed for {thread_id}: {exc}")
        return False


def append_log(run_id: str, entry: Dict[str, Any]) -> None:
    log_path = AUDIT_DIR / f"run_{run_id}.ndjson"
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ── Main ───────────────────────────────────────────────────────────────────────


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backlog Cleanup Agent v0.1")
    parser.add_argument("--dry-run", action="store_true", help="Log only — no mutations.")
    parser.add_argument("--phase", type=int, default=1, choices=[1, 2],
                        help="Phase 1 = dry run categories; Phase 2 = live limited categories.")
    parser.add_argument("--max-threads", type=int, default=200,
                        help="Max threads to process per run.")
    parser.add_argument("--backlog-days", type=int, default=DEFAULT_BACKLOG_DAYS,
                        help="Only process threads older than this many days.")
    parser.add_argument("--before-date", type=str, default=None,
                        help="Hard cutoff date (YYYY-MM-DD). Only process threads "
                             "older than this date. Overrides --backlog-days.")
    parser.add_argument("--recent-reply-days", type=int, default=14,
                        help="Deprecated — any reply now protects a thread regardless of age.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Phase 1 always forces dry-run
    dry_run = args.dry_run or (args.phase == 1)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    if SKILL_DOC.exists():
        logging.info(f"Skill: {SKILL_DOC}")
    else:
        logging.warning(f"Skill doc not found: {SKILL_DOC}")

    run_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6]
    logging.info(f"run_id={run_id} phase={args.phase} dry_run={dry_run} "
                 f"max_threads={args.max_threads} backlog_days={args.backlog_days}")

    service = get_gmail_service()

    # Build query
    if args.before_date:
        from datetime import date as _date
        cutoff = datetime(
            *[int(x) for x in args.before_date.split("-")], tzinfo=timezone.utc
        )
        logging.info(f"before_date={args.before_date} (overrides --backlog-days)")
    else:
        cutoff = datetime.now(timezone.utc) - timedelta(days=args.backlog_days)
    cutoff_epoch = int(cutoff.timestamp())
    query = f"in:inbox before:{cutoff_epoch} ({SCOPE_QUERY_CATEGORIES})"
    logging.info(f"query: {query}")

    # Fetch thread list
    thread_ids: List[str] = []
    page_token: Optional[str] = None
    while len(thread_ids) < args.max_threads:
        batch_size = min(500, args.max_threads - len(thread_ids))
        kwargs: Dict[str, Any] = {"userId": "me", "q": query, "maxResults": batch_size}
        if page_token:
            kwargs["pageToken"] = page_token
        resp = service.users().threads().list(**kwargs).execute()
        for item in resp.get("threads", []):
            if item.get("id"):
                thread_ids.append(item["id"])
        page_token = resp.get("nextPageToken")
        if not page_token or len(thread_ids) >= args.max_threads:
            break

    logging.info(f"threads_fetched={len(thread_ids)}")

    stats = {"total": 0, "archived": 0, "skipped_protected": 0, "skipped_uncertain": 0, "errors": 0}

    for thread_id in thread_ids:
        stats["total"] += 1
        try:
            thread = service.users().threads().get(
                userId="me", id=thread_id, format="metadata",
                metadataHeaders=["From", "Subject", "List-ID", "List-Unsubscribe", "Precedence"],
            ).execute()
        except Exception as exc:
            logging.warning(f"get thread {thread_id} failed: {exc}")
            stats["errors"] += 1
            continue

        messages = thread.get("messages", [])
        if not messages:
            continue

        # Use first message for headers, last for recency check
        first_msg = messages[0]
        last_msg = messages[-1]

        headers = first_msg.get("payload", {}).get("headers", [])
        sender = get_header(headers, "From")
        subject = get_header(headers, "Subject")
        snippet = first_msg.get("snippet", "")
        thread_labels = thread.get("messages", [{}])[0].get("labelIds", [])
        is_starred = "STARRED" in thread_labels

        # Protect if ML1 has ever replied (any SENT message in thread)
        has_recent_reply = any("SENT" in msg.get("labelIds", []) for msg in messages)

        # Step 1: Protected check
        protected, protect_reason = is_protected(
            thread_labels, is_starred, has_recent_reply, sender, subject
        )
        if protected:
            stats["skipped_protected"] += 1
            append_log(run_id, {
                "run_id": run_id, "thread_id": thread_id, "action": "skip",
                "reason": f"protected:{protect_reason}", "ts": now_iso(),
            })
            continue

        # Step 2: Deterministic rules
        should_archive, archive_reason = deterministic_archive_check(
            sender, thread_labels, headers, snippet, args.phase
        )

        if should_archive:
            success = archive_thread(service, thread_id, dry_run)
            action = "archive" if success else "archive_failed"
            if success:
                stats["archived"] += 1
            else:
                stats["errors"] += 1
            append_log(run_id, {
                "run_id": run_id, "thread_id": thread_id, "action": action,
                "reason": archive_reason, "dry_run": dry_run, "ts": now_iso(),
            })
        else:
            # Step 3: Ambiguity gate — default KEEP (classifier not yet wired)
            stats["skipped_uncertain"] += 1
            append_log(run_id, {
                "run_id": run_id, "thread_id": thread_id, "action": "keep",
                "reason": "ambiguity_gate:uncertain→keep", "ts": now_iso(),
            })

        time.sleep(0.05)  # gentle rate limit

    # Summary
    summary = {
        "run_id": run_id,
        "agent_version": AGENT_VERSION,
        "phase": args.phase,
        "dry_run": dry_run,
        "backlog_days": args.backlog_days,
        "max_threads": args.max_threads,
        "stats": stats,
        "ts": now_iso(),
    }
    summary_path = AUDIT_DIR / f"run_{run_id}_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False))

    logging.info(
        f"DONE run_id={run_id} total={stats['total']} archived={stats['archived']} "
        f"skipped_protected={stats['skipped_protected']} uncertain={stats['skipped_uncertain']} "
        f"errors={stats['errors']}"
    )


if __name__ == "__main__":
    main()
