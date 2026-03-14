#!/usr/bin/env python3
"""
inbox_cleanup.py — Bulk inbox soft-junk cleanup by sender query.

Operations:
  TRASH   — adds TRASH label, removes INBOX (reversible from Trash for 30 days)
  ARCHIVE — removes INBOX label only (messages remain searchable)

Governed by PRO-018.

Usage:
  # Dry run (default — safe, prints counts only):
  python scripts/inbox_cleanup.py

  # Execute:
  python scripts/inbox_cleanup.py --execute

Audit log: 06_RUNS/logs/inbox_cleanup.log
"""

import argparse
import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = REPO_ROOT / "06_RUNS" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

AUDIT_LOG = LOG_DIR / "inbox_cleanup.log"
BATCH_SIZE = 1000  # Gmail batchModify limit

# ---------------------------------------------------------------------------
# Queries
# ---------------------------------------------------------------------------

TRASH_QUERIES = [
    "in:inbox from:support@systemsandteams.com before:2026/1/1",
    "in:inbox from:news@bizbuysell.com before:2026/1/1",
    "in:inbox from:(noreply@medium.com OR newsletters@medium.com OR hello@medium.com) before:2026/1/1",
    "in:inbox from:david.a@plantationsinternational.com",
    "in:inbox from:notifications@account.brilliant.org before:2026/1/1",
    "in:inbox from:bettiegram@backofficebetties.com before:2026/1/1",
    "in:inbox from:email@e.lucid.co before:2026/1/1",
    "in:inbox from:noreply@skool.com before:2026/1/1",
    "in:inbox from:iwoszapar@user.luma-mail.com before:2026/1/1",
    "in:inbox from:support@epicnetwork.com before:2026/1/1",
    "in:inbox from:info@vivaglobal.us before:2026/1/1",
    "in:inbox from:communications@riskintelligence.lseg.com before:2026/1/1",
    "in:inbox from:communications@bnaibrith.ca before:2026/1/1",
    "in:inbox from:sales@infowisesolutions.com before:2026/1/1",
    "in:inbox from:team@weargustin.com before:2026/1/1",
    "in:inbox from:Windows365@mails.microsoft.com before:2026/1/1",
    "in:inbox from:teamzoom@zoom.us before:2026/1/1",
    "in:inbox from:customer-success-advisor@zoom.us before:2026/1/1",
    "in:inbox from:noreply@youtube.com before:2026/1/1",
    "in:inbox from:no-reply@mail.instagram.com before:2026/1/1",
    "in:inbox from:TDSurvey@feedback-td.com before:2026/1/1",
]

ARCHIVE_QUERIES = [
    "in:inbox from:(messaging@promo.lexisnexis.ca OR experts@lawpay.info) before:2026/1/1",
    "in:inbox from:(info@ontario-commercial.com OR support@ontario-commercial.com) before:2026/1/1",
    "in:inbox from:marketing@getappara.ai before:2026/1/1",
    "in:inbox from:bruna@legalboards.com before:2026/1/1",
    "in:inbox from:inquiries-portagemaadvisory.ca@shared1.ccsend.com before:2026/1/1",
    "in:inbox from:dbaskin@baskinwealth.com before:2026/1/1",
    "in:inbox from:jprekaski@fbc.ca before:2026/1/1",
    "in:inbox from:(notifications-noreply@linkedin.com OR linkedin@e.linkedin.com OR messages-noreply@linkedin.com OR jobs-listings@linkedin.com) before:2026/1/1",
]

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(AUDIT_LOG),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("inbox_cleanup")

# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def build_service():
    """Build Gmail API service from .env credentials."""
    import os
    from dotenv import load_dotenv
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    load_dotenv(REPO_ROOT / ".env")

    client_id = os.getenv("GMAIL_CLIENT_ID")
    client_secret = os.getenv("GMAIL_CLIENT_SECRET")
    refresh_token = os.getenv("GMAIL_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        raise ValueError("Missing GMAIL_CLIENT_ID / GMAIL_CLIENT_SECRET / GMAIL_REFRESH_TOKEN in .env")

    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/gmail.modify"],
    )
    return build("gmail", "v1", credentials=creds)

# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def collect_message_ids(service, query: str) -> list[str]:
    """Paginate through all messages matching query. Returns list of message IDs."""
    ids = []
    page_token = None

    while True:
        kwargs = {"userId": "me", "q": query, "maxResults": 500}
        if page_token:
            kwargs["pageToken"] = page_token

        resp = service.users().messages().list(**kwargs).execute()
        batch = resp.get("messages", [])
        ids.extend(m["id"] for m in batch)

        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    return ids


def batch_modify(service, message_ids: list[str], add_labels: list[str], remove_labels: list[str], dry_run: bool):
    """Apply label changes in batches of BATCH_SIZE."""
    total = len(message_ids)
    if total == 0:
        return

    for i in range(0, total, BATCH_SIZE):
        chunk = message_ids[i : i + BATCH_SIZE]
        if dry_run:
            log.info(f"  [DRY RUN] Would modify {len(chunk)} messages "
                     f"(add={add_labels}, remove={remove_labels})")
        else:
            service.users().messages().batchModify(
                userId="me",
                body={
                    "ids": chunk,
                    "addLabelIds": add_labels,
                    "removeLabelIds": remove_labels,
                },
            ).execute()
            log.info(f"  Modified {len(chunk)} messages (add={add_labels}, remove={remove_labels})")
            time.sleep(0.5)  # stay well under Gmail rate limits

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(dry_run: bool):
    run_ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    mode = "DRY RUN" if dry_run else "EXECUTE"
    log.info(f"=== inbox_cleanup START | {run_ts} | mode={mode} ===")

    service = build_service()

    total_trashed = 0
    total_archived = 0

    # --- TRASH ---
    log.info(f"--- TRASH ({len(TRASH_QUERIES)} queries) ---")
    for query in TRASH_QUERIES:
        ids = collect_message_ids(service, query)
        log.info(f"  query: {query!r}  →  {len(ids)} messages")
        if ids:
            # Add TRASH, remove INBOX (same as clicking "Move to Trash")
            batch_modify(service, ids, add_labels=["TRASH"], remove_labels=["INBOX"], dry_run=dry_run)
            total_trashed += len(ids)

    # --- ARCHIVE ---
    log.info(f"--- ARCHIVE ({len(ARCHIVE_QUERIES)} queries) ---")
    for query in ARCHIVE_QUERIES:
        ids = collect_message_ids(service, query)
        log.info(f"  query: {query!r}  →  {len(ids)} messages")
        if ids:
            # Remove INBOX only — messages stay in All Mail
            batch_modify(service, ids, add_labels=[], remove_labels=["INBOX"], dry_run=dry_run)
            total_archived += len(ids)

    log.info(f"=== inbox_cleanup COMPLETE | trashed={total_trashed} | archived={total_archived} | mode={mode} ===")
    print(f"\nSummary: {total_trashed} to trash, {total_archived} to archive")
    if dry_run:
        print("Re-run with --execute to apply changes.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk Gmail inbox cleanup")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Apply changes. Without this flag, runs in dry-run mode (counts only).",
    )
    args = parser.parse_args()
    run(dry_run=not args.execute)
