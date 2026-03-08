---
id: 04_initiatives__ll_portfolio__03_firm_operations__project_management__project_artifact_template_md
title: Project Artifact Template
owner: ML1
status: draft
created_date: 2026-03-08
last_updated: 2026-03-08
tags: [project-management, stage-gates, artifacts, template]
---

# Project Artifact Template

## Purpose

Define the canonical artifact set required per project stage.

Planning-stage artifacts are implementation-readiness controls used to authorize execution and achievement of project goals.

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

Required:
- `PROJECT_CHARTER.md`
- `PROBLEM_STATEMENT.md`
- `SUCCESS_CRITERIA.md`
- `STAKEHOLDERS.md`
- `RISK_SCAN.md`
- `APPROVAL_RECORD.md`

Notes:
- `RISK_SCAN.md` must include: Top 5 Risks, Key Assumptions, Go/No-Go Judgment.
- `PROJECT_CHARTER.md` must include:
  - `Project #` (canonical LL project number, e.g., `LLP-26-24`)
  - `Project Type` (`Strategic`, `Management`, or `Operational`)
- Stage advancement requires ML1 approval in `APPROVAL_RECORD.md`.

## Stage 2 - Planning (Implementation Readiness)

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
- `METRIC_DEFINITION.md`
- `MEASUREMENT_METHOD.md`
- `BASELINE_CAPTURE_PERIOD.md`
- `VALIDATION_REVIEW.md`
- `ML1_METRIC_APPROVAL.md`

Notes:
- Stage 2 exists to prepare controlled implementation, not to create standalone planning artifacts.
- Implementation must not begin until ML1 approves Planning -> Implementation in `APPROVAL_RECORD.md` and metric thresholds in `ML1_METRIC_APPROVAL.md`.

## Stage 3 - Implementation

Required:
- `EXECUTION_LOG.md`
- `DECISION_LOG.md`
- `CHANGE_LOG.md`
- `ISSUE_LOG.md`
- `DELIVERABLES_TRACKER.md`
- `QA_CHECKLIST.md`

Notes:
- `ISSUE_LOG.md` tracks materialized risks and corrective actions.

## Stage 4 - Monitoring

Required:
- `STATUS_REPORT.md`
- `KPI_DASHBOARD.md`
- `VARIANCE_REPORT.md`
- `RISK_UPDATES.md`
- `STAKEHOLDER_UPDATES.md`

## Stage 5 - Closing

Required:
- `DELIVERABLE_ACCEPTANCE.md`
- `LESSONS_LEARNED.md`
- `POST_IMPLEMENTATION_REVIEW.md`
- `FINAL_STATUS_REPORT.md`
- `ARCHIVE_INDEX.md`

## Stage-Gate Rule

No stage advancement is valid without explicit ML1 approval recorded in project artifacts.
