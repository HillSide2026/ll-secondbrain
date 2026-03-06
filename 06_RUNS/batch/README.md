# 06_RUNS/batch

Machine-generated run artifacts from the LL Inbox Governance batch classification system.

## Directory structure

```
06_RUNS/batch/
├── proposals/      # Proposed batch actions — generated before execution, require Sponsor approval
└── executions/     # Completed execution outputs — written after a proposal is applied
```

## Lifecycle

1. `gmail_governance/batch_classifier.py` generates a **proposal** (`batch_proposal_{timestamp}.json`) and writes it to `proposals/`.
2. Sponsor reviews and approves the proposal (may patch individual thread classifications).
3. `gmail_governance/apply_batch.py <path/to/proposal.json>` executes the approved proposal and writes the corresponding **execution record** (`batch_execution_{timestamp}.json`) to `executions/`.

## File naming

Both files share the same `{timestamp}` batch ID (format: `YYYYMMDD_HHMMSS`), making proposal/execution pairs easy to correlate.

## Contents

| File type | Key fields |
|---|---|
| Proposal | `batch_id`, `threads[]` with `proposed_label`, `proposed_matter_label` |
| Execution | `batch_id`, per-thread `state`, `archived`, `matter_outcome`, run summary counters |

## Notes

- Proposals are read-only until approved. Patching a proposal before execution is expected and documented.
- Execution records are append-only audit artifacts. Do not edit after the fact.
- The `gmail_governance/execution_log.json` is a separate rolling log distinct from these per-batch records.
