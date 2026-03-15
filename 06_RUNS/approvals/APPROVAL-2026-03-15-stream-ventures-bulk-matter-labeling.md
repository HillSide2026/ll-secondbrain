---
id: APPROVAL-2026-03-15-stream-ventures-bulk-matter-labeling
title: Approval — Bulk Matter Labeling — Stream Ventures / SnowCap Financial (2026 Threads)
type: label_write_approval
status: PENDING_ML1_APPROVAL
created: 2026-03-15
owner: ML1
---

# Approval — Stream Ventures Bulk Matter Labeling (2026)

## Purpose

Authorize bulk application of Stream Ventures matter labels to 2026 Gmail inbox threads
that are currently unlabeled. Live inbox audit conducted 2026-03-15 via gmail_mcp_server.py
after OAuth token refresh.

## Finding

A live Gmail query found **68 unique Stream-related threads** from 2026.
**Zero threads have any matter label applied.**

Prior labeling (batch_proposal_20260303_184542.json) was never executed — threads show
no LL/ label in the live Gmail mailbox.

## Proposed Label Actions

### Group A — Matter 25-927-00003 (Stream Ventures Limited — Essential)
**Label:** `LL/1./1.1/25-927-00003 -- Stream Ventures Limited`
**Gmail Label ID:** `Label_68`

All threads from stream.money senders + directly related operational/SnowCap discussions.
**Thread count:** 62 threads

Representative threads:
- `19ce3e9e4c82f91e` Re: [Ext Sender] commercial bank account (Harry Bedi)
- `19ce7be54280572c` Invitation: Ops Risk Policy- Matthew/Tulika (Tulika Dhar)
- `19ce379f7add4471` Re: SnowCap AML Policy (Harry Bedi)
- `19cdddea1bb63310` Re: Snowcap FInancial - Bank Account (Harry Bedi)
- `19cd31b99d866735` Fwd: FAQ - Equals money (Tulika Dhar)
- `19cb8c2e8f63faec` Re: Equals Money and Stream Money White Label Agreement Review
- `19cbe08186285d0d` Re: Verto - SnowCap shareholding structure
- `19cc1b78203a1ab0` Trust Ledger Report – Stream Ventures Limited
- `19cedca3a9c9f35c` Asana: REVIEW Signed AML Doc Snowcap [25-927-00003]
- `19cf15e4c2ce2d70` Notification: Stream x Innowise
- `19c7a541b6e0eadc` Accepted: Compliance & Legal Chat (Tulika)
- `19c8094882db02ce` Invitation: Snowcap Run Through
- `19c8b275b5366fd9` Stream Money / Elliptic - Mid Trial Check in
- `19c9f639faa3d8a7` Re: AML Policy Request (James Hayes)
- `19c9a7c11cdf1c8c` Re: Document shared: Global Onboarding Analyst_Draft
- `19cd2d7d50dc0403` Stream x Marble (checkmarble.com)
- `19cd2ddbc2727896` RE: Industry Risk Profile Documentation (equalsmoney.com)
- `19cc3a89d1969354` Fwd: Utility bill (Harry Bedi)
- `19cba05361e91c1c` Re: Pricing Information (Gevork Grigorian)
- `19cba814f66c6368` Asana: HANDLE Verto <> Stream <> Snowcap Financial
- (and all remaining stream.money sender threads from 2026)

### Group B — Matter 26-927-00004 (Stream Ventures Limited — Counsel)
**Label:** `LL/1./1.1/26-927-00004 -- Stream Ventures Limited`
**Gmail Label ID:** `Label_72`

Thread count: 2 threads

- `19cd24a5fd6165d9` RE: Contract review and advice [Hamlins-DMS.S0184991.5] (Harmony Kennedy, hamlins.com — sent to matthew@stream.money)
- `19cce4e591fed4cb` Asana: REVIEW KYC Docs [26-927-00004 - Stream Ventures] (Asana explicitly tags 26-927-00004)

### Group C — Matter 24-682-00002 (Stream Ventures Limited — Acquisition, Parked)
**Label:** `LL/1./1.4/24-682-00002 -- Stream Ventures Limited`
**Gmail Label ID:** `Label_89`

Thread count: 1 thread

- `19c8b43fe130cbb1` Asana: ATTEND Feb. 24 Meeting [24-682-00002 - Stream Ventures] (Asana explicitly tags 24-682-00002)

### Group D — Ambiguous / Requires ML1 Judgment
These threads relate to Stream Ventures but routing is unclear:

- `19c1aeb7f729fbed` "Canadian Accountant" — Matthew to Sonia Bedi (sbedi@berkeley-ig.com), 10-message thread — likely 25-927-00003 but requires ML1 confirmation
- `19c9a08fda2dfc4d` "Resubmission of Trust Request TR2761" — firm to sbedi@berkeley-ig.com — likely 25-927-00003 but confirm

### Group E — Exclude (not matter-specific)
- `19ce7491723664aa` Asana overdue tasks summary (generic)
- `19ce7b472ffe7245` Asana weekly tasks summary (generic)
- `19cc48c44e94f945` Security alert for matthew@stream.money (Google account security, informational)

## Recommended Query Strategy for Bulk Application

Rather than thread-by-thread, use `apply_matter_label_query` with:

**Group A:**
```
query: in:inbox from:(stream.money OR snowcap.com) after:2026/01/01
```

**Group B (thread-by-thread):**
```
thread_ids: [19cd24a5fd6165d9, 19cce4e591fed4cb]
```

**Group C (thread-by-thread):**
```
thread_ids: [19c8b43fe130cbb1]
```

## Approval Required

- [ ] ML1 approves Group A labeling (25-927-00003, stream.money senders)
- [ ] ML1 approves Group B labeling (26-927-00004, Hamlins + KYC)
- [ ] ML1 approves Group C labeling (24-682-00002, Feb24 meeting)
- [ ] ML1 confirms routing for Group D (ambiguous threads)
- [ ] ML1 confirms exclusion of Group E

**No label writes will occur until this document is confirmed by ML1.**
