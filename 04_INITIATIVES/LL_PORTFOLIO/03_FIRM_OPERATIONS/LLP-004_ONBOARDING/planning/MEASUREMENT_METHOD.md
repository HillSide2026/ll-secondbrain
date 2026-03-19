# Measurement Method

Project ID: LLP-004
Project Path: 03_FIRM_OPERATIONS/LLP-004_ONBOARDING
Stage: Planning

## Method
- Use onboarding run artifacts as primary measurement source.
- Require source evidence pointers for Gate 1 and Gate 2 transitions.
- Measure cycle timing from observed timestamps only.
- Track exception lifecycle by age and severity.
- Compute SLA using elapsed time from Gate 1 validation to agreement send event.

## Rules
- `qualified_leads` includes only records with Gate 1 validation evidence.
- `engagements_signed` requires explicit signed agreement evidence.
- `agreements_sent_within_24h` counts only records where `agreement_sent_at - gate1_at <= 24h`.
- `onboarding_cycle_time_days` includes only records with both `gate1_at` and `agreement_signed_at`.
- `open_onboarding_exceptions` includes unresolved exceptions at reporting cut-off.

## Reporting Window
- Weekly trailing 7 days.
- Monthly rollup for trend analysis.
