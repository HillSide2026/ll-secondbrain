---
id: 04_initiatives__ll_portfolio__03_firm_operations__project_management__project_artifact_template_md
title: Project Artifact Template
owner: ML1
status: draft
created_date: 2026-03-08
last_updated: 2026-03-14
tags: [project-management, stage-gates, artifacts, template]
---

# Project Artifact Template

## Purpose

Define the canonical artifact set required per project stage.

This template is subordinate to
`01_DOCTRINE/03_POLICIES/FIRM_PROJECT_POLICY.md`.

Planning-stage artifacts are execution-readiness controls used to authorize execution and achievement of project goals.

## Project Types

This template acknowledges four project/work types used in LL:
- Strategic projects
- Management projects
- Operational projects
- Client matters (aka client projects)

Applicability:
- The staged project artifact lifecycle in this template applies to strategic, management, and operational projects.
- Client matters/client projects are governed by matter doctrine and matter-stage artifacts, not this project-stage lifecycle template.

## Stage 1 - Initiating

Required (all projects):
- `PROJECT_CHARTER.md`
- `PROBLEM_STATEMENT.md`
- `SUCCESS_CRITERIA.md`
- `STAKEHOLDERS.md`
- `RISK_SCAN.md`
- `APPROVAL_RECORD.md`

Required (strategic projects only):
- `BUSINESS_CASE.md`

Notes:
- `RISK_SCAN.md` must include: Top 5 Risks, Key Assumptions, Go/No-Go Judgment.
- `PROJECT_CHARTER.md` must include:
  - `Project ID` (canonical globally unique identifier, e.g., `LLP-26-24`)
  - `Project Path` (repository path key, e.g., `08_MARKETING/LLP-011_FUNNEL1_MANAGEMENT`)
  - `Project Type` (`Strategic`, `Management`, or `Operational`)
- Stage advancement requires ML1 approval in `APPROVAL_RECORD.md`.

Identity Rule:
- `Project ID` is canonical.
- Legacy folder labels (for example `LLP-004_ONBOARDING`) are location slugs only and are not valid identity fields.

## Stage 2 - Planning (Execution Readiness)

Purpose:
- Lock the execution-ready shape of the specific project.
- Reduce uncertainty before execution.
- Prepare a clean ML1 gate decision.

Anti-Bloat Rule:
- Planning artifacts exist to support execution authorization, not planning for the sake of planning.
- If an artifact does not help lock scope, confirm dependencies, reduce risk, define controls, or support the gate decision, merge it or remove it.
- Planning artifacts must use project-specific language. Avoid generic PM boilerplate that could apply to any project.

### Core Planning
Required:
- `SCOPE_DEFINITION.md`
- `WORKPLAN.md` (must include workstreams, execution sequence, milestones, resource plan, completion condition)
- `ASSUMPTIONS_CONSTRAINTS.md`
- `DEPENDENCIES.md`
- `RISK_REGISTER.md`
- `COMMUNICATION_PLAN.md`

### Measurement Architecture
Required:
- `METRICS.md`

Notes:
- Stage 2 exists to prepare controlled execution, not to create standalone planning artifacts.
- `METRICS.md` is the single canonical measurement document and must contain metric definitions, measurement method, baseline capture period, validation review, and ML1 threshold approval.
- Executing must not begin until ML1 approves Planning -> Executing in `APPROVAL_RECORD.md` and threshold approval is recorded in `METRICS.md`.
 - `METRICS.md` is the single canonical measurement document and must contain metric definitions, measurement method, baseline capture period, validation review, and ML1 threshold approval.
 - Executing must not begin until ML1 approves Planning -> Executing in `APPROVAL_RECORD.md` and threshold approval is recorded in `METRICS.md`.

Best-Practice Rules:
- `SCOPE_DEFINITION.md`
  Must define the real execution boundary for the project, including explicit exclusions.
- `WORKPLAN.md`
  Must focus on the project decisions that still need to be locked for execution. It must not become a generic project-management report.
- `ASSUMPTIONS_CONSTRAINTS.md`
  Must state the assumptions the project is relying on and the hard limits it cannot cross.
- `DEPENDENCIES.md`
  Must list only dependencies that could block or materially change execution.
- `RISK_REGISTER.md`
  Must focus on risks that threaten scope, schedule, budget, operating control, or authorization readiness.
- `COMMUNICATION_PLAN.md`
  Must be limited to decision loops, coordination points, and escalation triggers that the project actually needs.
- `METRICS.md`
  Must be the single source for metric definitions, calculation method, baseline logic, validation rules, and ML1 threshold approval.
## Stage 3 - Executing

Required:
- `EXECUTION_LOG.md`
- `DECISION_LOG.md`
- `CHANGE_LOG.md`
- `ISSUE_LOG.md`
- `DELIVERABLES_TRACKER.md`
- `QA_CHECKLIST.md`
- `STATUS_REPORT.md`
- `KPI_DASHBOARD.md`
- `VARIANCE_REPORT.md`
- `RISK_UPDATES.md`
- `STAKEHOLDER_UPDATES.md`

Notes:
- `ISSUE_LOG.md` tracks materialized risks and corrective actions.
- Executing includes active implementation plus increased monitoring while the work is live.

## Stage 4 - Closing

Required:
- `DELIVERABLE_ACCEPTANCE.md`
- `LESSONS_LEARNED.md`
- `POST_EXECUTION_REVIEW.md`
- `FINAL_STATUS_REPORT.md`
- `ARCHIVE_INDEX.md`

## Stage-Gate Rule

No stage advancement is valid without explicit ML1 approval recorded in project artifacts.
