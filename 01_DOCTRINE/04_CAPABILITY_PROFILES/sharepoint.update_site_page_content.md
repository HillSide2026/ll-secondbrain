---
id: 01_doctrine__03_capability_profiles__sharepoint_update_site_page_content_md
title: Capability Profile: SharePoint.UpdateSitePageContent
owner: ML1
status: draft
version: 0.1
created_date: 2026-03-28
last_updated: 2026-03-28
tags: [capability, sharepoint, mcp, sitepages]
---
# Capability Profile: SharePoint.UpdateSitePageContent (v0.1)

## Purpose
Apply narrow, non-structural content updates to an existing SharePoint site page within the approved Clients `SitePages` surface.

## Allowed Actions
- Update page title
- Update page description
- Update `innerHtml` for existing text web parts on existing `SitePages/*.aspx` pages
- Execute only when invoked by an approved workflow, runbook, or capability and run evidence is emitted into ML2

## Disallowed Actions
- Creating, deleting, renaming, moving, publishing, or demoting pages
- Altering page layout, canvas structure, title area structure, navigation, permissions, sharing, retention, or site settings
- Creating, deleting, or repositioning web parts
- Updating standard web part configuration
- Treating this exception as write authority over the broader `Clients` site

## Inputs (Typed)
- page_path: string (`SitePages/<name>.aspx`)
- expected_e_tag: string
- title: string (optional)
- description: string (optional)
- text_webparts: array of `{webpart_id: string, inner_html: string}` (optional)

## Outputs (Typed)
- page_id: string
- page_path: string
- updated_fields: array
- updated_webparts: array
- previous_e_tag: string
- new_e_tag: string
- web_url: string

## Required Logs
- page_path
- page_id
- updated field list
- updated webpart ids
- run identifier
- acting tool or agent
- artifact version reference
- provenance label
- reason code
- upstream artifact reference
- approval_reference when execution depends on an ML1-scoped exception

## Approval Mode
- Auto when the request stays within the approved Clients `SitePages` surface, uses an approved workflow, runbook, or capability, and satisfies the active SharePoint write invariants.
- Site-structure, navigation, or other non-content change batches require explicit ML1 approval recorded through an `approval_reference`.

## Boundary Rules
- The request MUST target an existing `SitePages/*.aspx` page in `/sites/Clients`.
- The request MUST include an expected page eTag for version-safe execution.
- The request MUST include artifact version reference and `Derived from ML2 vX.Y` provenance labeling or equivalent governed marker.
- The tool MUST NOT mutate page structure or any non-content Clients surface.
