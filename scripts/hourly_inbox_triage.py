#!/usr/bin/env python3
"""
Hourly Inbox Triage Agent
=========================
AI Agent Spec — Hourly Inbox Triage Agent (approved 2026-04-13)

Runs every hour during business hours (09:00–17:00, Mon–Fri) to:

  1. Fetch Gmail threads updated since the last run
  2. Classify each thread: Essential Matter, Strategic Matter, or Non-Priority
  3. For Essential/Strategic threads: apply 05_Priority_Essential or 06_Priority_Strategic
     and remove any competing canonical state labels
  4. For non-priority threads: apply exactly one canonical state label
     (remove all competing state labels)
  5. Log every decision to NDJSON run log

Priority naming follows LL delivery status taxonomy (not the spec's raw labels):
  - 05_Priority_Essential  = highest tier (spec called these "Strategic")
  - 06_Priority_Strategic  = second tier  (spec called these "Essential")

Authority: ML1 approval per Hourly Inbox Triage Agent spec (2026-04-13)
Policy: POL-042 Inbox Governance Policy
"""

import datetime
import json
import logging
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# ── Repo paths ─────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "gmail_governance"))

# ── Shared imports from gmail_governance ──────────────────────────────────────

from state_enforcement import get_gmail_service, CANONICAL_LABELS
from matter_enforcement import get_matter_labels, MATTER_TIER_PREFIXES
from batch_classifier import (
    resolve_thread_matter,
    classify_thread,
    get_matter_signal_confidence,
    is_matthew,
)

# ── Constants ──────────────────────────────────────────────────────────────────

AGENT_VERSION = "hourly-triage-v1.0"
APPROVAL_ARTIFACT = "AI Agent Spec — Hourly Inbox Triage Agent (2026-04-13)"
APPROVAL_BY = "ML1"

# Priority labels: names follow LL delivery status taxonomy
# Essential = highest tier; Strategic = second tier
PRIORITY_LABEL_ESSENTIAL = "05_Priority_Essential"
PRIORITY_LABEL_STRATEGIC = "06_Priority_Strategic"
ALL_PRIORITY_LABELS = {PRIORITY_LABEL_ESSENTIAL, PRIORITY_LABEL_STRATEGIC}

# Matter label tier prefix → priority classification
TIER_TO_PRIORITY: Dict[str, str] = {
    "LL/1./1.1/": "ESSENTIAL_MATTER",   # Essential delivery tier
    "LL/1./1.2/": "STRATEGIC_MATTER",   # Strategic delivery tier
    # 1.3 Standard and 1.4 Parked are NON_PRIORITY
}

PRIORITY_TO_LABEL: Dict[str, str] = {
    "ESSENTIAL_MATTER": PRIORITY_LABEL_ESSENTIAL,
    "STRATEGIC_MATTER": PRIORITY_LABEL_STRATEGIC,
}

# Confidence thresholds
CONFIDENCE_LOW = 0.65      # Below this → 00_Triage + needs_review=True
CONFIDENCE_AUTO = 0.75     # At or above this → auto-apply without review flag

# Time window: fetch threads with activity in the last N minutes
# 70 min ensures overlap between hourly runs with no gaps
LOOKBACK_MINUTES = 70

# File paths
STATE_DIR = REPO_ROOT / "06_RUNS" / "INBOX_TRIAGE" / "state"
LOG_DIR = REPO_ROOT / "06_RUNS" / "INBOX_TRIAGE" / "logs"
STATE_FILE = STATE_DIR / "last_run.json"
RUN_LOG_FILE = LOG_DIR / "hourly_triage_run.ndjson"


# ── Gmail label utilities ──────────────────────────────────────────────────────

def get_full_label_map(service) -> Dict[str, str]:
    """Return full label name → label ID map for the Gmail account."""
    results = service.users().labels().list(userId="me").execute()
    return {lbl["name"]: lbl["id"] for lbl in results.get("labels", [])}


def ensure_priority_labels_exist(service, label_map: Dict[str, str]) -> Dict[str, str]:
    """Create 05_Priority_Essential and 06_Priority_Strategic in Gmail if absent."""
    for label_name in ALL_PRIORITY_LABELS:
        if label_name not in label_map:
            created = service.users().labels().create(
                userId="me",
                body={
                    "name": label_name,
                    "labelListVisibility": "labelShow",
                    "messageListVisibility": "show",
                },
            ).execute()
            label_map[label_name] = created["id"]
            logging.info(f"Created Gmail label: {label_name} (id={created['id']})")
    return label_map


# ── Thread fetching ────────────────────────────────────────────────────────────

def fetch_updated_threads(service, last_run_epoch: Optional[int]) -> List[Dict]:
    """
    Return thread stubs for all threads that received a new message since
    last_run_epoch. Falls back to LOOKBACK_MINUTES window if no prior run.
    """
    after_ts = last_run_epoch if last_run_epoch else int(time.time()) - (LOOKBACK_MINUTES * 60)
    query = f"after:{after_ts}"

    threads, page_token = [], None
    while True:
        params: Dict[str, Any] = {"userId": "me", "q": query, "maxResults": 100}
        if page_token:
            params["pageToken"] = page_token
        resp = service.users().threads().list(**params).execute()
        threads.extend(resp.get("threads", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return threads


def fetch_thread_detail(
    service, thread_id: str, label_id_to_name: Dict[str, str]
) -> Optional[Dict[str, Any]]:
    """
    Fetch thread metadata needed for classification:
    subject, sender, last_sender, snippet, current_labels, message_count.
    """
    thread = service.users().threads().get(
        userId="me",
        id=thread_id,
        format="metadata",
        metadataHeaders=["Subject", "From"],
    ).execute()

    messages = thread.get("messages", [])
    if not messages:
        return None

    first_msg = messages[0]
    last_msg = messages[-1]

    def hdr(msg, name):
        for h in msg.get("payload", {}).get("headers", []):
            if h["name"] == name:
                return h["value"]
        return ""

    # Collect all label IDs from every message in the thread
    all_label_ids: set = set()
    for msg in messages:
        all_label_ids.update(msg.get("labelIds", []))

    current_labels = [
        label_id_to_name[lid] for lid in all_label_ids if lid in label_id_to_name
    ]

    return {
        "thread_id": thread_id,
        "subject": hdr(first_msg, "Subject") or "(No Subject)",
        "sender": hdr(first_msg, "From") or "(Unknown)",
        "last_sender": hdr(last_msg, "From"),
        "snippet": first_msg.get("snippet", "")[:300],
        "current_labels": current_labels,
        "all_label_ids": all_label_ids,
        "message_count": len(messages),
        "is_unread": "UNREAD" in all_label_ids,
        "latest_message_at": last_msg.get("internalDate", ""),
    }


# ── Priority classification ────────────────────────────────────────────────────

def classify_priority(
    thread_detail: Dict[str, Any],
    matter_labels: Dict,
) -> Tuple[str, Optional[str], Optional[str], float]:
    """
    Determine whether a thread belongs to an Essential Matter, Strategic Matter,
    or is Non-Priority.

    Returns:
        (priority, priority_label_name, matter_number, confidence)
          priority:            'ESSENTIAL_MATTER' | 'STRATEGIC_MATTER' | 'NON_PRIORITY'
          priority_label_name: '05_Priority_Essential' | '06_Priority_Strategic' | None
          matter_number:       matched Clio matter ID or None
          confidence:          float 0.0–1.0
    """
    matter = resolve_thread_matter(
        subject=thread_detail["subject"],
        sender=thread_detail["sender"],
        snippet=thread_detail["snippet"],
        current_labels=thread_detail["current_labels"],
        matter_labels=matter_labels,
    )

    if matter["status"] != "matched":
        return "NON_PRIORITY", None, None, 0.90

    proposed_label = matter.get("proposed_label") or ""
    matter_number = matter.get("matter_number")
    signal = matter.get("signal", "")

    signal_confidence_map = {
        "determinative": 0.99,
        "high": 0.90,
        "medium": 0.75,
        "none": 0.50,
    }
    confidence = signal_confidence_map.get(get_matter_signal_confidence(signal), 0.70)

    for tier_prefix, priority_key in TIER_TO_PRIORITY.items():
        if proposed_label.startswith(tier_prefix):
            return priority_key, PRIORITY_TO_LABEL[priority_key], matter_number, confidence

    # Matched Standard or Parked tier → non-priority (but note the matter number)
    return "NON_PRIORITY", None, matter_number, 0.85


# ── Label application ──────────────────────────────────────────────────────────

def _thread_modify(service, thread_id: str, add_ids: List[str], remove_ids: List[str]):
    """Apply a single Gmail threads.modify call."""
    service.users().threads().modify(
        userId="me",
        id=thread_id,
        body={"addLabelIds": add_ids, "removeLabelIds": remove_ids},
    ).execute()


def apply_priority_label(
    service,
    thread_id: str,
    priority_label_name: str,
    label_map: Dict[str, str],
    current_label_ids: set,
) -> bool:
    """
    Apply priority label; remove any canonical state labels from the thread.
    Priority threads should not carry ordinary state labels.
    """
    target_id = label_map.get(priority_label_name)
    if not target_id:
        logging.error(f"Priority label '{priority_label_name}' missing from label_map")
        return False

    canonical_ids = {label_map[n] for n in CANONICAL_LABELS if n in label_map}
    remove_ids = list(current_label_ids & canonical_ids)

    # Idempotent: already has this priority label and nothing to remove
    if target_id in current_label_ids and not remove_ids:
        return True

    _thread_modify(service, thread_id, add_ids=[target_id], remove_ids=remove_ids)
    return True


def apply_state_label_to_thread(
    service,
    thread_id: str,
    state_label_name: str,
    label_map: Dict[str, str],
    current_label_ids: set,
) -> bool:
    """
    Apply exactly one canonical state label; remove all competing state labels.
    """
    if state_label_name not in CANONICAL_LABELS:
        logging.error(f"'{state_label_name}' is not a canonical state label")
        return False

    target_id = label_map.get(state_label_name)
    if not target_id:
        logging.error(f"State label '{state_label_name}' not found in Gmail")
        return False

    canonical_ids = {label_map[n] for n in CANONICAL_LABELS if n in label_map}
    remove_ids = list((current_label_ids & canonical_ids) - {target_id})

    if target_id in current_label_ids and not remove_ids:
        return True  # Already correct

    _thread_modify(service, thread_id, add_ids=[target_id], remove_ids=remove_ids)
    return True


# ── Logging ────────────────────────────────────────────────────────────────────

def write_log_entry(entry: Dict[str, Any]):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(RUN_LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def build_thread_log(
    run_id: str,
    thread_detail: Dict[str, Any],
    priority: str,
    priority_label: Optional[str],
    state_label: Optional[str],
    matter_number: Optional[str],
    confidence: float,
    action_taken: str,
    reason: str,
    needs_review: bool,
) -> Dict[str, Any]:
    return {
        "run_id": run_id,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "agent_version": AGENT_VERSION,
        "thread_id": thread_detail["thread_id"],
        "subject": thread_detail["subject"][:120],
        "sender": thread_detail["sender"][:80],
        "latest_message_at": thread_detail.get("latest_message_at"),
        "is_unread": thread_detail.get("is_unread", False),
        "existing_labels": thread_detail["current_labels"],
        "priority_classification": priority.lower(),
        "priority_label": priority_label,
        "state_label": state_label,
        "matter_number": matter_number,
        "confidence": round(confidence, 3),
        "reason_summary": reason,
        "action_taken": action_taken,
        "needs_review": needs_review,
        "approval_artifact": APPROVAL_ARTIFACT,
        "approved_by": APPROVAL_BY,
    }


# ── Run state ──────────────────────────────────────────────────────────────────

def load_run_state() -> Dict[str, Any]:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


def save_run_state(run_id: str, thread_count: int):
    state = {
        "last_run_id": run_id,
        "last_run_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "last_run_epoch": int(time.time()),
        "threads_processed": thread_count,
    }
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    run_id = datetime.datetime.now(datetime.timezone.utc).strftime("triage-%Y%m%d-%H%M%S")
    run_start = datetime.datetime.now(datetime.timezone.utc)

    logging.info(f"=== Hourly Inbox Triage | Run: {run_id} ===")
    logging.info(f"Approval: {APPROVAL_BY} / {APPROVAL_ARTIFACT}")

    prior_state = load_run_state()
    last_run_epoch = prior_state.get("last_run_epoch")

    service = get_gmail_service()
    label_map = get_full_label_map(service)
    label_map = ensure_priority_labels_exist(service, label_map)
    label_id_to_name = {v: k for k, v in label_map.items()}

    matter_labels = get_matter_labels(service)
    raw_threads = fetch_updated_threads(service, last_run_epoch)

    logging.info(f"Fetched {len(raw_threads)} threads since last run")

    stats = {
        "total": len(raw_threads),
        "essential_matter": 0,
        "strategic_matter": 0,
        "non_priority": 0,
        "low_confidence": 0,
        "errors": 0,
        "skipped": 0,
        "by_state": {lbl: 0 for lbl in CANONICAL_LABELS},
    }

    for thread_stub in raw_threads:
        thread_id = thread_stub["id"]
        try:
            detail = fetch_thread_detail(service, thread_id, label_id_to_name)
            if not detail:
                stats["skipped"] += 1
                continue

            current_label_ids: set = detail["all_label_ids"]

            # ── Step 1: Priority classification ──────────────────────────────
            priority, priority_label_name, matter_number, confidence = classify_priority(
                detail, matter_labels
            )

            needs_review = confidence < CONFIDENCE_AUTO
            if confidence < CONFIDENCE_LOW:
                stats["low_confidence"] += 1

            state_label: Optional[str] = None

            if priority in ("ESSENTIAL_MATTER", "STRATEGIC_MATTER"):
                # ── Priority path ─────────────────────────────────────────────
                apply_priority_label(
                    service, thread_id, priority_label_name, label_map, current_label_ids
                )

                if priority == "ESSENTIAL_MATTER":
                    stats["essential_matter"] += 1
                else:
                    stats["strategic_matter"] += 1

                action = f"apply_priority:{priority_label_name}"
                reason = f"Matter {matter_number} — {priority.lower().replace('_', ' ')}"

            else:
                # ── Non-priority path ─────────────────────────────────────────
                stats["non_priority"] += 1

                raw_state = classify_thread(
                    subject=detail["subject"],
                    sender=detail["sender"],
                    snippet=detail["snippet"],
                    current_labels=detail["current_labels"],
                    last_sender=detail["last_sender"],
                    message_count=detail["message_count"],
                    has_matter_association=False,
                )

                # Low confidence → 00_Triage regardless of classifier output
                state_label = "00_Triage" if confidence < CONFIDENCE_LOW else raw_state
                reason = f"Non-priority → {state_label}"
                if confidence < CONFIDENCE_LOW:
                    reason += " [low confidence → triage]"

                apply_state_label_to_thread(
                    service, thread_id, state_label, label_map, current_label_ids
                )
                stats["by_state"][state_label] += 1
                priority_label_name = None
                action = f"apply_state:{state_label}"

            log_entry = build_thread_log(
                run_id=run_id,
                thread_detail=detail,
                priority=priority,
                priority_label=priority_label_name,
                state_label=state_label,
                matter_number=matter_number,
                confidence=confidence,
                action_taken=action,
                reason=reason,
                needs_review=needs_review,
            )
            write_log_entry(log_entry)

        except Exception as exc:
            stats["errors"] += 1
            logging.error(f"Thread {thread_id}: {exc}")
            write_log_entry({
                "run_id": run_id,
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "thread_id": thread_id,
                "error": str(exc),
                "action_taken": "error",
            })

    save_run_state(run_id, len(raw_threads))

    duration = (datetime.datetime.now(datetime.timezone.utc) - run_start).total_seconds()

    # ── Run summary ───────────────────────────────────────────────────────────
    print(f"\n{'='*56}")
    print(f"  Hourly Inbox Triage  |  {run_id}")
    print(f"{'='*56}")
    print(f"  Duration:        {duration:.1f}s")
    print(f"  Threads total:   {stats['total']}")
    print(f"  Essential:       {stats['essential_matter']}")
    print(f"  Strategic:       {stats['strategic_matter']}")
    print(f"  Non-priority:    {stats['non_priority']}")
    print(f"  Low confidence:  {stats['low_confidence']}")
    print(f"  Errors:          {stats['errors']}")
    print(f"  Skipped:         {stats['skipped']}")
    active_states = {k: v for k, v in stats["by_state"].items() if v > 0}
    if active_states:
        print(f"\n  State label breakdown:")
        for lbl, count in sorted(active_states.items()):
            print(f"    {lbl}: {count}")
    print(f"\n  Log:   {RUN_LOG_FILE}")
    print(f"  State: {STATE_FILE}")
    print(f"{'='*56}\n")


if __name__ == "__main__":
    main()
