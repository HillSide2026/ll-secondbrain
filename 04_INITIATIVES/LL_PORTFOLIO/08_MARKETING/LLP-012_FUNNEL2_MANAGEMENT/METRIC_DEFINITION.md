# Metric Definition

Project #: LLP-26-25
Repo: 08_MARKETING/LLP-012_FUNNEL2_MANAGEMENT
Stage: Planning

## Intake-Stage Metrics (ML1 Targets)

| Process | Step | SLA | KPI | Target |
| --- | --- | --- | --- | --- |
| 3.3 Intake | Welcoming | Call out within 24 hours of opt-in | Leads worked within 24 hours | `>= 90%` |
| 3.4 Intake | Scheduling | N/A | Leads scheduled | `>= 30%` |

## Onboarding / Conversion Stage Metrics (ML1 Targets)

| Process | Step | SLA | KPI | Target |
| --- | --- | --- | --- | --- |
| 3.5 Onboarding | Consulting | N/A | Consulting stage tracking | Instrumentation required |
| 3.6 Onboarding | Closing (aka Engaging / Conversion) | N/A | Paid lead to engaged conversion | `>= 1/10` paid leads (`>= 10%`) |

## Metric Definitions
- `leads_worked_within_24h_rate`
  Formula: `(count of opt-in leads with first outbound call/contact <= 24h) / (count of opt-in leads)` x 100
- `leads_scheduled_rate`
  Formula: `(count of opt-in leads with consult/meeting scheduled) / (count of opt-in leads)` x 100
- `paid_lead_to_engaged_conversion_rate`
  Formula: `(count of paid leads that reach closing/engaged conversion) / (count of paid leads)` x 100

## Measurement Cadence
- Weekly operational review
- Monthly governance summary

## Scope Notes
- Intake-stage metrics apply to pre-conversion funnel behavior.
- Intake aliases to `inquiry` in canonical lifecycle normalization.

## Notes
- Intake targets above were provided by ML1.
- Onboarding conversion target above was provided by ML1.
- Consulting-stage KPI target is currently instrumentation-only until ML1 sets a numeric threshold.
