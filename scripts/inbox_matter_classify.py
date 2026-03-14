#!/usr/bin/env python3
"""
inbox_matter_classify.py — Classify inbox threads by matter per PRO-014.

Scans threads in inbox that have no canonical state label.
For each thread:
  - Extracts matter ID from subject or snippet
  - Resolves to canonical matter label (LL/1./{tier}/{id} -- {name})
  - Assigns state label per PRO-014 §5.1 decision tree
  - ADD-ONLY: never removes existing labels

Does NOT create labels, archive, or delete.

Usage:
  python3 scripts/inbox_matter_classify.py           # dry run (counts + proposals)
  python3 scripts/inbox_matter_classify.py --execute
"""

import argparse
import os
import re
import time
from pathlib import Path
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Canonical matter labels (matter_id → full label name)
# ---------------------------------------------------------------------------

_MATTER_LABELS_RAW = [
    "LL/1./1.1/25-927-00003 -- Stream Ventures Limited",
    "LL/1./1.1/26-1639-00001 -- Andersen",
    "LL/1./1.1/26-1639-00002 -- Andersen",
    "LL/1./1.1/26-1639-00003 -- Andersen",
    "LL/1./1.1/26-927-00004 -- Stream Ventures Limited",
    "LL/1./1.2/24-336-00004 -- Mascore Helical Piles",
    "LL/1./1.2/25-1231-00001 -- Charmaine Spiteri",
    "LL/1./1.2/25-1318-00001 -- Zelko Culibrk",
    "LL/1./1.2/25-256-00005 -- Aspire Infusions Inc",
    "LL/1./1.2/26-1593-00002 -- KaleMart",
    "LL/1./1.3/22-194-00006 -- Rousseau Mazzuca LLP",
    "LL/1./1.3/23-194-00013 -- Rousseau Mazzuca LLP",
    "LL/1./1.3/23-235-00001 -- Baobab Energy Africa Ltd",
    "LL/1./1.3/24-646-00001 -- ByNature Design",
    "LL/1./1.3/25-1185-00001 -- Alexander Klys",
    "LL/1./1.3/25-1363-00001 -- Raevan Joy Sambrano",
    "LL/1./1.3/25-1525-00001 -- Kleenup Cleaning Services Inc.",
    "LL/1./1.3/25-1538-00002 -- Georgiana Nicoară",
    "LL/1./1.3/25-1553-00001 -- 15652227 Canada Inc.",
    "LL/1./1.3/25-1571-00001 -- Kishmish Inc.",
    "LL/1./1.3/25-1588-00001 -- Gregory Popov",
    "LL/1./1.3/25-1593-00001 -- KaleMart",
    "LL/1./1.3/25-1603-00001 -- IBERBANCO LTD",
    "LL/1./1.3/25-1614-00001 -- HillSide",
    "LL/1./1.3/25-194-00059 -- Rousseau Mazzuca LLP",
    "LL/1./1.3/25-845-00001 -- STAR 333 SPORTS INC.",
    "LL/1./1.3/25-845-00002 -- STAR 333 SPORTS INC.",
    "LL/1./1.3/26-259-00003 -- LL Onboarding",
]

# matter_id → full label name
MATTER_ID_TO_LABEL = {}
for _lbl in _MATTER_LABELS_RAW:
    _leaf = _lbl.split("/")[-1]                  # "25-927-00003 -- Stream Ventures Limited"
    _mid = _leaf.split(" --")[0].strip()          # "25-927-00003"
    MATTER_ID_TO_LABEL[_mid] = _lbl

# Also index base IDs (without sub-matter suffix) for partial matching
MATTER_BASE_TO_LABEL = {}
for _mid, _lbl in MATTER_ID_TO_LABEL.items():
    _base = "-".join(_mid.split("-")[:2])         # "25-927" from "25-927-00003"
    if _base not in MATTER_BASE_TO_LABEL:
        MATTER_BASE_TO_LABEL[_base] = []
    MATTER_BASE_TO_LABEL[_base].append(_mid)

# Canonical state labels
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

MATTER_TIER_PREFIXES = ("LL/1./1.1/", "LL/1./1.2/", "LL/1./1.3/", "LL/1./1.4/")

# Sender signals
MATTHEW_EMAILS = {"matthew@levinelegal.ca", "matthew@levine-law.ca"}
AUTOMATED_SIGNALS = ("noreply", "no-reply", "donotreply", "do_not_reply",
                     "notifications@", "automated@", "system@")
CALENDAR_SENDER = "calendar-notification@google.com"

# Matter ID extraction
SUB_MATTER_RE = re.compile(r"\b(\d{2,3}-\d{3,4}-\d{5})\b")
BASE_MATTER_RE = re.compile(r"\b(\d{2,3}-\d{3,4})\b")


def build_service():
    load_dotenv(REPO_ROOT / ".env")
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    creds = Credentials(
        token=None,
        refresh_token=os.getenv("GMAIL_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GMAIL_CLIENT_ID"),
        client_secret=os.getenv("GMAIL_CLIENT_SECRET"),
        scopes=["https://www.googleapis.com/auth/gmail.modify"],
    )
    return build("gmail", "v1", credentials=creds)


def is_automated(sender: str) -> bool:
    s = sender.lower()
    return any(sig in s for sig in AUTOMATED_SIGNALS)


def extract_matter_id(text: str):
    """Return (matter_id, canonical_label) or (None, None). Sub-matter preferred."""
    # Sub-matter match (e.g. 25-927-00003)
    for m in SUB_MATTER_RE.findall(text):
        if m in MATTER_ID_TO_LABEL:
            return m, MATTER_ID_TO_LABEL[m]
    # Base match (e.g. 25-927) → only if exactly one sub-matter maps to it
    for m in BASE_MATTER_RE.findall(text):
        candidates = MATTER_BASE_TO_LABEL.get(m, [])
        if len(candidates) == 1:
            mid = candidates[0]
            return mid, MATTER_ID_TO_LABEL[mid]
    return None, None


def classify_state(sender: str, last_sender: str, msg_count: int,
                   current_label_names: list, has_matter: bool) -> str:
    """PRO-014 §5.1 decision tree (10 steps)."""
    s_low = sender.lower()

    # 1. Calendar
    if CALENDAR_SENDER in s_low:
        return "50_Calendar"

    # 2-3. Matter label
    if has_matter:
        return "60_Filing" if is_automated(sender) else "10_Action_Matthew"

    # 4. Team
    TEAM = {"levinelegalservices.com", "lino@levinelegal.ca", "grace@levinelegal.ca",
            "lino@levine-law.ca", "grace@levine-law.ca"}
    if any(t in s_low for t in TEAM):
        return "20_Action_Team"

    # 5. Admin vendor / subject keyword
    ADMIN = {"telus.com", "connect.telus.com", "soulpepper.com",
             "amazon.ca", "amazon.com", "regus.com"}
    if any(a in s_low for a in ADMIN):
        return "20_Action_Team"

    # 6. Promotional
    labels_low = [l.lower() for l in current_label_names]
    if "category_promotions" in labels_low:
        return "80_Junk (Pending Review)"

    # 7. ML1 replied last
    if last_sender and last_sender.lower() in MATTHEW_EMAILS and msg_count >= 2:
        return "40_Replied_Awaiting_Response"

    # 8. Archive signals
    ARCHIVE_SIGS = ("you just signed", "order confirmation", "your order", "signed by all signers")

    # 9. Legal senders
    LEGAL = {"cra-arc.gc.ca", "hamlins.com", "clio.com", "mail.hellosign.com",
              "dropbox.com", "cassels.com", "rousseaumazzuca.com", "docuseal.com",
              "cestlavielaw.ca", "asana.com"}
    if any(l in s_low for l in LEGAL):
        return "10_Action_Matthew"

    # 10. Default
    return "00_Triage"


def get_header(headers, name):
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""


def run(dry_run: bool):
    service = build_service()

    # Build label name → ID map
    all_labels = service.users().labels().list(userId="me").execute().get("labels", [])
    name_to_id = {l["name"]: l["id"] for l in all_labels}
    id_to_name = {l["id"]: l["name"] for l in all_labels}

    # Verify all canonical labels exist in Gmail
    missing_labels = [l for l in _MATTER_LABELS_RAW if l not in name_to_id]
    if missing_labels:
        print(f"WARNING: {len(missing_labels)} canonical labels not found in Gmail:")
        for l in missing_labels:
            print(f"  ⚠️  {l}")
        print()

    # Exclude query: no canonical state label applied
    exclude_q = " ".join(f'-label:"{lbl}"' for lbl in CANONICAL_STATE_LABELS)

    proposals = []
    seen_thread_ids = set()

    # Search per matter ID — 28 targeted searches instead of scanning all 40k+ threads
    print(f"Searching inbox for {len(MATTER_ID_TO_LABEL)} matters...\n")

    for matter_id, matter_label in sorted(MATTER_ID_TO_LABEL.items()):
        query = f'in:inbox "{matter_id}" {exclude_q}'
        threads = []
        page_token = None
        while True:
            kwargs = {"userId": "me", "q": query, "maxResults": 500}
            if page_token:
                kwargs["pageToken"] = page_token
            resp = service.users().threads().list(**kwargs).execute()
            threads.extend(resp.get("threads", []))
            page_token = resp.get("nextPageToken")
            if not page_token:
                break

        if not threads:
            continue

        print(f"  {matter_id}  →  {len(threads)} thread(s)")

        for t in threads:
            if t["id"] in seen_thread_ids:
                continue
            seen_thread_ids.add(t["id"])

            thread = service.users().threads().get(
                userId="me", id=t["id"], format="metadata",
                metadataHeaders=["Subject", "From"]
            ).execute()

            messages = thread.get("messages", [])
            if not messages:
                continue

            first = messages[0]
            last = messages[-1]
            first_headers = first.get("payload", {}).get("headers", [])
            last_headers = last.get("payload", {}).get("headers", [])

            subject = get_header(first_headers, "Subject")
            sender = get_header(first_headers, "From")
            last_sender = get_header(last_headers, "From")

            all_lid = set()
            for msg in messages:
                all_lid.update(msg.get("labelIds", []))
            current_names = [id_to_name.get(lid, lid) for lid in all_lid if lid in id_to_name]

            already_has_matter = any(n.startswith(MATTER_TIER_PREFIXES) for n in current_names)

            # Determine what to add
            add_matter = None if already_has_matter else matter_label
            state = classify_state(sender, last_sender, len(messages), current_names, True)

            proposals.append({
                "thread_id": t["id"],
                "subject": subject[:80],
                "sender": sender[:60],
                "matter_id": matter_id,
                "matter_label": add_matter,
                "state_label": state,
                "existing_matter": (
                    next((n for n in current_names if n.startswith(MATTER_TIER_PREFIXES)), None)
                    if already_has_matter else None
                ),
            })

    print(f"\nTotal threads to classify: {len(proposals)}\n")

    if not proposals:
        print("Nothing to classify.")
        return

    # Group by matter for display
    by_matter = {}
    for p in proposals:
        key = p.get("existing_matter") or p.get("matter_label") or "unknown"
        by_matter.setdefault(key, []).append(p)

    print(f"{'[DRY RUN] Proposed' if dry_run else 'Applying'} classifications:\n")
    for matter_lbl, items in sorted(by_matter.items()):
        print(f"  {matter_lbl}  ({len(items)} thread{'s' if len(items) > 1 else ''})")
        for p in items[:3]:
            state_arrow = f"→ {p['state_label']}"
            print(f"    {state_arrow:35s}  {p['subject'][:60]}")
        if len(items) > 3:
            print(f"    ... and {len(items) - 3} more")
    print()

    if dry_run:
        print(f"Total: {len(proposals)} threads would be classified.")
        print("Re-run with --execute to apply.")
        return

    # Execute: add labels (no removes)
    ok = 0
    err = 0
    for p in proposals:
        add_ids = []

        # Add matter label if not already present
        if p["matter_label"] and p["matter_label"] in name_to_id:
            add_ids.append(name_to_id[p["matter_label"]])

        # Add state label
        if p["state_label"] in name_to_id:
            add_ids.append(name_to_id[p["state_label"]])

        if not add_ids:
            continue

        try:
            service.users().threads().modify(
                userId="me",
                id=p["thread_id"],
                body={"addLabelIds": add_ids},
            ).execute()
            ok += 1
            time.sleep(0.1)
        except Exception as e:
            print(f"  ❌ {p['thread_id']} — {e}")
            err += 1

    print(f"Done. Classified: {ok}  Errors: {err}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    run(dry_run=not args.execute)
