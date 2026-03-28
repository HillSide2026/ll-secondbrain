---
id: 00_system__integrations__sharepoint__readme_md
title: SharePoint Integration
owner: ML1
status: active
version: 2.9
created_date: 2026-02-15
last_updated: 2026-03-28
tags: [integration, sharepoint, mcp]
---

# SharePoint Integration

## Contract
- [`sharepoint_sources.yaml`](sharepoint_sources.yaml) — canonical drive/path registry
- [`sharepoint_tool_surface_spec.md`](sharepoint_tool_surface_spec.md) — approved abstract SharePoint tool-surface contract
- [`sharepoint_tool_control_matrix.md`](sharepoint_tool_control_matrix.md) — control matrix for allowed, ML1-gated, and prohibited SharePoint tools

## Access Surface

Two access modes exist. Both are strictly bounded to the same access surface.

| Mode | Script | Purpose |
|------|--------|---------|
| Script | `scripts/sharepoint_integration.py` | Manual/automated runs |
| MCP | `scripts/sharepoint_mcp_server.py` | Native Claude Code access |

The MCP server is a controlled replacement interface — it enforces the explicit
runtime boundary declared in this repo and does not act as a general SharePoint gateway.

## Sites, Drives, and Permissions

| Alias | Site | Drive Scope | Authority |
|-------|------|-------------|-----------|
| `legalmatters` | `/sites/LegalMatters` | Working Files | READ ONLY |
| `documentation` | `/sites/Documentation` | Site-wide across approved drives/libraries | READ / WRITE / MANAGE |
| `clients` | `/sites/Clients` | Site-wide managed workspace authority with current runtime exposing a narrower implemented subset | READ / WRITE / MANAGE |

## Clients Runtime Scope

The `Clients` site is approved as a managed workspace at the site level. The current executable layer still exposes only a narrower implemented subset of that broader authority. Today it exposes the following library aliases and helper surfaces:

- `clients_documents` -> Documents library, restricted to `Playbooks`, `Policies and Processes`, `Templates`, `Work in Progress`
- `clients_master_client_library` -> Master Client Library, full library read
- `clients_yellowbricks_capital` -> Yellowbricks Capital, full library read
- `clients_turtle_island` -> Turtle Island, full library read
- `clients_our_sharepoint_test2` -> Our-SharePoint-Test2, full library read
- `clients_our_sharepoint_test` -> our-sharepoint test, full library read

Home page reference: `/sites/Clients/SitePages/Home.aspx`

### clients — Intended Portal Pattern
- Branded sign-in page for credentialed client users
- Shared home page accessible to all credentialed client users
- Home page customized per client so each client sees links to client-specific pages
- Client-specific pages link onward to document libraries scoped to that client

### clients — Current MCP Implementation
- Metadata access across the configured Clients document-library aliases
- Read/review access for existing `SitePages/*.aspx` pages in `/sites/Clients`
- Current page-content helper updates on existing `SitePages/*.aspx` pages only
- Current `provision_client_workspace` helper for one new client page, one new `*-Documents` library, explicit principal assignment on those created resources, and one shared-home navigation link
- Broader Clients managed-workspace authority is approved in doctrine, but additional runtime tools still need to be implemented before that broader authority is executable through MCP
- No group creation, guest invitation, tenant identity administration, or tenant-wide retention/compliance changes through the current runtime

### legalmatters — Approved Read Paths (intake_paths only)
- `LL Matters (Essential)`
- `LL Matters (Strategic)`
- `LL Matters (Standard)`
- `LL Matters (Standard Cash Cows)`
- `LL Matters (Parked)`
- `Clerk Work`

**Excluded** (root-confirmed but NOT in intake_paths, no access granted):
- `Data Management`
- `Model File`

### documentation — Approved Site Authority
- Site-wide read access for configured system operations
- Site-wide write and manage access for approved workflows, runbooks, and capabilities
- Remains a managed external workspace, not canonical doctrine storage
- Canonical ML2 artifacts must still be promoted through ML2 and not treated as SharePoint-native truth

### documentation — Current MCP Template/WIP Scope
- `find_latest_template` reads template metadata only within the allowlisted `SB Execution/TEMPLATES` zone
- `diff_docs` may read file content only for allowlisted template and WIP documents in Documentation
- `copy_template_to_wip` may copy an allowlisted template into an allowlisted Documentation WIP folder
- `upload_draft` writes only into the allowlisted Documentation `SB Execution/DRAFTS` zone

### governance — Abstract Tool Contract vs Current Runtime
- `sharepoint_tool_surface_spec.md` defines the abstract `sp_*` SharePoint tool surface, authority model, write invariants, and audit requirements
- `sharepoint_tool_control_matrix.md` classifies each abstract tool as allowed, ML1-gated, or prohibited
- `scripts/sharepoint_mcp_server.py` currently implements a narrower subset and helper mapping rather than the full abstract `sp_*` surface
- `list_folder` aligns to `sp_list_folder`
- `get_item` aligns to a metadata-only subset of `sp_get_metadata`
- `upload_draft` aligns to a limited `sp_create_draft_document`
- `copy_template_to_wip` aligns to a limited managed-workspace draft-creation helper
- `find_latest_template` and `diff_docs` are bounded helper tools inside the Documentation allowlist rather than tenant-general SharePoint tools
- `review_site_page` aligns to `sp_get_site_page`
- `update_site_page_content` aligns to `sp_update_site_page_content`
- `provision_client_workspace` aligns to `sp_provision_client_workspace`

## MCP Tools

| Tool | Drive(s) | Operation |
|------|----------|-----------|
| `list_folder` | `legalmatters`, `documentation`, `clients_*` | Enumerate folder children (metadata only, no file content) |
| `get_item` | `legalmatters`, `documentation`, `clients_*` | Get metadata for one item by path |
| `find_latest_template` | documentation allowlist only | Search allowlisted template registry + live metadata |
| `diff_docs` | documentation allowlist only | Read allowlisted template/WIP file contents and generate a read-only diff summary |
| `copy_template_to_wip` | documentation allowlist only | Copy an allowlisted template into an allowlisted Documentation WIP destination |
| `upload_draft` | documentation only | Upload file to Documentation workspace surface |
| `review_site_page` | clients SitePages helper | Review one existing `SitePages/*.aspx` page, including text web parts and page metadata |
| `update_site_page_content` | clients SitePages helper | Update title, description, and existing text web part content on one existing `SitePages/*.aspx` page |
| `provision_client_workspace` | clients managed workspace helper | Create one client page, create one `*-Documents` library, assign existing principals, and add one shared-home navigation link |
| `manage_clients_site` | clients managed workspace wrapper | Broad `/sites/Clients` page, library, folder, navigation, permission, and site operations under the governed wrapper and token-gated controls |

## Operations NOT Yet Exposed via MCP

- Arbitrary file-content reading outside the allowlisted Documentation template/WIP zones
- Writes to `legalmatters`
- Delete, move, share, or permission operations outside the explicitly admitted wrappers and scope locks
- Copy operations outside the allowlisted template-to-WIP flow
- Group creation, guest invitation, tenant identity administration, retention/compliance changes, or cross-site mutation in `Clients`
- Site or drive enumeration/discovery
- Cross-site search
- Access to any site or library beyond the configured `legalmatters`, `documentation`, and `clients` runtime scopes

Site-wide Documentation authority is approved in doctrine, but MCP/server implementation must still declare the exact tool surface it exposes. Broader site authority does not require exposing every possible Graph operation to every runtime tool.

## MCP Registration

Registered in `.mcp.json` (project root).
Server process: `scripts/sharepoint_mcp_server.py` (Python 3.9, no external MCP SDK).
Auth: Azure client credentials (AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET from .env).
Clients provisioning and site-management note: `provision_client_workspace` and `manage_clients_site` depend on Graph page/list write access plus SharePoint REST authorization on `/sites/Clients` for inheritance-breaking, role assignment, navigation, page-home, and other structural changes.

## Change Notes
- v1.0 2026-02-15: Integration stub created.
- v2.0 2026-03-11: MCP server implemented. Access boundary documented.
  MCP replaces script interface for Claude Code sessions; script retained for
  manual/automated runs. Access surface unchanged.
- v2.1 2026-03-27: Documentation site elevated to managed-workspace authority
  (site-wide read/write/manage) by ML1 direction. LegalMatters remains read-only.
- v2.2 2026-03-27: Added explicit in-repo reference for `/sites/Clients` as the confirmed portal-linked site. Identification recorded without widening current MCP tool scope.
- v2.3 2026-03-27: Added the intended `Clients` portal flow so the repo captures the expected client-facing navigation model.
- v2.4 2026-03-27: Expanded the repo MCP runtime boundary to include read-only Clients site libraries and updated the documented runtime limits accordingly.
- v2.5 2026-03-27: Added Documentation-scoped MCP tools for template lookup, allowlisted diffing, and template-to-WIP copy without widening LegalMatters access.
- v2.6 2026-03-28: Added the abstract SharePoint tool-surface spec and control matrix, and clarified how the current MCP runtime maps to that narrower approved contract.
- v2.7 2026-03-28: Added the ML1-approved Clients `SitePages` exception for page review and existing-page content updates only. Site-structure and navigation changes remain separately ML1-gated.
- v2.8 2026-03-28: Added the ML1-gated Clients workspace-provisioning exception and admitted a narrow provisioning batch for one new client page, one new client library, explicit principal assignment, and one shared-home navigation link.
- v2.9 2026-03-28: Elevated Clients to site-wide managed-workspace authority and clarified that the current runtime still exposes only a narrower implemented subset of that broader approval.
- v2.10 2026-03-28: Added the governed `manage_clients_site` wrapper for broad `/sites/Clients` operations with explicit token-gated controls for destructive and permission-bearing actions.
