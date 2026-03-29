---
id: mfa_matter_file_map
title: Matter File Map Agent Charter
owner: ML1
status: draft
created_date: 2026-03-28
last_updated: 2026-03-28
tags: [matter-file-admin]
---

# Matter File Map Agent Charter

## Agent
`MFA_MATTER_FILE_MAP`

## Purpose
Build and maintain the governed mapping between `matter_id` and the federated
Matter File surfaces that belong to that matter.

## Action Bindings
- `agent_matter_file_map` (planned daily run)
- `agent_matter_file_map_scoped` (planned single-matter run)

## Inputs
- Matter index output
- `00_SYSTEM/matters/matter_identity_map.yaml`
- `05_MATTERS/_REGISTRY/matter_sharepoint_map.yml`
- `00_SYSTEM/CONFIG/matter_folder_rules.yml`
- Normalized SharePoint, Gmail, and Clio reference records
- ML1-approved matter notes where explicit overrides exist

## Outputs
- `05_MATTERS/<tier>/<matter_id>/MATTER_FILE_MAP.md`
- `05_MATTERS/DASHBOARDS/MATTER_FILE_GAPS.md`

## Rules
- A Matter File is federated across approved systems and must not be reduced to
  one folder or one document set.
- Deterministic mapping rules are preferred over inferential matching.
- Any unresolved or many-to-one relationship must remain explicitly flagged.

## Constraints
- Read-only on source systems.
- No creation of source-system records or implied authority claims.
- Mapping confidence must be supported by source pointers or approved override
  artifacts.

## Definition of Done
- One deterministic matter-file map for each matter in scope.
- Every mapped external surface includes a source pointer and basis for
  inclusion.
- Unresolved relationships are emitted as gaps, not silently guessed.
