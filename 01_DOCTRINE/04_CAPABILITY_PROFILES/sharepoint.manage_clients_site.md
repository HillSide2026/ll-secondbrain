---
id: 01_doctrine__03_capability_profiles__sharepoint_manage_clients_site_md
title: Capability Profile: SharePoint.ManageClientsSite
owner: ML1
status: draft
version: 0.1
created_date: 2026-03-28
last_updated: 2026-03-28
tags: [capability, sharepoint, clients, management]
---

# Capability Profile: SharePoint.ManageClientsSite (v0.1)

## Purpose
Provide broad site-wide authority for the `/sites/Clients` SharePoint workspace.

## Allowed Actions
- Create, update, replace, move, rename, publish, demote, and delete pages and libraries
- Alter page layout, canvas structure, title area structure, navigation, permissions, sharing, retention, and site settings within `Clients`
- Create, delete, reposition, and configure web parts within `Clients`
- Create, update, move, rename, and delete client folders, libraries, and routing paths
- Break inheritance and assign SharePoint principals within the `Clients` site
- Maintain shared portal pages, client-specific workspace pages, and client routing surfaces
- Execute only when invoked by an approved workflow, runbook, or capability and when run evidence is emitted into ML2

## Disallowed Actions
- Modifying ML2 canonical artifacts in place through SharePoint
- Expanding authority to other SharePoint sites by implication
- Writing to `LegalMatters` or any unapproved SharePoint site under this authority
- Altering tenant-wide identity management, retention, or compliance settings unless separately approved

## Inputs (Typed)
- site_path: string (`/sites/Clients`)
- operation: string
- target: object
- options: object
  - may include `approval_token` for ML1-gated operations
  - may include `dry_run`, `create_if_missing`, `overwrite`, `publish_after_update`, `expected_version`, and `reason`

## Outputs (Typed)
- status: string
- operation_id: string
- site_path: string
- operation: string
- target_ref: object
- changes_applied: array
- warnings: array
- errors: array
- approval_used: boolean

## Required Logs
- site_path
- target_ref
- operation
- structured target/options input record
- run identifier
- acting tool or agent
- success/failure state

## Approval Mode
- Auto for the wrapper operations admitted without ML1 token in the active Clients control matrix.
- `approval_token` required for the wrapper operations that the active Clients control matrix marks as ML1-gated.

## Boundary Rules
- The request MUST remain within `/sites/Clients`.
- The capability MUST not infer authority over any non-`Clients` SharePoint surface.
- The capability MUST satisfy the active SharePoint write invariants.
