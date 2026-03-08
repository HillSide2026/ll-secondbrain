#!/usr/bin/env python3
"""
Scan SENT folder for all emails to roop.christopher@gmail.com in 2026.
Output: unique dates where a reply was sent.
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

load_dotenv(Path(__file__).resolve().parents[2] / '.env')

SCOPES = os.getenv('GOOGLE_SCOPES', '').split()

def build_service():
    creds = Credentials(
        token=None,
        refresh_token=os.getenv('GMAIL_REFRESH_TOKEN'),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv('GMAIL_CLIENT_ID'),
        client_secret=os.getenv('GMAIL_CLIENT_SECRET'),
        # Do not pass scopes — avoids invalid_scope on refresh
    )
    return build('gmail', 'v1', credentials=creds)

def get_header(headers, name):
    for h in headers:
        if h['name'].lower() == name.lower():
            return h['value']
    return None

def scan_roop_replies():
    service = build_service()

    # Search sent mail to Chris Roop in 2026
    query = "to:roop.christopher@gmail.com in:sent after:2025/12/31 before:2027/01/01"
    print(f"Query: {query}\n")

    # Paginate through all results
    all_messages = []
    page_token = None

    while True:
        kwargs = {
            'userId': 'me',
            'maxResults': 500,
            'q': query,
        }
        if page_token:
            kwargs['pageToken'] = page_token

        result = service.users().messages().list(**kwargs).execute()
        msgs = result.get('messages', [])
        all_messages.extend(msgs)
        print(f"  Fetched {len(msgs)} messages (total so far: {len(all_messages)})")

        page_token = result.get('nextPageToken')
        if not page_token:
            break

    print(f"\nTotal emails found: {len(all_messages)}\n")

    if not all_messages:
        print("No emails found to roop.christopher@gmail.com in 2026.")
        return

    # Collect dates
    dates_by_day = defaultdict(list)

    for i, msg in enumerate(all_messages):
        try:
            detail = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['Date', 'To', 'Subject']
            ).execute()

            headers = detail.get('payload', {}).get('headers', [])
            date_str = get_header(headers, 'Date')
            subject = get_header(headers, 'Subject') or '(no subject)'
            to = get_header(headers, 'To') or ''

            if date_str:
                date_str_clean = date_str.strip()
                # Remove timezone name in parens like "(EST)"
                date_str_clean = re.sub(r'\s*\([^)]*\)\s*$', '', date_str_clean)

                parsed = None
                for fmt in [
                    '%a, %d %b %Y %H:%M:%S %z',
                    '%d %b %Y %H:%M:%S %z',
                    '%a, %d %b %Y %H:%M:%S',
                    '%d %b %Y %H:%M:%S',
                ]:
                    try:
                        parsed = datetime.strptime(date_str_clean, fmt)
                        break
                    except ValueError:
                        continue

                if parsed:
                    day_key = parsed.strftime('%Y-%m-%d')
                    dates_by_day[day_key].append({
                        'subject': subject,
                        'to': to,
                        'time': parsed.strftime('%H:%M'),
                    })
                else:
                    print(f"  [WARN] Could not parse date: {date_str!r}")
        except Exception as e:
            print(f"  [ERROR] Message {msg['id']}: {e}")

        if (i + 1) % 20 == 0:
            print(f"  Processed {i+1}/{len(all_messages)} messages...")

    print("\n" + "="*60)
    print("DAYS IN 2026 WITH SENT EMAIL TO roop.christopher@gmail.com")
    print("="*60)

    if not dates_by_day:
        print("No dated emails found.")
        return

    sorted_days = sorted(dates_by_day.keys())
    for day in sorted_days:
        emails = dates_by_day[day]
        print(f"\n{day}  ({len(emails)} email{'s' if len(emails) > 1 else ''})")
        for e in emails:
            print(f"  {e['time']}  {e['subject'][:70]}")

    print(f"\n{'='*60}")
    print(f"TOTAL UNIQUE DAYS: {len(sorted_days)}")
    print(f"TOTAL EMAILS:      {sum(len(v) for v in dates_by_day.values())}")
    print("="*60)

if __name__ == '__main__':
    scan_roop_replies()
