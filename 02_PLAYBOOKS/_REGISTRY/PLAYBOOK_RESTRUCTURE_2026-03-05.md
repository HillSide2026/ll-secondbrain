---
id: 02_playbooks___registry__playbook_restructure_2026_03_05_md
title: Playbook Restructure 2026-03-05
owner: ML1
status: draft
created_date: 2026-03-05
last_updated: 2026-03-05
tags: [migration, playbooks]
---

# Playbook Restructure (2026-03-05)

## Decision

Adopt top-level structure:

- `02_PLAYBOOKS/LL_OPERATIONS/`
- `02_PLAYBOOKS/CONTRACTS/`
- `02_PLAYBOOKS/CORPORATE/`
- `02_PLAYBOOKS/FINANCIAL_SERVICES/`
- `02_PLAYBOOKS/_ASSETS/`
- `02_PLAYBOOKS/_REGISTRY/`

`core`, `substantive`, `execution`, and `system` are metadata categories, not directories.

## Path Mapping

### Operations

- `02_PLAYBOOKS/CORE/doc_drop_issue_list/` -> `02_PLAYBOOKS/LL_OPERATIONS/doc_drop_issue_list/`
- `02_PLAYBOOKS/CORE/inbox_triage/` -> `02_PLAYBOOKS/LL_OPERATIONS/inbox_triage/`
- `02_PLAYBOOKS/CORE/matter_dashboard_update/` -> `02_PLAYBOOKS/LL_OPERATIONS/matter_dashboard_update/`
- `02_PLAYBOOKS/CORE/new_matter_scaffold/` -> `02_PLAYBOOKS/LL_OPERATIONS/new_matter_scaffold/`
- `02_PLAYBOOKS/EXECUTION/review_ritual/` -> `02_PLAYBOOKS/LL_OPERATIONS/review_ritual/`
- `02_PLAYBOOKS/EXECUTION/rollback_procedure/` -> `02_PLAYBOOKS/LL_OPERATIONS/rollback_procedure/`
- `02_PLAYBOOKS/EXECUTION/supervised_execution_runbook/` -> `02_PLAYBOOKS/LL_OPERATIONS/supervised_execution_runbook/`
- `02_PLAYBOOKS/SYSTEM/` -> `02_PLAYBOOKS/LL_OPERATIONS/system_runbooks/`

Legacy preservation:
- `02_PLAYBOOKS/INBOX_TRIAGE/` -> `02_PLAYBOOKS/LL_OPERATIONS/INBOX_TRIAGE_LEGACY/`
- `02_PLAYBOOKS/MATTER_DASHBOARD/` -> `02_PLAYBOOKS/LL_OPERATIONS/MATTER_DASHBOARD_LEGACY/`
- `02_PLAYBOOKS/STAGE3/` -> `02_PLAYBOOKS/LL_OPERATIONS/STAGE3_LEGACY/`

### Practice Workflows

- `02_PLAYBOOKS/SUBSTANTIVE/contracts/` -> `02_PLAYBOOKS/CONTRACTS/WORKFLOWS/`
- `02_PLAYBOOKS/SUBSTANTIVE/corporate/` -> `02_PLAYBOOKS/CORPORATE/WORKFLOWS/`
- `02_PLAYBOOKS/SUBSTANTIVE/financial_services/` -> `02_PLAYBOOKS/FINANCIAL_SERVICES/WORKFLOWS/`

## Notes

- Legacy bucket metadata files are retained under:
  `02_PLAYBOOKS/_REGISTRY/LEGACY_BUCKET_METADATA/`
- Registry paths were updated in:
  - `02_PLAYBOOKS/_REGISTRY/PLAYBOOK_INDEX.md`
  - `02_PLAYBOOKS/_REGISTRY/DRAFT_INDEX.md`
