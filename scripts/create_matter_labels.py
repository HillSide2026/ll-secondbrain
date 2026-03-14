#!/usr/bin/env python3
"""
create_matter_labels.py — Create canonical Gmail matter labels for governed matters.

Canonical format: LL/1./{tier}/{matter_id} -- {client_name}
  Tier 1.1 = Essential
  Tier 1.2 = Strategic
  Tier 1.3 = Standard
  Tier 1.4 = Parked

Usage:
  python3 scripts/create_matter_labels.py           # dry run
  python3 scripts/create_matter_labels.py --execute # create labels
"""

import argparse
import os
from pathlib import Path
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent

CANONICAL_LABELS = [
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

    existing = {
        l["name"]
        for l in service.users().labels().list(userId="me").execute().get("labels", [])
    }

    to_create = [l for l in CANONICAL_LABELS if l not in existing]
    already_exist = [l for l in CANONICAL_LABELS if l in existing]

    print(f"Total canonical labels: {len(CANONICAL_LABELS)}")
    print(f"Already exist:          {len(already_exist)}")
    print(f"To create:              {len(to_create)}")
    print()

    if already_exist:
        print("Already exist (no action):")
        for l in already_exist:
            print(f"  ✅ {l}")
        print()

    if not to_create:
        print("Nothing to create.")
        return

    print(f"{'[DRY RUN] Would create' if dry_run else 'Creating'}:")
    for label_name in to_create:
        if dry_run:
            print(f"  ➕ {label_name}")
        else:
            try:
                service.users().labels().create(
                    userId="me",
                    body={"name": label_name},
                ).execute()
                print(f"  ✅ {label_name}")
            except Exception as e:
                print(f"  ❌ {label_name}  ERROR: {e}")

    if dry_run:
        print("\nRe-run with --execute to create.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    run(dry_run=not args.execute)
