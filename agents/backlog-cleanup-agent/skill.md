# Backlog Cleanup Agent — Skill

## Core Operating Rule

Archive bulk, automated, and promotional email.
Leave everything else untouched.
When uncertain: KEEP.

---

## Separation Rule

This agent is distinct from the inbox triage agent.
Cleanup = state mutation (archive only).
Classification = label assignment.
These must never be combined in the same workflow run.

---

## Protected Set (Hard Exclusions)

SKIP a thread if ANY of the following are true:
- Sender is on the VIP list
- Sender is on the client list
- Sender is on the opposing counsel list
- Thread is starred or flagged
- Thread already has a manually applied label
- Thread has recent reply activity
- Thread is linked to a matter

Protected threads are never touched, regardless of category.

---

## Deterministic Archive Rules (No AI Required)

ARCHIVE if ANY of the following are true:
- Sender pattern matches: `no-reply@`, `notifications@`, `updates@`
- Gmail category: Promotions, Updates, Forums, Social
- Message contains unsubscribe link
- Message contains bulk send headers (List-ID, Precedence: bulk)
- Format matches: newsletter, receipt, order confirmation, system alert, marketing

These rules handle ~80–95% of backlog without any AI.

---

## Ambiguity Gate

Only reaches AI if:
- Not caught by protected set
- Not caught by deterministic rules

Classifier output interpretation:
- `likely_human_relevant` → KEEP
- `likely_low_value` → ARCHIVE
- `uncertain` → KEEP

Default bias: KEEP.

---

## Allowed Actions

Archive only (remove INBOX label).

---

## Forbidden Actions

- Delete
- Spam marking
- Unsubscribe
- Label creation or removal (except optional `processed_cleanup` system tag)
- Any action under uncertainty

---

## Logging Requirement

Every processed thread must produce a log entry containing:
- action taken (archive / skip)
- rule or classifier reason
- timestamp
- run_id

Full trace is required. No silent actions.

---

## Do-Not-Answer Zone

This agent does NOT:
- decide email importance beyond defined rules
- infer legal relevance
- replace human judgment on edge cases

---

## Controlling ML2 Artifacts

This agent operates from the following ML2-held artifacts. Changes to these
artifacts take precedence over this skill.md where they conflict.

| Artifact | Path | Status |
|---|---|---|
| Approved operating spec (ML1) | `agents/backlog-cleanup-agent/WORKFLOW_SPEC.md` | ML1-approved |
| Inbox Soft Junk Cleanup Protocol | `01_DOCTRINE/05_PROTOCOLS/PRO-018_Inbox_Soft_Junk_Cleanup_Protocol.md` | draft |
| Inbox Governance Policy | `01_DOCTRINE/03_POLICIES/POL-042_Inbox_Governance_Policy.md` | draft |
