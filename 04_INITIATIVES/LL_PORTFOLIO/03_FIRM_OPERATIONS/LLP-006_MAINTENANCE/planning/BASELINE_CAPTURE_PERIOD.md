# Baseline Capture Period

Project ID: LLP-26-07
Project Path: 03_FIRM_OPERATIONS/LLP-006_MAINTENANCE
Stage: Planning

## Baseline Window
- Start: 2026-03-08
- End: 2026-03-29

## Purpose
Capture initial four-cycle operating baseline before implementation hardening decisions, so exception behavior and parity performance can be compared against post-implementation performance.

## Inclusion Rules
- Include only scheduled Sunday reconciliation cycles.
- Include only active matters in each cycle snapshot.
- Include only exceptions with source pointers and severity labels.

## Exclusion Rules
- Test/sandbox runs.
- Runs missing one or more required systems without explicit partial-run classification.
- Artifacts lacking run ID or timestamp traceability.

## Output
- Baseline metric snapshot for all KPIs in `METRIC_DEFINITION.md`.
- Baseline exception taxonomy distribution (critical/high/medium/low).
- Baseline median time-to-resolution for critical exceptions.
