"""
LL Inbox Governance - Phase 2B: Batch Classifier
Generates state and matter classification proposals for inbox threads (no execution).
"""

import json
from pathlib import Path
from state_enforcement import get_gmail_service, CANONICAL_LABELS
from matter_enforcement import (
    extract_matter_number,
    get_matter_labels,
    resolve_matter_label
)

# Matthew's known email addresses
MATTHEW_EMAILS = {
    'matthew@levinelegal.ca',
    'matthew@levine-law.ca',
}

# Team member identifiers → 20_Action_Team
TEAM_SENDERS = {
    'levinelegalservices.com',
    'lino@levinelegal.ca',
    'grace@levinelegal.ca',
    'lino@levine-law.ca',
    'grace@levine-law.ca',
}

# Known legal service providers → 10_Action_Matthew
LEGAL_SENDERS = {
    'cra-arc.gc.ca',
    'hamlins.com',
    'clio.com',
    'mail.hellosign.com',
    'dropbox.com',
    'cassels.com',
    'rousseaumazzuca.com',
    'docuseal.com',
    'cestlavielaw.ca',
    'asana.com',
}

# Known firm admin / vendor senders → 20_Action_Team
ADMIN_SENDERS = {
    'telus.com',
    'connect.telus.com',
    'soulpepper.com',
    'amazon.ca',
    'amazon.com',
    'regus.com',
}

# Sender signals indicating automated / system-generated email
AUTOMATED_SENDER_SIGNALS = [
    'noreply',
    'no-reply',
    'donotreply',
    'do_not_reply',
    'notifications@',
    'automated@',
    'system@',
]

# Subject keywords indicating firm admin → 20_Action_Team
ADMIN_SUBJECT_KEYWORDS = [
    'invoice',
    'billing',
    'statement of account',
    'social event',
    'printer',
    'office supply',
    'supplies',
    'get ready for your bill',
]

# Subject/snippet signals for completed automated actions → 90_Archive
ARCHIVE_SUBJECT_SIGNALS = [
    'you just signed',
    'order confirmation',
    'your order',
    'signed by all signers',
]

# Gmail label prefix for matter labels
# LL/1./ = Delivery (lawyer/legal work)
# LL/2./ = Fulfillment (team admin and accounts related to matters)
MATTER_LABEL_PREFIX = 'LL/'


def is_matthew(sender):
    """Return True if sender is one of Matthew's known addresses."""
    sender_lower = (sender or '').lower()
    return any(email in sender_lower for email in MATTHEW_EMAILS)


def is_team(sender):
    """Return True if sender is a known team member."""
    sender_lower = (sender or '').lower()
    return any(s in sender_lower for s in TEAM_SENDERS)


def is_automated_sender(sender):
    """Return True if sender appears to be automated / system-generated."""
    sender_lower = (sender or '').lower()
    return any(signal in sender_lower for signal in AUTOMATED_SENDER_SIGNALS)


def generate_batch(batch_size=25):
    """
    Generate batch classification proposal for inbox threads.

    Args:
        batch_size: Number of threads to include in batch (default: 25)

    Returns:
        dict with:
            - batch_id: str (timestamp-based)
            - threads: list of dicts containing:
                - thread_id: str
                - subject: str
                - sender: str
                - snippet: str
                - current_labels: list of str
                - proposed_label: str (one of CANONICAL_LABELS)
                - extracted_matter_number: str or None
                - proposed_matter_label: str or None
                - matter_resolution_status: str
                - ambiguous_matches: list

    Does NOT apply any changes, archive, or modify labels.
    """
    import datetime

    service = get_gmail_service()

    batch_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Exclude threads already carrying any canonical label so each batch
    # contains only fresh / unclassified inbox threads.
    exclude_q = ' '.join(f'-label:{label}' for label in CANONICAL_LABELS)

    results = service.users().threads().list(
        userId='me',
        labelIds=['INBOX'],
        q=exclude_q,
        maxResults=batch_size
    ).execute()

    threads_data = results.get('threads', [])

    # Get all Gmail labels once for label ID → name mapping
    all_gmail_labels = service.users().labels().list(userId='me').execute().get('labels', [])
    label_id_to_name = {label['id']: label['name'] for label in all_gmail_labels}

    # Get matter labels once for all threads
    matter_labels = get_matter_labels(service)

    batch_proposals = []

    for thread_info in threads_data:
        thread_id = thread_info['id']

        # Fetch full thread metadata (all messages, Subject + From headers)
        thread = service.users().threads().get(
            userId='me',
            id=thread_id,
            format='metadata',
            metadataHeaders=['Subject', 'From']
        ).execute()

        messages = thread.get('messages', [])
        first_message = messages[0]
        last_message = messages[-1]

        # Extract subject and sender from first message
        headers = first_message.get('payload', {}).get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), None)
        sender = next((h['value'] for h in headers if h['name'] == 'From'), None)

        # Extract last sender from last message
        last_headers = last_message.get('payload', {}).get('headers', [])
        last_sender = next((h['value'] for h in last_headers if h['name'] == 'From'), None)

        # Collect labels from ALL messages in thread
        all_label_ids = set()
        for msg in messages:
            all_label_ids.update(msg.get('labelIds', []))

        current_labels = [
            label_id_to_name.get(lid, lid)
            for lid in all_label_ids
            if lid in label_id_to_name
        ]

        # Check for existing matter label
        has_matter_label = any(MATTER_LABEL_PREFIX in label for label in current_labels)

        snippet = first_message.get('snippet', '')

        proposed_label = classify_thread(
            subject, sender, snippet, current_labels,
            last_sender=last_sender,
            message_count=len(messages),
            has_matter_label=has_matter_label
        )

        # Phase 2B: Extract and resolve matter label
        extracted_matter = extract_matter_number(subject or '', snippet)
        matter_resolution = resolve_matter_label(extracted_matter, matter_labels)

        batch_proposals.append({
            'thread_id': thread_id,
            'subject': subject or '(No Subject)',
            'sender': sender or '(Unknown)',
            'snippet': snippet[:200],
            'current_labels': current_labels,
            'proposed_label': proposed_label,
            'extracted_matter_number': extracted_matter,
            'proposed_matter_label': matter_resolution['proposed_label'],
            'matter_resolution_status': matter_resolution['status'],
            'ambiguous_matches': matter_resolution['ambiguous_matches']
        })

    return {
        'batch_id': batch_id,
        'batch_size': len(batch_proposals),
        'threads': batch_proposals
    }


def classify_thread(subject, sender, snippet, current_labels,
                    last_sender=None, message_count=1, has_matter_label=False):
    """
    Classify a thread into one of 9 canonical state labels.

    Decision order:
        1. Promotional / bulk mail                       → 80_Junk (Pending Review)
        2. Calendar notifications                        → 50_Calendar
        3. Matter label + automated sender               → 60_Filing
        4. Matter label + human sender                   → 10_Action_Matthew
        5. Sender is team member                         → 20_Action_Team
        6. Admin vendor / admin subject keyword          → 20_Action_Team
        7. Matthew replied last (multi-message thread)   → 40_Replied_Awaiting_Response
        8. Automated receipt / completion (no matter)    → 90_Archive
        9. Legal service sender                          → 10_Action_Matthew
       10. Default                                       → 00_Triage

    Args:
        subject: Email subject line
        sender: From header of first message
        snippet: Email snippet text
        current_labels: All Gmail label names on the thread
        last_sender: From header of last message in thread
        message_count: Total number of messages in thread
        has_matter_label: True if thread already carries an LL/ matter label (any tier)

    Returns:
        One of the 10 CANONICAL_LABELS strings
    """
    subject_lower = (subject or '').lower()
    sender_lower = (sender or '').lower()
    snippet_lower = snippet.lower()

    # 1. Calendar notifications → 50_Calendar (archived, no inbox noise)
    if 'calendar-notification@google.com' in sender_lower:
        return '50_Calendar'

    # 2 & 3. Thread has a matter label → legal matter
    if has_matter_label:
        # Automated sender (informational update) → file it, exit inbox
        if is_automated_sender(sender):
            return '60_Filing'
        # Human sender → Matthew needs to act or review
        return '10_Action_Matthew'

    # 4. Sender is a known team member → firm admin → 20_Action_Team
    if is_team(sender):
        return '20_Action_Team'

    # 5. Known admin vendor sender or admin subject keyword → 20_Action_Team
    #    (checked BEFORE junk so admin senders override unsubscribe footers)
    if (any(s in sender_lower for s in ADMIN_SENDERS) or
            any(kw in subject_lower for kw in ADMIN_SUBJECT_KEYWORDS)):
        return '20_Action_Team'

    # 6. Promotional / bulk → 80_Junk (Pending Review)
    #    (after admin checks so known senders aren't caught by unsubscribe footers)
    if 'CATEGORY_PROMOTIONS' in current_labels or 'unsubscribe' in snippet_lower:
        return '80_Junk (Pending Review)'

    # 7. Matthew sent the last message in a multi-message thread
    #    → waiting for external response → 40_Replied_Awaiting_Response
    if is_matthew(last_sender) and message_count >= 2:
        return '40_Replied_Awaiting_Response'

    # 8. Automated receipt / completion (no matter label) → 90_Archive
    if any(sig in subject_lower for sig in ARCHIVE_SUBJECT_SIGNALS):
        return '90_Archive'

    # 9. Legal service sender → requires Matthew's attention → 10_Action_Matthew
    if any(domain in sender_lower for domain in LEGAL_SENDERS):
        return '10_Action_Matthew'

    # 10. Default: needs review
    return '00_Triage'


if __name__ == "__main__":
    import sys

    batch_size = 25

    if len(sys.argv) > 1:
        try:
            batch_size = int(sys.argv[1])
        except ValueError:
            print("Usage: python batch_classifier.py [batch_size]")
            sys.exit(1)

    print(f"Generating batch proposal for {batch_size} threads...")
    batch = generate_batch(batch_size)

    print(json.dumps(batch, indent=2))

    _proposals_dir = Path(__file__).resolve().parents[1] / "06_RUNS" / "batch" / "proposals"
    _proposals_dir.mkdir(parents=True, exist_ok=True)
    output_filename = _proposals_dir / f"batch_proposal_{batch['batch_id']}.json"
    with open(output_filename, 'w') as f:
        json.dump(batch, f, indent=2)

    print(f"\nProposal saved to: {output_filename}")
    print(f"Threads proposed: {batch['batch_size']}")
