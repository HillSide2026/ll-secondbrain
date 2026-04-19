---
run_id: 20260419_052342_run_log_validator
run_date: 2026-04-19
run_time: 05:23:42 UTC
agent_or_script: run_log_validator.py
matter_id: none
task: Validate run log entries against PRO-023 Run Log Standard
slas_covered: [SLA-ML2-001, KPI-ML2-004]
output_classification: internal
status: complete
---

# Run Log Validation — 2026-04-19

## Summary

Scanned `06_RUNS` for run log files.

| Metric | Value |
|--------|-------|
| Files scanned | 6 |
| Files passed | 0 |
| Files with violations | 6 |
| Total violations | 61 |
| Overall result | **FAIL** |

## SLA Status

| SLA | Status |
|-----|--------|
| SLA-ML2-001 Record Integrity | BREACH |
| KPI-ML2-004 Schema Compliance | 0.0% |

## Findings

### Critical (36)

- **06_RUNS/RUN-2026-02-13-STAGE5-template/runlog.md** — `frontmatter`: No frontmatter block found
- **06_RUNS/STAGE4.1/RUN_001.md** — `run_date`: Missing required field: run_date
- **06_RUNS/STAGE4.1/RUN_001.md** — `run_time`: Missing required field: run_time
- **06_RUNS/STAGE4.1/RUN_001.md** — `agent_or_script`: Missing required field: agent_or_script
- **06_RUNS/STAGE4.1/RUN_001.md** — `matter_id`: Missing required field: matter_id
- **06_RUNS/STAGE4.1/RUN_001.md** — `task`: Missing required field: task
- **06_RUNS/STAGE4.1/RUN_001.md** — `slas_covered`: Missing required field: slas_covered
- **06_RUNS/STAGE4.1/RUN_001.md** — `output_classification`: Missing required field: output_classification
- **06_RUNS/STAGE4.1/RUN_002.md** — `run_date`: Missing required field: run_date
- **06_RUNS/STAGE4.1/RUN_002.md** — `run_time`: Missing required field: run_time
- **06_RUNS/STAGE4.1/RUN_002.md** — `agent_or_script`: Missing required field: agent_or_script
- **06_RUNS/STAGE4.1/RUN_002.md** — `matter_id`: Missing required field: matter_id
- **06_RUNS/STAGE4.1/RUN_002.md** — `task`: Missing required field: task
- **06_RUNS/STAGE4.1/RUN_002.md** — `slas_covered`: Missing required field: slas_covered
- **06_RUNS/STAGE4.1/RUN_002.md** — `output_classification`: Missing required field: output_classification
- **06_RUNS/STAGE4.1/RUN_003.md** — `run_date`: Missing required field: run_date
- **06_RUNS/STAGE4.1/RUN_003.md** — `run_time`: Missing required field: run_time
- **06_RUNS/STAGE4.1/RUN_003.md** — `agent_or_script`: Missing required field: agent_or_script
- **06_RUNS/STAGE4.1/RUN_003.md** — `matter_id`: Missing required field: matter_id
- **06_RUNS/STAGE4.1/RUN_003.md** — `task`: Missing required field: task
- **06_RUNS/STAGE4.1/RUN_003.md** — `slas_covered`: Missing required field: slas_covered
- **06_RUNS/STAGE4.1/RUN_003.md** — `output_classification`: Missing required field: output_classification
- **06_RUNS/STAGE4.1/RUN_004.md** — `run_date`: Missing required field: run_date
- **06_RUNS/STAGE4.1/RUN_004.md** — `run_time`: Missing required field: run_time
- **06_RUNS/STAGE4.1/RUN_004.md** — `agent_or_script`: Missing required field: agent_or_script
- **06_RUNS/STAGE4.1/RUN_004.md** — `matter_id`: Missing required field: matter_id
- **06_RUNS/STAGE4.1/RUN_004.md** — `task`: Missing required field: task
- **06_RUNS/STAGE4.1/RUN_004.md** — `slas_covered`: Missing required field: slas_covered
- **06_RUNS/STAGE4.1/RUN_004.md** — `output_classification`: Missing required field: output_classification
- **06_RUNS/STAGE4.1/RUN_005.md** — `run_date`: Missing required field: run_date
- **06_RUNS/STAGE4.1/RUN_005.md** — `run_time`: Missing required field: run_time
- **06_RUNS/STAGE4.1/RUN_005.md** — `agent_or_script`: Missing required field: agent_or_script
- **06_RUNS/STAGE4.1/RUN_005.md** — `matter_id`: Missing required field: matter_id
- **06_RUNS/STAGE4.1/RUN_005.md** — `task`: Missing required field: task
- **06_RUNS/STAGE4.1/RUN_005.md** — `slas_covered`: Missing required field: slas_covered
- **06_RUNS/STAGE4.1/RUN_005.md** — `output_classification`: Missing required field: output_classification

### Major (25)

- **06_RUNS/STAGE4.1/RUN_001.md** — `run_id`: run_id format invalid: 'STAGE4.1_RUN_001' (expected YYYYMMDD_HHMMSS_<agent>)
- **06_RUNS/STAGE4.1/RUN_001.md** — `status`: Invalid status: 'draft' (must be complete/partial/failed)
- **06_RUNS/STAGE4.1/RUN_001.md** — `body`: Missing required body section: 'findings'
- **06_RUNS/STAGE4.1/RUN_001.md** — `body`: Missing required body section: 'violations'
- **06_RUNS/STAGE4.1/RUN_001.md** — `body`: Missing required body section: 'next actions'
- **06_RUNS/STAGE4.1/RUN_002.md** — `run_id`: run_id format invalid: 'STAGE4.1_RUN_002' (expected YYYYMMDD_HHMMSS_<agent>)
- **06_RUNS/STAGE4.1/RUN_002.md** — `status`: Invalid status: 'draft' (must be complete/partial/failed)
- **06_RUNS/STAGE4.1/RUN_002.md** — `body`: Missing required body section: 'findings'
- **06_RUNS/STAGE4.1/RUN_002.md** — `body`: Missing required body section: 'violations'
- **06_RUNS/STAGE4.1/RUN_002.md** — `body`: Missing required body section: 'next actions'
- **06_RUNS/STAGE4.1/RUN_003.md** — `run_id`: run_id format invalid: 'STAGE4.1_RUN_003' (expected YYYYMMDD_HHMMSS_<agent>)
- **06_RUNS/STAGE4.1/RUN_003.md** — `status`: Invalid status: 'draft' (must be complete/partial/failed)
- **06_RUNS/STAGE4.1/RUN_003.md** — `body`: Missing required body section: 'findings'
- **06_RUNS/STAGE4.1/RUN_003.md** — `body`: Missing required body section: 'violations'
- **06_RUNS/STAGE4.1/RUN_003.md** — `body`: Missing required body section: 'next actions'
- **06_RUNS/STAGE4.1/RUN_004.md** — `run_id`: run_id format invalid: 'STAGE4.1_RUN_004' (expected YYYYMMDD_HHMMSS_<agent>)
- **06_RUNS/STAGE4.1/RUN_004.md** — `status`: Invalid status: 'draft' (must be complete/partial/failed)
- **06_RUNS/STAGE4.1/RUN_004.md** — `body`: Missing required body section: 'findings'
- **06_RUNS/STAGE4.1/RUN_004.md** — `body`: Missing required body section: 'violations'
- **06_RUNS/STAGE4.1/RUN_004.md** — `body`: Missing required body section: 'next actions'
- **06_RUNS/STAGE4.1/RUN_005.md** — `run_id`: run_id format invalid: 'STAGE4.1_RUN_005' (expected YYYYMMDD_HHMMSS_<agent>)
- **06_RUNS/STAGE4.1/RUN_005.md** — `status`: Invalid status: 'draft' (must be complete/partial/failed)
- **06_RUNS/STAGE4.1/RUN_005.md** — `body`: Missing required body section: 'findings'
- **06_RUNS/STAGE4.1/RUN_005.md** — `body`: Missing required body section: 'violations'
- **06_RUNS/STAGE4.1/RUN_005.md** — `body`: Missing required body section: 'next actions'

## Violations

See Findings above. 61 total violation(s).

## Next Actions

Fix 61 violation(s) identified above. Re-run validator after corrections.
