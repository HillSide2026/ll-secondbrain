---
id: 04_initiatives__system_portfolio__sys_003_sharepoint_integration__readme_md
title: SYS-003 — SharePoint Integration
owner: ML1
status: planning
created_date: 2026-03-28
last_updated: 2026-03-28
tags: [system-portfolio, integration, sharepoint]
---

# SYS-003 — SharePoint Integration

## Project Classification

- Project Type: `Operational Project`
- Project Subtype: `System Integration Packet`

## Purpose

Formalize the active SharePoint integration surface inside the System Portfolio
so its multi-site authority model, runtime tools, and governed wrappers are
described by a canonical project packet.

## Scope

### In Scope

- SharePoint script and MCP integration surfaces
- Site-class and runtime-boundary documentation
- LegalMatters read-only surface
- Documentation and Clients managed-workspace surfaces
- SharePoint governance wrappers and helper tools

### Out of Scope

- Treating SharePoint as canonical ML2 doctrine storage
- Tenant-wide ungoverned SharePoint access
- Unbounded cross-site mutation
- Any implication that every approved doctrine surface is already implemented in runtime

## Current Runtime State

- SharePoint integration is active and in use.
- The runtime now includes both metadata and governed write/management surfaces.
- The actual surface is broader than the original backlog label of "read-only integration."
- This packet is a retroactive governance formalization of an already active and materially evolved integration.

## Approval State

Initiating -> Planning approved by ML1 on `2026-03-28`.
The integration surface is active. Planning is now authorized to normalize the
boundary between doctrine, control matrix, and runtime implementation.

## Artifact Layout

Initiation artifacts live in `initiation/`:

- `initiation/PROJECT_CHARTER.md`
- `initiation/PROBLEM_STATEMENT.md`
- `initiation/SUCCESS_CRITERIA.md`
- `initiation/STAKEHOLDERS.md`
- `initiation/RISK_SCAN.md`
- `initiation/APPROVAL_RECORD.md`

Planning artifacts live in `planning/`:

- `planning/SCOPE_STATEMENT.md`
- `planning/PROJECT_PLAN.md`
- `planning/ASSUMPTIONS_CONSTRAINTS.md`
- `planning/DEPENDENCIES.md`
- `planning/RISK_REGISTER.md`
- `planning/COMMUNICATION_PLAN.md`
- `planning/METRICS.md`

## Key Runtime Links

- `00_SYSTEM/integrations/sharepoint/README.md`
- `00_SYSTEM/integrations/sharepoint/sharepoint_sources.yaml`
- `00_SYSTEM/integrations/sharepoint/sharepoint_tool_surface_spec.md`
- `00_SYSTEM/integrations/sharepoint/sharepoint_tool_control_matrix.md`
- `scripts/sharepoint_integration.py`
- `scripts/sharepoint_mcp_server.py`
