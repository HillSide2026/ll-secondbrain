"""
LL Inbox Governance - Phase 2B: Apply Batch
Executes approved batch classifications with validation and controlled archiving.
Includes matter label application (separate from state labels).
"""

import collections
import json
import os
import datetime
from pathlib import Path
from state_enforcement import apply_state, get_gmail_service, get_label_id_map, CANONICAL_LABELS
from matter_enforcement import (
    apply_matter_label,
    validate_matter_exclusivity,
    get_matter_labels,
    resolve_matter_label
)


_REPO_ROOT = Path(__file__).resolve().parents[1]
_EXECUTIONS_DIR = _REPO_ROOT / "06_RUNS" / "batch" / "executions"
EXECUTION_LOG_PATH = os.path.join(os.path.dirname(__file__), 'execution_log.json')


def load_execution_log():
    """Load execution log from file."""
    if os.path.exists(EXECUTION_LOG_PATH):
        with open(EXECUTION_LOG_PATH, 'r') as f:
            return json.load(f)
    return []


def append_to_log(log_entry):
    """
    Append entry to execution log.

    Args:
        log_entry: dict with required fields:
            - timestamp
            - thread_id
            - prior_state
            - new_state
            - archived
            - matter_proposed
            - matter_applied
            - matter_outcome
            - action_type
            - batch_id
    """
    log = load_execution_log()
    log.append(log_entry)

    with open(EXECUTION_LOG_PATH, 'w') as f:
        json.dump(log, f, indent=2)


def validate_thread_exclusivity(thread_id):
    """
    Validate that thread has exactly one canonical state label.

    Args:
        thread_id: Gmail thread ID

    Returns:
        dict with:
            - valid: bool (True if exactly 1 canonical label)
            - canonical_labels: list of canonical label names
            - error: str (if not valid)

    Phase 2A: This validation MUST pass before archiving.
    """
    service = get_gmail_service()
    label_map = get_label_id_map(service)

    # Reverse mapping
    id_to_canonical_name = {
        label_id: label_name
        for label_name, label_id in label_map.items()
    }

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

    # Identify canonical labels
    canonical_labels = [
        id_to_canonical_name[label_id]
        for label_id in all_label_ids
        if label_id in id_to_canonical_name
    ]

    # Validation rules
    if len(canonical_labels) == 0:
        return {
            'valid': False,
            'canonical_labels': canonical_labels,
            'error': 'Thread has NO canonical labels'
        }
    elif len(canonical_labels) > 1:
        return {
            'valid': False,
            'canonical_labels': canonical_labels,
            'error': f'Thread has multiple canonical labels: {canonical_labels}'
        }
    else:
        return {
            'valid': True,
            'canonical_labels': canonical_labels,
            'error': None
        }


def archive_thread(thread_id):
    """
    Archive a thread by removing INBOX label.

    Args:
        thread_id: Gmail thread ID
    """
    service = get_gmail_service()

    service.users().threads().modify(
        userId='me',
        id=thread_id,
        body={'removeLabelIds': ['INBOX']}
    ).execute()


def apply_approved_batch(batch_data, batch_id):
    """
    Execute approved batch classification with Phase 2B validation.

    Args:
        batch_data: dict containing:
            - threads: list of thread proposals
        batch_id: str identifier for this batch

    Returns:
        dict with:
            - batch_id: str
            - executed_count: int
            - archived_count: int
            - errors: list of dicts with thread_id and error message

    Phase 2B Execution Order (Per Thread):
        1. Apply new canonical state label
        2. Remove all other canonical labels
        3. Validate exactly one canonical label remains
        4. If validation fails → HALT batch execution
        5. Apply matter label (if proposed)
        6. Validate at most one matter label
        7. If validation fails → HALT batch execution
        8. If new_state ∉ {00_Triage, 10_Action_Matthew}: Archive thread
        9. Append execution_log entry (include matter fields)
       10. Continue to next thread
    """
    threads = batch_data.get('threads', [])

    executed_count = 0
    archived_count = 0
    errors = []
    state_transition_counts = collections.Counter()
    matter_outcome_counts = collections.Counter()
    matter_failures = []

    print(f"Executing batch {batch_id} with {len(threads)} threads...")
    print("Phase 2B: State + Matter validation and controlled archiving enabled\n")

    for thread in threads:
        thread_id = thread['thread_id']
        proposed_label = thread['proposed_label']

        try:
            # Step 1-2: Apply state (enforces exclusivity)
            result = apply_state(thread_id, proposed_label)

            prior_state = result.get('prior_state')
            new_state = result.get('new_state')

            # Step 3: Validate exactly one canonical label remains
            validation = validate_thread_exclusivity(thread_id)

            # Invariant: exactly one state label after apply
            if not validation['valid']:
                print(f"INVARIANT VIOLATION: thread={thread_id} expected 1 canonical label, found {validation['canonical_labels']}")

            # Step 4: HALT if validation fails
            if not validation['valid']:
                error_msg = f"VALIDATION FAILED: {validation['error']}"
                print(f"\n❌ HALTING BATCH EXECUTION")
                print(f"  Thread: {thread_id}")
                print(f"  Error: {error_msg}")
                print(f"  Canonical labels found: {validation['canonical_labels']}")
                print(f"\nBatch halted at thread {executed_count + 1}/{len(threads)}")

                errors.append({
                    'thread_id': thread_id,
                    'error': error_msg,
                    'validation_failure': True
                })

                return {
                    'batch_id': batch_id,
                    'executed_count': executed_count,
                    'archived_count': archived_count,
                    'errors': errors,
                    'halted': True,
                    'halt_reason': 'Validation failure'
                }

            # Step 5-7: Apply matter label (if proposed) and validate
            proposed_matter_label = thread.get('proposed_matter_label')
            extracted_matter = thread.get('extracted_matter_number')
            matter_applied = None
            matter_outcome = 'none'

            if proposed_matter_label:
                # Resolve matter label ID
                matter_labels = get_matter_labels(get_gmail_service())
                matter_resolution = resolve_matter_label(extracted_matter, matter_labels)

                if matter_resolution['status'] == 'matched':
                    proposed_matter_label_id = matter_resolution['proposed_label_id']

                    # Apply matter label
                    matter_result = apply_matter_label(thread_id, proposed_matter_label_id)
                    matter_applied = matter_result.get('new_matter')
                    matter_outcome = 'applied'

                    # Validate matter exclusivity
                    matter_validation = validate_matter_exclusivity(thread_id)

                    # Invariant: 0 or 1 matter label after apply
                    if not matter_validation['valid']:
                        print(f"INVARIANT VIOLATION: thread={thread_id} expected ≤1 matter label, found {matter_validation['matter_labels']}")

                    if not matter_validation['valid']:
                        error_msg = f"MATTER VALIDATION FAILED: {matter_validation['error']}"
                        print(f"\n❌ HALTING BATCH EXECUTION")
                        print(f"  Thread: {thread_id}")
                        print(f"  Error: {error_msg}")
                        print(f"  Matter labels found: {matter_validation['matter_labels']}")

                        errors.append({
                            'thread_id': thread_id,
                            'error': error_msg,
                            'validation_failure': True
                        })

                        return {
                            'batch_id': batch_id,
                            'executed_count': executed_count,
                            'archived_count': archived_count,
                            'errors': errors,
                            'halted': True,
                            'halt_reason': 'Matter validation failure'
                        }

                else:
                    # Resolution failed at apply time — track as failure
                    matter_outcome = matter_resolution['status']
                    matter_failures.append({
                        'thread_id': thread_id,
                        'matter_number': extracted_matter,
                        'proposal': proposed_matter_label,
                        'matches': matter_resolution.get('ambiguous_matches', [])
                    })

            # Invariant: matter must not trigger archive
            # Archive decision is based solely on new_state — assert matter plays no role
            if matter_applied and new_state in ['00_Triage', '10_Action_Matthew']:
                # Matter was applied but thread stays in inbox — correct behavior
                pass
            elif matter_applied and new_state not in ['00_Triage', '10_Action_Matthew']:
                # Matter applied and thread will be archived — valid, matter does not drive this
                pass

            # Step 8: Archive if non-actionable state (matter labels never cause archive)
            should_archive = new_state not in ['00_Triage', '10_Action_Matthew']

            if should_archive:
                archive_thread(thread_id)
                action_type = 'state_change_with_archive'
                archived_count += 1
            else:
                action_type = 'state_change_no_archive'

            # Track counters
            transition_key = f"{prior_state or '(none)'}→{new_state}"
            state_transition_counts[transition_key] += 1
            matter_outcome_counts[matter_outcome] += 1

            # Step 9: Log the execution (new schema)
            log_entry = {
                'timestamp': datetime.datetime.now().isoformat(),
                'thread_id': thread_id,
                'prior_state': prior_state,
                'new_state': new_state,
                'archived': should_archive,
                'matter_proposed': extracted_matter,
                'matter_applied': matter_applied,
                'matter_outcome': matter_outcome,
                'action_type': action_type,
                'batch_id': batch_id
            }

            append_to_log(log_entry)
            executed_count += 1

            # Step 10: Deterministic per-thread output
            matter_display = extracted_matter if extracted_matter else 'none'
            archived_display = 'YES' if should_archive else 'NO'
            print(f"  ✓ thread={thread_id} state={prior_state or '(none)'}→{new_state} matter={matter_display} archived={archived_display}")

        except Exception as e:
            error_msg = str(e)
            print(f"\n❌ HALTING BATCH EXECUTION")
            print(f"  Thread: {thread_id}")
            print(f"  Error: {error_msg}")

            errors.append({
                'thread_id': thread_id,
                'error': error_msg
            })

            # HALT on any exception
            return {
                'batch_id': batch_id,
                'executed_count': executed_count,
                'archived_count': archived_count,
                'errors': errors,
                'halted': True,
                'halt_reason': 'Exception during execution'
            }

    # === RUN SUMMARY ===
    print(f"\n=== RUN SUMMARY ===")
    print(f"Batch:    {batch_id}")
    print(f"Executed: {executed_count}/{len(threads)}")
    print(f"Archived: {archived_count}")
    print(f"Errors:   {len(errors)}")

    print(f"\nState Transitions:")
    for transition, count in sorted(state_transition_counts.items()):
        print(f"  {transition}: {count}")

    print(f"\nMatter Outcomes:")
    for outcome, count in sorted(matter_outcome_counts.items()):
        print(f"  {outcome}: {count}")

    if matter_failures:
        print(f"\nMatter Resolution Failures ({len(matter_failures)}):")
        for failure in matter_failures:
            matches_info = f" ambiguous={failure['matches']}" if failure['matches'] else ""
            print(f"  thread={failure['thread_id']} matter={failure['matter_number']} proposal={failure['proposal']}{matches_info}")

    print(f"===================")

    return {
        'batch_id': batch_id,
        'executed_count': executed_count,
        'archived_count': archived_count,
        'errors': errors,
        'halted': False,
        'state_transition_counts': dict(state_transition_counts),
        'matter_outcome_counts': dict(matter_outcome_counts),
        'matter_failures': matter_failures
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python apply_batch.py <batch_proposal_file.json>")
        print("\nThis will execute the batch proposal from the specified file.")
        print("The batch proposal file should be generated by batch_classifier.py")
        sys.exit(1)

    batch_file = sys.argv[1]

    if not os.path.exists(batch_file):
        print(f"Error: File not found: {batch_file}")
        sys.exit(1)

    # Load batch proposal
    with open(batch_file, 'r') as f:
        batch_data = json.load(f)

    batch_id = batch_data.get('batch_id')

    if not batch_id:
        print("Error: Batch file missing 'batch_id' field")
        sys.exit(1)

    # Confirm execution
    print(f"Batch ID: {batch_id}")
    print(f"Threads to process: {batch_data.get('batch_size', len(batch_data.get('threads', [])))}")
    print("\nThis will apply labels and potentially archive threads.")
    confirm = input("Proceed with execution? (yes/no): ")

    if confirm.lower() != 'yes':
        print("Execution cancelled.")
        sys.exit(0)

    # Execute batch
    result = apply_approved_batch(batch_data, batch_id)

    # Save execution summary
    _EXECUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    summary_file = _EXECUTIONS_DIR / f"batch_execution_{batch_id}.json"
    with open(summary_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"\nExecution summary saved to: {summary_file}")
