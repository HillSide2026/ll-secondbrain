---
id: 00_system__integrations__sharepoint__tool_surface_spec_md
title: SharePoint Tool Surface Spec
owner: ML2
status: active
version: 1.0
created_date: 2026-03-28
last_updated: 2026-03-28
tags: [integration, sharepoint, governance, mcp]
---

# SharePoint Tool Surface Spec (v1.0)

Status: approved by ML1

## Purpose

Define the controlled, auditable SharePoint tool surface through which agents may interact with SharePoint as an external execution system rather than as an unbounded workspace.

This artifact is the abstract SharePoint tool contract. It does not by itself widen the currently implemented MCP surface. Runtime exposure must still be explicitly implemented and validated.

## Scope

This specification defines:
- approved SharePoint tool classes
- required input and output structure
- authority boundaries
- write invariants
- logging requirements
- failure conditions
- escalation triggers

This specification does not:
- grant autonomous authority outside existing doctrine
- authorize unrestricted SharePoint browsing
- permit silent write-back into LL systems
- replace ML1 judgment where ambiguity exists

## Architectural Role

- SharePoint is an external execution and storage environment
- SharePoint MCP is the protocol adapter exposing approved SharePoint operations as callable tools
- agents invoke approved tools within explicit task scope
- ML2 governs schemas, guardrails, logging, and change control
- ML1 retains final approval authority for doctrine, exceptions, and expanded scope

SharePoint is not canonical doctrine storage. ML2 remains the authority for doctrine and governed canonical artifacts, while SharePoint may remain authoritative for external operational object facts such as drive item identifiers and paths under the systems-of-record contract.

## Operating Doctrine

A SharePoint tool exists only when all of the following are defined:
- explicit tool name
- input schema
- output schema
- allowed authority
- logging behavior
- failure behavior
- escalation behavior

The system must bias toward:
- read before write
- narrow scope before broad scope
- deterministic retrieval before freeform exploration
- draft generation before authoritative publication
- escalation before assumption

## Authority Model

### Site Class Dependency

SharePoint tool execution must inherit site classification from `POL-059_Integration_Control_Policy.md`.

- `read_only_authority` sites permit retrieval and diagnostic reads only, within explicitly approved site, library, and path scopes
- `managed_workspace` sites permit read, write, and manage operations only when the site is explicitly named in integration contracts, the action is invoked by an approved workflow, runbook, or capability, and run evidence is emitted into ML2

Current approved site classes are defined in:
- `00_SYSTEM/CONFIG/systems_of_record.yml`
- `01_DOCTRINE/03_POLICIES/POL-059_Integration_Control_Policy.md`

### Read Controls

Read and search operations are allowed only when they satisfy the active external read controls in `POL-059_Integration_Control_Policy.md`. At minimum, the read must be triggered by one of:
- QC gate
- ML1 request
- drift detection need

Bulk ingestion remains prohibited unless separately approved.

### Write Invariants

Any write-capable SharePoint tool must enforce the following invariants from active doctrine:
- writes must target designated folders or sites only
- requests must include an artifact version reference
- requests must include a `Derived from ML2 vX.Y` label or equivalent provenance marker
- canonical ML2 paths or artifacts must not be modified externally
- destination scope must validate before execution
- schema validation must pass before execution
- run evidence must be emitted into ML2

For Documentation-site writes and manages, the audit trail must also capture:
- run identifier
- acting tool or agent
- target site, drive, and path
- operation type
- before and after reference where practical
- success or failure state

### Approval-Reference Model

The SharePoint tool surface does not use opaque approval tokens.

When a tool class requires explicit ML1 approval, the request must carry an `approval_reference` that points to an ML2-governed artifact or run record containing:
- approving human
- approved scope
- rationale
- approval timestamp
- expiry, revocation, or scope notes when applicable

Missing, invalid, or out-of-scope `approval_reference` values must hard-fail or escalate.

## Approved Abstract Tool Classes

### Retrieval Tools

Approved abstract tools:
- `sp_get_document`
- `sp_search_documents`
- `sp_list_folder`
- `sp_get_metadata`

These tools are read-only and must remain bounded to approved scope.

### Drafting Tools

Approved abstract tools:
- `sp_create_draft_document`
- `sp_update_draft_document`
- `sp_tag_document`

These tools are allowed only on `managed_workspace` surfaces and only under approved workflows, runbooks, or capabilities.

### Controlled Update Tools

Approved abstract tools:
- `sp_move_document`

These tools are not generally allowed by default and require explicit ML1 approval-reference validation before execution.

### Diagnostic Tools

Approved abstract tools:
- `sp_get_version_history`
- `sp_inspect_library_schema`

These tools are read-only and must not mutate structure, permissions, or workflow control state.

### Prohibited Tool Classes in v1

The following remain prohibited in v1:
- delete operations
- permission modification
- tenant-wide search
- site or library creation
- retention or compliance modification
- autonomous publication or finalization

## Input Contract Requirements

All SharePoint tool inputs must be explicit. No tool may depend on hidden context for:
- site target
- library target
- folder target
- document target
- write destination
- action reason

Write-capable tools must additionally carry:
- workflow, runbook, or capability reference
- artifact version reference
- provenance label or equivalent

ML1-gated tools must additionally carry:
- `approval_reference`

## Output Contract Requirements

All SharePoint tools must return structured, machine-parseable responses containing:
- `status`
- `operation_id`
- `target_ref`
- `result_payload`
- `errors`
- `warnings`
- `executed_at`

Allowed status values:
- `success`
- `partial_success`
- `not_found`
- `permission_denied`
- `validation_failed`
- `version_conflict`
- `scope_denied`
- `connector_error`
- `escalation_required`

## Logging and Auditability

Every SharePoint tool action must generate auditable logs containing:
- `operation_id`
- `tool_name`
- `timestamp`
- `actor_type`
- `actor_id`
- `authorized_scope`
- `target_object`
- `action_type`
- structured input record or input hash
- `output_status`
- `version_before`
- `version_after`
- `reason_code`
- `upstream_artifact_ref`
- `approval_reference` when applicable
- `escalation_flag`

## Failure and Escalation

SharePoint tools must fail explicitly and preserve traceability. Silent mutating retries are prohibited.

Escalate instead of execute when:
- more than one plausible target document exists
- the requested destination is outside approved scope
- the requested action implies publication or finalization
- metadata schema is missing or contradictory
- connector permissions do not match expected doctrine
- a requested action would overwrite non-draft content
- the task requires legal or policy interpretation
- the requested action conflicts with prior system rules

## Current Repo Mapping

The current `scripts/sharepoint_mcp_server.py` implementation is narrower than this abstract tool surface.

Current mapping:
- `list_folder` maps to `sp_list_folder`
- `get_item` maps to a metadata-only subset of `sp_get_metadata`
- `upload_draft` maps to a limited `sp_create_draft_document`
- `copy_template_to_wip` maps to a limited managed-workspace draft-creation helper
- `find_latest_template` and `diff_docs` are bounded Documentation-scoped helper tools

Abstract tools named here remain blocked until both of the following are true:
- they are admitted by the SharePoint control matrix
- they are explicitly implemented in the runtime with schema, scope, and logging enforcement
