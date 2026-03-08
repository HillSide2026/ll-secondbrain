# Metric Definition

Project #: LLP-26-24
Repo: 08_MARKETING/LLP-011_FUNNEL1_MANAGEMENT
Stage: Planning

## Funnel 01 Core Metrics

| KPI | Definition | Formula |
| --- | --- | --- |
| `cost_per_qualified_lead` | Average paid acquisition cost per lead | `ad_spend / leads` |
| `lead_to_booked_rate` | Share of captured leads that progress to booked consult | `(booked / lead_captured) * 100` |
| `lead_to_retained_rate` | Share of captured leads that become retained | `(retained / lead) * 100` |
| `consult_show_rate` | Share of booked consults completed | `(consult_complete / booked) * 100` |
| `consult_to_retained_rate` | Share of completed consults that become retained | `(retained / consult_complete) * 100` |

## Goal Alignment
- `cost_per_qualified_lead` supports acquisition efficiency goal.
- `lead_to_booked_rate` and `consult_show_rate` support execution-throughput goal.
- `lead_to_retained_rate` and `consult_to_retained_rate` support conversion achievement goal.

## Stage Mapping
- Canonical progression: `lead_captured -> screened -> booked -> consult_complete -> retained`
- Formula token `lead` corresponds to count of `lead_captured` events in the measurement window.
- Lifecycle normalization alignment: `inquiry (intake)` and `conversion (onboarding)` references are preserved for reporting labels when required.

## Target Status
- Target thresholds are `TBD` pending ML1 metric approval for Planning -> Implementation gate authorization.

## Measurement Cadence
- Weekly operational review
- Monthly governance summary
