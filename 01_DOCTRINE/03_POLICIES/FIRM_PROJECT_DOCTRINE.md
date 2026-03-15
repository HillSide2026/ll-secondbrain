---
id: 01_doctrine__02_policies__firm_project_doctrine_md
title: Firm Project Doctrine
owner: ML1
status: draft
version: '1.0'
created_date: 2026-03-14
last_updated: 2026-03-14
tags: [doctrine, policy, projects, stage-gates]
---

# Firm Project Doctrine

## 1. Purpose

This doctrine is the canonical policy source for governed project stages,
stage-gate rules, and required project artifacts.

Its purpose is to eliminate persistent drift between templates, agent specs,
project packets, and portfolio summaries.

## 2. Scope

This doctrine applies directly to Levine Law strategic, management, and
operational projects.

It may also be adopted by other repo-governed project systems, including
HillSide project packets, unless a portfolio-specific doctrine explicitly
overrides it.

This doctrine does not apply to legal matter stages, which are governed by
matter doctrine.

## 3. Canonical Delivery Stages

The canonical project delivery stages are:

1. `Initiating`
2. `Planning`
3. `Executing`
4. `Closing`

Rules:

- `Monitoring` is not a separate project stage.
- Monitoring and reporting artifacts belong inside `Executing`.
- `Implementation` is a deprecated stage label and must not be used as the
  canonical stage name going forward.
- Historical references to `Implementation` or `Monitoring` should be treated
  as legacy until migrated.

## 4. Decision Lifecycle Is Separate

Delivery stages must not be confused with register-level decision tracking.

Where needed, a separate decision lifecycle may be used for project register
management, for example:

- `idea`
- `screening`
- `validating`
- `modeling`
- `deciding`
- `approved`
- `rejected`

Decision lifecycles do not replace delivery stages.

## 5. Stage-Gate Authority

No project stage advancement is valid without explicit ML1 approval recorded in
project artifacts.

Required gate sequence:

- `Initiating -> Planning`
- `Planning -> Executing`
- `Executing -> Closing`

ML2 may draft artifacts, structure options, and prepare packets.
ML1 alone decides stage advancement.

## 6. Canonical Artifact Set

### Stage 1 - Initiating

Required:

- `PROJECT_CHARTER.md`
- `PROBLEM_STATEMENT.md`
- `SUCCESS_CRITERIA.md`
- `STAKEHOLDERS.md`
- `RISK_SCAN.md`
- `APPROVAL_RECORD.md`

### Stage 2 - Planning

Required:

- `SCOPE_DEFINITION.md`
- `WORKPLAN.md`
- `ASSUMPTIONS_CONSTRAINTS.md`
- `DEPENDENCIES.md`
- `RISK_REGISTER.md`
- `COMMUNICATION_PLAN.md`
- `METRICS.md`

### Stage 3 - Executing

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

### Stage 4 - Closing

Required:

- `DELIVERABLE_ACCEPTANCE.md`
- `LESSONS_LEARNED.md`
- `POST_EXECUTION_REVIEW.md`
- `FINAL_STATUS_REPORT.md`
- `ARCHIVE_INDEX.md`

## 7. Planning Discipline

Planning exists to support execution readiness, not planning for planning's
sake.

Rules:

- Planning artifacts must be project-specific.
- Planning artifacts must help lock scope, dependencies, controls, or gate
  readiness.
- Abstract or duplicative planning artifacts should be merged or removed.
- `METRICS.md` is the single canonical measurement artifact.

## 8. Drift Control

This doctrine overrides conflicting project-stage language in:

- templates
- agent specifications
- project README files
- portfolio summaries
- project packet placeholders

If any lower-level project-governance artifact conflicts with this doctrine,
this doctrine governs.

## 9. Related Artifacts

- `04_INITIATIVES/LL_PORTFOLIO/03_FIRM_OPERATIONS/PROJECT_MANAGEMENT/PROJECT_ARTIFACT_TEMPLATE.md`
- `00_SYSTEM/AGENTS/LLM-004_PROJECT_MANAGEMENT_AGENT.md`
- `01_DOCTRINE/03_POLICIES/DOCTRINE-RISK-0002-project-risk-artifact-lifecycle-policy.md`
