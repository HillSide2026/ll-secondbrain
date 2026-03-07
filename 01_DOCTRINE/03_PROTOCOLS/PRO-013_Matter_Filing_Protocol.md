---
id: PRO-013
title: Matter Filing Protocol
owner: ML1
status: draft
approval: pending
approved_by: ~
project: LLP-006
version: 0.2
created_date: 2026-03-07
last_updated: 2026-03-07
tags: [protocol, sharepoint, legalmatters, filing, provenance, classification]
---

# PRO-013 — Matter Filing Protocol

> **DRAFT — PENDING ML1 APPROVAL.**
> This protocol has not been approved and is not in effect.
> Classification rules defined here must not be implemented in any script,
> agent, or automated workflow until ML1 approves and sets `status: active`.

---

## 1. Purpose

This protocol defines:

1. The required folder structure for matter files in `levinellp.sharepoint.com/sites/LegalMatters` (Working Files drive).
2. The five provenance classes assigned to documents within that structure.
3. The classification signals used to assign provenance.
4. The agent access rules that follow from provenance classification.

The protocol applies only to matters where the filing structure has been
implemented (as identified in the Phase 2 filing structure scan, 2026-03-06).
Matters that have not implemented the structure are out of scope for automated
classification until their filing structure is remediated.

---

## 2. Terminology

| Term | Definition |
|------|------------|
| **Filing Protocol** | This document. The prescriptive standard for how matter files must be organized and classified. |
| **Filing Structure** | The six-folder hierarchy defined in Section 3. A matter has "implemented the filing structure" when at least the numbered folder set is present. |
| **Provenance** | The origin and authorship of a document — whether it came from the client, was drafted by LL, or was finalized by LL. |
| **Classification** | The act of assigning a provenance class to a document based on signals defined in Section 5. |
| **Client Productions** | Documents provided by the client to LL. The preferred term for what the `02` folder contains. |

---

## 3. Required Filing Structure

The canonical structure is defined by the Model File at:

```
Working Files/Model File/
```

Reference document: `Doc Control - Client Files - Model File.pdf`

Every matter folder must contain the following six numbered subfolders:

```
{matter_id} - {client_name}/         ← NTD: sub-matter reference may be suppressed
├── 01_Admin/
│   ├── Accounts/
│   ├── Conflicts and ID/
│   ├── Engagement Agreement/
│   └── Notes to File/               ← if applicable
├── 02_Client Provided Documents/    ← NTD: may be renamed "Client Productions"
├── 03_Transaction_Documents/
├── 04_Diligence/
├── 05_Research/
└── 06_Post_Closing/
```

### Folder descriptions

| Folder | Contents |
|--------|----------|
| `01_Admin` | LL-administered matter management documents: engagement agreement, conflict checks, ID records, accounts, notes to file. These are LL-internal administrative records, not client work product. |
| `02_Client Provided Documents` | Documents provided by the client to LL (client productions). Does not include LL-maintained corporate records — those are classified separately (see Section 4). |
| `03_Transaction_Documents` | Documents provided to and delivered to the client by LL. The primary LL work product folder. |
| `04_Diligence` | Mixed: may contain LL work product, LL-generated deliverables, or documents gathered from the client. Classification requires filename signal as tiebreaker. |
| `05_Research` | LL-generated research and analysis. |
| `06_Post_Closing` | Post-closing deliverables and records. |

### `02_Corporate_Records` — distinct from `02_Client Provided Documents`

These are **not equivalent**:

- `02_Client Provided Documents` (or "Client Productions"): documents the client sent to LL.
- `02_Corporate_Records`: corporate records **maintained by LL** on behalf of the client (minute books, resolutions, registers). These carry a distinct classification (`LL_ADMIN`) because LL is the custodian, not the author of the underlying corporate fact.

If a `02_Corporate_Records` folder is present in lieu of `02_Client Provided Documents`, its contents are classified `LL_ADMIN` unless the filename indicates they were received from the client rather than maintained by LL.

### Observed folder name variations (accepted for compliance detection)

| Position | Canonical name | Accepted equivalents |
|----------|----------------|----------------------|
| 01 | `01_Admin` | `1. Admin`, `01_Admin_` |
| 02 | `02_Client Provided Documents` | `2. Client Provided Information including Corporate Records`, `02_Client Provided Documents_` |
| 02 (alt) | `02_Corporate_Records` | `02_Corporate_Records _`, `02_Corporate_Records (AKA Client Provided Information)` — classified `LL_ADMIN`, not `CLIENT_PROVIDED` |
| 03 | `03_Transaction_Documents` | `3. Transaction Documents`, `03_Transaction_Documents _` |
| 04 | `04_Diligence` | `4. Diligence`, `04_Diligence _` |
| 05 | `05_Research` | `5. Research`, `05_Research_` |
| 06 | `06_Post_Closing` | `6. Post-Closing`, `06_Post_Closing` |

---

## 4. Provenance Classes

Every document retrieved from LegalMatters must be assigned one of five
provenance classes before it may be accessed by any agent.

| Class | Meaning | Permissible agent actions |
|-------|---------|--------------------------|
| `CLIENT_PROVIDED` | Document originated from the client or a third party (client productions) | Reference only; never treat as LL work product; do not paraphrase as LL output |
| `LL_ADMIN` | LL-administered matter management document or LL-maintained corporate record | Reference only for administrative context; do not treat as substantive work product or cite externally |
| `LL_DRAFT` | An LL-generated working draft, not finalized | May be used for context; must not be cited as final; must be labeled as draft if surfaced |
| `LL_FINAL` | An LL-signed or executed deliverable | May be cited as authoritative LL output; source URL must be included |
| `UNKNOWN` | Cannot be classified with available signals | Blocked from agent access until manually resolved by ML1 |

**Reservation:** Nothing from LegalMatters is assumed to be `LL_FINAL` without
at least one positive signal from Section 5 and explicit confirmation. Absence
of a draft signal does not imply final status.

---

## 5. Classification Signals

Classification is determined by evaluating signals in priority order. The
highest-confidence matching signal wins. If no signal matches, the class
is `UNKNOWN`.

### 5.1 Folder-path signals (highest priority)

| Folder | Class assigned | Notes |
|--------|---------------|-------|
| `02_Client Provided Documents` (or accepted equivalent) | `CLIENT_PROVIDED` | Determinative |
| `02_Corporate_Records` (or accepted equivalent) | `LL_ADMIN` | LL-maintained records; apply filename tiebreaker if file appears to be client-sourced |
| `01_Admin` | `LL_ADMIN` | Engagement agreements, conflict checks, accounts, notes to file are all LL-administered |
| `05_Research` | `LL_DRAFT` | Determinative |
| `04_Diligence` | Ambiguous — apply filename signal | May be LL work product, LL deliverable, or client-sourced |
| `03_Transaction_Documents` | Ambiguous — apply filename signal | Primary LL work product folder; may also include received counterparty documents |
| `06_Post_Closing` | Ambiguous — apply filename signal | May be LL final deliverable or client-received document |

### 5.2 Filename signals (secondary)

Applied when folder path is ambiguous, or as tiebreaker within `01_Admin`,
`04_Diligence`, `03_Transaction_Documents`, and `06_Post_Closing`.

| Pattern (case-insensitive) | Class assigned | Confidence |
|----------------------------|---------------|------------|
| `DRAFT` anywhere in name | `LL_DRAFT` | High |
| `redline` anywhere in name | `LL_DRAFT` | High |
| `_v1`, `_v2`, `_v3` … suffix | `LL_DRAFT` | High |
| `FINAL ML` in name | `LL_FINAL` | High |
| `For Execution` in name | `LL_FINAL` (pending execution) | High |
| `For Signature` in name | `LL_FINAL` (pending signature) | High |
| `Executed` in name | `LL_FINAL` | High |
| `PRECEDENT` in name | `LL_DRAFT` (template, not matter-specific) | High |
| `CLIENT RFI` in name | `CLIENT_PROVIDED` | Medium |
| Government form number prefix (e.g. `5261E`, `5271E`) | `UNKNOWN` — requires manual review | — |

### 5.3 `createdBy` signal (not used)

Graph API `createdBy` always reflects the uploader, not the document author.
All sampled files showed `Matthew Levine` as creator regardless of provenance.
This field **must not** be used as a classification signal.

### 5.4 File extension signal (not used alone)

`.pdf` is not a reliable provenance signal — it can be any class. `.docx`
is more likely to be LL-generated but is not determinative. Extension may
be used as a supplementary signal only when combined with others.

---

## 6. Classification Procedure

For each document in a matter that has implemented the filing structure:

1. Evaluate folder-path signal (Section 5.1).
2. If folder-path signal is determinative, assign class and record basis.
3. If folder-path signal is ambiguous, evaluate filename signal (Section 5.2).
4. If a filename signal matches, assign class and record basis.
5. If no signal is determinative, assign `UNKNOWN` and add to the unclassified
   review list for ML1 resolution.
6. For any `LL_FINAL` assignment, record the specific positive signal(s) that
   support it. A bare `.pdf` with no naming signal does not qualify.

Classification results are written to `SHAREPOINT_MANIFEST.yaml` in the
matter's secondbrain folder (e.g., `05_MATTERS/STANDARD/{matter_id}/`).
No document content is written to secondbrain — only metadata and
provenance classification.

---

## 7. Agent Access Rules

| Class | May agent read content? | May agent cite externally? | Label required when surfaced |
|-------|------------------------|---------------------------|------------------------------|
| `CLIENT_PROVIDED` | Yes — for context only | No | "client-provided document" |
| `LL_ADMIN` | Yes — for administrative context only | No | "LL administrative record" |
| `LL_DRAFT` | Yes — for context only | No | "LL draft — not final" |
| `LL_FINAL` | Yes | Yes — with source URL | Source URL required |
| `UNKNOWN` | **No** | **No** | Blocked until ML1 resolves |

---

## 8. Scope Limitations

This protocol applies only to matters listed in the Phase 2 compliance scan
as `filing_structure_implemented: true`. As of 2026-03-06, that is 11 of 41
matters (27%).

Matters not implementing the filing structure:
- Are not subject to automated classification.
- May not have their documents passed to any agent.
- Should be remediated by applying the six-folder structure before being
  brought into scope.

`Clerk Work`, `Data Management`, and `Model File` root folders are excluded
from classification scope entirely.

---

## 9. Open Items (NTD)

| Item | Description |
|------|-------------|
| NTD-1 | Confirm whether sub-matter reference should be suppressed in the matter folder name pattern |
| NTD-2 | Confirm whether `02_Client Provided Documents` should be renamed to `02_Client Productions` going forward |

---

## 10. Approval Gate

This protocol becomes active only after ML1 review and explicit approval.
Upon approval:
- Change `status` from `DRAFT` to `active`
- Change `version` from `0.2` to `1.0`
- Update `last_updated`
- Resolve NTD items before or concurrent with activation

Classification rules in Section 5 must not be coded into any script or agent
prior to that approval.

---

## 11. Change Log

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-03-07 | Initial draft. Based on Phase 2 enumeration (2026-03-06) and ML1 preliminary specifications. |
| 0.2 | 2026-03-07 | Revised per ML1 review: (1) Added `LL_ADMIN` as fifth provenance class. (2) Separated `02_Corporate_Records` from `02_Client Provided Documents` — not equivalent. (3) Clarified `01_Admin` as `LL_ADMIN` (not client provided). (4) Clarified `04_Diligence` as mixed folder requiring filename tiebreaker. (5) Government forms confirmed as `UNKNOWN`. (6) Added NTD items for sub-matter folder naming and `02` folder rename. |
