---
id: 01_doctrine__03_capability_profiles__readme_md
title: Capability Profiles
owner: ML1
status: draft
version: 1.0
created_date: 2026-02-08
last_updated: 2026-03-08
tags: []
---

# Capability Profiles

Definition: Capability profiles define explicit permission boundaries for components, layers, and tools under ML1 control.
Capability profiles are system boundaries for what a component may and may not do.
Boundary: Profiles do not replace binding doctrine, policies, or protocols.

This directory contains capability profiles for:
- Layer/component authority boundaries
- Agent-level exceptions
- Tool-level operational permissions

---

## Relationship to Doctrine

| Layer | Analogy | Changeability |
|-------|---------|---------------|
| Canonical Doctrine | Constitutional law | Rarely changed |
| Capability Profiles | Statutes / Permits | Task-specific, revocable |

Doctrine defines **what agents cannot do by default**.
Profiles define **what specific agents may do under controlled conditions**.

---

## Agent Profile Relaxation Axes

Profiles relax constraints along **one axis at a time**:

| Axis | Example Relaxation |
|------|-------------------|
| Write access | Read-only → draft-only → scoped edits |
| Scope | Single folder → project class → portfolio |
| Autonomy | On-demand → batch → scheduled |
| Confidence | Conservative → moderate (never assertive) |
| Memory | Stateless → session → scoped retrieval |

---

## Agent Progression Model

| Phase | Capability | Constraints |
|-------|-----------|-------------|
| 1 — Analysis Only | Read, summarize, recommend | No writes, no memory |
| 2 — Draft Generation | Create draft files | No overwrites, no lifecycle changes |
| 3 — Maintenance Edits | Update drafts | Append-only logs, no deletions |
| 4 — Structured Updates | Schema-bound updates | Still no authority, still reversible |

For agent execution profiles, at no point does an agent: **decide**, **approve**, **or override doctrine**.

---

## Profile Index

| ID | Name | Status | Scope |
|----|------|--------|-------|
| CAP-001 | ML1 (Human Authority Layer) | ACTIVE | Human authority permissions |
| CAP-002 | ML2 (System-of-Record Layer) | ACTIVE | Canonical record permissions |
| CAP-003 | System (Execution Layer) | ACTIVE | Runtime execution permissions |
| CAP-004 | LL (Distribution Layer) | ACTIVE | Market-facing distribution permissions |
| CAP-005 | Execution Bridge (Integration Layer) | ACTIVE | Integration transport permissions |
| 0001 | Draft Write Access | ACTIVE | Documentation synthesis |
| gmail.get_thread | Capability Profile: Gmail.GetThread | DRAFT | Gmail read retrieval |
| gmail.search_threads | Capability Profile: Gmail.SearchThreads | DRAFT | Gmail search |
| gmail.create_draft | Capability Profile: Gmail.CreateDraft | DRAFT | Draft-only outbound composition |
| sharepoint.find_latest_template | Capability Profile: SharePoint.FindLatestTemplate | DRAFT | Template lookup |
| sharepoint.diff_docs | Capability Profile: SharePoint.DiffDocs | DRAFT | Read-only comparison |
| sharepoint.copy_template_to_wip | Capability Profile: SharePoint.CopyTemplateToWIP | DRAFT | WIP copy in allowlisted zones |
| calendar.list_events | Capability Profile: Calendar.ListEvents | DRAFT | Read-only schedule retrieval |
| calendar.generate_prep_packet | Capability Profile: Calendar.GeneratePrepPacket | DRAFT | Prep packet generation |

---

## Creating a New Profile

1. Copy `_TEMPLATE.md`
2. Assign next sequential ID
3. Define scope narrowly
4. Document all relaxations explicitly
5. Require ML1 approval

---

## Revocation

To revoke a profile:
1. Change status to `REVOKED`
2. Add revocation date
3. No justification required
