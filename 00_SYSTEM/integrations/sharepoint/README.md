---
id: 00_system__integrations__sharepoint__readme_md
title: SharePoint Integration
owner: ML1
status: active
version: 2.1
created_date: 2026-02-15
last_updated: 2026-03-27
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

## Sites, Drives, and Permissions

| Alias | Site | Drive Scope | Authority |
|-------|------|-------------|-----------|
| `legalmatters` | `/sites/LegalMatters` | Working Files | READ ONLY |
| `documentation` | `/sites/Documentation` | Site-wide across approved drives/libraries | READ / WRITE / MANAGE |

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

## MCP Tools

| Tool | Drive(s) | Operation |
|------|----------|-----------|
| `list_folder` | both | Enumerate folder children (metadata only, no file content) |
| `get_item` | both | Get metadata for one item by path |
| `upload_draft` | documentation only | Upload file to Documentation workspace surface |

## Operations NOT Permitted via MCP

- File content reading (any drive)
- Writes to `legalmatters`
- Delete, move, copy, share, or permission operations
- Site or drive enumeration/discovery
- Cross-site search
- Access to any site beyond the two configured drives

Site-wide Documentation authority is approved in doctrine, but MCP/server implementation must still declare the exact tool surface it exposes. Broader site authority does not require exposing every possible Graph operation to every runtime tool.

## MCP Registration

Registered in `.mcp.json` (project root).
Server process: `scripts/sharepoint_mcp_server.py` (Python 3.9, no external MCP SDK).
Auth: Azure client credentials (AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET from .env).

## Change Notes
- v1.0 2026-02-15: Integration stub created.
- v2.0 2026-03-11: MCP server implemented. Access boundary documented.
  MCP replaces script interface for Claude Code sessions; script retained for
  manual/automated runs. Access surface unchanged.
- v2.1 2026-03-27: Documentation site elevated to managed-workspace authority
  (site-wide read/write/manage) by ML1 direction. LegalMatters remains read-only.
