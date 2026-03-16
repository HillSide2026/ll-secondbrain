# Doctrine Drift Report

- Generated: 2026-03-16T18:00:00Z
- Agent: LLM-006 Portfolio Governance Agent (via LLM-001 Chief of Staff)

> Advisory output. ML1 approval required before any action is taken.

## Systemic Patterns

Two distinct drift patterns are present across the portfolio. The first is structural (split measurement schema replacing canonical METRICS.md). The second is behavioral (execution proceeding ahead of gate authorization in at least two projects).

## Measurement Schema Drift

| Artifact | Missing In N Projects | Implication |
|----------|-----------------------|-------------|
| METRICS.md (canonical) | 4 of 5 Stage 2 projects | Split schema has become the de facto standard despite doctrine requiring single artifact |
| ML1 threshold approval (signed) | 4 of 5 Stage 2 projects | Metric architecture exists but no project has completed ML1 sign-off |

The split schema (METRIC_DEFINITION.md + MEASUREMENT_METHOD.md + BASELINE_CAPTURE_PERIOD.md + VALIDATION_REVIEW.md) appears to have been systematically pre-loaded into Stage 1 projects that have not yet reached Planning, including LLP-001 through LLP-004_PARTNER_SUPERVISION and 09_SERVICE_MANAGEMENT sub-projects. This means the non-canonical pattern is propagating forward into projects before they reach the stage that requires measurement architecture. If left uncorrected, every future project will arrive at Stage 2 with a non-compliant schema already in place.

## Planning Drift

| Artifact | Missing In N Projects | Implication |
|----------|-----------------------|-------------|
| SCOPE_DEFINITION.md | 1 (LLP-013 — not yet drafted) | Not yet systemic; LLP-013 authorized Planning 2026-03-15 |
| WORKPLAN.md | 1 (LLP-013 — not yet drafted) | Same |

No systemic planning artifact drift beyond LLP-013's as-yet-unstarted Planning stage.

## Non-Standard Artifact Names Detected

- `IMPLEMENTATION_SPEC.md` — present in LLP-023 (non-canonical Stage 2 substitute)
- `MILESTONE_PLAN.md` — present in LLP-023 (non-canonical Stage 2 substitute)
- `METRIC_DEFINITION.md`, `MEASUREMENT_METHOD.md`, `BASELINE_CAPTURE_PERIOD.md`, `VALIDATION_REVIEW.md` — present across 5+ projects as split-schema substitutes for canonical `METRICS.md`

## Assessment

The dominant drift is the systematic replacement of `METRICS.md` with a four-file split schema across all planning-stage projects. This is not a project-level error — it is a template-level propagation failure. Whatever template or agent produced the initial Stage 2 planning artifact sets for LLP-004, LLP-005, LLP-011, and LLP-013 used the split schema, and that schema has now been pre-loaded into Stage 1 projects that haven't yet reached Planning. This is a systemic issue requiring a doctrine clarification communication and a template correction before further Stage 2 projects are initiated. The behavioral drift in LLP-006 (Stage 3 artifacts with no authorization) is the most urgent signal: it suggests execution is occurring outside the gate framework, which is the core risk the doctrine exists to prevent.

## Rule

Doctrine interpretation remains ML1 authority.
