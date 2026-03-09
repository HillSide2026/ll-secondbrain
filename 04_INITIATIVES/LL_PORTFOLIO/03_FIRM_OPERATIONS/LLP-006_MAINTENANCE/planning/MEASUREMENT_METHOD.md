# Measurement Method

Project ID: LLP-26-07
Project Path: 03_FIRM_OPERATIONS/LLP-006_MAINTENANCE
Stage: Planning

## Method
- Execute reconciliation once per Sunday against active matter set.
- Record run completeness and system-specific extraction results.
- Compute coverage/parity/linkage metrics from observed records only.
- Track exception lifecycle (new, open, resolved) with timestamps.
- Preserve source pointers for all mismatch assertions.

## Calculation Rules
- `active_matters` denominator is the active set from the cycle's canonical matter index snapshot.
- `covered_active_matters` requires usable records from SB, Clio, SharePoint, and Asana for the same matter_id.
- `parity_matters` requires no mismatch in governed status fields between Clio and SB snapshot.
- `sharepoint_linked_matters` requires a valid mapped folder/pointer for the matter.
- `asana_linked_matters` requires at least one valid matter-linked Asana artifact or an explicit N/A classification rule.
- `critical_exceptions_due` includes critical exceptions whose SLA window ended in the measurement window.

## Window and Reporting
- Operational window: weekly Sunday run.
- Default reporting window: trailing 4 weeks for trend metrics.
- If `open_exceptions_last_week = 0`, `exception_backlog_growth_rate` is reported as `N/A` for that cycle.

## Data Sources
- SB matter artifacts (`05_MATTERS`, mappings in `00_SYSTEM`)
- Clio matter export/API snapshot
- SharePoint metadata snapshot
- Asana task/project export/API snapshot
- Reconciliation run logs and exception artifacts
