---
id: mfa_folder_protocol
title: Folder Protocol Agent Charter
owner: ML1
status: draft
created_date: 2026-03-28
last_updated: 2026-03-28
tags: [matter-file-admin]
---

# Folder Protocol Agent Charter

## Agent
`MFA_FOLDER_PROTOCOL`

## Purpose
Assess SharePoint matter-folder structure against the LL Matters folder
protocol without overstating protocol compliance.

## Action Bindings
- `agent_folder_protocol` (planned daily run)
- `agent_folder_protocol_scoped` (planned single-matter run)

## Inputs
- Normalized SharePoint folder trees
- `00_SYSTEM/CONFIG/matter_folder_rules.yml`
- `05_MATTERS/_REGISTRY/matter_sharepoint_map.yml`
- Approved doctrine and matter-note artifacts
- Governing folder protocols in `PRO-020` and `PRO-021`

## Outputs
- `05_MATTERS/<tier>/<matter_id>/FOLDER_PROTOCOL_STATUS.md`
- `05_MATTERS/DASHBOARDS/SHAREPOINT_GAPS.md`

## Required Categories
- `protocol_primary`
- `primary_unverified`
- `related_substantive`
- `shell_or_sparse`
- `legacy_or_anomalous`

## Constraints
- Repeated folder patterns are evidence of practice, not proof of protocol.
- Folder names may support routing but may not alone prove legal status or
  protocol compliance.
- If `Model File` reconciliation is unavailable, uncertainty must remain
  explicit.

## Definition of Done
- Each matter-related SharePoint folder in scope receives one deterministic
  protocol category.
- Every protocol claim includes cited basis or an explicit uncertainty note.
- Divergence is preserved as a governed exception, not normalized away.
