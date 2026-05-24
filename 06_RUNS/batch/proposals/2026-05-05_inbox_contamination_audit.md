---
id: batch_proposal__2026_05_05_inbox_contamination_audit
title: Pass A — Inbox Contamination Audit
type: proposal
status: awaiting_ml1_approval
created_date: 2026-05-05
proposed_action: archive
labels_audited: 10
labels_contaminated: 7
labels_clean: 3
owner: ML2
last_updated: 2026-05-24
tags: []
---

# Pass A — Inbox Contamination Audit

**Date:** 2026-05-05  
**Step:** 1 of 4 (read-only audit)  
**Proposed action:** Archive all confirmed contaminated threads (remove inbox flag; preserve labels)  
**Execution:** Pending ML1 approval

---

## Summary

A read-only audit query was run against all 10 state labels. A thread is
contaminated if it is simultaneously `in:inbox` AND carries a state label.
Inbox presence + state label = contradiction under the governing rule.

---

## Label-by-Label Results

| Label | First Page Threads | Paginated? | Status |
|---|---|---|---|
| `00_Triage` | 50 | Yes — more pages | Contaminated |
| `10_Action_Matthew` | 50 | Yes — more pages | Contaminated |
| `20_Action_Team` | 0 | — | **Clean** |
| `30_Waiting_External` | 0 | — | **Clean** |
| `40_Replied_Awaiting_Response` | 50 | Yes — more pages | Contaminated + **label accuracy flag** |
| `50_Calendar` | 11 | Yes — more pages | Contaminated |
| `60_Filing` | 12 | No | Contaminated |
| `70_Filed` | 0 | — | **Clean** |
| `80_Junk_to_Review` | 7 | No | Contaminated |
| `90_Archive` | 50 | Yes — more pages | Contaminated |

**Clean labels (no Pass A action needed):** `20_Action_Team`, `30_Waiting_External`, `70_Filed`

**Minimum confirmed contaminated threads:** 180+ across first pages only.  
**Full scope:** Several hundred threads once pagination is completed for the four large labels.

---

## Flag — Label Accuracy Problem (Pass B Priority)

`40_Replied_Awaiting_Response` returned 50+ Google Calendar notification emails
(from `calendar-notification@google.com`, subjects: LLA 1, LLA 2, LLA 3, LLA 4,
LLA 5, LLA 6, Open Office, Firm Management, LL Lunch, etc.).

These are automated calendar reminder emails. They should not carry the label
`40_Replied_Awaiting_Response`. This is a label accuracy error at scale —
the label implies a human replied and is awaiting a response, which does not
apply to calendar notifications.

**Pass A action still applies:** Archive them (they are in inbox + labeled = contradiction).  
**Pass B action required:** Relabel these threads correctly (likely `50_Calendar` or `90_Archive`).

---

## Sample Contaminated Threads — 00_Triage (first page)

| Thread ID | Subject | Sender |
|---|---|---|
| 19df9e091d9ab710 | [Nikko Discovery] Some plugins were automatically updated | wordpress@nikkodiscovery.com |
| 19df9c2f4d4ad473 | Alessandra P. Goulet has joined your meeting | no-reply@zoom.us |
| 19df99fdcfd8077b | Connect | basit_ahmad@cooperators.ca |
| 19df996319333afe | New missed call from Joana A. Malheiro | voice-noreply@google.com |
| 19df960d673edadc | QUICK FIX: Add more contact options to your ads | ads-noreply@google.com |
| 19df85831acbc7dc | Interac e-Transfer: Dina Moore accepted $811.07 | catch@payments.interac.ca |
| 19df4d2d67c575e9 | prenuptial agreement (thread w/ Alessandra Goulet) | matthew@levinelegal.ca |
| 19df8484ddf3fa51 | FINTRAC announces administrative monetary penalties | fintrac.canafe@notification.canada.ca |

*50 threads total on first page; additional pages not retrieved.*

---

## Sample Contaminated Threads — 10_Action_Matthew (first page)

| Thread ID | Subject | Sender |
|---|---|---|
| 19df9401b0b0f739 | Lien dispute (referral) — auto-reply | JRoutliff@rousseaumazzuca.com |
| 19df90c284b18aa2 | FW: Call Back (Carpenters) | Neera@rousseaumazzuca.com |
| 19df86642046ab66 | Lien dispute (referral) — AllPro | JRoutliff@rousseaumazzuca.com |
| 19de3e08815b4726 | ATTENTION! Migration to Microsoft 365 — Stream | gevorkg@stream.money |
| 19de288c813625eb | Fwd: FW: Request for Additional Documentation — Stream | tulika.d@stream.money |
| 19dde8aa30447d10 | Schedule your Docusign Onboarding Call — Stream | reem.elhadidy@docusign.com |
| 19dd597b76a481d5 | Re: RPAA | harry@stream.money |
| 19dc52dfdd5de5dd | Meeting to Discuss Next Steps (Laura Hinton / Stream) | laura@levine-law.ca |

*50 threads total on first page; additional pages not retrieved.*

---

## Sample Contaminated Threads — 80_Junk_to_Review (complete — 7 threads)

| Thread ID | Subject | Sender |
|---|---|---|
| 19df804fe71c8c19 | 🦞 Anthropic Overplays Mythos Risk | MyClaw@aisecret.us |
| 19df2df9d7cc920e | 🦞 OpenClaw Abused at Scale | MyClaw@aisecret.us |
| 19de36aeadf2d720 | 🦞 Software 3.0 Arrives | MyClaw@aisecret.us |
| 19dde447db43c058 | 🦞 Headless SaaS Wave | MyClaw@aisecret.us |
| 19dd91ebc6340fd6 | 🦞 Memes Became Cashflow | MyClaw@aisecret.us |
| 19dd3f92569b2c33 | 🦞 Only Nonlinear Work Survives | MyClaw@aisecret.us |
| 19dba389b3302be0 | 🦞 Chinese Workers Train Replacements | MyClaw@aisecret.us |

All 7 are MyClaw newsletter duplicates (sent to both matthew@levinelegal.ca and
matthew@levine-law.ca, appearing as separate threads). Safe to archive.

---

## Sample Contaminated Threads — 60_Filing (complete — 12 threads)

| Thread ID | Subject | Sender |
|---|---|---|
| 19dd8e29ca3f8862 | FCA EMI Authorisa... @harry@stream.money — Google Docs comment | comments-noreply@docs.google.com |
| 19dcb492bad8ed7e | CREATE: Custom Records in Clio [26-927-00004 - Stream] | no-reply@asana.com |
| 19dcb3b26c73655e | CREATE: Custom Records in Clio [26-1639-00003 - Andersen] | no-reply@asana.com |
| 19dab5d58e5ce7e7 | New email from Chris Roop | noreply@donotreply.soulpepper.com |
| 19d9c516c61b57fe | New email from Chris Roop | noreply@donotreply.soulpepper.com |
| 19d9aaf4c23f0f2c | Spreadsheet shared: Stream Money Project Plan | drive-shares-dm-noreply@google.com |
| 19d9950a190f721b | New email from Chris Roop | noreply@donotreply.soulpepper.com |
| 19d921e29144176e | Payment plan installment submitted — Stream | notifications@clio.com |
| 19d1bcd25fc6a5e7 | Matthew, did you forget to send your comment — Asana | no-reply@asana.com |
| 19cb0fe6128a77f4 | Your document has been signed by all signers — Clio | notifications@clio.com |
| 19cb0fd8a688dad7 | YCI Exit signature requested | noreply@mail.hellosign.com |

*Note: Three "New email from Chris Roop" threads (Soulpepper notifications) — likely label accuracy candidates for Pass B.*

---

## Proposed Execution Scope

**Pass A Step 2 (pending ML1 approval):**

1. Retrieve all pages for the four paginated labels:
   - `00_Triage` (page 1 retrieved; continue from nextPageToken `16602271585409144445`)
   - `10_Action_Matthew` (page 1 retrieved; continue from nextPageToken `05656077084473613408`)
   - `40_Replied_Awaiting_Response` (page 1 retrieved; continue from nextPageToken `12551739852887977144`)
   - `90_Archive` (page 1 retrieved; continue from nextPageToken `00339461725200115252`)
   - `50_Calendar` (page 1 retrieved; continue from nextPageToken — to be retrieved)

2. Compile full thread ID list.

3. Archive all threads (remove INBOX label via Gmail API).

4. Write execution artifact to `06_RUNS/batch/executions/2026-05-05_inbox_contamination.json`.

---

## ML1 Decision Required

- Approve Pass A execution scope (all 7 contaminated labels)?
- Any threads to exclude from archiving before execution?
- Confirm Pass B priority: `40_Replied_Awaiting_Response` calendar notification
  relabeling to be addressed first?
