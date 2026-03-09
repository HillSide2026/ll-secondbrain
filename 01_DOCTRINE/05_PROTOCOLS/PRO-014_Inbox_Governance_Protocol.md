---
id: PRO-014
title: Inbox Governance Protocol
owner: ML1
status: draft
approval: pending
approved_by: ~
project: LLP-006
version: 0.2
created_date: 2026-03-07
last_updated: 2026-03-09
tags: [protocol, gmail, inbox, labeling, classification, legalmatters, clio]
---

# PRO-014 — Inbox Governance Protocol

Enforces Policy: POL-042

> **DRAFT — PENDING ML1 APPROVAL.**
> This protocol has not been approved and is not in effect.
> No labeling operations, batch executions, or automated classifications
> may be run under this protocol until ML1 approves and sets `status: active`.

---

## 1. Purpose

This protocol defines:

1. The canonical label taxonomy applied to Gmail threads in the LL inbox.
2. The classification signals used to assign state and matter labels to threads.
3. The approval gate required before any label is written to Gmail.
4. The agent access rules that govern inbox data within secondbrain.

**Objective:** The ultimate goal of inbox governance is to ensure that every matter-related
email is linked to its corresponding legal matter — both as a Clio matter reference and,
where applicable, as a SharePoint LegalMatters folder. This protocol operates in two phases:

- **Interim (current):** Tag emails within Gmail with the relevant legal matter / Clio matter
  number, using the label hierarchy defined in Section 4. This establishes a traceable
  matter-thread link without moving or copying email content.
- **Future:** Route or file emails from the inbox to the relevant matter record in SharePoint
  LegalMatters, once cross-system linking is in scope (see LLP-005).

The protocol applies to the Gmail account(s) associated with `matthew@levinelegal.ca`
and `matthew@levine-law.ca`. It does not govern Google Calendar or SharePoint directly
(those systems are addressed in separate protocols or are pending).

---

## 2. Terminology

| Term | Definition |
|------|------------|
| **State label** | A canonical label expressing the action state of a thread (e.g., `10_Action_Matthew`). Only one state label may be applied to a thread at a time. |
| **Matter label** | A hierarchical label linking a thread to a matter number (e.g., `LL/1./1.1 - Essential/25-1593-00001`). |
| **Triage** | The process of reviewing unclassified threads and assigning state and/or matter labels. |
| **Batch proposal** | A machine-generated list of proposed label changes, not yet applied. Requires ML1 approval before execution. |
| **Execution** | Applying approved label changes to Gmail via the API. |

---

## 3. Canonical State Labels

Exactly one state label must be applied to each thread. State labels are mutually exclusive.

| Label | Meaning |
|-------|---------|
| `00_Triage` | Received; not yet reviewed. Default state for new threads. |
| `10_Action_Matthew` | Requires ML1 action. |
| `20_Action_Team` | Delegated to team member. |
| `30_Waiting_External` | Waiting on external party (counterparty, court, government). |
| `40_Replied_Awaiting_Response` | ML1 has replied; awaiting response. |
| `50_Calendar` | Thread is calendar-related; no separate action. |
| `60_Filing` | Thread requires filing in SharePoint or Clio; no separate action. |
| `70_Filed` | Thread has been filed; no further action required. |
| `80_Junk (Pending Review)` | Suspected low-value or junk; flagged for ML1 review before archiving. |
| `90_Archive` | No further action required. |

**Enforcement rule:** Any thread carrying more than one state label is in violation.
The enforcement script (`state_enforcement.py`) detects and reports these violations
but does not resolve them without ML1 approval.

---

## 4. Matter Label Structure

The canonical matter identifier is the **Clio matter ID**, which takes the form:

```
\d{2}-\d{3,4}-\d{5}  (e.g., 25-1593-00001)
```

This ID is the authoritative cross-system reference key linking a Gmail thread to:
- the corresponding Clio matter record, and
- the corresponding SharePoint LegalMatters folder (where the filing structure has been implemented).

Matter labels follow the hierarchy:

```
LL/
└── {tier_number}./ (e.g., 1. or 2.)
    └── {tier_name}/ (e.g., 1.1 - Essential)
        └── {clio_matter_id}  (e.g., 25-1593-00001)
```

A thread may carry at most one matter label. If a thread relates to multiple matters,
it is flagged for ML1 manual assignment.

---

## 5. Classification Signals

### 5.1 State classification signals (in priority order)

| Signal | State assigned | Notes |
|--------|---------------|-------|
| Thread sender domain in `TEAM_SENDERS` | `20_Action_Team` | Lino, Grace, levinelegalservices.com |
| Thread sender domain in `ADMIN_SENDERS` | `20_Action_Team` | Telus, Regus, Amazon, etc. |
| Thread sender domain in `LEGAL_SENDERS` | `10_Action_Matthew` | CRA, counterparty counsel, courts |
| Automated sender signal (noreply, no-reply, donotreply, notifications@) | `90_Archive` (candidate) | Flag for ML1 review before applying |
| ML1 is sender (outbound thread) | `40_Replied_Awaiting_Response` | ml1 is in `MATTHEW_EMAILS` |
| No signal matches | `00_Triage` | Default — requires manual review |

**Note:** State signals are proposals only. No state is applied without the approval gate
(Section 7).

### 5.2 Matter classification signals (in priority order)

| Signal | Assignment | Notes |
|--------|-----------|-------|
| Matter number in existing Gmail label path | Confirmed matter label | Determinative — already labeled |
| Matter number (`\d{2}-\d{3,4}-\d{5}`) in email subject | Proposed matter label | High confidence |
| Matter number in email snippet/body | Proposed matter label | Medium confidence — flag for review |
| No matter number signal | Unmapped | Logged to `INBOX_UNMAPPED.md`; requires ML1 assignment |

### 5.3 Signals not used

| Signal | Reason excluded |
|--------|----------------|
| Sender name alone | Not unique across contacts |
| Thread age | Not a reliable classification signal |
| Email body full-text (unsupported) | Only subject and snippet are available without full message fetch |

---

## 6. Classification Procedure

For each unclassified thread (threads carrying `00_Triage` or no state label):

1. Apply state signals (Section 5.1) in priority order. Record the signal that matches.
2. Apply matter signals (Section 5.2) in priority order. Record the signal that matches.
3. Produce a batch proposal entry with:
   - `thread_id`
   - `proposed_state_label`
   - `proposed_matter_label` (if determinable)
   - `signal_basis` (which signal drove each assignment)
   - `confidence` (`high` / `medium` / `review_required`)
4. All proposals with `confidence: review_required` are excluded from automated batch execution
   and must be resolved by ML1 manually.
5. Submit the completed batch proposal to ML1 for approval before execution.

Batch proposals are written to `06_RUNS/batch/` as JSON files.
No label changes are applied to Gmail until ML1 approves via a signed approval record
in `06_RUNS/approvals/`.

---

## 7. Approval Gate

**All label writes to Gmail require prior ML1 approval.**

The approval record must specify:
- The batch file being approved (file path or hash).
- The scope of approval (all threads in batch, or specific thread IDs).
- The date of approval.
- Any exclusions or overrides.

Approval records are stored in `06_RUNS/approvals/` as Markdown files with
frontmatter `status: approved`.

The execution script (`apply_batch.py`) checks for a corresponding approval record
before writing any labels. If no approval record exists for a batch, execution is
blocked.

---

## 8. Audit and Enforcement

### 8.1 State exclusivity audit

`state_enforcement.py` scans all threads for state label exclusivity violations.
Violations are reported but not auto-resolved.

### 8.2 Matter mapping audit

`matter_enforcement.py` scans all labeled threads and verifies that matter labels
correspond to known matter numbers in secondbrain.

### 8.3 Unmapped thread log

Threads that cannot be assigned a matter label are logged to:
```
05_MATTERS/DASHBOARDS/INBOX_UNMAPPED.md
```

This file is updated on each classification run and reviewed by ML1.

---

## 9. Data Access Rules

| Data | May agent read? | May agent cite externally? | Notes |
|------|----------------|---------------------------|-------|
| Thread subject and snippet | Yes — for classification only | No | Never reproduce in external output |
| Thread body | Only via explicit ML1-approved fetch | No | Full body fetch requires separate approval |
| Sender/recipient metadata | Yes — for classification only | No | — |
| Gmail label state | Yes | No | Classification context only |

---

## 10. Scope Limitations

This protocol covers state and matter labeling of Gmail threads only.

Out of scope (pending separate protocols or manual processes):
- Google Calendar event classification
- Clio matter data integration
- SharePoint document classification (see PRO-013)
- Cross-system matter linking (Gmail ↔ Clio ↔ SharePoint)

---

## 11. Open Items (NTD)

| Item | Description |
|------|-------------|
| NTD-1 | Confirm canonical list of `TEAM_SENDERS`, `LEGAL_SENDERS`, and `ADMIN_SENDERS` — current lists in `batch_classifier.py` are working drafts |
| NTD-2 | Define handling rule for multi-matter threads |
| NTD-3 | Confirm whether `80_Junk (Pending Review)` threads are auto-proposed for `90_Archive` or held for ML1 review |
| NTD-4 | Document matter label tier structure: `LL/1./` = Delivery (lawyer/legal work); `LL/2./` = Fulfillment (team admin and accounts related to matters). Classification must match on `LL/` prefix across both tiers. |

---

## 12. Change Log

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-03-07 | Initial draft. Based on gmail_governance scripts and batch execution artifacts from 2026-02-09 to 2026-03-04. |
| 0.2 | 2026-03-09 | Clarify purpose: interim Gmail tagging to legal matter / Clio matter; future filing to SharePoint LegalMatters. Remove duplicate Section 12. Add `clio` tag. Establish Clio matter ID as canonical matter identifier in Section 4. Add POL-042 reference. |
