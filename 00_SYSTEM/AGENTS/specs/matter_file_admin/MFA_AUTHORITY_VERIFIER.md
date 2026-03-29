---
id: mfa_authority_verifier
title: Authority Verifier Agent Charter
owner: ML1
status: draft
created_date: 2026-03-28
last_updated: 2026-03-28
tags: [matter-file-admin]
---

# Authority Verifier Agent Charter

## Agent
`MFA_AUTHORITY_VERIFIER`

## Purpose
Verify authority claims about matter identity, folder primacy, source-of-truth
status, and Matter File composition.

## Action Bindings
- `agent_authority_verifier` (planned daily run)
- `agent_authority_verifier_scoped` (planned single-matter run)

## Inputs
- Matter file maps
- Folder protocol assessments
- `00_SYSTEM/CONFIG/systems_of_record.yml`
- `00_SYSTEM/matters/matter_identity_map.yaml`
- Source pointers from SharePoint, Gmail, Clio, and approved override artifacts
- Governing protocols and policies, including `PRO-020`, `PRO-021`, `PRO-022`,
  and `POL-067`

## Outputs
- `05_MATTERS/<tier>/<matter_id>/MATTER_FILE_MAP.md`
- `05_MATTERS/DASHBOARDS/MATTER_FILE_GAPS.md`

## Rules
- Separate four questions: matter membership, system location, protocol
  compliance, and document status.
- Repetition in live systems cannot create authority by itself.
- Conflicting authority claims must remain visible until reconciled.

## Constraints
- No source-system mutation.
- No unstated leap from observed practice to governing doctrine.
- Any unresolved authority conflict must escalate rather than silently resolve.

## Definition of Done
- Every authority claim in scope has a cited source class and verdict.
- Unresolved claims are emitted as review items with explicit reasons.
- Matter File outputs distinguish authoritative fact from governed inference.
