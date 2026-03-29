---
id: mfa_document_delta
title: Document Delta Agent Charter
owner: ML1
status: draft
created_date: 2026-03-28
last_updated: 2026-03-28
tags: [matter-file-admin]
---

# Document Delta Agent Charter

## Agent
`MFA_DOCUMENT_DELTA`

## Purpose
Track document inventory and deterministic deltas for Matter File surfaces,
with SharePoint as the currently active source in scope.

## Action Bindings
- `agent_document_delta` (daily run)

## Inputs
- Normalized SharePoint `DocRef` records
- Matter-to-folder and matter-file mapping rules
- Prior snapshot state from cache

## Outputs
- `05_MATTERS/<tier>/<matter_id>/DOC_INDEX.md`
- `05_MATTERS/<tier>/<matter_id>/DOC_DELTAS.md`
- `05_MATTERS/DASHBOARDS/SHAREPOINT_GAPS.md`

## Delta Model
- Added items
- Changed items (path, modified timestamp, or key metadata)
- Removed items
- Duplicate file names
- Missing expected folders

## Constraints
- SharePoint is the authority for currently indexed document surfaces; ML2
  stores metadata and pointers only.
- Document-level delta reporting is subordinate to Matter File mapping and must
  not redefine Matter File scope by itself.
- No file writes to SharePoint.

## Definition of Done
- Deterministic per-matter index.
- Deterministic delta report against prior snapshot.
- Firm-wide gaps dashboard for unmapped, ambiguous, or structurally divergent
  items.
