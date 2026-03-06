"""
LL Inbox Governance - Phase 1: Test State Enforcement
Tests state_enforcement.py on 5 threads.
"""

import json
from state_enforcement import get_gmail_service, apply_state, CANONICAL_LABELS


def get_test_threads(count=5):
    """
    Fetch thread IDs from inbox for testing.

    Args:
        count: Number of threads to fetch

    Returns:
        list of dicts with thread_id, subject, current_labels
    """
    service = get_gmail_service()

    # Get threads from inbox
    results = service.users().threads().list(
        userId='me',
        labelIds=['INBOX'],
        maxResults=count
    ).execute()

    threads = results.get('threads', [])

    # Get label mapping
    all_labels = service.users().labels().list(userId='me').execute().get('labels', [])
    label_id_to_name = {label['id']: label['name'] for label in all_labels}

    test_threads = []

    for thread_info in threads:
        thread_id = thread_info['id']

        # Get thread details
        thread = service.users().threads().get(
            userId='me',
            id=thread_id,
            format='metadata',
            metadataHeaders=['Subject']
        ).execute()

        # Get subject
        first_message = thread['messages'][0]
        headers = first_message.get('payload', {}).get('headers', [])
        subject = '(No Subject)'

        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
                break

        # Get current labels
        label_ids = first_message.get('labelIds', [])
        current_labels = [label_id_to_name.get(lid, lid) for lid in label_ids]

        # Identify canonical labels
        canonical_labels = [label for label in current_labels if label in CANONICAL_LABELS]

        test_threads.append({
            'thread_id': thread_id,
            'subject': subject,
            'current_labels': current_labels,
            'canonical_labels': canonical_labels
        })

    return test_threads


def verify_canonical_labels():
    """
    Verify all canonical labels exist in Gmail account.

    Returns:
        dict with missing_labels list
    """
    service = get_gmail_service()

    all_labels = service.users().labels().list(userId='me').execute().get('labels', [])
    existing_label_names = {label['name'] for label in all_labels}

    missing = []
    for canonical_label in CANONICAL_LABELS:
        if canonical_label not in existing_label_names:
            missing.append(canonical_label)

    return {
        'all_exist': len(missing) == 0,
        'missing_labels': missing
    }


def run_tests():
    """
    Run state_enforcement tests on 5 threads.
    """
    print("=" * 60)
    print("Phase 1: Testing State Enforcement")
    print("=" * 60)

    # Step 1: Verify canonical labels exist
    print("\n[1/3] Verifying canonical labels exist...")
    label_check = verify_canonical_labels()

    if not label_check['all_exist']:
        print(f"❌ Missing canonical labels: {label_check['missing_labels']}")
        print("\nYou must create these labels in Gmail before proceeding.")
        return False

    print("✓ All canonical labels exist")

    # Step 2: Fetch test threads
    print("\n[2/3] Fetching 5 test threads from inbox...")
    test_threads = get_test_threads(5)

    if len(test_threads) == 0:
        print("❌ No threads found in inbox")
        return False

    print(f"✓ Found {len(test_threads)} threads")

    for i, thread in enumerate(test_threads, 1):
        print(f"\n  Thread {i}:")
        print(f"    ID: {thread['thread_id']}")
        print(f"    Subject: {thread['subject'][:60]}")
        print(f"    Canonical labels: {thread['canonical_labels'] or '(none)'}")

    # Step 3: Test state enforcement
    print("\n[3/3] Testing state enforcement...")
    print("\nTest: Apply '00_Triage' to first thread, then restore prior state")

    first_thread = test_threads[0]
    thread_id = first_thread['thread_id']
    prior_canonical = first_thread['canonical_labels'][0] if first_thread['canonical_labels'] else None

    print(f"\nThread ID: {thread_id}")
    print(f"Prior state: {prior_canonical or '(none)'}")

    try:
        # Apply 00_Triage
        result1 = apply_state(thread_id, '00_Triage')
        print(f"\n✓ Applied '00_Triage'")
        print(f"  Result: {json.dumps(result1, indent=2)}")

        # Restore prior state if it existed
        if prior_canonical:
            result2 = apply_state(thread_id, prior_canonical)
            print(f"\n✓ Restored '{prior_canonical}'")
            print(f"  Result: {json.dumps(result2, indent=2)}")
        else:
            print("\n  (No prior canonical state to restore)")

        print("\n" + "=" * 60)
        print("✓ State enforcement test PASSED")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n❌ Test FAILED: {e}")
        return False


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
