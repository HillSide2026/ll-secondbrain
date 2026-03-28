---
id: 00_system__integrations__sharepoint__tool_control_matrix_md
title: SharePoint Tool Surface Control Matrix
owner: ML2
status: active
version: 1.3
created_date: 2026-03-28
last_updated: 2026-03-28
tags: [integration, sharepoint, governance, control-matrix]
---

# SharePoint Tool Surface Control Matrix (v1.3)

Status: approved by ML1

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
- target either a site classified as `managed_workspace` or an explicitly approved ML1 sub-surface exception declared in integration contracts
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

Runtime-specific exception:
- `manage_clients_site` uses `approval_token` for its ML1-gated `/sites/Clients` operations

## Control Matrix

| Tool Name | Category | Control | Notes |
|-----------|----------|---------|-------|
| `sp_get_document` | Read | `ALLOWED` | Scoped retrieval only; read controls apply |
| `sp_search_documents` | Read | `ALLOWED` | Must be bounded; no tenant-wide search |
| `sp_list_folder` | Read | `ALLOWED` | Known folder or approved library scope only |
| `sp_get_metadata` | Read | `ALLOWED` | Metadata only; no hidden inference |
| `sp_get_site_page` | Read | `ALLOWED` | Explicit page path only; currently admitted for the Clients `SitePages/*.aspx` review surface |
| `sp_get_version_history` | Diagnostic | `ALLOWED` | Metadata only |
| `sp_inspect_library_schema` | Diagnostic | `ALLOWED` | Structure only; no modification |
| `sp_create_draft_document` | Draft | `ALLOWED` | `managed_workspace` only; approved workflow, runbook, or capability required |
| `sp_update_draft_document` | Draft | `ALLOWED` | `managed_workspace` only; draft-state only; version-safe update |
| `sp_tag_document` | Draft | `ALLOWED` | `managed_workspace` only; metadata schema must validate |
| `sp_update_site_page_content` | Controlled Update | `ALLOWED` | Existing pages only; current helper admitted for Clients `SitePages/*.aspx`; this tool remains content-focused by implementation but does not cap broader Clients SitePages authority |
| `sp_provision_client_workspace` | Controlled Update | `ALLOWED` | Clients managed-workspace helper; may create one page, create one `*-Documents` library, assign existing principals, and add one shared-home navigation link |
| `manage_clients_site` | Controlled Update | `ALLOWED` / `REQUIRES ML1 APPROVAL` | `/sites/Clients` wrapper. Read, create, update, folder create/rename/move, library create/update, navigation upsert/reorder, and inspection operations are allowed without token. Publish, delete, set-home, permission mutation, inheritance changes, and folder/library/navigation delete require `approval_token`. |
| `sp_move_document` | Controlled Update | `REQUIRES ML1 APPROVAL` | Cross-boundary risk; `approval_reference` required |
| `(future) sp_publish_document` | Controlled Update | `REQUIRES ML1 APPROVAL` | Not admitted to v1 runtime; `approval_reference` required |
| `(future) sp_bulk_update` | Controlled Update | `REQUIRES ML1 APPROVAL` | High blast radius; `approval_reference` required |
| `(any) unscoped delete operation` | Destructive | `PROHIBITED` | Removed in v1 outside explicitly admitted wrappers and scope locks |
| `(any) unscoped permission modification` | Admin | `PROHIBITED` | Governance boundary outside an explicitly admitted tool and scope |
| `(any) tenant-wide search` | Read | `PROHIBITED` | Scope violation |
| `(any) arbitrary cross-site site or library creation` | Admin | `PROHIBITED` | Out of scope outside an explicitly admitted tool and scope |
| `(any) group or tenant identity administration` | Admin | `PROHIBITED` | Out of scope |
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
    IF valid approval_reference or runtime-specific approval token present and in scope -> ALLOW
    ELSE -> ESCALATE

IF tool is ALLOWED:
    IF scope invalid -> FAIL SAFE
    IF read tool and read controls not satisfied -> FAIL SAFE
    IF write tool and site_class != managed_workspace and no explicit ML1-approved sub-surface exception applies -> FAIL SAFE
    IF write tool and no approved workflow/runbook/capability ref -> FAIL SAFE
    IF write invariants or schema validation fail -> FAIL SAFE
    ELSE -> ALLOW
```

## Current Runtime Note

This matrix governs the abstract approved SharePoint tool surface.

The current `scripts/sharepoint_mcp_server.py` runtime now includes the broad
`manage_clients_site` wrapper for `/sites/Clients` in addition to the narrower
helper tools. Abstract tools without explicit runtime implementation remain
blocked until they are implemented and validated in the runtime.
