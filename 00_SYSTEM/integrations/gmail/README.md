---
id: 00_system__integrations__gmail__readme_md
title: Gmail Integration
owner: ML1
status: draft
version: 2.0
created_date: 2026-02-15
last_updated: 2026-03-14
tags: [integration, gmail, mcp]
---

# Gmail Integration

Status (index): active

## Contract

- `gmail_sources.yaml`

## Access Modes

| Mode | Script | Purpose |
|------|--------|---------|
| Script | `scripts/fetch_gmail.py` | Manual or automated mailbox fetch |
| Script | `scripts/gmail_labeler.py` | Controlled label application from manifest |
| Script | `scripts/run_matter_dashboard.py` | Daily matter pipeline, including optional label execution |
| MCP | `scripts/gmail_mcp_server.py` | Native Claude Code access |

The MCP server is a controlled replacement interface for interactive Gmail work.
It preserves the same approval boundary as the script-based write paths and does
not expand the Gmail access surface.

## MCP Tools

| Tool | Operation | Write |
|------|-----------|-------|
| `list_messages` | List message stubs using Gmail query syntax | No |
| `get_message` | Fetch one message by id | No |
| `list_threads` | List thread stubs using Gmail query syntax | No |
| `get_thread` | Fetch one thread by id | No |
| `list_labels` | List mailbox labels | No |
| `apply_state_label` | Apply one canonical state label to a thread | Yes |
| `apply_matter_label` | Apply one canonical matter label to a thread | Yes |

## Controlled Write Policy

- Default posture is proposal-first.
- Write tools are limited to label application only.
- Every write tool call must include:
  - `approved_by`
  - `approval_artifact`
  - `reason`
- Gmail MCP write audits are appended to:
  - `06_RUNS/ops/gmail_mcp_audit.ndjson`

## Operations NOT Permitted via MCP

- Send mail
- Draft creation or sending
- Delete, trash, or untrash
- Label deletion or label patch/update
- Broad mailbox mutation beyond controlled thread label writes

## Registration

Registered in `.mcp.json` (project root).
Server process: `scripts/gmail_mcp_server.py`.
Auth: Gmail OAuth token from `00_SYSTEM/local_secrets/google_token.json`.

## Change Notes

- v1.0 2026-02-15: Integration stub created.
- v2.0 2026-03-14: Gmail MCP server implemented for interactive use. Read tools
  plus controlled state/matter label writes documented.
