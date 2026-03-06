# Phase 2 Gate Report — LegalMatters Folder Structure & Document Metadata
**Scanned:** 2026-03-06
**Drive:** Working Files (`b!h1ZUioTppUufgSXSnMchs...`)
**Matters sampled:** 24-845-00001 (STAR 333), 23-235-00001 (Baobab), 25-1185-00001 (Klys)
**Raw data:** `phase2_enumeration.json`

---

## 2.1 Root-Level Folder Structure

```
Working Files/
├── Clerk Work/              (3 children)   ← exclude from classification
├── Data Management/         (2 children)
├── LL Matters (Essential)/  (4 children)
├── LL Matters (Parked)/     (10 children)
├── LL Matters (Standard Cash Cows)/  (2 children)
├── LL Matters (Standard)/   (17 children)
├── LL Matters (Strategic)/  (9 children)
└── Model File/              (7 children)   ← likely templates/precedents
```

---

## 2.2 Matter Folder Contents

### Naming convention at the tier level
Folders in `LL Matters (Standard)` follow no single naming pattern:

| Folder name | Pattern |
|-------------|---------|
| `24-845-00001 - STAR 333 SPORTS INC` | `{matter_id} - {client_name}` |
| `23-194-00013 RM - Legacy` | `{matter_id} {initials} - {label}` |
| `25-1185-00001 - Klys` | `{matter_id} - {surname}` |
| `Newmarket accountant` | No matter number — structural anomaly |
| `shareholder review` | No matter number — structural anomaly |

**Anomaly:** One `.doc` file (`MTW-018 Services Agreement...`) is sitting loose at the `LL Matters (Standard)` root — outside any matter folder.

---

### 24-845-00001 — STAR 333 SPORTS INC

**Structure:** Organized by matter number and topic. No files at the client folder root.

```
24-845-00001 - STAR 333 SPORTS INC/
├── 24-845-00001 - Corporate Governance/   (49 items)
│   ├── 24-845-00001 - Corporate Finance/  (11 items)
│   ├── 24-845-00001 - Governance - Ancillary License Agreement/  (13 items)
│   ├── Corporate Governance - Indemnity/  (1 item)
│   ├── Director Appointment/              (3 items)
│   ├── Franchising/                       (2 items)
│   ├── resolutions/                       (5 items)
│   ├── round2/                            (10 items)
│   ├── round3/                            (9 items)
│   ├── Shareholder Agreement/             (16 items)
│   ├── STAR 333 SPORTS INC. Minutebook/   (17 items)
│   ├── STAR 333 SPORTS INC. Minutebook 2/ (17 items)
│   ├── Subscription Agreement/            (7 items)
│   └── [37 files at subfolder root — mixed .pdf and .docx]
├── 24-845-00002 - League Operations/      (29 items)
│   ├── Alberta/      (1)
│   ├── Cricket Canada - Escrow/  (5)
│   ├── Ontario/      (1)
│   ├── Team License Agreement/   (9)
│   ├── venue/        (3)
│   └── [24 files at subfolder root — all .docx]
├── Portal/                                (3 items)
└── stakeholder management/                (7 items)
```

**Notable:** Matter 24-845-00002 (League Operations) is stored *inside* the 24-845-00001 client folder — two matter numbers share one SharePoint folder hierarchy.

---

### 23-235-00001 — Baobab Energy Africa Ltd

**Structure:** No subfolders except one WIP folder. Files dumped at matter root.

```
23-235-00001 - Baobab/
├── Work In Progress Folder/
│   ├── PRECEDENT_Board Resolution (Financial Statements...).docx
│   └── PRECEDENT_Board Resolution_Declaring Dividend_.docx
└── [5 files at root — all .pdf, all created by Matthew Levine 2025-10-19]
    ├── Articles of Amendment re name change (2).pdf
    ├── Baobab Energy Africa Ltd. - Rectification resolution...pdf
    ├── NexGen Africa Energy Ltd. - Certificate and Articles...pdf
    ├── NexGen Africa Energy Ltd. - Notice of Change.pdf
    └── Special resolution re name change (2).pdf
```

**Notable:** The `Work In Progress Folder` contains PRECEDENT templates, not matter-specific documents.

---

### 25-1185-00001 — Alexander Klys

**Structure:** Numbered, labeled subfolders — the most consistent structure found.

```
25-1185-00001 - Klys/
├── 1. Admin/
├── 2. Client Provided Information including Corporate Records/
├── 3. Transaction Documents/
├── 4. Diligence/
├── 5. Research/
└── 6. Post-Closing/
```

**Notable:** This is the only matter with a folder explicitly named `Client Provided Information` — directly relevant to provenance classification. This numbering system appears to be the intended standard but is not consistently applied across matters.

---

## 2.3 File Metadata Patterns

### `createdBy` / `lastModifiedBy`

**Every file sampled shows `Matthew Levine` as both creator and last modifier.**

This is a critical finding: `createdBy` in Graph API records who *uploaded* the file to SharePoint, not who *authored* it. Client-provided documents uploaded by LL will show `Matthew Levine` as creator. **This field cannot be used to distinguish client-provided from LL-generated documents.**

### File naming signals (observed patterns)

| Pattern in filename | Likely provenance | Examples |
|--------------------|-------------------|---------|
| `DRAFT` | LL working draft | `DRAFT FitByte Subscription Agreement`, `DRAFT Shareholder Agreement Star333Sports` |
| `FINAL ML` | LL final (ML = Matthew Levine) | `CC S60 - FINAL ML 5March 2025` |
| `redline` | LL working draft | `CC S60 - FINAL ML redline`, `Share Investment Agreement redline` |
| `For Execution` / `For Signature` | LL near-final | `Articles of Amendment - For Execution.pdf` |
| `PRECEDENT` | LL template (not matter-specific) | `PRECEDENT Shareholder Agreement`, `PRECEDENT_Board Resolution` |
| `CLIENT RFI` | Client-related document | `CLIENT RFI - Franchise - Disclosure` |
| `5261E`, `5271E` | Ontario government form | `5261E Star 333 Sports Inc.pdf` |
| Numbered copies `(1)`, `(2)` | Version duplicates | `Articles of Amendment re name change (2).pdf` |

### File extension patterns

| Extension | Observation |
|-----------|-------------|
| `.docx` | Working documents — almost exclusively LL-authored or LL-edited |
| `.pdf` | Mixed: executed final docs, government forms, client scans, LL-generated PDFs |
| `.zip` | Archives (e.g., Minutebook.zip) |
| `.doc` | Legacy format — rare |

---

## Summary: Structural Problems Identified

1. **No consistent subfolder taxonomy.** Three different structural patterns observed across three matters. Only Klys uses a system that could support programmatic classification.

2. **`createdBy` is not a provenance signal.** All files are uploaded by LL, making Graph API creator metadata useless for distinguishing client-provided vs LL-generated documents.

3. **Multiple matter numbers per client folder.** 24-845-00001 and 24-845-00002 share a top-level SharePoint folder. Matter-number-based folder lookup requires handling this nesting.

4. **PRECEDENT files stored in active matter folders.** Templates and precedents are mixed in with matter-specific documents.

5. **Unstructured version accumulation.** Multiple near-identical filenames exist with numeric suffixes (`(1)`, `(2)`) or minor name variations (Draft, Draft2, redline, redline2).

6. **Structural anomalies at tier level.** Two folders without matter numbers and one loose file exist at the `LL Matters (Standard)` root.

7. **Clerk Work folder excluded.** Confirmed as low-value operational output; excluded from classification scope.

---

## Gate: Folder Structure Description (for Phase 3 input)

The actual LegalMatters folder structure does NOT support a deterministic folder-path-based classification system across all matters.

The only reliable classification signals available are:

**High confidence (file-name-based):**
- `DRAFT` in name → `LL_DRAFT`
- `FINAL ML` in name → `LL_FINAL`
- `redline` in name → `LL_DRAFT`
- `For Execution` / `For Signature` in name → `LL_FINAL` (pending)
- `PRECEDENT` in name → `LL_TEMPLATE` (new class — not matter work product)
- `CLIENT RFI` in name → requires review

**High confidence (folder-path-based — Klys-style only):**
- Parent folder contains `Client Provided` → `CLIENT_PROVIDED`

**Cannot be classified without manual review:**
- .pdf files with no naming signal
- .docx files with no naming signal
- Files at matter root
- Government forms (blank vs executed)

**Recommended action for Phase 3:** Define classification rules based on file-name patterns as the primary signal, with folder path as a secondary signal where Klys-style structure exists. All files without a deterministic signal should be classified `UNKNOWN` and excluded from agent access pending manual resolution.
