"""
LL Inbox Governance - Phase 2B: Matter Enforcement
Enforces matter label exclusivity (separate from State labels).
"""

import os
import re
from state_enforcement import get_gmail_service, get_label_id_map


# Matter label pattern: LL/1./<priority>/<matter> -- <name>
MATTER_LABEL_PREFIX = "LL/1./"
MATTER_LEAF_PATTERN = re.compile(r"^(\d{2,3}-\d{2,5}(?:-\d{5})?)\b")

# Matter number extraction patterns
BASE_MATTER_PATTERN = re.compile(r"\b(\d{2,3}-\d{2,5})\b")
SUB_MATTER_PATTERN = re.compile(r"\b(\d{2,3}-\d{2,5}-\d{5})\b")


def load_matter_registry():
    """
    Load matter registry from 05_MATTERS/README.md.

    Returns:
        set of matter numbers (both base and sub-matter)
    """
    registry_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "05_MATTERS",
        "README.md"
    )

    if not os.path.exists(registry_path):
        return set()

    matter_numbers = set()

    with open(registry_path, 'r') as f:
        content = f.read()

    # Extract all matter_id values from the tables
    # Pattern: | <matter_id> | ...
    for match in re.finditer(r"\|\s*(\d{2,3}-\d{2,5}(?:-\d{5})?)\s*\|", content):
        matter_numbers.add(match.group(1))

    return matter_numbers


def extract_matter_number(subject, snippet):
    """
    Extract matter number from email subject/snippet.

    Args:
        subject: Email subject
        snippet: Email snippet

    Returns:
        str or None: Most specific matter number found (sub-matter preferred)

    Priority rule: If both base and sub-matter match, return sub-matter.
    """
    text = f"{subject} {snippet}"

    # Find all sub-matters
    sub_matters = SUB_MATTER_PATTERN.findall(text)

    if sub_matters:
        # Return first sub-matter (most specific)
        return sub_matters[0]

    # Find base matters
    base_matters = BASE_MATTER_PATTERN.findall(text)

    if base_matters:
        return base_matters[0]

    return None


def get_matter_labels(service):
    """
    Retrieve all matter labels from Gmail.

    Args:
        service: Gmail API service

    Returns:
        dict: mapping of matter_number → list of full label paths
    """
    all_labels = service.users().labels().list(userId='me').execute().get('labels', [])

    matter_labels = {}

    for label in all_labels:
        label_name = label['name']

        # Check if label starts with LL/1./
        if not label_name.startswith(MATTER_LABEL_PREFIX):
            continue

        # Extract leaf (last part after final /)
        parts = label_name.split('/')
        if len(parts) < 3:
            continue

        leaf = parts[-1]

        # Check if leaf begins with matter number pattern
        match = MATTER_LEAF_PATTERN.match(leaf)
        if not match:
            continue

        matter_number = match.group(1)

        if matter_number not in matter_labels:
            matter_labels[matter_number] = []

        matter_labels[matter_number].append({
            'label_id': label['id'],
            'label_name': label_name
        })

    return matter_labels


def resolve_matter_label(matter_number, matter_labels):
    """
    Resolve matter number to Gmail label.

    Args:
        matter_number: Extracted matter number (e.g., "25-927-00003")
        matter_labels: Dict from get_matter_labels()

    Returns:
        dict with:
            - status: "matched" | "none_found" | "ambiguous"
            - proposed_label: full label path (if matched)
            - proposed_label_id: Gmail label ID (if matched)
            - ambiguous_matches: list of candidate label paths (if ambiguous)
    """
    if not matter_number:
        return {
            'status': 'none_found',
            'proposed_label': None,
            'proposed_label_id': None,
            'ambiguous_matches': []
        }

    candidates = matter_labels.get(matter_number, [])

    if len(candidates) == 0:
        return {
            'status': 'none_found',
            'proposed_label': None,
            'proposed_label_id': None,
            'ambiguous_matches': []
        }
    elif len(candidates) == 1:
        return {
            'status': 'matched',
            'proposed_label': candidates[0]['label_name'],
            'proposed_label_id': candidates[0]['label_id'],
            'ambiguous_matches': []
        }
    else:
        return {
            'status': 'ambiguous',
            'proposed_label': None,
            'proposed_label_id': None,
            'ambiguous_matches': [c['label_name'] for c in candidates]
        }


def apply_matter_label(thread_id, matter_label_id):
    """
    Apply matter label with exclusivity enforcement.

    Removes any existing LL/1./ matter labels, then applies new one.

    Args:
        thread_id: Gmail thread ID
        matter_label_id: Gmail label ID to apply

    Returns:
        dict with:
            - success: bool
            - prior_matter: str or None (previous matter label name)
            - new_matter: str (new matter label name)
    """
    service = get_gmail_service()

    # Get all labels
    all_labels = service.users().labels().list(userId='me').execute().get('labels', [])
    label_id_to_name = {label['id']: label['name'] for label in all_labels}

    # Get thread
    thread = service.users().threads().get(userId='me', id=thread_id).execute()

    # Collect current label IDs
    current_label_ids = set()
    for message in thread.get('messages', []):
        current_label_ids.update(message.get('labelIds', []))

    # Identify existing matter labels to remove
    matter_labels_to_remove = []
    prior_matter = None

    for label_id in current_label_ids:
        label_name = label_id_to_name.get(label_id)
        if not label_name:
            continue

        # Check if it's a matter label
        if label_name.startswith(MATTER_LABEL_PREFIX):
            parts = label_name.split('/')
            if len(parts) >= 3:
                leaf = parts[-1]
                if MATTER_LEAF_PATTERN.match(leaf):
                    matter_labels_to_remove.append(label_id)
                    prior_matter = label_name

    # Idempotency check
    if len(matter_labels_to_remove) == 1 and matter_labels_to_remove[0] == matter_label_id:
        return {
            'success': True,
            'prior_matter': label_id_to_name.get(matter_label_id),
            'new_matter': label_id_to_name.get(matter_label_id),
            'no_change': True
        }

    # Apply modification
    modify_body = {
        'addLabelIds': [matter_label_id],
        'removeLabelIds': matter_labels_to_remove
    }

    service.users().threads().modify(
        userId='me',
        id=thread_id,
        body=modify_body
    ).execute()

    return {
        'success': True,
        'prior_matter': prior_matter,
        'new_matter': label_id_to_name.get(matter_label_id)
    }


def validate_matter_exclusivity(thread_id):
    """
    Validate that thread has at most one matter label.

    Args:
        thread_id: Gmail thread ID

    Returns:
        dict with:
            - valid: bool (True if 0 or 1 matter labels)
            - matter_labels: list of matter label names
            - error: str (if not valid)
    """
    service = get_gmail_service()

    # Get all labels
    all_labels = service.users().labels().list(userId='me').execute().get('labels', [])
    label_id_to_name = {label['id']: label['name'] for label in all_labels}

    # Get thread
    thread = service.users().threads().get(
        userId='me',
        id=thread_id,
        format='metadata'
    ).execute()

    # Collect all label IDs
    all_label_ids = set()
    for message in thread.get('messages', []):
        all_label_ids.update(message.get('labelIds', []))

    # Identify matter labels
    matter_labels = []

    for label_id in all_label_ids:
        label_name = label_id_to_name.get(label_id)
        if not label_name:
            continue

        if label_name.startswith(MATTER_LABEL_PREFIX):
            parts = label_name.split('/')
            if len(parts) >= 3:
                leaf = parts[-1]
                if MATTER_LEAF_PATTERN.match(leaf):
                    matter_labels.append(label_name)

    # Validation: 0 or 1 matter labels allowed
    if len(matter_labels) > 1:
        return {
            'valid': False,
            'matter_labels': matter_labels,
            'error': f'Thread has multiple matter labels: {matter_labels}'
        }
    else:
        return {
            'valid': True,
            'matter_labels': matter_labels,
            'error': None
        }
