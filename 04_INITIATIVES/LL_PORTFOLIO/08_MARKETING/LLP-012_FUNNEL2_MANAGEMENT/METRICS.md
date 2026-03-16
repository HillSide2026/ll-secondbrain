# Metrics

Project ID: LLP-26-25
Project Path: 08_MARKETING/LLP-012_FUNNEL2_MANAGEMENT
Stage: Planning

Approval Status: Pending — metric framework drafted; ML1 threshold approval required before Planning → Executing gate.

---

## KPI Definitions

### Intake Stage

| KPI | Process Step | SLA | Formula | Target |
| --- | --- | --- | --- | --- |
| `leads_worked_within_24h_rate` | 3.3 Intake — Welcoming | Call out within 24h of opt-in | `(opt-in leads with first contact ≤ 24h) / (opt-in leads) × 100` | `≥ 90%` |
| `leads_scheduled_rate` | 3.4 Intake — Scheduling | N/A | `(opt-in leads with consult scheduled) / (opt-in leads) × 100` | `≥ 30%` |

### Conversion Stage

| KPI | Process Step | SLA | Formula | Target |
| --- | --- | --- | --- | --- |
| `consulting_stage_tracking` | 3.5 Conversion — Consulting | N/A | Instrumentation complete and reportable | Instrumentation required |
| `paid_lead_to_engaged_conversion_rate` | 3.6 Conversion — Closing/Engaging | N/A | `(paid leads reaching closing/engaged) / (paid leads) × 100` | `≥ 10%` |

Intake targets and conversion target provided by ML1.
`consulting_stage_tracking` is instrumentation-only until ML1 sets a numeric threshold.

## Measurement Method

- Capture intake-stage and conversion-stage events from governed funnel artifacts.
- Normalize stage aliases: `intake → inquiry`. Treat `conversion` as canonical marketing terminal stage; `onboarding` as downstream fulfillment handoff label.
- Record stage transitions with timestamped evidence references.
- Measure against ML1-approved thresholds.

### Calculation Rules
- `leads_worked_within_24h_rate`: numerator = opt-in leads with first outbound call/contact timestamp ≤ 24h of opt-in; denominator = opt-in leads in window.
- `leads_scheduled_rate`: numerator = opt-in leads with scheduled consult/meeting event; denominator = opt-in leads in window.
- `consulting_stage_tracking`: consulting-stage events must be captured for conversion-qualified leads and handoff records.
- `paid_lead_to_engaged_conversion_rate`: numerator = paid leads reaching closing/engaged conversion; denominator = paid leads in window.

### Window and Reporting
- Default window: rolling 7 days for operational management.
- Governance rollup: monthly.
- Any metric below target for 2 consecutive weekly windows requires escalation review.

### Data Sources
- Website and landing-page conversion instrumentation (`levine-law.ca`)
- Funnel intake forms / booking events
- Conversion evidence artifacts (engagement signed, retainer received, or invoice paid), with handoff reference to fulfillment onboarding
- Governed run artifacts and signal reports

## Baseline Capture Period

Status: To Be Defined
Notes: Baseline window has not been established. Must be defined before Planning → Executing gate.

## Validation

Status: To Be Defined
Notes: Pending ML1 metric approval and baseline window definition before gate review.
