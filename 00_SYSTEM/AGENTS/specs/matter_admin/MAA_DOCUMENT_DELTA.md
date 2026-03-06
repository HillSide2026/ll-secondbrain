---
id: maa_document_delta
title: Document Delta Agent Charter
owner: ML1
status: draft
created_date: 2026-03-05
last_updated: 2026-03-05
tags: [matter-admin]
---

# Document Delta Agent Charter

## Agent
`MAA_DOCUMENT_DELTA`

## Purpose
Track SharePoint matter-file inventory and deterministic deltas versus previous run snapshots.

## Action Bindings
- `agent_document_delta` (daily run)

## Inputs
- Normalized SharePoint `DocRef` records
- Matter-to-folder mapping rules
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
- SharePoint is authority for documents; ML2 stores metadata and pointers only.
- Every indexed row includes `source_pointer` and `web_url` where available.
- No file writes to SharePoint.

## Definition of Done
- Deterministic per-matter index.
- Deterministic delta report against prior snapshot.
- Firm-wide gaps dashboard for unmapped and ambiguous items.

