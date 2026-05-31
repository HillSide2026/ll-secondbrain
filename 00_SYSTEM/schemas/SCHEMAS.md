---
id: 00_system__schemas_md
title: Artifact Schemas
owner: ML1
status: draft
created_date: 2026-02-08
last_updated: 2026-03-06
tags: []
---

# Artifact Schemas

All markdown files in this repository MUST begin with YAML frontmatter.

## Required Fields (All Artifacts)

---
id:
title:
owner: ML1
status: draft | proposed | approved | deprecated
created_date:
last_updated:
tags: []
---

## Additional Fields (Doctrine)

---
effective_date:
supersedes:
provenance:
  decided_by: ML1
  decided_on:
  context:
---

## Matter

Matter = {
  overview,
  facts,
  Records (documents + communications including email)
  analysis,
  Outputs
  actions,
}

---

## MATTER.yaml Schema (05_MATTERS)

Location: `05_MATTERS/{delivery_status}/{matter_id}/MATTER.yaml`

### Canonical Matter-Record Fields

```yaml
matter_id: string                  # Canonical matter identifier
clio_matter_id: string             # Must match matter_id
client_name: string                # Canonical client identity
instructing_officer_name: string   # Canonical instructing officer; null if data gap
matter_description: string         # Canonical matter description; null if data gap
status: enum                       # Pending | Open | Closed
delivery_status: enum              # Lawyer attention priority
fulfillment_status: enum           # Admin workload state
engagement_date: date              # Canonical engagement/opening date
closed_date: date                  # Canonical closure date; null until set
services:
  - service_type: enum             # solution | strategy
    service_name: string
```

### Compatibility And Operational Fields

```yaml
matter_name: string      # Legacy display/matter label retained for compatibility
created_date: date       # Legacy creation/opening field retained during migration
delivery_stage: enum     # Operational lifecycle field; important but not matter canon
practice_area: string    # Optional descriptive field
```

Legacy compatibility:
- `solutions` MAY be present and is normalized to `services` with `service_type=solution`
- `strategies` MAY be present and is normalized to `services` with `service_type=strategy`
- New authoring should use `services` only
- `matter_name` and `created_date` remain supported while canonical consumers
  migrate to `client_name` / `engagement_date`
- `delivery_stage` may remain in `MATTER.yaml`, but it is not a matter-level
  canonical field under Matter Management

### Field Enums

| Field | Allowed Values |
|-------|----------------|
| `status` | `Open` \| `Pending` \| `Closed` |
| `delivery_status` | `essential` \| `strategic` \| `standard` \| `normal` (highest to lowest) |
| `delivery_stage` | `backlog` \| `activated` \| `active` \| `parked` \| `finished` (operational; non-canonical) |
| `fulfillment_status` | `urgent` \| `active` \| `keep in view` \| `dormant` \| `inactive` \| `pausing` |
| `services[].service_type` | `solution` \| `strategy` |

### Non-Inference Rule

These fields remain independent. Do not infer any field from any other:
- `status` (Clio) does not imply `delivery_status`, `delivery_stage`, or `fulfillment_status`
- `delivery_status` (ML1) does not imply `status`, `delivery_stage`, or `fulfillment_status`
- `delivery_stage` (ML1 operational lifecycle) does not imply `status`, `delivery_status`, or `fulfillment_status`
- `fulfillment_status` (Admin) does not imply `status`, `delivery_status`, or `delivery_stage`

### Derived Category: ML Active

`ML Active` is a computed category (not a stored field) defined by:
- `status` in `Open|Pending`
- `delivery_status` in `Essential|Strategic|Standard`
- `fulfillment_status` in `urgent|active`

`ML Watch` is a computed category for dormant matters kept visible:
- `status` in `Open|Pending`
- `delivery_status` = `normal` AND `delivery_stage` in `parked|backlog`
- `fulfillment_status` in `keep in view|active|urgent`

### Example

```yaml
matter_id: "25-927-00003"
clio_matter_id: "25-927-00003"
matter_name: "Stream Ventures Limited"
client_name: "Stream Ventures Limited"
instructing_officer_name: null
matter_description: "SnowCap AML Policy Transition"
status: "Open"
delivery_status: "Essential"
fulfillment_status: "urgent"
engagement_date: "2025-09-27"
created_date: "2025-09-27"
closed_date: null
services:
  - service_type: "solution"
    service_name: "shareholder_agreement"
    status: "active"
    playbook_ref: "02_PLAYBOOKS/CORPORATE/WORKFLOWS/solutions/shareholder_agreement"
  - service_type: "strategy"
    service_name: "closing_negotiation"
    status: "active"
```

### Directory Mapping

Matters are placed in directories by `delivery_status` only:
- `essential` → `05_MATTERS/ESSENTIAL/`
- `strategic` → `05_MATTERS/STRATEGIC/`
- `standard` → `05_MATTERS/STANDARD/`
- `normal` → `05_MATTERS/NORMAL/`
---

## Matter Stages Schema

Location: `00_SYSTEM/schemas/SCHEMAS_MATTER_STAGES.md`  
Status: draft

## Matter Summary — Schema

Location: `00_SYSTEM/schemas/SCHEMAS_MATTER_SUMMARY.md`  
Status: draft

## Solutions Schema

Location: `00_SYSTEM/schemas/SCHEMAS_SOLUTIONS.md`  
Status: draft

## Draft Placement Plan — Schema

Location: `00_SYSTEM/schemas/SCHEMAS_INBOX_TRIAGE.md`  
Status: draft

## Risk Model — Schema

Location: `00_SYSTEM/schemas/SCHEMAS_RISK_MODEL.md`  
Status: draft

## Office Day — Schema

Location: `00_SYSTEM/schemas/SCHEMAS_OFFICE_DAY.md`  
Status: draft

## Run Log Schema — Matter Dashboard

### Required Fields
- run_id
- timestamp
- operator
- ledger_doc_id
- approved_folder_id
- boundary_check: pass/fail
- inputs_used (versions/hashes)
- actions_taken
- rows_added
- rows_updated
- rows_flagged_needs_review
- refusal_reason (if any)
- status: ok | noop | refused | partial

### Storage
- Logs stored under `06_RUNS/`
- One log per run cycle
- Immutable after write

### Purpose
Enable audit, rollback analysis, and post-mortem review without re-running the system.

---

## Gmail Label Audit Log (NDJSON)

Each line is a JSON object with the following required fields:

- message_id
- gmail_thread_id
- label_applied_or_removed
- matter_id
- operation (add | remove)
- timestamp (UTC, ISO-8601)
- approving_human
- approval_artifact_reference
- reason
- status (ok | refused | failed)
