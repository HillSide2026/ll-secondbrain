---
id: backlog-cleanup-agent-workflow-spec
title: Workflow Spec — Backlog Cleanup Agent v0.1
owner: ML1
status: approved
approved_by: ML1
approved_date: 2026-04-16
version: 0.1
tags: [inbox, cleanup, backlog, gmail]
---

# Workflow Spec — Backlog Cleanup Agent v0.1

## Status

Approved. Execution owner: ML2. System runtime.

## Architecture

Rule engine handles ~80–95% of backlog (near-zero LLM cost).
AI touches ambiguous residue only.
Default = leave untouched.

## Workflow

### Step 0 — Scope Filter

Process only:
- Emails older than X days (open decision — see Known Gaps)
- Inbox only
- Include categories: Promotions, Updates, Forums, Social
- Exclude: Archived, Sent

### Step 1 — Protected Set (Hard Exclusions)

SKIP if ANY true:
- Sender in VIP list
- Sender in client list
- Sender in opposing counsel list
- Thread starred or flagged
- Thread already manually labeled
- Thread has recent reply activity
- Thread linked to a matter

### Step 2 — Deterministic Archive Rules (No LLM)

ARCHIVE if ANY true:
- Sender pattern: `no-reply@`, `notifications@`, `updates@`
- Gmail category: newsletters, marketing, promotions, receipts, system alerts
- Bulk headers present (List-ID, Precedence: bulk)
- Unsubscribe link present
- Transactional format (order confirmation, receipt, etc.)

### Step 3 — Ambiguity Gate (Minimal AI)

Only if: not protected AND not caught by rules.

Pass to lightweight classifier. Output:
- `likely_human_relevant` → KEEP
- `likely_low_value` → ARCHIVE
- `uncertain` → KEEP

Default bias: KEEP.

### Step 4 — Action + Logging

For every processed thread:
- action taken (archive / skip)
- rule or classifier reason
- timestamp
- run_id

## Policy Constraints

Allowed: archive only (remove INBOX label).

Forbidden:
- Delete
- Spam marking
- Unsubscribe
- Label mutation (except optional `processed_cleanup` system tag)
- Any action under uncertainty

## Rollout Plan

### Phase 1 — Dry Run
- No archiving
- Log what WOULD happen
- Sample 100–200 threads

### Phase 2 — Limited Live
- Enable archive
- Restrict to: newsletters, receipts, notifications
- Cap: 200–500 threads/run

## Metrics (Per Run)

- % archived vs skipped
- false positives (manual review sample)
- cost per 1k threads
- % requiring classifier
- backlog reduction rate

## Known Gaps — Require ML1 Input

| Decision | Options | Recommended |
|---|---|---|
| Backlog window | 30 days / 60 days / full history | TBD |
| VIP / protected list source | Static list vs domain-based | TBD |
| Classifier threshold | Aggressive vs conservative | TBD |
| Uncertain handling | Always keep vs queue for review | Always keep |

## Do-Not-Answer Zone

This system does NOT:
- decide email importance beyond defined rules
- infer legal relevance
- replace human judgment on edge cases
