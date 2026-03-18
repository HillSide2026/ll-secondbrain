---
id: 04_initiatives__ll_portfolio__07_strategic_projects__llp_024_nda_esq__metrics_md
title: NDA Esq - Metrics
owner: ML1
status: approved
created_date: 2026-03-14
last_updated: 2026-03-15
tags: [nda-esq, strategic-project, planning, metrics]
---

# Metrics and Validation

Project ID: LLP-26-24
Project Path: 04_INITIATIVES/LL_PORTFOLIO/07_STRATEGIC_PROJECTS/LLP-024_NDA_ESQ
Stage: Planning

## Metric Definition

| KPI | Definition | Formula |
| --- | --- | --- |
| `mvp_ready_on_or_before_target` | Whether the MVP is launched on or before the approved target date | `1 if launch_date <= target_date, else 0` |
| `first_month_onboarded_users` | Number of onboarded users in the first 30 days after MVP launch | `count(onboarded_users in first_30_days)` |
| `nda_risk_flag_accuracy_rate` | Share of sampled NDA risk flags that match the approved validation benchmark | `(correct_risk_flags / sampled_risk_flags) * 100` |
| `first_90_day_users` | Number of users acquired in the first 90 days after launch | `count(users in first_90_days)` |
| `mrr_4_month` | Monthly recurring revenue achieved by month 4 | `sum(active_recurring_revenue at month_4_close)` |
| `cac_per_paid_user` | Average acquisition cost per paid user | `acquisition_spend / paid_users` |
| `monthly_mrr_growth_rate` | Month-over-month MRR growth rate | `((current_month_mrr - prior_month_mrr) / prior_month_mrr) * 100` |
| `customer_retention_rate` | Share of customers retained over the defined retention window | `(retained_customers / starting_customers) * 100` |
| `support_response_time_hours` | Average or monitored response time for customer support | `average(first_response_time_hours)` |

### Goal Alignment

- `mvp_ready_on_or_before_target`, `first_month_onboarded_users`, and `nda_risk_flag_accuracy_rate` support product-readiness goals.
- `first_90_day_users`, `mrr_4_month`, and `cac_per_paid_user` support acquisition and growth goals.
- `monthly_mrr_growth_rate`, `customer_retention_rate`, and `support_response_time_hours` support operating-performance goals.

### Target Status

- Thresholds are proposed in `ML1_METRIC_APPROVAL.md`.
- Metrics are not active implementation gates until ML1 signs off on thresholds.

### Measurement Cadence

- weekly planning review for readiness metrics
- monthly governance summary for revenue and retention metrics

## Measurement Method

### Method

- Capture product, acquisition, subscription, and support events from approved operational systems.
- Use only observed system events, revenue records, campaign spend, and sampled validation outputs.
- Maintain evidence references for each aggregated metric report.
- Separate launch-window metrics from ongoing operating metrics so thresholds are not mixed across phases.

### Calculation Rules

- `mvp_ready_on_or_before_target`
  Rule: binary success measure based on launch date versus approved target date.
- `first_month_onboarded_users`
  Window: first 30 calendar days after MVP launch.
  Rule: count unique onboarded users with completed account activation.
- `nda_risk_flag_accuracy_rate`
  Numerator: correctly flagged risks in the approved sample set.
  Denominator: total sampled risk flags reviewed against the approved benchmark.
- `first_90_day_users`
  Window: first 90 calendar days after launch.
  Rule: count unique users meeting onboarding definition.
- `mrr_4_month`
  Rule: recurring revenue run-rate at the close of month 4.
- `cac_per_paid_user`
  Numerator: attributable acquisition spend for the relevant measurement window.
  Denominator: count of paid users acquired in the same window.
- `monthly_mrr_growth_rate`
  Rule: compare current-month MRR to prior-month MRR using the standard month-over-month formula.
- `customer_retention_rate`
  Rule: cohort-based retention using the approved retention window.
- `support_response_time_hours`
  Rule: measure first-response lag for inbound support requests.

### Windows and Reporting

- launch metrics: first 30 and first 90 days after MVP launch
- recurring operating metrics: monthly
- any metric below an ML1-approved threshold for two consecutive review windows triggers escalation

### Data Sources

- application event logs and user-account records
- Stripe revenue and subscription records
- campaign and ad-platform spend and conversion exports
- email automation and onboarding records
- support and ticketing or chat records
- sampled NDA review validation set and benchmark review notes

## Baseline Capture Period

### Baseline Window

- Launch baseline start: MVP launch date
- Launch baseline end: 30 calendar days after MVP launch
- Growth baseline end: 90 calendar days after MVP launch

### Purpose

NDA Esq is a greenfield project, so there is no legacy operating baseline. The
baseline will therefore be captured from the controlled launch period and used
as the first reference point for post-launch optimization.

### Inclusion Rules

- include only real user activity tied to the approved NDA Esq product
- include only attributable acquisition spend from approved channels
- include only paid users and revenue records reconciled to the approved billing system
- include only support requests generated by live product usage

### Exclusion Rules

- exclude test users, internal QA activity, and synthetic NDA submissions
- exclude spend or traffic from unapproved channels
- exclude any manual lawyer-review work that is not part of the approved premium path

### Output

- first-30-day baseline for onboarding, AI quality, and support metrics
- first-90-day baseline for user growth and acquisition metrics
- initial monthly operating baseline for MRR growth and retention review

## Validation Review

### Review Criteria

- scope boundaries are explicit across product, acquisition, and operations workstreams
- exclusions are clear enough to prevent drafting and consultation creep
- metric formulas and denominators are reproducible from approved evidence sources
- launch and growth baseline windows are unambiguous
- threshold package is sufficient to judge MVP, acquisition, and operations success
- risk, dependency, and communication controls are strong enough for implementation authorization

### Review Owner

- ML1
- Project Owner

### Review Outcome

Status: Proposed
Notes: Planning packet drafted; implementation remains gated pending ML1 review
of thresholds and final Planning -> Executing approval.

## ML1 Metric Approval

Approval Status: Proposed

Approved By: ______________________
Date: ______________________

### Metrics Submitted for Approval

- `mvp_ready_on_or_before_target`
- `first_month_onboarded_users`
- `nda_risk_flag_accuracy_rate`
- `first_90_day_users`
- `mrr_4_month`
- `cac_per_paid_user`
- `monthly_mrr_growth_rate`
- `customer_retention_rate`
- `support_response_time_hours`

### Proposed Thresholds

| KPI | Direction | Proposed Threshold |
| --- | --- | --- |
| `mvp_ready_on_or_before_target` | Higher is better | `= 1` |
| `first_month_onboarded_users` | Higher is better | `>= 100` |
| `nda_risk_flag_accuracy_rate` | Higher is better | `>= 85%` |
| `first_90_day_users` | Higher is better | `>= 1000` |
| `mrr_4_month` | Higher is better | `>= 5000` |
| `cac_per_paid_user` | Lower is better | `< 50` |
| `monthly_mrr_growth_rate` | Higher is better | `>= 10%` |
| `customer_retention_rate` | Higher is better | `> 80%` |
| `support_response_time_hours` | Lower is better | `< 24` |

### Threshold Status

- Thresholds are proposed and not yet active until ML1 approval is recorded.
- Any budget envelope or launch-spend ceiling remains separately subject to ML1 determination before implementation.

Notes:
- This file is the canonical measurement, baseline, validation, and threshold-approval document for NDA Esq.
- Implementation must not begin until ML1 records threshold approval in this document.
