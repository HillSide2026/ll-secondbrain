---
id: 00_system__integrations__sharepoint__tool_control_matrix_md
title: SharePoint Tool Surface Control Matrix
owner: ML2
status: draft
version: 1.0
created_date: 2026-03-28
last_updated: 2026-03-28
tags: [integration, sharepoint, governance, control-matrix]
---

# SharePoint Tool Surface Control Matrix (v1.0)

Status: Draft for ML1 approval

## Purpose

Define execution permissions for each approved abstract SharePoint tool under ML2 governance.

## Legend

- `ALLOWED` means the tool may execute only within the defined site class, scope, schema, and logging guardrails
- `REQUIRES ML1 APPROVAL` means execution requires a valid `approval_reference`
- `PROHIBITED` means the tool is blocked in v1 regardless of prompt or chaining attempt

## Global Conditions

### Allowed Read Tools

Even when marked `ALLOWED`, read tools must:
- remain within approved site, library, and path scope
- satisfy the active read controls in `POL-059_Integration_Control_Policy.md`
- avoid tenant-wide discovery or hidden inference
- generate full audit logs

### Allowed Write Tools

Even when marked `ALLOWED`, write tools must:
- target a site classified as `managed_workspace`
- be invoked by an approved workflow, runbook, or capability
- write only to designated folders or sites
- include artifact version reference
- include `Derived from ML2 vX.Y` provenance labeling
- pass schema validation before execution
- emit run evidence into ML2

### ML1-Gated Tools

Tools in the `REQUIRES ML1 APPROVAL` class must include a valid `approval_reference` pointing to an ML2 artifact or run record that states:
- approving human
- approved scope
- rationale
- timestamp
- expiry or scope notes when applicable

## Control Matrix

| Tool Name | Category | Control | Notes |
|-----------|----------|---------|-------|
| `sp_get_document` | Read | `ALLOWED` | Scoped retrieval only; read controls apply |
| `sp_search_documents` | Read | `ALLOWED` | Must be bounded; no tenant-wide search |
| `sp_list_folder` | Read | `ALLOWED` | Known folder or approved library scope only |
| `sp_get_metadata` | Read | `ALLOWED` | Metadata only; no hidden inference |
| `sp_get_version_history` | Diagnostic | `ALLOWED` | Metadata only |
| `sp_inspect_library_schema` | Diagnostic | `ALLOWED` | Structure only; no modification |
| `sp_create_draft_document` | Draft | `ALLOWED` | `managed_workspace` only; approved workflow, runbook, or capability required |
| `sp_update_draft_document` | Draft | `ALLOWED` | `managed_workspace` only; draft-state only; version-safe update |
| `sp_tag_document` | Draft | `ALLOWED` | `managed_workspace` only; metadata schema must validate |
| `sp_move_document` | Controlled Update | `REQUIRES ML1 APPROVAL` | Cross-boundary risk; `approval_reference` required |
| `(future) sp_publish_document` | Controlled Update | `REQUIRES ML1 APPROVAL` | Not admitted to v1 runtime; `approval_reference` required |
| `(future) sp_bulk_update` | Controlled Update | `REQUIRES ML1 APPROVAL` | High blast radius; `approval_reference` required |
| `(any) delete operation` | Destructive | `PROHIBITED` | Removed in v1 |
| `(any) permission modification` | Admin | `PROHIBITED` | Governance boundary |
| `(any) tenant-wide search` | Read | `PROHIBITED` | Scope violation |
| `(any) site or library creation` | Admin | `PROHIBITED` | Out of scope |
| `(any) retention or compliance change` | Admin | `PROHIBITED` | Legal and governance risk |
| `(any) autonomous publish` | Workflow | `PROHIBITED` | Violates ML1 authority |

## Enforcement Rules

### Allowed Does Not Mean Unbounded

All `ALLOWED` tools must still:
- validate site class
- validate scope
- validate schema
- emit full audit logs
- fail safe on ambiguity

### Capability Does Not Equal Permission

Even if SharePoint can technically perform an action, the system may:
- decline to expose it
- restrict it to narrower scope
- require ML1 intervention before execution

### No Implicit Promotion

No action may move from `ALLOWED` to ML1-approved exception handling without an explicit approval artifact. No action may move from `PROHIBITED` to executable without spec revision and ML1 approval.

## Execution Gate

Before any tool call:

```text
IF tool not in matrix -> BLOCK

IF tool is PROHIBITED -> BLOCK + log

IF tool REQUIRES ML1 APPROVAL:
    IF valid approval_reference present and in scope -> ALLOW
    ELSE -> ESCALATE

IF tool is ALLOWED:
    IF scope invalid -> FAIL SAFE
    IF read tool and read controls not satisfied -> FAIL SAFE
    IF write tool and site_class != managed_workspace -> FAIL SAFE
    IF write tool and no approved workflow/runbook/capability ref -> FAIL SAFE
    IF write invariants or schema validation fail -> FAIL SAFE
    ELSE -> ALLOW
```

## Current Runtime Note

This matrix governs the abstract approved SharePoint tool surface.

The current `scripts/sharepoint_mcp_server.py` runtime implements only a narrower subset. Abstract tools named here remain blocked until they are explicitly implemented and validated in the runtime.
