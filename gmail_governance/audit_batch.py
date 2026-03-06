"""
LL Inbox Governance - Phase 1: Audit Batch
Targeted audit for threads in a specific batch.
"""

import json
import sys
from state_enforcement import get_gmail_service, get_label_id_map, CANONICAL_LABELS


def audit_batch(batch_id):
    """
    Audit threads from a specific batch execution for exclusivity violations.

    Args:
        batch_id: The batch ID to audit

    Returns:
        dict with audit results
    """
    # Load execution log
    with open('execution_log.json', 'r') as f:
        log = json.load(f)

    # Filter for this batch
    batch_entries = [entry for entry in log if entry.get('batch_id') == batch_id]

    if not batch_entries:
        print(f"No entries found for batch {batch_id}")
        return {'violation_count': 0, 'violations': []}

    print(f"Auditing {len(batch_entries)} threads from batch {batch_id}...")

    service = get_gmail_service()
    label_map = get_label_id_map(service)

    # Reverse mapping
    id_to_canonical_name = {
        label_id: label_name
        for label_name, label_id in label_map.items()
    }

    violations = []

    for entry in batch_entries:
        thread_id = entry['thread_id']

        # Get thread
        thread = service.users().threads().get(
            userId='me',
            id=thread_id,
            format='metadata',
            metadataHeaders=['Subject']
        ).execute()

        # Collect label IDs
        all_label_ids = set()
        for message in thread.get('messages', []):
            all_label_ids.update(message.get('labelIds', []))

        # Identify canonical labels
        canonical_labels_present = [
            id_to_canonical_name[label_id]
            for label_id in all_label_ids
            if label_id in id_to_canonical_name
        ]

        # Check for violation
        if len(canonical_labels_present) > 1:
            first_message = thread['messages'][0]
            headers = first_message.get('payload', {}).get('headers', [])
            subject = '(No Subject)'

            for header in headers:
                if header['name'] == 'Subject':
                    subject = header['value']
                    break

            violations.append({
                'thread_id': thread_id,
                'subject': subject,
                'canonical_labels': canonical_labels_present
            })

        elif len(canonical_labels_present) == 1:
            print(f"  ✓ {thread_id}: {canonical_labels_present[0]}")
        else:
            print(f"  ⚠ {thread_id}: No canonical label")

    if violations:
        print(f"\n❌ Found {len(violations)} exclusivity violations:")
        for v in violations:
            print(f"  - {v['thread_id']}: {', '.join(v['canonical_labels'])}")
    else:
        print(f"\n✓ No exclusivity violations in batch {batch_id}")

    return {
        'batch_id': batch_id,
        'threads_audited': len(batch_entries),
        'violation_count': len(violations),
        'violations': violations
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python audit_batch.py <batch_id>")
        sys.exit(1)

    batch_id = sys.argv[1]
    result = audit_batch(batch_id)

    # Save result
    report_file = f"audit_batch_{batch_id}.json"
    with open(report_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"\nAudit report saved to: {report_file}")

    sys.exit(0 if result['violation_count'] == 0 else 1)
