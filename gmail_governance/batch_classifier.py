"""
LL Inbox Governance - Phase 2B: Batch Classifier
Generates state and matter classification proposals for inbox threads (no execution).
Soft-junk cleanup is handled separately under PRO-018.
"""

import json
import re
from functools import lru_cache
from pathlib import Path
import yaml
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

# Canonical matter label tier prefixes (PRO-014 v0.4+)
# Format: LL/1./{tier}/{matter_id} -- {name}
# LL/1./1.1/ = Essential, LL/1./1.2/ = Strategic, LL/1./1.3/ = Standard, LL/1./1.4/ = Parked
MATTER_LABEL_PREFIX = 'LL/1./'
MATTER_TIER_PREFIXES = ('LL/1./1.1/', 'LL/1./1.2/', 'LL/1./1.3/', 'LL/1./1.4/')
SOFT_JUNK_GMAIL_CATEGORY_LABELS = {
    'CATEGORY_PROMOTIONS',
    'CATEGORY_SOCIAL',
    'CATEGORY_FORUMS',
}
DETERMINATIVE_MATTER_SIGNALS = {
    'existing_matter_label',
}
HIGH_CONFIDENCE_MATTER_SIGNALS = {
    'subject_matter_number',
    'identity_sender',
    'identity_domain',
    'thread_lineage',
}
MEDIUM_CONFIDENCE_MATTER_SIGNALS = {
    'snippet_matter_number',
    'identity_name_key',
}
GENERIC_IDENTITY_KEYS = {
    'alerts',
    'email',
    'gmail',
    'hello',
    'info',
    'marketing',
    'ontario',
    'support',
}
_REPO_ROOT = Path(__file__).resolve().parents[1]
_MATTER_IDENTITY_MAP_PATH = _REPO_ROOT / "00_SYSTEM" / "matters" / "matter_identity_map.yaml"


def _normalize_identity_token(value):
    return re.sub(r'[^a-z0-9]+', '', (value or '').lower())


def _tokenize_identity_text(value):
    return {
        token
        for token in re.split(r'[^a-z0-9]+', (value or '').lower())
        if token
    }


def _extract_sender_email(sender):
    sender_lower = (sender or '').strip().lower()
    match = re.search(r'[\w.+-]+@[\w.-]+\.\w+', sender_lower)
    return match.group(0) if match else ''


def _extract_sender_domain(sender):
    email = _extract_sender_email(sender)
    if '@' not in email:
        return ''
    return email.split('@', 1)[1]


@lru_cache(maxsize=1)
def load_identity_indexes():
    """
    Load exact sender / domain identity signals from matter_identity_map.yaml.

    This is a proposal-time routing aid only. Generic or empty tokens are excluded.
    """
    if not _MATTER_IDENTITY_MAP_PATH.exists():
        return {'senders': {}, 'domains': {}, 'name_keys': {}}

    with _MATTER_IDENTITY_MAP_PATH.open('r', encoding='utf-8') as handle:
        raw = yaml.safe_load(handle) or {}

    sender_map = {}
    domain_map = {}
    name_key_map = {}

    for matter in raw.get('matters', []):
        matter_id = str(matter.get('matter_id', '')).strip()
        aliases = (((matter.get('aliases') or {}).get('email')) or {})

        for sender in aliases.get('senders', []) or []:
            sender_norm = str(sender).strip().lower()
            if not sender_norm:
                continue
            sender_map.setdefault(sender_norm, set()).add(matter_id)

        for domain in aliases.get('domains', []) or []:
            domain_norm = str(domain).strip().lower()
            if not domain_norm:
                continue
            domain_map.setdefault(domain_norm, set()).add(matter_id)

        for name_key in aliases.get('name_keys', []) or []:
            token = _normalize_identity_token(name_key)
            if not token or token in GENERIC_IDENTITY_KEYS:
                continue
            name_key_map.setdefault(token, set()).add(matter_id)

    return {
        'senders': sender_map,
        'domains': domain_map,
        'name_keys': name_key_map,
    }


def _parse_existing_matter_label(current_labels):
    for label in current_labels:
        if not label.startswith(MATTER_TIER_PREFIXES):
            continue
        leaf = label.split('/')[-1]
        matter_id = leaf.split(' --', 1)[0].strip()
        if matter_id:
            return {
                'status': 'matched',
                'proposed_label': label,
                'proposed_label_id': None,
                'ambiguous_matches': [],
                'signal': 'existing_matter_label',
                'matter_number': matter_id,
            }
    return None


def _resolve_identity_candidate(candidate_ids, matter_labels, signal):
    if not candidate_ids:
        return None

    candidate_ids = sorted(set(candidate_ids))
    if len(candidate_ids) > 1:
        return {
            'status': 'ambiguous',
            'proposed_label': None,
            'proposed_label_id': None,
            'ambiguous_matches': candidate_ids,
            'signal': signal,
            'matter_number': None,
        }

    matter_number = candidate_ids[0]
    resolved = resolve_matter_label(matter_number, matter_labels)
    resolved['signal'] = signal
    resolved['matter_number'] = matter_number if resolved['status'] == 'matched' else None
    return resolved


def resolve_thread_matter(subject, sender, snippet, current_labels, matter_labels):
    """
    Resolve thread → matter using current label, explicit matter number, then exact identity hints.
    """
    existing = _parse_existing_matter_label(current_labels)
    if existing:
        return existing

    subject = subject or ''
    snippet = snippet or ''

    subject_match = extract_matter_number(subject, '')
    if subject_match:
        resolved = resolve_matter_label(subject_match, matter_labels)
        resolved['signal'] = 'subject_matter_number'
        resolved['matter_number'] = subject_match if resolved['status'] == 'matched' else None
        return resolved

    snippet_match = extract_matter_number('', snippet)
    if snippet_match:
        resolved = resolve_matter_label(snippet_match, matter_labels)
        resolved['signal'] = 'snippet_matter_number'
        resolved['matter_number'] = snippet_match if resolved['status'] == 'matched' else None
        return resolved

    identity = load_identity_indexes()
    sender_email = _extract_sender_email(sender)
    sender_domain = _extract_sender_domain(sender)
    sender_tokens = _tokenize_identity_text(sender)
    subject_tokens = _tokenize_identity_text(subject)

    if sender_email:
        resolved = _resolve_identity_candidate(identity['senders'].get(sender_email, []), matter_labels, 'identity_sender')
        if resolved:
            return resolved

    if sender_domain:
        resolved = _resolve_identity_candidate(identity['domains'].get(sender_domain, []), matter_labels, 'identity_domain')
        if resolved:
            return resolved

    matched_name_keys = set()
    for name_key, candidate_ids in identity['name_keys'].items():
        if name_key and (name_key in sender_tokens or name_key in subject_tokens):
            matched_name_keys.update(candidate_ids)
    resolved = _resolve_identity_candidate(matched_name_keys, matter_labels, 'identity_name_key')
    if resolved:
        return resolved

    return {
        'status': 'none_found',
        'proposed_label': None,
        'proposed_label_id': None,
        'ambiguous_matches': [],
        'signal': 'none',
        'matter_number': None,
    }


def get_soft_junk_gmail_categories(current_labels):
    return sorted(label for label in current_labels if label in SOFT_JUNK_GMAIL_CATEGORY_LABELS)


def get_matter_signal_confidence(signal):
    if signal in DETERMINATIVE_MATTER_SIGNALS:
        return 'determinative'
    if signal in HIGH_CONFIDENCE_MATTER_SIGNALS:
        return 'high'
    if signal in MEDIUM_CONFIDENCE_MATTER_SIGNALS:
        return 'medium'
    return 'none'


def supports_auto_matter_routing(signal):
    return get_matter_signal_confidence(signal) in {'determinative', 'high'}


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

        snippet = first_message.get('snippet', '')
        matter_resolution = resolve_thread_matter(subject, sender, snippet, current_labels, matter_labels)
        matter_signal = matter_resolution.get('signal')
        matter_confidence = get_matter_signal_confidence(matter_signal)
        has_matter_association = (
            matter_resolution['status'] == 'matched'
            and supports_auto_matter_routing(matter_signal)
        )
        requires_matter_review = (
            matter_resolution['status'] == 'matched'
            and not has_matter_association
        )

        proposed_label = classify_thread(
            subject, sender, snippet, current_labels,
            last_sender=last_sender,
            message_count=len(messages),
            has_matter_association=has_matter_association
        )

        batch_proposals.append({
            'thread_id': thread_id,
            'subject': subject or '(No Subject)',
            'sender': sender or '(Unknown)',
            'snippet': snippet[:200],
            'current_labels': current_labels,
            'proposed_label': proposed_label,
            'soft_junk_gmail_categories': get_soft_junk_gmail_categories(current_labels),
            'soft_junk_cleanup_candidate': bool(get_soft_junk_gmail_categories(current_labels)) and matter_resolution['status'] == 'none_found',
            'extracted_matter_number': matter_resolution.get('matter_number'),
            'proposed_matter_label': matter_resolution['proposed_label'],
            'matter_resolution_status': matter_resolution['status'],
            'matter_resolution_signal': matter_resolution.get('signal'),
            'matter_resolution_confidence': matter_confidence,
            'matter_review_required': requires_matter_review,
            'ambiguous_matches': matter_resolution['ambiguous_matches']
        })

    return {
        'batch_id': batch_id,
        'batch_size': len(batch_proposals),
        'threads': batch_proposals
    }


def classify_thread(subject, sender, snippet, current_labels,
                    last_sender=None, message_count=1, has_matter_association=False):
    """
    Classify a thread into one of 9 canonical state labels.

    Decision order:
        1. Calendar notifications                        → 50_Calendar
        2. Matter-associated thread + automated sender   → 60_Filing
        3. Matter-associated thread + human sender       → 10_Action_Matthew
        4. Sender is team member                         → 20_Action_Team
        5. Admin vendor / admin subject keyword          → 20_Action_Team
        6. Matthew replied last (multi-message thread)   → 40_Replied_Awaiting_Response
        7. Automated receipt / completion (no matter)    → 90_Archive
        8. Legal service sender                          → 10_Action_Matthew
        9. Promotional footer only                       → 80_Junk_to_Review
       10. Default                                       → 00_Triage

    Args:
        subject: Email subject line
        sender: From header of first message
        snippet: Email snippet text
        current_labels: All Gmail label names on the thread
        last_sender: From header of last message in thread
        message_count: Total number of messages in thread
        has_matter_association: True if the thread already carries or deterministically resolves to a matter

    Returns:
        One of the 10 CANONICAL_LABELS strings
    """
    subject_lower = (subject or '').lower()
    sender_lower = (sender or '').lower()
    snippet_lower = snippet.lower()
    # 1. Calendar notifications → 50_Calendar (archived, no inbox noise)
    if 'calendar-notification@google.com' in sender_lower:
        return '50_Calendar'

    # 2 & 3. Matter-associated thread → legal matter
    if has_matter_association:
        # Automated sender (informational update) → file it, exit inbox
        if is_automated_sender(sender):
            return '60_Filing'
        # Human sender → Matthew needs to act or review
        return '10_Action_Matthew'

    # 4. Sender is a known team member → firm admin → 20_Action_Team
    if is_team(sender):
        return '20_Action_Team'

    # 5. Known admin vendor sender or admin subject keyword → 20_Action_Team
    if (any(s in sender_lower for s in ADMIN_SENDERS) or
            any(kw in subject_lower for kw in ADMIN_SUBJECT_KEYWORDS)):
        return '20_Action_Team'

    # 6. Matthew sent the last message in a multi-message thread
    #    → waiting for external response → 40_Replied_Awaiting_Response
    if is_matthew(last_sender) and message_count >= 2:
        return '40_Replied_Awaiting_Response'

    # 7. Automated receipt / completion (no matter label) → 90_Archive
    if any(sig in subject_lower for sig in ARCHIVE_SUBJECT_SIGNALS):
        return '90_Archive'

    # 8. Legal service sender → requires Matthew's attention → 10_Action_Matthew
    if any(domain in sender_lower for domain in LEGAL_SENDERS):
        return '10_Action_Matthew'

    # 9. Promotional footer only → junk pending review
    if 'unsubscribe' in snippet_lower:
        return '80_Junk_to_Review'

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
