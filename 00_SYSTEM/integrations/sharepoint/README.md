---
id: 00_system__integrations__sharepoint__readme_md
title: SharePoint Integration
owner: ML1
status: active
version: 2.0
created_date: 2026-02-15
last_updated: 2026-03-11
tags: [integration, sharepoint, mcp]
---

# SharePoint Integration

## Contract
- [`sharepoint_sources.yaml`](sharepoint_sources.yaml) — canonical drive/path registry

## Access Surface

Two access modes exist. Both are strictly bounded to the same access surface.

| Mode | Script | Purpose |
|------|--------|---------|
| Script | `scripts/sharepoint_integration.py` | Manual/automated runs |
| MCP | `scripts/sharepoint_mcp_server.py` | Native Claude Code access |

The MCP server is a controlled replacement interface — it replicates the script's
access boundary and does not expand it.

## Drives and Permissions

| Alias | Site | Drive | Write |
|-------|------|-------|-------|
| `legalmatters` | `/sites/LegalMatters` | Working Files | PROHIBITED |
| `documentation` | `/sites/Documentation` | Doc Pro Workspace | PERMITTED (DRAFTS only) |

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

### documentation — Approved Paths
- Read: `Doc Pro  In Tray/SB Execution/DRAFTS`
- Write: `Doc Pro  In Tray/SB Execution/DRAFTS` (filename only, no subdirectories)

## MCP Tools

| Tool | Drive(s) | Operation |
|------|----------|-----------|
| `list_folder` | both | Enumerate folder children (metadata only, no file content) |
| `get_item` | both | Get metadata for one item by path |
| `upload_draft` | documentation only | Upload file to DRAFTS; path hardcoded, filename only |

## Operations NOT Permitted via MCP

- File content reading (any drive)
- Writes to `legalmatters`
- Writes outside `Doc Pro  In Tray/SB Execution/DRAFTS`
- Delete, move, copy, share, or permission operations
- Site or drive enumeration/discovery
- Cross-site search
- Access to any site beyond the two configured drives

## MCP Registration

Registered in `.claude/settings.json` (project-level).
Server process: `scripts/sharepoint_mcp_server.py` (Python 3.9, no external MCP SDK).
Auth: Azure client credentials (AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET from .env).

## Change Notes
- v1.0 2026-02-15: Integration stub created.
- v2.0 2026-03-11: MCP server implemented. Access boundary documented.
  MCP replaces script interface for Claude Code sessions; script retained for
  manual/automated runs. Access surface unchanged.
