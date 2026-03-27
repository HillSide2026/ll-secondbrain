---
id: POL-059
title: Integration Control Policy
owner: ML1
status: draft
version: 1.1
created_date: 2026-02-27
last_updated: 2026-03-23
tags: [integration, policy, control]
---

# Integration Control Policy

(Operational Control Specification)

This is the enforceable layer.

---

## 0. Precedence

For operational external writes, this policy **supersedes** `POL-058_System_Write_Back_Policy.md`.
Only explicit hard prohibitions defined as invariants remain controlling.

---

## 1. Data Classification

### 1.1 Canonical Data (ML2 Only)

- Templates
- Playbooks
- Risk registers
- Fallback ladders
- Governance documents

Cannot be modified externally.

### 1.2 Published Data

- Working drafts
- Client deliverables
- Internal collaboration copies

Editable externally but non-authoritative.

---

## 2. Read Controls

Agents may read external documents when:
- Triggered by QC gate
- Requested by ML1
- Required for drift detection

Bulk ingestion prohibited unless approved.

---

## 3. Write Controls

All writes must:
- Be to designated folders/sites
- Include artifact version reference
- Include "Derived from ML2 vX.Y" label
- Avoid modifying canonical paths

No direct writes into ML2 from external suites.

### 3.1 SharePoint Site Classes

SharePoint surfaces must be classified as one of:
- `read_only_authority`
- `managed_workspace`

Current approved classes:
- `levinellp.sharepoint.com/sites/LegalMatters` = `read_only_authority`
- `levinellp.sharepoint.com/sites/Documentation` = `managed_workspace`

### 3.2 Managed Workspace Rule

For a site classified as `managed_workspace`, the system MAY perform read, write, and manage operations across the approved site when:
- the site is explicitly named in ML2 integration contracts
- the operation is invoked by an approved workflow, runbook, or capability
- run evidence is emitted into ML2

Managed-workspace authority does not convert that site into canonical storage.
ML2 remains the authority for doctrine and governed canonical artifacts.

---

## 4. Folder & Site Segmentation

External platforms must maintain:
- /Published Templates/
- /Working Drafts/
- /Candidate for Promotion/
- /Archive/

No canonical artifacts stored outside ML2 repository.

For SharePoint:
- `Documentation` may implement this segmentation site-wide.
- `LegalMatters` remains outside this write-capable segmentation model and stays read-only.

---

## 5. Promotion Workflow (Enforced)

When an external document is proposed for canonical status:

Step 1 — Move to /Candidate for Promotion/  
Step 2 — Automated diff vs canonical  
Step 3 — Structured change summary generated  
Step 4 — ML1 approval recorded  
Step 5 — Version increment in ML2  
Step 6 — Republish to /Published Templates/  

If ML1 does not approve, document remains non-canonical.

---

## 6. Audit Requirements

System must retain:
- 24-month integration activity log minimum
- Diff history for each promoted artifact
- Approval reference ID
- Agent version that executed action

---

## 7. Escalation Triggers

Immediate ML1 escalation if:
- Canonical artifact modified externally
- Version mismatch detected
- Unauthorized write detected
- Drift exceeds threshold
