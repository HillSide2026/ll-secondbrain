# Metric Definition

Project ID: LLP-26-07
Project Path: 03_FIRM_OPERATIONS/LLP-006_MAINTENANCE
Stage: Planning

## LLP-006 Core Metrics

| KPI | Definition | Formula |
| --- | --- | --- |
| `weekly_run_completion_rate` | Share of scheduled Sunday runs completed | `(completed_runs / scheduled_runs) * 100` |
| `active_matter_coverage_rate` | Share of active matters represented in all required reconciliation inputs | `(covered_active_matters / active_matters) * 100` |
| `clio_sb_status_parity_rate` | Share of active matters with no Clio-vs-SB status mismatch | `(parity_matters / active_matters) * 100` |
| `sharepoint_linkage_rate` | Share of active matters with valid SharePoint linkage | `(sharepoint_linked_matters / active_matters) * 100` |
| `asana_linkage_rate` | Share of active matters with valid Asana linkage | `(asana_linked_matters / active_matters) * 100` |
| `critical_exception_resolution_rate` | Share of critical exceptions resolved within SLA window | `(critical_resolved_within_sla / critical_exceptions_due) * 100` |
| `exception_backlog_growth_rate` | Week-over-week growth rate of unresolved exceptions | `((open_exceptions_this_week - open_exceptions_last_week) / open_exceptions_last_week) * 100` |

## Goal Alignment
- Coverage/parity metrics support accurate matter status refresh.
- Linkage metrics support deterministic cross-system reconciliation.
- Resolution/backlog metrics support sustainable weekly operations.

## Target Status
- Thresholds are `TBD` pending ML1 approval.

## Measurement Cadence
- Weekly (Sunday cycle, reported Monday)
- Monthly governance rollup
