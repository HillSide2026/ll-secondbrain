---
id: STANDING-APPROVAL-PRO018-DAILY-2026-04-19
title: Standing ML1 Approval — PRO-018 Daily Automated Cleanup
approved_by: ML1
approved_date: 2026-04-19
scope: deterministic-rules-only
policy: POL-042
protocol: PRO-018
script: scripts/backlog_cleanup_agent.py
status: active
---

# Standing Approval — PRO-018 Daily Automated Cleanup

## Approval

ML1 grants standing approval for daily automated execution of the PRO-018 backlog cleanup agent under the following conditions.

## Scope

This approval covers deterministic-rule-only archiving (Phase 2). It does NOT cover AI-assisted or ambiguous classification.

Threads are archived only if they match one or more of the following deterministic rules:

- Sender pattern matches: `no-reply@`, `noreply@`, `notifications@`, `updates@`, `newsletter@`, `donotreply@`, `do-not-reply@`, `mailer@`, `bounce@`, `automated@`, `automailer@`
- Gmail category: `CATEGORY_PROMOTIONS` or `CATEGORY_UPDATES`
- Bulk send headers present: `List-ID`, `List-Unsubscribe`, or `Precedence: bulk/list/junk`
- Unsubscribe link present in snippet

## Protected Set (Hard Exclusions — Never Touched)

- Starred or flagged threads
- Threads with a matter label (`LL/` prefix)
- Threads with recent reply activity (within 14 days)

## Execution Parameters

| Parameter | Value |
|---|---|
| Phase | 2 (live) |
| Max threads per run | 500 |
| Backlog window | 1 day (threads older than 24 hours) |
| Action | Archive only (remove INBOX label) |
| Delete | Forbidden |
| Spam marking | Forbidden |
| Label mutation | Forbidden |

## Schedule

Daily at 07:00 local time, every day.

## Audit

Every run produces a full trace log in `06_RUNS/ops/backlog_cleanup/` with action, reason, timestamp, and run_id for every processed thread.

## Revocation

This standing approval is revoked by updating `status` to `revoked` in this file frontmatter, or by superseding with a new approval artifact.
