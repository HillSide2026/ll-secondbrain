---
id: POL-059
title: Integration Control Policy
owner: ML1
status: draft
version: 1.3
created_date: 2026-02-27
last_updated: 2026-03-28
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
- `levinellp.sharepoint.com/sites/Clients` = `read_only_authority`

### 3.1.1 Scoped Sub-Surface Exceptions

ML1 may approve a narrower operational exception inside a site that otherwise remains
`read_only_authority` when all of the following are true:
- the exact site, library or list, and path scope are named in ML2 integration contracts
- allowed tools and prohibited actions are explicitly listed
- structure, permission, deletion, publication, and retention authority remain separately controlled
- the action is invoked by an approved workflow, runbook, or capability when the exception permits writes
- run evidence is emitted into ML2

A scoped sub-surface exception does not reclassify the parent site.

### 3.2 Read-Only Authority Rule

For a site classified as `read_only_authority`, the system MAY perform read-only
operations within the explicitly approved site, library, and path scope when:
- the site is explicitly named in ML2 integration contracts
- the operation satisfies Section 2 read controls
- runtime boundaries restrict access to the approved read-only scope

The system MUST NOT, for a `read_only_authority` site:
- create, update, replace, move, or delete files or folders
- alter permissions, sharing state, or site structure
- infer write authority from visibility, existing credentials, or related site access

### 3.2.1 Approved Clients SitePages Exception

For `levinellp.sharepoint.com/sites/Clients`, the parent site remains
`read_only_authority`.

An ML1-approved scoped exception exists for `/sites/Clients/SitePages` only.

Within this exception, the system MAY:
- review existing `SitePages/*.aspx` pages for metadata, text content, supported web-part inventory, and link review
- update page title, description, and existing text web part content on existing `SitePages/*.aspx` pages

The Clients SitePages exception is valid only when:
- the operation stays within the explicit `SitePages` scope declared in ML2 integration contracts
- read actions satisfy Section 2 read controls
- write actions are invoked by an approved workflow, runbook, or capability
- write invariants in Section 3 are satisfied
- run evidence is emitted into ML2

The system MUST NOT under this exception:
- create, delete, rename, move, publish, or demote pages
- alter page layout, canvas structure, navigation, permissions, sharing, retention, or site settings
- create, delete, or reposition web parts
- infer authority over any non-`SitePages` Clients surface

Any Clients SitePages structure change, navigation change, or other non-content
change requires explicit ML1 approval per change batch recorded through an
`approval_reference`.

### 3.3 Managed Workspace Rule

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
- `Clients` remains outside this write-capable segmentation model except for the approved `SitePages` page-review and page-content-update exception in Section 3.2.1.

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

For the Clients SitePages exception, the retained audit trail must also make the
page path and updated page-content targets reconstructable from the run record.

---

## 7. Escalation Triggers

Immediate ML1 escalation if:
- Canonical artifact modified externally
- Version mismatch detected
- Unauthorized write detected
- Drift exceeds threshold
