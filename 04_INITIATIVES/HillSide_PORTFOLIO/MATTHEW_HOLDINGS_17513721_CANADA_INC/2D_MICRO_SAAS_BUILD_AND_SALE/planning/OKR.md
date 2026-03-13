# OKR

Project ID: MHS-2D-MICRO-SAAS-001
Project Path: 04_INITIATIVES/HillSide_PORTFOLIO/MATTHEW_HOLDINGS_17513721_CANADA_INC/2D_MICRO_SAAS_BUILD_AND_SALE
Stage: Planning

## Decision Use
Use this file weekly to decide if execution is on track for launch, early usage validation, and budget control.

## Objectives and Key Results

### Objective 1: Launch a viable MVP on schedule
- KR1: `mvp_launch_on_or_before_target = 1`
- KR2: `pilot_activation_rate >= 25%`
- KR3: `launch_exception_backlog <= 3`

### Objective 2: Validate early post-launch usage
- KR1: `week4_retention_rate >= 20%`
- KR2: `activated_pilot_users >= 10`

### Objective 3: Maintain budget discipline
- KR1: `project_budget_variance_pct <= 10%`

## KPI Definitions

| KPI | Definition | Formula | Decision Use |
| --- | --- | --- | --- |
| `mvp_launch_on_or_before_target` | Whether MVP goes live by approved launch date | `1 if mvp_launch_date <= target_launch_date else 0` | Launch discipline |
| `pilot_activation_rate` | Share of onboarded pilot users reaching activation event | `(activated_pilot_users / onboarded_pilot_users) * 100` | Product value signal |
| `launch_exception_backlog` | Count of unresolved launch-blocking issues | `open_launch_blockers` | Launch stability control |
| `week4_retention_rate` | Share of activated pilot users still active in week 4 | `(active_week4_users / activated_pilot_users) * 100` | Early usage durability |
| `activated_pilot_users` | Count of pilot users reaching activation event | `count(activated_pilot_users)` | Early traction volume |
| `project_budget_variance_pct` | Variance from approved budget envelope | `((actual_spend - planned_spend) / planned_spend) * 100` | Budget control |

## Measurement Method
- Use product analytics, release logs, and issue tracking logs as primary sources.
- Require timestamped evidence for launch, activation, and retention events.
- Measure budget variance using approved spend envelope and booked spend only.
- Track launch blocker backlog using a fixed severity definition.

## Measurement Rules
- `mvp_launch_on_or_before_target` is valid only when both target date and actual launch date are recorded.
- `activated_pilot_users` requires completion of defined activation event(s), not just signup.
- `launch_exception_backlog` includes only unresolved severity-1 or severity-2 launch blockers.
- `week4_retention_rate` includes only users who reached activation before week-4 measurement cut-off.
- `project_budget_variance_pct` excludes speculative or unbooked expenses.

## Reporting Cadence
- Weekly trailing 7 days for operating review.
- Monthly rollup for trend and decision support.

## Baseline Capture

### Baseline Window
- Start: 2026-03-21
- End: 2026-04-20

### Baseline Purpose
Capture the first implementation-cycle baseline for launch discipline, user activation, retention, launch stability, and budget variance.

### Baseline Inclusion Rules
- Include only events with timestamped evidence.
- Include only pilot users onboarded through approved channels.
- Include only spend entries booked to this project.

### Baseline Output
- Baseline snapshot for all defined project KPIs.
- Initial variance and risk trend notes for ML1 review.

## Threshold Governance
Thresholds are proposed in `ML1_METRIC_APPROVAL.md` and become active only after explicit ML1 approval.
