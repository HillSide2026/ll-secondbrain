# Gmail Label Audit Log Format

**File:** `06_RUNS/ops/gmail_label_audit.ndjson`

Each line is a JSON object with the following fields:

- message_id
- gmail_thread_id
- label_applied_or_removed
- matter_id
- operation (add | remove)
- timestamp (UTC, ISO-8601)
- approving_human
- approval_artifact_reference
- reason
- status (ok | refused | failed)
- error (optional)
