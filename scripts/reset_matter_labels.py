#!/usr/bin/env python3
"""
reset_matter_labels.py — Full reset of LL/1. matter label hierarchy.

Problem: old-format parent labels (LL/1./1.1 - Essential, etc.) caused new
labels to nest incorrectly. This script:
  1. Deletes all LL/1. labels NOT in the canonical set
  2. Creates any canonical labels that are missing

Canonical labels live at: LL/1./{tier}/{matter_id} -- {name}

Usage:
  python3 scripts/reset_matter_labels.py           # dry run
  python3 scripts/reset_matter_labels.py --execute
"""

import argparse
import os
import time
from pathlib import Path
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent

CANONICAL_LABELS = [
    # Parents
    "LL/1.",
    "LL/1./1.1",
    "LL/1./1.2",
    "LL/1./1.3",
    "LL/1./1.4",
    # 1.1 Essential
    "LL/1./1.1/25-927-00003 -- Stream Ventures Limited",
    "LL/1./1.1/26-1639-00001 -- Andersen",
    "LL/1./1.1/26-1639-00002 -- Andersen",
    "LL/1./1.1/26-1639-00003 -- Andersen",
    "LL/1./1.1/26-927-00004 -- Stream Ventures Limited",
    # 1.2 Strategic
    "LL/1./1.2/24-336-00004 -- Mascore Helical Piles",
    "LL/1./1.2/25-1231-00001 -- Charmaine Spiteri",
    "LL/1./1.2/25-1318-00001 -- Zelko Culibrk",
    "LL/1./1.2/25-256-00005 -- Aspire Infusions Inc",
    "LL/1./1.2/26-1593-00002 -- KaleMart",
    # 1.3 Standard
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
    # 1.4 Parked
    "LL/1./1.4/23-169-00003 -- Best Bottles Inc.",
    "LL/1./1.4/24-347-00002 -- Brand Butter",
    "LL/1./1.4/24-409-00001 -- A. Mukherjee & Co.",
    "LL/1./1.4/24-601-00001 -- Meta Bytes North America Inc",
    "LL/1./1.4/24-682-00002 -- Stream Ventures Limited",
    "LL/1./1.4/25-1024-00001 -- AllPro Construction Group",
    "LL/1./1.4/25-1192-00001 -- The Knot Churros International Limited",
    "LL/1./1.4/25-174-00001 -- Danielle Thompson",
    "LL/1./1.4/25-192-00003 -- If Not Me Inc",
    "LL/1./1.4/25-822-00001 -- Majid Hajibeigy",
    "LL/1./1.4/26-1630-00001 -- Marcela Hernandez",
]

CANONICAL_SET = set(CANONICAL_LABELS)


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


def run(dry_run: bool):
    service = build_service()
    all_labels = service.users().labels().list(userId="me").execute().get("labels", [])

    label_map = {l["name"]: l["id"] for l in all_labels}

    # All LL/1. labels currently in Gmail
    ll1_labels = {name: lid for name, lid in label_map.items() if name.startswith("LL/1.")}

    to_delete = {name: lid for name, lid in ll1_labels.items() if name not in CANONICAL_SET}
    to_create = [name for name in CANONICAL_LABELS if name not in ll1_labels]
    already_correct = [name for name in CANONICAL_LABELS if name in ll1_labels]

    print(f"Current LL/1. labels in Gmail: {len(ll1_labels)}")
    print(f"Canonical target:              {len(CANONICAL_LABELS)}")
    print(f"Already correct:               {len(already_correct)}")
    print(f"To DELETE (stale/wrong):       {len(to_delete)}")
    print(f"To CREATE (missing):           {len(to_create)}")
    print()

    if to_delete:
        print(f"{'[DRY RUN] Would delete' if dry_run else 'DELETING'} ({len(to_delete)}):")
        # Delete leaf labels first (children before parents)
        sorted_deletes = sorted(to_delete.keys(), key=lambda x: -x.count("/"))
        for name in sorted_deletes:
            if dry_run:
                print(f"  🗑  {name}")
            else:
                try:
                    service.users().labels().delete(userId="me", id=to_delete[name]).execute()
                    print(f"  🗑  {name}")
                    time.sleep(0.1)
                except Exception as e:
                    print(f"  ❌ {name}  ERROR: {e}")
        print()

    if to_create:
        print(f"{'[DRY RUN] Would create' if dry_run else 'CREATING'} ({len(to_create)}):")
        # Create parents before children
        sorted_creates = sorted(to_create, key=lambda x: x.count("/"))
        for name in sorted_creates:
            if dry_run:
                print(f"  ➕ {name}")
            else:
                try:
                    service.users().labels().create(
                        userId="me", body={"name": name}
                    ).execute()
                    print(f"  ✅ {name}")
                    time.sleep(0.15)
                except Exception as e:
                    print(f"  ❌ {name}  ERROR: {e}")
        print()

    if dry_run:
        print("Re-run with --execute to apply.")
    else:
        print("Done. Verifying final state...")
        final = {
            l["name"]
            for l in service.users().labels().list(userId="me").execute().get("labels", [])
            if l["name"].startswith("LL/1.")
        }
        missing = [l for l in CANONICAL_LABELS if l not in final]
        unexpected = [l for l in final if l not in CANONICAL_SET]
        print(f"  Canonical labels present: {len(CANONICAL_LABELS) - len(missing)}/{len(CANONICAL_LABELS)}")
        if missing:
            print(f"  Still missing: {missing}")
        if unexpected:
            print(f"  Unexpected remaining: {unexpected}")
        if not missing and not unexpected:
            print("  ✅ Label hierarchy is clean.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    run(dry_run=not args.execute)
