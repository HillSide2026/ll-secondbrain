# Measurement Method

Project #: LLP-26-25
Repo: 08_MARKETING/LLP-012_FUNNEL2_MANAGEMENT
Stage: Planning

## Method
- Capture intake-stage events and onboarding-stage events from governed funnel artifacts.
- Normalize stage aliases: `intake -> inquiry`, `onboarding -> conversion` in canonical fields while preserving operational labels for reporting.
- Record stage transitions with timestamped evidence references.
- Measure against ML1-approved thresholds when provided.

## Intake KPI Calculation Rules
- `leads_worked_within_24h_rate`
  Numerator: count of opt-in leads with first outbound call/contact timestamp within 24 hours of opt-in timestamp.
  Denominator: count of opt-in leads in the measurement window.
  Target: `>= 90%`.
- `leads_scheduled_rate`
  Numerator: count of opt-in leads with scheduled consult/meeting event.
  Denominator: count of opt-in leads in the measurement window.
  Target: `>= 30%`.

## Onboarding / Conversion KPI Calculation Rules
- `consulting_stage_tracking`
  Requirement: consulting-stage events must be captured for onboarding leads.
  Target: instrumentation complete and reportable.
- `paid_lead_to_engaged_conversion_rate`
  Numerator: count of paid leads that reach closing/engaged conversion.
  Denominator: count of paid leads in the measurement window.
  Target: `>= 1/10` paid leads (`>= 10%`).

## Window and Reporting
- Default window: rolling 7 days for operational management.
- Governance rollup: monthly.
- Any metric below target for 2 consecutive weekly windows requires escalation review.

## Data Sources (If Any)
- Website and landing-page conversion instrumentation (`levine-law.ca`)
- Funnel intake forms / booking events
- Onboarding evidence artifacts (engagement signed, retainer received, or invoice paid)
- Governed run artifacts and signal reports
