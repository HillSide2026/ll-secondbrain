---
title: Doctrine Drift Report
generated: 2026-03-18T00:00:00Z
agent: LLM-006 Portfolio Governance Agent
---

# Doctrine Drift Report

- Generated: 2026-03-18T00:00:00Z
- Agent: LLM-006 Portfolio Governance Agent

> Advisory output. ML1 approval required before any action is taken.

---

## Systemic Patterns

Three distinct drift patterns are present across the portfolio as of this audit.

**Pattern 1 — Split measurement schema propagation.** The deprecated split-schema (METRIC_DEFINITION.md + MEASUREMENT_METHOD.md + BASELINE_CAPTURE_PERIOD.md + VALIDATION_REVIEW.md) has been used instead of the canonical METRICS.md in three Planning+ projects and has been pre-loaded into at least twelve Stage 1 projects that have not yet reached Planning. This is a template-level propagation failure, not a project-level error.

**Pattern 2 — Substantively empty projects advancing through the system.** A cluster of at least nine projects have PROJECT_CHARTER.md files with entirely placeholder content ("To be defined by ML1."), APPROVAL_RECORD.md files with blank signature fields, and split-schema measurement artifacts pre-loaded before any substantive work has been done. These projects are structurally hollow but carry the same governance footprint as substantive projects, creating noise in portfolio oversight.

**Pattern 3 — Charter field inconsistency.** Several projects are missing standard charter fields (Project Type, Stage) in machine-readable format, and at least one project (LLP-012) has a charter stage field that was not updated after an ML1-approved stage gate advancement.

---

## Measurement Drift

| Artifact | Missing in N Projects | Implication |
|----------|-----------------------|-------------|
| METRICS.md (canonical) | 4 of 8 Stage 2+ projects | Split schema has become the de facto template despite doctrine requiring the single canonical artifact |
| ML1 threshold approval (signed within METRICS.md) | 2 of 8 Stage 2+ projects | Approval record and artifact content are inconsistent for LLP-024; LLP-025 pending |
| METRIC_DEFINITION.md (non-canonical) | 12+ projects | Split schema pre-loaded into Stage 1 projects before Planning stage reached |
| MEASUREMENT_METHOD.md (non-canonical) | 12+ projects | Same |
| BASELINE_CAPTURE_PERIOD.md (non-canonical) | 12+ projects | Same |
| VALIDATION_REVIEW.md (non-canonical) | 12+ projects | Same |

---

## Planning Drift

| Artifact | Missing in N Projects | Implication |
|----------|-----------------------|-------------|
| WORKPLAN.md | 2 (LLP-012, LLP-013) | Both are Planning-stage projects; Stage 2 artifacts absent or not present on disk |
| SCOPE_DEFINITION.md | 2 (LLP-012, LLP-013) | Same |
| ASSUMPTIONS_CONSTRAINTS.md | 2 (LLP-012, LLP-013) | Same |
| DEPENDENCIES.md | 2 (LLP-012, LLP-013) | Same |
| RISK_REGISTER.md | 2 (LLP-012, LLP-013) | Same |
| COMMUNICATION_PLAN.md | 2 (LLP-012, LLP-013) | Same |
| BUSINESS_CASE.md | 4 Strategic Projects (LLP-001, LLP-002, LLP-003, LLP-004_PARTNER_SUPERVISION, LLP-023) | Required for Strategic Project type at Stage 1; systematically absent |

---

## Non-Standard Artifact Names Detected

- `IMPLEMENTATION_SPEC.md` — present in LLP-023_MATTER_COMMAND_CONTROL. Non-canonical Stage 2/3 substitute.
- `MILESTONE_PLAN.md` — present in LLP-023_MATTER_COMMAND_CONTROL. Non-canonical substitute for WORKPLAN.md.
- `METRIC_FRAMEWORK.md` — present in LLP-025_MARKETING_STRATEGY. Non-canonical name for what should be content within METRICS.md.
- `METRIC_DEFINITION.md`, `MEASUREMENT_METHOD.md`, `BASELINE_CAPTURE_PERIOD.md`, `VALIDATION_REVIEW.md` — present across 15+ project folders as split-schema substitutes for canonical METRICS.md. Deprecated per PROJECT_POLICY.md §8.
- `RISKS_INITIAL.md` — present in LLP-024_NDA_ESQ. Used as a legacy initiating-stage risk artifact before RISK_SCAN.md was adopted; RISK_SCAN.md was later added to align with policy. Both files present simultaneously.
- `TIER1_SOLUTIONS_SUBSTANCE_REVIEW.md`, `FIRST_RUN_CORPORATE_SOLUTIONS_ARTIFACT_OPINION.md` — present in LLP-001_CORPORATE_ENTITY_MANAGEMENT. Non-standard research artifacts; no canonical equivalent but not in conflict with required artifacts.

---

## Structural Charter Gaps

| Issue | Projects Affected |
|-------|-------------------|
| "Project Type:" field absent or non-standard in charter | LLP-025_MARKETING_STRATEGY, LLP-030_FIRM_STRATEGY |
| "Stage:" field not updated after approved gate advancement | LLP-012_FUNNEL2_MANAGEMENT |
| Charter body entirely placeholder ("To be defined by ML1.") | PORTFOLIO_MANAGEMENT, 09_SERVICE_MANAGEMENT (×5), LLP-017_STRATEGIC_RISK, LLP-009_CLERK_SUPERVISION, LLP-010_ASSOCIATE_SUPERVISION (9 projects total) |

---

## Assessment

The dominant drift is the systematic propagation of the deprecated four-file split measurement schema into both Planning-stage and pre-Planning projects. This is not a project-level error — it is a template-level failure. Whatever template was used to scaffold Stage 1 and Stage 2 projects continues to install the non-canonical split schema, meaning every new project arrives at Stage 2 already non-compliant. The policy (PROJECT_POLICY.md §8) is unambiguous: METRICS.md is the single canonical measurement artifact and the split schema must be consolidated before Planning→Executing gate closure. New projects must not use the split schema at all. Until the template source is corrected, this drift will continue to accumulate with every project scaffold.

The second concern is the cluster of nine structurally hollow projects — projects with placeholder charters, unsigned approvals, and pre-loaded split-schema measurement files. These projects occupy governance bandwidth and create a misleading picture of portfolio breadth without representing actual work commitments. A batch decision from ML1 (approve with substantive content, or formally park) would clean up this pattern.

The third concern is a behavioral pattern: APPROVAL_RECORD.md artifact lists are being written to reference artifacts that do not yet exist on disk (LLP-013), and charter stage fields are not being updated after gate advancements (LLP-012). Both suggest that artifact records are being populated ahead of actual artifact creation — a documentation discipline gap that erodes the reliability of the approval trail.

---

## Rule

Doctrine interpretation remains ML1 authority.
