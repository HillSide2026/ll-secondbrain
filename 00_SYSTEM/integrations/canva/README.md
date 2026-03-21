---
id: 00_system__integrations__canva__readme_md
title: Canva Integration
owner: ML1
status: draft
version: 1.0
created_date: 2026-03-21
last_updated: 2026-03-21
tags: [integration, canva, mcp, design]
---

# Canva Integration

Status (index): initiated

## Contract

- `canva_sources.yaml`

## Access Surface

Two access modes exist at present:

| Mode | Script | Purpose |
|------|--------|---------|
| MCP | `canva_bridge.py` | Persistent Claude-callable Canva access |
| Browser OAuth | `start_oauth` tool + local callback | One-time consent/bootstrap |

The MCP server replaces the old one-shot connectivity proof with a persistent,
tool-callable interface. It does not authorize publishing or distribution.

## MCP Tools

| Tool | Operation | Write |
|------|-----------|-------|
| `auth_status` | Inspect Canva OAuth/token readiness | No |
| `start_oauth` | Start one-time OAuth bootstrap | No |
| `list_designs` | List Canva designs | No |
| `get_design` | Fetch one design by id | No |
| `create_design` | Create a Canva draft design | Yes, draft only |

## Controlled Write Policy

- Default posture is draft-only.
- `create_design` creates draft designs only.
- No publish, delete, share, or permission mutation tools exist.
- Output authorization remains outside Canva and outside the MCP server.

## Operations NOT Permitted via MCP

- Publish or distribute designs
- Delete designs
- Change team/workspace permissions
- Bypass approved templates or brand controls
- Treat Canva as canonical storage for doctrine or brand authority

## Registration

Registered in `.claude/settings.json` (project-level).
Server process: `canva_bridge.py`.
Auth: Canva OAuth client credentials from `.env`.

## Change Notes

- v1.0 2026-03-21: Canva MCP server introduced. Supports OAuth bootstrap,
  design listing, design lookup, and draft design creation.
