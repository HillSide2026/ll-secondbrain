---
id: PRO-018
title: Inbox Soft Junk Cleanup Protocol
owner: ML1
status: draft
approval: pending
approved_by: ~
project: LLP-006
version: 0.1
created_date: 2026-03-14
last_updated: 2026-03-14
tags: [protocol, gmail, inbox, cleanup, soft-junk]
---

# PRO-018 — Inbox Soft Junk Cleanup Protocol

Enforces Policy: POL-042

> **DRAFT — PENDING ML1 APPROVAL.**
> This protocol has not been approved and is not in effect.
> No cleanup operations, inbox removal, or bulk sender execution may be run
> under this protocol until ML1 approves and sets `status: active`.

---

## 1. Purpose

This protocol governs the inbox admin lane for non-matter cleanup.

It defines:

1. how soft-junk candidates are identified
2. the matter-first rule that prevents cleanup from overriding matter routing
3. the confirmed sender cleanup lists used for bulk cleanup
4. the approval and audit requirements for inbox cleanup actions

This protocol is separate from `PRO-014`, which governs inbox state and matter
management.

---

## 2. Scope

This protocol applies to Gmail inbox cleanup for:

- `matthew@levinelegal.ca`
- `matthew@levine-law.ca`

It governs:

- category-driven soft-junk review
- confirmed sender cleanup lists
- ML1-directed trash and archive cleanup operations

It does not govern:

- canonical state labels
- matter label structure
- matter-routing logic
- state exclusivity enforcement

Those are governed by `PRO-014`.

---

## 3. Terminology

| Term | Definition |
|------|------------|
| **Soft junk** | Non-matter inbox content that is low-value, promotional, social, forum-based, or otherwise cleanup-oriented rather than matter-related. |
| **Soft-junk cleanup candidate** | A thread reported for cleanup review under this protocol. Reporting does not itself authorize inbox removal. |
| **Confirmed noise sender** | A sender or sender group that ML1 has designated as trash-class. |
| **Confirmed archive sender** | A sender or sender group that ML1 has designated as archive-class. |

---

## 4. Identification Rules

### 4.1 Matter-first rule

Inbox cleanup must never override matter management.

Before a category-driven cleanup action is proposed:

1. Check whether the thread already carries a canonical matter label.
2. Check whether the thread deterministically resolves to an active matter using
   the approved matter-routing signals from `PRO-014`.
3. If the thread belongs to a matter, route it back into the `PRO-014` lane for
   matter and state handling.
4. Only non-matter threads may proceed as cleanup candidates under this protocol.

### 4.2 Gmail category-driven soft junk

Gmail category labels are cleanup signals only. They are not evidence that a
thread has already been classified.

If a thread is:

- in `INBOX`
- carries `CATEGORY_PROMOTIONS`, `CATEGORY_SOCIAL`, or `CATEGORY_FORUMS`
- and does not belong to a matter

then it should be reported as a **soft-junk cleanup candidate**.

Default action:

- report only
- do not archive
- do not delete
- do not remove `INBOX`

### 4.3 Confirmed noise senders (trash-class)

The following senders have been confirmed as noise by ML1 (2026-03-14). Emails from these
senders may be trashed during cleanup operations.

- `support@systemsandteams.com`
- `news@bizbuysell.com`
- `noreply@medium.com`, `newsletters@medium.com`, `hello@medium.com`
- `david.a@plantationsinternational.com`
- `notifications@account.brilliant.org`
- `bettiegram@backofficebetties.com`
- `email@e.lucid.co`
- `noreply@skool.com`
- `iwoszapar@user.luma-mail.com`
- `support@epicnetwork.com`
- `info@vivaglobal.us`
- `communications@riskintelligence.lseg.com`
- `communications@bnaibrith.ca`
- `sales@infowisesolutions.com`
- `team@weargustin.com`
- `Windows365@mails.microsoft.com`
- `teamzoom@zoom.us`
- `customer-success-advisor@zoom.us`
- `noreply@youtube.com`
- `no-reply@mail.instagram.com`
- `TDSurvey@feedback-td.com`

### 4.4 Confirmed archive senders (archive-class)

The following senders have been confirmed as low-value but retainable by ML1 (2026-03-14).
Emails from these senders may be archived during cleanup operations.

- `messaging@promo.lexisnexis.ca`, `experts@lawpay.info`
- `info@ontario-commercial.com`, `support@ontario-commercial.com`
- `marketing@getappara.ai`
- `bruna@legalboards.com`
- `inquiries-portagemaadvisory.ca@shared1.ccsend.com`
- `dbaskin@baskinwealth.com`
- `jprekaski@fbc.ca`
- `notifications-noreply@linkedin.com`, `linkedin@e.linkedin.com`,
  `messages-noreply@linkedin.com`, `jobs-listings@linkedin.com`

---

## 5. Execution Rules

### 5.1 Default mode

The default mode for soft-junk cleanup is proposal-only.

Proposal outputs may include:

- thread id
- sender
- subject
- Gmail category labels
- cleanup class (`soft_junk`, `trash_class`, `archive_class`)

### 5.2 Prohibited actions without explicit instruction

Without explicit ML1 instruction, the system must not:

- archive a soft-junk cleanup candidate
- trash a soft-junk cleanup candidate
- delete any message
- remove `INBOX`

### 5.3 ML1-directed cleanup execution

ML1 may authorize direct cleanup execution for:

- confirmed noise senders
- confirmed archive senders
- explicitly approved soft-junk cleanup candidate sets

Such operations must be logged to:

- `06_RUNS/logs/inbox_cleanup.log`
- any applicable Gmail audit artifact for the execution path used
- substantive review / approval / execution artifacts under
  `06_RUNS/INBOX_GOVERNANCE/PRO-018_SOFT_JUNK/`

---

## 6. Audit and Review

Cleanup reviews should retain:

- the query used
- the candidate set generated
- the approval reference, if execution occurred
- the execution counts for trash/archive actions

Canonical storage location for substantive `PRO-018` artifacts:

- `06_RUNS/INBOX_GOVERNANCE/PRO-018_SOFT_JUNK/reviews/`
- `06_RUNS/INBOX_GOVERNANCE/PRO-018_SOFT_JUNK/approvals/`
- `06_RUNS/INBOX_GOVERNANCE/PRO-018_SOFT_JUNK/executions/`

If a thread later proves to belong to a matter, cleanup routing must stop and the
thread must be handled under `PRO-014`.

---

## 7. Related Doctrine

- `POL-042` Inbox Governance Policy
- `PRO-014` Inbox State and Matter Management Protocol

---

## 8. Change Log

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-03-14 | Initial split-out protocol for inbox soft-junk cleanup. Separates category-driven cleanup and confirmed sender cleanup from `PRO-014`. |
