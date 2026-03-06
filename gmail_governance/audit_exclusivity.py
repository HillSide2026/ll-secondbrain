"""
LL Inbox Governance - Phase 1: Audit Exclusivity
Identifies threads with multiple canonical state labels (violations).
"""

import json
import datetime
from state_enforcement import get_gmail_service, get_label_id_map, CANONICAL_LABELS


def audit():
    """
    Audit all threads for canonical state exclusivity violations.

    Returns:
        dict with:
            - audit_timestamp: str (ISO format)
            - total_threads_checked: int
            - violations: list of dicts containing:
                - thread_id: str
                - subject: str
                - canonical_labels: list of str (should have only 1, has multiple)
            - violation_count: int

    Does NOT modify any threads.
    """
    service = get_gmail_service()
    label_map = get_label_id_map(service)

    # Reverse mapping: label_id → label_name (for canonical labels only)
    id_to_canonical_name = {
        label_id: label_name
        for label_name, label_id in label_map.items()
    }

    violations = []
    threads_checked = 0

    print("Starting exclusivity audit...")

    # Query all threads (we'll paginate through them)
    # For Phase 1, we check inbox + archive
    page_token = None
    batch_count = 0

    while True:
        batch_count += 1
        print(f"  Checking batch {batch_count}...", end='\r')

        # Get threads
        results = service.users().threads().list(
            userId='me',
            maxResults=100,
            pageToken=page_token
        ).execute()

        threads = results.get('threads', [])

        if not threads:
            break

        for thread_info in threads:
            thread_id = thread_info['id']
            threads_checked += 1

            # Get thread details
            thread = service.users().threads().get(
                userId='me',
                id=thread_id,
                format='metadata',
                metadataHeaders=['Subject']
            ).execute()

            # Collect all label IDs from all messages in thread
            all_label_ids = set()
            for message in thread.get('messages', []):
                all_label_ids.update(message.get('labelIds', []))

            # Identify which canonical labels are present
            canonical_labels_present = [
                id_to_canonical_name[label_id]
                for label_id in all_label_ids
                if label_id in id_to_canonical_name
            ]

            # Violation if more than one canonical label
            if len(canonical_labels_present) > 1:
                # Get subject from first message
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

        # Check for next page
        page_token = results.get('nextPageToken')
        if not page_token:
            break

    print(f"\n\nAudit complete.")
    print(f"Threads checked: {threads_checked}")
    print(f"Violations found: {len(violations)}")

    if violations:
        print("\nExclusivity Violations:")
        for v in violations:
            print(f"  - {v['thread_id']}: {v['subject'][:60]}")
            print(f"    Labels: {', '.join(v['canonical_labels'])}")

    return {
        'audit_timestamp': datetime.datetime.now().isoformat(),
        'total_threads_checked': threads_checked,
        'violations': violations,
        'violation_count': len(violations)
    }


if __name__ == "__main__":
    import sys

    # Run audit
    result = audit()

    # Save audit report
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"audit_report_{timestamp}.json"

    with open(report_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"\nAudit report saved to: {report_file}")

    # Exit with error code if violations found
    if result['violation_count'] > 0:
        sys.exit(1)
    else:
        print("\n✓ No exclusivity violations found.")
        sys.exit(0)
