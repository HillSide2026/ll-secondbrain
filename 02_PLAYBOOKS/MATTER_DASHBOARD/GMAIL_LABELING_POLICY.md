---
id: 02_playbooks__matter_dashboard__gmail_labeling_policy_md
title: Gmail Matter Labeling Policy — Stage 2.13
owner: ML1
status: draft
created_date: 2026-02-09
last_updated: 2026-02-09
tags: []
---

# Gmail Matter Labeling Policy — Stage 2.13

## Purpose
Define the deterministic rules and guardrails for applying matter-number labels to Gmail messages.

## Label Naming
- Format: `LL/1./<delivery_status>/<matter_id>`
  - Example: `LL/1./1.1 - Essential/25-927-00003`
- Labels are created on demand at first authorized use
- Label deletion is prohibited (labels may only be added to or removed from messages)

## Eligibility (Deterministic Attribution)
A message is eligible for labeling only if it is deterministically associated to a matter via an approved structured source:
- Pre-approved participant mapping table
- Prior authoritative linkage (e.g., thread-level mapping)

Free-text inference is prohibited.

## Allowed Operations
- Add label to message
- Remove label from message

No other Gmail write operations are allowed.

## Approval Gate
- A human approval artifact is required per run
- Absence of approval artifact blocks execution

## Audit Logging
Every label write must be logged with:
- message_id
- gmail_thread_id
- label
- matter_id
- operation (add|remove)
- timestamp (UTC, ISO-8601)
- approving_human
- approval_artifact_reference
- reason
